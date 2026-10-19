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
- active_work_unit: `P4-SYSTEM.14` → final execution/manifest composition.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: after LC0049 normal COMMIT/brief0/exact postconditions/host census,
  return to P4-SYSTEM.14 final execution/manifest/planned record/input-author-impact,
  then capture/full policy. Read that leaf's current frontier and affected contracts.
  Do not add another prerequisite-only review loop without a concrete delivery need.
- LC0049: director2026-10-19 directly approved the verified158-shard migration,
  exact finite archive bound and local commit without push after two automatic
  review refusals. See LIVE-CONTAINMENT.4 .4j; target/live-containment/history-rollover.
- blockers: LC0049 approval resolved; normal commit/handoff checks still required.
  LIVE-CONTAINMENT.4 owns captured D79 analysis and D80, scheduled separately.
  No push below300commits without the director's act (COMMIT.md).
