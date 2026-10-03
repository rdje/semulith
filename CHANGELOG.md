# CHANGELOG.md

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

## SEMULITH-P4-0006 (leaf P4-SYSTEM.2, slice c1) — the privileged state constructs, the staged 33-CSR document, gen_state's rv64gc branch, the csr-set and reset-census gate arms

- Slice (c) split, recorded in the tree: **(c1)** schema + document + generator + gates,
  zero Rust; **(c2)** the engine-side consumption follows. `schema/state.sexp` gained
  `privilege_mode` (the current mode is hart state, not a CSR — the xPP/xPIE/xIE stack
  lives in mstatus) and the `csr` construct with per-field WPRI/WARL/WLRL tables
  (RVP-CSR §1.1.3.1–3), legalization rules, resets and locators per field, and `view_of`
  for the view CSRs (sstatus/sie/sip, the counter shadows — a view declares no storage).
- The rv64gc state document is authored and fully validated from `target/p4-system-2/`
  (placing it in profiles/ is a refused route contradiction until the flip): all 33 CSRs
  of D-CSR-SET with their tables — mstatus/sstatus with the stack and TSR/TW/TVM gates,
  mtvec/stvec BASE/MODE, medeleg with the brief's pinned delegatable subset (11 and 16
  read-only 0), mepc/sepc bit-1 writable at IALIGN=16, misa read-only at the declared
  value (a stated laboratory WARL choice), satp MODE restricted to Bare|Sv39, STCE, the
  counter-enables, the FP CSRs present-with-reset (behaviour is `.7`'s); §2.1.4's
  architectural resets cited, every UNSPECIFIED reset a stated laboratory value; the
  SEM-08 hidden-state census re-earned, naming what each later slice reopens.
- gen_state.py emits both profiles: rv64i's `state.rs` re-derives byte-identical; rv64gc
  emits (storage/mode/resets/field tables as data) to a scratch `--out`, rustc-clean —
  emission into crates/ switches on in (c2). The generator composes per-field resets and
  cross-checks the csr-level value; it fired RED *naturally* on the document being
  authored (mstatus's composite 0xA0000000 vs the hand-computed 0x300000000 — the
  descriptor was wrong, the check named it). Gate gaps closed: PROFILE-CONSISTENCY's
  csr-set cross-check, both directions (+3 self-test arms, 44 total; plus a `--csr-cross`
  staging probe), EXTRACTION's reset leg counts csrs and the mode (+3 arms), STATE-GEN
  +7 arms (17 total).
- Validation: all focused gates green, `make gate` green (DERIVED-COUNTS 385→395 arms).
  CSR name↔address ownership: migration deferred to the flip (a fact-ownership row cannot
  name an untracked owner); the state document's map is proven against the pinned
  csrs.csv (33/33 exact) and the probe is recorded in the leaf.

## SEMULITH-P4-0005 (leaf P4-SYSTEM.2, slice b) — the semantics language learns privilege: 8 operators, the zicsr/zicntr/system sem files, ECALL/EBREAK refined by declaration

- `schema/semantics.sexp` grew from 32 to 39 forms, each operator's meaning tied to the
  pinned chapters: `(field X)` (a raw operand field — the csrrs "rs1=x0 shall not write"
  discipline is a fact about the field, not the register), `(inst)` (the instruction word,
  for illegal-instruction xtval), `(mode)` (current privilege 0/1/3), `(csr-state a)` (the
  machine's own state read — no permission model, no recursion through the gates),
  `(csr-read a)` / `(csr-write a v)` (the architectural CSR access under a UNIFORM
  permission model: address mode bits and read-only bits per RVP-CSR §1.1.1, counter-enable
  gates, TM/STCE on stimecmp, TVM on satp — every CSR instruction gets it once),
  `(trap-deliver c t)` (delegation selection, the xPIE/xIE/xPP stack, xepc/xcause/xtval,
  pc←xtvec), and `(xret x)` (the §2.1.3.2 privilege-stack pop incl. the MPRV clear). The
  language's READS-AND-WRITES contract is now stated: register reads see the
  pre-instruction register file (the csrrw swap is exact even for rd==rs1); no RV64I rule
  changes meaning.
- Three authored sem files, every rule locator-cited and resolution-checked: `zicsr.sem`
  (the read/write side-effect disciplines, RVI-ZICSR §5.1.1; ECALL/EBREAK refined by
  declaration — MODEL-COMPOSE.6's anticipated case — cause 8/9/11 by mode, ebreak tval=pc,
  both measured on the references), `zicntr.sem` (the pseudo-semantics mechanism, measured:
  a pseudo specializes csrrs by NAME — no refines possible or needed — exact because the
  counter gating lives in csr-read), `system.sem` (mret M-only, sret M/S + the TSR gate;
  wfi a stated NOP-when-legal, illegal in U and in S with TW=1, the spec's latitudes
  resolved for trapping under laboratory authority; sfence.vma's invalidation a stated NOP
  — no translation caches exist yet, Sv39 is `.3`'s). The WARL seam is recorded: csr-write
  legalizes under slice (c)'s per-field tables, applied at slice-(d) lowering.
- Measured in execution, fixed at root: the semantics corpus gate's COMPOSE leg carried
  slice (a)'s dropped-`(extensions …)`-form bug (a silent override in the second form was
  invisible — the new self-test arm proven RED pre-fix); `check_citations.py` was
  hard-coded to rv64i.sem.sexp, so the new files' locators resolved against nothing — the
  `--corpus` mode binds each sem file to every profile pinning all its cited sources
  (52/52 ×3 profiles, 8/8, 3/3, 4/4 resolved); the mstatus field positions are figure-only
  in the pinned spec, so `encoding.h` (masks) and `causes.csv` (trap causes) joined the
  rv64gc encoding-source pin.
- Validation: check_semantics self-test 15/15 (+7 arms), check_citations 13/13 (+3),
  corpus gate 8/8 (+1); rv64i.sem.sexp untouched and rv64i's generated surfaces byte-exact
  (DEF-GEN/STATE-GEN/GUEST-GEN); both profiles' fetch verify green; `make gate` green
  (DERIVED-COUNTS 384→385 arms).

## SEMULITH-P4-0004 (leaf P4-SYSTEM.2, slice a) — the Zicsr/Zicntr/privileged-system fragments from the re-pinned riscv-opcodes; the csr operand field; IALIGN as profile data

- The upstream census (riscv-opcodes master, the fetch script's own route) measured what
  the design brief delegated: the six Zicsr instructions are real rows in
  `extensions/rv_zicsr`; mret/wfi live in `rv_system`, sret/sfence.vma in `rv_s`; and
  Zicntr's rdcycle/rdtime/rdinstret exist ONLY as `$pseudo_op` rows of csrrs — Zicntr adds
  no encodings. Upstream moved every table from the repository root to `extensions/`; the
  moved rv_i/rv64_i/rv_m/rv64_m hash byte-identical to the rv64i pins, so the fetch route's
  new `extensions/` mapping keeps both profiles' `--verify-only` green (a scripted fresh
  re-fetch of rv_s came back byte-identical).
- The re-pin landed as `profiles/rv64gc-lab-v0/references.sexp` (rv_zicsr, rv_zicntr,
  rv_system, rv_s, csrs.csv + the shared arg_lut.csv — sha256+bytes each; rv64i's ledger
  untouched; the pinned arg_lut already carried csr (31..20) and zimm5 (19..15), so no
  arg_lut re-pin). Three new generated fragments: `definitions/riscv/zicsr.sexp` (owns the
  csr/zimm5 fields), `zicntr.sexp` (the counter reads as `(pseudo …)` — a new fragment
  construct for assembler spellings that add nothing to the encoding space, decided by the
  disjointness gate under a specialization rule; requires rv64i AND zicsr, the pinned rows'
  own `rv_zicsr::csrrs`), `system.sexp` (the D-PRIV-INSNS four). rv64i.sexp/m.sexp
  re-derive byte-identical; the 62-instruction 4-fragment trial union is collision-free.
- The assembler gained the csr/zimm5 operand fields (positions always derived from the
  pinned arg_lut.csv), csr names resolved through the pinned csrs.csv, pseudo-op support
  through the canonical path, and profile-derived IALIGN (rv64i 32 / rv64gc 16 — the
  line-486 hard-code retired). All 13 new forms assemble and round-trip through spike-dasm
  exactly. Measured in execution, fixed at root: `resolve_composition` silently dropped
  every `(extensions …)` form after the first (latent since MODEL-COMPOSE.2), the
  disjointness checker's `DUPLICATE NAME(S)` was advisory-only, and the assembler's label
  pass ate csr names. No Rust surface touched.
- Validation: check_encoding_disjoint self-test 12/12 (the pseudo and dupes arms RED
  first), UNIT-COMPOSITION 9/9, EXERCISE-COVERAGE 21/21, the focused gates green,
  fetch_references `--verify-only` green for BOTH profiles, `make gate` green
  (DERIVED-COUNTS 383→384 self-test arms re-derived).

## SEMULITH-AC-0057 (tree ARTIFACT-CLEANUP) — the 2026-10-03 §8 run: 0 incremental caches present to delete; the reference evidence logs kept

- The ~24 h trigger fired (the `2026-10-02` record was a day old). The census found
  **zero** cargo incremental `.bin` caches — none accumulated since the previous run —
  and zero stray `.bin`/`.log` in `target/release`/`target/debug/deps`. 62
  `target/refs/*.log` (2.2 M, evidence trails of the last reference run) and the 7
  cargo-home crate fixtures (inputs) kept by standing policy. `docs/ARTIFACT_CLEANUP.md`
  overwritten with the dated one-line record; `target` 3.9 G, `.app-data` 1.4 G,
  unchanged.

## SEMULITH-P4-0002 (leaf P4-SYSTEM.1) — the profile resolved: rv64gc-lab-v0, every element source-located; the profile-resolution vehicle route

- The Linux-capable profile is selected and recorded as data: `profiles/rv64gc-lab-v0/`
  carries the resolution — RV64I + M/A/F/D/C + Zicntr + Zicsr + Zifencei (+ Sstc
  privileged), M/S/U modes, Sv39, IALIGN 16 with C, one hart, the 33-CSR committed
  minimum, LP64D ABI, SBI 2.0 as the P6 firmware contract. 18 decisions, each mirrored
  verbatim into a requirement and a contract obligation (`rv64gc-lab-env-v0` v0), every
  element with its source locator. The pinned v20260120 snapshot was measured to CARRY
  the privileged chapters (24 priv/ + 46 unpriv/ pages, 21/21 pins re-hashed against
  the tracked SHA256SUMS); the 2026-09-27 census's "privileged volume absent" phrasing
  is superseded. The closure is measured (G = IMAFDZicsr_Zifencei; D⇒F; F⇒Zicsr;
  C⇒Zca+Zcd at RV64). FP is in the profile; its model evidence is gated on `.7`'s
  backend qualification. The unit is deliberately unregistered.
- The machinery gained the `profile-resolution` vehicle route by declaration (the .2
  discipline): EXTRACTION / EXERCISE-COVERAGE / INTERACTION-MATRIX honor it, a
  definition-pipeline document beside the declaration is RED (self-tests 11/11, 21/21,
  15/15). check_citations.py learned subdirectory `file` fields and named non-snapshot
  skips; gen_platform.py's ISA derivation fixed to the canonical order. FACT-OWNERSHIP
  +4 rows (61 kinds), the obligations fixture re-pinned to six units.
- Validation: `make gate` green (DERIVED-COUNTS 376→383 arms re-derived);
  check_citations 52/52 for both RISC-V units offline; RECORD-SCHEMA 18 record files.

## SEMULITH-P5-0019 (leaf P5-BOARD.6) — the platform capability manifest: derived, schema-gated, drift-gated by PLATFORM-GEN; the dossier pin load-bearing; endianness a data owner

- The board's read-only export for a compatibility checker landed:
  `profiles/netboard-lab-v0/platform.sexp` (export version 0) — OWN-06: derived, never
  handwritten, so a consumer imports facts rather than becoming a second hardware
  implementation. One generator (`scripts/gen_platform.py`, boards discovered by
  declaration) derives it from three fingerprinted canonical inputs — the board
  definition, the pinned processor's profile dossier, the composed contract
  obligations — through the one board reader, the one dossier mapping, the one record
  mapping. Schema-gated by `schema/platform.sexp`; drift-gated by the 34th project
  doctrine PLATFORM-GEN (`scripts/check_platform_gen.sh`, self-test 11/11, every RED
  arm asserting its reason on copies of the real board).
- The document mirrors `docs/ARCHOGEN_INTEGRATION.md` §3's six bullets: processor/ISA
  facts (endianness included — prose-only until this leaf gave it a data owner in the
  CPU dossier), the resolved memory map, the device pins, the declared absences, the
  composition dispositions, the newly declared boot contract and test-control surface
  (`boot`/`test-control` blocks in board.sexp), the time/event/ordering facts derived
  from the composed obligations' parameters, explicit per-facility `presence` markers,
  and the limitations and non-claims as data — including the recorded boundary that
  archogen is actively developed and has no functional eADL interface today, so the
  export is validated by derivation freshness, schema conformance and §3 coverage,
  never by archogen acceptance.
- The board's `dossier-sha256` pin is load-bearing now: measured display-only (rendered,
  re-derived by nothing), it is verified against the live dossier at every derivation
  (`gate_report.dossier_digest`, factored out of `build_cpulab` — byte-identical
  measured). The leaf's own endianness edit exercised the cascade for real: GC-REPORT
  regenerated, the pin re-pinned `1879ba18…` → `95ebca2f…`.
- Measured and fixed at root: a planned edit to ARCHOGEN_INTEGRATION.md was reverted —
  the file is a frozen-in-place delivered input and DELIVERY-PROVENANCE fired as
  designed; the announcement lives in the books and the DOSSIER. TOOLBOX.md's missing
  `.3`/`.4` board-tooling rows were backfilled. FACT-OWNERSHIP +3 rows (57 kinds) with
  the corpus census's three platform pairs; REGEN_GOVERNORS grew per the `.12` ruling;
  DERIVED-COUNTS re-derived (34 doctrines, 376 arms). The board book gained the
  manifest chapter (the generated file included — one owner, two readers).
- Validation: `gen_platform.py --check` byte-exact; PLATFORM-GEN green (self-test
  11/11); schema validation on all touched documents incl. the schema fixpoint;
  BOARD-GEN / BOARD-VERDICT / GATE-REPORT / MATERIALS-BILL / UNIT-BOOKS green;
  `make gate` → all doctrines green; both books build; the book index regenerated.

## SEMULITH-P5-0017 (leaf P5-BOARD.4) — the composition verdict: ACCEPTED, decided on every commit by BOARD-VERDICT; four dispositions as data; the 16-bit declaration measured false and narrowed

- The gate's core obligation landed: for every CPU environment assumption, the named
  board or device guarantee that satisfies it — or a rejection. The verdict is
  **ACCEPTED** and re-decided on every commit by the 33rd project doctrine,
  **BOARD-VERDICT** (`scripts/board_verdict.py` + `scripts/check_board_verdict.sh`):
  the discharge over the composed catalogues (8/8), every `satisfies` edge resolved to
  a discharged assumption (3/3), and every board-deferred device obligation bound to
  exactly one decision `answers` edge (4/4) — an unmatched assumption or a dangling
  edge is a REJECTION by name, never a note.
- The machinery: four deferred obligations (`OB-NIC-STRAP-RESETS` joined the three
  `.10` pre-wired records) carry the marker param `composition_disposition "required"`;
  `schema/board.sexp`'s `decision` gained the optional `answers` edge; the
  dispositions mirror into `hardware.sexp` (schema + `gen_board.py`) for the model
  route. The dispositions, decided: D32 tied high + SPEED_SEL at its pull-up
  (`D-BOARD-NIC-STRAPS`); the NIC's guest-readable time sources frozen
  (`D-BOARD-NIC-TIME-FROZEN`); the replay link scene static-complete at 100BASE-TX FD
  from before the guest's first access (`D-BOARD-NIC-LINK-SCENE`, BSR `0x782D`); pin
  reads tied off at 0 (`D-BOARD-NIC-PIN-TIEOFFS`).
- Measured in execution, fixed at root: the board's eth0 declared 16-bit accesses from
  the datasheet's summary sentence (§1.10), but §3.6 makes the bus widths
  mode-exclusive — with D32 strapped the declaration narrowed to 32; the NIC dossier's
  pairing-latch census entry flipped to absent with the new reason. The expectations
  re-pinned what the verdict determines (`hw_cfg` `0x00050004`, `free_run` `0` frozen,
  `phy_basic_status` `0x782D`).
- The authored verdict: `profiles/netboard-lab-v0/COMPOSITION-VERDICT.md` — the
  per-assumption table (every §5 aspect enumerated; the not-arising ones recorded with
  reasons), the `OB-PLATFORM` note (the discharge edges alone would be materially
  misleading), the interface-test leg (`make check` + smoke green — the RAM half; the
  MMIO halves attach with the device models, named), and MODEL-COMPOSE's open question
  answered for this board shape: no operator beyond union + discharge is needed.
  Included as the board book's verdict chapter.
- Validation: BOARD-VERDICT self-test 6/6 (every RED asserting its reason on copies of
  the real board) + real run green; `make gate` → all doctrines green (DERIVED-COUNTS
  re-derived 32 → 33 doctrines, 359 → 365 arms); `make check` + `run_smoke` green;
  `mdbook build` rc 0; `gen_book_index.py --check` rc 0. No Rust surface touched.

## SEMULITH-P5-0016 (tree P5-BOARD) — the `.4` design brief: the verdict's shape and the four dispositions decided

- The verdict's shape recorded before execution: the mechanical discharge (green at
  8/8 — but its platform-dependent edges land on `OB-PLATFORM`, the laboratory
  guarantee) re-established at content level by the declared `satisfies` edges plus
  four composition dispositions; a re-runner required (the MODEL-COMPOSE.4 lesson).
