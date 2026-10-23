# Ten legs satisfied is a measurement; the credit is a separately owned act

- **Type:** `decision`
- **Date:** `2026-10-23`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a42ax, `SEMULITH-P4-0292`; continues
  [`decision_policy-legs-measured-two-pending.md`](decision_policy-legs-measured-two-pending.md)
  (a42aq: eight legs, two pending, measurement grants no credit) after the m-forms capture
  (a42aw) and the retained pointers' switch
  ([`decision_caller-names-the-case.md`](decision_caller-names-the-case.md)).
answers: What does the retained case measure now that the m-forms capture is retained, and what does a fully satisfied measurement still not do?

## The fact / decision

With `scripts/review_div_method.py` and `scripts/review_div_policy.py` pointed at
`rv64gc-m-forms-v3` (the consumers only; no pinned module moved, so no declaration was
invalidated), the real tree measures on 2026-10-23:

1. Finite method `satisfied`: record `valid`, capture binding `matched`, evaluation `pending`,
   85 files / 1,076,834 B authenticated, 40,438 snapshot bytes, 1,142,222 charged of 134,217,728,
   39 checker sources matched; measured record 16,942 B
   `fb22d5e5554a0e132c231e5551ed8314ab4be35ff93e7f086fceeacb6235a152`.
2. Policy `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit`: the twelve
   Table 1 rows (steps 20–24, 26–32) present and all predeclared, 13 of 13 forms predeclared and
   exercised, control DIVERGE at step 12 x15 as the `control_run`'s property names.
3. `credited` is false, the receipt's `qualification` is false and `scripts/requirement_status.py`
   derives `REQ-GC-M` `planned` with both cases pending and none credited.

A satisfied measurement is what the policy calls the input to a crediting record. It is not the
record. Crediting is a separately owned act with its own authority and mechanism — open
questions the next unit answers, not this one: `requirement_status.credited()` reads a receipt's
`qualification`, but a retained receipt is never replaced, so the credit cannot be a rewrite of
`verification.json`; and only the DIV statement is a retained normative excerpt
(`profiles/rv64gc-lab-v0/retained/div-statement.html`) while the multiply and Table 1 statements
the 25 properties cite are cited in the expectations, not retained.

The first case, `rv64gc-signed-div-truncation-v2`, stays `invalidated` history: its bytes are
untouched, its measurement (8 of 10, then invalidated by its own binding's edit at a42at) is
recorded, and nothing reruns it.

## Why

The policy's words ("Public reference agreement adds only its declared observations"; a credited
disposition is the output of a crediting record, not of a measurement) are the reason the
measurement and the credit are two acts. Letting the measurement credit would make the consumer
the authority over the requirement it reads, which is the "typed success word substitutes for
executed evidence" failure the gate refuses. The two open questions above are exactly what a
crediting record must settle in writing before any status moves.

## How to apply

- Read `python3 -B scripts/review_div_policy.py` as a status of the retained bytes. `satisfied`
  means every leg is met; it never means credited.
- The crediting act is its own task-tree leaf and its own decision record: name the authority
  (who credits, on what retained excerpts), the mechanism (a new record the status derivation
  reads, never a replaced receipt), and the retained normative statements it rests on.
- Switching the retained case again follows a42ax: pointers in the two consumers, the fixture and
  real-tree arms of their probes, the chapters and the toolbox rows, in one commit with no
  pinned-module edit.
