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
  Children: `ARTIFACT-CLEANUP.1`, `ARTIFACT-CLEANUP.2`, `ARTIFACT-CLEANUP.3`, `ARTIFACT-CLEANUP.4`, `ARTIFACT-CLEANUP.5`, `ARTIFACT-CLEANUP.6`, `ARTIFACT-CLEANUP.7`, `ARTIFACT-CLEANUP.8`, `ARTIFACT-CLEANUP.9`, `ARTIFACT-CLEANUP.10`, `ARTIFACT-CLEANUP.11`, `ARTIFACT-CLEANUP.12`, `ARTIFACT-CLEANUP.13`, `ARTIFACT-CLEANUP.14`, `ARTIFACT-CLEANUP.15`, `ARTIFACT-CLEANUP.16`, `ARTIFACT-CLEANUP.17`, `ARTIFACT-CLEANUP.18`, `ARTIFACT-CLEANUP.19`, `ARTIFACT-CLEANUP.20`, `ARTIFACT-CLEANUP.21`, `ARTIFACT-CLEANUP.22`, `ARTIFACT-CLEANUP.23`, `ARTIFACT-CLEANUP.24`, `ARTIFACT-CLEANUP.25`, `ARTIFACT-CLEANUP.26`, `ARTIFACT-CLEANUP.27`, `ARTIFACT-CLEANUP.28`, `ARTIFACT-CLEANUP.29`, `ARTIFACT-CLEANUP.30`

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
  Status: `done` (`2026-10-20` UTC; closed by `ARTIFACT-CLEANUP.14`, `SEMULITH-AC-0080`)
  Children: `ARTIFACT-CLEANUP.11`, `ARTIFACT-CLEANUP.12`, `ARTIFACT-CLEANUP.13`, `ARTIFACT-CLEANUP.14`, `ARTIFACT-CLEANUP.15`, `ARTIFACT-CLEANUP.16`, `ARTIFACT-CLEANUP.17`, `ARTIFACT-CLEANUP.18`, `ARTIFACT-CLEANUP.19`, `ARTIFACT-CLEANUP.20`, `ARTIFACT-CLEANUP.21`, `ARTIFACT-CLEANUP.22`
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
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0080`)
  Goal: after .16 guarded core, bind explicit caller quiescence and a fresh bounded
  invocation of the public host-census workflow before cache mutation. Preserve
  UID, exemptions and observation limits; census remains outside the doctrine.
  Add supported delete/inspect CLI, truthful partial/error outcomes and recovery
  examples. Test failed/unavailable process/identity observations, interruption
  and cold copied runtime in owned fixtures; no real cleanup event needed.
  Sync help/book/toolbox/live docs, focused checks and normal COMMIT; close the
  priority1 durable-instrument activity, then return to full P4 policy/status.

  Result (`2026-10-20` UTC, `SEMULITH-AC-0080`): artifact_cleanup_operator.py is
  the single deleting command. `--delete` runs the public handoff census as a
  bounded child (same user, sanctioned exemptions and limits, 60 s, 1 MiB) and
  proceeds only on exit 0 with the `handoff: OK` verdict; exit 1 refuses, and
  exit 2, timeout, empty, oversized or verdict-less output refuse as unavailable.
  Then the guarded core runs and one JSON receipt names disposition, stage,
  counts, failure and journal; `--inspect` reports plan, selection and journal
  without a census. Recovery is documented: never reuse a work directory. The
  priority1 activity closes; every cleanup event from .24 on runs through it.

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
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0079`)
  Goal: after .17 bound output ownership, add whole-cohort/per-file SHA/identity/tracked
  and same-volume/non-Git parent revalidation immediately before each unlink.
  Connect durable intent/outcome records; retained/residue post-checks and known
  partial failure/uncertain window. Cover D1/staleness/aliases/parent changes,
  output errors and interruption in owned fixtures only. No supported operator
  mutation until .14 host binding; no real cleanup merely for testing. Normal COMMIT.
  Owned D14 (priority3, from AC0078): a stale verdict names no member; two real
  selections went stale on one growing run log inside the census scope and only
  an ad-hoc plan diff showed it. Make check_plan report the first differing member
  and count, with a control, before .16's unlink path relies on stale verdicts.

  Result (`2026-10-20` UTC, `SEMULITH-AC-0079`): artifact_cleanup_guarded.py is
  the only unlink path: its preflight re-decides the strict selection and must
  match the saved one; a version-2 journal binds the selection digest and the
  approved indices; each file is revalidated through its parent descriptor
  (identity, digest, single link, tracked state) immediately before unlink with
  the intent flushed first and absence required after; the after-state must
  equal the plan minus the approved files. D14 fixed: stale verdicts name the
  first differing member. Only --dry-run is public; the operator act is .14.

