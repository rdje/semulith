# P4-SYSTEM — archived completed-leaf evidence (part 2)

The continuation of [`P4-SYSTEM.md`](P4-SYSTEM.md) (part 1), which reached 130,981 B
of the 131,072 B per-part ceiling on `2026-10-04`: every archive move from
`P4-SYSTEM.4` slice (b) onward lands here — the ceiling was obeyed, not raised, per
the `docs/tasks/` precedent (the `P2-SCALAR` checklists/designs split). The live
tree keeps the frontier, the decisions, the open questions, the blockers, every
leaf's goal/acceptance/result narrative, the ACTIVE slice's checklist, and both
logs.

Archived sections, verbatim:

`P4-SYSTEM.4` slice (b) — a.sem.sexp + the new operators through the schema/check/generator path (`2026-10-04`, `SEMULITH-P4-0024`):

- [x] **REPRODUCE / ISSUE** — the brief's pre-conditions 4–6 re-measured, then the
  language census:

  ```
  $ grep -c '^(operator' schema/semantics.sexp
  40                        # the language had no atomic operator
  $ sed -n '71,72p' schema/semantics.sexp
  (operator (name load) (fixed 3)) / (operator (name store) (fixed 3))   # exactly the two memory operators
  $ ls definitions/riscv/a.sem.sexp; grep -c 'LoadReserved\|Amo' scripts/gen_definition.py
  No such file / 0        # slice (a)'s fragment had no semantics; the generator knew no A operator
  $ grep -c 'Sem::TlbInvalidate' crates/semulith-core/src/exec_rv64gc.rs; sed -n '539,548p' <same>
  the Sem match's LAST arm is TlbInvalidate with NO wildcard — the match is EXHAUSTIVE:
  a variant added to the tracked module does not compile until slice (c)'s arms
  # the normative sentences, located in the pinned chapters (re-measured):
  "AMOs never raise load page-fault exceptions" ×1 (RVP-SUPERVISOR);
  "store, store-conditional, and AMO instructions generate store/AMO exceptions" ×1 (RVP-MACHINE);
  "load and load-reserved instructions generate load exceptions" ×1 (same table);
  "Regardless of success or failure, executing an SC.W instruction invalidates any
  reservation held by this hart" ×1 (RVI-A §12.1.2);
  "Portable software should only assume the failure code will be non-zero" ×1;
  "at most 16 instructions placed sequentially" ×1 (§12.1.3);
  "as viewed by other RISC-V harts" ×1 (§12.1.1); § anchors 12.1.1–12.1.4 / 17.1.x resolve
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in existing behavior: the slice executes
  decisions 1–6, and execution settled two design points the brief left open, each
  tool-backed:

  ```
  $ python3 -  # check_pair on a draft sem spelling the AMO operation as a bare symbol
  a-badsym.sem.sexp [amoadd.w]: 'add' is not an operand this instruction has (it provides
  ['aq', 'rd', 'rl', 'rs1', 'rs2']) nor an implicit value        rc=1
  $ python3 scripts/gen_definition.py --check   # before the hash-only regeneration
  DRIFT — the ONLY diff lines are the OWN-03 generator pin (sha256), both modules
  ```

  1. **The AMO's operation cannot ride as a bare symbol** — the checker's walk treats
     every bare-symbol argument as an operand reference (the measurement above), so
     `(amo add …)` is refused as a phantom operand. The op is the funct5 ENCODING as
     `(lit N)` — the value the instruction's own fixed bits carry — which lets the
     generator RE-DERIVE the closed nine from the composed encodings
     (`amo_operations`: every amo*.w/.d row's bits 31..27) and refuse anything outside
     it by name. A constant that is a function of the pinned tables is derived, never
     typed.
  2. **The variants cannot land on the tracked module this slice** — the evaluator's
     exhaustive match (the first measurement) is the .2 slice-d wall: emitting the A
     variants unconditionally breaks compilation until slice (c)'s arms. WHERE:
     `gen_definition.emit` — the variants emit exactly when the unit's own fragment
     list composes `riscv/a`, and an A operator where it does not is a refusal, named
     (the second guard), beside the rv64i guard.

- [x] **FIX** — `schema/semantics.sexp` (40→43 forms: the RESERVATION contract block —
  §12.1.2/§12.1.3 cited, decisions 2–4 and 6 stated; `load-reserved`,
  `store-conditional`, `amo` with their full contracts: the deterministic never-spurious
  SC policy as decision-3 data, the AMO's one store/AMO-rules translation with the
  load-then-store boundary pair and the Request::Atomic rejection recorded, cause 7 for
  misaligned atomics); `definitions/riscv/a.sem.sexp` (NEW, hand-written — all 22
  forms, every rule locator-cited, the shared policies stated once at the operators);
  `scripts/gen_definition.py` (A_TERNARY + the amo special case + the derived closed
  set + the conditional variant emission + both guards; the doc's refusal list
  extended); the self-test arms (below). No Rust edited — the tracked modules
  regenerate HASH-ONLY (the OWN-03 generator fingerprint, the .2 slice-d precedent);
  the evaluator arms are slice (c)'s.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/check_semantics.py definitions/riscv/a.sexp definitions/riscv/a.sem.sexp
  22 of 22 declared instruction(s) have checked semantics
  $ python3 scripts/check_semantics.py --compose rv64i a   /   --compose rv64i zicsr zicntr system a
  the semantics compose — every override is declared (×2; zicsr's ecall/ebreak points reported)
  $ bash scripts/check_semantics_corpus.sh
  SEMANTICS: ok (8 check(s) — pairs, refinement rule, citations)
  $ python3 scripts/check_citations.py --corpus
  a.sem.sexp against rv64gc-lab-v0 (materials cache, offline): ok RVI-A §12.1.2 ×4 / §12.1.4 ×18
  corpus: 5 sem file(s), 7 resolution(s)
  $ python3 scripts/gen_definition.py --encoding target/p4-system-4/…/encoding.sexp …   # scratch, untracked
  gen_definition: wrote target/p4-system-4/definition_rv64gc.rs (78752 bytes)
  $ rustc --edition 2021 --crate-type lib target/p4-system-4/definition_rv64gc.rs   → rc=0
  # the lowered trees, inspected in the scratch module:
  lr.w    → Sem::Set(Reg("rd"), Sext(64, LoadReserved(Lit(32), Lit(1), Reg("rs1"))))
  amoadd.w → Sem::Set(Reg("rd"), Sext(64, Amo(0, Lit(32), Reg("rs1"), Trunc(32, Reg("rs2")))))
  $ git diff -- crates/ | grep -E '^[+-][^+-]' | grep -vc 'sha256\|Generator:'
  0                          # both tracked modules regenerate HASH-ONLY
  ```

