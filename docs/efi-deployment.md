# אפי — deployment & operations runbook

Operational notes for **אפי**, the OpenClaw assistant. Captured 2026-06-15 while
diagnosing a "stuck" incident. אפי runs on a Hetzner server **not** built from
this repo; this is hand-authored knowledge so the next session doesn't re-learn
it from scratch.

> No secrets here. Credentials live on the server / in the Hetzner console and
> are referenced by name only.

## Where it runs

- **Host:** Hetzner VPS, hostname `ubuntu-4gb-fsn1-1` (Ubuntu, ~4GB RAM, ~150GB
  disk). Public IP is in the Hetzner Cloud Console (`console.hetzner.cloud`).
- **Access:** `ssh root@<ip>`. SSH is firewall-restricted to known IPs — if it
  times out, your IP may have changed; use the **Console** (VNC) button in the
  Hetzner Cloud Console, which doesn't go through port 22.
- **Runtime:** Docker. Find the gateway container with `docker ps` (id is
  ephemeral; match image `openclaw:latest`, name `…openclaw-gateway-1`,
  listening on `127.0.0.1:18789`).
- Two unrelated containers also run here: `powdercoat-powdercoat-site` and
  `…-mailer` (Rightek site). Don't touch them when working on אפי.

## Config

- **Live config:** `/root/.openclaw/openclaw.json` (mounted into the container
  at `/home/node/.openclaw`). Edits take effect on hot-reload or container
  restart.
- **Backups** sit next to it: `openclaw.json.bak*`, `openclaw.json.last-good`.
  The edit commands in this repo also drop a timestamped `…pre-*` copy first.
- **Model provider:** `codex` — i.e. the ChatGPT/Codex **subscription** auth
  (a "local" provider profile), surfaced as model id `openai/gpt-5.5`. This is
  *not* an OpenAI platform API key; its quota is the Codex subscription quota.
- **Channels enabled:** WhatsApp (Baileys/libsignal), Telegram. WhatsApp
  connects on startup and logs `Listening for WhatsApp inbound messages`.

## Model fallback — the part that's easy to get wrong

OpenClaw distinguishes two config keys under `agents.defaults`:

- `models` (plural map) — **just the model catalog** (keys are full
  `provider/model` ids, values hold per-model metadata). Adding an entry here
  does **not** create a fallback.
- `model` (singular object) — **this is the selection + fallback chain:**
  ```jsonc
  "model": { "primary": "openai/gpt-5.5", "fallbacks": ["openai/gpt-5.4"] }
  ```
  `fallbacks` is the ordered list used when the primary fails. (Verified against
  `src/config/schema.base.generated.ts`: *"Ordered fallback models … Used when
  the primary model fails."*)

Current setting: primary `openai/gpt-5.5`, fallback `openai/gpt-5.4`.

> ⚠️ **A same-account fallback does not escape a subscription-wide limit.** Both
> `gpt-5.5` and `gpt-5.4` ride the same Codex subscription, so when the
> subscription quota is exhausted, the fallback fails too (see incident below).
> For real resilience, a fallback must point at a **different provider/account**
> (e.g. an Anthropic key, or an OpenAI platform API key separate from the Codex
> subscription).

## Symptom → cause map

- **WhatsApp shows "typing…" but no reply** → the channel is connected and the
  message was received, but **model generation failed**. Look at the gateway
  logs for `FailoverError` / `usage limit`, not at the WhatsApp layer.
- **161 zombie processes** (login banner / `ps`) → the gateway leaks
  `openclaw-hooks` and `git` child processes it doesn't reap. Harmless short
  term; a `docker restart` clears them. Durable fix: add `init: true` to the
  compose service (PID-1 reaper).

## The 2026-06-15 incident (root cause on record)

אפי stopped replying. Logs showed, on every inbound message:

```
All models failed (2):
  openai/gpt-5.5: Provider openai is in cooldown (rate_limit)
  openai/gpt-5.4: You've reached your Codex subscription usage limit.
```

- Root cause: **Codex subscription usage limit, exhausted** — and it is
  **subscription-wide, not per-model**, so the `gpt-5.4` fallback (same account)
  failed identically. The cooldown is provider/auth-profile-scoped.
- The error message itself states the only fixes: *use another Codex account, or
  switch to another configured model/provider* (or wait for the reset).
- **Resolution:** Gal upgraded the OpenAI/Codex account → quota freed → אפי
  recovered. (If an upgrade ever raises the cap but doesn't reset the current
  window, expect recovery only at the billing reset; a restart clears the
  internal cooldown so אפי re-probes immediately.)

## Diagnostic runbook (read-only first)

```bash
# 1. find the gateway container
docker ps -a | grep openclaw            # note the id

# 2. is it the server or the app? (server was healthy in this incident)
df -h / ; free -h ; uptime

# 3. what is אפי doing right now / why no reply
docker logs --tail 60 <id>
docker logs --since 5m <id> 2>&1 | grep -iE 'fallback|candidate|usage limit|FailoverError|cooldown'

# 4. inspect model config (no secrets printed)
python3 -c 'import json;print(json.load(open("/root/.openclaw/openclaw.json"))["agents"]["defaults"]["model"])'

# 5. apply config change safely (backup, edit, restart)
cd /root/.openclaw && cp openclaw.json "openclaw.json.pre-edit.$(date +%Y%m%d-%H%M%S)"
#   …edit via python3/jq…
docker restart <id>
```

> The agent sandbox cannot reach this server (firewall + no key) — by design.
> Operate it via the copy-paste runbook above, with a human at the shell.
