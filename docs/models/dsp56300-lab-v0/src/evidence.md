# The evidence and the gates

## What was measured

Subset v0 is **form-complete and differentially agreed**: six synthetic guests
(`micro`, `alu`, `shift`, `rn`, `jsr`, `rep`) execute under both the model and the
pinned reference and AGREE 6/6 over canonical end-state dumps — 51–64 compared fields
per case, `cyc` excluded by rule. Every one of the 19 declared forms is exercised by
the corpus, and the differential campaign's five measured corrections (the method
chapter lists them) are recorded in the profile's decisions.

The re-derivation stack, in layers:

- **Commit-level proof.** The crate's 17 tests (`cargo test -p semulith-dsp56300`) run
  in `make check` on every commit — decode, semantics, the dump format, the typed
  stops.
- **The live differential.** `scripts/run_dsp56300_smoke.py` re-runs the six-case
  agreement against the reference binaries — deliberately NOT a commit gate, because
  the binaries are untracked and network-acquired; it is the same honesty as the
  scalar unit's live three-way smoke.
- **The gates.** Every doctrine below re-derives its verdict from the tracked
  documents at every commit (`make gate`):

| Gate | What it re-derives for this unit |
| --- | --- |
| `EXERCISE-COVERAGE` | the declared scope vs the `.a56` corpus, both directions — 19/19, no guest instruction the scope does not name |
| `EXTRACTION` | the sibling-crate route, reported by name (a declaration contradicted by an `encoding.sexp` would be a finding) |
| `INTERACTION-MATRIX` | the 21 cells of `interactions.sexp` over the 6 axes, every disposition resolving |
| `PROFILE-CONSISTENCY` | the dossier's internal consistency (2 dossiers) |
| `DOSSIER-SCHEMA` | every dossier document validates against its schema |
| `RECORD-SCHEMA` | the requirements/obligations catalogues — statements byte-identical to the decisions, mirrors verbatim |
| `FACT-OWNERSHIP` | every restated fact has exactly one owner, every mirror a governor |
| `MATERIALS-BILL` | this book's materials tables equal the pinned dossier, regenerated in memory |
| `SCOPE-COVERAGE` | every category the declared scope requires is covered — the unit may code |

## The capability report

This unit's evidence is one half of the cross-architecture picture; the other half is
what the exercise proved about the public abstraction. The `BREADTH` gate report —
generated from pinned inputs by `scripts/gate_report.py --gate BREADTH`, gated against
drift by `GATE-REPORT` — publishes that picture per axis: the stated real subset's
evidence (this unit), the abstraction's exercised-case constructs, and the explicit
list of unclaimed families. The report lives at `docs/BREADTH-REPORT.md`.

## What the evidence does not say

- **No DSP56300 family compatibility.** The corpus is synthetic; the verdicts are
  end-state equality on it; the exclusions are named and each one bounds the claim.
- **No universal proof.** Six guests is finite, tested evidence (EVD-01); the one
  oracle's independent legs are upstream proof artifacts (EVD-04).
- **No timing claim.** `cyc` is informational and never compared.
- **No inherited evidence.** Nothing from `rv64i-lab-v0`'s gates transfers; a
  source-reviewed experimental subset cannot inherit a differentially validated claim
  from another target (`docs/EVIDENCE_AND_GATES.md` §1).
