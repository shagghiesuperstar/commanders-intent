---
name: research-done-gate
description: "Use this when marking any research, recon, probe, or 'answer whether X' ticket Done — require tracker status Done + a written evidence artifact before reporting complete to <OWNER_NAME>. Never equate parking a UI or skipping a widget with research complete."
---

# Research Done gate (COS)

## When
Any ticket whose Definition of Done is research, recon, probe, or "answer whether X" (vendor API capability, inventory path, competitor scan, case handling, etc.).

## Hard rule
Never report "done" to <OWNER_NAME> and never mark a todo complete for research unless **all** of:
1. The matching <ISSUE_TRACKER> issue status is **Done** (or In Review with a <LEAD_OPERATOR_NAME>-signed brief attached), AND
2. A written artifact exists: a brief under `COS/<ticket>/` **or** an <ISSUE_TRACKER> comment with findings and **≥3 concrete examples**, AND
3. You read that artifact this turn before claiming done.

## Forbidden
- Marking research Done because a **widget was skipped**, UI was **parked**, or "default accept until override."
- Equating "we are not building the feature yet" with "we finished the research."
- Trusting only a local todo checklist without checking <ISSUE_TRACKER> and the artifact.
- Reporting done to <OWNER_NAME> based on memory, prior chat, or another agent's verbal claim — live evidence only.

## How to report to <OWNER_NAME>
Plain English, in one message: what was asked → what the vendor/API returned → concrete examples → recommendation. If the probe has not actually run yet this turn, say **not run** and start it — never invent a prior completion.

## Minimal-change-operator checklist (run before reporting)
- **Purpose:** verify research ticket is genuinely complete, not just checked off.
- **Method:** open <ISSUE_TRACKER> ticket → confirm status → locate artifact path → read it this turn → cross-check artifact examples against live result.
- **Observable end state:** <ISSUE_TRACKER> = Done **and** artifact cited in the report **and** artifact contents consistent with the live probe.
- **Rollback:** if any check fails, revert todo to open, write the missing piece (run the probe or write the artifact), do not send "done."
- **Premortem:** the artifact is stale or copied from a prior, unrelated probe → label examples with timestamps and the command that produced them.

## Fail mode this skill prevents
A past failure: a local checklist was marked Done after a case-toggle UI was parked; the <ISSUE_TRACKER> issue stayed in Todo; no live probe was run. <OWNER_NAME> correctly called it a transparency fail. This skill exists so that exact pattern cannot recur silently.

## Proactive triggers
Run this gate without being asked whenever any of the following is true:
- A ticket title, description, or DoD contains research / recon / probe / "answer whether" / "find out" / "does X support Y" / "is Y possible."
- A draft reply to <OWNER_NAME> uses "done," "completed," "research is finished," or similar for a research-shaped ticket.
- A local todo was just checked off for a research item but the matching <ISSUE_TRACKER> ticket is not Done **or** no artifact was written under `COS/<ticket>/` this turn.
- Nightly reflection, cron, or the self-healing layer finds a research-shaped ticket older than its deadline with no artifact path.
- The bot is about to close a lane, archive a thread, or stop polling something — and a research question was logged against it.

When triggered: open the <ISSUE_TRACKER> ticket, verify status, find the artifact path, read it this turn, then either (a) report true Done with the artifact cited, or (b) push back in writing with the exact missing piece and start it now with a deadline and required proof. Follow up at the deadline. If <OWNER_NAME> skips the question, act on the bot's own recommendation for the reversible work (probe it, write the artifact) and never let the question die silently. Convert every new gap found into a permanent check so it cannot recur.


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
