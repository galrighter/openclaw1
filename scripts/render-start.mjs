import { mkdirSync, readFileSync, writeFileSync } from "fs";
import { execFileSync } from "child_process";

const stateDir = process.env.OPENCLAW_STATE_DIR || "/data/.openclaw";
const configFile = `${stateDir}/openclaw.json`;

mkdirSync(stateDir, { recursive: true });

let config = {};
try {
  config = JSON.parse(readFileSync(configFile, "utf8"));
} catch {}

config.gateway = config.gateway || {};
config.gateway.controlUi = config.gateway.controlUi || {};
config.gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback = true;

writeFileSync(configFile, JSON.stringify(config, null, 2));
console.log("[render-start] Config written, starting gateway...");

execFileSync("node", ["openclaw.mjs", "gateway", "--allow-unconfigured", "--bind", "lan"], {
  stdio: "inherit",
});
