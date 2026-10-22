# My probe's fixture is green — how do I know it has the shape the real records have?

**Short answer:** build the fixture from a real record, or assert on the real tree what the
fixture asserts on itself. A fixture written from the reader's own expectation encodes the
author's assumption twice: the reader expects a shape, the fixture supplies that shape, and
both agree whether or not any real record looks like it. The only reading that can disagree
is one of the real records.

## The founding measurement

`scripts/requirement_status.py` (P4-SYSTEM.14 a42ap, 2026-10-21) derived each requirement's
status from the evidence cases' `property` forms, read at the experiment root. Every real
record nests them under `(verification …)`, as the schema and `scripts/review_div_policy.py`
do. Its probe's fixture wrote `(experiment (id …) (property …))` — flat — and its seventeen
tests passed in both modes on every commit. Measured on 2026-10-22 when the m-forms case was
declared (a42au): `load_cases` returned both case directories with **0 bindings**, so
`REQ-GC-M` listed no uncredited case, the declared case derived `0 declared`, and a receipt
claiming `qualification` would have credited no obligation at all — a status gate that could
not have advanced a status.

## The rule

- A fixture is a claim about the shape of the real data. Derive it from a real record (copy a
  tracked one, or generate it through the same producer the real records use), not from the
  code under test.
- Where the real tree is available, add one test that reads it and asserts the fact the
  fixture-based tests assume (here: both retained cases bind `REQ-GC-M`, one `pending`, one
  `declared`). That test fails the day the shapes diverge.
- A green probe over a self-made fixture proves the reader is consistent with the author, not
  with the records. The gate that reads the real tree on every commit is the one that can say
  otherwise — give it something to assert.

## Related

`an-oracle-can-share-the-convention-it-judges.md` (an oracle built from the implementation's
convention agrees for the wrong reason); `an-identity-proof-needs-a-must-diverge-control.md`
(a comparison that cannot fail proves nothing). Owner: `P4-SYSTEM.14` a42au,
`SEMULITH-P4-0289`; evidence `target/p4-system-14/a42au/probes-fast.log`.
