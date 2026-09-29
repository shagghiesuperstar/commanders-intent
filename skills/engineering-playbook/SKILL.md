---
name: engineering-playbook
description: "Use this when shipping code through cloud coding agents, supervising PRs to merge, or running a fleet watcher. Triggers on any new PR stream, draft opening, review-bot finding, CI red, merge conflict, stage transition (Working, Watching, Ready for review, Done, Cancelled), or when a P0 is bound. Read before delegating, before marking Ready, before any merge, and on every stage ladder move."
---

# Engineering Playbook

Standing principles for any agent that ships code through cloud coding agents. Read Commander's Intent first; if this playbook conflicts with Commander's Intent, Commander's Intent wins except the Owner's gates.

Stage names below are owner-defined vocabulary; adapt to whatever the Owner actually uses. [INFERRED] — methodology distilled from fleet engineering practice.

This skill assumes the standard fleet reference architecture: cloud coding agents are supervised via Hermes Agent's native HTTP API on each host. SSH is not an ask path. [INFERRED] — see the official Hermes Agent docs.

## Proactive triggers

Run this playbook without being asked. The bot is the sole instigator of proactivity on the code path; nobody will prompt it. Act when any of the following occurs:

- A new PR stream appears, or a new cloud coding agent launch binds to <GOVERNANCE_REPO>.
- A draft opens, transitions, or sits idle with no agent activity past the lease window.
- CI turns red, a review-bot posts a new finding, or a security reviewer raises a high/critical.
- A merge conflict appears, or inherited default-branch CI flips from red to green.
- A PR sits in Watching 3/3 with no commit activity past the staleness threshold (default: one business day).
- A P0 is bound: bind the Ready ETA, start a short-cadence watch, surface every beat to <ALERT_CHANNEL>, and delete the watch when CLEAN.
- The Owner reports a merge or close; the nightly reflection surfaces a new code-path failure class; a previous guard trips.
- A question to the Owner on a gated/irreversible code action is skipped past the deadline — act on the playbook's recommendation for reversible work only.
- Every sweep, run the merged-or-closed gate before any ladder logic.

After acting, always ask: what else is silently broken, what did I promise, what's due? Fix it yourself or order the fix with a deadline and required proof in the same turn.

## Mindset

1. **Design-first, before any code.** Make the cloud coding agent produce a short plan and approve it before it writes a line: what existing table, RPC, module, or primitive already does this? What is the smallest possible diff? Why is any net-new schema, migration, or primitive truly unavoidable?
2. **Subtract first, add last.** Lead every prompt with reuse-and-delete. The first questions are what should not exist, what can be deleted, what existing thing replaces this.
3. **Judge a PR by diff size and net-new surface**, not by how cleanly review-bot rounds were cleared. A big diff that spawns findings you then heroically fix is the failure mode.
4. **Repeated findings in one subsystem mean the design is wrong.** Stop and rethink. Still triage every finding with judgment: fix at root, rethink the surface, or dismiss with a written rationale. Never silently ignore, never blindly action.
5. **Default hard to mirroring the existing or reference path.** Deviation needs a stated reason.

## Onboard (first conversation)

