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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-06`, `SEMULITH-AC-0059`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (6/10 — the profile resolved as `rv64gc-lab-v0` (`.1`), the privileged machinery landed (`.2`), and four leaves CLOSED: Sv39 (`.3`), atomics (`.4`), interrupts/counters/wait with the timer wake WITHOUT CPU RETIREMENT (`.5`), instruction visibility with the fence.i contract validated on both engines (`.6`, 6 AGREE of 6)).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.7` slice (c2) — the `rv_f`/`rv64_f` re-pin (fetched
  3,050/320 B: 26 + 4 = 30 forms, 13 pseudo rows) + the `f.sexp` fragment
  owning `rs3`/`rm`, under the bind-gated named exclusion. Slice (c) runs as
  checkpoints (c1)–(c6) — the `2026-10-06` split decision in the tree: (c3) the
  semantics language learns FP (the FS gate judged at the head of any FP-state
  rule; f-register class derived from the semantics for the assembler), (c4)
  `fp.rs` over rustc_apfloat, (c5) the staged corpus, (c6) THE BIND. (c1) landed
  `2026-10-06` (`SEMULITH-P4-0041`): frm holds any 3-bit value (slice b's WARL
  retention contradicted the FSRM sentence — fixed at root); the book's P4
  chapter partitioned per leaf (39 chapters); tree archive part 3 opened. Then
  (d) the D bind, (e) fixtures at scale + the Sail match + the acceptance.
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
