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
- next_action: run full CI on the clean a41 composition milestone, record the
  actual revision/log/result, then start owned a42 complete method adequacy:
  parent-program/source/image correspondence, complete relevant dependency
  closure, conservative impact and collector provenance. Positive byte evidence
  remains pending, blanket v1 qualification refusal and CPU status unchanged.
- in_flight_uncommitted: none after COMMIT; inspect Git before resuming.
  A41 evaluator42 controls/29 omissions normal/O; PROFILE374/0,1197 arms.
  Focused17/sharder12/0/seven books/3122 links/all10 literal examples pass;
  complete source/history/task/canonical inverses protect102 entries/1326 files.
  DEV17=15+2/5355B into0250; whole receipt+digest edits refuse. New book chapter
  documents independent findings, fixed budgets, frozen context/exact snapshots,
  coherent failed processes, released payloads and incomplete adequacy.
  Last full CI c84bb7b all five legs green (443 Rust/smoke53/seven books).
- blockers: none. Archive seal LC0006 is complete; full containment adoption remains.
