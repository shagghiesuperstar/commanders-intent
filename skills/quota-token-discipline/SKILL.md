---
name: quota-token-discipline
description: "Use on every task that spends tokens, model quota, API calls, or the Owner's attention: one digest per task, no FYI wakes, right-sized models, no tight polling, main effort first, and loud early warning when quota runs low."
---

# Skill: quota and token discipline

Canonical rule: `COMMANDERS-INTENT.md` section 17. This skill is how to apply it.

## Rules

1. **One digest per task.** Report once when the task finishes or blocks: result first, then evidence links, then what is needed from whom. No running commentary. No raw log dumps. No paraphrase of a log when a link will do.
2. **No FYI wakes.** Never wake the Owner or another agent for information that needs no action. Batch it into the next digest. When nothing changed, nothing was due, and nothing is blocked, stay silent.
3. **Right-size the model.** Top models where quality shows (design, security review, doctrine and intent work). The cheapest capable model for everything else. The Chief of Staff issues and signs orders; drafting long documents and token-heavy digging (logs, admin panels, payment integrations) go to a cheaper session (skill: `delegate-troubleshooting`).
4. **No tight polling.** Poll external APIs no faster than every 5 minutes unless a live incident needs it. Prefer a completion notification, a webhook, or a single scheduled check over a loop. Never poll in a loop to fill time.
5. **Main effort first.** When quota is limited, the main effort and keep-alive floors keep their share. Everything else queues with a note.
6. **Read before you re-derive.** Check the memory bank and the `commanders-intent` mental model before rebuilding context. Never make the Owner repeat an answer.
7. **Loud early warning.** When a quota, credit balance, or rate limit is near its cap (at a warning level the Owner sets, with time still left before reset), tell the Chief of Staff in one line and propose what to pause, with the six-part ask if a decision is needed. Never degrade silently.
8. **Model fallback is never silent.** If a provider or model fails over to another, report it in the next digest (or at once if quality-critical work is affected): which model, why, and what work ran on the fallback.

## Proactive triggers

- A routine or agent sends more than one message per task, or sends messages with no action in them.
- A loop polls faster than every 5 minutes.
- Quota or credit usage crosses a warning level.
- A provider fallback is observed in logs.

When triggered: fix it yourself if it is your own behavior; otherwise order the fix with a deadline and proof. Add a permanent guard (for example a routine check that counts messages per task, or a cap in the poller).

## Check

- Count messages per task in the last day: target one digest each, plus real blockers.
- List active pollers and their intervals.
- Read current quota and credit usage; report `N/A <reason>` if unreadable, never an estimate.

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
