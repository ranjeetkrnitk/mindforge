import { getConnection } from "../db/connection.js";

export async function listSchemas(envName: string) {
  const conn = getConnection(envName);
  if (!conn) {
    throw new Error(`Not connected to "${envName}". Call connect first.`);
  }
  const schemas = await conn.listSchemas();
  return { env: envName, schemas };
}

export async function listTables(envName: string, schema: string) {
  const conn = getConnection(envName);
  if (!conn) {
    throw new Error(`Not connected to "${envName}". Call connect first.`);
  }
  const tables = await conn.listTables(schema);
  return { env: envName, schema, tables };
}

export async function describeTable(envName: string, schema: string, table: string) {
  const conn = getConnection(envName);
  if (!conn) {
    throw new Error(`Not connected to "${envName}". Call connect first.`);
  }
  const columns = await conn.describeTable(schema, table);
  return { env: envName, schema, table, columns };
}
