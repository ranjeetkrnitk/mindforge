# ranjeet — Agent-Agnostic Second Brain

A personal repository of skills, agents, plugins, and MCP server configs.
Everything here is agent-agnostic — works with Claude, GPT, Cursor, Gemini,
or any LLM that can read markdown.

## Structure

```
.agent/
├── skills/        # Task instructions — "how to do X"
├── agents/        # Persona definitions — "who does X"
├── plugins/       # Behavioral modifiers — "how agent acts"
└── mcp-servers/   # Tool connectors — "what agent can access"

helpers/           # Implementation scripts (Python, bash)
docs/              # Architecture decisions and guides
```

## Philosophy

Built on **Complementary Learning Systems (CLS) theory** — fast capture,
slow consolidation, graph-based linking. See `docs/architecture.md`.

## Quickstart

```bash
# Capture a new memory
./helpers/cli/run.sh skill memorize capture "I learned that X causes Y"

# Consolidate recent notes
./helpers/cli/run.sh skill memorize consolidate

# Remap an existing Obsidian vault
./helpers/cli/run.sh skill memorize remap --dry-run
```

## Categories

| Category | Count | Docs |
|---|---|---|
| Skills | 1 | [how-skills-work.md](docs/how-skills-work.md) |
| Agents | 0 | [how-agents-work.md](docs/how-agents-work.md) |
| Plugins | 0 | [how-plugins-work.md](docs/how-plugins-work.md) |
| MCP Servers | 0 | [how-mcp-servers-work.md](docs/how-mcp-servers-work.md) |

## Contributing

See [docs/contributing.md](docs/contributing.md) for how to add a new skill,
agent, plugin, or MCP server.
