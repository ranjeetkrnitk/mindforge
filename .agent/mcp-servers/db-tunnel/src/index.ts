import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { listEnvironments } from "./tools/list-environments.js";
import { connect } from "./tools/connect.js";
import { disconnect } from "./tools/disconnect.js";
import { query } from "./tools/query.js";
import { listSchemas, listTables, describeTable } from "./tools/schema.js";
import { setCredential, deleteCredentialTool } from "./tools/set-credential.js";

const server = new McpServer({
  name: "db-tunnel",
  version: "0.1.0",
});

// ── list_environments ──────────────────────────────────────────────────────────
server.tool(
  "list_environments",
  "List all configured database environments and their current connection status.",
  {},
  async () => {
    const result = listEnvironments();
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── connect ────────────────────────────────────────────────────────────────────
server.tool(
  "connect",
  "Open an SSH tunnel (if needed) and database connection for the given environment. For PROD (TOTP), either store the TOTP secret via set_credential first (fully automated) or pass totp_code manually.",
  {
    env: z.string().describe("Environment name (e.g. dev, semi, prod, local)"),
    totp_code: z.string().optional().describe("6-digit TOTP code for PROD environments (only needed if TOTP secret is not stored in keychain)"),
  },
  async ({ env, totp_code }) => {
    const result = await connect(env, totp_code);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── disconnect ─────────────────────────────────────────────────────────────────
server.tool(
  "disconnect",
  "Close the database connection and SSH tunnel for the given environment.",
  {
    env: z.string().describe("Environment name"),
  },
  async ({ env }) => {
    const result = await disconnect(env);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── query ──────────────────────────────────────────────────────────────────────
server.tool(
  "query",
  "Execute a SQL query on a connected environment. SELECT results are automatically capped at the configured row limit. Destructive statements (DROP, TRUNCATE, DELETE, ALTER, GRANT, REVOKE) return a requires_confirmation warning first — you MUST show the warning to the user and ask for explicit confirmation before calling again with allow_mutations: true.",
  {
    env: z.string().describe("Environment name"),
    sql: z.string().describe("SQL query to execute"),
    params: z.array(z.unknown()).optional().describe("Parameterized query values (safe, prevents SQL injection)"),
    allow_mutations: z.boolean().optional().describe("Set true to allow DROP/TRUNCATE/DELETE/ALTER statements"),
    row_limit: z.number().optional().describe("Override the default row limit for this query"),
  },
  async ({ env, sql, params, allow_mutations, row_limit }) => {
    const result = await query(env, sql, params as unknown[], allow_mutations, row_limit);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── list_schemas ───────────────────────────────────────────────────────────────
server.tool(
  "list_schemas",
  "List all schemas (PostgreSQL) or databases (MySQL) in the connected environment.",
  {
    env: z.string().describe("Environment name"),
  },
  async ({ env }) => {
    const result = await listSchemas(env);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── list_tables ────────────────────────────────────────────────────────────────
server.tool(
  "list_tables",
  "List all tables in a given schema/database.",
  {
    env: z.string().describe("Environment name"),
    schema: z.string().describe("Schema name (PostgreSQL) or database name (MySQL)"),
  },
  async ({ env, schema }) => {
    const result = await listTables(env, schema);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── describe_table ─────────────────────────────────────────────────────────────
server.tool(
  "describe_table",
  "Get column definitions, types, nullability, defaults, and primary key info for a table.",
  {
    env: z.string().describe("Environment name"),
    schema: z.string().describe("Schema name"),
    table: z.string().describe("Table name"),
  },
  async ({ env, schema, table }) => {
    const result = await describeTable(env, schema, table);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── set_credential ─────────────────────────────────────────────────────────────
server.tool(
  "set_credential",
  "Save a credential for an environment to the OS Keychain. Run this once per environment on first setup. Kinds: ssh-password, db-password, totp-secret (base32 from authenticator app).",
  {
    env: z.string().describe("Environment name (e.g. dev, prod)"),
    kind: z.enum(["ssh-password", "db-password", "totp-secret"]).describe("What to store"),
    value: z.string().describe("The secret value (never stored in config files or git)"),
  },
  async ({ env, kind, value }) => {
    const result = await setCredential(env, kind, value);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── delete_credential ──────────────────────────────────────────────────────────
server.tool(
  "delete_credential",
  "Remove a stored credential from the OS Keychain (e.g. when a password changes).",
  {
    env: z.string().describe("Environment name"),
    kind: z.enum(["ssh-password", "db-password", "totp-secret"]).describe("Which credential to delete"),
  },
  async ({ env, kind }) => {
    const result = await deleteCredentialTool(env, kind);
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// ── Start ──────────────────────────────────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);
