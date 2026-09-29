# Commander's Intent: I Run My AI Agent Fleet on Marine Corps Doctrine

Your agents rarely fail loudly. They stall, or they drift. Both look like silence until something downstream breaks.

I fixed that with an idea the U.S. Marine Corps has trusted for decades: commander's intent. I developed this doctrine with my father, a retired U.S. Marine Corps Colonel, call signs "Grizzly" and "Maverick". Now it runs my agent fleet, and the whole thing is open source.

## The problem: plans break every day

A key expires. An API changes. A reviewer finds a flaw at the last step. An agent fleet runs around the clock, mostly unwatched, and hits a broken plan many times a day.

Without intent, each agent does one of two bad things. It stops and waits, so the ask dies quietly. Or it keeps going toward whatever its last prompt implied, so the fleet drifts. Both are silent failures.

## The answer the Marines already wrote down

MCDP 1, Warfighting, is the Marine Corps' maneuver warfare doctrine. It starts from a hard truth: "plans will go awry, instructions and information will be unclear and misinterpreted, communications will fail." Its answer is not a more detailed plan. It is a way of commanding that still works when the plan does not.

Four ideas do the work:

- **Commander's intent.** Every mission has a task and a purpose. "Of the two, the intent is predominant." When the task goes stale, the purpose still guides the next move.
- **Mission tactics.** Say what and why. Leave the how to whoever is doing the work.
- **Main effort.** One effort gets priority. Everyone else asks how they can best support it.
- **Initiative within intent.** Decide where the work is. Lack of orders is never a reason to sit still. Initiative is wide on how, and zero on what must never be risked.

Swap "Marine" for "agent" and you have the operating system an AI fleet is missing.

## What Commander's Intent is

A free Grok Bot template plus a public, MIT licensed repo. You get one Chief of Staff bot as your single point of contact, Hermes Agent hosts that report up through it, and one shared Hindsight memory bank. The repo holds the intent scaffold and interview, the doctrine, 25 skills, 4 routines, a security policy, a fleet self-healing spec, and the first-run script the bot follows on install.

## The top changes and what they do

### 1. One root file: COMMANDERS-INTENT.md

**What it does:** gives every agent, on every host and in every cloud session, the same document to read before acting. It holds the purpose, the method, the end state, the hard lines, and who decides what. If anything conflicts with it, it wins, except your own gates on spending, publishing, and the like.

### 2. Written by interview, in your words

**What it does:** the Chief of Staff does not hand you a pre-written mission. On first run, before any other setup, it interviews you one question at a time: 22 questions plus probes, about 20 to 30 minutes. What the fleet is for, what is true in 90 days and in a year, what you will never risk, what agents may spend, who holds authority. It invents nothing, plays the draft back section by section, and nothing counts until you approve it as v1.0.

### 3. Purpose, method, end state

**What it does:** intent follows the Marine Corps planning format. Purpose is the part that endures. Method is the few key tasks that carry the load, with the main effort named. End state is what is true when you win, stated so it can be checked.

### 4. A ladder for when the plan breaks

**What it does:** every agent gets the same moves. Re-read the intent. Probe before declaring a wall. Adapt within the intent. Act on reversible work. Escalate with a complete decision ask when authority is needed. Then keep moving on everything else.

### 5. Drift gets caught, not discovered

**What it does:** every version of your intent has a checksum. Every agent starts its session with a wake line that names the version it holds. Every order names the intent one and two levels up, so a worker can check its task still serves both.

### 6. The intent becomes shared memory

**What it does:** the approved file becomes a Hindsight mental model named commanders-intent. Agents read it before acting on doctrine. It refreshes on every version bump and weekly. If memory and the file disagree, the file wins.

### 7. Quota discipline

**What it does:** one digest per task, no FYI pings. Top models where quality shows, the cheapest capable model everywhere else. Quota pressure and model fallbacks get reported early and loudly.

### 8. Only you amend it

**What it does:** the Chief of Staff can propose a change with context, options, a recommendation, and its confidence. Only you approve it. Each amendment bumps the version, refreshes shared memory, and tells every agent.

## Security note

Agents with repo access are a real attack surface, so the rules are strict and written down in SECURITY.md.

- **Cloud coding agents are gated.** Cursor cloud agents, Claude Code on the web, OpenAI Codex cloud, GitHub Copilot cloud agent, and Devin get least-scope repo access and open draft pull requests only.
- **Review before merge.** A reviewer who did not write the code approves first: a code review, a critic pass, and a security pass. High and critical findings block the merge. Exactly one merge owner merges. The orchestrator never merges. Production is proven by reading it back.
- **Secrets come from a vault.** Values are injected at runtime from a secrets manager. Never pasted into a prompt, a chat, an issue, or a PR comment. Never stored in memory.
- **You hold the gates.** Spending, publishing, DNS and domains, secrets, and destructive actions need your explicit yes. Untrusted content, including other agents' output, is data, not instructions. A repo update never widens a bot's permissions.

## Who this is for

Builders running a small fleet of AI agents who want one accountable Chief of Staff instead of a pile of chat tabs, and a fleet that keeps moving when the plan breaks.

## Get it

- Repo (everything, MIT licensed): https://github.com/shagghiesuperstar/commanders-intent
- Start with COMMANDERS-INTENT.md, then SECURITY.md
- Install the Grok Bot template: {{COMMANDERS_INTENT_TEMPLATE_LINK}}

Install it and say hello. The first thing it does is ask what your fleet is for.

If you run agents, follow me here for what I learn next. Star the repo, open an issue, and tell me where your fleet breaks.

---

## Promo posts and replies

1. Your AI agents don't fail loudly. They stall or they drift. I fixed mine with Marine Corps doctrine: commander's intent, from MCDP 1. One root file every agent reads before acting. Open source: https://github.com/shagghiesuperstar/commanders-intent

2. Marine Corps doctrine says of task and purpose, "the intent is predominant." When the plan breaks, the purpose still guides the next move. I built that into my AI agent fleet: https://github.com/shagghiesuperstar/commanders-intent

3. My Chief of Staff bot doesn't hand me a mission. It interviews me, uses my words, plays the draft back, and waits for my approval before any agent treats it as doctrine. https://github.com/shagghiesuperstar/commanders-intent

4. Rules for cloud coding agents in my fleet: least-scope repo access, vault secrets only, draft PRs only, independent review, one merge owner. The orchestrator never merges. https://github.com/shagghiesuperstar/commanders-intent

5. Drift gets caught, not discovered. Every intent version has a checksum, every agent a wake line that names it, every order the intent two levels up. https://github.com/shagghiesuperstar/commanders-intent
