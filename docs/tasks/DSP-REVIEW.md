# DSP-REVIEW: put real DSP pressure on the abstraction before it is stable

## Metadata

- Tree ID: `DSP-REVIEW`
- Status: `proposed`
- Roadmap lane: `ROADMAP.md` §6 → the **D** node, feeding `P3-BREADTH`
- Gate: none of its own; it is a precondition of `BREADTH`
- Depends on: `P1-LAB` (gate `G1`)
- Unlocks: `P3-BREADTH`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Use **real** DSP specifications to find the places where a scalar-CPU-shaped abstraction is
already wrong, while changing it is still cheap — and to do so without acquiring a DSP oracle
or claiming DSP compatibility.

## Non-Goals

- No real DSP compatibility claim. Synthetic behaviour tests the **interface**, not any
  manufacturer's part (`ROADMAP.md` §P3).
- No oracle acquisition. TI C64x/C64x+ (SPRU732J) is a **documentation** candidate; no runnable
  oracle access has been established (`docs/SOURCES_AND_NAMING.md`).

## Acceptance Criteria

- 15–20 discriminating instruction/sequence cases, each grounded in a real manual with a
  locator, chosen for properties those processors genuinely have.
- Every case answers at least one of the fifteen DSP collection questions in
  `docs/INFORMATION_CATALOG.md` §5.
- Each case is classified: *the abstraction expresses this*, *it needs a change*, or *it cannot
  express this and here is what that costs*.

## Task Tree

- ID: `DSP-REVIEW.1` — **width and accumulator semantics**
  Status: `pending`
  Goal: operand, product, accumulator, guard and output widths; fractional formats and where scaling is applied (catalog questions 1–2).
  Acceptance: each answer carries a manual locator; "absent" is a legitimate, recorded answer.

- ID: `DSP-REVIEW.2` — **rounding, saturation and sticky flags**
  Status: `pending`
  Goal: whether rounding precedes or follows accumulation, saturation and narrowing; saturation per operation / lane / transfer; which sticky flags survive interrupts and context switches (questions 3–5).
  Acceptance: the ordering is expressed as a sequence of defined steps, not as a single "saturating add".

- ID: `DSP-REVIEW.3` — **addressing and address spaces**
  Status: `pending`
  Goal: whether instruction and data addresses share units; multiple memory spaces and address generators; modulo, circular, strided and bit-reversed modes (questions 6–8, catalog `C10`).
  Acceptance: the abstraction is checked against *units*, not just widths — `SEM-05` says an address identifies its space, unit, width and packing.

- ID: `DSP-REVIEW.4` — **issue groups and exposed sequencing**
  Status: `pending`
  Goal: packet membership, old/new operand visibility, delayed results, interlocks, early reads, resource-conflict status (questions 9–11, catalog `C09`).
  Acceptance: determines whether `Advance` and the execution unit can represent a packet and a delayed effect — the single most likely place the scalar abstraction breaks.

- ID: `DSP-REVIEW.5` — **loops, repeats and interrupt interaction**
  Status: `pending`
  Goal: hardware loops and repeats interacting with interrupts and exceptions; multi-access instructions; stream/DMA ordering (questions 12–14, catalog `C05`).
  Acceptance: restart state requirements stated in terms of `SEM-04` partial progress.

- ID: `DSP-REVIEW.6` — **executable synthetic stress fixture** *(task card `T010`)*
  Status: `pending`
  Goal: a synthetic target exercising nonstandard widths, distinct address spaces, packets and delayed effects through the real API.
  Acceptance: labelled **synthetic** everywhere it appears; its passing evidence may never be cited for a real DSP claim.

- ID: `DSP-REVIEW.7` — **interface findings report**
  Status: `pending`
  Goal: the classified list of required abstraction changes, with cost, feeding `P3-BREADTH`.
  Acceptance: a finding routed to another tree carries its `ROUTING EVIDENCE`.

## ROUTING EVIDENCE

This tree exists to route findings **out** to `P3-BREADTH` (leaf `.7`), so the routing method is
declared here before the first finding exists rather than improvised when one does.

- **Does a finding reproduce outside the family it is routed to?** Not yet measurable — no
  finding has been produced. `git ls-files 'docs/tasks/P3-BREADTH.md'` exists and its `.1` leaf
  is the receiver, but the DSP review has not run. **Measured: nothing. Routed: nothing.** This
  section is a pre-commitment, not a result.
- **What will be measured before a finding leaves this tree.** For each candidate interface
  change: (1) the manual locator that states the target behaviour; (2) whether the current
  abstraction can express it — demonstrated by an executable synthetic fixture in `.6`, not by
  reading the type definitions; (3) whether the same limitation also fires for the **scalar**
  profile `rv64i-lab-v0`. If it does, the finding is not a DSP finding and does not belong in
  `P3-BREADTH` — it belongs in `P2-SCALAR` or in the core abstraction, and routing it to the
  breadth lane would hide a scalar defect behind a DSP label.
- **What would make the routing wrong.** A finding that reproduces on the scalar profile, or one
  whose "requirement" comes from a manual passage that turns out to describe an
  implementation-defined choice rather than architectural behaviour (`SEM-07`, catalog `C22`).
  Both are checked in `.7` before the finding is handed over.
- **Honest limit.** This is reasoning, not measurement, because the population it quantifies
  over does not exist yet. It is recorded so that the first real routing is graded against a
  method chosen in advance, rather than one chosen to fit the finding.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `DSP-REVIEW.1` | `pending` | widths are the foundation the other questions are asked against |

## Decisions

- `2026-09-13`: DSP work is **not** postponed until after Linux. Architectural pressure is
  applied early; a large unverified DSP implementation is not made mandatory (`ROADMAP.md` §2).

## Open Questions

- Which real DSP, if any, gets a bounded slice in `P3-BREADTH`? Resolved by whether an evidence
  path can be demonstrated — not by which manual is easiest to read (`RK08`).

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

- `2026-09-13`: Created from `ROADMAP.md` §P3 (the D node), catalog §5, and task card `T010` by `SEMULITH-TREES.2`.
