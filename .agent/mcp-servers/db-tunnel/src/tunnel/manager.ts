import { Client } from "ssh2";
import { createServer, type Server } from "net";
import type { SshTunnelEnvironment } from "../config/types.js";
import { getSshPassword, getTotpSecret } from "../credentials/keychain.js";
import { generateTotp } from "./totp.js";

export interface ActiveTunnel {
  env: string;
  localPort: number;
  close: () => void;
}

const activeTunnels = new Map<string, ActiveTunnel>();
// Tracks in-flight connect promises to prevent concurrent duplicate connections
const pendingTunnels = new Map<string, Promise<ActiveTunnel>>();

/** Find a free local port starting from a given base. */
function findFreePort(start: number): Promise<number> {
  return new Promise((resolve, reject) => {
    const server = createServer();
    server.listen(start, "127.0.0.1", () => {
      const port = (server.address() as { port: number }).port;
      server.close(() => resolve(port));
    });
    server.on("error", () => findFreePort(start + 1).then(resolve).catch(reject));
  });
}

/**
 * Open an SSH tunnel for the given environment.
 * Returns the local port that the DB is accessible on.
 * Concurrent calls for the same env share a single in-flight promise.
 */
export function openTunnel(
  envName: string,
  envConfig: SshTunnelEnvironment,
  localPortStart: number,
  connectTimeoutMs: number,
  totpCode?: string
): Promise<ActiveTunnel> {
  // Return existing tunnel immediately
  if (activeTunnels.has(envName)) {
    return Promise.resolve(activeTunnels.get(envName)!);
  }
  // Coalesce concurrent connect calls — only one SSH handshake per env
  if (pendingTunnels.has(envName)) {
    return pendingTunnels.get(envName)!;
  }

  const promise = _openTunnel(envName, envConfig, localPortStart, connectTimeoutMs, totpCode)
    .finally(() => pendingTunnels.delete(envName));

  pendingTunnels.set(envName, promise);
  return promise;
}

async function _openTunnel(
  envName: string,
  envConfig: SshTunnelEnvironment,
  localPortStart: number,
  connectTimeoutMs: number,
  totpCode?: string
): Promise<ActiveTunnel> {
  const { ssh, db } = envConfig;

  const sshPassword = await getSshPassword(envName);
  if (!sshPassword) {
    throw new Error(
      `No SSH password found for "${envName}". Run set_credential first:\n` +
      `  set_credential({ env: "${envName}", kind: "ssh-password", value: "..." })`
    );
  }

  // For TOTP: validate secret is available, but do NOT generate the code yet —
  // codes expire every 30s and SSH negotiation can take 5-15s. The code is
  // generated inside the keyboard-interactive callback, right when needed.
  if (ssh.auth === "totp" && !totpCode) {
    const secret = await getTotpSecret(envName);
    if (!secret) {
      throw new Error(
        `PROD environment "${envName}" requires TOTP.\n` +
        `Option 1 (automated): Store TOTP secret via set_credential({ env: "${envName}", kind: "totp-secret", value: "BASE32SECRET" })\n` +
        `Option 2 (manual):    Pass totp_code parameter to connect()`
      );
    }
  }

  const localPort = await findFreePort(localPortStart);

  return new Promise((resolve, reject) => {
    const sshClient = new Client();
    const proxyServers: Server[] = [];

    const cleanup = () => {
      for (const srv of proxyServers) srv.close();
      sshClient.end();
      activeTunnels.delete(envName);
    };

    const timeout = setTimeout(() => {
      cleanup();
      reject(new Error(`SSH connection to "${envName}" timed out after ${connectTimeoutMs}ms`));
    }, connectTimeoutMs);

    sshClient.on("ready", () => {
      clearTimeout(timeout);

      // Detect tunnel drop after it's established and clean up stale map entry
      sshClient.on("close", () => cleanup());
      sshClient.on("end", () => cleanup());

      // Create a local TCP server that forwards to the remote DB
      const proxyServer = createServer((localSocket) => {
        sshClient.forwardOut(
          "127.0.0.1",
          localPort,
          db.host,
          db.port,
          (err, stream) => {
            if (err) {
              localSocket.destroy();
              return;
            }
            localSocket.pipe(stream);
            stream.pipe(localSocket);
            localSocket.on("close", () => stream.close());
            stream.on("close", () => localSocket.destroy());
          }
        );
      });

      proxyServer.listen(localPort, "127.0.0.1", () => {
        proxyServers.push(proxyServer);
        const tunnel: ActiveTunnel = { env: envName, localPort, close: cleanup };
        activeTunnels.set(envName, tunnel);
        resolve(tunnel);
      });

      proxyServer.on("error", (err) => {
        cleanup();
        reject(new Error(`Tunnel proxy server error: ${err.message}`));
      });
    });

    sshClient.on("error", (err) => {
      clearTimeout(timeout);
      cleanup();
      reject(new Error(`SSH error for "${envName}": ${err.message}`));
    });

    const connectConfig: Parameters<Client["connect"]>[0] = {
      host: ssh.host,
      port: ssh.port,
      username: ssh.user,
      readyTimeout: connectTimeoutMs,
    };

    if (ssh.auth === "password") {
      connectConfig.password = sshPassword;
    } else if (ssh.auth === "totp") {
      connectConfig.password = sshPassword;
      connectConfig.tryKeyboard = true;
      connectConfig.authHandler = (methodsLeft, _partial, cb) => {
        if (!methodsLeft || methodsLeft.includes("keyboard-interactive")) {
          cb("keyboard-interactive");
        } else if (methodsLeft.includes("password")) {
          cb("password");
        } else {
          cb(false as never);
        }
      };

      sshClient.on("keyboard-interactive", (_name, _instructions, _lang, prompts, finish) => {
        // Resolve promises in the callback — getTotpSecret is sync-cached after
        // the check above, so we use a sync-style resolution here via a void async wrapper
        void (async () => {
          const responses: string[] = await Promise.all(
            prompts.map(async (prompt) => {
              const lc = prompt.prompt.toLowerCase();
              if (lc.includes("password")) return sshPassword;
              if (lc.includes("verification") || lc.includes("otp") || lc.includes("token") || lc.includes("code")) {
                if (totpCode) return totpCode;
                // Generate fresh code right here — maximizes remaining window
                const secret = await getTotpSecret(envName);
                return secret ? generateTotp(secret) : "";
              }
              return "";
            })
          );
          finish(responses);
        })();
      });
    }

    sshClient.connect(connectConfig);
  });
}

export function closeTunnel(envName: string): boolean {
  const tunnel = activeTunnels.get(envName);
  if (!tunnel) return false;
  tunnel.close();
  return true;
}

export function getTunnel(envName: string): ActiveTunnel | undefined {
  return activeTunnels.get(envName);
}

export function listActiveTunnels(): string[] {
  return [...activeTunnels.keys()];
}

