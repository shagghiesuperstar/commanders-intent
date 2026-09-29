---
name: fleet-stand-up-runbook
description: "Use this when standing up the agent fleet from zero — installing the private net, Hermes Agent, the shared memory bank, secrets, skills, routines, and the self-healing cron across every host."
---

# Fleet stand-up runbook

## Purpose / method / observable end state

- **Purpose.** Bring the fleet from bare hosts to a working, governed, self-healing agent fleet in one pass, without the Owner babysitting each step.
- **Method.** Run the 12 steps below in order. Each step ends with an **observed** verify check, not a hope. Skip nothing. If any step blocks, report BLOCKED to the Owner in the same turn with the failing check, and stop. Don't paper over failures to keep marching — the fleet stands up once, correctly.
- **Observable end state.** Every host answers `GET /health` on its loopback Hermes port over the private net; the memory bank holds the setup facts; the self-healing cron is live; governance canaries pass; the Owner sees one executive read-back, not twelve pings.

## Preconditions (verify before step 1)

- The Owner has approved the mission and the chain of command. [INFERRED — Owner approval is the gate]
- The Owner has chosen the canonical intent commit. Capture as `<INTENT_COMMIT_SHA>`.
- A secrets manager project `<SECRETS_PROJECT>` exists with the Owner authorized to mint items.
- The Tailscale tailnet `<PRIVATE_NET_NAME>` exists; the Owner is signed in on the control host `<CONTROL_HOST>`.
- The governance repo `<GOVERNANCE_REPO>` exists and is reachable from `<WORKHORSE_HOST>`.

If any precondition is missing, **stop and tell the Owner in one ask, six parts, no fragments**. Do not invent.

## Proactivity rule (hard, applies to every step)

You are the sole instigator. After every step, end by asking: *what else is silently broken, what did I promise, what's due?* Then act. If a verify check fails, **fix it yourself or order the fix with deadline + required proof in the same turn**. If the Owner skips your question, act on your own recommendation **only for reversible work** — never for gated/irreversible work (DNS, spend, secrets, destructive ops). Every failure becomes a permanent guard (check, cron, test, or directive) so it cannot recur silently.

---

## Step 1 — Write Commander's Intent in Git

**Action.** Run the Commander's Intent interview with the Owner (skill `commanders-intent-interview`, script `interview/commanders-intent-interview.md`). The Owner's answers fill the slots in the `COMMANDERS-INTENT.md` scaffold; the fixed doctrine (five hard rules, initiative within intent, drift prevention, chain of command) stays as shipped. After the Owner explicitly approves the text as v1.0, save it under `/home/box/agent-data/commanders-intent/`, and with the Owner's yes commit it to the root of `<GOVERNANCE_REPO>` as `COMMANDERS-INTENT.md`. Capture the commit SHA as `<INTENT_COMMIT_SHA>` and the file's SHA-256 (first 12) as the intent checksum.

**Verify.** `git -C <GOVERNANCE_REPO> log -1 --format=%H -- COMMANDERS-INTENT.md` matches `<INTENT_COMMIT_SHA>`; the file has zero `{{...}}` slots; `sha256sum` matches the recorded checksum; the five hard rules are present.

**Rollback.** `git revert` the commit. Intent is the source of truth, so reverting is safe; nothing else should depend on a particular intent version yet — that gate goes in at step 10.

---

## Step 2 — Create the one shared memory bank

**Action.** Provision a single Hindsight Cloud memory bank. Store its ID as `<MEMORY_BANK_ID>`. Mint a masked secret named `<MEMORY_API_KEY_SECRET>` inside the secrets project `<SECRETS_PROJECT>`. Load the secret onto every host that will read or write the bank (typically `<CONTROL_HOST>` and `<WORKHORSE_HOST>` for now; agents get their copy at step 4). [INFERRED — Hindsight Cloud API surface is from the brief; verify exact endpoints in official docs]

**Verify.** `GET /banks/<MEMORY_BANK_ID>` returns 200 with a non-empty body from `<CONTROL_HOST>` using the secret from the secrets manager (never echo the secret in logs). The same key works from `<WORKHORSE_HOST>`. Two hosts sharing one bank confirms "one bank, not per-agent" — the directive.

**Rollback.** Delete the bank. Rotate the secret in the secrets manager. Agents holding the old key fail fast on next call — that's intended, not silent failure.

---

## Step 3 — Join hosts to the Tailscale private net

**Action.** On each of `<HOST_1>` .. `<HOST_4>`, `<CONTROL_HOST>`, `<WORKHORSE_HOST>`, `<CODE_MAP_HOST>`, run `tailscale up` with the tailnet `<PRIVATE_NET_NAME>` tag the Owner approved. Confirm `tailscale status` shows each host. [VERIFIED — Tailscale `up` / `status` are standard CLI; specific flags vary, verify in official docs]

