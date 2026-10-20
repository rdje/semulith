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
- active_work_unit: `ARTIFACT-CLEANUP` → `.21` (pending; actual capture/publication).
- pnt_status: stopped at the director-requested checkpoint (`2026-10-20`);
  resume work only on a new instruction.
- last_unit: `.22` / `SEMULITH-AC-0075` — versioned support-source records.
- next_action: bind successful actual Cargo builds to anchored before/after facts
  and the complete v2 source tuple, then atomically publish bounded merged ledgers.
  Preserve unchanged unowned inputs and existing output paths. Read the tree's
  `.21` goal before code; `.17` strict selection follows, then `.16` core/`.14` CLI.
- in_flight_uncommitted: none after the normal commit workflow.
- blockers: none requiring director input. Cleanup input-ownership finding P1
  remains open until `.17`; no supported mutation API or new cleanup event.
- evidence: `docs/tasks/ARTIFACT-CLEANUP.md`; diagnostics `target/artifact-cleanup-0075`.
- continuity: historical plans/ledger bytes, immutable task/history terminals and
  the original capture remain preserved. Read the task tree and `LIVE_STATUS.md`
  for canonical progress; return to P4 full policy/status after cleanup readiness.
- environment: use `target/tmp` as TMPDIR. Read cleanup currency from
  `docs/ARTIFACT_CLEANUP.md`; derive push cadence with
  `scripts/check_push_cadence.sh --status`.
