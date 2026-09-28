---
name: wire-hermes-native-api
description: "Use this when an installer needs to enable Hermes Agent's native HTTP API on port 8642 on an agent host, verify health, or add a private-network-reachable hermes-<hostname> connector in the orchestrator (Grok Bot / Chief of Staff)."
---

# Wire Hermes native API

## When to use
Installer wants the native Hermes Agent HTTP API method (gateway + API server on port 8642) on an agent host, and wants to expose it to the orchestrator over the private network (e.g. Tailscale tailnet `<PRIVATE_NET_NAME>`).

## Standing lock (fleet governance)
The talk path between the orchestrator and any agent host is **SOLE PATH HTTP :8642** over the private network. SSH is **not** an ask path: do not use SSH to talk to Hermes Agent, do not run an SSH relay, do not fall back to SSH when `:8642` flakes. This applies to every identity bot the orchestrator owns (the named bot personas on each host). Soft "prefer HTTP" is wrong — there is no SSH ask door [VERIFIED].

## Preconditions
- Hermes Agent gateway running with `API_SERVER_ENABLED=true` on the host [VERIFIED].
- A strong `API_SERVER_KEY` stored only in the secrets manager (e.g. secret name `<HERMES_API_KEY_SECRET>` in project `<SECRETS_PROJECT>`). Never in templates, repos, or chat paste.
- `API_SERVER_HOST` bound to a private-network address — never Funnel, never public internet [VERIFIED].
- Orchestrator can `curl http://<PRIVATE_NET_HOSTNAME>:8642/health` and an authenticated `GET /v1/models` from the tailnet.

## Steps
1. Confirm the gateway + API server are running on the Hermes host; restart the gateway after any env change so the new key/host bind takes effect.
2. Verify from the orchestrator host over the private network: hit `/health` first (expect 200), then authenticated `GET /v1/models` with `Authorization: Bearer <API_SERVER_KEY>`. Expect the response to indicate HTTP mode (e.g. `mode=http` or equivalent marker) [VERIFIED].
3. Add one connector per host named `hermes-<hostname>` pointing at the base URL `http://<PRIVATE_NET_HOSTNAME>:8642` plus the Bearer key pulled from the secrets manager (reference the secret by name, never paste the value).
4. Set the bot instructions / system prompt to **SOLE PATH HTTP :8642 — SSH IS NOT AN ASK PATH**, naming the live host identifier. Delete any orphan instructions that still mention SSH as a talk path.
5. Smoke-test with a tiny ask + a health call; do not write into Hermes memory plugins unless a memory write was explicitly planned. Long jobs escape via host-local `POST http://127.0.0.1:8642/v1/runs` with body `{"input": "..."}`, then poll `GET /v1/runs/{run_id}`; connector asks time out around 120s (-32001) [VERIFIED].
6. Hosts that run no Hermes gateway at all are out of scope for this skill. Do not wire an alternative ask path; flag the host as BLOCKED and route the fix through `<FLEET_OPS_AGENT>`.
7. Messaging bots are orthogonal: if a host also runs Telegram/Discord across profiles, route that to Hermes Fleet Ops and the messaging-token-isolation skill (`:8642` does not resolve a shared `TELEGRAM_BOT_TOKEN` conflict across profiles — one bot token lives on exactly one host).

## Never
- Pack, echo, log, or paste API keys, SSH keys, or live ledgers anywhere (templates, chat, memory, commits).
- Suggest Funnel or any public bind of `:8642`.
- Probe SSH or fall back to SSH when `:8642` flakes — report BLOCKED on the HTTP path and fix the sidecar, tailnet, or API key, not the transport.
- Promote this bot into a fleet ops orchestrator — stay on template hygiene and installer wiring.
- Recommend or link any SSH-relay template or skill: SSH is not an ask path, period.

## Proactive triggers
Run this skill without being asked when any of the following is observed [INFERRED]:
- A new agent host appears in the fleet and has no `hermes-<hostname>` connector in the orchestrator.
- The orchestrator's connector list shows a host with an empty, missing, or stale key reference.
- The nightly cron on a host writes `<WORKSPACE_PATH>/fleet-status.json` and the Hermes health probe is missing, failing, or older than the freshness window.
- A bot instruction is edited to mention SSH as a talk path, or an SSH-related instruction ID is left orphaned after a host rename or rebuild.
- The Owner asks "why is the orchestrator not talking to `<HOST>`?" and the last successful `:8642` health check is older than the freshness window.
- After any connector edit, re-run steps 2 and 5 inside the same turn; if either fails, order the fix with a deadline and required proof (live `curl /health` + authenticated `/v1/models` output) before reporting done.
- A failure recurs: convert it into a permanent guard (cron probe, connector liveness check, or directive) so it cannot recur silently.

## Docs
- Official Hermes Agent repository and documentation (Nous Research): https://github.com/NousResearch/hermes-agent [VERIFIED]
- Hindsight Cloud docs (memory bank wiring is independent of this skill) [INFERRED]


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
