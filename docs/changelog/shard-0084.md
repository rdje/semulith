# CHANGELOG shard — SEMILITH-PS-0005 … SEMILITH-PS-0003

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-PS-0005 (leaf P2-SCALAR.3) — fault, suppression and reserved cases: the failure layer, pinned three-way

- Every reference behavior was MEASURED before any guest existed (16 probe ELFs against
  sail-riscv 0.14 AND spike 1.1.1-dev). Then eighteen guests pinned the measurements as
  specification-derived expectations (`EVD-05`), all agreeing three-way: **32 guests,
  454/454 aligned steps**, byte-identical reproduction.
- **DEFECT-A inverted.** The `.1` log said a reserved-`fm` FENCE must trap; the pinned
  spec mandates the nop, verbatim ("Base implementations shall treat all such reserved
  configurations as FENCE instructions (with fm = 0000)", RVI-RV32I §1.1.7), and both
  references execute exactly as the model does. The dossier was wrong, the model right:
  `D-FENCE` and its `REQ-D-FENCE`/`OB-FENCE` restatements are corrected; `fault-fence`
  pins reserved-fm, FENCE.TSO, ignored rs1/rd and pred/succ-zero configurations as nops.
- **DEFECT-B fixed in semantics data.** A misaligned `jal`/`jalr` wrote its link register
  before trapping; both references suppress the write (a synchronous exception retires
  nothing). The `jal`/`jalr` effect trees now check the target (`set-pc`) before the link
  write — the evaluator is untouched; `fault-jal-mis`/`fault-jalr-mis` pin it with
  `never_written x5`; the mutation matchers were re-derived for the new tree shape.
- **The word-less fetch-fault step.** A fetch fault on a jump TARGET is reported on the
  target with no instruction word (D-FETCH-FAULT-REPORT): `run::Step.word` is now
  `Option<u32>`, the runner emits the trap with no word and keeps `Stop::FetchFault`,
  the CLI prints `(fetch fault)`, replay round-trips the null, and both trace adapters
  synthesize the same shape — `fault-fetch` compares three-way.
- **Reserved cases keep their source meaning (SEM-07).** The interpreter reports the
  UNSPECIFIED case (`Stop::Undefined`); the laboratory's declared `D-RESERVED-DECODE`
  policy — the harness's explicit act in `run.rs`, never the interpreter — converts it
  to the illegal-instruction observation with tval = the offending word, measured
  identical on both references. `fault-reserved` (0xFFFFFFFF) and `fault-shiftw-res`
  (`slliw` imm[5]=1) pin it — the second **answers OQ-2**: both current references treat
  the reserved `*IW` shift as illegal (`REQ-D-SHIFTW-RESERVED` → `resolved`; G0 shows one
  open question where there were two).
- Suppressed effects (SEM-06): six not-taken branches to misaligned targets raise nothing
  (`fault-branch-nt`); misaligned stores never cross the boundary — proven by the
  crossing log (`fault-st-mis-h/w/d`); misaligned loads across widths (`fault-ld-mis-h`,
  the 4-aligned-but-not-8 `fault-ld-mis-d`); `D-LOAD-X0` still faults with a discarded
  destination on both failure paths (`fault-ld-x0-mis`, `fault-ld-x0-fault`); access
  faults run cross-model at 0x40000000, no platform's device (`fault-access-ld`,
  `fault-access-sd`); the RV64I HINT table's ALU forms are nops that must not trap
  (`fault-hints`); a store over a later-fetched word is fetch-visible immediately —
  measured on BOTH references first (`fault-selfmod`, D-CODE-VISIBILITY).
- Recorded, not exercised: `fence.i` executes on both references although the matched ISA
  strings exclude Zifencei — a legitimate UNSPECIFIED divergence the comparator cannot
  yet express; `DIFF-FENCEI-EXECUTED` in `references.sexp`, the guest routed to `.4`.
