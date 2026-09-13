# SEMULITH-TREES: represent the whole roadmap as task-trees

## Metadata

- Tree ID: `SEMULITH-TREES`
- Status: `active`
- Roadmap lane: project foundation (precedes P0 execution)
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Convert **every** activity and phase of `ROADMAP.md` into a task-tree under `docs/tasks/`,
registered in `docs/TASK_TREE.md`, so that no lane of the plan exists only as prose and a lost
session cannot lose a lane. Each milestone tree carries its gate as its acceptance criteria, its
leaves as the executable breakdown, and its open questions as the decisions that must be made
before its work depends on them.

## Non-Goals

- This tree does not **execute** any milestone. It produces the trees that own that execution.
- It does not re-plan. Where the roadmap and this tree disagree, the roadmap is the plan and
  the disagreement is a defect in the tree.
- It does not invent schedule estimates. `ROADMAP.md` §7 declines to attach elapsed time before
  the P0/P1 experiments exist, and a task-tree is not a place to smuggle one back in.

## Acceptance Criteria

- One tree per roadmap milestone and cross-cutting lane, each registered in `docs/TASK_TREE.md`.
- Every tree names its gate, its dependencies, and the roadmap section it is derived from, so a
  reader can check it against the plan rather than trusting it.
- Every tree's leaves are small enough to finish, verify and commit as one signoff slice.
- `docs/tasks/`'s family bounds are re-reviewed against the resulting corpus, not exceeded.
- The book's milestone chapters and the live docs reflect the conversion in the same commits.

## Acceptance Checklist (current leaf — `SEMULITH-TREES.2`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: the CPU lane — where both processor gates sit — had
  no trees. `git ls-files 'docs/tasks/*.md' | grep -vc 'TEMPLATE\|BOOTSTRAP\|SEMULITH-'` → `2`
  before this leaf, against four CPU-lane sections in the plan
  (`grep -c '^### P2\|^### P3\|^### P4' ROADMAP.md` → `3`, plus the **D** node that §6's graph
  makes a separate prerequisite of `BREADTH`). `CPU-LAB` and `CPU-SYSTEM` are the two gates the
  whole project's credibility rests on, and neither had an owner.
- [x] **ADDRESSED (verified)** — four trees created and registered: `P2-SCALAR` (9 leaves, gate
  `CPU-LAB`), `DSP-REVIEW` (7 leaves, no gate of its own — a precondition of `BREADTH`),
  `P3-BREADTH` (6 leaves, gate `BREADTH`), `P4-SYSTEM` (10 leaves, gate `CPU-SYSTEM`). Census
  after: `git ls-files 'docs/tasks/*.md' | grep -vc 'TEMPLATE\|BOOTSTRAP\|SEMULITH-'` → `6`.
  Each tree's acceptance criteria **are** its gate, quoted from
  `docs/EVIDENCE_AND_GATES.md` §7 rather than restated.
- [x] **NO REGRESSION** — `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`;
  `make check` → `test result: ok. 1 passed; 0 failed`, `rc=0`. `README-ROUTING-CLOSURE`
  re-measured the grown `docs/tasks/` family and stayed inside its bounds. Leg 2, stated
  honestly: the only oracle for *"this tree matches the plan"* is the plan, so every leaf cites
  the roadmap section, task card, rule ID or catalog entry it derives from — a reader refutes a
  leaf by reading one paragraph. That is the strongest control available for a prose-to-
  structure conversion, and it is weaker than a test.
- [x] **FIX** — `P2-SCALAR.md`, `DSP-REVIEW.md`, `P3-BREADTH.md`, `P4-SYSTEM.md` created and
  registered in `docs/TASK_TREE.md`.
- [x] **LOCKSTEP** — `docs/TASK_TREE.md`, `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md` updated
  in this commit.

## Task Tree

- ID: `SEMULITH-TREES`
  Status: `active`
  Goal: represent the whole roadmap as task-trees
  Children: `SEMULITH-TREES.1` … `SEMULITH-TREES.4`

- ID: `SEMULITH-TREES.1`
  Status: `done`
  Goal: the near-term lane — `P0-PROFILE` and `P1-LAB`.
  Acceptance: both trees exist with gate-derived acceptance criteria and executable leaves; both registered.
  Verification: see the Verification Log.
  Commit: `SEMULITH-TREES-0009`

- ID: `SEMULITH-TREES.2`
  Status: `done`
  Goal: the CPU lane — `P2-SCALAR`, `DSP-REVIEW`, `P3-BREADTH`, `P4-SYSTEM`.
  Acceptance: four trees, each naming its gate, its dependencies and its roadmap section; registered.
  Verification: see the Verification Log.
  Commit: `SEMULITH-TREES-0010`

- ID: `SEMULITH-TREES.3`
  Status: `pending`
  Goal: the system lane — `P5-BOARD`, `AG-OS`, `P6-LINUX`, `P7-COMPUTER`, `MC-MULTICORE`.
  Acceptance: five trees, each naming its gate, its dependencies and its roadmap section; registered.
  Verification: `pending`
  Commit: `pending`

