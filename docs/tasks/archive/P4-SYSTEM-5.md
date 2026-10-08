# P4-SYSTEM — archived completed-slice evidence (part 5)

Completed `.12` acceptance checklists (a), (a2), (b), moved verbatim from
[`../P4-SYSTEM.md`](../P4-SYSTEM.md) at the d3 promotion crossing (`2026-10-08`).

`P4-SYSTEM.12` slice (a) — the C re-pin and the fragment: 37 forms, their scatter layouts, the declared specializations (`2026-10-06`, `SEMULITH-P4-0079`):

- [x] **REPRODUCE / ISSUE** — at `2c7c454` no C table is on disk or pinned and no fragment exists:

  ```
  $ ls target/refs/riscv-opcodes/ | grep -c _c → 0
  $ git ls-files 'definitions/riscv/c.sexp' → nothing
  $ python3 scripts/check_encoding_disjoint.py definitions/riscv/c.sexp (first draft, before the rule) → rc=1:
    COLLISIONS … c.addi16sp overlaps c.lui, c.ebreak overlaps c.jalr, c.jr overlaps c.mv … REJECTED
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: C's first slice. Two measured facts shaped it:
  the base layout loader accepted only `imm[…]` descriptors (`git show HEAD:scripts/riscv_asm.py`,
  `load_immediate_layout` — the C pieces read `uimm[…]`, `nzimm[…]`, `nzuimm[…]`); and the
  disjointness rule had no notion of an overlap BY DESIGN, which the pinned table itself lists
  (`constants.py` `overlapping_instructions`, six pairs).

- [x] **FIX** — the ledger re-pins `rv_c` (23 rows), `rv64_c` (10), `rv_c_d` (4) by content (the
  RV32-only tables deliberately not pinned); `fetch_references.sh`'s census gains the named C
  exclusion (flips when the scope declares a `c.` form); `load_immediate_layout` takes a field set
  and the C descriptors (the base path byte-identical: all nine fragments regenerate unchanged);
  `gen_fragments.py` emits `definitions/riscv/c.sexp` — 37 forms, 11 register fields, 24
  immediate-piece scatter layouts, and the six upstream overlaps as `(specializes …)` oriented by
  the fixed bits (refused at generation if neither row contains the other); `schema/fragment.sexp`
  gains the construct; the resolver carries it; `check_encoding_disjoint.judge_overlaps` accepts
  exactly the DECLARED strict specializations — one rule, used by UNIT-COMPOSITION too.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/check_encoding_disjoint.py definitions/riscv/c.sexp → composed set: 37 instruction(s);
    declared specializations: 6 (the special row decodes first); no collisions … the fragments COMPOSE
  $ python3 scripts/check_encoding_disjoint.py <rv64i zicsr f d a m c> → composed set: 192 instruction(s) … COMPOSE
  $ python3 scripts/check_encoding_disjoint.py --self-test → 17 pass / 0 fail (5 new: a declared strict
    specialization GREEN; the same overlap undeclared, a reversed declaration, a declaration naming an absent
    row, an overlap the declaration does not name — each RED)
  $ bash scripts/fetch_references.sh --verify-only rv64gc-lab-v0 → MATCH rv_c / rv64_c / rv_c_d; MATCH encoding
    tables vs profile scope 163 == 163 (C excluded by name until the bind); fetch_references: ok
  every C piece layout reconciles with its field width (24 of 24; e.g. c_imm12 (12, 2) [(11,11),(4,4),(9,8),(10,10),(6,6),(7,7),(3,1),(5,5)])
  ```

- [x] **NO REGRESSION** — the nine existing fragments byte-identical (`git status --short definitions` →
  only `c.sexp` new); `make check` rc=0; `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — the ledger, the fetch/census script, the loader, the fragment generator, the
  fragment and its schema, the resolver, the disjointness rule and UNIT-COMPOSITION, `GS-REPORT.md`,
  this tree, `CHANGELOG.md`, `MEMORY.md`, the book (`plan/p4/c.md`, new).
  promotion: declined (the overlap-by-design rule is recorded in its schema construct and its checker; no general lesson)

`P4-SYSTEM.12` slice (a2) — a found defect, owned: JAL's offset sign taken from bit 19 in both engines (`2026-10-06`, `SEMULITH-P4-0080`):

- [x] **REPRODUCE / ISSUE** — found reading `extract()` for slice (b) (C's immediates are scattered
  pieces too), then reproduced on both CLIs with assembler-built ELFs:

  ```
  $ semulith run jal-back-rv64i-lab-v0.elf --profile=rv64i-lab-v0 --steps=2 (rc=1) → trap cause=0x00
    tval=0x000000008007fffe — the specification's target is 0x7ff7fffe (pc - 0x80002)
  $ semulith run jal-fwd-rv64gc-lab-v0.elf --profile=rv64gc-lab-v0 --steps=2 → [1] [M]: 0x000000007ff80000
    — the specification's target is 0x80080000 (pc + 0x80000)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — both extractors push a scattered field at its FIELD width:
  `git show HEAD:crates/semulith-core/src/exec.rs` (`let width = u32::from(f.hi - f.lo + 1)` in the
  generic arm) and `exec_rv64gc.rs` `extract()` (the same). `jimm20` is 20 bits wide but carries
  imm[20:1], so `(sext 64 (imm jimm20))` extended from bit 19. `exec.rs`'s own module doc states the
  intended algebra — "an `Imm` carries its composed field width (12/13/21/20 for
  imm12/bimm12/jimm20/imm20)" — and `bimm12` was special-cased to 13; `jimm20` never was. No corpus
  program jumps ±512 KiB.

