---
name: hindsight-mental-models
description: "Use this when creating, listing, refreshing, dry-running, clearing, or deleting Hindsight Cloud mental models in the single fleet memory bank, so every fleet member can push and read the same living summaries."
---

# Hindsight mental models (fleet push)

## Proactive triggers
Run this skill without being asked when:
- A new standing lock, SOP, status report, auth map, bake gate, or other "always check this first" knowledge is declared and needs to be published as a living summary.
- A dry-run refresh shows drift (`mode_fallback_reason`, fact-count delta, missing facts, or stale `last_memory_seen_at`) — clear and re-refresh in the same turn.
- A `source_query` was PATCHed without a refresh — auto-refresh (update alone does not regenerate).
- A new fleet member (host, Grok bot persona, cloud coding agent) joins and needs the same context.
- Reflect on a related query does not surface an expected model — investigate (missing facts, wrong tags, deleted model, wrong bank).
- Facts were retained for a lock that has no model yet — create one in the same turn.
- A scheduled cron is due and the target model has fresh facts — refresh.
- Two fleet members give conflicting answers on a high-priority topic — publish a mental model that locks the answer.

After any action, ask: what else is silently broken, what did I promise, what's due? Act on it (fix it, or order the fix with deadline + required proof in the same turn). Follow up at the deadline. If a question to the Owner is skipped, act on your own recommendation for reversible work (never for gated/irreversible work). Turn every failure into a permanent guard (check, cron, test, or directive).

## When to use
Use this when the fleet needs to **proactively publish living summaries** into Hindsight Cloud so every fleet member (hosts running Hermes Agent, Grok bot personas including COS, and cloud coding agents) can reference the same high-priority context on Reflect/recall — locks, SOPs, status reports, directories, bake gates, auth maps, and other "always check this first" knowledge.

Mental models sit at the **top of Hindsight's hierarchy** (Mental Models → Observations → Raw Facts). Reads are a fast cached lookup (no LLM at get time). Creates/refreshes run Reflect in the background and cost mental-model / reflect tokens.

## Standing locks
- **One bank for the whole fleet: `<MEMORY_BANK_ID>`.** Every host running Hermes Agent, every Grok bot persona, and every cloud coding agent reads and writes the same Hindsight Cloud bank. There is no other bank and no other durable-memory store.
- **Ordinary memory work** (recall, reflect, retain, reading mental models) goes through the fleet's shared `hindsight-memory` skill (CLI helper `<WORKSPACE_PATH>/tools/hindsight/hs.py`, shipped in this repo at `tools/hindsight/hs.py`, e.g. `mm list`, `mm get <id>`; since v0.2.0 also `mm create <body.json>`, `mm patch <id> <body.json>`, `mm refresh <id>`). This skill covers mental-model CRUD only.
- **Who changes models:** any fleet member may list/get models. Create / update / refresh / clear / delete only when COS or the Owner explicitly assigned that job.
- **If Hindsight fails** (auth, 5xx, `BLOCKED:`), report BLOCKED with the reason and retry later. Never save the content somewhere else instead.
- **Talking to hosts** (asking a Hermes Agent host to do work) stays **HTTP `:8642` only**. SSH is not an ask path. That is the talk path, not a memory restriction.
- **API key:** use the existing fleet `HINDSIGHT_API_KEY` (`hsk_…`) from the environment — already set in the standard environment; on hosts, loaded from a secrets manager (e.g. Bitwarden Secrets Manager). Never print, paste, or store the value, and never mint a new key. Prefer the locally-loaded key over a drifted override.
- **Never** put secrets, tokens, private restore URLs, or filled credential maps into a `source_query`, model `content`, or skill paste.

## Mental model (what you are pushing)
A mental model is a **user-curated living document**: you choose `name` + `source_query`; Hindsight runs Reflect and stores markdown `content`. Optionally auto-refresh after consolidation or on a UTC cron. Models are eventually consistent.

Docs: https://docs.hindsight.vectorize.io/mental-models  
OpenAPI base: `https://api.hindsight.vectorize.io`  
Auth header: `Authorization: Bearer hsk_…`

## Endpoint map (all under one bank)  [VERIFIED — Hindsight API docs]

