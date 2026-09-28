---
name: hermes-fleet-messaging-token-isolation
description: "Use this when storing messaging bot tokens (Telegram, Discord, Slack, etc.) for a Hermes Agent fleet in a shared secrets manager — never share one bot token across hosts; use per-profile keys so Hermes auto-aliases per active profile."
---

# Hermes fleet messaging token isolation

## When
Setting up a secrets manager (e.g. Bitwarden Secrets Manager, or any bulk secret source) across multiple Hermes Agent hosts and profiles that use Telegram, Discord, Slack, or other messaging-platform bots.

[VERIFIED] Hermes auto-aliases profile-scoped credential secrets: a secret named `<VENDOR>_BOT_TOKEN_<PROFILE>` is exposed to the active profile as `<VENDOR>_BOT_TOKEN`. Confirm against current official Hermes Agent documentation for the deployed version; vendor-specific behavior may change across releases.

## Hard rule
**Never store a single shared `<VENDOR>_BOT_TOKEN` (or any messaging-bot token) in a fleet-wide vault project that every host pulls with `override_existing: true`.**

That pattern makes every gateway the same bot → the messaging platform returns `Conflict: terminated by other getUpdates` (Telegram) or the equivalent polling-conflict error on other vendors → one host "wins," the others go silent, and crons/DMs cross-wire (e.g. host B's cron replies appear as host A's bot).

## Correct pattern (Hermes-native)
Use one bot token per Hermes host/profile; let Hermes auto-alias it into the unsuffixed env var the gateway code expects.

- Vault keys: `<VENDOR>_BOT_TOKEN_<PROFILE>` (profile name uppercased, `-` → `_`)
- Active profile `<PROFILE_A>` → `<VENDOR>_BOT_TOKEN_<PROFILE_A>` is applied as `<VENDOR>_BOT_TOKEN`
- Same scheme for `<PROFILE_B>`, `<PROFILE_C>`, etc.
- Profile name `default` does **not** get a suffix alias — use an unsuffixed local `.env` value, or run a named profile.

Shared vault is still fine for secrets that **should** be identical (provider API keys, shared infra tokens, etc.).

## Checklist
1. One bot per messaging identity per host, created on the platform's bot admin (e.g. BotFather for Telegram). [VERIFIED]
2. Store `<VENDOR>_BOT_TOKEN_<PROFILE>` per profile in the secrets manager — **not** bare `<VENDOR>_BOT_TOKEN` in a shared project. [VERIFIED]
3. Confirm on gateway start: log line `applied profile-scoped <VENDOR>_BOT_TOKEN_… as <VENDOR>_BOT_TOKEN`. [INFERRED] Wording may change across Hermes versions; verify against the deployed build.
4. Smoke: the platform's bot-introspection call (e.g. Telegram `getMe`) returns the intended bot username; no `Conflict: terminated by other getUpdates` (or vendor equivalent) in the gateway logs. [VERIFIED for Telegram; INFERRED for other vendors — check each vendor's polling-conflict error text against official docs.]
5. Only **one** process may poll a given bot token (no second gateway, sidecar, or debug script on the same token). [VERIFIED]

## Recovery if already broken
1. Fingerprint each host's live bot via the platform's introspection call (e.g. Telegram `getMe`); never print tokens.
2. Restore correct tokens from pre-sweep `.env` backups.
3. Delete the shared vault entry `<VENDOR>_BOT_TOKEN`; create per-profile keys.
4. Clear the secrets-manager cache entries for that vendor (e.g. `bws_cache.json` for the Bitwarden CLI); restart gateways; re-verify.

## Proactive triggers
Run this skill without being asked when any of the following is observed:
- A secrets-manager diff shows a bare `<VENDOR>_BOT_TOKEN` in a project that more than one host pulls from.
- A gateway log shows `Conflict: terminated by other getUpdates` (Telegram) or an equivalent polling-conflict error from another vendor.
- A new Hermes host or profile is being provisioned and messaging tokens are being set up.
- An audit or rotation script touches messaging-bot secrets.

When triggered:
1. Inventory (read-only) which hosts share which token today; record per host.
2. If collision is live, fail loud to <ALERT_CHANNEL> with host list and offending vault item names — never values.
3. Order the fix with a deadline and required proof: per-host introspection-call username plus a clean gateway log after restart.
4. Follow up at the deadline; if not closed, escalate to the Owner.
5. Add a permanent guard so it cannot recur silently: a check (CI, cron, or pre-deploy) that refuses a bare `<VENDOR>_BOT_TOKEN` in any secrets-manager project pulled by two or more hosts.

## End-of-skill sweep (do not skip)
- What else is silently broken? Other shared secrets in the same project that should be per-host: webhook secrets, per-host signing keys, per-host OAuth refresh tokens. Treat them the same way.
- What did I promise? Re-check every open fix order this skill has issued against its deadline; follow up or escalate.
- What's due? Next scheduled rotation, next onboarding of a new host, next secrets-manager schema audit.
- Act on it now, or hand it to the Owner with a deadline and required proof. Never let an ask quietly die.


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
