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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-02`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (1/10 — the profile resolved as `rv64gc-lab-v0`; `.2` slices (a)–(g) + slice (h) part 1 landed: THE FLIP — the unit carries its encoding, 33-CSR state document, 62-guest corpus and interaction matrix TRACKED, the route is `generated-definition`, the tracked engine runs the corpus 62/62).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.2` slice (h) part 2 — the Sail privileged matched-experiment
  ATTEMPT (decision 8: Sail 0.14's full config namespace, the rv64i matched-override
  precedent at profiles/rv64i-lab-v0/reference/; a small set of mm-* guests; AGREE /
  named divergence / NOT MATCHABLE recorded honestly) + the LEAF acceptance (the
  same instruction's behaviour tested in each supported mode — the mm corpus mapping)
  + the reports and the book, then leaf status done (`SEMULITH-P4-0013`). The flip
  landed as `SEMULITH-P4-0012`: rv64gc-lab-v0 is a full generated-definition unit
  (all gates judge it; rv64i's verdicts unchanged; DERIVED-COUNTS 419).
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
