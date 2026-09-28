# Changelog

All notable changes to the Commander's Intent fabric. Versions follow semantic versioning. Newest first.

> **Fabric note.** This repo and its sister Grok Bot templates (Hermes API Fleet, Hermes Fleet Ops, n8n Master, and the legacy Hermes SSH Relay) are versioned together. A fabric version names the doctrine every template in the set follows. When a release changes shared doctrine, every affected sister template is updated in the same release. See [FABRIC.md](FABRIC.md).

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
