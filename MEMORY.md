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
- next_action: run full CI on the clean P4-SYSTEM.14 a42b ELF repair commit,
  record its result, then activate a42c source-byte image builder. Resume through
  docs/tasks/P4-SYSTEM.md; no canonical matched-v1 capture/qualification yet.
- in_flight_uncommitted: none after this repair commit; full CI is next.
  Writer/controls/docs and Rust fixture clarification are committed together. Four exact old-source ABI defects reproduced;15 controls/
  eight omissions normal/O;49 RV64I/167 GC payloads and full ELF inverses exact.
  Rust443/two public CLI profiles/focused17/sharder12/0/seven books/3138 links/
  all12 examples green, GUEST222/0,39 doctrines1231 arms. Whole old source/task/
  book/history/canonical/scope proofs pass. Evidence target/p4-system-14/a42b.
  Last full CI remains clean03ed501 all5 legs443 Rust/smoke53/seven books;
  target/p4-system-14/a41/full-ci. Next a42b full CI is confirmatory and required
  before a42c; complete closure/impact/collector provenance remains further work.
- blockers: none. Archive seal LC0006 complete; full containment adoption remains.
