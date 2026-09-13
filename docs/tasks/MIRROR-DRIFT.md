# MIRROR-DRIFT: every hand-kept mirror of a machine-readable source is gated

## Metadata

- Tree ID: `MIRROR-DRIFT`
- Status: `active`
- Roadmap lane: project foundation (cross-cutting; serves every lane)
- Gate: none — this tree adds gates rather than passing one
- Depends on: nothing
- Unlocks: nothing; it protects the resume path every other tree is resumed through
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Find every tracked document that **restates** a fact some other tracked file already owns in
machine-readable form, and make the restatement either **derived** or **gated**. A mirror kept
by a conditional manual step is not a mirror; it is a copy with a half-life.

## Non-Goals

- Not a campaign to delete prose. A human-readable mirror is often the right artifact — the
  requirement is that its *facts* be checked against their owner, not that it stop existing.
- Not a generator. Deriving a table is one legitimate fix; gating a hand-written one is another,
  and for a document whose wording carries argument the second is usually better.
- No new content is authored here. A leaf that discovers a mirror is wrong fixes the mirror; if
  the *source* is wrong that is a finding routed to the tree that owns it.

## Acceptance Criteria

1. Each leaf names a specific mirror, the source that owns its facts, and the drift it measured
   (or the census showing there is none).
2. Each fix is a gate with a `--self-test` whose RED arms assert the **reason**, fired RED
   against the **real** corpus before being trusted — never only against fixtures.
3. No gate is registered that has not been observed failing on the actual repository or on a
   deliberately broken copy of it.

## Task Tree

- ID: `MIRROR-DRIFT.1` — **the task-tree index mirrors the trees**
  Status: `done`
  Goal: `docs/TASK_TREE.md` restates each tree's status, frontier leaf and leaf counts.
  `COMMIT.md` updates it "only if the frontier changes" — a conditional manual step. Gate the
  agreement and repair the drift that already exists.
  Acceptance: the index's status cell, frontier leaf and any leaf count are checked against the
  owning tree; the gate fires RED on the real index before the repair and green after.
  Verification: see the Verification Log.
  Commit: `SEMULITH-MIR-0017`

- ID: `MIRROR-DRIFT.2` — **the doctrine documents mirror the enforcer registry**
  Status: `pending`
  Goal: `DOCTRINE_ENFORCEMENT.md` and `docs/book/src/working/doctrines.md` both restate the
  doctrine registry held in the two driver scripts. Measured today: the book chapter is missing
  `PROFILE-CONSISTENCY` and `SEAM-INTEGRITY` — the two most recently registered — so the surface
  the director reviews shows 3 project doctrines where 5 run.
  Acceptance: every registered id appears in both mirrors and every id in a mirror is registered;
  the count sentence ("Thirteen checks run today") is derived or gated; fired RED on the real
  tree before the repair.

