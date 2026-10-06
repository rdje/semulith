# DEV_NOTES.md

## _(2026-10-06)_ — the identity proof's RED control is what makes it a proof (P4-SYSTEM.7 slice b)

Slice (b)'s byte-level identity proof (101 pre-slice guests, both CLIs — the
parent worktree's build vs the post-slice build) came back "101 byte-identical,
0 diverge" on its first run. It was also worthless: the harness had passed
`--profile NAME` where the CLI wants `--profile=NAME`, so every one of the 202
runs had failed with the SAME usage-error text — and identical failure output
compares byte-identical. What caught it was the control the proof carried by
design: the two NEW guests (fp-fs-off, fp-fcsr-view) MUST diverge on the parent
engine — the FS gate and the fcsr composition did not exist there — and they
"didn't". A comparison harness whose failure mode is identical on both sides
reports identity on garbage; the must-diverge control is the only arm that can
see it (the a-shorter-trace lesson's sibling: prefix agreement was the green
there, identical errors here). After the fix: 101 byte-identical for real
(5,491 trace lines), both new guests diverging on the parent as required.

Also measured this slice, for the record: Sail puts the FS gate on the DECODE
clause (`encdec … when currentlyEnabled(Ext_F)` — a dynamic state gate at
legality, never a static encoding property), which settled where ours lives
(the permission model for the FP CSRs now; `fp_enabled()` for the binds' arms);
and Sail's `write_fcsr` marks the context Dirty on every FP-CSR write
(fdext_regs.sail:455), the discipline our csr_write now follows.

- **Validation:** the fixed harness re-ran green with the control RED where it
  must be; `cargo test -p semulith-verify run_rv64gc` 4/4 (103/103); STATE-GEN
  29/29 with the new RED arm; `make check` rc=0, `make gate` green
  (DERIVED-COUNTS 430→431 re-derived).
- Promotion: PROMOTED — the must-diverge-control lesson is retrievable
  (docs/knowledge/an-identity-proof-needs-a-must-diverge-control.md + INDEX;
  the map regenerated). The Sail placements are recorded in the leaf's own
  checklist and need no card.

## _(2026-10-06)_ — the FP qualification: two candidates, three lineages, and MPFR is a thing you measure too (P4-SYSTEM.7 slice a)

The `.7` brief's slice (a) measured:

- **The arithmetic core is the easy part; the policy surface is where backends
  differ.** rustc_apfloat matches MPFR on every add/sub/mul/div/fma value across
  all five rounding modes and both widths — 63,752 cases, zero core
  disagreements. Every disagreement was a boundary the crate explicitly does not
  own: LLVM signals opOverflow only for infinite results (IEEE wants the
  magnitude rule — 362 measured cases), format conversion of an sNaN carries no
  NV (24), NaN→int converts to 0 (RISC-V wants max + NV — 340), fmin/fmax's
  signed-zero pair and both-NaN payload are LLVM's conventions (240), and
  format-conversion payloads scale per LLVM where RISC-V canonicalizes (32). A
  backend qualification that stops at "the adds agree" would have missed the
  whole story; the per-op disagreement tables BY NAME are the deliverable.
- **MPFR needed four corrections of its own.** The DON'T-USE MPFR_RNDNA (RNDA
  behavior for the arithmetic ops — RMM rides mpfr_round_nearest_away); the OF/UF
  flags are exponent-range-shaped (computed spec-side against an exact shadow —
  and the shadow needs 2100 bits, not 300: f64max + 1 spans 1024 bits); NaN
  results canonicalize (payloads dropped); the NAN flag is "result is NaN", never
  IEEE's NV. A reference library's flags are ITS semantics — the generator that
  trusts them writes a wrong spec.
