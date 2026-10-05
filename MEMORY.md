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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-04`, `SEMULITH-AC-0058`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (5/10 — the profile resolved as `rv64gc-lab-v0` (`.1`), the privileged machinery landed and flipped (`.2`), Sv39 translation and protection CLOSED (`.3`), atomics and reservations CLOSED (`.4`), and interrupts, counters and wait CLOSED (`.5`): the declared virtual-time domain, the step-head pending evaluation with both vector modes, the halted state with WFI's real wake — the timer wake WITHOUT CPU RETIREMENT evidenced by w-timer's own run; the Sail attempt 6 AGREE + 6 named of 12).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.6` — instruction visibility and fence semantics, slice (c):
  the Sail matched experiment (the fencei guests AGREE by design — Sail's FENCEI is
  "a nop for the memory model" too) + the fetch-cache census re-answer (decision 6)
  + the reports and the book + the leaf acceptance. Slice (b) landed `2026-10-05`
  (`SEMULITH-P4-0036`): THE BIND — the unit composes riscv/zifencei (slot→extension,
  the census 87→88), fence.i legal over the existing Sem::Nop, REQ-GC-FENCEI +
  OB-GC-FENCEI, the fencei guests re-derived (the slice-(g) pre-commit fulfilled),
  the acceptance pair landed (fencei-selfmod WITH, fault-selfmod WITHOUT), 101/101
  corpus, 98/99 pre-bind guests byte-identical. `P4-SYSTEM.5` closed `2026-10-05`
  (`SEMULITH-P4-0033`): the timer wake WITHOUT CPU RETIREMENT evidenced by
  w-timer's own run; the Sail attempt 6 AGREE + 6 named of 12; DERIVED-COUNTS 430.
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
