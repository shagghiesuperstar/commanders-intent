# Commander's Intent interview script

The Chief of Staff runs this interview with the Owner on first run, before any other setup, to fill Part II of [`COMMANDERS-INTENT.md`](../COMMANDERS-INTENT.md). It also covers amending the intent later. The skill that drives it is [`skills/commanders-intent-interview`](../skills/commanders-intent-interview/SKILL.md).

Written to the Chief of Staff, in the second person.

## Rules for the whole interview

1. **One question at a time**, or a small batch of two or three closely related questions if the Owner asks to go faster. Wait for the answer.
2. **The Owner's own words.** Record answers verbatim first. Tighten wording only during playback, and only with the Owner's yes. Never swap in your own phrasing silently.
3. **No invented facts.** Never propose numbers, dates, targets, names, or limits. If the Owner cannot answer, record the slot as an open field with what it blocks. A gap you surface is better than a guess you fill.
4. **Restate and confirm** after each answer: "So what I heard is ... Is that right?"
5. **Probe once or twice, not ten times.** Use the follow-up probes to make an answer checkable, then move on.
6. **Plain English.** No jargon, no military idiom. The doctrine words used here (purpose, end state, key tasks, main effort) are explained the first time you use them.
7. **Never ask for a secret.** If an answer needs a credential, ask for its name only and note it for the secure secret request later.
8. **Pause and resume.** If the Owner stops, save progress (in the persistent home copy; in memory once the bank is connected) and resume at the same question next time.
9. **Explicit approval.** Nothing becomes the Owner's intent until the Owner explicitly approves the final text. "Looks fine" in passing is not approval; ask for a clear yes to the exact version.

## Stage 0. Frame (say this, in your own words)

"Before I set anything else up, I want to write down your Commander's Intent: what this fleet is for, what winning looks like, and the lines we never cross. Every agent will read it before acting, so when a plan breaks they can keep moving toward your goal without drifting. It takes about 20 to 30 minutes. I will use your words, not mine, and you approve the final text before it counts. You can skip any question and we can pause any time."

Then ask question 0: **"What should I call you, and what should you call me?"** Fills `{{OWNER_NAME}}` and `{{COS_NAME}}`. The header slots `{{INTENT_VERSION}}`, `{{INTENT_STATUS}}`, `{{APPROVAL_DATE}}`, and `{{INTENT_CANONICAL_LOCATION}}` are filled by the skill at approval time, not asked.

## Stage 1. Mission and why (fills section 4)

| # | Question | Slot | Follow-up probes |
|---|---|---|---|
| 1 | In one or two sentences, what is this fleet for? Try the form "We do X in order to Y." | `{{MISSION}}` | "Who benefits when this works?" "If a new agent read only this sentence, what would it do first?" |
| 2 | What breaks, or what is lost, if this mission fails? | `{{WHY_IT_MATTERS}}` | "Is that money, time, people, or reputation?" "What happens in the first month if nothing changes?" |
| 3 | Who does this serve? Groups, not individuals. | `{{WHO_IT_SERVES}}` | "Anyone we should not serve, or not yet?" |

## Stage 2. End state (fills section 5)

| # | Question | Slot | Follow-up probes |
|---|---|---|---|
| 4 | Ninety days from now, what is true that is not true today? | `{{END_STATE_90_DAYS}}` | "How would we check that from a dashboard, a URL, or a report?" |
| 5 | One year from now, what is true? | `{{END_STATE_1_YEAR}}` | "Is that a business fact or a method? A deploy or a merge is a method." |
| 6 | Pick a date. On that date, what would you look at to know we won? List each condition. | `{{WINNING_DATE}}`, `{{WINNING_CONDITIONS}}` | "Can an agent answer yes, no, or N/A for each line today?" "Is one proof enough, or does it need to keep passing?" |
| 7 | What should we deliberately not chase right now? | `{{NOT_IN_END_STATE}}` | "What looks useful but would be a distraction?" |

## Stage 3. Key tasks and main effort (fills section 6)

| # | Question | Slot | Follow-up probes |
|---|---|---|---|
| 8 | What are the three to seven things the fleet must do to reach that end state? | `{{KEY_TASKS}}` | "If we did only these, would we win?" "Which one is actually a method for another?" |
| 9 | Which one gets first claim on attention and quota right now? Only one. | `{{MAIN_EFFORT}}` | "Until when, or until what is true?" |
| 10 | What must stay true while we work on that, no matter what? For example site up, orders flowing, backups fresh. | `{{KEEP_ALIVE_FLOORS}}` | "What number counts as broken for each?" |

## Stage 4. Hard lines, risk, and spend (fills section 7)

| # | Question | Slot | Follow-up probes |
|---|---|---|---|
| 11 | Name one thing we will never trade away for any other gain. | `{{NEVER_RISK}}` | "What would a breach of that look like in practice?" |
| 12 | Here is the fixed never-without-GO list (read it out from section 7). Anything you want to add? | `{{OWNER_EXTRA_GATES}}`, `{{OWNER_EXTRA_GATES_WHY}}` | "Any action that would embarrass you if an agent did it without asking?" Remind the Owner the fixed items cannot be removed. |
| 13 | Where are you comfortable taking risk to go faster, and where do you want extra caution? | `{{RISK_TOLERANCE}}` | "Staging versus production? Internal versus customer-facing?" |
| 14 | How much may agents spend without asking, per what period? Who, by role, may spend? Should anything be frozen right now? | `{{SPEND_LIMIT}}`, `{{NAMED_SPENDERS}}`, `{{SPEND_FREEZE}}` | "Is 'none' the right answer for now?" Never suggest an amount. |

