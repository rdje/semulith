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
- next_action: `P4-SYSTEM.7` slice (d2) — the language for D: the ONE new operator `f2f`
  (the format conversion FCVT.S.D/FCVT.D.S — schema, check_semantics, the lowering, a `Sem`
  variant), `d.sem.sexp` (32 rules over the width-generic FP vocabulary), the gated
  lowering + the assembler's derived register files on a staged composition. Then (d3)
  fp.rs's conversions (deviation (ii) patched) + specfp + FP-VECTORS, (d4) the staged D
  corpus, (d5) THE BIND (118 → 150). The (d) split is the tree's `2026-10-06` decision.
  (d1) landed (`-0049`): rv_d/rv64_d pinned, `definitions/riscv/d.sexp` (requires f).
  ⚠ The live P4 tree is at ~125 KiB: archive the closed (b)–(c4) checklists first.
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
