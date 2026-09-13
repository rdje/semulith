# P7-COMPUTER: deliver a useful headless computer

## Metadata

- Tree ID: `P7-COMPUTER`
- Status: `proposed`
- Roadmap lane: `ROADMAP.md` §6 → **P7 — Deliver a useful headless computer**
- Gate: `SYSTEM`
- Depends on: `P6-LINUX` (gate `LINUX`)
- Unlocks: the later SMP system, jointly with `MC-MULTICORE`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

The first bounded full-computer release: persistent block storage, file workloads, networking,
reset and reboot, and system snapshots — each added as an **individually specified increment**
with reproducible guest workloads and device evidence.

## Non-Goals

- No graphics, keyboard/pointer input or desktop. Those form a subsequent product increment
  with an explicit device list and performance budget, kept visible rather than hidden inside
  this milestone (`ROADMAP.md` §P7).

## Acceptance Criteria — gate `SYSTEM`

The declared headless workload suite passes, storage persists correctly, and snapshot/restore
preserves the relevant CPU, device and event state.

## Task Tree

- ID: `P7-COMPUTER.1` — **declare the workload suite**
  Status: `pending`
  Goal: name the guest workloads the release will claim, before implementing the devices they need.
  Acceptance: the suite is the claim; anything outside it is explicitly unclaimed.

- ID: `P7-COMPUTER.2` — **persistent block storage**
  Status: `pending`
  Goal: a block device with its own dossier, requirement links and evidence.
  Acceptance: persistence verified across a full stop/start cycle, not just within a run.

- ID: `P7-COMPUTER.3` — **file workloads**
  Status: `pending`
  Goal: guest file workloads with reproducible expected results.
  Acceptance: results are independently derived, not read back from the model.

- ID: `P7-COMPUTER.4` — **networking**
  Status: `pending`
  Goal: a network device increment with device evidence and a reproducible guest workload.
  Acceptance: external interaction is replayable — recorded event streams, not live timing (`ENV-03`).

- ID: `P7-COMPUTER.5` — **reset and reboot at system scope**
  Status: `pending`
  Goal: full-system reset and reboot with devices returning to their specified reset state.
  Acceptance: retained state that must survive reset is identified, not discovered.

- ID: `P7-COMPUTER.6` — **system snapshots**
  Status: `pending`
  Goal: snapshot and restore preserving relevant CPU, device and event state.
  Acceptance: a mid-execution snapshot captures **all future-relevant pending state** and validates compatibility; a seed without the generator version and event stream is insufficient (`docs/ARCHITECTURE.md` §7).

- ID: `P7-COMPUTER.7` — **the `SYSTEM` gate report**
  Status: `pending`
  Goal: generate from pinned inputs.
  Acceptance: the report names the declared suite as the boundary of the claim.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P7-COMPUTER.1` | `pending` | declaring the suite first is what stops the claim expanding to fit whatever was built |

## Decisions

- `2026-09-13`: graphics and a desktop are a **separate** increment. The long-term personal
  computer ambition is preserved without hiding its work inside this gate.

## Open Questions

- Which snapshot boundaries are genuinely implementable at this stage. Answered by what
  `P4-SYSTEM` and `P5-BOARD` actually implemented, not by what would be convenient.

## Blockers

- `P6-LINUX` gate `LINUX`.

## Acceptance Checklist (filled per leaf at execution time)

- [ ] **ROOT CAUSE (WHY + WHERE)** — <the command run and its real output>
- [ ] **ADDRESSED (verified)** — <measured before → after>
- [ ] **NO REGRESSION** — <the suite or gate re-run, and its result>
- [ ] **FIX** — <the change made>
- [ ] **LOCKSTEP** — <docs, contracts and indexes updated>

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| — | — | not started | — |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| — | `pending` | `pending` |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P7 by `SEMULITH-TREES.3`.
