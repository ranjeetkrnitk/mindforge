#!/usr/bin/env python3
"""
Generate weekly reflection HTML report.
Usage: python3 weekly_html.py <vault_root>
"""

import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def extract_summary(content):
    """Extract summary section from note content."""
    # Look for ## Summary section
    summary_match = re.search(r'##\s*Summary\s*\n+(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL | re.IGNORECASE)
    if summary_match:
        summary = summary_match.group(1).strip()
        # Clean up: remove links, limit to ~3 sentences
        summary = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', summary)
        summary = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', summary)
        # Take first 2-3 sentences (up to 300 chars)
        sentences = re.split(r'(?<=[.!?])\s+', summary)
        short = ' '.join(sentences[:3])
        if len(short) > 300:
            short = short[:297] + '...'
        return short
    
    # Fallback: first non-frontmatter paragraph
    content_no_fm = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
    content_no_heading = re.sub(r'^#[^\n]*\n+', '', content_no_fm)
    para = content_no_heading.strip().split('\n\n')[0]
    para = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', para)
    if len(para) > 200:
        para = para[:197] + '...'
    return para if para else None


def extract_title_from_filename(filename):
    """Extract clean title from episode filename."""
    # Remove date prefix like "2026-05-17 -- "
    title = re.sub(r'^\d{4}-\d{2}-\d{2}\s*--?\s*', '', filename)
    return title if title else filename


def scan_weekly(vault_root):
    """Scan vault for weekly reflection data."""
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
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    notes = [f for f in vault.rglob("*.md") if not any(p in f.parts for p in exclude)]
    
    link_pattern = re.compile(r'\[\[([^\]|#]+)')
    domain_pattern = re.compile(r'domain/(\w+)')
    type_pattern = re.compile(r'type/(\w+)')
    arousal_pattern = re.compile(r'arousal:\s*(\w+)', re.IGNORECASE)
    valence_pattern = re.compile(r'valence:\s*(\w+)', re.IGNORECASE)
    maturity_pattern = re.compile(r'maturity/(\w+)')
    
    modified = []
    domains = defaultdict(int)
    types = defaultdict(int)
    emotion_data = []
    orphans = []
    promotion_candidates = []
    questions = []
    recent_notes = []
    change_log = []  # New: track changes with summaries
    
    one_week_ago = end_date - timedelta(days=7)
    
    for f in notes:
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            content = f.read_text(errors='ignore')
            links = link_pattern.findall(content)
            file_types = type_pattern.findall(content)
            maturity = maturity_pattern.findall(content)
            
            in_range = start_date <= mtime <= end_date
            
            if in_range:
                modified.append((f.stem, mtime, len(links)))
                recent_notes.append((f.stem, mtime))
                
                for d in domain_pattern.findall(content):
                    domains[d] += 1
                for t in file_types:
                    types[t] += 1
                
                arousal = arousal_pattern.search(content)
                valence = valence_pattern.search(content)
                if arousal or valence:
                    emotion_data.append({
                        'name': f.stem,
                        'arousal': arousal.group(1) if arousal else 'medium',
                        'valence': valence.group(1) if valence else 'neutral',
                        'date': mtime.strftime('%b %d')
                    })
                
                if len(links) == 0:
                    orphans.append(f.stem)
                
                if '?' in f.stem:
                    questions.append(f.stem)
                
                # Extract change summaries from episodes
                if 'episode' in file_types:
                    summary = extract_summary(content)
                    if summary:
                        change_log.append({
                            'title': extract_title_from_filename(f.stem),
                            'summary': summary,
                            'date': mtime.strftime('%b %d'),
                            'domain': domain_pattern.findall(content)[0] if domain_pattern.findall(content) else 'other',
                            'mtime': mtime
                        })
            
            # Promotion candidates: episode + 3+ links + 7+ days old
            if 'episode' in file_types and len(links) >= 3 and mtime < one_week_ago:
                if 'fleeting' in maturity or not maturity:
                    promotion_candidates.append({
                        'name': f.stem,
                        'links': len(links),
                        'date': mtime.strftime('%b %d')
                    })
        except:
            pass
    
    promotion_candidates.sort(key=lambda x: -x['links'])
    recent_notes.sort(key=lambda x: -x[1].timestamp())
    change_log.sort(key=lambda x: -x['mtime'].timestamp())  # Most recent first
    
    high_arousal = [e for e in emotion_data if e['arousal'].lower() == 'high']
    
    valence_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    for e in emotion_data:
        v = e['valence'].lower()
        if v in valence_counts:
            valence_counts[v] += 1
    
    total_valence = sum(valence_counts.values()) or 1
    
    return {
        'date_range': f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}",
        'modified_count': len(modified),
        'orphans_count': len(orphans),
        'emotion_count': len(emotion_data),
        'domains': dict(sorted(domains.items(), key=lambda x: -x[1])),
        'high_arousal': high_arousal[:5],
        'valence': valence_counts,
        'valence_pct': {k: int(v/total_valence*100) for k, v in valence_counts.items()},
        'promotion': promotion_candidates[:5],
        'questions': questions[:5],
        'recent': [n[0] for n in recent_notes[:10]],
        'change_log': change_log[:10]  # Top 10 recent changes
    }


