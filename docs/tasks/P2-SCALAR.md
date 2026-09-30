# P2-SCALAR: validate the first RV64I profile

## Metadata

- Tree ID: `P2-SCALAR`
- Status: `active`
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
  Status: `done` (`2026-09-29`)
  Goal: every remaining selected RV64I form, not just the mnemonics already exercised.
  Acceptance: coverage reported with its **denominator**; `SCP-02`'s dependency closure holds.
  Design: recorded before code; archived to [`archive/P2-SCALAR-designs.md`](archive/P2-SCALAR-designs.md) (per-part ceiling).
  Result: met, `2026-09-29`. **52/52 declared forms exercised, with the denominator, gated.**
  The coverage instrument fired RED against the real corpus before anything was built —
  15/52, all 37 missing forms named — and has read GREEN since: the 24th project doctrine
  `EXERCISE-COVERAGE`, self-test 7/0, mirrored per the registry rules. Five scope-completion
  guests landed with every expectation derived from the pinned specification before any run
  (`EVD-05`): `scope-alu` (31 steps), `scope-mem` (29; 17 census-pinned data crossings),
  `scope-branch` (19 from 24 instructions; five `never_written` negatives), `scope-ecall`
  and `scope-ebreak` (requested traps, cause/tval matching both references exactly). `fence`
  forced the honest path for its operands: `fm`/`pred`/`succ` now come from the pinned
  `arg_lut.csv` (fragment whitelist + assembler extended, both generated artifacts
  regenerated, no hand-typed opcode; the field-count pin moved 12→15). The trace adapter
  learned the measured ecall/ebreak spellings of sail 0.14 and spike 1.1.1-dev (unknown
  spellings raise). Two `sltu`/`sltiu` 0-results are pre-written with 1 because the
  observation vocabulary is the VISIBLE register change — an empty write would prove
  nothing. The live experiment: 9 guests, **117/117 aligned steps** against sail-riscv AND
  spike, byte-identical reproduction. One defect found in flight, logged above and routed
  to `.3` (reserved-`fm` FENCE nops; `D-FENCE` says illegal-instruction). The frontier
  moves to `.2` (boundary arithmetic and state interactions).
  Lessons: `promotion: declined (the lesson is mechanical where it bites — the commit gate fails any invisible expected write, measured this leaf)`.
  The leaf's one generalizable lesson — when the observation vocabulary is a diff, pre-write
  the destination or the step proves nothing — was enforced, not just noted: the offline
  differential failed the `sltu`/`sltiu` 0-results exactly so (`left: []` vs
  `right: [(13, 0)]`). A knowledge card would restate what the gate enforces; the doctrine
  row carries the coverage rule.

- ID: `P2-SCALAR.2` — **boundary arithmetic and state interactions**
  Status: `done` (`2026-09-29`)
  Goal: boundary values, sign/zero extension, shift corner cases, alias and overlap effects.
  Acceptance: exhaustive checks where a reduced width makes them tractable; source-linked expected values.
  Design: recorded before code; archived to [`archive/P2-SCALAR-designs.md`](archive/P2-SCALAR-designs.md) (per-part ceiling).
  Result: met, `2026-09-29`. **Five boundary guests, 259 new steps, all agreeing with
  sail-riscv AND spike — 376/376 aligned steps over the 14-guest corpus.** The 6-bit shamt
  domain is exhausted by `bound-shift`'s 64-point `srli` sweep and the 5-bit domain by
  `bound-shiftw`'s 32-point `sraiw` sweep, with every amount bit pinned on the remaining
  forms and the rs2 = 64 / 96 / -1 register-amount corners (the `srl`/`srlw` pair on rs2 =
  96 answers differently under the 6-bit and 5-bit reads, as designed). `bound-arith` pins
  the signed-extreme wraps on both the register and the immediate path, the *W wraps with a
  garbage upper half provably ignored, and `auipc 0x80000` wrapping the address sum to
  exactly 4·n (`D-ADDR-WRAP` inside `D-LUI-AUIPC`). `bound-ext` probes the sign edge at
  each width through sign/zero pairs (32 census-pinned crossings); `bound-alias` proves the
  little-endian lanes, overlap composition, register aliasing including a load over its own
  base register, and x0 in both directions (16 crossings). The commit gate caught two
  AUTHORING defects, never a model one: the overlap-composition constant was hand-assembled
  wrong twice (0x4CD's high byte is 0x04, not 0x4C; then the AA lane mis-placed one hex
  pair over) — each time the pinned expectation failed RED against the real model, the
  derivation was re-done from the spec rule (`SH` stores the low 16 bits, little-endian),
  and the corrected value is what the rule computes. The ceiling expansion landed as
  designed: `profiles/` 32 → 42 files / ~307 KB, registry ceilings 34 → 46 files and
  256 KiB → 384 KiB, per-part 32 KiB untouched (largest new file 27,848 B).
  Lessons: `promotion: declined (the commit gate fails any expected value the spec rule
  does not compute — it fired RED twice this leaf, on the author's own arithmetic; a
  knowledge card would restate what the gate enforces)`.

- ID: `P2-SCALAR.3` — **fault, suppression and reserved cases**
  Status: `done` (`2026-09-29`)
  Goal: fetch and access faults, suppressed effects, reserved encodings, controlled event boundaries.
  Acceptance: a failing access that already modified memory or a device is modelled as the source defines it (`SEM-06`, catalog `C11`); reserved cases keep their source meaning (`SEM-07`).
  Design: recorded before code; archived to [`archive/P2-SCALAR-designs.md`](archive/P2-SCALAR-designs.md) (per-part ceiling).
  Result: met, `2026-09-29`. **Eighteen fault guests, 78 new steps, all agreeing with
  sail-riscv AND spike — 454/454 aligned steps over the 32-guest corpus, byte-identical
  reproduction.** Both defect threads closed, in opposite directions. DEFECT-A was
  INVERTED by measurement: RVI-RV32I §1.1.7 mandates the reserved-FENCE-configuration
  nop verbatim, both references execute exactly as the model does, and `D-FENCE` (with
  its `REQ-D-FENCE`/`OB-FENCE` restatements) is corrected — the dossier was wrong, the
  model right, no encoding change was ever needed (`fault-fence` pins the corrected
  behavior three-way). DEFECT-B was real: the `jal`/`jalr` effect trees wrote the link
  before the target check; the fix is semantics DATA (`set-pc` first — the evaluator is
  untouched), and `fault-jal-mis`/`fault-jalr-mis` pin it with `never_written x5`,
  matching both references. The observation vocabulary learned the **word-less
  fetch-fault step** (`run::Step.word` → `Option<u32>`; the runner emits the trap with
  no word and keeps `Stop::FetchFault`; the CLI prints `(fetch fault)`; the sail
  adapter synthesizes the step at pc = tval, the spike adapter at an unrecorded epc for
  cause 0x01 alone) — `fault-fetch` compares three-way, closing the gap `run.rs` had
  named as future work. The **reserved-decode policy conversion** is the harness's
  explicit act in `run.rs` (never the interpreter): the reserved word becomes the
  illegal-instruction observation with tval = the word — measured identical on both
  references — while `Stop::Undefined` keeps the source classification (SEM-07);
  `fault-reserved` and `fault-shiftw-res` pin it, and the second **answers OQ-2**: both
  current references raise illegal-instruction on the imm[5] `*IW` shift, the previous
  spec text's behavior (`REQ-D-SHIFTW-RESERVED` is now `resolved`; `G0` shows one open
  question where there were two). The trace adapter learned four measured spellings
  (`misaligned-fetch`, `trap_instruction_address_misaligned`, `store/amo-access-fault`,
  `misaligned-store/amo`) — its refusal discipline fired mid-run on the last one,
  exactly as designed, before the guest pinned it. `riscv_asm.py` learned the `.word`
  directive for raw reserved words. `fence.i` executes on both references despite ISA
  strings excluding Zifencei — recorded as `DIFF-FENCEI-EXECUTED`, its guest routed to
  `.4`. The mutation/reduce suites' stale-by-design expectations were re-derived for
  the new tree shape and the policy-converted world (the SEM-02 arm's distinction now
  lives in the stop reason, where SEM-02 put it). Ceiling expansion landed as designed:
  `profiles/` 42 → 78 files / 367,466 B; registry ceilings 46 → 82 files and 393,216 →
  471,040 bytes; per-part 32,768 untouched (largest new file 4,017 B). The gate caught
  only AUTHORING slips, never another model defect: the systematic trailing-paren slip
  in all 18 expectation documents (check_sexp_schema RED on all 18), the store operand
  order in 4 guests (the pre-wiring dry-run), and the REQ-D-FENCE statement drift
  (RECORD-SCHEMA RED at the commit gate).
  Lessons: `promotion: declined (the instruments fired RED on the author's own slips —
  schema, dry-run, statement-drift, spelling-refusal — and each enforcement IS the
  lesson; a knowledge card would restate what the gates enforce)`.

