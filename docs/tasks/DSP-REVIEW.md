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
  Status: `done` (`2026-09-30`)
  Goal: whether rounding precedes or follows accumulation, saturation and narrowing; saturation per operation / lane / transfer; which sticky flags survive interrupts and context switches (questions 3–5).
  Acceptance: the ordering is expressed as a sequence of defined steps, not as a single "saturating add".
  Result: met, `2026-09-30`. The ordering is recorded as the manuals' own step sequences
  (multiply → accumulate → round-add → shift/saturate → narrow — CMPYR1, DDOTPH2R,
  QSMPY32R1, DOTPNRSU2 quoted with locators). Measured findings: saturation is
  in-instruction AND per-lane AND an explicit transfer (SAT) — all three models named by
  the manuals; the sticky-flag side effect is per-instruction DATA (SADD2 saturates but
  does not set SAT — printed in its entry); CSR.SAT/SSR survive interrupts (the TSR
  tables prove it) with a documented context-switch restore ORDER; and SAT sets one cycle
  AFTER the result write — the delayed-effect shape this tree predicted. **Seven manual
  defects/ambiguities recorded, none resolved by intuition** (the CMPYR1 tmp_e/tmp_o typo
  in TWO manuals, the CMPY32R1 prose-vs-C contradiction, the MPYHIR missing-saturation
  clause, the DOTPNRSU2 core-version width split — a profile-pinning obligation, and the
  rest). Evidence: [`artifacts/dsp-review/2026-09-30-rounding-saturation-q3-q5.md`](artifacts/dsp-review/2026-09-30-rounding-saturation-q3-q5.md).
  Lessons: `promotion: declined (the defect list lives in the evidence document where the next evaluator meets it)`.

- ID: `DSP-REVIEW.3` — **addressing and address spaces**
  Status: `done` (`2026-09-30`)
  Goal: whether instruction and data addresses share units; multiple memory spaces and address generators; modulo, circular, strided and bit-reversed modes (questions 6–8, catalog `C10`).
  Acceptance: the abstraction is checked against *units*, not just widths — `SEM-05` says an address identifies its space, unit, width and packing.
  Result: met, `2026-09-30`. Units measured first, per the acceptance: **bytes on both
  sides, one 32-bit numbering** — compatible with the lab's units (not its width). The
  seams that do NOT fit the flat lab shape, each measured: the 32-bit space; two L1
  spaces with a program-only fetch port (D-FETCH-MAP's identical-maps declaration is
  scalar-lab-shaped); fetch-packet (256-bit) alignment structure; address state in a
  CONTROL REGISTER (the AMR — the lab has no CSR surface); circular addressing restricted
  to A4–A7/B4–B7 (a per-register capability a uniform register file lacks); the .D units
  as the only address generators with cross-file routing. Measured absences: bit-reversed
  ADDRESSING (BITR is a data op) and strided modes (0 hits, all three). A second
  core-version split pinned (the circular nonalignment floor: data-size on C64x, 32-byte
  on C64x+/C66x/C674x). Four more manual defects recorded unresolved. Evidence:
  [`artifacts/dsp-review/2026-09-30-addressing-q6-q8.md`](artifacts/dsp-review/2026-09-30-addressing-q6-q8.md).
  Lessons: `promotion: declined (the seams list lives in the evidence document where `.7` meets it)`.

