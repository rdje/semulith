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
- **Active trees:** `CITATION-ACCURACY` (1/2 — CITATION-QUOTES registered; `.2` the Markdown census, proposed) · `LIVE-CONTAINMENT` (3/4 — the closed-tree register, the orientation sources, TOOLBOX/DOCTRINE_ENFORCEMENT partitioned; `.4` active: finite archive sealed; full inventory/adoption remains) · `CI-RECOVERY` (3/4 — local repairs verified; native/endian Miri 153/153 each and Rust 1.99 full CI green; hosted evidence next) · `LAB-BENCH` (1/2 — `.2` feedback-gated) · `ARTIFACT-CLEANUP` (recurring §8; last run `2026-10-08`, `SEMULITH-AC-0060`) · `P5-BOARD` (10/12 — the platform capability manifest landed: `platform.sexp`, derived and drift-gated by the 34th doctrine PLATFORM-GEN; the dossier pin load-bearing; `.5` probes and `.7` gate report stay gated on the CPU's acceptance trajectory) · `P4-SYSTEM` (11/18 — the profile resolved as `rv64gc-lab-v0` (`.1`), the privileged machinery landed (`.2`), and nine leaves CLOSED: Sv39 (`.3`), atomics (`.4`), interrupts/counters/wait (`.5`), the fence.i contract (`.6`), the FP backend with F and D bound (`.7`), faults/restart/partial progress (`.8`), the environment contract v1 (`.9`), the CPU-SYSTEM report (`.10`, `incomplete`, 9/10 axes open), and M (`.11`)).
  Milestone frontier: `P4-SYSTEM` (the CPU the board waits on). (`BOOK-APPARATUS` and `MCU-DOCS` closed `2026-10-02`, 2/2 each — the MCU documentation set is acquired and digest-verified.)
- next_action: `CI-RECOVERY.4` — CI-repair pushes now approved without asking again:
  decision_ci-recovery-push-approval. Push f4364bc completed; observe exact-SHA runs:
  rust 37800114021, doctrines 37800113792, portability 37800113741 (tree has URLs).
  doctrines failed at GUEST-GEN self-test. Cold parcel probe omitted CSR metadata;
  repaired locally with a permanent tracked-only guard. Push this fix; rust/native hosts/
  manifest agreement and native Miri pass; endian still running on the first push. Repair/re-push
  as needed; authorization expires at all-three-green, then cadence resumes.
  Archive sealed; P4.12 e1d C/count staging follows CI recovery.
- in_flight_uncommitted: none at commit; hosted endian running at f4364bc.
- blockers: cold fixture fix awaits hosted confirmation; scoped push approval remains active.
  Handoff census
  rc=1: Kimi holds two read-only AGENTS.md handles; closure or sanctioned exemption pending.
  0 open upstream issues (`scripts/upstream_exposure.py`; submodules remain read-only).
