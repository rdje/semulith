# The retained DIV case's policy legs are measured, and two stay pending

- **Type:** `decision`
- **Date:** `2026-10-21`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42aq, `SEMULITH-P4-0285`; `scripts/review_div_policy.py` on
  the real tree prints `DIV-POLICY: pending — 8 of 10 legs satisfied; missing boundary-fixtures,
  form-coverage; no qualification credit`. Precedents:
  [`decision_sail-gpr-comparison-method.md`](decision_sail-gpr-comparison-method.md) (finite
  method checked, full policy pending) and the policy itself, `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md`.
answers: Which bytes does the retained DIV case pin, and why can a leg never be closed by editing them, the expected author included?

## The fact / decision

The policy's requirements for a `defined` requirement of low or medium risk are read as ten
measurable legs: source-located expectations, boundary fixtures, matched reference
comparison, repeated execution, a discriminating control, record linkage, currentness, the
risk method, the feature rules and form coverage. The retained case
`rv64gc-signed-div-truncation-v2` satisfies eight from its own bytes. Two stay pending:
six Table 1 boundary rows are present in the program and the expectation file but none is
predeclared as a property, and one of the thirteen M forms is predeclared (four are
exercised). The feature disposition for `OB-GC-M` is declared: none of the seven feature
families applies to integer multiply/divide. The measurement grants no credit — `credited`
is always false — and a receipt whose `qualification` is true while a leg is pending is a
gate failure. `REQ-GC-M` keeps deriving `planned`.

## Why

- The predeclaration's own limitation line said only "full source/risk/feature policy
  remains pending", without naming which legs; nothing measured them, so the next capture
  could not know what to predeclare.
- The policy credits only declared observations. The boundary rows agreed with Sail on the
  baseline, but an undeclared agreement is not a predeclared property, and relabeling the
  retained bytes is exactly what the retained-identity controls refuse.
- The policy document is one of the case's 64 pinned reviewed inputs (the first a42ap gate
  run refused 30 arms after a one-paragraph edit to it). A currentness leg that reads the
  pin makes that fact visible instead of surprising.
- A feature disposition inferred from mnemonics would be the "unmapped obligation" the
  policy forbids; declaring it in the consumer keeps it tracked and reviewable.

## How to apply

- A crediting capture predeclares one property per Table 1 row and covers every M form
  with a program, expectations and properties of its own; the consumer must then measure
  `satisfied` before any record cites it. `qualification` stays the only crediting word the
  status derivation reads; a crediting record is separate, later work.
- Never close a leg by editing bytes the case pins: the policy, the guest, the expectation
  file, the predeclaration or the expected author. A policy change is a new tracked declaration
  and a capture.
- A new obligation needs its feature disposition declared in `FEATURE_DISPOSITIONS` before
  its legs can be satisfied; a high- or critical-risk requirement stays pending until a
  second-method vocabulary exists.
- Related: [[sail-gpr-comparison-method]], [[decisions-family-second-rederivation]].

## Measured again: the expected author is a pinned input (a42ar, 2026-10-21)

The first commit of `SEMULITH-P4-0286` added one line to `scripts/derive_rv64gc_expectations.py`,
a `PARCEL_OWNED_GUESTS` entry registering the new corpus program. The pre-commit gate refused it:
`DIV-POLICY: blocked — 6 of 10 legs satisfied; missing boundary-fixtures,
matched-reference-comparison, currentness, form-coverage; FINDING finite method not satisfied
(stale)`. Of the 64 pinned children exactly one differed from the staged tree, the author. The
currentness leg did what it is for: evidence derived with an author is invalid once the author
differs, whether or not the edit touches a derivation. Restoring the author returned the method to
`satisfied` and the line to `pending — 8 of 10`; the program is checked with its explicit budget
(`--check --parcels --steps 33`) and its ownership is registered together with the fresh capture
that pins the changed author. The focused runner cannot see this: the finite method runs only in
`check_profile_consistency.sh`. A unit that edits any path under `evidence/<case>/dependencies.sexp`
runs that gate before its commit.