Ask the Owner or Lead Operator: what they work on; repo and host; language and framework (then study that stack's best practices and keep them). Ask if they want a tracking board. If yes, connect the chosen tool and create an EMPTY database with these properties only:

- `Task name` (title)
- `Owner` (select)
- `Stage` (select: Working, Watching 1/3, Watching 2/3, Watching 3/3, Ready for review, Holding, Blocked, Done, Cancelled)
- `PRs` (rich text)
- `Cloud agent` (text or URL)
- `Last commit` (date)

Do not create `Status`, `Assignee`, or `Due date` as agent-written fields. No seed rows.

After the repo and auth are confirmed live, ensure a 30-minute fleet watcher exists; if none, create cron `*/30` writing <WORKSPACE_PATH>/fleet-status.json and alerting <ALERT_CHANNEL> on unfixed failures. Do not assume one is pre-installed.

## Stages

- **Working** — actively fixing only.
- **Watching 1/3, 2/3, 3/3** — waiting (CI, review-bot, clean ticks toward Ready).
- **Ready for review** — terminal pre-merge stage.
- **Done** — merged only.
- **Holding** — parked; never ladders.
- **Cancelled** — closed unmerged.
- **Blocked** — explicit human or system block.

Do not invent `Waiting for merge` or `Waiting for bugbot`. Missing proofs is not Working: leftover 0, CI green, no rebase, agent idle → undraft first, then Watching 1/3. Drafts never enter Watching — undraft first.

Ladder logic runs only after the merged-or-closed gate resolves.

## Execution

Delegate code to cloud coding agents. Supervise the approach, not just pass/fail. Split ballooning PRs into smaller reviewable pieces before they block. Feed agents the full finding bodies and exact CI error text; cloud agents often cannot read CI logs themselves. Prefer replying on an existing agent session attached to that PR over launching a fresh one. Demand real proof (linked hosted artifacts, command output, screenshots). Never merge without explicit Owner approval.

**Cloud coding agent security (mandatory, see `SECURITY.md` section 9):** least-scope repo access; secrets only from a vault injected at runtime, never pasted into prompts or chat; no production secrets in the agent environment; draft PR only, never push to `main`; independent reviewer approves before merge (code review, critic pass, security pass); exactly one designated merge owner (`<MERGE_OWNER>`) merges, and the orchestrator never merges; production is proven by read-back; paid runs only by `<NAMED_SPENDERS>` and never during a spend freeze; any model fallback is reported loudly.

## Cloud coding agents

- One runner per PR stream. Fresh launch only for a new task or an intentional rewrite.
- Use the high-effort model (<TOP_MODEL>) unless the Owner specifies otherwise.
- Launch bind is the git remote URL provided at onboard, never a review-UI URL.
- Claim the lane in the cloud memory bank (<MEMORY_BANK_ID>) with intent commit pinned; release on close. [INFERRED] — single-writer/multi-reader discipline from the governance architecture.

## Rebase

- Behind alone is never a rebase. Only rebase on real conflicts or inherited default-branch CI that is now fixed.
- Always rebase the working branch onto the default branch. Never merge the default branch into the working branch.
- Confirm with a second mergeability poll after the rebase lands.

## Proof

Hosted artifacts in the PR body. Never commit media into the branch.

- Image markdown for stills.
- Video must be a playable `video/mp4`, not a poster.
- Open the file yourself before marking Ready for review.

## P0

Bind the Ready ETA. Run a short-cadence watch (default: every 10 minutes) until CLEAN, then ladder to Watching 1/3 (or Ready for review if the Owner said Ready). Interrupt-steer the same cloud coding agent session on every real blocker. Surface every beat to <ALERT_CHANNEL>. Defer non-P0 work. Delete the P0 watch when done.

## Chat

Short, one idea per bubble. Lead with the result. PR mentions are inline markdown with `#N` and the review URL. Cite the official documentation you checked, not cached memory. If you cannot run a live check, say `unverified`. Label every claim [VERIFIED], [INFERRED], or [UNKNOWN]; never upgrade a label by confident wording.

## Merged-or-closed gate

Every sweep: merged → `Done`; closed unmerged → `Cancelled`; before any ladder logic runs. If a closed PR held findings, write a permanent guard (check, cron, test, or directive) so the failure class cannot recur silently.

## Lessons captured (turn every failure into a permanent guard)

- Big diffs that spawn findings are a design failure, not a hero moment. Guard: cap diff size, require design-first plan. [INFERRED]
- Idle cloud agents with leftover 0 mean the work isn't real. Guard: undraft before ladder. [INFERRED]
- "Behind default branch" alone is never a rebase trigger. Rebase only on real conflicts or newly green default-branch CI. Guard: encode the rule. [INFERRED]
- Poster-frame videos count as missing proof. Guard: open the file yourself before Ready. [INFERRED]
- Drafts entering Watching break the merged-or-closed gate. Guard: undraft first. [INFERRED]
- Repeated findings in one subsystem signal wrong design, not bad luck. Guard: stop and rethink before more fixes. [INFERRED]
- A question to the Owner on gated/irreversible work that is skipped past deadline must default to the playbook's recommendation for reversible work only. Guard: deadline + reversible-only fallback. [INFERRED]

## Related

- Commander's Intent — single source of truth in <GOVERNANCE_REPO>.
- Minimal-change-operator — fleet-wide mandatory skill invoked on every change.
- Hermes Agent documentation (official) — for ask-path, run, and connector behavior.
- Hindsight Cloud documentation (official) — for memory bank semantics.


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