- ID: `P2-SCALAR.4` — **the interaction matrix** — `G-INTERACTIONS`
  Status: `done` (`2026-09-29`)
  Goal: the declared fault × alias × boundary × event × progress × restart matrix, exercised.
  Acceptance: the matrix is declared first and then exercised; unexercised cells are reported, not omitted.
  Design: recorded before code; archived to [`archive/P2-SCALAR-designs.md`](archive/P2-SCALAR-designs.md) (per-part ceiling — moved there on `2026-09-30` to make room for the `.5` strand-2 design).
  Result: met, `2026-09-29`. **The 21-cell matrix is declared as tracked data and every
  cell resolves; eight new guests, 38 new steps — 492/492 aligned steps over the 40-guest
  corpus, byte-identical reproduction, plus the one declared expected divergence.** The
  matrix (`profiles/rv64i-lab-v0/interactions.sexp`, schema `schema/interactions.sexp`)
  declares the six grounded axes and the full upper triangle; the 25th project doctrine
  `INTERACTION-MATRIX` re-derives the 21 cells from the axes and refuses by name an
  omitted cell, an unresolved disposition, an orphan guest, or an unrecorded difference id
  — fired RED against the real corpus before registration (`NO MATRIX rv64i-lab-v0`),
  GREEN at 21/21 with zero orphans, self-test 12/0, mirrored per the registry rules. The
  eight guests pin the measured interactions: fault priority three-way (`it-prio-jump` —
  a misaligned AND unmapped jump target raises 0x00 on the jump, link suppressed;
  `it-prio-load` — the same double fault on a load raises 0x04 before the boundary is
  crossed), the fault×alias base preservation (`it-fault-alias` — `lw x5, x5, 1` traps and
  x5 survives), the address wrap INTO the fault on both paths (`it-fault-wrap-ld`,
  `it-fault-wrap-sd` — tval 0 three-way, the store kept below 2^56 by design after the
  probes found sail's 56-bit tval masking, recorded as `DIFF-TVAL-PHYS-MASK`),
  self-aliased operators at boundary values (`it-alias-bound`), the unbounded loop under
  the budget contract with the x0-discarded link (`it-progress-loop`, `Stop::Budget`, every
  iteration visible), and the `fence.i` expected divergence (`it-fencei`). The comparator
  learned the expected divergence: `expect_divergence` on the expectation document (schema
  + dossier round-trip), `compare_traces.py`'s `check_expected_divergence` (self-test
  16/0, +4 arms — an AGREE at the declared step is RED: a stale pin, not a good
  comparison), and the smoke run's four-step protocol — `it-fencei`: semulith meets its
  spec-derived expectations, the FIRST divergence against each reference lands at exactly
  step 1 with semulith carrying the policy trap, sail vs spike AGREE over their full 4
  steps (including the measured run-off-the-end illegal word), and
  `DIFF-FENCEI-EXECUTED` is recorded. `cross_model` stayed a comparison DISABLE. The
  restart axis is commit-gated as mechanism: the new offline determinism suite runs every
  guest twice from `zeroed_at(entry)` and asserts identical traces AND crossing logs, next
  to the smoke's reproduce leg. `run/tests.rs`: 157 → 166 suites (+8 guest suites, +1
  determinism suite); the mutation census pins all 8 new guests — six in the empty arm,
  the two wrap guests with their faulted crossings (the design said "all 8 join the empty
  arm"; the recorded crossings of a REFUSED access are pinned exactly like
  `fault-access-ld`/`-sd` — the design's operative constraint, "no new guest has a
  successful store crossing", holds). The design's 21-cell census named the distinguishing
  guests per cell; the orphan rule forced the 14 pre-existing guests it did not name into
  cells, assigned by the axes each genuinely exercises (fault guests whose trap IS the
  progress boundary → F×P; the boundary-valued arithmetic of `smoke-arith`/`bound-ext`/
  `scope-alu` → B×B; `scope-mem`'s one-address-many-widths reads → A×A; the loop guests →
  P×P) — stated here so the assignments are reviewable, not silent. One instrument RED in
  flight, on the author's own derivation: the gate's first GREEN run reported three
  phantom OMITTED CELLs because the derived cell set was built in declared-axis order
  while the document's cells normalize to sorted pairs — the derivation, not the document,
  was wrong; fixed in the gate, self-test still 12/0. Ceiling expansion landed as designed
  (see Decisions): `profiles/` 78 → 95 files / 402,967 B; registry ceilings 82 → 99 files
  and 471,040 → 516,096 bytes; per-part 32,768 untouched — which bit on
  `references.sexp` itself (31,434 + the new difference record), so the record was written
  tighter rather than the ceiling moved; the 25th doctrine row also crossed BOTH mirror
  caps (TOOLBOX.md 16,380/16,384 and DOCTRINE_ENFORCEMENT.md 24,573/24,576 at the
  boundary), re-derived to 20 KiB / 28 KiB on the row-count contract, the SEMILITH-PL-0001
  precedent.
  Lessons: `promotion: declined (the instruments fired RED on the author's own work — the
  gate's own cell-derivation order bug, the per-part ceiling the new difference record
  crossed — and each enforcement IS the lesson; a knowledge card would restate what the
  gates enforce)`.

- ID: `P2-SCALAR.5` — **external and directed campaigns** — `G-REGRESSION`
  Status: `done` (`2026-09-30` — all three strands landed: the C guest, the ACT4
  campaign, the eight directed guests)
  Goal: matched reference comparisons, configured external tests, directed sequence tests, and compiled freestanding programs.
  Acceptance: ACT4 results are recorded as **external tests with Sail-derived expected values**, never as a second independent semantics (`EVD-04`).
  Design (recorded before code, `2026-09-30` — three strands, each its own commit):
  1. **The C-toolchain guest** (flips G1 criterion 6). Tracked: `guests/c-scope.c` — a
     freestanding C tour of the declared scope (64/32-bit ALU, every load/store width,
     branches, function calls through JAL/JALR with a real stack, shifts), compiled
     `-march=rv64i -mabi=lp64 -nostdlib -ffreestanding` so the compiler may emit only
     RV64I, results retired into REGISTERS before the closing `ebreak` (the observation
     vocabulary is register writes; a result left only in memory would prove nothing —
     the `.1` lesson). Tracked build script compiles+links via the pinned toolchain
     (clang 21.1.8 + `ld.lld` 21.1.8, refusing by name if absent) into
     `target/refs/guests/c-scope.elf` — untracked, same standing as the reference
     binaries. `scripts/run_semulith_smoke.py` learns the `.c` path: build, then the same
     three-way first-divergence comparison and reproduce leg as the assembled guests.
     There is deliberately **no per-step expectation document** for the compiled guest —
     the compiler, not the author, chooses the instruction sequence; the evidence is the
     differential itself (`EVD-04` recorded: agreement is tested evidence for these
     inputs, never universal proof). `gate_report.py`'s criterion-6 probe already counts
     `guests/*.c`; its hardcoded NOT-met prose and the Limitations section gain the
     met/unmet branch, the met prose naming the guest, the toolchain pin and the re-run
     command, with GATE-REPORT self-test arms for both branches. Guest-corpus ceiling
     expansion is its own reviewed decision at commit time, per the `.1` rule.
  2. **The ACT4 external suite**: fetch the generated half (635 MB `.S` + 31 MB `.svh`,
     pinned upstream commit `e2216915d9a17acc142610831d88de8b65683866`), build the
     harness (gas-syntax sources assemble with the same pinned clang; the suite's
     signature mechanism adapts to the laboratory's observation vocabulary), run, record
     as external tests with Sail-derived expectations. Sized at strand time — if it
     outgrows a safe slice it becomes its own leaf.
  3. **Directed sequence tests**: the directed campaigns the matrix does not already
     cover, designed from the `.1`–`.4` evidence gaps.
  Strand 2 design: recorded before code `2026-09-30` (measured against the pinned fetch);
  archived to [`archive/P2-SCALAR-designs.md`](archive/P2-SCALAR-designs.md) (per-part ceiling) once the
  strand landed.
  Strand 1 landed `2026-09-30` (`SEMULITH-PS-0063`): `c-scope.c` retires three-way
  129/129; G1 reads `passed`. The model book's compiled-guest chapter landed with it
  (`SEMULITH-PS-0065`).
  Strand 2 slice (b) landed `2026-09-30` (`SEMULITH-PS-0067`): the observation vocabulary
  gained the store trace (`semulith run --trace-stores` surfaces the runner's crossing
  log — observability, not semantics), the DUT-side pieces stand
  (`profiles/rv64i-lab-v0/act4/`: `rvtest_config.h`, `rvmodel_macros.h`, `link.ld`),
  `scripts/fetch_act4.sh` is the reproducible acquisition route (pin-verified, census
  51/18,092), and `scripts/run_act4_campaign.py` builds and runs `I-add-00` end-to-end
  three-way: both toolchain risks retired by measurement (clang 21.1.8 assembles the
  suite's macro machinery clean; sail 0.14's HTIF terminates under the laboratory
  override with `RVCP-SUMMARY: TEST SIGRUN`), all three models' verdicts pass, and the
  513-slot signature agrees semulith↔sail-derived AND spike↔sail. The harness carries
  RED/GREEN controls (self-test 7/0 — a corrupted slot is caught at its ordinal, a
  shorter signature is not agreement, a verdict-less trace refuses).
  Strand 2 slice (c) landed `2026-09-30` (`SEMULITH-PS-0068`): **the full campaign —
  51/51 test files, every HTIF verdict pass on all three models, every signature
  agreeing slot-for-slot (semulith vs the Sail-derived expectations AND spike vs sail,
  17,017 slots in sum), first run.** The slot census reconciles exactly against the
  measured static counts (18,092 `RVTEST_SIGUPD` instances): −1,530 dead-path instances
  in the six branch tests (each testcase executes one path), +414 store-test read-back
  slots (2n+1 per store form), +51 `final_sig_offset` words. `I-fence-00` — the
  reserved-`fm`/`fence.tso`/HINT encodings — passes: DEFECT-A's inversion now has
  external-suite confirmation. The record is `profiles/rv64i-lab-v0/act4.sexp` (emitted
  by the runner's `--record` from measured rows; schema `schema/act4.sexp`; RECORD-SCHEMA
  rule 13 CAMPAIGN re-derives every carried count from the rows and confines the verdict
  vocabulary — RED arms: a contradicted count, total, summary, and two out-of-vocabulary
  verdicts; self-test 39/0). Two in-flight REDs, both the author's own: the schema
  rejected `(min N)` on a non-repeat integer field (a facet-arity rule, fixed in the
  schema), and the emitter's multi-value `sparse_paths`/`evidence_note` fields failed the
  record contract's uniform arity (fixed in the emitter, the record regenerated — never
  hand-edited). The `profiles/` and `schema/` ceilings re-derived per the design's
  reviewed expansion (100 files / 427,926 B; 17 files / 47,347 B).
  Strand 3 design: recorded before code `2026-09-30` (the measured coverage census
  + the two probes); archived to [`archive/P2-SCALAR-designs.md`](archive/P2-SCALAR-designs.md)
  (per-part ceiling) once the strand landed.
  Strand 3 landed `2026-09-30` (`SEMULITH-PS-0070`): the eight directed guests — `dir-runoff`
  (semulith's first run off a program's end: the zero word, the policy trap, measured
  identical three-way), `dir-chase` (the load→use-as-address chase and the jump through
  memory — the idiom that existed nowhere, including the constant-folded compiled guest),
  `dir-ext-matrix` (the cross-width sign-extend matrix at the sign edges, 35 steps),
  `dir-selfmod-fence` (the patch visible through `fence rw,rw` — probed before authored),
  `dir-cmp-branch` (compare→branch, all four senses), `dir-memwalk` (the load+store loop),
  `dir-chain` (14 varied serial links), `dir-x0-writes` (every unpinned producer to x0) —
  **150 new aligned steps, all agreeing three-way; 642/642 over the 48-guest assembled
  corpus**, every run byte-identical. The offline differential fired RED on two AUTHORING
  slips, never a model defect: `dir-ext-matrix`'s first draft put its data cell INSIDE the
  code (entry+0x60 < the 0x8C code end — the stores patched the remaining instructions;
  moved to 0xA0, the census addresses with it) and `dir-x0-writes`'s step-0 constant was
  hand-typed wrong (caught at the first run, re-derived). One documented defect found by
  the census and fixed: `c-scope.c`'s comment overclaimed its constant-folded ELF (the
  switch's indirect jump does not exist in the artifact); the comment and the model book's
  compiled-guest chapter are corrected, and the promised idiom became `dir-chase`'s
  measured guest. Matrix cells assigned per the census (`dir-runoff` F×E + E×P beside
  `fault-reserved`; `dir-chase`/`dir-ext-matrix`/`dir-x0-writes` A×A; `dir-ext-matrix`
  also B×B; `dir-selfmod-fence` F×P beside `fault-selfmod`; `dir-cmp-branch` B×E;
  `dir-memwalk`/`dir-chain` P×P) — the orphan rule green. The mutation census pins the
  55 new data crossings; `run/tests.rs` 166 → 174 suites. **The leaf's three strands are
  landed — `.5` is DONE** (the acceptance: ACT4 recorded as external tests with
  Sail-derived expectations, `EVD-04` on the record).
  Lessons (strand 3): `promotion: declined (the code/data collision rule — a guest's data
  must live past its code's end — is enforced where it bites: the offline differential
  caught the draft's self-patch at first run; a knowledge card would restate the gate)`.

- ID: `P2-SCALAR.6` — **discrepancy reduction**
  Status: `done` (`2026-09-30` — the census measured exactly one model-vs-references
  divergence; the minimized case is retained and reproduces it)
  Goal: minimize every discrepancy and retain the minimized case.
  Acceptance: the minimized case reproduces the original divergence; no discrepancy is closed by widening a mask or editing an expected value without a **source-grounded** justification (`EVD-05`, `AI-05`).
  Design: recorded before code `2026-09-30` (the discrepancy census, measured
  first); archived to [`archive/P2-SCALAR-designs.md`](archive/P2-SCALAR-designs.md) (per-part
  ceiling) at the leaf's completion.
  Result: met, `2026-09-30`. **One word retains the one divergence.** `min-fencei`
  (`.word 0x0000100F` alone): semulith's policy trap at step 0, the expected-divergence
  protocol green with `at_step 0` against EACH reference, sail vs spike AGREE over their
  full 2-step length (the nop, then the measured run-off-the-end illegal zero word), and
  the run reproduces byte-identically. The census's other seven differences stay
  dispositioned with their citations — nothing was closed by a widened mask or an edited
  expectation. No RED moment in flight: the protocol, the adapters, and the
  run-off-the-end shape were all built and measured under `.4` and strand 3; this leaf
  reused them unchanged. 175 verify suites (+1); the matrix's F×E cell gains the guest
  (orphan rule green); `references.sexp`'s difference record names the retained case
  (the file sits at 32,765 of its 32,768 ceiling — the note was written to fit, not the
  ceiling moved).
  Lessons: `promotion: declined (the census-is-the-work lesson lives in the leaf's own
  design record; no instrument fired because none needed to)`.

- ID: `P2-SCALAR.7` — **snapshot and replay for implemented boundaries** — `G-REPLAY`
  Status: `active` (`2026-09-30` — design recorded before code; the pending-state census
  is already measured by `state.sexp`)
  Goal: demonstrate replay only for the state boundaries actually implemented.
  Acceptance: a mid-execution snapshot captures all future-relevant pending state or is not offered at all.
  Design (recorded before code, `2026-09-30`):
  - **The pending-state census is the pinned dossier's own** (`state.sexp`
    `hidden_state_census`, SEM-08): all seven hidden-state candidates are measured ABSENT
    (CSRs, reservation set, FP state, vector state, privilege/trap state, fetch-cache
    state, partially committed effects) — its consequence sentence already says
    "snapshot and replay reduce to the register file, pc and memory". So a complete
    mid-execution snapshot for THIS profile is exactly: the 31 writable registers + pc
    (the `ArchitecturalState`) + the memory content (the FlatMemory bytes). Anything
    beyond that is **not offered at all** — the acceptance's second arm — and the suite
    states so by name.
  - **The mechanism** (`semulith-verify::snapshot`): a `Snapshot` record — the
    definition-identity pins flattened from `MANIFEST` (the `P1-LAB.10` bundle
    discipline: replaying against a different definition is refused BY NAME, not
    mis-replayed), the region declaration, entry, the step index `k`, the register file
    and pc, and the memory content SPARSE-encoded (offset + non-zero runs — a 2 GiB
    region of zeros is not data; the encoding is deterministic and its round-trip is
    the first thing tested). JSON both ways, the crate's own reader/writer (the
    wasm-safe, dependency-free rule).
  - **The proof suite** (the G-REPLAY evidence): every tracked guest, at several step
    indices (early / mid / final-quiescent): run to `k`, snapshot, continue to the stop
    → the reference continuation; fresh environment, restore the snapshot, continue →
    the replayed continuation; the two must be IDENTICAL (trace tails and crossing
    logs). RED arms: a snapshot with one memory byte corrupted must be caught (the
    continuation diverges or the digest refuses); a snapshot whose definition pins do
    not match the live manifest is refused by name; a snapshot restored onto a
    different base/entry refuses. The honest-negative discipline: a snapshot that
    silently dropped future-relevant state would pass exactly NONE of these arms
    against a guest whose later behavior depends on it — the memory-walk and chase
    guests (state in MEMORY, not registers) are the load-bearing cases, and the suite
    names them.
  - **The CLI surface** mirrors bundle/replay: `semulith snapshot <elf> --at N` writes
    the record; `semulith resume <file.json>` re-runs from it and prints the
    continuation. Exit codes and refusal shapes follow the existing commands.
  - **Cascades:** `snapshot.rs` + its tests; the CLI's two subcommands + doc comment +
    USAGE; the book (the model book's evidence chapter — replay now covers mid-execution,
    not only cold reset); `G?-REPORT.md` regenerate. No guest corpus change;
    `EXERCISE-COVERAGE` untouched.

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
| 1 | `P2-SCALAR.7` | `pending` | `.6` DONE `2026-09-30` (the census: exactly one divergence — `DIFF-FENCEI-EXECUTED`; `min-fencei` retains it, reproducing the divergence at step 0). Snapshot and replay for implemented boundaries (`G-REPLAY`) is next — the replay machinery exists from `P1-LAB.10`; the leaf proves it for the state boundaries actually implemented |

