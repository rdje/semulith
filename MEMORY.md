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
- next_action: P4-SYSTEM.14 optional authenticated author composition.
  P4-0260 adds pure reviewed-author binding;21 controls/16 omissions normal/O.
  Freeze full reviewed inventory before reads; bind selected leaf, digest-version,
  consumed source/manifest and snapshot path/route/source/budget metadata.
  Matched remains metadata only, with no execution attestation or qualification.
  Integrate through retained evaluator next, then source-grounded property meaning.
  Source/image, input/impact and snapshot/value APIs are implemented; do not repeat.
  Full canonical closure/review, property/collector adequacy, captures/retention
  and policy/status remain. Qualification closed; P4 14/18; replay4/4green.
- in_flight_uncommitted: none after P4-0260 normal COMMIT and postconditions.
- blockers: none for implementation; no terminal command needed.
  LIVE-CONTAINMENT.4 owns captured D79 analysis and D80; see that tree's
  Delivery priority and capture handoff. Maintenance remains scheduled separately.
  No push below300commits without the director's act (COMMIT.md).
