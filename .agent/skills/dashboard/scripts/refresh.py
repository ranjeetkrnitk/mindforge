#!/usr/bin/env python3
"""
Refresh Obsidian vault dashboard with current metrics.
Usage: python3 refresh.py <vault_root>
"""

import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Import copilot usage module
try:
    from copilot_usage import get_usage_metrics, generate_html_widget
    COPILOT_AVAILABLE = True
except ImportError:
    COPILOT_AVAILABLE = False

def scan_vault(vault_root):
    """Scan vault and return metrics including link suggestions."""
    vault = Path(vault_root)
    # Exclude folders without .md content or system folders
    exclude = {
        # System folders
        "_archived", "_system", "_attachments", "_dashboards", ".trash", ".obsidian", ".claude",
        # Export/data folders (no .md files)
        "Notion Import", "Release Docs", "QA Exports", "SEMI Exports", "Prod Exports",
        "Alti ASP", "Docker", "bruno", "scripts", "Requestly", "splunk-labs",
        "Important Details", "Notes"
    }
    
    notes = [f for f in vault.rglob("*.md") if not any(p in f.parts for p in exclude)]
    total = len(notes)
    
    # Build note name index for link suggestions
    note_names = {f.stem.lower(): f.stem for f in notes}
    # Also track common words to exclude from matching
    common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
                    'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'will', 'more',
                    'when', 'who', 'way', 'may', 'new', 'now', 'how', 'any', 'get', 'use',
                    'see', 'from', 'with', 'this', 'that', 'what', 'your', 'which', 'their',
                    'about', 'would', 'there', 'could', 'other', 'into', 'than', 'then',
                    'some', 'these', 'them', 'being', 'its', 'also', 'just', 'over', 'such',
                    'make', 'like', 'time', 'very', 'after', 'most', 'only', 'come', 'made',
                    'find', 'here', 'many', 'where', 'did', 'get', 'should', 'each', 'much'}
    
    link_pattern = re.compile(r'\[\[([^\]|#]+)')
    domain_pattern = re.compile(r'domain/(\w+)')
    type_pattern = re.compile(r'type/(\w+)')
    
    total_links = 0
    orphans = 0
    hubs = 0
    domains = defaultdict(int)
    types = defaultdict(int)
    hub_list = []
    link_suggestions = []  # (source_file, target_note, context)
    
    for f in notes:
        try:
            content = f.read_text(errors='ignore')
            links = link_pattern.findall(content)
            linked_names = {l.lower() for l in links}
            total_links += len(links)
            
            if len(links) == 0:
                orphans += 1
            if len(links) >= 5:
                hubs += 1
                hub_list.append((f.stem, len(links)))
            
            for d in domain_pattern.findall(content):
                domains[d] += 1
            for t in type_pattern.findall(content):
                types[t] += 1
            
            # Find link suggestions: note names mentioned but not linked
            content_lower = content.lower()
            for note_lower, note_original in note_names.items():
                # Skip if already linked, same file, too short, or common word
                if (note_lower in linked_names or 
                    note_lower == f.stem.lower() or 
                    len(note_lower) < 4 or
                    note_lower in common_words):
                    continue
                
                # Look for whole word match (not inside another word)
                pattern = rf'\b{re.escape(note_lower)}\b'
                if re.search(pattern, content_lower):
                    # Get context snippet
                    match = re.search(pattern, content_lower)
                    if match:
                        start = max(0, match.start() - 30)
                        end = min(len(content), match.end() + 30)
                        context = content[start:end].replace('\n', ' ').strip()
                        if start > 0:
                            context = '...' + context
                        if end < len(content):
                            context = context + '...'
                        link_suggestions.append((f.stem, note_original, context))
        except:
            pass
    
    health_score = max(0, min(100, 100 - (orphans / total * 100) + (hubs / total * 20))) if total > 0 else 0
    hub_list.sort(key=lambda x: -x[1])
    
    # Deduplicate suggestions (same source->target pair)
    seen = set()
    unique_suggestions = []
    for s in link_suggestions:
        key = (s[0], s[1])
        if key not in seen:
            seen.add(key)
            unique_suggestions.append(s)
    
    return {
        'total': total,
        'links': total_links,
        'orphans': orphans,
        'hubs': hubs,
        'health': health_score,
        'domains': dict(sorted(domains.items(), key=lambda x: -x[1])[:6]),
        'types': dict(sorted(types.items(), key=lambda x: -x[1])[:6]),
        'top_hubs': hub_list[:10],
        'link_suggestions': unique_suggestions
    }


