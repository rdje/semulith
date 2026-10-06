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


`P4-SYSTEM.5` slice (c)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0032`), split out on `2026-10-05` at the live file's seventeenth
ceiling firing (slice (d) landing):

`P4-SYSTEM.5` slice (c) — the halted state + WFI's real wake + the `<halted>` vocabulary + the wake corpus + mm-wfi's re-derivation (`2026-10-05`, `SEMULITH-P4-0032`):

- [x] **REPRODUCE / ISSUE** — the acceptance's enabling machinery was absent, and
  exactly one guest's legal-WFI cells depended on the stated nop:

  ```
  $ grep -c "waiting\|wake" crates/semulith-core/src/exec_rv64gc.rs   # pre-slice
  0 — no hart-state bit, no wake; a legal wfi retired as a stated nop
  $ grep -ln "wfi" profiles/rv64gc-lab-v0/guests/*.s
  mm-wfi.s — the ONLY guest containing wfi (the hard boundary's census,
  re-measured): the identity proof's by-design exception is exactly one guest
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in decided behavior; the wake
  sentences were measured verbatim before authoring (the delegation-wake cell
  especially): RVP-MACHINE §2.1.3.3 — 'the hart must resume if a locally enabled
  interrupt becomes pending, even if it has been delegated to a less-privileged
  mode', 'required to resume … at any privilege level, regardless of the global
  interrupt enable', and the WFI-specific 'mepc = pc + 4'. The brief's claims
  measured TRUE, so the wake condition is exactly mip & mie != 0 — no globals,
  no mideleg — and a delegated source waking an M-mode hart is spec-backed
  (w-deleg rides it).

- [x] **FIX** — `wait.rs` (NEW: the ACTIVE/WAITING bit, cold-ACTIVE at reset, a
  pure function of hart history — the TLB/reservation module discipline);
  `exec_rv64gc.rs` (the halted-step head arm — the wake first, else tick-and-
  stay — and the legal-wfi enter); `interrupts.rs` (`wake_pending` + 2 tests);
  the SEM-08 census's wait-state candidate (gen_state carries the bit, the gate
  gains the RED arm); `system.sem.sexp`'s stated nop superseded by the halt with
  its date; EVD-05: the 4 w-* guests + mm-wfi re-derived, never fitted.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core --lib
  test result: ok. 128 passed — the bit, the wake (globals/mideleg ignored,
  the timer's arrival through the domain), the whole suite
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed — 99/99: the wake family (w-timer 23 steps with
  rdinstret=11 at the handler's first step — the acceptance observed; w-notrap
  19, w-deleg 26, w-sw 17; 6 `<halted>` steps at fetches 0), mm-wfi 61 (4
  halted; the TW=1/U trap cells measured unchanged), and everyone else
  $ <the 95 pre-slice guests × demo on both builds, cmp> → 94 IDENTICAL,
  mm-wfi the only difference (by design, corpus-proven; the worktree removed)
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (fmt + clippy -D warnings + 8
  groups); `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS 429 →
  430 re-derived — the wait-state RED arm; LIVE_STATUS's count re-derived,
  byte-neutral); STATE-GEN: both pairs in sync with the new candidate gated
  RED-first; the matrix resolves 28 cells with the wake family mapped.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  logs + changelog; the slice-(b) checklist and the closed `.4` leaf's log rows
  moved to the archive at the sixteenth ceiling firing), `docs/TASK_TREE.md`,
  `MEMORY.md` (next_action → slice d), `CHANGELOG.md`, `DEV_NOTES.md` (the
  span-zero wake and the end-marker text-collision lessons; the promotion
  decision:
promotion: declined (the durability is the machinery — the wake rule and the halt are armed by the wait/interrupts suites and the 99-guest corpus, both in make check)),
  `LIVE_STATUS.md` (the arm count re-derived 429→430), `docs/book/src/plan/
  p4.md` (the `.5` section's slice line).


`P4-SYSTEM.5` slice (d)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0033`; the leaf's acceptance record), split out on `2026-10-05`
at the live file's eighteenth ceiling firing (the `.6` slice-(a) landing):

`P4-SYSTEM.5` slice (d) — the Sail matched attempt + the reports + the book; the LEAF CLOSES (`2026-10-05`, `SEMULITH-P4-0033`):

- [x] **REPRODUCE / ISSUE** —

  ```
  $ target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim --config-override \
      target/refs/sail-rv64gc-lab-v0.override.json --validate-config
  The default configuration merged with … is valid. rc=0 — the override needed
  NO change (materialized fresh from the tracked .sexp, itself unchanged since
  bfa6aaa — git log; mideleg/mip/mie/Sstc were already covered, pre-condition
  measured, never assumed)
  $ ls target/p4-system-5/sail/*.elf | wc -l
  0 → 13 — the 12 corpus guests + the TW probe had no Sail-runnable images
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no engine defect this slice; the six named
  divergences are all platform-shaped, each measured to its sentence:

  ```
  $ grep -n "plat_have_clint" target/refs/sail-riscv-src/model/core/interrupt_regs.sail
  250:  let platform_has_timer = plat_have_clint; — the gate, measured in the pinned
  source: with clint.supported=false (D-PLATFORM) mip[STI] never sets (i-prio step 24,
  i-timer step 3); the counter registers themselves are the `.2` wall — Zicntr
  supported=false, so rdtime/rdinstret trap illegal on sail (the mm-wfi trace's
  tval=0xC01023F3). And platform.wfi_is_nop=true: sail's wfi never dwells and the
  TW judgment lives only in the wait-exit path the nop never reaches (step.sail,
  the run_hart_waiting arm)
  ```

- [x] **FIX** — untracked experiment tooling (`target/p4-system-5/sail/`: the ELF
  builder — the tracked assembler's bytes, .word-only + PHDRS at exactly
  0x8000_0000, measured; the row-keyed comparator — Sail NUMBERS the
  interrupt-delivery step and prints no row, measured on i-accept's [9]→[11]
  jump, the `.3` fetch-fault convention's own shape); probe-tw (the TW cells in
  isolation); `references.sexp` (the fourth experiment recorded in
  matched_scope); the book's `.5` section completed + the index regenerated.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 target/p4-system-5/sail/compare_sail.py
  AGREE ×6 (i-accept 36, i-deleg 60, i-enable 21, i-nest 31, i-vector 53,
  w-sw 17 — 218 steps' change-observations exact, the delivery-step convention
  identical on both sides)
  DIVERGE ×6, all named platform-shaped: i-prio step 24 (sail x13=2 vs 34 —
  STIP), i-timer step 3 (sail x7=0 vs 32 — STIP), w-deleg step 12 / w-notrap
  step 6 / w-timer step 11 / mm-wfi step 9 ('sail printed a row for the
  <halted> step the convention says it skips')
  $ probe-tw: DIVERGE under the matched config (step 25 — sail never judges
  TW), AGREE 30/30 under the wfi-wait variant (cause 2, mepc = the wfi's pc,
  xtval = the wfi's word — the delivered trap identical, only its timing is
  sail's own)
  $ the `.4` corpus re-run under the fresh override: 11 AGREE + 1 NAMED of 12
  — the identical outcome (the width cell's sail x9=0 at step 22) —
  verdict-neutral, the `.4` expectations untouched since 495b4b8
  $ python3 scripts/check_interaction_matrix.py profiles/rv64gc-lab-v0
  28 cells declared, every disposition resolves; the three RED legs fired by
  name on a scratch copy (ORPHAN GUEST w-timer / OMITTED CELL restart×restart
  / UNKNOWN DIFFERENCE)
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed — 99/99
  ```

- [x] **THE LEAF ACCEPTANCE** — "timer or interrupt wake occurs without CPU
  retirement — the laboratory must be able to make time pass while nothing
  executes", quoted from the actual w-timer run (`semulith demo --guest=w-timer`):

  ```
  [11] [M]: 0x000000008000002c      — three boundaries, no register observation
  [12] [M]: 0x000000008000002c        (the two `<halted>` steps and the delivery)
  [13] [M]: 0x000000008000002c
  [14] [M]: 0x0000000080000030
  x14 <- 0x000000000000000b         — rdinstret = 11 at the handler's first step:
                                      the ten setup instructions and the wfi, and
                                      NOTHING across the halt or the delivery —
                                      the wake occurred WITHOUT CPU RETIREMENT
  x11 <- 0x8000000000000005         — mcause: the Interrupt bit with cause 5
  x12 <- 0x000000008000002c         — mepc = the wfi's pc + 4 (§2.1.3.3)
  ```

  `make check` rc=0 (fmt + clippy -D warnings + 8 groups), `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 430 unchanged); RECORD-SCHEMA
  20 files ok (references.sexp's matched_scope gain); PROFILE-CONSISTENCY 5;
  smoke-bench 53 arms + bench wasm + both books green — re-run this slice even
  though no tracked engine/fixture content changed (the experiment tooling is
  untracked scratch; the bench/books are the cheap proof, `make ci`'s legs).

- [x] **LOCKSTEP** — same commit: this tree (leaf status **done** + the Result
  narrative + frontier → `.6` + checklist + logs + changelog; the slice-(c)
  checklist moved to the archive at the seventeenth ceiling firing),
  `docs/TASK_TREE.md` (5/10), `MEMORY.md` (next_action → `.6`'s design brief),
  `LIVE_STATUS.md` (5/10), `CHANGELOG.md`, `DEV_NOTES.md` (the promotion
  decision:
promotion: declined (the durability is the machinery — the corpus verdicts are armed by make check, and the matched attempt is re-derivable: the override materializes from the tracked unit and the scratch comparator/ELFs are preserved under target/)),
  `docs/book/src/plan/p4.md` (the `.5` section completed) + the book index.


`P4-SYSTEM.6` slice (a)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0035`), split out on `2026-10-05` at the live file's nineteenth
ceiling firing (slice (b) landing):

`P4-SYSTEM.6` slice (a) — the rv_zifencei re-pin + the one-form fragment + zifencei.sem.sexp + the assembler acceptance (`2026-10-05`, `SEMULITH-P4-0035`):

- [x] **REPRODUCE / ISSUE** —

  ```
  $ ls target/refs/riscv-opcodes/rv_zifencei 2>&1
  No such file — the slot's table was pinned nowhere (pre-condition 1 re-measured)
  $ curl -sSL -o target/refs/riscv-opcodes/rv_zifencei \
      https://raw.githubusercontent.com/riscv/riscv-opcodes/master/extensions/rv_zifencei
  $ shasum -a 256 target/refs/riscv-opcodes/rv_zifencei; wc -c < target/refs/riscv-opcodes/rv_zifencei
  be2d8f7286e06fadafffbde14656e6adb3f923ce704ea0829229d3a3b5f35758; 73 bytes —
  exactly one row: `fence.i imm12 rs1 14..12=1 rd 6..2=0x03 1..0=3`
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — one brief claim measured FALSE as written and
  is recorded honestly: decision 1's "no assembler shapes (the zero-operand
  ecall/ebreak precedent)" — ecall/ebreak carry NO operand fields, but fence.i's
  table row LISTS imm12/rs1/rd, so the table-driven assembler refused the
  standard-software spelling:

  ```
  $ <assemble "fence.i" through the trial composition, pre-fix>
  REFUSED 'fence.i' -> fence.i expects 3 operand(s) ['imm12', 'rs1', 'rd'], got 0
  $ grep -c "shall ignore these fields" .materials/riscv/pinned-v20260120/unpriv/zifencei.html
  1 — the sentence the acceptance implements, measured in the pinned chapter
  ```

  The chapter's own sentence ("base implementations shall ignore these fields,
  and standard software shall zero these fields", RVI-ZIFENCEI §4.1 — every
  normative sentence re-located in the pinned chapter) makes the bare spelling
  the STANDARD one, so the acceptance lands as a named, cited special case in
  `riscv_asm.py` (the A-suffix precedent's shape) — never a table edit. Decision
  1's OTHER no-change claims measured TRUE: the nop effect needs no Sem variant
  and no generator change (the lowering below).

- [x] **FIX** — the pin (references.sexp's row + supplies/note amendments);
  `fetch_references.sh`'s named exclusion (the `.4` slice-(a) M/A pattern: the
  table is pinned for the fragment, not the scope, until slice (b)'s bind flips
  it); the FRAGMENTS entry → generated `zifencei.sexp` (owns NO fields,
  requires rv64i, funct3=1); `zifencei.sem.sexp` (hand-written, `(effect (nop))`
  with the three normative sentences, the coherent/uncached-RAM latitude and the
  shall-ignore rule cited); the zero-operand acceptance in `riscv_asm.py`.

- [x] **ADDRESSED (verified)** —

  ```
  $ <fetch --verify-only, both profiles> — 87 == 87 (the exclusion holds),
  52 == 52; "owned fragments agree with the pinned upstream"; a scripted fresh
  re-fetch byte-identical (cmp clean)
  $ python3 scripts/check_encoding_disjoint.py rv64i+zifencei
  53 instruction(s), no collisions — COMPOSE; the profile's set + zifencei:
  85 instruction(s) (+ 3 pseudo), no collisions — COMPOSE; self-test 12/12
  $ python3 scripts/check_semantics.py zifencei.sexp zifencei.sem.sexp
  1 of 1 checked; --compose base+zifencei and the full set: "the semantics
  compose — every override is declared"; self-test 17/17
  $ python3 scripts/check_citations.py --corpus
  RVI-ZIFENCEI §4.1 ×1 — 6 sem files, 8 resolutions, offline
  $ <the assembler probe> — 'fence.i' -> 0x0000100f; 'fence.i 0, x0, x0' the
  same word; 'fence.i 1, x2, x3' -> 0x0011118f (the shall-ignore word);
  REFUSED by name: 'fence.i x1', 'fence.i 0, x0', 'fence.i foo';
  spike-dasm round-trip exact: DASM(0000100f) -> fence.i, DASM(0011118f) ->
  fence.i (the second decoder applies the shall-ignore rule too)
  $ <gen_definition over BOTH trial compositions> — fence.i emits mask
  0x0000707f / value 0x0000100f over the EXISTING Sem::Nop (mask covers
  funct3+opcode only — the shall-ignore decode); rustc rc=0 standalone; NO
  generator change (the nop-effect one-form measured; justified)
  $ <gen_fragments + gen_guests> — the six existing fragments byte-identical;
  all 99 guests re-assemble byte-identical through the edited assembler
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (fmt + clippy -D warnings + 8
  groups); `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS 430
  unchanged — the exclusion is a script line, no new arm); the slot STAYS
  declared (encoding.sexp untouched); the census STAYS 87; no corpus, no Rust.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  logs + changelog; the slice-(d) checklist moved to the archive at the
  eighteenth ceiling firing), `MEMORY.md` (next_action → slice b, THE BIND),
  `CHANGELOG.md`, `DEV_NOTES.md` (the promotion decision:
promotion: declined (the durability is the machinery — the zero-operand acceptance is armed by the probe spellings in this checklist and the 99-guest byte-exact re-assembly, both re-runnable)),
  `LIVE_STATUS.md` (unchanged — the leaf is open), `docs/TASK_TREE.md` (unchanged
  — the frontier leaf is `.6` already), `docs/book/src/plan/p4.md` (the `.6`
  section's slice line) + the book index.


`P4-SYSTEM.6` slice (b)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0036`), split out on `2026-10-05` at the live file's twentieth
ceiling firing (slice (c) landing):

`P4-SYSTEM.6` slice (b) — THE BIND: fence.i legal in the tracked unit (`2026-10-05`, `SEMULITH-P4-0036`):

- [x] **REPRODUCE / ISSUE** —

  ```
  $ grep -c "slot (id zifencei)" profiles/rv64gc-lab-v0/encoding.sexp
  1 — the slot waited (cause-2 pre-bind); 0 rows generated
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; one shape correction against my
  own first draft, measured by the mirror governor (GUEST-GEN):

  ```
  $ bash scripts/check_guest_gen.sh --self-test
  MIRROR DRIFT — the four edited .s files broke byte-identity with their rv64i
  owners: the mirror holds .s byte-identical ALWAYS; the bound-state story
  belongs to the expectation comment blocks (the .2 slice-(g) shape)
  ```

- [x] **FIX** — encoding.sexp (slot→extension); the census dual edit 87→88
  (the .4 lesson's four places, the zifencei_fencei family); definition_rv64gc.rs
  regenerated; REQ-GC-FENCEI + OB-GC-FENCEI (no new D-* — the wfi-nop
  precedent); the fencei re-derivations + the two new guests; the decision-3
  corrections as recorded mirror re-derivations.

- [x] **ADDRESSED (verified)** —

  ```
  $ bash scripts/fetch_references.sh rv64gc-lab-v0 --verify-only
  MATCH 88 == 88 — the exclusion flipped on its own (rv64i 52 == 52)
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed — 101/101 (x2 written, 0x0011118F ignored,
  the patched fetch reads 7)
  $ <99 pre-bind guests × demo, cmp> → 98 IDENTICAL; it-fencei the only
  difference (min-fencei's trace byte-identical — the delivery wrote
  nothing at mtvec=0); worktree removed
  $ python3 scripts/check_interaction_matrix.py profiles/rv64gc-lab-v0
  28 cells declared, every disposition resolves; EXERCISE-COVERAGE 88/88;
  GUEST-GEN self-test 16/16; RECORD-SCHEMA both files ok
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (fmt + clippy -D warnings + 8
  groups); `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS 430
  unchanged); UNIT-COMPOSITION 3; SHARD-FREEZE 186 rows.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  logs + changelog; the slice-(a) checklist archived at the nineteenth
  firing), `MEMORY.md` (next_action → slice c), `CHANGELOG.md`,
  `DEV_NOTES.md` (the mirror-discipline lesson; the promotion decision:
promotion: declined (the durability is the machinery — the mirror governor names drift on every gate run, and the bind's corpus verdicts are armed by make check)),
  `LIVE_STATUS.md` (unchanged), `docs/book/src/plan/p4.md` + the book index.


`P4-SYSTEM.6` slice (c)'s checklist (completed `2026-10-05`,
`SEMULITH-P4-0037`; the leaf's acceptance record), split out on `2026-10-06`
at the live file's twenty-first ceiling firing (the `.7` slice-(a) landing):

`P4-SYSTEM.6` slice (c) — the Sail matched experiment + the census re-answer + the reports and the book; the LEAF CLOSES (`2026-10-05`, `SEMULITH-P4-0037`):

- [x] **REPRODUCE / ISSUE** —

  ```
  $ <validate-config with the override materialized fresh from the tracked unit>
  The default configuration merged with … is valid. rc=0; Zifencei supported
  true (the .6 brief's pre-condition 3 re-measured; the tracked .sexp unmoved
  since bfa6aaa — git log); NO override change needed
  $ grep -c "instruction-fetch cache" profiles/rv64gc-lab-v0/state.sexp
  1 — the candidate's why still read rv64i's recording, whose clause argues the
  choice from the extension's ABSENCE (true of rv64i, stale at the bind)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; one brief phrasing measured
  imprecise (recorded): pre-condition 2 located the 'without Zifencei' clause
  IN rv64gc's candidate — it actually lives one hop away, in rv64i's verbatim
  text the candidate references; the re-answer makes the bind's consequence
  explicit in place either way. The designed outcome held everywhere else:

  ```
  $ grep -n "encdec = FENCEI" target/refs/sail-riscv-src/model/extensions/Zifencei/zifencei_insts.sail
  mapping clause encdec = FENCEI(imm, rs, rd) — the fields are VARIABLES
  (decoded-not-fixed), the shall-ignore sentence quoted in sail's own comment;
  execute = sail_barrier + RETIRE_SUCCESS ('a nop for the memory model')
  ```

- [x] **FIX** — the experiment tooling (`target/p4-system-6/sail/`: 6 ELFs at
  exactly 0x8000_0000 — fencei-selfmod/dir-selfmod-fence's auipc-derived patch
  targets MEASURED entry-relative, so the absolute entry matters); the row-keyed
  comparator; `state.sexp`'s fetch-cache candidate re-answered in place (the
  consequence line unchanged); `references.sexp`'s fifth experiment recorded;
  the book's `.6` section completed.

- [x] **ADDRESSED (verified)** —

  ```
  $ <the 6-guest comparator against sail 0.14, the matched override>
  AGREE ×6 (it-fencei 3, min-fencei 1, fencei-reserved 2, fencei-selfmod 8,
  fault-selfmod 7, dir-selfmod-fence 8 — 29 steps' change-observations exact,
  the patched fetch reading the new value on both sides): the designed AGREE
  measured, not assumed; ZERO non-AGREE cells to name
  $ git log --oneline -1 -- profiles/rv64gc-lab-v0/guests/a-amo-aqrl.expected.sexp
  495b4b8 — the wider corpus's expectations unmoved since their verdicts;
  nothing to re-run (the bind touched only the fencei surface)
  $ python3 scripts/gen_state.py <the re-answered descriptor> && cargo build
  wrote state_rv64gc.rs (the candidate's new why carried into the module),
  rc=0; STATE-GEN's own pair check green at make gate
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed — 101/101
  ```

- [x] **THE LEAF ACCEPTANCE** — "rewrite-code fixtures with and without the
  architectural synchronization", measured on BOTH engines: WITH —
  fencei-selfmod's fence.i retires between the store and the fetch and the
  patched word reads 7 (sail AND semulith, step-for-step); WITHOUT —
  fault-selfmod's patch is visible with NO synchronization, D-CODE-VISIBILITY
  named (the laboratory's declared legal subset of the chapter's may-or-may-not);
  the staleness half answered as the declared latitude (intro.html's
  implicit-reads sentence — a valid implementation may cache every fetchable
  byte forever; the caching-hart model rejected at the brief, decision 2).

- [x] **NO REGRESSION** — `make check` rc=0 (fmt + clippy -D warnings + 8
  groups); `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS 430
  unchanged); RECORD-SCHEMA 20 files ok (references.sexp's matched_scope gain
  and the two mirror files verbatim-identical); PROFILE-CONSISTENCY 5;
  smoke-bench 53 arms + bench wasm + both books green (no tracked
  engine/fixture content changed this slice beyond the re-derived
  state/definition pair — the experiment tooling is untracked scratch; the
  legs re-run anyway as the cheap proof).

- [x] **LOCKSTEP** — same commit: this tree (leaf status **done** + the Result
  narrative + frontier → `.7` + checklist + logs + changelog; the slice-(b)
  checklist and the `.1`/`.2` changelog entries moved to the archive at the
  twentieth ceiling firing), `docs/TASK_TREE.md` (6/10), `MEMORY.md`
  (next_action → `.7`'s design brief, the routed ancestry flagged),
  `LIVE_STATUS.md` (6/10, byte-neutral), `CHANGELOG.md`, `DEV_NOTES.md` (the
  promotion decision:
promotion: declined (the durability is the machinery — the six AGREEs are re-runnable against the materialized override, and the acceptance pair is armed by make check)),
  `docs/book/src/plan/p4.md` (the `.6` section completed) + the book index.



`P4-SYSTEM.7` slice (a)'s checklist (completed `2026-10-06`,
`SEMULITH-P4-0039`), split out on `2026-10-06` at the live file's
twenty-third ceiling firing (the `.7` slice-(b) landing):

`P4-SYSTEM.7` slice (a) — the backend qualification: rustc_apfloat QUALIFIED (`2026-10-06`, `SEMULITH-P4-0039`):

- [x] **REPRODUCE / ISSUE** — the acceptance requires the qualification MEASURED,
  and the census's claims were web leads:

  ```
  $ curl -sSL crates.io/api/v1/crates/{rustc_apfloat,softfloat} + the .crate tarballs
  rustc_apfloat: 0.2.3+llvm-462a31f5a5ab, updated 2025-06-11, Apache-2.0 WITH
    LLVM-exception (the LICENSE texts measured in the extracted crate)
  softfloat: 1.0.0, updated 2023-11-03, MIT OR Apache-2.0 — the musl-libc
    lineage via const_soft_float, NOT Berkeley
  the negatives re-confirmed: softfloat-sys/-wrapper are Berkeley C FFI;
  softfloat-pure does not resolve
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; the capability gaps measured in
  the extracted sources (the `grep -c` tallies are on the vlog row): softfloat
  has NO rounding modes, NO exception flags ("Not Asserted" is a comment), NO
  fma, NO 64-bit int conversions, NO min/max — five of ARCH §6's explicit
  requirements; rustc_apfloat carries the whole surface EXCEPT sqrt (never
  ported) and two measured LLVM-vs-IEEE flag deviations. One census claim
  measured UNVERIFIABLE (softfloat's "TestFloat-verified upstream" — its own
  documents carry no such statement; recorded, not counted). The MPFR path
  needed four measured corrections of MPFR's own semantics (a reference
  library's flags are ITS semantics; a generator that trusts them writes a
  wrong spec).

- [x] **FIX** — the scratch harnesses (`target/p4-system-7/`: `probe/` the
  corpus/APFloat/softfloat/cross-check/timing harness; `mpfr/vec_gen.c` the
  MPFR vector generator over the system libmpfr 4.2.2, MPFR's own semantics
  corrected spec-side: RNDNA, exponent-range OF/UF, NaN canonicalization,
  NAN ≠ NV); the decision record + INDEX + the knowledge card; the dependency
  landing (`=0.2.3+llvm-462a31f5a5ab` pinned in semulith-core, the lib.rs
  re-export compile-use, the cargo home on-volume).

- [x] **ADDRESSED (verified)** —

  ```
  $ probe run (63,752 cases, directed + seeded, per op × 5 modes × 2 widths):
  ZERO arithmetic-core value disagreements; 612 value + 386 flag disagreements,
  all named — the two LLVM-vs-IEEE deviations (362 want OFNX; 24 want NV on
  sNaN conversions) and the policy surfaces (NaN→int 340, fmin/fmax 240, NaN
  payloads 32); sqrt not probed on APFloat (1,440 — fp.rs owns it); SOFTFLOAT
  vs MPFR (4,416): 68, ALL the NaN-sign family — MPFR-exact where it exists
  $ probe time: apfloat f64 add/mul/div 10.1/10.5/40.7 ns/op, fma 15.7;
  softfloat 3.2/2.3/5.1, sqrt 44.1
  $ cargo build --release --target wasm32-unknown-unknown (both): Finished —
  PORT-WEB proof for both
  $ <the landing> — Cargo.lock 4 → 7 (rustc_apfloat + bitflags + smallvec);
  make bench wasm 133,715 bytes, smoke-bench 53 arms ok
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (fmt + clippy -D warnings + 8
  groups); `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS 430
  unchanged; the knowledge map regenerated for the new decision record); no
  corpus touch, no engine touch.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  logs + changelog; the `.6` slice-(c) checklist + changelog entries archived at
  the 21st/22nd ceiling firings), `MEMORY.md` (next_action → slice b),
  `CHANGELOG.md`, `DEV_NOTES.md` — the promotion MEASURED positive: the
  candidate-landscape lesson promoted to docs/knowledge/
  (a-candidate-landscape-census-entry-is-a-lead.md + INDEX), `docs/decisions/`
  INDEX + the new record, `LIVE_STATUS.md` (unchanged), `docs/TASK_TREE.md`
  (unchanged — the frontier leaf is `.7` already), `docs/book/src/plan/p4.md`
  (the `.7` section opened) + the book index.

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


`P4-SYSTEM`'s Verification Log rows for leaf `.3` (closed `2026-10-04`),
split out verbatim on `2026-10-05` at the live file's seventeenth ceiling firing
(the `.5` slice-(d) landing) — the same closed-leaf lifecycle:

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-04` | `.3` slice (e) part 2 | the pre-slice census (the mm driver names no sv39 guest; the override's medeleg mask 0x3FF — page faults not delegatable, the laboratory pins 0-10 \| 12-15 \| 18-20 WARL-any; sail's --trace-ptw/--trace-tlb present as own flags); the ELF build (the tracked assembler owns the bytes — a .word-only source + a PHDRS link at EXACTLY 0x8000_0000, the chains' absolute addressing requires it); the fetch-fault harness convention (sail numbers the step, prints no row — the `<fetch page fault>` pseudo-steps are exactly the no-row no-write steps); the sv39-deleg measurement (sail x22=13 vs expected x7=13 — the override's mask, not the engine); the mask bisection (sail 0.14 names causes 10/14 reserved, rejects 17-20 → 0xB3FF, the widest mask both sides honor); the experiment (13 AGREE + 1 AGREE-RECORDED of 14 — every walk read-for-read identical incl. tlb-fence's 7 add / 2 flush; svade's A/D-placement convention recorded: sail judges A/D after the walk, the laboratory at step 9, the delivered trap identical); the no-regression (the widened mask verdict-neutral: 11/12 mm AGREE under it, mm-wfi's TW cell named at the same step; `git diff SEMULITH-P4-0019 -- crates/ profiles/rv64gc-lab-v0/guests/ | wc -l` → 0); `cargo test -p semulith-verify run_rv64gc` 4/4; `make check` 8/8, `make gate` all green (DERIVED-COUNTS 424 unchanged) | slice (e) part 2 landed and the leaf CLOSES: the sv39 matched experiment — architecture, PTW and TLB explicit per guest — the acceptance met: the correct fault AND the permitted page-table side effects (none under Svade, the ld-back proof); A/D validated, not a knob |
| `2026-10-04` | `.3` slice (e) part 1 | the pre-slice census (0 sv39 guests in the run order; the sv39 path proven only by the 25 translation unit tests; the one-fetch-per-step witness unable to speak about a fetch page fault); the authoring tooling (fixpoint layout + the chain-accumulating audit that knows table targets; the spec-side model — the pinned 10-step walk, Svade, MPRV, medeleg, region bounds, the slice-(d) TLB semantics — EVD-05, never engine output); the 14 guests each executed green through `demo` (translate-4k/2m/1g with the PTE-byte-untouched ld-backs; the four fault guests' causes 12/13/15 with xtval; the R/W/X and U/SUM/MXR permission matrices incl. the fetch page fault; the Svade no-update proofs; MPRV's translated/physical distinction incl. the no-code-mapping fetch-immunity proof; the TLB stale/fence/G-retention sequence; the non-contiguous-page straddle as two fetch requests; medeleg's selective routing S-vs-M); the probe-bug corrections (mscratch is M-only — an S-mode write traps illegal, engine measured right; x8-already-zero records no change; the coalescing rule is address contiguity, measured 53 fetches); `cargo test -p semulith-verify run_rv64gc` 4/4 (76/76, per-step writes + never_written + determinism + declared fetch counts); the `fetches` schema field optional with the parcel-bounds refusal (GUEST-GEN 15→16, the RED arm fired); INTERACTION-MATRIX 28 cells every disposition resolves (the 14 guests on the SAME seven axes); the byte-level identity proof (both CLIs, all 62 pre-slice guests, `62 byte-identical, 0 diverge`, worktree removed); `make check` 8/8, `make gate` all green (DERIVED-COUNTS 423→424), smoke-bench 53 arms, bench wasm, both books | slice (e) part 1 landed: the 14-guest sv39 corpus with EVD-05 spec-side expectations — every walk fault cause, the permission matrix, Svade's no-update, MPRV, the TLB's fence semantics, the straddle, and delegation — with Bare byte-exact and the fetch-count witness made declarational |
| `2026-10-04` | `.3` slice (d) | the pre-slice census (the stated nop at `system.sem.sexp:14-19,53-59` — the header bullet + the effect; the census's own reopen hook — the `address-translation caches (TLBs)` candidate with `.3 reopens this candidate`; mm-sfence's three fence cells); the parameter decision recorded (4 entries, fully-associative, FIFO, ASID-tagged at ASIDLEN=16, keyed by 4 KiB page — minimal for every rule to be testable; authority laboratory; the census carries the same parameters as data and the generator REFUSES a silent one, with a RED arm); the satp-visibility measurement (per-access reads for MODE/ASID — immediate; root-PPN visible on the next miss with stale hits sanctioned until a fence, the fence being the contract; SUM/MXR never cached — always immediate); the install discipline (a faulting access installs nothing; a load past a D=0 leaf installs the D=0 entry — the legal stale store fault after software sets D without fencing, then the fence restores); the sem-operator landing (`tlb-invalidate` in schema + the extended binary map + the Sem variant + the evaluator arm — rs1 the VA, rs2's low 16 the ASID, no register written; the time-scoped nop superseded with its date); the TLB suite (25/25: hit skips the walk, FIFO evicts in order, ASID tags + G hits, staleness legal then restored, Svade staleness through the cache, the four fence cases with retentions, the non-canonical rs1 no-op, the fence INSTRUCTION end-to-end, cold-reset determinism — tuples identical); the census re-answer + STATE-GEN 26/26 (+1 RED arm) + DEF-GEN both pairs (the definition manifest re-derived after the descriptor change); mm-sfence measured — NO re-derivation needed (its cells never claimed a nop; a fence writes no register); the byte-level identity proof on the TLB engine (both CLIs, all 62 guests, 1,884 == 1,884, cmp clean, worktree removed); `make check` 8/8 groups, `make gate` all green (DERIVED-COUNTS 422→423), smoke-bench 53 arms, bench wasm, both books | slice (d) landed: the minimal fully-specified TLB (4-entry FA FIFO, ASID-16, G-bit retention, keyed by 4 KiB page), sfence.vma's four cases implemented as specified over it (over-fence recorded-not-taken; the invalid rs1 VA a no-op), the census re-answered with the parameters as data and the storage emitted from it, and the determinism rule tested — all with Bare byte-exact |
| `2026-10-04` | `.3` slice (c) | the pre-slice census (`grep -c FETCH` over rv64gc's requirements → 0: the amendment has NO mirrored record to supersede — the mirror's closure is 13 records and REQ-D-FETCH-IMPLICIT is not among them, so rv64i's owner record stays true of rv64i and the amendment lands as a new authored pair); the 10-step walk implemented cited step-by-step (§11.1.4.1's canonical check before any read; walk-access reads with the step-2 access fault by kind 1/5/7; V=0 and the W-without-R reserved case — the first draft's R∧W inversion caught by the fault-matrix tests written before the fix; bits 63/62–61/60–54 zero with Svnapot/Svpbmt named unselected; superpage misalignment; non-leaf D/A/U reserved; the shadow-stack step named N/A; U/SUM/MXR + R/W/X; Svade step 9 page-fault-instead-of-update with the byte-untouched proof; the PA by level); 17 translation tests covering the full matrix (3 leaf sizes with their walk counts 3/2/1, canonical-VA, V=0, reserved-RW, reserved bits ×3, misaligned superpage, non-leaf D/A/U ×3 + last-level pointer, U/SUM/MXR 6 cells, R/W/X 3 cells, Svade 4 cells, the step-2 access fault by kind, the MPRV cells, the satp.MODE defect, the straddle with 2 fetches + 6 walk reads + the joined word); `cargo test -p semulith-verify run_rv64gc` 4/4 groups; the byte-level identity proof on the walk-live engine (both CLIs, all 62 guests, 1,884 == 1,884, `cmp` clean, worktree removed); the probe updated (S-mode fetch under Sv39 with an empty root → V=0 → `mcause = 12`, `mtval =` the faulting VA — the slice-(b) stub now faults properly); the requirement amendment (D-WALK-IMPLICIT + verbatim REQ/OB mirrors, dependencies D-SV39/D-SVADE, RECORD-SCHEMA 20 files ok); `make check` 8/8 groups, `make gate` all green, smoke-bench 53 arms, bench wasm, both books | slice (c) landed: the 10-step Sv39 walk is live — cited step-by-step, the fault matrix proven cell-by-cell with the walk reads counted and the Svade PTE-untouched proof, the straddled fetch live, and the implicit-access vocabulary amended honestly (a new authored pair; the mirror measured absent) |
| `2026-10-04` | `.3` slice (b) | the pre-slice census (the brief's three hook sites read at exec_rv64gc.rs:87/291/328; satp.MODE `(one-of 0 8)` reset Bare in the state document; `git grep -c PageFault -- crates/ | wc -l` → 0); the parcel/coalescing measurement (decision 5's 16-bit parcels translate independently, but the fetch issues exactly one request whenever both translated addresses share one physical 32-bit unit — under Bare every case, so the Bare request shape is byte-exact by construction; the fetch-count assertion family holds it); the translation module (6 unit tests: Bare-identity × mode/kind, M never translated even under Sv39, the sub-M walk entry, MPRV selects MPP for data accesses only with SUM/MXR carried, the out-of-vocabulary satp.MODE named panic, the 12/13/15 vocabulary); the walk-access variant's three match sites answered per profile (FlatMemory answers, the bench census gains `walks`, rv64i's TestEnv panics named); `cargo test -p semulith-verify run_rv64gc` 4/4 groups (62/62, fetch counts unchanged); the byte-level identity proof (both CLIs from a 4fdac5b worktree vs the post-change build over all 62 guests: 1,884 == 1,884 trace lines, `cmp` clean); the Sv39-entry probe (an S-mode `ld` with satp.MODE=Sv39 → `model error: Unimplemented { what: "Sv39 translation — the walk is P4-SYSTEM.3 slice (c)'s" }`, cli rc=1); `make check` 8/8 groups, `make gate` all green (DERIVED-COUNTS 422 unchanged), smoke-bench 53 arms, bench wasm, both books | slice (b) landed: the translation machinery shell — the effective-mode computation, satp.MODE dispatch, the page-fault vocabulary, the parcels with their recorded coalescing choice, the walk-access boundary variant — with Bare proven an EXACT identity path byte-for-byte |
| `2026-10-03` | `.3` slice (a) | the pre-slice census (ADUE inside menvcfg's wpri_62_0 by construction; the .2 override's Svade explicitly `false` against Sail's default `true`; validate_gc carrying NONE of the rv64i path's three construct refusals; the ISA-string census over seven trees); the canonical-order re-derivation (gen_platform's declared-order rule — the string is `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade` exactly as the brief names it); the dossier flip (D-SVADE with the three evidence legs + the D-SV39 note, the verbatim REQ/OB mirrors — RECORD-SCHEMA 20 files ok, rule 4/rule 9 by its own run); DOSSIER OQ-2 CLOSED with the legs quoted; sources measured (RVP-SUPERVISOR's pin covers §11.1.3.1/§11.1.10 inline — NO new pins); the override one-field flip + `--validate-config` valid + the full 12-guest re-run (`re-run after the Svade flip: 11/12 guests AGREE against the tracked override's derived JSON` — baseline-identical, the mm-wfi TW cell unchanged); the validate_gc refusals with three RED arms on mapping-valid injected shapes (STATE-GEN 22→25 arms, both real pairs byte-identical); `make check` 8/8 groups; `make gate` all green (DERIVED-COUNTS 419→422 re-derived) | slice (a) landed: the profile's identity is Svade (OQ-2 closed with evidence), the reference flips to match with every verdict measured unchanged, and the generator hole the brief named is refused by name |


`P4-SYSTEM`'s Verification Log rows for leaf `.5` (closed `2026-10-05`), split out
verbatim on `2026-10-05` at the live file's eighteenth ceiling firing (the `.6` design
brief landing) — the closed-leaf log-row lifecycle established at the fourteenth:

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-05` | `.5` slice (d) + LEAF | the override measured first (materialized fresh from the tracked .sexp — unchanged since bfa6aaa; validate-config rc=0, NO change needed); the 13 ELFs at exactly 0x8000_0000 (.word-only + PHDRS, the tracked assembler owning the bytes); the row-keyed comparator with the delivery-step convention MEASURED (sail numbers the interrupt-delivery step and prints no row — i-accept's [9]→[11] jump, the .3 fetch-fault convention's own shape); the experiment (6 AGREE + 6 NAMED of 12 — the six named all platform-shaped: sail's timer block gated on plat_have_clint so STIP never sets (i-prio step 24 sail x13=2 vs 34, i-timer step 3 sail x7=0 vs 32), sail's wfi a nop under the matched platform so the halt has no counterpart (w-deleg 12 / w-notrap 6 / w-timer 11 / mm-wfi 9 — 'sail printed a row for the `<halted>` step'), and probe-tw DIVERGE under the matched config (sail never judges TW — the judgment lives only in the wait-exit path the nop never reaches) but AGREE 30/30 under the wfi-wait variant with the delivered trap identical — cause 2, mepc = the wfi's pc, xtval = the wfi's word); the verdict-neutrality re-run (the .4 corpus under the fresh override reproduces 11 AGREE + 1 NAMED of 12 exactly); the matrix invocation (28 cells resolve) + the three RED legs fired by name on a scratch copy (ORPHAN GUEST / OMITTED CELL / UNKNOWN DIFFERENCE); references.sexp's fourth experiment recorded; the acceptance evidence quoted from the actual w-timer run (rdinstret=11 at the handler's first step; mcause=int\|5; mepc=wfi+4); `cargo test -p semulith-verify run_rv64gc` 4/4 (99/99); `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS 430 unchanged), RECORD-SCHEMA 20 files, PROFILE-CONSISTENCY 5, smoke-bench 53 arms + bench wasm + both books | the LEAF CLOSES: the timer wake occurs WITHOUT CPU RETIREMENT (w-timer's own run quoted); masks, priority, pending/active state, nesting and return validated; the 64-bit domain's width and declared rate validated with the wrap position stated honestly; the mode gates stand; the matched attempt confirms the matchable cells and records every not-matchable with its measurement; frontier → `.6` |
| `2026-10-05` | `.5` slice (c) | the pre-slice census (0 waiting/wake in the step; mm-wfi the ONLY wfi guest of the 95); §2.1.3.3's wake sentences measured verbatim (the delegation claim TRUE — the wake is exactly mip & mie; xepc = wfi+4 falls out of the generic delivery, the WFI retiring into the halt); the wait module 2/2 + the wake tests 2/2 (globals/mideleg ignored, the timer's arrival through the domain); the SEM-08 wait-state candidate with gen_state carrying the bit and the RED arm (the synthetic fixture + the present-false surgery); the 4 w-* guests + mm-wfi re-derived BEFORE any engine run (23/19/26/17/61 steps, 10 `<halted>` at fetches 0 — w-timer's rdinstret=11 the acceptance observed; mm-wfi's TW/U cells unchanged; the end_at text-collision caught and fixed at the guest); `cargo test -p semulith-verify run_rv64gc` 4/4 (99/99); the identity proof (94/95 byte-identical, mm-wfi the designed exception, worktree removed); the matrix (28 cells resolve, the family mapped); `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS 429→430 re-derived) | slice (c) landed: the hart halts and time passes anyway — the timer wake occurs WITHOUT CPU RETIREMENT, the TW resolutions stand, only mm-wfi's trace moved |
| `2026-10-05` | `.5` slice (b) | the pre-slice census (0 interrupt writes in all 88 guests — name and numeric form; 0 mip/sip/mie readers; mm-stimecmp stimecmp-only ⇒ the identity proof unconditional); the interrupts module 8/8 (the taken-rule per mode, the delegation mask, the priority walk, the delivery shape, both vector modes, the stack, the S view); the derivation tool hardened to the engine's field tables (mstatus reset 0xA0000000, sstatus/sie/sip views + per-field write legalization + the computed STIP, the CSR-privilege refusal, pc-keyed derivations, the (fetches N) convention) — the authoring model's own defects caught by execution and re-derived, never fitted (the tool's inverted trap-entry stack; i-accept's 8-byte-long mtvec delta; i-timer's retired-count clock; i-vector's SEIP-clear through read-only sip); the 7 i-* guests + EVD-05 expectations derived BEFORE any engine run (36/60/21/31/63/26/53 steps, 13 fetch-less deliveries); `cargo test -p semulith-verify run_rv64gc` 4/4 (95/95); the identity proof (88/88 traces cmp-clean against e37e664, worktree removed); the matrix (28 cells resolve, 7 mapped, no orphan); `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS 429 unchanged) | slice (b) landed: pending is evaluated at every step head and delivered honoring both vector modes — the corpus proves the taken-rule, the mask, the priorities, the timer, the vector arithmetic and the nesting stack; every pre-slice guest byte-identical |
| `2026-10-05` | `.5` slice (a) | the pre-slice census (the counters frozen at 0; the full-88-guest read census — mm-counters the ONLY counter reader (7 reads), 0 mip/sip readers (the STIP-at-reset quirk and the ticking STIP unobservable today), mm-stimecmp clean of counter/mip/sip reads); the storage-shape decision (ONE domain — mcycle's storage, time a view, 'a valid implementation of RDTIME', §6.1; the duplicate row retired, FACT-OWNERSHIP); the LATENT view defect measured and fixed at root (a field-less view masked to 0 — the counters would have read 0 forever; a field-less view is now a full-width shadow); the timekeeping module 7/7 (advance per boundary, instret only on retired, cycle==time both read paths, the ticking STIP incl. the reset quirk, cold-reset determinism, the M-writable base, the ACCESS gates); mm-counters' 5 value cells re-derived BY DESIGN (0/1/2/25/51 — time at executed step k is k; the trap cells 13/39 untouched); `cargo test -p semulith-verify run_rv64gc` 4/4 (88/88); the identity proof (4,892 == 4,892 lines, cmp clean — 87 non-counter guests byte-identical, worktree removed); `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS 429 unchanged), STATE-GEN both pairs re-derived (CSR storage 33→32) | slice (a) landed: the declared virtual-time domain ticks one per step boundary (retired or halted), instret counts genuinely, the rate is state-document data, mm-counters re-derived, everyone else byte-identical |


`P4-SYSTEM`'s Changelog entries for leaves `.1` and `.2` (both closed
`2026-10-03`), split out verbatim on `2026-10-05` at the live file's twentieth
ceiling firing (the `.6` slice-(c) landing) — the first CHANGELOG-ENTRY move in
this tree (the checklists, design briefs and log rows moved before; the section's
per-slice entries for a closed leaf are the same lifecycle category, and the
archive's own per-part ceiling bounds what can land at once):

- `2026-10-03`: `.2` slice (f) done (`SEMULITH-P4-0010`) — the guests corpus, executed.
  The base mirror runs on the rv64gc engine: all 49 rv64i guests staged byte-identically
  (c-scope.c excluded — the pinned toolchain script hard-codes `-march=rv64i`, the rv64gc
  C-guest question recorded for the flip) and executed against their expectations by the
  scratch corpus runner (the declared MainMemory map, fetch/load/store fault delivery on
  the pinned cause vocabulary, the trap-END discipline fixed after it-fault-alias exposed
  it, the rv64i verify runner's per-step x-register-change comparison rule). 46
  expectation files carry over byte-identically; 3 were RE-DERIVED BY DESIGN — under
  D-IALIGN-16 the misaligned-jump targets (2 mod 4) are legal (RVI-C 27.1), so the link
  write lands and no fetch fault fires; a declared profile difference, measured, never a
  soundness contradiction and never fitted to output. The mode matrix adds 13 guests with
  EVD-05 expectations derived from the pinned chapters BEFORE the run: the six zicsr
  forms' rw semantics, M-CSR legality per mode, delivered breakpoints that resume, ecall
  causes 11/9/8 by mode and medeleg delegation to S (M-ecall never delegates), mret mode
  pops with the MPRV clear-below-M / preserve-at-M rule, sret legality and the TSR gate,
  wfi and the TW gate, sfence.vma/satp and the TVM gate, the counter enables
  (mcounteren then scounteren), stimecmp's TM then STCE gating, read-only CSR writes and
  the mstatus all-ones WARL read-back. Execution itself caught and fixed 14 stale
  auipc+addi vector deltas (labels assemble to no word), two guest-design bugs (M-level
  CSR writes inline in S-mode — the drops now happen before or inside the M handler),
  one hex-digit slip in the mstatus WARL constant and one no-change mis-derivation —
  every mismatch re-derived, never fitted. `corpus: 62 guest(s) PASS, 0 FAIL`, and the
  coverage rehearsal over the staged 65-form scope reads 65/65 (the base 52 via the
  mirror, the 13 extension forms via mm-*). Everything stays untracked scratch — no gate
  arms this slice (the guests' registry governor lands at the flip); `make gate` green
  (DERIVED-COUNTS unchanged at 408).
  Next: slice (g) — the interactions.sexp.

- `2026-10-03`: `.2` slice (e) done (`SEMULITH-P4-0009`) — the unit's census, catalogues,
  and the flip's staged encoding. The scope census grows 52→65 by the mandated dual edit
  (`schema/profile.sexp` + `dossier_sexp._SCOPE_LISTS`: +zicsr_csrs, +system_privileged,
  +zicntr_counters). The pseudo-census decision, measured and recorded in the profile's
  scope comment: the Zicntr reads ARE census forms (the spec's listings name them), the
  encoding realizes them as csrrs specializations, and EXERCISE-COVERAGE observes the
  spelling in the expectations' insn text (measured: the numerator is its first token);
  EXTRACTION's integrative claim now counts the composition's pseudo names. The base
  corpus's requirement mirror is derived, not typed: the closure probe measured 13
  requirement records (the 9 instruction families + fence/ecall-ebreak + XLEN/ENDIAN
  dependencies) and their 13 obligations; rv64gc's catalogues carry them byte-verbatim but
  for the profile-scoped fields, with `mirrored_from` provenance, plus 3+3 authored records
  for the new forms (34/34 each). RECORD-SCHEMA's new rule 14 (MIRROR-DERIVE) is the
  governor, registry-driven by two new FACT-OWNERSHIP rows (63 kinds); its self-test arms
  fired RED on a drifted, a missing, an ungoverned-authored, and a wrong-contract mirror.
  The flip's encoding.sexp is staged at `target/p4-system-2/profiles/rv64gc-lab-v0/` with
  the flip's own bytes (relative fragment-root, `(status partial)`, six slots), validated
  collision-free; the slice-(d) proof regenerated from it and re-run (26/26). The
  dropped-`(extensions …)`-form latent bug was censused to its SIXTH reader and the
  pattern is gone (`git grep` clean). `make gate` green; the docs/tasks/ aggregate ceiling
  re-derived 1.5→3 MiB by decision record (the slice checklists are the designed growth).
  Next: slice (f) — the guests corpus.

- `2026-10-03`: `.2` slice (d) done (`SEMULITH-P4-0008`) — the generators parameterize and
  the privileged machinery lands. The two-profile shape was measured into existence: the
  tracked evaluator matches rv64i's byte-frozen generated `Sem` enum, so the new
  operators' evaluation arms cannot compile tracked until the rv64gc definition module is
  tracked (the flip) — and the MACHINERY doesn't wait: `crates/semulith-core/src/
  privilege.rs` owns trap delivery (delegation selection, the xPIE/xIE/xPP stack,
  xepc/xcause/xtval, pc←xtvec), xret, the uniform CSR permission model and WPRI/WARL/WLRL
  legalization over a `PrivilegedHart` trait whose metadata types it owns; the generated
  rv64gc state module (scratch until the flip) implements the trait with the descriptor's
  tables. The WARL seam closed: prose legalization became the structured `(legalize …)`
  mini-language (schema + document + mapping + generator + the read-only/reset
  cross-checks). gen_definition's rv64gc branch lowers the 8 slice-(b) operators and emits
  pseudos as PSEUDOS metadata (60,984 bytes, rustc-clean at scratch); its composition name
  list carried the THIRD copy of the dropped-`(extensions …)`-form bug — fixed. gen_guests
  is directory-derived (the set is the directory; the run order is the tracked
  run-order.txt, cross-checked both directions; rv64i regenerates hash-only — measured:
  the brief's "51-name list" was 49). elf.rs's IALIGN is a parameter (rv64i 32, rv64gc 16
  — the routed twin of the slice-(a) fix). The scratch execution proof: six assembled
  guests through the generated modules + the tracked machinery — the CSR read/write
  disciplines, trap delivery with and without delegation, the mret/sret mode pops, wfi/sret
  legality per mode, counter gating, the TVM gate — 26/26, catching two authoring defects
  on the way (an atomic CSR's write preserving everything; medeleg[8] delegated where an
  S-ecall is cause 9). The dossier digest rotated on run-order.txt and the cascade
  re-derived (reports, the board pin, the platform manifest, both model books); the
  PLATFORM-GEN stale-pin arm that assumed the digest's leading digit was fixed to a
  fixed-shape mutation. `make check` + `make gate` green (DERIVED-COUNTS 395→404 arms).
  Next: slice (e) — the unit artifacts.

- `2026-10-03`: `.2` slice (c2) done as a refinement (`SEMULITH-P4-0007`) — the tracked
  landing of the rv64gc state module is flip-bound, measured, not assumed: STATE-GEN
  proves rv64i's module byte-exact from its TRACKED descriptor in a fresh clone, and a
  tracked module generated from the staged (untracked) document would be unjudgeable
  there — a copy, not a derivation. The three alternatives were each measured dishonest
  (a skip-if-absent gate leg is a standing hole in the byte-exact property; a hand-written
  interim module is a second owner, OWN-01; a non-unit descriptor home is a category lie).
  The interim evidence: the generated module (40,198 bytes) compiles standalone and a
  scratch `rustc --test` harness proves it behaviorally (reset per the document, the
  33-CSR address lookup, the view discipline, the field tables, x0/mode — 4/4).
  `decision_generated-mirror-needs-tracked-input` records the rule; it constrains slice
  (d)'s engine execution the same way. Next: slice (d) — gen_definition/gen_guests
  parameterization + engine exec of the CSR/trap instructions.

- `2026-10-03`: `.2` slice (c1) done (`SEMULITH-P4-0006`) — the state leg, split recorded:
  (c1) zero Rust — the schema's privileged constructs, the staged document, the generator,
  the gates; (c2) the engine-side consumption follows. `schema/state.sexp` gained
  `privilege_mode` (hart state, not a CSR — the stack lives in mstatus) and the `csr`
  construct with per-FIELD tables (WPRI/WARL/WLRL per RVP-CSR §1.1.3.1–3, legalization,
  reset, locator per field; `view_of` records the sstatus/sie/sip and counter views — a
  view declares no storage). The rv64gc state document is authored and fully validated
  from `target/p4-system-2/state.sexp` — the route contradiction makes profiles/ placement
  RED until the flip, so validation runs against the scratch path: schema conform, the new
  `--csr-cross` probe (profile's (csrs …) == the document, 33/33 both directions),
  `_state_resets` over the scratch dir, addresses == pinned csrs.csv 33/33, field coverage
  complete. The 33 CSRs carry their tables: mstatus/sstatus with the xIE/xPIE/xPP stack
  and the TSR/TW/TVM gates, mtvec/stvec BASE/MODE, medeleg with the brief's pinned
  delegatable subset (11 and 16 read-only 0), mideleg all-delegatable, mepc/sepc bit-1
  writable at IALIGN=16, misa read-only at the declared value (0x800000000014112D — a
  stated laboratory WARL choice), satp MODE restricted to Bare|Sv39, menvcfg.STCE,
  mcounteren/scounteren CY/TM/IR with Zihpm read-only 0, the counters with rate/progress
  deferred to .5/.9, the FP CSRs present-with-reset with behaviour at .7. Resets: §2.1.4's
  architectural ones cited; every UNSPECIFIED reset is a stated laboratory value. gen_state
  emits both profiles — rv64i byte-identical, rv64gc to a scratch out (40198 bytes,
  rustc-clean) with per-field resets composed and cross-checked against the csr-level value
  (fired RED naturally: mstatus's UXL/SXL composite caught a hand-computed wrong value).
  Gate gaps closed: PROFILE-CONSISTENCY's csr-set cross-check (+3 arms, 44 total) and
  EXTRACTION's reset leg now counts csrs and the mode (+3 arms, 9 total); STATE-GEN 17
  arms. `make gate` green (DERIVED-COUNTS 385→395). Next: slice (c2).

- `2026-10-03`: `.2` slice (b) done (`SEMULITH-P4-0005`) — the semantics language learns
  privilege. Eight operators joined the schema (32→39 forms), each with its meaning tied to
  the pinned chapters: `(field X)` raw operand-field value; `(inst)` the instruction word;
  `(mode)` current privilege; `(csr-state a)` the machine's own state read; `(csr-read a)`
  / `(csr-write a v)` the architectural CSR access under a UNIFORM permission model
  (address mode bits + read-only bits, counter-enables, TM/STCE, TVM — every CSR
  instruction gets it once); `(trap-deliver c t)` delegation + the xPIE/xIE/xPP stack +
  xepc/xcause/xtval + pc←xtvec; `(xret x)` the §2.1.3.2 stack pop incl. MPRV clear. The
  language gained its READS-AND-WRITES contract (register reads see the pre-instruction
  register file — the csrrw swap is exact for rd==rs1; no RV64I rule changes meaning). The
  three sem files landed: zicsr (the read/write side-effect disciplines; ECALL/EBREAK
  REFINED by declaration — MODEL-COMPOSE.6's anticipated case — cause 8/9/11 by mode),
  zicntr (the pseudo-semantics mechanism, measured: specialization by NAME, no refines
  possible or needed), system (mret/sret legality per mode + the TSR gate; wfi a stated
  NOP-when-legal with the spec's latitudes resolved for trapping, laboratory authority;
  sfence.vma's invalidation a stated NOP — Sv39 is `.3`'s). The WARL seam is recorded:
  csr-write legalizes under slice (c)'s declared tables, applied at slice-(d) lowering.
  Measured in execution, fixed at root: the corpus gate's COMPOSE leg carried slice (a)'s
  dropped-`(extensions …)`-form bug (a silent override in the second form was invisible —
  the new arm proven RED pre-fix); check_citations was hard-coded to rv64i.sem.sexp (the
  new `--corpus` mode binds by declared pins: 52/52 ×3, 8/8, 3/3, 4/4 resolved); the
  mstatus field positions are figure-only in the spec, so `encoding.h` + `causes.csv`
  joined the rv64gc ledger. rv64i.sem.sexp untouched; `make gate` green. Next: slice (c) —
  the state schema, gen_state and the 33-CSR document.

- `2026-10-03`: `.2` slice (a) done (`SEMULITH-P4-0004`) — fragments + assembler whitelist +
  IALIGN data. The upstream census measured what the brief delegated: Zicsr's six
  instructions are real rows in `rv_zicsr`; mret/wfi live in `rv_system`, sret/sfence.vma in
  `rv_s`; and Zicntr's rdcycle/rdtime/rdinstret exist ONLY as `$pseudo_op` rows of csrrs —
  Zicntr adds no encodings. Upstream also moved every table from the repository root to
  `extensions/` (the moved rv_i/rv64_i/rv_m/rv64_m hash byte-identical to the rv64i pins);
  the fetch route now maps table names under `extensions/` and both profiles'
  `--verify-only` stay green. The re-pin landed as `profiles/rv64gc-lab-v0/references.sexp`
  (rv64i's ledger untouched; the pinned arg_lut.csv already carried csr/zimm5, so it needed
  no re-pin). The fragment layer gained the `(pseudo …)` construct — assembler spellings
  decided under a specialization rule, never encodings — and `zicntr.sexp` declares its real
  dependency (`requires` rv64i AND zicsr, the rows' own `rv_zicsr::csrrs`). Measured in
  execution and fixed at root: `resolve_composition` silently dropped every `(extensions …)`
  form after the first (latent since MODEL-COMPOSE.2), the disjointness checker's
  `DUPLICATE NAME(S)` was advisory-only, and the assembler's label pass ate csr names.
  IALIGN is profile data now (rv64i 32, rv64gc 16 — the line-486 assumption retired).
  rv64i.sexp/m.sexp re-derive byte-identical; all 13 new forms assemble and round-trip
  through spike-dasm exactly; `make gate` green. The unit stays on the
  `profile-resolution` route — the flip remains slice (h)'s atomic commit. Next: slice (b) —
  the semantics-language operators + the new sem files.

- `2026-10-03`: the `.2` design brief recorded (`SEMULITH-P4-0003`). The measured
  pre-conditions: the route flip is atomic by construction (a partial flip is RED by
  name in EXTRACTION/EXERCISE-COVERAGE/INTERACTION-MATRIX); the model has no privilege
  or CSR concept anywhere executable; the three GEN generators are single-profile by
  refusal; the assembler lacks the csr operand field and hard-codes IALIGN=32; no
  privileged matched experiment has ever run (Spike's Sv57/CLINT platform conflicts
  with this profile, worse than rv64i). The design: `.2` owns xRET + synchronous-trap
  entry/exit + the CSR permission matrix + delegation + mode-dependent decode legality
  (WFI/SFENCE.VMA/counters/STCE), with the boundary lines to `.3`/`.5`/`.8` drawn
  explicitly; the flip composes base rv64i + Zicsr + privileged-system + Zicntr
  fragments with slots declared partial; base-corpus inheritance is mirror-derivation
  executed on the rv64gc engine; the mode-matrix guests observe through the ISA
  (x0..x31 expectations unchanged); the generators parameterize behind the schema
  layer with rv64i's surfaces re-derived byte-identical; Sail privileged matching
  attempted, Spike recorded platform-conflicted. The tree's privilege-revision open
  question closes (D-PRIV-REVISION). Eight execution checkpoints named.

- `2026-09-13`: Created from `ROADMAP.md` §P4 and task card `T011` by `SEMULITH-TREES.2`.
- `2026-09-14`: received a routed finding from `P0-PROFILE.7` — Sail and Spike share Berkeley
  SoftFloat, 184 of 199 overlapping files byte-identical. `.7`'s ancestry inventory now starts
  from a measurement instead of a suspicion, and its "independent numeric fixtures" requirement
  has a concrete constraint to satisfy.
- `2026-10-02`: the `.1` design brief recorded (`SEMULITH-P4-0001`) and the tree
  activated. The measured pre-condition that shapes everything: the pinned v20260120
  snapshot CARRIES the privileged chapters (`priv/` — 24 pages, digest-pinned), so the
  privileged evidence base is citable today and the category census's "absent" phrasing
  is superseded. The selection decided: `rv64gc-lab-v0` — RV64I + M/A/F/D/C/Zicsr/
  Zifencei, M/S/U, Sv39, harts 1, IALIGN 16 with C; FP in the profile with its
  execution evidence gated on `.7`'s backend qualification; SBI 2.0 / psABI 1.0 (both
  already cached) as the firmware/toolchain contracts; the snapshot's `priv/` pages the
  citation authority, the PDFs reference-only. The output: the unit's profile.sexp +
  sources.sexp + DOSSIER.md, unregistered (the `.2`/`.11` precedent); catalogues arrive
  with the evidence leaves.
- `2026-10-03`: `.1` done (`SEMULITH-P4-0002`) — the profile resolved: **rv64gc-lab-v0**.
  Every element source-located against the pinned publication: RV64I + M/A/F/D/C +
  Zicntr + Zicsr + Zifencei (+ Sstc privileged), M/S/U, Sv39, IALIGN 16 / ILEN 32,
  harts 1, the 33-CSR committed minimum, LP64D, SBI 2.0 for the P6 route. The pinned
  snapshot's privileged chapters measured present (24 pages — the 2026-09-27 census's
  "absent" phrasing superseded); the closure measured (D⇒F, F⇒Zicsr, C⇒Zca+Zcd at
  RV64, G = IMAFDZicsr_Zifencei); FP declared with its evidence gated on `.7`. The
  machinery gained the `profile-resolution` vehicle route by declaration (EXTRACTION /
  EXERCISE-COVERAGE / INTERACTION-MATRIX honor it, contradiction = RED; self-tests
  11/21/15); check_citations learned subdirectory `file` fields and named non-snapshot
  skips; gen_platform's ISA derivation fixed to the canonical order. The unit is
  deliberately unregistered — registration day is a later leaf. Frontier: `.2` —
  privilege and mode transitions.

`P4-SYSTEM`'s Verification Log rows for leaf `.6` (closed `2026-10-05`), split out
verbatim on `2026-10-05` at the live file's nineteenth ceiling firing (the `.7` design
brief landing) — the closed-leaf log-row lifecycle established at the fourteenth:

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-05` | `.6` slice (c) + LEAF | the override measured first (materialized fresh from the tracked .sexp — unmoved since bfa6aaa; validate-config rc=0; Zifencei supported true, NO change needed); sail's FENCEI measured in source (encdec fields VARIABLES — decoded-not-fixed, the shall-ignore sentence in its own comment; execute a nop for the memory model); the 6 ELFs at exactly 0x8000_0000 (the selfmod pair's auipc-derived patch targets entry-relative, measured); the experiment (**6 AGREE of 6** — it-fencei 3, min-fencei 1, fencei-reserved 2, fencei-selfmod 8, fault-selfmod 7, dir-selfmod-fence 8 = 29 steps' change-observations exact, the patched fetch reading 7 on both sides; ZERO non-AGREE cells); the verdict-neutrality measurement (the wider corpus's expectations unmoved since their verdicts — git log on a-amo-aqrl → 495b4b8; the bind touched only the fencei surface); the census re-answer (the fetch-cache candidate's why re-written in place — Zifencei declared AND bound, the re-read stays laboratory policy, FENCE.I's nop the sanctioned implementation; the consequence line unchanged; gen_state re-derived, build rc=0; the brief's clause-location phrasing measured imprecise and recorded — the clause is rv64i's text, referenced); references.sexp's fifth experiment (difference-free re-measured: 0 difference records); the acceptance box (WITH: fencei-selfmod on both engines; WITHOUT: fault-selfmod with D-CODE-VISIBILITY; the staleness half the declared latitude with intro.html's sentence); `cargo test -p semulith-verify run_rv64gc` 4/4 (101/101); `make check` rc=0, `make gate` all green (DERIVED-COUNTS 430 unchanged), RECORD-SCHEMA 20 files, PROFILE-CONSISTENCY 5, smoke-bench 53 arms, bench wasm, both books | the LEAF CLOSES: the fence.i contract is validated on both engines — newly written code is executable by construction, the synchronization executes legally as the declared nop, the acceptance pair stands on both sides, and the staleness half is answered as the declared latitude; frontier → `.7` |
| `2026-10-05` | `.6` slice (b) — THE BIND | the pre-bind census (the slot at encoding.sexp:18, 0 fence.i rows, the fencei guests trapping cause 2); slot→extension; the census dual edit 87→88 (the .4 lesson's four places); definition_rv64gc.rs regenerated (fence.i over Sem::Nop); REQ-GC-FENCEI + OB-GC-FENCEI, no new D-*; the fencei re-derivations (it-fencei 2→3 steps with x2 written — the pre-commit fulfilled; min-fencei one retiring nop); fencei-reserved (0x0011118F ignored) + fencei-selfmod (the acceptance pair's WITH member; fault-selfmod stands WITHOUT); the decision-3 corrections as recorded mirror re-derivations (the governor measured the .s edits as drift first); the flip 88==88; `cargo test -p semulith-verify run_rv64gc` 4/4 (101/101); the identity proof (98/99 byte-identical, it-fencei the designed exception, worktree removed); the matrix (28 cells resolve); EXERCISE-COVERAGE 88/88; GUEST-GEN 16/16; `make check` rc=0, `make gate` all green (DERIVED-COUNTS 430 unchanged) | THE BIND landed: the unit composes `riscv/zifencei` — fence.i legal over the existing nop, 88 forms, 101 guests green, 98 pre-bind byte-identical |
| `2026-10-05` | `.6` slice (a) | the pre-slice census (rv_zifencei pinned nowhere; 6 FRAGMENTS entries; the slot at encoding.sexp:18); the tracked-route fetch (73 bytes, one row, be2d8f72…, fresh re-fetch byte-identical); the recorded deviation (decision 1's "no assembler shapes" FALSE for the bare spelling — the row's operand list refused it; the named zero-operand special case; no Sem variant / no generator change TRUE — mask 0x0000707f over Sem::Nop, rustc rc=0 ×2); the fragment (owns NO fields, requires rv64i, funct3=1; 6 others byte-identical); zifencei.sem.sexp (the three sentences + both latitudes re-located; pair 1/1, both composes, citations RVI-ZIFENCEI §4.1 ×1 offline, corpus 6/8); the disjointness trials (53 and 85+3 COMPOSE; self-test 12/12); the probe (bare+full spellings, the shall-ignore word, 3 named REDs, spike-dasm exact); both profiles 87==87/52==52 with the named exclusion; 99 guests byte-identical; `make check` rc=0, `make gate` all green (DERIVED-COUNTS 430 unchanged) | slice (a) landed: the pin, the fragment, the sem file and the assembler acceptance — the slot stays declared, the census stays 87, no corpus, no Rust |


`P4-SYSTEM`'s Changelog entries for leaf `.6` (closed `2026-10-05`):
slice (a)'s entry split out verbatim on `2026-10-06` at the live file's
twenty-second ceiling firing (the `.7` slice-(a) landing), slices (c) and (b)
at the twenty-fourth (the `.7` slice-(b) landing) — the closed-leaf lifecycle
the `.1`/`.2` entries established at the twentieth:

- `2026-10-05`: `.6` slice (c) done and the LEAF CLOSES (`SEMULITH-P4-0037`) — the
  Sail matched experiment for the fence.i surface, scoped to decision 2's designed
  outcome and measured, not assumed: the override is measured first (materialized
  fresh from the tracked unit — unmoved since bfa6aaa; validate-config rc=0;
  Zifencei supported true; NO change needed), sail's FENCEI measured in source
  (its encdec carries the fields as VARIABLES — decoded-not-fixed, the
  shall-ignore sentence quoted in its own comment; execute is a nop for the
  memory model). Against the matched configuration, **6 AGREE of 6**: it-fencei
  3, min-fencei 1, fencei-reserved 2, fencei-selfmod 8, fault-selfmod 7,
  dir-selfmod-fence 8 — 29 steps' change-observations exact, the patched fetch
  reading the new value on both engines; ZERO non-AGREE cells. Verdict-neutrality
  measured: the wider corpus's expectations are unmoved since their verdicts
  (git log → 495b4b8; the bind touched only the fencei surface). The fetch-cache
  census candidate is re-answered in place (decision 6 — Zifencei declared AND
  bound; the re-read stays laboratory policy; FENCE.I's nop is the sanctioned
  implementation; the consequence line unchanged; gen_state re-derived, build
  rc=0; the brief's clause-location phrasing measured imprecise and recorded —
  the clause is rv64i's text, referenced). references.sexp records the fifth
  experiment (difference-free re-measured: 0 difference records). **The LEAF
  ACCEPTANCE**: rewrite-code fixtures with and without the architectural
  synchronization, measured on BOTH engines — WITH: fencei-selfmod's fence.i
  retires between the store and the fetch, the patched word reading 7 on both;
  WITHOUT: fault-selfmod's patch visible with no synchronization,
  D-CODE-VISIBILITY named (the laboratory's declared legal subset); the
  staleness half answered as the declared latitude (intro.html's implicit-reads
  sentence; the caching-hart model rejected at the brief). `make check` rc=0,
  `make gate` green (DERIVED-COUNTS 430 unchanged), RECORD-SCHEMA 20,
  PROFILE-CONSISTENCY 5, smoke-bench 53 arms, bench wasm, both books. Next:
  `.7` — floating-point backend qualification (the design brief first, starting
  from the leaf card's routed-in SoftFloat shared-ancestry measurement).

- `2026-10-05`: `.6` slice (b) done (`SEMULITH-P4-0036`) — **THE BIND**: the unit
  composes `riscv/zifencei`, and fence.i is legal in the tracked engine. The
  slot becomes the extension (the header restated); the census dual edit 87→88
  lands in all four places (the zifencei_fencei family, RVI-ZIFENCEI §4.1);
  definition_rv64gc.rs regenerates with fence.i over the existing Sem::Nop;
  REQ-GC-FENCEI + OB-GC-FENCEI with no new D-* (the wfi-nop precedent).
  it-fencei/min-fencei re-derive to the legal fence.i — the slice-(g) pre-commit
  FULFILLED (it-fencei grows 2→3 steps, the marker committing as on both
  references; min-fencei one retiring nop, its demo trace byte-identical
  anyway — the pre-bind delivery wrote nothing at mtvec=0). fencei-reserved
  exercises the shall-ignore decode end-to-end; fencei-selfmod is the
  acceptance pair's WITH member (the patched fetch reading 7); fault-selfmod
  stands WITHOUT. The decision-3 comment corrections land as RECORDED mirror
  re-derivations — the governor measured my direct .s edits as drift (the
  mirror holds .s byte-identical ALWAYS). The fetch leg's exclusion flipped on
  its own (88==88, rv64i 52==52); the corpus reads **101/101**; the identity
  proof holds 98/99 (it-fencei the designed exception); the matrix resolves 28
  cells; EXERCISE-COVERAGE 88/88; GUEST-GEN 16/16. `make check` rc=0, `make
  gate` green (DERIVED-COUNTS 430 unchanged). Next: slice (c) — the Sail
  matched experiment + the census re-answer + the reports and the book + the
  leaf acceptance.

- `2026-10-05`: `.6` slice (a) done (`SEMULITH-P4-0035`) — the `rv_zifencei`
  re-pin through the tracked `extensions/` route (73 bytes, one row, sha256
  be2d8f72…; a fresh re-fetch byte-identical), recorded in references.sexp with
  the supplies amendment; the fetch leg's named exclusion (the M/A pattern —
  pinned for the fragment, not the scope, until slice (b)'s bind flips it):
  both profiles' `--verify-only` green, 87==87 and 52==52. The
  FRAGMENTS entry generates `zifencei.sexp` (owns NO fields — imm12/rs1/rd are
  the base's; requires rv64i; funct3=1; the six others byte-identical) and
  `zifencei.sem.sexp` lands hand-written with `(effect (nop))` — the three
  normative sentences, the coherent/uncached-RAM latitude and the shall-ignore
  rule re-located in the pinned chapter (Version 2.0; citations offline, corpus
  6 files / 8 resolutions). One brief claim measured FALSE as written: decision
  1's "no assembler shapes" — the row's operand list refused the
  standard-software spelling, so the zero-operand acceptance lands as a named,
  cited special case (the A-suffix precedent's shape): bare `fence.i` →
  0x0000100f, the full spelling unchanged, 3 named REDs, spike-dasm exact incl.
  the shall-ignore word 0x0011118f. The OTHER no-change claims measured TRUE:
  no Sem variant, no generator change — gen_definition emits mask 0x0000707f
  (the shall-ignore decode) over the existing Sem::Nop, rustc rc=0 over both
  trial compositions; check_encoding_disjoint COMPOSEs base+zifencei (53) and
  the profile's set +zifencei (85+3); all 99 guests re-assemble byte-identical. The slot STAYS
  declared, the census STAYS 87, no corpus, no Rust. `make check` rc=0, `make
  gate` green (DERIVED-COUNTS 430 unchanged). Next: slice (b) — THE BIND:
  slot→extension, 87→88, the re-derived fencei guests, the reserved-fields
  probe, the acceptance pair, the matrix cells, the identity proof.