- **softfloat's failure is capability, not quality.** Its arithmetic core is
  MPFR-exact where it exists (including the sqrt APFloat lacks), 3-5× cheaper
  per op; it simply has no rounding modes, no flags, no FMA, no 64-bit
  conversions, no min/max — five of §6's explicit requirements. The one family
  it differs on (it clears the propagated NaN's sign; IEEE-unspecified) is
  recorded as its convention, moot for the verdict. The lesson reached the
  knowledge layer as its own card (the candidate-landscape census is a lead,
  the crate's own documents are the measurement surface) — PROMOTED, the kind
  the layer exists for.

promotion: PROMOTED — `docs/knowledge/a-candidate-landscape-census-entry-is-a-lead.md`
(the landscape-census lesson; the MPFR-measurement half lives in the decision record's
own text, which is the durable home for backend-specific facts).
## _(2026-10-05)_ — a designed AGREE is still a measurement, and a clause can live one hop away (P4-SYSTEM.6 slice c)

Execution of the `.6` brief's checkpoint (c) measured:

- **"Sail lands identically" is a hypothesis until the trace agrees.** Decision
  2 promised AGREE by design — Sail's FENCEI is "a nop for the memory model" —
  and the experiment's job was to measure it, not assume it. The measurement
  has two legs before any guest runs: the override validates unchanged
  (Zifencei already true), and Sail's OWN source carries the shall-ignore
  sentence as a comment while its encdec binds the fields as variables — so
  0x0011118F decodes as FENCEI on both sides. Then the traces: 6 AGREE of 6,
  zero non-AGREE cells to name. A designed outcome with zero divergences is
  the easiest experiment to wave through, and the one that most needs the
  numbers written down.
- **A referenced clause is still load-bearing — and its location is not the
  reference.** The brief's pre-condition 2 said the fetch-cache candidate's
  why "says 'without Zifencei'" — the clause actually lives in rv64i's
  verbatim text, which rv64gc's candidate only references. The re-answer would
  have been the same either way, but the imprecision is recorded because the
  census's whole point is that these sentences are checked, not remembered
  (promotion: declined — the re-answered candidate is in the descriptor and
  STATE-GEN re-derives it on every change).
- **The staleness half of an acceptance can be honest as a latitude.** The
  goal asks "when stale state MAY persist" — and the spec's own implicit-reads
  sentence lets a valid implementation cache every fetchable byte forever. The
  rejected option was modelling a caching hart to make staleness executable:
  it would contradict the unit's own `present false` census to demonstrate a
  machine this unit is not. The latitude is pinned by declaration (the
  sentence is located, the choice is named, the census is re-answered), which
  is the whole truth of the position — a fixture for it would have been a lie.

promotion: declined (the durability is the machinery — the six AGREEs re-run
against the materialized override; the acceptance pair is armed by make check).
## _(2026-10-05)_ — the mirror's byte-identity is the point, and a bind can be invisible in its own trace (P4-SYSTEM.6 slice b)

Execution of the `.6` brief's checkpoint (b) measured:

- **The mirror holds .s byte-identical ALWAYS — and that is the discipline, not
  an obstacle.** My first draft restated four .s headers to the bound state, and
  the governor measured every one as MIRROR DRIFT: the base mirror's rule is
  that rv64gc's .s files are byte-identical to rv64i's owners with NO exception
  list, while an .expected.sexp may differ only for a RECORDED re-derivation.
  The `.2` slice-(g) shape was already the answer: the rv64gc-specific reading
  lives in the expectation comment block, never in the mirrored source. The
  decision-3 corrections (dir-selfmod-fence's data fence is not the fetch
  synchronization; fault-selfmod's stale "without Zifencei") landed exactly
  there, with both names joining MIRROR_REDERIVED and the reason recorded
  beside the slice-(f)/(g) reasons (promotion: declined — the durability is the
  machinery: the governor names drift on every gate run).
- **A bind can be invisible in its own trace.** min-fencei's demo trace is
  byte-identical pre- and post-bind: the pre-bind ReservedDecode delivery wrote
  no register and vectored to mtvec=0, so the recorded step (pc, mode, writes)
  is the same tuple as the post-bind retiring nop. The semantic change (a
  trap-conversion vs a retirement) is real and shows in the expectations; the
  trace just has no slot for it. it-fencei carries the visible half: the
  continuation marker commits now (x2 ← 7), exactly as on both references.
- **Memory-backed fetch is a derivation-level discipline too.** The new
  fencei-selfmod guest needs the spec-side model to re-read the patched word —
  the store's effect lands in the program map with the patch named in the insn
  text (the `.2` comment convention, tooled at last). The engine always re-read
  (D-CODE-VISIBILITY); the derivation tool simply had to catch up — a guest
  whose patch the model ignores would derive the WRONG patched step silently.

promotion: declined (the durability is the machinery — the mirror governor and
the 101-guest corpus re-run every one of these).
## _(2026-10-05)_ — "no assembler shapes" was true until the table said otherwise (P4-SYSTEM.6 slice a)

Execution of the `.6` brief's checkpoint (a) measured:

- **A no-change claim must be measured, not inherited.** Decision 1's "no
  assembler shapes (the zero-operand ecall/ebreak precedent)" read true — and
  was FALSE on first probe: ecall/ebreak carry no operand fields, but fence.i's
  table row LISTS imm12/rs1/rd, and the table-driven arity check refused the
  bare standard-software spelling. The chapter itself settles what the correct
  behavior is ("standard software shall zero these fields"), so the acceptance
  landed as a named, cited special case in the assembler — the same shape as
  the A-suffix machinery, never a table edit. The OTHER no-change claims held
  under the same discipline: the nop effect needs no Sem variant (the existing
  arm), and gen_definition's lowering of the one-form fragment needs no
  conditional support at all — the emitted mask covers funct3+opcode only,
  which is exactly the shall-ignore decode, over two standalone-compiling trial
  compositions.
- **The pin's strength is the second measurement.** 73 bytes is one curl — the
  evidence is the fresh re-fetch being byte-identical, the scope-vs-tables leg
  enumerating 87==87 with the table pinned-but-excluded (the named exclusion
  with its flip condition), and the fragment leg agreeing the generated
  zifencei.sexp against the pin. A pin nobody re-derives is a number, not a
  corroboration.
- **The shall-ignore rule is a DECODE property, and both decoders show it.**
  The fragment keeps the operand fields out of the mask, so 0x0011118f
  (nonzero imm12/rs1/rd) decodes as fence.i in the generated module — and
  spike-dasm, the documented second decoder, returns `fence.i` for the same
  word. The reserved-fields probe cell at slice (b) is already sanctioned by
  measurement.

promotion: declined (the durability is the machinery — the zero-operand
acceptance is armed by the probe spellings and the 99-guest byte-exact
re-assembly, both re-runnable).
## _(2026-10-05)_ — Sail numbers the delivery step too, and a named gap can be configuration-shaped (P4-SYSTEM.5 slice d)

The `.5` matched attempt measured:

- **The interrupt-delivery step convention is the fetch-fault convention.** The
  first comparator run "diverged" every i-* guest at its first delivery — Sail
  had no row there. Reading the trace: Sail's numbering JUMPS [9] → [11] at the
  delivery — it numbers the step and prints no row, exactly the `.3` `<fetch
  page fault>` convention. The comparator keys on row numbers (the `.3`
  comparator's own shape); a step no row carries must declare no observation —
  which is precisely what our delivery steps declare. What looked like a
  systematic mismatch was the same declaration in two notations.
- **Every named divergence was platform-shaped, and each had a sentence.** STIP
  needs plat_have_clint (interrupt_regs.sail:250-263) — without a CLINT the
  whole timer block, not just the counter registers, is silent. The halt needs
  a dwell — Sail's wfi is a nop under the matched platform (wfi_is_nop=true, a
  platform declaration, not a shortcut). The TW gap is configuration-shaped:
  under the matched platform Sail NEVER judges TW (the judgment lives only in
  the wait-exit path the nop never reaches); under the wfi-wait variant the
  delivered trap is identical to ours — cause 2, mepc = the wfi's pc, xtval =
  the wfi's word — 30/30. A "reference-model gap" can be the platform both
  sides agreed to declare, and re-measuring it beats inheriting its name.

promotion: declined (the durability is the machinery — the corpus verdicts are
armed by make check; the attempt re-derives from the tracked override).
## _(2026-10-05)_ — the wake is a head evaluation like any other, and the span-zero wake is still evidence (P4-SYSTEM.5 slice c)

Execution of the `.5` brief's checkpoint (c) measured:

- **The WFI-specific mepc rule needs no special case.** §2.1.3.3's "execution
  resumes in the trap handler and mepc = pc + 4" looked like a WFI-only delivery
  path. It falls out of the generic machinery: the WFI RETIRES into the halt (pc
  advanced, instret counted), so the resume's between-instructions delivery writes
  xepc = the hart's pc, which IS the WFI's pc + 4. The halt's whole shape is one
  head evaluation in front of slice (b)'s: waiting → wake? → fall through to the
  ordinary pending evaluation — the same step does wake and delivery, and the
  untrapped resume just executes. One evaluation point, no parallel path.
- **A software-posted source wakes in zero halted steps — and the cell still
  falsifies.** With SSIP posted before the wfi, the very next head resumes, so
  the trace is observationally a nop's. The cell's power is against the WRONG
  wake rule: a wake that required the global enable would stall the guest
  forever, and its expectations (which continue past the wfi) could never derive.
  Evidence strength is not always a trace difference; sometimes it is the
  impossibility of deriving the same file under the false rule (promotion:
  declined — the durability is the machinery: w-sw and the wake suite re-run it).
- **The text-keyed `#|end` is a collision hazard.** mm-wfi's derivation stopped
  26 steps early: stage1's `csrrs x8, mepc, x0` has the same text as the
  fall-through's `#|end` instruction, and the text-keyed marker fired at the
  first occurrence the flow reached. The pc-keyed directives fixed this class
  for derivations at slice (b); the end marker still keys on text — stage1's
  mepc-step moved to x10 to disambiguate. A marker keyed on content will
  eventually meet two identical instructions; the fix is at the guest, never by
  weakening the convention.
- **A gated CSR read is a delivery, not a refusal.** The derivation tool models
  the counter-ACCESS gates (rdtime below M with the gates shut) as the engine's
  own cause-2 trap; the mode-privilege refusal stays for authoring errors. The
  wake corpus reads counters in M only, but the honest mirror is what lets a
  future guest exercise the gate without tooling work.

promotion: declined (the durability is the machinery — the wait/interrupts suites
and the 99-guest corpus re-run every one of these).
## _(2026-10-05)_ — the trap-entry stack runs the other way, and sip cannot clear SEIP (P4-SYSTEM.5 slice b)

Execution of the `.5` brief's checkpoint (b) measured:

- **The derivation tool had the xRET-side stack where trap entry runs the other
  way.** The forked tool's `deliver()` wrote MIE <- MPIE, MPIE <- 0 — mret's
  direction. Trap entry is MPIE <- MIE, MIE <- 0, and the engine's privilege.rs
  had it right all along. The .2–.4 corpora never caught the tool: every prior
  trap fired with MIE=MPIE=0, where the inverted and the correct forms coincide.
  The first guest that enabled interrupts (i-deleg's ecall with MIE=1) nested the
  re-posted SSI INSIDE the M handler and marched mepc into an mret self-loop —
  the tracer showed MIE=1 one step after the ecall, where spec delivery leaves
  it 0. A state-discipline bug hides exactly where every prior execution made
  the wrong and the right form agree; the test that varies the input bit is the
  one that matters (promotion: declined — the durability is the machinery: the
  i-deleg guest and the interrupts suite re-run it).
- **Two read-only bits are load-bearing guest-design facts.** i-vector's
  SEI-to-S cell asked the S handler to clear SEIP through sip — read-only there
  (Computed in the field tables); the engine would have re-delivered forever.
  The guest now rides SEI to M (cleared through mip) and SSI to S (cleared
  through sip) — the same vector evidence with legal clears. And i-accept's
  mtvec delta was 8 bytes long: the delivery landed past the handler's two
  evidence reads and the guest "passed" gutted — caught by reading the
  derivation, not by any verdict. A guest that terminates is not a guest that
  evidenced anything.
- **Authoring against the wrong clock is a silent narrative lie.** i-timer's
  stimecmp=3 assumed time counts the marker instructions; the declared domain
  ticks every step, so time was 5 at that write and STIP never cleared. The
  re-authored guest writes stimecmp=8 and observes 1→0→1 at steps 3→6→8, the
  step counts spelled in the derivations. The same census discipline caught
  S-mode `mstatus` accesses (illegal from S — the guests now ride sstatus) and
  mstatus's UXL/SXL reset bits the tool never modeled (0xA00000000 — the
  runner's first mismatch named them).

## _(2026-10-05)_ — the counters started moving, and a view that masked them appeared (P4-SYSTEM.5 slice a)

Execution of the `.5` brief's checkpoint (a) measured:

- **The `.2` zeros were right for the wrong reason.** mm-counters read 0 at
  every cell because nothing moved — and nothing could have SHOWN a move: the
  architectural CSR read computes a view's exposed mask from the view's declared
  fields, and a field-LESS view masks to zero. The counter views would have read
  0 forever, statements notwithstanding ("a read-only shadow of mcycle"). The
  first timekeeping test caught it (cycle read 0 where the storage held 2,
  rc=1), and the root fix is the statement's own meaning: a view declaring no
  fields is a full-width shadow of its owner (promotion: declined — the
  durability is the machinery: the suite and the corpus re-run it in make
  check).
- **"One tick per step boundary" has exactly one honest reading.** The runner
  executes a count of steps; a tick at every non-Failed outcome makes time at
  executed step k equal k — main flow, handler flow, trapping `.word` steps all
  alike. That is what makes mm-counters' re-derivation mechanical (0/1/2/25/51
  at steps 0/1/2/25/51) and the determinism proof trivial (the domain is a pure
  function of the step index by construction, not by argument).
- **instret's genuine count was already in the engine's vocabulary.** The
  trap-END discipline's `frame.trapped` flag IS "the instruction did not
  complete" — a delivered trap, a faulting fetch, a reserved decode. Retired is
  its negation; no new state was needed, and the trap cells in mm-counters
  (gated reads at 13/39) needed no re-derivation because a trap is not a read.

## _(2026-10-05)_ — the experiment that graded its own policy (P4-SYSTEM.4 slice f; the leaf closes)

Execution of the `.4` brief's checkpoint (f) measured:

- **"AccessFault" is a family, not a number.** Decision 6's reasoning — "the
  override declares AccessFault for the atomic kinds, so uniform cause 7 makes
  the cells AGREE" — measured FALSE the first time `a-lrsc-fault` ran under
  Sail: a misaligned LR came back cause 5, and the exception table says why
  ("load and load-reserved instructions generate load exceptions"). The offered
  choice is misaligned (4/6) OR access-fault (5/7), and within access-fault the
  cause follows the access kind. The bind-day uniform-7 was not a legal option
  for LR at all — and the matched experiment is what caught it, exactly the job
  it exists for. The policy is now kind-matched (LR → 5, SC/AMO → 7) everywhere
  the policy is written down: the engine arm, the schema contract, the state
  document, and the decision record with its verbatim mirrors (promotion:
  declined — the durability is the machinery: the a-lrsc-fault guest and the
  comparator re-run it).
- **A declared policy and a platform extern can honestly disagree.** The width
  cell was the leaf's flagged watch item from slice (c) onward, and it measured
  exactly as flagged: Sail's reservation externs take physaddrbits and no width,
  so `sc.d` after `lr.w` matches and stores; the laboratory's declared
  width-equal policy fails with code 1. Both are legal under §12.1.2's latitude
  — the spec's must-fails key on the reservation SET and implementations may
  fail any unconstrained sequence. The verdict is a named divergence, not a
  defect on either side, and the divergence's downstream is consequential (the
  re-converging recovery pair is the corpus's own consistency proof).
- **The flip condition outlived its slice.** The fetch leg's A exclusion,
  written at slice (a) with the M precedent's shape, flipped on its own the
  moment the census declared the A forms — 87 == 87 the day of the bind, no edit
  needed. A check written against the future state it will judge is the
  difference between a mechanism and a to-do list.

## _(2026-10-05)_ — the bind that fit in one commit, and the formatter that graded the manifest (P4-SYSTEM.4 slice e)

Execution of the `.4` brief's checkpoint (e) — the atomic bind — measured:

- **The flip mechanism is load-tested by construction.** The pieces the earlier
  slices staged each landed once: the slot became an extension; the census dual
  edit (schema + `_SCOPE_LISTS` + the scope block + the PARTS family) read 87;
  the fetch leg's slice-(a) exclusion flipped ON ITS OWN the moment the census
  declared the A forms (87 == 87, rv64i unchanged) — the flip condition written
  six days earlier did exactly what it was written to do. The evaluator arms
  ported byte-identically from the scratch proof, so the tracked engine is the
  proven one, and the 88/88 corpus plus the 16/16 cell proof re-ran against the
  tracked build with the same tallies (promotion: declined — the durability is
  the machinery: the gates judge the bound unit on every commit from here).
- **rustfmt is a generator constraint, not a style preference.** The manifest's
  five-fragment list tripped rustfmt's vertical array layout where the
  four-fragment one had stayed inline — measured: 79 chars inline-clean, 90
  broken. A generator that emits code a formatter would rewrite produces drift
  on every regeneration; the emission now decides the layout by construction
  (the 80-char cutoff), and `cargo fmt --check` inside `make check` is the gate
  that arms it.
- **The identity proof is the bind's spine.** 76 pre-bind guests, both CLIs,
  the parent worktree against the post-bind build: 3,468 == 3,468 trace lines,
  `cmp` clean. Additive extensions are supposed to leave the old corpus alone —
  but "supposed to" is a hope and 3,468 lines is a measurement.

## _(2026-10-05)_ — the corpus grades its author four times before it grades the engine once (P4-SYSTEM.4 slice d)

Execution of the `.4` brief's checkpoint (d) measured:

- **A derivation tool that never applies its writes derives a fiction.** The
  spec-side stepper computed every register write into the expectation and
  mutated nothing — so the next instruction read zeros, and the first run
  "completed" every guest in 5-6 steps. Caught at the first `sw`: the step after
  it left the program. The READS-AND-WRITES contract is what makes the fix
  correct by construction: execute reads the pre-instruction file throughout,
  the writes land after the whole effect (promotion: declined — the corpus
  itself re-runs the rule at the bind).
- **The comparison rule is part of the corpus's vocabulary, not a detail.** The
  runner observes register CHANGES, so a register written its own value is no
  observation — the `.3` "x8-already-zero" rule. Eleven of twelve guests failed
  the first run on exactly this (the aq/rl cells' repeated 41s, the handlers'
  repeated CSR reads). The expectations now derive only observable changes.
- **"Reserved" must be checked against the decode table, not remembered.**
  funct5 0x02 is LR's OWN — my "reserved AMO funct5" `.word` decoded as
  `lr.w x6, (x1)` and executed, reading the handler's first word through a
  register the mtvec setup had consumed (the observed `0x342025f3` named it).
  The genuinely reserved 0x05 replaced it; the census that matters is the closed
  set {0x00,0x01,0x04,0x08,0x0C,0x10,0x14,0x18,0x1C} plus LR 0x02 and SC 0x03.
- **A data PA is an allocation, and allocations collide.** The sv39 guest's data
  leaf pointed at base+0x1000 — the ROOT TABLE's page. Cell 3's own store
  overwrote root[0] with 17, turning it into a leaf with R=0, and every later
  walk faulted on schedule. The fix is the honest one (move the data to
  base+0x4000), and the failure mode is now a named audit step: a guest's data
  addresses and its page-table addresses live in one map.

## _(2026-10-05)_ — the cancellation site is the spec sentence, and the proof grades the tests too (P4-SYSTEM.4 slice c)

Execution of the `.4` brief's checkpoint (c) measured:

- **"Regardless of success or failure" has a boundary, and Sail marks it.**
  Decision 4's invalidation set says any SC clears — but Sail 0.14's execute
  clause (`zalrsc_insts.sail:71-79`) runs `vmem_write` FIRST and cancels only on
  the `Ok(b)` path; the `Err(e)` trap path cancels nothing. The spec sentence's
  "success or failure" is exactly the completed path: an SC that page-faults is
  neither, and the reservation survives. That is also decision 4's own second
  half (a trap does NOT invalidate), now with a reference-model measurement
  behind it — the evaluator arm's clear sites sit after the policy match and
  after a successful store, never on a deliver path, and the scratch proof's
  trapped-SC cell pins it (promotion: declined — the durability is the machinery:
  the proof cell and the reservation module's suite arm it).
- **The scratch proof grades the TESTS as hard as the engine.** The first run
  came back 13/3, and all three failures were mine: an "LR replaces" sequence
  that let the failing SC clear the reservation before the final SC (the engine
  correctly failed it — any completed SC clears); a "trapped SC" cell using a
  mismatched address, which fails with code 1 BEFORE any memory operation — no
  trap exists to observe (the boundary-fault variant, with the address matching
  and the store scripted to fault, tests the real path); and one expected value
  that forgot the final SC's overwrite. A proof that only ever passes teaches
  nothing; the 13/3 run is the evidence the harness discriminates.
- **The AMO needs its own translation kind.** `AccessKind::Store` judges W only
  (translation.rs:374), so an AMO on an unreadable page would have passed
  translation untouched — while RVP-SUPERVISOR demands a store page fault (15,
  never 13). `AccessKind::Atomic` judges R∧W under the store/AMO causes; the
  translation suite's new cells fire all four fault flags.

## _(2026-10-04)_ — the operation is the encoding, and the variant waits for the composition (P4-SYSTEM.4 slice b)

Execution of the `.4` brief's checkpoint (b) measured:

- **The AMO's operation cannot be spelled.** A first draft wrote `(amo add …)` —
  and the checker's walk refused it: `'add' is not an operand this instruction
  has` (rc=1). Every bare-symbol argument in this language is an operand
  reference, so an operation name in argument position reads as a phantom
  operand. The op is the funct5 ENCODING as `(lit N)` — the value the
  instruction's own fixed bits carry — and that choice composes with the
  repository's own rule (a constant that is a function of the pinned tables is
  derived, never typed): `gen_definition`'s `amo_operations` RE-DERIVES the
  closed Zaamo nine from the composed encodings' bits 31..27 and refuses an op
  outside it by name. The sem file cannot invent an operation the pinned tables
  do not carry, and the refusal text lists the derived set (promotion: declined
  — the durability is the machinery: the DEF-GEN RED arms fire the refusal).
- **The variant waits for the composition.** The evaluator's `Sem` match is
  exhaustive with no wildcard (measured: TlbInvalidate is the last arm) — the
  `.2` slice-d wall exactly. Emitting the A variants unconditionally would break
  compilation until slice (c)'s arms exist, so the variants emit exactly when
  the unit's own fragment list composes `riscv/a`: the tracked modules
  regenerate hash-only (the OWN-03 generator pin), the scratch composition
  (base+Zicsr+Zicntr+system+A, untracked) lowers and compiles standalone, and an
  A operator where the composition lacks A is a refusal, named. The mirror stays
  a pure function of the canonical definition — the definition today has no A
  forms, so the mirror has no A surface, and the bind (slice e) lands variants,
  instructions and evaluator arms in one commit.

## _(2026-10-04)_ — the pin that exposed its own census's blind spot (P4-SYSTEM.4 slice a)

Execution of the `.4` brief's checkpoint (a) measured:

- **The scope-vs-tables leg could not see a 64-bit table.** The `extra` collector
  in `fetch_references.sh` tested `n.startswith("rv_")` — so `rv64_a` (and
  `rv64_m` before it) never joined the census the leg enumerates. The gap was
  latent for exactly one reason: no profile had ever declared an A or M form
  while pinning the 64-bit table, so the missing rows never faced a census that
  expected them. The rv64_a pin was the first input that made the gap load-bearing:
  with the collector fixed, the pin broke the leg outright — 87 enumerated vs 65
  declared. Both halves of the fix are the dossier's own precedents: the rv64i
  ledger's declared M exclusion ("pinned for the fragment test case, not the
  scope") extends to the A tables verbatim in shape, with the same flip
  condition — a declared lr./sc./amo form includes them, which is exactly what
  slice (e)'s atomic bind will do when the census grows 65→87. A check whose
  blind spot is found by the first input that needs it is the RED-before-green
  discipline working as designed: the fix was written against the measured 87-vs-65
  failure, not against a reading of the code (promotion: declined — the durability
  is the machinery: the exclusion and its flip condition live in the fetch leg
  itself, and the leg's own verdict arms them).
- **The brief's "aqrl field" is two tokens in the tables.** Every rv_a/rv64_a row
  lists `aq rl` as separate operand tokens; the pinned arg_lut.csv's `"aqrl",26,25`
  is the combined field, and no row carries an `aqrl` (or `amoop`) token. So the
  generated fragment owns `aq` and `rl` — the generator's own rule is that a field
  nothing references invites a reader to believe it is supported — and the
  assembler's suffix rule lands the `.aq`/`.rl`/`.aqrl` value in exactly those
  bits. Deriving from the rows rather than from the brief's shorthand is what kept
  the fragment generated, never hand-authored.
- **spike-dasm prints `lr.w` plain for all four suffix words.** The aq/rl bits are
  measurably set in the emitted words (0x100120af / 0x140120af / 0x120120af /
  0x160120af) and sc/amo print their suffixes back exactly — lr's plain printing
  is spike's own preference, the rdcycle-prints-as-csrr precedent from `.2` slice
  (a). The round-trip is exact for the 22 forms × 4 suffix combinations with that
  one recorded convention.

## _(2026-10-04)_ — the matched experiment that caught its own config (P4-SYSTEM.3 slice e part 2; the leaf closes)

Execution of the `.3` brief's checkpoint (e), part 2, measured:

- **The experiment's first DIVERGE was the override's, not the models'.**
  sv39-deleg came back `sail x22=13 vs expected x7=13` — the delegated page
  fault reached M on Sail. The engine delegates bit 13 (the corpus is green),
  Sail delegates it when allowed — the tracked override's `delegatable_bits`
  0x3FF (causes 0-9, authored at `.2` before page faults existed in the
  corpus) was the stale fact. The laboratory's state.sexp pins 0-10 | 12-15 |
  18-20 WARL-any; Sail 0.14 REFUSES a mask covering its reserved causes, so
  the matched value is the bisection's 0xB3FF (0-9 | 12 | 13 | 15) — the
  widest both sides honor, proven verdict-neutral on the mm corpus before the
  sv39 run went green. The override mirrors the laboratory only up to the
  reference's own validation; the latitude is recorded, never hidden (the
  override-mirror discipline is the rv64i dossier's DIFF-PLATFORM-DEFAULT
  lesson applied — the census before the config, the measurement before the
  claim; promotion: declined).
- **A/D placement is a vocabulary difference, not a behavior one.** sv39-svade
  was the lone non-AGREE: the model's walk faults at step 9 (A=0 → page fault,
  never an update), Sail's `--trace-ptw` prints `Success` and takes the fault
  a step later. Same reads, same delivered trap — where the check is JUDGED
  differs. Recorded as the A/D-placement convention, never normalized away:
  the trace comparison keys on the read sequence, and the architecture leg
  proves the outcomes identical.
- **Sail prints no row for a fetch that page-faults — but numbers it.** The
  step counter jumps across the faulting fetch; indexing the comparison by the
  PRINTED number (never list position) makes the expectations' `<fetch page
  fault>` pseudo-steps exactly the no-row, no-write steps. And the TLB
  dimensions needed no normalization at all: sv39-tlb-fence's 7 adds and 2
  flushes match the laboratory's 4-entry FIFO event-for-event — a stronger
  match than the brief priced (TLB-size/timing differences were budgeted as
  recorded differences; on THIS corpus, Sail's defaults and the laboratory's
  minimal cache produce identical event counts).

## _(2026-10-04)_ — the corpus that made the walk real, and three probe bugs it paid for (P4-SYSTEM.3 slice e part 1)

Execution of the `.3` brief's checkpoint (e), part 1 (the corpus), measured:

- **A guest is a different falsifier than a unit test.** The walk, TLB, MPRV
  and Svade had 25 unit tests; the first full guest (`sv39-translate-4k`, 111
  steps — build five page-table pages in M, csrw satp, drop to S, translate a
  load/store/load, ecall home, then read the walked PTE back in M) passed only
  after the pc-map audit trusted `pc_of` over the printed line index (a label
  occupies an index but no bytes — the print lied, the map was right) and after
  the stage token moved OUT of the S-mode cells: `csrrw mscratch` in S is an
  illegal-instruction trap (cause 2), which the engine delivered correctly.
  The family rule paid again: an unexpected-but-correct trace is a probe bug
  until proven an engine bug. Tokens S must set now travel in sscratch, and
  the handler routes on a two-token scheme.
- **The fetch-count witness had to learn the architecture.** The corpus's
  no-extraneous-fetch assertion was `fetches == steps`. Two real guests break
  it honestly: a step whose FETCH page-faults in the walk issues walk accesses
  but never a `Request::Fetch` (0 for that step), and the straddled
  instruction on non-contiguous pages issues 2. The expectations schema grew
  the optional `fetches` field — the count is a DECLARED observation with a
  parcel-bounds refusal in the generator (RED-armed), never a computed
  allowance — and the 62 pre-slice guests keep the old strictness by default.
  My first model of the coalescing rule (one physical 32-bit unit) was wrong;
  the engine's recorded rule is address contiguity (`pa[1] == pa[0] + 2`), and
  the measured 53 fetches corrected the probe, not the engine.
- **EVD-05 by a spec-side model.** `target/p4-system-2/sv39/sv39gen.py`'s
  `Spec` re-derives the pinned 10-step walk (§11.1.3.2, LEVELS=3/PTESIZE=8 per
  §11.1.4.1), Svade (a needed A/D update is a page fault, never a write), MPRV
  effective mode, medeleg, the region bounds, and the slice-(d) TLB semantics
  in Python — every expectation value comes from the chapters, and the corpus
  runner falsifies all of them. The auipc+addi chain discipline (lui
  sign-extends bit 19; ≤ 2047 per step; fixpoint layout; the audit accumulates
  chains and knows the table targets) is what kept 14 guests' pc maps honest
  (the classes above are the family's recorded probe-bug and pc-map
  disciplines applied, and this slice's checklist carries the instances —
  promotion: declined).

## _(2026-10-04)_ — the cache made the test suite honest twice (P4-SYSTEM.3 slice d)

Execution of the `.3` brief's checkpoint (d) measured:

- **The TLB caught test-design bugs the walk never could.** Two existing
  fault-matrix cells failed the moment the cache was live — and the cache was
  right both times: the SUM=0 cell "faulted" into a legal Physical because the
  previous cell's installed entry answered first, and the A=1,D=1 store "faulted"
  on the D=0 entry the D=0-load cell had installed (the spec's sanctioned
  staleness, exactly as designed). The cells were never wrong about the walk —
  they were wrong about SHARING a hart. Independent outcome cells now run cold,
  and the interaction itself became the Svade-staleness suite (install D=0 via a
  load, the stale store faults on the entry's bit, the fence restores truth) —
  the failure was the specification working, not breaking.
- **Two of my own bugs, two familiar classes.** The fence-instruction test wrote
  `0x12039073` for sfence.vma x3,x4 — rs1 and rs2 swapped by a nibble (the real
  word is `0x12438073`; the wrong one decoded RESERVED and the probe answered
  correctly with a delivered cause 2 to mtvec=0). And the fence-case lookups
  passed full addresses where the API takes page numbers. The cache was
  acquitted on evidence both times; the test took the fix. The discipline the
  family already owns — print the constructed word/address and treat an
  unexpected-but-correct answer as a test bug until proven an engine bug — is
  what closed both in minutes.
- **The census drives the storage, and the gate guards the driver.** The TLB's
  parameters live in the state document's SEM-08 census (the candidate
  re-answered `present true` — the census's own reopen hook, placed at .2), and
  gen_state emits the hart-state field FROM that declaration. The refusal that
  anchors it — a descriptor silent on the cache is refused by name — fired on
  the self-test's synthetic descriptor the moment it landed, and the fixture's
  census now carries the candidate, with a RED arm pinning the refusal. The
  generated module, the trait, and the document can no longer drift apart
  silently in either direction.
- **Validation:** 25/25 translation tests (the walk's 17 plus the TLB suite:
  hit/FIFO/tagging/staleness/Svade-staleness/the four fence cases with
  retentions/the non-canonical no-op/the fence instruction end-to-end/
  determinism tuples identical); the corpus 62/62 and 1,884 == 1,884 trace lines
  byte-clean against the parent engine; STATE-GEN 26/26, DEF-GEN both pairs;
  `make check` 8/8, `make gate` all green (DERIVED-COUNTS 422→423). Promotion:
  declined (both bug classes are the family's own recorded disciplines applied —
  this slice's checklist carries the instances).

## _(2026-10-04)_ — the fault matrix catches the author; the amendment that wasn't there (P4-SYSTEM.3 slice c)

Execution of the `.3` brief's checkpoint (c) measured:

- **The reserved encoding is W-without-R, and the tests said so first.** The
  walk's first draft faulted on R=1 ∧ W=1; the fault-matrix suite (written
  before the implementation, from the pinned §11.1.3.1) named three cells
  PageFault-for-the-wrong-reason in one run. The pinned rule: W=1 requires R=1;
  R=0 ∧ W=1 is the reserved case. EVD-05 held at the test layer — the walk was
  fixed to the derivation, never the tests to the output. The same suite caught
  a second author error of a different class: three leaf constructions missing
  the V bit (V=0 faults correctly — the walk was right, the fixture was wrong).
- **"Supersede the old record" had nothing to supersede.** The brief's
  requirement amendment read like a mirror edit; the measurement
  (`grep -o 'id "REQ-D-…"' | grep -c FETCH` → 0) shows rv64gc's catalogue never
  carried REQ-D-FETCH-IMPLICIT — the slice-(e) mirror closure is 13 records and
  it is not among them. The honest shape followed: a NEW authored
  D-WALK-IMPLICIT + verbatim REQ/OB pair naming the translated composition's
  implicit-access vocabulary, with the owner relationship recorded in the
  statement itself (rv64i's record stays true of rv64i — no translation exists
  there). The mirror rule stayed untouched, which is exactly what it's for.
- **The probe has its own bug class, and it is the auipc class.** Updating the
  slice-(b) Sv39 probe surfaced two of my own construction bugs: stale auipc/addi
  deltas (mtvec landing mid-prologue — the .2 slice-(f) audit's exact class, and
  it fired again on new code) and a `slli` chain that shifted the satp MODE bit
  out of existence (2⁶³+8 ≪ 16 mod 2⁶⁴ drops the top — the trace showed x2 lose
  0x8000000000000000, and the "unexpected" cause-5 answer was the probe's
  correct Bare behavior, not an engine fault). The discipline that ends the
  class is the one the family already owns: print the pc map and the constructed
  CSR value before running anything, and treat an unexpected-but-correct trace
  as a probe bug until proven an engine bug.
- **Validation:** 17 fault-matrix tests (every step's fault path and every
  success path, walk reads counted per scenario, the region byte-identical
  across every Svade fault); the corpus 62/62 with fetch counts unchanged; the
  byte-level identity proof on the walk-live engine (1,884 == 1,884 trace lines,
  cmp clean); RECORD-SCHEMA green on the amendment; `make check` 8/8, `make
  gate` all green. Promotion: declined (the pc-map/constructed-value discipline
  is already the family's recorded rule — this slice's checklist carries the
  instances).

## _(2026-10-04)_ — the enum-addition census; parcels coalesce, the request shape is the contract (P4-SYSTEM.3 slice b)

Execution of the `.3` brief's checkpoint (b) measured:

- **Adding one enum variant is a census, and the compiler is the census-taker.**
  `Request::WalkAccess` broke three exhaustive matches, and each site got its own
  profile's honest answer: FlatMemory ANSWERS it (8-byte aligned region read,
  never a fetch — the one-fetch-per-step census keeps its meaning), the bench's
  Counting census gains a `walks` field (zero on the rv64i bench by construction),
  and rv64i's TestEnv panics named (the base profile has no translation
  machinery — a fixture seeing the variant is a test bug, not an answer). The
  alternative — a wildcard arm anywhere — is the silent-lie shape every gate here
  exists to refuse.
- **The request shape is the contract; the parcel split is machinery under it.**
  Decision 5's 16-bit fetch parcels are required by the C slot's straddle, but
  the corpus pins one `Request::Fetch` per step. The resolution is WHERE the
  coalescing is defined: not "one fetch per step" as an invariant to break and
  apologize for, but "one request whenever both translated parcel addresses share
  one physical 32-bit unit" — a rule that is every case under Bare (byte-exact
  today) and that names the page-straddle case as slice (c)'s own case rather
  than silently coalescing it. The proof is two-layer: the fetch-count
  assertions (1/step, every guest) and a full byte-level diff — both CLIs, the
  parent commit's and this one, over all 62 guests: 1,884 == 1,884 lines, `cmp`
  clean. "Bare is an exact identity path" is now a byte-measured sentence, not a
  design hope.
- **The unimplemented case names its slice.** A scratch probe (satp.MODE=Sv39,
  drop to S, `ld`) produces `model error: Unimplemented { what: "Sv39 translation
  — the walk is P4-SYSTEM.3 slice (c)'s" }`, cli rc=1 — the machinery shell's
  honesty: the walk entry can never answer wrong, because it answers by name.
- **Validation:** 6 translation unit tests (Bare-identity, M-never-translated,
  the sub-M walk entry, MPRV selects MPP for data accesses only with SUM/MXR
  carried, the out-of-vocabulary satp.MODE named panic, the 12/13/15 vocabulary);
  the corpus 62/62 with fetch counts unchanged; `make check` 8/8 groups;
  `make gate` all green (DERIVED-COUNTS 422 unchanged — the new arms are cargo
  tests, not gate census members); smoke-bench 53 arms, bench wasm, both books.
  Promotion: declined (the enum-addition ripple is structural — the compiler
  names every match site, and this slice's checklist records the dispositions).

## _(2026-10-03)_ — the override must name what it depends on (P4-SYSTEM.3 slice a)

Execution of the `.3` brief's checkpoint (a) measured:

- **Sail's default had Svade on all along.** The .2 override's template-driven
  generation set every extension it named — including `Svade supported: false` —
  so the .2 experiment ran with the hardware-update policy (irrelevant then: no
  guest activates translation). But the default config's `Svade.supported` is
  `true`: had the template not named it, the .2 config would have silently
  inherited the Svade policy. The flip to `true` is the D-SVADE match — and the
  discipline it crystallizes: a matched override NAMES every flag its experiment
  depends on, because inheriting a default is a silent config, not a chosen one.
  The re-run is the proof the flip is behavior-free for this corpus: 11/12 AGREE,
  byte-identical verdicts to the pre-flip baseline (measured, never assumed).
- **The refusal arm's fixture must pass the mapping first.** The first
  validate_gc refusal arms failed for the wrong reason — my synthetic
  `(hardware_stack (placeholder true))` was refused by the dossier MAPPING
  (`missing (levels …)`) before validate_gc ever ran. A RED arm proves the right
  refusal only when its fixture is valid up to the layer under test: the arms now
  inject mapping-valid construct shapes, so the refusal that fires is
  validate_gc's own, named. (The same discipline the acceptance boxes' census
  arms already carry — a RED against the wrong layer is a GREEN lie wearing red.)
- **The ISA string is the declared order, and the brief's string was checkable.**
  gen_platform's rule (the .1 fix): single-letters concatenated, multi-letter
  underscore-joined, Z* before S*, alphabetical within. Appending Svade after
  Sstc yields exactly the brief's `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade` —
  the brief's own string was right, and the rule re-derived it rather than
  trusting it. The census (`git grep -l 'rv64imafdc'` over seven trees) found two
  authored occurrences to amend (with owners named), two Sail-DEFAULT mentions to
  leave (not our string), one archive to leave, and no derived surface to
  regenerate (no board pins rv64gc today).
- **Validation:** the dossier flips schema-valid and RECORD-SCHEMA green (rule 4
  statement-identity, rule 9 restatement, the D-SV39 note correctly NOT
  mirrored); the override flip config-valid; the full 12-guest re-run
  baseline-identical; STATE-GEN 22→25 arms, both real pairs byte-identical;
  `make check` 8/8, `make gate` all green (DERIVED-COUNTS 419→422 re-derived).
  Promotion: declined (the matched-override name-your-flag discipline is the
  reference dossier's own record, and this slice's checklist carries the
  measurement).

