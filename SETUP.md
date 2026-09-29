# SETUP.md — Commander's Intent

> The installed bot runs `FIRST-RUN.md` for you. This file is the full manual reference behind it.

> **Start with the intent.** Before any placeholder below, the Chief of Staff interviews the Owner to fill [`COMMANDERS-INTENT.md`](COMMANDERS-INTENT.md) (script: [`interview/commanders-intent-interview.md`](interview/commanders-intent-interview.md)). Intent slots (upper-case names in double curly braces) come only from the Owner's answers; install placeholders (upper-case names in angle brackets) come from the table below. Security gates are in [`SECURITY.md`](SECURITY.md).

This file walks an installer from a blank template to a working fleet. Run it once, in order. Every placeholder in the table below must be resolved before step 11 (read-back).

---

## Part 1 — Setup prompts

The installer answers each row before any code or config ships. "Example format" shows a plausible shape, not a real value.

| Placeholder | What to ask the installer | Example format (fake/generic) | Where used |
|---|---|---|---|
| `<OWNER_NAME>` | Legal human commander / principal who approves intent and gated actions. One name, never an alias. | `Jane Doe` | SOUL.md, governance/skill files, all Owner-bound prompts |
| `<LEAD_OPERATOR_NAME>` | Optional second-in-command. Leave blank if none. | `Sam Roe` | SOUL.md, chain-of-command references |
| `<COS_NAME>` | Bot persona name for the Chief of Staff. Used in alerts and signatures. | `Aria` | SOUL.md, routines, alert channel naming |
| `<BUSINESS_NAME>` | Public-facing venture name. | `Acme Labs` | README, Commander's Intent Mission section, customer-facing copy |
| `<PRIMARY_DOMAIN>` | The one domain that defines the business. Used for DNS / branding decisions only by the Owner. | `example.org` | Commander's Intent, identity references (not for resolving in code) |
| `<TIMEZONE>` | IANA timezone the Owner lives in. Cron values in routines are evaluated in this zone unless noted UTC. | `America/Los_Angeles` | All cron schedules, "today" / "tonight" references |
| `<UTC>` | UTC offset string for the same zone. Used in logs and renewal timestamps. | `UTC-08:00` | Renewal timestamps, log timestamps, audit rows |
| `<DATE>` | The single target date "winning looks like by ___". One date, hard. | `2026-12-31` | Commander's Intent "What winning looks like by" |
| `<NOW>` | Current ISO-8601 timestamp at install time. Filled once, used as the canary epoch. | `2026-01-15T14:30:00Z` | Install canary, governance audit anchor |
| `<PRIVATE_NET_NAME>` | Tailscale tailnet name. Hosts are reachable only inside this net. | `<PRIVATE_NET_HOSTNAME>` | All host reachability checks, connector URLs |
| `<PRIVATE_NET>` | Private network reference (CIDR or generic). | `<PRIVATE_NET_IP>/10` | Network policy / firewall rules |
| `<PRIVATE_NET_HOSTNAME>` | MagicDNS hostname for a canonical host. | `<PRIVATE_NET_HOSTNAME>` | Connector URLs, health probes |
| `<HOST>` | Placeholder for "this host" in per-host scripts. Replaced per host by the installer loop. | `host-X` | Per-host install scripts, skill envelopes |
| `<HOST_1>` | First fleet host (usually control plane). | `control-1` | SOUL.md wiring, control-plane-only routines |
| `<HOST_2>` | Second fleet host (usually workhorse). | `workhorse-1` | SOUL.md wiring, repo-bearing routines |
| `<HOST_3>` | Third fleet host. | `host-three` | SOUL.md wiring |
| `<HOST_4>` | Fourth fleet host. | `host-four` | SOUL.md wiring |
| `<HOST_N>` | Generic Nth host for fleets beyond four. | `host-N` | Scalable install loops |
| `<CONTROL_HOST>` | The single control-plane host that mutates policy/models. | `control-1` | Single-writer governance references, judge assignment |
| `<WORKHORSE_HOST>` | Host with local repos and desktop, used for coding work. | `workhorse-1` | Code-map references, repo-bound routines |
| `<CODE_MAP_HOST>` | Host running the code-map index service. | `code-map-1` | "Code questions go to the code map first" doctrine |
| `<USER_HOME>` | Filesystem user-home path on each host. | `/home/operator` | Skill install paths, cron user context |
| `<WORKSPACE_PATH>` | Workspace path for fleet status and run artifacts. | `/home/operator/fleet` | `fleet-status.json`, run logs, status files |
| `<MEMORY_BANK_ID>` | The single cloud memory bank ID shared by all agents. | `mb_xxxxxxxxxxxxxxxx` | All memory read/write calls, recall verification |
| `<MEMORY_API_KEY_SECRET>` | Secret name in the secrets manager that holds the memory bank API key. Never paste in chat. | `memory-bank-api-key` | Secrets-manager fetch calls on every host |
| `<HERMES_API_KEY_SECRET>` | Secret name holding the Hermes HTTP API bearer key (per host, rotated). | `hermes-api-key-<HOST>` | `Authorization: Bearer ...` header on /v1/runs and /v1/runs |
| `<API_SERVER_KEY>` | Same as `<HERMES_API_KEY_SECRET>` when not split per host; otherwise leave empty and rely on the secret only. | `—` | Connector config; always prefer the secret over a literal |
| `<SECRETS_PROJECT>` | Secrets-manager project identifier. | `proj-xxxxxxxx` | All secret fetch calls |
| `<SECRET_ITEM_NAME>` | Generic placeholder for any secret item the installer must reference. | `some-secret` | Skill envelopes that read arbitrary secrets |
| `<GOVERNANCE_REPO>` | Org/repo that holds Commander's Intent and doctrine. Git wins on mismatch. | `acme/governance` | Intent-version gate, preflight reads |
| `<INTENT_COMMIT_SHA>` | Commit SHA of the canonical Commander's Intent. Pin it; upgrade intentionally. | `a1b2c3d4e5f6...` | Preflight version gate, canary |
| `<AGENT_NAME>` | Generic agent identifier used in skill envelopes. | `agent-x` | Skill templates, run metadata |
| `<ROLE_NAME>` | Generic role label (Owner / Lead Operator / COS / named Owner). | `Owner` | Authorization tables, gate enforcement |
| `<CLOUD_CODING_AGENT>` | Vendor name for the cloud coding agent used via PRs. Public vendor names are fine. | `VendorX Coder` | Coding-lane delegation, PR creation |
| `<TOP_MODEL>` | Top-tier inference model name, used where quality shows. | `top-model-v3` | Design, security, doctrine calls |
| `<VENDOR>` | Generic vendor placeholder when a skill talks to any external service. | `VendorY` | Skill templates that take a vendor name |
| `<FLEET_OPS_AGENT>` | Identifier of the fleet-ops / self-healing agent that owns cron health checks. | `fleet-ops` | fleet/self-healing.md cron target |
| `<SECURITY_REVIEWER>` | Identifier of the adversarial security reviewer (separate from the author). | `sec-reviewer` | "No code ships without adversarial security review" gate |
| `<ISSUE_TRACKER>` | Issue tracker identifier (project / repo) for blockers and follow-ups. | `acme/issues` | Order-followup runner, blocker logging |
| `<ALERT_CHANNEL>` | Where the bot posts alerts that could not be auto-fixed. | `ops-alerts` (channel) | fleet/self-healing.md, escalation paths |
| `<SPEND_LIMIT>` | Hard spending cap per period; below this the COS may act, above this the Owner must approve. | `USD 500 / month` | Spending gate, "who decides" table |
| `<NAMED_SPENDERS>` | The only identities (by role) allowed to spend inside `<SPEND_LIMIT>`. Everyone else reads spend and never writes it. | `COS only` | Spend gate, cloud coding agent paid runs (`SECURITY.md` section 9) |
| `<MERGE_OWNER>` | The one identity allowed to merge reviewed pull requests. Never the author, never the Chief of Staff. | `merge-owner` | Merge gate, CODEOWNERS, `SECURITY.md` section 9 |
| `<OWNER_GITHUB_HANDLE>` | GitHub handle used in CODEOWNERS for doctrine files. | `@example-owner` | `.github/CODEOWNERS` example in `SECURITY.md` |
| `<HANDLER>` | Identifier of the long-running Hermes run handler (async jobs that escape the 120s connector timeout). | `run-handler` | `POST /v1/runs`, poll `GET /v1/runs/{run_id}` |
| `<HANDLER_NIGHTLY>` | Identifier of the nightly reflection handler that writes new guards from the day's failures. | `nightly-reflection` | Nightly cron, self-improvement loop |
| `<ORDER_FOLLOWUP_RUNNER>` | Identifier of the agent/runner that pings the Owner at every order deadline and pings again if missed. | `order-followup` | Proactivity loop, "push and pester until asks are closed" |
| `<PROFILE>` | Generic profile placeholder (e.g. for routine scopes). | `default` | Routine metadata, cron scoping |
| `<PROFILE_A>` | Profile A: routine scope for the control-plane host. | `control-plane` | Routine metadata |
| `<PROFILE_B>` | Profile B: routine scope for the workhorse host. | `workhorse` | Routine metadata |
| `<PROFILE_C>` | Profile C: routine scope for the code-map host. | `code-map` | Routine metadata |
| `<PR_REF>` | Pull-request reference for the current code change under review. | `https://github.com/<GITHUB_ORG>/<REPO>/pull/<N>` | Security review, judge verification |
| `<ONE_LINE_PURPOSE>` | One-sentence purpose the Owner can read aloud. Used in SOUL.md header and on every status report. | `Ship a working fleet in one afternoon.` | SOUL.md, status report header |
| `<UTC_RENEWAL_TIMESTAMP>` | Exact UTC timestamp at which a token, cert, or secret must be renewed. | `2026-04-15T00:00:00Z` | Renewal cron, alert at T-7d |

