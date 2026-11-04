# Requirement status derived

The catalogue's `implementation_status` is not carried; it is derived from the
evidence graph and drift-checked, as the policy's "Status and supersession"
section requires. `scripts/requirement_status.py` is the one derivation; the
`PROFILE-CONSISTENCY` gate runs it on every commit for every profile whose dossier
carries `EVIDENCE_POLICY.md`, and refuses a status that disagrees with its
derivation. The graph it reads is bounded and tracked: `requirements.sexp`, the
effective `contract-obligations.sexp`, and every retained evidence case's
predeclaration (`planned-experiment.sexp`, which names the requirement and
obligation ids a property addresses) and derived receipt (`verification.json`, a
complete capture that carries no verdict of its own), and — since a42ay (2026-10-23) —
the profile's credit catalogue `credits.sexp`, the one crediting word. This chapter, not
the policy document, names the checker: the policy is one of the reviewed inputs the
retained case pins by SHA256, so editing it is a re-capture, not a note.

| Derived status | Rule |
| --- | --- |
| `not-applicable` | applicability `excluded` and source category `not-applicable` together — the explicit, checked argument; one without the other is a finding |
| `implemented` | research `resolved`, included, every effective obligation the requirement names credited by at least one case |
| `partial` | a credited case or an `implementation_refs` entry exists but closure is incomplete; an unresolved source question caps the requirement here |
| `planned` | no credited implementation or evidence; pending, failed, stale or refused cases are reported as uncredited, never counted |

## How a case is credited

A credited disposition is a `(credit …)` record in `profiles/<profile>/credits.sexp`
(schema `schema/credits.sexp`, validated by RECORD-SCHEMA like the other catalogues). It
names the requirement, the effective obligations and the case, pins the measured record,
the receipt and the policy document by path, SHA256 and size, and names the retained
sources it rests on, its authority, date, decision record and limitations.
`scripts/credit_records.py` reads the catalogue and reports each record `current` or
`lapsed`: current only while every pin and every input of the case's dependency manifest
still describe the tree, the receipt is a complete canonical capture with `qualification`
false, and the declaration binds the credited requirement and obligations. The derivation
credits a binding only through a current record naming its case, requirement and
obligation. A receipt whose `qualification` is true is a finding — a typed success word —
and so is a lapsed record or one naming an unknown case or requirement: a moved pin lapses
the credit, the status falls back, the recorded status drifts and the gate fails. The
policy review reports `credited` from the same catalogue and makes a record over a
measurement that is not `satisfied` a finding (`decision_credit-is-a-catalogue-record.md`).

A case naming an obligation outside the effective contract, or a requirement the
catalogue does not hold, is a finding: supersession preserves the old record and
edge and credits no successor by name. Today 46 requirements derive `planned` and two
`implemented` through two current records: `REQ-GC-M` through `CR-GC-M-3`, naming
`rv64gc-m-forms-v5`, and `REQ-D-XLEN` — the first `state` requirement — through `CR-D-XLEN-2`,
naming `rv64gc-xlen-forms-v2` (`P4-SYSTEM.14` a43b-2e, 2026-11-02). Both re-issue retired records:
the planned lapse that opens CSR-SET (a43b-2b; `decision_producer-debt-paid-before-the-next-case.md`)
moved pinned inputs of the cases `CR-GC-M-2` (v4, a44-5) and `CR-D-XLEN-1` (xlen-v1, a43a-3) named,
so both were removed with the catalogue file and the statuses read `planned` until the cases were
re-captured with their control declared (a43b-2c, a43b-2d) and credited again. The other five cases
are uncredited at `pending`: v2, v3 (`CR-GC-M-1` from 2026-10-26 until a44-2b), v4, xlen-v1 and the
CSR-SET case, captured at a43b-3f, 10 of 10 legs at a43b-3g and not yet credited. No recorded status drifts.
`python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` prints
`CREDIT-RECORDS: rv64gc-lab-v0: 2 credit(s), 2 current, 0 lapsed; records read and
authenticated, nothing granted`. The probe `scripts/probe_requirement_status.py` runs 22
synthetic-graph tests in both interpreter modes and seven seam omissions that each fail
their discriminating test. Nothing here advances a status: a credit record, with the recorded
status moving in the same commit, is the crediting act (a42az for `CR-GC-M-1`, a44-5 for its
re-issue `CR-GC-M-2`, a43a-3 for `CR-D-XLEN-1`, both retired at a43b-2b, and a43b-2e for `CR-GC-M-3` and
`CR-D-XLEN-2`), under the rulings on its authority and on the
sufficiency of one finite case (`decision_req-gc-m-credited-implemented.md`). The normative text each
rests on is retained (`RVI-M-DIV-STATEMENT`, and `RVI-M-STATEMENTS` since a42bb; `RVI-RV64I-STATEMENTS`
since a43a-2a).
