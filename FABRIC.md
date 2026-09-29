# FABRIC.md

The "fabric" is the set of Grok Bot templates that share one doctrine. Commander's Intent is the command layer; the sister templates cover specific parts of the stack. They are versioned together so a bot installed from any of them follows the same rules.

## The root of the fabric

[`COMMANDERS-INTENT.md`](COMMANDERS-INTENT.md) is the root of the fabric. Every template in the set, and every agent a template installs, answers to the installing Owner's approved Commander's Intent, created by interview from that scaffold. Its fixed doctrine (Parts I and III: the five hard rules, disciplined initiative, drift prevention, chain of command, quota discipline) is shared by every template. Its Part II is each Owner's own. [`SECURITY.md`](SECURITY.md) is part of the intent by reference and applies across the fabric. Everything else (skills, routines, fleet specs, sister templates) sits under those two files.

## How the templates fit together

| Layer | Template | Role in the fabric |
|---|---|---|
| Command | **Commander's Intent** (this repo) | Root doctrine, Chief of Staff persona, proactivity, memory, survival, routines |
| Talk path | **Hermes API Fleet** ([install](https://x.ai/bot/5KLpaL-JIM2q629kbTh5L)) | Grok Bot to Hermes over HTTP :8642 on a private network. The default and only fleet ask path |
| Operations | **Hermes Fleet Ops** ([install](https://x.ai/bot/rzq0UV2MmBsvVR1EspZE-)) | Multi-host ops desk and secrets playbook |
| Automation | **n8n Master** ([install](https://x.ai/bot/Zvqbrq6yN68ijhEpRz0lU), [repo](https://github.com/shagghiesuperstar/n8n-master-grok-bot)) | n8n control plane from Grok |
| Legacy | **Hermes SSH Relay** ([install](https://x.ai/bot/NVF3Rx9T7jkQPsqYjeDn-)) | SSH bridge for a single desktop host without an API gateway. Not used for fleet asks or identity bots |

Shared across all of them:

- The Owner's approved `COMMANDERS-INTENT.md` as the root document, created by interview, versioned, and mirrored into the `commanders-intent` mental model.
- The five hard rules and the 11 standing rules (see `README.md`).
- The security gates and cloud coding agent rules in `SECURITY.md`.
- One Hindsight memory bank per fleet; Git is the source of truth.
- HTTP :8642 is the only fleet talk path to Hermes.
- Computer-update survival for anything installed on the Grok Bot computer.
- No secrets in templates, chat, memory, or Git.

## Versioning

- **Fabric version** = the version at the top of this repo's `CHANGELOG.md`.
- **Major** (1.0.0): a rule is added, removed, or changes meaning. Every sister template must be updated.
- **Intent versions are separate.** The template version (this changelog) versions the scaffold and fixed doctrine. Each Owner's own intent has its own version (`v1.0`, `v1.1`, ...) and only that Owner amends it (see `COMMANDERS-INTENT.md` section 20).
- **Minor** (0.2.0): new skill, routine, or capability. Update sister templates that reference it.
- **Patch** (0.1.1): wording, fixes, and clarifications. Sister templates update only if they carry the changed text.

## Update-in-unison process

1. **Change here first.** Open a PR against this repo with the smallest change. Label claims. Run the leak scan below.
2. **Bump the version** in `CHANGELOG.md` with Added / Changed / Fixed entries and the date.
3. **Update the sister templates** that carry the changed doctrine. Each template's memory names the fabric version it follows. Re-share each updated template and note it in the changelog entry.
4. **Regenerate `MANIFEST.md`** (every file, purpose, byte size).
5. **Write the release article** at `social/x-article-vX.Y.md`: top changes, plain benefits, links. No invented metrics.
6. **Read back:** fetch README and CHANGELOG raw from `main`, confirm the version, and confirm each sister template shows the update.
7. **Installed bots pick it up:** at session start they read `CHANGELOG.md`, summarize changes for their Owner, and apply them after a yes.

## Leak scan (run before every push)

Every file, every release. Zero hits outside the allowlist, or no push.

- IPv4 addresses (loopback `127.0.0.1` and bind-all `0.0.0.0` are the only allowed values), private-network ranges, mDNS (dot-local) names
- Hostnames or machine names from your own fleet
- Home-directory paths containing a username
- Anything shaped like a key or token (known provider key prefixes followed by characters, long random strings)
- Email addresses, personal names, business names, store domains
- Secrets-manager item names or project names from your own setup

Use `<PLACEHOLDER>` tokens in every example.
