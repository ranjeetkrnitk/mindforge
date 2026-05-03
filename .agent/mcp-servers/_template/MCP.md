---
name: "{{MCP_SERVER_NAME}}"
version: 0.1.0
description: >
  What external service or tool this MCP server exposes to agents.
  When should an agent use this server?
service: "{{e.g. github | notion | obsidian | filesystem | custom}}"
transport: "{{stdio | sse | http}}"
auth: "{{none | api-key | oauth}}"
---

# {{MCP_SERVER_NAME}} MCP Server

## What This Exposes

{{Describe what tools/resources this MCP server makes available to agents.
Be specific — list the operations agents can perform.}}

## Tools

| Tool Name | Description | Input | Output |
|---|---|---|---|
| `{{tool_name}}` | {{what it does}} | `{{input schema}}` | `{{output schema}}` |
| `{{tool_name}}` | {{what it does}} | `{{input schema}}` | `{{output schema}}` |

## Setup

```bash
# Install dependencies
{{install command}}

# Configure
cp .env.example .env
# Edit .env with your credentials

# Run the server
{{start command}}
```

## Authentication

Auth type: `{{none | api-key | oauth}}`

```env
# .env
{{ENV_VAR_NAME}}=your-key-here
```

## Usage with Agents

To enable this server for an agent, add to the agent's config:

```json
{
  "mcp_servers": [
    {
      "name": "{{MCP_SERVER_NAME}}",
      "transport": "{{stdio | sse}}",
      "command": "{{start command}}"
    }
  ]
}
```

## Limitations

- {{Known limitation 1}}
- {{Known limitation 2}}

---

See `server.json` for the full MCP manifest and `docs/` for tool-specific usage.
