# CHANGELOG shard — SEMULITH-P4-0028 … SEMULITH-P4-0024

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0028 (leaf P4-SYSTEM.4, slice f) — the Sail matched experiment (11 AGREE + 1 named of 12); the leaf CLOSES

- The matched experiment runs the 12-guest atomics corpus under Sail 0.14 with the
  tracked override — validated unchanged (`--validate-config` rc=0; A supported
  true, the region's AMOCASQ / RsrvEventual / `(amo|lrsc AccessFault)` all
  re-measured present, the brief's pre-condition 7 confirmed by measurement, not
  assumed). The 12 ELFs are built at exactly 0x8000_0000 by the tracked assembler
  (a .word-only lowering + a PHDRS link — clang never parses the corpus's operand
  syntax), and the comparison rides the corpus's own change-observation rule
  against the EVD-05 expectations: **11 AGREE** (every LR/SC cell, the AMOs at
  both widths with old-value rd sign-extended, the suffix cells, the translated
  AMO faulting 15 never 13, the alias cell, the first-SC loop — Sail's SC proves
  deterministic under RsrvEventual, exactly the declared never-spurious policy).
- **1 NAMED DIVERGENCE** (the `.2` mm-wfi naming precedent): `a-lrsc-mustfail`'s
  width cells — Sail's platform reservation matches a `.D` SC after a `.W` LR on
  the physical ADDRESS alone (the externs take physaddrbits, no width), while the
  laboratory's declared width-equal policy fails with code 1. Both are legal
  under §12.1.2's latitude; the laboratory's is the declared, more-discriminating
  rule (state.sexp, decision 3). The trace is quoted in the leaf.
- The experiment also caught a REAL defect: the bind-day uniform-cause-7
  misaligned policy is **illegal for LR** — Sail delivered the LOAD access-fault
  cause 5 for a misaligned LR, and RVP-MACHINE's exception table says why ("load
  and load-reserved instructions generate load exceptions"). The policy is now
  kind-matched (LR → 5, SC/AMO → 7) in the engine arm, the schema contract, the
  state.sexp policy text, and the D-ATOMIC-MISALIGN decision (amended with its
  note; the REQ/OB mirrors verbatim-identical). Exactly ONE guest expectation was
  re-derived (`a-lrsc-fault.expected.sexp`); the other 87 guests and the override
  are untouched.
- The LEAF CLOSES: single-core reservation behaviour is validated — atomic
  widths, reservation semantics, failed conditional stores, overlap and
  external-write cases — against EVD-05 expectations AND the differential; the
  multicore memory model stays `MC-MULTICORE`'s (RVWMO §17.1.1–§17.1.1.4), never
  smuggled. `make check` rc=0 (8 groups), `make gate` all green (DERIVED-COUNTS
  429 unchanged). `references.sexp` records the third experiment in
  matched_scope. Next: `P4-SYSTEM.5` — interrupts, counters and wait, its
  design brief first.

## SEMULITH-P4-0027 (leaf P4-SYSTEM.4, slice e) — THE BIND: the unit composes `riscv/a` (87 forms, 88 guests, the arms tracked)

- One green commit makes the A extension real in the tracked unit, the `.2` flip's
  discipline: `encoding.sexp`'s `(slot (id a) …)` becomes `(extensions "riscv/a")`;
  the census dual edit grows 65 → 87 (schema/profile.sexp + `_SCOPE_LISTS` + the
  scope block + PROFILE-CONSISTENCY's PARTS family — the pinned RVWMO Tables 6/7
  enumeration); `REQ-GC-ATOMICS` names the 22 forms and the reservation model, the
  deterministic SC policy and the misaligned-cause-7 choice land as laboratory
  decisions with verbatim REQ/OB mirrors and CHK pairs (RECORD-SCHEMA 20 files ok).
- `definition_rv64gc.rs` regenerates: the 22 forms, the `LoadReserved`/
  `StoreConditional`/`Amo` variants, the era comment 40→43 forms. The evaluator
  arms port from the scratch proof — the tracked `exec_rv64gc.rs` is byte-identical
  to the slice-(c)-proven copy. The 12 corpus guests land tracked
  (`guests_rv64gc.rs` 88), the matrix cells resolve (28, no orphan).
- Every tally green: `cargo test -p semulith-verify run_rv64gc` 4/4 (**88/88** —
  per-step writes, never_written, determinism, declared fetch counts); the
  slice-(c) 16/16 proof and the 88/88 corpus re-run against the TRACKED build;
  the fetch leg's exclusion flips on its own — **87 == 87** for rv64gc, 52 == 52
  for rv64i; EXTRACTION 5 units, EXERCISE-COVERAGE (87/87, 52/52),
  UNIT-COMPOSITION 3 (partial declared), INTERACTION-MATRIX 5,
  PROFILE-CONSISTENCY 5 dossiers. **BARE-IDENTITY: 3,468 == 3,468 trace lines,
  `cmp` clean** — all 76 pre-bind guests byte-identical against the parent
  engine (worktree, both CLIs); the 22 new forms are additive and the corpus
  never noticed.
