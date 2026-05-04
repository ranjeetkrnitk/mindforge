import { closeTunnel } from "../tunnel/manager.js";
import { closeConnection } from "../db/connection.js";

export async function disconnect(envName: string) {
  let tunnelClosed = false;
  try {
    await closeConnection(envName);
  } finally {
    // Always close the tunnel even if DB disconnect throws or hangs
    tunnelClosed = closeTunnel(envName);
  }

  return {
    disconnected: true,
    env: envName,
    message: `Disconnected from "${envName}"${tunnelClosed ? " and closed SSH tunnel" : ""}`,
  };
}
