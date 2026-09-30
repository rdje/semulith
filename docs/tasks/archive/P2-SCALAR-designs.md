# P2-SCALAR — archived completed-leaf designs

The recorded-before-code design detail of the completed work of the
[`P2-SCALAR`](../P2-SCALAR.md) tree — leaves `.1`–`.4`, `.5`'s landed strands 2 and 3,
and `.6`'s discrepancy census — split from `P2-SCALAR.md` (the checklist archive)
on `2026-09-30` when the combined archive crossed the per-part ceiling. The ceiling
was obeyed by the split, not raised. The checklists live in `P2-SCALAR.md` beside
this file. Archived design sections, verbatim:


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

---

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

---

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

  Strand 2 design (recorded before code, `2026-09-30` — measured against the PINNED FETCH
  itself, not the planning docs alone; the probe material is the sparse clone named below):
  - **The fetch, measured.** A blobless sparse clone of `github.com/riscv/riscv-arch-test`
    at the pinned commit `e2216915d9a17acc142610831d88de8b65683866` stands at
    `target/refs/riscv-arch-test/` — untracked, the reference binaries' standing, on the
    repository volume (data-locality policy). Sparse paths: `tests/env/` (784 KB — the
    macro headers), `tests/rv64i/I/` (13 MB — the campaign), `config/` (2.3 MB — the
    example DUT configs); 45 MB on disk. The "~672 MB" figure in the materials catalogue
    is the WHOLE generated tree; the RV64I campaign needs 13 MB of it. Re-fetch:
    `git clone --filter=blob:none --no-checkout <url>`, `git sparse-checkout set
    tests/env tests/rv64i/I config`, `git checkout e2216915…`. Census (measured): **51
    test files** — exactly one per RV64I instruction row of the cached
    `testplans/I.csv` (51 rows, all `RV64=x`) — 199,768 lines, **18,092 `RVTEST_SIGUPD`
    invocations, 14,820 testcases**. Every file's YAML header reads
    `REQUIRED_EXTENSIONS: ['I']`, `MARCH: rv64i_zicsr_zifencei`, `MXLEN: 64`.
  - **The suite's mechanism, measured from the pinned headers** (`tests/env/*.h` — the
    cached README's "0.13.1" is stale; the checked-in `sail.json` targets the 0.14.1
    schema). A test is one self-contained gas-syntax `.S` including only
    `riscv_arch_test.h`. `RVTEST_SIGUPD(sigptr, link, temp, result, …)` in SIGNATURE mode
    (no `RVTEST_SELFCHECK`) stores the result word to the signature region
    (`SIG_STRIDE` = 8 for rv64i); `sail_macros.h` is forcibly included in this mode and
    redefines halt/console to HTIF `tohost` stores. The region, between the `.global`
    symbols `begin_signature`/`end_signature`: a canary, `SIGUPD_COUNT`×8 bytes of
    `0xdeadbeef` fill (a per-file define, 10 over the file's sigupd count), the
    `final_sig_offset` slot, a trap-signature reservation (`TRAP_SIGUPD_COUNT` default
    15000 → 120 KB), the end canary. The host reads the bounds from the ELF symbol
    table. Termination: `RVMODEL_HALT_PASS/FAIL` = `tohost ← 1 / 3` in a store loop; the
    console is `tohost` byte pairs carrying the suite's own verdict strings
    (`RVCP-SUMMARY: TEST SIGRUN/PASSED/FAILED`).
  - **The observation-vocabulary adaptation — the strand's core decision.** Run the
    SIGNATURE-mode build, never the self-check build (its `SIGNATURE_FILE` format lives
    in the un-fetched framework; trace-based extraction is the laboratory's native
    vocabulary and gives first-mismatch minimization, `EVD-02`). The laboratory's
    observation vocabulary gains the one thing the campaign needs: **data-store
    crossings**. The runner already records every boundary crossing (`run.rs`'s
    `Vec<Crossing>`, request and answer); the CLI discards it. `semulith run` learns a
    store trace (each data store — address, width, value — interleaved with the steps):
    sail's `--trace-mem` equivalent, an observability addition; the interpreter and the
    semantics data are untouched. From each model's store trace the harness extracts the
    writes into `[begin_signature, end_signature)` (the per-testcase signature words)
    and the `tohost` stores (the completion verdict — 1 pass-shape / 3 failure — and the
    console text).
  - **Sail-derived expectations, EVD-04-recorded.** sail-riscv 0.14 (our pin) runs each
    ELF under the SAME matched lab override (`rv64i-lab-v0`: one MainMemory region
    `0x8000_0000` + 2 GB — identical to the suite's default RAM map — no devices,
    misaligned raises); its stores to the signature region ARE the expected values,
    recorded as **external tests with Sail-derived expectations** — the
    `references.sexp` independence row (act4 shares Sail's semantics by construction)
    already forbids reading agreement as a second opinion. spike runs the same ELFs as
    the CONTROL PAIR: spike-vs-sail over the signature is the genuine differential;
    semulith-vs-signature is the external-test evidence. ⚠️ spike's bundled board
    (`DIFF-PLATFORM-SPIKE`) is a stated precondition, held by the link map: HTIF is
    spike's native mechanism and every test byte lives at ≥ `0x8000_0000`, never in
    `0x1000` or `0x0200_0000..0x11ff_ffff`.
  - **The DUT-side pieces this project authors** (tracked, `profiles/rv64i-lab-v0/act4/`
    — the framework normally generates them from UDB; the minimal honest set is
    hand-written): `rvtest_config.h` (`UDB_MXLEN 64` + `UDB_MXLEN_64` and NOTHING else —
    no `STANDARD_SM_SUPPORTED`/`S`/`U`/`F`: the trap handlers, T-SBI and every CSR path
    compile out; measured by grep over all 51 files — no body carries a CSR or `fence.i`
    instruction outside compiled-out guards), `rvmodel_macros.h` (every macro
    `check_defines.h` refuses the build without: `RVMODEL_HALT_PASS/FAIL`,
    `RVMODEL_IO_WRITE_STR`, `RVMODEL_DATA_SECTION` (tohost/fromhost), the
    interrupt-latency/timer/MSW set — defined even though `sail_macros.h` overrides the
    halt/console trio in sig mode), `link.ld` (the `sail-RVI20U64` shape:
    `TEST_BASE = 0x8000_0000` = the lab's declared region base,
    `.text.init`/`.text.rvtest`/`.rodata`/`.data`/`.bss`/stack(0x20000)/`.text.rvmodel`
    last, `ENTRY(rvtest_entry_point)`).
  - **The harness** (tracked, `scripts/run_act4_campaign.py`): per test — assemble+link
    with the pinned clang 21.1.8 + `ld.lld` 21.1.8 (`-march` from the file's own `MARCH`
    key, `-mabi=lp64 -mno-relax`, `-I tests/env -I <act4 config>`, `-DTEST_FILE`,
    `-DTEST_FLEN=32`, `-DSAIL_CLINT_BASE_ADDRESS=0x2000000` and
    `-DSAIL_SIMPLE_INTERRUPT_GENERATOR_BASE_ADDRESS=0xC000000` — `sail_macros.h`'s
    compile-time demands; those addresses are never touched by an I-suite test, and a
    store there access-faults on all three models — a detectable failure, not a silent
    assumption) into `target/refs/guests/act4/` (untracked); run all three models under
    a budget; extract signatures and verdicts; compare semulith against the Sail-derived
    signature word-by-word (first mismatch = the minimized discrepancy, naming the
    testcase by sigupd ordinal) and spike against sail likewise; record per-test
    verdicts.
  - **The record**: `profiles/rv64i-lab-v0/act4.sexp` behind a new `schema/act4.sexp`
    family (the RECORD-SCHEMA layer admits no un-gated dossier): the campaign metadata
    (pin, toolchain, model versions, counts) and per-test rows (file, sigupd count,
    signature sha256, the two comparison verdicts). The smoke corpus and the
    INTERACTION-MATRIX/EXERCISE-COVERAGE gates are untouched — ACT4 tests are an
    EXTERNAL corpus, not tracked guests; the matrix's orphan rule is not engaged.
  - **The fence watch-item.** `I-fence-00.S` exercises `fence.tso`, reserved-`fm`,
    nonzero-rs1/rd fences and a HINT — exactly the corrected `D-FENCE` and `D-HINTS`
    territory (DEFECT-A's inversion). Both references execute them as nops (measured at
    `.3`/`.4`); this test is the external check of that correction.
  - **Reviewed ceiling expansion** (the `.1` rule): `profiles/` gains the three `act4/`
    harness files + `act4.sexp` (+4) against a 99-file ceiling standing at 95 —
    re-derived at commit time with measured sizes; `schema/` +1 (inside its row's
    headroom); `scripts/` +1 (no registry row); the crates change is the CLI flag alone.
    Per-part 32 KiB stays untouched (largest new file ≈ the dossier, ~10 KB).
  - **Sizing verdict** (the strand note: outgrowing a safe slice makes it its own leaf):
    three slices, each its own commit — (a) THIS design + the fetch record + the
    acquisition facts (`references.sexp` candidate 4, the catalogue note); (b) the CLI
    store trace + the harness building ONE test (`I-add-00.S`) end-to-end three-way —
    retiring the two measured toolchain risks before the fleet: clang 21.1.8 assembling
    the suite's macro machinery (the docs name LLVM 22 / GCC 15) and sail-0.14's HTIF
    behavior under our override; (c) the 51-test campaign, the record, the gates, the
    book. A framework-absence blocker discovered in (b) (e.g. `derived_config.h` needing
    more than the minimal set) promotes the strand to its own leaf instead.

  Design (recorded before code, `2026-09-30` — the census over every recorded difference
  and every campaign result, each dispositioned with its citation):
  - **The census.** Eight `difference` records in `references.sexp` + the live corpora
    (48 guests, 642/642 steps; the ACT4 campaign 51/51, 17,017 slots; the offline
    differential; the mutation suite). Dispositioned: `DIFF-ELF-STRICTNESS` (harness —
    the writer fixed at P0), `DIFF-RESET-VECTOR` (harness — alignment, not semantics),
    `DIFF-TRAP-RECORD-SHAPE` (trace vocabulary — the adapter reassembles spike's split
    record), `DIFF-FETCH-GRANULARITY` (below the profile's observation granularity),
    `DIFF-PLATFORM-DEFAULT` (a configuration DEFECT, corrected at `P0-PROFILE.10`, pinned
    by `guest-no-device`), `DIFF-PLATFORM-SPIKE` (a layer difference — the reference
    bundles a board; a stated precondition, not minimizable into a model defect),
    `DIFF-TVAL-PHYS-MASK` (reference-vs-REFERENCE — sail masks, spike AND semulith agree
    on the full address; nothing of ours to minimize). **One genuine
    model-vs-references behavioral divergence exists: `DIFF-FENCEI-EXECUTED`** — the
    legitimate UNSPECIFIED case (the profile declares Zifencei absent; both references
    execute fence.i anyway), already pinned by `it-fencei`'s expected-divergence
    protocol.
  - **The minimization.** `it-fencei` is 3 instructions (agreeing prefix, fence.i, the
    continuation marker). The minimal reproducer of the divergence is ONE word:
    `0x0000100F` alone — semulith's policy trap lands at step 0, the references nop and
    run off the end into the zero word (measured: both raise illegal-instruction there —
    they stay each other's control over their full 2-step length). The minimized case is
    retained as the tracked guest `min-fencei` (expect_divergence at_step 0 — the prefix
    agreement is vacuous, the protocol's four legs unchanged). ⛔ The hand route, not
    `semulith reduce`: the reducer minimizes a guest against a MUTATION's divergence
    (P1-LAB.9); a reference difference has no mutant table row, and widening the
    reducer's scope for one word would be machinery beyond the case.
  - **What is deliberately NOT done:** no mask widened, no expected value edited
    (EVD-05/AI-05 — the census found no discrepancy tempting either); no "reduction" of
    reference-vs-reference differences (they are the references' owners', and
    `DIFF-TVAL-PHYS-MASK`'s reopening owner is named in its record).
  - **Cascades:** `min-fencei` × 2 files; `gen_guests.py` + `guests.rs`; one
    `run/tests.rs` suite (Stop::Undefined at entry, trap (0x02, 0x100F)); the census
    (empty arm + justification); the smoke tuple; the matrix (F×E, beside `it-fencei` —
    same difference id); the G-reports regenerate; the book. `profiles/` 116 → 118 —
    inside the reviewed 120 ceiling. `EXERCISE-COVERAGE` stays 52/52.

  Strand 3 design (recorded before code, `2026-09-30` — the gap analysis is MEASURED by a
  census over the tracked corpus, the compiled `c-scope.elf` disassembly, and the ACT4
  testplan/bodies; the two uncertain behaviors were then MEASURED BY PROBE
  (`target/refs/guests/probes/run_probes_p25s3.py`, 2 probe ELFs) against sail-riscv 0.14
  AND spike 1.1.1-dev AND semulith before any guest was authored — the `.3`/`.4`
  doctrine):
  - **The census verdicts** (each a measured coverage claim, not a remembered one):
    run-off-the-end — NO COVERAGE on semulith (every straight-line guest's budget equals
    its expectation count, so the fetch past the last word never happens; the references
    do it in `it-fencei`'s fourth step, semulith never has). PROBE: the zero word traps
    illegal-instruction (0x02, tval 0, word 0) on ALL THREE — sail spells it `c.illegal`,
    spike `c.unimp`, semulith the policy-converted reserved decode; the trace adapters
    read all three spellings with the machinery already landed.
    Load→use as ADDRESS/JUMP TARGET (pointer chase, jump table) — NO COVERAGE anywhere:
    every jalr base in the corpus is LUI/ADDI/AUIPC-materialized, ACT4's jalr targets are
    `LA`-built, and `c-scope.c`'s "indirect jump through a switch" was constant-folded
    out of its ELF (the comment overclaimed the artifact — the defect is logged below and
    corrected in this strand). Load→use as DATA is saturated (ACT4's
    testdata-load→op structure).
    Cross-width SIGN-extending round-trips at sign edges — PARTIAL: `bound-ext` pins the
    same-width sign/zero pairs, `scope-mem`/`bound-alias` pin zero-extending wider reads;
    the sign-EXTENDING cross-width matrix (sb 0x80 → lh/lw/ld, sh 0x8000 → lw/ld, sw
    0x80000000 → ld, the high-lane narrow reads) is unpinned.
    Self-mod with a FENCE between store and execution — UNCOVERED (`fault-selfmod` pins
    the distance-2 no-fence shape). PROBE: the patch is visible through `fence rw,rw` on
    ALL THREE (x2 ← 7 at the patched word).
    Compare→branch (slt/slti/sub feeding the immediately following branch) — NO COVERAGE
    (corpus slt results are observed as writes; ACT4's slt is compare-and-store;
    branch-on-loaded-value is ACT4-covered).
    Loop with load+store per iteration (a memory walk) — PARTIAL (`c-scope`'s loop only
    stores).
    10+-deep serial dependency chains through VARIED producers — UNCOVERED (deepest
    pinned: 7–8, single-producer addi chains).
    x0 from every producer kind — PARTIAL: unpinned are the lb/lbu/lh/lhu/lwu/ld → x0
    success paths (only lw) and subw/srlw/sraw/slliw/srliw/sraiw → x0 (only
    addiw/addw/sllw, via `fault-hints`).
  - **Eight directed guests** (EVD-05 expectations before any run; the trap step last;
    each guest's point is the DEPENDENCE, not the ops): `dir-runoff` (3 steps — two
    writes, then the fall-through fetch of the zero word and its policy trap; cell F×E),
    `dir-chase` (a pointer chase — lw then the loaded value as the next address — and a
    two-entry jump table: lw the entry, jalr to the stub; cell A×A), `dir-ext-matrix`
    (the sign-extending cross-width round-trips at the sign edges; B×B), `dir-selfmod-fence`
    (the probed store→fence→execute; the cell `fault-selfmod` carries), `dir-cmp-branch`
    (slt/slti/sub → beq/bne, taken AND not-taken; B×E), `dir-memwalk` (a counted loop
    copying a buffer backwards — load AND store per iteration, then the closing trap;
    P×P), `dir-chain` (a 12-deep serial chain through varied producers — immediate,
    register, load, shift, *W; B×B), `dir-x0-writes` (x0 destinations from the unpinned
    producers — every load width's success path and the six unpinned *W forms; A×A).
    Final cell assignments are checked against `interactions.sexp` at authoring time —
    the INTERACTION-MATRIX orphan rule refuses a guest with no cell.
  - **Reviewed ceiling expansion** (the `.1` rule): 8 guests × 2 files → `profiles/`
    100 → 116 tracked files, aggregate re-measured at commit; `ceiling_lines` re-derived
    with the +4 headroom pattern; per-part 32,768 untouched (guest files are ~2–4 KB).
  - **Cascades owned by this strand:** the smoke tuple, `gen_guests.py` + regenerated
    `guests.rs`, one `run/tests.rs` suite per guest (`dir-runoff` asserts
    `Stop::Undefined`; the memwalk/cmp-branch traps assert `Stop::Trap`), the mutation
    census (per-line justifications), the bench's dynamic enumeration (no edit), the
    matrix's cells (orphan rule), `G?-REPORT.md` regeneration, the book (`plan/p2.md`,
    the model book's evidence chapter), and the `c-scope.c` comment correction (the
    logged defect). `EXERCISE-COVERAGE` stays 52/52 — no new form.
  Lessons (strands 1–2): `promotion: declined (the C-shift-UB lesson lives in the guest's
  own comments where it bites — section 6 names the rule, the failed draft and the
  bound-shiftw owner; the visible-change vocabulary is enforced by the comparator's two
  new self-test arms, which fail RED the day the normalization masks a real difference;
  knowledge cards would restate what the code and the gates already say)`.


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
