# Changelog

All notable changes to the Commander's Intent fabric. Versions follow semantic versioning. Newest first.

> **Fabric note.** This repo and its sister Grok Bot templates (Hermes API Fleet, Hermes Fleet Ops, n8n Master, and the legacy Hermes SSH Relay) are versioned together. A fabric version names the doctrine every template in the set follows. When a release changes shared doctrine, every affected sister template is updated in the same release. See [FABRIC.md](FABRIC.md).

## v0.2.0 (2026-09-28)

The intent release. Commander's Intent is now a real document at the root of the repo, created by interviewing the Owner, turned into shared fleet memory, and backed by a security policy.

### Added
- **`COMMANDERS-INTENT.md`**: the fleet-wide source of truth, shipped as a scaffold. Fixed doctrine grounded in mission command (purpose, key tasks, end state; disciplined initiative; act within intent when the plan breaks), plus slots the Owner fills by interview: purpose, end state at 90 days and one year, key tasks, main effort, keep-alive floors, the one thing never to risk, the never-without-GO list, risk tolerance, spend limit and named spenders, conflict rules, who decides what, chain of command, blocked and drift preferences, communication. Also: moving the ball forward, the decision ladder when blocked, halt conditions, orders that carry intent two levels up, three kinds of authority with one merge owner, drift prevention (version, checksum, wake line, correction loop), verify and fail loud, quota and token discipline, precedence, and amendment rules (only the Owner amends).
- **`interview/commanders-intent-interview.md`**: the Chief of Staff's staged interview (22 questions plus probes), playback, explicit approval as v1.0, and the re-interview and amend flow.
- **`skills/commanders-intent-interview`**: runs the interview, writes the approved file under `/home/box`, optionally commits it to the Owner's repo with their yes, builds the `commanders-intent` mental model, and notifies the fleet.
- **`mental-models/commanders-intent.md` and `.json`**: the Hindsight mental model built from the approved intent, scoped by version tag, refreshed on every version bump and weekly.
- **`examples/commanders-intent-example.md`**: a fictional filled intent, marked example only.
- **`SECURITY.md`**: threat model and trust boundaries, authority rules, human-in-the-loop gates, secrets, prompt injection, repo supply chain, a cloud coding agent section (Cursor cloud agents, Claude Code on the web, OpenAI Codex cloud, GitHub Copilot cloud agent, Devin) with vendor facts checked on 2026-09-28, Hermes network rules, memory hygiene, data handling, computer-wipe survival, incident response runbook, and private vulnerability reporting.
- **`skills/quota-token-discipline`**: one digest per task, no FYI wakes, right-sized models, no tight polling, loud quota and model-fallback warnings.
- `tools/hindsight/hs.py`: `mm create`, `mm patch`, and `mm refresh` subcommands.
- `social/x-article-v0.2.md`: release article.

### Changed
- **`FIRST-RUN.md`**: step 1 is now the Commander's Intent interview, before any other setup; then memory and the mental model, alignment confirmation with the Owner, and a review of the `SECURITY.md` gates. Later steps renumbered (now 0 to 12). 25 skills.
- **Wake line** gains the intent version and checksum: `DOCTRINE <INTENT_COMMIT_SHA> | INTENT <version> <checksum12> | LANE <lane>` (v0.1 short form accepted until the next audit). Updated in `persona/SOUL.md` and `soul-md-template`.
- `commanders-intent`, `chief-of-staff-persona`, `persona/SOUL.md`, and `commanders-intent-getting-started` point to `COMMANDERS-INTENT.md` as the canonical doctrine instead of restating it. The v0.1 six-question interview is superseded.
- "COS role and fleet self-healing" section restored (scrubbed and placeholdered) in the `commanders-intent` skill and intent section 14.
- `hermes-fleet-bws-inventory`: secret checks report present or not present only, never length.
- `engineering-playbook`: mandatory cloud coding agent security rules, pointing to `SECURITY.md` section 9.
- `fleet-stand-up-runbook` step 1 now runs the interview.
- `README.md`, `INSTALL.md`, `SETUP.md`, `FABRIC.md`, `OPEN-QUESTIONS.md`, and `MANIFEST.md` updated; `FABRIC.md` names `COMMANDERS-INTENT.md` as the root of the fabric.
- New install placeholders: `<NAMED_SPENDERS>`, `<MERGE_OWNER>`, `<OWNER_GITHUB_HANDLE>`.

### Known open items
- See `OPEN-QUESTIONS.md` "Added in v0.2.0": the new `hs.py` subcommands are checked against the API schema but not yet run live; private vulnerability reporting and branch protection are off on this repo until the Owner decides.

## v0.1.0 (2026-09-28)

First public release.

### Added
- **Commander's Intent root document** method: six-question Owner interview, fixed section template, Git as source of truth, memory bank as derived view (`skills/commanders-intent`).
- **Chief of Staff persona** as the single point of contact, with order, escalation, and status-report templates (`persona/SOUL.md`, `skills/chief-of-staff-persona`).
- **Proactivity at every level:** soul, routines, and skills all end with "what else is silently broken, what did I promise, what's due?" and act in the same turn.
- **Four routines** with copy-paste prompts and cron values: proactivity sweep (30 min), compliance audit (daily), order follow-up (15 min), update-survival restore (hourly).
- **Fleet self-healing spec:** 10-minute host checks, auto-fix of known failures, a fleet status file, alerts, and nightly reflection that adds a guard per new failure class (`fleet/self-healing.md`).
- **Verify-by-read-back** and **failure-to-permanent-guard** skills.
- **One Hindsight memory bank** for the whole fleet, with mental-model CRUD and a standard-library REST helper (`tools/hindsight/hs.py`, bank from `HINDSIGHT_BANK`).
- **Computer-update survival:** state under `/home/box`, idempotent restore scripts, hourly self-restore, and a drill. Proven live on 2026-09-27: restore completed in 137 seconds with no human step.
- **HTTP-only Hermes talk path** on :8642 over a private network; SSH relay listed only as a legacy alternate.
- **Minimal-change operator** as a mandatory fleet-wide skill with [VERIFIED]/[INFERRED]/[UNKNOWN] labels.
- `FIRST-RUN.md` (the script the installed bot follows), `INSTALL.md`, `FABRIC.md`, this changelog, and the release article `social/x-article-v0.1.md`.
- `commanders-intent-getting-started` skill.

### Changed (from the internal draft pack)
- Standing rule 11 (computer-update survival) added to the standing-rules footer of every skill and routine, so all files carry the same 11 rules.
- Routine counts reconciled to four across `SETUP.md`, `routines/README.md`, and the stand-up runbook.
- Draft-only TODO markers replaced with pointers to `fleet/self-healing.md`.
- Memory-key example in `soul-md-template` corrected to `HINDSIGHT_API_KEY`.

### Known open items
- See [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md). Template size caps, routine timezone semantics, and exact Hermes cron syntax are still [UNKNOWN].
