# P1-LAB: build the processor laboratory and the machinery that can tell the truth about it

## Metadata

- Tree ID: `P1-LAB`
- Status: `done` (first leaf landed `2026-09-27`; completed `2026-09-29` — 13/13 leaves,
  reopened once for `.13`; gate `G1` RUN, verdict `incomplete`: criterion 6, the
  C-toolchain guest, is owned by `P2-SCALAR.5` — the G0 precedent)
- Roadmap lane: `ROADMAP.md` §6 → **P1 — Build the processor laboratory**
- Gate: `G1`
- Depends on: `P0-PROFILE` (gate `G0`)
- Unlocks: `P2-SCALAR`, `DSP-REVIEW`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Three Rust crates that can execute a vertical instruction slice deterministically under a
controlled environment, and the evidence machinery — canonical definition, requirement graph,
comparator, reducer, mutation suite — that makes a result from them mean something.

## Non-Goals

- No board and no devices. The laboratory supplies controlled responses; a board models real
  hardware and follows the CPU gate (`SCP-03`).
- No complete instruction scope. That is `P2-SCALAR`.
- No optimization. The first backend is a **readable** interpreter (`ROADMAP.md` §1).

## Acceptance Criteria — gate `G1`

1. Failures are **replayable** from recorded inputs.
2. Model limitations are **distinguishable** from target traps (`SEM-01`, `SEM-02`).
3. Malformed evidence links are **rejected** — schema validity alone is not sufficient.
4. Known validator mutations are **detected**.
5. The performance baseline is **measured** on a named host, with allocation counts.
6. A **compiled freestanding guest program retires under first-divergence comparison**
   against a pinned reference — the star-facing proof, not a hand-encoded toy; C is the
   first guest path (`ROADMAP.md` §6, sharpened by `ROADMAP-V3.3`). *Absorbed into this
   tree by `.12` (`2026-09-28`): the tree's five criteria had drifted from the roadmap's
   six. Standing at the `.12` measurement: the four tracked guests are freestanding
   programs assembled by the tracked assembler and retire under first-divergence
   comparison against sail-riscv AND spike (34/34 aligned steps) — but no C-toolchain
   guest exists, so the criterion stands UNMET as written; the gate report says so, and
   the owner is `P2-SCALAR.5` (external and directed campaigns).*

## Task Tree

- ID: `P1-LAB.1` — **crate skeleton**
  Status: `done`
  Goal: replace the placeholder crate with `semulith-core`, `semulith-verify`, `semulith-cli`, wired to the ownership rules in `docs/ARCHITECTURE.md` §4.
  Acceptance: `semulith-core` depends on neither of the others; `semulith-verify` contains the test fixtures; `make check` green at `-D warnings`.
  Result: met, `2026-09-27`. `crates/app` (the `semulith` placeholder) is replaced by the three
  laboratory crates. `semulith-core` has **no** dependencies (`Cargo.lock`: the `semulith-core`
  package lists none); `semulith-verify` carries the fixtures home (`pub mod fixtures;` — filled
  by `P1-LAB.4`) and depends only on core; `semulith-cli` (binary name `semulith`, ROADMAP.md §8)
  depends on both and duplicates nothing. The workspace builds for the host and for
  `wasm32-unknown-unknown` in the same commit — the browser half of this skeleton is
  [`PORT-WEB.1`](PORT-WEB.md), landed in the same commit by design. The dependency edges are
  declared now and first exercised by `P1-LAB.2`+.

- ID: `P1-LAB.2` — **target arithmetic primitives** *(task card `T005`)*
  Status: `done`
  Goal: source-linked widths and operations with explicit intermediate precision, truncation, sign/zero extension, and shift corner cases (`SEM-03`).
  Acceptance: boundary cases plus **exhaustive checks at a tractably reduced width**; host-mode consistency verified rather than assumed.
  Result: met, `2026-09-27`. `semulith-core::arith` — 18 primitives (ALU reg/imm, shifts, word ops,
  extension/extraction, LUI/AUIPC offset), each with a SEM-03 contract and a source link to its
  requirement record and pinned locator (`REQ-D-XLEN/ALU-REG/ALU-IMM/SHAMT/WSUFFIX/LUI-AUIPC/
  LOAD-EXT`). Verification: boundary cases at XLEN, an **8-bit exhaustive layer** over every
  `(x, y)` / `(x, shamt)` / `(x, width)` against references formulated on a different host
  width (multiply-as-shift, De Morgan, u16/u128 paths), and a boundary-heavy 100k-draw sweep
  of the word ops against a u64-width reference. The exhaustive layer caught a real test-design
  defect — signed comparison and arithmetic shift are width-sensitive — fixed by embedding the
  narrow signed view at XLEN (the lesson is promoted to
  `docs/knowledge/reduced-width-verification-of-signed-ops.md`). Unmasked shift amounts panic
  (`debug_assert`) instead of silently wrapping: a decoder bug must not become a plausible
  wrong result. The requirements' `implementation_status` stays `planned` — these are the
  executable halves; the obligations name instruction-level checks that need the interpreter
  (`.8`) to exercise state writeback.

- ID: `P1-LAB.3` — **architectural state**
  Status: `done`
  Goal: generated state accessors and inspection metadata from the state descriptors, including aliases and required pending state (SEM-08).
  Acceptance: writing one alias correctly affects every other view (catalog `C02`); fixed-width storage, no per-access allocation (`RUST-03`).
  Result: met, `2026-09-27`. `semulith-core::state` is GENERATED from `profiles/rv64i-lab-v0/state.sexp` by
  `scripts/gen_state.py` (through `dossier_sexp.load_state`, the single mapping owner; byte-deterministic;
  the input sha256 rides in the module header — OWN-03). One fixed-width storage: `[u64; 32]` + pc,
  264 bytes inline, no heap (RUST-03 — the API returns values from references, so per-access allocation
  is not possible by construction). x0 hardwired: write discarded, read masks to 0. The three roles the
  ISA chapter names (x1/x2/x5) are emitted as alias constants — views over the one storage, C02's
  question answered in both directions and held by tests. `ELEMENTS` carries the inspection metadata
  (name/width/class/role/source per element); the SEM-08 hidden-state census rides as data (7 candidates
  checked, none present — the recorded justification that replay reduces to registers, pc and memory).
  The generator REFUSES by name any shape it cannot emit (another profile, non-64 width, unmapped
  special register, missing census). The 21st doctrine `STATE-GEN` (`scripts/check_state_gen.sh`)
  regenerates in memory and refuses drift; fired RED against a hand-edited module before registration;
  the owner→mirror pair is registered in `doctrine/fact_ownership.tsv`. Reset is the laboratory
  declaration (REQ-D-ENTRY-STATE/OB-ENV-RESET: x1..x31 = 0, pc = environment-supplied entry).
  Lessons: promotion: declined (the three design notes — fmt-stable emission, family_for naming the dossier family from the file NAME, descriptor↔arith binding at generation time — are P1-LAB-generation specifics; nothing generalizes past `.6`, where the generation manifest lands).

