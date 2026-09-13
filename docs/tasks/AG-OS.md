# AG-OS: run and validate an archogen-generated OS on a gated Semulith platform

## Metadata

- Tree ID: `AG-OS`
- Status: `proposed`
- Roadmap lane: `ROADMAP.md` §6 → the **AG** node; `docs/ARCHOGEN_INTEGRATION.md` §5
- Gate: `ARCHOGEN-OS`
- Depends on: `P5-BOARD` (gate `BOARD`), and a CPU profile that has passed its own gate
- Unlocks: nothing downstream in this repository; it is a delivered capability
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Bind archogen's checked realization plan to qualified Semulith models through a **versioned
adapter**, export the platform's capabilities so archogen's checker can compare offered
behaviour against the original eADL requirements, and run a pinned generated OS to completion
with reproducible, replayable evidence.

## Non-Goals

- **No second eADL parser, matcher, scheduler or OS generator in Semulith.** Missing model
  behaviour is an unsupported engine realization, never a reason to put implementation into
  eADL (`OWN-06`, `docs/ARCHOGEN_INTEGRATION.md` §2).
- No dependency on archogen inside `semulith-core`. Semulith's core stays usable without it, and
  archogen's hosted S0 path must not wait for Semulith readiness.
- No claim about all archogen outputs, all OS properties, or real hardware timing.

## Acceptance Criteria — gate `ARCHOGEN-OS`

The selected CPU and board gates pass; incompatible requirements are rejected; the pinned
generated OS boots and completes its declared functional suite; reports replay; known
failure/control outcomes are distinguishable; evidence limitations are explicit.

## Task Tree

- ID: `AG-OS.1` — **inspect the real eADL/plan interfaces**
  Status: `pending`
  Goal: read archogen's actual typed representation and checked realization plan before fixing any adapter shape.
  Acceptance: the adapter is designed against the real interface. `ROADMAP.md` §1 makes this an explicit revisit condition, not an assumption.

- ID: `AG-OS.2` — **the versioned realization adapter**
  Status: `pending`
  Goal: consume the checked plan; select qualified CPU/device models; generate the composition, parameters and wiring.
  Acceptance: selection respects **joint** resources, topology and ownership — individually matching capabilities are insufficient (`docs/ARCHOGEN_INTEGRATION.md` §2).

- ID: `AG-OS.3` — **platform contract export and compatibility check**
  Status: `pending`
  Goal: export exactly what an OS needs — CPU profile and extensions, address widths, endianness, privilege modes, memory/atomicity model, RAM and reserved regions, MMIO map, device identity, interrupt routing, timers, boot resources, image format and entry state, ABI, firmware services, counter meaning, event delivery, test-control capabilities, and the fingerprints of the actual selected definitions (`docs/ARCHOGEN_INTEGRATION.md` §3).
  Acceptance: unsupported requirements are rejected **before boot** where they can be checked statically; required versus optional facilities are explicit.

- ID: `AG-OS.4` — **the OS test runner**
  Status: `pending`
  Goal: reproducible boot, console capture, and a declared guest completion protocol; then interrupts, timer-driven progress, protection and restart tests as the specific OS requires.
  Acceptance: results distinguish an OS assertion failure, a guest exception, an expected shutdown, an exhausted execution budget, an unsupported model capability, and a Semulith internal failure. **An OS exception is not automatically a test failure** — the test contract defines the expected outcome.

- ID: `AG-OS.5` — **run identity and replay**
  Status: `pending`
  Goal: record the eADL revision, archogen generator and mapping versions, toolchain and configuration, OS image hash, Semulith build and profile, platform contract, test-plan version, and event choices (archogen `F19`/`F22`).
  Acceptance: any of these changing invalidates the relevant evidence (`EVD-07`).

- ID: `AG-OS.6` — **the shared-trust inventory**
  Status: `pending`
  Goal: record Semulith code, models, generated configuration, adapters, source facts, and any sharing with archogen's hosted model or checker (archogen `F30`).
  Acceptance: if the hosted playground reuses Semulith device transitions, their agreement is recorded as **shared-model evidence**, not an independent hardware comparison. Semulith does not become independent by being a separate project (`docs/ARCHOGEN_INTEGRATION.md` §4).

- ID: `AG-OS.7` — **typed fault injection**
  Status: `pending`
  Goal: distinguish normal allowed hardware behaviour, a declared injected hardware failure, an adversarial device or input, and impossible states used to stress the emulator.
  Acceptance: success under one model is never cited as evidence for another.

- ID: `AG-OS.8` — **the `ARCHOGEN-OS` gate report**
  Status: `pending`
  Goal: generate from pinned inputs.
  Acceptance: discrepancies are minimized and assigned to OS generation, target mapping/boot contract, processor semantics, device semantics, or the test machinery. **The loop must never rewrite either project's specification to make a failing test pass.**

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `AG-OS.1` | `pending` | no eADL grammar or typed API has been supplied; designing the adapter first would design against a guess |

## Decisions

- `2026-09-13`: archogen's first profile is `rt-static-up-v1` — one core, fixed-priority
  preemption, static resources, a timer, observable output. It needs no Linux, MMU, filesystem,
  networking or virtio stack, so it can be served by a **smaller accepted CPU profile** than
  `P4-SYSTEM`'s. Do not promise that unprivileged RV64I alone suffices
  (`docs/ARCHOGEN_INTEGRATION.md` §6).

## Open Questions

- archogen's exact target width and feature decision. Compared against `rv64i-lab-v0` during
  `P0-PROFILE.1` when available (`ROADMAP.md` §1 revisit condition).
- archogen's `F29` repeated-preemption accounting: its synthetic total of 23 stays an archogen
  fixture. Semulith may export documented events but supplies **no** instruction-to-cycle
  conversion and no physical timing claim.

## Blockers

- `P5-BOARD` gate `BOARD`; the eADL interfaces of `AG-OS.1`.

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

- `2026-09-13`: Created from `ROADMAP.md` §P5 and `docs/ARCHOGEN_INTEGRATION.md` §§2–6 by `SEMULITH-TREES.3`.
