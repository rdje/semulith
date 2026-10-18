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
- next_action: P4-SYSTEM.14 collector process/output controls, then bounded
  retention/predeclared captures and complete policy/status/mirrors. P4-0263
  composes the finite signed-DIV property from actual raw context after source
  values/author review.22 controls/14 omissions,80 legacy omissions normal/O;
  scope1514 files/89 old entries,112 old selectors exact. Simulated external-pin
  CI is separate from unmocked23-file cached-page smoke. No capture credit.
  m-div.s step2/x7: signed -7/2→-3 only. Authority fingerprints normalize
  derived outputs; exact artifact/input/impact checks stay unfiltered. Current
  canonical authority, complete input coverage and code identity remain caller
  review obligations. Existing source/image/value/input/impact/author APIs done.
  Full closure/review, collector, captures/retention, policy/status remain;
  qualification closed, CPU14/18 and replay4/4green. No whole-M credit.
- in_flight_uncommitted: none after P4-0263; verify Git state on read.
- blockers: none for implementation; no terminal command needed.
  LIVE-CONTAINMENT.4 owns captured D79 analysis and D80; see that tree's
  Delivery priority and capture handoff. Maintenance remains scheduled separately.
  No push below300commits without the director's act (COMMIT.md).
