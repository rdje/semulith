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
  Status: `pending`
  Goal: a vertical slice executing an **independently encoded** program under the controlled environment, with first-divergence comparison against the reference.
  Acceptance: correct state, access and exception observations; the divergence report names the first differing observation, not a final checksum.

- ID: `P1-LAB.9` — **validator mutation suite** *(task card `T007`)*
  Status: `pending`
  Goal: intentional mutations that must be detected — wrong sign extension, suppressed register write, wrong trap cause, illegal-opcode substitution for a model limitation, an extra memory access, shifted event delivery, an overbroad mask hiding a changed defined bit, a stale reference configuration (`EVD-09`).
  Acceptance: **every** designated wrong behaviour is detected. A suite never run against a broken implementation is not known to detect anything.

- ID: `P1-LAB.10` — **replay and reduction**
  Status: `pending`
  Goal: an input bundle that replays the same result, and a minimizer whose output retains the original divergence.
  Acceptance: a seed is accompanied by algorithm/version and the actual relevant event choices — a bare seed is insufficient.

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
| 1 | `P1-LAB.8` | `pending` | first execution slice — T006; an independently encoded program under the controlled environment, with first-divergence comparison against the reference |

## Acceptance Checklist (leaf P1-LAB.7)

- [x] **REPRODUCE / ISSUE** — the standing gap as it stood: the PACKAGE_CHECKS schema results
  were a citation of Python `jsonschema 4.26.0` output from the planning package, and nothing
  in the workspace could re-derive them:

  ```
  $ git grep -cE "check-examples|check_bundle" HEAD -- crates/ | wc -l
  0
  $ grep -n "jsonschema 4.26.0" docs/provenance/planning-package-v0.2/PACKAGE_CHECKS.md
  | JSON Schema Draft 2020-12 schemas, checked with Python jsonschema 4.26.0 | All 3 schemas valid |
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — RUST-01 ("host production modeling is Rust by default")
  had no production evidence machinery to run on: the records the Python validator checks
  (`examples/*.jsonl`) had no Rust reader, no Rust schema engine, and no graph checker, so the
  "checked" claim could only be inherited from the delivery document. WHERE, measured — the
  whole Rust surface before this leaf:

  ```
  $ git ls-files 'crates/semulith-verify/src/*.rs' 'crates/semulith-verify/src/*/*.rs'
  crates/semulith-verify/src/fixtures.rs
  crates/semulith-verify/src/lib.rs          # four files, none of them evidence machinery
  ```

- [x] **FIX** — five modules in `semulith-verify` (`json`, `pattern`, `sha256`, `schema`,
  `graph`) and the `semulith check-examples` command in `semulith-cli`; `RECORD-SCHEMA`'s
  JSONL arm runs the Rust engine after the Python phase. The library is pure (no `std::fs` —
  evidence bytes arrive through an injected resolver); the two tightenings over the Python
  reference (array `type`; schema-valued `additionalProperties`) are documented in
  `schema.rs` and proven verdict-neutral on the frozen corpus by the suites below.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ cargo test -p semulith-verify 2>&1 | grep "test result"
  test result: ok. 59 passed; 0 failed; ...   # json 8, pattern 7, sha256 2, schema 12, graph 16, fixtures 12
  $ cargo run --quiet -p semulith-cli -- check-examples
  graph check: 2 requirement(s), 2 evidence record(s), 1 obligation(s)
  gate: incomplete — no graph defects, but 2 declared obligation(s) lack successful current evidence: OB-SYN16-ADD, OB-SYN16-INPUT
  $ cargo run --quiet -p semulith-cli -- check-examples >/dev/null; echo $?
  0                                          # incomplete is the honest fixture state, not a failure
  ```

  PACKAGE_CHECKS rows re-derived in Rust (suites in `graph/tests.rs`):
  5/5 frozen records validate on both engines; 6/6 negative controls rejected with the reason
  named (missing source, invalid research status, passing-without-completion, malformed
  fingerprint, passing-proof-without-metadata, invalid contract direction); the synthetic
  source fingerprint matches the ledger pin
  (`12787d59…43f`). Designated rejections, each with a mutation that must be caught: orphan
  evidence id, deleted dependency link, out-of-scope profile, duplicate id, unpinned source,
  missing artifact, stale hash (with the unsupported `passed` claim denied), missing
  evidence, undeclared required check, dependency cycle; and the positive control — a fully
  met bundle gates `passed`.

  ⛔ RECORD-SCHEMA fired RED against a mutated requirement before landing:
  `ORPHAN-EVIDENCE requirements:SYN16-ADD-001: cites evidence 'EV-GHOST' …`, rc=1, restored
  to rc=0 after revert (probe recorded in the verification log).

