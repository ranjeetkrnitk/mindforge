#!/usr/bin/env python3
"""
Extract Copilot CLI usage metrics from session store and logs.
Usage: python3 copilot_usage.py [--json]
"""

import sqlite3
import json
import sys
import re
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Session store location
SESSION_STORE = Path.home() / ".copilot" / "session-store.db"
LOGS_DIR = Path.home() / ".copilot" / "logs"
SESSION_STATE_DIR = Path.home() / ".copilot" / "session-state"


def extract_token_usage_from_logs():
    """Extract token usage statistics from Copilot log files."""
    usage = {
        'tokens_today': 0,
        'tokens_week': 0,
        'compactions_today': 0,
        'compactions_week': 0,
        'tokens_saved_today': 0,
        'tokens_saved_week': 0,
        'current_utilization': 0,
        'context_limit': 168000,
        'daily_tokens': [],
        'daily_activity': {}  # For heatmap: {date: {sessions, turns, tokens, saved}}
    }
    
    if not LOGS_DIR.exists():
        return usage
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    two_months_ago = today - timedelta(days=62)  # ~2 months for heatmap
    
    # Token usage pattern from CompactionProcessor
    token_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}).*Utilization (\d+\.?\d*)% \((\d+)/(\d+) tokens\)')
    compaction_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}).*Compaction complete.*saved ~(\d+) tokens')
    
    daily_max_tokens = defaultdict(int)
    daily_saved = defaultdict(int)
    daily_compactions = defaultdict(int)
    
    # Parse all log files for heatmap data
    log_files = sorted(LOGS_DIR.glob("process-*.log"), key=lambda x: x.stat().st_mtime, reverse=True)[:30]
    
    for log_file in log_files:
        try:
            content = log_file.read_text(errors='ignore')
            
            # Extract token utilization
            for match in token_pattern.finditer(content):
                date_str = match.group(1)
                log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                tokens = int(match.group(3))
                limit = int(match.group(4))
                
                # Track max tokens per day
                if tokens > daily_max_tokens[date_str]:
                    daily_max_tokens[date_str] = tokens
                
                if log_date == today:
                    usage['current_utilization'] = float(match.group(2))
                    usage['context_limit'] = limit
            
            # Extract compaction savings
            for match in compaction_pattern.finditer(content):
                date_str = match.group(1)
                log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                saved = int(match.group(2))
                
                daily_saved[date_str] += saved
                daily_compactions[date_str] += 1
                
                if log_date == today:
                    usage['compactions_today'] += 1
                    usage['tokens_saved_today'] += saved
                if log_date >= week_ago:
                    usage['compactions_week'] += 1
                    usage['tokens_saved_week'] += saved
                    
        except Exception:
            continue
    
    # Calculate totals from daily max tokens
    for date_str, tokens in daily_max_tokens.items():
        log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if log_date == today:
            usage['tokens_today'] = tokens
        if log_date >= week_ago:
            usage['tokens_week'] += tokens
            usage['daily_tokens'].append({'day': date_str, 'tokens': tokens})
        
        # Build activity data for heatmap
        if log_date >= two_months_ago:
            usage['daily_activity'][date_str] = {
                'tokens': tokens,
                'saved': daily_saved.get(date_str, 0),
                'compactions': daily_compactions.get(date_str, 0)
            }
    
    # Sort daily tokens
    usage['daily_tokens'].sort(key=lambda x: x['day'])
    
    return usage


