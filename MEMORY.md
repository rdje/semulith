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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-04`, `SEMULITH-AC-0058`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (2/10 — the profile resolved as `rv64gc-lab-v0` (`.1`) and the privileged machinery landed and flipped (`.2`); `.3` underway: slices (a)–(d) landed and slice (e) part 1 — the 14-guest sv39 corpus is green with EVD-05 spec-side expectations (every walk fault cause, the permission matrix, Svade's no-update, MPRV, the TLB's fence semantics, the straddle, delegation), Bare byte-exact).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.3` slice (e) part 2 — the Sail matched experiment
  (the PTW/TLB traces explicit via `--trace-ptw`/`--trace-tlb`, excluded from
  `--trace`) against the Svade-flipped tracked override, `compare_sail.py`
  extended — AGREE/divergence per guest recorded honestly (TLB-size/timing
  differences are RECORDED differences, never normalized) — then the leaf's
  acceptance and closure (`SEMULITH-P4-0020`; frontier → `.4` atomics and
  reservations, LIVE_STATUS 3/10). Slice (e) part 1 landed `SEMULITH-P4-0019`
  (DERIVED-COUNTS 424).
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
