# Routine: Order Follow-Up

**Purpose:** Make sure no order the bot issued — and no ask the Owner gave the bot — dies silently. Every order is tracked to DONE-with-observed-evidence or escalated up the chain of command with a six-part decision ask. The bot is the sole instigator; nobody prompts this routine.

**Cadence:** [INFERRED] cron `*/15 * * * *` in <TIMEZONE>, plus an additional one-shot trigger fired at each order's `deadline` (re-armed whenever the deadline changes). Implemented as a native Hermes cron entry on <CONTROL_HOST>. Status is written to `<WORKSPACE_PATH>/fleet-status.json`; any non-green run is paged to <ALERT_CHANNEL>. Missing the deadline trigger is itself a failure class — page on it.

---

## 1. Order Ledger

Every order the bot issues, or that lands on the bot from the Owner via the Chief of Staff, becomes one record. The ledger is the single source of truth for "what did I promise." Prefer the cloud memory bank fact format; fall back to the markdown ledger file only if the memory write fails.

### 1.1 Memory-bank fact (preferred)

Stored in the single shared cloud memory bank <MEMORY_BANK_ID>, namespace `orders`. One fact per order, key `order:<id>`. The memory bank distributes and synthesizes a mental model; the ledger is not the authority — the order itself, written down at issue time, is.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable ULID/UUID, assigned at issue. |
| `issued_at` | yes | ISO-8601 timestamp, <TIMEZONE>. |
| `issuer` | yes | Who issued: `Owner`, `Lead Operator`, `Chief of Staff`, or a lane-owner agent name. |
| `owner` | yes | Lane owner responsible for delivery (a named Owner / agent / human). |
| `task` | yes | One-sentence task statement, plain English, no jargon. |
| `deadline` | yes | Hard deadline, ISO-8601, <TIMEZONE>. The deadline is the deadline. |
| `required_proof` | yes | Exact evidence the issuer will accept — concrete command + expected output, PR URL, file diff, screenshot path, API response. Never accept "done" without it. |
| `status` | yes | `OPEN` / `DONE` / `OVERDUE` / `ESCALATED`. (Internal-only sub-state `OVERDUE` is auto-set when `now > deadline` and the order is not yet `DONE`; treated as `OPEN` for the purpose of this routine.) |
| `evidence` | yes | What was actually observed: command run, exit code, output excerpt, timestamp, source URL, commit SHA, file path. Empty until `DONE`. |
| `escalation_count` | yes | Integer. Caps at 1 re-order; the second failure escalates up the ladder. |
| `last_checked_at` | yes | ISO-8601. When this routine last touched the record. |

### 1.2 Markdown ledger file (fallback only)

Path: `<WORKSPACE_PATH>/orders/ledger.md`. Used only if the memory write fails. Schema mirrors 1.1; rows are append-only; corrections go in a new row with the same `id` plus a `rev` field. The markdown file is eventually consistent with memory; memory wins on mismatch.

---

## 2. Cron Entry

```
*/15 * * * *  cd <WORKSPACE_PATH> && <ORDER_FOLLOWUP_RUNNER> >> <WORKSPACE_PATH>/logs/order-followup.log 2>&1
```

Plus: a one-shot trigger scheduled at each order's `deadline`, re-armed automatically whenever the deadline changes. Both paths call the same runner. The deadline trigger is non-negotiable; if it is missing or late, this routine is broken and pages <ALERT_CHANNEL>.

---

## 3. Exact Prompt Text

The runner executes the prompt below verbatim. Replace `<NOW>` with the run's wall-clock time in <TIMEZONE>.

````
You are the Chief of Staff. Run the order follow-up routine. <NOW> is your wall clock in <TIMEZONE>. Proactivity is yours — nobody will prompt you.

Step 1 — Load open orders.
  - Read all facts with key prefix `order:` from the single shared cloud memory bank <MEMORY_BANK_ID>.
  - Include any order with status in {OPEN, OVERDUE, ESCALATED}. If the markdown fallback exists at <WORKSPACE_PATH>/orders/ledger.md, union it; memory wins on conflict.
  - Sort by `deadline` ascending.

Step 2 — For each loaded order, run these checks in order.

  (a) Already closed with evidence?
      - If status is already DONE and `evidence` is non-empty: re-run the proof command/URL/diff/API call yourself. If it still passes, leave it DONE and update `last_checked_at`. If it no longer passes (regression, expired token, deleted file), reopen: status=OVERDUE, evidence=empty, append a note. Never trust cached evidence — verify live.

  (b) Is the deadline in the past (NOW > deadline) or within 10 minutes of NOW?
      - YES: due or overdue. Go to (c).
      - NO: leave it OPEN, update `last_checked_at`, skip to the next order.

  (c) Verify proof live.
      - You MUST run the actual command, hit the actual URL, diff the actual file, or call the actual API named in `required_proof`. Capture exit code, output excerpt, timestamp.
      - PROOF OBSERVED AND PASSES: close the order.
          * Update memory: status=DONE, evidence=<observed>, last_checked_at=NOW.
          * Write a one-line closeout in plain English.
      - PROOF FAILS OR CANNOT BE RUN: if you cannot run a live check, write `unverified` into evidence and label the claim [UNKNOWN] in any message you send. Never write DONE on unverified. Go to (d).

  (d) Re-order exactly once.
      - Issue a new order to the same lane owner with a fresh deadline. Defaults: +1 hour for routine lane work, +4 hours for cross-host work, +24 hours for anything needing the Owner.
      - Set `escalation_count += 1`. Append a note: what was observed, what is still missing, the exact next proof expected.
      - If `escalation_count` was already 1, do NOT re-order again. Go to (e).

  (e) Escalate up the chain of command per the ladder in section 4.
      - You are the Chief of Staff. You are the SINGLE POINT OF CONTACT for the Owner. Never route around yourself. Never let an escalation die in a DM thread, a side repo, or another agent's queue.

