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
  Status: `done`
  Goal: create the output directory before redirections; remove the macOS-specific
  nightly name from the cross-endian target query; audit single-leg cold execution.
  Acceptance: hand stub controls on Linux/macOS shapes discriminate both old defects;
  the actual nightly/Miri result and any remaining provisioning gap are stated exactly.
  Verification: controls 9+15 green; immutable-snapshot native and big-endian Miri 153/153 each; full Rust 1.99 make ci green.
  Commit: SEMULITH-CI-0003 (slice a), SEMULITH-CI-0004 (confirmation/closure)

- ID: `CI-RECOVERY.4` — local/hosted evidence and follow-through
  Status: `active`
  Goal: run make ci after all repairs, record toolchain differences and omitted/absent
  legs honestly, and observe all workflows after the next cadence/approved push.
  Acceptance: no remote-green claim from local checks; failures owned until verified.
  Handoff subtask: own the observed Kimi reader census refusal before updating the
  resume pointer/book; resolve by director-led closure or an explicitly sanctioned
  exemption, then rerun the actual census. Never kill an unrelated editor or invent
  its exemption. This evidence-recording slice does not close the hosted obligation.
  Authorized next slice: record the director's 2026-10-08 approval of all pushes
  needed for this CI recovery, expiring when all three hosted workflows pass. Own
  the decision/index, COMMIT/MEMORY/book/log updates and any ordinary lossless head
  sharding required by their caps; then use approved_push.sh and observe exact-SHA
  hosted results. No hook bypass, cadence change or Kimi exemption is authorized.
  Push receipt slice: own the completed f4364bc push and three pending run IDs in
  MEMORY/logs/book before waiting. This tracking commit carries no new repair and
  does not claim the running hosted checks passed.
  Next repair ownership: doctrines run 37800113792 on f4364bc now fails at
  `GUEST-GEN: REFUSED — the check does not discriminate (self-test failed)`;
  mdBook provisioning itself passed. Own diagnosis through the public guest
  generator/check interfaces, preservation of the failed self-test output, and
  the evidence-backed fix in scripts/check_guest_gen.sh / scripts/gen_guests.py
  or the actual affected repository-owned dependency. No oracle or expectation
  weakening. Priority: blocking recovery; use the already approved next push.
  Diagnostic slice (d): local direct self-tests pass 103/103 on Python 3.14 and
  3.11, so hosted cause remains unidentified. Own a target-local self-test log in
  check_guest_gen.sh, its bounded failure tail, and failure-only artifact capture
  in doctrines.yml before edits. Verify a forced failure remains rc=2 and retains
  its diagnostic, then push this visibility repair; continue through the actual
  hosted root cause without claiming this diagnostic change repairs that cause.
  Root identified before the diagnostic push: a tracked-only cold fixture reproduces
  the parcel probe failure at named mtvec lookup. probe_gc_parcel_guest.py copies
  encoding/definitions into a temporary unit but omits state.sexp/profile.sexp;
  Assembler therefore falls back to absent target/refs/riscv-opcodes/csrs.csv.
  Own the fixture's metadata copy and explicit numeric address for the deliberately
  unmodeled mvendorid fixture before editing. Priority: fix now under `.4`, with cold
  baseline/mutations, native 103/103 and full CI before the already authorized push.
  Never provision an untracked oracle or change corpus expectations to hide this.
  Permanent guard: add --cold to the parcel probe, running its public default CLI
  from a temporary tracked-only source snapshot with no reference cache, and one
  GUEST-GEN GREEN arm for it. Own the updated derived control count and live/book
  mirrors before edits. Copy only regular project inputs; no Git repository is
  created and no external cache is changed. Existing eight mutation controls remain.
  Verification: pending
  Commit: pending

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `CI-RECOVERY.4` | `active` | recovery pushes approved; observe hosted workflows and resolve reader census |

## Decisions

- `2026-10-08`: director approves pushes needed to fix GitHub CI without asking
  again, until GitHub CI passes; then ordinary cadence resumes. Durable authority:
  docs/decisions/decision_ci-recovery-push-approval.md. Use the existing recorded
  approval act on every necessary repair push; no hook/cadence change. All three
  workflows must succeed on the repaired pushed SHA before retiring the exception.

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

- Handoff census at fc21b8f returns rc=1 for Kimi Code PID 1292. Targeted public
  lsof reports descriptors 55 and 59, both access mode `r`, on AGENTS.md; no other
  repository handles were reported for that PID. This establishes an open reader,
  not a project verification job or a claim about the app's other activity. The
  existing census intentionally counts every repository file handle. Ask the
  director to close Kimi or sanction its process per doctrine/sanctioned_processes.tsv
  before handoff; no exemption or process termination has been performed.

