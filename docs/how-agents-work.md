# How Agents Work

An agent is a role definition. It answers: who is performing the task?

## Anatomy

```
agent-name/
├── AGENT.md          # Role, capabilities, constraints, handoff logic
└── system-prompt.md  # Drop-in system prompt for any LLM
```

## Adding an Agent

1. Create `.agent/agents/<agent-name>/`
2. Fill `AGENT.md` — define role, capabilities, constraints
3. Write `system-prompt.md` — ready to paste into any LLM system prompt field
4. List which skills this agent uses

---

# How Plugins Work

A plugin modifies how an agent behaves — output format, reasoning style,
verbosity, or constraints. Plugins don't define what an agent does, just *how*.

## Anatomy

```
plugin-name/
├── PLUGIN.md         # What this plugin changes, when to load it
└── inject.md         # The raw prompt snippet to inject
```

## Inject Points

- `prefix` — inject before all other instructions
- `suffix` — inject after all other instructions
- `override` — replace a named section of the system prompt
- `filter` — post-process output before returning to user

## Adding a Plugin

1. Create `.agent/plugins/<plugin-name>/`
2. Fill `PLUGIN.md` — define what changes, when to load, inject point
3. Write `inject.md` — the actual text to inject (keep it tight)

---

# How MCP Servers Work

An MCP server exposes external tools to agents via the Model Context Protocol.

## Anatomy

```
server-name/
├── MCP.md            # What this server exposes, setup instructions
├── server.json       # MCP manifest (tools, transport, auth)
└── docs/
    └── usage.md      # Tool-by-tool usage reference
```

## Adding an MCP Server

1. Create `.agent/mcp-servers/<server-name>/`
2. Fill `MCP.md` — describe tools, setup, auth
3. Write `server.json` — the MCP manifest
4. Document each tool in `docs/usage.md`
5. Test with your agent of choice before committing
