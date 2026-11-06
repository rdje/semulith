# The retained cases

Every finite case this unit holds, one row each. The rows are generated from each case's own `case.sexp` and from the credit catalogue, on every commit, so this page cannot fall behind the evidence: a credit that lapses changes its row, and the commit refuses until the page is regenerated.

```text
$ python3 -B scripts/gen_model_book.py --unit rv64gc-lab-v0
```

{{#include materials/retained-cases.md}}

**State** is read, never typed:

| State | Means |
| --- | --- |
| `credited` | A credit record names the case, and every pin it holds still describes the tree |
| `history` | Another case of the same requirement holds the credit. Its bytes stay, and nothing reviews them |
| `captured, credited by nothing` | Captured once, with no current credit for its requirement: not yet reviewed, or its credit lapsed |
| `declared` | Committed before its capture, with no observations yet |

**Configuration** is `the override` when the case runs under the profile's own reference override, and `its own` when the case carries an overlay ([references](references.md)).
