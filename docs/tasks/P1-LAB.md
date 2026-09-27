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
  Status: `pending`
  Goal: source-linked widths and operations with explicit intermediate precision, truncation, sign/zero extension, and shift corner cases (`SEM-03`).
  Acceptance: boundary cases plus **exhaustive checks at a tractably reduced width**; host-mode consistency verified rather than assumed.

- ID: `P1-LAB.3` — **architectural state**
  Status: `pending`
  Goal: generated state accessors and inspection metadata from the state descriptors, including aliases and required pending state (`SEM-08`).
  Acceptance: writing one alias correctly affects every other view (catalog `C02`); fixed-width storage, no per-access allocation (`RUST-03`).

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
| 1 | `P1-LAB.2` | `pending` | every other leaf lands inside these crates; arithmetic primitives are the crate's first real content |

## Decisions

- `2026-09-13`: initial representation is **structured encoding/state/profile data plus typed
  Rust semantic functions**; a semantic IR is added only when an exercised target demonstrates
  a benefit (`ROADMAP.md` §1).
- `2026-09-13`: the reference interpreter is **not** an external oracle — it executes the
  canonical handlers, so its agreement with them is structural, not evidential
  (`docs/ARCHITECTURE.md` §2).

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

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-27` | `P1-LAB.1` | `cargo fmt --check` + `clippy -D warnings` + `cargo test --all` | 5 suites ok, 0 warnings |
| `2026-09-27` | `P1-LAB.1` | `cargo build --workspace --target wasm32-unknown-unknown` | rc=0 (with `PORT-WEB.1`) |
| `2026-09-27` | `P1-LAB.1` | `make gate` | `=== all doctrines green ===` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `P1-LAB.1` | `SEMILITH-PL-0001 (leaf P1-LAB.1, PORT-WEB.1): …` | the crate skeleton and the Wasm gate land in one commit, as PORT-WEB.1's acceptance requires |

## Changelog

- `2026-09-27`: Leaf `.1` done — the three crates exist and build for host and Wasm; the tree is
  `active`, the frontier moves to `.2` (target arithmetic primitives).
