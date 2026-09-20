# UPSTREAM-TRACK: defects we raise against our dependencies, tracked like our own

## Metadata

- Tree ID: `UPSTREAM-TRACK`
- Status: `active`
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
  Status: `pending`
  Goal: `fixed-upstream` → `verified` is the transition where a consumer inherits a regression if
  it is taken on trust. Require the evidence in the record: the new pin, the date, and the
  reproduction output.
  Acceptance: a record claiming `verified` without a pin and a captured re-run is refused; fired
  RED on exactly that.

- ID: `UPSTREAM-TRACK.3` — **age and exposure, derived**
  Status: `pending`
  Goal: from the dated history, derive how long each open issue has been reported and which of our
  leaves it blocks, so exposure is visible without reading every record.
  Acceptance: the figure is derived by a command, never typed; `DERIVED-COUNTS` owns it.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `UPSTREAM-TRACK.2` | `pending` | the transition that matters is the one nobody wants to slow down |
| 2 | `UPSTREAM-TRACK.3` | `pending` | derivation is only worth building once there is history to derive from |

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

## Acceptance Checklist (current leaf — `UPSTREAM-TRACK.1`)

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
| `UPSTREAM-TRACK.1` | `SEMULITH-UT-0048 (leaf UPSTREAM-TRACK.1): the issue owns its state, the indices are mirrors` | caught 3 real violations in its own tracker |

## Changelog

- `2026-09-20`: Created on two director instructions that turn out to be one design — a
  self-contained subtree cannot also be indexed by a second source of truth.