- ID: `ARTIFACT-CLEANUP.17` — **bind real build observations and plan selection**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0078`)
  Goal: use .15 records around bound public Cargo invocations; preserve exact
  existing output paths and protect unchanged unowned inputs. Bind actual
  source/root/command/return facts, bounded atomic merge/publication and current
  cohort selection; historical plans remain readable but grant no new mutation
  authority. Exercise actual owned builds, malformed/stale receipts, source and
  output changes, interruptions and cold CLI. Verify P1 fixed before .16 core.

  Result (`2026-10-20` UTC, `SEMULITH-AC-0078`): strict selection lands as
  artifact_cleanup_selection.py: re-census the plan, intersect its candidates
  with captured current authority, publish selection.json exclusively beside
  the plan. Owned D12 (a failed build records nothing but retires rows whose
  files rustc garbage-collected) and D13 (a ctime-only change from rustc
  hard-link seeding is not a changed output), both measured at b18971e in
  target/artifact-cleanup-0078 before the fix. P1 closed: a cache-named input
  is never approved. .16 binds plan, selection and journal before any unlink.

- ID: `ARTIFACT-CLEANUP.18`
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0072`)
  Goal: AC0072: recover template capacity; move guidance intact to a bounded guide,
  align six evidence labels/flat IDs. Verify docs/gates/books and normal COMMIT.
  Issue: template lacks REPRODUCE; reader rejects guide’s .2.1 (workflow-before.json).
  promotion: declined (repairs existing workflow/containment policy).

- ID: `ARTIFACT-CLEANUP.19`
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0073`)
  Goal: Retain completed ledger before .17; full predecessor/history/live graph.

- ID: `ARTIFACT-CLEANUP.20` — **bind public Cargo command and storage roots**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0074`)
  Goal: AC0074 from clean7804bc4. First safe .17 slice: give both existing
  C producers the exact public command required by .15: relative manifest,
  explicit unchanged target/build roots, offline host debug test/filter. Bind
  runtime root and validate source/input/output/store/temp ancestors before
  launch; isolate ambient Cargo/Rust build overrides. Bound both captured pipes
  and elapsed time, terminate/join the owned process group on interruption or
  failed observations. Keep producer result semantics and all existing outputs.
  Do not publish provenance or change current candidate selection yet; .21 owns
  before/after capture and atomic publication, then .17 selects strictly.
  Verify actual public builds, seeded unchanged cache-shaped inputs, both
  modes, omission controls and cold copied runtime with a real owned Cargo
  fixture. Shared book/toolbox/help/live/history synchronization and normal
  COMMIT; preserve old evidence/events/native3 and all fixed caps.
  Evidence: target/artifact-cleanup-0074; all project scratch on this volume.
  Policy review: fsmgen public package diff21f4d3d..HEAD is empty for README,
  doctrine and adoption guide; pgen claim source SHA9f99df25 still unchanged.
  promotion: declined (implements standing storage/explicit-command contracts).

- ID: `ARTIFACT-CLEANUP.21` — **observe and atomically publish bound build outputs**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0076`)
  Goal: after .20 command/runtime boundary, bind successful actual builds to
  exact anchored before/after file facts and recorder/producer identities.
  Serialize current-ledger merge/publication and preserve old ledger on build,
  source, observation or pre-publication failure. Bound records/bytes and test
  stale/alias/interruption/partial publication/cold runtime before .17 selection.
  Unchanged unowned inputs receive no authority; no cleanup mutation/event.

  Owned D11 (priority3, fixed by .22 documentation sync): COMMIT.md line85
  calls the full-suite book leg "both books". Reproduce with grep -n in
  COMMIT.md/Makefile: Makefile52-54 builds docs/book and every registered
  docs/models/*/book.toml; the current actual make book log has7 builds.
  Replace the stale cardinality with the stable project-and-unit-books
  contract. No suite or push policy changes; verify against the public target.

  Result (`2026-10-20` UTC, `SEMULITH-AC-0076`): `capture` surrounds each bound
  build with an anchored census of the producer's debug/incremental caches;
  only a new file or a changed digest becomes a v2 row carrying recorder,
  producer, runner and census pins, all rechecked at publication. Publication
  refuses a held lock, merges (same path replaced, this producer's absent rows
  retired, every other row kept as it was), writes a unique temporary, applies
  F_FULLFSYNC, renames it over the ledger and reads it back. A nonzero build,
  failed version query, changed source or write error publishes nothing and
  keeps the previous ledger exact; a partial temporary is retained as evidence.
  Both producers publish; `run` stays the bare boundary. Actual engine and
  guest runs published the first real v2 ledger. Evidence: target/artifact-cleanup-0076.

- ID: `ARTIFACT-CLEANUP.22` — **bind support sources without rewriting legacy records**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0075`)
  Goal: AC0075 after43f07ab normal hooks, exact17 committed files, brief0 and
  actual host census OK. The .20 command boundary adds two relevant sources:
  artifact_cargo.py and the artifact_cleanup.py census. Extend the closed
  record codec with a versioned, bounded support-source tuple before .21
  publication. Preserve v1 decode/re-encode bytes and historical read-only
  matching; strict captured-observation matching must reject unbound v1 rows
  and require both current support identities for v2. Unknown/duplicate/malformed
  support names and stale support code must refuse authority. No actual capture,
  publication, candidate reclassification or cache deletion in this leaf.
  Cover normal/O, old controls plus targeted omission controls, and cold copied
  readers; sync shared book/help/toolbox and normal COMMIT. Keep all prior
  task/history/evidence bytes and fixed caps. Resolve the already owned D11
  book wording in this leaf's documentation sync; make book's target is authority.
  Evidence: target/artifact-cleanup-0075. Then .21 capture/publication, .17 strict
  selection, .16 core and .14 host workflow; cleanup input-ownership P1 stays open.
  promotion: declined (implements existing source-identity/backward-read contracts).

  Handoff instruction (`2026-10-20`): the director requested the next
  handoff-ready checkpoint. Finish .22's existing normal commit workflow,
  clear the brief and verify clean Git/no jobs, then stop. .21 stays unstarted;
  MEMORY.md records the stopped PNT state and selected resume action.
  PNT resumed `2026-10-20` on the director's instruction; .21 followed.

