# INSTALL.md

## The short version

1. Install the Grok Bot template: **{{COMMANDERS_INTENT_TEMPLATE_LINK}}**
2. Say hello. The bot runs [`FIRST-RUN.md`](FIRST-RUN.md) with you.

## What to have ready

| Item | Needed for | Required? |
|---|---|---|
| A Hindsight Cloud account and one memory bank | Shared fleet memory | Yes |
| A Hindsight API key, added through the bot's secure secret request | Memory access | Yes |
| 20 to 30 minutes for the Commander's Intent interview | The bot writes your intent from your answers before anything else | Yes |
| A Git repo you control for your Commander's Intent (private is fine) | Versioned home for your approved intent | Recommended (until then the bot keeps it in its persistent folder) |
| An alert destination (channel or inbox) | Failures the bot cannot auto-fix | Yes |
| A private network (for example a Tailscale tailnet) | Reaching Hermes hosts | For fleet wiring |
| One or more hosts running Hermes Agent | The fleet the bot runs | For fleet wiring |
| A secrets manager project | Per-host keys, never in files or chat | For fleet wiring |

## What the bot will never ask for

- A secret pasted into chat. Keys go through the secure secret request or stay in your secrets manager.
- Permission to spend, publish, change DNS, touch secrets, or run destructive actions without your explicit yes for that specific action.
- An SSH relay for fleet asks. Hermes is reached over its native HTTP API on :8642 only.
- To let a cloud coding agent push to `main` or merge its own work. Cloud agents open draft PRs; one merge owner you name merges after independent review. See [`SECURITY.md`](SECURITY.md).

## Time

- About 20 to 30 minutes: the Commander's Intent interview, playback, and your approval.
- About 10 more minutes: memory connected, alignment confirmed, security gates reviewed, setup questions, skills installed, routines created.
- Longer, guided: wiring each Hermes host and running the computer-update survival drill.

## Start here

Read [`COMMANDERS-INTENT.md`](COMMANDERS-INTENT.md) to see what the interview fills in, and [`SECURITY.md`](SECURITY.md) for the gates the bot keeps.

## Manual install

Everything the bot does is written down. [`SETUP.md`](SETUP.md) is the full manual reference; [`FIRST-RUN.md`](FIRST-RUN.md) is the ordered script.

## Updating

The bot checks [`CHANGELOG.md`](CHANGELOG.md) at session start and proposes updates. See [`FABRIC.md`](FABRIC.md).
