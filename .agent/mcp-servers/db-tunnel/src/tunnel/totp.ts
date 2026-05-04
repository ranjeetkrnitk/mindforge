import { authenticator } from "otplib";

/**
 * Generate a TOTP code from a base32 secret.
 * Works identically to Google Authenticator.
 */
export function generateTotp(secret: string): string {
  return authenticator.generate(secret);
}

/**
 * Validate that a secret looks like a valid base32 TOTP secret.
 */
export function isValidTotpSecret(secret: string): boolean {
  return /^[A-Z2-7]+=*$/i.test(secret.trim()) && secret.trim().length >= 16;
}
