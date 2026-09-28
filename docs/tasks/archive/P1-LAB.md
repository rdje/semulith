# P1-LAB — archived completed-leaf evidence

The full, unedited acceptance checklists for the `done` leaves of the
[`P1-LAB`](../P1-LAB.md) tree (`.1`–`.11` — the final leaf's stays live), plus the
design detail of the completed leaves that carried one (`.7`–`.11`, moved on
`2026-09-29`), split out on `2026-09-28` (after leaf `.9`, then again after
`.10` and `.11`) when the live file crossed its per-part ceiling — the ceiling was obeyed,
not raised, per the `docs/tasks/` precedent set by `SOT-FORMAT`. The live tree keeps the
frontier, the decisions, the open questions, the blockers, every leaf's
goal/acceptance/result, the final leaf's checklist and both logs.

Archived sections, verbatim:

## Acceptance Checklist (leaf P1-LAB.9)

- [x] **REPRODUCE / ISSUE** — the EVD-09 demand as it stood after `.8`: the differential could
  only ever AGREE — the comparator had RED arms on hand-written streams, and the four guests
  passed, but no known-wrong model had ever been run through the laboratory, so "detects"
  was a claim without tested evidence:

  ```
  $ git grep -l "table_with_effect\|run_over\|step_over" HEAD -- crates/ | wc -l
  0                                      # no mutation seam; nothing could be mutated
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `.8` built the observation vocabulary and the comparator
  but the definition sat behind `exec::step`'s static call: a wrong model could only be run by
  forking the evaluator — an OWN-01 violation — so no mutation suite could exist. WHERE,
  measured at the parent commit:

  ```
  $ git grep -n "decode(word)\|pub fn step" HEAD -- crates/semulith-core/src/exec.rs | wc -l
  2                                            # one static step entry, one static decode call
  $ git ls-files 'crates/*' | xargs grep -ln "step_over" | wc -l
  0                                            # the table parameter existed nowhere
  ```

- [x] **FIX** — `exec::step_over` / `run::run_over` take the instruction table; production
  delegates with `INSNS`. `semulith-verify::mutate`: a tree transformer + table builders +
  eleven arms. Model-level mutations are data through the one evaluator; observation-level
  arms (deferred trap, SEM-02 substitution, stale entry, suppression exhibit) are documented
  as such — a wrong behaviour that can only exist as harness code is mutated at the harness
  boundary, never smuggled into the semantics data.

- [x] **ADDRESSED (verified)** — every designated class, detected at its designated step:

  ```
  $ cargo test -p semulith-verify mutate 2>&1 | grep "test result"
  test result: ok. 11 passed; 0 failed; ...   # 8 EVD-09 classes + JALR arm + census + suppression
  $ cargo test -p semulith-core exec 2>&1 | grep "test result"
  test result: ok. 25 passed; 0 failed; ...   # + the generated-table/decode equivalence pin
  ```

  Divergences named, per arm: sign extension → x1 @ step 1 (guest-control); suppressed write
  → x5 @ step 7; JALR odd bit → trap @ step 10, tval 0x80000029 (the fixture note's
  prediction); wrong cause → cause @ step 0; SEM-02 substitution → trap @ step 0; extra
  access → crossing census (trace agrees); overbroad mask → x1 @ step 2 + the hidden-bit
  witness; shifted delivery → missing trap @ step 2; stale entry → pc @ step 0; suppression →
  a writes-blind comparator shown agreeing with a caught mutant.

- [x] **NO REGRESSION** — `cargo fmt --all -- --check`, `clippy -D warnings`, `cargo test --all`
  (5 suites ok), wasm build rc=0, `make gate` green; the archive split obeys the per-part
  ceiling (P1-LAB.md 61 KiB ≤ 65,536; archive holds the unedited `.1`–`.8` checklists), and the
  family aggregate is re-derived with the documented grounds (lanes 25 → 32; per-part
  untouched — `decision_task-tree-family-bound-rederivation.md`).

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md` (+shard), `LIVE_STATUS.md`, `docs/TASK_TREE.md`
  (9/12), `docs/decisions/` (+INDEX) for the bound re-derivation, the book's P1 chapter
  ("Validating the validator" now describes the landed suite), and this tree — one commit. No
  doctrine-registry change: no new doctrine, no generated artifact.

## Acceptance Checklist (leaf P1-LAB.8)

- [x] **REPRODUCE / ISSUE** — the first-execution-slice goal as it stood after `.7`: the
  canonical definition had an evaluator nowhere; the graph checker could judge records, but
  no instruction of the profile could execute, and the roadmap's G1 proof ("a compiled
  freestanding guest program retires under first-divergence comparison against a pinned
  reference") had no first slice to stand on:

  ```
  $ git ls-files 'crates/semulith-core/src/exec.rs' 'crates/semulith-verify/src/run.rs'
  | wc -l
  0                                            # no interpreter, no observation runner
  $ git grep -c "fn step" HEAD -- crates/semulith-core/src | wc -l
  0                                            # nothing executed anything
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `.6` had lowered the semantics into `Sem` trees and
  pinned "evaluation stays with `.8`"; the missing piece was the evaluator plus the
  observation/comparison machinery to make its result mean something. The one genuinely
  undefined design point was the width algebra: `check_semantics.py` checks
  well-formedness/completeness/citations only, so `sext N` operational semantics was
  unpinned — WHERE, measured: two candidate readings each fail half the corpus ("extend the
  low N bits" zero-extends LB; "extend from N" identity-extends LUI); the only uniform rule
  is extend-FROM-the-operand-width-TO-N, with literal shifts widening — then verified
  differentially, not assumed.

- [x] **FIX** — `semulith-core::exec` (the evaluator; the width algebra and the outcome
  mapping documented in the module, every rule named by its requirement), `semulith-verify`
  (`run` — observation runner + first-divergence comparator; `elf` — the loader; `guests` —
  the generated fixture), `semulith-cli` (`semulith run`), `scripts/gen_guests.py`,
  `scripts/check_guest_gen.sh` (the 23rd doctrine `GUEST-GEN`), and
  `scripts/run_semulith_smoke.py` + `parse_semulith` (the live experiment).

- [x] **ADDRESSED (verified)** — the acceptance criteria, re-derived:

  Offline (the commit gate; GUEST-GEN fixture, EVD-05 expectations):

  ```
  $ cargo test -p semulith-verify 2>&1 | grep "test result"
  test result: ok. 77 passed; 0 failed; ...   # incl. all four guests' observations
  $ cargo test -p semulith-core exec 2>&1 | grep "test result"
  test result: ok. 24 passed; 0 failed; ...   # outcome families + width algebra
  $ bash scripts/check_guest_gen.sh
  GUEST-GEN: ok (crates/semulith-verify/src/guests.rs matches the tracked guests)
  ```

  Live (the experiment; `scripts/run_semulith_smoke.py`, `2026-09-28`):

  ```
  == smoke-arith ==   semulith vs sail-riscv  AGREE over 12 aligned step(s)
  == guest-control == semulith vs sail-riscv  AGREE over 13 aligned step(s)
  == smoke-trap ==    semulith vs sail-riscv  AGREE over 3 aligned step(s)
  == guest-no-device == semulith vs sail-riscv AGREE over 6 aligned step(s)
  run_semulith_smoke: ok — semulith matches the specification-derived expectations and
  reproduces; every cross-model comparison that is enabled agrees
  ```

  Every comparison vs spike that is enabled also agrees (12/13/3 steps); semulith's trace
  matches all 34 specification-derived expectation steps and both negative never-written
  registers; every run reproduces byte-identically. The first-divergence report names the
  differing observation — the comparator's RED arms: a register value, the trap cause, the
  tval, a missing write, a length mismatch, each named at its aligned step.

  ⛔ GUEST-GEN fired RED against a hand-edited fixture before registration (rc=1, naming
  DRIFT; restored to rc=0 after regeneration — probe in the verification log).

- [x] **NO REGRESSION** — the strict-lint suite, the Wasm target, and the doctrine gate,
  re-run with the slice wired in:

  ```
  $ cargo fmt --all -- --check && cargo clippy --all-targets --all-features -- -D warnings \
      && cargo test --all 2>&1 | grep -c 'test result: ok'
  5                                    # all suites ok; 141 tests total, 0 warnings
  $ cargo build --workspace --target wasm32-unknown-unknown 2>&1 | tail -1
      Finished `dev` profile ...       # rc=0, PORT-WEB holds
  $ make gate 2>&1 | tail -1
  === all doctrines green ===          # 23 doctrines, including the new GUEST-GEN
  ```

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `LIVE_STATUS.md`, `docs/TASK_TREE.md`,
  the book's P1 chapter (the new "The first execution slice" section) and doctrines
  chapter, `DOCTRINE_ENFORCEMENT.md` (the GUEST-GEN row), `TOOLBOX.md` (the new rows),
  `doctrine/fact_ownership.tsv` (the guest-programs/guest-expectations owner→mirror
  pairs), and this tree — one commit.

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
## Acceptance Checklist (leaf P1-LAB.11)

- [x] **REPRODUCE / ISSUE** — gate `G1`'s fifth criterion ("the performance baseline is
  measured") and ARCHITECTURE §6's three benchmark modes had no instrument at all: nothing
  could run an execution mix, count its allocations, or compare traced against untraced.
  Measured at the parent commit (`0d12c75`):

  ```
  $ git grep -c "run_untraced\|Mix::Arithmetic\|run_diagnostic" HEAD -- crates/ | wc -l
  0                                 # no harness, no mixes, no modes
  $ git grep -n "semulith bench" HEAD -- crates/semulith-cli/src/main.rs | wc -l
  0                                 # no command surface either
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `.8`/`.9`/`.10` built execution, mutation and replay,
  but every runner in the tree was correctness-oriented: `run::run_over` stops at the first
  trap (so a fault-heavy mix could not even be driven), nothing constructed the three
  ARCHITECTURE §6 modes as separately measurable cells, no allocation counting existed
  anywhere (the crate's zero-dependency rule rules out the usual benchmarking crates —
  RUST-01 makes the harness ours), and the static-vs-dynamic observer question was parked
  precisely because nothing could measure it. WHERE: the runner family lived only in
  `crates/semulith-verify/src/run.rs` (stops at first trap, always records crossings —
  one fused mode), and no bench/alloc/statistics code existed (`git grep` above).

- [x] **FIX** — `semulith-verify::bench`: the four programmatically generated mixes (every
  word decode-round-trip-pinned to `definition::decode`), the counting environment wrapper
  (`Census`), the stated harness policy for the fault mix (delivered exception → observe,
  resume at pc+4; requested trap → stop; fetch fault → stop silent, run.rs's rule),
  `run_untraced` / `run_instrumented<O: Observer + ?Sized>` / `run_diagnostic` (sharing
  `run`'s snapshot/diff/trap-mapping/`Recording` as `pub(crate)` — the measured modes ARE
  the production observation construction), `agree` (RUST-02 as data), the `alloc`
  counting allocator (std-only, installed by the CLI binary and the verify test binary,
  never the wasm cdylib), and `stats` (min/median/mean/max + spread). `semulith-cli` gains
  `bench` — names the host, runs warmup+reps per cell, checks RUST-02 as it measures
  (disagreement is exit 1), prints the noise table, sets no threshold. No core change.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify 2>&1 | grep "test result"
  test result: ok. 124 passed; 0 failed; ...   # +10 bench suites
  $ cargo build --release -p semulith-cli && ./target/release/semulith bench
  host: Apple M4 Pro; Darwin 27.0.0; rustc 1.95.0 (59807616e 2026-04-14)
  mix arithmetic: untraced 52.1 / instrumented 69.6 / dyn 69.6 / diagnostic 73.4 ns/step,
    allocs/step 1.00 -> 1.19, spread 1.7-3.6%
  mix control:    47.2 / 65.4 / 65.5 / 70.1, 1.00 -> 1.42, spread 4.6-6.0% (one 113%
    scheduler outlier on a millisecond-scale cell)
  mix memory:     54.1 / 71.0 / 70.9 / 76.9, 1.00 -> 1.23, spread 3.9-6.5%
  mix fault:      50.9 / 69.4 / 67.5 / 71.0, 1.00 -> 1.20, spread 4.6-7.4%
  static vs dynamic observer dispatch: x0.974-1.002 across the mixes
  bench: measured; every mode agrees on every mix (RUST-02 holds)   # rc=0
  ```

  Every generated word decode-round-trips to its intended instruction; each mix's census
  proves its class (arithmetic/control touch no data memory; memory: 7 loads + 4 stores
  per iteration; fault: causes 04/06/05 per iteration in order — the misaligned pair never
  crosses the boundary — plus the closing EBREAK); the delivered-exception policy is
  pinned (the step after a misaligned load is observed at pc+4); mode agreement holds for
  every mix at test budgets; the allocator counts a known allocation; the stats are pinned
  on known inputs; a pc outside the image is refused by name.

- [x] **NO REGRESSION** — `cargo fmt --all -- --check`, `clippy -D warnings`, `cargo test
  --all` (5 suites ok, 65 core + 124 verify), wasm build rc=0, `make gate` green; the live
  file stays under the per-part ceiling by archiving `.10`'s checklist (P1-LAB.md ≤ 65,536;
  the archive holds the unedited `.1`–`.10`).

- [x] **LOCKSTEP** — `MEMORY.md`, `CHANGELOG.md`, `LIVE_STATUS.md`, `DEV_NOTES.md`,
  `docs/TASK_TREE.md` (11/12), the book's P1 chapter ("The performance baseline" now
  carries the measured table), `TOOLBOX.md` (the `semulith bench` row), and this tree —
  one commit. No doctrine-registry change: no new doctrine, no generated artifact.
## Design detail (leaf P1-LAB.7)

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


## Design detail (leaf P1-LAB.8)

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


## Design detail (leaf P1-LAB.9)

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


## Design detail (leaf P1-LAB.10)

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


## Design detail (leaf P1-LAB.11)

  Design (recorded before code, `2026-09-28`): two pieces, on their owning sides of the
  `docs/ARCHITECTURE.md` §4 map — the harness in `semulith-verify` (measurement is evidence
  machinery beside the comparators; no core change), the command surface in `semulith-cli`.
  1. `semulith-verify::bench` — the measurement harness, four parts:
     - **Workload mixes** (`Mix::{Arithmetic, Control, Memory, Fault}`): `program(mix,
       iterations)` generates the guest words programmatically — encoders local to the
       harness (the same standing as `.9`'s mutated trees; a test pins EVERY word to the
       instruction `definition::decode` names for it). Each mix is a counted loop ending
       in EBREAK: **arithmetic** churns the ALU vocabulary with no memory traffic;
       **control** alternates taken/not-taken branches with jal/jalr; **memory** walks
       sd/sw/sh/sb stores and ld/lw/lh/lb/lwu/lhu/lbu loads over a scratch area;
       **fault** runs a model-side misaligned load and store (raised before the boundary)
       plus an environment-side out-of-region load (the boundary's AccessFault) every
       iteration, so the exception paths are the measured common case. The fault mix runs
       under a stated harness policy: a delivered exception is observed and execution
       resumes at pc+4 (delivery-continues, ARCHITECTURE §5); a requested trap (EBREAK)
       stops the run; the step budget is only a safety bound.
     - **The three modes** (ARCHITECTURE §6's untraced / instrumented / diagnostic):
       `run_untraced` (the bare `exec::step` loop — no observation is constructed),
       `run_instrumented<O: Observer + ?Sized>` (the Step stream built by `run`'s own
       snapshot/diff/trap-mapping, reused `pub(crate)`; the word comes from the harness's
       own image, never a second fetch), and `run_diagnostic` (+ the crossing log via
       `run`'s `Recording`). All modes share one counting environment wrapper so the
       census is comparable without being recorded. The instrumented runner is generic
       over the observer, so the open question — static vs dynamic dispatch — is MEASURED,
       not argued: one function instantiated with `VecObserver` and with `dyn Observer` is
       two cells of the same report.
     - **Allocation counts**: a `GlobalAlloc` wrapper over `System` (std-only, RUST-01),
       installed by the CLI binary and by verify's test binary; the wasm cdylib is
       untouched. Allocations and bytes per step per mix per mode — RUST-03's "no
       mandatory per-instruction allocation" as a number, not a posture.
     - **Noise first** (RUST-04): every cell repeated R times after W warmups; the report
       carries min/median/mean/max and the (max−min)/median spread. No threshold is set
       anywhere — the noise table is the deliverable a future threshold must cite.
  2. `semulith bench [--iterations N] [--reps R]` in `semulith-cli` — names the host (OS/arch,
     the CPU brand where the platform supplies one, the rustc version that built the binary),
     runs the cells, and checks RUST-02 AS it measures: per mix, all modes must agree on step
     count, stop classification, final architectural state and crossing census, and the
     instrumented (static and dyn) and diagnostic Step streams must be identical — a
     disagreement is a refusal (exit 1), not a footnote.
  3. Suite (Rust tests, `make check`; no new doctrine — no generated artifact; the harness
     guards measurement honesty, not drift): decode round-trip for every word; per-mix
     census proving each mix exercises its own class; four-mode agreement at small budgets
     (RUST-02 exercised, not just reported); the allocator counts a known allocation; the
     statistics pinned on known inputs.

