# One case declares many predeclared properties; the control discriminates one; every value is held to the source derivation

- **Type:** `decision`
- **Date:** `2026-10-22`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42at, `SEMULITH-P4-0288`; the policy measurement of a42aq
  (`boundary-fixtures` and `form-coverage` pending: six Table 1 rows present, none predeclared; one of
  thirteen forms predeclared) and the a42ar program `profiles/rv64gc-lab-v0/guests/m-forms.s`;
  `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md` "Risk and feature obligations" ("at least one
  discriminating negative control") and "Records, controls and currentness" ("Public reference
  agreement adds only its declared observations"). Precedents:
  [`decision_policy-legs-measured-two-pending.md`](decision_policy-legs-measured-two-pending.md),
  [`decision_stale-method-invalidates-not-locks.md`](decision_stale-method-invalidates-not-locks.md).
answers: How does one capture satisfy the boundary-fixtures and form-coverage legs, what does the control run discriminate when a case declares twenty-five properties, and where does each predeclared value get checked?

## The fact / decision

The policy credits only declared observations, and its two pending legs ask for one capture that
predeclares every Table 1 row and every M form. Until a42at the property binding supported exactly
one property per case: the relation binder required one `property` record, the context carried one
statement and one witness, the evaluation and the collector read `graph["property"][0]`, and the
policy's control leg read the first property's witness.

1. **A case table, not a case swap.** `scripts/matched_gpr_property.py` owns the reviewed cases.
   `rv64gc-signed-div-truncation-v2` keeps its one property (`signed-quotient`, boundary 2, x7, −3)
   and stays the retained case (`CASE_ID`) that the method review, the policy review and the capture
   command select. `rv64gc-m-forms-v3` is declared beside it before its declaration record and its
   capture: 33 boundaries over `m-forms.s`, 25 properties — the 13 forms once each (`form:<mnemonic>`)
   and the 12 Table 1 cells (`table1:<row>`) — each with a reviewed RV64 value, and the reviewed
   instruction word of every one of the 33 boundaries. The probe re-derives every word from the
   encoding fields and every value from plain integer arithmetic and the chapter's Table 1 rules,
   independently of the author and the assembler.
2. **The relation plan carries every declared property.** `RelationPlan.properties` holds one
   `PropertyRelation(property_id, witness)` per declared property, one to sixty-four, each a
   `gpr-change` property with a typed in-budget witness, no two witnessing the same step and
   register. The control run names exactly one declared property: `control_property_id`, whose
   witness `control_witness` is the witness the three-run byte comparison discriminates.
3. **One control, many values.** The byte comparison keeps its single witness (the control's), and
   the source-value finding is computed for that witness; the binding then reads every other
   predeclared value from the source derivation that finding already carries, so no second source
   read and no arithmetic engine is introduced. A property whose witness is not an actual derived
   register change carrying exactly the reviewed value refuses by name
   (`predeclared value differs from the source derivation: <property>`).
4. **Claims are the record's own words.** The evaluation and the collector build one
   `PropertyClaim` per declared property from the record — identity, requirement, obligations,
   statement, and the relation plan's witness for it — and the binding requires the sorted claims,
   the control's identity, the program and the authority to equal the reviewed case exactly.
   A record that declares a property the case does not review, or renames one, is refused
   (`property claims differ from reviewed finite case`); identities are reviewed, not labels.
5. **The policy's control leg reads the named property.** `scripts/review_div_policy.py` takes the
   discriminating witness from the `control_run`'s `property_ids`, not from the first property.

## Why

Three alternatives were weighed. One case per property means twenty-five captures of three runs
each for one requirement, and the legs ask for one case that predeclares the rows. One control per
property contradicts the method: the three-run unit has one control, and the policy asks for at
least one discriminating negative control, not one per observation. Reading the other values from
the expectation file would check the author against itself; the derivation is the independent
source-side reading the finite method already trusts for the control, so holding every predeclared
value to it costs nothing new and credits nothing new.

The retained case is invalidated by this commit, as a42as designed: the binding is one of its 64
pinned inputs, so the method reports `stale`, the policy `invalidated` with exit 0, and the next
capture supersedes it. Nothing is credited or removed; `REQ-GC-M` keeps deriving `planned`.

## How to apply

- A new reviewed case is a new builder in the case table with its reviewed words and values; the
  probe's independent re-derivation is the review's second leg, written before the declaration.
- `capture_div.py --declare` emits one `property` form per reviewed property and a `control_run`
  naming the control's property; the planned record may hold up to sixty-four properties.
- The control's property is the one whose value the mutant expectation changes; for the m-forms
  case that is `form-div` (boundary 12, x15, −3 → −4), the same discrimination as the retained case.
- `RelationPlan.control_witness` is the comparison witness; `RelationPlan.properties` is the
  declaration. A consumer that needs "the" witness needs the control's.
