# CHANGELOG.md

## SEMULITH-AC-0060 (leaf ARTIFACT-CLEANUP.3) — due cleanup

- Removed 102 untracked incremental caches (364,047,724 B); re-census 0. Preserved diagnostic
  and reference logs and dependency fixtures. No product behavior or milestone state changed.

## SEMULITH-P4-0081 (leaf P4-SYSTEM.12, slice b) — recover C's language slice

- Recovered the five unfinished files after the machine/session crash. `expand` declares
  36 named base expansions and C.JALR's own pc+2 rule, with exact operand mappings and
  reserved predicates quoted from RVI-C. The semantics checker refuses malformed bindings;
  the generator emits C metadata only with C composed and decodes by fixed-bit specificity.
- `probe_c_expansions.py`: 37 forms, 104 spec-side checks; compiled mappings/effects and
  decoder (8/8). A wrong register offset and reversed decode order are caught. DEF-GEN
  51/51 controls; semantics 46/46; citation reader extended to expansions; 0 quote findings.
  M's existing quoted sentences now use the quote checker's spelling. Existing executable
  tables unchanged; `make check`, `make gate`, all books green; handoff OK.
- Tracking and book synchronized. Handoff before slice (c), the engine, as requested.

## SEMULITH-P4-0080 (leaf P4-SYSTEM.12, slice a2) — a found defect: JAL's offset sign, both engines

- Both extractors pushed a scattered immediate at its FIELD width; `jimm20` holds imm[20:1] in
  20 bits, so JAL offsets were sign-extended from bit 19 — a +512 KiB jump went backward, a
  −512 KiB − 4 one forward (reproduced on both CLIs). `exec.rs`'s own doc stated the right
  algebra (21). Fixed: a scattered field carries its composed immediate's width.
- `jal_offsets_at_the_sign_boundary_reach_their_targets` in both engines (RED before, GREEN
  after); both corpora unchanged. The rv64i release decision amended: its recorded evidence is
  unaffected by construction (every result a PASS).

## SEMULITH-P4-0079 (leaf P4-SYSTEM.12, slice a) — the C re-pin and the fragment

- The ledger pins `rv_c` (23), `rv64_c` (10), `rv_c_d` (4) by content; the census excludes them
  by name until the bind.
- `definitions/riscv/c.sexp` generated: 37 forms, the compressed register fields, 24 immediate
  piece layouts (the loader generalized; the base path byte-identical), and the six upstream
  overlaps as declared specializations (`schema/fragment.sexp` `specializes`).
- `check_encoding_disjoint.judge_overlaps`: only DECLARED strict specializations are legal (5 new
  controls, 17/17); UNIT-COMPOSITION uses the same rule.
- Book: `plan/p4/c.md` (44 chapters).

## SEMULITH-P4-0078 (tree P4-SYSTEM) — the `.12` design brief: bind C

- Recorded before execution. Measured: no C table on disk or pinned; 37 forms at RV64 + D
  (Zca 33 + Zcd 4); ILEN stays 32 — what is missing is instruction length; the fetch
  translates both parcels before reading either, and the pc advances by a hard-coded 4;
  upstream's constraints live in field names and six overlapping pairs, which the name-ordered
  decoder would resolve wrongly; every tool assumes 4-byte instructions; Sail selects Zca/Zcd.
- The design: each compressed form declared by the base instruction it expands into, operands
  mapped, the spec's own sentence quoted (C.JALR its own rule — the spec's stated exception);
  decode by specificity with reserved code points from the spec; a parcel-first fetch;
  parcel-aware tools; an EVD-05 corpus with the second-parcel page fault; Sail. Slices (a)–(f).

## SEMULITH-P4-0077 (leaf P4-SYSTEM.11, slice d) — THE LEAF ACCEPTANCE; the leaf CLOSES

- Measured: the `m` slot gone; 13 of 13 M forms in the four guests, on the lab engine (139/139)
  and on Sail (4 of 4), from expectations pinned before the engine had M; Table 1's rows at both
  widths in 17 guest lines and among the 4,485 engine-run vectors.
- `P4-SYSTEM.11` is **done**; the tree reads 11/18; the frontier moves to `.12`, bind C.
  `.9`'s and `.10`'s checklists archived verbatim to part 4.

## SEMULITH-P4-0076 (leaf P4-SYSTEM.11, slice c2) — Sail over the M corpus: 4 AGREE of 4

