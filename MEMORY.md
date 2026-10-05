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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-04`, `SEMULITH-AC-0058`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (4/10 — the profile resolved as `rv64gc-lab-v0` (`.1`), the privileged machinery landed and flipped (`.2`), Sv39 translation and protection CLOSED (`.3`), and atomics and reservations CLOSED (`.4`): the unit composes `riscv/a` (87 forms), the 12-guest atomics corpus green, the Sail matched experiment 11 AGREE + 1 NAMED DIVERGENCE of 12 (the width-equal SC policy vs Sail's address-only reservation, both legal); the experiment caught and fixed at root the bind-day misaligned policy — LR takes the LOAD access-fault 5, never 7).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.6` — instruction visibility and fence semantics, the
  DESIGN BRIEF first (the cadence: brief before execution). `P4-SYSTEM.5` closed
  `2026-10-05` (`SEMULITH-P4-0033`): the timer wake WITHOUT CPU RETIREMENT
  evidenced by w-timer's own run (two `<halted>` steps + the delivery with no
  observation, rdinstret=11 at the handler, mcause=int|5, mepc=wfi+4); the Sail
  matched attempt 6 AGREE + 6 named platform-shaped of 12 (probe-tw's TW gap
  fresh: DIVERGE matched, AGREE 30/30 under the wfi-wait variant); 99/99 corpus,
  DERIVED-COUNTS 430.
  `P4-SYSTEM.4` closed `2026-10-05` with `SEMULITH-P4-0028` (DERIVED-COUNTS 429).
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
