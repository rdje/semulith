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
- last_unit: `ARTIFACT-CLEANUP.13` / SEMULITH-AC-0070 attempt journal.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: .15 first fixes P1 input ownership: a retained-input fixture can
  match cache names/path without Cargo output provenance. Bind regenerable
  build-output ownership before any mutation, then anchored core/journal; .14
  host-bound operator CLI last. Read .11-.15 and tool/probes/book first.
- last_evidence: target/artifact-cleanup-0070. Journal26 tests normal/O/10 guard
  omissions each1 failure/0 errors,22 outcomes; total gate48. Actual metadata-only
  source-bound plan/full-sync/read smoke: intent0/returns0, owned dummy intact.
  Focused16/books7/normal-print/scope;18 files/protected1456/1Gitlink/98 old entries,
  4030B whole0382/0383. Plan logic unchanged; no cache unlink API. All caps fixed.
- blockers: none requiring director input. Original37/native3/41514B/canonical
  observations and original events stay exact. P4 policy/status follows repair;
  method satisfied/policy pending;CPU14/18,BOARD10/12,GC replay4/4green.
  D79/D80 LC.4; runtime P2 P4 a42ab.40 doctrines/1631 literal sites/42 routes.
  No push below300;241 before AC0070. Always target/tmp as TMPDIR. Last cleanup
  timestamp unchanged in its record; no real event required by journal testing.