- [x] **NO REGRESSION** — the strict-lint suite, the Wasm target, and the doctrine gate,
  re-run with the checker wired in:

  ```
  $ make check 2>&1 | grep -cE "test result: ok"
  5                                          # all suites ok; clippy -D warnings clean
  $ cargo build --workspace --target wasm32-unknown-unknown 2>&1 | tail -1
      Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.64s   # rc=0, PORT-WEB holds
  $ make gate 2>&1 | tail -1
  === all doctrines green ===                # RECORD-SCHEMA now two-engine, still green
  ```

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, the book's P1 chapter (new "The graph and report checker" section) and
  doctrines chapter, `DOCTRINE_ENFORCEMENT.md` (RECORD-SCHEMA row), `TOOLBOX.md` (the new
  row), `scripts/check_requirements.sh` (the engine-2 arm), and this tree — one commit.

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
- `2026-09-28` (`.6`): the canonical definition is **lowered, not hand-coded**: encodings,
  semantics trees and the OWN-03 manifest generate into `semulith-core::definition` by
  `scripts/gen_definition.py`; drift is the `DEF-GEN` doctrine's refusal. The generator is the
  executable owner of the *lowering* and re-derives the SEMANTICS doctrine's checks it emits
  through (schema validation, operand binding, the refinement rule, completeness) rather than
  trusting them — a mirror that cannot re-derive its rule is a hope, not a derivation. The
  semantics DATA remains the one executable owner of every rule (OWN-01); `decode` is dispatch
  metadata, and evaluation stays with `.8`.

## Open Questions

- Exact shapes of the four outcome enums — a P1 design result, not a P0 commitment
  (`docs/ARCHITECTURE.md` §5). Does not block `.1`.
- Static versus dynamic dispatch for the diagnostic observer: chosen on **measured** cost, not
  assumed to be free (`docs/ARCHITECTURE.md` §6). Resolved by `.11`.
- Benchmark host, sample sizes and thresholds: no threshold before the noise is characterized.

## Blockers

- `P0-PROFILE` gate `G0`. Building the laboratory before the profile is resolved would bake
  unresolved choices into code.

## Acceptance Checklist (leaf P1-LAB.1)

- [x] **REPRODUCE / ISSUE** — the tree as it stood: one placeholder crate, not three laboratory crates:

  ```
  $ ls crates/
  app
  $ grep '^name' crates/app/Cargo.toml
  name = "semulith"        # the starter crate, owns nothing of the laboratory
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the laboratory's crate boundary existed only as a table in
  `docs/ARCHITECTURE.md` §4; nothing in `crates/` implemented it, so there was no place the
  schema-sufficient definition (`EXTRACTION` verdict) could be consumed from. WHERE, measured:

  ```
  $ git ls-files crates | sort
  crates/app/Cargo.toml
  crates/app/src/main.rs        # two files, the whole of the Rust workspace
  ```

- [x] **FIX** — replaced `crates/app` with `semulith-core` (no dependencies), `semulith-verify`
  (`fixtures` module home, depends on core only), `semulith-cli` (bin `semulith`, depends on
  both). Each crate's docs state its ownership rule from day one; behaviour stays with its
  owning leaf (`P1-LAB.2`+).

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ grep -A2 'name = "semulith-core"' Cargo.lock
  name = "semulith-core"
  version = "0.1.0"          # no [dependencies] block: core depends on neither other crate
  $ cargo tree --workspace --prefix none | sort -u | head -4
  semulith-cli v0.1.0 (.../crates/semulith-cli)
  semulith-core v0.1.0 (.../crates/semulith-core)
  semulith-verify v0.1.0 (.../crates/semulith-verify)
  semulith-verify v0.1.0 (.../crates/semulith-verify) (*)
  $ cargo build --workspace --target wasm32-unknown-unknown 2>&1 | tail -1
      Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.25s   # rc=0
  ```

