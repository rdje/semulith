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
- active_work_unit: `P4-SYSTEM.16` → its Current Frontier.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: after P4-0254 normal COMMIT, take P4-SYSTEM.14 a42g:
  bind declared inputs to a separate caller-reviewed inventory, freeze context,
  reject missing/extra/changed entries and preserve unqualified status.
  Read a42/a42f and the matched-GPR contract/evaluator. Source fixes0192–0197
  are complete. Remaining method work: closure/impact/property/provenance,
  fresh captures/retention and policy/status/mirror derivation; full mutation .15.
  P4.16 is complete, G-REPLAY4/4green, P4 now14/18; CPU incomplete on six axes.
- in_flight_uncommitted: none after P4-0254 normal COMMIT/postcheck.
- blockers: none for implementation; no terminal command needed.
  LIVE-CONTAINMENT.4 owns captured D79 analysis and D80; see that tree's
  Delivery priority and capture handoff. Maintenance remains scheduled separately.
  No push below300commits without the director's act (COMMIT.md).
