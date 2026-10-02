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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-02`) · `MCU-DOCS` (idle — 12 requests filed, awaiting the channel) · `P5-BOARD` (4/11 — the three units registered; both device dossiers gated).
  Milestone frontier: `P5-BOARD`. (`BOOK-APPARATUS` closed `2026-10-02`, 2/2.)
- next_action: `P5-BOARD.3` — generated maps and the hardware description from the
  canonical board definition (`profiles/netboard-lab-v0/board.sexp`): address maps and
  wiring generated, no handwritten duplicate map anywhere, drift gated (OWN-05). The
  composition verdict (`.4`) follows — the devices' composition records
  (`REQ-D-NIC-TIME-SOURCES`, `REQ-D-NIC-PHY-LINK`, the strap values) are pre-wired to it.
  All five units are registered (`materials/units.sexp`) with books that build.
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
