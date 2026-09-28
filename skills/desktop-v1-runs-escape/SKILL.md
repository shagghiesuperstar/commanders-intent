---
name: desktop-v1-runs-escape
description: "Use this when a Grok connector ask to a Hermes host running Hermes locally dies around ~120s with tool error -32001 — escape via host-local POST /v1/runs on the same host, not via any fleet ask path."
---

# Long-job escape via host-local Hermes /v1/runs

## When
A Grok connector `ask` to a Hermes host that already runs Hermes on loopback (default `:8642`) dies around ~120s with tool error `-32001` or an equivalent connector-timeout error. [VERIFIED — Hermes HTTP API timeout behavior; cross-check current docs.]

## What this is / is not
- **Is:** a long-job escape for hosts that run Hermes locally, used for AR/merge/tool jobs that exceed the connector ask window.
- **Is not:** the fleet ask path. The fleet ask path stays on the Hermes HTTP API over the private network only. SSH is not an ask path — period, no soft "prefer HTTP."

## Proactive triggers
Run this skill without being asked when any of the following is true:
- Any connector ask to a Hermes host returned `-32001` or a near-120s timeout in the last 24 hours.
- A scheduled AR/merge/tool job is queued for a host that runs Hermes on loopback.
- A nightly reflection log records a new failure class matching "connector timeout against localhost Hermes host."
- Any other skill or routine references a long-running local job on a Hermes host without naming its escape path.
- A peer agent reports "ask died," "sidecar hung," or "120s flake" against a Hermes host — confirm before assuming it is a fleet-side issue.

## Steps
1. Confirm Hermes HTTP API is up on the target host: `API_SERVER_ENABLED=true`, a strong `API_SERVER_KEY` is set, default bind `127.0.0.1:8642`. [INFERRED for env-flag names — verify against the current Hermes HTTP API docs before relying on them.]
2. From that host itself, POST to `http://127.0.0.1:8642/v1/runs` using the live `API_SERVER_KEY`. Never reach across hosts for this escape; the whole point is loopback.
3. **Body shape (required):** `{"input": "<work order text>"}`. Sending only `prompt`, `goal`, or `message` returns HTTP 400 Missing `input`. [VERIFIED — Hermes HTTP API.]
4. **Auth:** `Authorization: Bearer $API_SERVER_KEY` and/or `X-API-Key: $API_SERVER_KEY`. Load the key from the host-local env file (default `~/.hermes/.env`) or the secrets manager entry scoped to that host. Never echo the value, never commit it, never paste it in chat or memory. [INFERRED for the env path; treat default locations as [INFERRED] until checked.]
5. **Success response:** HTTP 202 with body `{"run_id":"run_…","status":"started"}`. [VERIFIED — Hermes HTTP API.]
6. Poll with `GET /v1/runs/{run_id}` until a terminal state. Persist the run_id with the originating ticket.
7. Raise the Grok connector / sidecar timeout locally if short asks still flake near ~120s; do not raise it past what the sidecar can hold open, and record the new value.
8. Do **not** open an upstream Hermes issue or PR for a timeout complaint unless you hold a reproducible host-hang capture (logs, timestamps, request/response). Speculative upstream tickets waste reviewer time.
9. Never put `API_SERVER_KEY` in any public template, chat transcript, git commit, memory bank entry, or PR description. Local env file or secrets manager only.

## Failure → permanent guard
Every time this skill fires, finish by asking: *what else is silently broken, what did I promise, what's due?* Then act:
- New failure class (e.g. 202 returned but run never reaches terminal state) → add a host-local cron that polls `/v1/runs/{run_id}` for any run older than a deadline and alerts the alert channel.
- Key leaked somewhere it shouldn't → add a pre-commit grep guard for the key shape; refuse the commit on match.
- Connector timeout recurs after the sidecar timeout was raised → open a follow-up against the connector config, not the loopback API.
- Host-loopback port changed or key rotated without notice → add a preflight check at the top of this skill that fails loud before retrying.

## Related (public docs only)
- Hermes HTTP API documentation (official).
- Fleet ask path over the private network.
- Nightly reflection routine.
- Pre-commit secret-scan guard.


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