- ID: `ARTIFACT-CLEANUP.23` — **retire the next completed-checklist suffix**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0077`)
  Goal: own the live-narrative rollover before ordinary growth stops at 90% of
  the 16,384 B health target (the reader warns at 75%): seal the completed
  .19–.22 checklists and their log rows into a second finite ledger terminal
  under the .19 descriptor contract, keep the whole graph live and verify both
  publishing views. Becomes the frontier when the warning fires or when .17,
  .16 or .14 need the capacity; it adds no cleanup authority.

- ID: `ARTIFACT-CLEANUP.24` — **the first recurring cleanup through the supported act**
  Status: `done` (`2026-10-20` UTC, `SEMULITH-AC-0081`)
  Goal: when `docs/ARTIFACT_CLEANUP.md` is more than 24 h old (after
  2026-10-20T23:07Z), run the four acts in one fresh work directory under
  target/artifact-cleanup with the run log inside it: plan, strict select,
  `--delete` (fresh host census, guarded core, receipt), `--inspect`. Only
  approved captured outputs may go; unrecorded candidates, inputs and logs stay
  byte-exact. Overwrite the one-entry record with the receipt's counts, keep the
  work directory as evidence, sync tree/index/MEM/DEV/CH and normal COMMIT.

  Result (`2026-10-20T22:11Z`, `SEMULITH-AC-0081`): run at 23 h under the
  "roughly 24 h" cadence, after cfca1c2 with a clean tree and `handoff: OK`,
  in target/artifact-cleanup/AC0081 with run.log inside it. Plan: 19 candidates
  (78,250,756 B), 18,724 retained files (153,136,400 B). Strict selection: 6
  approved (15,766,463 B, the latest captured engine/guest/core sessions), 13
  unrecorded (the .13 smoke-input fixture and sessions left by failed mutation
  builds). The act's fresh census returned `handoff: OK`; the guarded core
  removed exactly the 6, residue 0, journal `recorded-complete` at `verified`;
  `--inspect` confirms plan, selection and journal with current pins. The
  one-entry record is overwritten. No unrecorded candidate, input or log moved.

- ID: `ARTIFACT-CLEANUP.25` — **the next recurring cleanup**
  Status: `done` (`2026-10-22` UTC, `SEMULITH-AC-0082`)
  Goal: when `docs/ARTIFACT_CLEANUP.md` is about 24 h old (after
  2026-10-21T22:11Z), repeat the four acts in a fresh work directory with the
  log inside it; overwrite the record from the receipt; sync and normal COMMIT.

  Result (`2026-10-22T08:12Z`, `SEMULITH-AC-0082`): run at 34 h — the slot
  fell inside a 46-minute gate run and the a42as unit the director had just
  picked — after 39e7016 with a clean tree and `handoff: OK`, in
  target/artifact-cleanup/AC0082 with run.log inside it (08:07:38Z to
  08:12:32Z). Plan: 73 candidates (296,851,352 B), 18,995 retained files
  (153,566,281 B). Strict selection: 6 approved (15,766,472 B, the latest
  captured engine/guest/core sessions), 67 unrecorded (281,084,880 B: the
  sessions the pre-commit gate's mutation builds leave behind, which capture
  never records). The act's fresh census returned `handoff: OK`; the guarded
  core removed exactly the 6, residue 0, journal `recorded-complete` at
  `verified`; `--inspect` confirms plan, selection and journal with current
  pins. The one-entry record is overwritten. Finding: the unrecorded population
  grew from 13 sessions (62,484,293 B) to 67 (281,084,880 B) in 34 h — three
  commits through the gate, each running the mutation builds — so the gate now
  leaves about 90 MB of never-captured incremental caches per commit behind;
  an Open Question below. promotion: declined (routine recurrence; the .24 entry
  carries the procedure and the finding is recorded here).

- ID: `ARTIFACT-CLEANUP.26` — **the next recurring cleanup**
  Status: `done` (`2026-10-23` UTC, `SEMULITH-AC-0083`)
  Goal: when `docs/ARTIFACT_CLEANUP.md` is about 24 h old (after
  2026-10-23T08:12Z), repeat the four acts in a fresh work directory with the
  log inside it; overwrite the record from the receipt; sync and normal COMMIT.

  Result (`2026-10-23T10:15Z`, `SEMULITH-AC-0083`): run at 26 h, after 6336c62
  with a clean tree and `handoff: OK`, in target/artifact-cleanup/AC0083 with
  run.log inside it (10:10:09Z to 10:15:09Z). The first launch wrote nothing:
  the run script appends its log inside the work directory before the plan act
  creates it, so the directory is made first (mode 700, as the tool's own
  creation; the plan act accepts an existing directory). Plan: 73 candidates
  (296,851,336 B), 19,342 retained files (153,838,837 B). Strict selection: 6
  approved (15,766,468 B, the latest captured engine/guest/core sessions), 67
  unrecorded (281,084,868 B). The act's fresh census returned `handoff: OK`;
  the guarded core removed exactly the 6, residue 0, journal
  `recorded-complete` at `verified`; `--inspect` confirms plan, selection and
  journal. The one-entry record is overwritten. Finding: the unrecorded
  population held at 67 sessions (281,084,868 B, 12 B less) across 26 h and
  nine gated commits plus five refused gate runs, so the mutation builds reuse
  a fixed set of sessions rather than adding about 90 MB per commit as .25
  feared; the Open Question below is updated. promotion: declined (routine
  recurrence; the .24 entry carries the procedure).

- ID: `ARTIFACT-CLEANUP.27` — **the next recurring cleanup**
  Status: `done` (`2026-10-26` UTC, `SEMULITH-AC-0084`)
  Goal: when `docs/ARTIFACT_CLEANUP.md` is about 24 h old (after
  2026-10-24T10:15Z), create the fresh work directory, repeat the four acts
  with the log inside it; overwrite the record from the receipt; sync and
  normal COMMIT.

  Result (`2026-10-26T08:50Z`, `SEMULITH-AC-0084`): run at 70 h (the session
  was away for the weekend), after ddb4d25b with a clean tree and `handoff:
  OK`, in target/artifact-cleanup/AC0084 (made first, mode 700) with run.log
  inside it (08:45:03Z to 08:50:21Z). Plan: 253 candidates (786,490,888 B),
  20,071 retained files (154,698,634 B). Strict selection: 6 approved
  (15,766,335 B, the latest captured engine/guest/core sessions), 247
  unrecorded (770,724,553 B). The act's fresh census returned `handoff: OK`;
  the guarded core removed exactly the 6, residue 0, journal
  `recorded-complete` at `verified`; `--inspect` confirms plan, selection and
  journal. The one-entry record is overwritten. Finding (the open question's
  trigger has fired): the unrecorded population grew from 67 files
  (281,084,868 B) to 247 files (770,724,553 B) across 18 gated commits. A
  census of the plan against AC0083's (target/artifact-cleanup/AC0084,
  census in the leaf's reply of 2026-10-26): 252 files added, 72 gone; 83
  incremental sessions, every one in a crate-hash directory that holds no
  live session — so a successful build of the same crate configuration, which
  would garbage-collect them, never follows; 198 files under target/debug, 36
  under the wasm32 target, 18 under target/p4-system-12; by crate dsp56300 54,
  core 42, verify 36, the CLI 30, xtask 30, the four rv64gc binaries 12 each;
  by hour, 10-23 21h to 10-24 07h UTC, the window of the XTASK slices' gated
  commits and their before/after measurements (which build the workspace with
  altered sources or flags, each a configuration no later build repeats). Not
  deleted here: strict selection leaves what the ledger does not record, by
  the scope decision. The deferral is over; the options are listed in the Open
  Question for the director. promotion: declined (routine recurrence; the .24
  entry carries the procedure).

- ID: `ARTIFACT-CLEANUP.28` — **the next recurring cleanup**
  Status: `done` (`2026-10-27` UTC, `SEMULITH-AC-0085`)
  Goal: when `docs/ARTIFACT_CLEANUP.md` is about 24 h old (after
  2026-10-27T08:50Z), create the fresh work directory (mode 700), repeat the
  four acts with the log inside it; overwrite the record from the receipt;
  sync and normal COMMIT. Re-census the unrecorded population against AC0084.

  Result (`2026-10-27T09:33Z`, `SEMULITH-AC-0085`): run at 25 h, after f67eaa43 with a clean tree and
  `handoff: OK` (deferred past the rv64gc portability legs, which built under target/
  until 09:59 local), in target/artifact-cleanup/AC0085 (made first, mode 700) with run.log
  inside it (2026-10-27T09:28Z to 2026-10-27T09:33Z). Plan: 349 candidates (1,135,162,995 B), 21,991 retained files
  (266,514,643 B). Strict selection: 6 approved (15,766,334 B), 343 unrecorded (1,119,396,661 B).
  The act's fresh census returned `handoff: OK`; the guarded core removed exactly the
  6, residue 0, journal `complete`/`verified`; `--inspect` confirms plan, selection and
  journal. The one-entry record is overwritten. Re-census against AC0084: the unrecorded
  population moved from 247 files (770,724,553 B) to 343 (1,119,396,661 B); the ruling on
  `.29` stands open, so nothing outside the recorded classes is touched. promotion:
  declined (routine recurrence; the .24 entry carries the procedure).
  Finding (§9, carded `a-name-one-tool-writes-is-a-path-another-tool-refuses.md`): the plan act refused twice
  (`unsafe relative path`; 73 s and 86 s walks) on 4460 names under target/xtask/xt0017 carrying U+001F/U+001E —
  the XTASK.8 slice-c prefetch records (rest/rec12 and rest/rec24, 2228 files each) and 4 control-shadow files.
  My first census grouped the offenders by a three-component prefix and acted on its one example (4 files removed,
  second refusal); the second listed the population per directory. Both populations were archived whole to
  target/xtask/xt0017/{shadow-record,rest}.tar (4 and 4,459 entries, counted against the files before anything
  was removed) and removed; the census then found 0 such names and the acts ran. Open design item for this
  tree: a refusal that names the path, or quarantines an unrepresentable entry and plans the rest.

- ID: `ARTIFACT-CLEANUP.29` — **the recorded class "orphan incremental session"**
  Status: `pending` (blocked on a ruling; see Blockers)
  Goal: execute ruling 2 of `decision_orphan-incremental-sessions.md` — strict selection gains the
  class, approved as a group and recorded beside `approved`/`unrecorded` as `orphan`; the guarded core
  and the operator carry it; probe arms fired RED; then a cleanup act removes the backlog. Design:
  target/artifact-cleanup/AC29/design.md.
  Finding before implementation (`2026-10-26`, measured on the live tree, `SEMULITH-XTASK-0013`): the
  class as recorded has no structural discriminator. A census of the four cargo roots (target/debug, the
  wasm32 target, the two PRODUCERS roots) finds 106 crate-hash directories, every one holding only
  session directories and one zero-byte `.lock` per session; the directories built 2 h earlier and the
  400–700 h-old ones have the same shape (two finished sessions, two locks), because rustc keeps the
  previous and the current session and collects only within a directory. Definition (2), "every regular
  file under D is a plan candidate", therefore holds for the live directories too: the class approves the
  current configuration's caches, and a daily cleanup is followed by one full rebuild. The plan's
  `.bin`-only scope covers 64 % of the bytes under those roots (`.bin` 786,755,579 B in 252 files; `.o`
  381,613,191 B in 10,471 files; `.rmeta` 60,305,342 B in 66; total 1,228,674,112 B): removing an orphan
  session's `.bin` files leaves its work products and directory skeleton forever, and rustc starts fresh
  silently on a missing dep-graph. Options for the ruling: (A) implement the class as recorded — ~787 MB
  now, the live caches daily, ~442 MB of skeletons kept forever, the smallest change; (B) widen the class
  to whole sessions (every regular file under an orphan session directory, then the emptied directories)
  — the full 1.23 GB and every future orphan, a widening of the directive's enumerated scope to record;
  (C) B restricted to directories with no session younger than the last recorded cleanup act — keeps the
  live caches between daily cleanups, an age rule anchored to the record. The workflow holds ruling 2
  under the delegation; the scope widening in B and C is new, so it is raised, not taken.

- ID: `ARTIFACT-CLEANUP.30` — **the next recurring cleanup**
  Status: `pending`
  Goal: when `docs/ARTIFACT_CLEANUP.md` is about 24 h old (after
  2026-10-28T09:33Z), create the fresh work directory (mode 700), repeat the
  four acts with the log inside it; overwrite the record from the receipt;
  sync and normal COMMIT. Re-census the unrecorded population against AC0085.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `ARTIFACT-CLEANUP.30` | `pending` | the next recurring cleanup, due after 2026-10-28T09:33Z; until then the feature cycle (P4-SYSTEM) resumes |

## Decisions

- `2026-09-26`: scope is the directive's enumerated cargo scope and nothing else without
  per-class evidence. The `.app-data/cargo-home/**/tests/data/*.bin` files are crate **source**
  fixtures (inputs), not artifacts — deleting them would be damage wearing a cleanup's clothes.

## Open Questions

- Do `target/refs/*.log` (spike build logs, smoke guest outputs) join the deletion scope? They
  are regenerable but are evidence trails of the last reference run; at 1.3 MB they cost nothing.
  Deferred until their size or staleness makes them a question again.

- Does the pre-commit gate's mutation-build residue need its own disposition? AC0082 found 67
  unrecorded cache-named sessions (281,084,880 B) against 13 (62,484,293 B) at AC0081, 34 h and
  three gated commits earlier: capture never records them, strict selection rightly leaves them,
  and rustc garbage-collects them only on a successful build of the same session — which the
  mutation copies never get. Either the gate's mutation runs build into a disposable session
  directory, or the ledger gains a recorded class for them. Deferred until a cleanup finds them
  still growing; nothing here is an input. AC0083 (2026-10-23, .26): still 67 sessions
  (281,084,868 B) after nine more gated commits — a stable set, not growth; deferral stands.
  AC0084 (2026-10-26, .27): 247 files / 83 orphan sessions (770,724,553 B) after 18 gated
  commits — growth, so the deferral ends. The sessions come from builds of the workspace under
  altered sources or flags (the gate's mutation copies, and the XTASK slices' RED measurements),
  each a crate configuration no later successful build repeats, so rustc never collects them.
  For the director, three options: (a) the gate's mutation builds and the measurement runs use a
  disposable target directory that the act removes whole; (b) the ledger gains a recorded class
  "orphan incremental session: a crate-hash directory with no live session", so strict
  selection can approve them; (c) a size cap on the unrecorded population, beyond which (a) or
  (b) is required. Nothing is deleted outside the act; the act's scope is the decision above.

## Blockers

- `ARTIFACT-CLEANUP.29`: a ruling between options A, B and C (the leaf's finding, `2026-10-26`); until
  then the recurring cleanups (`.30` …) run the supported act unchanged.

<!-- ARTIFACT-CLEANUP-LEDGER: 6776eca32531dcb5bd1e4e8fa030b290c4fcfeb3a8eb8811b0a1dffd5c0d481d -->
Completed checklists/logs: [exact ledger](../artifact-cleanup-history/ledger-db1260a6fa02df38fe81d6368cb4f7ba544e8cc67ac339dd8dbf4509383f9a63.md).
The [whole predecessor](../artifact-cleanup-history/predecessor-ec938336682f4bb4443d57838d45d431dc330a1dabd5ad011cd64f7117d04aa4.md) and
[retention contract](../artifact-cleanup-history/README.md) remain directly readable.
<!-- /ARTIFACT-CLEANUP-LEDGER -->

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.14)

- [x] **REPRODUCE / ISSUE** — grep -c "check_no_background_jobs" scripts/artifact_cleanup_guarded.py
  at 1ed7cbe = 0: the guarded core had no supported deleting command and nothing
  bound the host census to a mutation.
- [x] **ROOT CAUSE (WHY + WHERE)** — bash scripts/check_no_background_jobs.sh --help
  rc=0 documents exit 0/1/2 and the `handoff: OK` verdict, and
  scripts/artifact_cleanup_guarded.py exposed only `--dry-run`; the census was a
  handoff ritual, never a precondition the unlink path could prove it had run.
- [x] **FIX** — artifact_cleanup_operator.py: bounded fresh census child, green
  verdict required, then the guarded core; one receipt; inspect; recovery text.
- [x] **ADDRESSED (verified)** — bash scripts/check_artifact_cleanup.sh --self-test
  rc=0: ARTIFACT-COHORT --self-test: 146 pass / 0 fail. Operator 10 tests
  normal/O with 3 omissions, each 1 failures / 0 errors: running work refuses,
  unavailable/empty/oversized/timed-out/verdict-less censuses refuse, partial
  and interrupted attempts receipt their stage, a second act on the same
  directory is stale and names the gone member.
- [x] **NO REGRESSION** — focused 18 checks rc=0, seven fresh books, original
  native3/41514 bytes; bash scripts/check_task_history.sh --self-test rc=0;
  literal self-test arms 1641 → 1643 re-derived by DERIVED-COUNTS.
- [x] **LOCKSTEP** — usage/toolbox/doctrine/book include, LIVE_STATUS arms,
  tree (activity closed, .24 opened, frontier), index, MEM/DEV/CH; shards.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.16)

- [x] **REPRODUCE / ISSUE** — grep -c "os.unlink" scripts/artifact_cleanup.py
  scripts/artifact_cleanup_journal.py scripts/artifact_cleanup_selection.py at
  6740f24 = 0 each: plan, selection and journal existed with no unlink path
  binding them, and a stale verdict named nothing (D14).
- [x] **ROOT CAUSE (WHY + WHERE)** — git show 6740f24:scripts/artifact_cleanup_journal.py
  | grep -c "index == progress.removed" = 1: intents were bound to the whole
  plan's order, so a selection-restricted attempt could never finish `complete`;
  git show 6740f24:scripts/artifact_cleanup.py | grep -c '"scoped cohort or
  authority changed"' = 1: check_plan's stale reason was that constant
  (actual-selection-quiescent.log).
- [x] **FIX** — journal v2 begin binds selection digest and approved indices;
  guarded core re-decides the selection, revalidates per file through the
  parent descriptor, flushes intent before unlink, requires absence and a
  plan-minus-approved census; difference() names the first stale member.
- [x] **ADDRESSED (verified)** — bash scripts/check_artifact_cleanup.sh --self-test
  rc=0: ARTIFACT-COHORT --self-test: 138 pass / 0 fail. Guarded 12 tests
  normal/O with 4 omissions, journal 29 with 11, planner 27 with 10, each
  omission 1 failures / 0 errors; fixture removals leave legacy rows, inputs
  and logs byte-exact and the journal recorded-complete at verified.
- [x] **NO REGRESSION** — focused 18 checks rc=0, seven fresh books, original
  native3/41514 bytes; bash scripts/check_task_history.sh --self-test rc=0;
  literal self-test arms 1639 → 1641 re-derived by DERIVED-COUNTS.
- [x] **LOCKSTEP** — usage/toolbox/doctrine/book include, LIVE_STATUS arms,
  tree (frontier .14), index, MEM/DEV/CH; history heads sharded.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.17)

- [x] **REPRODUCE / ISSUE** — target/artifact-cleanup-0078/selection-before.log at
  b18971e: SELECTION-BEFORE: candidates 19, approved_strict 0, approved_legacy 0;
  the plan selected a smoke-input fixture by name and no current file matched.
- [x] **ROOT CAUSE (WHY + WHERE)** — grep -c "^NO-ROW" target/artifact-cleanup-0078/
  ledger-vs-candidates.log = 13 and grep -c "ctime_ns" = 6: 13 candidates had no
  row (D12: the hook's failing mutation builds returned early in
  artifact_cargo.capture while rustc garbage-collected the recorded sessions)
  and 6 rows differed only in ctime_ns (D13: rustc hard-link seeding, rejected
  by exact Fact equality in artifact_output_provenance.authorize); candidate()
  in artifact_cleanup.py never consulted the ledger (P1).
- [x] **FIX** — capture retires absent rows after a failed build; authorize
  tolerates ctime alone; artifact_cleanup_selection.py re-censuses a plan and
  exclusively publishes the strict approved/unrecorded partition beside it.
- [x] **ADDRESSED (verified)** — bash scripts/check_artifact_cleanup.sh --self-test
  rc=0: ARTIFACT-COHORT --self-test: 128 pass / 0 fail. Selection 11 tests
  normal/O with 5 omissions, each 1 failures / 0 errors; Cargo 23 and
  provenance 42 pass with their reworked controls. Actual run: both producers
  captured, then --select on the real tree approved 9 latest-session
  outputs and left 10 unrecorded, the smoke-input fixture among them. Two
  earlier attempts went stale because a growing run log sat inside the census
  scope; plan-diff.log named that single member (target/artifact-cleanup/AC0078-c).
- [x] **NO REGRESSION** — focused 18 checks rc=0, seven fresh books, original
  native3/41514 bytes; bash scripts/check_task_history.sh --self-test rc=0;
  literal self-test arms 1637 → 1639 re-derived by DERIVED-COUNTS.
- [x] **LOCKSTEP** — usage/toolbox/doctrine/book include, LIVE_STATUS arms,
  tree (frontier .16), index, MEM/DEV/CH; history heads sharded.

## Acceptance Checklist (leaf ARTIFACT-CLEANUP.23)

- [x] **REPRODUCE / ISSUE** — python3 scripts/artifact_task_history.py at b18971e:
  CLEANUP-TASK-HISTORY: 12947 live narrative bytes; warning: owned rollover due.
  The .17 checklist alone would cross 90% of 16,384 B, where ordinary growth stops.
- [x] **ROOT CAUSE (WHY + WHERE)** — grep -n "len(found) < 4\|SOURCE = \|== terminal(previous)"
  scripts/artifact_task_history.py scripts/artifact_task_history_preservation.py: the
  reader pinned one four-file generation (one SOURCE, owner .19, one descriptor
  digest) and the publisher froze that terminal, so no second generation could land.
- [x] **FIX** — generational descriptor whose retained entries re-derive each
  superseded descriptor byte-exactly; generation 2 retains the b18971e predecessor
  and its exact suffix, which begins with the first pointer; the publisher accepts
  exactly one new generation per transition and freezes every earlier object.
- [x] **ADDRESSED (verified)** — python3 scripts/artifact_task_history.py:
  CLEANUP-TASK-HISTORY: 2 generations; 2724 live narrative bytes; within
  health target. python3 -B scripts/probe_artifact_task_history.py: 45 tests
  / 0 failures / 0 errors normal/O; 20 omissions each 1 failures / 0 errors.
- [x] **NO REGRESSION** — bash scripts/check_task_history.sh --self-test rc=0:
  TASK-HISTORY --self-test: 52 pass / 0 fail; focused checks rc=0; seven books.
- [x] **LOCKSTEP** — descriptor/front/objects; registry row re-derived under this
  leaf (6 files / 192,801 B, per-part 76,937); toolbox/doctrine/book, tree/index/
  MEM/DEV/CH; both history heads within ceilings.
- **ROUTING EVIDENCE** — a decision record for the row was drafted and withdrawn:
  bash scripts/check_readme_routes.sh with only its index row added reports
  OVER CEILING docs/decisions/: 262242 aggregate bytes > 262144 (61 files, health
  163,840, no registered owner). The pressure reproduces with no cleanup file
  involved, so LIVE-CONTAINMENT.4 slice (k) owns the family's re-derivation or
  partition; the routing is wrong only if that family already had an owner.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-26` UTC | `.27` | plan/select/delete/inspect on the real tree; receipt complete/verified; census against AC0083 | 6 of 253 candidates removed (15,766,335 B), residue 0, 247 unrecorded (83 orphan sessions, grown) and 20,071 retained kept |
| `2026-10-23` UTC | `.26` | plan/select/delete/inspect on the real tree; receipt complete/verified | 6 of 73 candidates removed (15,766,468 B), residue 0, 67 unrecorded and 19,342 retained kept |
| `2026-10-22` UTC | `.25` | plan/select/delete/inspect on the real tree; receipt complete/verified | 6 of 73 candidates removed (15,766,472 B), residue 0, 67 unrecorded and 18,995 retained kept |
| `2026-10-20` UTC | `.24` | plan/select/delete/inspect on the real tree; receipt complete/verified | 6 of 19 candidates removed (15,766,463 B), residue 0, 13 unrecorded and 18,724 retained kept |
| `2026-10-20` UTC | `.14` | operator 10 tests normal/O; 3 omissions; artifact146 | census bound before the core; receipts truthful; activity closed |
| `2026-10-20` UTC | `.16` | guarded 12 tests normal/O; 4 omissions; journal 29/11; planner 27; artifact138 | fixture unlinks exact, journaled and verified; D14 fixed; dry-run only public |
| `2026-10-20` UTC | `.17` | selection 11 tests normal/O; 5 omissions; artifact128; actual select | 9 approved / 10 unrecorded on the real tree; D12/D13 fixed; P1 closed |
| `2026-10-20` UTC | `.23` | 45 tests normal/O; 20 omissions; TASK-HISTORY self-test; focused | generation 2 exact; chain re-derives the superseded descriptor; live narrative 2724 B |

## Commit Log

`SEMULITH-AC-0084 (leaf ARTIFACT-CLEANUP.27): the fourth recurring cleanup through the supported act` — 6 captured outputs removed under a fresh census, journaled and verified; record overwritten; the unrecorded population grew to 83 orphan sessions, the deferral ends, three options for the director.

`SEMULITH-AC-0083 (leaf ARTIFACT-CLEANUP.26): the third recurring cleanup through the supported act` — 6 captured outputs removed under a fresh census, journaled and verified; record overwritten; the unrecorded residue measured stable at 67.

`SEMULITH-AC-0082 (leaf ARTIFACT-CLEANUP.25): the second recurring cleanup through the supported act` — 6 captured outputs removed under a fresh census, journaled and verified; record overwritten; the unrecorded mutation-build residue measured as an open question.

`SEMULITH-AC-0081 (leaf ARTIFACT-CLEANUP.24): the first recurring cleanup through the supported act` — 6 captured outputs removed under a fresh census, journaled and verified; record overwritten.

`SEMULITH-AC-0080 (leaf ARTIFACT-CLEANUP.14): bind the host census into the supported cleanup act` — operator act, receipts, recovery; priority1 activity closed; .24 next when due.

`SEMULITH-AC-0079 (leaf ARTIFACT-CLEANUP.16): unlink only what plan, selection and journal agree on` — guarded core, journal v2, D14; .14 operator act next.

`SEMULITH-AC-0078 (leaf ARTIFACT-CLEANUP.17): select strictly against the published ledger` — selection record beside the plan, D12/D13 fixed, P1 closed; .16 guarded core next.

`SEMULITH-AC-0077 (leaf ARTIFACT-CLEANUP.23): retire the completed-checklist suffix into a second ledger generation` — chain-verified transition; .17 strict selection next.

## Changelog

- `2026-10-26` UTC: .27 done; fourth cleanup event through the act, 6 outputs removed, record overwritten; the unrecorded population grew to 83 orphan sessions (770,724,553 B), the open question's deferral ends.
- `2026-10-23` UTC: .26 done; third cleanup event through the act, 6 outputs removed, record overwritten; the 67 unrecorded sessions are a stable set.
- `2026-10-22` UTC: .25 done; second cleanup event through the act, 6 outputs removed, record overwritten; 67 unrecorded sessions measured.
- `2026-10-20` UTC: .24 done; first cleanup event through the act, 6 outputs removed, record overwritten.
- `2026-10-20` UTC: .14 verified; the supported act binds a fresh host census before the guarded core; activity closed.
- `2026-10-20` UTC: .16 verified; guarded core and selection-bound journal land, dry-run only; no operator deletion yet.
- `2026-10-20` UTC: .17 verified; strict selection publishes beside the plan; no deletion authority added.
- `2026-10-20` UTC: .23 verified; second ledger generation retained, live narrative reset. No cleanup authority changed.
