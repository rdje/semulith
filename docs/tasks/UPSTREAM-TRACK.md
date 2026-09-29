# UPSTREAM-TRACK: defects we raise against our dependencies, tracked like our own

## Metadata

- Tree ID: `UPSTREAM-TRACK`
- Status: `done` (4/4 leaves complete `2026-09-29`; `.3` derived the exposure figure and
  closed the tree)
- Roadmap lane: cross-cutting; the discipline spine pointed outward
- Gate: contributes `UPSTREAM-INDEX` — the indices mirror the issues, checked not trusted
- Depends on: `docs/upstream/` (created by `SOT-FORMAT.9`)
- Unlocks: adopting a dependency's fix on evidence rather than on its changelog
- Created: `2026-09-20`
- Owner: repo-local workflow

## Goal

A defect found in a dependency is **work this project owns** until it is verified fixed. Track it
with the same discipline as our own: an id, a state, a dated history, and an index that cannot
silently disagree with the issues it lists.

Director, `2026-09-20`: *"For each vendor you should keep an index of all the bugs you reported,
their state, ..."* and *"The subtree for each bug reported shall be self-contained."*

⭐ Those two requirements are one design. If each subtree is self-contained it must carry its own
state; and if it carries its own state, then **every index is derived** and must be checked rather
than believed. That is the same shape `FRONTIER-SYNC` and `REGISTRY-MIRROR` already enforce
inwards, applied outwards.

⛔ Measured before building: the same facts are currently stated in **three** places — the top
index, the vendor index, and each `REPORT.md` — and `grep -c upstream scripts/check_doctrines.project.sh`
is `0`. Nothing checks they agree. That is exactly how `MIRROR-DRIFT` began.

## Non-Goals

- Not a replacement for the upstream's own tracker. Their issue system is authoritative for *their*
  work; this one records **our** exposure and what we verified.
- Not a place for opinions about a dependency. An issue lands only when it is reproducible from
  the files beside it.
- Not a workflow for issues raised *against* this project — those are task-tree leaves.

## Acceptance Criteria

1. **One owner per fact.** An issue's id, title, severity, state and history live in exactly one
   file; every index and every prose table is checked against it.
2. **Self-contained, mechanically.** No file inside an issue subtree may reference anything outside
   that subtree, and the check proves it rather than asserting it — a maintainer copies the
   directory out and it still works.
3. An index row with no issue, or an issue with no index row, is a **breach**, not a warning.
4. A state outside the declared vocabulary is refused; so is a `verified` with no re-run evidence.
5. Every state change is dated, so "how long has upstream had this" is answerable.

## Task Tree

- ID: `UPSTREAM-TRACK.1` — **the issue owns its state; the indices are checked against it**
  Status: `done`
  Goal: give each issue a machine-readable record in its own subtree, make both indices mirrors of
  those records, and gate the mirroring. Prove self-containment rather than claiming it.
  Acceptance: `UPSTREAM-INDEX` registered in `scripts/check_doctrines.project.sh` with a
  `--self-test` fired RED before registration; ≥ 10 arms; an issue subtree referencing a path
  outside itself is refused; both indices agree with every issue record or the commit is blocked.
  Verification: `12 pass / 0 fail`, 10 arms RED; the gate caught 3 real self-containment
  violations in the tracker it was written for.
  Commit: `SEMULITH-UT-0048`

- ID: `UPSTREAM-TRACK.2` — **a `verified` state must carry the re-run that earned it**
  Status: `done`
  Goal: `fixed-upstream` → `verified` is the transition where a consumer inherits a regression if
  it is taken on trust. Require the evidence in the record: the new pin, the date, and the
  reproduction output.
  Acceptance: a record claiming `verified` without a pin and a captured re-run is refused; fired
  RED on exactly that.
  Verification: `16 pass / 0 fail` (12 → 16 arms: pin-without-repro, missing artifact, escaping
  artifact refused, pin+artifact accepted); the strengthened gate fired RED on the REAL LS-001
  record — verified with a pin but no captured output — before the artifact landed; all three
  issues then earned their states: LS-001 `verified` (repro 8/0 captured),
  LS-003 `verified` (guide remedies exercised, transcript captured), LS-002 `acknowledged`
  (upstream `.83.1 owned`).
  Commit: `SEMULITH-UT-0052`

