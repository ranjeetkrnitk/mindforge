---
name: reflect
version: 0.2.0
description: >
  Vault retrospective grounded in Complementary Learning Systems (CLS) theory
  and Personal Knowledge Graph (PKG) research. Summarizes activity, surfaces
  consolidation candidates, tracks emotional patterns.
  Triggers: "reflect", "weekly", "monthly", "vault insights".
agent: agnostic
research: RESEARCH.md
---

# /reflect

## Load Order
1. `../_shared/conventions.md` — cross-skill standards
2. `REF.md` — skill-specific procedures
3. `config/user.md` — vault path
4. `config/settings.md` — thresholds

## Setup
Check `config/user.md`. If empty:
1. Try copying from `~/.copilot/skills/memorize/config/user.md`
2. Or ask: *"Vault path?"*
3. Show: `💡 /add-dir ~/.copilot/skills` and `/add-dir <vault>`

## Modes
| Mode | Trigger | Prompt |
|------|---------|--------|
| weekly | "weekly", "last week" | `prompts/weekly.md` |
| monthly | "monthly", "this month" | `prompts/monthly.md` |
| custom | "reflect on [dates]" | `prompts/custom.md` |
| insights | "vault insights" | `prompts/insights.md` |

## Key Features
- **CLS signals**: replay events, promotion candidates, maturity progression
- **Spaced rep**: dormant topics, review suggestions
- **Graph metrics**: hub/bridge/orphan scores
- **Emotion tracking**: arousal peaks, valence trends
- **Health score**: 0-100 with recommendations

## Output Conventions
- Emoji section headers for scannability
- Bar charts for distributions
- Comparison deltas with ↑↓ arrows
- 2-3 reflection prompts per summary
- Wikilinks for actionable notes
