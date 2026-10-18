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
- active_work_unit: `P4-SYSTEM.14` → its Current Frontier.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: P4-SYSTEM.14 receipt writing/unit collection, then complete
  closure/impact/policy binding and bounded retention/predeclared canonical
  captures. P4-0264 implements one fresh bounded process and shared unpinned
  observations;25 controls/18 omissions normal/O, original reader behavior exact.
  Physical path aliases now refuse before cleanup; all output names reserve
  exclusively. Reproduced/fixed case-insensitive input overwrite before signoff.
  Real Sail smoke normal/O:3 fresh PIDs, exit0, AGREE/AGREE/DIVERGE, identical
  2298B traces; step2/x7 -3 vs -4. Optional one-command smoke is reproducible;
  no canonical capture/receipt/qualification. Per-call accounting is not the
  pending shared experiment budget. Property/source/image/value/review/author
  APIs exist; complete closure review, collector unit and policy remain.
  CPU14/18, BOARD10/12, replay4/4green; qualification closed, no whole-M credit.
- in_flight_uncommitted: none after P4-0264; verify Git state on read.
- blockers: none for implementation; no terminal command needed.
  LIVE-CONTAINMENT.4 owns captured D79 analysis and D80; see that tree's
  Delivery priority and capture handoff. Maintenance remains scheduled separately.
  No push below300commits without the director's act (COMMIT.md).