- Four composition records, not three: `OB-NIC-STRAP-RESETS` (the strap values) joins
  TIME-SOURCES / PHY-LINK / GPIO-PINS. Dispositions decided from the pinned datasheet:
  D32 tied high (§3.6's native 32-bit mode; EEDIO has no internal pull — an explicit
  board tie), SPEED_SEL unwired to its pull-up, the time sources frozen, the link
  scene static-complete at 100BASE-TX FD, the pin reads tied off at 0.
- The measured defect the brief caught: eth0's declared 16-bit width is mode-exclusive
  per §3.6 and narrows to 32 with the leaf.

## SEMULITH-P5-0015 (leaf P5-BOARD.12) — the two-tier per-part ceiling: authored content bounded, regeneration-gated derived members exempt as a checked property

- The director-delegated ruling (`SEMULITH-P5-0014`,
  `decision_derived-members-of-bounded-families`) executed: the per-part byte
  ceiling's founding failure mode — silent accretion in hand-maintained files —
  cannot occur in a regeneration-gated file, so the instrument now matches the
  failure mode. Authored members keep the **65,536** ceiling (the day-old 128 KiB
  interim raise reverted; `decision_profiles-family-composed-units` superseded in
  part); derived members are exempt **as a checked property** — a
  `doctrine/fact_ownership.tsv` mirror row with a regeneration-doctrine governor
  (the closed set: STATE-GEN, DEF-GEN, GUEST-GEN, BOARD-GEN, GATE-REPORT,
  MATERIALS-BILL, BOOK-INDEX) — never as a declaration.