---

## Part 2 — Install steps

Do these in order. Do not skip. The bot's first act after install is step 10 (audit + canaries); the installer's first act is step 1.

### 1. Import the template
- Create a new Grok Bot from the Commander's Intent template (link in `README.md`).
- Do not rename the bot until step 11 confirms the placeholder sweep is clean.

### 2. Answer setup prompts / find-replace placeholders
- Fill every row of Part 1. No `<…>` tokens left in the shipped files.
- Run a repo-wide grep for `<[A-Z_0-9]+>`; every hit must map to a resolved row above.
- Pin `<INTENT_COMMIT_SHA>` and `<NOW>`; the version gate treats a drift as stale intent and BLOCKS.

### 3. Connect the memory bank
- Store the memory bank API key as a MASKED secret in the secrets manager under `<MEMORY_API_KEY_SECRET>` inside `<SECRETS_PROJECT>`. Never paste the key in chat, in SOUL.md, in a skill file, or in a log.
- Set `<MEMORY_BANK_ID>` in the memory client config.
- Verify with a recall: write a known fact ("install completed at <NOW>"), then read it back. The recall must return the fact unaltered. If it does not, BLOCKED — do not proceed.

### 4. Join every host to the Tailscale private network
- For each of `<HOST_1>` … `<HOST_N>`: install Tailscale, authenticate to `<PRIVATE_NET_NAME>`, confirm `tailscale status` shows the host.
- Confirm every host can reach every other host by MagicDNS name (`<PRIVATE_NET_HOSTNAME>`-style). [VERIFIED for Tailscale MagicDNS behavior.]
- Confirm Funnel is OFF on every host (`tailscale serve --no-funnel` or equivalent). No public exposure of any agent port.
- Confirm SSH relay is OFF for agent traffic. Agents talk only over the Hermes HTTP API.

