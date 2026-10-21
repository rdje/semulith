# Requirement status derived

The catalogue's `implementation_status` is not carried; it is derived from the
evidence graph and drift-checked, as the policy's "Status and supersession"
section requires. `scripts/requirement_status.py` is the one derivation; the
`PROFILE-CONSISTENCY` gate runs it on every commit for every profile whose dossier
carries `EVIDENCE_POLICY.md`, and refuses a status that disagrees with its
derivation. The graph it reads is bounded and tracked: `requirements.sexp`, the
effective `contract-obligations.sexp`, and every retained evidence case's
predeclaration (`planned-experiment.sexp`, which names the requirement and
obligation ids a property addresses) and derived receipt (`verification.json`,
whose boolean `qualification` is the only crediting word). This chapter, not the
policy document, names the checker: the policy is one of the reviewed inputs the
retained case pins by SHA256, so editing it is a re-capture, not a note.

| Derived status | Rule |
| --- | --- |
| `not-applicable` | applicability `excluded` and source category `not-applicable` together — the explicit, checked argument; one without the other is a finding |
| `implemented` | research `resolved`, included, every effective obligation the requirement names credited by at least one case |
| `partial` | a credited case or an `implementation_refs` entry exists but closure is incomplete; an unresolved source question caps the requirement here |
| `planned` | no credited implementation or evidence; pending, failed, stale or refused cases are reported as uncredited, never counted |

A case naming an obligation outside the effective contract, or a requirement the
catalogue does not hold, is a finding: supersession preserves the old record and
edge and credits no successor by name. Today the derivation is honest and small:
48 requirements derive `planned`, the one retained case (`rv64gc-signed-div-truncation-v2`)
is uncredited at `pending`, and no recorded status drifts. The probe
`scripts/probe_requirement_status.py` runs 17 synthetic-graph tests in both
interpreter modes and five seam omissions that each fail their discriminating test.
Nothing here advances a status; only executed, qualified evidence does.
