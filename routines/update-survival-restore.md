# Routine: update-survival-restore

**Cron:** `17 * * * *` (hourly, every day; never weekday-only, because computer updates also happen on weekends). Timezone `<TIMEZONE>`.

## Why
The Grok Bot computer can be updated at any time without the operator doing it. An update wipes installed software, running processes, and everything outside /home/box. Keep all state, keys, configs and restore scripts under /home/box, give anything installed an automatic hourly self-restore, and never call a setup done until it's proven to survive an update.

## Prompt (paste as the routine body)
Check whether this Grok Bot computer was updated or reset. For every tool you depend on (the private-net client first), run its detect script under /home/box (for example `/home/box/agent-data/infra/scripts/detect-fresh-box.sh`). If detect says a restore is needed, run the matching idempotent restore script, then re-verify with a live check (the node is Running, keeps its expected identity and IP, and a known fleet host answers). Stay silent when everything is healthy. Report RESTORED (with what came back) or BLOCKED (with the reason, such as a missing injected secret or a needed signature) to <ALERT_CHANNEL>. Never echo secrets. If a new tool is found without a restore script, treat it as a failure and turn it into a permanent guard with the `grok-bot-computer-update-survival-tailscale` skill.

## Proof before enabling
Run the drill in `skills/grok-bot-computer-update-survival-tailscale/SKILL.md` once. The setup is not done until it passes.
