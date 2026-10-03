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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-02`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (2/10 — the profile resolved as `rv64gc-lab-v0` (`.1`) and the privileged machinery landed and flipped (`.2`); `.3` underway: slice (a) landed — the profile adds **Svade** (OQ-2 closed with the three evidence legs; the ISA string is `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade`), the Sail override flips to match with every verdict measured unchanged (11/12 AGREE), and gen_state's validate_gc refusal closed).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.3` slice (b) — the translation module + the three hooks
  (fetch/load/store) + effective mode + the Bare-identity proof (the 62-guest corpus
  unchanged — satp resets to Bare, an EXACT identity path, measured). Then (c) the
  walk with its fault matrix, (d) the TLB + real sfence.vma, (e) MPRV/SUM/MXR +
  the sv39 guests + the Sail experiment. Routed INTO `.5` from `.2`'s Sail attempt:
  Sail 0.14 does not implement mstatus.TW's effect on WFI legality (the measurement
  is in the `.2` slice-(h) part-2 checklist). Slice (a) landed `SEMULITH-P4-0015`
  (DERIVED-COUNTS 422).
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
