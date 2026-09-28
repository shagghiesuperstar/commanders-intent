# MANIFEST

Commander's Intent v0.1.0 (2026-09-28). 41 files. Byte sizes measured before push.

| File | Purpose | Bytes |
|---|---|---:|
| `CHANGELOG.md` | Fabric changelog | 2901 |
| `FABRIC.md` | How the sister templates fit together and the update-in-unison process | 3452 |
| `FIRST-RUN.md` | Exact first-run script the installed bot follows (questions, skills, routines, proofs) | 12548 |
| `INSTALL.md` | Human install overview: what to have ready, what the bot never asks for | 1774 |
| `LICENSE` | MIT license | 1075 |
| `MANIFEST.md` | This file | 6264 |
| `OPEN-QUESTIONS.md` | Open [UNKNOWN] items and how to check them on your fleet | 8335 |
| `README.md` | Landing page: what it is, install, doctrine, architecture, related templates | 8198 |
| `SETUP.md` | Full manual reference: placeholder table and install steps | 18873 |
| `fleet/self-healing.md` | 10-minute host self-heal checks, status file, alerts, nightly reflection | 24275 |
| `persona/SOUL.md` | Chief of Staff persona plus SOUL.md requirements and skeleton for every agent | 22579 |
| `routines/README.md` | How to create the four routines manually, cron table | 4203 |
| `routines/compliance-audit.md` | Daily compliance audit of every standing rule on every host | 11935 |
| `routines/order-follow-up.md` | Order follow-up: ledger format, prompt and cron | 12809 |
| `routines/proactivity-sweep.md` | 30-minute proactivity sweep: prompt and cron | 12142 |
| `routines/update-survival-restore.md` | Hourly self-restore after a Grok Bot computer update | 1538 |
| `skills/chief-of-staff-persona/SKILL.md` | Operating as Chief of Staff (<COS_NAME>) for the Owner — sole point of contact, owner of proactivity, planner not order-taker, runs the dail... | 12238 |
| `skills/commanders-intent/SKILL.md` | An agent needs to load, obey, draft, audit, or refresh the Commander's Intent root document that governs the fleet, or when any task must be... | 15131 |
| `skills/commanders-intent-getting-started/SKILL.md` | On the first conversation after someone installs the Commander's Intent template: fetch FIRST-RUN.md from the canonical repo and run it with... | 1938 |
| `skills/delegate-troubleshooting/SKILL.md` | Troubleshooting backend, admin, logs, or payment-integration issues would burn orchestrator tokens — delegate the dig to a capable model ses... | 4505 |
| `skills/desktop-v1-runs-escape/SKILL.md` | A Grok connector ask to a Hermes host running Hermes locally dies around ~120s with tool error -32001 — escape via host-local POST /v1/runs ... | 5741 |
| `skills/engineering-playbook/SKILL.md` | Shipping code through cloud coding agents, supervising PRs to merge, or running a fleet watcher. Triggers on any new PR stream, draft openin... | 10167 |
| `skills/failure-to-permanent-guard/SKILL.md` | Something has already failed, almost failed, or could fail silently again — to turn that failure into the cheapest permanent guard that make... | 9861 |
| `skills/fleet-post-sprint-hygiene/SKILL.md` | A Hermes or Grok orchestration sprint finishes long asks, merges, browser smokes, CLI harnesses, or heavy SSH work — before declaring DONE o... | 6483 |
| `skills/fleet-reference-architecture/SKILL.md` | Designing, integrating, or troubleshooting the Grok Bot fleet — Owner, Chief of Staff, Hermes agents, Hindsight memory, secrets, Git, and se... | 10815 |
| `skills/fleet-stand-up-runbook/SKILL.md` | Standing up the agent fleet from zero — installing the private net, Hermes Agent, the shared memory bank, secrets, skills, routines, and the... | 15765 |
| `skills/grok-bot-computer-update-survival-tailscale/SKILL.md` | >- | 4544 |
| `skills/hermes-bridge-method-chooser/SKILL.md` | Choosing how Hermes is reached from Grok Bot — the fleet default and only allowed ask/manage path is the native Hermes HTTP API on port 8642... | 7561 |
| `skills/hermes-fleet-bws-inventory/SKILL.md` | Inventorying or verifying Bitwarden Secrets Manager (BWS) on Hermes Agent hosts, or when API_SERVER_KEY or Hindsight auth drifts — never ass... | 7421 |
| `skills/hermes-fleet-messaging-token-isolation/SKILL.md` | Storing messaging bot tokens (Telegram, Discord, Slack, etc.) for a Hermes Agent fleet in a shared secrets manager — never share one bot tok... | 6548 |
| `skills/hermes-http-only-talk-path/SKILL.md` | Wiring a Hermes Agent ask/health/manage connector, when an ask or health check fails, when MCP custom instructions still mention SSH, or any... | 6773 |
| `skills/hindsight-hermes-memory/SKILL.md` | Any agent in the fleet needs to remember or look up anything durable: recall context before non-trivial work, reflect for a reasoned answer,... | 10492 |
| `skills/hindsight-mental-models/SKILL.md` | Creating, listing, refreshing, dry-running, clearing, or deleting Hindsight Cloud mental models in the single fleet memory bank, so every fl... | 13716 |
| `skills/minimal-change-operator/SKILL.md` | Planning, reviewing, proposing, or implementing any code or configuration change. Use it before writing code, when reviewing a diff or pull ... | 18974 |
| `skills/proactivity-sweep/SKILL.md` | Running the periodic (or on-demand) silent-failure and overdue-promise sweep across the fleet, when the Owner asks 'what's silently broken?'... | 7816 |
| `skills/research-done-gate/SKILL.md` | Marking any research, recon, probe, or 'answer whether X' ticket Done — require tracker status Done + a written evidence artifact before rep... | 5555 |
| `skills/soul-md-template/SKILL.md` | Creating or auditing a SOUL.md file for any agent host in the fleet — the persona file that pins identity, lane, chain of command, standing ... | 14080 |
| `skills/verify-by-read-back/SKILL.md` | You have just made any write or change to prove the artifact matches the intended state by reading it back from the live system before repor... | 9145 |
| `skills/wire-hermes-native-api/SKILL.md` | An installer needs to enable Hermes Agent's native HTTP API on port 8642 on an agent host, verify health, or add a private-network-reachable... | 6539 |
| `social/x-article-v0.1.md` | v0.1 release article and reply variants | 6351 |
| `tools/hindsight/hs.py` | Standard-library Hindsight REST helper (bank from HINDSIGHT_BANK) | 3545 |

Total files: 41. Total bytes: 374605.