- One defect found and fixed at root: the definition emission was not
  rustfmt-stable at five fragments (rustfmt lays a >79-char array out vertically —
  measured: 79 inline-clean, 90 broken); the emission now decides the layout by
  construction and `cargo fmt --check` is clean.
- `make check` rc=0 (fmt + clippy `-D warnings` + 8 groups), `make gate` all green
  (DERIVED-COUNTS 429 unchanged), smoke-bench 53 arms, bench wasm, both books.
  Next: slice (f) — the Sail matched experiment + the reports and the book + the
  leaf acceptance.

## SEMULITH-P4-0026 (leaf P4-SYSTEM.4, slice d) — the staged atomics corpus: 12 guests, EVD-05 expectations, the matrix + coverage rehearsals

- Twelve staged guests (`target/p4-system-4/`, untracked — the `.2` slices-(f)/(g)
  discipline) cover the brief's families: the nine AMOs × `.W`/`.D` with rd the old
  value sign-extended at the 0x8000_0005 edge and the min/max signed-vs-unsigned
  disagreement cells; every aq/rl combination executed identically at one hart;
  rd=rs1=rs2 / rd=rs2 / rd=rs1 overlaps; the LR/SC pairs at both widths; every
  one-hart must-fail (different address, an intervening SC clearing, LR-replaces,
  width mismatch both ways, SC-without-LR — each with its no-memory-write read-back)
  plus recovery; a constrained loop terminating on its first SC; misaligned atomics
  taking cause 7 before translation; the 77-step `a-amo-sv39` — an AMO on an
  unreadable page faulting 15 NEVER 13, W=0 → 15, R∧W succeeding, the alias cell
  (the reservation is PHYSICAL-keyed), a trapped SC trapping AGAIN (survival
  proven), misaligned-before-translation under Sv39; and three reserved encodings
  delivered as cause 2 with xtval the word.
- Expectations are EVD-05 specification-derived: a spec-side model
  (`tools/derive_expectations.py`) written from the pinned chapters and the
  declared deterministic policy (state.sexp's reservation candidate) — never
  engine output — emits each `.expected.sexp` (schema-valid ×12); every word is
  assembled by the TRACKED assembler's A machinery (gen_guests ×12). The scratch
  runner mirrors run_rv64gc's comparison semantics and the corpus executes
  **12 PASS / 0 FAIL** through the slice-(c) engine, deterministic on re-run.
  Execution caught FOUR authoring defects — the tool's unapplied register writes,
  the unmodeled same-value-write comparison rule (the `.3` "x8-already-zero"
  rule), a "reserved" funct5 0x02 that is LR's own (it decoded and EXECUTED), and
  the sv39 data PA colliding with the root page table — each fixed by
  re-derivation, never fitted.
- The matrix rehearsal: `check_interaction_matrix.py target/p4-system-4/unit` —
  28 cells declared, every disposition resolves, the new guests riding the seven
  EXISTING axes (decision 9); the three RED legs fired by name on a scratch copy
  (ORPHAN GUEST, OMITTED CELL, UNKNOWN DIFFERENCE). The coverage rehearsal reads
  22/22 A forms exercised — the bind's 87-form denominator (65 measured at `.2`
  slice f + these 22). Nothing tracked changed; `make gate` green (DERIVED-COUNTS
  429). Next: slice (e) — THE BIND: slot→extension, the 65→87 census dual edit,
  the requirement/obligation growth, the generated mirrors, this corpus tracked,
  the evaluator arms, the matrix cells — one green commit with the full gate
  suite.

## SEMULITH-P4-0025 (leaf P4-SYSTEM.4, slice c) — the reservation state, the SC policy as data, the AMO/LR/SC arms proven in scratch

- `crates/semulith-core/src/reservation.rs` (NEW, additive — the
  `translation.rs`/TLB precedent): the reservation is (physical address, width,
  valid) of the most recent LR — the minimal conformant set (decision 2),
  physical-keyed. Invalidation is exactly the spec's one-hart set: any LR replaces;
  any COMPLETED SC clears; a trap clears nothing — measured on Sail 0.14 before
  choosing the clear sites (`zalrsc_insts.sail:71-79`: `cancel_reservation` fires
  on the completed path, the `Err(e)` trap path cancels nothing). The deterministic
  SC policy rides as DATA in `state.sexp` beside the census candidate (decision 3:
  succeeds iff valid ∧ PA equal ∧ width equal; failure code 1; never spurious), and
  `gen_state`'s census-candidate gate is GENERALISED: any hart state the module
  carries must be census-declared (a RED arm, STATE-GEN 26→27). The state module
  regenerates with the field/reset/accessor; rv64i's state is byte-identical.
