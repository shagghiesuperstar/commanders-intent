# Routines

Four scheduled routines drive the bot's proactivity. Each one is a standalone prompt the bot runs on a cron schedule; nothing else runs the bot's day-to-day oversight.

## Files in this folder

| File | Purpose |
|---|---|
| `proactivity-sweep.md` | Catches silent failures and things due. The bot's main "instigator" tick. |
| `compliance-audit.md` | Daily check that the fleet still matches Commander's Intent, doctrine, and gates. |
| `order-follow-up.md` | Walks every open Owner order and nudges / re-raises / closes it. |
| `update-survival-restore.md` | Hourly check that everything installed on the Grok Bot computer survived an update; restores it or reports BLOCKED. |

## Schedule and outputs

| Routine | Cron (5-field) | Timezone note | Produces |
|---|---|---|---|
| `proactivity-sweep.md` | `*/30 * * * *` (every 30 min) | Verify local vs UTC on the host; see note below | A short sweep report: silent failures found, self-fixes attempted, items requiring the Owner (with deadline + required proof). Writes to the alert channel on anything not auto-fixed. |
| `compliance-audit.md` | `15 8 * * *` (daily, 08:15) | Verify local vs UTC on the host | A daily compliance scorecard against Commander's Intent and governance canaries; flags drift (stale intent commit, secret-in-memory, unauthorized merge, missed gates). |
| `update-survival-restore.md` | `17 * * * *` (hourly, every day) | Verify local vs UTC on the host | Silent when healthy; RESTORED or BLOCKED report to the alert channel after an update. |
| `order-follow-up.md` | `*/15 * * * *` (every 15 min) [INFERRED] | Verify local vs UTC on the host | A follow-up ledger: every open Owner order, its deadline, who owns closing it, and the next nudge action (re-prompt, escalate, or close). |

> **IMPORTANT — manual setup required.** A Grok Bot template cannot auto-create routines or scheduled tasks on import [INFERRED]. The installer MUST create each routine by hand or the bot will have no proactivity at all. Steps:
> 1. Open the bot's **Scheduled tasks / Routines** screen.
> 2. Create a new routine for each file above; paste the file's **prompt text** as the routine body.
> 3. Set the **cron** to the value from the table (5-field standard: `min hour dom mon dow`).
> 4. Set the **timezone** to `<TIMEZONE>` for every routine.
> 5. Set the **alert channel** to `<ALERT_CHANNEL>` for any non-trivial output.
> 6. **Run each routine once manually** and confirm it produced the expected output (see "Produces" column) before leaving it on a schedule.
> 7. Re-run all four manually after any change to Commander's Intent until the cron is confirmed firing on its own.

## Cron notes (read before installing)

- **5-field cron only.** Format: `minute hour day-of-month month day-of-week`. The bot's scheduler does not accept 6-field or 7-field expressions [INFERRED].
- **UTC vs local time ambiguity is platform-dependent [UNKNOWN].** Confirm whether the scheduler interprets cron in UTC or in the routine's timezone field before relying on wall-clock timing. Test with the manual run above and check the next scheduled fire time.
- **Missed fires.** If the bot is offline when a routine fires, behavior on catch-up is platform-dependent [UNKNOWN]. Do not assume missed ticks replay automatically; sweep logic must be idempotent.
- **Idempotency.** All four routines must be safe to re-run: nothing destructive, no duplicate alerts. Verify before enabling.

## What "good" looks like

- Each routine fires on schedule and writes a visible artifact (message, log line, or status file) on every run.
- Findings surface in `<ALERT_CHANNEL>` within one tick of being detected; the Owner is never the last to know.
- Every detected failure becomes a permanent guard (check, cron, test, or directive) before the routine stops looking at it.
- No routine silently no-ops. If a routine has nothing to report, it says so explicitly.

## Failure to set up is a fleet-wide silent failure

If these routines are not created at install time, the bot loses all proactivity and the Owner finds out only when something breaks. The install checklist MUST include "four routines scheduled and verified firing" as a blocking item.
