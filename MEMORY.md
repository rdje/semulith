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
- last_unit: `ARTIFACT-CLEANUP.15` / SEMULITH-AC-0071 provenance records/reader.
- **Active trees:** `CITATION-ACCURACY`, `LIVE-CONTAINMENT`, `LAB-BENCH`, `ARTIFACT-CLEANUP`, `P5-BOARD`, `P4-SYSTEM`.
- next_action: .17 binds actual successful public Cargo observations and strict
  plan selection to .15 provenance. P1 remains open: legacy names/path metadata
  is not generation. Then .16 anchored core/journal and .14 host/operator CLI.
  Read .11-.17, current code/probes/shared book before changes; preserve old plans.
- last_evidence: target/artifact-cleanup-0071. Provenance25 tests normal/O/13
  omissions each1 failure/0 errors,28 outcomes; gate76. Public Cargo dry-run
  preserves three owned inputs and lists a profile input too. D3 root/D5 profile
  guards repaired; D4 complete task prefix/node/history inverse restored.
  Focused16/books7/normal-print/scope:18 files/protected1460/1Gitlink/97 old
  entries;3844B whole0384/0385. No producer integration or cache-mutation API.
- blockers: none requiring director input. Original37/native3/41514B/canonical
  observations/events exact. P4 full policy/status follows repair; method
  satisfied/policy pending; CPU14/18,BOARD10/12,GC replay4/4green unchanged.
  D79/D80 LC.4; runtime P2 P4 a42ab.40 doctrines/1633 literal sites/42 routes.
  All fixed caps retained; task family has little headroom: verify before each
  slice and preserve complete nodes/history during containment. No push below300;
  242 before AC0071. Always target/tmp as TMPDIR. Latest cleanup record unchanged;
  instrument tests are not a new cleanup event.
