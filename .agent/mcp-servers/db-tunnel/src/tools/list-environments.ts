import { loadConfig } from "../config/loader.js";
import { listActiveTunnels } from "../tunnel/manager.js";
import { listActiveConnections } from "../db/connection.js";

export function listEnvironments() {
  const config = loadConfig();
  const tunnels = new Set(listActiveTunnels());
  const connections = new Set(listActiveConnections());

  const envs = Object.entries(config.environments).map(([name, env]) => ({
    name,
    label: env.label,
    type: env.type,
    dbType: env.db.type,
    tunnelActive: tunnels.has(name),
    dbConnected: connections.has(name),
    status: connections.has(name) ? "connected" : tunnels.has(name) ? "tunnel-open" : "disconnected",
    ...(env.type === "ssh-tunnel"
      ? { sshAuth: env.ssh.auth, sshHost: env.ssh.host }
      : { direct: true }),
  }));

  return {
    environments: envs,
    hint: "Use connect({ env }) to open a connection before running queries.",
  };
}