- `scripts/check_readme_routes.sh`: `derived_exempt` consumes the FACT-OWNERSHIP
  registry (already completeness-checked — no second declaration surface);
  `regen_set_registered` refuses set/driver drift so the exemption can never silently
  widen; the per-part loop now judges EVERY over-ceiling member (it previously
  inspected only the biggest) — exempt members are reported as proof, the rest fail
  by name. Aggregates untouched.
- Real-corpus verdict: both composed catalogues (104,372 / 94,027 B) exempt with
  proof printed; the NIC's authored 60,112 B catalogue under the restored authored
  ceiling (0.92×) — the rule discriminates exactly as ruled. Self-test 12 → 17 arms
  (17/0; the RED authored-fail paths fire on fixtures, the real corpus's authored
  members being correctly under the ceiling). Measured in execution: a new
  `armregen` helper idiom made 2 arms invisible to DERIVED-COUNTS' enumerator
  (357 ≠ 359) — folded into `arm`'s optional `[cmd...]` probe form instead.
- The lesson PROMOTED: `docs/knowledge/a-byte-ceiling-applies-to-authored-content.md`
  (+ INDEX) — the instrument must match the failure mode.
- Validation: `make gate` → all doctrines green (DERIVED-COUNTS re-derived 354 →
  359 arms); `mdbook build` rc 0; `gen_book_index.py --check` rc 0. No Rust surface
  touched. P7's soc/computer compositions inherit the rule.

