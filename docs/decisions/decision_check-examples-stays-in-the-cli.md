# `semulith check-examples` stays a product command; `XTASK.5` closes without a code change

- **Type:** `decision`
- **Date:** `2026-10-26`
- **Status:** `active`
- **Owner / source:** the workflow under [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md);
  measured in `docs/tasks/XTASK.md` (Blockers, 2026-10-24).
answers: Does the record-graph check move from the product CLI to `cargo xtask`, as `XTASK.5` planned?

## The fact / decision

No. `semulith check-examples` validates the frozen records bundle and presents its report; that is the CLI's
architectural role ("user commands and report presentation", `docs/ARCHITECTURE.md` §4), so it was never
development-only tooling. `XTASK.5` is closed `done` by this decision with no code change. The development
gate (`RECORD-SCHEMA`, `scripts/check_requirements.sh`) keeps calling it through `cargo run`.

## Why

- The G1 gate report computes its criterion 3 from the CLI source naming `check-examples`
  (`scripts/gate_report.py` lines 383 and 391), and that script is pinned by the retained M case
  (`evidence/rv64gc-m-forms-v3/dependencies.sexp`). Moving the command would turn a retained verdict false
  unless the pinned script changed, which needs a planned capture of the whole case — a cost with no product
  gain, since the command's job (report presentation over the records graph) is the CLI's.
- The tree's premise, "the product CLI keeps product commands only", holds: this is one.

## How to apply

- `XTASK.5` is `done` (closed by decision); the xtask migration ports development checks, not product
  commands. If the command ever moves, it moves in the same unit as a planned capture that also teaches
  `gate_report.py` the new location — never before.
