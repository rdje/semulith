# P2-SCALAR — archived completed-leaf evidence

The full, unedited acceptance checklists for the `done` leaves `.1` and `.2` of the
[`P2-SCALAR`](../P2-SCALAR.md) tree (the most recent done leaf's, `.3`, stays live per the
`P1-LAB` precedent), plus the recorded-before-code design detail of the completed leaves
`.1`–`.3`, split out on `2026-09-29` when the live file crossed its per-part ceiling — the
ceiling was obeyed, not raised, per the `docs/tasks/` precedent set by `SOT-FORMAT` and
continued by `P1-LAB`. The live tree keeps the frontier, the decisions, the open questions,
the blockers, the defect log, every leaf's goal/acceptance/result, the active leaf's design
and checklist, and both logs.

Archived sections, verbatim:

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

---

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

---

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
