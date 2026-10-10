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
- next_action: `LIVE-CONTAINMENT.4b` browsing direction for the proposed finite
  12-file closed-P4 history seal. Read
  `docs/decisions/decision_task-history-seal-review.md`: exact manifest,
  byte-identical375029B archive, all retrievals/negative controls, five incoming
  consumer files and proposed path/anchor stubs. Original files remain intact;
  no ceiling/checker changed. Source guide explicitly requires direction for this
  browsing change; previous210-changelog approval does not cover task history.
  Task aggregate is effectively full; do not start ordinary evidence growth.
  After direction, own/verify/commit the approved bounded transition, then resume
  `P4-SYSTEM.14` experiments, mechanical policy/status and mirror reconciliation.
  A10/0201 registration/scope fix is complete; full five-leg CI green,
  Rust173/17/253, six units/seven books/672 arms, CPU incomplete7axes/P4 13/18;
  frozen114/114 unchanged. CleanupAC0062 last2026-10-10. No push below cadence.
- in_flight_uncommitted: none at commit.
- blockers: changed task-history browsing needs director direction under the source
  guide. The committed proposal is reviewable; originals are intact. Do not grow
  ordinary task history before the bounded transition. No upstream issue is open.
