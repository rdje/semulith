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
- next_action: finish P4-SYSTEM.14 a42f COMMIT postconditions, then the next
  finite complete-closure/impact/source-grounded property/collector adequacy unit.
  D46 repair verified; no qualification integration or new method/API.
- in_flight_uncommitted: a42f complete/verified, final COMMIT pending. Focused13/
  full PROFILE/sharder12/seven books/3196 links/normal+print pass. Whole source/
  task inverses,17 examples exact; actual gate prefixes33/0 normal/O differ only
  in reason.102 history entries/1358 other files/modes/Gitlinks exact normal/O;
  real receipt+digest edits refuse. D46 closed; PROFILE454/GUEST328/global1401.
  Latest full CI exact3e5a3ea:443 Rust/all doctrines/bench/smoke53/seven books,
  all1370 tracked bytes/modes/Gitlinks unchanged; jobs closed before ownership.
  Receipt target/p4-system-14/a42d3b/full-ci/result.json. Canonical/CPU/caps/seals
  unchanged; no canonical v1 capture or qualification.
- blockers: none. Archive seal LC0006 complete; full containment adoption remains.