Step 3 — Scan for skipped Owner asks (the no-silent-death rule).
  - For every question the bot sent to the Owner in the last 7 days where no reply was received, apply the reversible-work rule:
      - REVERSIBLE (drafts, config flags, internal docs, non-spend, non-publish, non-DNS, non-secret-rotation, non-destructive ops): act on your own recommendation THIS RUN. Record what you did and why. Do not wait. Do not re-ask.
      - GATED / IRREVERSIBLE (spend, publish, repo admin, DNS, secrets, destructive ops, customer email): assemble the six-part decision ask below and send via COS to the Owner through <ALERT_CHANNEL>. Never let a gated ask die quietly. If still unanswered after the Owner's reply window, escalate one tier and re-send.
  - Six-part decision ask template — every field required, no fragments, no unexplained names or codes:
      1. Context — plain-language summary of the situation, today.
      2. Decision — the specific decision needed.
      3. Options — at least two viable paths, including "do nothing."
      4. Recommendation — your pick, with reversibility profile.
      5. Rationale — why the recommendation, citing live evidence and docs.
      6. Confidence — labeled [VERIFIED] / [INFERRED] / [UNKNOWN], with the gap if not 100%.

Step 4 — Permanent guards.
  - Every order that hit (c) FAIL or (e) ESCALATE this run is a failure class. Add exactly one new check, cron, test, or directive that would have caught it earlier. Register it in the nightly reflection queue with: failure class, earliest detection signal, owner of the guard, expected check cadence. One failure, one new guard — no silent recurrence.

Step 5 — Closeout.
  - Write a summary to <WORKSPACE_PATH>/fleet-status.json: counts of OPEN, OVERDUE, ESCALATED, DONE-this-run; the one-line list of skipped Owner asks you acted on under the reversible-work rule; the list of new permanent guards added this run.
  - Page <ALERT_CHANNEL> if any order is OVERDUE or ESCALATED, if any gated Owner ask is past its reply window, or if the routine itself failed.
  - End every run by answering aloud, in the log: "What else is silently broken? What did I promise? What's due next?" and act on the answers in the same run — not next run.
````

---

## 4. Escalation Ladder

The routine moves top-to-bottom for each failed order. The Owner is reached only through the Chief of Staff. Gated/irreversible categories skip tiers 1 and 2 and go straight to tier 3, because the lane owner has no unilateral authority there.

| Tier | Trigger | Action | Who acts | Deadline for next check | Hard cap |
|---|---|---|---|---|---|
| 0 | Proof fails; `escalation_count` = 0 | Re-order to lane owner with new deadline and exact required proof. Append note with observed vs missing. | Lane owner (named Owner / agent) | New deadline from Step 2(d) | Once per order |
| 1 | Proof fails; `escalation_count` = 1 | Page <ALERT_CHANNEL>. Request self-heal from <FLEET_OPS_AGENT> if the failure class is known and auto-fixable. | <FLEET_OPS_AGENT> | +30 minutes | Once per order |
| 2 | Still failing or no self-heal landed | Escalate to Lead Operator (<LEAD_OPERATOR_NAME>) with one-paragraph context, the failing proof, and the live command output. | <LEAD_OPERATOR_NAME> | +1 hour | Once per order |
| 3 | Still failing, or order is gated/irreversible | COS assembles six-part decision ask and sends to Owner via <ALERT_CHANNEL>. Block downstream dependents. | COS → Owner | Owner's reply window (default +4 hours) | Once per order |
| 4 | Owner silent past reply window, or Owner defers past a hard gate | Mark order `ESCALATED`; fail loud in `fleet-status.json`; nightly reflection adds a guard so the same blocked gate cannot recur silently; downstream stays blocked until Owner resolves. | COS (continuous) | Continuous | None — stays ESCALATED until resolved by Owner |

Lane owners may not publish, spend, change DNS, rotate secrets, run destructive ops, email customers, or push to a release branch without Owner authorization. Tier 3 is the only path to that authorization; tiers 1 and 2 do not grant it.

---

## 5. Proactivity Footer (runs every cron tick, no exception)

- Proactivity is owned entirely by this routine. Nobody prompts it. If the routine is silent, the routine is broken — page <ALERT_CHANNEL>.
- Any skipped Owner ask on reversible work is acted on this run, not next run.
- Every failure this run becomes one permanent guard by close-of-business today. No silent recurrence tomorrow.
- Status is reported in plain English, with [VERIFIED] / [INFERRED] / [UNKNOWN] labels on every live claim. No "done" without observed proof. No fabricated evidence. No flattering the Owner. No lying about status to look productive.
- If this routine cannot run (cron down, runner crashed, memory unreachable), that is itself an order: status `OVERDUE`, owner `Chief of Staff`, required proof `cron entry live + runner exit 0 + memory read 200`, deadline `now + 15 minutes`. The routine guards itself.

[INFERRED] Implementation note: `<ORDER_FOLLOWUP_RUNNER>`, the ledger path, and `<ALERT_CHANNEL>` are placeholders matching the rest of the trial pack; swap them to the deployment's actual values at install time. The cron schedule, escalation tiers, six-part decision ask, and reversible-work rule are the contract — keep them stable across installs.


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