Base path: `/v1/default/banks/{bank_id}/mental-models` (fleet `bank_id` is always `<MEMORY_BANK_ID>`)

| Action | Method | Path |
| --- | --- | --- |
| List | GET | `/` (query: `tags`, `tags_match=any\|all\|exact`, `detail=metadata\|content\|full`; list default `detail=metadata`) |
| Create | POST | `/` → async; returns `operation_id` (+ optional `mental_model_id`) |
| Get | GET | `/{mental_model_id}` (query: `detail`; get default `full`) |
| Update | PATCH | `/{mental_model_id}` (name / source_query / tags / max_tokens / trigger) — **does not** regenerate content |
| Delete | DELETE | `/{mental_model_id}` |
| History | GET | `/{mental_model_id}/history` |
| Refresh | POST | `/{mental_model_id}/refresh` → async `operation_id` |
| Dry-run refresh | POST | `/{mental_model_id}/dry-run-refresh` — same pipeline, **no persist** (preview mode/outcome/diff/fact counts) |
| Clear | POST | `/{mental_model_id}/clear` — wipe content so next refresh is a **full** re-synthesis (fix delta drift) |

Track async work: `GET /v1/default/banks/{bank_id}/operations/{operation_id}` (or `<WORKSPACE_PATH>/tools/hindsight/hs.py op <operation_id>`).

## Create body (required fields)  [VERIFIED — Hindsight API docs]
```json
{
  "id": "fleet-http-only-talk-path",
  "name": "Fleet HTTP-only talk path",
  "source_query": "What is the standing lock for how Hermes fleet agents talk to each other (HTTP :8642 vs SSH)?",
  "tags": ["fleet", "lock", "talk-path"],
  "max_tokens": 2048,
  "trigger": {
    "mode": "full",
    "refresh_after_consolidation": true
  }
}
```

Notes:
- `id` optional — alphanumeric lowercase + hyphens; use **stable fleet IDs** so every fleet member targets the same model.  [VERIFIED — Hindsight API docs]
- `name` + `source_query` required.  [VERIFIED — Hindsight API docs]
- `max_tokens` default 2048, range 256–8192.  [VERIFIED — Hindsight API docs]
- `trigger.mode`: `full` (default) or `delta` (surgical edits; falls back to full if no baseline / source_query changed).  [VERIFIED — Hindsight API docs]
- `trigger.refresh_after_consolidation` and `trigger.refresh_cron` are **mutually exclusive** (cron is UTC 5-field). Prefer consolidation auto-refresh for living locks; cron for daily digests; neither for stable SOPs you refresh on purpose.  [VERIFIED — Hindsight API docs]

## Proactive fleet push playbook

### 0) Bank + key (any fleet member)
1. `BANK_ID=<MEMORY_BANK_ID>` — always. Do not create or target any other bank.
2. Make sure `HINDSIGHT_API_KEY` is in the env (already set in the standard environment; on hosts, load from a secrets manager). Do not echo it. Confirm prefix `hsk_`.
3. Health: `curl -sS -H "Authorization: Bearer $HINDSIGHT_API_KEY" https://api.hindsight.vectorize.io/health/ready`

If health fails or the key is missing, report BLOCKED with the reason. Do not fall back to any other memory store. Add a permanent guard (cron + alert) so the failure cannot recur silently.

### 1) Inventory before create
```bash
curl -sS -H "Authorization: Bearer $HINDSIGHT_API_KEY" \
  "https://api.hindsight.vectorize.io/v1/default/banks/$BANK_ID/mental-models?detail=metadata&tags=fleet&tags_match=any"
```
Skip create if a stable `id` / same name already exists — PATCH + refresh instead.

### 2) Retain facts first (so Reflect has evidence)
Mental models synthesize **what is already in the bank**. Before create/refresh of a new lock:
- Retain the authoritative facts/observations into bank `<MEMORY_BANK_ID>` via the memory helper skill (world facts for locks; experience for "we decided…").
- Wait for consolidation if you enabled `refresh_after_consolidation`.

