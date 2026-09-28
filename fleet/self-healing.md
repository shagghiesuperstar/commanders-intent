# Fleet Self-Healing & Self-Improvement (Hermes-style)

Scope: the on-host agent layer that keeps the fleet honest between human attention. Applies to every host that runs a Hermes Agent (`<HOST_1>`, `<HOST_2>`, `<HOST_3>`, `<HOST_4>`, `<CONTROL_HOST>`, `<WORKHORSE_HOST>`, `<CODE_MAP_HOST>`). All routines are proactive — the bot is the sole instigator; no one will prompt it.

**Proactivity (hard, restated).** Every routine below ends with the question "what else is silently broken, what did I promise, what's due?" and acts on it in the same turn: fix it yourself, or order the fix with a deadline and required proof. Follow up at every deadline. Every failure becomes a permanent guard so it cannot recur silently.

---

## Part 1 — Self-Healing (10-minute cron)

### 1.1 Schedule

OS-level cron entry on every agent host [INFERRED — exact Hermes scheduler CLI must be verified against official docs: https://hermes-agent.nousresearch.com/docs/]:

```
*/10 * * * * <HANDLER>
```

`<HANDLER>` invokes the local Hermes scheduler to run the prompt in §1.6 against this host. Acceptable shapes [INFERRED, both must be checked against current Hermes docs]:

- Direct Hermes scheduler subcommand, e.g. `hermes cron run --name fleet-self-heal --prompt-file <WORKSPACE_PATH>/prompts/self-heal.md` [UNKNOWN exact flags].
- Shell wrapper that POSTs to `http://127.0.0.1:8642/v1/runs` with body `{"input": "<prompt body>"}` and polls `GET /v1/runs/{run_id}`, bearer token from local env (never echoed).

Lock down which one is correct in the first 24h of operation and record the verified invocation in `<GOVERNANCE_REPO>` under `fleet/hermes-invocation.md`. Until verified, prefer the curl path because it matches the documented `/v1/runs` behavior in the source brief.

### 1.2 Checks (every host, every 10 minutes)

Each check produces one entry in `checks[]` with `status ∈ {pass, fail, warn}`, an `observed` string (command + output excerpt), and a `duration_ms`.

| # | Check | How | Pass condition |
|---|-------|-----|----------------|
| 1 | Hermes API loopback | `curl -fsS --max-time 5 http://127.0.0.1:8642/health` | HTTP 200 with expected schema |
| 2 | Private-net reachability (Tailscale `<PRIVATE_NET_NAME>`) | `tailscale status` plus one HEAD to each of `<CONTROL_HOST>`, `<CODE_MAP_HOST>`, plus one peer round-trip per zone | Tailscale state `running`; at least one peer returns 2xx/3xx in <1s |
| 3 | Disk | `df -P <WORKSPACE_PATH> /var/log /tmp` | <85% used on every checked mount |
| 4 | Memory bank reachability | Masked-key GET against `<MEMORY_BANK_ID>` health endpoint over private net, timeout 5s | 2xx within retry budget (1 retry) |
| 5 | Required crons present | `crontab -l` parsed for the 10-min self-heal and `30 2 * * *` nightly reflection entries | both entries present and enabled |
| 6 | SOUL.md hash vs expected | `sha256sum` of `<WORKSPACE_PATH>/SOUL.md` matches value stored in `<GOVERNANCE_REPO>` `fleet/expected-hashes.json` for this host | exact match |
| 7 | Token isolation | Enumerate bot/API tokens present in local env/secrets; cross-check each against `<GOVERNANCE_REPO>` `fleet/token-assignments.json` (token → exactly one host) | every local token assigned to this host; no foreign tokens present |
| 8 | Last-run timestamp | Read `checked_at` from previous `<WORKSPACE_PATH>/fleet-status.json` | previous run within the last 30 minutes (i.e., the cron itself is alive) |

### 1.3 Auto-fix table

Rule of thumb: only reverse, additive, local fixes. Anything that mutates policy, secrets, credentials, or remote state goes to COS, not the cron. "Fixed 3+ times in 24h" on the same check is a structural problem, not a fix loop — see §1.5.

| Failure | Safe auto-fix | When NOT to auto-fix |
|---------|---------------|----------------------|
| Hermes API loopback down | If local Hermes process is missing/dead, restart the local service via the host's standard unit (`systemctl --user restart hermes` or equivalent [UNKNOWN exact unit name — verify]). If process is up but unhealthy, no fix, escalate. | Process restart fails twice in a row; port conflict from another listener; service unit missing entirely (config drift). |
| Private-net reachability (partial peer loss) | If `tailscaled` is down and the host's `tailscale` state is `Stopped`, bring it up via `tailscale up` (uses existing auth key in local env). | Auth key expired or missing; Tailscale admin ACL change required; multiple peers down simultaneously (likely tailnet-wide). |
| Disk ≥85% on `/var/log` or `/tmp` | Rotate logs older than 7 days via the host's standard logrotate; delete files in `/tmp` older than 24h and owned by the agent user. Skip `/tmp` files the agent doesn't own. | Disk pressure on `<WORKSPACE_PATH>` (where data lives); inodes near full despite % free; disk growth tied to a running job (let the job finish or kill it explicitly via COS). |
| Memory bank reachability timeout | One retry with 2s backoff; record the transient in `fixed[]`. | Both attempts fail; auth error (masked key rejected) — escalate immediately. |
| Required cron missing | If the 10-min self-heal entry is missing, restore it from `<GOVERNANCE_REPO>` `fleet/crontab-snapshots/<host>.cron`. | The nightly reflection entry is missing (different intent — escalate, do not silently reinstall, because missing reflection is a behavioral drift signal). |
| Last-run gap >30 min | None. | Always. A gap means the cron is broken or the host is overloaded — escalate; do not silently re-mark as healthy. |
| SOUL.md hash mismatch | **Never.** | Always. This is a tamper signal. |
| Token isolation violation | **Never.** | Always. A foreign token on this host is a credential leak; escalate and treat as incident. |

Every fix writes one entry to `fixed[]` with `name`, `fix` (one-line description), and `ts`. Every unfixed failure writes one entry to `failing[]` with `name`, `detail`, `first_seen`, and `auto_fixed: false`.

### 1.4 Status file schema

Path: `<WORKSPACE_PATH>/fleet-status.json`. One file per host. Written by that host's self-heal run only — single-writer per file. Schema:

```json
{
  "host": "<HOST_1>",
  "checked_at": "2026-01-15T12:30:00Z",
  "guard_version": "1.0.0",
  "checks": [
    {
      "name": "hermes_api_loopback",
      "status": "pass",
      "observed": "HTTP 200 in 45ms",
      "duration_ms": 45
    },
    {
      "name": "disk",
      "status": "warn",
      "observed": "/var/log 88% used (threshold 85%)",
      "duration_ms": 12
    }
  ],
  "fixed": [
    {
      "name": "disk",
      "fix": "rotated /var/log journal files older than 7d",
      "ts": "2026-01-15T12:30:00Z"
    }
  ],
  "failing": [
    {
      "name": "memory_bank_reachability",
      "detail": "timeout after 5s; retry also failed",
      "first_seen": "2026-01-15T12:20:00Z",
      "auto_fixed": false
    }
  ],
  "alerts_sent": 1
}
```

Field rules: `checked_at` is ISO-8601 UTC. `guard_version` is the version of this self-heal definition (bumped whenever a new check is added — see Part 2). `checks` is the truth of the last sweep; `fixed` and `failing` are the deltas. The file must never contain secrets (see §4.2). Keep under 64 KB; if it grows, archive previous runs to `<WORKSPACE_PATH>/fleet-status.archive/<date>.json`.

### 1.5 Alerts

Send to `<ALERT_CHANNEL>` when **any** of:

- `failing[]` is non-empty after a sweep.
- Same `name` appears in `fixed[]` 3 or more times in the trailing 24h (counts read from `<WORKSPACE_PATH>/fleet-status.archive/` plus the live file) — this is a recurring-incident signal, not a fix loop.
- Any check is `UNKNOWN` because the cron could not gather evidence (better to admit blind than to claim pass).
- Status file is older than 30 minutes (the cron itself is dead or wedged).

Alert payload is short: host, failing names, first_seen, last fix attempt, what the next human-or-COS action should be. Never include token material, even partial. Never include raw command output longer than 200 chars.

### 1.6 Example self-heal prompt (fenced)

```text
You are the on-host self-healing agent for host {HOST} on tailnet {PRIVATE_NET_NAME}.
Local time: {LOCAL_TS_ISO}. Previous status: {PREV_STATUS_PATH}.

Run these checks in order, with these exact methods, and record each as one
checks[] entry with status pass|warn|fail, observed (one line), duration_ms.

1. hermes_api_loopback:
   curl -fsS --max-time 5 http://127.0.0.1:8642/health
   pass = HTTP 200 with JSON body containing {"status":"ok"}.
2. private_net_reachability:
   tailscale status (capture state); then
   for peer in {CONTROL_HOST}, {CODE_MAP_HOST}, and one peer per zone:
     curl -fsSI --max-time 3 https://$peer:8642/health
   pass = tailscale state=running AND at least one peer returns 2xx/3xx.
3. disk:
   df -P {WORKSPACE_PATH} /var/log /tmp
   warn = any mount >=85%; fail = any mount >=95%.
4. memory_bank_reachability:
   GET {MEMORY_BANK_HEALTH_URL} with bearer from env {MEMORY_API_KEY_SECRET},
   timeout 5s. Retry once on timeout. pass = 2xx within retry budget.
5. required_crons_present:
   crontab -l | grep -E '\*/10 \* \* \* \*.*self-heal|30 2 \* \* \*.*reflect'
   pass = both patterns present.
6. soul_hash:
   sha256sum {WORKSPACE_PATH}/SOUL.md must equal the value at
   {GOVERNANCE_REPO_RAW_URL}/fleet/expected-hashes.json#{HOST}.
   Any mismatch is fail — DO NOT auto-fix.
7. token_isolation:
   For every token name present locally (env vars whose name contains TOKEN or
   SECRET, plus secrets pulled via the local secrets manager CLI for this
   host), each must appear in {GOVERNANCE_REPO_RAW_URL}/fleet/token-assignments.json
   with host == {HOST}. Any foreign token is fail — DO NOT auto-fix.
8. last_run_gap:
   Read checked_at from {PREV_STATUS_PATH}; if absent, fail.
   fail = now - checked_at > 30 min.

Apply the auto-fix table from fleet/self-healing.md verbatim. For every fix
applied, append to fixed[] with name, fix (one line), ts. For every
unfixed failure, append to failing[] with name, detail, first_seen,
auto_fixed=false.

Decision rule for alerting: if failing[] is non-empty, OR if any name
appears in fixed[] 3+ times in the trailing 24h, OR if status file is
older than 30 min, OR if any check could not be run, send one alert to
{ALERT_CHANNEL} via the host's messaging token (only this host's token).
Alert body: host, failing names, first_seen, last_fix, next action.
Never include token values, even partial.

Write the assembled JSON to {WORKSPACE_PATH}/fleet-status.json, atomically
(write to .tmp then rename). Set guard_version from
{GOVERNANCE_REPO_RAW_URL}/fleet/guard-version.json.

End by answering, in plain language:
- what else is silently broken on this host right now?
- what did the previous status file say was failing or fixed 3+ times?
- what's due in the next 24h that this host owns?
Then act on each: fix locally if safe per the table, or open a COS ask
with deadline and required proof.
```

### 1.7 Verification gate (one-time, blocking)

Until the exact Hermes scheduler invocation is confirmed against https://hermes-agent.nousresearch.com/docs/, the 10-min entry must be wrapped by a shell script that:

1. Captures stderr to `<WORKSPACE_PATH>/logs/self-heal.err.log` (rotated weekly).
2. Exits non-zero on any unhandled exception (cron will then skip the next run, which itself triggers the last_run_gap alert — desirable, fail-loud).
3. Records the invocation it tried in `<WORKSPACE_PATH>/logs/self-heal.invocation.log` so the exact syntax drift is auditable.

---

## Part 2 — Self-Improvement (nightly reflection)

### 2.1 Schedule

```
30 2 * * * <HANDLER_NIGHTLY>
```

Local time per host. `<HANDLER_NIGHTLY>` invokes Hermes with the prompt in §2.4. Same [UNKNOWN] flag situation as §1.1 — same curl-to-`/v1/runs` fallback applies.

### 2.2 What it reviews

Inputs (read-only):

- Today's `<WORKSPACE_PATH>/fleet-status.json` plus every archived hourly snapshot.
- Today's entries in `<ALERT_CHANNEL>` search.
- The day's COS reports to `<OWNER_NAME>` (read from memory bank `<MEMORY_BANK_ID>`, filtered by `lane=self_healing`).
- Any manual fixes `<LEAD_OPERATOR_NAME>` or `<COS_NAME>` made on this host today (memory bank, filtered by `host={HOST}, kind=manual_fix`).

Failure classes the reflection must enumerate:

1. Any check that failed today.
2. Any check that auto-fixed but recurred within 24h (3+ fix loop).
3. Any manual fix the human team applied that the cron *could* have done (and why the cron missed it).
4. Any near-miss: a check was passing but adjacent evidence suggested it was about to fail (e.g., disk at 84% climbing 1%/h).
5. Any silent gap: last_run_gap triggered, or a check returned UNKNOWN.

### 2.3 What it produces

For every **new** failure class (one not already covered by an existing check in §1.2), it:

1. Drafts the smallest new check (method, pass/fail thresholds, duration budget).
2. Adds the check to the running self-heal prompt body in `<WORKSPACE_PATH>/prompts/self-heal.md`, version-controlled under `<GOVERNANCE_REPO>` `fleet/prompts/self-heal.md` (single-writer for prompt changes — see §4.3).
3. Bumps `fleet/guard-version.json` by minor version.
4. Records a one-line guard entry in memory bank `<MEMORY_BANK_ID>` under `lane=self_healing, kind=guard_added, host={HOST}, guard=<name>, reason=<short>`.
5. Reports to `<ALERT_CHANNEL>`: "Added N guards on {HOST}: [names]. Bumped guard_version to X.Y."

If no new failure class is found, it reports "No new guards. Reviewed M classes. X were already guarded." — and still ends with the proactive sweep (§2.5).

### 2.4 Example nightly reflection prompt (fenced)

```text
You are the nightly reflection agent for host {HOST}. Local time {LOCAL_TS_ISO}.

Read in order:
1. {WORKSPACE_PATH}/fleet-status.json and all archived snapshots from today.
2. Today's messages in {ALERT_CHANNEL} mentioning {HOST}.
3. Memory bank {MEMORY_BANK_ID}, filter: lane=self_healing, host={HOST}, ts>=today_start.
4. The current self-heal prompt at {GOVERNANCE_REPO_RAW_URL}/fleet/prompts/self-heal.md.
5. The current check manifest at {GOVERNANCE_REPO_RAW_URL}/fleet/guard-version.json.

Enumerate today's failure classes (failed checks, 3+ fix loops, manual
fixes the cron could have done, near-misses, silent gaps).

For each NEW class not already covered by an existing check:
  a. Draft the smallest possible check (method + thresholds + duration budget).
  b. Append it to the self-heal prompt body via PR to
     {GOVERNANCE_REPO} path fleet/prompts/self-heal.md (do NOT push to main
     yourself — open the PR; the single-writer policy agent reviews/merges).
  c. Bump guard-version.json minor.
  d. Write one memory entry to {MEMORY_BANK_ID}: kind=guard_added,
     host={HOST}, guard=<name>, reason=<one sentence>.

Then answer in plain language and act:
- what new guards were added tonight, and what each prevents?
- what failure class recurred today that we still have no check for, and
  what's blocking the check (data source? permissions? docs gap?)?
- what's due in the next 24h on this host?
- what else is silently broken?

Send the report to {ALERT_CHANNEL}. Do not include token material.
```

### 2.5 Mandatory proactive close

Every reflection run ends by asking the four questions and acting on each in the same turn: either fix locally within the host's lane, or open a COS ask with deadline and proof. Reflection is not allowed to end on "looks fine."

---

## Part 3 — COS 30-minute sweep (how status files are consumed)

`<COS_NAME>` runs a 30-minute sweep routine [INFERRED cadence — confirm against current fleet load]. Each sweep:

1. **Collect.** Pull `<WORKSPACE_PATH>/fleet-status.json` from every host on `<PRIVATE_NET_NAME>` (over the tailnet, not public). One HTTP GET per host, 5s timeout. Missing or stale (>45 min) file is itself a failure to record.

2. **Normalize.** Merge into a fleet-wide view keyed by host × check. Track `failing[]` roll-up and the trailing-24h fix count per check name per host.

3. **Triage.** For each failing check across the fleet:

   | Pattern | Action |
   |---------|--------|
   | Single host, single check, auto-fixable per §1.3 but cron couldn't | Re-dispatch to that host's self-heal; queue follow-up at next 30-min sweep. |
   | Single host, single check, NOT auto-fixable (SOUL hash, token isolation, last_run_gap) | Open incident; page `<LEAD_OPERATOR_NAME>` if configured, else alert `<ALERT_CHANNEL>` and prepare an Owner decision ask using the six-element rule. |
   | Same name failing on ≥2 hosts | Likely tailnet or shared dep (memory bank, Tailscale, secrets). Dispatch `<FLEET_OPS_AGENT>` to investigate, not per-host self-heal. |
   | 3+ fixes in 24h on same name | Treat as structural; open a remediation issue, do **not** keep re-fixing. |
   | Status file missing entirely on a host | Host is dark or isolated. Re-check via Tailscale ping; if dark >15 min, escalate — silent host is worse than loud host. |

4. **Decide.** Of all failing items, decide which require `<OWNER_NAME>` attention today using the six-element decision rule: (1) context in plain language, (2) the decision, (3) the options, (4) recommendation, (5) rationale, (6) confidence. If any element is missing, do not send.

5. **Persist.** Write one memory entry per sweep to `<MEMORY_BANK_ID>` with `lane=self_healing, kind=sweep, summary=<counts>, hosts=<n>, failing=<n>, recurring_24h=<n>`. Memory is a mental model; the canonical state lives in `<GOVERNANCE_REPO>`.

6. **Report up.** Owner only sees aggregates and anything requiring a decision, not every host blip. Lead operator (if present) sees per-host detail for hosts in their lane.

7. **Mandatory proactive close.** Every sweep ends by answering "what else is silently broken in the fleet, what did I promise, what's due?" and acting: order the fix with deadline + proof, or fix it in COS's own lane.

---

## Part 4 — Guardrails

### 4.1 No destructive fixes

The self-heal cron must not, under any circumstance:

- `rm -rf` on any path not explicitly listed in §1.3's safe-fix set.
- Drop, truncate, or delete data files under `<WORKSPACE_PATH>` outside the log/tmp carve-outs.
- Restart non-local services or any service on another host.
- Rotate, regenerate, or revoke credentials, tokens, or keys. A leaked token gets rotated by humans, not by cron, and the rotation follows the secrets-manager runbook (project `<SECRETS_PROJECT>`), not an inline script.
- Run package installs, kernel changes, or anything that touches the OS image.
- Skip writing `failing[]` to make a status look clean. If evidence is missing, the check is UNKNOWN and must be reported, not omitted.

When in doubt: write to `failing[]` and let COS dispatch. Silence is the enemy.

### 4.2 No secrets in status files

`<WORKSPACE_PATH>/fleet-status.json` and every archive under `<WORKSPACE_PATH>/fleet-status.archive/` must never contain:

- Token values (bot tokens, API keys, signing keys) — even partial, even base64, even truncated.
- Secrets-manager item names mapped to their values (names alone are fine; values are not).
- Headers or bodies from authenticated requests.
- Memory-bank entries that themselves contain secrets.

Reason: status files are routinely shipped to `<ALERT_CHANNEL>`, attached to PRs, and persisted in archives. The blast radius of a leaked token includes the partner-facing channels. Mask at source: only reference tokens by name (e.g., `<MEMORY_API_KEY_SECRET>`), never by value. If a fix attempt accidentally logs a token, that token is now considered exposed and the incident playbook runs — see §4.4.

### 4.3 Single-writer for policy

| Asset | Writer | Readers |
|-------|--------|---------|
| `fleet/prompts/self-heal.md` | `<COS_NAME>` (the single control-plane writer) | All hosts, nightly reflection runs |
| `fleet/guard-version.json` | `<COS_NAME>` | All hosts, COS sweep |
| `fleet/expected-hashes.json` | `<COS_NAME>`, requires `<OWNER_NAME>` sign-off on any change | Self-heal check #6 on every host |
| `fleet/token-assignments.json` | `<SECURITY_REVIEWER>` via PR; merge requires `<OWNER_NAME>` | Self-heal check #7 on every host; COS sweep |
| `<WORKSPACE_PATH>/fleet-status.json` (per host) | That host's self-heal cron only | COS sweep, archived snapshots |
| `<GOVERNANCE_REPO>` main branch | `<COS_NAME>` for fleet/* ; `<LEAD_OPERATOR_NAME>` for app/* ; merge requires separate reviewer (no self-approve) | All |

The worker that writes the self-heal prompt body is **not** the worker that runs it. The self-heal cron is read-only against its own prompt definition. If a nightly reflection wants to change the prompt, it opens a PR; `<COS_NAME>` reviews and merges. This separation is what lets the judge/reviewer role be independent.

### 4.4 Incident posture

When check #6 (SOUL hash) or check #7 (token isolation) fails on any host:

1. Self-heal writes `failing[]` and alerts; does **not** attempt any fix.
2. COS sweep treats the host as compromised-pending and isolates it on the tailnet (revoke the host's ACL node via Tailscale admin API — `OWNER` authority, COS proposes with exact change in the decision ask).
3. `<SECURITY_REVIEWER>` reviews SOUL drift and token assignment state.
4. The host is not returned to service until SOUL hash matches and token set matches `fleet/token-assignments.json` exactly, verified by a separate host's sweep.

### 4.5 Audit trail

Every self-heal run writes to `<WORKSPACE_PATH>/logs/self-heal.log` (rotated weekly): timestamp, guard_version, which checks ran, which fixed/failing. Every nightly reflection writes to `<WORKSPACE_PATH>/logs/reflect.log`. These logs are read-only after write; append-only by convention. COS sweep consumes both. Owner can request a full audit export at any time; export goes via the secure file-share lane, never via `<ALERT_CHANNEL>`.

---

## Closing — Proactivity is the job

If the 10-min cron runs and everything is green, that is **not** a clean exit. It is a prompt to ask again: what else is silently broken on this host, what did the previous reflection promise to guard, what's due in the next window, what neighbor hosts are showing odd patterns? Fix what is safe per §1.3, open COS asks with deadline + proof for the rest, and record every new failure class as a guard so the next sweep is louder than this one.

The fleet does not get healthier by waiting. It gets healthier because the cron, the nightly reflection, and the COS sweep each refuse to finish without acting.

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