- [x] **FIX** — a scattered field carries the width of the immediate it composes (its highest piece
  bit + 1) in both extractors; `jal_offsets_at_the_sign_boundary_reach_their_targets` in both engines'
  tests (the words from the tracked assembler: a below-boundary control, +2^19, −2^19 − 4, and both
  extremes); the rv64i release decision amended (the released evidence unaffected by construction).

- [x] **ADDRESSED (verified)** —

  ```
  before the fix: cargo test -p semulith-core jal_offsets → test result: FAILED. "jal 0x80000 … left:
    18446744073709031424, right: 528384"; cargo test -p semulith-verify jal_offsets → test result: FAILED.
  after: both → test result: ok. 1 passed
  $ cargo test -p semulith-verify run → test result: ok. 76 passed (both corpora: no guest's observations moved)
  ```

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — both engines and their tests, the rv64i release decision (amendment), this tree
  (the execution decision recorded), `DEV_NOTES.md`, `CHANGELOG.md`, `MEMORY.md`, the book
  (`plan/p4/c.md`).
  promotion: declined (the boundary test is the durable record; the class — small corpus programs never reach an immediate's sign boundary — is mechanized for C at slice (b), whose expansion vectors cover every immediate's extremes)

`P4-SYSTEM.12` slice (b) — the language for C; interrupted session recovered (`2026-10-07`, `SEMULITH-P4-0081`):

- [x] **REPRODUCE / ISSUE** — the crash left five uncommitted files at `f877726` (recorded
  above). The committed language cannot express C's expansion declarations:

  ```
  $ git show f877726:schema/semantics.sexp > target/p4-system-12/semantics-before-recovery.sexp
  $ python3 scripts/check_sexp_schema.py definitions/riscv/c.sem.sexp target/p4-system-12/semantics-before-recovery.sexp
    REFUSED c.sem.sexp: construct "semantics": undeclared field "expand" (rc=1)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `git diff -- scripts/gen_definition.py` showed the surviving
  loader returning expansions while `load_inputs()` dropped them and `emit()` still emitted
  only ordinary rules in name order. C's six overlaps need specificity order. The live diagnostic
  found a second reader to extend: `bash scripts/check_semantics_corpus.sh` →
  `CITATIONS: REFUSED: c.sem.sexp: declares no (sem …) form`; `check_citations.citations()` iterated
  only `sem`. The first expansion probe also falsely treated C.ADDIW's zero immediate as reserved
  (its restriction is rd=x0); the probe was corrected from §27.1.5.2, before trusting it.

- [x] **FIX** — `schema/semantics.sexp` declares `expand`, `operand`, and the optional reserved
  predicate. `c.sem.sexp` supplies 37 cited declarations: 36 named base expansions and C.JALR's
  own pc+2 rule. M's five existing literal quotations use single quotes so CITATION-QUOTES judges
  them too (their meaning unchanged). `check_semantics.py` checks raw-field mappings, unique
  bindings, exactly the base rule's operand reads, the quoted expansion sentence, and the
  own-rule alternative; the generator re-judges those rules, lowers the base effect with its
  mappings and reserved predicate, emits instruction length, and sorts by fixed-bit specificity.
  C metadata emits only when C is composed, so the real unit stays unbound. The long C.J scatter
  array exposed the emitter's inline-array assumption under `rustfmt --check`; it now wraps at
  the already-used 80-character threshold. The citation reader checks `expand` as well as `sem`.

- [x] **ADDRESSED (verified)** — the permanent diagnostic is `scripts/probe_c_expansions.py`,
  run by DEF-GEN on a disposable full composition with C; its expected names, mappings and
  immediate limits are hand-written from §27.1.3–§27.1.5, not derived from the semantics file.

  ```
  $ python3 scripts/check_semantics.py definitions/riscv/c.sexp definitions/riscv/c.sem.sexp → 37 of 37
  $ python3 scripts/check_semantics.py --self-test → 46 pass / 0 fail
  $ bash scripts/check_definition_gen.sh --self-test → C expansion probe: 37 forms, 104 spec-side
    checks; compiled decoder 8/8; DEF-GEN --self-test: 51 pass / 0 fail
  RED controls: compact register offset +9 generates but fails (rd=16, expected 15); reversed
    table ordering fails the compiled specialization_decode test; an unbound base operand is refused.
  Compiled mappings also check the immediate extremes, copied base effects, C.JALR's own rule,
    7 reserved code points and 6 HINT examples; the disposable output is rustfmt-stable.
  $ python3 scripts/check_citation_quotes.py → 120 attributed quotes, 0 findings
    c.sem.sexp + m.sem.sexp alone: 51 attributed, 0 findings, 0 unattributed
  $ bash scripts/check_semantics_corpus.sh → SEMANTICS: ok (14 checks)
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (the complete workspace). `git diff` over both
  generated definition modules shows only generator/input fingerprints and M's quotation
  spelling: existing executable tables and effects unchanged. DEF-GEN's 51 controls and the
  semantics/citation corpus stay green; citation controls 15/15 and `make book` rc=0 (all books).
  `make gate` → `=== all doctrines green ===`; `bash scripts/check_no_background_jobs.sh`
  → `handoff: OK` before committing. The commit hook re-runs the gates on the staged checkpoint.
  C execution and fetch evidence belong to slices (c)–(f),
  so these finite declaration checks make no CPU-conformance claim.