**Rules (non-negotiable).**
- Private net only. **No Tailscale Funnel.** Public exposure is a reputation risk and the brief forbids it.
- MagicDNS names look like `<PRIVATE_NET_HOSTNAME>`; never copy them into the public repo or memory unredacted.

**Verify.** `tailscale ping` between every pair of hosts returns success; `tailscale status --json` shows each host in the same tailnet with the approved tags.

**Rollback.** `tailscale down` per host. Audit any host that briefly held a public cert.

---

## Step 4 — Install Hermes Agent on every host

**Action.** On each of `<HOST_1>` .. `<HOST_4>`, `<WORKHORSE_HOST>`, `<CODE_MAP_HOST>`:
1. Install Hermes Agent (open-source, Nous Research) per official install instructions. [VERIFIED — install method; specific package name and version verify in official docs]
2. Enable the Hermes HTTP API server on loopback `:8642`. **Never bind to a public interface.** Require a strong bearer key, loaded from `<SECRETS_PROJECT>` as `<HERMES_API_KEY_SECRET>`. The key never appears in plaintext in any file, log, or commit.
3. Expose the API to the tailnet via `tailscale serve` (private), **not Funnel**. Soak the port as `<HOST>:8642` reachable only over `<PRIVATE_NET_NAME>`.
4. Add a host-local escape hatch: long jobs POST to `http://127.0.0.1:8642/v1/runs` with `{"input": "..."}`, poll `GET /v1/runs/{run_id}`. Auth: `Authorization: Bearer <HERMES_API_KEY_SECRET>`. [INFERRED — endpoint shapes are per the brief; verify exact routes and timeout values in official docs]

**Forbidden.**
- SSH relay for talking to an agent. Loopback HTTP on `:8642` over the private net is the **sole** ask path.
- Echoing the bearer key anywhere. If it leaks, rotate the same turn.

**Verify.** From `<CONTROL_HOST>` over the private net: `curl -fsS -H "Authorization: Bearer $KEY" http://<PRIVATE_NET_HOSTNAME>:8642/health` returns 200 with `{"status":"ok"}` on every host. `curl` without the key returns 401. `curl` from a non-tailnet IP returns connection refused (no Funnel leakage).

**Rollback.** `tailscale serve reset`; stop the API; uninstall the agent; rotate the key. Re-run step 4 from scratch on affected hosts.

---

## Step 5 — Wire per-host health/ask connectors in Grok Bot

**Action.** In the COS configuration, register one **health** connector and one **ask** connector per host. Each connector points at the host's loopback API over the private net, uses its own `<HERMES_API_KEY_SECRET>` copy, and respects the 120s connector timeout (around `-32001` on long asks). [INFERRED — timeout code from the brief; verify exact error code in official docs]

**Verify.** Trigger a health probe per host — all green. Trigger one ask per host with a short prompt — all return content. Trigger one ask that would exceed the connector timeout — observe it fail with the expected code and route via the `/v1/runs` escape hatch instead, returning a `run_id` you can poll.

**Rollback.** Remove the connector entries; the per-host API keeps running independently, which is the point — connectors are Grok Bot-side wiring, not the agent's lifeline.

---

## Step 6 — Deploy SOUL.md to every host

**Action.** Ship `SOUL.md` (from the `soul-md-template`) to each host's `<WORKSPACE_PATH>`. The file must contain, at minimum: the chain of command, the four hard rules, the proactivity rule, the no-secret-in-memory rule, and the version-gate (`block if intent commit != <INTENT_COMMIT_SHA>`).

**Verify.** `sha256sum SOUL.md` is identical across all hosts. `grep` confirms each of the four hard rules is present on every host.

**Rollback.** Replace with the previous known-good SOUL.md (keep one in the repo). Track the rollback as a guard: if SOUL drifts across hosts again, the canary in step 10 catches it.

---

## Step 7 — Install skills

**Action.** For each skill in the template pack (`cos-product-manager`, `code-mapper`, `heartbeat-triage`, `memory-curator`, `policy-writer`, etc.), drop the skill file into each host's skills directory. Do not invent new skills mid-stand-up — installing the canonical set is the gate.

**Verify.** A named agent on each host can list its installed skills and the list matches the template pack exactly. Spot-run one skill per host to confirm it executes (not just loads).

**Rollback.** Remove the skill file; the agent continues operating with the remainder.

---

## Step 8 — Create the four routines manually

**Action.** Create the routines from `routines/`: **proactivity sweep** (every 30 min), **compliance audit** (daily), **order follow-up** (every 15 min), **update-survival restore** (hourly, every day). Each routine ends by asking *what else is silently broken, what did I promise, what's due?* and acting (or escalating to the Owner with a six-part ask).

