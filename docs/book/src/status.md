# Current status

Included from the authoritative `LIVE_STATUS.md` at build time:

{{#include ../../../LIVE_STATUS.md}}

## How to read a row

`Done` means work finished, verified and committed. A milestone's gate is a
separate claim: `passed`, `failed` or `incomplete`, recorded in its evidence.
Composition work closing does not qualify a processor or board.

Use `A of B leaves` beside a task-tree link for explicit progress.
TREE-CLAIMS checks that syntax; bare ratios are outside its current grammar.
D59 owns source-parser and broader ratio coverage before full adoption.
The same-total/wrong-completed control guards the completed-count branch:

```sh
bash scripts/check_tree_claims.sh --self-test
```

## Where the detail lives

Task-trees and evidence: `docs/tasks/`, indexed by `docs/TASK_TREE.md`.
Decisions: `docs/decisions/`. Changes: `CHANGELOG.md` and Git.
