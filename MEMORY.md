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
- active_work_unit: `P4-SYSTEM.14` → exact native DIV predeclarations.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: after P4-0279 normal COMMIT/brief0/exact postconditions/host census,
  curate/commit the composed command's three exact native declarations before
  three fresh canonical Sail processes/full policy. Source command has17 controls
  x2/seven omissions and84-file synthetic/offline controls; no canonical output.
  Read the active leaf and capture-plan/prepared-inputs before declarations.
- in_flight_uncommitted: verify Git state on read;0279 owns any unfinished workflow.
- blockers: none requiring director input. LC0049 migration directly approved
  and committed095f3ceb; host census/brief0/clean verified before this task.
  D79/D80 remain scheduled separately in LIVE-CONTAINMENT.4; runtime P2 in P4 a42ab.
  No push below300commits without the director's act (COMMIT.md).
