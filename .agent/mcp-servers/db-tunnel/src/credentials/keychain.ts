import { execFile } from "child_process";
import { promisify } from "util";
import { platform } from "os";

const exec = promisify(execFile);
const SERVICE = "mcp-db-tunnel";
const IS_MACOS = platform() === "darwin";

/**
 * Thin OS-keychain wrapper.
 * - macOS: uses the built-in `security` CLI (no native binaries, arm64-safe)
 * - Linux: uses `secret-tool` from libsecret (install: `apt install libsecret-tools`)
 */

async function keychainGet(account: string): Promise<string | null> {
  try {
    if (IS_MACOS) {
      const { stdout } = await exec("security", [
        "find-generic-password",
        "-s", SERVICE,
        "-a", account,
        "-w",
      ]);
      return stdout.trim() || null;
    } else {
      const { stdout } = await exec("secret-tool", [
        "lookup", "service", SERVICE, "account", account,
      ]);
      return stdout.trim() || null;
    }
  } catch {
    return null;
  }
}

async function keychainSet(account: string, value: string): Promise<void> {
  if (IS_MACOS) {
    // Delete first (add fails if the entry already exists)
    await keychainDelete(account).catch(() => {});
    await exec("security", [
      "add-generic-password",
      "-s", SERVICE,
      "-a", account,
      "-w", value,
    ]);
  } else {
    const child = execFile("secret-tool", [
      "store", "--label", `${SERVICE}:${account}`,
      "service", SERVICE, "account", account,
    ]);
    child.stdin?.write(value);
    child.stdin?.end();
    await new Promise<void>((resolve, reject) => {
      child.on("close", (code) => (code === 0 ? resolve() : reject(new Error(`secret-tool exited ${code}`))));
    });
  }
}

async function keychainDelete(account: string): Promise<boolean> {
  try {
    if (IS_MACOS) {
      await exec("security", [
        "delete-generic-password",
        "-s", SERVICE,
        "-a", account,
      ]);
    } else {
      await exec("secret-tool", [
        "clear", "service", SERVICE, "account", account,
      ]);
    }
    return true;
  } catch {
    return false;
  }
}

export async function getSshPassword(env: string): Promise<string | null> {
  return keychainGet(`${env}/ssh-password`);
}

export async function setSshPassword(env: string, password: string): Promise<void> {
  await keychainSet(`${env}/ssh-password`, password);
}

export async function getDbPassword(env: string): Promise<string | null> {
  return keychainGet(`${env}/db-password`);
}

export async function setDbPassword(env: string, password: string): Promise<void> {
  await keychainSet(`${env}/db-password`, password);
}

export async function getTotpSecret(env: string): Promise<string | null> {
  return keychainGet(`${env}/totp-secret`);
}

export async function setTotpSecret(env: string, secret: string): Promise<void> {
  await keychainSet(`${env}/totp-secret`, secret);
}

export async function deleteCredential(
  env: string,
  kind: "ssh-password" | "db-password" | "totp-secret"
): Promise<boolean> {
  return keychainDelete(`${env}/${kind}`);
}

export async function listStoredEnvs(): Promise<string[]> {
  return [];
}
