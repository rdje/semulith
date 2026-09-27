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
  Status: `pending`
  Goal: the request/response contract types in `semulith-core`, and controlled memory, fault and event fixtures in `semulith-verify` implementing them.
  Acceptance: the boundary is testable **without** the instruction handler (`docs/CPU_ENVIRONMENT.md` §4.1); negative fixtures are reported as contract violations, not target exceptions.

- ID: `P1-LAB.5` — **typed outcome families**
  Status: `pending`
  Goal: `TargetEvent`, `Advance`, `ModelError`, `UndefinedCase` as separate types (`SEM-01`).
  Acceptance: a target exception can be delivered and execution continue; an unimplemented instruction cannot be reported as an illegal-instruction trap.

- ID: `P1-LAB.6` — **canonical definition skeleton** *(task card `T003`)*
  Status: `pending`
  Goal: owned encodings, state and semantics plus a deterministic generation manifest carrying definition, generator, configuration and source fingerprints (`OWN-01`, `OWN-03`).
  Acceptance: **no duplicate executable owner** for any semantic rule; regeneration is byte-deterministic and CI detects drift.

- ID: `P1-LAB.7` — **graph and report checker** *(task card `T004`)*
  Status: `pending`
  Goal: validate identifier references, profile-scope consistency, graph integrity, artifact existence and hashes, evidence freshness, and gate policy over the JSONL records (`docs/EVIDENCE_AND_GATES.md` §3).
  Acceptance: rejects orphan IDs, stale hashes, unsupported `passed` claims, missing evidence, and deleted dependency links. ⭐ This leaf also discharges the standing gap that `PACKAGE_CHECKS.md`'s schema results are **cited, not re-derivable here** — rule `RUST-01` makes the re-derivation a Rust deliverable, not a Python dependency.

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
| 1 | `P1-LAB.4` | `pending` | environment boundary and fixtures — the state needs its controlled world to step against |

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `P1-LAB.3` | `cargo test --all` | 22 passed / 0 failed (12 arithmetic + 10 state suites) |
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
| `P1-LAB.3` | `SEMILITH-PL-0003 (leaf P1-LAB.3): …` | architectural state, generated from the descriptor; STATE-GEN registered and fired RED first |
| `P1-LAB.2` | `SEMILITH-PL-0002 (leaf P1-LAB.2): …` | arithmetic primitives, verified exhaustively at reduced width |
| `P1-LAB.1` | `SEMILITH-PL-0001 (leaf P1-LAB.1, PORT-WEB.1): …` | the crate skeleton and the Wasm gate land in one commit, as PORT-WEB.1's acceptance requires |

## Changelog

- `2026-09-27`: Leaf `.3` done — `semulith-core::state` generated from `state.sexp` (input
  sha256 in the header, byte-deterministic); x0 hardwired, three ISA-chapter aliases as
  views (C02), SEM-08 census as data; the 21st doctrine `STATE-GEN` refuses drift and was
  fired RED pre-registration; the frontier moves to `.4` (environment boundary). Leaf `.2`
  done the same day — `semulith-core::arith`, verified by boundary + 8-bit-exhaustive
  suites; the frontier moves to `.3` (architectural state). Leaf `.1` done the same day —
  the three crates + the Wasm gate.