- ID: `P1-LAB.4` — **environment boundary and fixtures**
  Status: `done`
  Goal: the request/response contract types in `semulith-core`, and controlled memory, fault and event fixtures in `semulith-verify` implementing them.
  Acceptance: the boundary is testable **without** the instruction handler (`docs/CPU_ENVIRONMENT.md` §4.1); negative fixtures are reported as contract violations, not target exceptions.
  Result: met, `2026-09-27`. `semulith-core::env` owns the contract: `Request` (Fetch — width pinned
  to 32 by construction per OB-ENV-FETCH-SUPPLY; Load/Store at `AccessWidth` B/H/W/D per
  OB-ENV-ACCESS-WIDTHS — an unofferable width cannot be formed), `Response` (raw bits, no
  extension — REQ-D-LOAD-EXT stays instruction-layer), and two failure families kept apart by
  construction: `Failure` (target-facing: AccessFault per OB-ADDRESS-SPACE, Misaligned per
  OB-MISALIGN-DATA — "not substituted", exactly as the profile declares) and
  `ContractViolation` (the environment broke a rule — SEM-01's separation, boundary-local
  until `.5` re-homes it). Addresses are bare `u64` (SEM-05; OB-ENV-ADDRESS-UNITS). One trait,
  `Environment::request`, drives every crossing — scriptable, countable, replayable.
  `semulith-verify::fixtures` implements it: `FlatMemory` — the platform's one little-endian
  main-memory region (OB-MAIN-VS-IO), re-read per fetch (OB-CODE-VISIBILITY, a store to a
  later-fetched address is visible immediately), fetch counter as the no-extraneous-fetch
  witness, alignment judged before region membership (order stated, testable); `ScriptedEnv`
  — the whole conversation pinned in advance, faults scriptable as environment answers, and a
  request the script does not cover reports `ResponseMismatch`/`ScriptExhausted` instead of
  inventing data — the §4.1.4 negative-fixture rule, exercised for real. No asynchronous
  event exists to script (OB-ENV-EVENT-DELIVERY: the platform declares none). Cold reset
  (OB-ENV-RESET) is construction plus image load. Lessons: promotion: declined (fixture
  specifics — alignment-before-region ordering, u128 region checks — are per-slice design
  choices recorded in the module docs; nothing here is a cross-cutting lesson yet).