- [x] **NO REGRESSION** — the strict-lint suite, re-run on the new workspace:

  ```
  $ cargo fmt --all -- --check && cargo clippy --all-targets --all-features -- -D warnings && cargo test --all 2>&1 | grep -c 'test result: ok'
  5                                    # 5 suites, all ok, 0 warnings at -D warnings
  $ make gate 2>&1 | tail -1
  === all doctrines green ===
  ```

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, `docs/book/src/plan/p1.md`, `docs/book/src/working/doctrines.md`,
  `DOCTRINE_ENFORCEMENT.md`, `TOOLBOX.md`, `.github/workflows/doctrines.yml` and this tree —
  one commit, with [`PORT-WEB.1`](PORT-WEB.md) (the browser half of the skeleton).

## Acceptance Checklist (leaf P1-LAB.2)

- [x] **REPRODUCE / ISSUE** — SEM-03's demand as it stood: no numeric operation existed, so
  widths/signedness/intermediate precision were nowhere stated in code:

  ```
  $ git ls-files 'crates/**/*.rs' | xargs wc -l
  3 crates/semulith-cli/src/main.rs       # the whole workspace: docs and a println
  5 crates/semulith-core/src/lib.rs
  5 crates/semulith-verify/src/lib.rs
  3 crates/semulith-verify/src/fixtures.rs
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the laboratory's first real content had no home: the
  semantics data (`definitions/riscv/rv64i.sem.sexp`) names the operations (`add`, `shl`,
  `sext`, `bits`, …) but nothing executable implemented them, and the ALU/shift requirements
  (`REQ-D-ALU-REG`, `REQ-D-ALU-IMM`, `REQ-D-SHAMT`, `REQ-D-WSUFFIX`) carried
  `implementation_status planned`. WHERE, measured: `grep -c 'pub fn' crates/semulith-core/src`
  → `0` before this leaf.

- [x] **FIX** — `semulith-core::arith`: one function per semantics-data operation, each
  contract stating width, signedness, intermediate precision, truncation, exceptional
  behavior (SEM-03), source-linked by requirement id + locator; `shamt64`/`shamt32` own the
  REQ-D-SHAMT masking; unmasked amounts panic in debug instead of silently wrapping.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ cargo test -p semulith-core 2>&1 | grep "test result"
  test result: ok. 12 passed; 0 failed; ...    # 5 boundary + 4 exhaustive + 1 should_panic + 2 word-op suites
  ```

  The exhaustive layer is genuinely exhaustive: every `(x, y)` in `0..=255²` for add/sub/
  and/or/xor/slt/sltu, every `(x, shamt)` in `256 × 0..8` for the shifts, every `(x, from)`
  for `sext`, every `(lo, hi)` window for `bits` — each against a different-host-width
  reference. The first run FAILED on exactly the class of mistake the acceptance names
  (`slt`/`sar` compared without embedding the signed view — `test result: FAILED. 10 passed;
  2 failed`), which is the host-mode-consistency assumption being verified rather than
  assumed; the fix is in the test design, the primitives were right.

- [x] **NO REGRESSION** — `cargo clippy --all-targets --all-features -- -D warnings` clean;
  `make gate` → `=== all doctrines green ===`; the new lesson is promoted, not dropped:
  `docs/knowledge/reduced-width-verification-of-signed-ops.md` + INDEX row, same commit.

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, the book's P1 chapter, the knowledge layer, and this tree — one commit.

## Acceptance Checklist (leaf P1-LAB.3)