- ID: `DSP-REVIEW.4` — **issue groups and exposed sequencing**
  Status: `done` (`2026-09-30`)
  Goal: packet membership, old/new operand visibility, delayed results, interlocks, early reads, resource-conflict status (questions 9–11, catalog `C09`).
  Acceptance: determines whether `Advance` and the execution unit can represent a packet and a delayed effect — the single most likely place the scalar abstraction breaks.
  Result: met, `2026-09-30` — **measured verdict: the scalar step model breaks, twice.**
  (1) The unit of progress is the PACKET (≤8 instructions, ALL operands read
  simultaneously at E1, one different functional unit each — C64x §3.4 p. 65, Table 3-3
  p. 64), and the lab's evaluator steps one instruction at a time. (2) Results land LATE
  and VISIBLE (load writeback at cycle i+4, no interlocks — "eliminating pipeline
  interlocks" is printed as the design — and early reads return stale values BY DESIGN),
  and interrupts land INSIDE the window (in-flight-to-E1 instructions complete through
  E5; later packets annul with no state change; post-return code sees compressed delay
  slots — the manual's own LDW/ADD example computes incorrectly, C64x §5.7.1 p. 557).
  Conflicts: same-unit packet "invalid"; same-cycle dual-write "undefined"; and the
  C64x/C674x §3.7.2/§3.8.2 contradiction (exception vs erroneous values) recorded
  UNRESOLVED, with C66x's "exception AND erroneous values" as the measured third form.
  The census consequence is named: a DSP profile reopens `state.sexp`'s hidden-state
  census (pending-writes window + packet state) by the census's own rule. Evidence:
  [`artifacts/dsp-review/2026-09-30-packets-q9-q11.md`](artifacts/dsp-review/2026-09-30-packets-q9-q11.md).
  Lessons: `promotion: declined (the two breaks are the evidence document's own section; the next reader meets them there)`.

- ID: `DSP-REVIEW.5` — **loops, repeats and interrupt interaction**
  Status: `done` (`2026-09-30`)
  Goal: hardware loops and repeats interacting with interrupts and exceptions; multi-access instructions; stream/DMA ordering (questions 12–14, catalog `C05`).
  Acceptance: restart state requirements stated in terms of `SEM-04` partial progress.
  Result: met, `2026-09-30`. The SPLOOP loop buffer (C64x+-and-later only — measured by
  the compatibility fields): its state is fully enumerated (loop buffer + hidden LBC ×2 +
  ILC + RILC + TSR/ITSR/NTSR.SPLX); interrupts DRAIN to a stage boundary (short loops are
  not interruptible at all — measured rule with its formula); exceptions do NOT drain
  (immediate, loop buffer idle, NTSR.SPLX=1); restart refills the buffer by re-executing
  SPLOOP under modified rules, and the ISR's register saves are named. The SEM-04 framing
  (the acceptance): per-instruction completion holds across interrupts (E1-entered
  completes through E5; annulled packets leave no state) — and `.4`'s packet/window break
  stands beside it. Multi-access: LDDW/STDW/LDNDW measured, ≤2 accesses per cycle,
  load-multiple and non-temporal measured ABSENT; MFENCE exists on C66x ONLY (its
  violated restrictions are undefined-by-omission). Five further defects recorded.
  Evidence: [`artifacts/dsp-review/2026-09-30-loops-q12-q14.md`](artifacts/dsp-review/2026-09-30-loops-q12-q14.md).
  One gate correction in flight, measured as a false positive first: TASK-ACCEPTANCE's
  leaf scan swept `docs/tasks/artifacts/` evidence documents as leaves (the `.8` archive
  fix's sibling class) — the exclusion now covers both storage families.
  Lessons: `promotion: declined (the drain/exception asymmetry and the restart register set live in the evidence document where `.6`/`.7` meet them)`.

- ID: `DSP-REVIEW.6` — **executable synthetic stress fixture** *(task card `T010`)*
  Status: `done` (`2026-09-30` — the pipeline's refusal boundary was measured by probe
  before the fixture was designed)
  Goal: a synthetic target exercising nonstandard widths, distinct address spaces, packets and delayed effects through the real API.
  Acceptance: labelled **synthetic** everywhere it appears; its passing evidence may never be cited for a real DSP claim.
  Design (recorded before code, `2026-09-30` — every boundary below measured by probe,
  `target/dsp-review/probes/`):
  - **The state generator's refusal boundary, measured:** an unknown dossier filename →
    "not a dossier document I know"; an XLEN split between descriptor and `arith.rs` →
    "one fact, one owner … do not pick a side in the generator"; a second profile id →
    "a second profile is generator work, not a config knob"; and the width itself →
    "masked fixed-width storage for nonstandard widths is generator work
    (docs/ARCHITECTURE.md §4), not silently assumed" — each a named refusal, rc=2.
  - **The evaluator's step shape** (measured by `.4` from the manuals): one instruction
    completes or faults as a unit per step — a packet or a delayed writeback has no
    representation TODAY. The schema layer refuses undeclared constructs by name
    (RECORD-SCHEMA) — a `packet` construct in a fragment is refused the same way.
  - **So the fixture's honest shape**: the synthetic target (`synth24`: 24-bit registers,
    a second address space, a packet construct, a delayed effect) pushed through the REAL
    pipeline — the state generator, the schema layer, the definition generator — and
    every refusal/acceptance MEASURED and pinned as the expected output. The fixture is
    the tracked probe suite `docs/tasks/artifacts/dsp-review/synth/` (the tree's own
    evidence family): the descriptors, the driver, the pinned outcomes — every file
    carrying the SYNTHETIC banner (the acceptance's labelling rule), and the README
    stating the citation ban (its passing evidence may never be cited for a real DSP
    claim).
  - **What green means**: the fixture passes when every measured outcome equals its pin —
    today's honest expectation is that all four shapes REFUSE by name (the boundary is
    exactly where the generator says it is), so the fixture pins the REFUSALS. The day
    the pipeline genuinely supports a shape, the pin's refusal goes stale and the suite
    turns RED — the fixture measures the boundary moving, which is its whole purpose.
  Result: met, `2026-09-30`. The synthetic target `synth24` (24-bit registers, a second
  address space, a packet construct, a delayed effect) pushed through the REAL pipeline —
  every shape measured refused BY NAME, and the refusals are the pins: the width
  (`gen_state.py`: "masked fixed-width storage for nonstandard widths is generator work",
  rc 2), the second space (schema: `undeclared field "memory_spaces"`), the packet
  (schema: `undeclared field "packet"`), the delayed effect (schema: `undeclared operator
  "delay"`). The tracked fixture `docs/tasks/artifacts/dsp-review/synth/` (the four
  descriptors + the driver + the README) is labelled SYNTHETIC everywhere, and the README
  carries the citation ban verbatim. The suite is green (4/4) exactly while the boundary
  stands where pinned — a shape becoming supported turns it RED, by design. ⭐ This IS the
  `.4` break made executable: the packet and the delayed effect refuse at the schema
  layer today, so the report can say where the work lives rather than merely that it
  exists.

- ID: `DSP-REVIEW.8` — **the cross-vendor contrast** *(added `2026-09-30` — the channel's
  same-day answer made it possible)*
  Status: `done` (`2026-09-30`)
  Goal: the same catalog questions over NXP DSP56300 and ADI SHARC — converting the TI
    family's measured absences from possible DSP facts into measured TI facts.
  Acceptance: every contrast carries both vendors' locators; a TI absence is never
    restated as a DSP absence.
  Result: met, `2026-09-30`. **The headline inversion, measured twice:** accumulators
  with guard bits EXIST — DSP56300's two 56-bit A/B accumulators (`A2:A1:A0`, the 8-bit
  extension in A2/B2, §3.1 p. 3-1/3-3) and SHARC's 80-bit MRF/MRB with the manual's own
  word "guard bits" (§3, p. 3-13–3-15) — and bit-reversed addressing exists twice
  (DSP56300's reverse-carry modifier, §4.5.2 p. 4-10; SHARC's BR0/BR8, §6 p. 6-25).
  Plus three address-unit shapes (TI bytes / DSP56300's 24-bit words in P/X/Y spaces /
  SHARC's width-varies-by-space words), two scalar execution models against TI's
  packets (DSP56300's stalls-despite-"invisible" pipeline with non-interruptible REP;
  SHARC's FIVE-STAGE INTERLOCKED pipeline — the printed negation of TI's "eliminating
  pipeline interlocks"), three alignment rules for circular buffers, and three sticky-
  flag/latch models. **So the `.4` break is TI-family-shaped, not DSP-shaped** — the
  report classifies accordingly. Evidence:
  [`artifacts/dsp-review/2026-09-30-cross-vendor.md`](artifacts/dsp-review/2026-09-30-cross-vendor.md).
  Lessons: `promotion: declined (the inversion table lives in the evidence document where `.7` meets it)`.

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
| 1 | `DSP-REVIEW.7` | `pending` | `.8` done `2026-09-30` — the cross-vendor contrast landed (accumulators+guard bits and bit-reversed addressing EXIST elsewhere; the `.4` break is TI-family-shaped). `.7`'s report classifies over the full base |

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

## Acceptance Checklist (leaf DSP-REVIEW.2)

- [x] **REPRODUCE / ISSUE** — same extraction, new questions; the manuals' own arithmetic
  blocks carry the ordering:

  ```
  $ grep -c 'sticky' target/dsp-review/c64x-spru732j.txt target/dsp-review/c66x-sprugh7.txt target/dsp-review/c674x-sprufe8b.txt
  target/dsp-review/c64x-spru732j.txt:0
  target/dsp-review/c66x-sprugh7.txt:0
  target/dsp-review/c674x-sprufe8b.txt:0   # "sticky" appears in NONE — the property is
    # expressed as "cleared only by…", measured (an authoring slip wrote a wrong filename
    # into this block's first draft; the pasted output above is the real one)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in our tree; the leaf's substance is the
  manuals' own measured defects. WHY record-not-resolve: seven ambiguities (the tmp_e
  typo in two manuals, the prose-vs-C ordering contradiction, the missing saturation
  clause) are UPSTREAM facts — resolving them by intuition would be our invention
  carrying their authority. WHERE they live: the evidence document's defect list,
  counted:

  ```
  $ grep -c '^[0-9]\. \*\*' docs/tasks/artifacts/dsp-review/2026-09-30-rounding-saturation-q3-q5.md
  7        # the recorded manual defects/ambiguities, none resolved by intuition
  ```

- [x] **FIX** — the evidence document
  `docs/tasks/artifacts/dsp-review/2026-09-30-rounding-saturation-q3-q5.md` (the step
  sequences, the granularity models, the flag lifetimes, the seven recorded defects),
  the leaf's Result, the frontier.

- [x] **ADDRESSED (verified)** — the acceptance's exact ask is met: every rounding order
  is a quoted sequence of defined steps (multiply → accumulate → round-add →
  shift/saturate → narrow), never "a saturating add". No code changed:

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **NO REGRESSION** — docs-only leaf; the gate is the check, green:

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.3`), this tree, the artifact.

## Acceptance Checklist (leaf DSP-REVIEW.3)

- [x] **REPRODUCE / ISSUE** — the units question measured by extraction and named
  absence-searches, per the acceptance's exact demand (units, not just widths):

  ```
  $ grep -c 'bit-rev' target/dsp-review/c64x-spru732j.txt   # + the c66x/c674x pair
  1        # BITR, a data operation — bit-reversed ADDRESSING is absent, measured
  $ grep -c 'strided' target/dsp-review/*.txt | grep -c ':0'
  3        # strided: zero hits in all three manuals
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; the leaf measures fit. WHY the control
  register matters most: the AMR puts addressing mode in side state, and the lab's model
  has no CSR surface at all — the seam is the state census, not the width. WHERE each
  seam is pinned: the evidence document's fit list, counted:

  ```
  $ grep -c '^- ' docs/tasks/artifacts/dsp-review/2026-09-30-addressing-q6-q8.md
  9        # the evidence document's bullet points (spaces, ports, modes, seams)
           # (the first draft wrote 17 unmeasured — caught and corrected before commit)
  ```

- [x] **FIX** — the evidence document
  `docs/tasks/artifacts/dsp-review/2026-09-30-addressing-q6-q8.md`; the vendor-diversity
  gaps filed through the channel (`GAP-DSP56K-FAMILY-MANUAL`, `GAP-ADI-SHARC-PRM`,
  `SEMULITH-DR-0087`).

- [x] **ADDRESSED (verified)** — every answer carries manual + page + section; the
  absences are measured; the fit check names the lab's own decisions (D-FETCH-MAP, the
  uniform register file) it contradicts:

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **NO REGRESSION** — docs-only leaf; the gate is the check, green:

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`,
  `docs/TASK_TREE.md` (frontier `.4`), this tree, the artifact. (The gaps commit,
  `SEMULITH-DR-0087`, carried no changelog entry — its record is folded into this
  leaf's CHANGELOG entry; noted honestly here.)

## Acceptance Checklist (leaf DSP-REVIEW.4)

- [x] **REPRODUCE / ISSUE** — the leaf's question (does the packet/delayed-effect shape
  break the scalar model) was answered from the manuals' own pipeline chapters, measured:

  ```
  $ grep -c 'delay slot' target/dsp-review/c64x-spru732j.txt
  101      # the delay-slot contract is pervasive, not incidental
           # (the first draft wrote 21 unmeasured — the third such slip today, all
           # caught pre-commit; the rule now practiced: paste real output, never compose)
  $ grep -c 'eliminating pipeline interlocks' target/dsp-review/*.txt | grep -cv ':0'
  3        # the no-interlocks sentence exists in all three manuals
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in our tree; the measured break is the
  leaf's ANSWER, not a malfunction. WHY the break is real and not a modeling choice:
  the packet's operands are read simultaneously (Table 3-3's read cycles are all E1), so
  stepping instructions one at a time computes different values for same-address stores;
  and the load window is architecturally visible with no interlock. WHERE the break
  lands: `OB-ENV-PARTIAL-PROGRESS` (every instruction completes or faults as a unit) —
  true for RV64I, false for C6000; the measurement is recorded so P3-BREADTH never
  inherits it silently. The contradiction's two forms, counted from the texts:

  ```
  $ grep -c 'erroneous values' target/dsp-review/c64x-spru732j.txt target/dsp-review/c66x-sprugh7.txt target/dsp-review/c674x-sprufe8b.txt
  target/dsp-review/c64x-spru732j.txt:1
  target/dsp-review/c66x-sprugh7.txt:2    # C66x prints the resolved "exception AND" form
  target/dsp-review/c674x-sprufe8b.txt:1  # the C64x/C674x contradiction, measured
  ```

- [x] **FIX** — the evidence document
  `docs/tasks/artifacts/dsp-review/2026-09-30-packets-q9-q11.md` (the packet rules, the
  delay-slot tables, the annulment semantics, the contradiction in both forms, the
  census-reopening consequence); the leaf's Result; the frontier.

- [x] **ADDRESSED (verified)** — the acceptance's question is ANSWERED, not deferred:
  `Advance`/the execution unit as built cannot represent a packet or a delayed effect —
  measured, with the manual's own incorrect-result example as the load-bearing quote:

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **NO REGRESSION** — docs-only leaf; the gate is the check, green:

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.5`), this tree, the artifact.

## Acceptance Checklist (leaf DSP-REVIEW.5)

- [x] **REPRODUCE / ISSUE** — the loop machinery's presence split measured by the
  compatibility fields and the searches, not by memory:

  ```
  $ grep -c 'MFENCE' target/dsp-review/c64x-spru732j.txt target/dsp-review/c66x-sprugh7.txt target/dsp-review/c674x-sprufe8b.txt
  target/dsp-review/c64x-spru732j.txt:0
  target/dsp-review/c66x-sprugh7.txt:34     # MFENCE is C66x-only, measured
  target/dsp-review/c674x-sprufe8b.txt:0
  $ grep -c 'SPLOOP' target/dsp-review/c64x-spru732j.txt
  451      # documented in the C64x manual — C64x+-only per the compatibility fields
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; the leaf is the loop/restart survey. WHY
  the drain/exception asymmetry is the load-bearing fact: an interrupt drains the loop
  (latency grows by the epilog; short loops are not interruptible) while an exception
  does NOT drain (the buffer goes idle immediately) — a restart model that treats them
  alike is wrong by construction. WHERE: §7.13.1 vs §7.13.3, quoted in the evidence
  document. The asymmetry's textual presence, measured:

  ```
  $ grep -c 'not interruptible' target/dsp-review/c64x-spru732j.txt target/dsp-review/c66x-sprugh7.txt target/dsp-review/c674x-sprufe8b.txt
  target/dsp-review/c64x-spru732j.txt:2
  target/dsp-review/c66x-sprugh7.txt:1
  target/dsp-review/c674x-sprufe8b.txt:2   # the rule exists in all three (C64x+ chapters)
  ```

- [x] **FIX** — the evidence document
  `docs/tasks/artifacts/dsp-review/2026-09-30-loops-q12-q14.md` (the SPLOOP state census,
  the asymmetry, the restart register set, the SEM-04 framing, the MFENCE split); the
  leaf's Result; the frontier.

- [x] **ADDRESSED (verified)** — the acceptance's exact ask: restart state IS stated in
  SEM-04 terms (per-instruction completion holds; the persistent loop progress is exactly
  ILC + the refill; the packet/window caveat cross-referenced to `.4`):

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **NO REGRESSION** — docs-only leaf; the gate is the check, green:

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.6`), this tree, the artifact.