## Blockers

- Hosted result pending the authorized recorded push and exact-SHA workflow runs.
- doctrines run 37800113792 failed its GUEST-GEN self-test; inner output was
  suppressed by the wrapper. Tracked-only fixture reproduces missing CSR-state
  metadata in the parcel probe; fix and verify on GitHub before closure. Rust,
  both native portability hosts and manifest agreement already pass.
- The handoff census remains refused until Kimi closes or the director explicitly
  sanctions its process. Owned by `.4` with priority before handoff.

## Acceptance Checklist

`.4` cold-input repair slice (e), 2026-10-08, SEMULITH-CI-0009; hosted confirmation pending:

- [x] **ROOT CAUSE** — tracked-only parcel probe reaches named mtvec lookup and
  raises AsmError for absent target/refs/riscv-opcodes/csrs.csv. The temporary unit
  omitted its state/profile owners; Assembler's documented fallback hid this on
  the warm host. Removing metadata from the repaired cold control reproduces rc=1
  and mtvec; restoring external mvendorid spelling also gives rc=1 by name.
  Its numeric 0xf11 address is verified in pinned RVP-CSR's machine-info table
  (priv-csrs.html:1540–1556); primary SHA matches 330a17314ef803231955a915748176e5175fc773469f25a8c6b5ae922c9df425.
- [x] **ADDRESSED** — copy profile.sexp/state.sexp into the private full composition,
  use the explicit address for its unmodeled-CSR case, and run public --cold from
  a temporary tracked-only snapshot. No Git repo/external cache is created or changed.
  `GC parcel cold probe: tracked-only inputs and no reference cache passed`, rc=0
  on Python 3.14 and 3.11. Two regression controls above refuse rc=1; the permanent
  GUEST-GEN GREEN arm exercises the same cold CLI on every enforcer run.
- [x] **NO REGRESSION** — Rust 1.99 actual guest gate rc=0, stored
  `GUEST-GEN --self-test: 104 pass / 0 fail`; all prior eight parcel mutations remain.
  Both generated fixtures match; 42 owned texts byte-identical; 176 legacy steps
  retain their writes/counts. `git diff --name-only -- profiles definitions crates`
  is empty. `DERIVED-COUNTS: ok (5 derived count claim(s) re-derived)`; make book rc=0.
- [x] **FIX / LOCKSTEP** — probe/guard, LIVE_STATUS 600 controls, MEMORY/logs/book
  and this receipt. P4 remains 11/18, C unbound; 38 doctrines / 37 routes unchanged.
  Original cold root evidence is retained; a first negative harness attempt outside
  a Git root is invalid (empty inventory). Corrected controls supply the real tracked
  inventory through a public Git stub and assert actual CSR diagnoses, not any failure.
  promotion: declined (specific temporary-fixture repair; permanent cold control and scoped evidence preserve the lesson).

`.4` diagnostic slice (d), 2026-10-08, SEMULITH-CI-0008; actual hosted cause remains open:

- [x] **ROOT CAUSE (visibility)** — doctrines 37800113792 fails at GUEST-GEN;
  the committed wrapper runs `self_test >/dev/null 2>&1`, hiding the failing arm.
  Local direct self-tests: `GUEST-GEN --self-test: 103 pass / 0 fail` on both
  Python 3.14 and 3.11. These passes do not identify the Linux cause.
- [x] **ADDRESSED** — normal wrapper captures target/guest-gen/self-test.log,
  prints version/last 80 lines on failure and retains rc=2. Forced Python sentinel
  yields `GUEST-GEN --self-test: 3 pass / 100 fail`, the sentinel and REFUSED, rc=2;
  full log retained/copied, both st_dev equal repository. Failure-only upload path
  added to doctrines.yml; YAML parsed and bash -n rc=0.
- [x] **NO REGRESSION** — actual Rust 1.99 default guest gate rc=0; two fixture
  matches and base mirror 91 byte-identical / 7 re-derived. Stored controls remain
  `103 pass / 0 fail`; no guest/generator/engine change (implementation diff empty
  outside wrapper/workflow). make book rc=0; ordinary DEV_NOTES shard is lossless:
  `completeness: 38 entries before == 37 kept + 1 moved, order and bytes exact`;
  `SHARD-FREEZE: ok (216 shard row(s) frozen, 2 heads + shards append-only, exactly partitioned)`.
