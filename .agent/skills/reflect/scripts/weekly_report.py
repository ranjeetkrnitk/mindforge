#!/usr/bin/env python3
"""
Comprehensive weekly productivity report with JIRA tracking, services, ideas, and caching.
Usage: python3 weekly_report.py <vault_root> [--force] [--week YYYY-WNN]
"""

import re
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Patterns for extraction - JIRA is only KIJI-XXX format
JIRA_PATTERN = re.compile(r'\b(KIJI-\d+)\b', re.IGNORECASE)
# Separate pattern for change requests (not JIRA)
CHANGE_PATTERN = re.compile(r'\b(CHG\d{7,}|SNOW-\d+|INC\d+)\b', re.IGNORECASE)
SERVICE_PATTERN = re.compile(r'\b(storefront|cart[-_]?service|payment[-_]?service|checkout|cxone|rex|giftcard|loyalty|order[-_]?service|api[-_]?gateway|blackhawk)\b', re.IGNORECASE)
IDEA_PATTERN = re.compile(r'\b(idea|concept|proposal|experiment|poc|prototype)\b', re.IGNORECASE)

# Exclude folders
EXCLUDE_FOLDERS = {
    "_archived", "_system", "_attachments", "_dashboards", ".trash", ".obsidian", ".claude",
    "Notion Import", "Release Docs", "QA Exports", "SEMI Exports", "Prod Exports",
    "Alti ASP", "Docker", "bruno", "scripts", "Requestly", "splunk-labs",
    "Important Details", "Notes"
}

def get_week_id(date=None):
    """Get week identifier like 2026-W20 (Sunday-Saturday week)."""
    d = date or datetime.now()
    # Adjust to Sunday-Saturday week (add 1 day so Sunday becomes start)
    adjusted = d + timedelta(days=1)
    return f"{adjusted.isocalendar()[0]}-W{adjusted.isocalendar()[1]:02d}"

def get_week_range(week_id=None):
    """Get start (Sunday) and end (Saturday) dates for a week ID."""
    if week_id:
        year, week = int(week_id[:4]), int(week_id.split('W')[1])
        # ISO week starts Monday, so get Monday then subtract 1 to get Sunday
        monday = datetime.strptime(f'{year}-W{week:02d}-1', '%G-W%V-%u')
        start = monday - timedelta(days=1)  # Sunday
    else:
        today = datetime.now()
        # Find most recent Sunday
        days_since_sunday = (today.weekday() + 1) % 7
        start = today - timedelta(days=days_since_sunday)
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)  # Saturday
    return start, end