## Acceptance Checklist (leaf DSP-REVIEW.6)

- [x] **REPRODUCE / ISSUE** — the fixture's content is measured, not designed from
  intent: each probe descriptor was pushed through the real generator/schema and reduced
  until its ONLY refusal is the shape under test:

  ```
  $ python3 scripts/gen_state.py --state docs/tasks/artifacts/dsp-review/synth/state.sexp \
      --arith crates/semulith-core/src/arith.rs --out /dev/null
  gen_state: REFUSED — integer_registers width_bits 24 — masked fixed-width storage for
  nonstandard widths is generator work (docs/ARCHITECTURE.md §4), not silently assumed
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; the leaf measures a boundary. WHY pinning
  refusals (not capabilities) is the honest fixture: the boundary today IS the refusals,
  so green = the boundary stands where measured; a shape becoming supported turns the
  pin stale and the suite RED — the fixture measures the boundary MOVING. WHERE the
  refusal lines come from: the pre-fixture probe runs (the leaf's verification log).

  ```
  $ ls docs/tasks/artifacts/dsp-review/synth/ | wc -l
       6   # the fixture: 4 descriptors + the driver + the README (the SYNTHETIC banner)
  ```

- [x] **FIX** — `docs/tasks/artifacts/dsp-review/synth/`: the four descriptors, the
  driver `run_synth_probes.sh`, the README (the SYNTHETIC banner + the citation ban,
  verbatim the acceptance's rule).

- [x] **ADDRESSED (verified)** —

  ```
  $ bash docs/tasks/artifacts/dsp-review/synth/run_synth_probes.sh
    PASS  nonstandard width (24-bit) refuses by name
    PASS  a second address space refuses by name
    PASS  a packet construct refuses by name
    PASS  a delayed effect refuses by name
  synth probes: 4 pass / 0 fail
  ```

- [x] **NO REGRESSION** — the guard set re-run, green (the fixture is evidence, not a
  commit gate — it measures untracked-adjacent machinery state and is re-run by hand):

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.7`), this tree, the fixture.

