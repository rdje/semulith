# The credit lapsed when I fixed a self-test fixture — why does a report generator pin a measurement?

**Because the case's dependency manifest pins every file its capture read, and the report generator was
one of them.** The credit's reader authenticates the whole manifest on every read (that is what makes a
credit honest when the tree moves), so a changed byte in any pinned file — a self-test control, a docstring
— lapses the credit and the derived status falls back. The rule is right; what it exposed is a *coupling*: a
reporting tool pinned beside the semantics, schemas and comparators that actually produce the measurement
couples every later report change to a re-capture of the case.

## What happened

On 2026-10-27 (`P4-SYSTEM.15` slice f) the workload campaign evidenced the last open G-REGRESSION kind.
Declaring it made the GS report generator's self-test miss: its "a not-applicable kind counts (+1)" control
appends a `not-applicable` form for the `workload` kind to a copy of the REAL manifest and expects the kind
count to rise — true only while that kind is open. The fix is six lines in `scripts/gate_report.py`; the M
case's retained `evidence/rv64gc-m-forms-v3/dependencies.sexp` pins that file (60 inputs, the generator
among them), so the fix read `credit CR-GC-M-1 lapsed: manifest input scripts/gate_report.py: SHA256
differs` and `REQ-GC-M` derived `planned`. The unit landed the campaign, its record, schema and gated
rule, and left the kind undeclared with the reason in the open row; declaring it is slice g.

## How to catch it, and what to do

- **A self-test that reads the real manifest encodes the manifest's state.** A control that assumes a
  kind is open, a count is N, a row is absent, is a prediction about the tree that the next unit falsifies
  (`a-real-tree-probe-arm-is-a-prediction-the-act-re-states.md`). Prefer synthetic fixtures; where a real
  copy is used, make the control trade a form for a form so the count holds.
- **Before editing any `scripts/*.py`, grep the retained manifests for it** (`grep -l 'scripts/x.py'
  evidence/*/dependencies.sexp`): a hit means the edit lapses a credit and needs the re-capture or a ruling,
  not a surprise at the gate.
- **A capture's dependency closure should be the measurement's, not the toolbox's.** Whether a report
  generator belongs in a case's manifest is a ruling for the capture's author; until it is made, the
  honest moves are a re-capture (a new case version with a fresh manifest) or leaving the dependent change
  undeclared and saying so where the status is read.

Evidence: `docs/tasks/P4-SYSTEM.md` `.15` slice f; target/p4-system-15/f (campaign.log, record-schema.log,
the reverted generator edit); `profiles/rv64gc-lab-v0/gate.sexp` G-REGRESSION open row.
