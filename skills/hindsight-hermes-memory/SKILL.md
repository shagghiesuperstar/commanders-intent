---
name: hindsight-hermes-memory
description: "Use this when any agent in the fleet needs to remember or look up anything durable: recall context before non-trivial work, reflect for a reasoned answer, retain a learning, or read the fleet's mental models in Hindsight Cloud via the REST API. This is the ONLY place durable memory is written; built-in memory files are never a substitute."
---

# Hindsight fleet memory (bank `<MEMORY_BANK_ID>`, REST API)

Every agent in the fleet shares ONE Hindsight Cloud bank: `<MEMORY_BANK_ID>`. There is no other bank; memory volume is never a reason to split. The Hindsight bank is the only durable-memory store; there is no fallback store. Git `<GOVERNANCE_REPO>` is the source of truth; Hindsight is a derived cache. When they disagree, Git wins.

Adapted from Hindsight's official Agent Skill (cloud mode) and the curated tool guidance shipped with the Hindsight MCP server, rewritten for REST so agents need no connector.

[INFERRED] The Hindsight REST API surface used below (`retain`, `recall`, `reflect`, mental models, knowledge base) follows the public Hindsight docs; confirm parameter and flag names against current Hindsight docs before relying on any specific shape.

## HARD RULE: Hindsight is the only memory you write
The Owner has seen agent platforms "cheat" by saving to a local flat file because it is easier. That is forbidden here.
- Every durable fact, decision, outcome, or lesson goes to Hindsight with `retain`. No exceptions for "quick" or "small" facts.
- NEVER write memories to the built-in agent memory (any built-in `update_state` / profile / log / note tier, shared user memory), to memory files under `<WORKSPACE_PATH>`, or to ad-hoc notes / markdown files as a stand-in for memory. The only allowed built-in memory entry is the single pointer rule that sends agents here; do not add to it.
- Never read the flat file as the source of truth. Recall from Hindsight first; if Hindsight has nothing, say so, or check Git, and do not fall back to the flat file silently.
- If Hindsight is down or `retain` returns `BLOCKED:`, do NOT save the fact somewhere else instead. Report BLOCKED with the reason to `<COS_NAME>` (and the Owner if it is blocking work) and retry once Hindsight is back. A failed retain is reported, never rerouted.
- Work files (evidence, exports, reports, drafts) on disk are fine. They are artifacts, not memory. A fact learned from them still gets retained to Hindsight.

