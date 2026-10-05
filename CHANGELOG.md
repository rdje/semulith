# CHANGELOG.md

## SEMULITH-P4-0033 (leaf P4-SYSTEM.5, slice d) — the Sail matched attempt; the LEAF CLOSES

- The matched attempt, scoped to what is matchable (decision 9). The override is
  measured first: materialized fresh from the tracked unit (unchanged since
  bfa6aaa), validate-config rc=0, NO change needed — and verdict-neutral (the
  `.4` corpus re-run under it reproduces 11 AGREE + 1 NAMED of 12 exactly). The
  13 ELFs build at exactly 0x8000_0000 (.word-only + PHDRS, the tracked
  assembler owning the bytes).
- Against the matched configuration the software-posted-bit cells match exactly:
  **6 AGREE of 12** (i-accept 36, i-deleg 60, i-enable 21, i-nest 31, i-vector
  53, w-sw 17 — 218 steps of change-observations). Sail numbers the
  interrupt-delivery step and prints no row (i-accept's trace jumps [9]→[11]) —
  the same convention the laboratory declares, the `.3` fetch-fault shape.
- The **6 NAMED divergences are all platform-shaped, never semantic**: Sail's
  timer block gates on `plat_have_clint`, so STIP never sets without a CLINT
  (i-prio step 24: sail x13=2 vs 34; i-timer step 3: sail x7=0 vs 32); Sail's WFI
  is a nop under the matched platform, so the real halt has no counterpart
  (w-deleg 12, w-notrap 6, w-timer 11, mm-wfi 9 — 'sail printed a row for the
  `<halted>` step'); and mm-wfi's TW cell is the `.2` named gap freshly measured
  with the isolated probe — DIVERGE under the matched config (Sail never judges
  TW: the judgment lives only in the wait-exit path the nop never reaches),
  AGREE 30/30 under the wfi-wait variant with the delivered trap identical
  (cause 2, mepc = the wfi's pc, xtval = the wfi's word).
- The matrix invocation resolves 28 cells with the three RED legs fired by name
  (ORPHAN GUEST / OMITTED CELL / UNKNOWN DIFFERENCE); references.sexp records
  the fourth experiment. **The LEAF ACCEPTANCE is w-timer's own run**: three
  boundaries with no register observation (the two `<halted>` steps and the
  delivery), the handler's first read rdinstret = 11 — nothing retired across
  the halt — then the timer trap with mcause = Interrupt|5 and mepc = the wfi's
  pc + 4. The timer wake occurred **without CPU retirement**. `make check`
  rc=0, `make gate` green (DERIVED-COUNTS 430), smoke-bench 53 arms, bench wasm,
  both books. Frontier → `.6` (instruction visibility and fence semantics).

## SEMULITH-P4-0032 (leaf P4-SYSTEM.5, slice c) — the halted state, WFI's real wake, the `<halted>` vocabulary, the wake corpus

- The hart gains its wait state (decision 4): one ACTIVE/WAITING bit (Sail's
  `HART_WAITING` precedent), cold-ACTIVE at reset, engine-owned hart state on the
  TLB/reservation discipline — the state document's SEM-08 census declares the
  `hart wait state (ACTIVE/WAITING)` candidate and gen_state carries the bit (the
  RED arm 27→28). A legal WFI ENTERS the wait (the nop latitude recorded-not-taken);
  a halted step retires nothing, issues no fetch, and ticks the domain once; the
  step's head evaluates the wake — exactly `mip & mie != 0`, regardless of the
  global enables and of mideleg (RVP-MACHINE §2.1.3.3's musts, measured verbatim).
  On resume the taken-rule decides: trap with xepc = the WFI's pc + 4 (the
  section's own rule, which the generic between-instructions delivery computes
  for free) or pc + 4 continuation.
- The wake corpus (EVD-05, derived before any engine run): **w-timer** — THE
  acceptance cell: the timer's arrival during the halt wakes the hart and the trap
  is taken, and the handler's rdinstret reads 11 at its first step — the wake
  occurred **without CPU retirement**; **w-notrap** — wake-without-trap and the
  spec's idle-loop idiom (two halts, pc + 4 each); **w-deleg** — a delegated STI
  wakes an M-mode hart anyway ("even if it has been delegated"), no trap fires
  until un-delegated; **w-sw** — the software-posted SSIP/SEIP sources waking with
  the globals off. mm-wfi re-derives (decision 10): its legal cells halt with
  arranged timer wakes (the S cell's source delegated), the TW=1 and U trap cells
  measured unchanged. The expectations vocabulary gains the `<halted>` pseudo-step
  (decision 6 — empty writes, fetches 0). The corpus reads **99/99**; the other
  94 pre-slice guests are byte-identical (only mm-wfi contains wfi — the census).
- The matrix carries the wake family (28 cells resolve). `make check` rc=0,
  `make gate` green (DERIVED-COUNTS 429 → 430 re-derived — the wait-state RED arm).

## SEMULITH-P4-0031 (leaf P4-SYSTEM.5, slice b) — the step-head pending evaluation; both vector modes; the 7-guest corpus

- Pending is evaluated at the head of **every step** (decision 3): the (a)(b)(c)
  taken-rule + the global rule + the delegation mask + the fixed priorities
  MEI>MSI>MTI>SEI>SSI>STI with the M-source bits read-only 0 (decision 5).
  Delivery honors BOTH xtvec.MODEs (Direct = BASE, Vectored = BASE + 4×cause)
  with xcause = cause|(1<<63), xepc the un-fetched pc, xtval 0 (declared
  UNSPECIFIED) and the xPIE/xIE/xPP stack — `interrupts.rs` (pending/deliver + 8
  module tests), wired before the fetch; delivery steps tick the domain and
  retire nothing.
- The acceptance corpus: 7 new i-* guests with EVD-05 expectations derived BEFORE
  any engine run — the taken-rule per mode (i-accept), the enable immediacy
  (i-enable), the timer across the ticking domain (i-timer), the delegation mask
  with an S round-trip (i-deleg), the fixed-priority drain (i-prio), both vector
  modes with the synchronous trap keeping BASE (i-vector), and a nested delivery's
  stack restoration (i-nest): 290 steps, 13 fetch-less deliveries. The corpus
  reads **95/95**; the interaction matrix carries the 7 (28 cells resolve).
- Execution caught the authoring model's own defects and re-derived, never
  fitted: the derivation tool's inverted trap-entry stack (the engine was right —
  every prior trap had fired with MIE=MPIE=0), i-accept's mtvec delta 8 bytes
  long, i-timer's stimecmp authored against a retired-count clock, i-vector's
  SEIP-clear through read-only sip. The pre-slice census (0 interrupt writes in
  all 88 guests) made the identity proof unconditional: 88/88 demo traces
  byte-identical against the e37e664 engine.

## SEMULITH-P4-0030 (leaf P4-SYSTEM.5, slice a) — the declared virtual-time domain; mm-counters re-derived by design

- The laboratory's virtual-time domain advances **one tick per step boundary,
  retired or halted** (authority laboratory, the Zicntr §6.1 rate latitude, the
  brief's pre-condition 8 answered: progress is a pure function of the step
  index, so determinism and EVD-05's exact values hold by construction). The
  storage shape is ONE domain: `mcycle` holds it, `time` views it read-only
  ("cycle count might represent a valid implementation of RDTIME", §6.1) — the
  duplicate `time` row retires (CSR storage 33 → 32), and the state document
  carries the declared rate and the count rule as DATA (the `.3` TLB-parameter
  precedent; the census's `.5` reopen answered for the counter-progress part).
  `minstret` counts GENUINELY: +1 per retired instruction, never for a
  trap-delivered, reserved-decoding or halted step.
- The moving counters exposed a **latent defect**: `csr_read`'s view path
  computed the exposed mask from a view's DECLARED fields, so a field-less view
  masked to ZERO — the counter views would have read 0 forever (the `.2` zeros
  passed only because nothing moved). Fixed at root: a view declaring no fields
  is a full-width shadow of its owner — the statements' own meaning ("a
  read-only shadow of mcycle").
- mm-counters — the ONLY counter-reading guest of all 88 (the full census
  re-measured: 7 reads; **0 mip/sip readers**, so the STIP-at-reset quirk and
  the ticking STIP are unobservable in today's corpus; mm-stimecmp reads
  stimecmp only, clean) — re-derives 5 cells BY DESIGN (time at executed step k
  is k: 0/1/2/25/51; the gating traps 13/39 untouched), from the pinned chapters
  + the declared rate, never fitted (the `.2` IALIGN-16 precedent).
- `timekeeping.rs` carries the advance and 7 module tests (the ticking STIP:
  reset 1, cleared above time, arriving on the third tick; cycle==time on both
  read paths; cold-reset determinism; the ACCESS gates untouched). The corpus
  reads **88/88**; the other 87 guests are **byte-identical** against the parent
  engine (4,892 == 4,892 trace lines, both CLIs, worktree removed) — time
  ticking is invisible outside the counter reads, and the CLI/demo surface is
  unchanged. `make check` rc=0 (fmt + clippy `-D warnings` + 8 groups), `make
  gate` all green (DERIVED-COUNTS 429 unchanged). Next: slice (b) — pending
  evaluation + interrupt-caused delivery (both vector modes) + the acceptance
  corpus.

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

## SEMULITH-P4-0023 (leaf P4-SYSTEM.4, slice a) — the rv_a/rv64_a re-pin, the a.sexp fragment, and the assembler's A machinery

- The A extension's encoding tables are pinned in the rv64gc ledger through the
  tracked `extensions/` fetch route (rv_a 858 B, rv64_a 885 B, sha256 recorded):
  Zaamo's nine AMOs and Zalrsc's load-reserved/store-conditional pair, each `.W`
  and `.D` — exactly the 22 forms the pinned RVWMO chapter's Tables 6/7 enumerate,
  so the pin corroborates rather than surprises. The pinned A chapter itself
  carries no encodings (its format diagrams are images). The pinned arg_lut.csv
  already carried the aq/rl positions, so it needed no re-pin.
- `definitions/riscv/a.sexp` is GENERATED by the extended `scripts/gen_fragments.py`
  (never hand-authored): the fragment owns the `aq` and `rl` operand fields,
  requires the rv64i base, and carries the pinned-table provenance. The existing
  five fragments re-derive byte-identical. Measured against the brief: its "aqrl
  field ownership" phrasing is imprecise — the tables carry no `aqrl` operand
  token; every row lists `aq rl` separately, and the pinned csv's combined `aqrl`
  (26..25) is where the mnemonic suffix's value lands.
- The assembler's A machinery: `aq`/`rl` whitelisted (positions read from the
  pinned arg_lut.csv at load time — derived, never typed); the `.aq`/`.rl`/`.aqrl`
  mnemonic suffix parsed as the aq/rl FIELD VALUES, with garbage suffixes
  (`lr.w.zz`) and suffixes on non-atomic forms (`add.aq`) refused by name; the
  `lr.w rd, (rs1)` / `sc.w rd, rs2, (rs1)` / `amoadd.w rd, rs2, (rs1)`
  parenthesized-address spelling accepted, every other shape refused by name.
  All 22 base forms × 4 suffix combinations assemble (88 words) and round-trip
  through spike-dasm exactly (lr's suffix words print plain — spike's own
  preference, the bits measured set). 11 RED refusals named.
- Measured in execution, fixed at root: the scope-vs-tables leg of
  `fetch_references.sh` never collected `rv64_*` tables (the rv64_a pin — and
  rv64_m before it — was invisible to the census; latent because no profile had
  ever declared an A or M form while pinning the 64-bit table), and the A pin
  then broke that leg (87 enumerated vs 65 declared) until the rv64i dossier's
  declared M-exclusion shape — "pinned for the fragment, not the scope" — was
  extended to the A tables with the same flip condition (slice e's bind grows the
  census to 87 and flips it). Both profiles' `--verify-only` stay green
  (65 == 65, 52 == 52) and a scripted fresh re-fetch of rv_a is byte-identical.
- The `(slot (id a) (requires "riscv/a"))` stays declared and the scope census
  stays 65 — both grow only at the atomic bind (slice e). Trial compositions
  through a synthetic unit doc: base+A 74 instructions collision-free; the
  five-fragment union 84 (+ 3 pseudo) collision-free with the M slot declared.
  No Rust touched; every generator's `--check` byte-exact; `make gate` green
  (DERIVED-COUNTS 424 unchanged). Next: slice (b) — `a.sem.sexp` + the new
  operators through the schema/check/generator path.

## SEMULITH-P4-0020 (leaf P4-SYSTEM.3, slice e part 2; the leaf CLOSES) — the sv39 Sail matched experiment (PTW/TLB traces explicit)

- The sv39 matched experiment runs on THREE explicit dimensions against Sail 0.14
  under the tracked Svade-flipped override: the ARCHITECTURE (the corpus's own
  change-observation rule against the EVD-05 expectations, indexed on Sail's
  printed step numbers — Sail numbers the fetch-fault step but prints no row for
  it, and the expectations' `<fetch page fault>` pseudo-steps are exactly those
  no-row, no-write steps, the recorded harness convention); the PAGE-TABLE WALKS
  (Sail's `--trace-ptw` against the spec-side model's walk log with the
  laboratory's 4-entry FIFO live — read-for-read identical on every guest:
  the PTE values at the same addresses at the same levels); and the TLB EVENTS
  (`--trace-tlb` — sv39-tlb-fence shows the same 7 adds / 2 flushes on both
  sides). Verdict: **13 AGREE + 1 AGREE-RECORDED, 0 DIVERGE of 14**. The one
  convention recorded, never normalized: Sail judges A/D AFTER the walk (PTW:
  Success, then the trap), the laboratory's walk judges it at step 9 (a
  walk-outcome fault) — the delivered trap (cause, xtval) is identical.
- The one tracked content change: the matched override's medeleg mask widened
  0x3FF → 0xB3FF — sv39-deleg measured the old mask making medeleg bit 13
  read-only-zero on Sail (the page fault reached M, not S: sail's x22=13 against
  the expectation's x7=13). The laboratory's state.sexp pins causes 0-10 | 12-15
  | 18-20 WARL-any; Sail 0.14 refuses its reserved causes (the bisection named
  10 and 14, 17-20 rejected wholesale), so 0xB3FF (0-9 | 12 | 13 | 15) is the
  widest mask both sides honor — proven verdict-neutral on the mm corpus (11/12
  AGREE under the widened override, mm-wfi's TW cell named at the same step).
- The ELF build keeps the tracked assembler the owner of the bytes (the corpus's
  operand syntax never reaches clang): a .word-only lowering plus a PHDRS link
  script puts the image at EXACTLY 0x8000_0000 — the auipc+addi chains compute
  absolute table addresses (the mm guests never noticed `--image-base`'s 0x1158
  offset; their addressing is pc-relative).
- The leaf's acceptance is met: permission failure produces the correct fault
  AND the permitted page-table side effects (under Svade: none — every
  translate/svade guest closes with the walked PTE read back byte-untouched);
  the A/D policy is validated against the selected extensions and revision, not
  chosen as a knob (Svade pinned at slice (a), Svadu not selected, the override
  carries Svade:true/Svadu:false). The engine and the 76-guest corpus are
  untouched (`git diff SEMULITH-P4-0019 -- crates/ profiles/.../guests/ | wc -l`
  → 0); `make check` 8/8, `make gate` all green (DERIVED-COUNTS 424 unchanged).
  Frontier → `P4-SYSTEM.4` atomics and reservations.

## SEMULITH-P4-0019 (leaf P4-SYSTEM.3, slice e part 1) — the sv39 guest corpus, the matrix cells, the fetch-count witness made declarational

- The 14-guest sv39 corpus lands at `profiles/rv64gc-lab-v0/guests/`, every
  expectation derived by a spec-side model of the pinned chapters (EVD-05 — the
  10-step walk, Svade, MPRV, medeleg, the region bounds, and the slice-(d) TLB
  semantics re-derived in Python, never read from an engine run) and falsified
  green through the tracked engine: `sv39-translate-4k`/`2m`/`1g` (the happy
  paths, each closing with the M-mode ld-back of the walked PTE byte-untouched
  at its authored value after the translated accesses — the Svade side-effect
  proof); `sv39-fault-canonical`/`-invalid`/`-reserved`/`-superpage` (the walk's
  steps 1/3/4 and misaligned superpages, causes 12/13/15 with xtval = the VA);
  `sv39-perm-rwx` (R-only store → 15, X-only load with MXR=0 → 13, a FETCH into
  the X=0 page → 12); `sv39-perm-usr` (U/SUM/MXR from S through sstatus, then a
  U-mode stage fetched from its own U=1 code page); `sv39-svade` (A=0 load and
  D=0 store fault, the D=0 load is legal, both PTEs byte-untouched);
  `sv39-mprv` (MPRV=1/MPP=S translated load+store in M with NO code mapping —
  execution continuing is the fetch-immunity proof; MPP=U → page fault; MPRV=0 →
  access fault, visibly distinct); `sv39-tlb-fence` (stale before the fence,
  the ASID-selective fence retaining the G=1 entry, the full fence restoring
  truth); `sv39-straddle` (a 32-bit instruction whose two parcels live on
  non-contiguous pages — two fetch requests — with the IALIGN-16 cells that
  coalesce); `sv39-deleg` (medeleg bit 13 routes the load page fault to the S
  handler — scause/stval/sepc + sret — while the ecall still lands in M).
- The fetch-count witness becomes a DECLARED observation: `fetches` enters the
  expectations schema as an optional field (a step whose fetch page-faults in
  the walk issues walk accesses but NO `Request::Fetch`; a straddled
  instruction whose parcels' physical addresses are non-contiguous issues two —
  the recorded coalescing rule is address contiguity, measured). The generator
  refuses a count outside the parcel bounds (a RED arm, GUEST-GEN 15→16), the
  corpus assertion compares the declared count, and the 62 pre-slice guests
  keep exactly their old strictness (the field defaults to the step count).
- The matrix names all 14 on the SAME seven axes (page faults are the fault
  axis's 12/13/15 vocabulary; the walk's permissions are legality; medeleg's
  page-fault bit is delegation; superpage sizes and the page-crossing fetch are
  boundary; MPRV/MPP and the xret returns are restart) — 28 cells, every
  disposition resolves, no axis added.
- The Bare-identity proof is byte-exact on the corpus-extended engine: both
  CLIs (a scratch worktree at `e839c1b`, removed after) drive all 62 pre-slice
  guests — `62 byte-identical, 0 diverge`. The run's probe bugs are recorded
  with their classes (mscratch is M-only — an S-mode write traps illegal, the
  engine measured right; x8-already-zero records no change; the unit-vs-
  contiguity fetch model, corrected by the measured 53 fetches). `make check`
  8/8, `make gate` all green (DERIVED-COUNTS 423→424), smoke-bench 53 arms,
  bench wasm, both books.
  Next: slice (e) part 2 — the Sail matched experiment (PTW/TLB traces
  explicit) + the leaf's acceptance and closure (`SEMULITH-P4-0020`).

## SEMULITH-P4-0018 (leaf P4-SYSTEM.3, slice d) — the TLB, sfence.vma's real four cases, the census/snapshot/determinism consequences

- The minimal fully-specified TLB: **4 entries, fully-associative, FIFO replacement,
  ASID-tagged at ASIDLEN=16, keyed by 4 KiB page** — the minimal parameters that make
  every rule testable (a superpage's other pages re-walk and install independently —
  conformant, and it keeps the fence's per-address case exact). Authority laboratory;
  the same parameters live as data in the state document's SEM-08 census (the
  `address-translation caches (TLBs)` candidate re-answered `present true` — the
  census's own ".3 reopens this candidate" hook), and gen_state emits the storage as
  hart state from that declaration — refusing, RED-armed, a descriptor whose census
  is silent on the cache (STATE-GEN 25→26 arms).
- The visibility record: satp is read per access, so MODE and ASID changes take
  effect immediately (dispatch and tagging); a root-PPN change is visible on the
  next miss, and stale entries may hit until a fence — §11.1.2.1's sanctioned
  staleness, the fence being the contract (the cache never auto-invalidates).
  SUM/MXR are read per access, never cached, always immediate. The install
  discipline: a faulting access installs nothing; a load past a D=0 leaf installs
  the D=0 entry — the cached entry's D bit then faults a later store after software
  sets D without fencing (a LEGAL stale fault), and the fence restores the walk's
  truth. The walk's step-9 A/D check uses the entry's stored bits — under Svade
  there is no hardware update for a cache to skip, and the fault path must not be
  cached.
- sfence.vma's effect lands through the full pipeline: the `tlb-invalidate` operator
  (schema/semantics.sexp, the four-case contract) → `system.sem.sexp`'s effect
  `(tlb-invalidate (reg rs1) (reg rs2))` — the time-scoped nop superseded with its
  date, the legality untouched — → gen_definition's extended map + the
  `Sem::TlbInvalidate` variant (DEF-GEN both pairs green, rv64i fingerprint-only) →
  the evaluator arm (rs1 the VA, rs2's low 16 the ASID, no register written). The
  over-fence latitude is recorded-not-taken, so the G-bit retention and the
  per-ASID cases are genuinely tested.
- The TLB suite (25/25 with the walk's 17): a hit skips the walk (count frozen);
  FIFO evicts in order (6 installs, the oldest re-walks); ASID tags with G hitting
  under any ASID; staleness legal without a fence then restored by it; Svade
  staleness through the cache (the D=0 install → the legal stale store fault → the
  fence); all four fence cases with their retentions (per-ASID and per-address+ASID
  keep globals; per-address evicts them; all-spaces empties everything); the
  non-canonical rs1 no-op; the fence INSTRUCTION end-to-end (sfence.vma x3,x4
  through the evaluator empties the entry); and cold-reset determinism — two runs,
  outcome tuples identical (the cache is a pure function of the hart's own history).
  Snapshot measured and recorded: no rv64gc snapshot surface today (the CLI's
  snapshot/resume is rv64i-scoped by refusal), and a cold-restored cache is always
  a legal state — a miss is never wrong.
- mm-sfence's expectations needed NO re-derivation — measured: its legal fence
  cells never claimed a nop, and a fence writes no register, exactly what they
  record. The Bare identity is byte-exact on the TLB engine: both CLIs over all
  62 guests, 1,884 == 1,884 trace lines, `cmp` clean (worktree removed after).
  `make check` 8/8, `make gate` all green (DERIVED-COUNTS 422→423), smoke-bench
  53 arms, bench wasm, both books.
  Next: slice (e) — MPRV/SUM/MXR + the sv39 guests + matrix cells + the Sail
  matched experiment + the reports and the book.

## SEMULITH-P4-0017 (leaf P4-SYSTEM.3, slice c) — the 10-step Sv39 walk, the fault matrix, the REQ-D-FETCH-IMPLICIT amendment

- The walk is live in `crates/semulith-core/src/translation.rs`, cited step-by-step
  (§11.1.3.2 with LEVELS=3/PTESIZE=8 per §11.1.4.1): the canonical-VA check
  (bits 63:39 == bit 38) before any read; per-level PTE reads through slice (b)'s
  walk-access boundary kind, a boundary fault reported as the ORIGINAL access's
  access fault (1/5/7 by kind, step 2); V=0 and the W-without-R reserved encoding
  (step 3 — the first draft's R∧W inversion caught by the fault-matrix tests
  written before the fix); reserved/PBMT/N bits 63/62–61/60–54 zero with
  Svnapot/Svpbmt named unselected (step 4); misaligned superpage (step 5);
  non-leaf D/A/U reserved per §11.1.3.1 (step 6); the shadow-stack step named
  N/A (step 7); U/SUM/MXR and R/W/X by access kind (step 8); Svade's
  page-fault-instead-of-update with the PTE byte-untouched (step 9 — the
  permitted page-table side effects are NONE, by construction not by inspection);
  the physical address by level (step 10).
- The fault-matrix suite: 17 translation tests covering all three leaf sizes with
  their walk-read counts (3 for 4 KiB, 2 for 2 MiB, 1 for 1 GiB), the canonical-VA
  fault, V=0, reserved-RW, the reserved bits ×3, misaligned superpage, non-leaf
  D/A/U ×3 + the last-level pointer, the U/SUM/MXR cells (S-page from S, U-page
  from S with and without SUM, S-fetch of a U-page unconditionally, U-page from
  U, MXR on/off), the R/W/X cells, the Svade A/D cells with the region
  byte-identical across the fault, the step-2 access fault by kind, the MPRV
  selection (data walks like S, fetch ignores MPRV, M never walks), and the
  satp.MODE named defect. The straddled fetch is live end-to-end: two parcels on
  non-adjacent physical pages, each fetched from its own unit and joined —
  2 fetch requests, 6 walk reads, the word exact (the coalescing rule is over
  translated addresses, not pages: adjacent physical pages correctly coalesce).
- The requirement amendment was measured first: rv64gc's catalogue NEVER carried
  REQ-D-FETCH-IMPLICIT (the mirror's closure is 13 records and it is not among
  them — `grep -c FETCH` → 0), so the amendment lands as a NEW authored pair:
  D-WALK-IMPLICIT in the profile and the verbatim REQ/OB mirrors
  (CHK-WALK-IMPLICIT-POS/NEG, dependencies REQ-D-SV39 + REQ-D-SVADE), naming the
  translated composition's implicit-access vocabulary (the fetch + up to LEVELS
  implicit 8-byte walk reads per access; no implicit writes under Svade).
  rv64i's owner record stays true of rv64i — no translation exists there;
  RECORD-SCHEMA green by its own run.
- The Bare identity is byte-exact on the walk-live engine: both CLIs (the parent
  commit's and this one) over all 62 guests — 1,884 == 1,884 trace lines, `cmp`
  clean (worktree removed after) — beside the standing cargo assertions (62/62,
  fetch counts unchanged). The slice-(b) stub probe now faults properly: an
  S-mode fetch under Sv39 with an empty root table page-faults (V=0) with
  mcause 12 and mtval = the faulting VA; the walk-access boundary fault path is
  measured separately (satp.PPN outside the region → access fault by kind with
  tval = the original VA). `make check` 8/8 groups, `make gate` all green,
  smoke-bench 53 arms, bench wasm, both books. The guests exercising the walk
  end-to-end land in slice (e), per the brief.
  Next: slice (d) — the TLB + sfence.vma's real four-case effect + the census /
  snapshot / determinism consequences.

## SEMULITH-P4-0016 (leaf P4-SYSTEM.3, slice b) — the translation module + hooks + effective mode; the Bare-identity proof byte-exact

- The translation machinery shell lands as evaluator machinery (the brief's
  decisions 3–6): `crates/semulith-core/src/translation.rs` beside `privilege.rs` —
  the effective-mode computation as ONE computation (RVP-MACHINE §2.1.1.6.4: fetch
  uses the current mode and M-mode fetch is never translated; loads/stores use
  mstatus.MPP when MPRV=1, with SUM/MXR carried for the walk); satp.MODE dispatch
  (M-effective and Bare are exact identity; Sv39 enters `Translate::Walk` — slice
  (c)'s entry, until then the named unimplemented case, never a wrong answer; an
  out-of-vocabulary satp.MODE is a named panic); the page-fault causes 12/13/15
  entering core as raw u64 with the typed-enum asymmetry stated (the privileged
  engine's causes are delivered raw through the one trap-deliver path).
- The three hooks wired in `exec_rv64gc.rs` (fetch at :87, load :291, store :328 —
  the brief's own locators): fetch in 16-bit parcels (decision 5) with the
  recorded coalescing choice — parcels translate independently, and the fetch
  issues exactly one `Request::Fetch` whenever both translated addresses share one
  physical 32-bit unit, which under Bare is every case, so the Bare request shape
  is byte-exact by construction (the corpus's one-fetch-per-step assertions hold
  it); loads and stores translate after the model-side misalignment check (the
  pinned implementation-defined priority, decision 7).
- The walk-access boundary variant enters the engine's vocabulary:
  `Request::WalkAccess { addr }` + `Response::WalkAccess(u64)` — 8-byte physical,
  read-only by construction under Svade (the D-FETCH-IMPLICIT precedent applied;
  the formal contract wording routed to `.9`, recorded). Its three exhaustive-match
  dispositions: FlatMemory answers it (8-byte aligned region read, never a fetch —
  the one-fetch-per-step census keeps its meaning), the bench census gains
  `walks`, and rv64i's TestEnv panics named (the base profile has no translation
  machinery).
- The Bare-identity proof is byte-level and complete: both CLIs (the parent
  commit's engine and this one, via a scratch worktree) drive all 62 guests and
  1,884 trace lines compare `cmp`-clean — beside the standing cargo assertions
  (62/62, per-step writes, step counts, never_written, fetch counts, cold-reset
  determinism) and the Sv39-entry probe (an S-mode `ld` with satp.MODE=Sv39 →
  `model error: Unimplemented { what: "Sv39 translation — the walk is P4-SYSTEM.3
  slice (c)'s" }`, cli rc=1 — the entry names itself, never a wrong answer).
  rv64i's engine untouched; 6 translation unit tests (Bare-identity,
  M-never-translated, the walk entry, the MPRV rule, the named defect, the cause
  vocabulary); `make check` 8/8 groups, `make gate` all green (DERIVED-COUNTS 422
  unchanged), smoke-bench 53 arms, bench wasm, both books.
  Next: slice (c) — the 10-step walk with its fault matrix, the reserved-bit and
  superpage checks, and the REQ-D-FETCH-IMPLICIT amendment.

## SEMULITH-AC-0058 (tree ARTIFACT-CLEANUP) — the 2026-10-04 §8 run: 90 incremental caches deleted (245 MB)

- The ~24 h trigger fired (the `2026-10-03` record was a day old). The census found
  90 cargo incremental `.bin` caches (245 MB; 72 `target/debug`, 18 wasm32), all under
  the enumerated `*/incremental/*` scope, deleted; 0 stray `.bin`/`.log` in
  `target/release`/`target/debug/deps`. 62 `target/refs/*.log` (2.2 M, evidence trails)
  and the 7 cargo-home crate fixtures (inputs) kept by standing policy.
  `docs/ARTIFACT_CLEANUP.md` overwritten with the dated one-line record; `target`
  4.2 G → 4.0 G, `.app-data` 1.4 G unchanged.

## SEMULITH-P4-0015 (leaf P4-SYSTEM.3, slice a) — the Svade identity edit, the Sail override flip (measured verdict-identical), the validate_gc refusal

- OQ-2 closes with evidence: the profile implements **Svade** — a translation needing
  an A or D PTE update raises a page fault, never a hardware update. The three legs:
  the pinned revision defines exactly two A/D schemes and names the page-fault one
  Svade (RVP-SUPERVISOR §11.1.3.1, §11.1.10 — inline in the already-pinned chapter,
  so sources.sexp gains no pins, measured); the U54 MMU the Sv39 choice already
  cites implements exactly that scheme ("does not automatically set the A and D
  bits … Instead, the U54 MMU will raise a page fault", FU540 §4.7); and the
  laboratory's observe-through-the-ISA discipline can evidence a page fault but not
  an implicit PTE write, so the hardware-update default would price a new
  observation vocabulary to test a side effect the laboratory need not produce.
  Svadu is NOT selected — menvcfg's ADUE stays WPRI (measured inside the state
  document's `wpri_62_0` field).
- The identity edit: `(extensions "Svade")` in declared order — the canonical ISA
  string is now `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade` (gen_platform's
  declared-order rule; the string matches the brief exactly) — the D-SVADE decision
  with authority laboratory and its verbatim REQ/OB mirrors (the D-ROUTE-FLIP
  shape: contract `rv64gc-lab-env-v0` version `"0"` unchanged, CHK-SVADE-POS/NEG),
  D-SV39's "not as this profile's rule" clause superseded by note (RECORD-SCHEMA's
  mirror rule kept), DOSSIER.md's OQ-2 closed with the legs quoted and its locator
  tables updated, and the ISA-string census discharged: two authored edits with
  owners named (the book, the `.1` Result narrative), the Sail-default mentions
  and the archive untouched, no derived regeneration needed (no board pins rv64gc
  today).
- The reference flips to match: `Svade supported: true` in the tracked override —
  one field, as the brief priced it (the .2 override had set it explicitly
  `false`; Sail's own default is `true`, so the flip also makes the override name
  what it depends on). The full 12-guest re-run against the tracked-derived JSON
  measures the effect: **11/12 AGREE — IDENTICAL to the pre-flip baseline** (no
  guest activates translation; the mm-wfi DIVERGE is the known TW cell, not a new
  effect). The config validates clean.
- The generator hole the brief's pre-condition 6 named closes: `validate_gc`
  refuses `register_family`/`memory_spaces`/`hardware_stack` by name with the
  rv64i path's own wording — three RED self-test arms on mapping-valid injected
  shapes (so the refusal that fires is the validator's own), STATE-GEN 22→25 arms,
  both real owner→mirror pairs byte-identical. `make check` 8/8 groups, `make
  gate` all green (DERIVED-COUNTS 419→422 re-derived, never hand-incremented).
  Next: slice (b) — the translation module + the three hooks + effective mode +
  the Bare-identity proof.

## SEMULITH-P4-0013 (leaf P4-SYSTEM.2, slice h part 2) — the Sail privileged matched experiment (11/12 AGREE, the TW cell named, mm-counters not matchable); the leaf closes

- The Sail privileged matched experiment (decision 8), attempted and honestly
  recorded. The matched override lands tracked at
  `profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp` (the .sexp is
  the truth, the JSON derived by `materialize_sail_override`): privileged ISA 1.13,
  misa held (WARL), FS four-state / VS off, the declared selection (M/A/F/D/C,
  Zicsr, Zifencei, Sstc, Sv39, S, U) minus Zicntr, no devices, no PMP, WFI a nop
  except in U, medeleg 0x3FF — Sail's own validator confirming the corpus's claims
  (cause 10 is reserved with H off; bit 11, ecall from M, is undelegatable by law;
  the matched mask derived by bisection).
- The evidence chain closes end to end: the tracked .sexp derives the JSON, Sail
  0.14 (git 29e6158) runs the mode-matrix guests under it, and **11 of 12 AGREE
  step-for-step against the specification-derived expectations** — the zicsr rw
  semantics, per-mode CSR legality with mtval = the word, delivered breakpoints and
  resumes, ecall causes 11/9/8 and medeleg delegation (the M-ecall never
  delegating), mret's MPRV clear-below-M / preserve-at-M, the mstatus all-ones
  WARL read-back bit-exact (`0x8000000A007E79AA`), stimecmp's TM then STCE gating,
  the TVM gates, sret and TSR. The comparison normalizes Sail's trace to the
  corpus's own change-observation rule — the reference's execution, the
  specification's values.
- The two honest boundaries, each with its evidence: mm-wfi's TW=1-in-S legality
  cell is a NAMED DIVERGENCE — Sail 0.14 does not implement mstatus.TW's effect on
  WFI legality (the wfi retires as a nop with `wfi_is_nop=true`, waits forever
  with it false; the bit is provably writable — mm-readonly's all-ones read-back
  AGREEs bit-exact, bit 21 included; no config knob exists). Our expectation
  stands on RVP-INSNS; the finding is routed to P4-SYSTEM.5 (the wfi/wake leaf)
  with the measurement recorded. mm-counters is NOT MATCHABLE — Sail requires a
  CLINT time source when Zicntr is enabled and D-PLATFORM declares no devices;
  the counter rate is the environment's own declaration (our laboratory holds
  zero). Spike stayed platform-conflicted, no attempt.
- The dossier-format owners learned the override's new keys:
  `schema/override.sexp` (optional fields — rv64i's override re-validated) and
  `dossier_sexp`'s mapping both directions (self-test 13→14; the round-trip
  field-for-field exact). `make check` and `make gate` fully green
  (DERIVED-COUNTS 419 unchanged).
- **Leaf P4-SYSTEM.2 is done** — the acceptance criterion "the same instruction's
  behaviour is tested in each supported mode" is the mode matrix itself: 13
  guests, every cell a mode crossing, falsified by the tracked engine (62/62) and
  differentially confirmed (11 full AGREE + 1 partial). Frontier: `.3` — Sv39
  translation and protection.

## SEMULITH-P4-0012 (leaf P4-SYSTEM.2, slice h part 1) — THE ATOMIC FLIP: the payload tracked, the route generated-definition, the corpus on the tracked engine

- The proven staging moves into `profiles/rv64gc-lab-v0/` byte-exact: the 33-CSR state
  document, the encoding composition (base + Zicsr + Zicntr + the privileged-system
  fragment, `(status partial)` with six declared slots for M/A/F/D/C/Zifencei), the
  62-guest corpus with run-order, and the 7-axis × 28-cell interaction matrix. The
  vehicle route flips to `generated-definition`; D-RESOLUTION-ROUTE is superseded by
  note (the D-FENCE convention — its statement stays verbatim because RECORD-SCHEMA
  mirrors it) and D-ROUTE-FLIP records the flip, its REQ/OB pair in the
  authored-records shape.
- The generated mirrors land tracked because their canonical inputs land tracked in the
  same commit (decision_generated-mirror-needs-tracked-input):
  `crates/semulith-core/src/state_rv64gc.rs` + `definition_rv64gc.rs`,
  `crates/semulith-verify/src/guests_rv64gc.rs` — content-hash-identical to the
  scratch-proven modules, provenance lines tracked-honest.
- The tracked engine runs the corpus 62/62: `exec_rv64gc` ports the evaluator with the
  trap-END discipline ridden in from the scratch runner (a delivered trap ends the
  step's remaining effects), delivery through the tracked `privilege` machinery,
  reserved decode reported for the diagnostic policy one layer up;
  `semulith-verify`'s `run_rv64gc` drives all 62 guests with the base differential's
  assertion family (per-step writes exact, never_written, one fetch per step,
  cold-reset determinism) — 4/4 test groups green. FlatMemory carries IALIGN as
  profile data (`with_fetch_align`; the rv64i default byte-exact).
- The CLI's profile becomes a runtime selection: `--profile=` on run and demo
  (rv64gc through the privileged engine), named refusals from the rv64i-scoped
  commands (bench, bundle, reduce, replay, snapshot, resume, mutations), rv64i the
  byte-exact default.
- Four gate gaps the flip measured, each fixed at its owner with RED-first arms:
  check_extraction honors MODEL-COMPOSE.6's refinement relation (self-test 11→13);
  EXERCISE-COVERAGE's SCP-02 closure leg counts the composition's pseudo children
  (21→23); the three GEN gates judge owner→mirror PAIRS (STATE-GEN 20→22, DEF-GEN
  15→17, GUEST-GEN 10→15 — the rv64gc pair each, plus the base-mirror governor: 93
  files byte-identical + 5 recorded re-derivations); FACT-OWNERSHIP re-pins to 5
  units / 74 fact kinds. The CSR name↔address ownership migrated to the state
  document (the assembler reads it; csrs.csv stays the derivation source, 33/33;
  `pmpaddr0` refused by name). gen_state's rv64gc emission is rustfmt-stable
  (cargo fmt runs over crates/; STATE-GEN compares against regeneration).
- Full local proof: `make check` (76 core / 184 verify), `make gate` all doctrines
  green (DERIVED-COUNTS 408→419 re-derived, never hand-incremented), bench wasm
  133,662 bytes, smoke-bench 53 arms, both books build, fetch_references MATCH for
  both profiles, and every rv64i verdict unchanged (52/52 exercised; its generated
  surfaces byte-identical but definition.rs's embedded generator fingerprint).
  The split is recorded: the flip is its own commit; the Sail privileged
  matched-experiment attempt lands as part 2.

## SEMULITH-P4-0011 (leaf P4-SYSTEM.2, slice g) — the interactions.sexp: 7 axes × 28 cells, rehearsed green against the staged unit

- The unit's interaction matrix, authored at scratch staging (route-contradicted until
  the flip): seven axes from the leaf's own vocabulary — fault, alias, boundary and
  progress carried from the mirrored base layers; **legality** (mode-dependent
  permission and refusal: M/S/U, TW/TVM/TSR, read-only/WARL, encoding validity) and
  **delegation** (interception routing: medeleg, the counter enables, STCE) added by the
  privileged machinery; **restart reframed guest-shaped** — rv64i's mechanism-shaped
  restart becomes the xret/xepc return discipline (the mechanism registry is closed and
  no rv64gc mechanism exists; mret/sret make restart observable by guests); rv64i's
  event axis absorbed into the mode-cause and delegation story.
- 28 cells, all dispositioned: every one of the 62 staged guests maps onto ≥1 cell (no
  new guests needed — the base mirror keeps rv64i's layer mapping, the mm guests land on
  their machinery's cells), and three cells (alias×restart, boundary×delegation,
  boundary×restart) are reported degenerate-with-reason — the doctrine's sanctioned
  shape for a cell the corpus honestly does not compose.
- The DIFFS rule forced the mirror's fourth and fifth re-derivations: it-fencei and
  min-fencei carried rv64i's `expect_divergence` pin (DIFF-FENCEI-EXECUTED), whose
  record is false for this unit — rv64gc DECLARES Zifencei and the staged encoding
  leaves the slot unbound. The divergence forms were dropped with the reason recorded in
  each file's comment; steps/writes/never_written unchanged; the corpus re-proven
  `62 guest(s) PASS, 0 FAIL`. The mirror now reads 49 `.s` byte-identical, 44
  expectations byte-identical, 5 re-derived (3 IALIGN-16 + 2 fencei-slot).
- The rehearsal ran the check's own invocation against the staged unit
  (`scripts/check_interaction_matrix.py <unit-dir>` — the `.sh` driver discovers tracked
  `profiles/*/` at the flip): 28 cells declared, every disposition resolves, rc=0. The
  RED legs fired by name against a scratch copy: DIFFS on the pre-re-derivation fencei
  files (NO REFERENCES + UNKNOWN DIFFERENCE), ORPHAN GUEST on a dropped name, OMITTED
  CELL on a deleted cell. Driver self-test 15/15; tracked units untouched
  (`INTERACTION-MATRIX: ok (5 unit(s))`); `make gate` green (DERIVED-COUNTS unchanged at
  408 — no arms this slice). Next: slice (h) — the atomic flip.

## SEMULITH-P4-0010 (leaf P4-SYSTEM.2, slice f) — the base mirror executed (49/49), the mode-matrix corpus, the coverage rehearsal

- The rv64i guest corpus runs on the rv64gc engine: all 49 guests staged byte-identically
  (c-scope.c excluded — `scripts/build_c_guest.sh` hard-codes `-march=rv64i`; the rv64gc
  C-guest question is recorded for the flip) and executed by the scratch corpus runner
  (`target/p4-system-2/proof/corpus.rs`) — the declared MainMemory map, fault delivery on
  the pinned cause vocabulary, the per-step x-register-change comparison rule from the
  rv64i verify runner. The runner's trap-END discipline was a real bug it-fault-alias
  exposed: a delivered trap now aborts the step's remaining effects.
- 46 expectation files carry over byte-identically; fault-jal-mis, fault-jalr-mis and
  it-prio-jump were RE-DERIVED BY DESIGN — under D-IALIGN-16 their 2-mod-4 jump targets
  are legal (RVI-C 27.1), so the link write lands and no misaligned-fetch fault fires. A
  declared profile difference, measured and re-derived from the pinned chapters — never
  fitted to engine output (EVD-05).
- The mode matrix: 13 new guests with expectations derived BEFORE the run — the six
  zicsr forms' read/write/set/clear semantics; M-CSR legality in S and U (mtval = the
  faulting word); delivered breakpoints that resume; ecall causes 11/9/8 by mode and
  medeleg delegation to S with sret return (an M-mode ecall never delegates); mret mode
  pops with MPRV cleared when the target is below M and preserved at M; sret legal in
  M/S, illegal in U, and the TSR gate; wfi and the TW gate; sfence.vma and satp reads
  under TVM; counter reads under mcounteren then scounteren; stimecmp under TM then
  STCE; read-only CSR writes trapping while misa (WARL) ignores them; the mstatus
  all-ones WARL read-back (0x8000000A007E79AA, the state document's field table).
- Execution was the falsifier: it caught 14 stale auipc+addi vector deltas (labels
  assemble to no word — every vector target re-audited through the real assembler), two
  guest-design bugs (M-level CSR writes inline in S-mode in mm-mret and mm-ecall-modes —
  the drops moved before/inside the M handler), one hex-digit slip in the mstatus WARL
  constant and one no-change mis-derivation. Every mismatch was re-derived, never
  fitted. `corpus: 62 guest(s) PASS, 0 FAIL` (49 base + 13 mode matrix, deterministic
  re-run); the coverage rehearsal over the staged 65-form scope reads 65/65 (the base 52
  via the mirror, the 13 extension forms via mm-*, per-guest counts recorded). All
  untracked scratch — no gate arms this slice (the corpus's registry governor lands at
  the flip); `make gate` green (DERIVED-COUNTS unchanged at 408).
  Next: slice (g) — the interactions.sexp.

## SEMULITH-P4-0009 (leaf P4-SYSTEM.2, slice e) — the 65-form census (dual edit), the base-corpus mirror + authored records, the flip's staged encoding

- The scope census grows 52→65 by the mandated dual edit (`schema/profile.sexp` +
  `dossier_sexp._SCOPE_LISTS`: +zicsr_csrs, +system_privileged, +zicntr_counters). The
  pseudo-census decision, recorded in the profile's scope comment: the Zicntr counter
  reads ARE census forms (the spec's Zicntr listings name them), the encoding realizes
  them as csrrs specializations (the fragment's pseudos), and EXERCISE-COVERAGE observes
  the spelling in the expectations' insn text — measured. EXTRACTION's integrative claim
  now counts the composition's pseudo names (+2 self-test arms, 11 total).
- The requirements growth: the base-corpus mirror is derived by closure, not typed — the
  9 instruction family records + fence/ecall-ebreak + the XLEN/ENDIAN dependencies (13)
  and their 13 obligations, byte-verbatim but for the profile-scoped fields, with
  `mirrored_from` provenance, plus 3 authored requirement records (Zicsr access model +
  permission refusals; the privileged four's per-mode legality; the Zicntr reads + gating)
  and their obligations with POS+NEG check pairs — 34/34 in rv64gc's catalogues. The
  governor: RECORD-SCHEMA rule 14 (MIRROR-DERIVE), registry-driven by two new
  FACT-OWNERSHIP rows (63 kinds), its four RED arms fired (drift, missing,
  ungoverned-authored, owner's-contract-kept).
- The flip's encoding.sexp is staged at `target/p4-system-2/profiles/rv64gc-lab-v0/` with
  the flip's own bytes (relative fragment-root, the definitions symlink, `(status
  partial)` + six slots for m/a/f/d/c/zifencei), validated: schema conform, the union
  collision-free (62 instructions + 3 pseudos), the holes honestly declared; the slice-(d)
  execution proof regenerated from the staged bytes and re-run (26/26). The staged
  payload's README records the flip mapping.
- Measured in execution, fixed at root: the dropped-`(extensions …)`-form bug's census
  found two MORE readers (check_exercise_coverage.sh, gen_model_book.py — six sites, the
  pattern now extinct, `git grep` clean); PROFILE-CONSISTENCY's PARTS DRIFT learned the
  extension families (it fired honestly on 40+12≠65 mid-edit); fetch_references' scope leg
  covers the pinned tables, pseudo-aware (rv64gc 65==65, rv64i 52==52 unchanged). The
  docs/tasks/ aggregate ceiling fired (63 files / 1,575,182 B > 1.5 MiB — the slice
  checklists are the designed growth) and was re-derived to 3 MiB by decision record.
  `make gate` green (DERIVED-COUNTS 404→408 arms). Next: slice (f) — the guests corpus.

## SEMULITH-P4-0008 (leaf P4-SYSTEM.2, slice d) — the generators parameterize to rv64gc, the privilege machinery lands, the scratch execution proof passes

- The two-profile shape, measured into existence: the tracked evaluator matches rv64i's
  byte-frozen generated `Sem` enum, so the slice-(b) operators' evaluation arms cannot
  compile tracked until the rv64gc definition module is tracked (the flip). The machinery
  doesn't wait: `crates/semulith-core/src/privilege.rs` (tracked, hand-authored) owns trap
  delivery (delegation selection, the xPIE/xIE/xPP stack, xepc/xcause/xtval, pc←xtvec),
  xret, the uniform CSR permission model (mode bits, read-only bits, counter-enables,
  TM/STCE, TVM) and WPRI/WARL/WLRL legalization — over a `PrivilegedHart` trait whose
  metadata vocabulary it owns; the generated rv64gc state module implements the trait with
  the descriptor's tables. The WARL seam closed: prose legalization became the structured
  `(legalize …)` mini-language, applied by the engine as a lookup. 11 machinery tests over
  a fixture hart.
- gen_definition's rv64gc branch lowers all 8 slice-(b) operators, emits pseudos as
  PSEUDOS metadata (the coverage mapping is slice (f)'s), and composes three separate
  `(extensions …)` forms correctly — its name list carried the THIRD copy of the
  dropped-form bug. gen_guests is directory-derived (the set is the directory; the run
  order is the tracked run-order.txt, cross-checked both directions; rv64i regenerates
  hash-only — the brief's "51-name list" measured 49). elf.rs's IALIGN is a parameter
  (the routed twin of slice a's assembler fix); the CLI passes the profile datum (32)
  explicitly. The dossier digest rotated on run-order.txt; the cascade re-derived
  (reports, the board's pin, the platform manifest, both books), and the PLATFORM-GEN
  stale-pin arm that assumed the digest's leading digit was fixed.
- Validation: the scratch execution proof — six guests assembled with the tracked
  assembler against the staged composition, run through the generated modules + the
  tracked machinery: the CSR disciplines (rs1=x0 never writes, the swap exact for
  rd==rs1), ecall delivered in M (cause 11, xepc=own address) and delegated to S (cause 9,
  the S handler, sret back), wfi legal-nop in M / illegal in U, sret illegal in U,
  sfence.vma under TVM, rdcycle gated then enabled — 26/26, catching two authoring defects
  on the way (an atomic CSR's write preserving everything; a wrong delegation bit). Both
  rv64i generated modules regenerate with only the embedded generator-hash lines changed.
  STATE-GEN 20/20, DEF-GEN 15/15, GUEST-GEN 10/10 (new arms RED-first); `make check` and
  `make gate` green (DERIVED-COUNTS 395→404). Next: slice (e) — the unit artifacts.

## SEMULITH-P4-0007 (leaf P4-SYSTEM.2, slice c2) — the rv64gc module's tracked landing is flip-bound; the scratch engine proof recorded

- The (c2) judgment, measured rather than assumed: STATE-GEN proves rv64i's state.rs
  byte-exact from its TRACKED descriptor in a fresh clone; a tracked rv64gc module
  generated from the staged (untracked) document would be unjudgeable there — a copy, not
  a derivation. The three alternatives were each measured dishonest (a skip-if-absent
  gate leg = a standing hole in the byte-exact property; a hand-written interim module =
  a second owner, OWN-01; a non-unit descriptor home = a category lie). So the module
  lands with the descriptor at the flip (slice h), in one green commit, with STATE-GEN's
  census and the FACT-OWNERSHIP rows extending there. Recorded as
  `decision_generated-mirror-needs-tracked-input`; constrains slice (d) the same way.
- The interim evidence, at scratch: the generated module (40,198 bytes) compiles
  standalone and a `rustc --test` harness exercises it behaviorally — reset per the
  document (mode M, mstatus `0xA0000000`, misa at the declared value), the 33-CSR address
  lookup, the view discipline, the field tables (the medeleg 11/16 read-only-0 rows, TSR
  at bit 22 per the pinned encoding.h), x0 hardwired, mode transitions — 4 passed / 0
  failed. Harness and module at `target/p4-system-2/gen/` (untracked, by design).

