# PREFIX-DISCIPLINE: the work-unit prefix is SEMULITH, never SEMILITH

## Metadata

- Tree ID: `PREFIX-DISCIPLINE`
- Status: `done` (`2026-09-30` — opened and closed the same day: the ruling, the pin, the watcher)
- Roadmap lane: cross-cutting traceability; session-directive §4 (`COMMIT.md`) — the work-unit
  id in every commit subject
- Gate: `COMMIT-PREFIX` (project doctrine, registered by `.1`)
- Created: `2026-09-30`
- Owner: repo-local workflow

## Goal

The director ruled `2026-09-30`: the work-unit prefix is **SEMULITH, never SEMILITH**. The
drift is real and measured: 123 commits at ruling time carry both spellings
(`SEMILITH-PL` ×13, `SEMILITH-PS` ×8, `SEMILITH-MM` ×8, `SEMILITH-MB` ×8, `SEMILITH-SF` ×5,
`SEMILITH-MC` ×4, `SEMILITH-AC` ×3, … alongside the correct `SEMULITH-*` majority; exactly one
commit, the initial one, carries neither). Commit subjects are immutable history — nothing
retroactive is fixable — so the doctrine's object is the **boundary where new subjects enter**:
the `commit-msg` hook refuses any leading work-unit id that does not begin with `SEMULITH-`.

## Non-Goals

- **Never rewriting history.** The misspelled subjects stay; they are the measurement that
  justified the pin.
- **Not a shape gate.** The hook stays permissive by design about the id's shape; this tree
  pins the PREFIX only — the one thing the director ruled on.
- **Not a gate over past commits.** A scan of history would fail on the immutably recorded
  drift forever; enforcement is forward-looking at the boundary.

## Acceptance Criteria

1. `.githooks/commit-msg` refuses a subject whose leading work-unit id does not begin with
   `SEMULITH-`, and the refusal names `SEMULITH`; a `SEMULITH-` subject passes.
2. `COMMIT-PREFIX` is registered in `scripts/check_doctrines.project.sh` with a `--self-test`
   whose RED arms were observed failing — including once against the REAL tree before the pin
   existed (a control never seen RED is not known to work).
3. Both registry mirrors (`DOCTRINE_ENFORCEMENT.md`, `docs/book/src/working/doctrines.md`)
   carry the row (REGISTRY-MIRROR green), and LIVE_STATUS's derived counts are restated.
4. The ruling is a decision record in `docs/decisions/` with its INDEX entry, and `COMMIT.md`
   states the pinned prefix.
5. The whole enforcer is green after the commit.

## Task Tree

- ID: `PREFIX-DISCIPLINE`
  Status: `done`
  Goal: the work-unit prefix is SEMULITH — pinned at the boundary, watched by a doctrine
  Children: `PREFIX-DISCIPLINE.1`

- ID: `PREFIX-DISCIPLINE.1` — **the pin, its watcher, and the decision record**
  Status: `done`
  Goal: the commit-msg hook pins `SEMULITH-`; `COMMIT-PREFIX` probes the hook BEHAVIOURALLY
  (a scaffold sync that reverts the neutral hook turns the next commit RED, named); the
  ruling is recorded as a decision; `COMMIT.md` states the prefix.
  Design (recorded before code, `2026-09-30`): the pin lives in a NEUTRAL scaffold file —
  `scripts/update_scaffold.sh` syncs `.githooks/commit-msg` from the spine, and carrying the
  fix upstream is unavailable by policy (§21: other repositories are read-only). This is the
  same exposure as the repaired spine defects (`check_task_acceptance.sh`, watched by
  SEAM-INTEGRITY), and the answer is the same shape: the local pin plus a project doctrine
  whose functional probe makes a silent revert loud. The probe judges what the hook DOES
  (run on synthetic messages), never what it says — prose is not code.
  Acceptance: as the tree's criteria 1–5.
  Verification: `2026-09-30` — all in the Acceptance Checklist and Verification Log below;
  the watcher fired RED against the real tree before the pin existed.
  Commit: `SEMULITH-PX-0001`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | `.1` done `2026-09-30` — the tree closes 1/1; the pin and its watcher carry the ruling from here |

## Decisions

- `2026-09-30`: the prefix is SEMULITH, never SEMILITH — director ruling, recorded in
  [`decision_work-unit-prefix-semulith`](../decisions/decision_work-unit-prefix-semulith.md).
- `2026-09-30`: the enforcement point is the `commit-msg` hook, not a history scan — past
  subjects are immutable, so the doctrine watches the boundary where new ones enter.

## Open Questions

- None.

## Blockers

- None.

## Acceptance Checklist (leaf PREFIX-DISCIPLINE.1)

