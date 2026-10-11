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
- **Active trees:** `CITATION-ACCURACY` (1/2 — CITATION-QUOTES registered; `.2` the Markdown census, proposed) · `LIVE-CONTAINMENT` (3/4 — the closed-tree register, the orientation sources, TOOLBOX/DOCTRINE_ENFORCEMENT partitioned; `.4` active: finite archive sealed; full inventory/adoption remains) · `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-11`, `SEMULITH-AC-0063`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (13/18 — `.1`–`.13` closed; CPU-SYSTEM `incomplete`, 7/10 axes open; `.14` evidence active).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: resume P4-SYSTEM.14 a42's remaining closure/collector/policy
  adequacy obligations. Read current public contracts and own the next finite
  slice on committed clean state. Fixed task-file capacity96/96 remains LC.4's inventory.
- in_flight_uncommitted: none after a42l2/0248 COMMIT. D49 fixed/verified:
  actual full gate1 rejects the same staged part18 receipt accepted before repair.
  Real index/1392 tracked identities/proposed index and source hashes exact,
  residue0;43 controls normal/O, nine omissions discriminate with zero errors.
  Original46 controls/reader exact; TASK-HISTORY48/0, derived1441. Focused12/
  sharder12/seven books/3206 links,95 prior entries and1380 protected files exact.
  Evidence target/p4-system-14/a42l2/replay/result.json. No CPU/qualification credit;
  fixed caps unchanged; full containment adoption stays LC.4. No push below cadence.
- blockers: none. Archive seal LC0006 complete; full containment adoption remains.
