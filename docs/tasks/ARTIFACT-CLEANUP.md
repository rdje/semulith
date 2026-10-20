# ARTIFACT-CLEANUP: generated artifacts never outlive their usefulness

## Metadata

- Tree ID: `ARTIFACT-CLEANUP`
- Status: `active`
- Roadmap lane: cross-cutting maintenance; session-directive §8 (cleanup ~every 24 h, tracked in `docs/ARTIFACT_CLEANUP.md`)
- Gate: ARTIFACT-COHORT checks bounded planning; actual cleanup still requires its separately recorded census/preflight workflow
- Created: `2026-09-26`
- Owner: repo-local workflow

## Goal

Keep generated artifacts from accumulating across sessions: roughly every 24 hours, census the
repository's artifact locations, delete only what is 100% safe (provably regenerable outputs, never
inputs), and record the run in `docs/ARTIFACT_CLEANUP.md` so the next session knows when the last
cleanup happened and what it removed.

## Non-Goals

- **Never tracked content.** Anything git tracks is out of scope by construction.
- **Never inputs, only outputs.** Dependency source data (crate test fixtures under
  `.app-data/cargo-home/`), the `.materials/` fetch cache (network-expensive to rebuild), and
  `vendor/` are inputs or caches of inputs — deleting any of them is not "cleanup", it is damage.
- **Not a space reclamation project.** The point is housekeeping and a verified procedure, not
  megabytes; a 1.3 MB regenerable evidence log can be worth more than the space it costs.

## Acceptance Criteria

1. A dated census (counts and bytes by directory) exists before any deletion, and the after-state
   is measured, not asserted.
2. Only items in the session-directive's enumerated safe scope — cargo incremental caches and
   stray `.bin`/`.log` in `target/release`, `target/debug/incremental`, `target/debug/deps` (and
   the same under the prescribed `.app-data/` build home) — are deleted, unless a later leaf
   extends the scope with per-class evidence.
3. `docs/ARTIFACT_CLEANUP.md` is overwritten with the date and a one-line summary each run; it
   never accumulates history.
4. The doctrine enforcer is green after every cleanup commit.

## Task Tree

- ID: `ARTIFACT-CLEANUP`
  Status: `active`
  Goal: bounded, evidenced artifact cleanup on a ~24 h cadence
  Children: `ARTIFACT-CLEANUP.1`, `ARTIFACT-CLEANUP.2`, `ARTIFACT-CLEANUP.3`, `ARTIFACT-CLEANUP.4`, `ARTIFACT-CLEANUP.5`, `ARTIFACT-CLEANUP.6`, `ARTIFACT-CLEANUP.7`, `ARTIFACT-CLEANUP.8`, `ARTIFACT-CLEANUP.9`, `ARTIFACT-CLEANUP.10`, `ARTIFACT-CLEANUP.11`, `ARTIFACT-CLEANUP.12`, `ARTIFACT-CLEANUP.13`, `ARTIFACT-CLEANUP.14`, `ARTIFACT-CLEANUP.15`, `ARTIFACT-CLEANUP.16`, `ARTIFACT-CLEANUP.17`

- ID: `ARTIFACT-CLEANUP.1` — **the first cleanup, the record, and the registry row**
  Status: `done`
  Goal: run the first §8 cleanup; create `docs/ARTIFACT_CLEANUP.md` (overwrite-only record);
  register the record as a governed live surface in `doctrine/readme_routes.tsv` in the same
  commit that creates it.
  Acceptance: census recorded in this leaf; only cargo incremental `.bin` caches deleted (40
  files expected from the pre-change census); record carries the date and a one-line summary;
  registry row added; `git status` clean apart from intended files; `check_doctrines.sh` green.
  Verification: `2026-09-26` — census, classification, post-delete re-census, gate; all in the
  Verification Log below.
  Commit: `SEMULITH-AC-0050`

