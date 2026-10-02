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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-02`) · `BOOK-APPARATUS` (1/2 — `.2` the reading-experience audit) · `P5-BOARD` (1/11 — the platform specified).
  Milestone frontier: `P5-BOARD`.
- next_action: `P5-BOARD.2` — the SiFive UART device dossier (`profiles/sifive-uart-lab-v0/`):
  sources, requirements, state, reset, access semantics, side effects, and independently
  sourced expected results, reusing the CPU's dossier machinery (`docs/EVIDENCE_AND_GATES.md`
  §8). Device order decided (`.2` brief, `SEMULITH-P5-0006`): UART first, LAN9118 in `.10`,
  registration day in `.11` (all three units). The platform is specified:
  `profiles/netboard-lab-v0/board.sexp` pins versions, not names. Then: `BOOK-APPARATUS.2`.
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