def get_usage_metrics():
    """Extract usage metrics from session store."""
    if not SESSION_STORE.exists():
        return None
    
    conn = sqlite3.connect(SESSION_STORE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    metrics = {}
    
    # Total sessions (all time)
    cur.execute("SELECT COUNT(*) as count FROM sessions")
    metrics['total_sessions'] = cur.fetchone()['count']
    
    # Sessions this week
    cur.execute("""
        SELECT COUNT(*) as count FROM sessions 
        WHERE created_at >= date('now', '-7 days')
    """)
    metrics['sessions_this_week'] = cur.fetchone()['count']
    
    # Sessions today
    cur.execute("""
        SELECT COUNT(*) as count FROM sessions 
        WHERE date(created_at) = date('now')
    """)
    metrics['sessions_today'] = cur.fetchone()['count']
    
    # Total turns (conversations) this week
    cur.execute("""
        SELECT COUNT(*) as count FROM turns 
        WHERE timestamp >= date('now', '-7 days')
    """)
    metrics['turns_this_week'] = cur.fetchone()['count']
    
    # Turns today
    cur.execute("""
        SELECT COUNT(*) as count FROM turns 
        WHERE date(timestamp) = date('now')
    """)
    metrics['turns_today'] = cur.fetchone()['count']
    
    # Unique projects this week
    cur.execute("""
        SELECT COUNT(DISTINCT cwd) as count FROM sessions 
        WHERE created_at >= date('now', '-7 days')
    """)
    metrics['projects_this_week'] = cur.fetchone()['count']
    
    # Sessions by day (last 7 days)
    cur.execute("""
        SELECT date(created_at) as day, COUNT(*) as count
        FROM sessions
        WHERE created_at >= date('now', '-7 days')
        GROUP BY date(created_at)
        ORDER BY day
    """)
    metrics['daily_sessions'] = [dict(r) for r in cur.fetchall()]
    
    # Turns by day (last 7 days)
    cur.execute("""
        SELECT date(timestamp) as day, COUNT(*) as count
        FROM turns
        WHERE timestamp >= date('now', '-7 days')
        GROUP BY date(timestamp)
        ORDER BY day
    """)
    metrics['daily_turns'] = [dict(r) for r in cur.fetchall()]
    
    # Top projects this week
    cur.execute("""
        SELECT 
            cwd,
            COUNT(*) as sessions
        FROM sessions
        WHERE created_at >= date('now', '-7 days')
        GROUP BY cwd
        ORDER BY sessions DESC
        LIMIT 10
    """)
    raw_projects = [dict(r) for r in cur.fetchall()]
    
    # Process project names in Python and aggregate by normalized name
    project_counts = {}
    for p in raw_projects:
        cwd = p['cwd'] or ''
        if '/repos/' in cwd:
            # Extract first folder after /repos/
            parts = cwd.split('/repos/', 1)
            if len(parts) > 1:
                name = parts[1].split('/')[0]
            else:
                name = cwd.split('/')[-1]
        elif 'Obsidian_Claude' in cwd:
            name = 'Obsidian_Claude'
        elif cwd == '/Users/rkuma05' or cwd.endswith('/rkuma05'):
            name = '~/ (home)'
        else:
            name = cwd.split('/')[-1] if cwd else 'unknown'
        project_counts[name] = project_counts.get(name, 0) + p['sessions']
    
    # Sort by count and take top 5
    metrics['top_projects'] = [
        {'project': k, 'sessions': v}
        for k, v in sorted(project_counts.items(), key=lambda x: -x[1])[:5]
    ]
    
    # Recent sessions with summaries
    cur.execute("""
        SELECT 
            id,
            cwd,
            summary,
            created_at
        FROM sessions
        WHERE summary IS NOT NULL
        ORDER BY created_at DESC
        LIMIT 5
    """)
    raw_recent = [dict(r) for r in cur.fetchall()]
    
    # Process recent session projects in Python
    recent_sessions = []
    for s in raw_recent:
        cwd = s['cwd'] or ''
        if '/repos/' in cwd:
            parts = cwd.split('/repos/', 1)
            name = parts[1].split('/')[0] if len(parts) > 1 else cwd.split('/')[-1]
        elif 'Obsidian_Claude' in cwd:
            name = 'Obsidian_Claude'
        else:
            name = cwd.split('/')[-1] if cwd else 'unknown'
        recent_sessions.append({
            'id': s['id'],
            'project': name,
            'summary': s['summary'],
            'created_at': s['created_at']
        })
    metrics['recent_sessions'] = recent_sessions
    
    # Files edited this week
    cur.execute("""
        SELECT COUNT(DISTINCT file_path) as count
        FROM session_files
        WHERE tool_name = 'edit' 
        AND first_seen_at >= date('now', '-7 days')
    """)
    metrics['files_edited_week'] = cur.fetchone()['count']
    
    # Average turns per session this week
    cur.execute("""
        SELECT 
            CAST(COUNT(t.turn_index) AS FLOAT) / MAX(1, COUNT(DISTINCT t.session_id)) as avg
        FROM turns t
        JOIN sessions s ON t.session_id = s.id
        WHERE s.created_at >= date('now', '-7 days')
    """)
    result = cur.fetchone()
    metrics['avg_turns_per_session'] = round(result['avg'], 1) if result['avg'] else 0
    
    # Daily activity for heatmap (last 62 days - ~2 months)
    cur.execute("""
        SELECT date(created_at) as day, COUNT(*) as sessions
        FROM sessions
        WHERE created_at >= date('now', '-62 days')
        GROUP BY date(created_at)
    """)
    daily_sessions_map = {r['day']: r['sessions'] for r in cur.fetchall()}
    
    cur.execute("""
        SELECT date(timestamp) as day, COUNT(*) as turns
        FROM turns
        WHERE timestamp >= date('now', '-62 days')
        GROUP BY date(timestamp)
    """)
    daily_turns_map = {r['day']: r['turns'] for r in cur.fetchall()}
    
    conn.close()
    
    # Extract token usage from logs
    token_usage = extract_token_usage_from_logs()
    metrics.update(token_usage)
    
    # Merge session/turn data into daily_activity
    for day, sessions in daily_sessions_map.items():
        if day not in metrics['daily_activity']:
            metrics['daily_activity'][day] = {'tokens': 0, 'saved': 0, 'compactions': 0}
        metrics['daily_activity'][day]['sessions'] = sessions
        metrics['daily_activity'][day]['turns'] = daily_turns_map.get(day, 0)
    
    # Ensure all days in turns map are included
    for day, turns in daily_turns_map.items():
        if day not in metrics['daily_activity']:
            metrics['daily_activity'][day] = {'tokens': 0, 'saved': 0, 'compactions': 0, 'sessions': 0}
        if 'turns' not in metrics['daily_activity'][day]:
            metrics['daily_activity'][day]['turns'] = turns
    
    # Fill in missing days for charts
    today = datetime.now().date()
    for i in range(7):
        day = (today - timedelta(days=6-i)).isoformat()
        if not any(d['day'] == day for d in metrics['daily_sessions']):
            metrics['daily_sessions'].append({'day': day, 'count': 0})
        if not any(d['day'] == day for d in metrics['daily_turns']):
            metrics['daily_turns'].append({'day': day, 'count': 0})
    
    metrics['daily_sessions'].sort(key=lambda x: x['day'])
    metrics['daily_turns'].sort(key=lambda x: x['day'])
    
    # Add timestamp
    metrics['generated_at'] = datetime.now().isoformat()
    
    return metrics


def generate_html_widget(metrics):
    """Generate HTML widget for the dashboard."""
    if not metrics:
        return '<div class="card"><h2>Copilot Usage</h2><p>No data available</p></div>'
    
    # Chart data
    days = [d['day'][-5:] for d in metrics['daily_sessions'][-7:]]  # MM-DD format
    session_counts = [d['count'] for d in metrics['daily_sessions'][-7:]]
    turn_counts = [d['count'] for d in metrics['daily_turns'][-7:]]
    
    # Top projects rows
    project_rows = '\n'.join([
        f'<div class="usage-row"><span class="project-name">{p["project"][:30]}</span><span class="project-count">{p["sessions"]}</span></div>'
        for p in metrics['top_projects'][:4]
    ]) or '<div class="usage-row"><span class="project-name" style="color: var(--text-dim);">No projects</span></div>'
    
    # Recent sessions
    recent_items = '\n'.join([
        f'<div class="recent-session"><span class="session-summary">{s["summary"][:35]}{"..." if len(s["summary"] or "") > 35 else ""}</span><span class="session-time">{s["created_at"][11:16]}</span></div>'
        for s in metrics['recent_sessions'][:3] if s['summary']
    ]) or '<div class="recent-session"><span class="session-summary" style="color: var(--text-dim);">No recent sessions</span></div>'
    
    return {
        'stats': {
            'sessions_today': metrics['sessions_today'],
            'turns_today': metrics['turns_today'],
            'sessions_week': metrics['sessions_this_week'],
            'turns_week': metrics['turns_this_week'],
            'projects_week': metrics['projects_this_week'],
            'files_edited': metrics['files_edited_week'],
            'avg_turns': metrics['avg_turns_per_session']
        },
        'chart_data': {
            'labels': days,
            'sessions': session_counts,
            'turns': turn_counts
        },
        'top_projects': metrics['top_projects'][:4],
        'recent_sessions': metrics['recent_sessions'][:3]
    }


def main():
    metrics = get_usage_metrics()
    
    if '--json' in sys.argv:
        print(json.dumps(metrics, indent=2, default=str))
    else:
        if not metrics:
            print("❌ Session store not found")
            return
        
        print(f"🤖 Copilot CLI Usage")
        print(f"   ─────────────────────────────────")
        print(f"   Today: {metrics['sessions_today']} sessions, {metrics['turns_today']} turns")
        print(f"   This week: {metrics['sessions_this_week']} sessions, {metrics['turns_this_week']} turns")
        print(f"   Projects: {metrics['projects_this_week']} | Files edited: {metrics['files_edited_week']}")
        print(f"   Avg turns/session: {metrics['avg_turns_per_session']}")
        print(f"\n   Top Projects:")
        for p in metrics['top_projects'][:3]:
            print(f"   - {p['project']}: {p['sessions']} sessions")


if __name__ == "__main__":
    main()
