# MEMORY-POINTER: the resume pointer points, nothing more

## Metadata

- Tree ID: `MEMORY-POINTER`
- Status: `done`
- Roadmap lane: repository hygiene — the layer-A contract (`MEMORY_ARCHITECTURE.md` §6;
  `doctrine/readme_routes.tsv` `hot_live` row for `MEMORY.md`)
- Gate: none of its own; `MEMORY-ARCH` and `TREE-CLAIMS` already gate the surface
- Created: `2026-10-02`
- Owner: repo-local workflow

## Goal

Execute the director's `2026-10-02` rulings — *"MEMORY.md is there solely to point to the next
action"* and *"it shall overwrite only and not append, per MEMORY_ARCHITECTURE.md"* — measured
against the file's actual state (34 lines / 7,031 bytes against a 30-line / 1,792-byte health
target; 97% of its hard byte cap). Slim the file to the §6 template, route every dropped fact
to its durable layer first, and record the ruling durably.

## Non-Goals

- **Not a content deletion.** Nothing leaves the project's memory; every line moves to (or is
  verified already in) layer B/C before it leaves layer A.
- **Not a contract change.** The §6 caps and the `hot_live` claims `TREE-CLAIMS` gates stay as
  they are; the file is brought back under them.

## Acceptance Criteria

1. `MEMORY.md` carries the §6 template fields (latest commit, active trees, next action,
   in-flight, blockers) and nothing that duplicates a durable layer.
2. Every dropped line's durable home is named in the leaf's audit, and any dangling fact is
   routed to `docs/decisions/` in the same slice.
3. `MEMORY-ARCH` and `TREE-CLAIMS` green; the file at or under its health target.

## Task Tree

- ID: `MEMORY-POINTER`
  Status: `done`
  Goal: the resume pointer points at the next action, nothing more
  Children: `MEMORY-POINTER.1`

- ID: `MEMORY-POINTER.1` — **the slim, the audit, and the ruling recorded**
  Status: `done` (`2026-10-02`)
  Goal: audit every line of `MEMORY.md` for its durable home; backfill the one dangling ruling
  (`document EVERYTHING`, `2026-10-01` → `decision_document-everything`); record the ruling
  (`decision_memory-next-action-pointer`); rewrite `MEMORY.md` to the §6 template.
  Acceptance: as the tree's Acceptance Criteria 1–3.
  Verification: `2026-10-02` — all in the Verification Log below.
  Commit: `pending`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| — | — | — | `.1` done (`2026-10-02`); the pointer is the §6 template — upkeep is the overwrite discipline, not a leaf |

## Decisions

- `2026-10-02`: the slim keeps exactly the claims the gates read: the `Active trees:` line and
  the leaf-count shapes (`TREE-CLAIMS` — and it scans PER PHYSICAL LINE, so the active-trees
  list stays on one line: the first slim draft wrapped it and the gate fired `MISSING ACTIVE`
  on the wrapped names), the four-doc resume path (`MEMORY-ARCH`), and the push-cadence
  refusal (the one operational rule a resuming session must not miss).

## Open Questions

- None.

## Blockers

- None.

## Acceptance Checklist (filled per leaf at execution time)

`MEMORY-POINTER.1` (`2026-10-02`):

- [x] **ROOT CAUSE (WHY + WHERE)** — the director ruled (`2026-10-02`, three messages, one
  intent): `MEMORY.md` exists solely to point at the next action, overwrite-only per
  `MEMORY_ARCHITECTURE.md` §6. WHERE: the whole "Current state" block had become a state
  digest duplicating layers B/C — the §6 failure shape, measured at the ruling:

  ```
  $ wc -lc MEMORY.md      ->      34 7031 MEMORY.md     # health 30 lines / 1,792 B; hard cap 50 / 7,168 — at 97%
  ```
