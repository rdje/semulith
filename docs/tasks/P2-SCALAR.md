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
  Design (recorded before code, `2026-09-29`):
  - **The gap, measured.** Denominator: the profile's declared scope — 52 RV64I forms
    (`profile.sexp` `[scope]`, count re-derived from the `riscv/rv64i` fragment). Exercised
    today: 15 — the union of mnemonics over the four tracked guests' expectation documents
    (`add addi addiw auipc bne jal jalr ld lui lw sd slli slliw srai srli`). Remaining: 37.
  - **Five new guests**, each form landing on a recorded decision, every expectation value
    derived from the pinned specification BEFORE any model runs (`EVD-05`):
    `scope-alu` (the 21 remaining logical/compare/shift forms, plus `fence`),
    `scope-mem` (the 8 remaining load/store forms), `scope-branch` (the 5 remaining branches,
    taken AND not-taken each), `scope-ecall` and `scope-ebreak` (a requested trap stops the
    run, so each gets its own guest, trap step last — the `smoke-trap` pattern).
  - **`fence` needs the assembler to learn three operand fields.** The pinned `arg_lut.csv`
    carries `fm`/`pred`/`succ` (31..28 / 27..24 / 23..20); `gen_fragments.py`'s `USED_FIELDS`
    whitelist predates any fence guest. The change is the sanctioned one: extend the
    whitelist, regenerate `definitions/riscv/rv64i.sexp` (three field lines), add the three
    fields to `riscv_asm.py`'s `CONTIGUOUS_OPERANDS` (the existing width-checked path
    range-checks 0..15), regenerate `definition.rs`. No opcode is typed by hand anywhere.
  - **Coverage with its denominator, gated.** New tracked diagnostic
    `scripts/check_exercise_coverage.{py,sh}`: exercised = the union of mnemonics the tracked
    expectation documents declare executed (the commit gate proves those steps execute);
    denominator = the declared scope; the SCP-02 closure printed as data through the one
    resolver (`riscv_asm.resolve_composition`): closure `{riscv/rv64i}`, `requires` empty,
    extensions none. Registered as project doctrine `EXERCISE-COVERAGE` with RED-arm
    self-tests, mirrored per the registry rules; `TOOLBOX.md` gains the row.
  - **Cascades owned by this leaf:** `gen_guests.py`'s guest tuple; `run/tests.rs` gains one
    test per guest (stop `Budget`, or `Trap` for the two env guests); `mutate.rs`'s
    `pinned_census` gains the `scope-mem` data crossings with per-line justifications (the
    census-pin test iterates every guest); `run_semulith_smoke.py`'s guest tuple (the live
    three-way run, references present under `target/refs/`); `gate_report.py`'s hardcoded
    "The four tracked guests" becomes derived and both `G?-REPORT.md` regenerate.
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
  Design (recorded before code, `2026-09-29`):
  - **The four named concerns map onto five new guests**, every expectation derived from the
    pinned specification prose BEFORE any model runs (`EVD-05`), each step carrying its
    `derivation` and `source` exactly as the `.1` guests do. Values are computed by spec-rule
    arithmetic at authoring time (never read back from any model's output); the live
    three-way differential (`run_semulith_smoke.py` vs sail-riscv AND spike) is the
    falsification leg, and the offline commit gate re-runs the pinned expectations.
  - **`bound-shift` — the 64-bit shift corner cases (`D-SHAMT`).** Operand
    `0x8000000000000001` (bit 63 AND bit 0 set) built from covered forms. The **6-bit shamt
    domain is exhausted**: a full 64-point `srli` sweep, whose 64 results are pairwise
    distinct so every step is a VISIBLE register change. `sll`/`sra` immediates take the
    bit-pinning set {0,1,2,4,8,16,32,63} — every shamt bit pinned on every form, the full
    sweep held once per domain rather than once per form (the amount decode is the shared
    structure; the fill/direction logic is what differs per form, and the boundary values
    discriminate it). Register-amount corners: `rs2 = 64` reads as 0 (identity — pre-written
    to observe) and `rs2 = -1` reads as 63, through `srl`/`sll`/`sra`. 89 steps.
  - **`bound-shiftw` — the *W shift corner cases (`D-SHAMT`'s 5-bit rule, `D-WSUFFIX`).**
    Operand low32 `0x80000001` (bit 31 set). The **5-bit domain is exhausted**: a full
    32-point `sraiw` sweep (sign fill within 32 bits, then the *W sign extension — 32
    distinct results); `slliw`/`srliw` take the bit-pinning set {0,1,2,4,8,16,31}.
    Register-amount corners: `rs2 = 96` — low6 = 32, low5 = 0 — as the discriminator PAIR
    (`srl` shifts by 32, `srlw` is the identity, same operands) and `rs2 = -1` (low5 = 31)
    through `sllw`/`sraw`. 52 steps.
  - **`bound-arith` — wrap/overflow and immediate boundaries (`D-ALU-REG`, `D-ALU-IMM`,
    `D-WSUFFIX`, `D-LUI-AUIPC`, `D-ADDR-WRAP`).** `INT64_MAX + 1` and `INT64_MIN - 1` wrap,
    on both the register and the immediate path; `INT64_MAX + INT64_MAX` wraps to -2; the
    immediate extremes -2048/2047; `addiw`/`addw`/`subw` 32-bit wraps sign-extend (operand
    carries garbage upper bits to prove they are ignored); `slt`/`sltu` at the signed
    extremes (the 0-result pre-written); `slti`/`sltiu` at the immediate extremes; `lui
    0x7FFFF` (positive U edge) vs `.1`'s `lui 0x80000`; `auipc 0x80000` at entry +
    4n — the sign-extended offset wraps modulo 2^64 and the result is exactly 4n. No memory
    crossings. ~30 steps.
  - **`bound-ext` — sign/zero extension at the sign edges (`D-LOAD-EXT`).** The byte edge
    0x7F/0x80, the halfword edge 0x7FFF/0x8000, the word edge 0x7FFFFFFF/0x80000000, each
    through the sign/zero PAIR at one address (the pair is the observation); the all-ones
    value at each width; the 0x00 byte observed through a pre-write. Store truncation at
    values where the truncated result differs from BOTH clamping outcomes (0x180 → 0x80,
    0xFFFF8000 → 0x8000 / 0xFFFF8000). ~43 steps, ~32 census-pinned crossings.
  - **`bound-alias` — alias, overlap and state interactions (`D-ENDIAN`, `D-LOAD-EXT`,
    reset-state rules).** The little-endian lane proof: `sd 0x0807060504030201` then `lbu`
    at each of the 8 byte lanes. Overlap composition: `sd` + `sb` over byte 3 + `sh` over
    bytes 6–7 + one `ld` read-back of the composed word. Register aliasing: `add x,x,x`
    doubling, `sub x,x,x` (nonzero → 0 transition), `slt x,x,x` (pre-written 1 → 0),
    self-referential `slli x,x,x`, and `lb x24, x24, 0` — a load that overwrites its own
    base register, proving the address is sampled before the write commits. x0: `addi x0,
    x0, -1` writes nothing (empty-writes expectation), `sw x0` zeroes a word (read back
    through `ld`). ~33 steps, ~16 census-pinned crossings.
  - **The visibility rule governs every reused destination** (measured in `.1`: the
    observation vocabulary is the VISIBLE register change, `run.rs`'s `diff(before, state)`):
    sweep operands are chosen so consecutive results differ, and every identity or 0-result
    is pre-written to a distinct value.
  - **Exhaustion judgement, stated:** the tractable reduced-width domains are the shamt
    FIELDS (6-bit = 64 values, 5-bit = 32) — each is exhausted once. The data-value domains
    (2^64, 2^32, 2^8) are intractable or near it, and their discriminating structure is the
    sign edge and the wrap point — enumerated as boundaries, not swept. A 256-point byte
    sweep was considered and rejected: the extension logic is generic over the width, so the
    edge pair discriminates everything the sweep would, at 1/40 the corpus cost.
  - **Reviewed ceiling expansion** (the `.1` decision names this leaf's guest growth as its
    own reviewed decision): the corpus grows 9 → 14 guests (+10 tracked files under
    `profiles/rv64i-lab-v0/guests/`), so `profiles/` rises 32 → 42 files and ~220 KB →
    ~315 KB aggregate. `doctrine/readme_routes.tsv`: `ceiling_lines` 34 → 46 (42 + 4
    headroom, the registry's proportional rule), `ceiling_bytes` 262144 → 393216 (the same
    ~1.2× band the existing ceiling holds), health targets re-based to the measured size.
    ⛔ `ceiling_part_bytes` stays 32768 — the per-part bound answers "has one member become
    the monolith", and no new file approaches it (largest: `bound-shift.expected.sexp`,
    ~27 KB); sweep derivations are deliberately terse to keep it that way.
  - **Cascades owned by this leaf:** `gen_guests.py`'s guest tuple and `guests.rs`
    regenerated; `run/tests.rs` gains one suite per guest (all `Stop::Budget`);
    `mutate.rs`'s `pinned_census` gains `bound-ext`'s and `bound-alias`'s crossings with
    per-line justifications and the three ALU guests join the empty arm;
    `run_semulith_smoke.py`'s guest tuple; both `G?-REPORT.md` regenerate (counts are
    derived); the browser bench enumerates guests dynamically — its arm count grows 13 → 18
    with no edit; `EXERCISE-COVERAGE` stays 52/52 (the scope did not change).
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
  Design (recorded before code, `2026-09-29` — every reference behavior below was MEASURED
  against sail-riscv 0.14 AND spike 1.1.1-dev by an untracked probe suite
  (`target/refs/guests/probes/`, 13 probe ELFs) before any guest was authored; the probes'
  traces are the measurement record, the guests below re-pin every one of them as tracked,
  spec-derived expectations):
  - **Measured: the misaligned JUMP does not write `rd`; semulith does — a MODEL DEFECT
    (new, found by the probe; logged below as DEFECT-B).** `jal x5, +2` and
    `jalr x5, 0(x1)` with x1 = 3 (the bit-0 clear leaves 2): both references raise
    instruction-address-misaligned ON THE JUMP, tval = the target (0x80000006 / 0x2), and
    spike emits NO commit record for the jump while sail shows no `x5` write — the link
    write is suppressed. Semulith writes `x5 <- pc+4` BEFORE trapping. ROOT CAUSE: the
    `jal`/`jalr` effect trees in `definitions/riscv/rv64i.sem.sexp` evaluate
    `(set (reg rd) (add (pc) (lit 4)))` BEFORE `set-pc`'s alignment check. FIX (semantics
    data, never evaluator): reorder the trees — `set-pc` first, then the link write.
    `(pc)` reads the frame's constant instruction address, so the reorder is exact on the
    success path and suppresses the write on the fault path, which is the architecture's
    rule for an instruction that raises a synchronous exception (RVI-RV32I §1.1.5.2
    raises the exception ON the jump; both references suppress the write). Falsified by
    `fault-jal-mis` / `fault-jalr-mis` below (`never_written x5`) and by the whole
    14-guest corpus re-run (guest-control jumps constantly).
  - **Measured: the reserved-`fm` FENCE defect is INVERTED — the dossier was wrong, the
    model is right; DEFECT-A becomes a DOSSIER correction.** RVI-RV32I §1.1.7, verbatim
    from the pinned artifact: *"Base implementations shall treat all such reserved
    configurations as FENCE instructions (with fm = 0000)"* and *"For forward
    compatibility, base implementations shall ignore these fields"* (rs1/rd). Reserved
    fm/pred/succ configurations are NOT the UNSPECIFIED reserved-decode case — the
    architecture specifies their behavior: execute as FENCE. Both references execute
    `fence fm=1` (0x1ff0000f) as a nop (sail prints `.insn`, spike `fence iorw,iorw`),
    `fence.tso rw,rw` as a nop, and `fence rd=x1` as a nop — exactly what semulith does.
    FIX: D-FENCE's last sentence ("Other fm values are reserved and fall under
    D-RESERVED-DECODE") is corrected in `profile.sexp` (and its `requirements.sexp`
    restatement) to the spec's mandate; `fault-fence` pins the corrected behavior
    three-way. NO legality constraint is needed anywhere in the encoding format — the
    `.1` note's premise is removed by the spec text itself.
  - **Measured: reserved encodings raise illegal-instruction with tval = the WORD, on
    both references — the laboratory's D-RESERVED-DECODE policy conversion is three-way
    provable.** 0xFFFFFFFF: sail `illegal-instruction` tval 0xFFFFFFFF, spike
    `trap_illegal_instruction` tval 0xffffffff; semulith reports
    `Undefined(ReservedDecode)`. `slliw` with imm[5] = 1 (0x0410911B): BOTH references
    raise illegal-instruction, tval = the word — **OQ-2 is ANSWERED**: neither current
    reference treats the reserved `*IW` shamt as executable; sail 0.14 and spike
    1.1.1-dev both trap, matching the laboratory policy's observable. Semulith already
    routes it to `ReservedDecode` (funct6 is mask-pinned). POLICY (the conversion is the
    laboratory's explicit act, one layer up — `run.rs`, the harness, never the
    interpreter): on `StepOutcome::Undefined(ReservedDecode{at})` the runner appends the
    policy-converted observation `(pc, word, [], trap = (0x02, word))` and stops with
    `Stop::Undefined` — the source classification (SEM-07's "must be able to report that
    the case WAS unspecified") is preserved in the stop reason and the CLI's stderr
    report, while the trace vocabulary carries what the laboratory's declared policy
    makes of it. `fault-reserved` and `fault-shiftw-res` pin this three-way.
  - **Measured: a fetch access fault on a jump TARGET is reported ON THE TARGET, with
    NO instruction word — the observation vocabulary must learn a word-less step.**
    `jalr` to 0x40000000 (outside sail's MainMemory region AND spike's DRAM, not a
    device on either): spike reports `trap_instruction_access_fault`, **epc =
    0x40000000**, tval = 0x40000000 — with no commit and no disasm line at the target
    (the current adapter REFUSES this shape); sail records the `jalr` step then
    `fetch-access-fault` tval = 0x40000000 (the current adapter would mis-attach the
    trap to the jump step — the opposite reporting point from `misaligned-fetch`, which
    DOES belong to the jump; the two rules point in opposite directions exactly as
    D-MISALIGN-REPORT / D-FETCH-FAULT-REPORT say). Semulith stops with
    `Stop::FetchFault` and records no observation — the gap `run.rs` names as future
    work; this leaf closes it. VOCABULARY EXTENSION: `run::Step.word` becomes
    `Option<u32>`; the runner emits the honest step `(pc = at, word = None, [],
    trap = (0x01, at))` and keeps `Stop::FetchFault` as the stop reason. Adapters:
    sail's `fetch-access-fault` synthesizes a word-less step at pc = tval (cascade
    lines after the first trap are ignored); spike's `trap_instruction_access_fault`
    with an unrecorded epc synthesizes the word-less step at epc (other causes keep the
    strict refusal); the CLI prints `(fetch fault)` for the word-less step and
    `parse_semulith` reads it back. `fault-fetch` pins it three-way.
  - **Measured spellings the adapter learns (from the pinned causes table's codes, the
    models' own words):** sail `misaligned-fetch` → 0x00 and `store/amo-access-fault`
    → 0x07. Unknown spellings still raise; each addition gets RED/GREEN self-test arms.
  - **Measured: a store over a later-fetched word is visible IMMEDIATELY on all three
    models.** `sw` patching `addi x2, x0, 2` into `addi x2, x0, 7`: sail and spike both
    write x2 = 7 (spike's commit line even shows the store: `mem 0x80000014
    0x00700113`). D-CODE-VISIBILITY's laboratory choice is three-way pinnable; the
    dossier's "a caching reference is not wrong" caveat stays true but does not fire on
    these two references. `fault-selfmod` pins it.
  - **Measured and RECORDED, not exercised: `fence.i` executes on both references
    although the matched ISA strings exclude Zifencei** (sail `rv64i_zvl32b` with
    `Zifencei supported false` still runs 0x0000100F; spike `--isa=rv64i` runs it). Our
    model reports it as a reserved encoding (the profile declares Zifencei absent) and
    the laboratory policy converts to illegal-instruction — a legitimate UNSPECIFIED
    divergence the comparator cannot yet express (`cross_model` disables only spike,
    and disabling sail too would leave the guest no live comparison). RECORDED as a new
    measured difference `DIFF-FENCEI-EXECUTED` in `references.sexp`; the guest that
    pins it is routed to `.4` (the interaction matrix's expected-divergence
    comparison), not built here.
  - **Also measured, all agreeing, becoming guests:** a not-taken branch to a
    misaligned target raises nothing (all three); `lw x0` at a misaligned address still
    raises cause 0x04 (D-LOAD-X0, both references); `ld` at 0x40000000 raises cause
    0x05 tval = address on all three (guest-no-device's 0x0200_BFF8 is spike's CLINT —
    0x40000000 is outside BOTH platforms, so the access-fault guests run cross-model,
    no skip); `lh +1` / `ld +4` misalignments agree (0x04); store misalignments agree
    (0x06).
  - **Eighteen new guests**, every expectation derived from the pinned specification
    prose BEFORE any model runs (EVD-05), each step carrying `derivation` + `source`;
    the trap step is always last (a contained trap stops the laboratory run, the
    smoke-trap pattern):
    `fault-jal-mis` (3 steps — trap (0x00, target) on the jump, `never_written x5`,
    DEFECT-B pin), `fault-jalr-mis` (3 — the bit-0-clear leaves a misaligned 2),
    `fault-branch-nt` (14 — all six branch forms NOT taken with misaligned targets,
    fall-through writes prove continuation, an aligned taken branch proves liveness;
    the suppressed-effect guest, SEM-06), `fault-fetch` (3 — the word-less step at the
    target, D-FETCH-FAULT-REPORT), `fault-ld-mis-h` (3 — `lh` at +1), `fault-ld-mis-d`
    (3 — `ld` at +4, the 4-aligned-but-not-8 case), `fault-st-mis-h` (3 — `sh` at +1;
    the crossing log proves the store never crossed the boundary),
    `fault-st-mis-w` (3 — `sw` at +2), `fault-st-mis-d` (3 — `sd` at +4),
    `fault-ld-x0-mis` (3 — `lw x0` at +2 still faults, D-LOAD-X0 misaligned path),
    `fault-ld-x0-fault` (3 — `ld x0` at 0x40000000 still faults, D-LOAD-X0 access-fault
    path), `fault-access-ld` (3 — cause 0x05, cross-model: 0x40000000 is no platform's
    device), `fault-access-sd` (3 — cause 0x07), `fault-reserved` (2 — 0xFFFFFFFF →
    (0x02, word), `Stop::Undefined`), `fault-shiftw-res` (2 — the OQ-2 closure),
    `fault-fence` (8 — the corrected D-FENCE: reserved-fm nops, fence.tso nops, rd/rs1
    nonzero ignored, pred/succ = 0 HINTs nop; ends on Budget), `fault-hints` (10 — the
    RV64I HINT table's ALU forms with rd = x0 execute as nops writing nothing:
    `lui x0`, `auipc x0`, `addi x0` (rs1 ≠ x0), `addiw x0`, `addw x0`, `sllw x0`,
    `sub x0`, and the NTL.P1 code point `add x0, x0, x2`; the semihosting markers are
    deliberately EXCLUDED — spike implements semihosting off a specific three-instruction
    sequence and a lone marker near a trap is a fragile probe), `fault-selfmod` (7 —
    D-CODE-VISIBILITY pinned three-way).
    The raw reserved words (0xFFFFFFFF, the imm[5] `slliw`) cannot be emitted by the
    assembler's operand path — `riscv_asm.py` learns a `.word 0x…` directive: a raw
    data word, the honest spelling of "this guest deliberately places a reserved
    encoding" (the assembler's range checks exist precisely to refuse these through the
    mnemonic path).
  - **Reviewed ceiling expansion** (the `.1`/`.2` decisions name each leaf's guest
    growth as its own reviewed decision): the corpus grows 14 → 32 guests (+36 tracked
    files under `profiles/rv64i-lab-v0/guests/`), so `profiles/` rises 42 → 78 files
    and ~307 KB → ~390 KB aggregate (trap-guest expectations are 1–3 KB each).
    `doctrine/readme_routes.tsv`: `ceiling_lines` 46 → 82 (78 + 4 headroom, the
    registry's proportional rule), `ceiling_bytes` re-based to the measured aggregate
    under the same ~1.2× band (≈ 470 KiB; the exact figure is re-derived from the
    landed corpus at implementation), health targets re-based. ⛔ `ceiling_part_bytes`
    stays 32768 — no new file approaches it (largest: ~4 KB). Consolidation was
    considered and rejected: one trap ends a run (the laboratory's contained-trap
    contract), so each fault case that needs its own cause/tval observation needs its
    own guest; merging unrelated traps into one guest is impossible by construction.
  - **Cascades owned by this leaf:** the sem-tree reorder regenerates `definition.rs`
    through the sanctioned generator (no interpreter change — the evaluator is
    untouched; DEFECT-B's fix is DATA); `run.rs`'s `Step.word` → `Option<u32>` with the
    fetch-fault step and the reserved-decode policy conversion, its doc comments
    re-synced (the "future work" sentence is deleted by this leaf); `bench.rs` and
    `mutate.rs` follow the type change; the CLI prints the two new step shapes;
    `compare_traces.py` (word-less steps, the two new sail spellings, the spike
    synthesis, self-test arms); `riscv_asm.py`'s `.word` directive; `gen_guests.py`'s
    guest tuple (18) and `guests.rs` regenerated; `run/tests.rs` gains one suite per
    guest (the fault suites assert the trap pair and the stop reason — `Stop::Trap`,
    `Stop::FetchFault`, or `Stop::Undefined` — exactly as the scope-ecall pattern
    does); `mutate.rs`'s census: `fault-selfmod` contributes its one aligned in-region
    store crossing, the other 17 join the empty arm with per-line justifications;
    `run_semulith_smoke.py`'s tuple; the routes-registry ceilings (above); OQ-2's
    answer lands in `DOSSIER.md` and `requirements.sexp`
    (`REQ-D-SHIFTW-RESERVED`'s open note resolves — both references measured);
    `references.sexp` gains `DIFF-FENCEI-EXECUTED`; both `G?-REPORT.md` regenerate
    (counts are derived); the browser bench enumerates guests dynamically (its arm
    count grows with no edit); `EXERCISE-COVERAGE` stays 52/52 (no new form — the fault
    guests exercise declared forms and reserved words, neither of which is a scope
    change). The book (`plan/p2.md`) carries the result; claim-scope and p1 pages
    re-sync to 32 guests.
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
| 1 | `P2-SCALAR.4` | `pending` | scope exercised (`.1`), boundaries pinned (`.2`), faults/suppression/reserved pinned (`.3`); the declared fault × alias × boundary × event × progress × restart matrix is the next evidence layer — and it owns the expected-divergence comparison the `fence.i` guest (`DIFF-FENCEI-EXECUTED`) is routed to |

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

## Acceptance Checklist (leaf P2-SCALAR.1)

- [x] **REPRODUCE / ISSUE** — the declared scope was 52 forms; only 15 had ever executed.
  The instrument built for this leaf measured the hole against the real corpus before any
  fix existed:

  ```
  $ bash scripts/check_exercise_coverage.sh
  EXERCISE-COVERAGE: the declared scope is not fully exercised (coverage 15/52).
    UNEXERCISED profiles/rv64i-lab-v0/profile.sexp: 'addw' … (37 forms named, rc=1)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: EXTRACTION proves every declared form HAS
  encoding+semantics+requirement (static sufficiency), but nothing measured the dynamic
  half — guests were written for P0/P1's smoke needs (15 mnemonics), never for scope
  completion, and no gate counted the difference. WHERE, measured: the denominator is
  `profiles/rv64i-lab-v0/profile.sexp` `[scope]`; the exercised set was the union over the
  four `guests/*.expected.sexp` — and a second, smaller hole sat one layer down: `fence`
  could not even be assembled, because `gen_fragments.py`'s `USED_FIELDS` whitelist
  predated any fence guest:

  ```
  $ python3 -c "… Assembler('profiles/rv64i-lab-v0/encoding.sexp').assemble(['fence'])"
  AsmError: 'fence' uses operand field 'fm', which this assembler does not support
  $ bash scripts/check_exercise_coverage.sh | sed -n 1,2p   # the measurement, re-runnable
  EXERCISE-COVERAGE: the declared scope is not fully exercised (coverage 15/52).
  ```

- [x] **FIX** — five scope-completion guests + EVD-05 expectations (derived before any
  run); `fm`/`pred`/`succ` added to `USED_FIELDS` and `CONTIGUOUS_OPERANDS` (the pinned
  `arg_lut.csv` carries them), `definitions/riscv/rv64i.sexp` and `definition.rs`
  regenerated through the sanctioned generators; `gen_guests.py`'s tuple extended and
  `guests.rs` regenerated (9 guests); `mutate.rs`'s census gained `scope-mem`'s 17
  crossings; `run/tests.rs` gained five guest suites; `compare_traces.py` learned the
  measured ecall/ebreak spellings; `gate_report.py`'s guest claims derived; the 24th
  doctrine `EXERCISE-COVERAGE` registered with a 7-arm self-test. All at the lowest-risk
  level: data (guests), whitelists fed by the pinned table, and one new check — no
  interpreter change.

- [x] **ADDRESSED (verified)** — before→after, same command:

  ```
  $ bash scripts/check_exercise_coverage.sh     # before: 15/52, rc=1 (37 named)
  EXERCISE-COVERAGE: ok (1 profile(s) — every declared form exercised, 52/52)
  $ python3 scripts/run_semulith_smoke.py       # the live three-way differential
  …scope-alu/-mem/-branch/-ecall/-ebreak: AGREE vs sail-riscv AND spike…
  run_semulith_smoke: ok — 9 guests, 117/117 aligned steps, byte-identical reproduction
  ```

- [x] **NO REGRESSION** — the guard set re-run, green:

  ```
  $ make check            # 133 verify suites (+5 guest suites), 5 core suites, clippy -D warnings
  $ make gate             # 24 doctrines green (EXERCISE-COVERAGE among them)
  $ make smoke-bench      # 13 arms — 9 clean guests, 3 trace-level mutants, the census arm
  $ bash scripts/check_exercise_coverage.sh --self-test   # 7 pass / 0 fail
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (P2 1/9,
  24 doctrines, 261 arms), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier
  `.2`), this tree, the book (`plan/p2.md` carries the result; `plan/p1.md` and
  `claim-scope.md` re-synced to 9 guests / 117 steps), the doctrine mirrors
  (`DOCTRINE_ENFORCEMENT.md`, `docs/book/src/working/doctrines.md`), `TOOLBOX.md` (the new
  row), and both regenerated `G?-REPORT.md`.

## Acceptance Checklist (leaf P2-SCALAR.2)

- [x] **REPRODUCE / ISSUE** — the corpus exercised every declared FORM (`.1`), but the
  boundary DOMAINS had only incidental samples: across the whole pre-leaf corpus, exactly
  four distinct immediate shift amounts had ever executed, and no guest had wrapped a
  signed extreme, probed a sign edge at exactly 0x80/0x8000/0x80000000, composed
  overlapping stores, or self-aliased a destination (rd = rs1 = rs2):

  ```
  $ git grep -h -E '^[[:space:]]*(slli|srli|srai|slliw|srliw|sraiw)[[:space:]]' HEAD \
        -- 'profiles/rv64i-lab-v0/guests/' | sed -E 's/#.*$//' \
      | grep -oE '[0-9]+[[:space:]]*$' | tr -d ' ' | sort -n | uniq
  25
  31
  32
  63
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY: the P1 guests were written for smoke coverage and
  the `.1` guests for form coverage — one instance per form — and neither brief includes
  the boundary structure of an operator (the shamt FIELD's 64/32 values, the wrap points,
  the sign edges, self-aliasing). Nothing was wrong; an evidence layer the leaf's
  acceptance names was simply unwritten. WHERE, measured: the exercised-amount census is
  the REPRODUCE box's command (4 of 64 values); the self-alias census is directly
  enumerable — a destination aliased onto BOTH its sources did not exist in the corpus
  (BSD grep: backreferences need the basic-syntax form, not `-E`):

  ```
  $ git grep -h '\(add\|sub\|slt\|sll\|sra\) \(x[0-9][0-9]*\), \2, \2\(,\|$\)' HEAD \
        -- 'profiles/rv64i-lab-v0/guests/' | wc -l        # before
  0
  $ grep -h '\(add\|sub\|slt\|sll\|sra\) \(x[0-9][0-9]*\), \2, \2\(,\|$\)' \
        profiles/rv64i-lab-v0/guests/*.s | wc -l          # after
  4
  ```

- [x] **FIX** — five boundary guests with EVD-05 expectations (every value computed by
  spec-rule arithmetic at authoring time, before any model ran, each step carrying
  derivation + source): `bound-shift` (89 steps — the 6-bit shamt domain exhausted by one
  `srli` sweep), `bound-shiftw` (55 — the 5-bit domain exhausted by one `sraiw` sweep, the
  rs2 = 96 `srl`/`srlw` discriminator pair), `bound-arith` (31 — wraps, immediate extremes,
  the `auipc` sign-edge wrap), `bound-ext` (47 — the sign-edge pairs, 32 crossings),
  `bound-alias` (37 — endian lanes, overlap composition, register aliasing, x0; 16
  crossings). Cascades as designed: `gen_guests.py`'s tuple, `guests.rs` regenerated, five
  `run/tests.rs` suites, `mutate.rs`'s census (48 new pins, per-line justifications), the
  smoke tuple, the routes-registry ceilings, both gate reports regenerated. No interpreter
  change — data and pins only.

- [x] **ADDRESSED (verified)** — before→after, same census command: 4 → 64 distinct
  immediate shift amounts (the 6-bit domain complete, the 5-bit domain within it), and:

  ```
  $ cargo test -p semulith-verify          # the offline differential, commitment-gated
  test result: ok. 138 passed; 0 failed (+5 guest suites; the census pin re-derives
  bound-ext's 32 and bound-alias's 16 crossings from the real runs)
  $ python3 scripts/run_semulith_smoke.py  # the live three-way differential
  …bound-shift/-shiftw/-arith/-ext/-alias: AGREE vs sail-riscv AND spike…
  run_semulith_smoke: ok — 14 guests, 376/376 aligned steps, byte-identical reproduction
  ```

- [x] **NO REGRESSION** — the guard set re-run, green; and the gate caught two AUTHORING
  slips during the leaf (the overlap-composition constant, twice), both corrected by
  re-deriving from the spec rule — the instrument discriminates in the right direction:

  ```
  $ make check            # 138 verify suites (+5), 65 core suites, clippy -D warnings, fmt
  $ make gate             # 24 doctrines green (GUEST-GEN, GATE-REPORT, the new ceilings…)
  $ make smoke-bench      # 18 arms — 14 clean guests, 3 trace-level mutants, the census arm
  $ bash scripts/check_exercise_coverage.sh [--self-test]   # 52/52; self-test 7/0
  ```

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (overwritten), `LIVE_STATUS.md` (P2 2/9),
  `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (frontier `.3`), this tree, the book
  (`plan/p2.md` carries the result; `plan/p1.md` and `claim-scope.md` re-synced to 14
  guests / 376 steps), the routes registry (the reviewed ceilings), and both regenerated
  `G?-REPORT.md`.

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
