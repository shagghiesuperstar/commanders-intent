# INSTALL.md

## The short version

1. Install the Grok Bot template: **{{COMMANDERS_INTENT_TEMPLATE_LINK}}**
2. Say hello. The bot runs [`FIRST-RUN.md`](FIRST-RUN.md) with you.

## What to have ready

| Item | Needed for | Required? |
|---|---|---|
| A Hindsight Cloud account and one memory bank | Shared fleet memory | Yes |
| A Hindsight API key, added through the bot's secure secret request | Memory access | Yes |
| A Git repo you control for Commander's Intent (private is fine) | Source of truth for the doctrine | Yes |
| An alert destination (channel or inbox) | Failures the bot cannot auto-fix | Yes |
| A private network (for example a Tailscale tailnet) | Reaching Hermes hosts | For fleet wiring |
| One or more hosts running Hermes Agent | The fleet the bot runs | For fleet wiring |
| A secrets manager project | Per-host keys, never in files or chat | For fleet wiring |

## What the bot will never ask for

- A secret pasted into chat. Keys go through the secure secret request or stay in your secrets manager.
- Permission to spend, publish, change DNS, touch secrets, or run destructive actions without your explicit yes for that specific action.
- An SSH relay for fleet asks. Hermes is reached over its native HTTP API on :8642 only.

## Time

- About 10 minutes: setup questions, memory connected, skills installed, Commander's Intent drafted, routines created.
- Longer, guided: wiring each Hermes host and running the computer-update survival drill.

## Manual install

Everything the bot does is written down. [`SETUP.md`](SETUP.md) is the full manual reference; [`FIRST-RUN.md`](FIRST-RUN.md) is the ordered script.

## Updating

The bot checks [`CHANGELOG.md`](CHANGELOG.md) at session start and proposes updates. See [`FABRIC.md`](FABRIC.md).
