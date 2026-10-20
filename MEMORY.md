# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (`MEMORY_ARCHITECTURE.md` §6). OVERWRITE "Current state"
> each update — never append. This file exists **solely to point at the next action** (director
> ruling `2026-10-02`, `decision_memory-next-action-pointer`); everything durable lives in the
> layers it points to.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active tree below → its Current Frontier → the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- latest_commit: derive on read with `git log -1 --format='%H %s'`.
- active_work_unit: `ARTIFACT-CLEANUP` → `.21`, successful build capture/publication.
- last_unit: `ARTIFACT-CLEANUP.20` / `SEMULITH-AC-0074`, explicit Cargo command boundary.
- next_action: bind anchored before/after facts and complete recorder/helper/producer
  source identities to successful real public builds; publish bounded merged ledgers
  atomically, preserving unknown/unchanged inputs and existing output paths. Then .17
  strict current-plan selection, .16 journal/core and .14 host CLI before P4 policy/status.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none requiring director input. P1 remains open until .17 is verified;
  no supported mutation API or new cleanup event. Historical plans/evidence unchanged.
- evidence: `target/artifact-cleanup-0074`; bound commands/actual engine18 and guest2
  pass. Seventeen fixture tests normal/O and eight omissions per mode discriminate;
  cold copied Cargo preserves an unchanged cache-shaped input. No output authority
  is published by this slice. Source/manifest checks and bounded process-group join
  are command observations, not loaded-code/race attestation.
- continuity: AC0073 retained ledger/source and all completed live history stay exact.
  Read `docs/artifact-cleanup-history/README.md` for both Markdown products. Current
  cleanup is derived from `docs/ARTIFACT_CLEANUP.md`; original37/native3/capture exact.
  CPU14/18, BOARD10/12, replay4/4green; full qualification remains pending.
  Use target/tmp as TMPDIR; push cadence derives with `scripts/check_push_cadence.sh --status`.
