# DSP-REVIEW: put real DSP pressure on the abstraction before it is stable

## Metadata

- Tree ID: `DSP-REVIEW`
- Status: `active` (`.1` landed `2026-09-30`)
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
  Status: `done` (`2026-09-30`)
  Goal: operand, product, accumulator, guard and output widths; fractional formats and where scaling is applied (catalog questions 1–2).
  Acceptance: each answer carries a manual locator; "absent" is a legitimate, recorded answer.
  Result: met, `2026-09-30`. The three catalogued TI C6000 manuals measured by text
  extraction (every fact quoted with its printed page + section; absences measured by
  named searches). Headline findings: **no accumulator and no guard bits anywhere**
  (measured absent in all three — accumulation is explicit ADDs); 40-bit "long" values in
  odd:even register pairs with a zero-fill rule (all three), 64-bit pairs (all three),
  128-bit quadruplets (C66x only); Q-notation nearly absent (Q31 exactly once, C66x's
  QSMPY32R1) with scaling INSTRUCTION-encoded (the S-family's <<1+saturate) — and one
  measured trap avoided: the opcode maps' `s` bit is the A/B side-select, NOT a scaling
  bit. The first classification (for `.7`): register GROUPING with a width+fill rule is
  the one candidate abstraction change; no accumulator/guard state is needed for these
  targets. Evidence document: [`artifacts/dsp-review/2026-09-30-widths-q1-q2.md`](artifacts/dsp-review/2026-09-30-widths-q1-q2.md).
  Lessons: `promotion: declined (the locator discipline is the leaf's own acceptance; the side-select trap is recorded in the evidence document where the next reader meets it)`.

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
| 1 | `DSP-REVIEW.2` | `pending` | `.1` done `2026-09-30` (widths measured across the three catalogued TI manuals, locators on every fact) — rounding/saturation/sticky flags (questions 3–5) build on the measured widths |

## Decisions

- `2026-09-13`: DSP work is **not** postponed until after Linux. Architectural pressure is
  applied early; a large unverified DSP implementation is not made mandatory (`ROADMAP.md` §2).

## Open Questions

- Which real DSP, if any, gets a bounded slice in `P3-BREADTH`? Resolved by whether an evidence
  path can be demonstrated — not by which manual is easiest to read (`RK08`).

## Blockers

- ~~`P1-LAB` gate `G1`.~~ Resolved: G1 reads `passed` since `2026-09-30` (`P2-SCALAR.5`).

## Acceptance Checklist (leaf DSP-REVIEW.1)

- [x] **REPRODUCE / ISSUE** — the leaf's premise (the manuals carry these facts) was
  measured by extraction, not trusted from memory:

  ```
  $ pdftotext .materials/ti/c64x-spru732j.pdf target/dsp-review/c64x-spru732j.txt   # +
    the c66x/c674x pair; 33042 / 49209 / 36598 text lines, page footers intact
  $ grep -ci 'guard' target/dsp-review/c64x-spru732j.txt
  1        # the legal boilerplate — the measured ABSENCE of guard bits
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; the leaf is a measured survey. WHY the
  one trap matters: the opcode maps' `s` bit reads like a scaling bit and is the A/B
  side-select (the MVC instruction text) — a misreading would invent a scaling mode that
  does not exist. WHERE the evidence lives: the artifact document with per-fact
  locators, cited from the leaf's Result. The measured Q-notation scarcity:

  ```
  $ grep -c 'Q31' target/dsp-review/c66x-sprugh7.txt   # the untracked extraction
  1        # Q31 appears exactly once, in the only manual that names a Q format
  $ grep -c 'Q31' target/dsp-review/c64x-spru732j.txt target/dsp-review/c674x-sprufe8b.txt
  target/dsp-review/c64x-spru732j.txt:0
  target/dsp-review/c674x-sprufe8b.txt:0
  ```

- [x] **FIX** — the evidence document
  `docs/tasks/artifacts/dsp-review/2026-09-30-widths-q1-q2.md` (the measured answers,
  the measured absences, the first classification), the leaf's Result, the tree's
  status/frontier/blocker repair (G1 long resolved).

- [x] **ADDRESSED (verified)** — every Q1/Q2 answer carries its manual + printed page +
  section; the absences are measured (`guard` 1 boilerplate hit, `Q15` 0 hits in all
  three, `Q31` exactly 1 hit in C66x); the classification candidates are stated for
  `.7`. No code changed — the guard set re-run:

  ```
  $ make gate             # all doctrines green
  $ make book             # both books render
  ```

- [x] **NO REGRESSION** — docs-only leaf; the gate is the check, re-run and green:

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

  The one correctness hazard of a review leaf — quoting from memory — was excluded by
  method: every fact extracted from the text layer and quoted.

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (the DSP
  row moves to In Progress), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md`
  (frontier `.2`), this tree, the artifact document.

## Acceptance Checklist (template for later leaves)

- [ ] **ROOT CAUSE (WHY + WHERE)** — <the command run and its real output>
- [ ] **ADDRESSED (verified)** — <measured before → after>
- [ ] **NO REGRESSION** — <the suite or gate re-run, and its result>
- [ ] **FIX** — <the change made>
- [ ] **LOCKSTEP** — <docs, contracts and indexes updated>

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-30` | `DSP-REVIEW.1` | the extraction (`pdftotext` of the three catalogued manuals) + the absence searches | every Q1/Q2 fact quoted with page+section; `guard`/`accumul`/`Q15` measured absent; the `s`-bit trap measured (side-select, not scaling) |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `DSP-REVIEW.1` | `SEMULITH-DR-0085 (leaf DSP-REVIEW.1): widths and accumulator semantics measured across the three TI manuals` | the evidence document with per-fact locators; the first classification for `.7`; the measured absences (no accumulator, no guard bits) |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P3 (the D node), catalog §5, and task card `T010` by `SEMULITH-TREES.2`.
