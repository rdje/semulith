# The caller names the case it binds; the retained pointer lives in a consumer no case pins

- **Type:** `decision`
- **Date:** `2026-10-22`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42av, `SEMULITH-P4-0290`; the declaration of `rv64gc-m-forms-v3`
  (a42au) and the invalidation rule of
  [`decision_stale-method-invalidates-not-locks.md`](decision_stale-method-invalidates-not-locks.md):
  a pinned input that moves invalidates the dependent evidence. Precedent for keeping a selection out
  of the pinned closure: `scripts/review_div_policy.py` and `scripts/review_div_method.py` are
  consumers outside the producer census, not children of any manifest.
answers: Which case does the evaluation bind when a second case is declared, and why does the retained pointer not live in the binding module?

## The fact / decision

The retained evaluation bound `G.reviewed_case(G.CASE_ID)`, the module constant of
`scripts/matched_gpr_property.py` naming the retained case. With a second case declared that is a
contradiction with two horns: capturing the m-forms case would bind the retained case's properties
against the m-forms record and refuse by name, while moving the constant to the m-forms case is an
edit to one of the 64 pinned children of every declaration — it invalidates the declaration just
committed (a42au) and points the method and policy reviews at a measured record that does not exist.

1. The case is an argument of the callers that know it: `evaluate_retained_unit(..., case_id=…)`,
   `capture_and_evaluate(..., case_id=…)`, `matched_gpr_adequacy.freeze_review(..., case_id=…)`
   (the review carries its case), `capture_div.capture(case_id)` passes the case it prepares. The
   default everywhere is the retained case, so every existing caller and fixture is unchanged; an
   unknown case refuses before any artifact read or process.
2. The retained, captured case is named by the consumers that read it — `review_div_method.py`'s
   `RETAINED_CASE_ID` and `review_div_policy.py`'s `CASE_ID` — which no manifest pins. Moving them to
   the next captured case invalidates nothing. `matched_gpr_property.CASE_ID` remains the default
   selection for commands and fixtures, not the binding's authority.
3. The m-forms declaration was re-emitted once over the edited modules before any capture: the
   dependency manifest, the authority record and the planned record's manifest pin changed; every
   property, input, observation and run declaration stayed byte-identical. Re-emitting a declared,
   uncaptured case is the designed path (`evidence/README.md`: an affected input change requires fresh
   declarations before execution); retained observations are never touched.

## Why

The alternative of binding the case the record itself declares (`experiment["id"]`) would make every
synthetic fixture — which carries its own identity — either unsupported or renamed to a reviewed
case; the explicit argument keeps the record's identity and the reviewed case as two facts the
caller must agree on, which is what the binding checks. Keeping a selection inside a pinned module
costs one re-declaration per switch and ties an unrelated review to it; the a42at commit paid that
cost once (the v2 case `invalidated` by its own binding's edit) and this record stops it recurring.

## How to apply

- A capture names its case: `capture_div.py --capture --case <id>`; the evaluation binds that case or
  refuses by name. Never move a constant in a pinned module to select a case.
- When a capture lands, switch `RETAINED_CASE_ID` and `review_div_policy.CASE_ID` and the measured pins
  in the same commit as the retained observations; no declaration moves.
- A pinned-module edit between a declaration and its capture re-emits the declaration (the planned
  record changes only in its manifest pin) — compare the before/after pins and say what moved.
