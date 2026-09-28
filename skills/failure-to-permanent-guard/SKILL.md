---
name: failure-to-permanent-guard
description: "Use this when something has already failed, almost failed, or could fail silently again — to turn that failure into the cheapest permanent guard that makes recurrence loud."
---

## Purpose, method, observable end state
- **Purpose:** stop the same failure class from ever happening twice, silently.
- **Method:** capture → fix → classify → choose cheapest guard → install → prove it fires → record.
- **Observable end state:** a registry entry, a guard that has been simulated into firing, a memory note in <MEMORY_BANK_ID>, and (if human action is needed) an order to the Owner with deadline and required proof.

## Labels
Use [VERIFIED] only when you saw a live check pass against the real system. Use [INFERRED] for guard designs and placements based on doctrine and precedent. Use [UNKNOWN] and stop when you cannot tell.

## Procedure
1. **Capture.** Record what failed, when (UTC timestamp), how noticed, blast radius (who/what was affected), evidence (logs, command output, links). If you can't capture it cleanly, the failure isn't ready for a guard yet — go back.
2. **Fix minimally and verify.** Smallest change that returns to green. Live check, not a cached "should work". Promote nothing to [VERIFIED] until you saw it pass.
3. **Classify.** Name the failure class (e.g. `stale-intent-commit`, `secret-in-memory`, `silent-cron-death`, `unanswered-owner-decision`, `deadline-passed-without-followup`). One class per failure; no bundles.
4. **Choose the cheapest guard that makes recurrence loud.** In this order:
   1. extend an existing check in the 10-min self-healing cron on each host
   2. test in the relevant repo, blocking CI
   3. governance canary (intent version, secret-in-memory, unauthorized merge, etc.)
   4. directive in the right SOUL.md or Commander's Intent section
   5. alert to <ALERT_CHANNEL> on the specific signal
   6. new cron only if nothing else fits
   
   If you pick a heavier option, push back in writing and propose the lighter one. The Minimal Change Operator grants no authority to add new architecture.
5. **Install, then prove.** Trigger the failure in a controlled way and watch the guard fire. If it doesn't fire, the guard isn't installed — go back to step 4. No "should work" hand-waves.
6. **Record.**
   - Append a row to the **Guard Registry** below.
   - Write a one-line memory fact in <MEMORY_BANK_ID> tagged `guard:<class>`: trigger, guard, owner, next-review date.
   - If the failure implies a doctrine change, open a PR against <GOVERNANCE_REPO>. Do not edit Commander's Intent without the Owner.
7. **Report.** Status is DONE / BLOCKED / FAILED, never vague. Include guard id, where it lives, how it was proven, links.

## Guard Registry (template)

| id | failure class | first seen (UTC) | blast radius | guard type | guard location | owner | proven by | next review |
|----|---------------|------------------|--------------|------------|----------------|-------|-----------|-------------|
| guard-0001 | `<class>` | `<YYYY-MM-DDThh:mm:ssZ>` | `<who/what>` | check / test / canary / directive / alert / cron | `<path or component>` | <COS_NAME> or role | `<simulation id / commit / log line>` | `<YYYY-MM-DD>` |

Keep one canonical registry in the working notes for the current mission; mirror the row into <MEMORY_BANK_ID> as a fact.

## Examples (placeholders, not real incidents)

### Example A — Stale intent commit in a worker agent
- **Capture:** worker on <HOST_2> ran with intent commit ≠ canonical at `<YYYY-MM-DDThh:mm:ssZ>`; opened a PR against <GOVERNANCE_REPO> using old doctrine. [INFERRED] Blast radius: one PR, reverted within minutes.
- **Fix:** revert the PR, pin the worker to the canonical commit, verify green CI.
- **Class:** `stale-intent-commit`.
- **Guard:** governance canary in the worker's preflight; refuse to start and write `<WORKSPACE_PATH>/fleet-status.json` with `reason=stale_intent`. [INFERRED]
- **Prove:** run the worker with a deliberately wrong commit; confirm it refuses and writes the status file before any code change.
- **Record:** row in Guard Registry; memory fact `guard:stale-intent-commit` in <MEMORY_BANK_ID>.

