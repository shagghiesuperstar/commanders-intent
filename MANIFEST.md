# MANIFEST

Commander's Intent v0.2.1 (2026-09-28). 51 files. Byte sizes measured before push.

| File | Purpose | Bytes |
|---|---|---:|
| `.github/CODEOWNERS` | Code owners: every path requests review from the repo owner (SECURITY.md section 8) | 85 |
| `CHANGELOG.md` | Fabric changelog | 8872 |
| `COMMANDERS-INTENT.md` | Start here. The Commander's Intent scaffold and fixed doctrine; filled by interview, approved by the Owner, fleet-wide source of truth | 29428 |
| `FABRIC.md` | The root of the fabric (COMMANDERS-INTENT.md), how sister templates fit together, update-in-unison process, leak scan | 4603 |
| `FIRST-RUN.md` | Exact first-run script: intent interview first, then memory and mental model, alignment, security gates, setup, skills, routines, proofs | 16189 |
| `INSTALL.md` | Human install overview: what to have ready, time, what the bot never asks for | 2448 |
| `LICENSE` | MIT license | 1075 |
| `MANIFEST.md` | This file | 7796 |
| `OPEN-QUESTIONS.md` | Open [UNKNOWN] items and how to check them on your fleet | 10354 |
| `README.md` | Landing page: start here (Commander's Intent), install, doctrine, architecture, repo map, related templates | 11720 |
| `SECURITY.md` | Threat model, secrets, prompt injection, supply chain, cloud coding agents, data handling, incident response, vulnerability reporting | 21280 |
| `SETUP.md` | Full manual reference: placeholder table and install steps | 19919 |
| `examples/commanders-intent-example.md` | Fictional filled Commander's Intent, example only | 7034 |
| `fleet/self-healing.md` | 10-minute host self-heal checks, status file, alerts, nightly reflection | 24275 |
| `interview/commanders-intent-interview.md` | Chief of Staff interview script: staged questions, probes, playback, approval, amend flow | 10451 |
| `mental-models/commanders-intent.json` | Create body for the commanders-intent mental model | 934 |
| `mental-models/commanders-intent.md` | The commanders-intent Hindsight mental model: scoping, refresh triggers, hs.py commands, how agents query it | 6533 |
| `persona/SOUL.md` | Chief of Staff persona plus SOUL.md requirements and skeleton for every agent | 23738 |
| `routines/README.md` | How to create the four routines manually, cron table | 4203 |
| `routines/compliance-audit.md` | Daily compliance audit of every standing rule on every host | 11935 |
| `routines/order-follow-up.md` | Order follow-up: ledger format, prompt and cron | 12809 |
| `routines/proactivity-sweep.md` | 30-minute proactivity sweep: prompt and cron | 12142 |
| `routines/update-survival-restore.md` | Hourly self-restore after a Grok Bot computer update | 1538 |
| `skills/chief-of-staff-persona/SKILL.md` | Operating as Chief of Staff (<COS_NAME>) for the Owner: sole point of contact, owner of proactivity, planner not order-taker, runs the dail... | 12725 |
| `skills/commanders-intent-getting-started/SKILL.md` | On the first conversation after someone installs the Commander's Intent template: fetch FIRST-RUN.md from the canonical repo and run it with... | 3123 |
| `skills/commanders-intent-interview/SKILL.md` | Run the interview, write the approved intent under /home/box, build the mental model, notify the fleet | 8063 |
| `skills/commanders-intent/SKILL.md` | An agent needs to load, obey, draft, audit, or refresh the Commander's Intent root document that governs the fleet, or when any task must be... | 12501 |
| `skills/delegate-troubleshooting/SKILL.md` | Troubleshooting backend, admin, logs, or payment-integration issues would burn orchestrator tokens: delegate the dig to a capable model ses... | 4505 |
| `skills/desktop-v1-runs-escape/SKILL.md` | A Grok connector ask to a Hermes host running Hermes locally dies around ~120s with tool error -32001: escape via host-local POST /v1/runs ... | 5741 |
| `skills/engineering-playbook/SKILL.md` | Shipping code through cloud coding agents, supervising PRs to merge, or running a fleet watcher. Triggers on any new PR stream, draft openin... | 10760 |
| `skills/failure-to-permanent-guard/SKILL.md` | Something has already failed, almost failed, or could fail silently again: to turn that failure into the cheapest permanent guard that make... | 9861 |
| `skills/fleet-post-sprint-hygiene/SKILL.md` | A Hermes or Grok orchestration sprint finishes long asks, merges, browser smokes, CLI harnesses, or heavy SSH work: before declaring DONE o... | 6483 |
| `skills/fleet-reference-architecture/SKILL.md` | Designing, integrating, or troubleshooting the Grok Bot fleet: Owner, Chief of Staff, Hermes agents, Hindsight memory, secrets, Git, and se... | 10815 |
| `skills/fleet-stand-up-runbook/SKILL.md` | Standing up the agent fleet from zero: installing the private net, Hermes Agent, the shared memory bank, secrets, skills, routines, and the... | 15863 |
| `skills/grok-bot-computer-update-survival-tailscale/SKILL.md` | >- | 4544 |
| `skills/hermes-bridge-method-chooser/SKILL.md` | Choosing how Hermes is reached from Grok Bot: the fleet default and only allowed ask/manage path is the native Hermes HTTP API on port 8642... | 7561 |
| `skills/hermes-fleet-bws-inventory/SKILL.md` | Inventorying or verifying Bitwarden Secrets Manager (BWS) on Hermes Agent hosts, or when API_SERVER_KEY or Hindsight auth drifts: never ass... | 7463 |
| `skills/hermes-fleet-messaging-token-isolation/SKILL.md` | Storing messaging bot tokens (Telegram, Discord, Slack, etc.) for a Hermes Agent fleet in a shared secrets manager: never share one bot tok... | 6548 |
| `skills/hermes-http-only-talk-path/SKILL.md` | Wiring a Hermes Agent ask/health/manage connector, when an ask or health check fails, when MCP custom instructions still mention SSH, or any... | 6773 |
| `skills/hindsight-hermes-memory/SKILL.md` | Any agent in the fleet needs to remember or look up anything durable: recall context before non-trivial work, reflect for a reasoned answer,... | 10492 |
| `skills/hindsight-mental-models/SKILL.md` | Creating, listing, refreshing, dry-running, clearing, or deleting Hindsight Cloud mental models in the single fleet memory bank, so every fl... | 14003 |
| `skills/minimal-change-operator/SKILL.md` | Planning, reviewing, proposing, or implementing any code or configuration change. Use it before writing code, when reviewing a diff or pull ... | 18974 |
| `skills/proactivity-sweep/SKILL.md` | Running the periodic (or on-demand) silent-failure and overdue-promise sweep across the fleet, when the Owner asks 'what's silently broken?'... | 7816 |
| `skills/quota-token-discipline/SKILL.md` | One digest per task, no FYI wakes, right-sized models, no tight polling, loud quota and fallback warnings | 4485 |
| `skills/research-done-gate/SKILL.md` | Marking any research, recon, probe, or 'answer whether X' ticket Done: require tracker status Done + a written evidence artifact before rep... | 5555 |
| `skills/soul-md-template/SKILL.md` | Creating or auditing a SOUL.md file for any agent host in the fleet: the persona file that pins identity, lane, chain of command, standing ... | 14219 |
| `skills/verify-by-read-back/SKILL.md` | You have just made any write or change to prove the artifact matches the intended state by reading it back from the live system before repor... | 9145 |
| `skills/wire-hermes-native-api/SKILL.md` | An installer needs to enable Hermes Agent's native HTTP API on port 8642 on an agent host, verify health, or add a private-network-reachable... | 6539 |
| `social/x-article-v0.1.md` | v0.1 release article and reply variants | 6351 |
| `social/x-article-v0.2.md` | v0.2 release article and reply variants | 6026 |
| `tools/hindsight/hs.py` | Standard-library Hindsight REST helper (bank from HINDSIGHT_BANK; recall, reflect, retain, mental model list/get/create/patch/refresh) | 3976 |

Total files: 51. Total bytes: 490271.