- ID: `P1-LAB.5` — **typed outcome families**
  Status: `done`
  Goal: `TargetEvent`, `Advance`, `ModelError`, `UndefinedCase` as separate types (`SEM-01`).
  Acceptance: a target exception can be delivered and execution continue; an unimplemented instruction cannot be reported as an illegal-instruction trap.
  Result: met, `2026-09-27`. `semulith-core::outcome` owns the four families, and nothing converts
  between them: `TargetEvent` (`Exception` with the unprivileged cause vocabulary — each cause named
  by its rule; `RequestedTrap` for ECALL/EBREAK), `Advance` (`Completed`, `Stop{reason}` — no
  waiting or partial advance, platform facts recorded in the type's docs), `ModelError`
  (`Unimplemented`/`InvalidDescription`/`InconsistentState`/`ContractViolation` — `.4`'s
  boundary-local violation family re-homed), `UndefinedCase` (`ReservedDecode` — the
  REQ-D-RESERVED-DECODE case carried as its own outcome, never auto-converted to an exception).
  A step returns `StepOutcome`, one of the four; `.8` produces it, the harness matches it.
  Tests prove the acceptance with a stub stepper (test code, not production semantics): a
  delivered `Breakpoint` trap is recorded by the harness and the next instruction still runs;
  the unimplemented arm is a `ModelError`, and the exhaustive match shows extracting an
  `IllegalInstruction` trap from it has no typed expression. Lessons: promotion: declined
  (family shapes are `.8`'s design consumer; nothing here generalizes past this module).

- ID: `P1-LAB.6` — **canonical definition skeleton** *(task card `T003`)*
  Status: `done`
  Goal: owned encodings, state and semantics plus a deterministic generation manifest carrying definition, generator, configuration and source fingerprints (`OWN-01`, `OWN-03`).
  Acceptance: **no duplicate executable owner** for any semantic rule; regeneration is byte-deterministic and CI detects drift.
  Result: met, `2026-09-28`. `scripts/gen_definition.py` lowers the unit's canonical definition into
  `semulith-core::definition`: the 12 declared operand fields (scatters attached), the 52
  instructions' decode rows (mask/value/operands/upstream-table/citation), and every semantics
  rule's effect tree as a typed `Sem` value — lowered from `definitions/riscv/rv64i.sem.sexp`,
  the execution authority (`decision_interpreter-before-compiler`), never handwritten. OWN-03's
  manifest rides as data (`MANIFEST`): the four canonical inputs by path and sha256, the
  generator named and content-hashed, the configuration (profile/ilen/fragments) as data, and
  the upstream source fingerprints the fragment pins. Regeneration is byte-deterministic and
  formatter-stable; the 22nd doctrine `DEF-GEN` (`scripts/check_definition_gen.sh`) regenerates
  in memory and refuses drift; fired RED against a hand-edited module before registration. The
  generator re-derives the SEMANTICS doctrine's checks it emits through — schema validation for
  every input, the binding rule (split `imm12`/`bimm12`, `shamt`), the MODEL-COMPOSE.6
  refinement rule, completeness — and refuses by name what it cannot emit (another unit, an
  unsupported ilen, an instruction without semantics, an operand the encoding does not provide,
  a missing semantics document, a non-literal width). `decode(word)` is generated dispatch
  metadata; evaluation stays with `.8`. Ten Rust suites re-derive the generation-time invariants
  on the emitted data (manifest completeness, alphabetical completeness, fixed-bit disjointness,
  self-decode, scatter accounting, the binding rule, the FENCE-decoration ratchet). The
  owner→mirror pairs (encodings, semantics, state → `definition.rs`) are registered in
  `doctrine/fact_ownership.tsv` and its census. Lessons: promotion — declined (the fmt-stable
  fully-broken emission trick is a P1-LAB-generation specific; see the checklist's design notes).

- ID: `P1-LAB.7` — **graph and report checker** *(task card `T004`)*
  Status: `done`
  Goal: validate identifier references, profile-scope consistency, graph integrity, artifact existence and hashes, evidence freshness, and gate policy over the JSONL records (`docs/EVIDENCE_AND_GATES.md` §3).
  Acceptance: rejects orphan IDs, stale hashes, unsupported `passed` claims, missing evidence, and deleted dependency links. ⭐ This leaf also discharges the standing gap that `PACKAGE_CHECKS.md`'s schema results are **cited, not re-derivable here** — rule `RUST-01` makes the re-derivation a Rust deliverable, not a Python dependency.
  Design: recorded before code; archived to [`archive/P1-LAB-2.md`](archive/P1-LAB-2.md) (per-part ceiling).
  Result: met, `2026-09-28`. `semulith-verify` gains five modules (29 suites): the checker
  refuses orphan IDs, stale hashes, unsupported `passed` claims, missing evidence, deleted
  dependency links, out-of-scope profiles, duplicate ids, unpinned sources, undeclared checks,
  and dependency cycles — one mutation suite per designated rejection, plus a fully-met
  bundle gating `passed`. The intact frozen bundle is graph-clean and honestly `incomplete`
  (its evidence is deliberately `planned`). The PACKAGE_CHECKS rows re-derive in Rust: 5/5
  records validate, 6/6 negative controls rejected with reasons named, the synthetic source
  fingerprint matches `sources.json`'s pin. `semulith check-examples` presents the report;
  `RECORD-SCHEMA` (doctrine 15) runs the Rust engine after the Python phase on every commit
  and fired RED against a mutated requirement (orphan evidence named, rc=1) before landing.
  The library stays `std::fs`-free; the workspace still builds for `wasm32-unknown-unknown`.

- ID: `P1-LAB.8` — **first execution slice** *(task card `T006`)*
  Status: `done`
  Goal: a vertical slice executing an **independently encoded** program under the controlled environment, with first-divergence comparison against the reference.
  Acceptance: correct state, access and exception observations; the divergence report names the first differing observation, not a final checksum.
  Design: recorded before code; archived to [`archive/P1-LAB-2.md`](archive/P1-LAB-2.md) (per-part ceiling).
  Result: met, `2026-09-28`. The definition executes. `semulith-core::exec` evaluates the
  generated `Sem` trees — 24 test suites on the core side cover every outcome family and the
  width algebra (including the two readings that pin it: LUI's sign extension from bit 31,
  LB's from 8; and the `sraiw` case that forced shifts to operate at the operand's width — an
  arithmetic shift of the low 32 bits replicates bit 31, not bit 63). `semulith-verify::run`
  records `(pc, word, writes, trap)` steps plus the full boundary-crossing log, and
  `compare` reports the first divergence with the differing field named (RED/GREEN arms
  mirroring `compare_traces.py`'s self-test). `semulith-verify::elf` loads the writer's
  ELF64 with named-field refusals. The offline differential runs all four guests against the
  generated fixture on every `make check` (75 verify suites green); the live experiment
  agrees with sail-riscv AND spike on every enabled comparison — 34 aligned steps, each run
  reproducing byte-identically. The 23rd doctrine `GUEST-GEN` fired RED against a hand-edited
  fixture before registration.

- ID: `P1-LAB.9` — **validator mutation suite** *(task card `T007`)*
  Status: `done`
  Goal: intentional mutations that must be detected — wrong sign extension, suppressed register write, wrong trap cause, illegal-opcode substitution for a model limitation, an extra memory access, shifted event delivery, an overbroad mask hiding a changed defined bit, a stale reference configuration (`EVD-09`).
  Acceptance: **every** designated wrong behaviour is detected. A suite never run against a broken implementation is not known to detect anything.
  Design: recorded before code; archived to [`archive/P1-LAB-2.md`](archive/P1-LAB-2.md) (per-part ceiling).
  Result: met, `2026-09-28`. The suite lands as `semulith-verify::mutate` — 11 suites: the nine
  designated arms (eight EVD-09 classes plus the JALR odd-bit arm the fixture note names), the
  four-guest data-crossing census pin, and the suppression exhibit. `exec::step_over` /
  `run::run_over` are the single execution path parameterized over the instruction table; the
  generated-table scan is pinned to `definition::decode` by a core suite over every canonical
  word, operand-varied encodings, and unclaimed words. Every arm that runs a guest first
  re-derives the pinned GUEST-GEN expectations against the real model, then asserts the mutant's
  divergence at its designated step naming its designated field: the JALR arm faults with
  `InstructionAddressMisaligned` at `0x80000029` exactly as the fixture note predicted; the
  extra-access arm proves the architectural trace agrees while the crossing census catches the
  phantom load; the suppression arm exhibits a writes-blind comparator agreeing with a mutant
  the real comparator catches. The completed-leaf checklists `.1`–`.8` archive to
  [`archive/P1-LAB.md`](archive/P1-LAB.md) — the live file crossed its per-part ceiling; the
  ceiling was obeyed, not raised. No new doctrine (no generated artifact; the suite guards
  discriminating power, not drift). Lessons: promotion — the general lesson ("a gate that has
  never been observed RED is not known to work") already lives in `TOOLBOX.md` and
  `docs/knowledge/self-test-arms-that-never-ran.md`; the seam's design rule (a mutation is data
  through the one evaluator, never a second implementation) is this tree's Decisions entry —
  nothing new generalizes past this leaf. The frontier moves to `.10` (replay and reduction).

- ID: `P1-LAB.10` — **replay and reduction**
  Status: `done`
  Goal: an input bundle that replays the same result, and a minimizer whose output retains the original divergence.
  Acceptance: a seed is accompanied by algorithm/version and the actual relevant event choices — a bare seed is insufficient.
  Design: recorded before code; archived to [`archive/P1-LAB-2.md`](archive/P1-LAB-2.md) (per-part ceiling).
  Result: met, `2026-09-28`. `semulith-verify::replay` is the recorded input bundle:
  algorithm pins flattened from `definition::MANIFEST` (profile, ilen, generator name+sha256,
  every input pin) plus the harness version and the `production`/`mutant:<name>` model, the
  platform region, the entry, the image words with a sha256 guard, the recorded event choice
  (`DeclaredNone`, OB-ENV-EVENT-DELIVERY named), the step budget, and the recorded steps plus
  the stop's canonical render. `replay()` checks identity by name — definition pins against
  the live manifest, then the image digest against the bundle's own words — and walks
  recorded-vs-replayed through `run::compare`, so a drifted result is named at its first
  differing observation. JSON both ways through the crate's own reader and a hand-rolled
  writer; a document missing any accompaniment fails parse naming the field — the bare-seed
  refusal is structural. `semulith-verify::reduce` is the ddmin minimizer: retention is the
  original first divergence exactly (same step, same field description — identical prefix
  semantics make the whole divergence byte-identical), every accepted removal preserves it
  structurally, and `Reduction` re-derives the retained divergence from the minimized words.
  The named boundary holds: phantom-load (the census class) is refused `NoDivergence` —
  observation reduction cannot retain what observations do not carry. `semulith-cli` gains
  `bundle` (write the bundle JSON), `replay` (re-derive and judge it), and `reduce` (print
  the minimized program with its retained divergence); all three exercised end to end. The
  `.9` acceptance checklist archives to [`archive/P1-LAB.md`](archive/P1-LAB.md) (per-part
  ceiling obeyed). No new doctrine (no generated artifact; the suite guards replay fidelity
  and discriminating power, not drift). Lessons: promotion — declined (the ddmin
  retention-invariant and the bare-seed-structural-refusal are this leaf's design notes,
  recorded in the module docs; the census-class boundary is the `.9` lesson reused, not a
  new one). The frontier moves to `.11` (performance baseline).

- ID: `P1-LAB.11` — **performance baseline**
  Status: `done`
  Goal: measure arithmetic, control-flow, memory and fault-heavy mixes separately on a **named** host, with allocation counts and trace settings, in untraced / instrumented / diagnostic modes.
  Acceptance: repeated measurement characterizes the noise **before** any regression threshold is set (`RUST-04`); no invented MIPS target; traced and untraced executions agree on observations (`RUST-02`).
  Design: recorded before code; archived to [`archive/P1-LAB-2.md`](archive/P1-LAB-2.md) (per-part ceiling).
  Result: met, `2026-09-28`. `semulith-verify::bench` is the measurement harness: the four
  mixes generated programmatically (every word pinned to the generated definition by the
  decode round-trip suite), the three modes sharing one counting environment so the census
  is comparable without being recorded, `agree` stating RUST-02 as data (facts plus every
  recorded stream), the std-only counting allocator, and the noise statistics.
  `semulith bench` names the host — **Apple M4 Pro; Darwin 27.0.0; rustc 1.95.0
  (59807616e 2026-04-14)** — and measured every cell at iterations=10000, warmup=2,
  reps=12: untraced 47.2–54.1 ns/step across the four mixes (~19–21 M instructions/s),
  instrumented +24–40% over untraced, diagnostic a further ~4–8%; allocations 1.00/step
  untraced (the `extract_operands` Vec — RUST-03's departure, now a measured number:
  126.3–140.8 bytes/step), 1.19–1.42/step traced; noise spread 1.7–7.4% per cell with one
  scheduler outlier at 113% on a millisecond-scale cell — the honest spread a future
  threshold must be set FROM, and none is set. Static vs dynamic observer dispatch:
  ×0.974–1.002 across the mixes — within the measured noise, so the open question resolves
  by measurement: static generics stay the default; a trait object costs nothing measurable
  at laboratory scale. RUST-02 was checked as it measured: all four modes agree on steps,
  stop, final state and census on every mix, every recorded observation stream identical,
  and the check is a refusal path (exit 1). 10 new suites (124 verify total). No new
  doctrine (no generated artifact — the harness guards measurement honesty, not drift).
  Lessons: promotion — declined (the harness-policy shape and the image-word lookup are
  this leaf's design notes, recorded in the module docs; the RUST-03 finding is this tree's
  Decisions entry; "a zero-cost assumption is a claim until measured" already lives in
  ARCHITECTURE §6). The frontier moves to `.12` (the G1 gate report). The `.10` acceptance
  checklist archives to [`archive/P1-LAB.md`](archive/P1-LAB.md) — the live file crossed
  its per-part ceiling; the ceiling was obeyed, not raised.

- ID: `P1-LAB.12` — **the `G1` gate report**
  Status: `done`
  Goal: generate the gate report from pinned inputs.
  Acceptance: reproducible from recorded definitions, tools, inputs and event choices; reads `passed` or `incomplete`.
  Design (recorded before code, `2026-09-28`): the G0 machinery generalized, not
  paralleled — one generator, one drift check, both gates.
  1. `scripts/gate_report.py` gains `--gate G1` (default `G0`, byte-unchanged output) and
     `build_g1(profile)` → `profiles/<profile>/G1-REPORT.md`, derived entirely from tracked
     inputs, regenerating byte-identically in a fresh clone (the G0 property, kept).
     The report evaluates the SIX criteria `ROADMAP.md` §6 states for `G1` — the five this
     tree carried, plus the sixth the roadmap added and this tree had not absorbed (the
     drift this leaf repairs, see the tree's acceptance criteria): the **compiled
     freestanding guest retiring under first-divergence comparison against a pinned
     reference**. Each criterion's standing is MEASURED from tracked files, never asserted:
     replay/reduce machinery and its CLI wiring by concrete name; the four outcome families
     and the SEM-02 arm by concrete type/arm names; the graph checker and `check-examples`;
     the mutation suite's arm count re-derived from its test module (11) and its
     model-level mutants from the `MUTATIONS` table (4); the baseline from the new tracked
     record (below), every required field present; the guest census from `guests/` itself —
     four `.s` sources, zero `.c`. The verdict is `passed` only while ALL SIX criteria are
     met — EVD-08's forbidden outcome ("passed with a missing required check") generalized:
     the generator has no code path to `passed` over a missing criterion. Today criterion 6
     stands unmet as the roadmap states it (the four guests are assembled by the tracked
     assembler from `.s` sources and DO retire under first-divergence comparison against
     sail-riscv and spike — 34/34 aligned steps, re-runnable via
     `scripts/run_semulith_smoke.py` — but no C-toolchain guest exists), so the report reads
     `incomplete` and names exactly that, with the owner (`P2-SCALAR.5`). This mirrors the
     G0 precedent exactly: the milestone's leaves complete; the gate's verdict stays honest.
  2. `profiles/rv64i-lab-v0/baseline.sexp` — the `.11` measurement as a tracked record
     (the references.sexp experiment-record precedent: a run's result, recorded once, with
     its re-derive command): host (cpu/kernel/rustc), config (iterations/warmup/reps), the
     16 cells (mix × mode: median ns/step, spread, allocs/step), the static/dyn ratios, the
     RUST-02 agreement, and the explicit no-threshold statement. Plain atoms and strings so
     every tracked reader (`sexp.py`, Lispish, SExprDocumentV1) parses it.
  3. `scripts/check_gate_report.sh` (GATE-REPORT) discovers `G0-REPORT.md` AND
     `G1-REPORT.md` per profile and regenerates each against its gate — the drift check
     covers both; the self-test's RED controls run against both. No new doctrine: the
     existing one already owns "a gate report is a function of its inputs"; G1 is a second
     instance. The registry row's prose is updated to say so.
  Result: met, `2026-09-29`. `scripts/gate_report.py --gate G1` generates
  `profiles/rv64i-lab-v0/G1-REPORT.md` from tracked inputs only, byte-stable in a fresh
  clone (the G0 path's output is byte-unchanged — verified by diff). The report evaluates
  all six roadmap criteria by concrete-name measurement: verdict **`incomplete`**, with
  criterion 6 named (no C-toolchain guest; the assembled guests' 34/34 differential
  recorded as the partial standing; owner `P2-SCALAR.5`). `baseline.sexp` lands as the
  recorded `.11` measurement — parsed and structurally validated by the generator (every
  required field present, `(thresholds none)` enforced), and it parses under all three
  tracked readers. GATE-REPORT discovers `G?-REPORT.md` per profile and covers both
  (self-test 6/0; RED probes: a tampered G1 report named, rc=1; a removed baseline flips
  criterion 5 to unmet; an unknown gate refused, rc=2). The tree's G1 acceptance absorbed
  the roadmap's sixth criterion — the drift this leaf found and repaired. The tree
  completes at 12/12 with the gate honest: the G0 precedent (the milestone's leaves
  complete; the gate's verdict stays `incomplete` with the reason named). Lessons:
  promotion — the general lesson (a tree's gate criteria must be re-read against the
  roadmap when the roadmap is revised; nothing gated it, and the drift was found by the
  leaf that had to score it) is recorded in `DEV_NOTES.md` and parked in this tree's
  Open Questions as a candidate doctrine — a candidate, not a gate, because a
  roadmap-criteria diff needs a designed criterion-id scheme first.

  ROUTING EVIDENCE (the compiled-C-guest gap routed to `P2-SCALAR.5`):
  - The finding reproduces OUTSIDE this tree: the sixth clause stands in `ROADMAP.md` §6's
    G1 text and in `ROADMAP-V3.3`'s record of the v0.3 sharpening, and `P2-SCALAR.5`'s own
    goal independently names "compiled freestanding programs" — three sources outside
    P1-LAB's leaf text.
  - What was measured: the `guests/` census (4 `.s`, 0 `.c` — re-derived by the generator
    on every report), the references dossier (no C-toolchain guest record), and the
    absence of any P1-LAB leaf owning a C guest (the tree's 12 leaves, enumerated).
  - What would make the routing WRONG: if the director intends the C guest to gate P1's
    completion — G1 must read `passed` before P2 opens — then the owner is a new P1-LAB
    leaf, not `P2-SCALAR.5`, and this routing plus the tree's `done` status must be
    revisited. The routing follows the G0 precedent (P0-PROFILE closed with G0
    `incomplete`); the report's verdict keeps the question visible every commit.

- ID: `P1-LAB.13` — **the allocation-count pin** *(reopened leaf)*
  Status: `done`
  Goal: the baseline's allocation claims must be exact, attributed, and gated — a measured
  number nothing re-checks is a running total's cousin (the DERIVED-COUNTS lesson).
  Acceptance: the suite pins the per-mode allocation behaviour with the attribution PROVEN
  (which allocation, from where), any figure in `baseline.sexp` that does not survive the
  proof is corrected and the G1 report regenerated, and the pinning suite fails if the
  behaviour changes.
  Design (recorded before code, `2026-09-29`): the verify test binary already installs the
  counting allocator (`.11`), so the pin is a suite, not a tool: step-count probes
  (the same mix run for N and 2N steps, so per-step behaviour separates from per-run
  setup by DIFFERENCE — a per-step allocation is the slope, setup is the intercept) name
  the exact per-step allocation count per mode; the attribution is proven by code path
  (the operands `Vec::with_capacity` in `extract_operands`, the writes Vec in `run::diff`,
  the big-Vec amortized growth) against the measured counts. If the measured truth
  contradicts the `.11` record, the record and its consumers (`baseline.sexp`, the G1
  report, the book, the tree) are corrected in the same commit.
  Result: met, `2026-09-29`. The diagnosis (slope/intercept probes over counted steps,
  thread-local counters so the test binary's parallelism cannot contaminate an exact
  count) PROVED the `.11` figures and nailed their mechanism: untraced is exactly 1
  allocation per step with zero intercept (the `extract_operands` Vec — 114 steps ⇔ 114
  allocations, 14,368 bytes, pinned); instrumented static and dyn allocate identically
  (pinned per mix); diagnostic adds exactly the crossing log's doubling growth (+4/+5/+6
  at 30/58/114 steps — the Vec's capacity doublings, pinned); and the traced figures are
  low because `run::diff` diffs VALUES — a write that changes nothing allocates nothing,
  and the mixes settle into near-fixed points (the instrumented pattern pinned at the
  measured 50/85/153 allocations for 1/2/4 arithmetic iterations). `baseline.sexp` stands
  uncorrected — every figure survived the proof; the G1 report (regenerated) and the book
  now state the mechanism so the traced columns are not misread as general. Four pin
  suites, each fired RED against a perturbed expectation before landing (the 114↛115 arm
  named the true value on failure). The tree closes again at 13/13. Lessons: promotion —
  PROMOTED to `docs/knowledge/pin-the-mechanism-slope-before-the-number.md` (a measured
  count is only signoff-grade when the mechanism producing it is pinned; separate the
  per-step slope from the per-run intercept before attributing anything).

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | the tree is complete (13/13 leaves done; reopened once for `.13`); gate `G1` RUN — verdict `incomplete`, criterion 6 (the C-toolchain guest) owned by `P2-SCALAR.5` |

## Decisions

- `2026-09-13`: initial representation is **structured encoding/state/profile data plus typed
  Rust semantic functions**; a semantic IR is added only when an exercised target demonstrates
  a benefit (`ROADMAP.md` §1).
- `2026-09-13`: the reference interpreter is **not** an external oracle — it executes the
  canonical handlers, so its agreement with them is structural, not evidential
  (`docs/ARCHITECTURE.md` §2).
- `2026-09-27` (`.3`): state accessors and inspection metadata are **generated from the state
  descriptor** by `scripts/gen_state.py`; drift is the `STATE-GEN` doctrine's refusal, and the
  generator refuses unknown descriptor shapes by name — a generator that guesses is a second
  definition. Reset stays a laboratory declaration supplied by the environment (entry address
  is a parameter, never a constant in the model).
- `2026-09-28` (`.8`): the definitional interpreter evaluates the generated `Sem` trees
  directly; the semantics DATA remains the one executable owner (OWN-01). The width algebra
  is pinned as: `sext`/`zext N` extend FROM the operand's own semantic width TO `N`; a
  literal shift amount widens the result by that amount; computed amounts shift within the
  left operand's width. This is the unique reading under which all 52 trees are correct at
  once (LUI extends from bit 31, LB from 8), and it is validated differentially against the
  references, not assumed from the notation. Reserved decode stays `UndefinedCase` at the
  interpreter boundary — conversion to any trap is the diagnostic policy's explicit act,
  one layer up.
- `2026-09-28` (`.6`): the canonical definition is **lowered, not hand-coded**: encodings,
  semantics trees and the OWN-03 manifest generate into `semulith-core::definition` by
  `scripts/gen_definition.py`; drift is the `DEF-GEN` doctrine's refusal. The generator is the
  executable owner of the *lowering* and re-derives the SEMANTICS doctrine's checks it emits
  through (schema validation, operand binding, the refinement rule, completeness) rather than
  trusting them — a mirror that cannot re-derive its rule is a hope, not a derivation. The
  semantics DATA remains the one executable owner of every rule (OWN-01); `decode` is dispatch
  metadata, and evaluation stays with `.8`.
- `2026-09-28` (`.11`): the diagnostic observer's dispatch is **static by measured default** —
  the instrumented runner is generic over `Observer`, and the dyn instantiation measured
  ×0.974–1.002 of the static one across the four mixes (within the cells' own noise), so
  ARCHITECTURE §6's "choose by measured cost" is answered: no measurable cost either way at
  laboratory scale; static generics remain the default and trait objects are permitted where
  extensibility needs them. Second, a measured RUST-03 departure, stated not hidden: the
  definitional interpreter allocates one Vec per step (`extract_operands`), 1.00
  allocation/step untraced — P1's Non-Goals exclude optimization and the readable
  interpreter keeps its shape; the number is now on record for the milestone that needs it
  (the compiled-handlers decision names its consumer).
- `2026-09-28` (`.9`): the mutation seam is **data, not a second implementation**: `exec` and
  `run` are parameterized over the instruction table, production passes `definition::INSNS`,
  and a mutated model is a copied table with one row swapped — evaluated by the one evaluator
  (OWN-01). Where a wrong behaviour can only exist as harness code (deferred traps, fabricated
  substitutions, stale configurations), the suite mutates the observation stream and says so;
  a mutation that needs a second implementation to inject faithfully is injected at the
  boundary it actually lives on.

## Open Questions

- Candidate doctrine (parked by `.12`, `2026-09-29`): nothing gated a tree's gate criteria
  against the roadmap's gate text, so the sixth G1 clause drifted from `2026-09-27` (when
  `ROADMAP-V3.3` landed it) until `.12` scored the gate on `2026-09-29`. A
  `ROADMAP-TREE-CRITERIA` check needs a designed criterion-id scheme first — candidate,
  not scheduled.
- Exact shapes of the four outcome enums — a P1 design result, not a P0 commitment
  (`docs/ARCHITECTURE.md` §5). Resolved by `.5`.
- ~~Static versus dynamic dispatch for the diagnostic observer~~ — resolved by `.11`
  (measured ×0.974–1.002, within noise; static by default, see Decisions).
- ~~Benchmark host, sample sizes and thresholds~~ — host named and noise characterized by
  `.11`; thresholds remain deliberately UNSET (RUST-04: the noise table is the deliverable,
  and the leaf that needs a threshold sets it from those numbers).
- Scripted-environment replay: `ScriptedEnv`'s pinned conversation is an event stream a bundle
  does not yet record (`replay::Events` carries only the platform's declared-none choice,
  and refuses other claims by name). Joins when a tracked consumer needs it — a fault-injection
  campaign that must replay its scripted faults is the natural first consumer. Does not block
  `.11`.

## Blockers

- `P0-PROFILE` gate `G0`. Building the laboratory before the profile is resolved would bake
  unresolved choices into code.




## Acceptance Checklist (leaf P1-LAB.13)

- [x] **REPRODUCE / ISSUE** — the `.11` allocation figures were a measured report with no
  falsification leg: nothing re-derived them, and the attribution ("the `extract_operands`
  Vec") was argued from code reading, not proven. Worse, the `.11` traced figures
  (1.19–1.42 allocs/step) did not match the naive mechanism (a diff Vec per step would
  give ~2) — an unexplained gap in a committed claim. And a process-global counter cannot
  give an exact count inside a parallel test binary. Measured at the parent commit
  (`4d09375`):

  ```
  $ git grep -c "thread_counts" HEAD -- crates/ | wc -l
  0                       # no exact-under-parallelism counter existed
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — slope/intercept probes (the same mix at 8/16/32
  budgeted steps, then 1/2/4 full iterations, under a new thread-local counter) separated
  per-step cost from per-run setup and named every component: untraced = 1 alloc/step,
  zero intercept (the operands Vec — `crates/semulith-core/src/exec.rs`
  `extract_operands`); instrumented = untraced + a writes Vec ONLY on a visible register
  change (`crates/semulith-verify/src/run.rs` `diff` diffs values — a write that changes
  nothing allocates nothing) + the stream's amortized doubling; diagnostic = instrumented
  + exactly the crossing log's doubling growth. The "gap" was the fixed point: the mixes
  settle into iterations that change almost nothing observable, so `.11`'s 1.19–1.42 was
  RIGHT and the naive model was wrong. The probes, verbatim:

  ```
  $ cargo test -p semulith-verify bench::tests::probe -- --nocapture | grep PROBE
  PROBE arithmetic untraced     budget= 8 steps= 8 allocs= 8 bytes= 1024   # 1.00/step
  PROBE arithmetic untraced     budget=16 steps=16 allocs=16 bytes= 2048   # zero intercept
  PROBE arithmetic instrumented budget= 8 steps= 8 allocs=11 bytes= 1856   # diff allocs
  PROBE arithmetic instrumented budget=16 steps=16 allocs=25 bytes= 4224   # only on change
  P2 arith it=1 untraced     steps= 30 allocs= 30    it=4: 114 / 114
  P2 arith it=1 instrumented steps= 30 allocs= 50    it=2: 85   it=4: 153  # fixed point
  P2 arith it=1 diagnostic   steps= 30 allocs= 54    it=2: 90   it=4: 159  # +4/+5/+6 =
  # the crossing log's capacity doublings at 30/58/114 crossings, exactly
  ```

- [x] **FIX** — `bench::alloc` gains thread-local counters (`thread_reset`/`thread_counts`;
  the process-global pair is unchanged — the single-threaded CLI sees both agree by
  construction); four pin suites in `bench/tests.rs` hold the exact truth; the G1 report
  generator and the book state the traced-mode mechanism so the numbers can't be
  misread as general. `baseline.sexp` stands uncorrected — every figure survived.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify bench 2>&1 | grep "test result"
  test result: ok. 14 passed; 0 failed; ...        # +4 pin suites
  $ cargo test --all 2>&1 | grep "^test result"
  ... 65 passed (core) ... 128 passed (verify) ... # 5 suites ok
  ```

  Pins: untraced 114 steps ⇔ 114 allocations / 14,368 bytes (all four mixes at 8 budgeted
  steps ⇔ 8 allocations); static == dyn exactly, per mix; diagnostic − instrumented =
  +4/+5/+6 at 30/58/114 steps (the crossing log's capacity doublings, exactly);
  instrumented arithmetic pinned at 50/85/153 allocations for 1/2/4 iterations. RED
  probes: 114↛115 and 50↛51 both failed naming the true value; restored green.
  `scripts/gate_report.py --gate G1` regenerated (the mechanism sentence) and GATE-REPORT
  confirms both reports in sync.

- [x] **NO REGRESSION** — `cargo fmt --all -- --check`, `clippy -D warnings`, `cargo test
  --all` (5 suites, 193 tests), wasm build rc=0, `make book`, `make gate` green; the live
  tree stays under the per-part ceiling by archiving `.12`'s checklist, and the ARCHIVE
  itself split into two parts when it crossed the same ceiling (65,617 bytes → part 1:
  checklists `.1`–`.9`; part 2: checklists `.10`–`.12` + design detail `.7`–`.11`) — the
  ceiling obeyed, not raised, at both levels.

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `LIVE_STATUS.md` (P1 13/13),
  `DEV_NOTES.md`, `docs/TASK_TREE.md`, the book's P1 chapter (the mechanism stated), the
  G1 report (regenerated, in sync), the knowledge card
  `docs/knowledge/pin-the-mechanism-slope-before-the-number.md` (+ INDEX row), and this
  tree — one commit. No doctrine-registry change: no new doctrine, no generated artifact
  (the pins are tests; the counters are harness).

## Completed-leaf evidence

Archived to [`archive/P1-LAB.md`](archive/P1-LAB.md) (part 1: checklists `.1`–`.9`) and
[`archive/P1-LAB-2.md`](archive/P1-LAB-2.md) (part 2: checklists `.10`–`.12`, design detail
`.7`–`.11`) — the full, unedited acceptance checklists for every `done` leaf but the last
and the design detail of the completed leaves that carried one (the live leaf entries keep
a pointer line), split out on `2026-09-28` and extended on `2026-09-29` when the live file
crossed its per-part ceiling, then split in two the same day when the archive itself
crossed it (65,617 bytes); the ceiling was obeyed, not raised, per the `SOT-FORMAT`
precedent. The live tree keeps the frontier, the decisions, the open questions, the
blockers, every leaf's goal/acceptance/result, the final leaf's checklist, and both logs.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-29` | `P1-LAB.13` | slope/intercept probes (thread-local counters), then 4 pin suites | untraced 114 steps ⇔ 114 allocs / 14,368 B exactly; static == dyn per mix; diagnostic − instrumented = crossing-log doublings (+4/+5/+6 at 30/58/114); instrumented pinned at 50/85/153 for 1/2/4 iterations — the fixed-point mechanism proven |
| `2026-09-29` | `P1-LAB.13` | pins fired RED (114↛115; 50↛51) | both named the true value on failure; restored green |
| `2026-09-29` | `P1-LAB.13` | `make check`, wasm build, `make gate` | 5 suites ok (65 core + 128 verify) / rc=0 / 23 doctrines green; G1 report regenerated and in sync |
| `2026-09-29` | `P1-LAB.12` | `scripts/gate_report.py rv64i-lab-v0 --gate G1` | G1-REPORT.md written (5,482 B), verdict `incomplete` — criterion 6 named, owner `P2-SCALAR.5`; G0 output byte-identical before/after |
| `2026-09-29` | `P1-LAB.12` | `check_gate_report.sh` + `--self-test` + RED probes | 2 reports in sync; 6 pass / 0 fail; tampered G1 report named rc=1; baseline removed → criterion 5 unmet; `--gate G9` refused rc=2 |
| `2026-09-29` | `P1-LAB.12` | `compare_readers.py baseline.sexp` | all three readers agree (513 nodes identical) |
| `2026-09-29` | `P1-LAB.12` | `make gate`, `cargo test --all`, wasm build, `make book` | 23 doctrines green / 189 tests ok / rc=0 / book builds |
| `2026-09-28` | `P1-LAB.11` | `cargo test -p semulith-verify` | 124 passed / 0 failed (+10 bench — decode round-trip, per-mix census, delivery-continues, four-mode agreement, budget stop, image refusal, allocator counting, pinned stats) |
| `2026-09-28` | `P1-LAB.11` | `./target/release/semulith bench` (Apple M4 Pro, Darwin 27.0.0, rustc 1.95.0) | rc=0; untraced 47.2–54.1 ns/step across the four mixes; instrumented +24–40%; diagnostic +4–8% further; 1.00 alloc/step untraced; noise spread 1.7–7.4% (one 113% scheduler outlier); static/dyn ×0.974–1.002; RUST-02 agreement OK on every mix |
| `2026-09-28` | `P1-LAB.11` | `make check`, wasm build, `make gate` | 5 suites ok (65 core + 124 verify) / rc=0 / 23 doctrines green |
| `2026-09-28` | `P1-LAB.10` | `cargo test -p semulith-verify` | 114 passed / 0 failed (+15 replay — round-trips, tamper/omission arms; +6 reduce — the three prefix minimizations with 1-minimality witnesses, the NoDivergence boundary) |
| `2026-09-28` | `P1-LAB.10` | `make check`, wasm build | 5 suites ok (65 core + 114 verify) / rc=0 |
| `2026-09-28` | `P1-LAB.10` | CLI end-to-end: `bundle` → `replay` → `reduce`, plus a hand-corrupted bundle | replay identical rc=0; jalr-odd-bit 12 → 9 words, retained step 10; phantom-load refused by name rc=1; tampered image refused naming the digest rc=1 |
| `2026-09-28` | `P1-LAB.10` | `make gate` | 23 doctrines green |
| `2026-09-28` | `P1-LAB.9` | `cargo test -p semulith-verify` | 88 passed / 0 failed (mutate 11 — nine designated arms + the census pin + the suppression exhibit; run 16 incl. the four guest suites; graph/schema/fixtures/json/pattern/sha256/elf unchanged) |
| `2026-09-28` | `P1-LAB.9` | `cargo test -p semulith-core exec` | 25 passed / 0 failed (+ the generated-table scan pinned to `definition::decode`) |
| `2026-09-28` | `P1-LAB.9` | `make check`, wasm build, `make gate` | 5 suites ok / rc=0 / 23 doctrines green |
| `2026-09-28` | `P1-LAB.8` | `scripts/run_semulith_smoke.py` (live, sail-riscv 0.14 + spike 1.1.1-dev) | semulith agrees with sail-riscv on 34/34 aligned steps across the 4 guests; spike agrees on all enabled comparisons; 34/34 spec-derived expectations; both never-written registers held; every run reproduces byte-identically |
| `2026-09-28` | `P1-LAB.8` | GUEST-GEN fired RED pre-registration (hand-edited fixture) | rc=1 naming DRIFT + regeneration command; restored rc=0 |
| `2026-09-28` | `P1-LAB.8` | `bash scripts/check_guest_gen.sh --self-test` | 7 pass / 0 fail |
| `2026-09-28` | `P1-LAB.8` | `cargo test -p semulith-verify` | 77 passed / 0 failed (run 13, elf 2, guests 4, fixtures 12, graph 16+16, json 8, pattern 7, sha256 2, schema 12, lib 2) |
| `2026-09-28` | `P1-LAB.8` | `cargo test -p semulith-core exec` | 24 passed / 0 failed (outcome families, width algebra, reporting points, code visibility) |
| `2026-09-28` | `P1-LAB.8` | `make check`, wasm build, `make gate` | 5 suites ok / rc=0 / 23 doctrines green |
| `2026-09-28` | `P1-LAB.7` | `cargo test -p semulith-verify` | 59 passed / 0 failed (json 8, pattern 7, sha256 2, schema 12, graph 16, fixtures 12, lib 2) |
| `2026-09-28` | `P1-LAB.7` | `cargo run -p semulith-cli -- check-examples` | intact bundle: 0 findings, gate `incomplete`, rc=0 |
| `2026-09-28` | `P1-LAB.7` | RECORD-SCHEMA RED probe (mutated requirement, `EV-GHOST`) | rc=1 naming ORPHAN-EVIDENCE; restored rc=0 |
| `2026-09-28` | `P1-LAB.7` | `bash scripts/check_requirements.sh` | ok — Python + Rust engines green on 7 record files |
| `2026-09-28` | `P1-LAB.7` | `make check`, wasm build, `make gate` | 5 suites ok / rc=0 / 22 doctrines green |
| `2026-09-28` | `P1-LAB.6` | `cargo test -p semulith-core definition` | 10 passed / 0 failed (manifest, completeness, disjointness, binding, FENCE ratchet, scatter) |
| `2026-09-28` | `P1-LAB.6` | `bash scripts/check_definition_gen.sh --self-test` | 8 pass / 0 fail |
| `2026-09-28` | `P1-LAB.6` | DEF-GEN fired RED pre-registration (hand-edited module) | rc=1, naming DRIFT + regeneration command |
| `2026-09-28` | `P1-LAB.6` | `make check`, wasm build, `make gate` | 5 suites ok / rc=0 / 22 doctrines green |
| `2026-09-27` | `P1-LAB.5` | `cargo test -p semulith-core outcome` | 5 passed / 0 failed (delivery-continues, unimplemented≠trap, distinctness, re-home, reserved) |
| `2026-09-27` | `P1-LAB.5` | `make check`, wasm build, `make gate` | 5 suites ok / rc=0 / all doctrines green |
| `2026-09-27` | `P1-LAB.4` | `cargo test -p semulith-verify` | 12 passed / 0 failed (fixtures, no instruction handler) |
| `2026-09-27` | `P1-LAB.3` | `bash scripts/check_state_gen.sh --self-test` | 6 pass / 0 fail |
| `2026-09-27` | `P1-LAB.3` | STATE-GEN fired RED pre-registration (hand-edited module) | rc=1, named DRIFT + regeneration command |
| `2026-09-27` | `P1-LAB.3` | `clippy -D warnings`, `make gate`, wasm build | clean / all doctrines green / rc=0 |
| `2026-09-27` | `P1-LAB.2` | `cargo test -p semulith-core` | 12 passed / 0 failed (incl. 8-bit exhaustive suites) |
| `2026-09-27` | `P1-LAB.2` | first exhaustive run | FAILED 2 (slt/sar width-sensitivity) → test design fixed, re-run green |
| `2026-09-27` | `P1-LAB.2` | `clippy -D warnings`, `make gate` | clean / all doctrines green |
| `2026-09-27` | `P1-LAB.1` | `cargo fmt --check` + `clippy -D warnings` + `cargo test --all` | 5 suites ok, 0 warnings |
| `2026-09-27` | `P1-LAB.1` | `cargo build --workspace --target wasm32-unknown-unknown` | rc=0 (with `PORT-WEB.1`) |
| `2026-09-27` | `P1-LAB.1` | `make gate` | `=== all doctrines green ===` |


## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `P1-LAB.13` | `SEMILITH-PL-0013 (leaf P1-LAB.13): …` | the allocation-count pin: thread-local counters; four exact pins (untracked slope/intercept, static==dyn, diagnostic growth, the fixed-point mechanism); `baseline.sexp` stands uncorrected — every figure survived the proof |
| `P1-LAB.12` | `SEMILITH-PL-0012 (leaf P1-LAB.12): …` | the G1 gate report, generated from pinned inputs: `gate_report.py --gate G1`, `baseline.sexp`, GATE-REPORT covering `G?-REPORT.md`; verdict `incomplete` — criterion 6 (the C guest) named and routed to `P2-SCALAR.5`; the tree's criteria re-aligned with the roadmap |
| `P1-LAB.11` | `SEMILITH-PL-0011 (leaf P1-LAB.11): …` | the performance baseline: `semulith-verify::bench` (four mixes, three modes, census, counting allocator, noise stats) and `semulith bench`; static/dyn dispatch resolved by measurement; the `.10` checklist archives per the per-part ceiling |
| `P1-LAB.10` | `SEMILITH-PL-0010 (leaf P1-LAB.10): …` | replay and reduction in `semulith-verify::{replay, reduce}`; `semulith bundle`/`replay`/`reduce`; the `.9` checklist archives per the per-part ceiling |
| `P1-LAB.9` | `SEMILITH-PL-0009 (leaf P1-LAB.9): …` | the validator mutation suite in `semulith-verify::mutate` (11 arms); the `step_over`/`run_over` table seam with the generated-decode equivalence pin; `.1`–`.8` checklists archived per the per-part ceiling |
| `P1-LAB.7` | `SEMILITH-PL-0007 (leaf P1-LAB.7): …` | the graph and report checker in `semulith-verify`; PACKAGE_CHECKS rows re-derived in Rust; RECORD-SCHEMA two-engine, fired RED on a mutated record first |
| `P1-LAB.6` | `SEMILITH-PL-0006 (leaf P1-LAB.6): …` | the canonical definition, generated: decode tables, lowered semantics trees, OWN-03's manifest; DEF-GEN registered and fired RED first |
| `P1-LAB.5` | `SEMILITH-PL-0005 (leaf P1-LAB.5): …` | the four SEM-01 outcome families as types; delivery-continues and unimplemented≠trap proven |
| `P1-LAB.4` | `SEMILITH-PL-0004 (leaf P1-LAB.4): …` | the environment boundary and its fixtures, testable without the instruction handler |
| `P1-LAB.3` | `SEMILITH-PL-0003 (leaf P1-LAB.3): …` | architectural state, generated from the descriptor; STATE-GEN registered and fired RED first |
| `P1-LAB.2` | `SEMILITH-PL-0002 (leaf P1-LAB.2): …` | arithmetic primitives, verified exhaustively at reduced width |
| `P1-LAB.1` | `SEMILITH-PL-0001 (leaf P1-LAB.1, PORT-WEB.1): …` | the crate skeleton and the Wasm gate land in one commit, as PORT-WEB.1's acceptance requires |


## Changelog

- `2026-09-29`: Leaf `.13` done (the tree reopened once) — the allocation-count pin: the
  `.11` figures are now PROVEN, not reported. Thread-local counters make exact counts
  possible inside a parallel test binary; slope/intercept probes nailed the mechanism —
  untraced is exactly 1 alloc/step with zero intercept (the operands Vec), instrumented
  adds a writes Vec only on a VISIBLE register change (the mixes settle into near-fixed
  points — that, not an error, is why `.11`'s traced columns sat near 1.2), diagnostic
  adds exactly the crossing log's doubling growth, static and dyn pay identically. Four
  exact pins, each fired RED before landing. `baseline.sexp` stands uncorrected; the G1
  report and the book state the mechanism. The archive split in two when it crossed the
  per-part ceiling (obeyed, not raised). The tree closes again, 13/13.
- `2026-09-29`: Leaf `.12` done — the `G1` gate report, and the tree completes (12/12):
  `scripts/gate_report.py --gate G1` generates `profiles/rv64i-lab-v0/G1-REPORT.md` from
  tracked inputs only (byte-stable in a fresh clone; the G0 path byte-unchanged), measuring
  each of the SIX roadmap criteria by concrete name — the tree's acceptance absorbed the
  sixth (the compiled freestanding guest; the drift repaired in-tree). Verdict
  `incomplete`: criteria 1–5 met, criterion 6 unmet as written (4 `.s` guests, 0 `.c`;
  the assembled guests' 34/34 differential recorded as partial standing; owner
  `P2-SCALAR.5`, routing evidence in the leaf). `baseline.sexp` freezes the `.11`
  measurement as validated data (`(thresholds none)` enforced); GATE-REPORT discovers
  `G?-REPORT.md` per profile and covers both (self-test 6/0; tamper and removal probes
  fired RED). The gate stays honest — the G0 precedent. Same commit: the `docs/changelog/`
  family's file-count ceiling is re-derived 40 → 80 (the family grows one file per shard
  EVENT by design; the content axes — per-part 64 KiB, 384 KiB aggregate — unchanged;
  derivation recorded in `doctrine/readme_routes.tsv`).
- `2026-09-28`: Leaf `.11` done — the performance baseline (RUST-04, gate `G1`'s fifth
  criterion): `semulith-verify::bench` generates the four workload mixes (arithmetic,
  control, memory, fault — every word decode-round-trip-pinned to the generated
  definition), drives them in ARCHITECTURE §6's three modes (untraced / instrumented,
  static and dyn / diagnostic) under one counting environment, and checks RUST-02 as data
  (all modes agree on steps, stop, final state, census, and every recorded stream, or the
  run is refused). The std-only counting allocator makes RUST-03 a number: 1.00
  allocation/step untraced, 1.19–1.42 traced. `semulith bench` names the host (Apple M4
  Pro; Darwin 27.0.0; rustc 1.95.0) and prints the noise table — untraced 47–54 ns/step,
  spread 1.7–7.4% per cell — with NO regression threshold set: the noise is characterized
  first, and the table is what a future threshold cites. The static-vs-dynamic observer
  question resolves by measurement (×0.974–1.002, within noise; static stays the default).
  The `.10` checklist archives to `archive/P1-LAB.md` (per-part ceiling obeyed). The
  frontier moves to `.12` (the G1 gate report).
- `2026-09-28`: Leaf `.10` done — replay and reduction (T008's second half; G-REPLAY,
  EVD-02): `semulith-verify::replay` records the input bundle — algorithm pins flattened
  from `definition::MANIFEST` (plus the harness version and the `production`/`mutant:<name>`
  model), the platform region, the entry, the image words with a sha256 guard, the recorded
  event choice (`DeclaredNone`, OB-ENV-EVENT-DELIVERY named), the step budget, and the
  recorded steps + stop render — and `replay()` re-derives it, checking identity by name
  and naming the first differing observation on drift. `semulith-verify::reduce` is the
  ddmin minimizer whose retention is the original first divergence exactly (same step,
  same field); every accepted removal preserves it structurally, each result carries an
  exhaustive 1-minimality witness, and census-class wrong behaviour (phantom-load) is
  refused `NoDivergence` by name. `semulith-cli` gains `bundle`/`replay`/`reduce`. The
  `.9` checklist archives to `archive/P1-LAB.md` (per-part ceiling obeyed). The frontier
  moves to `.11` (performance baseline).
- `2026-09-28`: Leaf `.9` done — the validator mutation suite (T007, EVD-09): `semulith-core::exec::step_over` and `semulith-verify::run::run_over` parameterize the single execution path over the instruction table (production delegates with `definition::INSNS`; the scan is pinned to the generated `decode`), and `semulith-verify::mutate` runs eleven arms — the eight designated wrong-behaviour classes, the JALR odd-bit arm the fixture note names (fault at 0x80000029, predicted), the four-guest data-crossing census pin, and the comparison-suppression exhibit. Every guest arm re-derives the pinned expectations against the real model before judging the mutant; divergences are asserted at their designated steps, fields named. Completed-leaf checklists `.1`–`.8` archive to `archive/P1-LAB.md` (per-part ceiling obeyed); the family aggregate is re-derived to 1 MiB per `decision_task-tree-family-bound-rederivation.md` (lanes grew 25 → 32; per-part stays 64 KiB). The frontier moves to `.10` (replay and reduction).
- `2026-09-28`: Leaf `.8` done — the first execution slice: `semulith-core::exec`, the
  definitional interpreter, evaluates the generated `Sem` trees (the semantics data stays
  the one executable owner, OWN-01); `semulith-verify` gains the observation runner and
  first-divergence comparator (`run`), the ELF64 loader (`elf`), and the generated guest
  fixture (`guests.rs`, GUEST-GEN — the 23rd doctrine, fired RED on a hand-edited fixture
  before registration); `semulith-cli` gains `semulith run`. The offline differential runs
  all four tracked guests against their specification-derived expectations on every commit;
  the live experiment (`scripts/run_semulith_smoke.py`) agrees with sail-riscv and spike on
  every enabled comparison — 34 aligned steps, byte-identical reproduction. The width
  algebra (`sext`/`zext` extend from the operand's own width; literal shifts widen) is the
  one reading under which all 52 effect trees are simultaneously correct, and it is now
  differentially validated evidence, not an assumption. The frontier moves to `.9`
  (validator mutation suite).
- `2026-09-28`: Leaf `.7` done — `semulith-verify` gains the graph and report checker
  (T004): `json`/`pattern`/`sha256`/`schema`/`graph`, five dependency-free modules
  re-deriving the PACKAGE_CHECKS schema results in Rust (RUST-01 — 5/5 records, 6/6 negative
  controls, the synthetic source fingerprint) and enforcing the `EVIDENCE_AND_GATES.md` §3
  invariants over the frozen `examples/` bundle (identifier references, profile scope, graph
  integrity, artifact hashes, freshness, gate policy — one mutation suite per designated
  rejection, positive control gating `passed`). `semulith check-examples` presents the
  report; `RECORD-SCHEMA` runs the Rust engine on every commit and fired RED on a mutated
  record before landing. The frontier moves to `.8` (first execution slice).
- `2026-09-28`: Leaf `.6` done — `semulith-core::definition`: the canonical definition
  GENERATED (`scripts/gen_definition.py`): 12 fields, 52 decode rows, the semantics effect
  trees lowered from the execution authority, `decode`, and OWN-03's manifest as data
  (definition, generator, configuration and source fingerprints); the 22nd doctrine `DEF-GEN`
  refuses drift and fired RED on a hand-edited module before registration; the owner→mirror
  pairs (encodings, semantics, state) are registered in `doctrine/fact_ownership.tsv`; the
  frontier moves to `.7` (graph and report checker).
- `2026-09-27`: Leaf `.5` done — `semulith-core::outcome`: `TargetEvent`/`Advance`/`ModelError`/
  `UndefinedCase` as distinct types with `StepOutcome` the step-level sum; a delivered trap
  proven non-stopping and an unimplemented instruction proven not-an-illegal-instruction-
  trap; `env`'s `ContractViolation` re-homed into `ModelError`; the frontier moves to `.6`
  (canonical definition skeleton). Leaf `.4` done — `semulith-core::env` (the
  request/response contract) and `semulith-verify::fixtures` (`FlatMemory`, `ScriptedEnv`),
  the negative-fixture rule exercised for real; the frontier moves to `.5`. Leaf `.3` done —
  `semulith-core::state` generated from `state.sexp`; the 21st doctrine `STATE-GEN` refuses
  drift; the frontier moves to `.4`. Leaf `.2` done — `semulith-core::arith`, verified by
  boundary + 8-bit-exhaustive suites; the frontier moves to `.3`. Leaf `.1` done — the three
  crates + the Wasm gate.
