# /reflect - Vault Retrospective

> Research-backed insights from your Obsidian vault.

## Research Foundation
| Theory | Paper | Application |
|--------|-------|-------------|
| CLS | McClelland 1995 | Consolidation signals |
| Spaced Rep | Latimier 2020 | Dormant detection |
| PKG | Balog 2024 | Hub/bridge analysis |

See `RESEARCH.md` for citations.

## Modes
| Trigger | Mode | What |
|---------|------|------|
| "weekly", "last week" | weekly | 7-day summary + consolidation |
| "monthly" | monthly | Trends + progression |
| "reflect on [dates]" | custom | Period comparison |
| "vault insights" | insights | Structure + health score |

## Key Metrics
| Metric | Formula | Purpose |
|--------|---------|---------|
| Hub | incoming_links | Knowledge anchors |
| Bridge | cross_domain/total | Connectors |
| Orphan Risk | age × 0.1 / (links+1) | Integration targets |
| Consolidation | 3+ links, 7+ days | Promotion candidates |

## Features
- 🔄 CLS consolidation signals (replay, promotion)
- 😴 Dormant topic detection (14+ days)
- 💚 Emotion tracking (arousal peaks, valence trends)
- 🏥 Vault health score (0-100)
- 💡 Reflection prompts

## Permissions
```bash
/add-dir ~/.copilot/skills
/add-dir /path/to/vault
```

## Integration
Shares vault path with `/memorize`. Uses same emotion schema (arousal, valence).
