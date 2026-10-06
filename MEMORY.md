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
- **Active trees:** `CITATION-ACCURACY` (1/2 — CITATION-QUOTES registered; `.2` the Markdown census, proposed) · `LIVE-CONTAINMENT` (3/4 — the closed-tree register, the orientation sources, TOOLBOX/DOCTRINE_ENFORCEMENT partitioned; `.4` the doctrine adoption, proposed) · `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-06`, `SEMULITH-AC-0059`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (6/10 — the profile resolved as `rv64gc-lab-v0` (`.1`), the privileged machinery landed (`.2`), and four leaves CLOSED: Sv39 (`.3`), atomics (`.4`), interrupts/counters/wait with the timer wake WITHOUT CPU RETIREMENT (`.5`), instruction visibility with the fence.i contract validated on both engines (`.6`, 6 AGREE of 6)).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.7` slice (c5) — the staged F corpus: the evaluator's F arms
  proven on a scratch engine composing `riscv/f` (FReg/Set-to-freg with Dirty, the Off gate
  at the instruction head, Rounding → illegal on reserved rm, the operators through
  `fp.rs` with fflags accrual), and the F guests with EVD-05 expectations authored by the
  spec-side tooling (`scripts/specfp.py` is now tracked — the FP authority). Then (c6)
  THE BIND, (d) D, (e) fixtures + Sail. (c4) landed `2026-10-06` (`-0045`/`-0046`):
  `fp.rs` (OF/UF on the exactly-unbounded value; 176 spec-side vectors; FP-VECTORS), the
  slice-(a) oracle's two rule defects found and the decision record amended, and the
  dependency store on-volume (`.cargo/config.toml` → `.app-data/vendor`, `make vendor`).
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