- The `.7` harness over the four `m-*` guests under the tracked matched configuration (re-
  materialized, unchanged; M supported): 99 steps, every change-observation exact. A planted
  wrong overflow quotient DIVERGES at its step. Recorded as the ledger's eighth experiment —
  for integer M the pair shares no code.

## SEMULITH-P4-0075 (leaf P4-SYSTEM.11, slice c1) — 4,485 generated M vectors through the engine; M-VECTORS

- `scripts/gen_m_vectors.py`: a spec-side exact-integer reference (truncation written out,
  Table 1 by name) → `crates/semulith-verify/src/m_vectors/vectors.txt` (4,485 vectors over the
  13 forms). `m_vectors/tests.rs` runs each through `exec_rv64gc::step` — decode, the rule's
  guard, the operators at their width — with words built from the chapter's layout.
- `scripts/check_m_vectors.sh` — M-VECTORS, the 38th doctrine: DRIFT, and the reference judged
  against the chapter's own identities on operands the table does not use (6/6 controls).
- `gate.sexp`: the table is G-REGRESSION `generated` evidence.

## SEMULITH-P4-0074 (leaf P4-SYSTEM.11, slice b) — THE BIND: the unit composes `riscv/m`

- The encoding composes M (slot `c` the one left); the census 150 → 163 (`m_muldiv`); the module
  regenerated; the engine's M arms through `muldiv`; the ledger re-pins `rv_m`/`rv64_m`.
- Four guests — `m-mul`, `m-div`, `m-word`, `m-alias` — every form at Table 1's edges, their
  expectations derived spec-side and digest-pinned before the engine had M: 139/139; the 135
  pre-slice guests byte-identical on the bound engine, the four RED on the parent.
- `REQ-GC-M`; `OB-GC-M` opens contract v2 (extends v1), realized in the registry at once.
- The generator's controls no longer pin the live unit's numbers (deltas from a run-time
  baseline + an independent recount; two mutations caught).
- `profiles/` crossed its byte ceiling — one unit's directed corpus, not a new unit:
  `decision_profiles-family-processor-corpus.md` re-derives it (2,867,200 → 3,145,728) and
  proposes the structural fix.

## SEMULITH-P4-0073 (leaf P4-SYSTEM.11, slice a) — the language for M

- `schema/semantics.sexp`: `mul`, `mulh`, `mulhsu`, `mulhu`, `div`, `divu`, `rem`, `remu` —
  arithmetic only, width-generic; signed overflow wraps; a zero divisor is outside the domain.
- `check_semantics.py`: a division must sit where its own divisor is known nonzero (6 new
  arms, 32/32); the generator re-derives the rule. `gen_definition.py`: the M variants lower
  only where the composition composes `riscv/m` (DEF-GEN 45/45; both modules regenerated —
  the pin and the language size 64 → 72).
- `definitions/riscv/m.sem.sexp`: 13 rules quoting RVI-M §11.1 (the brief's "§13" corrected
  against the pinned headings).
- `crates/semulith-core/src/muldiv.rs`: the model layer, six tests against independent routes;
  two mutations caught.
- Book: `plan/p4/m.md` (43 chapters).

## SEMULITH-P4-0072 (tree P4-SYSTEM) — the `.11` design brief: bind M

- Recorded before execution. Measured: `m.sexp` exists (13 instructions, pinned) with no
  semantics — the `.2` brief assigned it to an "M evidence leaf" that was never created; the
  language has no multiply or divide; the definition states ISA choices explicitly (`sll`'s
  mask) while operators stay arithmetic; RVI-M defines every edge (no trap); Sail's matched
  configuration supports M; v1 is frozen.
- The design: eight arithmetic operators (signed overflow wraps, as `add` does; a zero divisor
  is outside the domain, RISC-V's results stated by guards in `m.sem.sexp`, a static guard
  rule RED-proven); the bind with `OB-GC-M` in contract v2 (open); three evidence routes —
  an EVD-05 corpus, a generated operand table, the Sail matched experiment. Slices (a)–(d).
- `.8`'s closed checklists archived verbatim to `archive/P4-SYSTEM-4.md` (part 4 opened).

## SEMULITH-P4-0071 (leaf P4-SYSTEM.10, slice c) — THE LEAF ACCEPTANCE; the leaf CLOSES

- Reproducible from pinned inputs, measured: in a fresh worktree with no `target/`, the GS,
  GC, G1 and G0 reports regenerate byte-identically. Fidelity per axis: ten rows, never
  rolled up. Missing checks read `incomplete`: G-CONTRACT 14 of 100.
