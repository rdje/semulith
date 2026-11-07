# P6-LINUX: boot Linux to useful userspace

## Metadata

- Tree ID: `P6-LINUX`
- Status: `proposed`
- Roadmap lane: `ROADMAP.md` §6 → **P6 — Boot Linux to useful userspace**
- Gate: `LINUX`
- Depends on: `P5-BOARD` (gate `BOARD`)
- Unlocks: `P7-COMPUTER`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

A reproducible cold boot that reaches userspace `init` and a console shell, runs a guest
program, exercises timer-driven scheduling, and completes a documented shutdown or reboot path.

## Non-Goals

- Not a proof of the CPU. Linux is an independently developed, demanding **integration
  workload**; it validates composition and workload progress, not processor completeness
  (`docs/EVIDENCE_AND_GATES.md` §8).
- No desktop, graphics or input. Those are a separately sized later increment (`ROADMAP.md` §P7).

## Acceptance Criteria — gate `LINUX`

A reproducible cold boot reaches userspace `init` and a console shell, runs a guest program,
exercises timer-driven scheduling, and completes a documented shutdown or reboot path. **A
kernel banner alone is insufficient.**

## Task Tree

- ID: `P6-LINUX.1` — **pin the system**
  Status: `pending`
  Goal: firmware, kernel, build configuration, hardware description and initramfs, all pinned by hash.
  Acceptance: the boot is reproducible from the recorded set alone.

- ID: `P6-LINUX.2` — **the firmware/SBI contract**
  Status: `pending`
  Goal: run compatible M-mode firmware providing the selected SBI services before entering the S-mode kernel. Successor of `profiles/rv64gc-lab-v0`'s `REQ-D-SBI`.
  Acceptance: a host-modelled SBI is a **different contract** and is never silently substituted (`ROADMAP.md` §P6). Which route is in use is stated in the report.

- ID: `P6-LINUX.3` — **entry state and placement**
  Status: `pending`
  Goal: satisfy Linux's actual RISC-V entry-state and placement requirements as a separate, named system contract.
  Acceptance: the requirements are cited from the kernel's own boot documentation, not inferred from a working boot.

- ID: `P6-LINUX.4` — **reach `init` and a shell**
  Status: `pending`
  Goal: cold boot to userspace `init` and an interactive console shell.
  Acceptance: console output captured and replayable; the run identity records every pinned input.

- ID: `P6-LINUX.5` — **run a guest program and exercise scheduling**
  Status: `pending`
  Goal: execute a userspace program; demonstrate timer-driven preemption actually occurring.
  Acceptance: scheduling is demonstrated by observed preemption, not by the kernel booting.

- ID: `P6-LINUX.6` — **shutdown and reboot**
  Status: `pending`
  Goal: a documented shutdown path and a reboot path.
  Acceptance: both complete without a wedged model; reset ordering matches the board contract.

- ID: `P6-LINUX.7` — **seam-error routing**
  Status: `pending`
  Goal: for every failure found here, classify its owner — CPU, environment contract, device, or composition — reduce the failing interaction, amend the responsible artifact, **invalidate affected evidence**, and rerun the relevant gates (`docs/CPU_ENVIRONMENT.md` §5).
  Acceptance: no failure is fixed at the boot layer to make the boot proceed.

- ID: `P6-LINUX.8` — **the `LINUX` gate report**
  Status: `pending`
  Goal: generate from pinned inputs.
  Acceptance: states explicitly that it does not retroactively prove CPU completeness.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P6-LINUX.1` | `pending` | nothing here is reproducible until the inputs are pinned |

## Decisions

- `2026-09-13`: single-core console Linux reaching userspace and executing a program is the
  first Linux deliverable. Headless networking/storage and an optional desktop are later
  releases (`ROADMAP.md` §1).

## Open Questions

- Which firmware implementation. Due before `.2`. The revision is selected: SBI 2.0, by `REQ-D-SBI`, which moved here from `CPU-SYSTEM`'s scope (`decision_the-seventeen-called.md`).

## Blockers

- `P5-BOARD` gate `BOARD`.

## Acceptance Checklist (filled per leaf at execution time)

Each leaf adds its own rows when it runs. These record one amendment to `.2`, from `P4-SYSTEM.14` a51-0; no P6 leaf has run.

- [x] **ROOT CAUSE (WHY + WHERE)** — `REQ-D-SBI` sat in the CPU's catalogue though no firmware runs before this tree, and this tree did not name it: `git show 620afecd:docs/tasks/P6-LINUX.md | grep -c REQ-D-SBI` = 0.
- [x] **ADDRESSED (verified)** — `grep -c 'Successor of' docs/tasks/P6-LINUX.md` = 1: `.2` names it as its predecessor, and the open question keeps only the firmware implementation.
- [x] **NO REGRESSION** — `python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0` `rc=0`, `0 drift, 0 finding(s)`.
- [x] **FIX** — `.2`'s goal and the open question name `REQ-D-SBI` and its selection, SBI 2.0.
- [x] **LOCKSTEP** — `decision_the-seventeen-called.md`, `docs/models/rv64gc-lab-v0/src/requirement-status.md`.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| — | — | not started | — |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| — | `pending` | `pending` |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P6 by `SEMULITH-TREES.3`.
