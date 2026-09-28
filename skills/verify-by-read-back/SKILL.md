---
name: verify-by-read-back
description: "Use this when you have just made any write or change to prove the artifact matches the intended state by reading it back from the live system before reporting DONE."
---

# Verify by Read-Back

## The rule
A change is **not done** until an **independent read-back from the live system matches the intended state**. A tool's success message, an agent's report, a passing test, or your own memory of what you wrote are not evidence. Closeout status is **DONE** only when the read-back matches; otherwise it is **BLOCKED** or **unverified**, and you say which and why.

## Label every read-back claim
- `[VERIFIED]` — read-back matches intended state with timestamp, command, and output.
- `[INFERRED]` — plausible but not directly read back (say what would close it).
- `[UNKNOWN]` — cannot read back (say why and what you need).

Never upgrade a label by confident wording. The Commander's Intent's Truth Rule and Verify-Then-Trust Rule win here.

## Read-back recipes

### 1. File on a local host
Independent read means a fresh read after the write — not the writer re-reading its own buffer.

```
# Write
$EDITOR <WORKSPACE_PATH>/path/to/file
# Independent read-back
ls -la <WORKSPACE_PATH>/path/to/file           # exists, size sane
sha256sum <WORKSPACE_PATH>/path/to/file        # hash matches what you intended to write
sed -n '1,5p' <WORKSPACE_PATH>/path/to/file    # content excerpt matches intent
```

Report: path, size, sha256, excerpt, timestamp of the read command.

### 2. File on a remote host (<HOST_1>, <HOST_2>, etc.)
Do **not** SSH to read back. SSH is forbidden as the ask path. Use the host's Hermes Agent native HTTP API on the private tailnet.

```
# Ask the host's agent to read the file and report back
curl -sS -X POST http://<PRIVATE_NET_HOSTNAME>:8642/v1/runs \
  -H "Authorization: Bearer $HERMES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "Read back file <WORKSPACE_PATH>/path/to/file. Report ls -la, sha256sum, and first 10 lines. Do not edit."}'
```

Bearer key loaded from the host's local env, never echoed. If the read-back comes back short, ask a follow-up — do not assume success. [INFERRED] connector asks time out around 120s with error code -32001; if a read will exceed that, escape to a host-local run via POST http://127.0.0.1:8642/v1/runs with body `{"input": "..."}` and poll GET /v1/runs/{run_id}.

### 3. Cron job
```
crontab -l                                # current user's crontab
ls -la /etc/cron.d/ /etc/cron.daily/      # system drop-ins
systemctl list-timers --all               # systemd timers (Hermes self-heal runs here per host)
```
Read back must show: schedule, command, user, and that the job's binary or script exists. If the job is supposed to write a status file (e.g. <WORKSPACE_PATH>/fleet-status.json), confirm the file's mtime is recent relative to the schedule.

### 4. Cloud memory fact (Hindsight Cloud <MEMORY_BANK_ID>)
Write is not done until a recall returns the fact with the same key, scope, and value.

```
# Recall by the exact key/identifier you wrote
curl -sS "$HINDSIGHT_RECALL_URL" \
  -H "Authorization: Bearer $MEMORY_API_KEY" \
  -d '{"bank":"<MEMORY_BANK_ID>","query":"<key or phrase>"}'
```

Read-back must show: the fact, its scope, and the recall timestamp. If recall returns nothing or a different value, the write failed — fix the write, do not re-assert. Never store secrets in memory; if you wrote one, report it as a finding and rotate.

### 5. Pull request (GitHub or equivalent)
```
gh pr view <PR_REF> --json number,title,state,mergeable,headRefOid,baseRefOid
gh pr diff <PR_REF> | head -200
gh pr checks <PR_REF>
```
Read-back must show: PR exists, diff matches the intended change (no unrelated files), required checks pass. If CI is red, status is **BLOCKED**, not **DONE**.

### 6. Config / live-site setting
For cloud or live-site changes owned by COS with a heads-up to the Owner: read the live value back from the provider's API or console command, not from a local config file. Report provider, region/project, setting name, current value, timestamp.

### 7. Secrets manager entry (e.g. Bitwarden Secrets Manager project <SECRETS_PROJECT>)
```
# Confirm the item exists and is bound to the right host
bsec secret list --project <SECRETS_PROJECT> | grep <SECRET_ITEM_NAME>
```
Never echo the secret value. Read-back confirms: item name, project, bound host, masked value preview only. If a token is supposed to live on exactly one host, read back which host holds it and confirm no other host lists it.

## When read-back is impossible
Say so plainly. Use the word **unverified**. State:
1. What you tried (command, host, endpoint).
2. Why it failed or was unavailable (timeout, permission, vendor outage).
3. What would close it (a specific command a human or another agent can run).
4. Status: **BLOCKED** if the change is gated or load-bearing; **unverified** if reversible and time-boxed, with a deadline and a follow-up cron or check to close it.

Do not mark **DONE** on intent alone.

## Anti-patterns (each one is a failure mode that becomes a permanent guard)
- **Trusting a tool's "OK" / exit 0.** Exit code proves the tool ran, not that it changed what you intended. Always read back.
- **Trusting another agent's "done" report.** Cross-check with your own read-back on the artifact, not on the report. Verify first, then trust.
- **Re-reading your own write buffer.** A writer re-reading memory or a file it just wrote is not independent. Use a fresh process, host, or agent.
- **Caching an old read.** If the artifact is mutable, re-read at closeout, do not reuse a read from earlier in the task.
- **Hashing the wrong path.** Confirm path and hostname before hashing; one transposed character is a silent miss.
- **Skipping read back under deadline pressure.** Deadline pressure turns **DONE** into a lie. Status stays **BLOCKED** until verified.
- **Read-back via SSH on a remote host.** Forbidden ask path; the agent layer requires HTTP :8642 over the private tailnet.
- **Echoing secrets in the read-back output.** Mask, never print; rotate immediately if a secret was ever written to memory or a log.

## Permanent guard for each failure class
Every time a read-back is missed or faked and later caught, add one of:
- a CI check that re-reads the artifact and diffs it,
- a cron (the host's 10-minute Hermes self-heal cron) that re-verifies and writes <WORKSPACE_PATH>/fleet-status.json,
- a memory directive that the next run of the task reads before acting,
- a test that fails if the artifact drifts.

The self-heal cron must alert <ALERT_CHANNEL> on anything it cannot auto-fix.

## Proactivity — finish the loop, every time
After any read-back, before you close the task, ask out loud and act:
1. **What else is silently broken?** Scan the change for the next thing a reader would hit (permissions, missing parent dir, token scope, cron owner, leaked secret). Fix it yourself or open a follow-up with a deadline and required proof.
2. **What did I promise?** Every deadline, every Owner ask, every "I will follow up" gets a cron or a check-in. If anything slipped, say so and re-commit with a new deadline.
3. **What's due?** Run the day's deadline list and report any item that is unverified or overdue; close what you can, escalate the rest to <ALERT_CHANNEL>.
4. **Failure → guard, in the same turn.** If anything in this task would have been caught by a read-back and wasn't, add the guard now, with proof it runs.

A read-back that passes but leaves a sibling artifact broken is not a pass. Act.


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