- `P4-SYSTEM.10` is **done**; the tree reads 10/18; the frontier moves to `.11`, bind M.

## SEMULITH-P4-0070 (leaf P4-SYSTEM.10, slice b) — the first CPU-SYSTEM report: incomplete, every open axis owned

- `scripts/gate_report.py --gate GS` (`build_cpusystem`): all ten processor-gate axes, each
  measured from the unit's own files — no constant, no hard-coded count. Five computed from the
  dossier; five answered by the unit's evidence manifest (`schema/gate.sexp`,
  `profiles/rv64gc-lab-v0/gate.sexp`), every declaration verified against the tree, the
  required kinds held by the generator. `passed` needs all ten green.
- `profiles/rv64gc-lab-v0/GS-REPORT.md`: `incomplete` — 9 of 10 open (G-INTERACTIONS green: 28
  cells, each dispositioned), every open item owned by `.11`–`.18`.
- Controls: the generator's self-test 17/17; GATE-REPORT 16/16, five reports in sync.

## SEMULITH-P4-0069 (leaf P4-SYSTEM.10, slice a) — the contract measure becomes the unit's own

- `scripts/gate_report.py` `contract_measure()`: a check is implemented for a unit exactly when
  THAT unit's registry realizes it under the obligation that declares it, over the EFFECTIVE
  contract (superseded records out). The old tree-wide grep credited rv64i with a check only
  rv64gc runs — measured in a scratch worktree (1 of 72; now 0).
- `schema/contract.sexp`: a `registry` construct; rv64gc's contract names its registry.
- Controls: the generator's `--self-test` (7 arms), run by GATE-REPORT; the registry's pairing
  test (RED-proven). rv64gc reads 14 of 100; rv64i 0 of 72, its GC and G1 reports
  byte-identical, G0's measure paragraph re-worded (and the book's quote of it).
- Book: `plan/p4/gate.md`, the `.10` chapter.

## SEMULITH-P4-0068 (tree P4-SYSTEM) — the `.10` design brief: the gate report is an instrument; eight leaves own what it will find open

