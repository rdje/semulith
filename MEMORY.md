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

- latest_commit: derive on read with `git log -1 --format='%H %s'`.
- last_unit: `ARTIFACT-CLEANUP.12` / SEMULITH-AC-0069 historical helper retention.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: .13 guarded deletion core/journal, then .14 actual host-census and
  supported CLI/recovery. Read .11-.14 and current tool/help/probes first; no real
  cleanup needed for tests. Parent repair remains priority1 before P4 policy.
- last_evidence: target/artifact-cleanup-0069. Original5815B helper passive/SHA
  exact; five legacy tests normal/O, pin omission1 failure/0 errors each mode.
  Cold3/noGit/valid-parent CLI,26 gate outcomes, focused16/books7/source-history
  and normal-print checks pass. Scope18/protected1452/1Gitlink/98 old entries;
  native0380/0381 retain3172B; all caps fixed. Planner behavior remains read-only.
- blockers: none requiring director input. Preserve original37 producer modules,
  native3/41514B/canonical observations and historical event/helper identities.
  Full P4 policy/status follows repair; finite method satisfied/policy pending,
  CPU14/18,BOARD10/12,GC replay4/4green. D79/D80 LC.4; runtime P2 P4 a42ab.
 40 doctrines/1629 literal sites/42 routes. No push below300;240 before AC0069.
  Always target/tmp as TMPDIR; latest cleanup timestamp unchanged in its record.