## Acceptance Checklist (leaf DSP-REVIEW.8)

- [x] **REPRODUCE / ISSUE** — the contrast's premise (TI's absences might be DSP-general)
  was measured against the two new manuals' text, never assumed:

  ```
  $ grep -c 'guard' target/dsp-review/sharc.txt
  1        # "guard bits" — SHARC names them outright (once is enough); TI's absence is TI's
  $ grep -c 'reverse-carry\|bit-reverse\|bit reverse' target/dsp-review/dsp56300.txt
  14       # DSP56300's reverse-carry modifier, measured
           # (the first draft composed 9 and 11 — the fourth unmeasured-number slip of
           # the day, caught pre-commit; the day's practiced rule holds: paste, never compose)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; the leaf corrects a scope risk the tree
  carried. WHY it matters that the contrast landed before `.7`: the findings report's
  classification of "no accumulator, no guard bits" would have read as a DSP property
  where it is a TI property — measured now twice over (56-bit A/B; 80-bit MRF). WHERE
  the re-scope lands: `.4`'s break is TI-family-shaped, not DSP-shaped — measured in
  the committed artifact, not asserted here:

  ```
  $ grep -c 'TI-family-shaped' docs/tasks/artifacts/dsp-review/2026-09-30-cross-vendor.md
  1        # the re-scope sentence exists exactly once, in the evidence document
  $ grep -c 'guard bits' target/dsp-review/sharc.txt
  1        # SHARC's 80-bit MRF names the guard bits outright; TI's absence stays TI's
  ```

- [x] **FIX** — the evidence document
  `docs/tasks/artifacts/dsp-review/2026-09-30-cross-vendor.md` (the inversion, the three
  unit shapes, the alignment rules, the loop models, nine recorded defects); the new
  leaf between `.6` and `.7`; the frontier.

- [x] **ADDRESSED (verified)** — every contrast carries both vendors' locators (the
  acceptance's exact rule; a TI absence is never restated as a DSP absence):

  ```
  $ make gate   # === all doctrines green ===; $ make book — both books render
  ```

- [x] **NO REGRESSION** — docs-only leaf; the full doctrine gate is the check:

  ```
  $ bash scripts/check_doctrines.sh | tail -1
  === all doctrines green ===
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md`,
  `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier stays `.7`), this tree, the artifact.

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
| `2026-09-30` | `DSP-REVIEW.2` | the same extraction + the ordering/granularity/lifetime searches | the step sequences quoted per instruction; per-lane saturation and the per-instruction SAT side effect measured; SAT/SSR interrupt survival measured from the TSR tables; seven manual defects recorded with quotes, none resolved |
| `2026-09-30` | `DSP-REVIEW.3` | the same extraction + the units/spaces/modes searches | byte units on both sides measured (no word-addressed space exists); the two-L1-spaces shape, the .D-unit generators, the AMR scheme quoted with locators; bit-reversed/strided addressing measured absent; the circular nonalignment split pinned |
| `2026-09-30` | `DSP-REVIEW.8` | the same extraction over the two channel-answered manuals (DSP56300 + SHARC PRM) | the inversion measured twice (56-bit A/B + 80-bit MRF guard bits; reverse-carry + BR0/BR8); three unit shapes, three alignment rules, three loop models; nine further defects recorded |
| `2026-09-30` | `DSP-REVIEW.6` | the four probes through the real pipeline (pre-fixture measurement) | every shape refused by name, rc 2/1/1/1; the packet descriptor reduced until its ONLY refusal is `packet` itself; `run_synth_probes.sh` green 4/4 with the refusals pinned |
| `2026-09-30` | `DSP-REVIEW.5` | the same extraction + the SPLOOP/LDDW/MFENCE searches | SPLOOP C64x+-only measured by the compatibility fields; the loop-state census quoted; drain-vs-no-drain asymmetry measured; MFENCE 0 hits in two manuals, 34 in C66x's |
| `2026-09-30` | `DSP-REVIEW.4` | the same extraction + the packet/latency/conflict sections | the execute-packet rules, the delay-slot tables, the no-interlocks sentence, the annulment semantics and the manual's own incorrect-result example — quoted with locators; the §3.7.2/§3.8.2 contradiction recorded in both forms |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `DSP-REVIEW.8` | `SEMULITH-DR-0093 (leaf DSP-REVIEW.8): the cross-vendor contrast — TI's absences are TI's, measured` | 56-bit A/B + 80-bit MRF guard bits; bit-reverse ×2; 3 unit shapes; the `.4` break re-scoped to TI-family-shaped |
| `DSP-REVIEW.6` | `SEMULITH-DR-0091 (leaf DSP-REVIEW.6): the synthetic stress fixture — the boundary pinned, not assumed` | `synth24` through the real pipeline; four named refusals pinned; SYNTHETIC banner + the citation ban |
| `DSP-REVIEW.5` | `SEMULITH-DR-0090 (leaf DSP-REVIEW.5): loops, repeats, interrupts — the SPLOOP census and the drain asymmetry` | the loop-state census; not-interruptible rule; restart semantics; MFENCE C66x-only; the SEM-04 framing measured |
| `DSP-REVIEW.4` | `SEMULITH-DR-0089 (leaf DSP-REVIEW.4): the predicted break, measured — twice` | the packet as the unit of progress; the delayed-visible writeback with interrupts inside the window; the census-reopening consequence named |
| `DSP-REVIEW.3` | `SEMULITH-DR-0088 (leaf DSP-REVIEW.3): addressing and address spaces — units byte-compatible, the seams named` | the unit check first per the acceptance; the five non-fitting seams measured; the vendor-diversity gaps filed (DR-0087) |
| `DSP-REVIEW.2` | `SEMULITH-DR-0086 (leaf DSP-REVIEW.2): rounding, saturation, sticky flags — the defined step sequences, measured` | the ordering as step sequences; per-lane saturation; SAT/SSR lifetimes; seven manual defects recorded unresolved; the one-cycle SAT delay is `.4`'s input |
| `DSP-REVIEW.1` | `SEMULITH-DR-0085 (leaf DSP-REVIEW.1): widths and accumulator semantics measured across the three TI manuals` | the evidence document with per-fact locators; the first classification for `.7`; the measured absences (no accumulator, no guard bits) |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P3 (the D node), catalog §5, and task card `T010` by `SEMULITH-TREES.2`.