- [x] **NO REGRESSION** — RED-first, then the guard set: the three scratch RED probes
  named (`amo op 0x03 is not one of the closed Zaamo nine this composition encodes
  (0x00, 0x01, 0x04, 0x08, 0x0c, 0x10, 0x14, 0x18, 0x1c) — derived from the composed
  encodings' own funct5 fixed bits`; `(store-conditional …) … this composition does not
  compose riscv/a`; `(load-reserved …) is the rv64gc module's operator surface … the
  rv64i corpus does not lower it`); the new permanent arms: check_semantics 15→17
  (the A operators GREEN + the arity RED, every RED asserting its reason), DEF-GEN
  17→23 (the rv64gc+A emission + 3 variant needles + both REDs); corpus 8/8,
  citations 13/13, SOURCE-FORMAT 211 files, compare_readers 1/1; gen_state/guests/
  board/platform/model_book/book_index `--check` byte-exact; fetch_references
  `--verify-only` green both profiles (the fragments are untouched); `make check`
  rc=0 (8 test groups); `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS
  424→428 textual shell arms — the checker's Python arms ride outside that
  enumerator's scope, as before).

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  logs + changelog; slice (a)'s checklist archived verbatim to `archive/P4-SYSTEM.md`
  at the eighth crossing — the ceiling obeyed, not raised), `MEMORY.md` (next_action →
  slice c), `CHANGELOG.md`, `DEV_NOTES.md` (the two design points; the dated lesson's
  promotion decision:
promotion: declined (the durability is the machinery — the funct5-as-literal design and the conditional emission are armed by the new DEF-GEN/check_semantics RED arms, and the policies are contract text in the schema)),
  `LIVE_STATUS.md` (the re-derived arms count 424→428 only — no row's state moved),
  `docs/book/src/plan/p4.md` (the `.4` section's slice line). Routed INSIDE the tree:
  gen_definition's era-pinned "the 40 forms" module comment updates at slice (e) when
  the rv64gc module regenerates with A (byte-identity forbids it now); the
  `docs/tasks/archive/P4-SYSTEM.md` archive sits 91 B under its own ceiling — the next
  archive event must split the archive (the `P2-SCALAR` checklists/designs precedent).



`P4-SYSTEM.4` slice (c)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0025`), split out on `2026-10-05` at the live file's tenth
ceiling firing (slice (d) landing):

`P4-SYSTEM.4` slice (c) — the reservation state + the SC policy as data + the AMO/LR/SC arms in scratch (`2026-10-05`, `SEMULITH-P4-0025`):

- [x] **REPRODUCE / ISSUE** — the pre-slice census:

  ```
  $ sed -n '640,641p' profiles/rv64gc-lab-v0/state.sexp; git grep -c 'Reservation' -- crates/ | wc -l
  (candidate "reservation set (LR/SC)") (present true) — pre-declared ("so .4 cannot
  smuggle it in silently") but UNGATED: gen_state refused only a TLB-silent census
  (gen_state.py:472-481 pre-edit) / 0 — no reservation module existed
  $ sed -n '370,374p' crates/semulith-core/src/translation.rs
  AccessKind::Store if !entry.w — W only: an AMO on an unreadable page would PASS
  (decision 5 needs R∧W under store/AMO causes)
  $ sed -n '66,80p' target/refs/sail-riscv-src/model/extensions/A/zalrsc_insts.sail
  vmem_write first; on Ok(b): rd <- code, cancel_reservation() — on Err(e): e, NO
  cancel. Sail's two cancellation sites: the COMPLETED SC and reset.
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in existing behavior; the slice
  implements the slice-(b) contract, and execution settled three points, each
  tool-backed (the census above; the `13 pass / 3 fail` initial run):
  1. **The SC clears on the COMPLETED path only** — the Sail measurement above:
     decision 4's "success or failure" is exactly the completed path; a trap clears
     nothing. The arm's clear sites sit after the policy match and after a
     successful store, never on a deliver path.
  2. **The AMO needs `AccessKind::Atomic`** (the census's third line): W-only
     judgment would pass an unreadable page, so the joint R∧W rule with store causes
     (15/7, never 13) got its own kind — additive in `translation.rs` (a scope
     judgment call inside "the additive module" reading, flagged for re-verify).
  3. **The proof caught three TEST-design defects of mine, the engine right each
     time** (the initial run: `13 pass / 3 fail`): my "LR replaces" let the failing
     SC clear before the final SC; my "trapped SC" used a mismatched address, which
     fails with code 1 BEFORE any memory operation — no trap exists to test (the
     scripted boundary-fault variant tests the real path); one expected value
     ignored the final SC's overwrite.

- [x] **FIX** — tracked, additive: `reservation.rs` (NEW — (physical address, width,
  valid), 7 unit tests); `lib.rs`; `privilege.rs` (+ the `reservation()` trait
  accessor) + `privilege/tests.rs` (the Fixture); `translation.rs`
  (`AccessKind::Atomic` + tests); `state.sexp` (the candidate's why → the answered
  form with the deterministic SC policy as DATA, decision 3); `gen_state.py`
  (REQUIRED_CENSUS_CANDIDATES generalising the census gate + the
  field/reset/accessor emit); `state_rv64gc.rs` regenerated (rv64i's
  `state.rs` byte-identical); `definition_rv64gc.rs` regenerated (manifest-hash
  only); `check_state_gen.sh` (+1 RED arm). Scratch (`target/p4-system-4/`,
  untracked): the rv64gc+A module, `proof/exec_rv64gc_a.rs` (the tracked evaluator
  + the three arms), `proof/proof.rs`.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core --lib reservation / translation
  test result: ok. 7 passed (establish/replace/clear/mismatches/cold/determinism) /
  26 passed (25→26: R=0/W=0/A=0/D=0 → 15, R∧W ok, causes 15/7)
  $ bash scripts/check_state_gen.sh --self-test
  STATE-GEN --self-test: 27 pass / 0 fail (26→27: the RED census-silent-on-the-
    reservation arm — "does not declare a present reservation")
  $ target/p4-system-4/proof/proof
  PASS ×16, 0 fail — every cell named in the verification log row below
  $ git diff --stat HEAD -- crates/semulith-core/src/state.rs
  (empty — rv64i's state byte-identical; rv64gc's definition manifest-hash-only, 4 lines)
  ```

- [x] **NO REGRESSION** — RED-first (the initial 13/3 proof run; the STATE-GEN arm's
  RED fired on the fixture), then the guard set: STATE-GEN 26→27, DEF-GEN 23/23,
  corpus 9/9, SOURCE-FORMAT 211; every generator's `--check` byte-exact;
  fetch_references `--verify-only` green both profiles; `make check` rc=0 (fmt +
  clippy -D warnings + 8 groups incl. the new 7+1); `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 428→429 arms).

- [x] **LOCKSTEP** — same commit: this tree (status + frontier + checklist + logs +
  changelog; slice (b)'s checklist archived verbatim at the NINTH crossing — the
  archive was full, so it SPLIT: `archive/P4-SYSTEM.md` (part 1) keeps the earlier
  sections, NEW `archive/P4-SYSTEM-2.md` (part 2) takes this move onward),
  `MEMORY.md` (→ slice d), `CHANGELOG.md`, `DEV_NOTES.md` (the Sail cancellation
  measurement and the three test-design defects; the dated lesson's promotion
  decision:
promotion: declined (the durability is the machinery — the completed-path-only clear is armed by the trapped-SC proof cell and the reservation module's own suite, and the census gate refuses a silent descriptor by name)),
  `LIVE_STATUS.md` (the arms count 428→429 only), `docs/book/src/plan/p4.md` (the
  slice line). The bind's port mapping: the three arms land in `exec_rv64gc.rs`'s
  match after `Sem::TlbInvalidate` with `use crate::privilege::PrivilegedHart;`;
  the proof's cells inform slice (d)'s corpus design.



`P4-SYSTEM.4` slice (d)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0026`), split out on `2026-10-05` at the live file's eleventh
ceiling firing (slice (e) landing):

