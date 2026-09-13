# SEMULITH-TREES: represent the whole roadmap as task-trees

## Metadata

- Tree ID: `SEMULITH-TREES`
- Status: `done`
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

## Acceptance Checklist (current leaf — `SEMULITH-TREES.4`)

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: bounds written for a three-tree repository were
  still governing an eleven-lane one, and the partitioned-family control was incomplete.
  Measured: `git ls-files docs/tasks | wc -l` → `17` files, `133074` aggregate bytes against a
  `65536` health target set when the family held 5 files / 39,131 bytes — and
  `docs/tasks/SEMULITH-PKG.md` alone is `35395` bytes. `README_POLICY.md` requires a partitioned
  family to carry **per-part**, file-count and aggregate ceilings; the registry had only the
  last two, so one member could become the monolith the split was meant to avoid, invisibly.
  Separately, `CHANGELOG.md` crossed its health target within a day of ordinary work
  (`25814` bytes against `24576`), which is a miscalibrated instrument rather than a finding.
- [x] **ADDRESSED (verified)** — a ninth column, `ceiling_part_bytes`, now bounds the largest
  member of a directory family, and the bounds are re-derived from the final corpus with the
  derivation recorded in the registry header. `README-ROUTING-CLOSURE: ok (24 governed
  destination(s))` with **no health warnings**, where the previous run printed four.
  ⭐ The calibration insight is recorded because it is what made the first cut noisy: a
  **hot/live** surface's health target sits just above today's reviewed size, because
  unexpected growth is the signal; an **append_history** surface's belongs near its ceiling,
  because growth is expected and the only useful warning is that the shard threshold is
  approaching. `CHANGELOG.md` and `DEV_NOTES.md` moved to 75% of their ceilings for that reason
  — their ceilings were not touched.
- [x] **NO REGRESSION** — leg 2: the new ceiling was fired against the **real** corpus, not
  only a fixture. Temporarily setting `docs/tasks/`'s per-part ceiling to `20000` produced
  `OVER CEILING docs/tasks/: part docs/tasks/SEMULITH-PKG.md` / `35395 bytes > 20000` — the
  right member, the right number — and the registry was restored to `ok`. That control also
  exposed a usability defect in itself: it first printed an **absolute** path, which the
  `DOCPATH` doctrine would refuse inside a task leaf, so an author pasting this tool's own
  output as evidence would have been blocked by a different gate for a defect in this one. Now
  repo-relative. `README-ROUTING-CLOSURE --self-test: 12 pass / 0 fail` (9 RED arms);
  `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`; `make check` →
  `test result: ok. 1 passed; 0 failed`, `rc=0`; `mdbook build docs/book` → `HTML book written`.
