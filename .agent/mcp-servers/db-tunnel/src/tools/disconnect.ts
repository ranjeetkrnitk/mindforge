import { closeTunnel } from "../tunnel/manager.js";
import { closeConnection } from "../db/connection.js";

export async function disconnect(envName: string) {
  await closeConnection(envName);
  const tunnelClosed = closeTunnel(envName);

  return {
    disconnected: true,
    env: envName,
    message: `Disconnected from "${envName}"${tunnelClosed ? " and closed SSH tunnel" : ""}`,
  };
}