## Stage 5. Authority (fills sections 8 and 9)

| # | Question | Slot | Follow-up probes |
|---|---|---|---|
| 15 | When speed and polish fight, which wins, and where do you override that? | `{{CONFLICT_RULES}}` | "Where does quality show most for you?" |
| 16 | Let us walk the who-decides-what table row by row. Anything you want to keep for yourself? | `{{LIVE_SITE_DECIDER}}`, `{{LIVE_SITE_GATE}}`, `{{REPO_ADMIN_DECIDER}}`, `{{REPO_ADMIN_GATE}}`, `{{POLICY_DECIDER}}`, `{{POLICY_GATE}}`, `{{OTHER_DECISION}}`, `{{OTHER_DECIDER}}`, `{{OTHER_GATE}}` | For each row: "hard (your yes every time) or soft (heads-up and risk rundown, then act)?" |
| 17 | Who reviews code for security, and who is the one merge owner? Neither may be the author, and the merge owner is not me. | `{{SECURITY_REVIEWER}}`, `{{MERGE_OWNER}}` | "Person or separate agent?" "Is the merge owner a distinct account?" |
| 18 | What is the chain of command, and who acts for me if I go silent? | `{{CHAIN_OF_COMMAND}}`, `{{COS_DEPUTY}}` | "Is there a Lead Operator between you and me?" |

## Stage 6. Friction and drift (fills section 10)

| # | Question | Slot | Follow-up probes |
|---|---|---|---|
| 19 | When an agent is blocked, do you want it to try a reversible Plan B first and tell you after, or ask first? | `{{OWNER_BLOCKED_PREFERENCE}}` | "Does that change for anything customer-facing?" |
| 20 | What does drift look like to you? Give me an example of work that looks busy but is off-mission. | `{{DRIFT_LOOKS_LIKE}}` | "Has that happened before? What was the first sign?" |
| 21 | What tools or efficiencies have you built that every agent must use before building its own? | `{{EFFICIENCIES}}` | "Memory bank, code map, sign-ins, cheaper inference?" |

## Stage 7. Communication (fills section 10)

| # | Question | Slot | Follow-up probes |
|---|---|---|---|
| 22 | How should I reach you: channel, format, quiet hours, and how loud for a real blocker? How often do you want a digest? | `{{COMMS_PREFERENCES}}` | "One digest per task and no FYI pings is the default. Keep it?" |

## Stage 8. Playback and approval

1. **Draft.** Fill every slot in a copy of `COMMANDERS-INTENT.md`. Remove the interviewer notes. Leave Parts I and III untouched. Any unanswered slot becomes a row in an "Open fields" table with what it blocks and what proceeds without it.
2. **Play back section by section.** Read each filled section aloud in the Owner's words. After each, ask: "Is this right? Anything to change?" Apply edits and read the changed lines back.
3. **Checkability pass.** For each end state line, say how an agent will check it. If you cannot, ask the Owner to sharpen it or mark it `[UNKNOWN]`.
4. **Final read.** Show the full text. State the version (`v1.0`) and that it will become the fleet's root document.
5. **Explicit approval.** Ask: "Do you approve this text as v1.0 of your Commander's Intent?" Only a clear yes counts. Record the date, time, and the Owner's exact words of approval.
6. **Save and prove.** Hand off to the skill: write the file, compute the checksum, build the mental model, broadcast. Read each back.
7. **Alignment confirmation.** Say back to the Owner, in three sentences, the purpose, the end state, and the one thing never to risk, as you now understand them. Ask the Owner to confirm. This is your proof that the intent landed.

## Re-interview and amend flow

Use this when the Owner wants to change the intent, when the end state date passes, when the main effort is reached, or when the Chief of Staff sees repeated drift that traces to an unclear section.

1. **Only the Owner amends.** The Chief of Staff may propose an amendment with the six-part ask; it never edits the intent on its own.
2. **Scope it.** Ask which sections change. Re-run only those stages. Keep the rest.
3. **Version it.** Wording clarification: minor bump (`v1.0` to `v1.1`). Change to purpose, end state, hard lines, or who decides what: major bump (`v1.1` to `v2.0`).
4. **Play back and approve** the changed sections exactly as in Stage 8, then the whole file once more.
5. **Commit and record.** New file to the canonical location, new checksum, new row in the intent change log.
6. **Refresh memory.** Retain the changed sections with the new version tag and refresh the `commanders-intent` mental model (see [`mental-models/commanders-intent.md`](../mental-models/commanders-intent.md)).
7. **Notify the fleet.** Send every agent the new wake line (`DOCTRINE <sha> | INTENT <version> <checksum12> | LANE <lane>`) and a one-paragraph summary of what changed. Agents on the old version halt at their next action until they refresh.
8. **Verify.** Sample each agent's next wake line. Any agent still on the old version is a drift finding for the next sweep.
