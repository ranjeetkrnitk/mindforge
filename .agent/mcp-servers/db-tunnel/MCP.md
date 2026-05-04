---
name: "db-tunnel"
version: 0.1.0
description: >
  MCP server for querying DEV, SEMI, and PROD databases via SSH tunnels,
  or direct connections for local databases. Handles password auth (DEV/SEMI)
  and TOTP 2FA (PROD) automatically using credentials stored in OS Keychain.
  Supports PostgreSQL and MySQL.
service: "custom"
transport: "stdio"
auth: "os-keychain"
---

# db-tunnel MCP Server

## What This Exposes

Gives agents direct access to your databases across environments. Agents can:

- Open SSH tunnels (with password or TOTP 2FA)
- Run parameterized SQL queries safely
- Explore schemas and table structures
- Store passwords/TOTP secrets in OS Keychain on first use

## Tools

| Tool Name | Description | Key Inputs |
|---|---|---|
| `list_environments` | List configured envs + connection status | — |
| `connect` | Open SSH tunnel + DB connection | `env`, `totp_code?` |
| `disconnect` | Close tunnel + connection | `env` |
| `query` | Run SQL, get JSON results | `env`, `sql`, `params?`, `allow_mutations?` |
| `list_schemas` | List schemas/databases | `env` |
| `list_tables` | List tables in a schema | `env`, `schema` |
| `describe_table` | Get column info, types, PKs | `env`, `schema`, `table` |
| `set_credential` | Save password/TOTP to Keychain | `env`, `kind`, `value` |
| `delete_credential` | Remove a Keychain credential | `env`, `kind` |

## Setup

```bash
# 1. Navigate to the server directory
cd .agent/mcp-servers/db-tunnel

# 2. Install dependencies
npm install

# 3. Copy and configure your environments
cp config.example.json config.json
# Edit config.json — fill in your real SSH hosts, DB hosts, ports, usernames

# 4. Store credentials in OS Keychain (first time per environment)
# The agent will call set_credential, or you can do it via CLI for testing:
node -e "
import('./dist/index.js')  # build first
"
# Easier: just start the MCP server and have the agent call set_credential
```

## First-Time Credential Setup

When you first use an environment, ask the agent:

> "Set my dev SSH password to 'mypassword' for the dev environment"

The agent will call:
```json
set_credential({ "env": "dev", "kind": "ssh-password", "value": "mypassword" })
set_credential({ "env": "dev", "kind": "db-password", "value": "mydbpassword" })
```

For PROD with TOTP (fully automated):
```json
set_credential({ "env": "prod", "kind": "ssh-password", "value": "mypassword" })
set_credential({ "env": "prod", "kind": "totp-secret", "value": "BASE32SECRETFROMAPP" })
set_credential({ "env": "prod", "kind": "db-password", "value": "mydbpassword" })
```

If you don't store the TOTP secret, the agent will ask you for the 6-digit code each time.

## Authentication Flow

| Env | Flow |
|---|---|
| DEV/SEMI | SSH password from Keychain → tunnel → DB password from Keychain |
| PROD | SSH password + auto-generated TOTP → tunnel → DB password from Keychain |
| Local | Direct TCP → DB password from Keychain (optional) |

## Adding to Claude Desktop

```json
{
  "mcpServers": {
    "db-tunnel": {
      "command": "/Users/rkuma05/.nvm/versions/node/v20.20.0/bin/node",
      "args": ["/Users/rkuma05/repos/ranjeet/mindforge/.agent/mcp-servers/db-tunnel/dist/index.js"]
    }
  }
}
```

## Adding to GitHub Copilot (VS Code)

In `.vscode/mcp.json`:
```json
{
  "servers": {
    "db-tunnel": {
      "type": "stdio",
      "command": "/Users/rkuma05/.nvm/versions/node/v20.20.0/bin/node",
      "args": ["${workspaceFolder}/.agent/mcp-servers/db-tunnel/dist/index.js"]
    }
  }
}
```

## Security

- `config.json` is gitignored — real hosts/ports never committed
- Passwords and TOTP secrets are stored in OS Keychain (macOS Keychain / libsecret on Linux)
- Query results are capped at 500 rows by default (configurable in `config.json`)
- Destructive SQL requires explicit `allow_mutations: true`
- No credentials are ever logged

## Limitations

- PROD TOTP assumes keyboard-interactive SSH auth. If your server uses a different 2FA mechanism, update `tunnel/manager.ts`.
- SSH agent forwarding not supported (password/keyboard-interactive only).
- No SSL/TLS configuration for DB connections yet (add `ssl` option to pg/mysql2 pools if needed).
