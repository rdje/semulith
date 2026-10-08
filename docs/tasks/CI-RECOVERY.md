# CI-RECOVERY: repair the pushed GitHub workflow failures

## Metadata

- Tree ID: `CI-RECOVERY`
- Status: `active`
- Roadmap lane: cross-cutting verification / zero-defect ownership; no milestone credit
- Created: `2026-10-08`
- Owner: repo-local workflow

## Goal

Repair the three latest failed workflows and the additional cross-endian defect;
verify their exact cold-run triggers and distinguish local evidence from hosted results.

## Non-Goals

- Do not weaken strict Clippy, skip books, or turn missing mandatory legs into passes.
- Do not claim GitHub green before the repaired commit has a successful hosted run.
- No exceptional push without the director's explicit approval act per COMMIT.md.

## Acceptance Criteria

1. Each reported failure is reproduced and repaired with focused controls.
2. Cold CI provisioning matches the tools and paths the checks actually need.
3. Local full CI passes; hosted verification remains explicit until a permitted push.
4. Every slice commits separately with live docs and book reflecting measured evidence.

## Task Tree

- ID: `CI-RECOVERY`
  Status: `active`
  Goal: restore hosted CI and truthful validation claims
  Children: `CI-RECOVERY.1`, `CI-RECOVERY.2`, `CI-RECOVERY.3`, `CI-RECOVERY.4`

- ID: `CI-RECOVERY.1` — strict stable Clippy
  Status: `done`
  Goal: replace the map_or identity in bench.rs with its equivalent unwrap_or; run
  strict lint and meaningful benchmark diagnostics on the current/tested toolchain.
  Also repair the three constant-size chunk lints in sha256.rs exposed by Rust 1.99
  before editing those paths; preserve digest/padding behavior with known-answer tests.
  Acceptance: no lint suppression; same first-difference behavior; strict lint green.
  Verification: Rust 1.99 make check green; 259 hashlib comparisons; 1.95 bench 14/14 and SHA 2/2.
  Commit: SEMULITH-CI-0001

- ID: `CI-RECOVERY.2` — provision the doctrine runner
  Status: `done`
  Goal: explicitly install a compatible mdbook in the clean GitHub job and audit the
  enforcer's other mandatory provisioning requirements using public tool interfaces.
  Acceptance: required book tool exists before the gate; cold provisioning verified.
  Verification: cold missing-tool RED; verified native installation; UNIT-BOOKS 7/7 and five books; official Linux digest/layout verified.
  Commit: SEMULITH-CI-0002

- ID: `CI-RECOVERY.3` — portable cold Miri/endian legs
  Status: `active`
  Goal: create the output directory before redirections; remove the macOS-specific
  nightly name from the cross-endian target query; audit single-leg cold execution.
  Acceptance: hand stub controls on Linux/macOS shapes discriminate both old defects;
  the actual nightly/Miri result and any remaining provisioning gap are stated exactly.
  Verification: slice (a) controls 9+15 green; actual native Miri 153/153; big-endian confirmation running.
  Commit: SEMULITH-CI-0003 (slice a); closure pending confirmation

- ID: `CI-RECOVERY.4` — local/hosted evidence and follow-through
  Status: `proposed`
  Goal: run make ci after all repairs, record toolchain differences and omitted/absent
  legs honestly, and observe all workflows after the next cadence/approved push.
  Acceptance: no remote-green claim from local checks; failures owned until verified.
  Verification: pending
  Commit: pending

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `CI-RECOVERY.3` | `active` | reproduce cold log and Linux query failures, then repair and run real Miri |

## Decisions

- `2026-10-08`: read GitHub runs via authenticated gh. The latest pushed revision
  e1fe37942cba2eb4014a7a0f30dc7b9c8e0734e7 has three failures, and the current f356d76
  changes none of their affected files (`git diff e1fe379..HEAD -- .github/workflows
  crates/semulith-verify/src/bench.rs scripts/check_portability.sh`: empty).
  Root evidence:
  - Rust run https://github.com/rdje/semulith/actions/runs/37749540668: stable Rust
    1.99.0 Clippy map_or_identity at bench.rs:929–933; local Rust/Clippy is 1.95.0.
  - Doctrines https://github.com/rdje/semulith/actions/runs/37749541005: UNIT-BOOKS
    REFUSED, mdbook absent from PATH. Workflow provisions wasm/vendor but not mdbook.
  - Portability https://github.com/rdje/semulith/actions/runs/37749540622: miri.log
    redirection fails because target/portability does not exist in the cold Miri job.
  - `sed -n '180,200p' scripts/check_portability.sh` also exposes a macOS-only
    nightly-aarch64-apple-darwin target query used unconditionally on Linux; repair
    before claiming cross-endian verification. These are repository-owned defects.
  Priority: urgent before the next push; archive transition first, then these repairs,
  then P4 C/count staging. No interpretation of the archive approval authorizes a push.

