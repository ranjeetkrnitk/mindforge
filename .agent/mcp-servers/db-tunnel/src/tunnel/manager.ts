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
 */
export async function openTunnel(
  envName: string,
  envConfig: SshTunnelEnvironment,
  localPortStart: number,
  connectTimeoutMs: number,
  totpCode?: string
): Promise<ActiveTunnel> {
  if (activeTunnels.has(envName)) {
    return activeTunnels.get(envName)!;
  }

  const { ssh, db } = envConfig;

  const sshPassword = await getSshPassword(envName);
  if (!sshPassword) {
    throw new Error(
      `No SSH password found for "${envName}". Run set_credential first:\n` +
      `  set_credential({ env: "${envName}", kind: "ssh-password", value: "..." })`
    );
  }

  let finalPassword = sshPassword;

  if (ssh.auth === "totp") {
    let code = totpCode;
    if (!code) {
      const secret = await getTotpSecret(envName);
      if (secret) {
        code = generateTotp(secret);
      } else {
        throw new Error(
          `PROD environment "${envName}" requires TOTP.\n` +
          `Option 1 (automated): Store TOTP secret via set_credential({ env: "${envName}", kind: "totp-secret", value: "BASE32SECRET" })\n` +
          `Option 2 (manual):    Pass totp_code parameter to connect()`
        );
      }
    }
    // Many SSH servers accept password+TOTP concatenated, or password then keyboard-interactive TOTP.
    // We handle keyboard-interactive below for TOTP.
    finalPassword = sshPassword;
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
      connectConfig.password = finalPassword;
    } else if (ssh.auth === "totp") {
      // Use keyboard-interactive for TOTP (password first, then TOTP code)
      connectConfig.password = finalPassword;
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

      let resolvedTotpCode = totpCode;
      sshClient.on("keyboard-interactive", (_name, _instructions, _lang, prompts, finish) => {
        const responses: string[] = prompts.map((prompt) => {
          const lc = prompt.prompt.toLowerCase();
          if (lc.includes("password")) return finalPassword;
          if (lc.includes("verification") || lc.includes("otp") || lc.includes("token") || lc.includes("code")) {
            return resolvedTotpCode ?? "";
          }
          return "";
        });
        finish(responses);
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
