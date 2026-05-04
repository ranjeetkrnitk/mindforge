import { getEnvironment, getDefaults } from "../config/loader.js";
import { openTunnel } from "../tunnel/manager.js";
import { openConnection } from "../db/connection.js";

export async function connect(envName: string, totpCode?: string) {
  const env = getEnvironment(envName);
  const defaults = getDefaults();

  let localPort: number;

  if (env.type === "ssh-tunnel") {
    const tunnel = await openTunnel(
      envName,
      env,
      defaults.tunnelLocalPortStart,
      defaults.connectTimeoutMs,
      totpCode
    );
    localPort = tunnel.localPort;
  } else {
    // Direct connection — use the configured port directly
    localPort = env.db.port;
  }

  const conn = await openConnection(
    envName,
    env.db,
    localPort,
    defaults.connectTimeoutMs
  );

  return {
    connected: true,
    env: envName,
    dbType: conn.dbType,
    message: `Connected to "${envName}" (${conn.dbType}) ${env.type === "ssh-tunnel" ? `via SSH tunnel on local port ${localPort}` : "directly"}`,
  };
}
