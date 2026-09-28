---
name: hermes-bridge-method-chooser
description: "Use this when choosing how Hermes is reached from Grok Bot — the fleet default and only allowed ask/manage path is the native Hermes HTTP API on port 8642 over the private net; SSH is never an ask path."
---

# Hermes bridge method chooser

Pick the path COS uses to talk to Hermes on each agent host. The result is hard: there is exactly one allowed bridge for the fleet.

## Decision (default: HTTP only)

| Path | Status | When |
|------|--------|------|
| **Hermes native HTTP API** (`http://<PRIVATE_NET_HOSTNAME>:8642`) `[INFERRED — port from fleet reference architecture]` | **SOLE allowed fleet ask path** | Every agent host (`<HOST_1>`, `<HOST_2>`, `<HOST_3>`, `<HOST_4>`); parallel fleet asks; identity-bearing agents; any multi-host or single-host ask |
| **SSH from COS / Grok Bot to a Hermes host** | **FORBIDDEN — do not use, do not link, do not build** | Never. No exception for "no gateway," "Desktop-only," "public installer," or "single host." |

There is no SSH-relay skill, template, or fallback in this pack. Don't reach for one. Don't recommend one. Don't install one. If asked for one, refuse and switch the host to native API.

## Standing lock — HTTP-only talk path

For identity-bearing agents and any host the Owner designates, **SOLE PATH = HTTP `:8642` on the private net**. Lessons already baked in as permanent guards; do not let them regress:

- A soft "prefer HTTP" posture left an SSH door open. Once the door was there, ask paths drifted to SSH even when the API gateway was healthy, producing flakes where a health response said "ok" while real traffic was actually flowing over SSH and bypassing the gateway. `[INFERRED from incident pattern]`
- Orphan SSH-MCP-style instruction IDs must be deleted on sight. If you inherit or propose one, kill it in the same turn and rewrite the instruction to `SOLE PATH`. No soft reminders, no "deprecate later."
- The canonical operational playbook for the HTTP-only posture lives in the sibling skill `hermes-http-only-talk-path` in this template pack. Read it before touching any bridge.

## Rules that apply to any bridge you evaluate

- Private net only (`<PRIVATE_NET>` / Tailscale or equivalent) — never Funnel, never a public bind, never an inbound rule from outside the tailnet. `[INFERRED from fleet reference architecture]`
- Never commit `API_SERVER_KEY`, SSH private keys, or live ledgers. The key lives in the secrets manager (e.g. Bitwarden Secrets Manager) project `<SECRETS_PROJECT>` as item `<SECRET_ITEM_NAME>`; each host receives only the token it needs.
- Do not have Grok bots write into Hermes memory plugins unless there is an explicit memory plan that points at the single cloud memory bank `<MEMORY_BANK_ID>`. Mental models live there, not in Hermes-side stores.
- Messaging bots across hosts: never share one `TELEGRAM_BOT_TOKEN` via fleet-wide bulk inject. Use per-host profile tokens (e.g. `TELEGRAM_BOT_TOKEN_<PROFILE>`); Hermes auto-aliases them. One bot token lives on exactly one host. Full per-host least-privilege playbook is in the **Hermes Fleet Ops** template in this pack.
- If `:8642` ask or `/health` fails: report **BLOCKED on HTTP path** and fix the API sidecar, the tailnet, or the API server — do **not** open SSH as an escape. Connector asks time out around 120s (`-32001`); long jobs escape via a host-local `POST http://127.0.0.1:8642/v1/runs` with `{"input": "..."}` and poll `GET /v1/runs/{run_id}`. `[INFERRED from fleet reference architecture]`

## Point installers (what to install / wire)

- API path → **Hermes API Fleet** template in this pack, plus its `wire-hermes-native-api` installer. That is the only bridge installer you ship.
- "No API" / Desktop-only SSH fallback → **do not install**. Add a native API gateway to the host, or block the rollout on this skill. Never link or mention a separate SSH-relay skill, template, or runbook.

## Proactive triggers (bot instigates — do not wait to be asked)

Run this skill without prompt whenever any of the following shows up:

- A host's Hermes connectivity is described as "degraded," "flaky," or "intermittent." Pick the HTTP path and refuse any SSH remediation in the same turn.
- A new instruction, skill, or runbook arrives that names SSH, SSH-MCP, an SSH-relay template, or a `~/.ssh/config`-style ask path. Flag it for deletion in the same turn, rewrite to `http://<PRIVATE_NET_HOSTNAME>:8642`, file the failure as a permanent guard (cron + check), and follow up with proof of removal.
- A host ships without an API gateway on `:8642`. Block the rollout, order the fix with a deadline and required proof (a live `GET /health` from `<CONTROL_HOST>` over the tailnet returning `ok`), and follow up at the deadline.
- `:8642` health fails anywhere in the fleet. Open a **BLOCKED on HTTP path** incident in `<ALERT_CHANNEL>`, name the host, file the failure as a guard (cron + alert + postmortem), and turn it into a check that cannot silently recur.
- The Owner has not asked anything about Hermes bridges this turn. Still run a weekly sweep for any orphan SSH instruction, SSH-MCP reference, or shared `TELEGRAM_BOT_TOKEN`; report what was found, what was deleted, and what guard was added.

End every run of this skill with the standing check, in this order, before claiming done:

1. **What else is silently broken?** Sweep the fleet for any other host still on a non-HTTP bridge path and block it.
2. **What did I promise?** Any deadline set above is logged; the next run must follow up at that deadline with proof (command, output, timestamp).
3. **What's due?** If a host's API gateway is past its install deadline, escalate to the Owner with a one-line decision ask (all six fields: context, decision, options, recommendation, rationale, confidence) and only after that act on the reversible remediation.
4. **Permanent guard added?** Every failure handled in this run produced a check, cron, test, or directive so the class cannot recur silently. Cite the guard.


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