- ID: `SEMULITH-TREES.4`
  Status: `pending`
  Goal: re-review `docs/tasks/` family bounds against the resulting corpus; sync the book and live docs.
  Acceptance: measured file count and aggregate bytes recorded with a derivation; ceilings adjusted only with a stated contract expansion; `README-ROUTING-CLOSURE` green with no health warning.
  Verification: `pending`
  Commit: `pending`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `SEMULITH-TREES.3` | `pending` | the system lane completes roadmap coverage |
| 2 | `SEMULITH-TREES.4` | `pending` | bounds and the book are re-reviewed once the corpus is final, not per tree |

## Decisions

- `2026-09-13`: **one tree per milestone**, not one tree for the roadmap. A milestone's gate is
  its acceptance criteria, which only works if the milestone owns a tree.
- `2026-09-13`: every leaf cites the roadmap section or task card it derives from. A tree that
  cannot be checked against the plan is a second plan.
- `2026-09-13`: trees for milestones not yet started are `proposed`, with `pending` leaves and
  an unticked acceptance checklist. The checklist is filled at execution time, per leaf.

## Open Questions

- Does `ROADMAP.md` §6's dependency graph stay the authority once trees exist? **Yes** — the
  trees carry execution, the roadmap carries direction, and a contradiction is a tree defect.
  Does not block the frontier.

## Blockers

- None.

## Completed-leaf evidence (archive)

### `SEMULITH-TREES.1` — the near-term lane

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: the roadmap existed only as prose. Census of lanes
  represented as trees before this leaf: `git ls-files 'docs/tasks/*.md' | grep -vc
  'TEMPLATE\|BOOTSTRAP\|SEMULITH-'` → `0`, against `grep -c '^### P[0-9]' ROADMAP.md` → `8`
  milestone sections plus three cross-cutting lanes (DSP review, archogen OS integration,
  multicore). A lane with no tree has no frontier, no acceptance record and no owner, so a lost
  session loses it entirely — which is the failure the whole task-tree doctrine exists to
  prevent.
- [x] **ADDRESSED (verified)** — the two lanes that will actually be executed next now exist as
  trees: `P0-PROFILE` (9 leaves, gate `G0`) and `P1-LAB` (12 leaves, gate `G1`), both derived
  from `ROADMAP.md` §P0/§P1 and the task cards `T000`–`T007` in `docs/IMPLEMENTATION_GUIDE.md`,
  and both registered in `docs/TASK_TREE.md`. Same census after:
  `git ls-files 'docs/tasks/*.md' | grep -vc 'TEMPLATE\|BOOTSTRAP\|SEMULITH-'` → `2`.
- [x] **NO REGRESSION** — `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`
  (13 checks, including `README-ROUTING-CLOSURE` over the grown `docs/tasks/` family);
  `make check` → `test result: ok. 1 passed; 0 failed`, `rc=0`. Leg 2 named honestly: the
  falsifiable claim here is *"these trees match the roadmap"*, and the oracle for it is the
  roadmap itself — every leaf cites the section it derives from, so a reader can refute a leaf
  by reading one paragraph. No stronger control exists for a prose-to-structure conversion, and
  that limit is stated rather than dressed up.
- [x] **FIX** — `docs/tasks/P0-PROFILE.md` and `docs/tasks/P1-LAB.md` created; both registered.
- [x] **LOCKSTEP** — `docs/TASK_TREE.md`, `MEMORY.md`, `LIVE_STATUS.md` and `CHANGELOG.md`
  updated in this commit. The book's milestone chapters already describe these two lanes and
  are unchanged by this leaf; leaf `.4` re-reviews the family bounds once all trees exist.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-13` | `SEMULITH-TREES.1` | milestone-tree census before/after | `0` → `2` |
| `2026-09-13` | `SEMULITH-TREES.1` | `scripts/check_doctrines.sh` + `make check` | `all doctrines green`, `rc=0`; `test result: ok. 1 passed` |
| `2026-09-13` | `SEMULITH-TREES.2` | milestone-tree census before/after | `2` → `6` |
| `2026-09-13` | `SEMULITH-TREES.2` | `scripts/check_doctrines.sh` + `make check` | `all doctrines green`, `rc=0`; `test result: ok. 1 passed` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `SEMULITH-TREES.1` | `SEMULITH-TREES-0009 (leaf SEMULITH-TREES.1): the near-term lane as task-trees` | `P0-PROFILE` 9 leaves, `P1-LAB` 12 leaves |
| `SEMULITH-TREES.2` | `SEMULITH-TREES-0010 (leaf SEMULITH-TREES.2): the CPU lane as task-trees` | `P2-SCALAR` 9, `DSP-REVIEW` 7, `P3-BREADTH` 6, `P4-SYSTEM` 10 |

## Changelog

- `2026-09-13`: Created task tree; `SEMULITH-TREES.1` completed.
- `2026-09-13`: `SEMULITH-TREES.2` completed — the CPU lane, both processor gates now owned.
