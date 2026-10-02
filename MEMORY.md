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

- latest_commit: `git log -1`. ⛔ **Do not push** below the 300-commit cadence without the
  director's `scripts/approved_push.sh` act (`decision_push-cadence`) —
  `scripts/check_push_cadence.sh --status` says where we stand.
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-02`) · `P5-BOARD` (9/12 — the maps generated and drift-gated; the two-tier bound ruling executed; the composition verdict ACCEPTED and re-decided by BOARD-VERDICT).
  Milestone frontier: `P5-BOARD`. (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P5-BOARD.6` — the platform capability manifest: the read-only derived
  export of the accepted processor/device/board profile and its boot contract, for
  archogen's compatibility checker (`docs/ARCHOGEN_INTEGRATION.md` §3; OWN-06 — derived,
  never handwritten). The composition verdict (`.4`) is landed: ACCEPTED, with the four
  dispositions (straps, frozen time sources, link scene, pin tie-offs) as data in
  board.sexp → hardware.sexp; `.5` (probes) and `.7` (gate report) stay gated on the
  CPU's acceptance trajectory.
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
