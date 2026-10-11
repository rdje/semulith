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
- next_action: start owned P4-SYSTEM.14 a42b source/image correspondence through
  published project producer interfaces, explicit authenticated dependencies and
  bounds. Complete relevant closure, conservative old/new impact and collector
  provenance remain mandatory later a42 slices; positive evidence stays pending.
  Review the existing collector trust boundary before choosing the finite unit.
- in_flight_uncommitted: none after COMMIT; inspect Git before resuming.
  A42a parent-program23 controls/seven omissions normal/O, PROFILE390/0,1213 arms;
  D42 bound-before-rule selection corrected, exact draft loses1 assertion/no errors.
  Focused17/sharder12/0/seven books/3124 links/all11 literal commands pass;
  whole sources/task/history/canonical inverses protect102 entries/1329 files.
  DEV16=15+1/2262B into0251; actual receipt+digest rewrites refuse.
  Last full CI clean03ed501 all5 legs green:443 Rust/smoke53/seven books,
  18 verified sources unchanged. Log40152B SHA
  c6fd1d7b22b9770b2b7b07b98ad0b1a43a4c1ef0eccfda71e68def0cc3f01e24;
  receipt target/p4-system-14/a41/full-ci/result.json. CPU/canonical/caps/seal exact.
- blockers: none. Archive seal LC0006 complete; full containment adoption remains.
