# CHANGELOG shard — SEMULITH-P4-0080 … SEMULITH-P4-0046

> Sharded from `CHANGELOG.md` under its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

