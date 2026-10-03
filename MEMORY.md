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
- **Active trees:** `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-02`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (1/10 — the profile resolved as `rv64gc-lab-v0`, the unit unregistered by design; `.2` slices (a) fragments+assembler+IALIGN, (b) semantics operators+sem files, (c1) the staged 33-CSR state document + gen_state's two-profile branch landed).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `P4-SYSTEM.2` slice (e) — the unit artifacts at scratch→flip staging:
  `encoding.sexp` with the partial slots (m/a/f/d/c/zifencei), the requirements growth
  (the new instructions' requirement mirrors), the scope-census dual edit
  (schema/profile.sexp + dossier_sexp._SCOPE_LISTS, 52→65), all authored and validated
  from target/p4-system-2/ and moved unchanged at the flip (slice h). Slice (d) is
  committed (`SEMULITH-P4-0008`); the machinery (privilege.rs) and the generator
  parameterizations are tracked; the generated rv64gc modules stay scratch per
  `decision_generated-mirror-needs-tracked-input`.
- in_flight_uncommitted: none.
- blockers: none (0 open upstream issues — `scripts/upstream_exposure.py`; never patch the
  submodule, adopt by moving the pin).