- [x] **FIX / LOCKSTEP** — shell/workflow, MEMORY/logs/book and this receipt;
  counters remain 38/599, P4 11/18. The next authorized push must expose and own
  the actual hosted failure. Current portability has advanced to cross-endian.
  promotion: declined (bounded failure-visibility repair; unresolved cause and reproducible controls retained here).

`.4` push-receipt slice (c), 2026-10-08, SEMULITH-CI-0007; leaf remains active:

- [x] **ROOT CAUSE** — hosted verification needed the committed repairs pushed.
  Actual recorded act exits rc=0; output `e1fe379..f4364bc main -> main` and
  `approved-push: pushed`. Director approval is the preceding durable decision.
- [x] **ADDRESSED** — act runs full local CI green before its ledger commit, then
  the normal pre-push hook reruns it green and verifies SEMULITH-PUSH-0001 covers
  the range. `git rev-list --count origin/main..HEAD` returns 0 at f4364bc.
- [x] **NO REGRESSION** — `gh run list --commit f4364bc316656b2d303f838bb87eadc470a75747`
  reports all three runs in_progress, with empty conclusions; no hosted pass is
  claimed. All tracked changes in this receipt are documentation, rc=0 for the
  implementation-path diff against f4364bc.
- [x] **FIX / LOCKSTEP** — MEMORY, CHANGELOG, this receipt and book preserve the
  exact SHA and run IDs below. P4 remains 11/18; CI-RECOVERY remains 3/4. The
  authorization remains active until actual all-three-green; Kimi remains pending.
  promotion: declined (session execution receipt; authority already owns its durable decision).

`.4` authority-recording slice (b), 2026-10-08, SEMULITH-CI-0006; leaf remains active:

- [x] **ROOT CAUSE** — director explicitly grants the needed CI-repair pushes and
  requires ordinary cadence after hosted success. `git rev-list --count origin/main..HEAD`
  returns 19 at 2f29664; previous remote remains e1fe379 with all three workflows failed.
- [x] **ADDRESSED** — verbatim authority and exact-SHA/all-three-green expiry recorded
  in decision_ci-recovery-push-approval; COMMIT, prior cadence decision, MEMORY/frontier
  and book aligned. `FRONTIER-SYNC: ok (33 tree(s) mirrored by docs/TASK_TREE.md)`;
  make book rc=0. Existing recorded approval act remains the execution path.
- [x] **NO REGRESSION** — `git diff --name-only -- .githooks scripts .github Cargo.toml
  Cargo.lock crates` is empty, rc=0. Normal sharder moves one old entry verbatim:
  `completeness: 74 entries before == 73 kept + 1 moved, order and bytes exact`;
  `SHARD-FREEZE: ok (215 shard row(s) frozen, 2 heads + shards append-only, exactly partitioned)`.
  The preserved entry separator becomes a blank line at head EOF; that is the sole
  default diff whitespace warning. All other whitespace checks pass with only
  blank-at-eof excluded. Neither cadence nor a tracked history byte is weakened.
- [x] **FIX / LOCKSTEP** — records/index, COMMIT, MEMORY/frontier, live logs and book;
  new ordinary shard/manifest retain authenticated archive union. P4 stays 11/18.
  Hosted verification and Kimi decision stay open; approval questions are not repeated.
  promotion: completed (director ruling in docs/decisions/decision_ci-recovery-push-approval.md).

`.4` evidence-recording slice (a), 2026-10-08, SEMULITH-CI-0005; leaf remains active:

- [x] **ROOT CAUSE** — actual unsandboxed handoff census rc=1 identifies Kimi PID
  1292; targeted lsof reports two read-only AGENTS.md handles. The documented
  property-based census counts these handles; no missing verification result remains.
- [x] **ADDRESSED (record only)** — own the approval/census resolution in `.4`,
  publish the measured modes and specific director decisions in Open Questions,
  and update the resume pointer and book. Questions requested; neither assumed.
  `FRONTIER-SYNC: ok (33 tree(s) mirrored by docs/TASK_TREE.md)`; make book rc=0.
- [x] **NO REGRESSION** — `git diff --name-only fc21b8f` contains documentation
  only; no workflow, Rust, census or exemption-registry change. The prior local CI
  and both Miri receipts apply to the unchanged implementation; hosted remains pending.
- [x] **FIX / LOCKSTEP** — docs/frontier, MEMORY, CHANGELOG, DEV_NOTES and book
  record the handoff boundary. No clean-handoff assertion while the census refuses.
  promotion: declined (session-specific handoff evidence; standing approval rules already govern the resolution).