## Open Questions

- Hosted verification waits for a permitted cadence or director-approved exceptional push.

## Blockers

- Hosted result waits for a permitted push; local implementation and focused verification can proceed.

## Acceptance Checklist

`.3` slice (a), 2026-10-08, SEMULITH-CI-0003; parent remains active:

- [x] **ROOT CAUSE** — parent cold Miri control rc=1, `miri.log: No such file or
  directory`; Linux target query rc=1, `cross-endian: absent` despite a provisioned
  target. Dated/native queries were not generic. Actual local setup exposed the parent
  workspace and strict-vendor conflicts recorded below. Parent verdict emitted `passed`
  for `red (manifest mismatch)`, rc=0; translated-green selector returned rc=1.
- [x] **ADDRESSED (slice a)** — common output/Cargo/temp setup; dated nightly authority
  exposed via --print-toolchain; separate explicit MIRI_SYSROOTs; locked root/toolchain
  vendor synchronization before public setup. Root workspace excludes target, membership
  remains four crates. Outcome prefixes/unknown failures counted, translated green
  accepted, current native digest compared and digest failure refused.
  `PORTABILITY --self-test: 9 pass / 0 fail`; `PORTABILITY-COLD: 15 pass / 0 fail`.
- [x] **NO REGRESSION (slice a)** — final fixed script snapshot is byte-identical to
  the working script (`cmp` rc=0). Actual native dated Miri:
  `test result: ok. 153 passed; 0 failed; 0 ignored`, 1296.07 s; outer `miri: green`,
  rc=0. bash -n rc=0; all three workflow YAMLs parsed and their local stores checked.
  Cargo.lock unchanged. Big-endian confirmation is pending, not included in this claim.
- [x] **FIX / LOCKSTEP** — instrument and independent cold controls, Cargo.toml,
  rust/portability workflows, task/index, MEMORY, CHANGELOG, DEV_NOTES, tool/book docs.
  Failed leg tails and log-only CI artifacts preserve future diagnosis. The dated
  historical portability record is untouched; translation does not claim native hardware.
  promotion: declined (specific CI repair; public-interface controls and scoped receipts retain the reproducible causes).

Confirmation slice (b): observe target/ci-recovery/cross-real.log and
 target/portability/cross.log (immutable script target/ci-recovery/portability-verified.sh),
then record the actual outcome and run full local CI. The first live-source run was
invalidated and stopped; only the fixed-snapshot native receipt above is accepted.


`.2`, 2026-10-08, SEMULITH-CI-0002:

- [x] **ROOT CAUSE** — with mdbook absent from PATH, the actual check returned rc=2:
  `UNIT-BOOKS: REFUSED — mdbook is not on PATH; this check cannot judge.` The old
  doctrines.yml had no book provisioning. Mandatory enforcer prerequisites enumerated
  through `rg -n 'command -v' scripts/check_*.sh`: Python, Cargo, mdBook and standard
  OS utilities; PORT-WEB additionally checks the installed wasm target.
- [x] **ADDRESSED** — scripts/install_ci_mdbook.sh pins official 0.5.4 release assets
  from https://github.com/rust-lang/mdBook/releases/tag/v0.5.4, checks the compressed
  digest before extracting the one binary, and checks its version. Native cold run:
  `install-ci-mdbook: verified mdbook v0.5.4 in .app-data/ci-tools/bin`; Linux asset
  digest/layout verified independently (one mdbook member). Corrupt cache control:
  `MDBOOK-PROVISION: corrupt cache refused before binary replacement (rc=1)`.
  The workflow advertises GITHUB_PATH before the gate; YAML parsed and order checked.