def extract_summary(content):
    """Extract summary section from note content."""
    summary_match = re.search(r'##\s*Summary\s*\n+(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL | re.IGNORECASE)
    if summary_match:
        summary = summary_match.group(1).strip()
        summary = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', summary)
        summary = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', summary)
        sentences = re.split(r'(?<=[.!?])\s+', summary)
        short = ' '.join(sentences[:3])
        return short[:300] + '...' if len(short) > 300 else short
    
    content_clean = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
    content_clean = re.sub(r'^#[^\n]*\n+', '', content_clean)
    para = content_clean.strip().split('\n\n')[0]
    para = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', para)
    return para[:200] + '...' if len(para) > 200 else para

def extract_title(filename):
    """Extract clean title from filename."""
    return re.sub(r'^\d{4}-\d{2}-\d{2}\s*--?\s*', '', filename)

def scan_productivity(vault_root, start_date, end_date):
    """Comprehensive vault scan for productivity metrics."""
    vault = Path(vault_root)
    notes = [f for f in vault.rglob("*.md") if not any(p in f.parts for p in EXCLUDE_FOLDERS)]
    
    link_pattern = re.compile(r'\[\[([^\]|#]+)')
    domain_pattern = re.compile(r'domain/(\w+)')
    type_pattern = re.compile(r'type/(\w+)')
    
    metrics = {
        'modified': [], 'jira_tickets': defaultdict(list), 'change_requests': defaultdict(list),
        'services': defaultdict(list), 'ideas': [], 'domains': defaultdict(int), 'types': defaultdict(int),
        'code_changes': [], 'analysis_notes': [], 'new_concepts': [],
        'work_items': [], 'self_items': [], 'craft_items': []
    }
    
    for f in notes:
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if not (start_date <= mtime <= end_date):
                continue
            
            content = f.read_text(errors='ignore')
            links = link_pattern.findall(content)
            file_domains = domain_pattern.findall(content)
            file_types = type_pattern.findall(content)
            
            note_info = {
                'name': f.stem,
                'title': extract_title(f.stem),
                'path': str(f.relative_to(vault)),
                'mtime': mtime,
                'date': mtime.strftime('%b %d'),
                'links': len(links),
                'summary': extract_summary(content),
                'domains': file_domains,
                'types': file_types
            }
            
            metrics['modified'].append(note_info)
            
            for d in file_domains:
                metrics['domains'][d] += 1
            for t in file_types:
                metrics['types'][t] += 1
            
            # JIRA tickets (only KIJI-XXX)
            for ticket in JIRA_PATTERN.findall(content):
                ticket_upper = ticket.upper()
                if note_info not in metrics['jira_tickets'][ticket_upper]:
                    metrics['jira_tickets'][ticket_upper].append(note_info)
            
            # Change requests (CHG, SNOW, INC - tracked separately)
            for cr in CHANGE_PATTERN.findall(content):
                cr_upper = cr.upper()
                if note_info not in metrics['change_requests'][cr_upper]:
                    metrics['change_requests'][cr_upper].append(note_info)
            
            # Services
            for svc in SERVICE_PATTERN.findall(content):
                svc_lower = svc.lower().replace('_', '-')
                if note_info not in metrics['services'][svc_lower]:
                    metrics['services'][svc_lower].append(note_info)
            
            # Ideas
            if IDEA_PATTERN.search(f.stem) or IDEA_PATTERN.search(content[:500]):
                metrics['ideas'].append(note_info)
            
            # Categorize by domain
            primary_domain = file_domains[0] if file_domains else 'other'
            if primary_domain == 'work':
                metrics['work_items'].append(note_info)
            elif primary_domain == 'self':
                metrics['self_items'].append(note_info)
            elif primary_domain in ('craft', 'technology'):
                metrics['craft_items'].append(note_info)
            
            # Code changes (look for code blocks or technical content)
            if 'code' in file_types or '```' in content or 'def ' in content or 'function ' in content:
                metrics['code_changes'].append(note_info)
            
            # Analysis notes
            if 'analysis' in f.stem.lower() or 'review' in f.stem.lower() or 'investigation' in f.stem.lower():
                metrics['analysis_notes'].append(note_info)
            
            # New concepts
            if 'concept' in file_types or 'evergreen' in file_types:
                metrics['new_concepts'].append(note_info)
                
        except Exception:
            pass
    
    # Sort all lists by date
    for key in ['modified', 'ideas', 'code_changes', 'analysis_notes', 'new_concepts', 'work_items', 'self_items', 'craft_items']:
        metrics[key].sort(key=lambda x: -x['mtime'].timestamp())
    
    return metrics

def generate_prose_summary(metrics, start_date, end_date):
    """Generate a human-readable prose summary with bullet points."""
    paragraphs = []
    
    # Opening paragraph
    total_notes = len(metrics['modified'])
    jira_count = len(metrics['jira_tickets'])
    services_count = len(metrics['services'])
    
    if total_notes > 0:
        opening = f"This week saw activity across {total_notes} notes"
        if jira_count > 0:
            opening += f", with work spanning {jira_count} JIRA ticket{'s' if jira_count > 1 else ''}"
        if services_count > 0:
            opening += f" and {services_count} service{'s' if services_count > 1 else ''}"
        opening += "."
        paragraphs.append(opening)
    
    # Key focus areas
    bullets = []
    
    # Work items
    if metrics['work_items']:
        work_titles = [n['title'][:40] for n in metrics['work_items'][:3]]
        if len(work_titles) > 0:
            bullets.append(f"<strong>Work focus:</strong> {', '.join(work_titles)}")
    
    # JIRA tickets worked on
    if metrics['jira_tickets']:
        tickets = list(metrics['jira_tickets'].keys())[:5]
        bullets.append(f"<strong>JIRA:</strong> {', '.join(tickets)}")
    
    # Services touched
    if metrics['services']:
        svcs = list(metrics['services'].keys())[:5]
        bullets.append(f"<strong>Services:</strong> {', '.join(svcs)}")
    
    # Ideas captured
    if metrics['ideas']:
        idea_titles = [i['title'][:30] for i in metrics['ideas'][:3]]
        bullets.append(f"<strong>Ideas captured:</strong> {', '.join(idea_titles)}")
    
    # Code changes
    if metrics['code_changes']:
        code_titles = [c['title'][:30] for c in metrics['code_changes'][:3]]
        bullets.append(f"<strong>Code work:</strong> {', '.join(code_titles)}")
    
    # Craft/learning
    if metrics['craft_items']:
        craft_titles = [c['title'][:30] for c in metrics['craft_items'][:3]]
        bullets.append(f"<strong>Learning:</strong> {', '.join(craft_titles)}")
    
    # Generate HTML
    html_parts = []
    if paragraphs:
        html_parts.append(f'<p>{paragraphs[0]}</p>')
    
    if bullets:
        html_parts.append('<ul class="summary-bullets">')
        for bullet in bullets:
            html_parts.append(f'  <li>{bullet}</li>')
        html_parts.append('</ul>')
    
    # Closing insight
    work_count = len(metrics['work_items'])
    craft_count = len(metrics['craft_items'])
    self_count = len(metrics['self_items'])
    
    if work_count > craft_count and work_count > self_count:
        html_parts.append('<p class="insight">Primary focus this week was on <em>work deliverables</em>.</p>')
    elif craft_count > 0:
        html_parts.append('<p class="insight">Good balance between delivery and <em>skill development</em>.</p>')
    
    return '\n'.join(html_parts) if html_parts else '<p>No significant activity this week.</p>'

def generate_text_summary(metrics, start_date, end_date):
    """Generate human-readable productivity summary."""
    lines = []
    week_id = get_week_id(start_date)
    
    lines.append(f"# Weekly Productivity Report: {week_id}")
    lines.append(f"*{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}*\n")
    
    # Overview stats
    lines.append("## Overview")
    lines.append(f"- **{len(metrics['modified'])}** notes modified")
    lines.append(f"- **{len(metrics['jira_tickets'])}** JIRA tickets referenced")
    lines.append(f"- **{len(metrics['services'])}** services touched")
    lines.append(f"- **{len(metrics['ideas'])}** ideas captured")
    lines.append(f"- **{len(metrics['code_changes'])}** code-related notes\n")
    
    # Work breakdown
    lines.append("## Work Breakdown")
    lines.append(f"- Work: {len(metrics['work_items'])} items")
    lines.append(f"- Craft/Tech: {len(metrics['craft_items'])} items")
    lines.append(f"- Self: {len(metrics['self_items'])} items\n")
    
    # JIRA Work
    if metrics['jira_tickets']:
        lines.append("## JIRA Tickets Worked On")
        for ticket, notes in sorted(metrics['jira_tickets'].items()):
            note_names = ', '.join([n['title'][:30] for n in notes[:3]])
            lines.append(f"- **{ticket}**: {note_names}")
        lines.append("")
    
    # Services
    if metrics['services']:
        lines.append("## Services Touched")
        for svc, notes in sorted(metrics['services'].items(), key=lambda x: -len(x[1])):
            lines.append(f"- **{svc}**: {len(notes)} notes")
        lines.append("")
    
    # Key Changes (top 5)
    if metrics['modified']:
        lines.append("## Key Changes")
        for note in metrics['modified'][:5]:
            domain_tag = f"[{note['domains'][0]}]" if note['domains'] else ""
            lines.append(f"\n### {note['title']} {domain_tag}")
            if note['summary']:
                lines.append(note['summary'])
        lines.append("")
    
    # Ideas
    if metrics['ideas']:
        lines.append("## New Ideas")
        for idea in metrics['ideas'][:5]:
            lines.append(f"- **{idea['title']}**: {idea['summary'][:100]}...")
        lines.append("")
    
    # Analysis Done
    if metrics['analysis_notes']:
        lines.append("## Analysis & Investigations")
        for note in metrics['analysis_notes'][:5]:
            lines.append(f"- {note['title']}")
        lines.append("")
    
    return '\n'.join(lines)

def generate_html(metrics, start_date, end_date, vault_root):
    """Generate comprehensive HTML productivity report."""
    week_id = get_week_id(start_date)
    date_range = f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"
    
    domain_colors = {
        'technology': '#7aa2f7', 'craft': '#bb9af7', 'self': '#9ece6a',
        'work': '#ff9e64', 'people': '#7dcfff', 'other': '#565f89'
    }
    
    # Generate prose summary
    summary_html = generate_prose_summary(metrics, start_date, end_date)
    
    # Build JIRA section
    jira_items = '\n'.join([
        f'''<div class="ticket-item">
          <span class="ticket-id">{ticket}</span>
          <span class="ticket-count">{len(notes)} note{"s" if len(notes) > 1 else ""}</span>
        </div>'''
        for ticket, notes in sorted(metrics['jira_tickets'].items())
    ]) or '<div class="empty-state">No JIRA tickets this week</div>'
    
    # Build services section
    service_items = '\n'.join([
        f'''<div class="service-item">
          <span class="service-name">{svc}</span>
          <div class="service-bar" style="width: {min(len(notes)*20, 100)}%"></div>
          <span class="service-count">{len(notes)}</span>
        </div>'''
        for svc, notes in sorted(metrics['services'].items(), key=lambda x: -len(x[1]))[:8]
    ]) or '<div class="empty-state">No services referenced</div>'
    
    # Build changes section
    change_items = '\n'.join([
        f'''<div class="change-item" style="border-left-color: {domain_colors.get(note['domains'][0] if note['domains'] else 'other', '#565f89')}">
          <div class="change-header">
            <span class="change-title">{note['title'][:50]}{"..." if len(note['title']) > 50 else ""}</span>
            <span class="change-meta">{note['date']}</span>
          </div>
          <p class="change-summary">{note['summary'][:150]}{"..." if len(note['summary']) > 150 else ""}</p>
        </div>'''
        for note in metrics['modified'][:8]
    ]) or '<div class="empty-state">No changes this week</div>'
    
    # Build ideas section
    idea_items = '\n'.join([
        f'''<li>
          <span class="note-name">{idea['title'][:40]}{"..." if len(idea['title']) > 40 else ""}</span>
          <span class="note-meta">{idea['date']}</span>
        </li>'''
        for idea in metrics['ideas'][:5]
    ]) or '<li class="empty-state">No new ideas captured</li>'
    
    # Domain chart data
    domain_labels = list(metrics['domains'].keys())[:6]
    domain_values = list(metrics['domains'].values())[:6]
    
    # Productivity breakdown
    work_count = len(metrics['work_items'])
    craft_count = len(metrics['craft_items'])
    self_count = len(metrics['self_items'])
    total = work_count + craft_count + self_count or 1
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Productivity Report - {week_id}</title>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg-deep: #0f0f14; --bg-surface: #16161e; --bg-elevated: #1a1b26; --bg-card: #1f2028;
      --border: #2a2b3d; --text-primary: #c0caf5; --text-secondary: #787c99; --text-dim: #565f89;
      --accent-blue: #7aa2f7; --accent-cyan: #7dcfff; --accent-magenta: #bb9af7;
      --accent-green: #9ece6a; --accent-orange: #ff9e64; --accent-red: #f7768e;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Outfit', sans-serif; background: var(--bg-deep); color: var(--text-primary); line-height: 1.6; min-height: 100vh; }}
    .bg-grid {{ position: fixed; inset: 0; background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px); background-size: 60px 60px; opacity: 0.3; pointer-events: none; z-index: 0; }}
    .container {{ position: relative; z-index: 1; max-width: 1400px; margin: 0 auto; padding: 2rem; }}
    header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem; }}
    .logo {{ display: flex; align-items: center; gap: 1rem; }}
    .logo-icon {{ width: 48px; height: 48px; background: linear-gradient(135deg, var(--accent-orange), var(--accent-magenta)); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }}
    h1 {{ font-size: 1.8rem; font-weight: 700; background: linear-gradient(135deg, var(--text-primary), var(--accent-orange)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .subtitle {{ font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; }}
    .nav-link {{ color: var(--accent-cyan); text-decoration: none; font-size: 0.9rem; padding: 0.5rem 1rem; border: 1px solid var(--border); border-radius: 8px; transition: all 0.2s; }}
    .nav-link:hover {{ border-color: var(--accent-cyan); background: rgba(125, 207, 255, 0.1); }}
    .date-range {{ background: var(--bg-elevated); padding: 0.75rem 1.5rem; border-radius: 12px; border: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: var(--accent-orange); margin-bottom: 2rem; display: inline-block; }}
    .stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
    .stat-card {{ background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem; text-align: center; }}
    .stat-card .value {{ font-size: 2rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }}
    .stat-card .label {{ font-size: 0.8rem; color: var(--text-dim); margin-top: 0.25rem; }}
    .stat-card.blue .value {{ color: var(--accent-blue); }}
    .stat-card.green .value {{ color: var(--accent-green); }}
    .stat-card.magenta .value {{ color: var(--accent-magenta); }}
    .stat-card.orange .value {{ color: var(--accent-orange); }}
    .stat-card.cyan .value {{ color: var(--accent-cyan); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
    .card {{ background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; }}
    .card h2 {{ font-size: 1rem; color: var(--text-secondary); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
    .ticket-item {{ display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: var(--bg-card); border-radius: 8px; margin-bottom: 0.5rem; }}
    .ticket-id {{ font-family: 'JetBrains Mono', monospace; color: var(--accent-blue); font-weight: 600; }}
    .ticket-count {{ font-size: 0.8rem; color: var(--text-dim); }}
    .service-item {{ display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; }}
    .service-name {{ width: 100px; font-size: 0.85rem; color: var(--text-secondary); }}
    .service-bar {{ height: 8px; background: var(--accent-green); border-radius: 4px; flex: 1; max-width: 60%; }}
    .service-count {{ font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--text-dim); }}
    .change-item {{ background: var(--bg-card); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border-left: 3px solid var(--accent-blue); }}
    .change-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem; }}
    .change-title {{ font-weight: 600; color: var(--text-primary); font-size: 0.95rem; }}
    .change-meta {{ font-size: 0.75rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; }}
    .change-summary {{ color: var(--text-secondary); font-size: 0.85rem; line-height: 1.5; }}
    .note-list {{ list-style: none; }}
    .note-list li {{ padding: 0.75rem; margin-bottom: 0.5rem; background: var(--bg-card); border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }}
    .note-name {{ color: var(--text-primary); }}
    .note-meta {{ font-size: 0.8rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; }}
    .chart-container {{ height: 200px; }}
    .empty-state {{ color: var(--text-dim); font-style: italic; padding: 1rem; text-align: center; }}
    .full-width {{ grid-column: 1 / -1; }}
    .productivity-bar {{ display: flex; height: 24px; border-radius: 12px; overflow: hidden; margin: 1rem 0; }}
    .productivity-bar .work {{ background: var(--accent-orange); }}
    .productivity-bar .craft {{ background: var(--accent-magenta); }}
    .productivity-bar .self {{ background: var(--accent-green); }}
    .productivity-legend {{ display: flex; gap: 1.5rem; justify-content: center; font-size: 0.85rem; }}
    .productivity-legend span {{ display: flex; align-items: center; gap: 0.5rem; }}
    .productivity-legend .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .text-summary {{ background: var(--bg-card); border-radius: 12px; padding: 1.5rem; font-size: 0.9rem; line-height: 1.8; }}
    .text-summary h3 {{ color: var(--accent-cyan); margin-bottom: 0.5rem; font-size: 1rem; }}
    .text-summary p {{ color: var(--text-secondary); margin-bottom: 1rem; }}
    .summary-section {{ background: linear-gradient(135deg, var(--bg-elevated), var(--bg-card)); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; }}
    .summary-section h2 {{ color: var(--accent-cyan); margin-bottom: 1rem; font-size: 1.1rem; display: flex; align-items: center; gap: 0.5rem; }}
    .summary-section p {{ color: var(--text-secondary); line-height: 1.7; margin-bottom: 0.75rem; }}
    .summary-section .insight {{ color: var(--text-dim); font-style: italic; font-size: 0.85rem; margin-top: 1rem; border-top: 1px solid var(--border); padding-top: 1rem; }}
    .summary-bullets {{ list-style: none; margin: 1rem 0; padding: 0; }}
    .summary-bullets li {{ padding: 0.5rem 0.75rem; margin-bottom: 0.5rem; background: var(--bg-elevated); border-radius: 8px; border-left: 3px solid var(--accent-blue); font-size: 0.9rem; color: var(--text-secondary); }}
    .summary-bullets li strong {{ color: var(--text-primary); }}
    @media (max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} .stats-row {{ grid-template-columns: repeat(2, 1fr); }} }}
  </style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="container">
    <header>
      <div class="logo">
        <div class="logo-icon">📊</div>
        <div>
          <h1>Productivity Report</h1>
          <div class="subtitle">{week_id} - Comprehensive Analysis</div>
        </div>
      </div>
      <a href="vault-health.html" class="nav-link">← Back to Dashboard</a>
    </header>
    
    <div class="date-range">{date_range}</div>
    
    <div class="stats-row">
      <div class="stat-card blue"><div class="value">{len(metrics['modified'])}</div><div class="label">Notes Modified</div></div>
      <div class="stat-card orange"><div class="value">{len(metrics['jira_tickets'])}</div><div class="label">JIRA Tickets</div></div>
      <div class="stat-card green"><div class="value">{len(metrics['services'])}</div><div class="label">Services</div></div>
      <div class="stat-card magenta"><div class="value">{len(metrics['ideas'])}</div><div class="label">Ideas</div></div>
      <div class="stat-card cyan"><div class="value">{len(metrics['code_changes'])}</div><div class="label">Code Notes</div></div>
    </div>
    
    <div class="card full-width" style="margin-bottom: 1.5rem;">
      <h2>📈 Productivity Distribution</h2>
      <div class="productivity-bar">
        <div class="work" style="width: {work_count*100//total}%"></div>
        <div class="craft" style="width: {craft_count*100//total}%"></div>
        <div class="self" style="width: {self_count*100//total}%"></div>
      </div>
      <div class="productivity-legend">
        <span><div class="dot" style="background: var(--accent-orange)"></div>Work ({work_count})</span>
        <span><div class="dot" style="background: var(--accent-magenta)"></div>Craft ({craft_count})</span>
        <span><div class="dot" style="background: var(--accent-green)"></div>Self ({self_count})</span>
      </div>
    </div>
    
    <div class="summary-section">
      <h2>📋 Weekly Summary</h2>
      {summary_html}
    </div>
    
    <div class="grid">
      <div class="card">
        <h2>🎫 JIRA Tickets</h2>
        {jira_items}
      </div>
      
      <div class="card">
        <h2>🔧 Services Touched</h2>
        {service_items}
      </div>
      
      <div class="card">
        <h2>💡 Ideas Captured</h2>
        <ul class="note-list">
          {idea_items}
        </ul>
      </div>
      
      <div class="card">
        <h2>📊 Domain Activity</h2>
        <div class="chart-container">
          <canvas id="domainChart"></canvas>
        </div>
      </div>
      
      <div class="card full-width">
        <h2>📝 Key Changes</h2>
        {change_items}
      </div>
    </div>
  </div>
  
  <script>
    new Chart(document.getElementById('domainChart'), {{
      type: 'doughnut',
      data: {{
        labels: {domain_labels},
        datasets: [{{
          data: {domain_values},
          backgroundColor: ['#7aa2f7', '#bb9af7', '#9ece6a', '#ff9e64', '#7dcfff', '#565f89'],
          borderWidth: 0
        }}]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ position: 'right', labels: {{ color: '#c0caf5', padding: 15 }} }}
        }}
      }}
    }});
  </script>
