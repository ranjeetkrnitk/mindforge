# mindforge - Agent-Agnostic Second Brain

Personal repository of skills, agents, plugins, and MCP servers for knowledge management.
Works with Claude, GPT, Cursor, Gemini, or any LLM that reads markdown.

## Skills

| Skill | Purpose | Triggers |
|-------|---------|----------|
| **memorize** | Capture, consolidate, recall | "memorize", "consolidate", "recall" |
| **reflect** | Vault analysis, insights | "weekly", "monthly", "vault insights" |
| **jobhunt** | Job search pipeline - scan, evaluate, tailor, apply | "job search", "find jobs", "evaluate job", "track applications" |
| **dashboard** | Refresh vault health dashboard with metrics | "dashboard", "vault stats", "refresh dashboard" |
| **ideate** | Project planning - elicit requirements, PRD, implementation plans | "plan project", "new idea", "elicit requirements" |

## MCP Servers

| Server | Purpose |
|--------|---------|
| **db-tunnel** | Query DEV/SEMI/PROD databases via SSH tunnels; handles password auth and TOTP 2FA using OS Keychain |

## Core Features
- **CLS Theory**: fast capture (episodes) -> slow consolidation (concepts)
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
"vault stats"

# Plan a new project
"plan project: <idea>"

# Run a skill directly
./helpers/cli/run.sh skill memorize capture "I learned X"
```

## Structure

```
.agent/
├── skills/
│   ├── memorize/    # Capture, consolidate, harvest, recall
│   ├── reflect/     # Weekly, monthly, custom, insights
│   ├── jobhunt/     # Scan, evaluate, tailor, cover-letter, track, outreach, apply
│   ├── dashboard/   # Vault health metrics and scores
│   └── ideate/      # Requirements elicitation, PRD, implementation planning
├── agents/          # Role/persona definitions with system prompts
├── plugins/         # Behavioral modifiers (output format, verbosity, style)
└── mcp-servers/
    └── db-tunnel/   # SSH tunnel + direct DB access (Postgres, MySQL)

helpers/
├── cli/run.sh       # Universal entry point for all skills, agents, plugins
├── vault/audit.py   # Vault health auditing utilities
└── graph/link_strength.py  # Link graph metrics

docs/
├── architecture.md       # Four-layer design and CLS theory
├── contributing.md       # Contribution checklists and commit format
├── how-skills-work.md    # Skill anatomy and agent usage flow
└── how-agents-work.md    # Agent and plugin anatomy
```

## Research Foundation
- McClelland 1995 (CLS Theory)
- Latimier 2020 (Spaced Repetition)
- Balog 2024 (Personal Knowledge Graphs)
