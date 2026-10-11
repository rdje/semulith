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
- **Active trees:** `CITATION-ACCURACY` (1/2 — CITATION-QUOTES registered; `.2` the Markdown census, proposed) · `LIVE-CONTAINMENT` (3/4 — the closed-tree register, the orientation sources, TOOLBOX/DOCTRINE_ENFORCEMENT partitioned; `.4` active: finite archive sealed; full inventory/adoption remains) · `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-10`, `SEMULITH-AC-0062`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (13/18 — `.1`–`.13` closed; CPU-SYSTEM `incomplete`, 7/10 axes open; `.14` evidence active).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: P4-SYSTEM.14 full CI on clean d3b composition milestone,
  after COMMIT postconditions. Further finite closure/impact/source-grounded
  property/collector provenance and full policy remain; no qualification credit.
- in_flight_uncommitted: d3b completed/verified; final COMMIT postconditions
  before CI.26/14 and old42/29+23/seven all outcomes/counts exact normal/O;
  source/API/order/probe/checker/method/three-book/task inverses pass. PROFILE454,
  GUEST328/global1401 derived; focused17/sharder12/seven books/3186 links/all17
  examples/normal+print green.340 raw/243 maps,102 entries/1349 other files/
  modes/Gitlinks and216 ELF/167 GC exact; whole DEV0263/CH0264, actual receipt+
  digest rewrites refuse. CPU/canonical/caps/seals unchanged.
  Latest full CI clean93525ac all5 legs green:443 Rust/smoke53/seven books,
  18 sources unchanged; target/p4-system-14/a42b/full-ci/result.json.
  No canonical matched-v1 capture/qualification. D44/D45 repaired; no open defect.
- blockers: none. Archive seal LC0006 complete; full containment adoption remains.
