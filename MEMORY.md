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
- next_action: finish a42i /0244 COMMIT postconditions, then due recurring
  artifact cleanup (AC0062 last2026-10-10 17:22:34UTC), before ordinary-part gate
  assessment/remaining a42 adequacy. No dirty pivot.
- in_flight_uncommitted: a42i verified D47 repair, complete help/arity and
  synthetic make gate/CI wiring.19 cases normal/O; parent11 failures,
  omissions2/2/4/1, zero errors. Actual restricted2/host0/literal --all0;
  focused12/sharder12/seven books/3212 links/full normal+print, whole source/task/
  README/Makefile/workflow/book inverses/history100/scope1367 exact normal/O.
  39 doctrines/1439 arms/caps/seals/GC/canonical/CPU/qualification unchanged.
  First hook refused missing isolated REPO_ROOT binding; fixed fixture only.
  Locality57/57 normal/O/SEAM19 pass; two binding controls refuse before writes.
  Final14-file hooks retry/hash/mode/brief0/host census pending. Latest full CI exact3e5a3ea.
- blockers: none. Archive seal LC0006 complete; full containment adoption remains.
