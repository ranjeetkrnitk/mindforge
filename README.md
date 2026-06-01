# mindforge — Agent-Agnostic Second Brain

Personal repository of skills for knowledge management.
Works with Claude, GPT, Cursor, Gemini, or any LLM that reads markdown.

## Skills

| Skill | Purpose | Triggers |
|-------|---------|----------|
| **memorize** | Capture, consolidate, recall | "memorize", "consolidate", "recall" |
| **reflect** | Vault analysis, insights | "weekly", "monthly", "vault insights" |
| **jobhunt** | Job search pipeline - scan, evaluate, tailor, apply | "job search", "find jobs", "evaluate job", "track applications" |

## Core Features
- **CLS Theory**: fast capture (episodes) → slow consolidation (concepts)
- **Emotion Tracking**: arousal/valence tags for mood-congruent recall
- **Graph Analysis**: hubs, bridges, orphans, health score
- **Spaced Repetition**: dormant detection, review scheduling

## Quickstart

```bash
# Capture with emotion
"memorize: Just had a breakthrough moment understanding X!"

# Weekly reflection
"reflect on last week"

# Vault health check
"vault insights"
```

## Structure

```
.agent/skills/
├── memorize/    # Capture, consolidate, harvest, recall
├── reflect/     # Weekly, monthly, custom, insights
└── jobhunt/     # Scan, evaluate, tailor, cover-letter, track, outreach, apply
```

## Research Foundation
- McClelland 1995 (CLS Theory)
- Latimier 2020 (Spaced Repetition)
- Balog 2024 (Personal Knowledge Graphs)