### 5. Enable Hermes Agent API server on each host
- Bind Hermes HTTP API to loopback only: `127.0.0.1:8642`. Do not bind to `0.0.0.0`. [INFERRED — default bind per Hermes docs; verify on install.]
- Generate or rotate the API key and save it under `<HERMES_API_KEY_SECRET>` in `<SECRETS_PROJECT>`, one secret per host. The key must never appear in any file on disk.
- Expose the loopback port to the tailnet via `tailscale serve` on port 8642 over HTTPS, scoped to the tailnet only. [INFERRED — Tailscale serve behavior; verify on install.]
- Wire per-host connectors: `health` connector and `ask` connector pointing at the host's HTTPS-served `:8642` over `<PRIVATE_NET_NAME>`. Auth = `Authorization: Bearer <fetched secret>`.
- Verify each host: `GET /health` returns `{ok: true, mode: "http"}` (or equivalent). [INFERRED — shape of Hermes health response; verify on install.]
- Verify the long-job escape hatch: `POST /v1/runs` with a small input returns a `run_id`; `GET /v1/runs/{run_id}` reaches a terminal state. Connector-timeout jobs use this path, never the synchronous ask. [INFERRED — Hermes `/v1/runs` shape; verify on install.]

### 6. Deploy SOUL.md per host
- Copy `persona/SOUL.md` and the matching `skills/soul-md-template` to each host's workspace at `<WORKSPACE_PATH>`.
- Fill per-host fields: `<HOST>`, `<USER_HOME>`, `<PROFILE>` (or `<PROFILE_A>` / `<PROFILE_B>` / `<PROFILE_C>`).
- Confirm SOUL.md on every host contains: chain of command, the six decision-rule items, the truth rule, the no-silent-death rule, the verify-then-trust rule, the bitter pill, the one thing never to risk, the proactivity requirement, and the end-of-routine "what else is silently broken" loop.

