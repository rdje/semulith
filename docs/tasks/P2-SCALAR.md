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
  Design: recorded before code; archived to [`archive/P2-SCALAR.md`](archive/P2-SCALAR.md) (per-part ceiling).
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
  Design: recorded before code; archived to [`archive/P2-SCALAR.md`](archive/P2-SCALAR.md) (per-part ceiling).
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
  Design: recorded before code; archived to [`archive/P2-SCALAR.md`](archive/P2-SCALAR.md) (per-part ceiling).
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
  Status: `active`
  Goal: the declared fault × alias × boundary × event × progress × restart matrix, exercised.
  Acceptance: the matrix is declared first and then exercised; unexercised cells are reported, not omitted.
  Design (recorded before code, `2026-09-29` — every reference behavior below was MEASURED
  against sail-riscv 0.14 AND spike 1.1.1-dev by an untracked probe suite
  (`target/refs/guests/probes/run_probes_p24.py`, 8 probe ELFs) before any guest was
  authored, the `.3` doctrine):
  - **The six axes, grounded.** `fault` = the `.3` layer; `alias`/`boundary` = the `.2`
    layers; `event` = `OB-ENV-EVENT-DELIVERY` (synchronous exceptions and requested traps
    only); `progress` = `OB-ENV-PARTIAL-PROGRESS` + the budget contract; `restart` = the
    `state.sexp` census (no restartable suboperation) — restartability is **determinism
    of re-execution from cold reset**, a mechanism property, not a guest shape.
  - **The matrix is the 6×6 upper triangle = 21 cells, declared as tracked data** in
    `profiles/rv64i-lab-v0/interactions.sexp` (new `schema/interactions.sexp`), each cell
    carrying a disposition: guest(s) / mechanism / degenerate-with-reason. "Unexercised
    cells are reported, not omitted" is mechanized: the gate RE-DERIVES the 21 cells from
    the 6 declared axes and refuses by name a document that leaves one out or a cell
    whose disposition does not resolve.
  - **Measured: fault priority is three-way pinnable.** A jump target both misaligned AND
    unmapped (`jalr` → 0x40000002) raises misaligned-fetch (0x00) ON THE JUMP, tval = the
    target, link suppressed — all three models; a data access both misaligned AND
    unmapped (`lw` at 0x40000001) raises misaligned-load (0x04) — all three.
  - **Measured: the address wrap into a fault agrees three-way when tval < 2^56** (`ld`
    at base −4 + 4 → address 0: cause 0x05, tval 0, all three).
  - **⚠️ Measured: a NEW reference difference — sail-riscv 0.14 masks the access-fault
    tval to its 56-bit physical-address width.** `sd` at 0xFFFF…FFF8: sail reports
    tval 0x00FF_FFFF_FFFF_FFF8, spike AND semulith the full address; at exactly 2^56
    sail reports tval 0, spike the full 0x0100_0000_0000_0000; at 2^55 both intact. A
    reference-vs-reference difference, not a model defect — recorded as
    `DIFF-TVAL-PHYS-MASK` in `references.sexp`; consequence: three-way tval comparisons
    keep fault addresses below 2^56, so the wrap-sd guest wraps to address 0 (tval 0,
    three-way exact) instead of the top of the space. Owner of reopening: whichever
    profile declares ≥2^56 addresses meaningful.
  - **Measured: the fence.i expected-divergence shape is exact.** Both references nop
    fence.i and CONTINUE (the marker write commits); semulith reports the
    policy-converted illegal-instruction (0x02, tval = the word) and stops. Prefix
    agrees; divergence at exactly the fence.i step; the two references agree with each
    other over their whole length.
  - **Measured: a misaligned load over its own base** (`lw x5, x5, 1`) raises 0x04 with
    the base preserved — all three.
  - **Eight new guests** (EVD-05 expectations before any run; trap step last):
    `it-prio-jump` (3 steps, F×F), `it-prio-load` (3, F×F), `it-fault-alias` (2, F×A),
    `it-fault-wrap-ld` (2, F×B), `it-fault-wrap-sd` (3, F×B — the tval-0 redesign),
    `it-alias-bound` (~9, A×B — self-aliased ops at boundary values: `addw` wrap, `srl`
    shamt 65 → 1, `sll` shamt 63, `sub`/`slt` at −1), `it-progress-loop` (~13, P×P + A×E
    — a counting loop under `jal x0, -4` to budget, every iteration visible, the x0 link
    unwritten, `Stop::Budget`), `it-fencei` (2 steps semulith / 3 references, F×E — the
    `DIFF-FENCEI-EXECUTED` expected-divergence guest).
  - **The comparator learns the EXPECTED divergence.** `schema/expectations.sexp` gains
    an optional `(expect_divergence (difference "DIFF-…") (at_step N))`;
    `dossier_sexp.py` round-trips it; `compare_traces.py` gains
    `check_expected_divergence` with RED/GREEN self-test arms. The smoke path for a
    declaring guest: (a) semulith matches its own spec-derived expectations as always;
    (b) `compare(semulith, each reference)` reports FIRST DIVERGENCE at exactly
    `at_step`, semulith's step carrying the policy trap; (c) sail vs spike AGREE over
    their full length — the references stay each other's control; (d) the difference id
    exists in `references.sexp`, commit-gated by the matrix gate. `cross_model` stays a
    comparison DISABLE; an expected divergence is the opposite act — a comparison that
    must fail in exactly one declared way.
  - **The restart axis is a mechanism, not a guest.** The smoke runner's reproduce leg
    already re-runs every guest byte-identically; this leaf adds the offline half —
    `run/tests.rs` gains a determinism suite (every guest run twice from
    `zeroed_at(entry)`, identical traces) — so the restart cells are commit-gated, not
    only live. The fault-side half (a trap leaves the pre-instruction state) is already
    pinned by `.3`'s never_written + no-crossing evidence.
  - **The 21-cell census** (dispositions; NEW = this leaf's guests; MECH = the
    reproduce/determinism mechanism): F×F → `it-prio-jump`, `it-prio-load` (NEW);
    F×A → `it-fault-alias` (NEW) + `fault-ld-x0-mis`/`-x0-fault`; F×B →
    `it-fault-wrap-ld`, `it-fault-wrap-sd` (NEW); F×E → `it-fencei` (NEW) +
    `fault-reserved`, `fault-shiftw-res`, `scope-ecall`/`-ebreak`; F×P →
    `fault-st-mis-h`/`-w`/`-d`, `fault-jal-mis`/`-jalr-mis`, `fault-branch-nt`;
    F×R → MECH; A×A → `bound-alias`; A×B → `it-alias-bound` (NEW); A×E →
    `it-progress-loop` (NEW — the x0 link); A×P → `bound-alias` (load over own base);
    A×R → MECH; B×B → `bound-arith`, `bound-shift`/`-shiftw`; B×E → `scope-branch`,
    `fault-branch-nt`; B×P → `bound-shift`/`-shiftw` (every sweep step visible);
    B×R → MECH; E×E → degenerate-in-run (the contained-trap contract makes a second
    in-run event unreachable; the KINDS are exercised across guests — declared with that
    reason); E×P → `scope-ecall`/`-ebreak` (`Stop::Trap`), `fault-fetch`
    (`Stop::FetchFault`), `fault-reserved` (`Stop::Undefined`); E×R → MECH;
    P×P → `it-progress-loop` (NEW); P×R → MECH; R×R → MECH (the smoke reproduce leg +
    the NEW offline determinism suite).
  - **B×E exhaustion judgement, stated:** branch/jump offset extremes (±4092/±4096) were
    considered and rejected — the B/J immediate layouts are encoding-pinned (the
    accounted-bits self-check and the disjointness gates own them), `pc + sext(imm)` is
    exercised at both signs by `scope-branch`/`fault-branch-nt`, and ~1 KB of
    never-executed padding per direction buys no discrimination the sign edges do not
    already provide (the `.2` byte-sweep rejection is the precedent).
  - **The new doctrine `INTERACTION-MATRIX`** (`scripts/check_interaction_matrix.{py,sh}`,
    #25): re-derives the 21 cells from the axes (an omitted cell fails, named); every
    disposition resolves (guest cells name tracked guests with source AND expectations;
    mechanism cells name a closed registry — the smoke reproduce leg, the offline
    determinism suite; degenerate cells carry a non-empty reason); every tracked guest
    maps to ≥1 cell (an orphan fails, named); every difference id named in the matrix
    exists in `references.sexp`; the report prints every cell with its verdict. Self-test
    RED arms, fired RED against the real corpus before registration, mirrored per the
    registry rules; `TOOLBOX.md` gains the row.
  - **Reviewed ceiling expansion** (the `.1` decision names each leaf's guest growth as
    its own reviewed decision): the corpus grows 32 → 40 guests (+16 tracked files) and
    `interactions.sexp` lands, so `profiles/` rises 78 → 95 files and ~367 KB → ~395 KB.
    `doctrine/readme_routes.tsv`: `ceiling_lines` 82 → 99 (95 + 4 headroom),
    `ceiling_bytes` re-based to the measured aggregate under the same ~1.2× band, health
    targets re-based. ⛔ `ceiling_part_bytes` stays 32768 — no new file approaches it
    (largest: ~4 KB). `schema/` gains `interactions.sexp` (+1 file, its row's headroom).
  - **Cascades owned by this leaf:** `schema/expectations.sexp` + the new
    `schema/interactions.sexp`; `dossier_sexp.py` (the field round-trips); 8 guests × 2
    files; `gen_guests.py`'s tuple and `guests.rs` regenerated; `run/tests.rs` gains one
    suite per guest (fault suites assert trap pair + stop reason; `it-fencei` asserts
    `Stop::Undefined`; `it-progress-loop` asserts `Stop::Budget`) plus the determinism
    suite; `mutate.rs`'s census — all 8 join the empty arm with per-line justifications
    (no new guest has a successful store crossing); `compare_traces.py` (the divergence
    check + arms); `run_semulith_smoke.py` (the tuple + the divergence path);
    `references.sexp` gains `DIFF-TVAL-PHYS-MASK`; the new gate + registration + the
    three mirrors (`DOCTRINE_ENFORCEMENT.md`, `docs/book/src/working/doctrines.md`,
    `TOOLBOX.md`); the routes-registry ceilings; both `G?-REPORT.md` regenerate (counts
    are derived); the book (`plan/p2.md` carries the result; `claim-scope.md`/`plan/p1.md`
    re-sync to 40 guests); `EXERCISE-COVERAGE` stays 52/52 (no new form).

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
| 1 | `P2-SCALAR.4` | `active` | scope exercised (`.1`), boundaries pinned (`.2`), faults/suppression/reserved pinned (`.3`); the declared fault × alias × boundary × event × progress × restart matrix is the next evidence layer — and it owns the expected-divergence comparison the `fence.i` guest (`DIFF-FENCEI-EXECUTED`) is routed to. Design recorded `2026-09-29` (measured first: fault priority, the address wrap, the fence.i divergence shape; NEW reference difference `DIFF-TVAL-PHYS-MASK`) |

## Decisions

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

## Open Questions

- Is x86-64 **and** AArch64 CI infrastructure available at release time? If not, the honest
  outcome is `incomplete` or an explicitly narrower, labelled host policy (`RK14`).

## Blockers

- ~~`P1-LAB` gate `G1`.~~ G1 was RUN `2026-09-29` (verdict `incomplete`): criteria 1–5 met,
  criterion 6 (the C-toolchain guest) routed INTO this tree's `.5`. Scope work (`.1`–`.4`)
  does not depend on criterion 6.

## Defects found in flight (owned here per the defect-ownership rule)

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

## Acceptance Checklists (leaves P2-SCALAR.1–.2)

Archived to [`archive/P2-SCALAR.md`](archive/P2-SCALAR.md) (per-part ceiling) — the `.4`
checklist lands live at the leaf's completion, beside `.3`'s below.

## Acceptance Checklist (leaf P2-SCALAR.3)

- [x] **REPRODUCE / ISSUE** — three holes, each measured before any fix. (a) The `.1`
  defect log said reserved-`fm` FENCE must trap; the pinned spec says the opposite —
  the probe showed all THREE models nop it. (b) The misaligned-jump link write,
  reproduced against both references: semulith wrote `x5`, neither reference did. (c)
  The fetch-fault observation gap `run.rs` named as future work, and the reserved-decode
  case stopping with no observation to compare:

  ```
  $ cargo run -p semulith-cli -- run probe-jal-mis.elf --steps=4   # BEFORE the fix
  [1] [M]: 0x0000000080000004 (0x002002ef) jal
  x5 <- 0x0000000080000008                     # ← the write both references suppress
  trap cause=0x00 tval=0x0000000080000006
  $ cargo run -p semulith-cli -- run probe-fetch-fault.elf --steps=6
  run: fetch access fault at 0x0000000040000000; no observation recorded   # ← the gap
  $ cargo run -p semulith-cli -- run probe-reserved-ones.elf --steps=4
  run: undefined case: ReservedDecode { at: 2147483652 }   # rc=1, no trace observation
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — (a) WHY: the dossier author read "reserved" and
  reached for `D-RESERVED-DECODE`, but RVI-RV32I §1.1.7 SPECIFIES the behavior of
  reserved FENCE configurations ("shall treat all such reserved configurations as FENCE
  instructions (with fm = 0000)") — a specified reserved case, not the UNSPECIFIED one.
  WHERE: `D-FENCE`'s last sentence and its `REQ-D-FENCE`/`OB-FENCE` restatements.
  (b) WHY: the `jal`/`jalr` effect trees evaluated the link write before `set-pc`'s
  alignment check, so a trapping jump retired a write. WHERE:
  `definitions/riscv/rv64i.sem.sexp` — semantics data, never the evaluator. (c) WHY:
  the observation vocabulary had no honest shape for "the fetch supplied no word" and
  no policy act for the reserved case. WHERE: `run.rs`'s `Step`/`Stop` and the two
  trace adapters in `scripts/compare_traces.py`.

- [x] **FIX** — the dossier correction (`D-FENCE` + both restatements, the verbatim
  mandate cited, the correction noted like `D-MAIN-VS-IO`'s); the sem-tree reorder
  (`set-pc` first — data, regenerated through the sanctioned generator); the word-less
  fetch-fault step (`Step.word` → `Option<u32>`, emitted by the runner, printed by the
  CLI, synthesized by both adapters, round-tripped by replay); the reserved-decode
  policy conversion in the harness (`Stop::Undefined` keeps the classification);
  `riscv_asm.py`'s `.word` directive; eighteen EVD-05 guests; the adapter's four
  measured spellings + self-test arms (12/0); `DIFF-FENCEI-EXECUTED` recorded;
  OQ-2 answered (`REQ-D-SHIFTW-RESERVED` → `resolved`); the census and suites
  re-derived; ceilings expanded by reviewed decision.

- [x] **ADDRESSED (verified)** — before→after on the same probes: the misaligned jump
  now traps with NO link write (matching both references); the fetch fault records the
  word-less step; the reserved word records the policy-converted trap. And the full
  corpus:

  ```
  $ cargo test -p semulith-verify          # the offline differential, commitment-gated
  test result: ok. 157 passed; 0 failed (+18 guest suites, +2 runner unit suites;
    the census pins fault-selfmod's crossing and the three access-fault crossings)
  $ python3 scripts/run_semulith_smoke.py  # the live three-way differential
  …every fault-* guest: AGREE vs sail-riscv AND spike…
  run_semulith_smoke: ok — 32 guests, 454/454 aligned steps, byte-identical reproduction
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; and the instruments caught three
  AUTHORING slips in flight (the trailing paren in all 18 expectation documents — schema
  RED on all 18; the store operand order in 4 guests — the pre-wiring dry-run; the
  REQ-D-FENCE statement drift — RECORD-SCHEMA RED at the gate), never another model
  defect:

  ```
  $ make check            # 157 verify suites, 65 core suites, clippy -D warnings, fmt
  $ make gate             # all doctrines green (RECORD-SCHEMA, the new ceilings…)
  $ make smoke-bench      # 36 arms — 32 clean guests, 3 trace-level mutants, the census arm
  $ bash scripts/check_exercise_coverage.sh [--self-test]   # 52/52; self-test 7/0
  $ python3 scripts/compare_traces.py --self-test           # 12/0 (+4 new arms)
  $ make book             # renders
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (P2 3/9),
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.4`), this tree, the
  book (`plan/p2.md` carries the result; `plan/p1.md` and `claim-scope.md` re-synced to
  32 guests / 454 steps; `annex/assembler.md` documents `.word`), the routes registry
  (the reviewed ceilings), `references.sexp` (the new difference), the dossier
  (D-FENCE, OQ-2), and both regenerated `G?-REPORT.md`.

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

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `P2-SCALAR.1` | `SEMILITH-PS-0001 (leaf P2-SCALAR.1): …` | the declared scope completed and gated: five guests, EXERCISE-COVERAGE (24th doctrine), fence fields from the pinned table, ecall/ebreak adapter spellings, 117/117 live; the reserved-`fm` defect logged for `.3` |
| `P2-SCALAR.2` | `SEMILITH-PS-0002` (design, before code), `SEMILITH-PS-0003 (leaf P2-SCALAR.2): …` | boundary arithmetic landed: five guests (6-bit and 5-bit shamt domains exhausted, wraps on both paths, sign-edge pairs, endian lanes, overlap composition, register aliasing, x0), 376/376 live; ceilings expanded by reviewed decision; two authoring slips caught by the gate, never a model defect |
| `P2-SCALAR.3` | `SEMILITH-PS-0004` (design, before code — measured first), `SEMILITH-PS-0005 (leaf P2-SCALAR.3): …` | faults/suppression/reserved landed: DEFECT-A inverted (the FENCE dossier correction), DEFECT-B fixed in semantics data (the misaligned-jump link write), the word-less fetch-fault step, the reserved-decode policy conversion, OQ-2 answered, `.word` learned, DIFF-FENCEI-EXECUTED recorded — 454/454 live over 32 guests; ceilings expanded by reviewed decision; three authoring slips caught by the instruments, never another model defect |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §P2 and task cards `T008`–`T009` by `SEMULITH-TREES.2`.