</body>
</html>'''
    
    return html

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate weekly productivity report')
    parser.add_argument('vault_root', help='Path to vault')
    parser.add_argument('--force', action='store_true', help='Regenerate even if cached')
    parser.add_argument('--week', help='Week ID like 2026-W20 (default: current week)')
    args = parser.parse_args()
    
    vault = Path(args.vault_root)
    if not vault.exists():
        print(f"Error: Vault not found: {vault}")
        sys.exit(1)
    
    week_id = args.week or get_week_id()
    start_date, end_date = get_week_range(args.week)
    
    # Check cache
    output_dir = vault / "_dashboards"
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"weekly-{week_id}.html"
    md_path = output_dir / f"weekly-{week_id}.md"
    
    if html_path.exists() and not args.force:
        print(f"📋 Report already exists: {html_path}")
        print(f"   Use --force to regenerate")
        return
    
    print(f"🔍 Scanning vault for {week_id}...")
    metrics = scan_productivity(args.vault_root, start_date, end_date)
    
    # Generate outputs
    html_content = generate_html(metrics, start_date, end_date, args.vault_root)
    text_summary = generate_text_summary(metrics, start_date, end_date)
    
    html_path.write_text(html_content)
    md_path.write_text(text_summary)
    
    print(f"\n📊 Weekly Productivity Report: {week_id}")
    print(f"   {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}")
    print(f"   ─────────────────────────────────")
    print(f"   📝 {len(metrics['modified'])} notes modified")
    print(f"   🎫 {len(metrics['jira_tickets'])} JIRA tickets: {', '.join(list(metrics['jira_tickets'].keys())[:5])}")
    print(f"   🔧 {len(metrics['services'])} services: {', '.join(list(metrics['services'].keys())[:5])}")
    print(f"   💡 {len(metrics['ideas'])} ideas captured")
    print(f"   💼 Work: {len(metrics['work_items'])} | Craft: {len(metrics['craft_items'])} | Self: {len(metrics['self_items'])}")
    print(f"\n   → HTML: {html_path}")
    print(f"   → MD:   {md_path}")

if __name__ == "__main__":
    main()
