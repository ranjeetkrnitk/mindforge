import { readFileSync, existsSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import type { AppConfig } from "./types.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = resolve(__dirname, "../../config.json");
const EXAMPLE_PATH = resolve(__dirname, "../../config.example.json");

let cached: AppConfig | null = null;

export function loadConfig(): AppConfig {
  if (cached) return cached;

  const path = existsSync(CONFIG_PATH) ? CONFIG_PATH : EXAMPLE_PATH;
  if (!existsSync(path)) {
    throw new Error(
      `No config found. Copy config.example.json to config.json and fill in your environment details.`
    );
  }

  try {
    cached = JSON.parse(readFileSync(path, "utf-8")) as AppConfig;
    return cached;
  } catch (err) {
    throw new Error(`Failed to parse config at ${path}: ${(err as Error).message}`);
  }
}

export function getEnvironment(name: string) {
  const config = loadConfig();
  const env = config.environments[name];
  if (!env) {
    const available = Object.keys(config.environments).join(", ");
    throw new Error(`Unknown environment "${name}". Available: ${available}`);
  }
  return env;
}

export function listEnvironmentNames(): string[] {
  return Object.keys(loadConfig().environments);
}

export function getDefaults() {
  return loadConfig().defaults;
}
