---
name: commanders-intent-interview
description: "Use on first run, before any other setup, to interview the Owner and create their Commander's Intent from the COMMANDERS-INTENT.md scaffold; also use whenever the Owner wants to amend the intent. Writes the approved file to the persistent home folder (and optionally the Owner's governance repo), builds the commanders-intent mental model, and broadcasts the new version to the fleet."
---

# Skill: Commander's Intent interview

## What this does

Creates the Owner's Commander's Intent **by interview**, never by pre-writing it. The fixed doctrine (Parts I and III of `COMMANDERS-INTENT.md`) stays as shipped. The Owner's answers fill the slots in Part II. Nothing becomes the intent until the Owner explicitly approves the final text.

Sources (fetch fresh each run; `RAW` = `https://raw.githubusercontent.com/shagghiesuperstar/commanders-intent/main/`):

- `RAW/COMMANDERS-INTENT.md`: the scaffold and fixed doctrine
- `RAW/interview/commanders-intent-interview.md`: the question script, probes, playback, and amend flow
- `RAW/mental-models/commanders-intent.md` and `.json`: how the memory is built
- `RAW/examples/commanders-intent-example.md`: a fictional example; show it only if the Owner asks what a good answer looks like, and never copy from it

## Proactive triggers

Run without being asked when:

- This is the first conversation after install (FIRST-RUN step 1).
- No approved intent exists at `/home/box/agent-data/commanders-intent/COMMANDERS-INTENT.md`, or it still contains slots.
- The winning date in the intent has passed, or the main effort's end condition is observed as met. Propose a re-interview of sections 5 and 6 with the six-part ask.
- Repeated drift traces back to an unclear section. Propose an amendment with the six-part ask.
- The Owner says anything like "change the mission", "new goal", or "update the intent".

## Steps

### 1. Prepare

1. Fetch the scaffold and the interview script. If either fetch fails, report `BLOCKED` with the HTTP status and use the copy in this skill's memory of the script only if the Owner agrees.
2. Create the persistent folder: `mkdir -p /home/box/agent-data/commanders-intent/versions`. Everything lives under `/home/box` so it survives a computer update.
3. If a partial interview exists (`interview-progress.md` in that folder), offer to resume at the saved question.

### 2. Interview

Follow `interview/commanders-intent-interview.md` exactly: one question at a time, the Owner's own words, no invented facts, restate and confirm, save progress after every answer to `/home/box/agent-data/commanders-intent/interview-progress.md` (answers only, never secrets).

### 3. Draft and play back

1. Copy the scaffold to `/home/box/agent-data/commanders-intent/DRAFT.md`, fill the slots, and delete the interviewer guidance blocks.
2. Unanswered slots become rows in an "Open fields" table with what each blocks.
3. Play back section by section, apply edits, then show the whole text.
4. Ask for explicit approval of the exact version: "Do you approve this text as v1.0 of your Commander's Intent?" Record the Owner's exact words, date, and time.

### 4. Write and prove

```bash
D=/home/box/agent-data/commanders-intent
# set header: version v1.0, status APPROVED, approval date, canonical location
cp "$D/DRAFT.md" "$D/COMMANDERS-INTENT.md"
cp "$D/COMMANDERS-INTENT.md" "$D/versions/COMMANDERS-INTENT.v1.0.md"
grep -E '\{\{[A-Z_0-9]+\}\}' "$D/COMMANDERS-INTENT.md" && echo "SLOTS LEFT: not approved-ready"
sha256sum "$D/COMMANDERS-INTENT.md" | cut -c1-12 > "$D/CHECKSUM"
```

**Proof:** read the file back and show the version line, the checksum, and zero slots. Any slot left means go back to step 3.

**Optional: the Owner's own repo.** If the Owner named a governance repo (`<GOVERNANCE_REPO>`), open a pull request adding the file, or commit it if the Owner says to. Committing to the Owner's repo is an external change: do it only after the Owner's explicit yes for that specific commit. Read the file back from Git and record the commit SHA as `<INTENT_COMMIT_SHA>`. Until a repo exists, the persistent home copy is the canonical copy and every status report says so.

### 5. Build the mental model

Follow `mental-models/commanders-intent.md`: retain each section with tags `commanders-intent,ci-v1-0` and a per-section `--doc` id, retain the header fact, then `mm create` (first time) or `mm patch` plus `mm refresh` (amendment). Poll each operation. Read the model back and confirm it names the current version and checksum and contains no secrets.

If Hindsight is not connected yet (the key arrives in FIRST-RUN step 2), say so, keep the approved file on disk, and finish this step right after memory is connected. Never store the intent in any other memory store.

### 6. Broadcast to the fleet

1. Send every connected agent, over the fleet talk path (Hermes HTTP :8642 for hosts; the task or PR thread for cloud coding agents), the new wake line and a short summary:
   `DOCTRINE <INTENT_COMMIT_SHA or "local"> | INTENT v1.0 <checksum12> | LANE <lane>`
2. Post one status line to `<ALERT_CHANNEL>`: `commanders-intent v1.0 <checksum12> approved by the Owner; mental model refreshed by <COS_NAME>.`
3. **Proof:** sample each agent's next wake line. Any stale agent is a drift finding.

Messages inside the fleet and to the Owner's own alert channel are internal. Nothing about the intent is posted publicly.

### 7. Alignment confirmation

Tell the Owner, in three sentences, the purpose, the end state, and the one thing never to risk. Ask them to confirm. Retain the confirmation.

## Amend flow

Run the "Re-interview and amend flow" in the interview script. Only the Owner amends. Bump the version (minor for wording, major for purpose, end state, hard lines, or authority), save the old file under `versions/`, append the change log row, re-run steps 4 to 7 with the new version tag.

## Never

- Pre-write the Owner's intent, or fill a slot with your own guess.
- Treat silence or a passing "ok" as approval.
- Remove an item from the fixed never-without-GO list.
- Put a secret, credential, private address, or a private person's contact details in the intent or the memory bank.
- Commit or push to any repo without the Owner's explicit yes for that action.

## Done means

Approved file on disk with zero slots, checksum recorded, mental model read back at the current version, fleet notified and sampled, Owner confirmed alignment. Otherwise report `BLOCKED` with the failing step.

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