- [x] **REPRODUCE / ISSUE** — the laboratory's architectural state existed only as a descriptor;
  nothing executable implemented it, and C02's alias question had no code to answer it:

  ```
  $ git ls-files 'crates/**/*.rs' | sort
  crates/semulith-cli/src/main.rs
  crates/semulith-core/src/arith.rs
  crates/semulith-core/src/arith/tests.rs
  crates/semulith-core/src/lib.rs
  crates/semulith-verify/src/fixtures.rs
  crates/semulith-verify/src/lib.rs
  $ git grep -c "ArchitecturalState" HEAD -- crates/
  0 matches — no architectural state existed
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `state.sexp` (the authority, EXTRACTION-cited) had no
  executable half: `docs/ARCHITECTURE.md` §2 assigns "state accessors and inspection
  metadata" to the "state/alias definitions" as a DERIVATION, and no generator or hand code
  performed it. WHERE, measured — no accessor, alias, or state type existed anywhere in the
  workspace at this leaf's parent commit:

  ```
  $ git grep -c 'ArchitecturalState' HEAD -- crates/ | wc -l
  0
  ```

  The register file, pc, aliases, and the SEM-08 census lived in exactly one place — the
  descriptor itself.

- [x] **FIX** — `scripts/gen_state.py` derives `crates/semulith-core/src/state.rs` from
  `profiles/rv64i-lab-v0/state.sexp` through `dossier_sexp.load_state` (the single mapping
  owner), emitting: fixed-width storage (`[u64; 32]` + pc), the x0 hardwired discipline, the
  three ISA-chapter aliases as index views, the `ELEMENTS` inspection table, and the
  hidden-state census as data. Byte-deterministic; input sha256 in the module header (OWN-03).
  Hand-written tests live beside it in `state/tests.rs` (the arith layout). Drift is gated by
  the `STATE-GEN` doctrine (`scripts/check_state_gen.sh`, registered 21st, fired RED against a
  hand-edited module before registration); the owner→mirror pair is registered in
  `doctrine/fact_ownership.tsv`.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ cargo test -p semulith-core state 2>&1 | grep "test result"
  test result: ok. 10 passed; 0 failed; 0 ignored; 0 measured; 12 filtered out; finished in 0.01s
  ```

  Catalog C02 ("does writing one alias correctly affect every other view?"): ten suites,
  including `alias_write_is_visible_through_every_view` (both directions for all three named
  aliases) and `one_storage_means_every_view_agrees` (distinct value per register, read back
  through every view — a copied alias file would disagree). RUST-03:
  `state_is_33_words_inline` asserts `size_of::<ArchitecturalState>() == 33 * 8`; the
  accessors take `&self`/`&mut self` and return `u64`, so no per-access allocation exists in
  the API by construction. SEM-08: `census_records_every_candidate_checked_and_none_present`
  re-derives the census from the generated data. Reset/entry state and x0 discipline each
  carry their own suite. Generation itself is the acceptance's "generated" claim, kept
  honest:

  ```
  $ bash scripts/check_state_gen.sh
  STATE-GEN: ok (crates/semulith-core/src/state.rs matches profiles/rv64i-lab-v0/state.sexp, sha256 ff53fb04f3ed7ac2)
  $ bash scripts/check_state_gen.sh --self-test
  STATE-GEN --self-test: 6 pass / 0 fail
  ```

- [x] **NO REGRESSION** — the strict-lint suite and the doctrine gate, re-run on the new
  workspace:

  ```
  $ cargo fmt --all -- --check && cargo clippy --all-targets --all-features -- -D warnings && cargo test --all 2>&1 | grep -c 'test result: ok'
  5                                    # 5 suites, all ok; 22 tests, 0 warnings at -D warnings
  $ cargo build --workspace --target wasm32-unknown-unknown 2>&1 | tail -1
      Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.34s   # rc=0, PORT-WEB holds
  $ make gate 2>&1 | tail -1
  === all doctrines green ===          # 21 doctrines, including the new STATE-GEN
  ```

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, `docs/book/src/plan/p1.md`, `docs/book/src/working/doctrines.md`,
  `DOCTRINE_ENFORCEMENT.md`, `doctrine/fact_ownership.tsv` (+ its census in
  `scripts/check_fact_ownership.sh`), and this tree — one commit. `LIVE_STATUS`'s doctrine
  name list completed (STATE-GEN added; SCOPE-COVERAGE, omitted when it landed, restored).

## Acceptance Checklist (leaf P1-LAB.4)

