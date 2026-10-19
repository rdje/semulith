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
- active_work_unit: `P4-SYSTEM.14` full source/risk/feature policy and status integration.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: after AC0067 normal COMMIT/brief0/exact postconditions/actual host
  census, own the next safe P4 policy/status slice on clean state. Read P4 a42,
  EVIDENCE_POLICY and model method-adequacy chapter. P4-0283 committed59e210a:
  finite method satisfied/full policy pending/replay not checked by the consumer.
  Preserve original37 producer modules/native3/all canonical observations/results;
  never rerun historical names. Review task-family/head capacity before ownership.
- in_flight_uncommitted: derive Git on read; AC0067 owns normal commit workflow
  under target/artifact-cleanup-0067.18 caches removed/78250724B; immediate
  residue0 and18121 retained files exact. No deletion remains to repeat.
- blockers: none requiring director input. CPU14/18,board10/12,replay4/4green;
  D79/D80 remain LIVE-CONTAINMENT.4, runtime P2 in P4 a42ab. No push below300
  without director's act; cadence238 before this cleanup commit. Always derive
  TMPDIR from repository target/tmp. Latest cleanup timestamp is in its record.