def generate_html(data, vault_root):
    """Generate the weekly reflection HTML."""
    
    # Domain rows
    domain_rows = '\n'.join([
        f'        <div class="stat-row"><span class="stat-label">{d}</span><span class="stat-value">{c}</span></div>'
        for d, c in list(data['domains'].items())[:5]
    ])
    
    # Emotional peaks
    emotion_items = '\n'.join([
        f'''          <li>
            <span class="note-name">{e['name'][:50]}{'...' if len(e['name']) > 50 else ''}</span>
            <span class="badge positive">{e['valence']}</span>
          </li>'''
        for e in data['high_arousal'][:3]
    ]) or '<li><span class="note-name" style="color: var(--text-dim);">No high-arousal notes this week</span></li>'
    
    # Promotion candidates
    promo_items = '\n'.join([
        f'''          <li>
            <span class="note-name">{p['name'][:40]}{'...' if len(p['name']) > 40 else ''}</span>
            <span class="note-meta">{p['links']} links</span>
          </li>'''
        for p in data['promotion'][:4]
    ]) or '<li><span class="note-name" style="color: var(--text-dim);">No candidates ready</span></li>'
    
    # Questions
    question_items = '\n'.join([
        f'          <li><span class="note-name" style="font-size: 0.9rem;">{q[:60]}{"..." if len(q) > 60 else ""}</span></li>'
        for q in data['questions'][:3]
    ]) or '<li><span class="note-name" style="color: var(--text-dim);">No open questions</span></li>'
    
    # Change log items
    domain_colors = {
        'technology': '#7aa2f7', 'craft': '#bb9af7', 'self': '#9ece6a', 
        'work': '#ff9e64', 'people': '#7dcfff', 'other': '#565f89'
    }
    change_items = '\n'.join([
        f'''        <div class="change-item">
          <div class="change-header">
            <span class="change-title">{c['title'][:60]}{'...' if len(c['title']) > 60 else ''}</span>
            <span class="change-meta"><span class="domain-tag" style="background: {domain_colors.get(c['domain'], '#565f89')}20; color: {domain_colors.get(c['domain'], '#565f89')}">{c['domain']}</span> {c['date']}</span>
          </div>
          <p class="change-summary">{c['summary']}</p>
        </div>'''
        for c in data.get('change_log', [])[:8]
    ]) or '<div class="change-item"><p class="change-summary" style="color: var(--text-dim);">No changes recorded this week</p></div>'
    
    # Chart data
    domain_labels = list(data['domains'].keys())[:5]
    domain_values = list(data['domains'].values())[:5]
    
    # Valence bar
    v = data['valence_pct']
    valence_bar = f'''<div class="positive" style="width: {v['positive']}%;"></div>
            <div class="neutral" style="width: {v['neutral']}%;"></div>
            <div class="negative" style="width: {v['negative']}%;"></div>'''
    valence_text = ', '.join([f"{v}% {k}" for k, v in data['valence_pct'].items() if v > 0])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Weekly Reflection</title>
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
    .container {{ position: relative; z-index: 1; max-width: 1200px; margin: 0 auto; padding: 2rem; }}
    header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem; }}
    .logo {{ display: flex; align-items: center; gap: 1rem; }}
    .logo-icon {{ width: 48px; height: 48px; background: linear-gradient(135deg, var(--accent-magenta), var(--accent-blue)); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }}
    h1 {{ font-size: 1.8rem; font-weight: 700; background: linear-gradient(135deg, var(--text-primary), var(--accent-magenta)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .subtitle {{ font-size: 0.85rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; }}
    .nav-link {{ color: var(--accent-cyan); text-decoration: none; font-size: 0.9rem; padding: 0.5rem 1rem; border: 1px solid var(--border); border-radius: 8px; transition: all 0.2s; }}
    .nav-link:hover {{ border-color: var(--accent-cyan); background: rgba(125, 207, 255, 0.1); }}
    .date-range {{ background: var(--bg-elevated); padding: 0.75rem 1.5rem; border-radius: 12px; border: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: var(--accent-cyan); margin-bottom: 2rem; display: inline-block; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
    .card {{ background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; }}
    .card h2 {{ font-size: 1rem; color: var(--text-secondary); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
    .stat-row {{ display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--border); }}
    .stat-row:last-child {{ border-bottom: none; }}
    .stat-label {{ color: var(--text-secondary); }}
    .stat-value {{ font-weight: 600; color: var(--accent-blue); font-family: 'JetBrains Mono', monospace; }}
    .stat-value.green {{ color: var(--accent-green); }}
    .stat-value.magenta {{ color: var(--accent-magenta); }}
    .note-list {{ list-style: none; }}
    .note-list li {{ padding: 0.75rem; margin-bottom: 0.5rem; background: var(--bg-card); border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }}
    .note-list .note-name {{ color: var(--text-primary); }}
    .note-list .note-meta {{ font-size: 0.8rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; }}
    .badge {{ padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }}
    .badge.positive {{ background: rgba(158, 206, 106, 0.15); color: var(--accent-green); }}
    .chart-container {{ height: 200px; margin-top: 1rem; }}
    .reflect-card {{ background: linear-gradient(135deg, var(--bg-elevated), var(--bg-card)); border: 1px solid var(--accent-magenta); }}
    .reflect-card h2 {{ color: var(--accent-magenta); }}
    .reflect-list {{ list-style: none; }}
    .reflect-list li {{ padding: 1rem; margin-bottom: 0.75rem; background: var(--bg-deep); border-radius: 8px; border-left: 3px solid var(--accent-magenta); color: var(--text-secondary); font-style: italic; }}
    .valence-bar {{ height: 8px; border-radius: 4px; background: var(--bg-card); overflow: hidden; margin-top: 0.5rem; display: flex; }}
    .change-item {{ background: var(--bg-card); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; border-left: 3px solid var(--accent-blue); }}
    .change-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem; }}
    .change-title {{ font-weight: 600; color: var(--text-primary); font-size: 0.95rem; }}
    .change-meta {{ font-size: 0.75rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; display: flex; align-items: center; gap: 0.5rem; }}
    .domain-tag {{ padding: 0.2rem 0.5rem; border-radius: 6px; font-size: 0.7rem; font-weight: 500; }}
    .change-summary {{ color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; }}
    .valence-bar .positive {{ background: var(--accent-green); }}
    .valence-bar .neutral {{ background: var(--text-dim); }}
    .valence-bar .negative {{ background: var(--accent-red); }}
    .full-width {{ grid-column: 1 / -1; }}
    @media (max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="container">
    <header>
      <div class="logo">
        <div class="logo-icon">🔮</div>
        <div>
          <h1>Weekly Reflection</h1>
          <div class="subtitle">CLS-driven vault retrospective</div>
        </div>
      </div>
      <a href="vault-health.html" class="nav-link">← Back to Dashboard</a>
    </header>
    <div class="date-range">{data['date_range']}</div>
    <div class="grid">
      <div class="card">
        <h2><span class="emoji">📊</span> Activity Summary</h2>
        <div class="stat-row"><span class="stat-label">Notes Modified</span><span class="stat-value">{data['modified_count']}</span></div>
        <div class="stat-row"><span class="stat-label">Orphans Created</span><span class="stat-value green">{data['orphans_count']}</span></div>
        <div class="stat-row"><span class="stat-label">Emotion Tagged</span><span class="stat-value magenta">{data['emotion_count']}</span></div>
      </div>
      <div class="card">
        <h2><span class="emoji">🏷️</span> Domain Activity</h2>
{domain_rows}
      </div>
      <div class="card">
        <h2><span class="emoji">💚</span> Emotional Peaks</h2>
        <ul class="note-list">
{emotion_items}
        </ul>
        <div style="margin-top: 1rem;">
          <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem;">Valence Distribution</div>
          <div class="valence-bar">
            {valence_bar}
          </div>
          <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 0.25rem;">{valence_text}</div>
        </div>
      </div>
      <div class="card">
        <h2><span class="emoji">🔄</span> Consolidation Candidates</h2>
        <ul class="note-list">
{promo_items}
        </ul>
        <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.75rem;">Episodes with 3+ links, 7+ days old</div>
      </div>
      <div class="card">
        <h2><span class="emoji">🔥</span> Burst Topics</h2>
        <div class="chart-container">
          <canvas id="burstChart"></canvas>
        </div>
      </div>
      <div class="card">
        <h2><span class="emoji">❓</span> Open Questions</h2>
        <ul class="note-list">
{question_items}
        </ul>
      </div>
      <div class="card full-width">
        <h2><span class="emoji">📝</span> Change Log</h2>
{change_items}
      </div>
      <div class="card reflect-card full-width">
        <h2><span class="emoji">💡</span> Reflection Prompts</h2>
        <ul class="reflect-list">
          <li>What drove this week's activity? Was it focused work or exploration?</li>
          <li>Any high-arousal moments worth consolidating into evergreen notes?</li>
          <li>Which open questions deserve research time next week?</li>
        </ul>
      </div>
    </div>
  </div>
  <script>
    new Chart(document.getElementById('burstChart'), {{
      type: 'bar',
      data: {{
        labels: {domain_labels},
        datasets: [{{ data: {domain_values}, backgroundColor: ['#7aa2f7', '#bb9af7', '#9ece6a', '#7dcfff', '#ff9e64'], borderRadius: 6 }}]
      }},
      options: {{
        responsive: true, maintainAspectRatio: false, indexAxis: 'y',
        plugins: {{ legend: {{ display: false }} }},
        scales: {{ x: {{ grid: {{ color: '#2a2b3d' }}, ticks: {{ color: '#787c99' }} }}, y: {{ grid: {{ display: false }}, ticks: {{ color: '#c0caf5' }} }} }}
      }}
    }});
  </script>
</body>
</html>'''
    
    output_path = Path(vault_root) / "_dashboards" / "weekly-reflection.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 weekly_html.py <vault_root>")
        sys.exit(1)
    
    vault_root = sys.argv[1]
    
    if not Path(vault_root).exists():
        print(f"❌ Vault not found: {vault_root}")
        sys.exit(1)
    
    data = scan_weekly(vault_root)
    output = generate_html(data, vault_root)
    
    print(f"🔮 Weekly reflection updated")
    print(f"   {data['date_range']} | {data['modified_count']} notes | {len(data['high_arousal'])} peaks")
    print(f"   → {output}")


if __name__ == "__main__":
    main()
