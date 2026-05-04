import { getConnection } from "../db/connection.js";
import { getDefaults } from "../config/loader.js";

const DANGEROUS_PATTERN = /^\s*(drop|truncate|delete\s+from|alter\s+table|create\s+table|grant|revoke)/i;

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

  if (!allowMutations && DANGEROUS_PATTERN.test(trimmed)) {
    throw new Error(
      `Potentially destructive statement detected. Pass allow_mutations: true to proceed.\nSQL: ${trimmed.slice(0, 120)}`
    );
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
    columns: result.columns,
    rows: result.rows,
    rowCount: result.rows.length,
    truncated,
    truncatedAt: truncated ? limit : undefined,
    durationMs,
    sql: safeSql,
  };
}
