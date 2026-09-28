---
name: Grok Bot computer update survival (Tailscale)
description: >-
  Use this when setting up Tailscale (or any installed tool, daemon, or key) on
  the Grok Bot computer, when the computer may have been updated or reset, or
  when the bot can't reach tailnet hosts. It makes the setup survive a Computer
  Update and restore itself with no human step.
---
# Grok Bot computer update survival (Tailscale)

## Why
The Grok Bot computer can be moved to a fresh instance (a Computer Update) at any time, including without the operator doing it. When that happens:

| Wiped | Survives |
|---|---|
| Installed software (apt, npm, pip, CLIs) | Everything under `/home/box` |
| Running processes and daemons | Injected secrets (environment variables) |
| `/var/lib`, `/etc`, `/tmp`, `/var/run` | Server-side routines and skills |

Tailscale's default state lives in `/var/lib/tailscale`. That means a stock install loses its node identity on every update and needs a new login, a new approval, and a new Tailnet Lock signature. It also usually gets a new IP.

**Rule:** never leave state, keys, configs, or scripts outside `/home/box`. Anything installed needs a restore script under `/home/box`, plus an automatic check that runs the script.

## One-time setup
1. Pick a persistent folder, for example `/home/box/agent-data/infra/`, containing `scripts/` and `tailscale-state/`.
2. In the Tailscale admin console, mint a **reusable, tagged** auth key (for example `tag:bot-controller`).
   - Tagged nodes have no key expiry.
   - If Tailnet Lock is on, pre-sign the key, or sign the node once from a signing node. Never put Lock signing keys on the Grok Bot computer.
3. Store the key as an injected secret named `TAILSCALE_AUTHKEY_SIGNED`, through the secure secret request. Never paste it into chat.
4. Start `tailscaled` with its state in the persistent folder:
   `sudo tailscaled --state=$DIR/tailscale-state/tailscaled.state --statedir=$DIR/tailscale-state --socket=/var/run/tailscale/tailscaled.sock &`
   - Add `--tun=userspace-networking` if `/dev/net/tun` is missing.
   - Then run `tailscale up --auth-key=$TAILSCALE_AUTHKEY_SIGNED --advertise-tags=tag:bot-controller --hostname=<name>`.
   - If the node was already up with state elsewhere, stop it, copy that state into the folder, and restart with the flags above so it keeps the same IP.
5. Save `scripts/restore-tailscale.sh`, which must be idempotent and never echo secrets:
   - Install Tailscale if it's missing (`curl -fsSL https://tailscale.com/install.sh | sudo bash`).
   - Start `tailscaled` with the persistent state if it isn't running.
   - Fast path: if BackendState is `Running` and the node isn't locked out, exit 0. The identity is kept.
   - Otherwise, check that `TAILSCALE_AUTHKEY_SIGNED` is present and starts with `tskey-auth-`. If not, exit 10 (`NEED_SECRET`). If it's valid, run `tailscale up` with it.
   - If `tailscale status` says locked out, exit 20 (`NEED_LOCK_SIGNATURE`).
6. Save `scripts/detect-fresh-box.sh`. It exits 0 when a restore is needed: the binary is missing, `tailscaled` isn't running, or the backend isn't Running or is locked out.
7. Create an **hourly, every-day** routine. It runs detect. If a restore is needed, it runs restore and re-verifies. It stays silent when healthy. It tells the operator RESTORED (with the IP) or BLOCKED (`NEED_SECRET` means a secure secret request, `NEED_LOCK_SIGNATURE` means ask a signing node). Don't use weekday-only schedules, because updates happen on weekends too.

## Prove it (drill)
Run this once after setup, and again after changes, at a quiet time:
1. Record `tailscale ip -4`.
2. `sudo pkill -x tailscaled && sudo apt-get remove -y tailscale`. This simulates an update.
3. Run detect (expect exit 0), then restore (expect exit 0).
4. **Pass** means the IP matches the one from step 1, `tailscale lock status` shows the node signed, and a known tailnet host answers.
5. Keep a fallback in the drill (reinstall and start the daemon by hand) so a failed drill never leaves the bot offline.

## Recovery guidance for users
- Recover a wedged computer with **Update Grok Bot's Computer**. It keeps files and logins.
- Avoid **Reset** unless there's no other option. It restores an older snapshot and can lose recent state.

## Checklist before calling any setup on the Grok Bot computer done
- Is every file it needs under `/home/box`?
- Does something automatic reinstall or restart it after an update?
- Has the drill passed?
- If any answer is no, say so plainly instead of calling it done.