- [x] **NO REGRESSION** — cold PATH plus only the newly installed tool yields
  `UNIT-BOOKS: ok (5 unit(s) — every registered unit has its book, and every book builds)`;
  `UNIT-BOOKS --self-test: 7 pass / 0 fail`; all books via make book rc=0; bash -n rc=0.
  The exact public rustup provisioning command installed stable 1.99.0, rustfmt/Clippy
  and wasm into the local store, rc=0. Both tool/cache st_dev equal the repository.
- [x] **FIX / LOCKSTEP** — installer and doctrines.yml, tool register, tree/frontier,
  MEMORY/CHANGELOG/DEV_NOTES and book. Rust toolchains, Cargo downloads and temporary
  outputs derive from the repository root. Existing OS Git/Bash/Python/curl/tar and
  rustup launcher are necessary read-only system dependencies; self-update is disabled.
  Linux execution and hosted green remain explicitly with `.4`, not implied here.
  promotion: declined (bounded CI provisioning repair; authenticated installer and cold-run evidence capture the lesson).


`.1`, 2026-10-08, SEMULITH-CI-0001:

- [x] **ROOT CAUSE** — repository-local Rust/Clippy 1.99.0 reproduced
  `clippy::map_or_identity` in bench.rs and three `clippy::chunks_exact_to_as_chunks`
  errors in sha256.rs; strict lint rc=101. The latter path is unchanged since e1fe379
  (`git diff e1fe379..HEAD -- crates/semulith-verify/src/sha256.rs`: empty).
- [x] **ADDRESSED** — `RUSTUP_TOOLCHAIN=1.99.0 make check` rc=0: strict lint has no
  suppression. `Option::unwrap_or` preserves the mismatch index/fallback; fixed-size
  array chunks preserve SHA blocks/remainders and make the private 64-byte compression
  boundary a type contract. `SHA-PROBE: 259 independent hashlib comparisons passed`
  across lengths 0–256, 4096 and 65536, deterministic nonuniform input.
- [x] **NO REGRESSION** — Rust 1.99 make check rc=0 (fmt, all-target/all-feature lint,
  all workspace tests); existing 14 benchmark and two SHA suites pass. Rust 1.95 focused
  rerun: `test result: ok. 14 passed; 0 failed` and `2 passed; 0 failed`.
- [x] **FIX / LOCKSTEP** — bench.rs and sha256.rs, this tree/frontier/index, MEMORY,
  CHANGELOG, DEV_NOTES, LIVE_STATUS and book. No workflow change yet; GitHub remains
  unverified for these local commits. Toolchain/cache/scratch stay in .app-data/target;
  shared rustup launcher is read-only, provisioning uses `--no-self-update`.
  promotion: declined (ordinary lint/API maintenance; toolchain/evidence scope retained in this receipt and the book).


Discovery receipt only; the four repair leaves remain proposed and unverified.

- [x] **ROOT CAUSE** — `gh run view --log-failed` located `clippy::map_or_identity`
  on Rust 1.99.0, `UNIT-BOOKS: REFUSED` for missing mdbook, and the cold Miri log
  redirection failure. The run URLs and affected paths are recorded above.
- [x] **ADDRESSED (discovery)** — `git diff e1fe379..HEAD -- .github/workflows
  crates/semulith-verify/src/bench.rs scripts/check_portability.sh` returned no changes;
  all three failures remain. Four owned repair leaves now precede P4 staging.
  This checks ownership and scheduling, without claiming a repaired workflow.
- [x] **NO REGRESSION (discovery)** — the same `git diff` is empty: this discovery
  changes no workflow, Rust code or portability implementation. Archive verification
  remains with LIVE-CONTAINMENT.4 slice (a), not with this future repair tree.

## Verification Log

