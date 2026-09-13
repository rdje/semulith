# P2-SCALAR: validate the first RV64I profile

## Metadata

- Tree ID: `P2-SCALAR`
- Status: `proposed`
- Roadmap lane: `ROADMAP.md` §6 → **P2 — Validate the first RV64I profile**
- Gate: `CPU-LAB`
- Depends on: `P1-LAB` (gate `G1`)
- Unlocks: `P3-BREADTH`, `P4-SYSTEM`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Complete the **entire declared** scalar instruction and laboratory-environment scope of
`rv64i-lab-v0` and carry it through the full processor gate, producing a reusable CPU
deliverable with a versioned accepted profile and attached evidence.

## Non-Goals

- Not a boot test. `CPU-LAB` is a processor gate; no system workload substitutes for it.
- No privilege, translation, atomics or floating point — those are new work in `P4-SYSTEM`,
  and passing here shortens none of it (`ROADMAP.md` §P2).

## Acceptance Criteria — gate `CPU-LAB`

The full processor gate of `docs/EVIDENCE_AND_GATES.md` §7: `G-SCOPE`, `G-STATE`, `G-CONTRACT`,
`G-TRACE`, `G-OBLIGATIONS`, `G-INTERACTIONS`, `G-REGRESSION`, `G-PORTABILITY`, `G-REPLAY`,
`G-RELEASE`. A missing required check yields `incomplete`, never `passed`.

## Task Tree

- ID: `P2-SCALAR.1` — **complete the declared instruction scope** *(task card `T008`)*
  Status: `pending`
  Goal: every remaining selected RV64I form, not just the mnemonics already exercised.
  Acceptance: coverage reported with its **denominator**; `SCP-02`'s dependency closure holds.

- ID: `P2-SCALAR.2` — **boundary arithmetic and state interactions**
  Status: `pending`
  Goal: boundary values, sign/zero extension, shift corner cases, alias and overlap effects.
  Acceptance: exhaustive checks where a reduced width makes them tractable; source-linked expected values.

- ID: `P2-SCALAR.3` — **fault, suppression and reserved cases**
  Status: `pending`
  Goal: fetch and access faults, suppressed effects, reserved encodings, controlled event boundaries.
  Acceptance: a failing access that already modified memory or a device is modelled as the source defines it (`SEM-06`, catalog `C11`); reserved cases keep their source meaning (`SEM-07`).

- ID: `P2-SCALAR.4` — **the interaction matrix** — `G-INTERACTIONS`
  Status: `pending`
  Goal: the declared fault × alias × boundary × event × progress × restart matrix, exercised.
  Acceptance: the matrix is declared first and then exercised; unexercised cells are reported, not omitted.

- ID: `P2-SCALAR.5` — **external and directed campaigns** — `G-REGRESSION`
  Status: `pending`
  Goal: matched reference comparisons, configured external tests, directed sequence tests, and compiled freestanding programs.
  Acceptance: ACT4 results are recorded as **external tests with Sail-derived expected values**, never as a second independent semantics (`EVD-04`).

- ID: `P2-SCALAR.6` — **discrepancy reduction**
  Status: `pending`
  Goal: minimize every discrepancy and retain the minimized case.
  Acceptance: the minimized case reproduces the original divergence; no discrepancy is closed by widening a mask or editing an expected value without a **source-grounded** justification (`EVD-05`, `AI-05`).

- ID: `P2-SCALAR.7` — **snapshot and replay for implemented boundaries** — `G-REPLAY`
  Status: `pending`
  Goal: demonstrate replay only for the state boundaries actually implemented.
  Acceptance: a mid-execution snapshot captures all future-relevant pending state or is not offered at all.

- ID: `P2-SCALAR.8` — **portability matrix** — `G-PORTABILITY`
  Status: `pending`
  Goal: native x86-64 and AArch64 execution fixtures agree; the selected pure-Rust primitive/state/endian tests pass their pinned Miri and cross-endian plan.
  Acceptance: both native hosts are **mandatory**; if the infrastructure is unavailable the profile stays experimental and the gate reads `incomplete` — no "when available" clause (`RUST-05`, `docs/EVIDENCE_AND_GATES.md` §7).

- ID: `P2-SCALAR.9` — **the `CPU-LAB` release** *(task card `T009`)* — `G-RELEASE`
  Status: `pending`
  Goal: a reproducible gate report from pinned inputs, explicit capability limits, a named release decision, and a versioned accepted artifact.
  Acceptance: fidelity reported **separately** per axis (`SCP-05`); "supports RV64I" appears nowhere.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P2-SCALAR.1` | `pending` | the accepted profile must cover its entire declared scope, so scope completion precedes campaigns |

## Decisions

- `2026-09-13`: "Locked" means a **versioned accepted profile whose evidence is attached to its
  exact inputs**. A semantic fix invalidates affected evidence and produces a new accepted
  version. It never means errors become unfixable (`ROADMAP.md` §5).

## Open Questions

- Is x86-64 **and** AArch64 CI infrastructure available at release time? If not, the honest
  outcome is `incomplete` or an explicitly narrower, labelled host policy (`RK14`).

## Blockers

- `P1-LAB` gate `G1`.

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

- `2026-09-13`: Created from `ROADMAP.md` §P2 and task cards `T008`–`T009` by `SEMULITH-TREES.2`.