## Proactive triggers
Run this skill without being asked when any of the following is true:
- Before starting any non-trivial task (recall context first).
- After any decision, outcome, failure, fix, or verified state change (retain immediately, one specific fact per retain, with `--context`).
- When any `retain` call returned `BLOCKED:` and has not been retried successfully (report BLOCKED and retry; never reroute to a flat file).
- When a mental model referenced in canon has drifted from Git (refresh from the named commit, or flag to `<COS_NAME>`).
- When a nightly reflection surfaces a new failure class (retain the lesson and add a permanent guard so it cannot recur silently).
- When a question to the Owner on a reversible item is skipped or unanswered (act on this skill's own recommendation, retain the decision, retain the lesson).
- When a follow-up deadline the bot set has arrived (check the result; if not done, escalate with the missing piece and a new deadline).
- When a sibling agent reports a fact that has not yet been retained (retain it; do not assume someone else will).

## Tool
Shared helper on the host, shipped in this repo at `tools/hindsight/hs.py` (standard library only). Set `HINDSIGHT_BANK=<MEMORY_BANK_ID>` in the environment; the helper refuses to run without it. The API key is loaded from a secrets-manager item referenced by a local env var; the key is masked, never printed, pasted, or stored in memory:

```bash
H=<WORKSPACE_PATH>/tools/hindsight/hs.py
python3 $H recall "question or topic" [--tags canon] [--max 2048]
python3 $H reflect "what should we do about X?" [--tags canon]
python3 $H retain "specific fact" --context "source and why it matters" [--tags lane:x] [--by "Bot name"]
python3 $H mm list            # living summaries the fleet reads first
python3 $H mm get commanders-intent
python3 $H kb tree | python3 $H kb search "query" | python3 $H kb page <id>
python3 $H op <operation_id>  # check an async retain finished
```

Any `BLOCKED:` line means the call failed. Report BLOCKED with the reason; never claim done, and never save the fact elsewhere instead.

## Recall first
Always recall (or read a mental model) before:
- starting any non-trivial task, or making a decision about approach, owner, or tooling
- answering "who owns / what's the status / what did `<OWNER_NAME>` decide" questions
- suggesting a tool, vendor, or process the fleet may already have chosen

`recall` returns raw facts (fast lookup: "what did we say about X?"). `reflect` reasons across memories with the bank's directives and mission ("what should I do about X?"). For bare ticket IDs, add descriptive words (the real subject, e.g. "`<BUSINESS_NAME>` subscriptions status").

SSH is not an ask path. If the only apparent way to reach memory looks like SSH, the path is wrong — use the REST API above.

## Mental models (read these first for policy)
- `commanders-intent`: the Owner's mission, risk tolerance, what only the Owner decides
- `fleet-operating-doctrine`: the five rules, the Bitter Pill, Minimal Change Operator, engineering edicts
- `plan-current-gates`: G0–G4 done sentences, rules, the Owner's ⛔ list, council riders (verbatim)
- `fleet-ssdlc-gates`: review, approval, CI, release rules
- `fleet-execution-state`: current gate, lane owners, blocked items (refreshes twice daily)

Policy models are built only from canon docs at a named commit. For exact wording that gates real action, confirm against the Git file — Git wins on mismatch.

## What to retain
Store immediately, one specific fact per retain, with `--context` saying where it came from:
- decisions and who made them ("the Owner decided that ...")
- procedure outcomes: what worked, what failed and why, workarounds
- verified live state changes (deployed SHA, ticket moved to Done), with the evidence
- lessons from failures and fixes

Attribute people by role / placeholder name (`<OWNER_NAME>`, a named lane Owner), not "the user". Label each claim [VERIFIED], [INFERRED], or [UNKNOWN] in the content. Do not upgrade a label by confident wording alone — VERIFY-THEN-TRUST.

## Never retain
- secrets, tokens, keys, passwords, or personal data of customers
- chatter, acknowledgements, or plans that were not executed
- policy you invented; doctrine changes land in Git first, then get uploaded as canon by `<COS_NAME>`

Do not delete, invalidate, or edit memories, change bank config, directives, or mental models unless `<COS_NAME>` or the Owner explicitly assigned that job. This skill grants no authority.

## Correcting a wrong fact
Retain the corrected fact with context naming what it supersedes. Only `<COS_NAME>` (or an assigned named Owner) uses invalidate / update on existing memories.

## Proactivity tail (every run ends here)
Ask and act: **what else is silently broken, what did I promise, what's due?**
- If a `retain` is BLOCKED → report to `<COS_NAME>` (and the Owner if blocking), retry, never reroute to a flat file; follow up at the retry deadline.
- If a recall surfaced a decision I have not acted on → act, or order the Owner to act with a deadline + required proof in this same turn; follow up at the deadline.
- If a mental model is stale vs Git → refresh it from the named commit, or flag to `<COS_NAME>`.
- If I just learned a lesson → retain it now with [VERIFIED] / [INFERRED] / [UNKNOWN] label and source.
- If the Owner skipped my question on a reversible item → act on my own recommendation, retain the decision, retain the lesson. Never act on my own for gated or irreversible work.
- If any failure class is new → write a permanent guard (cron check, test, or directive) so it cannot recur silently.

## Governance gates this skill honors
- VERIFY-THEN-TRUST: every retained claim is labeled [VERIFIED] / [INFERRED] / [UNKNOWN]; never trust a label just because the wording sounds confident.
- NO-SILENT-DEATH: a failed `retain` is reported and followed up at its deadline, not rerouted; a skipped Owner question on reversible work does not die quietly.
- Minimal Change Operator: do not invent a new memory store, new connector, or new file path — Hindsight REST only.
- Authority separation: only `<COS_NAME>` or an assigned named Owner mutates mental models, directives, or invalidates memories; workers only `retain` / `recall` / `reflect` within their lane lease.
- Ambiguity policy: if intent version, lane lease, or mental-model commit is unclear, BLOCKED with one deciding question — do not guess.


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