- ID: `MIRROR-DRIFT.3` — **the live docs' derived numbers**
  Status: `pending`
  Goal: `MEMORY.md` names an active tree and a frontier leaf; `LIVE_STATUS.md` states a leaf
  count per milestone tree. Census run at `.1`: all 11 leaf counts and both `MEMORY.md`
  assertions agree today, so this leaf is prevention, not repair — and the leaf must say so
  rather than manufacture a defect.
  Acceptance: `MEMORY.md`'s active tree and frontier leaf, and every `N leaves` / `A of B leaves`
  claim in `LIVE_STATUS.md`, are checked against the trees; the gate fires RED on a deliberately
  edited copy.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MIRROR-DRIFT.2` | `pending` | the drift is already measured and it is on the book — the surface the director reviews instead of the code |
| 2 | `MIRROR-DRIFT.3` | `pending` | same mechanism, no measured drift yet; prevention after repair |

## Decisions

- `2026-09-14`: **the tree is authoritative, the index mirrors it.** Both orderings were
  available — the gate could have demanded the tree match the index. The tree is where the
  acceptance evidence, the frontier reasoning and the leaf statuses live; the index carries one
  cell per tree. A fix that edits the summary to match the record is safe; a fix that edits the
  record to match its summary destroys information. The gate's failure message says so, so the
  next reader does not have to re-derive the choice.
- `2026-09-14`: this tree adds **gates**, not generators. A derived `docs/TASK_TREE.md` would
  also have prevented the drift, and was rejected: the "why next" column carries reasoning that
  no generator can produce, and a generated file invites hand edits that are silently discarded.

## Open Questions

- Is there a mirror in this repository that nothing in this tree covers? `.3` closes the live
  docs; the census at `.1` covered the task-tree family and the doctrine registry. A sweep for
  the general case — any tracked number that is a function of the tree — is
  `docs/CLAIM_VERIFICATION.md` §7 and is not yet mechanized here. Owner: `MIRROR-DRIFT.3`.

## Blockers

- None.

## Acceptance Checklist (current leaf — `MIRROR-DRIFT.1`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: WHERE is `docs/TASK_TREE.md`'s `P0-PROFILE` row;
  WHY is that `COMMIT.md` makes updating it conditional ("update `docs/TASK_TREE.md` … **only if
  the frontier changes**") while nothing compares the two files. Commit `SEMULITH-P0-0014` moved
  the frontier from `.2` to `.5` inside the tree and left the index cell at `.2`. Measured over
  the whole population before any fix, with a probe that reads both files per tree:

  ```
  $ grep -c '^| \[' docs/TASK_TREE.md          # index rows
  14
  $ bash scripts/check_frontier_sync.sh; echo "rc=$?"
  FRONTIER-SYNC: the task-tree index no longer mirrors the trees it indexes.
    FRONTIER DRIFT P0-PROFILE: index says '.2', tree's Current Frontier says 'P0-PROFILE.5'
    DONE FRONTIER P0-PROFILE: the index points at '.2', which the tree records as `done`
    DONE FRONTIER P0-PROFILE: the index points at '.1', which the tree records as `done`
  rc=1
  ```

  ⭐ The falsifying question was *"is one stale cell out of fourteen worth a gate?"* — and the
  answer is that the drift landed on the **only `active` tree**, which is the only row anyone
  ever reads. `CLAUDE.md` routes a resuming agent `MEMORY.md` → the index → the frontier, so the
  cell that rotted is the second hop of the recovery procedure itself. A 1-in-14 drift rate is
  not the measurement that matters; a 1-in-1 drift rate on the followed row is.

- [x] **ADDRESSED (verified)** — before → after on the symptom, same command both times:
  `bash scripts/check_frontier_sync.sh` → `rc=1` with three findings (above), then after the
  index row was repaired → `FRONTIER-SYNC: ok (15 tree(s) mirrored by docs/TASK_TREE.md)` — 15, not 14, because
  this tree's own row was added under the same gate,
  `rc=0`. The repair edited the **index**, not the tree, per this tree's first decision. The
  census behind `.3`'s "no drift yet" was run here and is recorded so it is not re-asserted from
  memory: every `N leaves` claim in `LIVE_STATUS.md` was re-derived from the trees —
  `grep -cE '^- ID: .<TREE>\.[0-9]+.' docs/tasks/<TREE>.md` over all 14 trees gave
  `8,1,7,7,9,12,9,6,10,7,8,7,8,4`, matching all 11 milestone claims and both `MEMORY.md`
  assertions (`P0-PROFILE`, `2 of 9`, frontier `.5`) exactly — `drifted: 1 of 3 mirrors`.

- [x] **NO REGRESSION** — leg 2: the gate was fired RED before it was trusted, on synthetic
  fixtures **and** on the real corpus. `bash scripts/check_frontier_sync.sh --self-test` →
  `FRONTIER-SYNC --self-test: 16 pass / 0 fail` — 14 RED arms, each asserting the *reason* and
  not merely the verdict: `FRONTIER DRIFT`, `PREMATURE COMPLETE`, `STALE FRONTIER`,
  `DONE FRONTIER`, `STATUS DRIFT`, `UNKNOWN LEAF` (from the index and from the tree),
  `COUNT DRIFT` in both spellings, `UNLISTED TREE`, `NO TREE FILE`, and two REFUSE arms
  (`NO ROWS`, `NO INDEX`) that assert `rc=2` rather than a silent pass. Whole gate afterwards:
  `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`, `rc=0`.
  ⛔ The self-test itself was caught lying first, which is why it is worth reporting: the first
  run printed `4 pass / 0 fail` — **green, and judging almost nothing**. Ten `arm` calls sat on
  the same physical line as the fixture call that preceded them, so bash passed `arm` and its
  three arguments as extra positional parameters to a function that reads only `$1` and `$2`,
  and they were discarded in silence. Found by reading the arm count against the number of arms
  written (`4` vs `14`), not by reading the code. A self-test that runs a third of its arms and
  reports `0 fail` is precisely the "green gate that judges nothing" this repository's own
  `DEV_NOTES.md` names as the class a template must not ship.

- [x] **FIX** — `scripts/check_frontier_sync.sh` added (parse both files, compare six
  properties, refuse rather than pass when it cannot parse) and registered in
  `scripts/check_doctrines.project.sh` as `FRONTIER-SYNC`. `docs/TASK_TREE.md`'s `P0-PROFILE`
  row repaired to `.5` and given a leaf count the gate now re-derives. The new row for this tree
  was added under the same rule.

- [x] **LOCKSTEP** — leg 3: the agreement is re-derived on every commit by the pre-commit hook,
  so the index cannot rot again without the commit failing. `DOCTRINE_ENFORCEMENT.md` gains the
  registry row and `TOOLBOX.md` the diagnostic row; `MEMORY.md`, `LIVE_STATUS.md`,
  `CHANGELOG.md` and `DEV_NOTES.md` updated in this commit, and the lesson promoted to
  [`self-test-arms-that-never-ran`](../knowledge/self-test-arms-that-never-ran.md).
  ⛔ **The book is deliberately NOT updated by this leaf, and that is a named gap, not an
  oversight.** `docs/book/src/working/doctrines.md` already omits `PROFILE-CONSISTENCY` and
  `SEAM-INTEGRITY`; `FRONTIER-SYNC` makes three. Adding this one row by hand would repair the
  symptom and destroy the evidence `MIRROR-DRIFT.2` needs — that leaf's acceptance requires the
  new gate to be **fired RED against the real drift** before the repair, and a mirror that has
  been quietly patched cannot be fired RED. The gap is owned by `MIRROR-DRIFT.2`, which is the
  next commit, and the drift it will show is the stronger measurement: *the book fell further
  behind on the very commit that registered a doctrine*, which is the mechanism rather than an
  anecdote.
  ⭐ A second defect surfaced while editing the mirror, and it is invisible in the source: two
  blank lines inside the project-doctrine table split it into three GFM fragments, so
  `PROFILE-CONSISTENCY` and `SEAM-INTEGRITY` rendered as literal `| … |` text rather than table
  rows. `awk` over the section counted `rows: 8` (header + separator + 6) only after the blanks
  were removed; before, the table ended at three rows. Found by counting, not by reading —
  a table that is right in the file and wrong on the page is the exact failure mode
  `TABLE-ARITY-RATCHET` was written for one column over, and neither gate sees a blank line.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-14` | `MIRROR-DRIFT.1` | drift census over all 14 index rows | `1` drifted row, on the only `active` tree |
