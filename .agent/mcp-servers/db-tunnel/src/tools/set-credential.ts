import {
  setSshPassword,
  setDbPassword,
  setTotpSecret,
  deleteCredential,
} from "../credentials/keychain.js";
import { isValidTotpSecret } from "../tunnel/totp.js";

export type CredentialKind = "ssh-password" | "db-password" | "totp-secret";

export async function setCredential(
  envName: string,
  kind: CredentialKind,
  value: string
) {
  if (!envName || !kind || !value) {
    throw new Error("env, kind, and value are all required.");
  }

  if (kind === "totp-secret" && !isValidTotpSecret(value)) {
    throw new Error(
      `"${value}" does not look like a valid base32 TOTP secret. ` +
      `It should be a string like "JBSWY3DPEHPK3PXP" from your authenticator app's "show secret" option.`
    );
  }

  switch (kind) {
    case "ssh-password":
      await setSshPassword(envName, value);
      break;
    case "db-password":
      await setDbPassword(envName, value);
      break;
    case "totp-secret":
      await setTotpSecret(envName, value);
      break;
  }

  return {
    saved: true,
    env: envName,
    kind,
    message: `${kind} for "${envName}" saved to OS Keychain.`,
  };
}

export async function deleteCredentialTool(envName: string, kind: CredentialKind) {
  const deleted = await deleteCredential(envName, kind);
  return {
    deleted,
    env: envName,
    kind,
    message: deleted
      ? `${kind} for "${envName}" removed from OS Keychain.`
      : `No ${kind} found for "${envName}".`,
  };
}