def write_remap_report(vault_root, suggestions):
    """Write link suggestions to _REMAP_REPORT.md."""
    report_path = Path(vault_root) / "_system" / "_REMAP_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Group by source file
    by_source = defaultdict(list)
    for source, target, context in suggestions:
        by_source[source].append((target, context))
    
    lines = [
        f"# Link Suggestions Report",
        f"",
        f"Generated: {now}",
        f"Total suggestions: {len(suggestions)}",
        f"",
        f"---",
        f"",
    ]
    
    for source in sorted(by_source.keys()):
        targets = by_source[source]
        lines.append(f"## [[{source}]]")
        lines.append(f"")
        for target, context in targets:
            lines.append(f"- **[[{target}]]** - _{context}_")
        lines.append(f"")
    
    report_path.write_text('\n'.join(lines))
    return len(suggestions)

def update_dashboard(vault_root, metrics):
    """Update the HTML dashboard with fresh metrics."""
    dashboard = Path(vault_root) / "_dashboards" / "vault-health.html"
    
    if not dashboard.exists():
        print(f"⚠️  Dashboard not found at {dashboard}")
        return False
    
    html = dashboard.read_text()
    
    orphan_pct = (metrics['orphans'] / metrics['total'] * 100) if metrics['total'] > 0 else 0
    connected = metrics['total'] - metrics['orphans']
    connected_pct = ((connected / metrics['total']) * 100) if metrics['total'] > 0 else 0
    links_per_note = (metrics['links'] / metrics['total']) if metrics['total'] > 0 else 0
    suggestion_count = len(metrics.get('link_suggestions', []))
    
    # Update health score in the ring
    html = re.sub(r'(<div class="score">)\d+(<\/div>)', rf'\g<1>{int(metrics["health"])}\2', html)
    
    # Update health ring progress (stroke-dashoffset: 440 = 0%, 0 = 100%)
    offset = int(440 - (metrics['health'] / 100 * 440))
    html = re.sub(r'stroke-dashoffset:\s*\d+;', f'stroke-dashoffset: {offset};', html)
    html = re.sub(r'to \{ stroke-dashoffset:\s*\d+;\s*\}', f'to {{ stroke-dashoffset: {offset}; }}', html)
    
    # Update stat cards - Total Notes
    html = re.sub(
        r'(<div class="stat-card blue">.*?<div class="value">)[\d,]+(<\/div>)',
        rf'\g<1>{metrics["total"]:,}\2',
        html, flags=re.DOTALL
    )
    
    # Update stat cards - Total Links
    html = re.sub(
        r'(<div class="stat-card cyan">.*?<div class="value">)[\d,]+(<\/div>)',
        rf'\g<1>{metrics["links"]:,}\2',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'(<div class="stat-card cyan">.*?<span class="trend up">)[^<]+(<\/span>)',
        rf'\g<1>{links_per_note:.2f}/note\2',
        html, flags=re.DOTALL
    )
    
    # Update stat cards - Hub Notes
    html = re.sub(
        r'(<div class="stat-card magenta">.*?<div class="value">)[\d,]+(<\/div>)',
        rf'\g<1>{metrics["hubs"]:,}\2',
        html, flags=re.DOTALL
    )
    
    # Update stat cards - Connected
    html = re.sub(
        r'(<div class="stat-card green">.*?<div class="value">)[\d,]+(<\/div>)',
        rf'\g<1>{connected:,}\2',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'(<div class="stat-card green">.*?<span class="trend up">)[^<]+(<\/span>)',
        rf'\g<1>{connected_pct:.0f}%\2',
        html, flags=re.DOTALL
    )
    
    # Build dynamic action cards
    action_cards = []
    pending_count = 0
    
    # Link suggestions card (always show if > 0)
    if suggestion_count > 0:
        pending_count += 1
        action_cards.append(f'''        <div class="action-card warning">
          <div class="priority">📈</div>
          <div class="content">
            <div class="title">{suggestion_count} Link Suggestions</div>
            <div class="description">Found notes that could be connected. Review _REMAP_REPORT.md</div>
            <code class="command">open _system/_REMAP_REPORT.md</code>
          </div>
        </div>''')
    
    # Orphan card (only show if > 5%)
    if orphan_pct > 5:
        pending_count += 1
        action_cards.append(f'''        <div class="action-card urgent">
          <div class="priority">🚨</div>
          <div class="content">
            <div class="title">{metrics["orphans"]} Orphans Remain ({orphan_pct:.0f}%)</div>
            <div class="description">Many notes need links. Consider archiving stale ones.</div>
            <code class="command">/memorize prune orphans</code>
          </div>
        </div>''')
    
    # Weekly productivity report link (find latest with YYYY-WNN format)
    dashboard_dir = Path(vault_root) / "_dashboards"
    import re as re_module
    weekly_reports = [f for f in dashboard_dir.glob("weekly-*.html") 
                      if re_module.match(r'weekly-\d{4}-W\d{2}\.html', f.name)]
    weekly_reports = sorted(weekly_reports, reverse=True)
    if weekly_reports:
        latest_report = weekly_reports[0].name
        week_id = latest_report.replace("weekly-", "").replace(".html", "")
        action_cards.append(f'''        <a href="{latest_report}" class="action-card info" style="text-decoration: none;">
          <div class="priority">📊</div>
          <div class="content">
            <div class="title">Weekly Productivity Report</div>
            <div class="description">{week_id} - JIRA tickets, services, ideas overview.</div>
            <code class="command">View Report →</code>
          </div>
        </a>''')
        pending_count += 1
    
    # Weekly reflection card
    action_cards.append('''        <div class="action-card info">
          <div class="priority">🔄</div>
          <div class="content">
            <div class="title">Weekly Reflection</div>
            <div class="description">Review activity and surface consolidation opportunities.</div>
            <code class="command">/reflect weekly</code>
          </div>
        </div>''')
    
    # Replace actions section
    actions_html = '\n'.join(action_cards)
    html = re.sub(
        r'(<div class="section-header">[\s\S]*?<span class="badge">)\d+ pending(</span>)',
        rf'\g<1>{pending_count} pending\2',
        html
    )
    html = re.sub(
        r'(<div class="actions-grid">)[\s\S]*?(</div>\s*</section>\s*<section class="charts-section">)',
        rf'\1\n{actions_html}\n      \2',
        html
    )
    
    # Update domain chart data
    domains = list(metrics['domains'].items())
    if domains:
        domain_labels = [d[0].title() for d in domains]
        domain_values = [d[1] for d in domains]
        while len(domain_labels) < 6:
            domain_labels.append('Other')
            domain_values.append(0)
        html = re.sub(
            r"(labels: \[)'[^']+', '[^']+', '[^']+', '[^']+', '[^']+', '[^']+'(\])",
            rf"\g<1>'{domain_labels[0]}', '{domain_labels[1]}', '{domain_labels[2]}', '{domain_labels[3]}', '{domain_labels[4]}', '{domain_labels[5]}'\2",
            html
        )
        html = re.sub(
            r"(data: \[)\d+, \d+, \d+, \d+, \d+, \d+(\])",
            rf"\g<1>{domain_values[0]}, {domain_values[1]}, {domain_values[2]}, {domain_values[3]}, {domain_values[4]}, {domain_values[5]}\2",
            html, count=1
        )
    
    # Update type chart data
    types = list(metrics['types'].items())
    if types:
        type_labels = [t[0] for t in types]
        type_values = [t[1] for t in types]
        while len(type_labels) < 6:
            type_labels.append('other')
            type_values.append(0)
        html = re.sub(
            r"(labels: \[)'[^']+', '[^']+', '[^']+', '[^']+', '[^']+', '[^']+'(\],\s*datasets: \[\{\s*data:)",
            rf"\g<1>'{type_labels[0]}', '{type_labels[1]}', '{type_labels[2]}', '{type_labels[3]}', '{type_labels[4]}', '{type_labels[5]}'\2",
            html
        )
        html = re.sub(
            r"(indexAxis: 'y'[\s\S]*?data: \[)\d+, \d+, \d+, \d+, \d+, \d+(\])",
            rf"\g<1>{type_values[0]}, {type_values[1]}, {type_values[2]}, {type_values[3]}, {type_values[4]}, {type_values[5]}\2",
            html
        )
    
    # Update Copilot usage section if available
    copilot_stats = None
    if COPILOT_AVAILABLE:
        copilot_metrics = get_usage_metrics()
        if copilot_metrics:
            copilot_data = generate_html_widget(copilot_metrics)
            copilot_stats = copilot_data['stats']
            
            # Update stat values
            html = re.sub(
                r'(<div class="stat-value" id="copilotSessionsToday">)\d+(<\/div>)',
                rf'\g<1>{copilot_stats["sessions_today"]}\2',
                html
            )
            html = re.sub(
                r'(<div class="stat-value" id="copilotTurnsToday">)\d+(<\/div>)',
                rf'\g<1>{copilot_stats["turns_today"]}\2',
                html
            )
            html = re.sub(
                r'(<div class="stat-value" id="copilotSessionsWeek">)\d+(<\/div>)',
                rf'\g<1>{copilot_stats["sessions_week"]}\2',
                html
            )
            html = re.sub(
                r'(<div class="stat-value" id="copilotFilesEdited">)\d+(<\/div>)',
                rf'\g<1>{copilot_stats["files_edited"]}\2',
                html
            )
            
            # Update header stats (tokensUsed/contextLimit in header)
            tokens_today = copilot_metrics.get('tokens_today', 0)
            context_limit = copilot_metrics.get('context_limit', 168000)
            
            tokens_used_str = f"{tokens_today // 1000}K" if tokens_today >= 1000 else str(tokens_today)
            context_limit_str = f"{context_limit // 1000}K"
            
            html = re.sub(
                r'(<span id="tokensUsed">)[^<]+(<\/span>)',
                rf'\g<1>{tokens_used_str}\2',
                html
            )
            html = re.sub(
                r'(<span id="contextLimit">)[^<]+(<\/span>)',
                rf'\g<1>{context_limit_str}\2',
                html
            )
            
            # Update projects list (compact chip format)
            projects_html = '\n'.join([
                f'          <div class="project-chip"><span class="pname">{p["project"][:20]}</span><span class="pcount">{p["sessions"]}</span></div>'
                for p in copilot_data['top_projects'][:4]
            ]) or '          <div class="project-chip"><span class="pname">No projects</span><span class="pcount">0</span></div>'
            
            html = re.sub(
                r'(<div class="compact-projects" id="copilotProjects">)[\s\S]*?(</div>\s*</div>\s*</section>)',
                rf'\1\n{projects_html}\n        \2',
                html
            )
            
            # Update weekly stats
            tokens_week = copilot_metrics.get('tokens_week', 0)
            tokens_saved_week = copilot_metrics.get('tokens_saved_week', 0)
            
            tokens_week_str = f"{tokens_week // 1000}K" if tokens_week >= 1000 else str(tokens_week)
            tokens_saved_week_str = f"{tokens_saved_week // 1000}K" if tokens_saved_week >= 1000 else str(tokens_saved_week)
            
            html = re.sub(
                r'(<span class="stat-val" id="weekTokens">)[^<]+(<\/span>)',
                rf'\g<1>{tokens_week_str}\2',
                html
            )
            html = re.sub(
                r'(<span class="stat-val" id="weekSaved">)[^<]+(<\/span>)',
                rf'\g<1>{tokens_saved_week_str}\2',
                html
            )
            
            # Inject heatmap data
            import json
            daily_activity = copilot_metrics.get('daily_activity', {})
            heatmap_json = json.dumps(daily_activity)
            html = re.sub(
                r'const heatmapData = \{[^}]*\};',
                f'const heatmapData = {heatmap_json};',
                html
            )
    
    # Update hub list
    hub_html = ""
    for name, count in metrics['top_hubs'][:10]:
        hub_html += f'        <div class="hub-item"><span class="count">{count}</span><span class="name">{name}</span></div>\n'
    html = re.sub(
        r'(<div class="hubs-grid">)[\s\S]*?(</div>\s*</section>\s*</div>\s*<script>)',
        rf'\1\n{hub_html}      \2',
        html
    )
    
    dashboard.write_text(html)
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 refresh.py <vault_root>")
        sys.exit(1)
    
    vault_root = sys.argv[1]
    
    if not Path(vault_root).exists():
        print(f"❌ Vault not found: {vault_root}")
        sys.exit(1)
    
    metrics = scan_vault(vault_root)
    
    # Write link suggestions report
    suggestion_count = write_remap_report(vault_root, metrics.get('link_suggestions', []))
    
    if update_dashboard(vault_root, metrics):
        orphan_pct = (metrics['orphans'] / metrics['total'] * 100) if metrics['total'] > 0 else 0
        print(f"📊 Dashboard updated")
        print(f"Notes: {metrics['total']} | Links: {metrics['links']} | Orphans: {orphan_pct:.1f}% | Health: {metrics['health']:.0f}%")
        if suggestion_count > 0:
            print(f"💡 {suggestion_count} link suggestions written to _system/_REMAP_REPORT.md")
        
        # Print Copilot stats if available
        if COPILOT_AVAILABLE:
            copilot_metrics = get_usage_metrics()
            if copilot_metrics:
                print(f"🤖 Copilot: {copilot_metrics['sessions_today']} sessions today, {copilot_metrics['turns_today']} turns")

if __name__ == "__main__":
    main()
