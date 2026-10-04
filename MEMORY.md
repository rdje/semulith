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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-04`, `SEMULITH-AC-0058`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (3/10 — the profile resolved as `rv64gc-lab-v0` (`.1`), the privileged machinery landed and flipped (`.2`), and Sv39 translation and protection CLOSED (`.3`): the 14-guest sv39 corpus green with EVD-05 spec-side expectations and the Sail matched experiment on three explicit dimensions — 13 AGREE + 1 AGREE-RECORDED of 14 (the A/D-placement convention), the tracked override's medeleg mask widened to 0xB3FF, verdict-neutral on the mm corpus).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.4` — atomics and reservations: **record the design brief
  first** (the `.2`/`.3` cadence: two censuses — the C16/A-extension scope against the
  pinned `a-st-ext`/`rvwmo` chapters, and the machinery deltas — then the brief commit;
  the `.4` brief was queued `2026-10-04` and deferred, nothing in flight). The leaf:
  atomic widths, reservation semantics, failed conditional stores, overlap and
  external-write cases (catalog `C16`, `docs/CPU_ENVIRONMENT.md` §2); single-core
  reservation behaviour validated here, multicore stays `MC-MULTICORE`. `P4-SYSTEM.3`
  closed `2026-10-04` with `SEMULITH-P4-0020` (DERIVED-COUNTS 424).
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