## SEMULITH-P5-0013 (leaf P5-BOARD.3) — the generated maps: one generator, seven artifacts, the BOARD-GEN freshness gate

- `scripts/gen_board.py` discovers boards by declaration (`profiles/*/board.sexp`) and
  generates everything downstream of the canonical definition (OWN-05): the composition
  manifest (the part list derived from the pins, never restated), the four composed
  catalogues (99 requirements, 107 obligations, 5 sources, the rv64i encoding —
  materialized by the factorized `compose_units.compose_resolved`, the ONE code path
  the verdicts consume), `hardware.sexp` under the new `schema/hardware.sexp`, and
  `map.md`. Every artifact carries the OWN-03 fingerprint header.
- The **BOARD-GEN** doctrine (`scripts/check_board_gen.sh`) is the freshness proof
  `compose_units.py` deferred to the first tracked board: `--check` re-derives all
  seven artifacts and refuses DRIFT by name (self-test 9/9, every RED arm asserting
  the reason); the generator refuses an inconsistent definition by name (region
  overlap, MMIO window without device, executable MMIO, ghost console).
- The census found exactly ONE handwritten duplicate map (the DOSSIER's table) —
  replaced by the generated map: the DOSSIER links it, the board book includes it
  (one owner, two readers, the include verified in the built HTML). The DOSSIER's
  stale post-`.11` status rows (the brief's logged defect) fixed in the same pass.
- FACT-OWNERSHIP gained 8 rows (54 kinds; the two measured corpus pairs registered,
  never weakened) and the fixture re-pinned to five units; DERIVED-COUNTS fired as
  designed (31→32 doctrines, 345→354 arms, re-derived in `LIVE_STATUS.md`).
- Measured and recorded at root: the brief's register-surface containment check is
  not implementable — the device dossiers carry register offsets in prose, never as
  machine-readable data; the generator's refusals are scoped to what board.sexp
  proves, and machine-readable offsets arrive with the device models. And the
  `profiles/` per-part bound bit a second time (the first DERIVED member class:
  the composed `contract-obligations.sexp`, 104,372 B) — the standing reviewed-raise
  rule applied (`decision_profiles-family-composed-units`: 64 → 128 KiB at 0.80×,
  aggregates unmoved).
- Validation: BOARD-GEN ok; RECORD-SCHEMA 16 record files; FACT-OWNERSHIP 54 kinds;
  UNIT-BOOKS 5/5; `make gate` → all doctrines green; `mdbook build` rc 0;
  `gen_book_index.py --check` rc 0. No Rust surface touched. The composed catalogues
  on disk are `P5-BOARD.4`'s pre-staged input.

## SEMULITH-MCU-0002 (leaf MCU-DOCS.2) — the channel's twelve answers reconciled: the MCU documentation set acquired and digest-verified

- Verified live first: `build_responses.py --report` → **12 fulfilled / 0 blocked**, exit 0.
  The routes, measured by the channel: the Cortex-M TRMs from Arm's documentation-service
  API; FE310 from the SiFive CDN; MSP430 direct from ti.com; i.MX RT / SAM D21 / STM32 from
  Wayback captures of the official URLs (the live URLs 404/403/reset automated clients —
  measured routes, recorded in the answers' evidence); the three M-profile ARMs and the
  RP2040 datasheet already held corpus-side.
- Twelve materials adopted into `materials/catalog.sexp` (the three M-profile ARMs, three
  Cortex-M TRMs, FE310, i.MX RT1050 RM, MSP430FR59xx UG, SAM D21, STM32 RM0394 + PM0214)
  and fetched into `.materials/mcu/` with every sha256 re-verified — `materials --verify:
  64 verified / 0 unresolved` (52 at P5-BOARD.9 + the twelve). The corpus re-pinned
  `c4ad8a2` → `3dc4e62` (302 PDFs; 293 at the prior pin). All twelve requests marked
  `resolved` with their evidence.
- **Measured defect, fixed at root:** the `.1` survey measured the corpus's
  semulith-facing proposals feed only — the RP2040 datasheet was already adopted in our
  own catalog since 2026-09-14 (same sha256, cached), so one request was redundant from
  filing. No duplicate record adopted; the survey knowledge card gained the three-layer
  "already held" rule (tracked catalog + fetch cache + corpus tree, not just the feed).
  The tree closes (2/2).

## SEMULITH-MCU-0001 (leaf MCU-DOCS.1) — the MCU documentation set surveyed and requested through the chipdoc channel

- The director's `2026-10-02` steer (ARMs carry full MCU documentations; other vendors
  too — ask chipdoc) executed as documentation research, ahead of any MCU milestone
  (none owns MCU modeling yet — stated, not hidden). New tree:
  [`MCU-DOCS`](docs/tasks/MCU-DOCS.md).
- The survey measured the LIVE corpus feed (corpus `c4ad8a2` working tree, read-only):
  held — ESP32/C3/S3 and RP2040/RP2350 SVD register maps, the nRF52840 PS, the AM335x
  TRM (a Cortex-A8 SoC, not an MCU), the Arm PrimeCell/AMBA/GIC set (Cortex-A class);
  absent — every Arm M-profile architecture manual, every Cortex-M TRM, every vendor
  MCU datasheet/RM beyond the held trio.
- Twelve requests filed in `materials/requests.sexp` (the preferred channel): the three
  M-profile ARMs (v6-M/v7-M/v8-M), three Cortex-M TRMs (M0+/M3/M4), and six vendor
  documents (RP2040 datasheet, STM32 RM + PM0214, SiFive FE310, i.MX RT1050 RM, SAM
  D21, MSP430FR59xx). Pickup measured: the poller (read-only) reports exactly the
  twelve new ids, rc 1. One authoring defect (a heredoc paren over-close) caught by the
  one reader before landing — parse gates work.
- Fulfilment is chipdoc-side and asynchronous; a `MCU-DOCS.2` reconciles the answers
  when they arrive (the `P5-BOARD.9` pattern).

## SEMULITH-BA-0002 (leaf BOOK-APPARATUS.2) — the reading-experience audit pass: 29 main-line chapters, 16 kept / 13 revised; the yield was factual drift

- The first audit pass over the project book against
  [`decision_mdbook-incremental-engaging`](docs/decisions/decision_mdbook-incremental-engaging.md):
  six parallel chapter-group audits (the decision's four criteria operationalized), every
  flagged item re-verified against the repository before any edit. The per-chapter
  dispositions are recorded in [`docs/tasks/BOOK-APPARATUS.md`](docs/tasks/BOOK-APPARATUS.md).
- **Twelve stale facts fixed at their lines** (each measured): `claim-scope.md` (four crates,
  not three; the CPU-LAB self-contradiction; the 48+1-program corpus, not forty-one),
  `plan/p0.md` (the contract is 36 obligations / 72 checks — the quote now matches the
  regenerated G0-REPORT it claims to quote), `plan/p1.md` (G1 reads `passed` since
  2026-09-30; 48 guests / 642 steps), `plan/p5-p7.md` (registration day is done),
  `docs/ARCHITECTURE.md` (28/36/28 records), `docs/RISKS_AND_DECISIONS.md` §2 (four
  current-state rows updated with measured states and dates — the column whose point is
  tracking change), `docs/SOURCES_AND_NAMING.md` (the crates exist; the reservation claim
  narrowed), `LIVE_STATUS.md` ("1 unit today" → 5).
- **Three record violations revised**: the gates overview's duplicated sentence dropped;
  `plan/p3.md`'s 68-line leaf-by-leaf update chain collapsed to a final-state paragraph
  (both measured incidents kept; the tree carries the blow-by-blow); P7's cold mechanism
  open gained its why-sentence. Terminology pointers added where a concept was leaned on
  without introduction (F3/F6 → `docs/tasks/DSP-REVIEW.md`; CLINT glossed; the P3 forward
  reference named).
- **Two ` ```mermaid ` blocks rendered as raw source in the book** (no preprocessor) —
  replaced by text-rendered flows; `mdbook-mermaid` deliberately NOT added (an
  unsanctioned dependency is worse than a plainer diagram).
- The book builds; the index regenerates clean (`gen_book_index.py --check` rc 0);
  `make gate` green. The BOOK-APPARATUS tree closes (2/2).

## SEMULITH-P5-0011 (leaf P5-BOARD.11) — registration day: the three units register; the materials-bill machinery goes route-keyed by declaration

- `materials/units.sexp` now registers five units: `netboard-lab-v0` (kind `board`),
  `sifive-uart-lab-v0` and `lan9118-lab-v0` (kind `device`) beside the two processors —
  the schema's sanctioned "(values …) edit the day a real unit needs one":
  `schema/units.sexp` kind +board/+device, the shared layer taxonomy +device.
- The materials-bill machinery is **route-keyed by declaration**
  (`gen_model_book.unit_shape`: `board.sexp` present → board; the profile's vehicle
  route otherwise — never a guess): per-shape internal-contracts censuses (devices carry
  `expectations/`, the board carries `board.sexp`+`DOSSIER.md`), route-honest fragment
  content (a device has no encoding space and pins no reference models — the fragments
  say so), and `check_materials_bill.sh`'s COMPLETENESS keyed on the same shape. The
  pre-fix refusal was re-run from the parent commit and measured (`REFUSED —
  references.sexp: the pinned document is missing`); the two processor books' fragments
  regenerated byte-identical modulo the embedded generator hash. Four new self-test
  arms pin the device and board shapes (MATERIALS-BILL 11/11).
- The three per-unit books land under `docs/models/<unit-id>/` — authored chapters
  (devices: introduction / materials bill / gaps / methodology / evidence; the board:
  the composition narrative as its method, no evidence chapter until `.4`) with the
  generated fragments; UNIT-BOOKS 5/5 build, MATERIALS-BILL 5/5 (every material states
  what it does not supply), SCOPE-COVERAGE `5 unit(s) may code` over the 72 new census
  rows (the board's absences are `out-of-scope` WITH their contract reasons — never
  `missing`).
- Measured and corrected at execution: the BREADTH report's stale "2 registered units"
  prose was the **generator's** hardcoded string — fixed at `gate_report.py` (the count
  and the processor-units claim now derive), the report regenerated (5 units, verdict
  still `passed`); the project book's `models.md` updated to five units;
  DERIVED-COUNTS' self-test-arm total re-derived 341→345 by its enumerator.
- FACT-OWNERSHIP carries the book-side mirrors (46 fact kinds). The P5 frontier is
  `.3` (generated maps) then `.4` (the composition verdict — the devices' composition
  records are pre-wired to it).

## SEMULITH-P5-0009 (leaf P5-BOARD.10) — the second device dossier: `lan9118-lab-v0`, fully gated with no machinery edit; the per-part bound bites

- The LAN9118 NIC dossier lands under
  [`profiles/lan9118-lab-v0/`](profiles/lan9118-lab-v0/DOSSIER.md): the DS00002266B-pinned
  source (digest re-verified from the materials cache), 52 requirements (46 defined + the
  reserved/unspecified/implementation-defined silences and deferrals), 52 mirrored
  obligations (contract `lan9118-v0` v0, `device-guarantee`), the state document (49
  registers across three indexing levels + 4 FIFO families + the earned hidden-state
  census — the model additionally carries the TX command-parser state and the 16-bit
  pairing latch), 52 verbatim decision mirrors (generated from requirements.sexp
  mechanically — drift impossible by construction, refused by gate regardless), and 3
  datasheet-derived expectation documents (cold-reset reads; exact TX free-space
  accounting; the recorded-trace RX path) recorded **before any model exists**.
- **No machinery edit**: `.2`'s generalization by declaration covered the NIC — the
  gates attach by glob and derive device applicability from the `vehicle` declaration.
  The mechanical re-pins: FACT-OWNERSHIP +6 registry rows and fixture re-pins
  (`7→8`, `3→4`); the `profiles/` bound re-derived 4× → 5×
  ([`decision_profiles-family-five-units`](docs/decisions/decision_profiles-family-five-units.md))
  — where the **per-part bound bit for the first time** (32→64 KiB; the mirror
  discipline on a 52-record contract puts the largest catalogue at 60,112 B).
- Measured in execution, recorded at root: the two `pdftotext` modes disagree on
  Table 5-1's Default column (per-register sections are the authority, arithmetic
  cross-checks agree); §3.11's reset completion times render as `2 s`/`100 s` in the
  PDF's **own text layer** (hexdump-verified µ mis-mapping — only cleanly stated figures
  pinned); PHY ID2's model/revision nibbles are blank in the datasheet; ADDRH/ADDRL's
  Table 5-6 defaults sit beside §5.4.2's "undefined until loaded" — both recorded,
  nothing guessed. The lesson is promoted:
  [`a-pdf-text-layer-is-not-the-page`](docs/knowledge/a-pdf-text-layer-is-not-the-page.md).
- The design brief's sharpest finding is now contract data: the NIC's guest-readable
  time sources (`REQ-D-NIC-TIME-SOURCES`), the wire-domain PHY link scene under replay
  (`REQ-D-NIC-PHY-LINK`) and the pin tie-offs (`REQ-D-NIC-GPIO-PINS`) pre-wire
  `P5-BOARD.4`'s composition verdict. Registration day (`.11`) is next.

## SEMULITH-P5-0007 (leaf P5-BOARD.2) — the first device dossier: `sifive-uart-lab-v0`, fully gated; the machinery generalized by declaration

- The SiFive UART dossier lands under
  [`profiles/sifive-uart-lab-v0/`](profiles/sifive-uart-lab-v0/DOSSIER.md): the §13-pinned
  source (digest re-verified from the materials cache), 19 requirements (13 defined + 6
  measured silences — Reserved bits, X-marked resets, FIFO reset, off-map/non-32-bit
  accesses, the watermark mode), 19 mirrored obligations under contract `sifive-uart-v0`
  v0 with the schema's new third direction `device-guarantee`, the state document with
  its earned hidden-state census (registers + FIFO contents/occupancies, nothing else
  MMIO-visible), 19 verbatim decision mirrors, and 3 datasheet-derived register-read
  expectation documents recorded **before any model exists**.
- The dossier machinery generalized **by declaration, not exemption**
  ([`decision_device-applicability-by-declared-vehicle`](docs/decisions/decision_device-applicability-by-declared-vehicle.md)):
  `vehicle (route device-model) (comparison register-expectations)`; `profile.sexp`'s
  processor-only fields optional; `mmio_registers` scope; `expectations.sexp`
  entry/instructions optional; EXTRACTION / EXERCISE-COVERAGE / INTERACTION-MATRIX derive
  device applicability with contradiction = RED; a device-guarantee discharges a CPU
  assumption by construction (pinned GREEN arm); PROFILE-CONSISTENCY needed no
  conditional (measured by a new self-test arm).
- Measured in execution, fixed at root: the §13.8 watermark bits' level-vs-hold gap
  (`REQ-D-UART-WM-MODE` — expectations pin a bit only when its raised condition holds
  under every reading); the `REQ-U-` id prefix colliding with RECORD-SCHEMA's mechanical
  decision→requirement mapping (renamed); the interaction-matrix n/a note counted as a
  cell (fixed); FIFO resets recorded as "unspecified" data rather than weakening the
  every-element-a-reset contract.
- FACT-OWNERSHIP re-pinned to three units (registry + fixtures); the `profiles/` bound
  re-derived 4× ([`decision_profiles-family-four-units`](docs/decisions/decision_profiles-family-four-units.md)).
  Registration of all three units consolidates into `.11`; the LAN9118 dossier is `.10`.
- Validation: all dossier documents schema-validate; the three profile-glob gates decide
  the device by declaration; every edited check's self-test green (17/9/14/41/7/14/10
  arms, 0 fail); `make gate` all doctrines green; the mdBook builds.

## SEMULITH-PKG-0017 (leaf SEMULITH-PKG.9) — the policy note's provenance triple now re-derives from the note

- Session-start policy check (§14/§17/§18), measured live: `README_POLICY.md`'s neutral
  body is byte-identical to the originating project's current revision (no unadopted
  upstream change), and `docs/CLAIM_VERIFICATION.md`'s recorded source SHA-256
  (`9f99df25…6046bd`) matches the pgen source exactly. Nothing to re-adopt.
- One defect found and fixed: the policy adoption note's recorded SHA-256 / line / byte
  triple did not state its digest span, so it failed to reproduce as written (the measured
  span trims leading blank lines and the `---` separator). The note now states the span;
  the re-deriving command lives in task leaf `SEMULITH-PKG.9`; the recorded
  `77a1e934…c0182d6eefec` / `159 / 8,279` reproduces exactly.
- `SEMULITH-PKG` complete (9/9). Validation: `scripts/check_doctrines.sh` all green.

## SEMULITH-P5-0005 (leaf P5-BOARD.1) — the platform specified: `netboard-lab-v0` pins versions, not names; the 16550 label measured false and corrected

- The first board's canonical definition lands: [`profiles/netboard-lab-v0/board.sexp`](profiles/netboard-lab-v0/board.sexp)
  under the new [`schema/board.sexp`](schema/board.sexp) — the first non-processor
  source-of-truth schema (DOSSIER-SCHEMA pairs them by basename) — narrated by
  [`profiles/netboard-lab-v0/DOSSIER.md`](profiles/netboard-lab-v0/DOSSIER.md).
- Every pin is a version, never a name (OWN-05, the leaf's acceptance): the processor by
  unit id + version `0` + the GATE-REPORT-gated dossier content digest; each device by its
  datasheet's material id + revision + sha256. The memory map (2 GiB RAM at the harness's
  existing base, the UART at the sourced FU540 instance address, the NIC in the datasheet's
  256-byte direct-register span), cold-only reset, and the serial console are data.
- Timers and interrupt controllers are **absent by contract** — declared as data with their
  reasons and the obligations they satisfy (`OB-ENV-VIRTUAL-TIME`, `OB-ENV-EVENT-DELIVERY`);
  a CLINT/PLIC would be a composition rejection, not a feature. `satisfies` fields pre-wire
  `.4`'s composition verdict. Both devices' interrupt lines unconnected-and-declared;
  drivers poll. The NIC backend is recorded-trace replay RX / recording-sink TX.
- **Measured defect, found and fixed in execution:** the design brief's "16550-compatible
  UART" label is false against the pinned source — zero occurrences of "16550" in
  FU540-C000 v1p5 (`pdftotext` census); §13 documents the SiFive UART. The source pin was
  the intent: the board adopts the SiFive UART, `materials/catalog.sexp`'s supplies text is
  corrected, and the correction is recorded as `D-BOARD-UART-KIND`.
- Scope routing: board-unit registration (`materials/units.sexp`, the `kind` edit, the
  per-unit book) lands with `.3` — registration day carries the UNIT-BOOKS /
  MATERIALS-BILL / generator consequences, which are not a specification's to bear.
- The `profiles/` family's third unit directory: the bound re-derived to 3× by the standing
  arithmetic ([`docs/decisions/decision_profiles-family-three-units.md`](docs/decisions/decision_profiles-family-three-units.md));
  the board-definition fact kind registered in `doctrine/fact_ownership.tsv`.
- Validation: both schema validations ok; every pin re-derived from its source artifact;
  `make gate` green; `mdbook build docs/book` rc 0.

## SEMULITH-BA-0001 (leaf BOOK-APPARATUS.1) — the book's index: generated from the book's own text, gated against drift

- The director's `2026-10-02` apparatus directive audited against the real book: glossary
  present and unforkable (build-time `{{#include}}` of the canonical `docs/GLOSSARY.md`),
  two annexes present and on-policy — the **index was absent**. It lands derived, the only
  honest shape for a fact about a changing population: `scripts/gen_book_index.py` reads
  `SUMMARY.md` + the canonical glossary + the acronym table + every chapter's text;
  `docs/book/src/index.md` is what that derives (15,019 B, 40 terms).
- New project doctrine #31 **`BOOK-INDEX`** (`scripts/check_book_index.sh`): the index
  regenerates byte-exact or the commit fails — a hand-maintained index is a running total,
  and a running total is a memory of a measurement, not a measurement. Six self-test arms,
  fired RED before registration (DRIFT ×2, refusal-by-name ×2). Registered and mirrored
  (`DOCTRINE_ENFORCEMENT.md`, the book's doctrine chapter, `TOOLBOX.md`,
  `doctrine/fact_ownership.tsv`).
- The annex policy is stated in the book's introduction: chapters stay readable; what is too
  technical for the main line lives in an annex.
- The directive's second half became durable: `decision_mdbook-incremental-engaging` +
  `BOOK-APPARATUS.2` (the reading-experience audit). The TOC request was withdrawn by the
  director — the mdBook sidebar is the TOC; the contents page built for it was reverted.
- Defect fixed at root, not reported: the generator's printed term count was a fudge factor
  (read `47` against the real `40`); it now derives from the emitted rows.

## SEMULITH-MP-0001 (leaf MEMORY-POINTER.1) — MEMORY.md slimmed to the §6 next-action pointer

- The director's `2026-10-02` ruling executed: `MEMORY.md` exists solely to point at the next
  action, overwrite-only per `MEMORY_ARCHITECTURE.md` §6. Measured before: 34 lines / 7,031 B
  (97% of the hard cap; health 30 / 1,792). After: **29 lines / 1,865 B**.
- The audit verified every dropped line's durable home (trees, `docs/decisions/`,
  `docs/knowledge/`, TOOLBOX, git's submodule pin); exactly one ruling was dangling —
  `document EVERYTHING` (2026-10-01) — backfilled as `decision_document-everything`. The
  ruling itself is `decision_memory-next-action-pointer`.
- Gate lesson recorded: `TREE-CLAIMS` scans the `Active trees:` claim PER PHYSICAL LINE — the
  first slim draft wrapped the list and fired `MISSING ACTIVE`; the list stays on one line.

## SEMULITH-DS-0004 (tree DOC-SHARDING) — the append heads shard ahead of the next slice

- Trigger: `CHANGELOG.md` at 65,035 of 65,536 bytes (501 headroom) and `DEV_NOTES.md` at
  49,000 of 49,152 (152) with the next slice's entries already measured larger than the
  remaining room — the designed fire point, answered by sharding, never by raising the cap.
- `shard_history.py --max-bytes 63488`: 2 entries → `docs/changelog/shard-0113.md`,
  completeness `54 == 52 kept + 2 moved` order-and-bytes exact, head 65,035 → 62,570.
- `shard_history.py --head DEV_NOTES.md --max-bytes 46080`: 3 entries →
  `docs/changelog/shard-0114.md`, completeness `35 == 32 kept + 3 moved` exact, head
  49,000 → 45,633. Manifest 114 → 116 rows.

## SEMULITH-AC-0056 (tree ARTIFACT-CLEANUP) — the 2026-10-02 §8 cleanup: 105 incremental caches, 139 MB

- Time-triggered §8 run (the `2026-10-01` run was a full day old): 105 cargo
  incremental-cache `.bin` files deleted (139 MB), every one under a cargo
  `*/incremental/*` directory of `target/` (84 the project's own debug profile, 21
  wasm32) — exactly the enumerated safe scope; post-delete re-census 0; `target`
  4.0 G → 3.9 G; `.app-data` unchanged at 1.4 G.
- 0 stray `.bin`/`.log` in `target/release` / `target/debug/deps`; no
  `target/refs/*.log` present this run; the 7 cargo-home crate test fixtures kept
  by policy (inputs, not artifacts). `docs/ARTIFACT_CLEANUP.md` overwritten with
  the one-line record.

## SEMULITH-P5-0003 (leaf P5-BOARD.9) — the chipdoc answers reconciled: five adopted, five measured negatives

- Verified live first: `build_responses.py --report` → 5 fulfilled / 5 blocked, exit 0
  (every open request answered — the second incident's gap, closed by CHANNEL.md
  §0.3/§0.5, re-read `2026-10-01`).
- The five fulfilled adopted as catalog materials — `MICROCHIP-LAN9118` (the wired-NIC
  primary), `UBLOX-SARA-R4-AT` (the cellular AT primary), `ESPRESSIF-ESP-AT`,
  `NORDIC-NRF52840-PS`, `MICROCHIP-AT86RF233` (the two true RFICs) — fetched into
  `.materials/network/`, every sha256 re-verified (`materials --verify: 52/0`); the
  corpus re-pinned `c4ad8a2` (5696 files / 293 PDFs, the same census).
- All ten requests marked: five `resolved`, five `blocked` — each blocked a MEASURED
  NEGATIVE with its consequence named (e1000/RTL8139 → LAN9118 is primary; EC25/
  SIM7600 → SARA-R4 is primary; the AR9271 probe's negative IS its answer: no public
  register-level WiFi baseband documentation exists). Never re-filed without a new
  route. `P5-BOARD.1` inherits five sourced candidates plus five closed alternatives.
- The knowledge cards carry the ask→answer loop end-to-end
  (`the-chipdoc-request-channel.md` refreshed with the §0.3/§0.5 answer path;
  `the-chipdoc-channel.md` updated and cross-linked).

## SEMULITH-BR-0021 (leaf P3-BREADTH.6) — gate BREADTH runs: verdict passed; the capability report published

- `scripts/gate_report.py` gained the cross-unit builder (`--gate BREADTH`): the three
  roadmap axes measured from tracked files by concrete artifact name — axis 1 the
  subset's six evidence anchors (declared scope + vehicle, the `.a56` corpus, 17
  crate tests, the driver, the comparison contract, the registered mechanism), axis 2
  nine abstraction constructs DECLARED in their schema AND CARRIED by the mapping
  owner with the refusal boundary pinned (5 synth probes), axis 3 the registry as the
  complete claim list — **TI C6000 and ADI SHARC unclaimed explicitly**, everything
  else by omission. No code path to `passed` over an absent anchor (EVD-08).
- The report publishes at `docs/BREADTH-REPORT.md` — a cross-architecture gate cannot
  be owned by a profile directory — and `check_gate_report.sh` gained the repo-level
  leg: same regenerate-never-edit enforcement, same controls (self-test 12/12; 4
  reports in sync, G0/G1/GC byte-identical).
- `P3-BREADTH` **CLOSED 8/8** — the stable-API claim is permitted exactly where the
  report permits it (the exercised cases of the two registered units); `.1` stays
  `slice-gated` on the record, its TI/VLIW legs reopening by name.

## SEMULITH-BR-0020 (leaf P3-BREADTH.6) — the second unit registered; its book stands; the per-part ceiling rises by ruling

- `materials/units.sexp` gained `dsp56300-lab-v0` (the second unit; C17 in / C14 out
  against rv64i's requires set — reset is this unit's own decision, interrupts a named
  exclusion) and the 24-row category-needs census landed (8 covered / 6 partial /
  3 missing-with-closings / 4 out-of-scope / 3 deferred-to-board).
- `scripts/gen_model_book.py` learned the sibling-crate shape — three extensions, each
  naming the DSP case (the declared-vehicle encoding fragment; `encoding.sexp` as the
  one document a sibling-crate unit may lack, its row naming the deferred lane; register
  families / spaces / the `.a56` census where the rv64 shapes are absent). rv64i
  regression byte-exact: only the generator-digest header line moved.
- The book `docs/models/dsp56300-lab-v0/` stands (six chapters, the bill's 12 sections
  each with its does-not-supply); UNIT-BOOKS, MATERIALS-BILL and SCOPE-COVERAGE all
  green with 2 units; four fragment mirror rows registered (FACT-OWNERSHIP 29 kinds).
- **Director ruling (`2026-10-01`): task-tree growth is ALLOWED** — the docs/tasks/
  per-part bound rose to 128 KiB (`decision_task-tree-per-part-growth`) after six forced
  archive operations in one day taxed active slices; the aggregate bound and the archive
  lifecycle are unchanged, and a bound remains — a file stays readable in one sitting.

## SEMULITH-BR-0019 (leaf P3-BREADTH.6) — the DSP's contract records land governed; the fixture noticed

- `profiles/dsp56300-lab-v0/` gained `requirements.sexp` (seven records, statements
  byte-identical to the profile's decisions) and `contract-obligations.sexp` (thirteen
  obligations — seven mirrors plus six environment-assumptions; contract
  `dsp56300-lab-env-v0`; 26 declared checks). RECORD-SCHEMA attached on landing with zero
  gate edits (auto-discovery; 10 record files green on the first pass); FACT-OWNERSHIP
  gained the DSP's two registry rows.
- FACT-OWNERSHIP's GREEN self-test fixture went RED on the landing BY DESIGN — its pair
  glob follows the real corpus, and the fixture registry still named a one-unit world
  (`UNREGISTERED MIRROR PAIR`). Re-pinned to the two-unit corpus (`__CHECKED__ 5 → 6`),
  the reason recorded in the check's comment.
- Validation: both catalogues schema-validate; RECORD-SCHEMA, FACT-OWNERSHIP (25 kinds,
  self-test 10/10) and `make gate` all green; the rv64i catalogues byte-untouched. The
  DOSSIER's records row reads present; `.6` continues with slice 2 (the BREADTH report).

## SEMULITH-P5-0002 (leaf P5-BOARD.8) — the network-connected board's documentation researched; ten requests filed, the channel measured

- The `2026-10-01` design discussion (boards that touch the world) turned into a measured
  documentation position ahead of `P5-BOARD.1`'s board choice. The corpus survey (the
  snapshotted chipdoc feed, corpus `92a73b6`) measured the holdings: a complete
  register-level Ethernet MAC+PHY contract (TI-DP83816), ESP32/C3/S3 register maps, the
  SiFive FU540/FU740 manuals and HiFive board docs, the TI AM335x TRM — and the recorded
  negative: no standalone Cadence GEM / DesignWare GMAC spec is public.
- Ten acquisition requests filed in `materials/requests.sexp` (the preferred channel),
  each naming its consumer: wired NICs with QEMU precedents (LAN9118, Intel 82540EM,
  RTL8139), three LTE modem AT manuals (Quectel EC25, SIMCom SIM7600, u-blox SARA-R4),
  the WiFi-module command surface (ESP-AT), two register-documented radios for the
  true-RFIC leg (nRF52840, AT86RF233), and one honest probe (AR9271 register docs,
  expected absent). Pickup measured: chipdoc's poller (run read-only) reports exactly
  the ten new ids, rc 1.
- The channel's filing mechanics are now recorded semulith-side as a knowledge card
  (`docs/knowledge/the-chipdoc-request-channel.md` + INDEX) — they had lived only in the
  corpus-side manual, and a session re-derived them the hard way once.

## SEMULITH-BR-0018 (leaf P3-BREADTH.7) — the dsp56300-lab-v0 dossier lands, governed

- The three schema-validated documents moved from
  `docs/tasks/artifacts/p3-breadth/dsp56300-dossier/` to `profiles/dsp56300-lab-v0/`
  (rename lineage kept; headers rewritten from "NOT LANDED" to the landed gate map):
  `profile.sexp` (the subset decisions + the vehicle declaration), `state.sexp` (the F6
  census as data), `interactions.sexp` (6 axes, 21 cells).
- Every attaching gate green WITH the documents landed: EXERCISE-COVERAGE (19/19 DSP,
  52/52 rv64), EXTRACTION (sibling-crate route reported), INTERACTION-MATRIX (2 units —
  the DSP's 21 cells re-derived and resolved), PROFILE-CONSISTENCY (2 dossiers),
  DOSSIER-SCHEMA (62 validated, 2 skipped by name), FACT-OWNERSHIP (23 kinds — the DSP's
  five rows landed; the two post-landing census arms prove same-unit pairing, 10/10).
- The DOSSIER's rows now read present/deferred with owners; the stale "lands with the
  model slice" wording for requirements and unit registration re-routed to
  `P3-BREADTH.6`. `.7` DONE 3/3; the frontier is `.6`, the BREADTH gate report.
- Bookkeeping: `.7` slice 1's checklist archived verbatim (the 64 KiB per-part held).

