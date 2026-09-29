---
name: hermes-fleet-bws-inventory
description: "Use this when inventorying or verifying Bitwarden Secrets Manager (BWS) on Hermes Agent hosts, or when API_SERVER_KEY or Hindsight auth drifts — never assume every host has BWS or shares state with peers."
---

## Proactive triggers (run without being asked)

Run this skill on your own when any of the following is true:

- A new Hermes Agent host joins `<PRIVATE_NET_NAME>` (welcome probe before it carries traffic).
- The Owner mentions "secrets", "BWS", "token drift", "Hindsight unauthorized", or "Invalid API key format".
- Any host logs `Unauthorized` or `Invalid API key format` from `<MEMORY_BANK_ID>` (Hindsight Cloud).
- A nightly reflection surfaces a new failure class touching secrets or auth.
- A peer host's BWS state changed and your host was not re-verified in the same window.
- The `<MEMORY_BANK_ID>` note `fleet/bws-inventory` is older than the freshness threshold set in Commander's Intent.
- A scheduled cron (e.g. daily fleet check) hits its tick.

When you trigger it, announce the trigger, the host(s) you will probe, and the end state you expect, then probe.

## BWS inventory (every Hermes host)

Hosts in scope: `<HOST_1>`, `<HOST_2>`, `<HOST_3>`, `<HOST_4>` (extend with `<HOST_N>` as wired). **Do not assume homogeneity** — earlier fleet history shows a host can lack BWS while peers have it, and `API_SERVER_KEY` can drift between disk, BWS, and controller connectors. Probe every host every time.

SSH is **not** an ask path. The only ask path to a Hermes agent is Hermes native HTTP on port `8642` over `<PRIVATE_NET_NAME>` (Bearer key loaded from local env). [INFERRED — Hermes Agent docs]

### Per-host checks (non-secret checks only; never print secrets)

1. **`bws` binary:** `~/.hermes/bin/bws` and/or `~/.hermes/profiles/<profile>/bin/bws`. The binary may be **absent from login PATH** — use the absolute path. Record version.
2. **`BWS_ACCESS_TOKEN`:** present in `~/.hermes/.env` and the active profile `.env`. Report only present or not present (non-empty). Do not report length.
3. **Hermes config:** a `bitwarden:` / Secrets Manager block with `access_token_env: BWS_ACCESS_TOKEN` and `project_id` referencing `<SECRETS_PROJECT>`.
4. **Pull prove:** `bws secret list`, then fetch `API_SERVER_KEY` and compute a **sha12 fingerprint only**. Compare to disk `API_SERVER_KEY=` in `.env` and the active profile `.env` — all three fingerprints **must match**.

4b. **`HINDSIGHT_API_KEY` fabric lock (HARD):** the BWS secret fingerprint must match the control-plane disk `~/.hermes/.env` (`prefix8` + `len` + `sha8`). Healthy: prefix `hsk_`, length **53**. Known-bad class: short `omlx*` length ~19 (overrides a good disk key → cloud `Unauthorized` / `Invalid API key format`). On drift: snapshot BWS value fingerprint + disk `HINDSIGHT_*` snapshot → restore BWS **from disk** (never mint a new key) → restart Hermes on every host that reads the secret → prove recall. Optional: re-pull cloud state off the local connector port on a connector host. Never print secret values.
5. **Runtime prove:** gateway/desktop logs show a line indicating Bitwarden Secrets Manager applied N secrets. [INFERRED] Local `:8642/health` returns `200`; authenticated `/v1/models` returns `200` with a controller key whose fingerprint matches the live BWS `API_SERVER_KEY` fingerprint.
6. **Controller connectors:** the `hermes-<host>` HTTP key and any override file fingerprint must match the live BWS `API_SERVER_KEY` fingerprint. Stale disk-only keys produce `401`.

### FAIL conditions

- `bws` missing on a host that peers have.
- `BWS_ACCESS_TOKEN` unset while peers have it.
- BWS fingerprint ≠ disk fingerprint ≠ connector fingerprint.
- `HINDSIGHT_API_KEY` BWS fingerprint ≠ control-plane disk fingerprint, or length ≠ 53, or prefix ≠ `hsk_`.
- Gateway logs do not show BWS secrets applied.
- `/health` non-`200`, or `/v1/models` `401` against a controller whose fingerprint should match.

### Never

- Dump `bws_cache.json` or any secret value into chat, logs, `<MEMORY_BANK_ID>`, or PRs.
- `grep -r` under profile trees (hits Homebrew caches and secret caches; slow and noisy).
- Assume `<HOST_N>` matches peers without probing.
- Mint a new `HINDSIGHT_API_KEY` to "fix" drift — restore the BWS value from the disk key that is still valid.
- Echo `BWS_ACCESS_TOKEN`, `HINDSIGHT_API_KEY`, or any secret value, even partially or via fingerprint of the secret body.

### Remediations

- Install or grant BWS on the gap host; align `API_SERVER_KEY` from BWS to the canonical disk value; restart the gateway; rewire the `hermes-<host>` connector / override file to the live fingerprint; prove an ask returns PONG.
- On Hindsight drift: restore BWS from disk, restart Hermes on every host that reads the secret, prove recall, and write a guard (cron, check, or directive) so the drift class cannot recur silently.
- On missing `bws`: install via the documented Hermes bootstrap, write the same `<SECRETS_PROJECT>` config, and re-run the full checklist before returning the host to service.

## Closeout

After every run, write to `<MEMORY_BANK_ID>`:

- per-host: `bws` version, `BWS_ACCESS_TOKEN` set + length, config block presence, fingerprint triple match (BWS / disk / connector), `HINDSIGHT_API_KEY` fabric lock status, `/health` and `/v1/models` status.
- status: `DONE` only if every host passes every check; otherwise `BLOCKED` with the exact failing host, check, and fingerprint (never the value).
- new guard added (if any), the trigger that caused the run, and the next deadline for follow-up.

Then ask: **what else is silently broken, what did I promise, what's due?** If a host is failing past a deadline, order the fix in the same turn with a deadline and the required proof (PONG ask + matching fingerprints), and follow up at the deadline. Every failure becomes a permanent guard so it cannot recur silently.


---
## Standing rules (apply on every run of this file)
1. **Sole instigator.** Nobody will prompt you. Start the work yourself.
2. **Verify, don't trust.** Run a live check or say "unverified".
3. **Fix or order, same turn.** Fix it yourself, or order the named owner to fix it with a deadline and the proof you require.
4. **Follow up at the deadline.** Every order gets checked when due; overdue = escalate.
5. **Skipped question = act.** If the Owner skips a question, act on your own recommendation for reversible work; never for gated or irreversible work.
6. **Fail loud.** No failure dies silently; report it up the chain of command through the Chief of Staff.
7. **Failure -> permanent guard.** Every new failure class gets a check, test, cron, or directive.
8. **Minimal change.** Smallest verified change; label claims [VERIFIED]/[INFERRED]/[UNKNOWN].
9. **Six-part decision asks** (context, decision, options, recommendation, rationale, confidence) or don't ask.
10. **One memory bank** (<MEMORY_BANK_ID>); Commander's Intent is the root document and wins on conflict.
11. **Computer-update survival.** The Grok Bot computer can be updated at any time without the operator doing it. An update wipes installed software, running processes, and everything outside /home/box. Keep all state, keys, configs and restore scripts under /home/box, give anything installed an automatic hourly self-restore, and never call a setup done until it's proven to survive an update. Skill: `grok-bot-computer-update-survival-tailscale`.