The first hook refused this new record's ADDRESSED box because it omitted its tool
output. Added the actual frontier/book results inside that box; no checker change.

`.3` slice (b), 2026-10-08, SEMULITH-CI-0004 closes the parent:

- [x] **ROOT CAUSE** — the slice (a) causes and parent RED controls below remain the
  diagnosis; confirmation isolates host endianness after repairing setup/provisioning.
  `cmp scripts/check_portability.sh target/ci-recovery/portability-verified.sh` rc=0.
- [x] **ADDRESSED** — actual big-endian powerpc64 run: `cross-endian: green`, rc=0;
  `test result: ok. 153 passed; 0 failed; 0 ignored`, 1294.28 s. Native run above:
  153/153, rc=0. Distinct explicit sysroots under target/portability; no shared cache
  or source modification. The invalidated live-source run is excluded from both receipts.
- [x] **NO REGRESSION** — repository-local Rust 1.99.0 plus pinned mdBook 0.5.4:
  `make ci` rc=0 at c769d93, `ci: all legs green (check, gate, bench, smoke-bench, book)`.
  All mandatory local suite legs ran; current code/script bytes unchanged in this docs
  confirmation. Both Miri suites ran every core test, none ignored.
- [x] **FIX / LOCKSTEP** — close `.3`; index/MEMORY point at `.4`; CHANGELOG, DEV_NOTES
  and book record both actual results and full local CI. P4 stays 11/18, doctrine counts
  stay 38/599 and routes 37. Hosted results remain failed at e1fe379 until verified on
  a permitted push.
  promotion: declined (confirmation-only receipt; concrete outputs and pending hosted obligation retained here).


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

Confirmation slice (b) completed: target/ci-recovery/cross-real.log and
target/portability/cross.log preserve the actual 153/153 result; full-ci.log is green.
The immutable script snapshot remained byte-identical through both runs. The first live-source run was
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

Cold-input receipts under target/ci-recovery/: guest-cold-parcel-before.log has the
mtvec failure; guest-cold-parcel-after.log and guest-permanent-cold-green.log pass.
guest-cold-missing-metadata-red.log / guest-cold-external-csr-name-red.log each rc=1;
guest-cold-python311-green.log rc=0; guest-cold-fixed-green.log rc=0, 104/104.

Diagnostic checks: guest-forced-failure.log rc=2, guest-forced-selftest.log retains
full sentinel; guest-diagnostic-green.log rc=0, target/guest-gen/self-test.log
103/103. guest-selftest-python311-before.log is also 103/103. All under target/.

Approved act: target/ci-recovery/approved-push-1.log rc=0; both full-suite runs green.
Approval ledger commit: f4364bc316656b2d303f838bb87eadc470a75747, SEMULITH-PUSH-0001.
All three hosted runs started at 2026-10-08T15:21:39Z on that exact SHA; initially in_progress:

- rust: https://github.com/rdje/semulith/actions/runs/37800114021
- doctrines: https://github.com/rdje/semulith/actions/runs/37800113792
- portability: https://github.com/rdje/semulith/actions/runs/37800113741

`.1`: target/ci-recovery/clippy-before.log rc=101; check-rust-1.99.log rc=0; hash-probe.txt independently checked; bench/sha-rust-1.95.log rc=0. These are regenerable local evidence, not tracked artifacts.

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-08` | `.4` b | remote SHA/runs, frontier, freeze, book, implementation diff | approval scope recorded; 215 logical rows authenticated; hosted run next |
| `2026-10-08` | discovery | gh run list/view, current-path diff, toolchain versions | three failures remain; roots and priority owned above |

## Commit Log

`SEMULITH-CI-0009 (leaf CI-RECOVERY.4): make parcel author controls independent of warm CSR reference data` — local cold reproduction/fix; hosted next.

`SEMULITH-CI-0008 (leaf CI-RECOVERY.4): preserve failed guest self-test diagnostics on GitHub` — visibility fixed, underlying hosted cause still open.

`SEMULITH-CI-0007 (leaf CI-RECOVERY.4): preserve the authorized push and pending hosted run receipts` — running hosted checks remain owned.

`SEMULITH-CI-0006 (leaf CI-RECOVERY.4): record bounded approval for necessary GitHub CI repair pushes` — authority slice, hosted result still pending.

`SEMULITH-CI-0005 (leaf CI-RECOVERY.4): record the reader census blocker before hosted verification` — evidence recording only, both director decisions pending.

`SEMULITH-CI-0004 (leaf CI-RECOVERY.3): confirm both Miri targets and the full Rust 1.99 local CI suite`.

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
