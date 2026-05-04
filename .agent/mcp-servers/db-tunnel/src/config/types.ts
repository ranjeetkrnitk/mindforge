export type DbType = "postgresql" | "mysql";
export type AuthType = "password" | "totp";
export type EnvConnectionType = "ssh-tunnel" | "direct";

export interface SshConfig {
  host: string;
  port: number;
  user: string;
  /** "password" = simple SSH password; "totp" = password + TOTP 2FA */
  auth: AuthType;
}

export interface DbConfig {
  type: DbType;
  host: string;
  port: number;
  database: string;
  user: string;
}

export interface SshTunnelEnvironment {
  label: string;
  type: "ssh-tunnel";
  ssh: SshConfig;
  db: DbConfig;
}

export interface DirectEnvironment {
  label: string;
  type: "direct";
  db: DbConfig;
}

export type EnvironmentConfig = SshTunnelEnvironment | DirectEnvironment;

export interface Defaults {
  queryRowLimit: number;
  tunnelLocalPortStart: number;
  connectTimeoutMs: number;
}

export interface AppConfig {
  environments: Record<string, EnvironmentConfig>;
  defaults: Defaults;
}