- [x] **REPRODUCE / ISSUE** — the boundary `docs/ARCHITECTURE.md` §4 assigns to
  `semulith-core` ("environment request/response contract types") existed only as the
  contract records; nothing crossed it:

  ```
  $ git grep -cE "trait Environment|FlatMemory|ContractViolation" HEAD -- crates/ | wc -l
  0
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `rv64i-lab-env-v0`'s obligations name a boundary
  (fetch supply, access widths, address space, misalignment) but no Rust type could express
  a crossing: `docs/CPU_ENVIRONMENT.md` §4.1 demands requests/responses be testable
  "independently of the CPU instruction handler", and there was no request to test.
  WHERE, measured — the four laboratory surfaces at this leaf's parent commit:

  ```
  $ git ls-files 'crates/*/src/*.rs' 'crates/*/src/*/*.rs' | sort
  crates/semulith-cli/src/main.rs
  crates/semulith-core/src/arith.rs
  crates/semulith-core/src/arith/tests.rs
  crates/semulith-core/src/env.rs            # does not exist yet — this leaf adds it
  crates/semulith-core/src/lib.rs
  crates/semulith-core/src/state.rs
  crates/semulith-core/src/state/tests.rs
  crates/semulith-verify/src/fixtures.rs     # a 5-line placeholder
  crates/semulith-verify/src/lib.rs
  ```

- [x] **FIX** — `semulith-core::env`: the contract types and the one-entry-point
  `Environment` trait (see the leaf Result above). `semulith-verify::fixtures`: `FlatMemory`
  and `ScriptedEnv` implementing it. Hand-written tests beside each module, the arith/state
  layout.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived with no instruction
  handler anywhere in the run:

  ```
  $ cargo test -p semulith-verify 2>&1 | grep "test result"
  test result: ok. 12 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
  $ cargo test -p semulith-core env 2>&1 | grep "test result"
  test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 22 filtered out; finished in 0.00s
  ```

  §4.1 boundary properties, each named: widths round-trip at every alignment; little-endian
  byte order; loads return raw bits (no extension at the boundary); stores write only low
  bits; fetch returns the LE word with a per-request fetch counter (no extraneous fetch);
  fetch re-reads (code visibility); misaligned → `Target(Misaligned)`; outside/crossing the
  region → `Target(AccessFault)`; region edge exact. Negative fixtures
  (§4.1.4): `wrong_request_is_a_contract_violation_not_a_target_failure` and
  `request_after_the_script_is_a_contract_violation` assert `BoundaryError::Violation(..)`
  and never a `Failure` — the fixture reports the contract breach to the harness instead of
  inventing data or dressing it as a target exception.

- [x] **NO REGRESSION** — the strict-lint suite and the doctrine gate, re-run:

  ```
  $ cargo fmt --all -- --check && cargo clippy --all-targets --all-features -- -D warnings && cargo test --all 2>&1 | grep -c 'test result: ok'
  5                                    # 5 suites, all ok; 42 tests total, 0 warnings
  $ cargo build --workspace --target wasm32-unknown-unknown 2>&1 | tail -1
      Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.33s   # rc=0, PORT-WEB holds
  $ make gate 2>&1 | tail -1
  === all doctrines green ===
  ```

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, `docs/book/src/plan/p1.md`, and this tree — one commit. (No doctrine
  registry changes this slice; `env` is a new module in an already-owned crate, and the
  fixtures live in the home `.1` fixed for them.)

## Acceptance Checklist (leaf P1-LAB.5)

- [x] **REPRODUCE / ISSUE** — SEM-01's separation existed only as a rules document; no Rust
  type could say "target event", "model error", or "undefined case" distinctly:

  ```
  $ git grep -cE "StepOutcome|ModelError|UndefinedCase" HEAD -- crates/ | wc -l
  0
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `docs/ARCHITECTURE.md` §5 assigns the four families
  to `semulith-core` ("use separate typed families") and notes "precise enum shapes are a
  P1 design result"; that design result had no home — the laboratory could report a
  contract violation (`.4`) but had nowhere to put a trap, a stop, a gap, or a reserved
  word. WHERE, measured: the `outcome` module this leaf adds is the fifth module in
  `semulith-core`; before it, four.

  ```
  $ git ls-files 'crates/semulith-core/src/*.rs' | sort
  crates/semulith-core/src/arith.rs
  crates/semulith-core/src/env.rs
  crates/semulith-core/src/lib.rs
  crates/semulith-core/src/outcome.rs   # does not exist yet — this leaf adds it
  crates/semulith-core/src/state.rs
  ```

- [x] **FIX** — `semulith-core::outcome`: the four families as enums with named,
  source-linked variants (see the leaf Result), plus `StepOutcome`, the step-level sum a
  harness matches on. `env::ContractViolation` re-homes into `ModelError` by a `From` impl
  in this module; `BoundaryError` stays boundary-local until `.8`'s instruction layer
  converts its `Target` arm into `TargetEvent`.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  ```
  $ cargo test -p semulith-core outcome 2>&1 | grep "test result"
  test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 26 filtered out; finished in 0.00s
  ```

  Clause one — `a_delivered_exception_lets_execution_continue`: a stub program
  [add, break, add] runs under a harness that records the delivered `Breakpoint` trap and
  steps on; the register shows both adds ran and pc advanced past all three. Clause two —
  `an_unimplemented_instruction_is_not_an_illegal_instruction_trap`: the stub's
  `Missing` arm produces `Failed(ModelError::Unimplemented)`, and the exhaustive match in
  the test demonstrates that reaching an `IllegalInstruction` `Exception` from a
  `Failed` value has no typed expression. Family distinctness, the `ContractViolation`
  re-homing, and the `UndefinedCase`-is-not-`Exception` separation each carry their own
  suite.