- [x] **FIX** — `ceiling_part_bytes` added to the registry and the checker; bounds re-derived;
  the book's task-tree chapter now includes the live tree index by mdBook anchor, verified
  rendered (`P4-SYSTEM` present in the built HTML, anchor markers absent). Also:
  `.doctrine/evidence_tokens.txt`'s **enumerated** list of doctrine names had fallen behind the
  registry for the second time — this leaf's own `README-ROUTING-CLOSURE: ok (24 governed
  destination(s))` evidence was refused by `TASK-ACCEPTANCE` because the doctrine post-dated
  the list. A list that must be edited whenever a sibling file changes will be stale, so it is
  now the **shape** every gate here prints, `[A-Z][A-Z0-9]+(-[A-Z0-9]+)+: `, verified against
  five real verdict lines (`README-ROUTING-CLOSURE`, `DELIVERY-PROVENANCE`,
  `FIXTURE-FINGERPRINT`, `README-STABILITY`, `TASK-ACCEPTANCE`) — all `MATCH`. Firing the gate
  RED afterwards (this box replaced by *"I thought about it and I am confident"*) still gave
  `rc=1`, so the generalization did not make it vacuous.
- [x] **LOCKSTEP** — leg 3: every bound is enforced on every commit, and the derivation sits in
  the file that holds the numbers. `docs/TASK_TREE.md` gained the anchors, `MEMORY.md`,
  `LIVE_STATUS.md` and `CHANGELOG.md` are updated in this commit.

## Task Tree

- ID: `SEMULITH-TREES`
  Status: `done`
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
  Status: `done`
  Goal: the system lane — `P5-BOARD`, `AG-OS`, `P6-LINUX`, `P7-COMPUTER`, `MC-MULTICORE`.
  Acceptance: five trees, each naming its gate, its dependencies and its roadmap section; registered.
  Verification: see the Verification Log.
  Commit: `SEMULITH-TREES-0011`

- ID: `SEMULITH-TREES.4`
  Status: `done`
  Goal: re-review `docs/tasks/` family bounds against the resulting corpus; sync the book and live docs.
  Acceptance: measured file count and aggregate bytes recorded with a derivation; ceilings adjusted only with a stated contract expansion; `README-ROUTING-CLOSURE` green with no health warning.
  Verification: see the Verification Log.
  Commit: `SEMULITH-TREES-0012`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | **tree complete (4/4).** All eleven roadmap lanes are task-trees. The next work is execution: `P0-PROFILE.1`, the `rv64i-lab-v0` profile dossier. |

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

### `SEMULITH-TREES.3` — the system lane

- [x] **ROOT CAUSE (WHY + WHERE)** — leg 1: five lanes still had no tree.
  `git ls-files 'docs/tasks/*.md' | grep -vc 'TEMPLATE\|BOOTSTRAP\|SEMULITH-'` → `6` before
  this leaf, against eleven lanes in `ROADMAP.md` §6 — the graph's `P5`, `AG`, `P6`, `P7` and
  `MC` nodes were unowned. `AG` and `MC` are the two most dangerous of them: `AG` is the lane
  where another project's interfaces enter this one, and `MC` is the lane where a capability is
  most easily claimed by adding host threads.
- [x] **ADDRESSED (verified)** — five trees created and registered: `P5-BOARD` (7 leaves, gate
  `BOARD`), `AG-OS` (8 leaves, gate `ARCHOGEN-OS`), `P6-LINUX` (8 leaves, gate `LINUX`),
  `P7-COMPUTER` (7 leaves, gate `SYSTEM`), `MC-MULTICORE` (7 leaves, its own gate). Census
  after: `git ls-files 'docs/tasks/*.md' | grep -vc 'TEMPLATE\|BOOTSTRAP\|SEMULITH-'` → `11`
  — **every lane of `ROADMAP.md` §6 now has an owner.**
- [x] **NO REGRESSION** — `scripts/check_doctrines.sh` → `=== all doctrines green ===`, `rc=0`;
  `make check` → `test result: ok. 1 passed; 0 failed`, `rc=0`. `README-ROUTING-CLOSURE`
  re-measured `docs/tasks/` and reports it inside its enforced ceiling while **over its health
  target** — which is the two-tier design working as intended, and is leaf `.4`'s subject.
  Leg 2, stated honestly: the oracle for *"this tree matches the plan"* is the plan, so every
  leaf cites its roadmap section, contract section, rule ID or archogen obligation. A reader
  refutes a leaf by reading one paragraph.
- [x] **FIX** — `P5-BOARD.md`, `AG-OS.md`, `P6-LINUX.md`, `P7-COMPUTER.md`, `MC-MULTICORE.md`
  created and registered.
- [x] **LOCKSTEP** — `docs/TASK_TREE.md`, `MEMORY.md`, `LIVE_STATUS.md`, `CHANGELOG.md` updated
  in this commit.

### `SEMULITH-TREES.2` — the CPU lane

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
| `2026-09-13` | `SEMULITH-TREES.3` | milestone-tree census before/after | `6` → `11` — every `ROADMAP.md` §6 lane owned |
| `2026-09-13` | `SEMULITH-TREES.3` | `scripts/check_doctrines.sh` + `make check` | `all doctrines green`, `rc=0`; `test result: ok. 1 passed` |
| `2026-09-13` | `SEMULITH-TREES.4` | `docs/tasks/` corpus measurement | `17` files, `133074` bytes, largest member `35395` |
| `2026-09-13` | `SEMULITH-TREES.4` | per-part ceiling fired on the real corpus | named `docs/tasks/SEMULITH-PKG.md`, `35395 > 20000`; restored `ok` |
| `2026-09-13` | `SEMULITH-TREES.4` | `check_readme_routes.sh --self-test` | `12 pass / 0 fail` (9 RED arms) |
| `2026-09-13` | `SEMULITH-TREES.4` | `README-ROUTING-CLOSURE` after re-derivation | `ok (24 governed)`, **0 health warnings** (was 4) |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `SEMULITH-TREES.1` | `SEMULITH-TREES-0009 (leaf SEMULITH-TREES.1): the near-term lane as task-trees` | `P0-PROFILE` 9 leaves, `P1-LAB` 12 leaves |
| `SEMULITH-TREES.2` | `SEMULITH-TREES-0010 (leaf SEMULITH-TREES.2): the CPU lane as task-trees` | `P2-SCALAR` 9, `DSP-REVIEW` 7, `P3-BREADTH` 6, `P4-SYSTEM` 10 |
| `SEMULITH-TREES.3` | `SEMULITH-TREES-0011 (leaf SEMULITH-TREES.3): the system lane as task-trees` | `P5-BOARD` 7, `AG-OS` 8, `P6-LINUX` 8, `P7-COMPUTER` 7, `MC-MULTICORE` 7 |
| `SEMULITH-TREES.4` | `SEMULITH-TREES-0012 (leaf SEMULITH-TREES.4): bound the task-tree family per part` | 9th column; bounds re-derived; book gains the live tree map |

## Changelog

- `2026-09-13`: Created task tree; `SEMULITH-TREES.1` completed.
- `2026-09-13`: `SEMULITH-TREES.2` completed — the CPU lane, both processor gates now owned.
- `2026-09-13`: `SEMULITH-TREES.3` completed — all eleven roadmap lanes are task-trees.
- `2026-09-13`: `SEMULITH-TREES.4` completed and **the tree is done**. The partitioned-family
  control is now complete (per-part + file-count + aggregate), and the health targets are
  calibrated by lifecycle rather than by one rule for every surface.
