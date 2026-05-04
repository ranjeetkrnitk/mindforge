import { getConnection } from "../db/connection.js";
import { getDefaults } from "../config/loader.js";

const DANGEROUS_OPS: Array<{ pattern: RegExp; label: string }> = [
  { pattern: /^\s*drop\s+/i,     label: "DROP" },
  { pattern: /^\s*truncate\s+/i, label: "TRUNCATE" },
  { pattern: /^\s*delete\s+/i,   label: "DELETE" },
  { pattern: /^\s*alter\s+/i,    label: "ALTER TABLE" },
  { pattern: /^\s*create\s+/i,   label: "CREATE TABLE" },
  { pattern: /^\s*grant\s+/i,    label: "GRANT" },
  { pattern: /^\s*revoke\s+/i,   label: "REVOKE" },
];

function detectDangerousOp(sql: string): string | null {
  for (const { pattern, label } of DANGEROUS_OPS) {
    if (pattern.test(sql)) return label;
  }
  return null;
}

export async function query(
  envName: string,
  sql: string,
  params: unknown[] = [],
  allowMutations = false,
  rowLimit?: number
) {
  const conn = getConnection(envName);
  if (!conn) {
    throw new Error(
      `Not connected to "${envName}". Call connect({ env: "${envName}" }) first.`
    );
  }

  const trimmed = sql.trim();
  const dangerousOp = detectDangerousOp(trimmed);

  if (dangerousOp && !allowMutations) {
    // Return a structured warning — do NOT execute. The agent must show this
    // to the user and ask for explicit confirmation before retrying with
    // allow_mutations: true.
    return {
      requires_confirmation: true,
      env: envName,
      dangerous_operation: dangerousOp,
      sql_to_run: trimmed,
      warning: [
        `⚠️  DESTRUCTIVE OPERATION DETECTED: ${dangerousOp}`,
        ``,
        `Environment : ${envName}`,
        `SQL         : ${trimmed}`,
        ``,
        `This statement can permanently delete or alter data.`,
        `Please confirm with the user before proceeding.`,
        `To execute, call query() again with allow_mutations: true.`,
      ].join("\n"),
    };
  }

  const defaults = getDefaults();
  const limit = rowLimit ?? defaults.queryRowLimit;

  // Inject LIMIT for SELECT queries to prevent runaway results
  let safeSql = trimmed;
  if (/^\s*select/i.test(trimmed) && !/\blimit\b/i.test(trimmed)) {
    safeSql = `${trimmed} LIMIT ${limit}`;
  }

  const start = Date.now();
  const result = await conn.query(safeSql, params);
  const durationMs = Date.now() - start;

  const truncated = result.rows.length === limit;

  return {
    env: envName,
    ...(dangerousOp ? { executed_destructive_operation: dangerousOp } : {}),
    columns: result.columns,
    rows: result.rows,
    rowCount: result.rows.length,
    truncated,
    truncatedAt: truncated ? limit : undefined,
    durationMs,
    sql: safeSql,
  };
}
