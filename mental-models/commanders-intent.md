# Mental model: `commanders-intent`

A Hindsight mental model that turns the Owner's approved [`COMMANDERS-INTENT.md`](../COMMANDERS-INTENT.md) into a fast, shared memory every agent can read. The file stays the authority; the model is a derived view. On any mismatch, the file wins and the model is refreshed.

- **Model id:** `commanders-intent` (stable across the whole fleet)
- **Bank:** the one fleet bank, from the `HINDSIGHT_BANK` environment variable (`<MEMORY_BANK_ID>`)
- **Source:** the Owner-approved `COMMANDERS-INTENT.md`, retained section by section with version tags
- **Create body:** [`commanders-intent.json`](commanders-intent.json)
- **Helper:** `tools/hindsight/hs.py` (standard library only; key from `HINDSIGHT_API_KEY`, never echoed)

## Why a mental model

Mental models sit at the top of Hindsight's memory hierarchy. Reading one is a cached lookup with no model call. On every Reflect, Hindsight injects matching mental models as high-priority context, so an agent asking "should I do X?" sees the intent first. [VERIFIED: Hindsight mental models documentation, docs.hindsight.vectorize.io/mental-models, read 2026-09-28]

## How the model is scoped to the approved version

The model's tags are `commanders-intent` plus a version tag (`ci-v1-0` for v1.0). When a model has tags and no `tags_match` override, Hindsight refreshes it with `all_strict` matching: a memory must carry every one of the model's tags, and untagged memories are excluded. [VERIFIED: Hindsight OpenAPI schema `MentalModelTrigger`, read 2026-09-28] So only the sections retained for the current version feed the model. Old versions stay in the bank as history but cannot leak into the current model.

Version tag rule: `ci-v<MAJOR>-<MINOR>`, for example `ci-v1-0`, `ci-v1-1`, `ci-v2-0`.

## Refresh triggers

1. **Every intent version bump** (manual refresh, part of the amend flow). This is the one that matters.
2. **Weekly** via `trigger.refresh_cron` `0 13 * * 1` (Mondays 13:00 UTC). `refresh_cron` and `refresh_after_consolidation` are mutually exclusive; the weekly cron is chosen because the intent is stable and should only change on purpose. [VERIFIED: Hindsight OpenAPI schema, read 2026-09-28]
3. **On drift:** if an agent's wake line checksum does not match the model's recorded checksum, the Chief of Staff refreshes and re-checks.

Only the Chief of Staff (or the Owner) creates, patches, or refreshes this model. Every agent may read it.

## Commands

Set once per shell (the key comes from the secrets manager or the platform's secure secret request; never paste it):

```bash
export HINDSIGHT_BANK=<MEMORY_BANK_ID>
HS=/home/box/agent-data/tools/hindsight/hs.py
INTENT=/home/box/agent-data/commanders-intent/COMMANDERS-INTENT.md
V=v1-0   # version tag suffix for the approved version
```

**1. Retain the approved intent, one section per item** (so recall and the model see each section clearly). Split the file on `## ` headings; for each section number `NN` and its text:

```bash
python3 "$HS" retain "<section NN text>" \
  --context "Commander's Intent $V approved by the Owner on <date>, checksum <checksum12>, section NN" \
  --tags commanders-intent,ci-$V --doc commanders-intent-$V-sNN --by "<COS_NAME>"
```

Also retain one header fact: `"Commander's Intent current version is v1.0, checksum <checksum12>, canonical copy at <location>, approved <date>."` with the same tags.

Retaining again with the same `--doc` id replaces that document (Hindsight's default `update_mode` is `replace`). [VERIFIED: Hindsight OpenAPI schema `MemoryItem`, read 2026-09-28] Poll async retains with `python3 "$HS" op <operation_id>`.

**2. Create the model** (first time only; check `python3 "$HS" mm list` first and skip if `commanders-intent` exists):

```bash
python3 "$HS" mm create mental-models/commanders-intent.json
python3 "$HS" op <operation_id>
python3 "$HS" mm get commanders-intent
```

**3. On a version bump** (for example v1.0 to v1.1): retain the new sections with `ci-v1-1`, point the model at the new tag, then refresh:

```bash
echo '{"tags":["commanders-intent","ci-v1-1"]}' > /tmp/ci-tags.json
python3 "$HS" mm patch commanders-intent /tmp/ci-tags.json
python3 "$HS" mm refresh commanders-intent     # patch alone does not regenerate content
python3 "$HS" op <operation_id>
python3 "$HS" mm get commanders-intent
```

**4. Verify.** The model content must name the current version and checksum, contain no `{{...}}` slots, contain no secrets, and match the file section by section. Record the check, then send the fleet the new wake line.

For create, patch, refresh, dry-run, and clear against the raw REST API, see the `hindsight-mental-models` skill. The `mm create`, `mm patch`, and `mm refresh` subcommands were added to `hs.py` in v0.2.0 and follow the same REST paths; they have been checked against the published API schema but not yet run against a live bank from this repo. [INFERRED: first live run is the installer's step 2 proof]

## How agents use it before acting

Before any gated action, multi-step task, or change of plan, an agent:

1. Reads the model: `python3 "$HS" mm get commanders-intent` (fast, cached), or asks a doctrine question with `python3 "$HS" reflect "Does <planned action> serve the current Commander's Intent and stay inside its hard lines?"` (the model is injected automatically).
2. Compares the version and checksum in the model with its own wake line. Mismatch: halt, report `BLOCKED stale intent`, and wait for the Chief of Staff to refresh.
3. Checks the planned action against purpose, end state, hard lines, and its order's intent two levels up. If it does not serve them, it adapts within intent or escalates with the six-part ask (see `COMMANDERS-INTENT.md` section 12).

If Hindsight is unreachable, the agent reads the canonical file directly, says so, and reports `BLOCKED: memory` to the Chief of Staff. It never saves the intent to another memory store instead.

## Failure modes and guards

- **Model built from a draft, not the approved text.** Guard: retain only after the Owner's explicit approval; the context line records the approval date.
- **Old version bleeding into the model.** Guard: version tag plus `all_strict` scoping; verify the version line after each refresh.
- **Patch without refresh.** Guard: the amend flow always runs `mm refresh` after `mm patch`.
- **Secret in a retained section.** Guard: scan each section for key-shaped strings before retaining; a hit stops the retain and follows the incident runbook in `SECURITY.md`.
