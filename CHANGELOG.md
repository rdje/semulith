# CHANGELOG.md

## SEMULITH-P4-0044 (leaf P4-SYSTEM.7, slice c3 part 2) — the semantics language learns FP; f.sem.sexp; the gated lowering; the assembler's derived register files

- `schema/semantics.sexp`'s floating-point block: the FP-state contract stated once (f-file
  reads pre-instruction, writes mark FS Dirty, the Off gate judged at the head of any rule
  that touches FP state, sticky accrual with Precise dirtiness, NaN-boxing in the tree, the
  reserved-rm policy) and 18 operators (freg fbox funbox rounding fadd fsub fmul fdiv fsqrt
  fmadd fmin fmax feq flt fle fclass f2i i2f).
- `definitions/riscv/f.sem.sexp`: the 30 F rules, cited (26 quotes judged by CITATION-QUOTES,
  0 findings). `check_semantics.py`'s `check_fp`: an rm-carrying encoding must resolve
  `(rounding (field rm))`; literal formats/widths/signedness; one register file per operand
  (+6 arms, 23/23).
- `gen_definition.py`: the `Surface` bundle; the F lowering and Sem variants emitted only
  when `riscv/f` is composed (+8 DEF-GEN arms, 31/31); `check_fp` re-derived; the module's
  form count derived (62) — the typed "43" had been wrong (44) since `.4` slice b.
- `riscv_asm.py`: an operand is spelled `f0..f31` exactly when its rule names it through
  `(freg …)` (derived from the composed semantics; the other spelling refused by name);
  `rs3`/`rm` supported. 30/30 F forms round-trip through spike-dasm. Both definition modules
  and both guest fixtures emission-neutral; `make check` + `make gate` green (455 arms).

## SEMULITH-LC-0003 (leaf LIVE-CONTAINMENT.3) — TOOLBOX and DOCTRINE_ENFORCEMENT partitioned behind bounded indexes

- `DOCTRINE_ENFORCEMENT.md` (32,669 / 32,768 B): the 35 long-form project-doctrine rows
  moved verbatim into `docs/doctrines/` (governance / definition / evidence / board); the
  parent keeps a complete id → family index. REGISTRY-MIRROR gains a project-scoped mirror
  and judges the families' union (13/13 arms; RED on a removed row).
- `TOOLBOX.md` (20,478 / 20,480 B): the 76 tool rows moved verbatim into `docs/toolbox/`
  (governance / definition / composition / execution) behind a family index. A first pass
  dropped one row (its first cell had no backtick) and a census reusing the mover's filter
  missed it; a positional census caught it and the move re-ran from HEAD.
- Both families registered (partitioned, per-part bounds); "Adding a doctrine" and the
  add-a-tool note point at the families; LIVE_STATUS 36 destinations / 451 arms; `make
  gate` green, `make book` rc=0.

## SEMULITH-LC-0002 (leaf LIVE-CONTAINMENT.2) — the stale orientation sources corrected

