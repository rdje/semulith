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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-04`, `SEMULITH-AC-0058`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (6/10 — the profile resolved as `rv64gc-lab-v0` (`.1`), the privileged machinery landed (`.2`), and four leaves CLOSED: Sv39 (`.3`), atomics (`.4`), interrupts/counters/wait with the timer wake WITHOUT CPU RETIREMENT (`.5`), instruction visibility with the fence.i contract validated on both engines (`.6`, 6 AGREE of 6)).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.7` — floating-point backend qualification: slice (b) —
  the FP state (the f-file + FS gating + the fcsr fix + fflags/frm semantics +
  the census re-answer) with the FS=Off corpus. Slice (a) landed `2026-10-06`
  (`SEMULITH-P4-0039`): **rustc_apfloat QUALIFIED** — the arithmetic core
  MPFR-exact over 63,752 probe cases (zero core disagreements; 612 value + 386
  flag disagreements all named policy surfaces or the two LLVM-vs-IEEE
  deviations); softfloat disqualified on capability (five §6 gaps) though
  MPFR-exact where it exists; the dependency pinned (`=0.2.3+llvm-462a31f5a5ab`)
  and wasm-proven; the decision record + the PROMOTED knowledge card landed;
  DERIVED-COUNTS 430. Then (c) the F bind (30 forms), (d) the D bind (32 forms +
  NaN-boxing), (e) the independent fixtures at scale + the Sail encoding/state
  match + the acceptance. `P4-SYSTEM.6` closed `2026-10-05` (`SEMULITH-P4-0037`;
  DERIVED-COUNTS 430).
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
