# P1-LAB: build the processor laboratory and the machinery that can tell the truth about it

## Metadata

- Tree ID: `P1-LAB`
- Status: `active` (first leaf landed `2026-09-27`; was `proposed`)
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
  Design (recorded before code, `2026-09-28`): the checker lands in `semulith-verify`
  (`docs/ARCHITECTURE.md` §4 assigns "source/evidence graph, adapters, comparators, reducer"
  there; the crate "does not supply production instruction semantics" — checking evidence is
  not a semantic rule). Four support modules plus the checker: `json` (a JSON reader — the
  verify crates carry no dependencies, so the reader is ours, with `scripts/validate_records.py`
  as the reference contract), `pattern` (a regex subset — exactly the constructs the three
  tracked schemas' patterns use, refusing anything else by name), `sha256` (FIPS 180-4,
  std-only — re-deriving the synthetic source fingerprint), and `schema` (the same keyword
  subset as the Python validator, unknown keywords REFUSED; `additionalProperties` as a schema,
  which the Python tool silently skips, is enforced — a tightening, verdicts unchanged on the
  frozen corpus, proven by running both). `graph` is the checker itself: pure functions over
  parsed records (no `std::fs` in the library — the workspace builds for `wasm32-unknown-unknown`
  and evidence bytes arrive as `&[u8]` through an injected resolver). `semulith-cli` owns the
  command surface (`check-examples`, report presentation per §4) and `RECORD-SCHEMA`'s JSONL
  arm runs both engines, Python and Rust, so the PACKAGE_CHECKS rows are re-derived by the
  gate itself, not cited.
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
  Design (recorded before code, `2026-09-28`): three pieces, each on its owning side of the
  `docs/ARCHITECTURE.md` §4 map.
  1. `semulith-core::exec` — the definitional interpreter: `step(&mut ArchitecturalState, &mut
     impl Environment) -> StepOutcome`. Fetches through the environment contract, decodes with
     `.6`'s `decode`, extracts operands (scatter-aware, with the binding rule `.6` documents:
     `imm12hi`/`imm12lo` → `imm12`, `bimm12hi`/`bimm12lo` → `bimm12`, either shift field →
     `shamt`), and evaluates the instruction's `Sem` tree — the semantics DATA stays the one
     executable owner (OWN-01); the interpreter is its evaluator, not a second implementation.
     Expression evaluation carries an explicit **width** (the semantics file's own rule:
     "WIDTHS ARE ALWAYS EXPLICIT"): `sext`/`zext N` extend FROM the operand's own width TO `N`
     (which is what makes `sext 64 (shl (imm imm20) (lit 12))` the LUI sign-extension from bit
     31, and `sext 64 (load …)` the LB extension from 8 — the two readings that make every one
     of the 52 trees correct at once); shifts of a literal widen by the literal amount. Outcome
     mapping: misaligned branch/jump target → `InstructionAddressMisaligned` reported AT the
     target value, raised on the branch (REQ-D-IALIGN, REQ-D-MISALIGN-REPORT); fetch
     access-fault → `InstructionAccessFault` at the pc (REQ-D-FETCH-FAULT-REPORT); a misaligned
     or faulting load/store raises its exception before/at the boundary without substituting
     (D-MISALIGN-DATA, D-MAIN-VS-IO); reserved decode → `UndefinedCase::ReservedDecode`
     (D-RESERVED-DECODE — reported as the unspecified case it is, never auto-converted);
     ECALL/EBREAK → `RequestedTrap` with the cause vocabulary's codes 11/3 (REQ-D-ECALL-EBREAK).
  2. `semulith-verify` — the observation runner and the first-divergence comparator, on the
     four tracked guests (`smoke-arith`, `guest-control`, `smoke-trap`, `guest-no-device`).
     A step is `(pc, word, register writes, trap)` — the same normalized observation vocabulary
     `scripts/compare_traces.py` already reduces the references to — and `first_divergence`
     walks two streams and names the first differing observation (pc / insn / a register write /
     the trap cause or tval), or reports a length mismatch as a non-agreement, never a prefix
     pass. The guests and their specification-derived expectations become a GENERATED Rust
     fixture (`scripts/gen_guests.py` → `semulith-verify/src/guests.rs`, the 23rd doctrine
     `GUEST-GEN` refuses drift), so the commit gate re-runs the whole slice offline: every
     expectation value the guests carry was derived from the pinned specification prose
     (EVD-05), not from any model's output.
  3. `semulith-cli` — `semulith run <elf>`, a minimal ELF64 loader + the runner + a normalized
     trace print, so the live three-way experiment (`scripts/run_semulith_smoke.py` — semulith
     vs sail-riscv vs the pinned expectations, NOT a commit gate, same standing as
     `run_smoke.py`) compares all models through the one vocabulary.
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
  Design (recorded before code, `2026-09-28`): eight designated classes plus the ninth arm the
  `guest-control.expected.sexp` note names — JALR keeping its odd bit, the one observation the
  two references can never discriminate (both clear the bit). Two injection levels, chosen by
  fidelity, each arm naming its injection, its detection instrument, and its designated
  divergence (step + field):
  1. **Model-level, through one new seam.** `semulith-core::exec` gains
     `step_over(state, env, insns: &[InsnDef])`; production `step` delegates with
     `definition::INSNS`, and the table scan applies exactly the predicate the generated
     `definition::decode` documents (`word & mask == value` — the generated body IS that scan),
     so the production path is unchanged and OWN-01 holds structurally: a mutation is *data the
     one evaluator consumes*, never a second implementation. `semulith-verify::run` gains the
     mirroring `run_over`. The suite (`semulith-verify::mutate`) builds a mutated table by
     copying `INSNS` and swapping one row — either the decode row (`mask`/`value`) or the
     effect pointer (a mutated tree rebuilt from the real tree by a small transformer, leaked
     test-locally, bounded). Arms at this level: **wrong sign extension** (addi's
     `(sext 64 …)` → `(zext 64 …)`; guest-control diverges on x1 at step 1); **suppressed
     register write** (jal's link `set` dropped; guest-control diverges on the missing x5 write
     at step 7); **the JALR odd-bit arm** (the `(and … (lit -2))` LSB-clear dropped from
     `set-pc`; guest-control diverges on the `InstructionAddressMisaligned` trap at step 10,
     tval `0x80000029` — the fault the fixture note predicted); **wrong trap cause** (ebreak's
     `(lit 3)` → `(lit 11)`; a suite-local `[ebreak]` program diverges on the cause at step 0);
     **extra memory access** (addi prepended with a discarded phantom byte load at a mapped
     address; the architectural trace is UNCHANGED — `compare` still agrees — and the pinned
     per-guest data-crossing census detects the extra `Load`; the suite pins that census for
     all four guests, justified from their `.s` sources); **overbroad mask** (srai's
     `mask`/`value` cleared at bit 30, the SRLI/SRAI discriminator; the suite proves the
     hidden-bit witness — srli's canonical word now matches the mutated srai row — and a
     suite-local `[addi, slli, srli]` program diverges on x1 when srli executes as srai).
  2. **Observation/outcome-level, where a faithful model-level seam would be a second
     implementation.** Documented per arm: **illegal-opcode substitution for a model
     limitation** (SEM-02: a limitation is carried as the undefined case — the arm removes
     fence's decode row and verifies the honest outcome is `UndefinedCase::ReservedDecode`,
     never a trap — then substitutes the fabricated `IllegalInstruction` observation, cause 2
     with tval = the word, and asserts the differential against the full-model reference
     diverges at step 0 naming the trap); **shifted event delivery** (the deferred-trap
     observation stream — smoke-trap's step-2 trap moved to a fabricated step 3 — diverges at
     the due step naming the missing trap); **stale reference configuration** (a reference run
     at a stale entry diverges at step 0 naming the pc) and **unjustified comparison
     suppression** (a writes-blind comparator variant is shown to AGREE with the sign-extension
     mutant that the real comparator catches — the writes leg is load-bearing, EVD-09's second
     half).
  Detection instruments are all real and already gated: `compare`/`render` verdicts (field and
  step named), the run's boundary-crossing census, and the pinned GUEST-GEN expectations as the
  GREEN anchor for every guest arm (the real model meets them in each arm before the mutant is
  judged). No new doctrine: the suite is Rust tests under `make check`, the same standing as
  the run suites — it guards discriminating power, not drift, so there is no generated artifact
  to refuse. Files owned: `crates/semulith-core/src/exec.rs` (+ its tests),
  `crates/semulith-verify/src/run.rs`, `crates/semulith-verify/src/mutate.rs` (+ tests),
  `crates/semulith-verify/src/lib.rs`.
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
  Design (recorded before code, `2026-09-28`): two pieces, both on the verify side per
  `docs/ARCHITECTURE.md` §4 ("adapters, comparators, reducer" — replay is evidence machinery
  beside them; no core change, the `.9` table seam is reused as-is).
  1. `semulith-verify::replay` — the recorded input bundle (G-REPLAY's "recorded definitions,
     tools, inputs, and event choices"; ARCHITECTURE §7's "a seed without the generator version
     and event stream is insufficient"):
     - `Bundle { algorithm, platform, entry, image, events, budget, recorded }`, JSON both
       ways (hand-rolled writer like `report::to_json`; parsed through the crate's own `json`
       reader with named-field errors — a document missing any accompaniment fails parse
       naming the field, so the bare-seed refusal is structural, not policy).
     - `algorithm` — the identity, flattened from `semulith-core::definition::MANIFEST` at
       record time (profile, ilen, generator name+sha256, every input pin) plus the harness
       version and the `model` under test (`"production"` or `"mutant:<name>"` resolved
       through `mutate::table_for`). At replay every pin is re-compared against the live
       MANIFEST and a mismatch is refused by name; an unknown mutation name likewise.
     - `platform` — the FlatMemory region declaration `{base, size}` (the environment
       policy); `entry` — the laboratory reset's pc (x1..x31 = 0 is the profile's declared
       reset, REQ-D-ENTRY-STATE, so it rides as documentation, not data).
     - `image` — the guest words plus the sha256 of the little-endian image bytes, recomputed
       and compared at replay (a tampered word is refused by name).
     - `events` — the actual relevant event choices, recorded as data:
       `DeclaredNone { obligation: "OB-ENV-EVENT-DELIVERY" }` is this platform's choice (no
       asynchronous event exists). Any other claim is refused by name as not-this-platform;
       scripted-env replay joins when a tracked consumer needs it (Open Question below).
     - `budget` — the step bound; `recorded` — the result: the observation steps plus the
       stop's canonical render, compared rendered (deterministic Debug; Failed/Undefined
       stops carry data no round-trip could rebuild typed, and rendering loses nothing).
     - `replay()` rebuilds the environment from the bundle, re-runs the recorded model over
       it, and reports `Replays` or `Mismatch` — the recorded-vs-replay first divergence via
       `run::compare`, step and field named.
  2. `semulith-verify::reduce` — the minimizer (EVD-02's minimized discrepancy; P2's "retain
     minimized discrepancies"):
     - `Case { model, reference, entry, region_size, budget }` — the differential's two
       tables (in the suite/CLI: a `.9` mutant against production `INSNS`), the laboratory
       platform facts, the step bound.
     - `reduce(case, words)`: the property is the first divergence of model-vs-reference on
       the candidate — `compare(reference_steps, model_steps, ("reference", "model"))` —
       and retention is the ORIGINAL divergence exactly: same `at`, same `what`. Identical
       prefix semantics make a same-step retained divergence byte-identical (values, pc,
       tval included); a removal that shifts the step or changes the field is correctly
       rejected. Classic ddmin over word indices (ILEN 32 ⇒ one word = one observation
       step); every accepted removal preserves the property, so the result ALWAYS retains —
       the invariant is structural, and `Reduction { words, retained, evaluations }` carries
       the witness count.
     - Named boundary: a case whose observations do not diverge — the phantom-load census
       arm is the standing example, a wrong behaviour the observation vocabulary cannot
       see — is refused `NoDivergence`: observation reduction cannot retain what
       observations do not carry (the `.9` census lesson, reused).
  3. `semulith-cli` — the laboratory surface: `semulith bundle --guest=X --mutate=Y` writes
     the bundle JSON; `semulith replay <file>` re-derives and judges it; `semulith reduce
     --guest=X --mutate=Y` prints the minimized program with its retained divergence. Exit
     codes keep the `.9` convention: a caught divergence is the tool working, not an error.
  Suite (Rust tests, `make check` — same standing as `.9`; no new doctrine, no generated
  artifact): replay round-trips every tracked guest under the production model and the
  zext-addi mutant; tamper arms (image word, entry, region, budget, manifest pin, event
  claim, missing accompaniment) are each refused by name; reduction minimizes
  zext-addi/guest-control to the 2-word divergent prefix (step 1, the x1 write),
  jal-no-link to the 4-word prefix (step 7, the x5 link write), jalr-odd-bit to the 9-word
  prefix (step 10, `InstructionAddressMisaligned` tval `0x80000029` — the fixture note's
  prediction, retained through minimization); every minimized result carries an exhaustive
  1-minimality witness (no single-word deletion retains), and phantom-load is refused
  `NoDivergence` by name.
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
  Status: `pending`
  Goal: measure arithmetic, control-flow, memory and fault-heavy mixes separately on a **named** host, with allocation counts and trace settings, in untraced / instrumented / diagnostic modes.
  Acceptance: repeated measurement characterizes the noise **before** any regression threshold is set (`RUST-04`); no invented MIPS target; traced and untraced executions agree on observations (`RUST-02`).

- ID: `P1-LAB.12` — **the `G1` gate report**
  Status: `pending`
  Goal: generate the gate report from pinned inputs.
  Acceptance: reproducible from recorded definitions, tools, inputs and event choices; reads `passed` or `incomplete`.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `P1-LAB.11` | `pending` | performance baseline — T-pending; measure the noise before any threshold (`RUST-04`) |

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
- `2026-09-28` (`.9`): the mutation seam is **data, not a second implementation**: `exec` and
  `run` are parameterized over the instruction table, production passes `definition::INSNS`,
  and a mutated model is a copied table with one row swapped — evaluated by the one evaluator
  (OWN-01). Where a wrong behaviour can only exist as harness code (deferred traps, fabricated
  substitutions, stale configurations), the suite mutates the observation stream and says so;
  a mutation that needs a second implementation to inject faithfully is injected at the
  boundary it actually lives on.

## Open Questions

- Exact shapes of the four outcome enums — a P1 design result, not a P0 commitment
  (`docs/ARCHITECTURE.md` §5). Does not block `.1`.
- Static versus dynamic dispatch for the diagnostic observer: chosen on **measured** cost, not
  assumed to be free (`docs/ARCHITECTURE.md` §6). Resolved by `.11`.
- Benchmark host, sample sizes and thresholds: no threshold before the noise is characterized.
- Scripted-environment replay: `ScriptedEnv`'s pinned conversation is an event stream a bundle
  does not yet record (`replay::Events` carries only the platform's declared-none choice,
  and refuses other claims by name). Joins when a tracked consumer needs it — a fault-injection
  campaign that must replay its scripted faults is the natural first consumer. Does not block
  `.11`.

## Blockers

- `P0-PROFILE` gate `G0`. Building the laboratory before the profile is resolved would bake
  unresolved choices into code.


## Acceptance Checklist (leaf P1-LAB.10)

- [x] **REPRODUCE / ISSUE** — G-REPLAY's demand as it stood after `.9`: a divergence the
  differential caught existed only as a test's in-memory value — nothing recorded the inputs
  that produced it, so "failures are replayable from recorded inputs" (gate `G1`'s first
  criterion) and T007's "replay/reduction preserves mismatch" had no artifact and no
  minimizer at all:

  ```
  $ git ls-files 'crates/*' | xargs grep -ln "Bundle\|ddmin\|first-divergence retention" | wc -l
  0                    # no recorded input bundle; no reducer; the vocabulary existed in run.rs only
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `.8`/`.9` built the observation vocabulary, the
  comparator, and the mutation seam, but a result was never *recorded*: there was no type
  carrying what ARCHITECTURE §7 says identity is — code/generator versions, initial state,
  guest image, environment policy, event choices — so no run could be re-derived from
  recorded inputs, and EVD-02's minimized discrepancy had no minimizer to produce it. WHERE,
  measured at the parent commit:

  ```
  $ git grep -n "pub fn replay\|pub fn reduce" HEAD -- crates/ | wc -l
  0                                            # the recorder and the minimizer existed nowhere
  $ git ls-files 'crates/*' | xargs grep -ln "struct Bundle" | wc -l
  0                                            # nothing recorded a run's inputs
  ```

- [x] **FIX** — `semulith-verify::replay`: the `Bundle` (algorithm pins flattened from
  `definition::MANIFEST` + harness version + `production`/`mutant:<name>` model, platform
  region, entry, image words with a sha256 guard, the recorded event choice
  `DeclaredNone { OB-ENV-EVENT-DELIVERY }`, the step budget, and the recorded steps + stop
  render), JSON both ways through the crate's own reader/writer, and `replay()` that checks
  identity by name and then walks recorded-vs-replayed through `run::compare`.
  `semulith-verify::reduce`: the ddmin minimizer over the guest word sequence, retention =
  the original first divergence exactly (same step, same field), with the structural
  invariant that every accepted removal retains. `semulith-cli` gains `bundle`, `replay`,
  and `reduce`. No core change — the `.9` table seam is reused as-is.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify 2>&1 | grep "test result"
  test result: ok. 114 passed; 0 failed; ...   # +15 replay suites, +6 reduce suites
  ```

  All four tracked guests replay identically under the production model (round-trip through
  JSON, mutant bundle included); every tamper arm — image word, entry, region, budget,
  generator pin, input pin, dropped pin, scripted event claim, missing accompaniment — is
  refused or named-mismatched; zext-addi minimizes to the 2-word prefix (x1 @ step 1),
  jal-no-link to 4 words (x5 @ step 7), jalr-odd-bit to 9 words (trap @ step 10, tval
  0x80000029 re-derived from the minimized program — the fixture note's prediction,
  retained); every minimized result carries an exhaustive 1-minimality witness; phantom-load
  is refused `NoDivergence` by name (the census class is not reducible on observations).
  CLI exercised end to end: `bundle` → `replay` identical (rc 0), `reduce` prints the
  minimized program, a hand-corrupted bundle is refused with the digest named (rc 1).

- [x] **NO REGRESSION** — `cargo fmt --all -- --check`, `clippy -D warnings`, `cargo test --all`
  (5 suites ok, 65 core + 114 verify), wasm build rc=0, `make gate` green; the live file
  stays under the per-part ceiling by archiving `.9`'s checklist (P1-LAB.md ≤ 65,536;
  archive holds the unedited `.1`–`.9`).

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md` (+shard), `LIVE_STATUS.md`, `DEV_NOTES.md`
  (+shard), `docs/TASK_TREE.md` (10/12), the book's P1 chapter ("Replay and reduction" now
  describes the landed machinery), and this tree — one commit. No doctrine-registry change:
  no new doctrine, no generated artifact.

## Completed-leaf evidence

Archived to [`archive/P1-LAB.md`](archive/P1-LAB.md) — the full, unedited acceptance checklists
for every `done` leaf (`.1`–`.9`), split out on `2026-09-28` when the live file crossed its
per-part ceiling; the ceiling was obeyed, not raised, per the `SOT-FORMAT` precedent. The live
tree keeps the frontier, the decisions, the open questions, the blockers, the final leaf's
checklist and both logs.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
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