- Tooling: `riscv_asm.py` learned the `.word` directive for raw reserved words (its
  mnemonic path's range checks exist to refuse them); the trace adapter learned four
  measured spellings (`misaligned-fetch`, `trap_instruction_address_misaligned`,
  `store/amo-access-fault`, `misaligned-store/amo`) — its refusal fired mid-run on the
  last one, exactly as designed; adapter self-test 12/0 (+4 arms).
- Reviewed ceiling expansion: `profiles/` 42 → 78 files / 367,466 B; registry ceilings
  46 → 82 files and 393,216 → 471,040 bytes; per-part 32 KiB unchanged (largest new file
  4,017 B). Instruments caught three AUTHORING slips in flight (a systematic trailing
  paren in all 18 expectation documents, the store operand order in 4 guests, the
  REQ-D-FENCE statement drift at the gate) — never another model defect.
- Verification: 157 verify suites (+18 guest suites, +2 runner suites), 65 core suites,
  clippy `-D warnings`, `make gate` all doctrines green, `make smoke-bench` 36 arms
  (32 clean guests), `EXERCISE-COVERAGE` 52/52 (self-test 7/0), `make book` renders.
  Live: **32 guests, 454/454 aligned steps** against sail-riscv AND spike.
- Lockstep: MEMORY/LIVE_STATUS (P2 3/9)/TASK_TREE (frontier `.4`)/CHANGELOG/DEV_NOTES +
  book P2 (the `.3` result), P1 and claim-scope (32 guests, 454 steps), annex/assembler
  (`.word`), the routes registry, the dossier (D-FENCE, OQ-2), references.sexp, and both
  regenerated `G?-REPORT.md`.


## SEMILITH-MB-0001 (leaf MODEL-BOOKS.7) — annex: how the tracked assembler works

- Director request: the project book gains `annex/assembler.md`, a teaching chapter on
  `scripts/riscv_asm.py` — why it exists (EVD-05: guest bytes encoded independently of the
  models under test), the table pipeline (pinned `riscv-opcodes` → fragments → the unit's
  composition → words → `guests.rs` / ELF), the three operand classes (fixed bits;
  width-checked contiguous fields; the B/J scramble derived from the pinned descriptors with
  the accounted-bits == field-width self-check), the two-pass label front-end (x0..x31 only,
  no ABI names, no pseudo-ops — deliberate), the ELF writer (the section table exists because
  Spike's loader was measured refusing a sectionless ELF), and the refusal discipline
  (`AsmError` — never a guess; a generator that guesses is a second definition). The shared
  ancestry of the encodings (riscv-opcodes is upstream of Sail and Spike) is stated, with the
  spike-dasm round-trip as the recorded mitigation.
- Out of order: leaf `.7` lands while `.1`–`.6` are pending — the per-unit book sequence is
  unchanged; the annex lives in the project book because the assembler is shared project
  machinery and the per-unit book structure is unbuilt (`.1`). Placement recorded in the tree.
- Verification: `make book` renders the chapter (28 → 29 chapters); the chapter's "Try it"
  snippet was executed, not imagined (`addi x1, x1, -1` → `0xfff08093`, label-resolved `bne`
  → `0xfe009ee3`); `make gate` green.
- Lockstep: MEMORY (MODEL-BOOKS 1/7), LIVE_STATUS (29 chapters, MODEL-BOOKS 1/7),
  CHANGELOG/DEV_NOTES, the tree (frontier `.1` unchanged), and the book itself.

## SEMILITH-PS-0003 (leaf P2-SCALAR.2) — boundary arithmetic and state interactions: the shamt domains exhausted

- Five boundary guests, every expectation value derived from the pinned specification before any model ran (`EVD-05`): `bound-shift` (89 steps — the **6-bit shamt domain exhausted** by one `srli` sweep over all 64 amounts of `0x8000000000000001`; `slli`/`srai` pinned at {0,1,2,4,8,16,32,63}; register-amount corners rs2 = 64 → reads as 0, pre-written to stay visible, and rs2 = -1 → 63), `bound-shiftw` (55 steps — the **5-bit domain exhausted** by one `sraiw` sweep; the rs2 = 96 `srl`/`srlw` pair on identical operands answers 0x00000000FFFFFFFF vs the sign-extended identity, pinning the 6-bit vs 5-bit read), `bound-arith` (31 steps — INT64_MAX + 1 / INT64_MIN - 1 wraps on the register AND immediate paths, *W wraps with a garbage upper half provably ignored, `slt`/`sltu` at the extremes, `auipc 0x80000` wrapping the address sum modulo 2^64 to exactly 4·n), `bound-ext` (47 steps — the sign edges 0x7F/0x80, 0x7FFF/0x8000, 0x7FFFFFFF/0x80000000 as sign/zero PAIRS at one address, the 0x00 byte through a pre-write, store truncation at non-clamping values; 32 census-pinned crossings), `bound-alias` (37 steps — the little-endian lane proof, overlap composition `sd`+`sb`+`sh`+`ld`, register aliasing incl. a load over its own base register, x0 in both directions; 16 crossings).
- The commit gate caught two **authoring** defects, never a model one: the overlap-composition constant was hand-assembled wrong twice (`0x4CD`'s high byte is 0x04; then the AA lane one hex pair over) — each RED was answered by re-deriving from the spec rule, and the corrected value is what the rule computes. Lesson declined for promotion: the gate already fails any expected value the spec rule does not compute — measured twice this leaf.
- Reviewed ceiling expansion (the `.1` decision names this leaf's guest growth as its own decision): `profiles/` 32 → 42 files / ~307 KB; registry ceilings 34 → 46 files and 256 → 384 KiB; per-part 32 KiB unchanged (largest new file 27,848 B).
- Verification: 138 verify suites (+5 guest suites), 65 core suites, clippy `-D warnings`, `make gate` 24 doctrines green, `make smoke-bench` 18 arms (14 clean guests), `EXERCISE-COVERAGE` 52/52 (self-test 7/0). Live: **14 guests, 376/376 aligned steps** against sail-riscv AND spike, byte-identical reproduction.
- Lockstep: MEMORY/LIVE_STATUS (P2 2/9)/TASK_TREE (frontier `.3`)/CHANGELOG/DEV_NOTES + book P2 (the `.2` result), P1 and claim-scope (14 guests, 376 steps), the routes registry, and both regenerated `G?-REPORT.md`.