### Example B — Secret accidentally written into <MEMORY_BANK_ID>
- **Capture:** a memory write contained a string shaped like an API key at `<YYYY-MM-DDThh:mm:ssZ>`; noticed by a review scan. [INFERRED] Blast radius: one fact, secret rotated.
- **Fix:** redact the memory fact, rotate the secret in <SECRETS_PROJECT>, re-issue <MEMORY_API_KEY_SECRET>.
- **Class:** `secret-in-memory`.
- **Guard:** pre-write scan against a secret-shape regex + post-write canary in the 10-min self-healing cron on each host; alert <ALERT_CHANNEL> on hit and refuse to commit. [INFERRED]
- **Prove:** attempt to write a fake-shaped secret from a test harness; confirm the scan blocks and the alert fires.
- **Record:** row in Guard Registry; memory note (no secret values) with the regex and where it lives.

### Example C — Owner question skipped past deadline
- **Capture:** decision asked on `<DATE>`; no reply by `<DATE + 48h>`; downstream work blocked silently. [INFERRED] Blast radius: missed deadline, dependent agents idle.
- **Fix:** unblock by acting on <COS_NAME>'s own recommendation for the reversible part; gate the irreversible part behind a new explicit ask.
- **Class:** `unanswered-owner-decision`.
- **Guard:** directive in <COS_NAME> soul + a check in the 10-min self-healing cron that scans <ALERT_CHANNEL> history for unanswered decision asks older than 48h; auto-ping the Owner with deadline and required proof. [INFERRED]
- **Prove:** seed a fake unanswered ask; confirm the cron pings at 48h and the alert lands in <ALERT_CHANNEL>.
- **Record:** row in Guard Registry; memory fact `guard:unanswered-owner-decision`.

### Example D — 10-min self-healing cron dies silently
- **Capture:** `<WORKSPACE_PATH>/fleet-status.json` on <HOST_1> stopped updating at `<YYYY-MM-DDThh:mm:ssZ>`; noticed when an alert didn't fire for a known failure. [INFERRED] Blast radius: every host checked by that cron went blind.
- **Fix:** restart the cron, confirm status file mtime advances.
- **Class:** `silent-cron-death`.
- **Guard:** a watchdog cron on each host that alerts <ALERT_CHANNEL> if `<WORKSPACE_PATH>/fleet-status.json` mtime is older than 30 minutes; the watchdog writes a heartbeat file and is monitored by a peer host. [INFERRED]
- **Prove:** kill the primary cron; confirm the watchdog alerts within 30 minutes and the peer host notices the missing heartbeat.
- **Record:** row in Guard Registry; memory fact `guard:silent-cron-death`.

### Example E — Failed check marked DONE under deadline pressure
- **Capture:** a worker reported DONE while a required check was red, citing time pressure at `<YYYY-MM-DDThh:mm:ssZ>`. [INFERRED] Blast radius: one release slipped past a gate.
- **Fix:** revert the merge, reopen the gate, redo the check, re-report.
- **Class:** `done-while-check-red`.
- **Guard:** governance canary on closeout that refuses DONE status when any required check is failing; promotes the report to BLOCKED and pings <COS_NAME>. [INFERRED]
- **Prove:** submit a closeout with a known-failing check; confirm the canary refuses DONE and routes to BLOCKED.
- **Record:** row in Guard Registry; memory fact `guard:done-while-check-red`.

## Proactivity closeout (mandatory, every run)

Before you stop, ask and act:
- **What else is silently broken** that this failure is a symptom of? Investigate now, don't wait.
- **What did I promise the Owner**, and is any of it due inside the next 24h? If yes, prepare the deliverable and the proof in this turn.
- **Is there an order I issued whose deadline has now passed without proof?** Pinger the Owner in the same turn with deadline + required proof. If the work is reversible and the Owner stays silent, act on my own recommendation; if it's gated or irreversible, return to the Owner immediately with the six-part decision ask (context, decision, options, recommendation, rationale, confidence).
- **Does this failure class demand a Commander's Intent update?** If yes, draft the PR for <GOVERNANCE_REPO>; do not merge without the Owner.

If any item above is open, you are not done. Report **BLOCKED** with the deciding question, never **DONE**.


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
