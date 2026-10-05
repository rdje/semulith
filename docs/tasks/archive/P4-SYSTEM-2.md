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