- [x] **ROOT CAUSE (WHY + WHERE)** — the prefix drifted because nothing refused the
  misspelling: the neutral hook checked identifier-shape only. WHERE, measured over the full
  history at ruling time (123 commits):

  ```
  $ git log --format='%s' | grep -oE '^[A-Za-z][A-Za-z0-9._-]*' | sed 's/-[0-9]*$//' | sort | uniq -c | sort -rn
       13 SEMILITH-PL
       12 SEMULITH-P0
       12 SEMULITH-MM
        8 SEMULITH-PKG
        8 SEMILITH-PS
        8 SEMILITH-MM
        8 SEMILITH-MB
        …
  $ git log --format='%s' | grep -vcE '^(SEMULITH|SEMILITH)-'
  1            # "Initial commit" — the only subject without a work-unit id
  ```

- [x] **ADDRESSED (verified)** — the hook now refuses `SEMILITH-` naming `SEMULITH`, and
  accepts `SEMULITH-` — probed live, both directions:

  ```
  $ printf 'SEMILITH-AC-0055 (tree ARTIFACT-CLEANUP): a misspelled probe\n' > target/doctrine_scratch/msg-bad
  $ bash .githooks/commit-msg target/doctrine_scratch/msg-bad ; echo rc=$?
  commit-msg: the work-unit id must begin with the pinned project prefix 'SEMULITH-' (never SEMILITH-)
    got: SEMILITH-AC-0055 (tree ARTIFACT-CLEANUP): a misspelled probe
  rc=1
  $ bash .githooks/commit-msg target/doctrine_scratch/msg-good ; echo rc=$?
  rc=0
  $ bash scripts/check_commit_prefix.sh
  COMMIT-PREFIX: ok (the hook refuses SEMILITH- naming SEMULITH, accepts SEMULITH-)
  ```

- [x] **NO REGRESSION** — the watcher fired RED against the REAL tree before the pin existed
  (a control never seen RED is not known to work); its self-test discriminates every fixture;
  the whole enforcer re-ran green after staging:

  ```
  $ bash scripts/check_commit_prefix.sh          # the real tree, BEFORE the pin
  COMMIT-PREFIX: the commit-msg hook does not pin the SEMULITH- work-unit prefix.
    NOT REFUSED: a SEMILITH- subject passed .githooks/commit-msg — the pin is absent or dead
  rc=1
  $ bash scripts/check_commit_prefix.sh --self-test
  COMMIT-PREFIX --self-test: 4 pass / 0 fail
  $ bash scripts/check_doctrines.sh
  === all doctrines green ===
  ```

- [x] **FIX** — the pin in `.githooks/commit-msg`; `scripts/check_commit_prefix.sh`
  registered as `COMMIT-PREFIX` (#29 in `scripts/check_doctrines.project.sh`); both registry
  mirrors (`DOCTRINE_ENFORCEMENT.md`, `docs/book/src/working/doctrines.md`) carry the row;
  the decision record `decision_work-unit-prefix-semulith.md` + its INDEX entry; COMMIT.md
  states the pinned prefix.

- [x] **LOCKSTEP** — `docs/TASK_TREE.md` row (added active, closed in the same commit);
  MEMORY.md closure clause; LIVE_STATUS.md's derived counts restated by the gate's own
  re-derivation (29 registered / 301 arms); CHANGELOG.md + DEV_NOTES.md entries, each head
  sharded as its ceiling fired.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-30` | `PREFIX-DISCIPLINE.1` | prefix census over all 123 commit subjects | both spellings across 10+ areas (`SEMILITH-PL` ×13 the worst); exactly 1 non-prefixed subject (`Initial commit`) |
| `2026-09-30` | `PREFIX-DISCIPLINE.1` | `check_commit_prefix.sh` against the real tree, pre-pin | RED `NOT REFUSED` — the control observed failing before registration |
| `2026-09-30` | `PREFIX-DISCIPLINE.1` | `--self-test` fixtures | 4 pass / 0 fail — unpinned RED, refuse-all RED (wrong reason), over-tight RED, correctly-pinned GREEN |
| `2026-09-30` | `PREFIX-DISCIPLINE.1` | live hook probes, both directions | `SEMILITH-` refused with `SEMULITH` named (rc 1); `SEMULITH-` accepted (rc 0) |
| `2026-09-30` | `PREFIX-DISCIPLINE.1` | registered: DERIVED-COUNTS + REGISTRY-MIRROR + the whole enforcer | 29 doctrines / 301 self-test arms re-derived by the gate; both mirrors carry the row; `=== all doctrines green ===` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `PREFIX-DISCIPLINE.1` | `SEMULITH-PX-0001 (leaf PREFIX-DISCIPLINE.1): the SEMULITH- prefix, pinned at the boundary and watched` | the pin, `COMMIT-PREFIX` #29, the decision record; fired RED pre-pin |

## Changelog

- `2026-09-30`: Created. The director ruled the prefix is SEMULITH (never SEMILITH) after the
  spelling drift was surfaced the same day; `.1` opened immediately — the pin, its watcher,
  and the decision record in one leaf. Closed the same day: the hook pins `SEMULITH-`,
  `COMMIT-PREFIX` (#29) probes it behaviourally.
  `promotion: declined (the ruling is the decision record; the mechanism is the hook, the probe, and their two mirror rows).`