- ID: `UPSTREAM-TRACK.3` — **age and exposure, derived**
  Status: `done` (`2026-09-29`)
  Goal: from the dated history, derive how long each open issue has been reported and which of our
  leaves it blocks, so exposure is visible without reading every record.
  Acceptance: the figure is derived by a command, never typed; `DERIVED-COUNTS` owns it.
  Design (recorded before code, `2026-09-29`):
  - **The linkage data already exists, ungated.** Every record carries `(blocks …)`
    (LS-001: "SOT-FORMAT.9"; LS-002/LS-003: empty) — written at `.1`, never checked. The
    gate upgrades it, which is the leaf's honest core: `blocks` becomes REQUIRED, and every
    non-empty entry must name a leaf id that EXISTS in `docs/tasks/` — a dangling
    exposure is a lie about what is blocked. (An id is data, not a path: the
    self-containment rule is untouched.) New self-test arms, RED-first per the `.2`
    pattern.
  - **The command** is `scripts/upstream_exposure.py`: for each issue record — id,
    project, state, age in days (earliest dated history event → TODAY, derived at run
    time; LIVE-DOC-CURRENCY forbids a tracked document carrying the figure), and its
    blocks. Open = `draft | reported | acknowledged | disputed | fixed-upstream`;
    `verified | closed | wontfix` are resolved (verified means WE re-ran it — the `.2`
    discipline). `--open-count` prints just the count. Self-test with fixture records.
  - **DERIVED-COUNTS owns the figure**: a new claim row (`open upstream issues`,
    enumerator `python3 scripts/upstream_exposure.py --open-count`), and MEMORY.md's
    Blockers line carries the claim so the gate re-derives it on every commit.
  - **The indices do NOT gain an age/exposure column** — age changes daily, and a typed
    figure in a tracked surface is exactly what LIVE-DOC-CURRENCY and the
    generated-or-gated rule refuse. The command IS the deliverable.
  - **Tree closure:** criterion 5 ("every state change is dated, so 'how long has
    upstream had this' is answerable") is what this leaf turns from answerable-in-
    principle into derived-by-a-command; criteria 1–4 landed at `.1`/`.2`/`.4`. With
    `.3` the tree closes at 4/4.
  Result: met, `2026-09-29`. **Age and exposure are derived by a command, and
  DERIVED-COUNTS owns the open-issue count.** `scripts/upstream_exposure.py` reads every
  issue record and derives, at run time: state, age in days from the earliest dated
  history event (9d for all three today), and the `blocks` exposure — printing
  `0 open / 3 resolved / 3 tracked` today, with an honest "no open issues" line when the
  open set is empty (self-test 5/0, including the fully-resolved fixture). The
  `UPSTREAM-INDEX` gate learned the field: `blocks` is now REQUIRED, and every entry must
  name a leaf that exists in `docs/tasks/` (DANGLING BLOCKS) and have the leaf-id shape
  (BAD BLOCKS) — self-test 17 → 21 arms, all RED named. DERIVED-COUNTS gained the
  `open upstream issues` claim (enumerator `… --open-count`), and MEMORY.md's Blockers
  line carries it, re-derived every commit. **Defect found in flight, owned:** the
  pre-existing `self-test arms` claim matched NO live document — its pattern
  (`([0-9]+) self-test arms`) never matched LIVE_STATUS.md's "N arms" wording, so the
  arms figure had never actually been re-derived and was silently stale (280 carried vs
  291 real after this leaf's +4 gate arms). Fixed in the document (the claim now reads
  "291 self-test arms"), not in the gate: DERIVED-COUNTS went from re-deriving 3 claims
  to 5 — the new one AND the arms claim, live for the first time. A second fixture
  defect, mine: the self-test's record-editing helper truncated each file before reading
  it (`open(p, "w").write(open(p).read()…)` — evaluation order), so four arms edited
  empty files; fixed (read first, then write). Tree closure: criteria 1–3 landed at `.1`,
  criterion 4 at `.2` (`.4` strengthened it), criterion 5 — dated history, answerable —
  is this leaf's derived figure. **The tree closes at 4/4.**
  Lessons: `promotion: declined (both defects are recorded where they bite: the arms claim's wording in LIVE_STATUS.md, the fixture fix in the gate's self-test)`.

- ID: `UPSTREAM-TRACK.4` — **the consumer tells upstream: `VERIFIED.md` lives in the issue subtree**
  Status: `done`
  ⭐ Director instruction, `2026-09-26`: the verification acknowledgment to LinkedSpec is a
  git-tracked note inside the bug's own directory, for the upstream maintainer to read in place.
  The subtree is already the envelope a maintainer copies out — the reply travels in the same
  envelope as the report it answers.
  Goal: a `verified` issue carries `VERIFIED.md` beside `REPORT.md` — addressed upstream: what
  shipped, what we re-ran against which pin, the result, what it unblocks, and where the residue
  (if any) is classified. The `UPSTREAM-INDEX` gate requires the note for every `verified` state
  and checks it names the same pin as the record, so the note cannot drift or be forgotten.
  Acceptance: `VERIFIED.md` exists for both currently verified issues (LS-001, LS-003), is
  self-contained (nothing outside the subtree), and names the `verified-against` pin; the gate
  refuses a `verified` without the note and a note whose pin disagrees with the record — fired
  RED on the missing-note state before the notes landed; self-test arms for both refusals.
  Verification: `2026-09-26` — 17 pass / 0 fail; the strengthened gate fired RED on the real
  LS-001 and LS-003 ("carries no VERIFIED.md") before the notes existed; green after, with both
  notes naming the record's pin.
  Commit: `SEMULITH-UT-0055`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | the tree is complete (4/4 leaves done): the issue owns its state (`.1`), `verified` earns its evidence (`.2`), age and exposure are derived (`.3`), and the consumer's reply travels in the subtree (`.4`, out of order on director instruction) |

## Acceptance Checklist (leaf UPSTREAM-TRACK.3)

- [x] **ROOT CAUSE (WHY + WHERE)** — the figure existed only as dated records nobody
  read end to end, and the exposure linkage existed but was never gated: `blocks` was
  written at `.1` and checked by nothing. Measured at the pre-leaf state:

  ```
  $ git show HEAD:scripts/check_upstream_index.sh | grep -c blocks   -> 0
  $ git show HEAD:scripts/check_derived_counts.sh | grep -c upstream -> 0
  ```

- [x] **ADDRESSED (verified)** — the command derives; the gate requires; DERIVED-COUNTS
  owns:

  ```
  $ python3 scripts/upstream_exposure.py
  upstream exposure — derived from the dated issue records, never typed
    no open issues — nothing upstream blocks any leaf today
    resolved LS-001   linkedspec   state verified       reported 2026-09-20 (9d ago)
    resolved LS-002   linkedspec   state verified       reported 2026-09-20 (9d ago)
    resolved LS-003   linkedspec   state verified       reported 2026-09-20 (9d ago)
  upstream exposure: 0 open / 3 resolved / 3 tracked
  $ python3 scripts/upstream_exposure.py --self-test -> 5 pass / 0 fail
  $ bash scripts/check_upstream_index.sh --self-test -> 21 pass / 0 fail (17 → 21 arms:
    GREEN a real leaf; RED dangling / bad shape / missing field)
  $ bash scripts/check_derived_counts.sh
  DERIVED-COUNTS: ok (5 derived count claim(s) re-derived)     ← was 3: see the defect
  ```

- [x] **NO REGRESSION** — the strengthened gate on the real tracker, and the whole
  registry:

  ```
  $ bash scripts/check_upstream_index.sh
  UPSTREAM-INDEX: ok (3 issue record(s) mirrored by both indices)
  $ make gate
  === all doctrines green ===
  ```

  ⛔ Defect found in flight, owned: the pre-existing `self-test arms` claim in
  DERIVED-COUNTS matched NO live document (`([0-9]+) self-test arms` vs LIVE_STATUS's
  "N arms"), so the arms figure was never re-derived and read 280 where the registry
  measured 291. Fixed in the document (the claim now reads "291 self-test arms"), never
  in the gate — the gate went from re-deriving 3 claims to 5. A second defect, mine:
  the self-test's record-edit helper truncated before reading
  (`open(p,"w").write(open(p).read()…)` — evaluation order), so four new arms first ran
  against empty files; fixed (read, then write).

- [x] **LOCKSTEP** — same commit: `MEMORY.md` (tree done, out of the active list; the
  Blockers line carries the derived claim), `LIVE_STATUS.md` (27 doctrines / 291
  self-test arms), `CHANGELOG.md`, `DEV_NOTES.md`, `docs/TASK_TREE.md` (the row → done),
  this tree (status done, frontier —), `TOOLBOX.md` (the command's row).

## Acceptance Checklist (leaf UPSTREAM-TRACK.2)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. The `verified` check named a pin but not the output:

  ```
  $ bash scripts/check_upstream_index.sh   (after the pin update, before this leaf)
  UPSTREAM-INDEX: ok (3 issue record(s) mirrored by both indices)     ← the hole
  ```

  WHY a pin alone is not evidence: the pin retires upstream's changelog claim, but OUR claim —
  "we re-ran it and it passed" — still rested on the event's prose. A maintainer copying the
  subtree out carried an assertion, not the run.

- [x] **ADDRESSED (verified)** — leg 2. `scan()` now requires, for every `verified` record, a
  `(repro "…")` in the verified event naming a file that EXISTS inside the subtree:

  ```
  $ bash scripts/check_upstream_index.sh --self-test
  UPSTREAM-INDEX --self-test: 16 pass / 0 fail
    (4 new arms, all RED-named: pin-but-no-repro, repro-missing, repro-escaping, pin+repro ok)
  $ bash scripts/check_upstream_index.sh        # against the real tracker, artifact not yet written
    UNEARNED  LS-001: `verified` names a pin but captures no (repro …) re-run output
    rc=1                                          ← fired RED on the real record, not just fixtures
  ```

  Then the artifacts landed and every state became earned: LS-001 `verified` with
  `evidence/verified-a8d34c845.txt` (the captured `8 matched / 0 differed`), LS-003 `verified`
  with its exercised-remedies transcript, LS-002 `acknowledged` (no re-run owed — upstream owns
  the design question).

- [x] **NO REGRESSION** — leg 3.

  ```
  $ bash scripts/check_upstream_index.sh -> ok (3 issue record(s) mirrored by both indices)
  $ python3 scripts/compare_readers.py --self-test -> 21 pass / 0 fail
  $ bash scripts/check_doctrines.sh -> all doctrines green
  ```

- [x] **LOCKSTEP** — both index mirrors and all three REPORT.md tables carry the new states in
  the same commit; MEMORY/TASK_TREE counts re-derived; CHANGELOG entry.

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
| `2026-09-20` | The issue subtree owns its state; indices are derived | director: subtrees are self-contained. Self-containment and a second source of truth cannot both hold |
| `2026-09-20` | The machine-readable record is an S-expression | `decision_one-format-every-source-of-truth` — an issue record is a source of truth like any other |
| `2026-09-20` | `REPORT.md` keeps its human-readable table, checked against the record | a maintainer who opens the report must see the state there; checking beats removing |
| `2026-09-20` | `fixed-upstream` and `verified` stay distinct states | a fix we have not re-run is a claim; adopting a pin on a changelog entry is how a consumer inherits a regression |

## Open Questions

- Should a closed issue's subtree be archived out of the active index? Not until one closes —
  designing an archive for zero items is how ceilings get miscalibrated.

## Blockers

- None.

## Acceptance Checklist (leaf UPSTREAM-TRACK.1 — done `2026-09-20`, kept as evidence)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1. WHERE: nowhere yet, and that is the finding. The same
  facts were stated in three places with nothing checking them:

  ```
  $ grep -c 'LS-00' docs/upstream/README.md                    -> 4   rows
  $ grep -c 'LS-00' docs/upstream/linkedspec/README.md         -> 5   rows
  $ grep -l 'State' docs/upstream/linkedspec/*/REPORT.md | wc -l -> 3  reports
  $ grep -c upstream scripts/check_doctrines.project.sh        -> 0   gates
  ```

  WHY it matters now rather than later: the two director instructions — *"keep an index of all the
  bugs, their state"* and *"the subtree for each bug shall be self-contained"* — are one design.
  A self-contained subtree must carry its own state, and the moment it does, **every index is a
  derived mirror**. An unchecked mirror drifts; that is the whole reason `FRONTIER-SYNC` and
  `REGISTRY-MIRROR` exist facing inwards.

- [x] **ADDRESSED (verified)** — leg 2. Each issue now carries `issue.sexp` as the single owner of
  its id, severity, state, affected pins, fix status and dated history. `UPSTREAM-INDEX` checks
  both indices and each `REPORT.md` against it, in both directions:

  ```
  $ bash scripts/check_upstream_index.sh
  UPSTREAM-INDEX: ok (3 issue record(s) mirrored by both indices)
  $ bash scripts/check_upstream_index.sh --self-test
  UPSTREAM-INDEX --self-test: 12 pass / 0 fail
  ```

  ⛔ **It caught real violations in the tracker I had just written**, which is the only evidence
  worth having that a gate discriminates:

  ```
  NOT CONTAINED LS-001: …/evidence/patched.txt:1 references '/Volumes/' — outside its own subtree
  NOT CONTAINED LS-001: …/evidence/shipped.txt:1 references '/Volumes/' — outside its own subtree
  NOT CONTAINED LS-001: …/issue.sexp:4 references 'scripts/' — outside its own subtree
  ```

  All three were genuine: a maintainer copying the directory out would have got a machine path
  from my disk and a pointer to this repository's tooling. Fixed in the content, not the gate.

  Ten of the twelve arms are RED, each naming its own reason: stale state in an index, stale
  severity, an issue with no row, a row with no issue, an invented state, an invented severity, a
  directory with no record, a `REPORT.md` disagreeing with the record beside it, a file pointing
  outside its subtree, a `verified` claim with no pin, and a directory whose name does not carry
  its id.

  ⛔ Three arms were fired RED and **failed for the wrong reason first** — the fixture computed
  `${1%%-*}` on `LS-001-a` and got `LS`, not `LS-001`. The fixture was wrong, not the gate; fixing
  the fixture is what turned 8/12 into 12/12. And the gate itself exited 1 printing **nothing**
  until `set -e` was stopped from aborting before `rc` could be read: a breach with no reason is
  indistinguishable from a crash.

- [x] **NO REGRESSION** — leg 3.

  ```
  $ python3 scripts/compare_readers.py | tail -1   -> compare_readers: 4 of 5 file(s) agree
  $ python3 scripts/materials.py --self-test       -> 20 pass / 0 fail
  $ python3 scripts/sexp.py --self-test            -> 18 pass / 0 fail
  $ bash scripts/check_doctrines.sh                -> all doctrines green
  ```

- [x] **LOCKSTEP** — `UPSTREAM-INDEX` registered in `scripts/check_doctrines.project.sh`, mirrored
  into `DOCTRINE_ENFORCEMENT.md` and the mdBook chapter (both checked by `REGISTRY-MIRROR`);
  `LIVE_STATUS.md` counts re-derived, never incremented. ⚠️ `README-ROUTING-CLOSURE` fired on the
  way through — `docs/tasks/` crossed its aggregate ceiling by 3,057 bytes — and it is raised
  under [`decision_task-tree-family-bound`](../decisions/decision_task-tree-family-bound.md),
  which records the two rejected alternatives and leaves the per-part bound untouched.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-29` | `UPSTREAM-TRACK.3` | pre-change census at HEAD | `check_upstream_index.sh` carried 0 mentions of `blocks`; `check_derived_counts.sh` carried 0 upstream claims — the field and the figure were ungated |
| `2026-09-29` | `UPSTREAM-TRACK.3` | `upstream_exposure.py [--self-test]` | `0 open / 3 resolved / 3 tracked`, ages 9d derived from the dated histories; self-test 5/0 (incl. the honest zero) |
| `2026-09-29` | `UPSTREAM-TRACK.3` | `check_upstream_index.sh --self-test` | 21 pass / 0 fail (17 → 21 arms: blocks required, DANGLING BLOCKS, BAD BLOCKS, missing field) |
| `2026-09-29` | `UPSTREAM-TRACK.3` | authoring RED moments | the fixture's edit helper truncated before reading (4 arms edited empty files — 13/8 became 21/0 after the fix); DERIVED-COUNTS' arms claim found dead (matched no live doc; arms figure stale 280 vs 291) — fixed in the document, not the gate |
| `2026-09-29` | `UPSTREAM-TRACK.3` | `check_derived_counts.sh`; `make gate` | 5 derived count claims re-derived (was 3 — the arms claim is live for the first time, plus the new open-issues claim); all doctrines green |
| `2026-09-26` | `UPSTREAM-TRACK.4` (regime) | LS-002 ancestry claim checked mechanically | `merge-base --is-ancestor`: `77d7b3db1` and `df845ce61` both in `a8d34c845` — upstream's claim verified, not trusted |
| `2026-09-26` | `UPSTREAM-TRACK.4` (regime) | LS-002 cases re-run with the prescribed instrument (`sexpr_file` + `SExprDocumentV1.spec`) | all four quoted/bare pairs distinguishable by kind; transcript captured in the subtree |
| `2026-09-26` | `UPSTREAM-TRACK.4` (regime) | LS-002 state `acknowledged` → `verified` | record, REPORT, VERIFIED.md and both index mirrors in one commit; gate green |
| `2026-09-26` | `UPSTREAM-TRACK.4` | `--self-test` after the gate extension | `17 pass / 0 fail` (16 → 17 arms: the wrong-pin note refused) |
| `2026-09-26` | `UPSTREAM-TRACK.4` | the gate on the real tracker BEFORE the notes | `UNANNOUNCED LS-001`, `UNANNOUNCED LS-003`, rc=1 — fired RED on the exact state the leaf exists to refuse |
| `2026-09-26` | `UPSTREAM-TRACK.4` | `VERIFIED.md` written for LS-001 and LS-003 | self-contained, addressed upstream, each names the record's `verified-against` pin |
| `2026-09-26` | `UPSTREAM-TRACK.4` | the gate after the notes | `ok (3 issue record(s) mirrored by both indices)` |
| `2026-09-26` | `UPSTREAM-TRACK.2` | `--self-test` after hardening | `16 pass / 0 fail` (12 → 16 arms) |
| `2026-09-26` | `UPSTREAM-TRACK.2` | the gate on the real tracker BEFORE the artifact | `UNEARNED LS-001 … captures no (repro …)`, rc=1 — the exact failure the leaf exists to refuse |
| `2026-09-26` | `UPSTREAM-TRACK.2` | LS-001 repro re-captured into its subtree | `evidence/verified-a8d34c845.txt`: `8 matched / 0 differed` |
| `2026-09-26` | `UPSTREAM-TRACK.2` | LS-003 remedies exercised at the new pin | transcript captured; bootstrap no-op by exit status, build 20.39 s, sweep 5/5 |
| `2026-09-26` | `UPSTREAM-TRACK.2` | LS-002 acknowledgment | upstream `8259719f8`: "LS-002 … remains .83.1 owned" |
| `2026-09-26` | `UPSTREAM-TRACK.2` | the gate after the artifacts | `ok (3 issue record(s) mirrored by both indices)` |
| `2026-09-20` | `UPSTREAM-TRACK.1` | census: places stating an issue's facts / gates checking them | 3 places / `0` gates |
| `2026-09-20` | `UPSTREAM-TRACK.1` | `--self-test`, first run | `8 pass / 4 fail` — the FIXTURE was wrong, not the gate |
| `2026-09-20` | `UPSTREAM-TRACK.1` | `--self-test`, after the fixture fix | `12 pass / 0 fail`, 10 of them RED |
| `2026-09-20` | `UPSTREAM-TRACK.1` | the gate on the real tracker, first run | 3 × `NOT CONTAINED` — genuine, in content I had just written |
| `2026-09-20` | `UPSTREAM-TRACK.1` | the gate after sanitising evidence and record | `ok (3 issue record(s) mirrored by both indices)` |
| `2026-09-20` | `UPSTREAM-TRACK.1` | self-containment, by copying a subtree out and running it | identical output outside the repository |
| `2026-09-20` | `UPSTREAM-TRACK.1` | regression: readers, materials, sexp, doctrines | 4 of 5, 20/0, 18/0, all green |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `UPSTREAM-TRACK.3` | `SEMULITH-UT-0053 (leaf UPSTREAM-TRACK.3): …` | age and exposure derived by `upstream_exposure.py`; the gate requires `blocks` and validates the named leaves exist; DERIVED-COUNTS owns the open-issue count (and its arms claim is live for the first time — a dead-claim defect found in flight); the tree CLOSES 4/4 |
| `UPSTREAM-TRACK.4` | `SEMULITH-UT-0055 (leaf UPSTREAM-TRACK.4): …` | VERIFIED.md in the issue subtree for both verified issues; gate requires the note and the pin match |
| `UPSTREAM-TRACK.2` | `SEMULITH-UT-0052 (leaf UPSTREAM-TRACK.2): …` | verified now requires the captured re-run; fired RED on the real LS-001; all three issues in earned states |
| `UPSTREAM-TRACK.1` | `SEMULITH-UT-0048 (leaf UPSTREAM-TRACK.1): the issue owns its state, the indices are mirrors` | caught 3 real violations in its own tracker |

## Changelog

- `2026-09-20`: Created on two director instructions that turn out to be one design — a
  self-contained subtree cannot also be indexed by a second source of truth.
- `2026-09-29`: Leaf `.3` done and **the tree closes** (4/4): age and exposure are derived
  by `scripts/upstream_exposure.py` from the dated records (never typed); the
  `UPSTREAM-INDEX` gate now requires the `blocks` field and refuses an exposure naming a
  leaf no tree declares; `DERIVED-COUNTS` owns the open-issue count — and its `self-test
  arms` claim, found dead in flight (it matched no live document), is live for the first
  time.
