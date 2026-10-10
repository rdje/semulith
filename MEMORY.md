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
- next_action: `P4-SYSTEM.14` a7/0198 — canonical rv64i six-pair and
  GC candidate reference rows. Replace unsupported implementation lineage with
  public-contract evidence/explicit unexamined scope; preserve ACT campaign's
  actual Sail-produced expectation dependence. Account for every derived report,
  rv64i dossier/board pin and model-book consequence before committing.
  A6 corrects maintained ancestry/FP acceptance/search/card/.7/.1/book assertions;
  five exact historical payloads16309B, full57117B task inverse, three damaged
  controls. Realized1/1/focused12/six books/verify green; all code/producers/
  profiles/frozen/registry/history/LIVE exact,114/114 frozen14, CPU incomplete7axes,
  P4 13/18, arms669. No new lineage/conformance/requirement-status credit.
  Then evidence policy/records/status derivation and sixth-unit registration.
  CleanupAC0062:204incremental caches/978509475B removed, residue0;
  6261retained inputs/evidence hashes exact, focused9/six books green.
  No push below cadence.
- in_flight_uncommitted: none at commit.
- blockers: none. Authorized Kimi closure clears the actual census (`handoff: OK`).
  Sandboxed census is invalid because ps is denied; use the actual unsandboxed check.
  0 open upstream issues (`scripts/upstream_exposure.py`; submodules remain read-only).