**Verify.** Trigger each routine on one host, observe the expected output, confirm the trailing self-prompt is present and acted upon (not just logged).

**Rollback.** Delete the routine files; nothing downstream depends on them yet.

---

## Step 9 — Install the 10-min self-healing cron and nightly reflection per host

**Action.** Per host, install a native Hermes cron that runs every 10 minutes: health checks, auto-fix known failures, write `<WORKSPACE_PATH>/fleet-status.json`, alert `<ALERT_CHANNEL>` on anything not auto-fixed. Install a nightly reflection job that reviews the day's failures and near-misses, writes a new check for each new failure class into the cron, and commits the change. [INFERRED — `fleet-status.json` is from the brief; exact schema and Hermes cron syntax verify in official docs]

**Verify.** Wait one cron tick (or fast-forward by invoking it once): `fleet-status.json` exists, is recent, and reports healthy on a clean host. Force a fake failure on one host — the cron catches it, alerts, auto-fixes if possible, else escalates. The nightly job is schedule-verified, not necessarily run yet.

**Rollback.** Disable the cron entries; remove `fleet-status.json`. Verify alerts stop.

---

## Step 10 — Run governance canaries

**Action.** Run the six canaries from the brief against the live fleet: intent conflict, stale intent commit, unauthorized merge/deploy/spend/DNS, failed check under deadline pressure (must report BLOCKED, not DONE), secret-in-memory (refuse), incomplete decision ask (don't send), ask can't complete (return to Owner immediately), over-abstraction (push back). Each must score 100% hard, 95% soft. [VERIFIED — the six canaries are governance requirements from the brief]

**Verify.** Each canary fires the expected refusal or BLOCKED state when triggered with a synthetic input; each passes 100% on the soft target.

**Rollback.** No fleet-wide rollback — fix the failing canary's rule or guard, re-run. A canary that passes by being silenced is a silent failure; do not accept.

---

## Step 11 — Read-back everything to the Owner (one ask, six parts)

**Action.** Send a single executive read-back to the Owner containing, in order:
1. **Context** — what was stood up and on which hosts.
2. **Decision needed** — none, unless a step blocked or a guard needs Owner sign-off.
3. **Options** — only if a blocker exists.
4. **Recommendation** — only if a blocker exists.
5. **Rationale** — only if a blocker exists.
6. **Confidence** — high on stand-up complete; low/medium only on items the Owner should re-check (e.g. Funnel audit, intent wording).

Attach the per-step verify transcripts and the canary scores. **No filler, no flattery.**

**Verify.** Owner acknowledges. If silent, follow up at the deadline the COS sets, then escalate.

**Rollback.** Not applicable — this is a report. If the read-back itself is wrong, correct it in the next turn and log the correction as a guard.

---

## Step 12 — Retain setup facts to memory

**Action.** Write the following facts to the one shared memory bank `<MEMORY_BANK_ID>` as locked, evidence-labeled entries:
- `<INTENT_COMMIT_SHA>` labeled `[VERIFIED]`.
- `<MEMORY_BANK_ID>` labeled `[VERIFIED]`.
- Per-host: hostname, MagicDNS name `<PRIVATE_NET_HOSTNAME>`, install status, SOUL.md hash, last cron tick, last health check result. All `[VERIFIED]`.
- Per-secret name in `<SECRETS_PROJECT>` (name only — never the value). `[VERIFIED]`.
- Per-step blocker or near-miss from this run, labeled `[INFERRED]` until re-checked, with a follow-up date.

**Verify.** `GET` each fact back from the bank; values match the live system. The intent entry is the **cached mental model only** — Git is the authority. If Git and memory disagree, treat Git as truth and re-derive memory next cycle.

**Rollback.** Memory holds mental models, not authority — bad entries are corrected in place, not rolled back. A memory entry that gets corrected twice in 30 days is a candidate for permanent deletion.

---

## After this runbook: what the bot owes itself

- A canary that fails after stand-up is a stand-up defect. Add a guard, re-run.
- Any near-miss in steps 1–12 becomes a one-line check appended to the nightly reflection job, not a forgotten story.
- The morning routine re-asserts: intent commit in Git == intent commit in memory == intent commit the agents are running under. Drift = BLOCKED.

The fleet stands up once. The next time the Owner adds a host, this runbook is the reference, not the rebuild plan.

> **Self-healing section.** The Chief of Staff's role in fleet self-healing is defined in `fleet/self-healing.md` (10-minute host checks plus nightly reflection). If your Commander's Intent adds a dedicated section for it, mirror it here.


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
