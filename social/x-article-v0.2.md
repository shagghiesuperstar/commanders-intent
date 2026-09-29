# Commander's Intent v0.2: Every Agent Knows the Mission, Even When the Plan Breaks

The U.S. Marine Corps builds its warfighting doctrine on a hard truth: plans go awry and communications fail. Its answer, in MCDP 1, Warfighting, is commander's intent. Every mission has a task and a purpose, and of the two the purpose wins. When the situation makes the task obsolete, every Marine still knows why they were sent, so they act within the intent instead of waiting for new orders or improvising their way off course. The Marines add mission tactics (say what and why, leave the how to the person doing it) and a main effort (one thing gets priority; everyone else asks how to support it).

This doctrine was developed with my father, a retired U.S. Marine Corps Colonel, call signs "Grizzly" and "Maverick".

An AI agent fleet hits a broken plan many times a day. A key expires, an API changes, a reviewer finds a flaw. Without intent, each agent either stops and waits, so the ask dies quietly, or it keeps going toward whatever its last prompt implied, so the fleet drifts. Both are silent failures.

Commander's Intent v0.1 gave you a Chief of Staff bot and the rules around it. v0.2 puts the intent itself at the center. Here is what changed.

## 1. The intent is a real file at the root: COMMANDERS-INTENT.md

One document every agent reads before acting, on every host and in every cloud session. It holds the purpose, the method (key tasks and the main effort), the end state, the hard lines, and who decides what. When anything conflicts with it, it wins, except your own gates on spending, publishing, and the like.

## 2. It is written by interview, in your words

The Chief of Staff does not hand you a pre-written mission. On first run, before any other setup, it interviews you one question at a time: what the fleet is for, what is true in 90 days and in a year, what winning looks like, what you will never risk, what agents may spend, who holds authority, what drift looks like to you, and how you want to be reached. It invents nothing, plays the draft back section by section, and nothing counts until you approve the final text as v1.0.

## 3. Agents know what to do when the plan breaks

The fixed doctrine gives every agent the same ladder: re-read the intent, probe before declaring a wall, adapt within the intent, act on reversible work, and escalate with a complete decision ask when authority is needed. Then keep moving on everything else. Initiative is wide on how. It is zero on what must never be risked.

## 4. Drift gets caught, not discovered

Every version of your intent has a checksum. Every agent starts its session with a wake line that names the version it holds. Every order names the intent one and two levels up, so a worker can check its task still serves both. The Chief of Staff watches for drift signals, including your own examples from the interview, and corrects through one loop.

## 5. The intent becomes shared memory

The approved file is turned into a Hindsight mental model named commanders-intent, scoped to the current version. Agents read it before acting on doctrine. It refreshes on every version bump and weekly, and the file always wins on a mismatch.

## 6. A security policy for a multi-agent fleet

SECURITY.md covers the threat model, secrets, prompt injection, repo supply chain, data handling, memory hygiene, and an incident runbook. Untrusted content, including other agents' output, is data, not instructions. Only you grant authority, and a repo update never widens a bot's permissions.

## 7. Cloud coding agents on a short leash

Cursor cloud agents, Claude Code on the web, OpenAI Codex cloud, GitHub Copilot cloud agent, Devin, and the rest follow the same rules: least-scope repo access, secrets from a vault at runtime and never pasted into a prompt, draft pull requests only, independent review, and exactly one merge owner. The orchestrator never merges. Production is proven by reading it back.

## 8. Quota discipline

One digest per task. No FYI pings. Top models where quality shows, the cheapest capable model everywhere else. Quota pressure and model fallbacks are reported early and loudly, never absorbed silently.

## 9. Only you amend it

The Chief of Staff can propose a change, with context, options, a recommendation, and its confidence. Only you approve it. Each amendment bumps the version, refreshes the shared memory, and tells every agent.

## Get it

- Repo (everything, MIT licensed): https://github.com/shagghiesuperstar/commanders-intent
- Start with COMMANDERS-INTENT.md, then SECURITY.md
- Install the Grok Bot template: {{COMMANDERS_INTENT_TEMPLATE_LINK}}

Install it and say hello. The first thing it does is ask what your fleet is for.

---

## Reply variants (each under 280 characters)

1. Commander's intent, straight from Marine Corps doctrine: tell every level why, what done looks like, and what never to risk, so they keep moving when the plan breaks. v0.2 builds it into an AI agent fleet. Open repo: https://github.com/shagghiesuperstar/commanders-intent

2. My Chief of Staff bot doesn't hand me a mission. It interviews me, uses my words, plays the draft back, and waits for my approval before any agent treats it as doctrine. v0.2: https://github.com/shagghiesuperstar/commanders-intent

3. Agents drift quietly. v0.2 gives every intent version a checksum, every agent a wake line that names it, and every order the intent two levels up. Drift gets caught, not discovered. https://github.com/shagghiesuperstar/commanders-intent

4. Rules for cloud coding agents in my fleet: least-scope repo access, vault secrets only, draft PRs only, independent review, one merge owner. The orchestrator never merges. Written up in SECURITY.md: https://github.com/shagghiesuperstar/commanders-intent

5. One digest per task. No FYI pings. Top models where quality shows, cheap ones elsewhere. Quota discipline is now part of the Commander's Intent doctrine in v0.2: https://github.com/shagghiesuperstar/commanders-intent