- [x] **NO REGRESSION** — the strict-lint suite and the doctrine gate, re-run:

  ```
  $ cargo fmt --all -- --check && cargo clippy --all-targets --all-features -- -D warnings && cargo test --all 2>&1 | grep -c 'test result: ok'
  5                                    # 5 suites, all ok; 43 tests total, 0 warnings
  $ cargo build --workspace --target wasm32-unknown-unknown 2>&1 | tail -1
      Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.34s   # rc=0, PORT-WEB holds
  $ make gate 2>&1 | tail -1
  === all doctrines green ===
  ```

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, `docs/book/src/plan/p1.md` (the families section now describes the
  landed types), and this tree — one commit.

## Acceptance Checklist (leaf P1-LAB.6)

- [x] **REPRODUCE / ISSUE** — the canonical definition had no executable half: the encodings
  and semantics the SEMANTICS gate checks existed only as documents; nothing in the workspace
  could consume them, and OWN-01/OWN-03's "one owned executable implementation per rule,
  generated artifacts with a manifest" had no artifact and no manifest:

  ```
  $ git grep -cE "DefinitionManifest|InsnDef|pub fn decode" HEAD -- crates/ | wc -l
  0
  $ git ls-files 'crates/semulith-core/src/*.rs' | sort
  crates/semulith-core/src/arith.rs
  crates/semulith-core/src/arith/tests.rs
  crates/semulith-core/src/env.rs
  crates/semulith-core/src/env/tests.rs
  crates/semulith-core/src/lib.rs
  crates/semulith-core/src/outcome.rs
  crates/semulith-core/src/outcome/tests.rs
  crates/semulith-core/src/state.rs
  crates/semulith-core/src/state/tests.rs   # no definition module — this leaf adds it
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the definition files were checkable (SEMANTICS: 52/52)
  but not consumable: `docs/ARCHITECTURE.md` §2 assigns "decoder and decoded-operation types"
  to the encoding definitions as a GENERATION, and no generator performed it; `.3` had proven
  the pattern for state alone, and OWN-03's manifest (definition, generator, configuration and
  source fingerprints) existed nowhere. WHERE, measured — nine modules before this leaf, and
  the definition lands as the tenth file with its tests beside it:

  ```
  $ git ls-files 'crates/semulith-core/src/*.rs' | wc -l
  9
  $ git ls-files 'crates/semulith-core/src/*.rs' | sort | tail -1
  crates/semulith-core/src/state/tests.rs   # definition.rs and definition/tests.rs land next
  ```

- [x] **FIX** — `scripts/gen_definition.py` lowers `profiles/rv64i-lab-v0/encoding.sexp`
  (composing `definitions/riscv/rv64i.sexp` through the one shared resolver, `riscv_asm.
  load_canonical_encoding`) plus `definitions/riscv/rv64i.sem.sexp` into
  `crates/semulith-core/src/definition.rs`: `FIELDS` (12, scatters attached), `INSNS` (52,
  sorted, with mask/value/operands/from/citation), the `Sem` effect trees, `decode`, and
  `MANIFEST` — OWN-03's manifest as data. The generator re-derives every check it emits
  through: schema validation per input, the SEMANTICS binding rule, the MODEL-COMPOSE.6
  refinement rule, completeness, fixed-field sanity — refusing by name what it cannot emit.

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  OWN-01 (no duplicate executable owner): the effect trees are lowered from the semantics
  data; the only handwritten Rust is tests, which re-derive invariants on the data rather
  than restating rules:

  ```
  $ cargo test -p semulith-core definition 2>&1 | grep "test result"
  test result: ok. 10 passed; 0 failed; ...    # manifest, completeness, disjointness,
                                               # binding rule, FENCE ratchet, scatter accounting
  ```

  OWN-03 (manifest carrying definition, generator, configuration and source fingerprints):
  `MANIFEST.inputs` names all four canonical inputs by path and sha256; `MANIFEST.generator`
  names `scripts/gen_definition.py` with its content hash; `profile`/`ilen`/`fragments` carry
  the configuration; `MANIFEST.sources` carries the `rv_i`/`rv64_i` pins from the fragment.
  Regeneration is byte-deterministic and CI-detected:

  ```
  $ bash scripts/check_definition_gen.sh --self-test
  DEF-GEN --self-test: 8 pass / 0 fail
  $ printf '\n// hand edit\n' >> crates/semulith-core/src/definition.rs
  $ bash scripts/check_definition_gen.sh
  gen_definition: DRIFT — crates/semulith-core/src/definition.rs no longer matches ...
  DEF-GEN: FAIL ... Regenerate — never edit: python3 scripts/gen_definition.py   # rc=1
  $ python3 scripts/gen_definition.py && bash scripts/check_definition_gen.sh
  DEF-GEN: ok (crates/semulith-core/src/definition.rs matches the canonical definition,
  encoding sha256 93a2d4718a50b60c)                                                # rc=0
  ```

  Fired RED against the real module (hand edit, rc=1, diff naming the appended bytes) before
  registration — the rite caught a real defect first: a relative `--encoding` path crashed
  `relative_to` and the check collapsed the crash to rc=1 (a verdict) instead of rc=2 (a
  refusal); fixed in the generator (`repo_rel`) and in the check (rc 2 propagates as REFUSED).

- [x] **NO REGRESSION** — the strict-lint suite, the Wasm target, and the doctrine gate,
  re-run with the doctrine registered:

  ```
  $ cargo fmt --all -- --check && cargo clippy --all-targets --all-features -- -D warnings \
      && cargo test --all 2>&1 | grep -c 'test result: ok'
  5                                    # 5 suites, all ok; 53 tests total, 0 warnings
  $ cargo build --workspace --target wasm32-unknown-unknown 2>&1 | tail -1
      Finished `dev' profile [unoptimized + debuginfo] target(s) in 0.54s   # rc=0, PORT-WEB holds
  $ make gate 2>&1 | tail -1
  === all doctrines green ===          # 22 doctrines, including the new DEF-GEN
  ```

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `DEV_NOTES.md`, `LIVE_STATUS.md`,
  `docs/TASK_TREE.md`, `docs/book/src/plan/p1.md`, `docs/book/src/working/doctrines.md`,
  `DOCTRINE_ENFORCEMENT.md`, `TOOLBOX.md`, `doctrine/fact_ownership.tsv` (+ its census in
  `scripts/check_fact_ownership.sh`), and this tree — one commit. (TOOLBOX also gains the
  rows `.3` owed: `gen_state.py`/`check_state_gen.sh` were missing from the tool table.)

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
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
| `P1-LAB.7` | `SEMILITH-PL-0007 (leaf P1-LAB.7): …` | the graph and report checker in `semulith-verify`; PACKAGE_CHECKS rows re-derived in Rust; RECORD-SCHEMA two-engine, fired RED on a mutated record first |
| `P1-LAB.6` | `SEMILITH-PL-0006 (leaf P1-LAB.6): …` | the canonical definition, generated: decode tables, lowered semantics trees, OWN-03's manifest; DEF-GEN registered and fired RED first |
| `P1-LAB.5` | `SEMILITH-PL-0005 (leaf P1-LAB.5): …` | the four SEM-01 outcome families as types; delivery-continues and unimplemented≠trap proven |
| `P1-LAB.4` | `SEMILITH-PL-0004 (leaf P1-LAB.4): …` | the environment boundary and its fixtures, testable without the instruction handler |
| `P1-LAB.3` | `SEMILITH-PL-0003 (leaf P1-LAB.3): …` | architectural state, generated from the descriptor; STATE-GEN registered and fired RED first |
| `P1-LAB.2` | `SEMILITH-PL-0002 (leaf P1-LAB.2): …` | arithmetic primitives, verified exhaustively at reduced width |
| `P1-LAB.1` | `SEMILITH-PL-0001 (leaf P1-LAB.1, PORT-WEB.1): …` | the crate skeleton and the Wasm gate land in one commit, as PORT-WEB.1's acceptance requires |

## Changelog

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
