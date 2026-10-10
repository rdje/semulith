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
- **Active trees:** `CITATION-ACCURACY` (1/2 — CITATION-QUOTES registered; `.2` the Markdown census, proposed) · `LIVE-CONTAINMENT` (3/4 — the closed-tree register, the orientation sources, TOOLBOX/DOCTRINE_ENFORCEMENT partitioned; `.4` active: finite archive sealed; full inventory/adoption remains) · `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-09`, `SEMULITH-AC-0061`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (12/18 — `.1`–`.12` closed; CPU-SYSTEM `incomplete`, 8/10 axes open; `.13` contract v2 active).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.13` priority c18c — repair citation readers accepting
  fetched HTML without checking exact source hashes. Both RV32I/RV64I fetched
  pages differ only in Antora UI metadata; authenticated .materials copies match
  the pinned hashes and supplied c18b review. Reproduce both locator/quote readers,
  add RED controls, refuse altered bytes, restore only verified project copies.
  Then c19 LOAD-X0/remaining runtime pairs. c18b binds all eleven load/store forms
  over 111 boundaries/222 parcels; seventeen isolated extension/truncation copies
  rejected before credit; declaration gate RED before registration. Prior 82
  bindings and all inputs/core/author/generated/frozen exact. Registry 84, effective
  82/114; sixteen runtime pairs/freeze remain. Corpus 167/5365/10524; GUEST-GEN 145,
  doctrine 649, book 47. c18a history inverse proofs in archive 8/shard 0223 (225 rows).
  .14 owns statuses/structured experiments/registration.
- in_flight_uncommitted: none at commit.
- blockers: none. Authorized Kimi closure clears the actual census (`handoff: OK`).
  Sandboxed census is invalid because ps is denied; use the actual unsandboxed check.
  0 open upstream issues (`scripts/upstream_exposure.py`; submodules remain read-only).
