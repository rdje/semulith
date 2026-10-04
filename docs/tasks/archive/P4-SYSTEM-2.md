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