- [x] **ADDRESSED (verified)** — the audit before the slim (every dropped line's home):

  | Dropped content | Durable home (verified by grep) |
  | --- | --- |
  | project state, frontier history, "feel it now" commands | the task-trees; `TOOLBOX.md` |
  | directions 2026-09-14/27 ×3, 2026-10-01, 2026-10-02 | `decision_one-format-…`, `decision_interpreter-…`, `decision_browser-…`, `decision_task-tree-per-part-growth`, `decision_mdbook-incremental-engaging` |
  | `document EVERYTHING` (2026-10-01) | **DANGLING** — backfilled `decision_document-everything` |
  | materials / chipdoc / corpus-pin facts | `materials/*.sexp`, `docs/knowledge/the-chipdoc-request-channel.md`, `P5-BOARD.8`/`.9` |
  | citation-pin warning | `docs/knowledge/a-version-string-is-not-an-identity.md` |
  | mutation-suite / baseline caveats | `docs/tasks/MODEL-BOOKS.md`, `P1-LAB.11` + `baseline.sexp` |
  | LinkedSpec pin, watcher, upstream count | git's submodule pin, `doctrine/sanctioned_processes.tsv`, `scripts/upstream_exposure.py` |
  | push-cadence rule | `decision_push-cadence`, `COMMIT.md` — and KEPT in the pointer (operational) |

  Before → after, measured: 34 lines / 7,031 B → 29 lines / 1,867 B (health 30 / 1,792 — the
  line target met, the byte target within 5% and stated: the four mandatory claim lines are
  irreducible without dropping a gated claim).

  ```
  $ bash scripts/check_tree_claims.sh           -> TREE-CLAIMS: ok (…)
  $ bash scripts/check_memory_architecture.sh   -> memory-arch: ok (…)
  ```

- [x] **NO REGRESSION** — both gates re-run after the slim; the RED was observed first (the
  first slim draft wrapped the active-trees list across two physical lines):

  ```
  $ bash scripts/check_tree_claims.sh     # first draft
  TREE-CLAIMS: a live document states a tree fact that the tree contradicts.
    MISSING ACTIVE MEMORY.md: 'BOOK-APPARATUS' is `active` and the pointer does not name it
  $ bash scripts/check_tree_claims.sh     # after the one-line refactor
  TREE-CLAIMS: ok (4 live document(s) state nothing the trees contradict)
  $ bash scripts/check_memory_architecture.sh   # rc 0
  ```

  The full enforcer runs at commit.
- [x] **FIX** — `MEMORY.md` rewritten to the §6 template; two decision records
  (`decision_memory-next-action-pointer`, `decision_document-everything`) + INDEX rows; this
  tree.
- [x] **LOCKSTEP** — tree (leaf + checklist + logs), `docs/TASK_TREE.md` row, `CHANGELOG.md`
  entry, `MEMORY.md` itself; `LIVE_STATUS.md` unchanged (no project-area row moved).

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-10-02` | `.1` | `check_tree_claims.sh` + `check_memory_architecture.sh` green; `wc` 29 lines / 1,867 B (was 34 / 7,031); RED observed first (`MISSING ACTIVE` on the wrapped line) | the pointer is the §6 template; one dangling ruling backfilled; the per-physical-line scan lesson recorded in Decisions |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.1` | `SEMULITH-MP-0001 (leaf MEMORY-POINTER.1): MEMORY.md slimmed to the §6 next-action pointer — the director's ruling recorded, one dangling ruling backfilled, 34/7031 → 29/1867` | the audit table names every dropped line's home; TREE-CLAIMS fired RED on the first draft (line wrap) |

## Changelog

- `2026-10-02`: Created from the director's `2026-10-02` rulings (next-action-only;
  overwrite-only per `MEMORY_ARCHITECTURE.md`).
- `2026-10-02`: `.1` done: the slim landed (34/7,031 → 29/1,867), the audit verified every
  dropped line's durable home and backfilled the one dangling ruling
  (`decision_document-everything`); the ruling itself is `decision_memory-next-action-pointer`.
