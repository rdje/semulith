# P4-SYSTEM: validate the processor Linux actually needs

## Metadata

- Tree ID: `P4-SYSTEM`
- Status: `proposed`
- Roadmap lane: `ROADMAP.md` §6 → **P4 — Validate the processor needed for Linux**
- Gate: `CPU-SYSTEM`
- Depends on: `P2-SCALAR` (gate `CPU-LAB`)
- Unlocks: the CPU release gate, and with it `P5-BOARD` and `MC-MULTICORE`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Select and validate a Linux-capable profile — provisionally RV64GC with an explicitly chosen
privilege revision, M/S/U modes, Sv39 translation, implemented CSRs, interrupt acceptance,
counter behaviour, and stated firmware/toolchain requirements — as a **processor**, in the
laboratory, before any board exists.

## Non-Goals

- No board, no boot. Booting does not prove the CPU, and a CPU bug found during a later boot
  returns here and invalidates affected evidence (`docs/CPU_ENVIRONMENT.md` §5).
- No floating-point support until its backend passes qualification. There is **no silent
  native-float or FFI fallback** (`docs/ARCHITECTURE.md` §6, `RUST-01`).

## Acceptance Criteria — gate `CPU-SYSTEM`

The complete declared profile passes the processor gate, **including its environment contract**.
This gate authorises the planned next engineering stage: board implementation.

## Task Tree

- ID: `P4-SYSTEM.1` — **resolve the profile**
  Status: `pending`
  Goal: turn "provisionally RV64GC" into an exact selection with a resolved dependency closure — privilege revision, modes, translation scheme, CSR list, interrupt and counter behaviour, firmware and toolchain requirements.
  Acceptance: nothing is inferred from the letters `GC`; each element has a source locator (`SCP-01`, `SCP-02`).

- ID: `P4-SYSTEM.2` — **privilege and mode transitions**
  Status: `pending`
  Goal: M/S/U transitions, control-register permissions, trap interception, context state, mode-dependent decoding (catalog `C15`).
  Acceptance: the same instruction's behaviour is tested **in each supported mode**, not once.

- ID: `P4-SYSTEM.3` — **Sv39 translation and protection**
  Status: `pending`
  Goal: page-table format, walk ordering, permission checks, A/D update policy, ASIDs, translation invalidation, permitted walk side effects (catalog `C12`).
  Acceptance: permission failure produces the correct fault **and** the permitted page-table side effects; A/D policy is validated against the selected extensions and revision, not chosen as a knob.

- ID: `P4-SYSTEM.4` — **atomics and reservations**
  Status: `pending`
  Goal: atomic widths, reservation semantics, failed conditional stores, overlap and external-write cases (catalog `C16`, `docs/CPU_ENVIRONMENT.md` §2).
  Acceptance: single-core reservation behaviour is validated here; multicore memory-model work is `MC-MULTICORE`, not smuggled in.

- ID: `P4-SYSTEM.5` — **interrupts, counters and wait**
  Status: `pending`
  Goal: masks, priority, pending/active state, nesting, return; counter width, rate, wrap and mode gating; a halted core still receiving its wake event (catalog `C14`, `C17`).
  Acceptance: timer or interrupt wake occurs **without CPU retirement** — the laboratory must be able to make time pass while nothing executes.

- ID: `P4-SYSTEM.6` — **instruction visibility and fence semantics**
  Status: `pending`
  Goal: when newly written code must become executable, and when stale state may persist (catalog `C13`).
  Acceptance: rewrite-code fixtures with and without the architectural synchronization.

- ID: `P4-SYSTEM.7` — **floating-point backend qualification** *(task card `T011`)*
  Status: `pending`
  Goal: name a Rust candidate; pin the exact target policy for rounding modes, flags, result bits, conversions, NaN payloads and boxing; inventory ancestry (shared SoftFloat lineage, specialization, thread-local vs global status, exact compiler and features); run independent numeric fixtures.
  Acceptance: a decision record with **measured** correctness and performance evidence. If no candidate passes, implement the required subset in Rust and defer the capability. TestFloat's usual SoftFloat expected-value path is recorded as shared ancestry (`RK07`, `EVD-04`).

- ID: `P4-SYSTEM.8` — **faults, restart and partial progress**
  Status: `pending`
  Goal: fault priority, suppressed effects, restart locations, partial commits under the new system features (`SEM-04`, `SEM-06`).
  Acceptance: a fault injected after the Nth suboperation leaves the architecturally required state.

- ID: `P4-SYSTEM.9` — **environment contract v1** — `G-CONTRACT`
  Status: `pending`
  Goal: extend the contract to cover translation inputs, interrupt sources, counter progress and reservation invalidation for this profile.
  Acceptance: every new assumption has a positive and a negative fixture; the contract is versioned, not edited in place.

- ID: `P4-SYSTEM.10` — **the `CPU-SYSTEM` gate report**
  Status: `pending`
  Goal: the full processor gate over the complete declared profile.
  Acceptance: reproducible from pinned inputs; fidelity reported per axis; missing checks read `incomplete`.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P4-SYSTEM.1` | `pending` | every later leaf is scoped by the resolved profile |

## Decisions

- `2026-09-13`: the default RISC-V Linux route runs compatible **M-mode firmware providing
  selected SBI services** before an S-mode kernel. A host-modelled SBI is a different contract
  and is never silently substituted (`ROADMAP.md` §P6) — which constrains what this profile
  must implement.

## Open Questions

- Exact privilege specification revision. Due before `.2` depends on it (`RK03`).
- Which Rust floating-point implementation, if any, qualifies. Due before `.7` completes; until
  then floating point is **not** part of the profile.

## Blockers

- `P2-SCALAR` gate `CPU-LAB`.

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

- `2026-09-13`: Created from `ROADMAP.md` §P4 and task card `T011` by `SEMULITH-TREES.2`.
