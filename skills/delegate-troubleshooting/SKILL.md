---
name: delegate-troubleshooting
description: "Use this when troubleshooting backend, admin, logs, or payment-integration issues would burn orchestrator tokens — delegate the dig to a capable model session via the Hermes Agent ask path, and return DONE or BLOCKED with a single next action."
---

# Delegate troubleshooting

## When
Any backend, admin, log, payment-integration, or env dig; payment-session errors; cloud env checks; or Hermes agent-bus diagnosis that would otherwise grind the orchestrator's tokens.

## Hard rules
1. Never grind troubleshooting on the orchestrator or Grok Bot (token burn forbidden).
2. Delegate to Hermes via HTTP on port `8642` (`hermes-*` MCP ask only) [INFERRED — per fleet reference architecture]. SSH is not an ask path.
3. Require frontier model: <TOP_MODEL> on that Hermes session.
4. Prefer a dedicated long-running `TROUBLESHOOT-*` session parked for follow-ups.
5. Code hotfixes on the implicated repo: launch <CLOUD_CODING_AGENT> in parallel on a tip PR; orchestrator merges only when told.
6. Orchestrator returns DONE or BLOCKED plus one next action only.
7. Never paste secrets; report key names as PRESENT/ABSENT and masked error codes only.

## Steps
1. Stamp standing memory in <MEMORY_BANK_ID> when <OWNER_NAME> tightens the rule.
2. Health-check the target Hermes host (expect `mode=http`). If down → BLOCKED. SSH is not an ask path and is not a fallback.
3. Send a crisp work order: goal, IDs/URLs, what was tried, deliverable, model preference.
4. If the ask times out [INFERRED — connector ask timeout around 120s, error code `-32001`]: try one other healthy host once; then BLOCKED on agent-bus — escalate bus repair as its own delegated work order; do not dig on the orchestrator.
5. Run <CLOUD_CODING_AGENT> in parallel when code is implicated.
6. Report DONE/BLOCKED up the chain only when <OWNER_NAME> is waiting.

## Proactive triggers
Run this skill without being asked when:
- A backend, admin, log, or payment-integration error lands in <ALERT_CHANNEL> with no owner assigned.
- An ask to a Hermes host times out twice in a row — treat as bus degradation, not a one-off, and open a bus-repair work order.
- <OWNER_NAME> asks for a dig that would obviously burn orchestrator tokens.
- A `TROUBLESHOOT-*` session has been idle past the agreed follow-up window — ping it before <OWNER_NAME> notices.
- A previous troubleshooting delegation returned BLOCKED on agent-bus and the bus still looks unhealthy — re-delegate or open a fresh work order.

After every action, ask: what else is silently broken, what did I promise, what's due? If blocked, return to <OWNER_NAME> immediately using the six-part decision rule (context, decision, options, recommendation, rationale, confidence). If a question to <OWNER_NAME> is skipped, act on the bot's own recommendation for reversible work only. Every failure becomes a permanent guard (cron, check, test, or directive) so it cannot recur silently.


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
