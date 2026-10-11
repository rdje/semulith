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
- next_action: finish P4-SYSTEM.14 a42g /0242 COMMIT postconditions, then
  next finite complete closure/property/collector adequacy unit. No qualification
  integration; caller still owns complete reviewed impact projection/currentness.
- in_flight_uncommitted: a42g complete/verified; final COMMIT pending.34 controls/
  18 omissions normal/O,4096 graph pairs and tracked32768 redundancy diagnostic;
  focused13/full PROFILE/sharder12/seven books/3212 fresh+actual links/normal+
  print/exact new example pass. Whole source/task/17 old examples/history102/
  scope1360 bytes/modes/Gitlinks exact normal/O; real receipt+digest edits refuse.
  PROFILE492/GUEST328/global1439 derived; canonical/CPU/caps/seals unchanged.
  Latest full CI exact3e5a3ea all five legs green (443 Rust/smoke53/seven books),
  receipt target/p4-system-14/a42d3b/full-ci/result.json. No canonical v1 capture.
  First hook refused two checklist signatures; failed owned job tree closed,
  HEAD unchanged. Repair own-box receipts and rerun. External Kimi Code has two
  read-only AGENTS.md handles; do not kill; recheck standard handoff after commit.
- blockers: none. Archive seal LC0006 complete; full containment adoption remains.
