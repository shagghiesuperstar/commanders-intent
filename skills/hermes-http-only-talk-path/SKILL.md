---
name: hermes-http-only-talk-path
description: "Use this when wiring a Hermes Agent ask/health/manage connector, when an ask or health check fails, when MCP custom instructions still mention SSH, or any time an SSH relay tempts as a fallback. SOLE PATH is HTTP API on port 8642 over the private net."
---

# Hermes HTTP-only talk path

## When to use
Any ask, health, or manage call to a fleet Hermes Agent host, or any time connector prompts, MCP instructions, operator reflexes, or a template still mention SSH as a path to Hermes.

## Standing lock
**SOLE PATH:** Hermes native HTTP API on port `:8642` [VERIFIED — fleet architecture] over the private network, reached via per-host connectors (e.g. `hermes-<HOST_1>`, `hermes-<HOST_2>`, `hermes-<HOST_3>`, `hermes-<HOST_4>`). Auth is a Bearer token loaded from the host's local environment; never echoed.

**SSH relay to Hermes is FORBIDDEN** as an ask or manage path. Not "prefer HTTP" — there is no SSH door for talking to Hermes. Long jobs escape the connector's ~120s ask timeout (error code `-32001` [VERIFIED — fleet architecture]) via host-local `POST http://127.0.0.1:8642/v1/runs` with body `{"input": "..."}`, then poll `GET /v1/runs/{run_id}` [INFERRED — poll pattern from fleet reference]. Host surgery for rare, non-talk work uses a separate host-surgery procedure, never this skill, and only after the HTTP API has been proven insufficient.

## Symptom this kills
Operators (and bots) say "HTTP API" but health "magically" flips back to ok on its own. Cause: live connectors already speak HTTP `:8642`, but stale `mcpCustomInstructionsByServerId` entries still label old server IDs as SSH, and soft wording like "HTTP not SSH" or "X may SSH" leaves an SSH option on the table. The first call that succeeds is the real HTTP path — the SSH wording is what confused the retry.

Lesson: "prefer HTTP" is a bug. Wording must deny SSH as an option, not deprioritize it.

## Hard-kill checklist (controller / Chief of Staff)
1. Audit `mcpCustomInstructionsByServerId` for every Hermes server (named + live IDs). Purge any entry whose text names SSH as a path.
2. Rewrite **all** Hermes MCP instructions — named and live-ID — to start with: `SOLE PATH HTTP :8642 — SSH RELAY IS FORBIDDEN`. No "prefer". No "may". No fallback clauses.
3. Update host identity prompts on every host the same way. SSH does not exist as a talk path.
4. Snapshot config before edits (e.g. `<WORKSPACE_PATH>/backups/hermes-http-only-YYYYMMDD_HHMMSS`).
5. Verify: connector `health` returns `mode=http`, status `ok` [INFERRED — expected response shape]; runtime MCP instructions begin with `SOLE PATH… SSH RELAY IS FORBIDDEN`.

## Common confusions (do not let them reopen the door)
- **Connector tool schema** for `health` may still say "SSH or HTTP" in the bridge package copy. Patch the schema so it cannot re-teach SSH. Schema text is the long tail of this failure [INFERRED — common in connector packages].
- **Ask timeouts (`-32001`)** are sidecar / fluidity issues, not path confusion. Fix sidecar or the private network, do not switch to SSH.
- **Health says ok after a delay** but no live HTTP call landed: that is the SSH-shaped hallucination above. Treat as not-ok until an observed HTTP round-trip is logged.

## Other templates
- **Hermes API Fleet** (primary talk path: `:8642`): keep installer docs aligned with SOLE PATH language. Any text saying "prefer HTTP" or "may SSH" is a regression.
- **Hermes Fleet Ops** (fleet ops, secrets, homogenize): same rule. Talk path is HTTP only. Do not document SSH as a fallback for ask / manage.

## Never
- Probe SSH as a first call when `:8642` flakes. Fix the sidecar, private network, or API.
- Fall back to SSH when health or ask fails. Report `BLOCKED on HTTP path` and fix the HTTP path; do not route around it.
- Use soft wording like "prefer HTTP" or "may use SSH" anywhere — that wording is the bug.
- Echo or store Hermes bearer tokens in chat, templates, or memory.

## Docs
- Official Hermes Agent: https://hermes-agent.nousresearch.com/docs/

## Proactive triggers
Run this skill without being asked whenever any of these are true:
- A new Hermes connector is being wired or renamed, before the first ask goes through it.
- Any connector or MCP instruction in the fleet mentions SSH as a talk path (even once, even in a comment).
- An ask or health check fails or returns a path / timeout error and the cause is unclear.
- The Chief of Staff's nightly reflection surfaces any Hermes health oddity, even if it self-resolved.
- A new host is being added to the fleet; SOLE PATH wording must be in its identity prompt before it takes live traffic.
- A template (API Fleet, Fleet Ops, or any marketplace installer) is updated; audit its wording for "prefer HTTP" / "may SSH" regressions.
- The native 10-minute per-host cron reports a Hermes flapping state on any host.

After acting, ask: what else is silently broken, what did I promise, what's due? Fix it in this turn, or assign the Owner a fix with a deadline and required proof, then follow up at the deadline. Every silent SSH relapse becomes a permanent guard (cron check on connector instruction text, schema lint, or alert) so it cannot recur silently.


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