- Recorded before execution. The census of rv64gc's evidence per processor-gate axis found:
  M and C declared but not bound (`encoding.sexp` `(status partial)`; the `.8` brief routed
  them to leaves that were never created); the contract measure not unit-scoped (26 check ids
  shared by MIRROR-DERIVE) and counting superseded records; the nearest report builder
  rv64i-shaped (hard-coded 21 cells, 51 ACT4 tests, G-REPLAY read from rv64i's suites); the
  seven Sail experiments recorded as prose, not records; all 46 requirements `planned`; no
  rv64gc external suite, mutation suite, snapshots, replay bundles, reducer or portability
  record.
- The design: `.10` builds a `GS` report over all ten axes from the unit's own tracked files —
  no constant, no hard-coded count, `passed` unreachable past an open axis — and records its
  first honest reading. Every open axis is owned before the instrument lands: `.11` bind M ·
  `.12` bind C · `.13` contract v2 · `.14` evidence records and obligation status · `.15`
  regression · `.16` replay · `.17` portability · `.18` the verdict and release decision.
- The closed `.8`/`.9` briefs archived verbatim to `archive/P4-SYSTEM-designs.md`.

## SEMULITH-P4-0067 (leaf P4-SYSTEM.9, slice d) — the ENVIRONMENT document, v1 frozen; the leaf CLOSES

- `profiles/rv64gc-lab-v0/ENVIRONMENT.md`: the versions, the boundary inventory dispositioned,
  the four assumptions with what would falsify each, the supersessions, the realized fixtures —
  and the gap it leaves, named: rv64i's eight base boundary assumptions were never restated
  for rv64gc.
- v1 is FROZEN (six members pinned). CONTRACT-FREEZE now judges before running its controls:
  its GREEN control copied the live files, so a broken tree read as "does not discriminate"
  instead of naming the edited record (the self-test knowledge card extended).
- `P4-SYSTEM.9` is **done**; the tree reads 9/10; the frontier moves to `.10`, the CPU-SYSTEM
  gate report. `make check` + `make gate` green.

## SEMULITH-P4-0066 (leaf P4-SYSTEM.9, slice c) — v0's stale statements superseded in v1

- Two frozen v0 statements are false of this unit: `OB-GC-PRIV-INSNS` calls wfi and
  sfence.vma no-ops (a wait state and a TLB exist since `.5`/`.3`), and the mirrored
  `OB-ECALL-EBREAK` says the traps are reported to the harness and stop execution (here they
  are delivered). v1 adds `OB-GC-PRIV-INSNS-V1` and `OB-GC-ECALL-EBREAK-V1` with `supersede`
  entries naming the old records and why; the old records stay, frozen. Their four checks are
  realized in the registry (14 of 14).
- The code comments that pointed forward to "`.9`'s charter" now name the v1 obligations, and
  `env.rs`'s module doc no longer scopes the boundary to rv64i alone. `make check` + `make
  gate` green.

## SEMULITH-P4-0065 (leaf P4-SYSTEM.9, slice b) — contract v1: the four environment assumptions, with realized fixtures

- `contract.sexp` gains v1 (extends v0, open) with the unit's first environment assumptions:
  `OB-GC-ENV-TRANSLATION-INPUTS`, `OB-GC-ENV-INTERRUPT-SOURCES` (none supplied in v1),
  `OB-GC-ENV-VIRTUAL-TIME` (one tick per step boundary; instret on retirement only),
  `OB-GC-ENV-RESERVATION-EVENTS` (no external invalidation at one hart) — each saying what would
  falsify it.
- A tracked check registry (`contract_checks_rv64gc.rs`) binds every v1 check, and `.8`'s
  partial-progress pair, to corpus guests and runs them under the corpus's own rule; a test
  refuses a declared check no entry realizes (RED-proven). One new negative fixture,
  `env-irq-sources`. `make check` + `make gate` green.

## SEMULITH-P4-0064 (leaf P4-SYSTEM.9, slice a) — the contract becomes a versioned document; v0 frozen; CONTRACT-FREEZE

- `schema/contract.sexp`: one `contract` form per version — its id, number, the version it
  extends, open or frozen, a statement, its member records (pinned by sha256 once frozen) and
  its supersessions. `profiles/rv64gc-lab-v0/contract.sexp` records v0 as it stands: 46
  members, frozen.
- CONTRACT-FREEZE (`scripts/check_contract_freeze.sh`, the 37th doctrine): every obligation
  belongs to exactly one version and carries its id and number; a frozen version's records
  still match their pins; extensions and supersessions are well-formed. 7/7 controls.
  Registered on its five surfaces; LIVE_STATUS re-derived (37 doctrines, 473 arms).
  `make check` + `make gate` green.

## SEMULITH-P4-0063 (tree P4-SYSTEM): the .9 design brief — a contract becomes a versioned, frozen document; v1 states the four environment assumptions with real fixtures

- Recorded before execution: contracts have no version mechanism (the version is a repeated
  string nothing checks); rv64gc states no environment assumption (46 CPU guarantees); the
  four topics are routed here by name a dozen times; two v0 statements are stale (wfi and
  sfence.vma described as no-ops); no profile check names a fixture.
- The design: a `contract` construct with members and supersessions, v0 frozen by a content
  manifest and a gate; v1 adds translation inputs, interrupt sources, counter progress and
  reservation invalidation as environment assumptions, each with a positive and a negative
  fixture that exist and run; stale statements superseded, never rewritten. Slices (a)–(d).
  `make gate` green.

## SEMULITH-P4-0062 (leaf P4-SYSTEM.8, slice e) — the sail attempt over the faults corpus; the leaf CLOSES

- Sail over the ten `.8` guests: 3 AGREE (mm-csr-ro-write, a-lrsc-fault, prio-sv39) + 7 NAMED
  — the counters guest (Zicntr off in the matched config) and the six injected guests, each
  diverging exactly at its first refused access (Sail's configuration carries no refusal
  regions). Recorded as the ledger's seventh experiment.
- `P4-SYSTEM.8` is **done**: every instruction completes or faults as a unit, fault priority
  is declared and pinned, and a fault injected at any suboperation leaves the required state.
  The tree reads 8/10; the frontier moves to `.9` (the environment contract v1 — design brief
  first). `make check` + `make gate` green.

## SEMULITH-P4-0061 (leaf P4-SYSTEM.8, slice d) — the injected-fault corpus; the partial-progress obligation

- Five guests over the typed carrier, each refusing one suboperation's access: `inj-atomics`
  (an LR's load — 5, no reservation registered; an SC's store — 7; an AMO's store after its
  load, and an AMO's load before its store — 7, rd and memory untouched), `inj-fp` (refused
  FP loads leave the f-register unwritten and FS Clean; refused FP stores leave memory
  unchanged), `inj-walk-l2/l1/l0` (a page-table read refused at each Sv39 level — the original
  access's access fault, never a page fault). 134/134; a mutation turning a refused walk read
  into a page fault is caught (and was invisible to the 129 earlier guests).
- rv64gc declares `OB-GC-PARTIAL-PROGRESS` (+ `REQ-GC-PARTIAL-PROGRESS`): every instruction
  completes or faults as a unit; the reads that crossed before a fault are declared, not rolled
  back; the fixtures named. The state candidate "pending or partially committed effects" is
  answered. Fetch-refusal guests named out of scope (no fetch model in the authoring tool).
  `make check` + `make gate` green.

## SEMULITH-P4-0060 (leaf P4-SYSTEM.8, slice c) — the typed fault-injection carrier

- A guest's expectations may declare `(refuse (kind fetch|load|store|walk) (base …) (size …))`
  regions; the rv64gc runner answers every boundary request whose kind matches and whose
  bytes intersect with an access fault (a `Refusing` environment under the fetch counter), and
  the spec-side authoring model predicts the same with the engine's own per-half causes. Both
  generated guest modules carry the refusal table.
- `inj-carrier` proves it end to end — a refused store, a refused load, an unrefused control,
  and an AMO whose store half is refused after its load completed (cause 7, rd and memory
  untouched). RED when the runner ignores refusals; a unit test pins the predicate's edges;
  the schema refuses an unknown kind. The authoring model's walk now answers an out-of-region
  PTE read with an access fault (it read zeros before). `make check` + `make gate` green.

## SEMULITH-P4-0059 (leaf P4-SYSTEM.8, slice b) — the fault-priority table declared and pinned

- `profile.sexp` declares `D-FAULT-PRIORITY` (with REQ-D-FAULT-PRIORITY and OB-FAULT-PRIORITY):
  the pinned synchronous-exception priority table (priv §2.1.1.15), the laboratory's one
  implementation-defined choice (load/store/AMO misaligned judged HIGH, before translation —
  `.3` decision 7), the unreachable rows named, and the guest pinning each adjacent pair.
- `prio-sv39` pins the four pairs no guest had: misaligned over a page fault (load and store),
  misaligned over a physical access fault, translation succeeding then the physical access
  refused (5/7), and illegal-instruction (FS=Off) over a page fault and over misaligned. It
  reuses sv39-fault-invalid's page-table prologue and adds one leaf mapping outside the
  region. 128/128 on the engine; Sail AGREE (128 steps). `make check` + `make gate` green.

## SEMULITH-P4-0058 (leaf P4-SYSTEM.8, slice a) — the CSR rd-before-trap defect fixed at root

- A CSR instruction whose write is refused (a read-only CSR) committed rd and then trapped —
  the zicsr rules read into rd before judging the write. The language gains `csr-rw`, the
  atomic read-write CSRRW's own sentence describes: both halves judged first, the old value
  yielded only on success; the six zicsr rules use it; the evaluator implements it.
- RED-first: `mm-csr-ro-write` failed on the old engine at step 9; after the fix 127/127,
  identity 125/0 with both new guests RED on the parent; Sail AGREE on `mm-csr-ro-write`
  (mhartid). `mm-csr-ro-counters` is a named not-matchable cell — the matched Sail config has
  no Zicntr, so the brief's own Sail evidence (a `cycle` probe) is corrected in place.
- Riding along: LR's unreachable boundary-misaligned cause 7 → 5; `a-lrsc-fault`'s prose said
  "cause 7 every visit" (the LR's is 5) — corrected and re-derived, every value identical; the
  authoring tool learns read-only writes, the immediate CSR forms and a family-aware header.
  The P4.8 book chapter opens. `make check` + `make gate` green.

## SEMULITH-P4-0057 (tree P4-SYSTEM): the .8 design brief — the unit discipline declared for rv64gc; a CSR rd-before-trap defect measured on both engines; typed, environment-shaped fault injection

- The `.8` brief recorded before execution: SEM-04/SEM-06 and the laboratory's declared
  preciseness; the engine's write-straight-through design (correct only where every fault
  point precedes every commit); a defect measured on both engines — a CSR instruction whose
  write is refused commits rd before trapping (semulith writes x5, sail does not); the
  standing implicit crossings declared, not hidden; the pinned fault-priority table; no
  rv64gc fault injection yet — designed as declared environment refusal regions. Slices
  (a)–(e).
- The closed `.5`/`.6`/`.7` design briefs and `.7`'s slice decisions archived verbatim to
  `archive/P4-SYSTEM-designs.md` (44,080 B; census exact). `make gate` green.

## SEMULITH-P4-0056 (leaf P4-SYSTEM.7, slice e3) — the decision record's closing measurement; the leaf CLOSES

- The qualification record's closing measurement, re-run at HEAD, lands as its own record
  (`reference_fp-model-layer-acceptance.md` — the decision record sits at its family's
  per-part ceiling): correctness spec-side and tracked (230 directed vectors
  + 3,168 seeded fixtures from the hardware-checked exact-rational reference), at corpus
  scale (0 of 63,752 disagreements), end to end on both engines (125/125 on the tracked
  engine; Sail 24 AGREE of 24 — an encoding/state match, Sail's FP being SoftFloat), and
  performance (the model layer 2.8–6.9× the raw backend, the exact OF/UF's cost).
- `P4-SYSTEM.7` is **done**: rustc_apfloat qualified behind `fp.rs`; F and D bound (150
  forms). The tree reads 7/10; the frontier moves to `.8` (faults, restart and partial
  progress — design brief first). `make check` + `make gate` green.

## SEMULITH-P4-0055 (leaf P4-SYSTEM.7, slice e2) — the numeric fixtures at scale + the per-op cost

- `scripts/gen_fp_vectors.py` now also emits `fp/tests/fixtures.txt`: 3,168 seeded cases from
  the exact-rational reference, biased toward the classes the rules distinguish, across all
  21 model-layer operations × both formats × every rounding mode (162 combinations; every
  flag raised). Read by `include_str!` and driven by a new unit test — all pass; RED when
  the underflow rule is removed. FP-VECTORS gates the second table with the same DRIFT rule
  (a new arm, 7/7); its doctrine row's stale "176 vectors" corrected.
- The final model layer's per-op cost measured beside the raw backend (release, 2M
  iterations): f64 add 47.8 vs 8.3 ns, div 122.7 vs 44.5 — 2.8–6.9× on the arithmetic core,
  the cost of evaluating every rounded result a second time for exact OF/UF. `make check` +
  `make gate` green.

## SEMULITH-P4-0054 (leaf P4-SYSTEM.7, slice e1) — the Sail matched experiment over the FP corpus: 24 AGREE of 24

- The override re-materialized from the tracked unit (unmoved since `.6`) and validated; Sail
  0.14 runs F and D with the same Precise flag-dirtiness rule the laboratory declares.
- All 24 floating-point guests (fp-fs-off, fp-fcsr-view, 11 F, 11 D) agree with their
  spec-derived expectations on Sail step for step — 927 steps, zero non-AGREE cells; the
  comparator's RED control (one corrupted expectation) diverges exactly there.
- Sail's FP is SoftFloat externs, so the result is the ENCODING/STATE match the brief
  designed plus one more numeric opinion — never numeric independence. `references.sexp`
  records the sixth experiment; the slice (e) split recorded. `make gate` green.

## SEMULITH-P4-0053 (leaf P4-SYSTEM.7, slice d5) — THE BIND: the unit composes riscv/d

- `encoding.sexp`: the `d` slot becomes `(extensions "riscv/d")` (147 instructions + 3 pseudo
  spellings; M and C remain slots); the census 118 → 150 in all four places as the 32-form
  `d_double` family; `definition_rv64gc.rs` regenerated (32/32 D forms, `FToF`).
- `exec_rv64gc.rs`: the `FToF` arm through `fp::convert`, flags accrued; `touches_fp_state`
  covers it. The 11 D guests tracked (125/125; the 114 older guests byte-identical);
  REQ-GC-D + OB-GC-D; the matrix places them on the seven existing axes.
- The census leg's D exclusion flipped by its own condition (150 == 150). The P4 tree's
  closed (c4)–(c6) checklists archived. `make check` + `make gate` green.

## SEMULITH-P4-0052 (leaf P4-SYSTEM.7, slice d4) — the staged D corpus

- 11 D guests staged in the bind worktree (the (c5) discipline), every expectation derived
  spec-side by the authoring tool — taught D by taking the format as data (F's 11 guests
  re-derive byte-identically through it): the Off gate, 64-bit transfers and a NaN-boxed
  single read as a double, arithmetic with all five flags, the fused forms, sign injection,
  min/max, compares, the ten classes, the integer and format conversions (boxing on the
  single side, signaling NaNs both ways), reserved rounding modes on exact operations.
- Three authoring defects caught and re-derived, never fitted (a misaligned doubleword
  address, a tool vocabulary gap, a false comment found by hand-checking derived values).
- The scratch engine (riscv/d composed, the FToF arm) passes 125/125 (RED when FToF ignores
  its mode); identity 114/0 with every D guest RED on the parent; re-derived from scratch
  22/22 byte-identical. No tracked content changed; `make gate` green.

## SEMULITH-P4-0051 (leaf P4-SYSTEM.7, slice d3) — fp.rs's format conversions; the record's deviation (ii) withdrawn

- `fp.rs::convert(m, n, rm, a)` (FCVT.S.D/FCVT.D.S): narrowing through the backend with OF/UF
  on the exactly-unbounded value, widening exact, NaN canonical, NV on a signaling NaN from
  the backend's own status; `specfp.convert`; 54 spec-side vectors (230 total); FP-VECTORS'
  hardware arm now also checks double→single RNE narrowing (directed ties) and exact widening
  (agree 2131).
- The planned patch for the qualification record's "deviation (ii)" passed its tests while
  bypassed; probed, the backend raises NV for a signaling NaN through a conversion, and all 24
  recorded cases were the MPFR oracle's (no signaling NaN in MPFR). The record carries a
  second dated amendment: two genuine backend flag deviations, not three. The schema, `fp.rs`
  and the tree text that repeated the error corrected; the oracle knowledge card extended.
- fp.rs over slice (a)'s 63,752-case corpus: 0 disagreements with the exact-rational
  reference. `make check` + `make gate` green.

## SEMULITH-P4-0050 (leaf P4-SYSTEM.7, slice d2) — the language for D: f2f + d.sem.sexp

- `schema/semantics.sexp`: `(f2f m n rm a)`, the format conversion — the one operation the
  D rules need that the width-generic FP vocabulary could not state (62 → 63 operators);
  `check_semantics.py` requires both formats literal and distinct (3 new arms).
- `gen_definition.py` lowers it to `Sem::FToF` only where `riscv/d` is composed (refused by
  name otherwise — RED-proven by mutation); the tracked modules change only their generator
  fingerprint and the derived language count; DEF-GEN 37 arms.
- `definitions/riscv/d.sem.sexp`: 32 rules, each F's counterpart at format 64, quoting the
  pinned D chapter (19 quotes judged, 0 findings). The assembler derives D's register files
  from them: 32/32 against spike-dasm, 4 refusals by name.
- The P4 tree's closed (b)–(c3) part 2 checklists archived verbatim. `make check` + `make
  gate` green.

## SEMULITH-P4-0049 (leaf P4-SYSTEM.7, slice d1) — the rv_d/rv64_d re-pin + the d.sexp fragment

- `rv_d`/`rv64_d` pinned in the rv64gc ledger (2,091/465 B; 26 + 6 = 32 forms; 3 pseudo
  rows written out, not carried), fetched through the tracked route and byte-identical to
  the census fetch; the census leg excludes them by name until the bind (RED-proven:
  exactly the 32 D names without it).
- `definitions/riscv/d.sexp` generated: requires `riscv/rv64i` and `riscv/f` (D depends on
  F and reuses its rs3/rm), owns no field. Trial units: D without F refused by name; F + D
  composes 147 instructions collision-free. The other 8 fragments byte-identical.
- The slice (d) split recorded: the FP vocabulary is width-generic, so D adds only the
  format conversion. `make gate` green; no Rust touched.

## SEMULITH-P4-0048 (leaf P4-SYSTEM.7, slice c6) — THE BIND: the unit composes riscv/f

- `encoding.sexp`: the `f` slot becomes `(extensions "riscv/f")`; the census 88 → 118 in
  all four places (schema, dossier reader, scope block, PROFILE-CONSISTENCY) as the 30-form
  `f_single` family; `definition_rv64gc.rs` regenerated (30/30 F forms).
- `exec_rv64gc.rs`: the FS=Off gate judged at the instruction head (cause 2 before any
  effect), f-register writes marking Dirty, the rounding-mode arm (static or frm; reserved →
  cause 2), every F operation through `fp.rs`; `privilege::accrue_fflags` (sticky, Dirty only
  when fflags changes).
- 11 F guests tracked (114/114; the 103 older guests byte-identical); REQ-GC-F + OB-GC-F;
  the matrix places them on the seven existing axes (28 cells resolve); EXERCISE-COVERAGE
  118/118; the pinned tables 118 == 118.
- Two stale facts from earlier slices corrected: `fp.rs` cited slice (a)'s 362 overflow
  cases (290 since the amendment); the schema's FP contract counted two backend deviations
  (three). And one of (c5)'s: `f-sgnj`'s comment opened with `|sNaN|`, whose bar is the
  directive separator — an empty derivation, refused by DOSSIER-SCHEMA only once the guests
  were staged (the sweep reads `git ls-files`; it judged 202 documents, not 213); the tool
  now refuses it, the pair re-derived; the zero-hits knowledge card extended. `make check` + `make gate` green.

## SEMULITH-P4-0047 (leaf P4-SYSTEM.7, slice c5) — the staged F corpus; specfp learns the signed fused forms

- `scripts/specfp.py`: `fma` takes `negate_product`/`negate_addend` and computes FMSUB,
  FNMSUB and FNMADD from the exact signed terms (the zero-sum sign and the ∞−∞ case read
  them) — the reference had only FMADD. Cross-checked against the independent sign-flip
  construction: 464,000 cases, 0 disagreements; two mutations caught (490 / 153,438).
  FP-VECTORS unchanged (176 vectors, the default arguments keep FMADD's bytes).
- The staged corpus (untracked, in the bind worktree): 11 F guests — FS=Off, NaN-boxing and
  the transfers, rounding modes incl. the reserved ones, flags, fused forms, sign injection,
  min/max, compares, classify, conversions, the Precise Dirty rule — every expectation
  spec-derived (EVD-05). On the scratch engine: 114/114 guests (RED: accrual dropped →
  f-arith step 9); identity 103/0 with all 11 F guests RED on the parent; re-authored and
  re-derived from scratch 22/22 byte-identical. The P4 tree's closed Commit Log rows
  archived to part 3. `make check` + `make gate` green.

## SEMULITH-P4-0046 (leaf P4-SYSTEM.7, slice c4 part 2) — fp.rs, the model layer; the qualification oracle's two rule defects; FP-VECTORS

- `crates/semulith-core/src/fp.rs`: the RISC-V policy over rustc_apfloat — canonical NaN,
  NaN-boxing, the rounding-mode resolution (reserved → None), add/sub/mul/div/fma through the
  backend, sqrt computed exactly (integer √ + sticky), min/max/compares/class in bits,
  float↔int per Table 5 (NaN → max + NV), the FMA ∞×0 rule. OVERFLOW and UNDERFLOW are judged
  on the exactly-unbounded result (a backend format of equal precision, 15-bit exponent).
- 176 spec-side unit vectors, generated by the tracked `scripts/gen_fp_vectors.py` from the
  exact-rational reference `scripts/specfp.py`; FP-VECTORS (the 36th doctrine) refuses a
  hand-edited vector and re-checks the reference against the host's hardware IEEE on directed
  ties (6/6; a half-up mutation caught).
- Their first run exposed that slice (a)'s MPFR oracle judged OF on the exact magnitude (72
  false overflows) and UF on the delivered result (hiding a third backend deviation at the
  smallest-normal boundary). Corrected, fp.rs: 0/51,840 vs MPFR, 0/63,480 vs the reference.
  The decision record amended; the pin expressed `=0.2.3` (Cargo.lock pins the artifact).
  `make check` + `make gate` green (461 arms).

## SEMULITH-P4-0045 (leaf P4-SYSTEM.7, slice c4 part 1) — the dependency store on-volume

- Slice (a)'s first registry dependency (`rustc_apfloat`, with `bitflags`/`smallvec`) was
  resolved by every routine build through the shared `~/.cargo` cache (`cargo metadata`
  named the user-home path): the on-volume fetch had been one command's environment.
- `.cargo/config.toml` replaces crates.io with the untracked on-volume `.app-data/vendor`
  (Cargo.lock's checksums stay the tracked identity); `make vendor` populates it
  idempotently and is a prerequisite of check/clippy/test/bench/gate; the three CI
  workflows and bootstrap populate it; a missing store fails loudly. The shared cache was
  left untouched (§13). README, the book's annex, a knowledge card. `make check` + `make
  gate` green.

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