- [x] **LOCKSTEP** — this tree (crash-recovery instruction, checklist, frontier, logs), the
  task index, MEMORY, LIVE_STATUS (11/18 unchanged; C's language ready), CHANGELOG, DEV_NOTES,
  the doctrine/toolbox descriptions and the book (its derived index regenerated after BOOK-INDEX
  named the new PC mention as drift). The status note was shortened when `check_readme_routes.sh`
  measured 6,160 B over its 6,144 B ceiling; 6,138 B after, the ceiling unchanged.
  The recovered work is committed, with (c)
  as the next action; handoff requires a clean tree and no project-owned background job.
  promotion: declined (the slice's findings are local reader/emitter adaptations; the permanent
  probe and its RED controls retain the evidence)

<!-- d3b crossing: c1/c2 appended verbatim -->

`P4-SYSTEM.12` slice (c1) — exact parcel boundary (`2026-10-08`, `SEMULITH-P4-0082`):

- [x] **REPRODUCE / ISSUE** — `cargo test -p semulith-verify parcel_fetch` exercises a
  two-byte region containing 0x0085: the existing word fetch returns `AccessFault`;
  no word response can represent the successful sixteen-bit read this instruction needs.
- [x] **ROOT CAUSE (WHY + WHERE)** — `rg -n 'Request::Fetch|fetch16'
  crates/semulith-core/src/env.rs crates/semulith-core/src/exec_rv64gc.rs` pins the mismatch:
  Fetch is fixed at 32 bits, and the helper called fetch16 sends that request before masking
  its answer. `fixtures.rs` correctly requires all four bytes inside the region.
- [x] **FIX** — additive `FetchParcel { addr }` / `FetchParcel(u16)` boundary types;
  the fixture reads exactly two bytes, aligns to two, and retains immediate code visibility.
  Fetch counters and the comparison filter recognize both implicit-read variants;
  fault-injection spans use two bytes for a parcel. Test providers answer the new kind.
  Production decode/fetch remains unchanged until (c2) and the bind.
- [x] **ADDRESSED (verified)** — `make check` rc=0; the two-byte region now supplies
  0x0085 through a parcel request (one successful fetch), while the word request still faults.
  Odd and outside-region parcel addresses fail with their proper target errors. A store to
  the final halfword is visible on its next parcel fetch. The injection control refuses a
  word crossing 0x1002 but accepts the parcel at 0x1000 and refuses the parcel at 0x1002.
- [x] **NO REGRESSION** — `make check` rc=0: fmt, strict clippy, 150 core, 17 DSP,
  193 verify tests; both existing corpora remain green. The pre-commit doctrine gate is
  required for this checkpoint, and `make book` checks all books. These boundary tests
  are finite evidence; C's execution and matched-reference evidence remain (c2)–(f).
- [x] **LOCKSTEP** — the tree, index, MEMORY, LIVE_STATUS, CHANGELOG, DEV_NOTES and C
  chapter updated. The closed `.11` checklists moved byte-verbatim (reconstruction asserted)
  into archive part 4 to leave room below the unchanged per-part ceiling.
  promotion: declined (the typed boundary and its extent tests retain this local finding).

`P4-SYSTEM.12` slice (c2) — the engine, proven before C binds (`2026-10-08`, `SEMULITH-P4-0083`):

- [x] **REPRODUCE / ISSUE** — `python3 scripts/probe_c_engine.py --engine-revision b71bc1b`
  → 0 passed / 15 failed (compiled successfully). On a temporary C composition the old
  evaluator reads missing base operands, advances pc by four, reads a whole word for a
  parcel and walks the next page before it knows the length; the failures name those cases.
- [x] **ROOT CAUSE (WHY + WHERE)** — the baseline probe's panics name
  `exec_rv64gc.rs:331` (missing rd/rs1); its compressed-last-parcel test observes pc=0,
  x1=0 instead of 0x5000/1. `rg -n 'wrapping_add\(4\)|operands: extract|fetch16'
  crates/semulith-core/src/exec_rv64gc.rs` pins the hard-coded length, unmapped fields and
  over-wide request. Generation had emitted C bindings, but no evaluator consumed them.
- [x] **FIX** — rv64gc tables always carry length and optional expansion metadata (4/None
  while unbound). The C-enabled table reads exact parcels in order; only a 32-bit encoding
  requests the second. It maps all operands against the original fields before replacing
  them, retains value widths, judges reserved predicates before effects, advances pc by the
  declared length, and exposes the instruction's own bit width through `inst`. Legacy fetch
  remains for the unbound table; rv64i changes only its generator fingerprint.
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_c_engine.py` → 15 passed / 0 failed.
  Hand-written instruction words and request schedules check signed immediates and jumps at
  their extremes, unsigned load offsets, overlapping operands, hints, reserved parcels,
  breakpoint specificity, FP gating/dirty state, 16/32-bit intermixing, 2-mod-4 targets,
  address wrap and malformed-environment classification. At a last halfword, C never walks
  the next page; a word's second-parcel page fault yields cause 12 / tval=pc+2 / epc=pc,
  and its access-fault pair yields cause 1 with the same address discipline. No fault retires.
- [x] **NO REGRESSION** — `make check` rc=0 (150 core / 17 DSP / 193 verify tests, strict
  clippy and fmt). `bash scripts/check_definition_gen.sh --self-test` → 54/54: the new
  compiled-engine GREEN and both RED mutations execute (erased mapped widths fail the
  signed-immediate test; word-for-parcel fetch fails the mixed-length/region-end test).
  The permanent probe runs within DEF-GEN on every commit. `git diff` on rv64i's generated
  module shows only the generator hash changed. C remains unbound in production until (e);
  the full corpus and matched Sail evidence remain (d)–(f), never claimed by these probes.
- [x] **LOCKSTEP** — the tree/frontier/logs, MEMORY, LIVE_STATUS (11/18 unchanged), task
  index, CHANGELOG, DEV_NOTES, toolbox/doctrine descriptions, and C chapter. Two stale
  FP open-question rows corrected from `.7`'s committed result. All books must build and
  the commit doctrine gate must pass. `check_derived_counts.sh --list` re-derives 493 arms.
  promotion: declined (the permanent engine probe and its RED controls retain the lesson).


`P4-SYSTEM.12` slice (d1) — assemble parcels without padding (`2026-10-08`, `SEMULITH-P4-0084`):

- [x] **REPRODUCE / ISSUE** — `python3 scripts/probe_c_assembler.py --assembler-revision
  e1fe379` exits 1: c.add's rd_rs1_n0 is unsupported. The legacy assembler only returns
  words and advances labels by four, so it cannot represent a mixed 16/32-bit program.
- [x] **ROOT CAUSE (WHY + WHERE)** — `git show e1fe379:scripts/riscv_asm.py` and
  `rg -n 'pc \+= 4|CONTIGUOUS_OPERANDS|def assemble' scripts/riscv_asm.py` identify the
  former hard-coded field vocabulary and word stride. Compressed immediates span several
  declared fields; compact register indices and mapped FP register files need interpretation.
  README's old implementation disclaimer predates the interpreter (`git blame -L 10,15
  README.md`, planning import 724e422) and contradicts the experimental implementation.
- [x] **FIX** — group declared immediate pieces, derive their width/signedness/alignment,
  derive FP spelling from expansion mappings, and encode compact architectural registers.
  Judge reserved predicates and more-specific encodings instead of silently changing the
  requested mnemonic. Sized units retain length, byte pc and text; `.half` emits two bytes,
  `.word` four, labels use byte offsets, and assemble_image never pads. The legacy word API
  explicitly refuses short units. Correct README's claim scope to experimental implementations.
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_c_assembler.py` passes 37 independent
  hand-encoded words (every selected form), 21 operand refusals, hints, raw-half refusals,
  mixed labels and the exact byte image. `--mutation compact-base`, `label-stride` and
  `padding` each exit 1 at their behavioral assertion. The prior assembler is RED.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh --self-test` passes 20/20;
  `bash scripts/check_definition_gen.sh --self-test` passes 54/54 (including the C engine).
  Both `scripts/gen_guests.py --check` invocations (rv64i and rv64gc) are byte-identical;
  `cargo test -p semulith-verify run` passes 77/77. The permanent assembler controls execute
  within GUEST-GEN on every commit. C remains unbound; guest image/runner integration is d2.
- [x] **LOCKSTEP** — tree/frontier/logs, MEMORY, LIVE_STATUS (11/18 unchanged, 497 arms),
  task index, CHANGELOG, DEV_NOTES, README, definition toolbox/doctrine and the assembler/C
  book chapters (including the stale RV64I/500-line description). Books and commit doctrine
  gate must pass. Lossless DEV_NOTES sharding
  preserves whole entries and digests without raising a ceiling.
  promotion: declined (the permanent fixture and RED controls preserve this local lesson).

`P4-SYSTEM.12` slice (d2) — exact guest images reach the runner (`2026-10-08`, `SEMULITH-P4-0085`):

- [x] **REPRODUCE / ISSUE** — `python3 scripts/probe_c_guest_image.py --generator-revision
  89a8e6d` exits 1: mixed.s does not assemble because the generator uses the refusing word
  API. `rg -n 'guest.words|to_le_bytes' crates/semulith-verify/src/run_rv64gc.rs` on the
  parent identifies the runner's four-byte reconstruction, unable to carry short units.
- [x] **ROOT CAUSE (WHY + WHERE)** — `git show 89a8e6d:scripts/gen_guests.py` pins
  load_guest's word list and emit's u32 arrays; `git show 89a8e6d:crates/semulith-verify/src/run_rv64gc.rs` pins reconstruction at lines 119–123. Length was absent from the fixture.
  The generator's rv64gc header and drift refusal also gave the default scalar regeneration
  command; the mode-specific command now names the canonical inputs, byte mode and output.
- [x] **FIX** — assemble sized units at the declared entry, emit exact u8 images with
  --image-format bytes, and load them directly in rv64gc. Word mode still emits rv64i's
  old API and explicitly refuses short units. The generated header carries the canonical
  mode-specific command independent of a temporary check output. Fetch docs count actual
  boundary requests (faulted included; delivery/walk/wait can prevent them).
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_c_guest_image.py` →
  `test result: ok. 2 passed; 0 failed` with the tracked runner and a temporary C composition. A hand-encoded
  14-byte image checks a word at 2-mod-4, signed results, a byte-addressed jump over an
  illegal parcel, the final halfword, exact loaded bytes and six requests across five steps.
  A word-only image reads two parcels. Padding and runner-offset mutations fail; word mode
  refuses the short guest. The prior generator is RED before any engine runs.
- [x] **NO REGRESSION** — `make check` passes fmt, strict clippy, 150 core / 17 DSP /
  193 verify tests. `bash scripts/check_guest_gen.sh --self-test` passes 23/23, including
  the new GREEN and both behavioral RED controls. The before/after load_guest census
  compares 139 rv64gc + 49 rv64i image hashes/byte counts and every expectation: all unchanged.
  `git diff -- crates/semulith-verify/src/guests.rs` is only its generator fingerprint.
  C remains unbound in production; the existing fetch expectations remain unchanged until e.
- [x] **LOCKSTEP** — tree/frontier/logs, MEMORY, LIVE_STATUS (11/18 unchanged, 500 arms),
  task index, CHANGELOG, DEV_NOTES, definition toolbox/doctrine, assembler/C book chapters.
  Books and commit doctrine gate must pass; check_derived_counts.sh re-derives 500 arms.
  promotion: declined (the permanent runner probe and its mutations preserve this lesson).


`P4-SYSTEM.12` slice (d3a) — the tracked spec-side author (`2026-10-08`, `SEMULITH-P4-0086`):

- [x] **REPRODUCE / ISSUE** — `rg --files scripts` found no tracked GC author; the producer
  lived at target/p4-system-11/tools/derive_expectations.py (sha256
  71269627672a608885b67ede326b57f779f58a7eeee219b3b983ac26982fea53). The 139-guest census
  found 42 exact records, 49 different outputs and 48 refusals. execute accepted reserved
  0x04000033 / 0x04001013 / 0x04004033 as sub/slli/xor. Its permission audit mismatched
  sv39-perm-usr at step 120 (SUM=1 rejected) and later MXR (178 vs 169 steps).
- [x] **ROOT CAUSE (WHY + WHERE)** — `rg -n 'ROOT|sys.path|funct7|self.mode == S|not r'
  target/p4-system-11/tools/derive_expectations.py` pins scratch-relative imports, OP's
  unconstrained funct7, shifts' missing upper-bit check, and data walk's absent SUM/MXR/U
  permission rules. The pinned supervisor.html lines 650–670/2478–2490 require SUM data
  access, prohibit S instruction fetch from U pages, and permit X-only reads with MXR.
  dir-runoff and sv39-straddle's differences trace to source-end stopping and absent fetch
  translation; d3d owns those explicit scope gaps, not a claim of full legacy author coverage.
- [x] **FIX** — tracked derive_rv64gc_expectations.py, repository-derived paths, --check and
  --check-owned, all derivations computed before any write. The measured 42-record owned
  corpus is explicit. Narrow OP/shift/misc-mem guards refuse reserved/unsupported shapes;
  missing stock rules produce named Refusal instead of KeyError. SUM/MXR/U permission
  rules repaired from the pinned chapter. No expectation record overwritten or fitted.
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_gc_author.py` rc=0 → 42 guest(s)
  byte-identical; 7 reserved words refuse without effects; named LBU vocabulary refusal;
  SUM data/fetch, U-bit and MXR direct PTE fixtures passed. All six mutations are RED:
  OP guard, shift guard, signed division rounding, SUM, MXR and U-bit. Before the small
  permission repair, all 91 legacy texts matched the original producer; afterwards 90 stay
  exact and repaired sv39-perm-usr matches all 169 committed step/write observations.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh --self-test` → 30 pass / 0 fail;
  both generated fixtures still match and base-mirror checks hold. The probe and six RED
  controls run on every commit. The 42 owned records stay byte-identical, and no tracked
  guest/expectation or production engine changed. Broader legacy fetch/budget authoring
  remains d3d; C expansions d3c. The Sail absence defect remains owned by immediate d3b.
- [x] **LOCKSTEP** — tree/frontier/logs, MEMORY, LIVE_STATUS (11/18 unchanged, 507 arms),
  task index, CHANGELOG, DEV_NOTES, toolbox/doctrine, assembler/C book chapters. Completed
  .12 a/a2/b checklists archived verbatim to part 5 with identity reconstruction asserted.
  Books and commit doctrine gate must pass; check_derived_counts.sh re-derives 507 arms.
  promotion: declined (the tracked producer, owned corpus and mutation probes retain this
  bounded authoring lesson; the Sail absence repair is scheduled before its next use).

`P4-SYSTEM.12` slice (d3b) — Sail requires evidence of every declared step (`2026-10-08`, `SEMULITH-P4-0087`):

- [x] **REPRODUCE / ISSUE** — `target/p4-system-12/d3-sail-gap.log` records the scratch
  comparator returning AGREE for a failed process, empty trace and one ordinary no-write
  expectation. The mock process reports rc=1; the result claims 1 steps exact. The producer
  and builder lived only in target/p4-system-11/sail and depended on fixed clang/zig paths.
- [x] **ROOT CAUSE (WHY + WHERE)** — `sed -n '64,86p'
  target/p4-system-11/sail/compare_sail.py` pins missing-row acceptance whenever wanted
  writes are empty; `rg -n 'proc|returncode|words|CLANG'` over its comparator/builder shows
  unjudged process status and word-only materialization. Existing delivery gaps were
  generalized to arbitrary absence, admitting false agreement. Prior process statuses
  were not retained; cached-trace audit can establish row evidence, not recover those statuses.
- [x] **FIX** — tracked run_rv64gc_sail.py: exact byte ELF through the assembler/writer's
  public API, dossier binary digest check, matched override materialized by its existing
  owner, successful process required, stale own trace removed before launch, two runs and
  byte-identical reproduction. Every ordinary expected row required. A declared interrupt
  or fetch-delivery gap also needs the matching numbered public trace event. Malformed,
  duplicate, unknown and orphan records refuse. Verdict covers declared GPR changes only.
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_gc_sail.py` rc=0: ordinary empty-write
  rows, witnessed interrupt/fetch gaps, wrong cause, absent events, failed status, malformed/
  duplicate/orphan records, x0/index legality, empty budget, write divergence and stale-output
  controls. All four mutations are RED (missing-row acceptance, ignored status, unwitnessed
  gap and stale trace reuse). Live `run_rv64gc_sail.py m-mul m-div m-word m-alias` rc=0 →
  4 AGREE of 4 (99 steps), two exact traces each. A temporary C composition's 14-byte image
  agrees on five independently derived writes, addresses and words, two exact traces.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh --self-test` → 35 pass / 0 fail.
  Strict cached audit: 79/79 AGREE-claimed trace cells pass the new adapter; no ordinary
  row missing. Nine interrupt deliveries and one fetch-page fault instead carry matching
  events. 95 total cached corpus traces inspected; sixteen dossier-declared not-matches
  retain their limitations. Audit outputs in target/p4-system-12/d3b; live M checks current
  status/digest/config plus observations. No source record, pin or production engine changed.
- [x] **LOCKSTEP** — tree/frontier/logs, MEMORY, LIVE_STATUS (11/18 unchanged, 512 arms),
  task index, CHANGELOG, DEV_NOTES, definition toolbox/doctrine, assembler/C book chapters.
  Completed .12 c1/c2 checklists appended byte-verbatim to part 5 with reconstruction asserted.
  Books and commit doctrine gate must pass; check_derived_counts.sh re-derives 512 arms.
  promotion: declined (the permanent adapter/probe and four mutations retain this scoped
  absence lesson; the comparison policy's wider landing remains .14).


`P4-SYSTEM.12` slice (d3c) — independent C component expectations (`2026-10-08`, `SEMULITH-P4-0088`):

- [x] **REPRODUCE / ISSUE** — d3c/before.log records execute_c absent and 6 named refusals:
  C.LI 0x5081 plus SRAI, ADDIW, ADDW/SUBW and JALR base shapes. The older word-only
  producer cannot derive compressed observations; execute's sequential advances assume 4.
- [x] **ROOT CAUSE (WHY + WHERE)** — `rg -n 'pc \+ 4|def execute|OP-IMM|1101111'
  scripts/derive_rv64gc_expectations.py` on parent 75c79af locates the 4-byte next/link
  values and missing base forms. Pinned c-st-ext.html 1327–1346 gives C.JALR pc+2;
  rv64.html 542–545 gives ADDIW at 3.1.2.1 (the unused stock locator was wrong).
  XML extraction of the three pinned diagrams exposes the scattered field positions;
  hashes and public linked names above. No generated expansion table supplies answers.
- [x] **FIX** — scripts/spec_c.py hand-decodes 37 RV64+D forms and reserved conditions
  from the pinned chapter. The author executes these independently reconstructed base
  words at length 2; C.JALR target uses old rs1 and links pc+2. Reserved parcels and
  FS-Off faults carry original 16-bit tval. Missing base forms gain narrow fixed-bit
  guards; word suffixes truncate then sign-extend; ADDIW locator repaired. The old guest
  author route remains word-only until d3d. No production profile or engine changed.
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_c_author.py` rc=0 → 37 expansion/
  effect fixtures, 22 limits, 79 one-hot scattered bits, 11 reserved parcels, 10 hints,
  two branch outcomes, aliasing links, integer/memory/FP state, four FS-Off original
  parcels, a misaligned load and word overflow/zero-immediate cases all pass. All 6
  mutations are RED (compact base, sign, length/link, reserved guard, bit permutation,
  expanded trap bits). Parent 75c79af is RED: execute_c absent. One-hot controls
  distinguish bit permutations that an all-ones limit alone cannot detect.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh --self-test` → 42 pass / 0 fail;
  `--check-owned` → 42 documents byte-identical. Full legacy before/after census:
  91/91 previously emitted texts exact; 6 new outputs from JALR vocabulary, all common
  numeric writes agree. Three need the already-owned fetch/end repair (named above).
  No historical record overwritten. The normal guest generator remains unchanged.
- [x] **LOCKSTEP** — tree/frontier/logs, MEMORY, LIVE_STATUS (11/18 unchanged, 519 arms),
  task index, CHANGELOG, DEV_NOTES, definition toolbox/doctrine and C/assembler book.
  Completed d1/d2 receipts archived byte-verbatim to part 5 (reconstruction asserted);
  no ceiling raised. Books and doctrine commit gate must pass. check_derived_counts.sh
  re-derives 519 arms. promotion: declined (the independent decoder, permanent probe and
  six discriminating mutations retain this component's local lesson).

`P4-SYSTEM.12` slice (d3d0) — retain every ILEN diagnostic bit (`2026-10-08`, `SEMULITH-P4-0089`):

- [x] **REPRODUCE / ISSUE** — new permanent C engine probes on b48201c: rc=1,
  15 passed / 3 failed. An all-ones 32-bit image returns ReservedDecode word 65535,
  expected 4294967295. With only the first 0xffff parcel accessible, it returns that
  reserved word instead of the expected access fault on pc+2. An unmapped second virtual
  page is also never walked. Logs: target/p4-system-12/d3d1/ilen-parent.log.
- [x] **ROOT CAUSE (WHY + WHERE)** — `git show b48201c:crates/semulith-core/src/exec_rv64gc.rs`
  locates fetch_instruction's `lo & 0x1f == 0x1f` early
  return refuses a wider prefix from its first parcel. The pinned intro.html 1148–1153
  defines all ones as ILEN bits long; machine.html 3427–3450 requires a nonzero illegal
  diagnostic to carry min(actual length, ILEN, MXLEN). This profile's ILEN is 32.
  The returned ReservedDecode word feeds the runner's nonzero illegal tval policy.
- [x] **FIX** — only a true compressed prefix can return after 2 bytes; every wider
  prefix fetches the remaining ILEN parcel before reserved decode. No third parcel
  is requested. Missing/denied upper parcels retain their access/page fault, pc+2
  tval and starting EPC. The production C slot remains unbound.
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_c_engine.py` rc=0 → 18 passed /
  0 failed: full all-ones/other unsupported-prefix diagnostics, upper-parcel access
  refusal, and translated second-page fault join the prior 15 controls. Parent b48201c
  and the new short-ilen mutation are RED on all 3 new cases; every RED is a behavioral
  failure, not a compilation failure. DEF-GEN registers that mutation permanently.
  Sharder header controls: old producer 10 pass / 2 fail, corrected producer 12 pass /
  0 fail; the new header states its bound accurately even below that ceiling.
- [x] **NO REGRESSION** — `make check` rc=0 (150 core, 17 DSP, 193 verify tests, fmt and
  strict clippy); `check_definition_gen.sh --self-test` → 55 pass / 0 fail. Existing
  production guest images/records unchanged; this repaired path uses a temporary C
  composition. The old erased-width and word-parcel mutations still discriminate.
- [x] **LOCKSTEP** — tree/frontier/logs, MEMORY, LIVE_STATUS (11/18 unchanged, 520 arms),
  task index, CHANGELOG, DEV_NOTES, definition doctrine/toolbox and C chapter. Completed
  d3a/d3b receipts archived byte-verbatim with reconstruction asserted. DEV_NOTES sharded
  by its governed whole-entry tool with exact reconstruction and freeze manifest updated;
  no ceiling raised. Books and commit doctrine gate must pass. promotion: declined
  (the permanent engine probes and short-ILEN control retain this local fetch lesson).


`P4-SYSTEM.12` slice (d3d1) — independent translated parcel fetch (`2026-10-08`, `SEMULITH-P4-0090`):

- [x] **REPRODUCE / ISSUE** — pure Hart fixtures reproduce four walker defects on
  f8f213c: inconsistent sign extension translates, PTE bit 63 translates, bottom pointer
  refuses, and MPRV+MPP=S data bypasses translation. The new odd-PC fetch fixture also
  catches mepc=0x80000001 instead of 0x80000000. Permanent parent probe rc=1 (canonical
  guard); five defects and their immediate ownership recorded above before each repair.
- [x] **ROOT CAUSE (WHY + WHERE)** — `git show f8f213c:scripts/derive_rv64gc_expectations.py`
  locates walk's upper-only sign check, absent PTE reserved guards, unconditional M bypass
  and pointer-loop Refusal; `rg -n 'mepc.*self.pc|sepc.*self.pc'` finds four unmasked delivery
  assignments. Pinned supervisor.html 2660, 2695, 2930, 2986–2996 defines non-leaf/high-bit/
  canonical rules; machine.html 1372–1380/1425 defines effective MPRV data privilege.
  machine.html 2951 and supervisor.html 1131 require EPC bit zero always clear.
- [x] **FIX** — Hart.fetch_instruction walks each required two-byte parcel before its
  memory request, records actual attempts, delivers start EPC/failing-parcel VA, and
  retains all ILEN=32 bits for wider prefixes. Compressed neighbors untouched, unwritten
  region bytes zero, no time/retire tick. Walk repairs sign, reserved high/non-leaf bits,
  bottom pointer and effective MPRV/SUM/U; M/S exception/interrupt EPC clears bit zero.
  Guest execution remains explicitly the historical word route until d3d2.
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_gc_fetch.py` rc=0: both canonical
  signs; all ten reserved high bits × four kinds; RSW/G; non-leaf U/A/D, bottom chains;
  effective MPRV/SUM/U; region/page-end parcels; wider ILEN prefixes; physical/walk refusals;
  exact logs, fault VA/start EPC, M/S/interrupt alignment and Svade no-write controls pass.
  All 9 mutations are behavioral RED with named assertions; parent f8f213c is RED.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh --self-test` → 52 pass / 0 fail;
  all 42 owned records exact. Complete legacy census: 97/97 prior emitted texts exact,
  42 refusals unchanged, no new/changed outputs or historical record writes. Prior author
  SUM/MXR/U mutations still discriminate after the effective-privilege seam update.
- [x] **LOCKSTEP** — tree/frontier/logs, MEMORY, LIVE_STATUS (11/18 unchanged, 530 arms),
  task index, CHANGELOG, DEV_NOTES, definition toolbox/doctrine, C and assembler book.
  Completed d3c/d3d0 receipts archived byte-verbatim to part 5 (reconstruction asserted);
  no ceiling raised. Books/commit doctrine gate must pass; derived counts enumerate 530.
  promotion: declined (permanent fetch/PTE fixtures and nine mutations retain this lesson).