`.1`: target/ci-recovery/clippy-before.log rc=101; check-rust-1.99.log rc=0; hash-probe.txt independently checked; bench/sha-rust-1.95.log rc=0. These are regenerable local evidence, not tracked artifacts.

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-08` | discovery | gh run list/view, current-path diff, toolchain versions | three failures remain; roots and priority owned above |

## Commit Log

`SEMULITH-CI-0003 (leaf CI-RECOVERY.3): repair cold portability execution and preserve failure evidence` — slice (a), big-endian confirmation pending.

`SEMULITH-CI-0002 (leaf CI-RECOVERY.2): provision authenticated mdBook and local Rust stores before the doctrine gate`.

`SEMULITH-CI-0001 (leaf CI-RECOVERY.1): repair strict Rust 1.99 lint without changing benchmark or hash results`.

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| discovery | included in LIVE-CONTAINMENT.4 slice (a) | owned before any CI code changes |

## Changelog

- `2026-10-08`: Created from the director's hosted-CI status question; four repairs scheduled.

- `2026-10-08`: `.1` active after archive commit `401956e`; repository clean at selection. Rust/map identity is owned before edits or toolchain provisioning.

- `2026-10-08`: `.2` active after clean d6693e5. Own scripts/install_ci_mdbook.sh and doctrines.yml before edits: pin verified official 0.5.4 assets for Ubuntu x86-64 and this native macOS verification host; install only into .app-data, cache under target, advertise PATH through GITHUB_PATH. Also set repository-derived CARGO_HOME/TMPDIR for the doctrine job and select Rust stable/wasm explicitly. Linux digest/layout checked; native cold installation, corruption refusal and UNIT-BOOKS controls will verify provisioning, with Linux execution reserved for the hosted run.

- `2026-10-08`: `.3` selected with clean d055dd9 before changes. Own
  check_portability.sh, its public-interface cold controls and portability.yml;
  additionally align rust.yml's stores with the same repository-derived provisioning
  contract. Pin nightly-2026-09-13 in the instrument, expose --print-toolchain to CI,
  matching the recorded rustc/Miri 809936eac6 (2026-09-12). The old workflow claimed a
  pin while installing floating nightly; this is a repository-owned reproducibility
  defect. Common output/Cargo/temp setup must precede every leg. Miri sysroots need
  explicit target-local storage: published https://github.com/rust-lang/miri documents
  MIRI_SYSROOT for both setup destination and test input. Use setup before tests with
  distinct native/endian sysroots, without global-cache migration or deletion.
  Priority: all these cold-run defects repaired now, with old-script RED controls and
  actual native/endian suites; full local/hosted follow-through remains `.4`.

- `.3` additional blocking root: actual dated Miri setup with repository-local TMPDIR
  rc=1: `current package believes it's in a workspace when it's not`, naming
  target/portability/tmp/.tmpruv5Pu/Cargo.toml and the root Cargo.toml. Parent workspace
  excludes vendor but not project-generated target workspaces. Own Cargo.toml now,
  before adding target to its exclusions; no modification to toolchain sources or
  temporary manifest internals. Verify membership unchanged and rerun actual setup.

- `.3` setup rerun after target exclusion reaches dependency resolution, then rc=1:
  `no matching package named cfg-if found`, directory source .app-data/vendor,
  required by std in the installed rust-src component. Local TMPDIR inherits the
  project's intentional crates.io replacement. Own synchronization of the toolchain's
  published Cargo manifest through public `cargo vendor --locked --sync` (documented
  https://doc.rust-lang.org/cargo/commands/cargo-vendor.html), alongside the root lock,
  before setup. Keep replacement strict, never fall back to a global cache or edit
  toolchain sources. Run store synchronization sequentially before either real leg.

- `.3` verdict defect discovered in the affected path and reproduced before repair:
  sourcing the parent's verdict function then calling `verdict green 'red (manifest
  mismatch)' green green` emits `passed`, rc=0. The full runner preserves decorated
  Rosetta outcomes, while verdict accepts only undecorated atoms; a mismatch is ignored.
  The single-leg x86 selector also rejects decorated green; its comparison uses the old
  frozen manifest rather than current native output. Own repairs now: normalize outcome
  prefixes, accept translated green in the single-leg selector and compare the same live
  guest set on both targets. Add independent public-interface translation controls;
  do not alter the dated historical portability record or claim native x86 hardware.

- `.3` verification invalidation: the first real native suite reached green, then Bash
  emitted `cho: command not found` and started reading different statements. Root:
  the live shell source was edited during its long run, so subsequent reads resumed at
  stale offsets. Stopped that exact script process tree; discard this run as evidence.
  All further long runs use an immutable same-volume script snapshot, byte-compared
  with the final working script before signoff. The log is retained in target/ only.

- `.3` owns failure-log visibility: real test/setup errors are redirected to target/portability logs. Print a bounded tail on a failed leg and attach only *.log files in CI, including on failure, so the next hosted failure is diagnosable without losing its cause.
