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