## Decisions

- `2026-09-30` (leaf `.5`, director delegation — the routing and toolchain call): the C
  guest lands in **this** leaf; `P1-LAB` stays `done` and G1's `incomplete` flips only
  when criterion 6's evidence lands. The toolchain is the two compilers already
  installed (Homebrew clang 21.1.8 with the RISC-V backend measured present; zig
  0.16.0's bundled `ld.lld` 21.1.8) — nothing new installed, both pinned in the leaf's
  evidence. Full record:
  [`decision_c-guest-routing-and-toolchain`](../decisions/decision_c-guest-routing-and-toolchain.md).
- `2026-09-13`: "Locked" means a **versioned accepted profile whose evidence is attached to its
  exact inputs**. A semantic fix invalidates affected evidence and produces a new accepted
  version. It never means errors become unfixable (`ROADMAP.md` §5).
- `2026-09-29` (leaf `.1`, reviewed ceiling expansion): the unit's guest corpus grows from 4
  to 9 programs (+10 tracked files under `profiles/rv64i-lab-v0/guests/`) as the planned
  scope completion — the `profiles/` surface's contract expands with it, so
  `doctrine/readme_routes.tsv`'s `ceiling_lines` for `profiles/` rises 30 → 34 (32 + two
  files of headroom, per the registry's proportional-headroom rule). Demotion was considered
  and rejected: the guests' canonical home is the unit's `guests/` directory — the
  generator, the smoke experiment and the coverage gate all read exactly there, and a
  second guest root would fragment the corpus the gates enumerate. Any FURTHER guest growth
  (`.2`'s boundary cases are a candidate) is its own reviewed decision at its own leaf.
- `2026-09-29` (leaf `.2`, reviewed ceiling expansion — the `.1` decision names this leaf's
  guest growth as its own reviewed decision): the guest corpus grows 9 → 14 programs (+10
  tracked files under `profiles/rv64i-lab-v0/guests/`), so `profiles/` rises 32 → 42 files
  and ~220 KB → ~307 KB aggregate. `doctrine/readme_routes.tsv`: `ceiling_lines` 34 → 46
  (42 + 4 headroom, the registry's proportional rule), `ceiling_bytes` 262144 → 393216
  (the same ~1.2× band over the measured size the existing ceiling holds), health targets
  re-based to the measured 42 files / 307,200 B. ⛔ `ceiling_part_bytes` stays 32768: the
  per-part bound answers "has one member become the monolith", and no new file approaches
  it (largest: `bound-shift.expected.sexp` at 27,848 B — the sweep derivations are
  deliberately terse to keep it that way). Splitting the sweeps across more, smaller
  guests was considered and rejected: a sweep is one argument (every amount of one domain
  on one operand), and splitting it would fragment exactly the claim it makes.
- `2026-09-29` (leaf `.3`, reviewed ceiling expansion — the `.1` decision names each
  leaf's guest growth as its own reviewed decision): the guest corpus grows 14 → 32
  programs (+36 tracked files under `profiles/rv64i-lab-v0/guests/`), so `profiles/`
  rises 42 → 78 files and 307,200 → 367,466 bytes aggregate.
  `doctrine/readme_routes.tsv`: `ceiling_lines` 46 → 82 (78 + 4 headroom, the registry's
  proportional rule), `ceiling_bytes` 393,216 → 471,040 (the same ~1.28× band over the
  measured size the existing ceiling holds), health targets re-based to the measured 78
  files / 367,466 B. ⛔ `ceiling_part_bytes` stays 32768: no new file approaches it
  (largest: `fault-branch-nt.expected.sexp` at 4,017 B). Consolidating the trap guests
  was considered and rejected: a contained trap stops the laboratory run, so each fault
  case that needs its own cause/tval observation needs its own guest — merging unrelated
  traps into one guest is impossible by construction, and merging them into one FILE as
  alternate entry points would fragment the one-guest-one-expectation-document contract
  every gate enumerates.
- `2026-09-29` (leaf `.4`, reviewed ceiling expansion — the `.1` decision names each
  leaf's guest growth as its own reviewed decision): the guest corpus grows 32 → 40
  programs (+16 tracked files under `profiles/rv64i-lab-v0/guests/`) and the interaction
  matrix lands as tracked data (`profiles/rv64i-lab-v0/interactions.sexp`, with
  `schema/interactions.sexp` in the schema family's headroom), so `profiles/` rises 78 →
  95 files and 367,466 → 402,967 bytes aggregate. `doctrine/readme_routes.tsv`:
  `ceiling_lines` 82 → 99 (95 + 4 headroom, the registry's proportional rule),
  `ceiling_bytes` 471,040 → 516,096 (the same ~1.28× band over the measured size the
  existing ceiling holds), health targets re-based to the measured 95 files / 402,967 B.
  ⛔ `ceiling_part_bytes` STAYS 32768 — and it bit: `references.sexp` (31,434 B) plus the
  measured `DIFF-TVAL-PHYS-MASK` record would have crossed it, so the record was written
  tighter (32,406 B) rather than the ceiling moved; no guest file approaches it (largest:
  `it-alias-bound.expected.sexp` at 3,750 B). The same row-count contract crossed two more
  caps — the 25th doctrine row put TOOLBOX.md at 16,380/16,384 B and
  DOCTRINE_ENFORCEMENT.md at 24,573/24,576 B before the row was even added — re-derived to
  20 KiB and 28 KiB respectively, the SEMILITH-PL-0001 precedent (the row count IS those
  surfaces' contract; health targets stay 0).

## Open Questions

- Is x86-64 **and** AArch64 CI infrastructure available at release time? If not, the honest
  outcome is `incomplete` or an explicitly narrower, labelled host policy (`RK14`).

## Blockers

- ~~`P1-LAB` gate `G1`.~~ G1 was RUN `2026-09-29` (verdict `incomplete`): criteria 1–5 met,
  criterion 6 (the C-toolchain guest) routed INTO this tree's `.5`. Scope work (`.1`–`.4`)
  does not depend on criterion 6.
- ~~**`2026-09-29` (blocks `.5`) — the ACT4 external-test material is not in the corpus.**~~
  **ANSWERED `2026-09-29` (leaf `MODEL-METHOD.15`) at the materials layer.** The director
  supplied the corpus root and ordered the cache; `RISCV-ARCH-TEST-ACT4` is now catalogued
  in `materials/catalog.sexp` (43 primary sources, corpus re-pinned `3c45e81` → `73711d6`)
  and cached, manifest-verified (136 entries): the suite's `docs/` and `testplans/` — the
  campaign's planning half. ⛔ What remains for resume day, by design: the generated tests
  (635 MB of `.S`, 31 MB of `.svh`) are pinned by upstream commit
  `e2216915d9a17acc142610831d88de8b65683866`, not committed to the corpus — the snapshot is
  partial by design, and the fetch of the generated half is part of `.5`'s resume, not of
  the catalogue act. Original record, for the trail: the leaf's acceptance requires ACT4
  results (`EVIDENCE_AND_GATES.md` §72 names `riscv-arch-test`, ACT4, Sail-derived
  expectations), but no `riscv-arch-test` entry existed in `materials/catalog.sexp`
  (36 primary sources, corpus `3c45e81`) — verified by grep `2026-09-29`.
- ~~**`2026-09-29` (blocks `.5`'s C-guest strand) — the director's routing answer is still
  open** (`P1-LAB.12` ROUTING EVIDENCE): is the C guest allowed to land in P2, or must G1
  read `passed` first? Compounding it: no RISC-V C toolchain is installed on this machine
  (`riscv64-unknown-elf-gcc` absent; only host `clang`). The strand cannot start without
  the answer AND a toolchain decision.~~
  **ANSWERED `2026-09-30` by the director's delegation** ("make the call yourself"),
  recorded in
  [`decision_c-guest-routing-and-toolchain`](../decisions/decision_c-guest-routing-and-toolchain.md):
  the C guest lands in `P2-SCALAR.5` (the G0 precedent — the tree completes, the gate
  keeps the criterion visible, `EVD-08` forbids `passed` over a missing check), and the
  toolchain was measured present, not installed: Homebrew `llvm@21` clang 21.1.8 (RISC-V
  backend verified by compile + objdump; Apple clang has none — the exact error is in the
  record) linked by zig 0.16.0's bundled `ld.lld` 21.1.8. Nothing new was installed.

## Defects found in flight (owned here per the defect-ownership rule)

- **`2026-09-30` — `c-scope.c`'s scope comment overclaims the compiled artifact.**
  **RESOLVED `2026-09-30` (this leaf's strand 3, `SEMULITH-PS-0070`):** the comment and
  the model book's compiled-guest chapter now state the constant folding and cover only
  what the ELF contains; the jump-table idiom the comment promised is pinned for real by
  `dir-chase` (a measured load→jalr sequence, three-way). — Original entry: the
  strand-3 coverage census (measured by disassembling `target/refs/guests/c-scope.elf`)
  found clang `-O1` constant-folded `fib`/`sum6`/`pick`: the "indirect jump through a
  switch" the header comment advertises does not exist in the ELF — all `jalr`s are
  auipc-relative calls/rets, and most "real function calls" were inlined away. The
  three-way evidence covers what the ELF contains, never what the C tours — so the defect
  is documentary, not evidential: no claim rests on the missing shapes (the strand-3
  census needed the fact, which is how it surfaced). Fix: the comment is corrected in
  this strand, and the jump-table idiom the comment promised becomes a REAL measured
  guest (`dir-chase`). Logged and owned here; closes with the strand.

- ~~**`2026-09-29` — reserved-`fm` FENCE executes as a nop; `D-FENCE` says it must raise
  illegal-instruction.**~~ **RESOLVED `2026-09-29` (leaf `.3`) as a DOSSIER defect, not a
  model defect — the logged defect was inverted.** Measured against the pinned
  specification before any fix: RVI-RV32I §1.1.7 mandates, verbatim, *"Base
  implementations shall treat all such reserved configurations as FENCE instructions
  (with fm = 0000)"* — the reserved `fm`/`pred`/`succ` configurations are an
  architecture-SPECIFIED case (execute as FENCE), not the UNSPECIFIED reserved-decode
  case, so they never belonged under `D-RESERVED-DECODE`. Both references execute the
  probe word `0x1ff0000f` as a nop, exactly as the model does. The correction lands in
  `D-FENCE` (`profile.sexp` and its restatements); `fault-fence` pins the corrected
  behavior three-way. No legality constraint in the encoding format was ever needed —
  the spec text removes the premise. Original reproduce, for the record: assemble word
  `0x1ff0000f` (fence, `fm=0x1`) into a two-word ELF and
  `cargo run -p semulith-cli -- run <elf> --steps=2` — the trace decodes `fence` and
  nops it, which is the architecturally correct behavior. Logged by `P2-SCALAR.1`
  scoping; closed by `P2-SCALAR.3`.

- **`2026-09-29` — a misaligned JAL/JALR writes `rd` before the trap; both references
  suppress the link write.** ~~Reproduce~~ **RESOLVED `2026-09-29` (leaf `.3`).**
  Reproduce (pre-fix): `addi x1, x0, 1; jal x5, 2` —
  `cargo run -p semulith-cli -- run <elf> --steps=3` printed `x5 <- 0x…8` and THEN
  `trap cause=0x00`; spike emitted no commit record for the jump at all and sail showed
  no `x5` write (measured, leaf `.3` probes). Impact: the model retired an architectural
  write from an instruction that raised a synchronous exception. ROOT CAUSE (measured):
  the `jal`/`jalr` effect trees in `definitions/riscv/rv64i.sem.sexp` evaluated the link
  write before `set-pc`'s alignment check. FIXED as semantics DATA (the trees now
  evaluate `set-pc` first; `(pc)` reads the frame's constant instruction address, so
  the success path is exact and the evaluator is untouched); `definition.rs`
  regenerated through the sanctioned generator. `fault-jal-mis`/`fault-jalr-mis` pin
  the fix three-way (`never_written x5`), the mutation matchers were re-derived for the
  new tree shape, and the whole 32-guest corpus re-proves the success path.

## Acceptance Checklist (leaf P2-SCALAR.6)

- [x] **REPRODUCE / ISSUE** — the leaf's premise was measured, not assumed: the census
  over every `references.sexp` difference record and all four corpora (48 guests /
  642 steps, ACT4 51/51 / 17,017 slots, the offline differential, the mutation suite)
  found exactly ONE model-vs-references behavioral divergence — `DIFF-FENCEI-EXECUTED`,
  pinned since `.4`. Every other difference dispositioned with its citation (the design
  block above carries the per-record dispositions).

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect: the divergence is the legitimate
  UNSPECIFIED case (the profile declares Zifencei absent; both references execute
  fence.i anyway — a platform-legitimate difference the reserved-instruction note
  permits). WHY no minimization machinery: `it-fencei`'s three words reduce to one
  because the prefix/marker exist to show agreement AROUND the divergence, not to
  reproduce it; the divergence itself is the first step. The census, re-derivable:

  ```
  $ grep -o 'DIFF-[A-Z-]*' profiles/rv64i-lab-v0/references.sexp | sort -u | wc -l
  8        # the census's denominator: eight recorded differences
  $ grep -c 'expect_divergence' profiles/rv64i-lab-v0/guests/*.expected.sexp | grep -v ':0'
  profiles/rv64i-lab-v0/guests/it-fencei.expected.sexp:2
  profiles/rv64i-lab-v0/guests/min-fencei.expected.sexp:1   # the one divergence's pins
  ```

- [x] **FIX** — the minimized case retained as tracked evidence: `guests/min-fencei.s`
  (one word) + its expectation document (`expect_divergence` at step 0), the full wiring
  (generator tuple, one suite, the census arm, the smoke tuple, the matrix cell), and the
  difference record naming the retained case. No mask widened; no expectation edited
  (`EVD-05`/`AI-05` — the census found no discrepancy tempting either).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify
  test result: ok. 175 passed; 0 failed   (+1 guest suite)
  $ python3 scripts/run_semulith_smoke.py
  …min-fencei: EXPECTED DIVERGENCE at aligned step 0 (DIFF-FENCEI-EXECUTED) vs EACH
    reference — semulith trap=(2, 0x100F), reference trap=None; sail vs spike AGREE
    over their full 2 steps (the nop, then the measured run-off-the-end illegal word)…
  run_semulith_smoke: ok
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; no instrument needed to change
  (the protocol, the adapters and the run-off-the-end shape all predated the leaf):

  ```
  $ make check            # 175 verify suites, 65 core suites, clippy -D warnings, fmt
  $ make gate             # all doctrines green
  $ make bench && node scripts/smoke_bench.js   # 53 arms — 49 clean guests
  $ bash scripts/check_exercise_coverage.sh     # 52/52 (no new form)
  $ bash scripts/check_interaction_matrix.sh [--self-test]   # no orphans; 12/0
  $ python3 scripts/compare_traces.py --self-test            # 19/0
  $ make book             # both books render
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (P2 6/9),
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.7`), this tree, the
  book (`plan/p2.md` carries the result), `references.sexp` (the difference record names
  `min-fencei`), the regenerated fragments and both `G?-REPORT.md`.

## Acceptance Checklists (leaves P2-SCALAR.1–.4, and `.5` — all done)

Archived to [`archive/P2-SCALAR.md`](archive/P2-SCALAR.md) (per-part ceiling) — `.4`'s
joined `.1`–`.3` on `2026-09-30` to make room for `.5`'s strand-3 design, and `.5`'s
(strand 1's) followed when the leaf closed the same day.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-29` | `P2-SCALAR.1` | `scripts/check_exercise_coverage.sh` (pre-registration RED) | 15/52, rc=1 — all 37 missing forms named against the real corpus |
| `2026-09-29` | `P2-SCALAR.1` | `scripts/check_exercise_coverage.sh [--self-test]` | GREEN 52/52; self-test 7 pass / 0 fail |
| `2026-09-29` | `P2-SCALAR.1` | `cargo test -p semulith-verify` | 133 passed / 0 failed (+5 guest suites; census pin over 9 guests incl. scope-mem's 17 crossings) |
| `2026-09-29` | `P2-SCALAR.1` | `scripts/run_semulith_smoke.py` (live, sail-riscv 0.14 + spike 1.1.1-dev) | 9 guests agree on 117/117 aligned steps; ecall = cause 0x0B/tval 0, ebreak = cause 0x03/tval=pc on all three models; every run reproduces byte-identically |
| `2026-09-29` | `P2-SCALAR.1` | `make check`, `make gate`, `make smoke-bench`, wasm build | rc=0; 24 doctrines green; 13 bench arms (9 clean guests); PORT-WEB rc=0 |
| `2026-09-29` | `P2-SCALAR.2` | shamt census (`git grep` over the pre-leaf corpus) | 4 distinct immediate shift amounts {25,31,32,63} of 64 — the boundary hole measured |
| `2026-09-29` | `P2-SCALAR.2` | `cargo test -p semulith-verify` — authoring RED→GREEN ×2 | the overlap-composition constant wrong twice (0x4CD's high byte; the AA lane one hex pair over) — the pinned expectations failed against the real model; the derivation was re-done from the spec rule both times; no model defect |
| `2026-09-29` | `P2-SCALAR.2` | `cargo test -p semulith-verify` | 138 passed / 0 failed (+5 guest suites; census pins bound-ext 32 / bound-alias 16 crossings) |
| `2026-09-29` | `P2-SCALAR.2` | `scripts/run_semulith_smoke.py` (live, sail-riscv 0.14 + spike 1.1.1-dev) | 14 guests agree on 376/376 aligned steps; every run reproduces byte-identically |
| `2026-09-29` | `P2-SCALAR.2` | `make check`, `make gate`, `make smoke-bench`, `check_exercise_coverage.sh [--self-test]` | rc=0; 24 doctrines green; 18 bench arms (14 clean guests); 52/52, self-test 7/0 |
| `2026-09-29` | `P2-SCALAR.3` | the probe suite (16 probe ELFs, untracked, vs sail-riscv 0.14 + spike 1.1.1-dev + semulith) | every design fact measured: the misaligned jump's suppressed link write (DEFECT-B found), the FENCE reserved-config mandate (DEFECT-A inverted), reserved-decode tval = word on both references, the fetch-fault record shapes, OQ-2's answer, immediate self-mod visibility, fence.i executed on both references |
| `2026-09-29` | `P2-SCALAR.3` | authoring RED moments | all 18 expectation documents failed `check_sexp_schema` (one systematic trailing paren); 4 guests failed assembly (store operand order — caught by the pre-wiring dry-run); REQ-D-FENCE failed RECORD-SCHEMA at the gate (statement drift); the adapter refused `misaligned-store/amo` mid-run (measured spelling, added) — no model defect among them |
| `2026-09-29` | `P2-SCALAR.3` | `cargo test -p semulith-verify` | 157 passed / 0 failed (+18 guest suites, +2 runner unit suites; census pins the fault-selfmod store and three access-fault crossings; the SEM-02 and jalr-odd-bit arms re-derived for the policy-converted world) |
| `2026-09-29` | `P2-SCALAR.3` | `scripts/run_semulith_smoke.py` (live, sail-riscv 0.14 + spike 1.1.1-dev) | 32 guests agree on 454/454 aligned steps — every fault guest three-way, including the word-less fetch-fault step and the two policy-converted reserved cases; every run reproduces byte-identically |
| `2026-09-29` | `P2-SCALAR.3` | `make check`, `make gate`, `make smoke-bench`, `check_exercise_coverage.sh [--self-test]`, `compare_traces.py --self-test`, `make book` | rc=0; all doctrines green; 36 bench arms (32 clean guests); 52/52, self-test 7/0; adapter self-test 12/0; the book renders |
| `2026-09-29` | `P2-SCALAR.4` | the `.3` probe suite (8 probe ELFs, untracked, vs sail-riscv 0.14 + spike 1.1.1-dev + semulith) | every design fact measured before any guest existed: fault priority both ways, the wrap-into-fault, the base preservation, the fence.i continuation — and the NEW `DIFF-TVAL-PHYS-MASK` (sail's 56-bit tval mask), which redesigned wrap-sd to address 0 |
| `2026-09-29` | `P2-SCALAR.4` | `scripts/check_interaction_matrix.sh` (pre-registration RED) | rc=1 — `NO MATRIX rv64i-lab-v0` named against the real corpus; then GREEN at 21/21 cells, zero orphans, after the data landed |
| `2026-09-29` | `P2-SCALAR.4` | authoring RED moment | the gate's first GREEN run reported three phantom OMITTED CELLs — the derived cell set was built in declared-axis order, the document's cells in sorted-pair order; the gate's derivation was wrong, not the document; fixed, self-test 12/0 |
| `2026-09-29` | `P2-SCALAR.4` | `cargo test -p semulith-verify` | 166 passed / 0 failed (+8 guest suites, +1 determinism suite; the census pins all 8 new guests — six empty arms, the two faulted wrap crossings) |
| `2026-09-29` | `P2-SCALAR.4` | `scripts/run_semulith_smoke.py` (live, sail-riscv 0.14 + spike 1.1.1-dev) | 40 guests, 492/492 aligned steps — 39 agreeing three-way; `it-fencei` via the four-step expected-divergence protocol (divergence at exactly step 1 vs each reference; sail vs spike AGREE over 4; the difference id recorded); every run reproduces byte-identically |
| `2026-09-29` | `P2-SCALAR.4` | `make check`, `make gate`, `make smoke-bench`, `check_exercise_coverage.sh [--self-test]`, `compare_traces.py --self-test`, `check_interaction_matrix.sh --self-test`, `make book` | rc=0; 25 doctrines green; 44 bench arms (40 clean guests); 52/52, self-test 7/0; comparator self-test 16/0 (+4 divergence arms); matrix self-test 12/0; the book renders |
| `2026-09-30` | `P2-SCALAR.5` (strand 1) | toolchain probes (compile + objdump + `ld.lld --version`) | Apple clang: NO RISC-V backend (exact error in the checklist); Homebrew `llvm@21` clang 21.1.8: correct RV64I; `zig ld.lld`: Homebrew LLD 21.1.8 — pinned in `decision_c-guest-routing-and-toolchain` |
| `2026-09-30` | `P2-SCALAR.5` (strand 1) | authoring RED moment — the guest's own self-check | `fail(0x0501)`: `w32 << 33` is UB in C; clang deleted the rest of the program. Proven by bisect (shift narrowed to 31 → `call fib` + 4× `call emit` restored; `-fno-strict-aliasing` control innocent). An AUTHORING defect, caught before any comparison ran |
| `2026-09-30` | `P2-SCALAR.5` (strand 1) | comparator RED — first divergence at aligned step 7 vs BOTH references | `li a0, 0` with a0 already 0: the references log the write, semulith's declared visible-change vocabulary does not; normalized in `align` (`_visible_changes`), self-test 19/0 (+2 arms) |
| `2026-09-30` | `P2-SCALAR.5` (strand 1) | `scripts/run_semulith_smoke.py` (live, sail-riscv 0.14 + spike 1.1.1-dev) | `c-scope`: AGREE over 129/129 aligned steps vs sail-riscv AND spike, byte-identical reproduction; the 40 assembled guests unchanged — 221 PASS / 0 FAIL |
| `2026-09-30` | `P2-SCALAR.5` (strand 1) | `scripts/gate_report.py rv64i-lab-v0 --gate G1`, `make gate`, `make book` | **G1 verdict `passed`** (criterion 6 met); all doctrines green; both books render |
| `2026-09-30` | `P2-SCALAR.5` (strand 2a) | the pinned sparse fetch (blobless clone at `e2216915…`, `target/refs/riscv-arch-test/`) + census of the fetched tree | 45 MB on disk (the RV64I campaign's share of the ~672 MB tree): 51 test files / 199,768 lines / 18,092 `RVTEST_SIGUPD`s / 14,820 testcases — every design number measured, not read from the docs; two doc facts found stale (the README's sail 0.13.1 pin; the signature flow) |
| `2026-09-30` | `P2-SCALAR.5` (strand 2a) | `bash scripts/check_profile_consistency.sh --self-test`, `make gate`, `make book` | self-test green with the new status vocabulary value; all doctrines green; both books render — a docs-only commit |
| `2026-09-30` | `P2-SCALAR.5` (strand 2b) | toolchain risk retirement (measured, not assumed) | clang 21.1.8 assembled `I-add-00.S` (the suite's full macro machinery) clean; `ld.lld` linked against the laboratory `link.ld`; sail 0.14 self-terminated on the HTIF verdict under the lab override — both documented-toolchain mismatches (LLVM 22 / sail 0.13.1 in the cached README) measured harmless |
| `2026-09-30` | `P2-SCALAR.5` (strand 2b) | `python3 scripts/run_act4_campaign.py` (live, three-way) | `I-add-00`: HTIF verdict pass on all three models; the 513-slot signature agrees semulith↔sail-derived AND spike↔sail |
| `2026-09-30` | `P2-SCALAR.5` (strand 2b) | `python3 scripts/run_act4_campaign.py --self-test` | 7 pass / 0 fail — the corrupted-slot RED, the shorter-signature RED, the verdict-less refusal, the console/verdict channel separation |
| `2026-09-30` | `P2-SCALAR.5` (strand 2c) | `python3 scripts/run_act4_campaign.py --all` (live, three-way) | **51/51 test files green, first run**: every HTIF verdict pass on all three models; every signature agrees slot-for-slot — semulith vs the Sail-derived expectations AND spike vs sail; 17,017 slots in sum |
| `2026-09-30` | `P2-SCALAR.5` (strand 2c) | the slot census vs the measured static counts | 17,017 = 18,092 sigupd instances − 1,530 dead-path branch instances (255 × 6) + 414 store read-back slots (2n+1 per store form) + 51 `final_sig_offset` words — exact |
| `2026-09-30` | `P2-SCALAR.5` (strand 2c) | authoring REDs ×2 | the schema kernel refused `(min N)` on a non-repeat integer field; the emitter's multi-value atom fields failed uniform arity — both fixed at the source, the record regenerated |
| `2026-09-30` | `P2-SCALAR.5` (strand 2c) | `python3 scripts/run_act4_campaign.py --record` + `bash scripts/check_requirements.sh [--self-test]` | the dossier `act4.sexp` emitted from measured rows (51 rows, `51 pass / 0 fail`); rule 13 CAMPAIGN green on the real record; self-test 39/0 (+5 arms) |
| `2026-09-30` | `P2-SCALAR.5` (strand 3) | the coverage census (tracked corpus + `c-scope.elf` disassembly + ACT4 testplan/bodies) | eight gaps measured, with citations: run-off-the-end (semulith), load→use-as-address, the cross-width sign-extend matrix, store→fence→execute, compare→branch, the memory-walk loop, 12-deep varied chains, the unpinned x0 producers; and one defect found — `c-scope.c`'s comment overclaims the constant-folded ELF |
| `2026-09-30` | `P2-SCALAR.5` (strand 3) | the probe suite (`run_probes_p25s3.py`, 2 probe ELFs, vs sail 0.14 + spike + semulith) | run-off-the-end: illegal-instruction 0x02/tval 0/word 0 on ALL THREE (sail `c.illegal`, spike `c.unimp`, semulith the policy conversion); self-mod through `fence rw,rw`: the patch visible on ALL THREE (x2 ← 7) |
| `2026-09-30` | `P2-SCALAR.5` (strand 3) | authoring REDs ×2 (the offline differential) | `dir-ext-matrix`'s data cell sat INSIDE the code (entry+0x60 < the 0x8C end — the stores patched the remaining instructions; 25 of 35 steps); `dir-x0-writes`' step-0 constant hand-typed wrong (0x8000000080000000) — both fixed by re-derivation, never a model defect |
| `2026-09-30` | `P2-SCALAR.5` (strand 3) | `cargo test -p semulith-verify` | 174 passed / 0 failed (+8 guest suites; the census pins the 55 new data crossings; the stop-reason table learned the dir-* shapes) |
| `2026-09-30` | `P2-SCALAR.5` (strand 3) | `scripts/run_semulith_smoke.py` (live, sail-riscv 0.14 + spike 1.1.1-dev) | 48 guests, **642/642 aligned steps** (+150) — every dir-* guest three-way at full length; `it-fencei`'s protocol unchanged; every run reproduces byte-identically |
| `2026-09-30` | `P2-SCALAR.5` (strand 3) | `make check`, `make gate`, `make bench` + `make smoke-bench`, `check_exercise_coverage.sh`, matrix and comparator self-tests, `make book` | rc=0; all doctrines green; 52 bench arms (48 clean guests); 52/52; matrix 12/0, comparator 19/0; both books render |
| `2026-09-30` | `P2-SCALAR.6` | the discrepancy census (every `references.sexp` difference + all four corpora) | exactly ONE model-vs-references behavioral divergence exists (`DIFF-FENCEI-EXECUTED`, already pinned); the other seven differences dispositioned with citations (harness ×2, trace vocabulary, sub-granularity observable, a corrected configuration defect, a board-layer difference, one reference-vs-reference) |
| `2026-09-30` | `P2-SCALAR.6` | `cargo test -p semulith-verify` + the live smoke's four-step protocol | 175 passed / 0 failed (+1 guest suite); `min-fencei`: EXPECTED DIVERGENCE at aligned step 0 vs EACH reference, sail vs spike AGREE over 2, byte-identical reproduction |
| `2026-09-30` | `P2-SCALAR.6` | `make check`, `make gate`, bench + smoke-bench, coverage/matrix/comparator self-tests, `make book` | rc=0; all doctrines green; 53 bench arms (49 clean guests); 52/52; both books render |
| `2026-09-30` | `P2-SCALAR.7` | the pending-state census source | `state.sexp`'s hidden-state census: all seven candidates measured absent — a complete snapshot for this profile is exactly registers + pc + memory (the census's own consequence sentence says so) |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `P2-SCALAR.1` | `SEMILITH-PS-0001 (leaf P2-SCALAR.1): …` | the declared scope completed and gated: five guests, EXERCISE-COVERAGE (24th doctrine), fence fields from the pinned table, ecall/ebreak adapter spellings, 117/117 live; the reserved-`fm` defect logged for `.3` |
| `P2-SCALAR.2` | `SEMILITH-PS-0002` (design, before code), `SEMILITH-PS-0003 (leaf P2-SCALAR.2): …` | boundary arithmetic landed: five guests (6-bit and 5-bit shamt domains exhausted, wraps on both paths, sign-edge pairs, endian lanes, overlap composition, register aliasing, x0), 376/376 live; ceilings expanded by reviewed decision; two authoring slips caught by the gate, never a model defect |
| `P2-SCALAR.3` | `SEMILITH-PS-0004` (design, before code — measured first), `SEMILITH-PS-0005 (leaf P2-SCALAR.3): …` | faults/suppression/reserved landed: DEFECT-A inverted (the FENCE dossier correction), DEFECT-B fixed in semantics data (the misaligned-jump link write), the word-less fetch-fault step, the reserved-decode policy conversion, OQ-2 answered, `.word` learned, DIFF-FENCEI-EXECUTED recorded — 454/454 live over 32 guests; ceilings expanded by reviewed decision; three authoring slips caught by the instruments, never another model defect |
| `P2-SCALAR.4` | `SEMILITH-PS-0006` (design, before code — measured first), `SEMILITH-PS-0007 (leaf P2-SCALAR.4): …` | the interaction matrix landed: 21 cells declared as tracked data and exercised, eight guests (fault priority, base preservation, the wrap-into-fault on both paths, self-aliased boundary ops, the budget loop, the fence.i expected divergence), the comparator's expected-divergence verdict, INTERACTION-MATRIX (25th doctrine, fired RED before registration), the offline determinism suite, DIFF-TVAL-PHYS-MASK recorded — 492/492 live over 40 guests; ceilings expanded by reviewed decision (incl. the two mirror caps the 25th row crossed); the gate's own derivation bug caught RED by the corpus, never a model defect |
| `P2-SCALAR.5` | `SEMULITH-PS-0062` (the routing answered + the three-strand design, before code), `SEMULITH-PS-0063 (leaf P2-SCALAR.5): …`, `SEMULITH-PS-0066` (strand 2a: ACT4 acquired sparse + the strand-2 design, before code — measured against the pinned fetch), `SEMULITH-PS-0067` (strand 2b: the store trace, the DUT-side pieces, the one-test harness three-way green), `SEMULITH-PS-0068` (strand 2c: the full campaign — 51/51, 17,017 slots, three-way; the gated `act4.sexp` record), `SEMULITH-PS-0069` (strand 3 design, before code — census + probes measured first), `SEMULITH-PS-0070` (strand 3: the eight directed guests — **`.5` DONE**) | strand 1 landed: `c-scope.c` — the first COMPILED guest (clang 21.1.8 + `ld.lld` 21.1.8, measured present, pinned by decision record) — retires three-way 129/129; the comparator learned the declared visible-change vocabulary (`_visible_changes`, +2 self-test arms); `gate_report.py`'s criterion-6 branch; **G1 reads `passed`**; two in-flight REDs, both authoring-side (the C UB shift; the comparator's normalization), never a model defect. Strand 2a: the suite's generated half on disk (45 MB sparse partial, pinned), the strand-2 design recorded (signature-mode + store-trace extraction + Sail-derived expectations), the acquisition facts synced (`references.sexp`, the catalogue, both books); `.4`'s design obeyed the per-part ceiling by moving to the archive |
| `P2-SCALAR.6` | `SEMULITH-PS-0071` (design, before code — the census measured first), `SEMULITH-PS-0072` (the minimized case retained — the leaf DONE) | one model-vs-references divergence exists (`DIFF-FENCEI-EXECUTED`); `min-fencei` (one word) reproduces it under the expected-divergence protocol at step 0; no mask widened, no expectation edited |
| `P2-SCALAR.7` | `SEMULITH-PS-0074` (design, before code) | mid-execution snapshots: the pending-state census is the pinned dossier's own (registers + pc + memory, all seven hidden-state candidates measured absent); the proof suite's load-bearing cases are the memory-state guests |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P2 and task cards `T008`–`T009` by `SEMULITH-TREES.2`.