### 7. Install skills
- Drop every file under `skills/` into each host's skill loader path.
- Confirm the minimal-change-operator skill is present on every host (it is mandatory fleet-wide).
- Confirm the proactivity clause is present in every skill, not just SOUL.md.

### 8. Create the routines manually
Templates cannot auto-create routines in Grok Bot [INFERRED]. Two layers:

- **Grok Bot routines (four):** proactivity sweep, compliance audit, order follow-up, update-survival restore. Copy-paste prompts and cron values are in `FIRST-RUN.md` step 7 and `routines/`.
- **Hermes host crons:** created on each Hermes host from `fleet/self-healing.md`, summarized here:

- **Order follow-up** — runner: `<ORDER_FOLLOWUP_RUNNER>` — cron: every 30 minutes during business hours in `<TIMEZONE>` (`*/30 8-18 * * 1-5`). Acts on the owner's outstanding orders at the deadline; pings once at deadline, pings again at +4h if unanswered, escalates to `<ALERT_CHANNEL>` at +24h.
- **Fleet health + auto-fix (10-minute loop)** — runner: `<FLEET_OPS_AGENT>` — cron: `*/10 * * * *` (UTC). Health checks per host, auto-fix known failures, write `<WORKSPACE_PATH>/fleet-status.json`, alert `<ALERT_CHANNEL>` on anything not auto-fixed.
- **Nightly reflection** — runner: `<HANDLER_NIGHTLY>` — cron: `0 2 * * *` in `<TIMEZONE>`. Reviews the day's failures and near-misses, adds one new guard (check, cron, test, or directive) per new failure class, commits to `<GOVERNANCE_REPO>` with PR. [INFERRED — 02:00 local is a defensible default; adjust to Owner preference.]

For long-running tasks (anything that may exceed ~120s connector timeout), use the async path: `POST http://127.0.0.1:8642/v1/runs` on the originating host, then poll `GET /v1/runs/{run_id}`. Never block a connector on a long job. [INFERRED — connector timeout window per Hermes; verify on install.]

### 9. Install fleet/self-healing.md crons per host
- For each host, install the cron entries defined in `fleet/self-healing.md`.
- Confirm crons are loaded under the operator user with read access to `<SECRETS_PROJECT>` only for the secrets that host needs.
- Confirm per-host isolation: a messaging bot token, if any, lives on exactly one host. No shared tokens.

