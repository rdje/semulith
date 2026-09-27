# DOC-SHARDING: shard the append-history surfaces when their ceilings fire

## Metadata

- Tree ID: `DOC-SHARDING`
- Status: `proposed`
- Roadmap lane: repository hygiene — the append-history ceilings (`doctrine/readme_routes.tsv`)
- Gate: none of its own; keeps `README-ROUTING-CLOSURE` green by giving the fired trigger its
  owner
- Consumed by: the commit workflow — every slice adds a `CHANGELOG.md` entry, so the surface
  fires again the moment the head has no room; must be consumed before the next slice lands
- Depends on: the fired trigger, measured `2026-09-27`: `CHANGELOG.md` at 65,527 of 65,536
  bytes (headroom 9 bytes) after `SEMILITH-RM-0060` compressed its entry to fit; `ROADMAP.md`
  at 24,522 of 24,576 after the same unit. The debt was recorded at adoption
  (`README_POLICY.md`): the ceilings "are the trigger that opens the leaf which builds it"
- Unlocks: unconstrained changelog entries again; the same tool later serves `DEV_NOTES.md`
  (48 KiB ceiling, ~37 KiB today, no headroom pressure yet)
- Created: `2026-09-27`
- Owner: repo-local workflow

## Goal

Build the sharding tool the adoption debt promised: when an `append_history` surface hits its
byte ceiling, its oldest entries move to frozen shards under a new repository-relative
directory, the head stays a readable recent-history surface under its ceiling, and a tracked
check proves the shards are frozen (a manifest of hashes; old rows never change) and the
partition is complete (no lost or duplicated entries). The trigger fired; this tree owns the
remedy.

## Non-Goals

- **Not a ceiling raise.** The registry raises a ceiling only on a reviewed contract
  expansion; sharding is the declared alternative.
- **Not rewriting history.** Committed entries move verbatim — bytes identical, git history
  unchanged; the manifest is the freeze proof going forward.
- **Not generalising beyond the append-history class.** Only `author_overflow`/`append_history`
  surfaces (`CHANGELOG.md` today, `DEV_NOTES.md` when it fires) are in scope.

## Acceptance Criteria

1. `scripts/shard_history.py` moves the oldest `CHANGELOG.md` entries into
   `docs/changelog/shard-NNNN.md` (bytes verbatim), rewrites the head under its ceiling, and
   updates `docs/changelog/SHARDS.sha256` — deterministic, re-running is a no-op.
2. A tracked check (with `--self-test`, fired RED before registration) proves: every shard
   hashes to its manifest row, manifest rows are append-only, and head + shards contain
   exactly the entries the head had before sharding — none lost, none duplicated.
3. `docs/changelog/` is registered in `doctrine/readme_routes.tsv` in the same commit that
   creates it, with the class and bounds its lifecycle demands.
4. Live docs (`MEMORY.md`, this tree, `README_POLICY.md`'s transition-debt note) updated in
   the same commit.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `DOC-SHARDING.1` | `pending` | CHANGELOG has 9 bytes of headroom — the next slice cannot land an entry without this tool |

## Task Tree

- ID: `DOC-SHARDING`
  Status: `active`
  Goal: the fired ceiling trigger gets its remedy — frozen shards, a manifest, a check
  Children: `DOC-SHARDING.1`

- ID: `DOC-SHARDING.1` — **the shard tool, the manifest, and the freeze check**
  Status: `pending`
  Goal: `scripts/shard_history.py` + `docs/changelog/` + a tracked freeze/completeness check,
    demonstrated against the real `CHANGELOG.md` (which shards the moment this lands)
  Acceptance: as the tree's Acceptance Criteria 1–4; the check's RED arms fired before
    registration; after sharding, the head is under 65,536 bytes and every pre-shard entry
    is findable in exactly one place.
  Verification: `pending`
  Commit: `pending`