- `knowledge-map/subsystems.md` (the one hand-curated input to the derived Knowledge Map)
  described a `crates/app/` scaffold placeholder that does not exist; it now names the four
  real crates (roles and the CLI's nine subcommands read from the sources), the
  definition fragments + semantics, the six unit directories, schema/materials, and the
  two book families. `KNOWLEDGE_MAP.md` regenerated.
- The workspace `Cargo.toml` header no longer tells the reader to replace a starter crate;
  `README_POLICY.md`'s adoption note states the measured ceiling firings instead of "no
  measured pressure … 16,228 bytes", and routes the doctrine adoption to
  `LIVE-CONTAINMENT.4` (the policy decision itself unchanged). `make check` + `make gate`
  green.

## SEMULITH-LC-0001 (leaf LIVE-CONTAINMENT.1) — the closed-tree register: completed trees leave the index

- New tree `LIVE-CONTAINMENT` (true and bounded live surfaces; four leaves). Its first
  leaf applies `docs/TASK_TREE.md`'s own registered control — "completed trees leave the
  index" — which had never been applied: FRONTIER-SYNC's CLOSURE rule required an index
  row for every tree, so obeying the registry would have failed the gate.
- The 22 completed rows moved verbatim into `docs/TASK_TREE_CLOSED.md` (registered: health
  8 / ceiling 16 KiB); the index 8,172 → 4,053 B. FRONTIER-SYNC gates both files (CLOSURE
  over the union; COMPLETED IN INDEX, OPEN TREE IN REGISTER, DUPLICATE ROW; 20/20 arms) —
  RED 22× on the real pre-move index. COMMIT.md, TASK_TREE_README.md and the book's
  task-tree chapter (both anchors included live) describe the move.

## SEMULITH-CA-0001 (leaf CITATION-ACCURACY.1) — the quoted-phrase-in-section gate: CITATION-QUOTES registered

- New tree `CITATION-ACCURACY`, owning the gap `P4-SYSTEM.7` slice (c3) part 1
  measured: a locator can resolve and still name the wrong section, and no gate read
  quotes (`check_citations.py` checks the semantics files' locators for existence only).
- `scripts/check_citation_quotes.py` judges every quoted phrase a tracked `.sexp`
  attributes to a pinned section (four decidable attribution rules; ellipsis pieces in
  order; case/whitespace/quote/dash folding and zero-width removal, both renderings
  measured on the pinned pages); a miss names where the phrase actually is.
- `scripts/check_citation_quotes.sh` — the 35th project doctrine: 14 controls on
  synthetic pages (a matcher mutation turns 6 red), a NAMED SKIP without the pinned
  pages. RED on the real pre-fix corpus: 6 misses, each "found in §20.1.2". HEAD: 24
  quotes judged, 0 findings. Mirrors: DOCTRINE_ENFORCEMENT.md, the book's doctrine
  chapter, TOOLBOX.md, LIVE_STATUS (35 doctrines, 445 arms). `.2` (the Markdown
  census) proposed.

## SEMULITH-P4-0043 (leaf P4-SYSTEM.7, slice c3 part 1) — the FP-CSR locators corrected

- The pinned F chapter numbers the fcsr section §20.1.2 (§20.1.1 is "F Register
  State"); the D chapter numbers FLEN=64 §21.1.1 (§21.1.2 is NaN boxing). Slice
  (b)'s locators — carried into c1 — cited §20.1.1 for fflags/frm/fcsr content in
  the state document (9 lines), both FP guests' directives (and so their derived
  expectations), a privilege.rs doc comment and a unit-test comment, and §21.1.2 for
  FLEN=64. All re-cited; both guests re-derived (sources only, every value
  byte-identical); the hash-pinned mirrors regenerated; 103/103.
- The class was invisible to tools: `check_citations.py` resolves only the
  semantics files' locators, and only by existence. Owned by the new
  `CITATION-ACCURACY` tree (a quoted-phrase-in-section gate), executed next.

## SEMULITH-P4-0042 (leaf P4-SYSTEM.7, slice c2) — the rv_f/rv64_f re-pin + the f.sexp fragment

- `rv_f`/`rv64_f` re-pinned in the rv64gc ledger through the tracked `extensions/`
  fetch route (3,050/320 B; a fresh re-fetch byte-identical): the F extension's 30
  forms (26 RV32F + 4 RV64F conversions). The census leg's named exclusion extends
  to them until the F bind grows the scope (RED-proven: without it the leg reads
  118 vs 88, exactly the 30 F names).
- `definitions/riscv/f.sexp` generated by `gen_fragments.py`: requires the base,
  owns `rs3` (31..27) and `rm` (14..12); the register-file class of `rd`/`rs1`/`rs2`
  is left to the semantics. The 13 upstream pseudo rows are written out, not
  carried (the rv64i policy). The other seven fragments re-derive byte-identical;
  the 115-form trial union is collision-free; both profiles verify; `make gate`
  green. No Rust touched — the slot stays declared until slice (c6).

## SEMULITH-P4-0041 (leaf P4-SYSTEM.7, slice c1) — frm holds any 3-bit value: slice (b)'s WARL retention fixed at root; the slice (c) split recorded

- **The defect, measured against the pinned chapter**: slice (b) declared `frm`
  WARL one-of 0..4 (an illegal write retaining the old value); RVI-F §20.1.2 says
  FSRM writes "the three least-significant bits of integer register rs1 into frm"
  and names 101–111 dynamic reserved rounding modes — values frm must hold. Fixed
  at the declaration (`(legalize (any))`, the sentence quoted), the generated
  state mirror and the definition manifest regenerated, the privilege unit tests
  rewritten to the spec rule.
- `fp-fcsr-view` re-derived spec-side first (the authoring tool corrected) and
  RED against the unfixed engine (fcsr `0x45` vs the spec's `0xE5`), green after;
  its step 13 now also exercises fcsr's ignored bit 8. Both FP guests' headers
  corrected (they named "P4-SYSTEM.5 … the interrupts corpus"); the authoring
  tool refuses a `"` in a directive by name.
- The reserved-rm policy recorded: the pinned revision makes it "reserved"; the
  laboratory takes illegal-instruction (still valid per the spec; Sail's
  `Fcsr_RM_Illegal`) — stated in the operator contract at slice (c3).
- The slice (c) execution split recorded in the tree (c1–c6; the FS gate judged
  at the head of any instruction whose rule touches FP state). Book: the
  duplicated `## Gate CPU-SYSTEM` heading and the stale `.3`/`.4` "underway"
  headings fixed; the `.7` section records the correction. Knowledge card
  promoted. 103/103; `make check` + `make gate` green.

## SEMULITH-AC-0059 (tree ARTIFACT-CLEANUP) — the 2026-10-06 §8 run: 192 incremental caches deleted (607 MB)

- The ~24 h trigger fired (the `2026-10-04` record was two days old). The census found
  192 cargo incremental `.bin` caches (607 MB; 144 `target/debug`, 36 wasm32, 12 the `.7`
  slice-(b) scratch probe's own cargo build under `target/p4-system-7/`), all under the
  enumerated `*/incremental/*` scope, deleted; 0 stray `.bin`/`.log` in
  `target/release`/`target/debug/deps`. 62 `target/refs/**/*.log` (2.2 M, evidence trails)
  and the 7 cargo-home crate fixtures (inputs) kept by standing policy.
  `docs/ARTIFACT_CLEANUP.md` overwritten with the dated one-line record; `target`
  4.8 G → 4.2 G, `.app-data` 1.4 G unchanged.

## SEMULITH-P4-0040 (leaf P4-SYSTEM.7, slice b) — the FP state: the f-file census-gated, the FS gate live, the fcsr two-owner view fixed at root

- The f0–f31 register file (FLEN=64, the LP64D ABI) is declared in the state
  document (the new `fp_registers` construct through `schema/state.sexp`, the
  dossier mapping both directions, and gen_state's validation/emission) and
  carried as hart state under the census discipline: the 4th
  `REQUIRED_CENSUS_CANDIDATES` entry with its RED arm (STATE-GEN self-test
  28→29), the SEM-08 candidate re-answered in place, the generated module
  gaining the field, the reset, `read_f`/`write_f`, and the `PrivilegedHart`
  accessor. Observation stays through the x-registers (the leaf's decision 8).
- Both latent defects fixed at root, re-measured live first (the scratch probe
  on the parent engine): **the FS gate** — `permitted()` answered Ok to all six
  fflags/frm/fcsr read/write combinations at FS=Off; the new arm refuses them
  (the Off-state sentence; Sail 0.14's placement measured: the gate rides
  decode-time legality, `fdext_control.sail:19`, so the instruction side is the
  `fp_enabled()` hook the F/D binds' arms call — no FP instruction decodes yet,
  and the FS=Off instruction cells land at slice (c), recorded). **The fcsr
  view** — the engine resolved the comma literal `"fflags, frm"` as one CSR name
  (reads 0, writes refused); the resolution now composes the owners' field
  blocks in list order (read: fflags[4:0] with frm[2:0] above) and splits writes
  back under each owner's own table (frm's one-of 0..4 judges its slice).
  FP-CSR writes mark FS=Dirty (Sail's `write_fcsr` → `dirty_fd_context`,
  fdext_regs.sail:455); SD follows, being computed. fflags' sticky accrual and
  frm's dyn/reserved-rm resolution are stated in the document for slice (c)'s
  operators.
- The corpus: `fp-fs-off` (the gate's cause-2 cells, the FS transitions, SD
  observed reacting to FS writes) and `fp-fcsr-view` (the 0x7f compose, the
  split write, the frm retention) — 103/103, expectations derived spec-side
  (EVD-05) by the forked derivation tool; both ride the existing seven matrix
  axes. The identity proof: the 101 pre-slice guests byte-identical against the
  parent engine (both CLIs, 5,491 trace lines); the RED control — the new guests
  MUST diverge there — fired, and first caught the identity harness's own
  `--profile=` option-syntax bug (two identical usage errors are not identity).
- `make check` rc=0 (8 groups; semulith-core 134/134), `make gate` green
  (DERIVED-COUNTS 430→431 re-derived; DEF-GEN re-derived after the descriptor
  change; rv64i's surfaces byte-identical), bench wasm 134,105 bytes,
  smoke-bench 53 arms ok, both books. Next: slice (c) — THE F BIND.

## SEMULITH-P4-0039 (leaf P4-SYSTEM.7, slice a) — the backend qualification: rustc_apfloat QUALIFIED by measurement

- The candidate landscape re-measured against the fetched artifacts (the census's
  web claims were leads): `rustc_apfloat 0.2.3+llvm-462a31f5a5ab` (updated
  2025-06-11, ~6.3M downloads; Apache-2.0 WITH LLVM-exception, LICENSE-DETAILS.md
  recording the port's provenance; forbid(unsafe_code), no_std, pure-value API)
  and `softfloat 1.0.0` (koute, 2023-11-03; MIT OR Apache-2.0; musl-libc lineage
  via const_soft_float — EVD-04-clean). The negatives re-confirmed from the
  metadata: softfloat-sys/softfloat-wrapper are Berkeley C FFI; softfloat-pure
  does not resolve. One census claim measured UNVERIFIABLE (softfloat's
  "TestFloat-verified upstream" — the crate's own documents carry no such
  statement; recorded, not counted).
- The capability measurement (the extracted sources): softfloat has NO rounding
  modes, NO exception flags, NO FMA, NO 64-bit int conversions, NO min/max — five
  of ARCH §6's explicit requirements; rustc_apfloat carries the whole surface
  EXCEPT sqrt (never ported) and two measured LLVM-vs-IEEE flag deviations
  (opOverflow only for ±inf results; no NV on sNaN format conversions). The
  **correctness tables** (63,752 cases vs MPFR, directed + seeded streams, per op
  × 5 modes × f32/f64): the arithmetic core (add/sub/mul/div/fma values, all
  modes, both widths) has **ZERO disagreements**; the 612 value disagreements are
  all model-layer policy surfaces (NaN→int 340, fmin/fmax signed-zero +
  both-NaN canonical 240, NaN payloads on format conversion 32) and the 386 flag
  disagreements are the two named deviations. softfloat vs MPFR on its 4,416-case
  shared set: 68, ALL the NaN-sign family (its arithmetic core is MPFR-exact
  where it exists, INCLUDING sqrt — the bar fp.rs's own sqrt must match).
- The MPFR path, recorded: no CLI/gmpy2/mpmath on this host — the system Homebrew
  libmpfr 4.2.2 driven by a scratch C generator with MPFR's own semantics
  measured and corrected spec-side (the DON'T-USE MPFR_RNDNA, the
  exponent-range-shaped OF/UF flags, the NaN canonicalization, the NAN-flag-is-
  not-NV mapping). Timing on this host: apfloat f64 add 10.1 / mul 10.5 / div
  40.7 ns/op (fma 15.7, conversions 3.5-5.4); softfloat ~3-5× cheaper where it
  exists. Both candidates build clean for wasm32-unknown-unknown (PORT-WEB).
- **The decision record** (`docs/decisions/decision_fp-backend-qualification.md`
  + INDEX; the candidate-landscape lesson PROMOTED to
  `docs/knowledge/a-candidate-landscape-census-entry-is-a-lead.md`): the FP
  backend is rustc_apfloat, pinned `=0.2.3+llvm-462a31f5a5ab`; the model layer
  (fp.rs, slice b) owns the RISC-V target policy AND the named deviations;
  softfloat disqualified on capability; the fallback stays named. The dependency
  lands in semulith-core (Cargo.lock 4 → 7 packages: rustc_apfloat + bitflags +
  smallvec; the cargo home stays on-volume), the lib.rs re-export as the
  compile-use. `make check` rc=0, `make gate` green (DERIVED-COUNTS 430
  unchanged), make bench wasm 133,715 bytes + smoke-bench 53 arms + both books.
  Next: slice (b) — the FP state (the f-file + FS gating + the fcsr fix +
  fflags/frm semantics + the census re-answer) with the FS=Off corpus.

## SEMULITH-P4-0037 (leaf P4-SYSTEM.6, slice c) — the matched experiment 6 AGREE of 6; the LEAF CLOSES

- The Sail matched experiment for the fence.i surface — decision 2's designed
  AGREE measured, not assumed. The override is measured first (materialized
  fresh from the tracked unit, unmoved since bfa6aaa; validate-config rc=0;
  Zifencei supported true; NO change needed); sail's FENCEI measured in source:
  its encdec carries the fields as VARIABLES (decoded-not-fixed — the
  shall-ignore sentence quoted in its own comment), and its execute is a nop
  for the memory model. Against the matched configuration, **6 AGREE of 6**:
  it-fencei 3, min-fencei 1, fencei-reserved 2, fencei-selfmod 8,
  fault-selfmod 7, dir-selfmod-fence 8 — 29 steps' change-observations exact,
  the patched fetch reading the new value on both engines; ZERO non-AGREE
  cells. Verdict-neutrality measured: the wider corpus's expectations are
  unmoved since their verdicts (the bind touched only the fencei surface).
- The fetch-cache census candidate is re-answered in place (decision 6):
  Zifencei declared AND bound; the re-read choice stays laboratory policy;
  FENCE.I's nop is the unit's sanctioned implementation of the synchronization
  (the consequence line unchanged; gen_state re-derived, build rc=0). One brief
  phrasing measured imprecise and recorded: pre-condition 2's 'without
  Zifencei' clause lives in rv64i's verbatim text, referenced by the candidate,
  not in the candidate itself. references.sexp records the fifth experiment
  (difference-free re-measured: 0 difference records).
- **The LEAF ACCEPTANCE closes**: rewrite-code fixtures with and without the
  architectural synchronization, measured on BOTH engines — WITH:
  fencei-selfmod's fence.i retires between the store and the fetch, the patched
  word reading 7 on both; WITHOUT: fault-selfmod's patch visible with no
  synchronization, D-CODE-VISIBILITY named (the laboratory's declared legal
  subset). The staleness half is answered as the declared latitude: intro.html's
  implicit-reads sentence lets a valid implementation cache every fetchable
  byte forever, and modelling such a hart would contradict the unit's
  always-coherent census (rejected at the brief). `make check` rc=0, `make
  gate` green (DERIVED-COUNTS 430 unchanged), RECORD-SCHEMA 20,
  PROFILE-CONSISTENCY 5, smoke-bench 53 arms, bench wasm, both books. Frontier
  → `.7` (floating-point backend qualification — the design brief first,
  starting from the routed-in SoftFloat shared-ancestry measurement).

## SEMULITH-P4-0036 (leaf P4-SYSTEM.6, slice b) — THE BIND: the unit composes riscv/zifencei

- The slot becomes the extension and fence.i is legal in the tracked engine.
  encoding.sexp's `(slot (id zifencei) …)` becomes `(extensions "riscv/zifencei")`
  (four slots stay, partial stays, the header's census restated); the census dual
  edit 87→88 lands in all four places (schema/profile.sexp +
  dossier_sexp._SCOPE_LISTS + the scope block + PROFILE-CONSISTENCY's PARTS key —
  the one-form zifencei_fencei family, RVI-ZIFENCEI §4.1);
  `definition_rv64gc.rs` regenerates with fence.i over the existing `Sem::Nop`
  (mask 0x0000707f — the shall-ignore decode, the manifest cascade);
  REQ-GC-FENCEI + OB-GC-FENCEI with no new D-* decision (the nop is the sem
  file's stated decision — the wfi-nop precedent; RECORD-SCHEMA both files ok).
- The fencei guests re-derive to the legal fence.i — the `.2` slice-(g)
  pre-commit FULFILLED: it-fencei grows 2→3 steps with the continuation marker
  committing (x2 ← 7, exactly as on both references); min-fencei is one retiring
  nop — and its demo trace stays byte-identical anyway (the pre-bind delivery
  wrote nothing observable at mtvec=0, measured). `fencei-reserved` exercises
  the shall-ignore decode end-to-end (0x0011118F ignored); `fencei-selfmod` is
  the acceptance pair's WITH member (the store, the legal fence.i, the patched
  fetch reading 7 through the new memory-backed derivation); fault-selfmod
  stands WITHOUT. The decision-3 comment corrections land as RECORDED mirror
  re-derivations — the governor measured my direct .s edits as drift: the mirror
  holds .s byte-identical to rv64i's owners ALWAYS, so the bound-state story
  lives in the expectation comment blocks (dir-selfmod-fence's data fence is
  not the fetch synchronization; fault-selfmod's stale qualifier corrected).
- The fetch leg's exclusion flipped on its own (88==88, rv64i 52==52); the
  corpus reads **101/101**; the identity proof holds 98/99 (it-fencei the
  designed exception, worktree removed); the matrix resolves 28 cells;
  EXERCISE-COVERAGE 88/88; EXTRACTION ok; GUEST-GEN 16/16; UNIT-COMPOSITION 3;
  SHARD-FREEZE 186 rows. `make check` rc=0, `make gate` green (DERIVED-COUNTS
  430 unchanged).

## SEMULITH-P4-0035 (leaf P4-SYSTEM.6, slice a) — the rv_zifencei re-pin, the one-form fragment, zifencei.sem.sexp, the zero-operand assembler acceptance

- The re-pin: `rv_zifencei` through the tracked `extensions/` fetch route — 73
  bytes, exactly one row (`fence.i imm12 rs1 14..12=1 rd 6..2=0x03 1..0=3`,
  sha256 be2d8f72…), recorded in references.sexp with the supplies amendment; a
  scripted fresh re-fetch byte-identical. The fetch leg gains the named
  zifencei exclusion (the M/A pattern — pinned for the fragment, not the scope,
  until slice (b)'s bind flips it): both profiles' `--verify-only` green,
  87==87 and 52==52, "owned fragments agree with the pinned upstream".
- The FRAGMENTS entry generates `definitions/riscv/zifencei.sexp` — owns NO
  operand fields (imm12/rs1/rd are the base's), requires rv64i, funct3=1
  against fence's 0; the six existing fragments re-derive byte-identical.
  `zifencei.sem.sexp` lands hand-written with `(effect (nop))`: the three
  normative sentences, the coherent/uncached-RAM latitude (a re-read-per-fetch
  machine has nothing to flush) and the shall-ignore rule, every sentence
  re-located in the pinned chapter (Version 2.0); citations resolve offline
  (RVI-ZIFENCEI §4.1 ×1; corpus 6 files / 8 resolutions).
- One brief claim measured FALSE as written: decision 1's "no assembler
  shapes" — the row's operand list refused the bare standard-software spelling,
  so the zero-operand acceptance lands as a named, cited special case in
  `riscv_asm.py` (the A-suffix precedent's shape): bare `fence.i` → 0x0000100f,
  the full spelling unchanged, 3 named RED refusals, the spike-dasm round-trip
  exact including the shall-ignore word 0x0011118f. The OTHER no-change claims
  measured TRUE: no Sem variant, no generator change — gen_definition emits
  fence.i with mask 0x0000707f (funct3+opcode only — the shall-ignore decode)
  over the existing `Sem::Nop`, rustc rc=0 over both trial compositions.
- check_encoding_disjoint COMPOSEs base+zifencei (53) and the profile's set
  +zifencei (85+3); check_semantics pair 1/1 and both --compose green; all 99
  guests re-assemble byte-identical. The slot STAYS declared, the census STAYS
  87, no corpus, no Rust. `make check` rc=0, `make gate` green (DERIVED-COUNTS
  430 unchanged).

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

