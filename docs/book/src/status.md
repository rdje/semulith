# Current status

The table below is **included live** from `LIVE_STATUS.md`, the repository's authoritative
progress tracker. It is not a copy: the book renders whatever that file says at build time, so
this page cannot drift from it.

{{#include ../../../LIVE_STATUS.md}}

## How to read a row

`Done` means the work is finished, verified, and committed — not that a milestone's *gate* has
passed. Gate status is a separate, stronger claim with its own vocabulary (`passed` / `failed` /
`incomplete`) and it is recorded in the evidence records, never in this tracker.

## Where the detail lives

- Active work, its frontier, and its evidence: the task-trees under `docs/tasks/`, indexed by
  `docs/TASK_TREE.md`.
- Durable decisions: `docs/decisions/`.
- What changed and when: `CHANGELOG.md` and git history.
