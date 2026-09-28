# Commander's Intent: How I Run an AI Agent Fleet That Fixes Itself and Reports to One Chief of Staff

Most agent setups fail the same way. Nothing tells you they broke. A cron dies, a key drifts, a promise slips, and you find out when something downstream is already on fire.

Commander's Intent is my answer to that. It is a free, open Grok Bot template plus a public repo. It gives you one Chief of Staff bot that runs your fleet (Grok Bot plus Hermes Agent hosts), governed by one written root document, backed by one shared memory bank. It does not wait to be asked. It finds what is silently broken, fixes what is safe to fix, and orders you to handle the rest with a deadline and the proof it needs.

Version 0.1 is live today. Here is what is in it.

## 1. One root document: Commander's Intent

Every agent reads the same document before acting: the mission, what winning looks like by a date, the one thing never to risk, and who decides what. It lives in Git, so it has history and an owner. When anything conflicts with it, the document wins, except your own gates on spending, publishing, DNS, and secrets.

## 2. One Chief of Staff, one chain of command

You talk to one bot. Every other agent reports up through it, so you never chase anyone. When it needs a decision, it must bring six things in one message: context, the decision, options, a recommendation, the reasoning, and its confidence. If any part is missing, it does not send.

## 3. One memory bank for the whole fleet

Every agent reads and writes the same Hindsight memory bank. Decisions, locks, and lessons are recorded once and shared, so you stop repeating yourself to each agent. Git stays the source of truth; memory is the fast shared view, and it never stores secrets.

## 4. Proactivity at every level

Proactivity is built into the persona, every routine, and every skill. Each one ends by asking what else is silently broken, what was promised, and what is due, and then acts in the same turn. A 30-minute sweep, a daily compliance audit, and a 15-minute order follow-up keep that loop running when you are not watching.

## 5. Self-healing every 10 minutes, reflection every night

Each Hermes host runs health checks every 10 minutes, auto-fixes known failures, writes a status file, and alerts you only on what it could not fix. A nightly reflection reviews the day's failures. Each new kind of failure gets a new check, so the same problem does not stay quiet twice.

## 6. Verify, then trust

A change is not done until it is read back from the live system and matches. A tool's "OK", another agent's "done", and the bot's own memory of what it wrote do not count. When a live check is not possible, the bot says "unverified" instead of guessing.

## 7. Every failure becomes a permanent guard

When something breaks, the fix is only half the job. The bot names the failure class, picks the cheapest guard that makes a repeat loud (a check, a test, a cron, or a written directive), then triggers the failure on purpose to prove the guard fires. Your fleet gets harder to break over time instead of just older.

## 8. Survives computer wipes

The Grok Bot computer can be replaced under you at any time, which wipes installed tools and anything outside the home folder. Commander's Intent keeps all state and restore scripts in the persistent folder and runs an hourly self-restore. In a live drill we removed the private-network client and it came back with the same identity in 137 seconds, with no human step.

## 9. HTTP-only talk path to Hermes

The Chief of Staff reaches every Hermes host over the native Hermes HTTP API on port 8642, inside your private network. One path means one thing to secure, monitor, and debug. SSH relay stays available as a legacy option for a single desktop host, but it is never the fleet path.

## 10. A minimal-change operator on every agent

Before any change, an agent states the purpose, the method, and the observable end state, and labels each claim verified, inferred, or unknown. It looks for an existing capability before writing anything new and reports BLOCKED instead of DONE when any check fails. Less code, fewer surprises, and a clear trail of why each change happened.

## Bonus: templates that update together

Commander's Intent is the command layer of a small set of Grok Bot templates: Hermes API Fleet, Hermes Fleet Ops, and n8n Master. They follow one shared doctrine and ship under one changelog, so a bot installed from any of them follows the same rules. Installed bots check the changelog and propose updates to you; they never widen their own permissions because a file changed.

## Get it

- Repo (everything, MIT licensed): https://github.com/shagghiesuperstar/commanders-intent
- Install the Grok Bot template: {{COMMANDERS_INTENT_TEMPLATE_LINK}}

Install it, say hello, and it walks you through setup one question at a time: names, memory, skills, your Commander's Intent, and its routines. It proves each step before moving on.

If you run agents and you are tired of finding out last, try it and tell me what breaks. That is exactly the kind of failure it is built to turn into a guard.

---

## Reply variants (each under 280 characters)

1. Agents rarely fail loudly. They just stop. Commander's Intent gives your fleet one Chief of Staff that checks every 30 min, fixes what's safe, and orders you on the rest with a deadline. Free template + repo: https://github.com/shagghiesuperstar/commanders-intent

2. The fix for "my agent said done but it wasn't": read-back or it didn't happen. Every change in Commander's Intent is verified against the live system before it counts. Open repo: https://github.com/shagghiesuperstar/commanders-intent

3. One root doc. One Chief of Staff. One memory bank for every agent. That's how I run my Grok Bot + Hermes fleet. Open-sourced the whole thing: https://github.com/shagghiesuperstar/commanders-intent

4. Grok Bot's computer can get wiped under you. Mine restores itself hourly; in a live drill it came back in 137 seconds with no human step. Setup is in the repo: https://github.com/shagghiesuperstar/commanders-intent

5. Every failure in my agent fleet becomes a permanent guard: a check, test, cron, or rule, proven to fire. The fleet gets harder to break over time. Template + repo: https://github.com/shagghiesuperstar/commanders-intent