### 3) Create (async)
```bash
curl -sS -X POST \
  -H "Authorization: Bearer $HINDSIGHT_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.hindsight.vectorize.io/v1/default/banks/$BANK_ID/mental-models" \
  -d @create.json
```
Poll the returned `operation_id` until complete, then:
```bash
curl -sS -H "Authorization: Bearer $HINDSIGHT_API_KEY" \
  "https://api.hindsight.vectorize.io/v1/default/banks/$BANK_ID/mental-models/$MM_ID?detail=content"
```
Verify markdown looks right (no secrets, lock language is hard not soft).

### 4) Safe refresh loop (production)
1. **Dry-run** first for high-stakes / bake / auth models:
   `POST .../mental-models/$MM_ID/dry-run-refresh`
   Check `effective_mode`, `mode_fallback_reason`, `outcome`, `would_persist`, fact counts, and diff.
2. If preview is good → **Refresh** `POST .../refresh` and poll `operation_id`.
3. If delta models have drifted → **Clear** then **Refresh** (forces full rebuild).
4. After **PATCH** of `source_query`, always refresh (update alone does not regenerate).

### 5) How the fleet "references" them
- On Reflect, Hindsight injects matching mental models as **high-priority** context automatically.
- Agents can also **GET** by stable id or **LIST** by tags (`fleet`, `lock`, `bake`, `auth`, …) with `detail=content` when they need the cached text without a Reflect call (CLI: `hs.py mm list` / `hs.py mm get <id>`).
- Everything lives in the single bank `<MEMORY_BANK_ID>`, so a stable `id` means the same model for every host, Grok bot persona, and cloud coding agent. No mirrored per-host banks.

### 6) Suggested starter catalog (push when facts exist)
| Stable `id` | Purpose | Auto-refresh |
| --- | --- | --- |
| `commanders-intent` | The Owner's approved Commander's Intent, scoped to the current version tag. Definition: `mental-models/commanders-intent.md` | weekly cron + manual on every version bump |
| `fleet-http-only-talk-path` | HTTP `:8642` only; SSH ask forbidden | consolidation |
| `fleet-memory-fabric` | Single Hindsight bank `<MEMORY_BANK_ID>` for the whole fleet; key rules | consolidation |
| `fleet-bake-gates` | What must be BAKE_OK before human demo | manual or cron |
| `fleet-host-roles` | Which host owns what lane | consolidation |

Existing policy models (read via the memory helper skill): Commander's Intent, operating doctrine, plan gates, secure-SDLC gates, and execution state — keep their stable IDs identical across the fleet.

Write **specific** `source_query` strings ("What is the standing lock for …?") not vague ones ("Tell me about the fleet").

## Delete / never-do
- Delete only when the operator explicitly retires a model.
- Never dry-run-skip then blast-refresh every model on a schedule without a reason (token burn).
- Never create models whose source_query asks the bank to invent policy that was never retained.
- Never paste `hsk_` into chat or marketplace packs; never target a bank other than `<MEMORY_BANK_ID>`.

## Verification
- List shows the new/updated model under expected tags; `is_stale` / `last_memory_seen_at` make sense after refresh.
- Get `detail=content` returns sensible markdown with no secrets.
- Reflect on a related query lists the model under `mental_models` in the response when applicable.
- Cross-member: another fleet member (host, Grok bot, or cloud coding agent) can list/get the same stable `id` in bank `<MEMORY_BANK_ID>`.

## Install
- Orchestrators / cloud agents: shared skill library at `<WORKSPACE_PATH>/hindsight-mental-models/SKILL.md`.
- Hosts running Hermes Agent: copy to `<USER_HOME>/.hermes/skills/hindsight-mental-models/SKILL.md` on each host (or fleet skill sync). Verify with Hermes skill search / slash command.

## Related
- Concepts: https://docs.hindsight.vectorize.io/mental-models
- API: list/create/get/update/delete/history/refresh/dry-run-refresh/clear under docs.hindsight.vectorize.io/api-reference/*
- cURL examples: https://docs.hindsight.vectorize.io/curl-examples
- Sister skills: the fleet's `hindsight-memory` skill (all ordinary memory reads/writes), the talk-path skill, the secrets-manager inventory skill, the post-sprint hygiene skill.
- Broader daemon/local setup lives in the separate `hindsight` / `hindsight-memory-setup` Hermes skills — this skill is **Cloud mental-model CRUD + proactive fleet push** only.


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
