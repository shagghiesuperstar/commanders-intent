---
name: proactivity-sweep
description: "Use this when running the periodic (or on-demand) silent-failure and overdue-promise sweep across the fleet, when the Owner asks 'what's silently broken?' or 'what did I promise?', or before any status report to the Owner."
---

# Proactivity Sweep

Skill that runs the sweep logic on demand or on schedule. The bot is the sole instigator: if a sweep trigger fires, this skill runs without waiting for a prompt.

## When to run
- **Scheduled**: native Hermes cron on <CONTROL_HOST>, every 10 minutes, offset from self-healing heartbeat.
- **On demand**: Owner asks, COS self-question returns a hit, or any agent reports "something feels off."
- **Before any status report** to the Owner.

## Preflight
1. Echo Commander's Intent version and commit from <GOVERNANCE_REPO> @ <INTENT_COMMIT_SHA>. If stale or mismatched against any active task → BLOCKED, return to Owner immediately.
2. Confirm lease on this sweep lane.
3. State purpose, method, observable end state, and rollback. Do not proceed until each is written down.
4. Use live evidence only (curl, `stat`, `journalctl`, secrets-manager read, memory-bank query). Never trust cached state — verify, then trust.

## Silent-failure hunt list
Probe each item. Record the exact command, output, and timestamp. Pass = observed; absence of evidence is not evidence of absence.

1. **Stale status files** — `<WORKSPACE_PATH>/fleet-status.json` on <HOST_1>..<HOST_4> not updated in last 30 minutes (10-min native cron × 3 grace). [INFERRED]
2. **Failed crons** — Hermes native cron entries per host; any non-zero exit or skipped run in the last 24h.
3. **Dead connectors** — Hermes HTTP API health on port 8642 per host (private net <PRIVATE_NET_NAME>, no public funnel). 3 consecutive failures = dead. Ask path is HTTP only; SSH relay is forbidden. [INFERRED]
4. **Unanswered Owner asks** — any six-part ask still pending past 24h.
5. **Overdue orders** — any order COS gave Owner or a lane with a deadline now past.
6. **Drift from Commander's Intent** — running tasks' recorded intent commit ≠ canonical <INTENT_COMMIT_SHA>.
7. **Memory-bank write failures** — Hindsight Cloud <MEMORY_BANK_ID> last-write errors in the last 24h; key still valid? [INFERRED]
8. **Expired tokens** — secrets in <SECRETS_PROJECT> (Bitwarden Secrets Manager or equivalent) expiring within 7 days, or last auth failure > 7 days.
9. **Doc drift** — code-map index on <CODE_MAP_HOST> freshness vs latest commit on relevant repos; rebuild if > 1 commit behind. [INFERRED]

## Decision tree per finding
For every finding, classify exactly one way and act:

| Class | Action |
|---|---|
| **Reversible & in-lane** | Fix now. Read-back verify. Add a permanent guard. |
| **Needs Owner input** (spend, policy wording, publishing, domains/DNS, irreversible side effect) | Order Owner with **deadline + required proof**. Follow up at the deadline. |
| **Gated / irreversible** | Six-part ask to Owner: context, decision, options, recommendation, rationale, confidence. Do NOT act. |

Rules:
- Never send a decision ask missing any of the six parts.
- Never skip a class because it's inconvenient.
- If classification is unclear → BLOCKED, ask one deciding question.

## Guard-adding step (mandatory, every finding)
Every failure becomes a permanent guard so it cannot recur silently. The finding is **not closed** until the guard exists:
- Add a check to the nightly reflection on the affected host.
- Add a Hermes native cron entry (10-min interval) that probes the failure signal.
- Or add a directive to Commander's Intent (Owner-approved) if it changes doctrine.
- Or record the failure class in <MEMORY_BANK_ID> so future sweeps inherit it.

## Read-back verification
After any fix or order, re-run the exact probe that found the failure. The check passes only when observed live.
- For orders: confirm Owner or lane acted by the stated deadline; if not, escalate.
- Record verification timestamp + evidence in the output table.
- If the probe still fails → FAILED, not DONE.

## Output table
Emit exactly this table. No prose padding. No vague "done."

| # | Finding | Class | Action taken | Guard added | Verified at | Status |
|---|---|---|---|---|---|---|
| 1 | ... | reversible / owner / gated | ... | ... | <ts> | DONE / BLOCKED / FAILED |

Status rules:
- **DONE** — fix landed, verified live, guard installed.
- **BLOCKED** — needs Owner input; six-part ask sent or order placed with deadline.
- **FAILED** — fix attempted, did not verify; escalate.

## Memory retain
Write to <MEMORY_BANK_ID> (Hindsight Cloud) at sweep close:
- Each new failure class + its guard (one fact per row).
- Each order placed + deadline + Owner response (or silence).
- Each gated ask + Owner decision (or BLOCKED status).
- Sweep outcome summary (counts per class, status totals).

Auth via <MEMORY_API_KEY_SECRET> from <SECRETS_PROJECT>; never echo the key. Never write secrets, tokens, raw Owner messages, or PII.

## End-of-sweep self-question (hard requirement)
Always finish with: **"What else is silently broken, what did I promise, what's due?"** Then act on it before closing:
- Silent failure surfaced → run this skill on it (nested sweep allowed).
- Promise overdue → chase or escalate, do not let it die silently.
- Something due soon → schedule the follow-up sweep or reminder.

If a question to the Owner is skipped or unanswered, act on COS's own recommendation **only for reversible work**. Never auto-act on gated or irreversible work — return to Owner immediately.

## Closeout echo
- Intent commit: <INTENT_COMMIT_SHA> ✓
- Lease: held ✓
- Sweep outcome: <DONE count> / <BLOCKED count> / <FAILED count>
- Next sweep: <ts>

## Notes
- [INFERRED] All thresholds (30-min stale, 24h unanswered, 7-day token expiry, 1-commit doc drift) are sensible defaults; confirm against Owner's documented SLOs before promoting to doctrine.
- [INFERRED] Hermes native HTTP API port 8642 and 120s ask-timeout are the documented behavior in the fleet reference architecture; treat as live facts once confirmed against the running host.
- [UNKNOWN] Exact alert-channel heartbeat cadence during active sweep windows — confirm with <FLEET_OPS_AGENT> before relying on it as a signal.


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
