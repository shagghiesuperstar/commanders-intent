---
name: fleet-post-sprint-hygiene
description: "Use this when a Hermes or Grok orchestration sprint finishes long asks, merges, browser smokes, CLI harnesses, or heavy SSH work — before declaring DONE or publishing/updating shared templates. Ensures the ask bus is HTTP :8642 only, long jobs use /v1/runs when MCP times out near 120s, no orphan browsers or CLI processes remain, and secrets stay in the secrets manager."
---

# Fleet post-sprint hygiene

## Proactive triggers
Run this skill WITHOUT being asked when ANY of these are true:

- A Hermes or Grok orchestration sprint just ended (declared status, returned control, or went idle).
- A long ask returned `-32001` or a ~120s MCP/sidecar timeout within the last sprint.
- A browser/computer-use subagent was spawned during the sprint and may still be alive.
- Any host was touched over SSH for host surgery, even if the ask itself used HTTP.
- Before `Share→Update` of any shared template or before publishing a new marketplace/playbook entry.
- The fleet nightly reflection notes orphan processes, leftover SSH sessions, or pasted secrets in chat.

If you cannot prove all post-sprint checks passed, do not declare DONE — return BLOCKED with the failing check.

## When to use
After any Hermes/Grok orchestration sprint involving long asks, merge/PR work, browser smokes, CLI harnesses, or heavy host surgery — before declaring DONE or publishing/updating shared templates.

## Standing law
- Fleet / identity talk path = **HTTP `:8642` only**. SSH is NOT an ask path for fleet Hermes. SSH is forbidden for talking to agents; it may be used only for rare host surgery after the API is proven insufficient, never as a fallback for a timed-out ask. [INFERRED — fleet reference architecture in Commander's Intent]
- Long tool jobs: prefer host-local Hermes `POST http://127.0.0.1:8642/v1/runs` with body `{"input": "..."}`, poll `GET /v1/runs/{run_id}` when the connector ask dies near 120s (`-32001`). [INFERRED — Hermes connector ~120s timeout] Raise the local sidecar timeout first; only take an upstream Hermes PR if you can reproduce the Desktop hang.
- Orchestrator (Chief of Staff, <COS_NAME>) routes asks; troubleshooting digs → dedicated Hermes frontier session, not orchestrator token burn.

## Checklist (run every time)
1. **Ask bus:** short `health` returns OK on every host that participated. If any tool ask returned `-32001` near 120s, switch that job to `/v1/runs` or raise the local sidecar timeout; do NOT invent a merged/OK status.
2. **SSH leftovers:** no orphan SSH MCP/connector instructions labeled as an ask path; fleet connectors say HTTP-only. SSH is not an ask path.
3. **Browser agents:** stop orphan computer-use / browser subagents from the sprint; pin one browser-limb host and stick to it; do not use the human as a Network tab.
4. **CLI harnesses:** kill stuck Codex / Claude / `gh` / cloud-agent CLIs and leftover `tmux` / `screen` jobs from the sprint.
5. **Heavy SSH:** close idle SSH sessions announced as `SSH-IN-PROGRESS`; no cross-host Hermes SSH.
6. **Secrets:** nothing pasted in chat; secrets manager (e.g. Bitwarden Secrets Manager) only; no private restore URLs in any public pack.
7. **Templates:** if playbooks changed, stage them on the staging lane, then have the Owner do the `Share→Update` (never publish from the orchestrator).

## Verification (observed, not inferred)
- Fleet `health` returns HTTP-mode OK on every host that ran the sprint.
- No stray browser / CLI / `tmux` / `screen` processes remain from the sprint.
- No pasted secrets, private URLs, or SSH-ask instructions found in any pack or memory entry from this sprint.
- If this sprint was a fleet incident, the hygiene boxes are checked in the incident tracker.

## Permanent guards (failures must not recur silently)
- Cron on each host every 10 minutes: health check + auto-kill of known orphan browser/CLI processes; write status to `<WORKSPACE_PATH>/fleet-status.json`; alert <ALERT_CHANNEL> on anything not auto-fixed.
- Nightly reflection: review the day's failed hygiene checks; add one new check per new failure class.

## End-of-skill proactivity (mandatory)
Before reporting done, ask yourself: *what else is silently broken, what did I promise, what's due?*

- Any silent failure found → fix it yourself or order the Owner to fix it with a deadline and required proof, in this turn.
- Any order to the Owner → follow up at the deadline.
- Any skipped Owner question → act on your own recommendation for reversible work (never for gated/irreversible work).
- Every failure → a new permanent guard so it cannot recur silently.

If a check fails and you cannot fix it now, return BLOCKED (never DONE).

## Related
- Skill: minimal-change-operator (fleet-wide mandatory)
- Vendor docs: Hermes Agent native API (HTTP :8642), Hindsight Cloud, Tailscale
- Governance: Commander's Intent → Engineering doctrine → Fleet reference architecture


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