| `2026-09-14` | `MIRROR-DRIFT.1` | `check_frontier_sync.sh` on the real index, before | `rc=1`: `FRONTIER DRIFT` + 2 × `DONE FRONTIER` |
| `2026-09-14` | `MIRROR-DRIFT.1` | `check_frontier_sync.sh` on the real index, after | `ok (15 tree(s) mirrored)`, `rc=0` |
| `2026-09-14` | `MIRROR-DRIFT.1` | `check_frontier_sync.sh --self-test` | `16 pass / 0 fail` (14 RED arms) |
| `2026-09-14` | `MIRROR-DRIFT.1` | leaf-count re-derivation vs `LIVE_STATUS.md` / `MEMORY.md` | 11 of 11 counts and both pointer claims agree |
| `2026-09-14` | `MIRROR-DRIFT.1` | project-doctrine table fragments in `DOCTRINE_ENFORCEMENT.md` | 3 fragments before, `rows: 8` in one table after |
| `2026-09-14` | `MIRROR-DRIFT.1` | `scripts/check_doctrines.sh` + `make check` | `all doctrines green`, `rc=0`; `test result: ok. 1 passed` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MIRROR-DRIFT.1` | `SEMULITH-MIR-0017 (leaf MIRROR-DRIFT.1): gate the task-tree index against the trees` | 14 RED arms; one real drift repaired |

## Changelog

- `2026-09-14`: Created after a drift found while resuming: `MEMORY.md` and `docs/TASK_TREE.md`
  disagreed about which leaf was next, and the index was the one that was wrong.
- `2026-09-14`: `MIRROR-DRIFT.1` completed. The index is now a checked mirror rather than a
  remembered one.