- The evaluator arms exist — in scratch, the `.2` slice-d discipline: the tracked
  `exec_rv64gc.rs` cannot gain them until the bind (its `Sem` match is exhaustive),
  so `target/p4-system-4/` carries the rv64gc+A definition module and the tracked
  evaluator + the three arms. The proof passes **16/16**: the LR/SC pair; every
  must-fail cell (address mismatch, width mismatch both ways, the intervening-SC
  clear, LR-replaces both ways, a failed SC issuing NO memory operations); the
  trapped SC keeping its reservation; misaligned atomics taking cause 7 before
  translation (an unmapped VA included); the AMO nine × `.W`/`.D` with rd the old
  value sign-extended and the load-then-store boundary pair asserted per op; the
  rd=rs1=rs2 / rd=rs2 overlaps; the translated AMO on an unreadable Sv39 page
  faulting 15 never 13 (a new `AccessKind::Atomic` judges R∧W under store/AMO
  causes); the alias cell (the reservation is PHYSICAL-keyed); the constrained loop
  succeeding on its first SC; aq/rl ×4 identical; cold-reset determinism. The proof
  first caught three test-design defects of mine — the engine was right each time.
- `make check` rc=0 (fmt + clippy `-D warnings` + 8 groups, 109 core tests incl. the
  reservation module's 7 and the translation suite's 25→26), `make gate` green
  (DERIVED-COUNTS 428→429). The slot stays declared, the census 65, the tracked
  evaluator untouched; the bind's port mapping is recorded in the leaf. The
  checklist archive SPLIT at its own ceiling: `archive/P4-SYSTEM.md` (part 1)
  keeps the earlier sections, new `archive/P4-SYSTEM-2.md` (part 2) takes every
  move onward. Next: slice (d) — the staged corpus + expectations + the matrix
  rehearsal.

## SEMULITH-P4-0024 (leaf P4-SYSTEM.4, slice b) — the reservation contract, the three atomic operators, a.sem.sexp, the conditional lowering

- `schema/semantics.sexp` grows 40→43 forms. A RESERVATION contract block states the
  one-hart rules once, citing §12.1.2/§12.1.3 and the brief's decisions 2–4 and 6:
  the minimal exact reservation (physical address, width, valid of the most recent
  LR); any LR replaces, any SC clears, traps do NOT invalidate; the external
  invalidation event is P4-SYSTEM.9's contract vocabulary; misaligned atomics take
  the access-fault cause 7, reference-matched to the pinned override's declared
  PMAs. The operators: `load-reserved` (load-rules translation, sets/replaces the
  reservation), `store-conditional` (yields the rd code — 0 on success, 1 on
  failure, NEVER spurious under the declared deterministic policy, decision 3;
  clears the reservation either way), `amo` (the closed nine by funct5 encoding;
  ONE store/AMO-rules translation — never a load page fault; reads the old value,
  computes at width, writes, yields the old value; the boundary shape a load
  followed by a store, a `Request::Atomic` variant recorded as rejected, decision 5).
- `definitions/riscv/a.sem.sexp` is hand-written from the pinned A chapter: all 22
  forms, every rule locator-cited — `check_semantics.py` 22/22, the trial
  compositions (`--compose` base+A and the five-fragment set) with every override
  declared, and the citations resolving offline against rv64gc's pins (RVI-A
  §12.1.2 ×4, §12.1.4 ×18).
- `scripts/gen_definition.py` lowers the new operators, with two measured design
  points: the AMO's operation is the funct5 LITERAL (a bare symbol is refused as a
  phantom operand — measured rc=1), and the closed Zaamo set is RE-DERIVED from the
  composed encodings' own funct5 fixed bits, an out-of-set op refused by name; and
  the `Sem` variants emit exactly when the composition composes `riscv/a` (the
  evaluator's exhaustive match is the `.2` slice-d wall), so the tracked modules
  regenerate HASH-ONLY (the OWN-03 generator pin, 0 non-hash diff lines) while the
  scratch composition — base+Zicsr+Zicntr+system+A, untracked — lowers and compiles
  standalone (rustc rc=0), the lowered lr.w/amoadd.w trees inspected. Three RED
  probes name the guards; the permanent arms record them (check_semantics 15→17,
  DEF-GEN 17→23).
- No Rust edited — the evaluator arms are slice (c)'s. The slot stays declared, the
  census 65. `make check` rc=0 (8 test groups), `make gate` green (DERIVED-COUNTS
  424→428 textual shell arms). Next: slice (c) — the reservation state (the
  census-candidate gate generalised, the emit, the module) + the deterministic
  policy as data + the engine's AMO/LR/SC arms proven in scratch.