`P4-SYSTEM.4` slice (d) — the staged corpus + expectations + the matrix rehearsal (`2026-10-05`, `SEMULITH-P4-0026`; untracked `target/p4-system-4/`):

- [x] **REPRODUCE / ISSUE** — the slice-(c) engine is proven, but the bind's
  corpus did not exist yet:

  ```
  $ ls target/p4-system-4/corpus 2>&1 | head -1
  No such file or directory — 0 atomics guests; the tracked matrix's guests are all
  pre-A (its denominator 65, the A forms exercised by none of them)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in tracked behavior; the slice builds
  the staging, and execution caught FOUR authoring defects of mine, each named and
  fixed by re-derivation, never fitting (the corpus's first run read `1 guest(s)
  PASS, 11 FAIL`, rc=1): (1) the derivation tool RECORDED register writes but
  never APPLIED them (downstream values read zeros — the truncation named it at the
  first `sw`); (2) the runner's change-comparison
  rule was unmodeled — a register written ITS OWN VALUE is no observation (the .3
  "x8-already-zero" rule; the first corpus run named 11/12 on exactly this); (3) my
  "reserved funct5 0x02" was LR's OWN funct5 — the .word decoded as `lr.w x6, (x1)`
  and EXECUTED (the observed handler-word read named it; 0x05 replaced it); (4) the
  sv39 data PA collided with the ROOT TABLE (cell 3's store overwrote root[0]; moved
  to base+0x4000).

- [x] **FIX** — staging only: 12 guests (`corpus/*.s` with inline derivation
  directives); `tools/derive_expectations.py` (the EVD-05 spec-side model — from the
  pinned chapters + state.sexp's declared policy, NEVER engine output); its
  `.expected.sexp` (schema-valid ×12) + `run-order.txt`; `guests_staged.rs`
  (gen_guests — the TRACKED assembler assembled every word); `corpus-run/main.rs`;
  `unit/` + `unit-red/` (the staged matrix and the RED legs). No tracked content
  changed.

- [x] **ADDRESSED (verified)** —

  ```
  $ target/p4-system-4/corpus-run/corpus-run; ./corpus-run > r1 && ./corpus-run > r2 && cmp r1 r2
  corpus: 12 guest(s) PASS, 0 FAIL
  $ python3 scripts/check_interaction_matrix.py target/p4-system-4/unit
  28 cells declared, every disposition resolves (rc=0); coverage reads 22 of 22 A
  forms exercised (87 = 65 + 22)
  ```

- [x] **NO REGRESSION** — the RED legs fired by name on `unit-red/`: ORPHAN GUEST,
  OMITTED CELL, UNKNOWN DIFFERENCE. Nothing tracked changed; `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 429 unchanged).

- [x] **LOCKSTEP** — same commit: this tree (status + frontier + checklist + logs +
  changelog; slice (c)'s checklist archived at the TENTH crossing), `MEMORY.md`
  (→ slice e, THE BIND), `CHANGELOG.md`, `DEV_NOTES.md` (the authoring defects; the
  promotion decision:
promotion: declined (the durability is the machinery — the change-comparison rule and the funct5 census are armed by the runner and the corpus, re-runnable at the bind)),
  `LIVE_STATUS.md` (unchanged), `docs/book/src/plan/p4.md` (the slice line). The
  bind's re-run commands are recorded in the changelog.



`P4-SYSTEM.4` slice (e)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0027`), split out on `2026-10-05` at the live file's twelfth
ceiling firing (slice (f) landing):

`P4-SYSTEM.4` slice (e) — THE BIND (`2026-10-05`, `SEMULITH-P4-0027`):

- [x] **REPRODUCE / ISSUE** —

  ```
  $ grep -n 'slot (id a)' profiles/rv64gc-lab-v0/encoding.sexp
  14:    (slot (id a) (requires "riscv/a")) — the staging proven, but A unbound, the
  census 65, the 12 guests and the arms untracked
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; the bind is decision 10. One measured
  generator defect, fixed at root: rustfmt lays the five-fragment list out vertically
  where the four-fragment one stayed inline (79 inline-clean, 90 broken) —
  `gen_definition.py`'s emission was not rustfmt-stable past 80 chars and is now, by
  construction (`cargo fmt --check` rc=0).

- [x] **FIX** — one atomic commit: `encoding.sexp` (slot→extension); the census dual
  edit (schema/profile.sexp + dossier_sexp._SCOPE_LISTS + the scope block 65→87 +
  the PARTS family); REQ-GC-ATOMICS + three D-* mirror sets with CHK pairs;
  `gen_definition.py` (+43-forms comment, +the fmt-stable emission) →
  `definition_rv64gc.rs` (22 forms + 3 variants); the arms ported — the tracked
  evaluator is BYTE-IDENTICAL to the scratch-proven copy; the 12 guests + run-order
  tracked (88); `interactions.sexp` (the staged cells).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed — 88/88; the scratch proofs against the TRACKED build:
  16/16, 88/88
  $ bash scripts/fetch_references.sh --verify-only rv64gc-lab-v0 / rv64i-lab-v0
  MATCH encoding tables vs profile scope 87 == 87 (the exclusion flipped on its own)
  / 52 == 52; owned fragments agree
  $ cmp /tmp/p4s4e-traces-pre.txt /tmp/p4s4e-traces-post.txt
  3,468 == 3,468, clean — BARE-IDENTITY: all 76 pre-bind guests byte-identical
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (8 groups); EXTRACTION 5,
  EXERCISE-COVERAGE (87/87, 52/52), UNIT-COMPOSITION 3 (partial declared),
  INTERACTION-MATRIX 5, RECORD-SCHEMA 20 files, PROFILE-CONSISTENCY 5; `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 429); smoke-bench 53 arms, bench
  wasm, both books.

- [x] **LOCKSTEP** — same commit: this tree (slice (d)'s checklist archived at the
  11th crossing), `MEMORY.md` (→ slice f), `CHANGELOG.md`, `DEV_NOTES.md` (the
  fmt-stability measurement; the promotion decision:
promotion: declined (the durability is the machinery — the rustfmt-stable emission is armed by cargo fmt --check inside make check, which the gate re-runs)),
  `LIVE_STATUS.md` (the P4 row), `docs/book/src/plan/p4.md` + the book index.

`P4-SYSTEM.4` slice (f) : pending — the Sail matched experiment + the leaf acceptance.


`P4-SYSTEM.4` slice (f)'s checklist (completed `2026-10-05`, `SEMULITH-P4-0028`; the
leaf's acceptance record), split out on `2026-10-05` at the live file's thirteenth
ceiling firing — moved to make room for the `.5` design brief:

`P4-SYSTEM.4` slice (f) — the Sail matched experiment; the LEAF CLOSES (`2026-10-05`, `SEMULITH-P4-0028`):

- [x] **REPRODUCE / ISSUE** —

  ```
  $ target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim --config-override <derived>.json --validate-config
  The default configuration merged with … is valid. rc=0 — the override needed NO
  change (A supported true; the region's AMOCASQ / RsrvEventual / (amo|lrsc
  AccessFault) all present — pre-condition 7 re-measured, not assumed)
  $ ls target/p4-system-4/sail/*.elf | wc -l
  0 — the 12 guests had no Sail-runnable images (the corpus ran only in-engine)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — one REAL defect found by the experiment, fixed at
  root, with the measurements on the page:

  ```
  $ <the comparator, first run>        — DIVERGE a-lrsc-fault — step 11 (csrrs x11,
  mcause, x0): sail {'x11': 5}, expectations {'x11': 7}
  $ git diff --stat -- profiles/rv64gc-lab-v0/guests/    # after the fix
  1 file changed, 2 insertions(+), 2 deletions(-) — a-lrsc-fault.expected.sexp only
  ```

  The bind-day misaligned policy (uniform cause 7 for the atomic kinds) is
  measured ILLEGAL for LR — `a-lrsc-fault` came back `sail x11=5 vs expected 7`, and
  RVP-MACHINE's exception table says why: "load and load-reserved instructions
  generate LOAD exceptions" (measured ×1 in the pinned chapter), so the legal set for
  a misaligned LR is causes 4/5, never 7. The policy is now kind-matched (LR → 5,
  SC/AMO → 7) in the engine arm, the schema contract, the state.sexp policy text, the
  D-ATOMIC-MISALIGN decision (+amendment note) and its verbatim REQ/OB mirrors —
  decision 6's "makes the cells AGREE" clause measured false as written and true now.
  The flagged width cell measured as designed: Sail's platform reservation matches on
  the physical ADDRESS alone (the externs take physaddrbits, no width), the
  laboratory's declared width-equal policy fails — both legal, a named divergence.

- [x] **FIX** — untracked experiment tooling (the 12 ELFs at exactly 0x8000_0000 —
  .word-only source + PHDRS link, the tracked assembler owning the bytes; the
  arch-leg comparator on the corpus's change-observation rule); the kind-matched
  policy fix (the files above + the a-lrsc-fault expectations re-derived — the ONLY
  guest file changed, by design, the `.2` slice-f re-derivation pattern);
  `references.sexp` (the third experiment recorded in matched_scope).

- [x] **ADDRESSED (verified)** —

  ```
  $ <the 12-guest comparator against sail 0.14, the tracked override>
  AGREE ×11 (21/20/22/17/18/16/77/41/33/11/14 steps' change-observations exact)
  DIVERGE a-lrsc-mustfail — step 22 (sc.d after lr.w): sail x9<-0 and the store lands
  (trace quoted), the laboratory fails with code 1 under the declared width-equal
  policy; 11 AGREE + 1 NAMED DIVERGENCE of 12. Sail's SC is deterministic under
  RsrvEventual (the pair/loop cells AGREE — the declared never-spurious policy
  matches); the alias cell AGREEs (physical-keyed on both sides)
  $ git diff --stat -- profiles/rv64gc-lab-v0/guests/
  1 file changed — a-lrsc-fault.expected.sexp only (the other 87 guests untouched;
  the override unchanged — nothing predates the policy fix except my own guest)
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed — 88/88; the slice-(c) proof 16/16 against the fixed engine
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (8 groups), `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 429 unchanged); the definition and
  state manifests re-derived (input-hash cascade only); RECORD-SCHEMA 20 files ok
  (the amended decision and its mirrors verbatim-identical); PROFILE-CONSISTENCY 5.

- [x] **LOCKSTEP** — same commit: this tree (leaf status **done** + the Result
  narrative + frontier → `.5` + checklist + logs + changelog), `docs/TASK_TREE.md`
  (4/10), `MEMORY.md` (next_action → `.5`'s design brief), `LIVE_STATUS.md` (4/10),
  `CHANGELOG.md`, `DEV_NOTES.md` (the exception-table measurement and the width-cell
  verdict; the promotion decision:
promotion: declined (the durability is the machinery — the kind-matched policy is armed by the a-lrsc-fault guest and the Sail comparator, both re-runnable)),
  `docs/book/src/plan/p4.md` (the `.4` section completed) + the book index.


`P4-SYSTEM.5` slice (a)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0030`), split out on `2026-10-05` at the live file's fifteenth
ceiling firing (slice (b) landing):

`P4-SYSTEM.5` slice (a) — the virtual-time domain + counter progress + mm-counters' re-derivation (`2026-10-05`, `SEMULITH-P4-0030`):

- [x] **REPRODUCE / ISSUE** — the counters never moved, and one view path could never
  have shown it if they had:

  ```
  $ grep -c "advance\|tick" crates/semulith-core/src/exec_rv64gc.rs
  0 — time/mcycle/minstret all read their reset 0 forever (pre-slice)
  $ grep -l "rdcycle\|rdtime\|rdinstret" profiles/rv64gc-lab-v0/guests/*.s
  mm-counters.s  # the ONLY counter-reading guest of all 88 (7 reads — the brief's
  # census re-measured); grep -l "mip\|sip" → 0 (no mip/sip reader: the STIP-at-reset
  # quirk and the ticking STIP are unobservable in today's corpus); stimecmp only in
  # mm-stimecmp.s, which reads stimecmp and NEVER mip/sip (clean, verified)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in decided behavior; the slice
  implements decision 1, and execution caught one LATENT defect the moving counters
  exposed, with the measurement on the page:

  ```
  $ cargo test -p semulith-core --lib timekeeping    # the first run
  test result: FAILED. 3 passed — csr_read of cycle (0xC00) read 0 where the storage
  held 2: the view mask computed from the view's DECLARED fields is 0 for a
  field-less view, so the counter views would have read 0 forever (rc=1)
  ```

  `csr_read`'s view path exposes exactly the view's declared non-WPRI fields; a
  field-LESS view masks to ZERO (the `.2` zeros passed only because nothing moved).
  Fixed at root: a view declaring no fields is a full-width shadow of its owner (the
  statements' own meaning — "a read-only shadow of mcycle"). Also measured: decision
  1's "one tick per step boundary" has exactly one honest read — time at executed
  step k is k — and instret's genuine count is the trap-END discipline's own flag
  (`!frame.trapped`).

- [x] **FIX** — `timekeeping.rs` (NEW: the domain advance + 7 module tests — the
  TLB/reservation suite pattern); the tick wired into `step_over` (every non-Failed
  outcome, `!frame.trapped` for instret); `privilege.rs` (the full-shadow view fix);
  `state.sexp` (time → view_of mcycle — one domain, one storage, FACT-OWNERSHIP's
  discipline; mcycle/minstret statements carry the declared rate as DATA; the
  census's environment-state candidate answered for the counter-progress part);
  `state_rv64gc.rs` + `definition_rv64gc.rs` regenerated (the manifest cascade;
  CSR storage 33 → 32 as the duplicate row retires); mm-counters' 5 value cells
  re-derived BY DESIGN (the trap cells 13/39 untouched).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core --lib timekeeping
  test result: ok. 7 passed — the domain advances per boundary; instret moves only
  on retired steps; cycle==time reads through the machine AND architectural paths;
  the ticking STIP (reset 1, cleared above time, arriving on the third tick);
  cold-reset determinism; the M-writable base survives the tick; the ACCESS gates
  untouched (gated-off still counts)
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed — 88/88 with the re-derived mm-counters (time values
  0/1/2/25/51 at executed steps 0/1/2/25/51; the gating traps 13/39 unchanged)
  $ cmp /tmp/p4s5a-traces-pre.txt /tmp/p4s5a-traces-post.txt
  4,892 == 4,892 lines, clean — IDENTITY: all 87 non-counter guests byte-identical
  against the parent engine (worktree, both CLIs, removed after)
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (fmt + clippy -D warnings + 8 groups);
  `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS 429 unchanged — the
  new tests are Rust unit tests, invisible to the shell-arm enumerator);
  STATE-GEN both pairs byte-exact against the changed descriptor; the CLI/demo
  trace surface measured unchanged for every guest except mm-counters by design
  (the identity proof above is that measurement — the tick writes no x-register).

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  logs + changelog), `MEMORY.md` (next_action → slice b), `CHANGELOG.md`,
  `DEV_NOTES.md` (the full-shadow measurement and the "time is k" reading; the
  promotion decision:
promotion: declined (the durability is the machinery — the ticking STIP cell and the full-shadow fix are armed by the timekeeping suite and the corpus, both in make check)),
  `LIVE_STATUS.md` (the corpus count is unchanged at 88), `docs/book/src/plan/
  p4.md` (the `.5` section opened).


`P4-SYSTEM.5` slice (b)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0031`), split out on `2026-10-05` at the live file's sixteenth
ceiling firing (slice (c) landing):

`P4-SYSTEM.5` slice (b) — the step-head pending evaluation + interrupt-caused delivery (both vector modes) + the acceptance corpus (`2026-10-05`, `SEMULITH-P4-0031`):

- [x] **REPRODUCE / ISSUE** — decided-but-unimplemented behavior (decision 3), with a
  census that makes the landing provably invisible to the existing corpus:

  ```
  $ grep -c "pending\|deliver" crates/semulith-core/src/exec_rv64gc.rs   # pre-slice
  0 — no interrupt evaluation anywhere; mip/mie/mideleg reset to 0 and stayed there
  $ grep -ln ", mie,\|, sie,\|, mideleg,\|0x304\b\|0x104\b\|0x303\b\|0x344\b\|0x144\b" \
      profiles/rv64gc-lab-v0/guests/*.s | wc -l
  0 — NO existing guest can become interrupt-eligible: the identity proof is unconditional
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in decided behavior; execution caught
  the authoring model's own defects, each measured (the derivation tool's deliver()
  pushing xIE <- xPIE where trap entry wants xPIE <- xIE, xIE <- 0 — the .2–.4
  corpora passed only because every prior trap fired with both 0; i-accept's mtvec
  delta 8 bytes long; i-timer's stimecmp=3 authored against a retired-count clock):

  ```
  $ grep -n "MPIE, take" crates/semulith-core/src/privilege.rs
  465: mstatus = put(mstatus, MPIE, take(mstatus, MIE)); — the engine was right
  all along; the DERIVATION TOOL was wrong, never the engine
  ```

- [x] **FIX** — `interrupts.rs` (NEW: `pending` — the (a)(b)(c) taken-rule + the
  global rule + the delegation mask + the fixed priorities with the M-source bits
  read-only 0 (decision 5) — and `deliver` — the Interrupt-bit shape, xepc the
  un-fetched pc, xtval 0 (declared UNSPECIFIED), the stack, Direct AND Vectored
  honoring xtvec.MODE; 8 module tests); `exec_rv64gc.rs` (the head evaluation
  before the fetch; the boundary still ticks); the derivation tool hardened to the
  engine's field tables (mstatus reset 0xA0000000, the sstatus/sie/sip views,
  per-field write legalization, pc-keyed derivations, the `(fetches N)` convention);
  EVD-05: the seven `i-*` guests + expectations derived BEFORE any engine run.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core --lib interrupts
  test result: ok. 8 passed; 0 failed
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed — 95/95 (the 88 + i-accept/deleg/enable/nest/prio/
  timer/vector: 36+60+21+31+63+26+53 steps, 13 fetch-less deliveries)
  $ <the 88 guests × demo on both builds, cmp> → 88/88 traces IDENTICAL against
  the e37e664 engine (worktree removed) — the census prediction held
  $ python3 scripts/check_interaction_matrix.py profiles/rv64gc-lab-v0
  28 cells declared, every disposition resolves (the 7 i-* mapped, no orphan)
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (fmt + clippy -D warnings + 8 groups);
  `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS 429 unchanged);
  `git status --porcelain -- profiles/rv64gc-lab-v0/guests/ | grep -c "^ M"` → 1,
  and it is run-order.txt's: 14 NEW i-* files, no pre-slice guest file touched,
  nothing fitted.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  logs + changelog; the slice-(a) checklist moved to the archive at the fifteenth
  ceiling firing), `docs/TASK_TREE.md` (the `.5` row), `MEMORY.md` (next_action →
  slice c), `CHANGELOG.md`, `DEV_NOTES.md` (the trap-entry stack measurement and
  the read-only-SEIP lesson; the promotion decision:
promotion: declined (the durability is the machinery — the stack discipline and the view legalizations are armed by the interrupts suite and the 7-guest corpus, both in make check)),
  `LIVE_STATUS.md` (unchanged — it does not count guests), `docs/book/src/plan/
  p4.md` (the `.5` section's slice line).



`P4-SYSTEM`'s Verification Log rows for leaves `.1` and `.2` (both closed `2026-10-03`),
split out verbatim on `2026-10-05` at the live file's fourteenth ceiling firing — the
first LOG-ROW move in this tree (the checklists and design briefs moved before; the
rows' content is preserved here, never summarised):

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-03` | `.2` slice (h) part 2 + LEAF | the config-namespace census (Sail 0.14 git 29e6158, the schema + default pinned; the rv64i override precedent); the validator's three named constraints measured (Zicntr needs a CLINT time source — D-PLATFORM forbids it; medeleg's reserved bit 10 with H off and undelegatable bit 11 — the rule the corpus proves; mideleg's string-typed default len) and the matched mask 0x3FF derived by bisection; the matched override authored and validated; the dossier-format owners extended (schema/override.sexp optional fields — rv64i re-validated; dossier_sexp both directions, self-test 13→14; convert round-trip field-for-field exact); the evidence chain closed (the TRACKED .sexp → materialize_sail_override → Sail → `experiment: 11/12 guests AGREE against the tracked override's derived JSON` — step-for-step on the spec-derived expectations, mm-readonly's all-ones WARL read-back bit-exact); the mm-wfi TW cell named with both wfi-mode traces + the writable-bit proof; mm-counters NOT MATCHABLE with the validator line + the first-step trap; `make check` 8/8 groups, `make gate` all green (DERIVED-COUNTS 419 unchanged) | slice (h) part 2 landed and the LEAF is done: the Sail privileged matched experiment ATTEMPTED and honestly recorded — 11/12 AGREE, mm-wfi's TW cell a named divergence routed to `.5`, mm-counters NOT MATCHABLE with evidence; the leaf's acceptance criterion evidenced by the mode matrix |
| `2026-10-03` | `.2` slice (h) part 1 | the pre-flip rehearsal (a flipped-route copy: EXTRACTION's refines gap and INTERACTION-MATRIX green measured before any tracked edit); the payload byte-probe (state + encoding + interactions + 125 guest files byte-exact from the proven staging); the dossier flip (route `generated-definition`, D-RESOLUTION-ROUTE superseded by note per the D-FENCE precedent, D-ROUTE-FLIP + REQ/OB pair — RECORD-SCHEMA 20 files ok); the generated mirrors content-hash-identical to the scratch-proven modules; `cargo test -p semulith-verify run_rv64gc` 4/4 groups (62/62 on the TRACKED engine path, per-step writes exact + never_written + determinism); the engine port (exec_rv64gc with the trap-END discipline; FlatMemory's fetch alignment as profile data); the CLI smoke (rv64gc run/demo green, bench refusal rc=2, rv64i default trace byte-identical); the gate census (STATE-GEN 22/22 +2 arms, DEF-GEN 17/17 +2, GUEST-GEN 15/15 +5, EXTRACTION 13/13 +2, EXERCISE-COVERAGE 23/23 +2, FACT-OWNERSHIP 10/10, re-pinned 5 units / 74 kinds); the generator's rustfmt-stability fixed at the source (STATE-GEN `--check` compares against regeneration, `cargo fmt` runs over crates/); the CSR migration (the state document owns; csrs.csv 33/33 the derivation source; the pmpaddr0 RED probe); fetch_references both profiles MATCH; `make check` (76 core / 184 verify), `make gate` all green (DERIVED-COUNTS 408→419 re-derived), bench wasm + smoke-bench 53 arms + both books green | the flip landed: the staged unit, corpus, encoding, state and matrix tracked in one atomic commit; the route is `generated-definition`; every gate judges rv64gc fully with rv64i's verdicts unchanged; the split (flip first, Sail second) recorded |
| `2026-10-03` | `.2` slice (g) | the pre-slice census (rv64i's matrix the model — 6 axes/21 cells; the check's four rules read from source; 2 staged expectations carrying rv64i's DIFF-FENCEI-EXECUTED against a references.sexp with 0 difference records; 62 guests to absorb); the axis design derived from the leaf's vocabulary (the 4 corpus layers + legality + delegation + restart REFRAMED guest-shaped — the mechanism registry is closed and no rv64gc mechanism exists); the DIFFS-forced re-derivation of it-fencei/min-fencei (steps unchanged, the divergence form dropped with the reason recorded — the mirror now 44 byte-identical + 5 re-derived); the matrix schema-valid and rehearsed via the check's own invocation (`check_interaction_matrix.py <unit-dir>`): 28 cells declared, every disposition resolves, rc=0; the three RED legs fired by name against a scratch copy (DIFFS on the pre-re-derivation state, ORPHAN GUEST on a dropped name, OMITTED CELL on a deleted cell); the corpus re-proven 62/62; the driver self-test 15/15 and the tracked run `INTERACTION-MATRIX: ok (5 unit(s))`; `make gate` green (DERIVED-COUNTS unchanged at 408) | slice (g) landed: the 7-axis × 28-cell interaction matrix authored at staging (route-contradicted until the flip), all 62 staged guests mapped, 3 cells honestly reported degenerate, no difference ids — the flip's matrix proven |
| `2026-10-03` | `.2` slice (f) | the pre-slice census (49 base guests on disk — c-scope.c toolchain-scoped to rv64i by `scripts/build_c_guest.sh`'s hard-coded `-march=rv64i`; the laboratory memory map and cause vocabulary in the runner); the mirror byte-probe (49 `.s` byte-identical, 46/49 expectations byte-identical, 3 re-derived BY DESIGN under D-IALIGN-16 — targets 2 mod 4 legal with C, RVI-C 27.1 — never fitted); the trap-END bug found by it-fault-alias and fixed in the runner (`trapped` flag); the auipc+addi target audit through the real assembler (14 stale deltas, labels assemble to no word); two execution-caught guest-design bugs (M-level CSR writes inline in S — mm-mret re-laid-out, mm-ecall-modes' handler stage-aware); all 13 mm expectations schema-valid and EVD-05-derived before the run; `corpus: 62 guest(s) PASS, 0 FAIL` (49 base + 13 mm, per-step writes exact, deterministic re-run); the coverage rehearsal over the staged 65-form scope (denominator 65 consistent, exercised 65/65, the 13 extension forms via mm-*); `make gate` green (13 checks, DERIVED-COUNTS unchanged at 408 — no arm added) | slice (f) landed: the base mirror executed 49/49 on the rv64gc engine (3 declared IALIGN-16 divergences), the mode-matrix corpus 13/13 with EVD-05 expectations, the 65/65 coverage rehearsal — all untracked scratch, the flip's corpus proven |
| `2026-10-03` | `.2` slice (e) | the pre-slice census (rv64gc scope 52 vs the fragments' 62+3; the catalogues at 18/18 decision mirrors; the rv64i requirement corpus covers 49 of 52 base forms in 9 instruction records — ecall/ebreak/fence ride event/memory records, the closure measured by probe); the pseudo-census decision measured against EXERCISE-COVERAGE's numerator (the first token of the expectations' insn text observes the spelling); the FOURTH dropped-`(extensions …)`-form copy found and fixed (`_semantics_names`) and the pattern then censused to two MORE readers (check_exercise_coverage.sh, gen_model_book.py — all six sites now uniform, `git grep` clean); the mirror extent derived as a closure (13 requirements + 13 obligations), RECORD-SCHEMA rule 14 MIRROR-DERIVE registered as the governor (self-test 39→43, arms RED-first: drift / missing / ungoverned-authored / owner's contract kept); the fetch leg extended (rv64gc 65==65, rv64i 52==52 unchanged); PARTS DRIFT learned the extension families; EXTRACTION counts pseudos (self-test 9→11); the staged encoding validated (62 + 3 pseudo, PARTIAL with 6 slots, schema conform) and the slice-(d) proof regenerated from it and re-run (26/26); `make gate` green (DERIVED-COUNTS 404→408 arms; the docs/tasks/ aggregate ceiling re-derived 1.5→3 MiB by `decision_task-tree-family-aggregate-rederivation`) | slice (e) landed: the 65-form census by the mandated dual edit, the base-corpus mirror + 3 authored records (34/34), the flip's encoding staged byte-ready, the registry rows (63 fact kinds) |
| `2026-10-03` | `.2` slice (d) | the pre-slice census (gen_definition refuses rv64gc by name; gen_guests' list measured 49 names — the brief's "51" was stale; no privileged arms in exec.rs; elf.rs:88's hard-coded IALIGN=32; the CLI's profile statically rv64i's at main.rs:83); the third copy of the dropped-extensions-form bug (gen_definition's name list — "4 declared instruction(s) have NO semantics: mret, …" named it); `cargo test -p semulith-core --lib privilege` 11/11 (permission model, legalization, views, delivery both ways, xret, computed SD); the scratch execution proof (26/26 checks over six guests — the CSR disciplines, trap delivery with and without delegation, xret mode pops, wfi/sret legality per mode, counter gating, the TVM gate); the digest cascade re-derived (reports + board pin + board artifacts + platform manifest + both books); the PLATFORM-GEN stale-pin arm fixed (it assumed the digest's leading digit); STATE-GEN 20/20 (+3), DEF-GEN 15/15 (+6), GUEST-GEN 10/10 (+3); `make check` green (76 core / 180 verify tests), `make gate` green (DERIVED-COUNTS 395→404) | slice (d) landed: both generators parameterize (rv64i surfaces regenerate hash-only — the embedded generator fingerprints); the tracked privilege.rs machinery over the generated tables; elf.rs's IALIGN is profile data; the scratch execution proof green; the evaluator's new-variant arms port at the flip |
| `2026-10-03` | `.2` slice (c2) | the landing question measured against the gates: STATE-GEN proves the tracked state.rs byte-exact from the TRACKED descriptor in a fresh clone; a tracked rv64gc module from the staged (untracked) descriptor would be unjudgeable there — the three alternatives (skip-if-absent leg, a hand-written interim module, a non-unit descriptor home) each measured dishonest. The scratch proof: gen_state emits `target/p4-system-2/gen/state_rv64gc.rs` (40,198 bytes); a `rustc --test` harness over it — reset-is-the-document (mode M, mstatus 0xA0000000, misa 0x800000000014112D), the 33-CSR address lookup, the view discipline (views carry no storage, every view_of resolves), the field tables (WARL-without-legalization absent, the medeleg 11/16 read-only-0 rows, TSR at bit 22 per the pinned encoding.h), x0/mode transitions — 4 passed / 0 failed | slice (c2) refined: the tracked landing rides the flip (one green commit with the descriptor's move); the interim evidence is recorded; `decision_generated-mirror-needs-tracked-input` |
| `2026-10-03` | `.2` slice (c1) | the pre-slice census (no privileged construct in schema/state.sexp; the route contradiction measured at scripts/check_extraction.py:224-233; gen_state single-profile by refusal; PROFILE-CONSISTENCY csrs cross-check absent, EXTRACTION's reset leg csr-blind); the house-shape refusals (fields wrapper, candidates wrapper — refused by name, reshaped); the staged document validated from target/p4-system-2/: schema conform, --csr-cross 33/33 both directions, _state_resets over the scratch dir green, addresses == pinned csrs.csv 33/33 EXACT, field tables no-overlap/full-coverage; gen_state rv64i byte-identical + rv64gc emits 40198 bytes and rustc-compiles standalone; the composed-reset cross-check fired RED naturally on the real document (mstatus 0xA0000000 ≠ hand-computed 0x300000000 — the descriptor was wrong, the check named it); STATE-GEN self-test 17/17 (+7), PROFILE-CONSISTENCY 44/44 (+3), EXTRACTION 9/9 (+3); `make gate` green (DERIVED-COUNTS 385→395) | slice (c1) landed: the privileged state constructs (csr + per-field discipline tables + privilege_mode), the staged 33-CSR document with the re-earned SEM-08 census, gen_state's two-profile branch with rv64i byte-exact, the two gate gaps closed; the (c1)/(c2) split recorded |
| `2026-10-03` | `.2` slice (b) | the pre-slice census (32 operators, no csr/mode/xret form; ecall's cause a constant 11; a pseudo could not carry semantics; check_citations hard-coded to rv64i.sem.sexp); the spec-text census (xRET/WFI/TSR/TW/TVM/mcounteren/scounteren/STCE/sfence locators read from the pinned chapters; mstatus positions figure-only → encoding.h pinned); check_semantics pair checks 6/6 + 0/0(+3 pseudo) + 4/4 and `--compose` over the trial composition (refinement points ebreak/ecall declared); check_citations `--corpus` 6 resolution(s) — rv64i 52/52 ×3 profiles, zicsr 8/8, zicntr 3/3, system 4/4 under rv64gc; self-tests semantics 15/15 (+7), citations 13/13 (+3), corpus 8/8 (+1, the dropped-form arm proven RED pre-fix); fetch_references `--verify-only` green both profiles (+encoding.h, +causes.csv); DEF-GEN/STATE-GEN/GUEST-GEN byte-exact; `make gate` green (DERIVED-COUNTS 384→385) | slice (b) landed: 8 new operators (field, inst, mode, csr-state, csr-read, csr-write, trap-deliver, xret), the three sem files with every per-instruction decision cited, the WARL seam recorded for slice (c), rv64i.sem.sexp untouched |
| `2026-10-03` | `.2` slice (a) | the upstream census (13 mnemonics over master's `extensions/`: rv_zicsr 6 real rows, rv_zicntr 3 pseudo-only rows of csrrs, rv_system mret/wfi + rv_s sret/sfence.vma; the moved rv_* tables byte-identical to the rv64i pins; the pinned arg_lut.csv already carries csr/zimm5); fetch_references `--verify-only` green for BOTH profiles + a scripted fresh re-fetch of rv_s byte-identical; check_sexp_schema on the new references.sexp and all 5 fragments; check_encoding_disjoint self-test 12/12 (+3 pseudo arms, +1 dupes arm) and the trial compositions (base+each new fragment; the 62-instruction 4-fragment union collision-free through a synthetic unit doc); the assembler probe (all 13 forms assembled, the spike-dasm round-trip exact, 4 RED operand refusals named, IALIGN 32 refuses / 16 accepts an entry 2 mod 4, rv64i derives 32 and rv64gc 16); UNIT-COMPOSITION self-test 9/9; EXERCISE-COVERAGE 21/21; EXTRACTION / INTERACTION-MATRIX / SOURCE-FORMAT / SEMANTICS / DOSSIER-SCHEMA / PROFILE-CONSISTENCY green; GUEST-GEN / DEF-GEN / STATE-GEN byte-exact; `make gate` green (DERIVED-COUNTS 383→384 arms re-derived) | slice (a) landed: the Zicsr / Zicntr / privileged-system fragments from the re-pinned tables, the csr operand field and IALIGN as profile data; rv64i's generated surfaces byte-identical; the unit stays on the `profile-resolution` route |
| `2026-10-03` | `.1` | the snapshot census measured on disk (24 priv + 46 unpriv pages, 21/21 pins re-hashed against the tracked SHA256SUMS); the chapter versions measured from the page titles (M 2.0, A 2.1, F 2.2, D 2.2, C 2.0, Zicsr/Zifencei/Zicntr 2.0, RVWMO 2.0, Machine/Supervisor 1.13, Sstc 1.0); the closure statements measured (G = IMAFDZicsr_Zifencei — naming 36.1; D⇒F — 21.1; F⇒Zicsr — 20.1; C⇒Zca+Zcd at RV64 — zc 28.1.2; IALIGN=16 — 27.1); the PDF pins re-verified against the catalog (3/3); RECORD-SCHEMA 18 record files; EXTRACTION 5 units (the resolution leg: obligations checked both ways); EXERCISE-COVERAGE / INTERACTION-MATRIX 5 units (n/a by declaration); PROFILE-CONSISTENCY 5 dossiers; FACT-OWNERSHIP 61 kinds (fixture re-pinned 9→10); check_citations 52/52 for both units + the 3 named skips; route self-tests 11/11 + 21/21 + 15/15; `make gate` green (DERIVED-COUNTS 376→383 arms re-derived) | the profile resolved: rv64gc-lab-v0 — every element source-located, the closure measured, the dossier landed unregistered with the new profile-resolution route honored by declaration in three gates |


`P4-SYSTEM`'s Verification Log rows for leaf `.4` (closed `2026-10-05`),
split out verbatim on `2026-10-05` at the live file's sixteenth ceiling firing
(the `.5` slice-(c) landing) — the closed-leaf lifecycle of the `.1`/`.2` rows
above:

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-05` | `.4` slice (f) + LEAF | the override census (validate-config rc=0; A/AMOCASQ/RsrvEventual/AccessFault all present — no change needed, pre-condition 7 re-measured); the 12 ELFs at exactly 0x8000_0000 (.word-only + PHDRS, the tracked assembler owning the bytes); the experiment (11 AGREE + 1 NAMED DIVERGENCE of 12 on the corpus's change-observation rule — the width cell: sail's address-only reservation matches sc.d-after-lr.w, the laboratory's declared width-equal policy fails, both legal; sail's SC deterministic under RsrvEventual; the alias cell physical-keyed on both sides); the REAL defect it caught (the bind-day uniform-7 misaligned policy measured ILLEGAL for LR — sail x11=5 vs expected 7; the exception table's kind mapping) fixed at root (engine arm, schema contract, state.sexp, D-ATOMIC-MISALIGN + note, verbatim mirrors) with exactly ONE guest file re-derived (a-lrsc-fault.expected.sexp; the other 87 untouched; the override unchanged); `cargo test -p semulith-verify run_rv64gc` 4/4 (88/88), the slice-(c) proof 16/16; `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS 429 unchanged), RECORD-SCHEMA 20 files, PROFILE-CONSISTENCY 5 | the LEAF CLOSES: single-core reservation behaviour validated — the corpus falsifies EVD-05 expectations and the differential confirms them (11 AGREE + 1 named of 12); the multicore boundary named (MC-MULTICORE, RVWMO §17.1.1–§17.1.1.4); frontier → `.5` |
| `2026-10-05` | `.4` slice (e) — THE BIND | the pre-bind census (the slot open); the bind landed whole: slot→extension; the census dual edit 65→87 (+ the PARTS family); REQ-GC-ATOMICS (22) + three D-* mirror sets (RECORD-SCHEMA 20 files ok); definition_rv64gc.rs regenerated (22 forms + 3 variants + the era comment 40→43); the evaluator ported byte-identical to the scratch proof; the 12 guests + matrix cells tracked (28 resolve, no orphan); the one generator defect fixed at root (rustfmt's vertical array past 79 chars — stable by construction now); `cargo test -p semulith-verify run_rv64gc` 4/4 (88/88 with per-step writes, never_written, determinism, fetch counts); the scratch proofs against the TRACKED build (16/16, 88/88); the fetch leg flipped on its own (87==87, rv64i 52==52); BARE-IDENTITY 3,468 == 3,468 lines, cmp clean (parent worktree, both CLIs, 76 guests); `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS 429), smoke-bench 53 arms, bench wasm, both books | THE BIND landed: the unit composes `riscv/a` — 87 forms judged, 88 guests green, the 76 pre-bind guests byte-identical |
| `2026-10-05` | `.4` slice (d) | the pre-slice census (0 atomics guests); the 12-guest staged corpus with the EVD-05 spec-side derivation (schema-valid ×12); four authoring defects caught and re-derived (the tool's unapplied register writes; the same-value-write rule; the "reserved" funct5 0x02 that IS LR's; the sv39 data PA in the root table); every word through the TRACKED assembler; the corpus through the slice-(c) scratch engine: **12 PASS / 0 FAIL**, deterministic re-run identical; the matrix rehearsal 28 cells resolve with the three named RED legs; coverage 22/22 (87 = 65 + 22); nothing tracked changed; `make gate` all green (DERIVED-COUNTS 429) | slice (d) landed: the atomics corpus staged and proven — the bind's payload is ready |
| `2026-10-05` | `.4` slice (c) | the pre-slice census (the reservation candidate pre-declared but ungated; 0 reservation module; Store judging W-only at translation.rs:374; Sail's cancellation sites read at zalrsc_insts.sail:71-79 — completed-path cancel only); the reservation module 7/7; AccessKind::Atomic with the suite 25→26 (R=0/W=0/A=0/D=0 → 15 never 13); the generalised census gate with the STATE-GEN RED arm 26→27; rv64i's state byte-identical, the definition manifest hash-only; the scratch proof 16/16 (every must-fail cell, the trapped SC keeping its reservation, misaligned → 7 before translation, the AMO nine × .W/.D with the boundary pair asserted, the translated-AMO and alias cells, the first-SC loop, cold-reset determinism — plus three caught test-design defects of mine); gen pairs byte-exact; fetch `--verify-only` both profiles; `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS 428→429) | slice (c) landed: the reservation state with the SC policy as state-document data, the generalised census gate, and the AMO/LR/SC arms proven in scratch — the tracked evaluator untouched, the bind's port mapping recorded |
| `2026-10-04` | `.4` slice (b) | the pre-slice census (40 operators, no atomic form; the memory operators exactly load/store; no a.sem.sexp; the generator knowing no A operator; the evaluator's Sem match exhaustive — TlbInvalidate the last arm, no wildcard); the normative sentences re-located in the pinned chapters (the AMO store/AMO fault rules ×1 each in RVP-SUPERVISOR/RVP-MACHINE; the SC-invalidates and nonzero-code sentences ×1 in RVI-A §12.1.2; the 16-instruction loop ×1 in §12.1.3); the bare-symbol-op probe (`'add' is not an operand this instruction has` rc=1 — the funct5-as-lit design); the pair check 22/22, the two trial compositions (--compose base+A and the 5-fragment set) with every override declared; the corpus gate ok (8 checks) and the citations corpus (a.sem.sexp vs rv64gc offline: RVI-A §12.1.2 ×4, §12.1.4 ×18; 5 files / 7 resolutions); the scratch lowering (78,752-byte module over base+zicsr+zicntr+system+A, rustc rc=0 standalone, the lr.w/amoadd.w trees inspected) with three named RED probes (the closed-nine refusal derived from the composed encodings, the no-A-composition guard, the rv64i guard); self-tests check_semantics 15→17, DEF-GEN 17→23, corpus 8/8, citations 13/13; the tracked modules hash-only (0 non-hash diff lines); `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS 424→428) | slice (b) landed: the 43-form language with the reservation contract, a.sem.sexp for all 22 forms cited, and the conditional lowering — the tracked surfaces gain not one A byte, the slot stays declared, rv64i's module hash-only |
| `2026-10-04` | `.4` slice (a) | the pre-slice census (`grep rv_a\|rv64_a` over the ledger → rc=1; 9 files under definitions/riscv, no A; the whitelists aq-count 0; the whole-token lookup refusing `lr.w`; the pinned arg_lut.csv carrying aqrl/aq/rl/amoop; the A chapter encoding-free, RVWMO Tables 6/7 the 22-form enumeration); the tracked-route fetch (rv_a 858 B d9eaa988…, rv64_a 885 B 819e0487… — 11+11 real rows, tokens `aq rl`, no amoop/aqrl token, lr's 24..20=0); the root fixes measured RED-first (the rv64_* collector gap — the census saw neither rv64_a nor rv64_m; the A pin without the named exclusion → `tables 87 vs declared 65`, the M-exclusion shape followed); fetch_references `--verify-only` green for BOTH profiles (65==65, 52==52, ISA string MATCH) + a scripted fresh re-fetch of rv_a byte-identical; gen_fragments re-run with the existing five byte-identical (`git diff --stat -- definitions/` empty); check_sexp_schema ok on a.sexp; the trial compositions through a synthetic unit doc (base+A 74 COMPOSE; the 5-fragment union 84 + 3 pseudo COMPOSE, slot declared); the assembler probe (88 words = 22 forms × 4 suffix combinations, the spike-dasm round-trip exact — lr's suffix words print plain, spike's preference, the bits measured set; 11 RED refusals named: garbage suffix, suffix-on-non-atomic, bare/offset address shapes, wrong arities); disjoint self-test 12/12, unit-composition 9/9 + 3 units decided, SOURCE-FORMAT 210, compare_readers 1/1, all generators byte-exact; `make gate` green (DERIVED-COUNTS 424 unchanged) | slice (a) landed: the rv_a/rv64_a re-pin, the generated a.sexp fragment (owns aq/rl, requires rv64i), and the assembler's A machinery (the suffix-as-field-value rule, the `(rs1)` spelling, refusals by name); the slot stays declared, the census 65, rv64i's surfaces byte-identical |

