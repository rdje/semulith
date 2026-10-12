# Current status

Authority: `LIVE_STATUS.md` (included below).

{{#include ../../../LIVE_STATUS.md}}

## Reading progress

Work closure (`Done`) and gate verdicts differ. Composition closure qualifies
no processor/board; slice-gated is conditional.

Use `A of B leaves`, `B leaves`, or leading `A/B` after a known tree ID
(optional dash/parenthesis). Later bare ratios are excluded. Guards validate
backtick/bold statuses and whole archived ranges. Bad source refuses2; drift
fails1. Closed counts allow semicolon/comma annotations. Syntax is finite.

```sh
bash scripts/check_tree_claims.sh
bash scripts/check_frontier_sync.sh
python3 scripts/qualify_task_claim_inputs.py
```

Last command: historical assessment (`docs/tasks/artifacts/live-containment/task-claims.md`).
Routes: `docs/TASK_TREE.md`, `docs/decisions/`, `CHANGELOG.md`, Git.
