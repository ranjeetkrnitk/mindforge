import pg from "pg";
import mysql from "mysql2/promise";
import type { DbConfig } from "../config/types.js";
import { getDbPassword } from "../credentials/keychain.js";

export interface DbConnection {
  env: string;
  dbType: DbConfig["type"];
  query: (sql: string, params?: unknown[]) => Promise<{ columns: string[]; rows: unknown[][] }>;
  listSchemas: () => Promise<string[]>;
  listTables: (schema: string) => Promise<string[]>;
  describeTable: (schema: string, table: string) => Promise<ColumnInfo[]>;
  close: () => Promise<void>;
}

export interface ColumnInfo {
  column: string;
  type: string;
  nullable: boolean;
  default: string | null;
  primaryKey: boolean;
}

const activeConnections = new Map<string, DbConnection>();

export async function openConnection(
  envName: string,
  dbConfig: DbConfig,
  localPort: number,
  connectTimeoutMs: number
): Promise<DbConnection> {
  if (activeConnections.has(envName)) {
    return activeConnections.get(envName)!;
  }

  const dbPassword = await getDbPassword(envName);

  if (dbConfig.type === "postgresql") {
    const pool = new pg.Pool({
      host: "127.0.0.1",
      port: localPort,
      database: dbConfig.database,
      user: dbConfig.user,
      password: dbPassword ?? undefined,
      connectionTimeoutMillis: connectTimeoutMs,
      max: 3,
    });

    const conn: DbConnection = {
      env: envName,
      dbType: "postgresql",
      async query(sql, params = []) {
        const result = await pool.query(sql, params as pg.QueryConfigValues<unknown[]>);
        const columns = result.fields.map((f) => f.name);
        const rows = result.rows.map((row) => columns.map((col) => row[col]));
        return { columns, rows };
      },
      async listSchemas() {
        const result = await pool.query(
          `SELECT schema_name FROM information_schema.schemata
           WHERE schema_name NOT IN ('pg_catalog','information_schema','pg_toast')
           ORDER BY schema_name`
        );
        return result.rows.map((r) => r.schema_name as string);
      },
      async listTables(schema) {
        const result = await pool.query(
          `SELECT table_name FROM information_schema.tables
           WHERE table_schema = $1 AND table_type = 'BASE TABLE'
           ORDER BY table_name`,
          [schema]
        );
        return result.rows.map((r) => r.table_name as string);
      },
      async describeTable(schema, table) {
        const result = await pool.query(
          `SELECT
             c.column_name,
             c.data_type,
             c.is_nullable,
             c.column_default,
             CASE WHEN pk.column_name IS NOT NULL THEN true ELSE false END AS is_pk
           FROM information_schema.columns c
           LEFT JOIN (
             SELECT ku.column_name
             FROM information_schema.table_constraints tc
             JOIN information_schema.key_column_usage ku
               ON tc.constraint_name = ku.constraint_name
               AND tc.table_schema = ku.table_schema
             WHERE tc.constraint_type = 'PRIMARY KEY'
               AND tc.table_schema = $1 AND tc.table_name = $2
           ) pk ON c.column_name = pk.column_name
           WHERE c.table_schema = $1 AND c.table_name = $2
           ORDER BY c.ordinal_position`,
          [schema, table]
        );
        return result.rows.map((r) => ({
          column: r.column_name as string,
          type: r.data_type as string,
          nullable: r.is_nullable === "YES",
          default: (r.column_default as string) ?? null,
          primaryKey: r.is_pk as boolean,
        }));
      },
      async close() {
        await pool.end();
        activeConnections.delete(envName);
      },
    };

    activeConnections.set(envName, conn);
    return conn;
  }

  if (dbConfig.type === "mysql") {
    const pool = mysql.createPool({
      host: "127.0.0.1",
      port: localPort,
      database: dbConfig.database,
      user: dbConfig.user,
      password: dbPassword ?? undefined,
      connectTimeout: connectTimeoutMs,
      waitForConnections: true,
      connectionLimit: 3,
    });

    const conn: DbConnection = {
      env: envName,
      dbType: "mysql",
      async query(sql, params = []) {
        const [rows, fields] = await pool.query(sql, params);
        const fieldList = (fields as mysql.FieldPacket[]) ?? [];
        const columns = fieldList.map((f) => f.name);
        const data = (rows as Record<string, unknown>[]).map((row) =>
          columns.map((col) => row[col])
        );
        return { columns, rows: data };
      },
      async listSchemas() {
        const [rows] = await pool.query(
          `SELECT schema_name FROM information_schema.schemata
           WHERE schema_name NOT IN ('information_schema','performance_schema','mysql','sys')
           ORDER BY schema_name`
        );
        return (rows as { schema_name: string }[]).map((r) => r.schema_name);
      },
      async listTables(schema) {
        const [rows] = await pool.query(
          `SELECT table_name FROM information_schema.tables
           WHERE table_schema = ? AND table_type = 'BASE TABLE'
           ORDER BY table_name`,
          [schema]
        );
        return (rows as { table_name: string }[]).map((r) => r.table_name);
      },
      async describeTable(schema, table) {
        const [rows] = await pool.query(
          `SELECT
             COLUMN_NAME as col,
             COLUMN_TYPE as type,
             IS_NULLABLE as nullable,
             COLUMN_DEFAULT as def,
             COLUMN_KEY as col_key
           FROM information_schema.COLUMNS
           WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
           ORDER BY ORDINAL_POSITION`,
          [schema, table]
        );
        return (rows as { col: string; type: string; nullable: string; def: string | null; col_key: string }[]).map((r) => ({
          column: r.col,
          type: r.type,
          nullable: r.nullable === "YES",
          default: r.def,
          primaryKey: r.col_key === "PRI",
        }));
      },
      async close() {
        await pool.end();
        activeConnections.delete(envName);
      },
    };

    activeConnections.set(envName, conn);
    return conn;
  }

  throw new Error(`Unsupported database type: ${(dbConfig as DbConfig).type}`);
}

export function getConnection(envName: string): DbConnection | undefined {
  return activeConnections.get(envName);
}

export function closeConnection(envName: string): Promise<void> | undefined {
  return activeConnections.get(envName)?.close();
}

export function listActiveConnections(): string[] {
  return [...activeConnections.keys()];
}
