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
edge and credits no successor by name. Today 45 requirements derive `planned` and three
`implemented` through three current records:

| Requirement | Record | Case | Category, risk |
| --- | --- | --- | --- |
| `REQ-GC-M` | `CR-GC-M-3` | `rv64gc-m-forms-v5` | `defined`, medium |
| `REQ-D-XLEN`, the first `state` requirement | `CR-D-XLEN-2` | `rv64gc-xlen-forms-v2` | `defined`, low |
| `REQ-D-CSR-SET`, the first `implementation-defined` one | `CR-D-CSR-SET-1` (a43b-3h, 2026-11-04) | `rv64gc-csr-set-v1` | `implementation-defined`, high |
| `REQ-D-ZICNTR` | `CR-D-ZICNTR-1` (a43c-5, 2026-11-05) | `rv64gc-zicntr-v1` | `implementation-defined`, high |

The first two (`P4-SYSTEM.14` a43b-2e, 2026-11-02) re-issue retired records:
the planned lapse that opens CSR-SET (a43b-2b; `decision_producer-debt-paid-before-the-next-case.md`)
moved pinned inputs of the cases `CR-GC-M-2` (v4, a44-5) and `CR-D-XLEN-1` (xlen-v1, a43a-3) named,
so both were removed with the catalogue file and the statuses read `planned` until the cases were
re-captured with their control declared (a43b-2c, a43b-2d) and credited again. The other four cases
are uncredited at `pending`: v2, v3 (`CR-GC-M-1` from 2026-10-26 until a44-2b), v4 and xlen-v1. No
recorded status drifts.
`python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` prints
`CREDIT-RECORDS: rv64gc-lab-v0: 4 credit(s), 4 current, 0 lapsed; records read and
authenticated, nothing granted`. The probe `scripts/probe_requirement_status.py` runs 22
synthetic-graph tests in both interpreter modes and seven seam omissions that each fail
their discriminating test. Nothing here advances a status: a credit record, with the recorded
status moving in the same commit, is the crediting act (a42az for `CR-GC-M-1`, a44-5 for its
re-issue `CR-GC-M-2`, a43a-3 for `CR-D-XLEN-1`, both retired at a43b-2b, a43b-2e for `CR-GC-M-3` and
`CR-D-XLEN-2`, a43b-3h for `CR-D-CSR-SET-1`, and a43c-5 for `CR-D-ZICNTR-1`), under the rulings on its authority and on the
sufficiency of one finite case (`decision_req-gc-m-credited-implemented.md`). The normative text each
rests on is retained (`RVI-M-DIV-STATEMENT`, and `RVI-M-STATEMENTS` since a42bb; `RVI-RV64I-STATEMENTS`
since a43a-2a; `RVP-CSR-STATEMENTS` since a43b-3b; `RVI-ZICNTR-STATEMENTS` and `RVP-COUNTEREN-STATEMENTS` since a43c-1).

`CR-D-CSR-SET-1` claims the committed set, and its record says what that leaves out
(`decision_req-d-csr-set-credited-implemented.md`):

| Not claimed | Why | Whose it is |
| --- | --- | --- |
| `mip`'s value directly | the case's CLINT holds `mip.MTIP`; `mip` is read with `rd` = x0 and its bits witnessed through `sip` | this case's configuration |
| a CLINT or any device | it is the reference's source of time for this case; the laboratory declares none | not claimed |
| a non-member address trapping | the spec-side deriver's vocabulary is the 33, and it is a pinned input | not witnessed; the negative side is the refused write and the privilege-refused access |
| field semantics | "Per-CSR field semantics (WPRI/WARL/WLRL) belong to the privilege leaf" | `P4-SYSTEM.2` |
| counter rates, timer delivery, numerics | each is witnessed as a member of the set, not as its behaviour | `REQ-D-ZICNTR`, `REQ-D-SSTC`, the F and D cases |

Its dependencies `REQ-D-PRIV-MODES` and `REQ-D-SSTC` stay `planned`: the derivation reads
obligations, and the capture plan orders CSR-SET before ZICNTR and SSTC.

`CR-D-ZICNTR-1` claims what the case read: the three base counters and the two machine views in M, their
progress, five refused write attempts with `rd` kept, a trap that retires nothing, each gate bit of `mcounteren` and
`scounteren` in S and U, and two alias pairs. Its record says what that leaves out
(`decision_req-d-zicntr-credited-implemented.md`):

| Not claimed | Why | Whose it is |
| --- | --- | --- |
| a write through `mcycle` or `minstret` | the spec-side deriver refuses it, and the laboratory's `time` is a view of `mcycle` where the reference's comes from its CLINT, so a write would separate them | not witnessed |
| Zihpm's absence | the deriver's vocabulary is the 33 | not witnessed; a statement of the selection |
| rate and progress semantics | "the counters' rate and progress semantics are the environment contract's to declare" | `P4-SYSTEM.5`, `P4-SYSTEM.9` |
| a CLINT or any device | it is the reference's source of time for this case; the laboratory declares none | not claimed |
| timer delivery | no interrupt or wait is scheduled | `REQ-D-SSTC` |

Its dependency `REQ-D-PRIV-MODES` stays `planned` for the same reason as CSR-SET's. Its measured record is not copied into the dossier either.

Its measured record is not copied into `references.sexp`, so `G-TRACE`'s table lists the M and XLEN records
only. The copy would take the file to 77,669 B against the family's 65,536 B per-part ceiling, and moving the copies elsewhere
would edit a pinned tool and lapse all three credits. The status does not rest on the copy: the record pins
`evidence/rv64gc-csr-set-v1/measured-experiment.sexp`, and the method review validates its graph on every read. The
director ruled on 2026-11-04 (`decision_dossier-copies-retire-at-the-next-window.md`): ZICNTR and SSTC follow the same way, and the next pinned window retires
all the copies, so `gate_report.py` reads each credited case's record from `evidence/`. That window also moves `contract_measure` out of `gate_report.py`, the one import that makes a
report generator a pinned input of every experiment, so editing a report never lapses evidence again.