- ID: `ARTIFACT-CLEANUP.2` — **the sanctioned-watcher exemption, data-owned**
  Status: `done`
  Goal: the director ruled (`2026-09-27`) that CHIPDOC's ChipdocWatcher — which holds an open
  handle on `materials/catalog.sexp` by design — "will stay there. It shouldn't bother you. Do
  not worry about it from now on." Encode the ruling so the handoff census stops crying wolf:
  a sanctioned-exemptions registry the check reads as data, with the detection itself untouched
  (the pattern-free census stays; only director-ruled standing processes are exempt).
  Acceptance: `check_no_background_jobs.sh` prints `handoff: OK` with the watcher running; the
  discrimination control shows the same process flags the moment its row is absent; an agent
  may propose a row but only the director's ruling lands one.
  Design (recorded before code, `2026-09-27`): the census header refutes list-matching as
  DETECTION ("a census built from a list of things you thought of cannot see the thing you did
  not") — so the exemption is shaped as a RULING, not a vocabulary: `doctrine/sanctioned_processes.tsv`
  carries executable-substring / ruling / date; the check excludes matching command lines from
  both arms (a sanctioned watcher holds repo handles AND names repo paths by design); the
  header records why a sanctioned list is principled where a detection list is not (auditable,
  reversible, director-owned). Tracked-content gates are unaffected — the exemption covers the
  handoff census only.
  Verification: `2026-09-27` — the real check prints `handoff: OK` with PID 36462 alive; the
  control probe (row absent) flags the same process again. Both directions in the log below.
  Commit: `SEMILITH-AC-0051`
  `promotion: declined (the propose-vs-dispose discipline is stated in the registry header).`

- ID: `ARTIFACT-CLEANUP.3` — **the 2026-10-08 recurring cleanup**
  Status: `done` (`2026-10-08`, `SEMULITH-AC-0060`)
  Goal: remove only untracked cargo incremental `.bin` outputs; retain dependency fixtures
  and diagnostic/reference evidence logs. The 2026-10-06 record is more than 24 hours old.
  Acceptance: a before/after count and byte census, no tracked-file deletion, updated latest
  record, green doctrine gate, committed handoff before resuming `P4-SYSTEM.12`.
  Pre-delete census: Python `Path.rglob` over `target` and `.app-data`, excluding symlinks,
  checked against `git ls-files -z`: 84 files / 295,197,153 B in
  `target/debug/incremental`; 18 / 68,850,571 B in the wasm32 incremental directory;
  no incremental bins under `.app-data`. No stray bins/logs in `target/release` or
  `target/debug/deps`. Retain 126 diagnostic logs (1,130,473 B), 62 reference logs
  (2,096,498 B), and seven dependency-source fixtures (1,056 B).

- ID: `ARTIFACT-CLEANUP.4` — **the 2026-10-09 recurring cleanup**
  Status: `done` (`2026-10-09`, `SEMULITH-AC-0061`)
  Goal: census and remove only untracked cargo incremental `.bin` outputs after the
  dated 2026-10-08 run; preserve reference/diagnostic logs and dependency inputs.
  Acceptance: enumerate counts/bytes and tracked/symlink exclusions before deletion;
  remove exactly the reviewed candidates, prove residue zero, overwrite the latest
  record, pass the doctrine gate and commit before returning to `P4-SYSTEM.12`.

- ID: `ARTIFACT-CLEANUP.5` — **the 2026-10-10 recurring cleanup**
  Status: `done` (`2026-10-10`, `SEMULITH-AC-0062`)
  Goal: the prior run is2026-10-09 17:21:23UTC; perform this recurring run at
  approximately24hours, on clean214a524 with brief0/actual census rc=0. Read
  standing safe-scope/exclusions, current artifact record and book task-tree
  workflow before changes. Census target/.app-data with no symlink traversal
  or nested repository inspection; select only project-local untracked cargo
  incremental .bin outputs. Preserve diagnostic/reference logs, crate-source
  fixtures, all dependency inputs and tracked files. Save path/count/byte/hash
  identities before deletion, revalidate all candidates, delete exactly them,
  then prove selected residue0 and retained inputs/evidence hashes exact.
  Acceptance: before/after evidence, overwrite-only latest record, task/index/
  live/book synchronization, focused doc gates/six books and committed clean
  handoff before P4-SYSTEM.14 a7. No running build during deletion.
  Evidence: target/artifact-cleanup-0062; all scratch on repository volume.

Result: completed2026-10-10T17:22:34.381524+00:00; exact saved204paths/978509475B
revalidated by size/device/inode/mtime/SHA and all-candidate safety preflight,
then unlinked. Twelve cargo incremental roots (84debug/18wasm and102scratch);
repeat census and every saved path show residue0. Release/deps stray bins/logs0.
Retain6192diagnostic logs/7913221B,62reference logs/2097132B and7dependency
source fixtures/1056B:6261files/10011409B, all SHA/bytes exact. Both target and
.app-data are real directories on the repository device; skip symlinks and
three nested repositories, no writes across any Git/volume boundary. Actual
pre-delete process census rc=0/handoff: OK; no active build. Latest record
has one entry. Focused9/six books/verify rc=0; all code/profile/catalog/frozen/
registry/history/LIVE exact. P4 13/18/CPU incomplete7axes unchanged.
promotion: declined (standing safe-scope procedure and measured exclusions remain in this recurring tree).
Next P4-SYSTEM.14 a7/0198, canonical reference rows and their generated consequences.

- ID: `ARTIFACT-CLEANUP.6` — **the 2026-10-11 recurring cleanup**
  Status: `done` (`2026-10-11`, `SEMULITH-AC-0063`)
  Goal: prior run2026-10-10T17:22:34.381524+00:00 is over24h old. Owned
  after clean b335c74, all14 committed hashes/modes/brief0 verified, full hooks
  green and unrestricted repaired handoff census rc=0. Finish/commit before
  returning to P4; no running build or other project-owned job during deletion.
  Read standing exclusions, prior .5 procedure/helpers, latest record and current
  book before this ownership. Select only untracked known cargo incremental
  dep-graph/query-cache/work-products .bin outputs on this repository device.
  Walk target/.app-data without symlink or nested-Git traversal; retain every
  diagnostic/reference log, dependency fixture/input and unknown stray class.
  Save relative-path/count/size/device/inode/mtime/SHA identities and retained
  hashes before deletion; revalidate the complete cohort before unlinking any.
  Explicit runtime conditions survive Python optimization. Re-census immediately
  after deletion: exact saved paths absent, selected residue0, retained hashes
  and counts unchanged. Later builds may regenerate caches and verification
  may update diagnostic logs; cleanup claims refer to this measured event.
  Own all cleanup scratch under target/artifact-cleanup-0063. No other Git repo
  or submodule implementation writes/inspection. All tracked code/data/modes/
  Gitlinks stay exact, apart from owned live/task/book/history documentation.
  Overwrite the single latest record, including a named include anchor, and
  include it directly in current book cleanup teaching; keep the same rules,
  shrink source within fixed caps. Book normal/print must show the exact latest
  receipt. Own tree/index/MEM/DEV/CH sync, whole-oldest sharding if necessary,
  complete predecessor task/head/source inverses, history/scope checks, focused
  documentation gates, seven books/fresh+actual navigation and full COMMIT.
  Also own durable logging of the observed scaffold-copy risk in P4's proposed
  priority1 a42j: the public updater still lists the locally repaired census as
  replaceable. No implementation pivot here; bounded public reproduction and
  retention fix follow this cleanup, then ordinary-part guard assessment.
  promotion: declined (existing safe-output/ownership/history/containment rules).
  Evidence: target/artifact-cleanup-0063. No full CI or push for this housekeeping.

  Final verification: focused.sh rc=0,12gates/sharder12/seven books;3212fresh+
  actual hyperlinks and exact latest normal/print receipt. history.py/verify.py
  rc=0 normal/O; all100old entries and full heads/task/index/book inverses exact,
  1372other files bytes/modes and Gitlinks unchanged. Book -51B, family524225/
  524288; task family95files/2326192B, largest127265; all fixed caps unchanged.
  Whole oldest DEV1817B/one entry to0272 (2050B/SHA256
  90852c46b07d4bcfd9ec81bae7c51be31b3f67a0356ee9680017fd6a88fb0803);
  CH690B/one to0273 (927B/SHA256
  ae8e00998430260ba84a69b5ab02e287b19ac4bacf8a4d84cb8e6251c647783a).
  65live+210sealed275logical shards; original/published/moved receipt edits
  with updated digests jointly refuse, permanent guards retained.
  Result: completed2026-10-11T18:24:49.098493+00:00. Exact24 untracked caches/
  155683881B removed: target/debug/incremental6/78086999B; C-engine6/46660980B;
  C-guest-image12/30935902B. All-candidate preflight then each saved relative
  path/device/inode/size/mtime/SHA rechecked before unlink. Immediate selected
  residue0, all9225retained files/128863947B byte/hash-exact:9156diagnostic logs/
  126765759B,62reference logs/2097132B,7source bins/1056B. No release/deps strays;
  four nested Git roots skipped, no symlink traversal or foreign-volume writes.
  Explicit conditions hold normal/O; changed candidate SHA and plan totals
  each refuse before deletion in both modes. Actual unrestricted pre-delete
  census rc=0/handoff: OK. Diagnostics remain evidence, including six large
  reserve/debit negative-control logs; later gates may rewrite diagnostic logs
  or regenerate caches, so this receipt describes the immediate cleanup event.
  Latest one-entry record included in book normal/print; book source shrinks.
  Focused12/sharder12/seven books, history/source/scope checks and full COMMIT
  verify the unit; detailed receipts below. No Rust/CPU/canonical/LIVE change.
  Next P4-SYSTEM.14 a42j/0245, bounded scaffold-retention reproduction/repair.

- ID: `ARTIFACT-CLEANUP.7` — **the 2026-10-16 recurring cleanup**
  Status: `done` (`2026-10-16`, `SEMULITH-AC-0064`)
  Goal: latest run2026-10-11T18:24:49Z is over24h old. Begin from clean
  d3d2904 after LC0038 normal hooks, exact committed bytes/modes/brief0 and
  unrestricted handoff census rc=0. Finish this maintenance commit before
  LC0039 D77 repair; no build or other project-owned job during deletion.
  Apply the standing .6 safe-cohort procedure: census target/.app-data without
  symlink, nested-Git or foreign-device traversal; delete only untracked known
  Cargo incremental dep-graph/query-cache/work-products .bin outputs. Retain
  every diagnostic/reference log, qualification capture, dependency fixture,
  source/input and unknown stray class. Save complete relative path, bytes,
  device/inode/mtime/SHA identities; preflight the entire cohort and retained
  data before any unlink, recheck each candidate immediately, then re-census
  for selected residue0 and exact retained counts/bytes/hashes. Conditions must
  survive Python optimization; damaged identity/totals must refuse pre-delete.
  Own scratch at target/artifact-cleanup-0064, latest single-entry record,
  tree/index/MEM/CH/DEV and whole-oldest history sharding if needed. The existing
  named latest-record include must show the exact new receipt in normal/print
  book output; no book source growth, fixed capacities unchanged. Preserve all
  original task/index/head bytes through explicit inverses, every unrelated
  tracked identity/mode and opaque Gitlink. Run focused12/sharder12/seven books,
  history/source/cap/rendered checks, normal COMMIT and unrestricted host census.
  Later gates can regenerate caches/update diagnostic logs; cleanup receipts
  describe the immediate measured event. No CPU/LIVE/adoption change or push.
  promotion: declined (standing safe-output/ownership/history rules).

  Result: cleanup.py --plan/--check/--delete rc=0: completed
  2026-10-16T21:24:43.629148+00:00;18saved paths/77596881B removed,
  selected residue0 immediately. Six C-engine caches/46660983B and twelve
  C-guest-image caches/30935898B; all10701retained files/131474223B exact
  bytes/SHA. Four nested Git roots skipped, release/deps strays0; no symlink,
  foreign-volume, tracked-input or other-repository deletion. Complete cohort
  identity preflight followed by each saved path/device/inode/mtime/size/SHA
  recheck before unlink. Actual unrestricted pre-delete census rc=0/handoff: OK.
  Changed candidate SHA and changed totals each refuse before deletion normal/O.
  External README/containment policy package still matches reviewed21f4d3d;
  claim-verification source SHA9f99df25 remains the locally imported body.
  Existing book latest-record include carries this event; original teaching
  and all unrelated code/data/modes/Gitlinks remain unchanged. Focused12,
  sharder12/seven books, exact normal/print receipt, whole history/source/cap
  verification and normal COMMIT close the unit. Next LC0039 D77 repair.

- ID: `ARTIFACT-CLEANUP.8` — **the 2026-10-17 recurring cleanup**
  Status: `done` (`2026-10-17`, `SEMULITH-AC-0065`)
  Goal: latest2026-10-16T21:24:43Z is over24h old. Own from clean cb39c69,
  LC0048 normal hooks/brief0 verified, before cleanup scratch or deletion.
  Use the existing .7 safe-cohort helper with only its owned output root changed
  to target/artifact-cleanup-0065. Census target/.app-data without symlink,
  nested-Git or foreign-device traversal. Delete only untracked known Cargo
  incremental dep-graph/query-cache/work-products bins, after complete saved
  path/device/inode/mtime/size/SHA and retained-data preflight. Recheck each
  candidate immediately before unlink; prove immediate residue0 and retained
  count/bytes/SHA exact. Preserve every diagnostic/reference log, dependency
  fixture/input, native capture and unknown stray class. No source/cache-input
  deletion or other-repository write. Test damaged identity/totals normal/O.
  Run host census before deletion and verify no active build or cache handle.
  LC0047's known app reads AGENTS.md only; if still present, record its separate
  handoff blocker without terminating/exempting it. Read-only app handles cannot
  use the selected incremental caches; do not misreport handoff as green.
  Own LC0047 app-release witness in LIVE-CONTAINMENT, overwrite-only latest
  receipt, book's existing direct include, tree/index/
  MEM/CH/DEV sync and whole-oldest sharding if needed. Preserve all predecessor
  source/history/modes/Gitlinks and fixed caps; focused gates/seven books,
  rendered receipt/inverses and normal COMMIT before returning to terminal D79
  capture. No Rust behavior, LIVE_STATUS, full CI or push change.
  promotion: declined (standing safe-output/locality/ownership contracts).

  Result: completed2026-10-17T22:50:22Z;18saved caches/77596894B removed,
  immediate selected residue0. Six C-engine caches/46660990B and twelve
  C-guest-image caches/30935904B. All14220retained files/131741041B size/SHA
  exact; four nested Git roots skipped, release/deps strays0. Whole-cohort and
  per-path identities revalidated before unlink; no tracked/input deletion.
  Four damaged identity/totals controls refuse normal/O; both complete positive
  preflights pass. An early census correctly refused while this slice's check
  child still ran; after all checks joined, repeated actual census rc=0/handoff:
  OK preceded deletion. No permission/exemption or other-app termination.
  LC0047 app handles are no longer observed after cb39c69; record this release
  witness in LIVE-CONTAINMENT and clear the stale resume blocker. This is an
  observed census boundary, not a claim about the app's internal state.
  External policy source hashes remain unchanged since the reviewed .7 check;
  claim-verification source still matches the exact imported body. The existing
  book include renders the latest receipt normal/print; source teaching stays
  byte-exact. Focused13/seven books/source/history checks and normal COMMIT
  qualify this housekeeping. Later hooks may regenerate caches or update logs;
  this receipt describes the immediate measured event. LIVE_STATUS unchanged.

- ID: `ARTIFACT-CLEANUP.9` — **the 2026-10-18 UTC recurring cleanup**
  Status: `done` (`2026-10-18` UTC, `SEMULITH-AC-0066`)
  Goal: latest2026-10-17T22:50:22Z is over24h old. Begin from clean9274231,
  completed P4-0269 with exact message/files/brief0 and actual host census OK.
  Use the standing .8 safe-cohort helper with only its owned output root changed
  to target/artifact-cleanup-0066. Census target/.app-data without symlink,
  nested-Git or foreign-volume traversal; remove only known untracked Cargo
  incremental dep-graph/query-cache/work-products bins. Preserve all inputs,
  source fixtures, diagnostics/reference/capture evidence and unknown classes.
  Save/revalidate whole-cohort and per-file identities/hashes, test damaged
  identity/totals refusals normal/O, join every check, then require an actual
  green pre-delete census. Delete exactly the saved cohort, prove immediate
  residue0 and retained byte/hash equality. Own latest single-entry receipt,
  task/index/MEM/CH/DEV sync, whole-entry sharding if needed, existing book
  direct-include rendering, focused checks/seven books and normal COMMIT.
  Fixed caps/LIVE/CPU/code/opaque Gitlinks unchanged; no full CI or push.
  Return to P4-SYSTEM.14 shared read allowance, then final canonical driver.
  promotion: declined (standing safe-cohort/locality/history contracts).

  Result: completed2026-10-18T23:00:27.051789Z. Exactly177 caches/674371444B
  removed after complete cohort/per-path identity+SHA preflight and actual host
  census OK; selected residue0 immediately. Retained16764files/145405416B exact
  bytes/SHA; four nested Git roots skipped,0strays, no input or tracked deletion.
  Normal/O positive preflights green; four damaged identity/totals checks refuse
  before deletion. Counts come from the saved plan/result; a preliminary progress
  misstatement was corrected before deletion. Later gates may regenerate caches
  or update diagnostics; this receipt describes the immediate measured event.
  Latest one-entry record is included directly in the book; source stays exact.
  Focused13/seven books and verify.py normal/O pass:1545other files/1Gitlink/
  92old entries exact, full task/index/head inverses, latest normal/print receipt.
  Fixed caps/LIVE/book teaching unchanged; normal COMMIT closes the unit;
  resume P4-SYSTEM.14 shared manifest/evaluation allowance before canonical driver.

- ID: `ARTIFACT-CLEANUP.10` — **the 2026-10-19 UTC recurring cleanup**
  Status: `done` (`2026-10-19` UTC, `SEMULITH-AC-0067`)
  Goal: prior2026-10-18T23:00:27Z is over24h old. Own from clean59e210a,
  P4-0283 normal hooks/exact20 files/brief0/actual host census verified.
  Read standing scope, .9 helper, task/book/latest record before this ownership.
  Reuse .9 helper with only owned output root target/artifact-cleanup-0067.
  Census target/.app-data without following symlinks, nested Git roots or other
  devices. Delete only known untracked Cargo incremental dep-graph/query-cache/
  work-products bins. Preserve every input, source fixture, retained capture,
  reference/diagnostic log and unknown class. Save path/device/inode/mtime/size/
  SHA identities and complete retained counts/hashes; require whole-cohort and
  per-path preflight, six normal/O positive/damaged checks and joined jobs plus
  actual pre-delete host census before unlink. Prove immediate residue0 and
  retained count/bytes/hash equality; later gates may regenerate/update outputs.
  Own latest one-entry receipt, tree/index/MEM/DEV/CH, existing book direct
  include/rendering, whole-history/source inverses, focused checks/seven books
  and normal COMMIT. Keep every fixed cap, unrelated code/data/mode/Gitlink and
  LIVE/CPU/board/replay state. No other repository write or full CI/push.
  Return to P4-SYSTEM.14 full source/risk/feature policy and status integration;
  preserve original capture. Promotion declined: existing safe-cohort doctrine.

  Result: completed2026-10-19T23:07:45.637459Z; exactly18 saved caches/78250724B removed.
  Six normal/O preflights: four damaged identity/totals plans refuse before
  deletion; both intact plans pass. Exact original plan restored, all jobs joined
  and actual pre-delete host census OK before whole-cohort/per-path revalidation.
  Immediate selected residue0;18121 retained files/152718645B size/SHA exact.
  Four nested Git roots skipped/0strays; no tracked/input or other-volume write.
  QA: early controls ran before plan completion and refused missing plan; join
  census before restart, no deletion then. Prior helper is byte-exact apart from
  owned output root. Latest normal/print receipt and focused13/seven books/source-history proof pass.
  Later builds may regenerate caches/update logs; this is the immediate event.

### Priority1 activity — make cleanup instruments durable
  Status: `active`
  Children: `ARTIFACT-CLEANUP.11`, `ARTIFACT-CLEANUP.12`, `ARTIFACT-CLEANUP.13`, `ARTIFACT-CLEANUP.14`, `ARTIFACT-CLEANUP.15`, `ARTIFACT-CLEANUP.16`, `ARTIFACT-CLEANUP.17`
  Goal: fix the verified workflow defect before returning to P4 policy/status.
  Reproduce: git ls-files --error-unmatch target/artifact-cleanup-0067/cleanup.py
  rc=1; tracked scripts/*cleanup* census empty; cache-name search in scripts/
  .githooks/docs/toolbox has no canonical implementation. The reused5815B helper
  SHA0396e669f9b798f010dcbe67b5f3462497afbcff478d353c7d989b9b2bd307e9
  and its normal/O controls live only in ignored target. Fresh checkout cannot
  execute the documented protocol. Root cause: recurring scratch copies were
  reused without promoting first-class instruments under TOOLBOX.md lines13/31.
  Own from clean568234a, AC0067 exact8 files/normal hooks/brief0/actual census OK.
  Read public cleanup/task/claim/locality/book/toolbox/gate interfaces before code.
  Add a tracked bounded same-volume safe-cohort tool and fixture controls; retain
  complete cohort/per-file preflight, no symlink/nested-Git/foreign-device walks,
  untracked known Cargo incremental class only, and unknown/input preservation.
  Malformed/stale plans must refuse before deletion; preserve distinct failures
  and measured partial outcomes. Separate read-only planning/checking from an
  explicit delete action. Tests use owned on-volume fixtures; no new real cleanup
  event is needed. Register public usage/toolbox/book and appropriate focused/CI
  checks, normal/O discriminating controls and cold copied-runtime validation.
  Preserve old event/receipts: AC0067 was run with its original helper, not a later
  implementation. Keep producer37/native3/canonical capture/statuses/fixed caps
  exact; no submodule or other-repository write. Own all activity under
  target/artifact-cleanup-0068, scope/history/retention/live docs and normal COMMIT.
  Split safe subunits if interface review requires it, commit each before next.
  promotion: declined (existing tools-first/reproducibility policy; repairs adoption).

  Owned defect D1 (reproduced2026-10-20): legacy release incremental caches
  are both selected and stray. reproduce-release.py rc=0: one owned fixture
  selected=stray=1; --delete unlinks it, then raises post-delete census differs,
  with no result receipt. safe() admits release/incremental, while census()
  records every release descendant as stray; the post-check expects that list
  unchanged. Fix classification disjointness and preserve explicit partial
  outcomes. Actual AC0067 contained only debug caches; its event stays unchanged.

- ID: `ARTIFACT-CLEANUP.11` — **tracked bounded planning and checking**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0068`)
  Goal: AC0068 first safe slice: scripts/artifact_cleanup.py read-only cache
  planning/checking plus an owned plan output, tracked fixture probe and gate.
  Explicit bounded counts/bytes/depth/path/JSON/Git reads; one repository volume,
  descriptor traversal, no symlink or nested-Git inspection; complete tracked-file
  inventory from public Git with exact runtime-root match, no parent fallback.
  Snapshot file identities/digests and disjoint selected/retained populations;
  release-cache D1 must discriminate. Strict immutable plan decoding and source
  identity, pre/post-state checking, exclusive repository-relative plan output.
  No cache deletion API or command in this slice. CI uses on-volume owned fixtures
  only; normal/O positives/guard omissions/cold copied CLI. Register one focused
  artifact-cohort gate, toolbox and shared book/CLI teaching; derive live counts.
  Preserve all old producer/capture bytes and original task/history/caps; normal
  COMMIT before .12. Output target/artifact-cleanup-0068, no real cleanup event.
  Public task_source.py accepts direct numeric leaves only; initial .11.1/.11.2
  refused foreign leaf before judgment. Use direct .11/.12 without weakening it.
  Owned D2: volume-open-before.log rc=0 measured one unnecessary directory open
  for a declared simulated foreign-device scope, before identity refusal. WHERE:
  OwnedRoot.directory checks device only after os.open/fstat. Repair .11 now:
  reject before.st_dev before opening, retain after-open race/identity checks;
  add a discriminating copied-fixture control. No real foreign data was read.
  Stopped only this pending commit and its descendants before publication,
  terminal143; HEAD remains568234a. Reverify current leaf before normal COMMIT.
  Fixed:26 tests normal/O pass; all22 outcomes exact. Each device-order guard
  omission loses one assertion/0 errors. Positive fixtures perform no foreign
  directory open or public query; retain later race/device checks too.
  Same D2 at public Git: git-volume-before.log rc=0 measured one metadata
  query despite a known foreign-device .git marker. Add marker-device check
  before public Git queries; preserve later indirect metadata-path validation.
  Own the additional copied fixture and guard omission in this same leaf.
  Final source-bound real narrow plan/check:6 candidates/46717788B matched;
  all six file facts are exact from the earlier default-cohort observation.

- ID: `ARTIFACT-CLEANUP.12` — **retain and replay the historical cleanup instrument**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0069`)
  Goal: AC0069 from clean847be8c/brief0/host census OK. Retain the original5815B
  AC0067 helper byte-exact as passive input under scripts/; authenticate
  SHA0396e669f9b798f010dcbe67b5f3462497afbcff478d353c7d989b9b2bd307e9.
  Track a bounded descriptor reader and replay copies only in newly owned
  on-volume fixtures, mocking only public Git root/inventory reads. Reproduce
  successful debug cleanup and release-D1 deletion/failed post-check/no receipt.
  No real project cache deletion or new event. Normal/O pin/shape/locality
  refusals and cold copied CLI from valid parent cwd; focused gate and truthful
  book/help. Partition artifact toolbox rows without loss or raised ceilings.
  Preserve native3/producer37/capture, old events and complete source/history.
  Normal COMMIT before .13; output target/artifact-cleanup-0069.
  promotion: declined (repairs existing first-class-tools/claim policy).

- ID: `ARTIFACT-CLEANUP.13` — **bounded recoverable attempt journal**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0070`)
  Goal: AC0070 from clean e9b4532/brief0/actual host census OK. Establish a bounded
  one-shot intent/outcome journal before connecting any cache mutation. Bind the
  published immutable plan and current recorder/actor source identities; anchored
  same-volume/non-Git exclusive creation and per-append parent/file validation.
  Canonical closed framed records, bounded counts/bytes, durable intents before
  reported unlink returns, explicit terminal status, and no overwrite/reuse.
  Reader retains partial-prefix/pending-intent uncertainty, rejects corruption
  and reports recorded observations only; no current-state or actor attestation.
  Cover torn/failed writes, fsync/close failures, source/plan/path changes and
  both modes/cold CLI in owned on-volume fixtures. No cache unlink API or actual
  cleanup event in this slice. Sync focused gate/toolbox/shared book/live docs,
  preserve original source/history/caps, normal COMMIT before .15 core/.14 CLI.
  Output target/artifact-cleanup-0070.
  Owned durability finding: Apple fsync(2) documents drive-buffer loss/reordering
  after ordinary fsync on power failure. Normal file/directory fsync succeeds on
  owned fixtures; F_FULLFSYNC succeeds for write/read file descriptors too.
  Add ordered plan/journal/parent synchronization and Darwin F_FULLFSYNC, refuse
  unsupported/failed barriers. Do not claim hardware/power-failure attestation.
  Evidence fullsync.json; primary Apple manual linked in shared usage.
  Book capacity: move only the complete cleanup teaching fragment into the
  bounded artifact-toolbox part, rebase its two includes explicitly, and include
  that anchor from the book. Preserve whole text/examples; add journal teaching
  there through its shared CLI usage. No cap increase or unbounded neighbor.
  promotion: declined (implements existing durable-source/partial-outcome policy).

- ID: `ARTIFACT-CLEANUP.14` — **bind host census and publish operator workflow**
  Status: `pending`
  Goal: after .16 guarded core, bind explicit caller quiescence and a fresh bounded
  invocation of the public host-census workflow before cache mutation. Preserve
  UID, exemptions and observation limits; census remains outside the doctrine.
  Add supported delete/inspect CLI, truthful partial/error outcomes and recovery
  examples. Test failed/unavailable process/identity observations, interruption
  and cold copied runtime in owned fixtures; no real cleanup event needed.
  Sync help/book/toolbox/live docs, focused checks and normal COMMIT; close the
  priority1 durable-instrument activity, then return to full P4 policy/status.

- ID: `ARTIFACT-CLEANUP.15` — **bounded per-file output-provenance records**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0071`)
  Goal: AC0071 from clean7f732ab/brief0/host census OK. Establish closed bounded
  per-file output-provenance records/reader first: successful public build,
  recorder/producer source pins, exact before/after facts, fixed output roots.
  Unknown or unchanged unowned input cannot gain authority from cache names.
  Fresh anchored current-source/file matching reports only recorded generation;
  no loaded-code attestation. Cover malformed/stale/forged-scope/alias/source
  refusals and normal/O omissions in owned copies. No mutation API or planner
  reclassification yet: .17 binds actual builds and selection; .16 core/.14 CLI
  follow. Preserve historical plans/journals, producer37/native3/capture/caps.
  Sync gate/toolbox/shared teaching/live records; normal COMMIT per slice.
  Output target/artifact-cleanup-0071; P1 stays open until .17 integration verified.
  Owned D3: root-mapping-before.log23 tests/1 failure/0 errors shows a renamed
  fixture root can borrow its old descriptor. WHERE load() compared only path
  spelling. Add pathname/device/inode guards before/after reads and return;
  restore fixture mapping before close. No real project path was renamed.
  QA D4: task-root-before.json finds lost old nodes after a leaf-local offset
  was reused for the document prefix. Restore the saved predecessor prefix and
  retain new leaf spans; verify old node/history inverses. Truncated work was
  never committed; no source history is lost.
  Owned D5: profile-binding-before.log25 tests/1 failure/0 errors accepts a
  release output for the fixed host cargo-test command. Restrict to debug and
  add a discriminating profile guard; cross-target outputs remain unclaimed.
  promotion: declined (implements existing output-only/input-preservation policy).
  Public-interface observation: cargo-contract.json (Cargo1.95.0) dry-run/dev
  lists both a cache-shaped toy and an input under target/debug/input-fixtures;
  all five fixture inputs remain byte-exact. Cargo metadata/root/profile scope
  cannot establish per-file generation. Require changed/new output observations
  from a bound successful build; unknown/unchanged unowned inputs stay retained.
  promotion: declined (implements existing output-only/input-preservation policy).
  Owned P1 input-ownership finding: input-candidate.log rc=0 shows a retained
  fixture under target/retained-fixture-inputs/debug/incremental selected solely
  by basename/path; no Cargo build-output provenance exists. candidate() checks
  name/prefix/incremental/link/tracked metadata, not regenerable ownership.
  Resolve before exposing cache mutation: bind declared published build-output
  roots/ownership and protect input/evidence/fixture namespaces; test omissions.
  Metadata-only planning/journal has deleted no such input; .15 owns the fix
  at highest priority for deletion readiness. No submodule implementation use.

- ID: `ARTIFACT-CLEANUP.16` — **anchored guarded deletion and journal integration**
  Status: `pending`
  Goal: after .17 bound output ownership, add whole-cohort/per-file SHA/identity/tracked
  and same-volume/non-Git parent revalidation immediately before each unlink.
  Connect durable intent/outcome records; retained/residue post-checks and known
  partial failure/uncertain window. Cover D1/staleness/aliases/parent changes,
  output errors and interruption in owned fixtures only. No supported operator
  mutation until .14 host binding; no real cleanup merely for testing. Normal COMMIT.

- ID: `ARTIFACT-CLEANUP.17` — **bind real build observations and plan selection**
  Status: `pending`
  Goal: use .15 records around bound public Cargo invocations; preserve exact
  existing output paths and protect unchanged unowned inputs. Bind actual
  source/root/command/return facts, bounded atomic merge/publication and current
  cohort selection; historical plans remain readable but grant no new mutation
  authority. Exercise actual owned builds, malformed/stale receipts, source and
  output changes, interruptions and cold CLI. Verify P1 fixed before .16 core.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `ARTIFACT-CLEANUP.17` | `pending` | bind actual builds and plan selection before .16 core/.14 CLI |

## Decisions

- `2026-09-26`: scope is the directive's enumerated cargo scope and nothing else without
  per-class evidence. The `.app-data/cargo-home/**/tests/data/*.bin` files are crate **source**
  fixtures (inputs), not artifacts — deleting them would be damage wearing a cleanup's clothes.

## Open Questions

- Do `target/refs/*.log` (spike build logs, smoke guest outputs) join the deletion scope? They
  are regenerable but are evidence trails of the last reference run; at 1.3 MB they cost nothing.
  Deferred until their size or staleness makes them a question again.

## Blockers

- None.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.1)

- [x] **ROOT CAUSE (WHY + WHERE)** — the record file §8 names did not exist; the directive's own
  trigger ("file does not exist → run a cleanup during this session") fired. WHERE the artifacts
  were, from the pre-delete census:

  ```
  $ find target .app-data -path '*incremental*' -name '*.bin' | wc -l               -> 40
  $ find target .app-data -path '*incremental*' -name '*.bin' -exec du -ch {} +     -> 341M total
    (22 files under target/…/incremental, 18 under .app-data/target/debug/incremental)
  $ find .app-data \( -name '*.bin' -o -name '*.log' \) | grep -v incremental        -> 7 files,
    all .app-data/cargo-home/registry/src/**/tests/data/*.bin  (digest, sha2 — crate source
    fixtures, i.e. INPUTS; deleting inputs is damage, not cleanup — kept)
  ```

- [x] **ADDRESSED (verified)** — before → after, measured:

  ```
  BEFORE: 40 incremental .bin / 341M; .app-data 1.4G
  $ find target .app-data -path '*incremental*' -name '*.bin' -delete
  AFTER:  find … '*.bin' | wc -l -> 0;  .app-data 1.1G;  target unchanged (its .bin were the
          linkedspec consumer caches; the superproject target/ still holds its build outputs)
  $ git status --porcelain   -> only the intended tracked files (tree, index, record, registry, changelog)
  ```

- [x] **NO REGRESSION** — nothing executable changed; the enforcer re-run after staging:

  ```
  $ bash scripts/check_doctrines.sh   -> === all doctrines green ===
  ```

  The deleted caches are cargo outputs; the next `make check` / consumer build regenerates them
  (a cold incremental cache is slower, never wrong).

- [x] **FIX** — deleted the 40 enumerated-scope caches; created `docs/ARTIFACT_CLEANUP.md`
  (overwrite-only record); registered it in `doctrine/readme_routes.tsv` in the same commit.

- [x] **LOCKSTEP** — `docs/TASK_TREE.md` row added; CHANGELOG entry; registry derivation comment;
  LIVE_STATUS unchanged (no project-area row describes housekeeping); MEMORY.md unchanged (the
  frontier did not move).

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.4)

- [x] **REPRODUCE / ROOT CAUSE** — the latest record names 2026-10-08; this dated
  run is 2026-10-09. Python Path.rglob census of target/.app-data, excluding symlinks
  and git ls-files entries, enumerates 249 incremental bins / 861,367,249 B. Breakdown:
  debug 165 / 526,348,156 B; Miri AArch64 9 / 53,876,225 B; Miri powerpc64 6 /
  32,141,295 B; wasm 33 / 109,923,020 B; C guest-image probe 24 / 55,985,016 B;
  C engine probe 12 / 83,093,537 B. No stray bins/logs in release/deps roots.
- [x] **FIX / ADDRESSED** — validate each target-local candidate is a regular .bin
  under incremental, untracked, unchanged in size and free of symlink ancestors;
  unlink exactly the saved census. Python repeat census: 249 / 861,367,249 B -> 0.
  Latest record overwritten. Diagnostic outputs 443 / 2,818,921 B, reference logs
  62 / 2,096,498 B and dependency-source fixtures 7 / 1,056 B retained.
- [x] **NO REGRESSION** — actual unsandboxed bash scripts/check_no_background_jobs.sh
  prints handoff: OK before deletion. No active build uses caches; no tracked file or
  dependency input removed. Commit doctrine gate must pass; caches regenerate normally.
- [x] **LOCKSTEP** — tree/index and latest record, MEMORY, CHANGELOG/DEV_NOTES updated.
  LIVE_STATUS reviewed: unchanged, P4 11/18 and CPU-SYSTEM incomplete. No user-visible
  behavior changes, so no product/book rewrite. promotion: declined (recurring procedure
  and measured exclusions remain in this tree). Return to P4-SYSTEM.12 e1d after commit.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.5)

- [x] **ROOT CAUSE** — cleanup.py --plan rc=0: prior2026-10-09 record,
  approximately24h recurrence;204 safe incremental paths/978509475B from twelve
  roots, stray release/deps0; tracked/symlink/nested-Git/volume exclusions checked.
- [x] **ADDRESSED** — cleanup.py --delete/verify.py rc=0:204paths→0,
  exact saved all-candidate identity preflight;6261retained input/evidence hashes
  and bytes exact; latest one-entry record overwritten with2026-10-10 receipt.
- [x] **NO REGRESSION** — actual pre-delete census rc=0/handoff: OK;
  focused9/six books/verify.py rc=0, all code/canonical/frozen/registry/history/
  LIVE unchanged. No active build, tracked-file or dependency-input deletion.
- [x] **LOCKSTEP** — task/index/latest record/MEMORY/DEV/CHANGELOG/book aligned;
  resume P4-SYSTEM.14 a7 after committed clean actual census.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.6)

- [x] **ROOT CAUSE** — cleanup.py --plan/--check rc=0 normal/O: last run2026-10-10T17:22:34Z;24safe caches/155683881B,9225retained/128863947B, four nested Git skips; actual unrestricted pre-delete census rc=0/handoff: OK.
- [x] **ADDRESSED** — cleanup.py --delete rc=0:24saved paths removed, selected residue0, all9225retained size/SHA exact immediately. Changed SHA/totals refuse normal/O before deletion; named latest-record include in book normal/print verified by verify.py rc=0.
- [x] **NO REGRESSION** — focused.sh rc=0:focused12/sharder12/seven books/navigation; history.py/verify.py rc=0 normal/O:complete old heads/task/book inverses and unrelated bytes/modes/Gitlinks exact. Full hooks and post-commit.py close COMMIT; no CPU/canonical/LIVE/cap changes.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.7)

- [x] **ROOT CAUSE** — cleanup.py --plan/--check rc=0 normal/O: latest2026-10-11 record is over24h old;18safe caches/77596881B,10701retained/131474223B, four nested-Git skips; actual unrestricted pre-delete census rc=0/handoff: OK.
- [x] **ADDRESSED** — cleanup.py --delete rc=0:18saved paths removed, selected residue0 and all10701retained bytes/SHA exact immediately. Changed identity/totals each refuse before deletion normal/O. Latest single-entry include reaches normal/print through the existing book source.
- [x] **NO REGRESSION** — focused.sh/history.py/verify.py rc=0 normal/O where applicable:focused12/sharder12/seven books, whole prior heads/task/index inverses and unrelated identities/modes/Gitlink exact. Required hooks/post-commit census close COMMIT. No source behavior, CPU, LIVE, archive or fixed-cap change.
- [x] **LOCKSTEP** — latest record/tree/index/MEM/CH/DEV updated; unchanged book source directly includes the new receipt. Return to LC.4 D77 after committed clean handoff.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.8)

- [x] **ROOT CAUSE** — `python3 target/artifact-cleanup-0065/cleanup.py --plan` rc=0: prior2026-10-16T21:24:43Z is over24h old;18safe caches/77596894B,14220retained/131741041B, four nested Git skips and0strays. Helper is the .7 public procedure with only its owned output root changed.
- [x] **ADDRESSED** — `python3 target/artifact-cleanup-0065/cleanup.py --delete` rc=0 after joined normal/O checks and green actual pre-delete host census:18saved paths absent, selected residue0, all retained counts/bytes/SHA exact immediately. Four damaged identity/totals controls each refuse before deletion normal/O. Early active-check census refuses; no deletion until repeated census rc=0.
- [x] **NO REGRESSION** — focused13/seven books and `python3 target/artifact-cleanup-0065/verify.py` normal/O rc=0: old source/history/modes/Gitlinks and original book teaching unchanged; latest receipt renders normal/print, fixed caps retained. Full normal COMMIT/postcheck closes the unit; no Rust behavior/full CI/push change.
- [x] **LOCKSTEP** — latest record/tree/index/MEM/CH/DEV and book's direct include agree. LC0047 app-release witness is in LIVE-CONTAINMENT, no exemption or app action; final census still required. promotion: declined (standing safe-cohort/locality/ownership procedure). Next LC0048 terminal D79 capture/analysis; D80 follows.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.9)

- [x] **ROOT CAUSE** — cleanup.py --plan/check rc=0 normal/O: prior2026-10-17T22:50:22Z is over24h old;177caches/674371444B,16764retained/145405416B; four nested-Git skips/0strays. Standing helper differs only in owned output root.
- [x] **ADDRESSED** — cleanup.py --delete rc=0 after six joined positive/negative preflights and actual pre-delete census OK:177saved paths absent, selected residue0 and retained bytes/SHA exact immediately. Four damaged-plan refusals precede deletion.
- [x] **NO REGRESSION** — focused.py/verify.py rc=0 normal/O where applicable:13 focused checks/seven books;1545 other files/1Gitlink/92 old entries and complete original task/index/head inverses exact; latest receipt in normal/print. Full hooks/actual handoff close COMMIT.
- [x] **LOCKSTEP** — verify.py rc=0:latest record/task/index/MEM/CH/DEV and existing book include agree; source teaching/LIVE/caps exact. DEV0355 keeps one whole-oldest4336B entry. promotion: declined (standing safe-cohort/locality/history contracts).

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.10)

- [x] **ROOT CAUSE** — cleanup.py --plan/check rc=0 normal/O: prior2026-10-18T23:00:27Z over24h;18 safe caches/78250724B,18121 retained/152718645B; four nested-Git skips/0strays.
- [x] **ADDRESSED** — cleanup.py --delete rc=0 after six joined preflights/actual host census:18 saved paths absent, selected residue0, retained bytes/SHA exact immediately; four damaged-plan refusals precede deletion.
- [x] **NO REGRESSION** — focused.py/verify.py rc=0:13 focused checks/seven books;1452 protected files/1Gitlink/97 predecessor entries exact, task/index inverses2 and normal/print latest receipt. Normal COMMIT/actual census follow.
- [x] **LOCKSTEP** — verify.py rc=0:latest record/task/index/MEM/CH/DEV/book include agree; source teaching/LIVE/caps unchanged. Native0377 retains636B whole predecessor; promotion declined: standing safe-cohort/locality/history contracts.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.11)

- [x] **REPRODUCE / ISSUE** — git ls-files --error-unmatch
  target/artifact-cleanup-0067/cleanup.py rc=1; tracked cleanup census empty.
  The legacy release fixture selected=stray=1, then unlinked and failed its
  post-check without a receipt. reproduce-release.py rc=0 owns this observation;
  tracked probe test_release_cache_is_not_a_retained_stray preserves the case.
- [x] **ROOT CAUSE (WHY + WHERE)** — TOOLBOX.md requires tracked instruments.
  Legacy safe() selects release caches while census() labels all release bins
  as retained strays. Release D1 is disjoint in artifact_cleanup.make_plan;
  deletion/partial-outcome repair stays explicitly ARTIFACT-CLEANUP.12.
  bash scripts/check_artifact_cleanup.sh --self-test checks this classification.
- [x] **FIX** — tracked immutable bounded planning/checking and exclusive plan
  publication only. Fixed runtime root; public HEAD/index inventory protects
  tracked aliases; descriptor traversal refuses boundary changes. Explicit
  per-pass limits, strict JSON, source identity and retained/selected separation.
  Ten copied-source guard omissions fail their own assertion without errors;
  no production mutation switch and no delete API. Shared CLI/book usage.
- [x] **ADDRESSED (verified)** — bash scripts/check_artifact_cleanup.sh
  --self-test:22 pass/0 fail, normal/O26 tests each; ten targeted omissions
  each1 failure/0 errors. Copied CLI uses valid parent cwd and no local Git
  metadata, refuses parent fallback; fake public Git exercises success without
  creating/modifying another repository. Actual CLI plan/check matched18 caches/
  78250715B and18219 retained files/152775548B;6836479B plan; no deletion.
- [x] **NO REGRESSION** — focused16 checks rc=0, including scripts/check_seam_integrity.sh
  and normal/O ARTIFACT-COHORT. Native3/41514B exact; seven books built, normal/
  print teaching verified. Scope18/protected1447/1 opaque Gitlink;98 whole old
  entries preserved, native0378/0379 retain3504B. Complete task/index inverses2,
  book inverses2/governance inverses4; fixed capacities and original inputs exact.
  D2 pre-open device check reverified26 tests normal/O/22 exact outcomes.
  Final Git-marker scoped CLI plan/check6/46717788B matches the current source
  and six earlier default-plan file facts. Staged checks follow before commit.
- [x] **LOCKSTEP** — task/index/MEM/CH/DEV/LIVE, governance/toolbox mirrors and
  shared book usage synchronized. Derived40 doctrines/1627 literal arms;42 routes,
  CPU14/18/BOARD10/12/replay4/4green unchanged. Normal COMMIT closes the unit.
  No latest-cleanup overwrite:
  this is an instrument change, not a new cleanup event.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.12)

- [x] **REPRODUCE / ISSUE** — git ls-files --error-unmatch
  target/artifact-cleanup-0067/cleanup.py rc=1; the original source was ignored.
  AC0068 preserves its5815B/SHA0396e669f9b798f010dcbe67b5f3462497afbcff478d353c7d989b9b2bd307e9
  identity, but a fresh checkout still lacked those original bytes. New fixture
  copies them exactly; tracked replay reproduces release-D1 in an owned fixture.
- [x] **ROOT CAUSE (WHY + WHERE)** — TOOLBOX.md requires first-class tracked
  producers. The original5815B helper remained only under target; its safe()
  selects release caches while census() also calls them strays. Legacy test
  `post-delete census differs` follows unlink with no receipt, retained bytes
  unchanged. python3 scripts/probe_legacy_artifact_cleanup.py rc=0:5 tests pass.
- [x] **FIX** — retain passive original source and an8KiB descriptor reader,
  immutable historical size/SHA pin and owned on-volume replay. Only public Git
  root/inventory reads mocked; real historical helper bytes execute only inside
  newly created fixtures. Source-pin omission applies only to a copied reader.
  Current planner keeps candidates separate; actual deletion/receipts remain .13/.14.
- [x] **ADDRESSED (verified)** — scripts/check_artifact_cleanup.sh --self-test:
  26 pass/0 fail. Five legacy tests normal/O; each pin omission1 failure/0 errors.
  Three-file cold CLI has no Git and a valid parent cwd, both modes5/0/0. Debug
  cleanup completes; release cache removed then legacy post-check refuses with
  no receipt. Old helper digest exact in replay; no real project deletion.
- [x] **NO REGRESSION** — focused16 rc=0, including scripts/check_seam_integrity.sh
  and26-outcome ARTIFACT-COHORT. Native3/41514B exact; seven books/normal-print
  teaching verified. Scope18/protected1452/1 opaque Gitlink/98 old live entries;
  native0380/0381 retain3172B whole. Task/index inverses2, prior planner logic and
  gate exact,78B toolbox row moved verbatim; all capacities/source inputs exact.
  Staged history/acceptance/default gate checks follow before normal COMMIT.
- [x] **LOCKSTEP** — task/index/MEM/CH/DEV/LIVE, bounded toolbox family and shared
  book/help synchronized. Derived1629 sites;40 doctrines/42 routes/CPU14/18/
  BOARD10/12/replay4/4green unchanged. Source book524285/524288B, no raised cap.
  Original event/producer/capture preserved; normal COMMIT closes .12 before .13.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.13)

- [x] **REPRODUCE / ISSUE** — tracked legacy replay (scripts/probe_legacy_artifact_cleanup.py)
  rc=0 shows release-D1: unlink followed by failed post-check/no receipt. A later
  caller needs recoverable progress before any cache operation. Source census:
  git ls-files scripts/*cleanup* at e9b4532 lists planner/replays, no attempt journal.
- [x] **ROOT CAUSE (WHY + WHERE)** — legacy cleanup.py writes result.json only
  after its post-check. Apple fsync(2) also documents drive-buffer loss/reordering
  after ordinary fsync. fullsync.json verifies owned file/directory fsync and
  Darwin F_FULLFSYNC on read/write descriptors; power failure remains untested.
  python3 scripts/probe_artifact_cleanup_journal.py rc=0:26 tests/0 failures/0 errors.
- [x] **FIX** — one-shot bounded framed journal; bind canonical published plan,
  recorder/actor source; synchronize plan/ancestors before yield and flush frames
  before accepting state. Revalidate root/parent/file/plan before each append,
  preserve failed writes, prohibit poisoned reuse. Strict reader preserves torn
  prefixes/pending uncertainty and reports records without current-state credit.
  Readonly inspect CLI; no cache-unlink API. .15 core then .14 operator workflow.
- [x] **ADDRESSED (verified)** — scripts/check_artifact_cleanup.sh --self-test:
  48 pass/0 fail. Journal26 tests normal/O; ten omissions each1 failure/0 errors,
  22 exact outcomes. Four-file copied inspect CLI has no Git/valid parent cwd;
  no producer launch needed. Actual source-bound plan/barriers/write/read smoke
  records intent0/returns0; newly owned dummy cache unchanged, report incomplete.
- [x] **NO REGRESSION** — focused16 rc=0; scripts/check_seam_integrity.sh and
  48-outcome ARTIFACT-COHORT green. Native3/41514B exact; books7/normal-print
  old/new teaching verified. Scope18/protected1456/1 opaque Gitlink/98 old entries;
  native0382/0383 retain4030B whole. Task/index inverses2; planner logic/gate and
  complete old book fragment retained, include-base inverses2; all caps exact.
  Staged history/acceptance/default gate checks follow before normal COMMIT.
- [x] **LOCKSTEP** — task/index/MEM/CH/DEV/LIVE and source-backed book/toolbox
  teaching synchronized. Rebase the complete old cleanup fragment into the
  bounded artifact family; preserve its text/examples and all fixed caps.
  Derived1631 sites;40 doctrines/42 routes/CPU14/18/BOARD10/12/replay4/4green
  unchanged. Book524076/524288B; normal COMMIT before .15 P1 ownership/core.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.15)

- [x] **REPRODUCE / ISSUE** — scripts/probe_artifact_output_provenance.py
  --cargo-contract rc=0: profile input is listed; three owned inputs remain exact.
- [x] **ROOT CAUSE (WHY + WHERE)** — candidate() infers class from names;
  profile scope cannot show generation. D3 load() lacked root identity; D5
  output_class() admitted release for a host test. Probe25 tests rc=0 after fixes.
- [x] **FIX** — bounded closed per-file observations; strict command/profile,
  before/after source/root/fact matching. No cache mutation; .17 integration next.
- [x] **ADDRESSED (verified)** — scripts/check_artifact_cleanup.sh --self-test
  rc=0:76 outcomes;25 tests normal/O/13 omissions each1 failure/0 errors.
- [x] **NO REGRESSION** — focused16 rc=0; native3/41514B, books7/normal-print;
  scope18/protected1460/1Gitlink/97 old entries;3844B whole0384/0385; all caps fixed.
- [x] **LOCKSTEP** — task/index/live/book/toolbox sync;1633 sites/40 doctrines/42
  routes; CPU14/18/BOARD10/12/replay4/4green unchanged. Normal COMMIT before .17.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-20` UTC | `.15` |25 tests normal/O/13 omissions, gate76/focused16/books7/scope |18 files/protected1460/1Gitlink/97 old entries;3844B whole0384/0385; no cache mutation; P1 integration .17 |
| `2026-10-20` UTC | `.13` |26 tests normal/O/10 omissions, actual metadata/full-sync smoke, gate48/focused16/books7/scope |18 files/protected1456/1Gitlink;98 old entries/4030B whole0382/0383; no cache unlink; P1 ownership fix .15 |
| `2026-10-20` UTC | `.12` | five legacy tests normal/O/pin omission, cold3, gate26, focused16/books7/scope |18 files/protected1452/1Gitlink;98 whole old entries,3172B native0380/0381; no real cleanup; staged checks/normal COMMIT follow |
| `2026-10-20` UTC | `.11` | focused16;26 tests normal/O/ten omissions each; actual plan/check; books7; whole source/history inverses |22 exact outcomes; scope18/protected1447/1Gitlink/98 old entries;3504B whole0378/0379; no real deletion; staged checks and normal COMMIT follow |
| `2026-10-19` UTC | `.10` | saved-cohort plan/check/delete; six normal/O controls; pre-delete actual census |18/78250724B removed; immediate residue0;18121/152718645B retained exact; focused13/books7/source-history/rendered receipt verified |
| `2026-10-18` UTC | `.9` | cleanup.py plan/check/delete; six normal/O preflights; actual pre-delete census |177/674371444B removed, immediate residue0;16764/145405416B retained exact; focused13/seven books/source-history inverses/normal-print receipt rc=0 |
| `2026-10-16` | `.7` | cleanup.py plan/check/delete; four normal/O refusal controls; actual pre-delete census; focused12/sharder12/seven books; whole source/history/cap/rendered verification |18/77596881B removed, immediate residue0;10701/131474223B retained byte/hash-exact; original book source and latest normal/print receipt verified |
| `2026-10-11` | `.6` | cleanup.py plan/check/delete; pre-delete host census; four damaged-input refusals normal/O; focused12/sharder12/seven books; history/verify normal/O |24/155683881B removed, immediate residue0;9225/128863947B retained byte/hash-exact; latest book include and complete source/history/scope inverses rc=0 |
| `2026-10-10` | `.5` | exact204path/978509475B identity+safe-scope preflight, actual pre-delete census, delete/re-census | residue0;6261kept/10011409B SHA exact; focused9/six books/verify rc=0, code/canonical/history/LIVE exact |
| `2026-10-09` | `.4` | Python census, tracked/symlink/size exclusions, exact deletion, repeat census; actual process census | 249 bins / 861,367,249 B -> 0; all evidence/input logs retained; handoff OK |
| `2026-10-08` | `.3` | Python `Path.rglob` census, tracked-file exclusion, deletion, re-census; `du -sh target .app-data` | 102 incremental bins / 364,047,724 B → 0; target 4.8 G → 4.5 G; .app-data 1.4 G unchanged; diagnostic/reference logs and dependency fixtures retained |
| `2026-10-06` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 192 files / 607 M, all in cargo `*/incremental/*` dirs (144 `target/debug`, 36 wasm32, 12 the `.7` scratch probe's own `target/p4-system-7/fsprobe/target/debug`); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 62 `target/refs/**/*.log` (2.2 M) kept by standing policy; 7 crate-source fixtures kept |
| `2026-10-06` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 4.8 G → 4.2 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-10-04` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 90 files / 245 M, all in cargo `*/incremental/*` dirs (72 `target/debug`, 18 wasm32); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 62 `target/refs/*.log` (2.2 M) kept by standing policy; 7 crate-source fixtures kept |
| `2026-10-04` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 4.2 G → 4.0 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-10-03` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` | 0 files / 0 M — none accumulated since the `2026-10-02` run; 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 62 `target/refs/*.log` (2.2 M) kept by standing policy; 7 crate-source fixtures kept |
| `2026-10-03` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin` (nothing to delete); `target` 3.9 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-10-02` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 105 files / 139 M, all in cargo `*/incremental/*` dirs (84 `target/debug`, 21 wasm32); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 0 `target/refs/*.log` present this run; 7 crate-source fixtures kept |
| `2026-10-02` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 4.0 G → 3.9 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-10-01` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 96 files / 248 M, all in cargo `*/incremental/*` dirs (48 `target/debug`, 18 `target/x86_64-apple-darwin`, 12 wasm32, 9+9 the two miri profiles); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 0 `target/refs/*.log` present this run; 7 crate-source fixtures kept |
| `2026-10-01` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 3.7 G → 3.5 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-09-30` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 90 files / 185 M, all in cargo `*/incremental/*` dirs (72 `target/debug/incremental`, 18 `target/wasm32-unknown-unknown/debug/incremental`); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 0 `target/refs/*.log` present this run; 7 crate-source fixtures kept |
| `2026-09-30` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 3.4 G → 3.2 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-09-29` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 169 files / 272 M, all in cargo `*/incremental/*` dirs (139 `target/debug/incremental`, 30 `target/wasm32-unknown-unknown/debug/incremental`); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; `target/refs/*.log` kept by standing policy; 7 crate-source fixtures kept |
| `2026-09-29` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `target` 3.4 G → 3.2 G, `.app-data` unchanged at 1.4 G; `git status` clean apart from intended files |
| `2026-09-28` | `ARTIFACT-CLEANUP` (time-triggered run) | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` + per-dir `uniq -c` | 132 files / 720 M, all in cargo `*/incremental/*` dirs (`target/` own + wasm32 profiles, `.app-data/target/` vendored-consumer builds); 0 stray `.bin`/`.log` in `target/release`/`target/debug/deps`; 7 crate-source fixtures kept |
| `2026-09-28` | `ARTIFACT-CLEANUP` (time-triggered run) | post-delete re-census + `du -sh` | 0 incremental `.bin`; `.app-data` 2.0 G → 1.4 G, `target` 3.1 G → 3.0 G; `git status` clean apart from intended files; `bash scripts/check_doctrines.sh` green |
| `2026-09-26` | `ARTIFACT-CLEANUP.1` | pre-delete census: `find target .app-data -path '*incremental*' -name '*.bin'` | 40 files / 341 M, all in cargo incremental dirs |
| `2026-09-26` | `ARTIFACT-CLEANUP.1` | kept-items classification: `.bin`/`.log` outside incremental | 7 crate-source fixtures (inputs), 13 `target/refs/*.log` (evidence) — kept |
| `2026-09-26` | `ARTIFACT-CLEANUP.1` | post-delete re-census + `du -sh` | 0 incremental .bin; `.app-data` 1.4 G → 1.1 G |
| `2026-09-26` | `ARTIFACT-CLEANUP.1` | `bash scripts/check_doctrines.sh` | all doctrines green |
| `2026-09-27` | `ARTIFACT-CLEANUP.2` | `bash scripts/check_no_background_jobs.sh` (live) | `handoff: OK` with the watcher (PID 36462) running — exemption fires |
| `2026-09-27` | `ARTIFACT-CLEANUP.2` | control probe (the row absent) | the same process flags again — the exemption, not blindness, is what changed |

## Commit Log

`SEMULITH-AC-0071 (leaf ARTIFACT-CLEANUP.15): bind per-file output-provenance records` —25 tests normal/O/28 provenance outcomes; gate76; actual Cargo dry-run witness; no cache mutation. .17 next.

`SEMULITH-AC-0070 (leaf ARTIFACT-CLEANUP.13): record recoverable cleanup intent` — bounded metadata journal/inspection,26 tests normal/O/22 journal outcomes, gate48 and actual barrier smoke; no cache unlink. P1 ownership/core .15 next.

`SEMULITH-AC-0069 (leaf ARTIFACT-CLEANUP.12): retain the historical cleanup helper` —5815B authenticated passive source, five legacy tests normal/O and pin controls; cold3/gate26/whole source-history preservation. No real cleanup event.

`SEMULITH-AC-0068 (leaf ARTIFACT-CLEANUP.11): track bounded cleanup planning` —26 fixture tests normal/O,22 guard outcomes, actual read-only plan/check; no new cleanup event. Guarded deletion/partial results remain .12.

`SEMULITH-AC-0067 (leaf ARTIFACT-CLEANUP.10): remove due incremental caches and retain method evidence` —18/78250724B removed, immediate residue0;18121 retained exact.

`SEMULITH-AC-0066 (leaf ARTIFACT-CLEANUP.9): remove due incremental caches and retain capture evidence` —177/674371444B removed, immediate residue0;16764retained exact.

`SEMULITH-AC-0065 (leaf ARTIFACT-CLEANUP.8): remove due incremental caches and preserve capture evidence` —18/77596894B removed, immediate residue0;14220retained exact.

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.7` | `SEMULITH-AC-0064 (leaf ARTIFACT-CLEANUP.7): remove due incremental caches and retain qualification evidence` |18caches/77596881B, immediate residue0;10701retained exact; next LC0039 D77 |
| `.6` | `SEMULITH-AC-0063 (leaf ARTIFACT-CLEANUP.6): clean incremental caches and include the latest book receipt` | 24caches/155683881B, immediate residue0;9225retained exact; next P4 a42j |
| `.5` | `SEMULITH-AC-0062 (leaf ARTIFACT-CLEANUP.5): remove recurring incremental caches and retain evidence` | 2026-10-10;204files/978509475B, residue0;6261retained inputs/evidence hashes exact |
| `.4` | `SEMULITH-AC-0061 (leaf ARTIFACT-CLEANUP.4): remove due incremental caches and preserve evidence inputs` | 2026-10-09 cleanup; 249 files / 861,367,249 B |
| `.3` | `SEMULITH-AC-0060 (leaf ARTIFACT-CLEANUP.3): remove the due incremental caches; preserve diagnostic evidence` | 2026-10-08 cleanup, 102 files / 364,047,724 B |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0059 (tree ARTIFACT-CLEANUP): …` | the 2026-10-06 cleanup — 192 incremental caches, 607 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0058 (tree ARTIFACT-CLEANUP): …` | the 2026-10-04 cleanup — 90 incremental caches, 245 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0057 (tree ARTIFACT-CLEANUP): …` | the 2026-10-03 cleanup — 0 incremental caches present to delete; 62 `target/refs/*.log` (2.2 M) kept |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0056 (tree ARTIFACT-CLEANUP): …` | the 2026-10-02 cleanup — 105 incremental caches, 139 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0055 (tree ARTIFACT-CLEANUP): …` | the 2026-10-01 cleanup — 96 incremental caches, 248 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMULITH-AC-0054 (tree ARTIFACT-CLEANUP): …` | the 2026-09-30 cleanup — 90 incremental caches, 185 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMILITH-AC-0053 (tree ARTIFACT-CLEANUP): …` | the 2026-09-29 cleanup — 169 incremental caches, 272 MB |
| `ARTIFACT-CLEANUP` (run) | `SEMILITH-AC-0052 (tree ARTIFACT-CLEANUP): …` | the 2026-09-28 cleanup — 132 incremental caches, 720 MB |
| `ARTIFACT-CLEANUP.2` | `SEMILITH-AC-0051 (leaf ARTIFACT-CLEANUP.2): …` | the sanctioned-watcher exemption, data-owned; the census stops crying wolf |
| `ARTIFACT-CLEANUP.1` | `SEMULITH-AC-0050 (leaf ARTIFACT-CLEANUP.1): …` | first §8 cleanup; record + registry row in the creating commit |

## Changelog

- `2026-10-19` UTC: `.10` cleanup event completed;18 caches/78250724B removed, immediate residue0;18121 retained hashes exact. Focused13/books7/whole source-history inverses/normal-print receipt pass; normal COMMIT closes the unit.

- `2026-10-18` UTC: `.9` cleanup completed;177caches/674371444B removed, immediate residue0;16764retained hashes exact. Existing book include/source and fixed caps preserved; next P4-SYSTEM.14 shared read allowance.

- `2026-10-16`: `.7` done;18incremental caches/77596881B removed, immediate residue0;10701retained bytes/SHA exact. Existing book latest include updates without source growth; fixed caps/CPU/LIVE unchanged. Next LC0039 D77 repair.

- `2026-10-11`: `.6` done;24incremental caches/155683881B removed, immediate residue0;9225retained size/SHA exact. Latest record directly included in book; focused12/sharder12/seven books/source/history/scope green. Proposed scaffold-retention risk owned in P4 a42j, next after this committed cleanup.

- `2026-10-10`: `.5` done;204 cargo incremental caches/978509475B removed, residue0;6261retained input/evidence files SHA exact, no tracked deletion. Latest record/index/book aligned, focused9/six books green.

- `2026-10-08`: `.3` done; 102 incremental caches removed (364,047,724 B), residue 0.
  Diagnostic and reference logs, dependency fixtures retained; latest record overwritten.

- `2026-10-06`: Time-triggered §8 run (the `2026-10-04` record was >24 h old): 192 incremental
  `.bin` caches deleted (607 MB; 144 `target/debug`, 36 wasm32, 12 the `.7` scratch probe's own
  cargo build); 0 stray `.bin`/`.log` in the enumerated locations; 62 `target/refs/**/*.log`
  (2.2 M) and the cargo-home fixtures kept by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with
  the one-line record.

- `2026-10-04`: Time-triggered §8 run (the `2026-10-03` record was >24 h old): 90 incremental
  `.bin` caches deleted (245 MB; 72 `target/debug`, 18 wasm32); 0 stray `.bin`/`.log` in the
  enumerated locations; 62 `target/refs/*.log` (2.2 M) and the cargo-home fixtures kept by
  policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line record.

- `2026-10-03`: Time-triggered §8 run (the `2026-10-02` record was >24 h old): 0 incremental
  `.bin` caches present to delete — none accumulated since the previous run; 0 stray
  `.bin`/`.log` in the enumerated locations; 62 `target/refs/*.log` (2.2 M) and the
  cargo-home fixtures kept by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the
  one-line record.

- `2026-10-02`: Time-triggered §8 run (the `2026-10-01` run was a full day old): 105
  incremental `.bin` caches deleted (139 MB; 84 `target/debug`, 21 wasm32); 0 stray
  `.bin`/`.log` in the enumerated locations; no `target/refs/*.log` present this run; the
  cargo-home fixtures kept by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the
  one-line record.

- `2026-10-01`: Time-triggered §8 run (the `2026-09-30` run was a full day old): 96 incremental
  `.bin` caches deleted (248 MB; 48 `target/debug`, 18 x86_64, 12 wasm32, 9+9 miri); 0 stray
  `.bin`/`.log` in the enumerated locations; no `target/refs/*.log` present this run; the
  cargo-home fixtures kept by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line
  record.

- `2026-09-30`: Time-triggered §8 run (the `2026-09-29` run was a full day old): 90 incremental
  `.bin` caches deleted (185 MB; 72 `target/debug`, 18 wasm32); 0 stray `.bin`/`.log` in the
  enumerated locations; no `target/refs/*.log` present this run; the cargo-home fixtures kept
  by policy. `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line record.

- `2026-09-29`: Time-triggered §8 run (the `2026-09-28` run was >24 h old): 169 incremental
  `.bin` caches deleted (272 MB; 139 `target/debug`, 30 wasm32); 0 stray `.bin`/`.log` in the
  enumerated locations; `target/refs/*.log` and the cargo-home fixtures kept by policy.
  `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line record.

- `2026-09-26`: Created. First leaf opened the same day, because the record file §8 names did not
  exist — the trigger condition "file does not exist → run a cleanup during this session" fired.

- `2026-10-20` UTC: `.11` bounded planning/checking verified, full original task/history/source retained. Early actual check refused missing plan while planning still ran; joined planner before repeat, then actual cohort matched. No cache deletion. Initial os.stat capability fixture and direct numeric task syntax corrected without weakening production guards. Complete staged checks/normal COMMIT; .12 stays next before P4.

- `2026-10-20` UTC: `.12` retained original helper and replayed debug/release-D1 in owned fixtures. Five tests normal/O, pin omission1 failure/0 errors, cold3 and expanded gate26 pass; focused16/books7/normal-print/scope source-history proof pass. Preserve complete old records and original event; normal COMMIT before .13 guarded core/journal and .14 host/CLI.

- `2026-10-20` UTC: `.13` journal verified; all old source/history retained.26 tests normal/O/22 journal outcomes, gate48/focused16/books7/actual smoke/scope pass. Source/parent/file/barrier faults discriminate; no cache unlink. Normal COMMIT before .15 P1 ownership and anchored core, then .14 host-bound CLI.