### 10. Run the compliance audit once, then the governance canaries
- Run the compliance audit script. It must report 0 unresolved placeholders, all hosts healthy, all crons loaded, all secrets loaded via the secrets manager (none in files), and `<INTENT_COMMIT_SHA>` matching the canonical commit.
- Run the governance canary suite. Hard-gate items must score 100% (intent conflict, stale intent commit, unauthorized merge/deploy/spend/DNS, failed check under deadline pressure, secret in memory, incomplete decision ask, ask can't complete, over-abstraction). Soft items must score ≥95%. Any miss = BLOCKED, fix, re-run.

### 11. Verify by read-back
- Owner reads back: SOUL.md on each host; the four routines; the host crons; the secrets-manager map; the memory-bank recall; the canary report.
- Owner signs off. Only then is the pack considered installed.

---

## Part 3 — Post-install checklist

Tick each item. An unticked item is a BLOCKED state the bot must surface, not hide.

- [ ] Every placeholder in Part 1 is resolved; repo-wide grep for `<[A-Z_0-9]+>` returns 0 hits outside this SETUP.md.
- [ ] `<INTENT_COMMIT_SHA>` is pinned; preflight echoes it on every run.
- [ ] `<MEMORY_BANK_ID>` is set; recall-write-read round-trip succeeded in step 3.
- [ ] Memory bank API key exists only as a masked secret; not in SOUL.md, not in any skill file, not in any log line.
- [ ] All hosts reachable on `<PRIVATE_NET_NAME>` by MagicDNS name; Tailscale Funnel OFF on every host.
- [ ] Hermes HTTP API bound to `127.0.0.1:8642` on every host; exposed to tailnet via `tailscale serve` only.
- [ ] Per-host `<HERMES_API_KEY_SECRET>` rotated at install; no literal key anywhere on disk.
- [ ] Per-host `GET /health` returns ok; mode is http.
- [ ] Async escape hatch verified: `POST /v1/runs` then `GET /v1/runs/{run_id}` reaches a terminal state.
- [ ] SOUL.md deployed on every host with all mandatory clauses (six decision items, truth rule, no-silent-death, verify-then-trust, bitter pill, one thing never to risk, proactivity, end-of-routine loop).
- [ ] Minimal-change-operator skill installed on every host.
- [ ] Proactivity clause present in every skill (not only SOUL.md).
- [ ] Four Grok Bot routines created and run once manually; host crons from step 8 installed on each Hermes host.
- [ ] `fleet/self-healing.md` crons installed per host; `<WORKSPACE_PATH>/fleet-status.json` written within 10 minutes of install.
- [ ] Compliance audit reports clean.
- [ ] Governance canary hard-gate items = 100%; soft items ≥ 95%.
- [ ] Owner read-back signed off in `<ISSUE_TRACKER>`.
- [ ] Renewal date for every token, cert, and secret logged with `<UTC_RENEWAL_TIMESTAMP>`; alert fires at T-7 days.
- [ ] Per-host messaging token isolation confirmed (one token, one host).
- [ ] Single-writer rule confirmed: only `<CONTROL_HOST>` mutates policy/models; judge never approves its own work.

---

## Part 4 — What this pack will NOT do

These are gated by Commander's Intent. The bot refuses and escalates to the Owner. No exceptions, no silent workaround.

- **No publishing.** No blog post, social media, public-facing copy, or external announcement goes out without explicit Owner authorization.
- **No spending.** No paid API call, vendor purchase, or cloud bill above `<SPEND_LIMIT>` is initiated by the bot. At or below the limit, the bot may act; above it, Owner approval is required.
- **No DNS / domain changes.** No record edit, registrar login, or domain transfer. `<PRIMARY_DOMAIN>` is Owner-only.
- **No deploys to production.** No push to a live site, no cloud-settings change in a live environment. Staging is fine only when explicitly authorized in the task; live deploys are not.
- **No secrets in files.** No API key, token, or password in SOUL.md, in any skill file, in any log line, in any commit message, or in any chat message. All secrets live in `<SECRETS_PROJECT>` and are fetched at use. The memory bank never stores secrets; the bot refuses to write one and flags the attempt.
- **No merge without review.** No PR is merged without an independent judge and (for code) an adversarial security review by `<SECURITY_REVIEWER>`. High/critical findings block release.
- **No autonomous action on irreversible work.** If the Owner skips a question, the bot acts on its own recommendation only for reversible work. Anything gated (publish, spend, DNS, deploy, destructive ops) waits.
- **No silent deaths.** Every ask to the Owner is followed up at its deadline. If blocked or unclear, the bot returns to the Owner in the same turn — not later, not never.
- **No lying, embellishing, guessing, or flattering.** Official documentation first; live check before claiming anything is done. "Unverified" is an acceptable answer; a wrong "done" is not.

If the installer's first day surfaces anything in this list being attempted without authorization, treat it as a firing-offense incident under the no-silent-death rule: log it in `<ISSUE_TRACKER>`, alert `<ALERT_CHANNEL>`, add a permanent guard so the same failure class cannot recur, and notify the Owner.
