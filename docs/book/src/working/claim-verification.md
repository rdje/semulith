# What "checked" means

This project's deliverable is claims about a processor model. So the definition of *checked* is
a load-bearing contract, and it is project-owned as `docs/CLAIM_VERIFICATION.md`.

## The three legs

Checking a claim twice does not make it twice as verified — a repeated pass repeats its own
blind spot. Verification must be *dimensionally different*:

| Leg | The question | What holds it here |
| --- | --- | --- |
| 1 — **re-derive** | does it reproduce, by command, from the source? | `TASK-ACCEPTANCE`: every hard-gated box carries real tool output |
| 2 — **falsify** | what would make this false, and is there an oracle I did not build? | `EVD-04` reference ancestry, `EVD-09` mutation suite, `GAP-CLAIM-CENSUS` |
| 3 — **durability** | is the producer tracked, and does anything fail when it goes stale? | `docs/provenance/` dispositions, the project doctrine gates, `EVD-07` invalidation |

A claim ships with its legs named. **When a leg is missing, name it** — *"re-derived and
falsified; not durable, the instrument is untracked"* is a signoff-grade sentence. A claim with
a named gap is usable; a claim with a hidden gap is the defect.

## The checks that cannot fail

Before trusting a check, ask what class of bug it still permits:

- `sum(parts) == total` catches dropped rows and double counts, and permits **any
  redistribution between parts** — so it is useless against a tool whose job is allocation;
- tests written from the same document as the implementation catch typos and permit **every
  misreading of that document**;
- a per-item fact checked against its *container's* data reproduces perfectly while being
  wrong for every item whose answer differs from its container's.

The general form: **a check and the thing it checks must not share a parent.** This is why
`EVD-01` refuses to call differential agreement a proof, and why ACT4's Sail-derived expected
results are external tests rather than a second semantics.

## Two habits this repository actually practises

**Make the control go RED on purpose.** Every project doctrine gate ships a `--self-test` whose
failing arms assert the *reason* as well as the verdict, and each was fired against the real
corpus before being registered. A control never observed failing is not known to work; two such
controls caught real defects in their own checkers before those checkers were trusted.

**A claim about a set carries its enumeration.** *"Nothing checks X"* is refuted by a single
counterexample, so it is a census, not an impression — and `GAP-CLAIM-CENSUS` requires the
enumerating command beside it. The mirror is equally wrong: a search returning N hits is a
*population*, not a defect count.

## Grading a published claim

When a claim is challenged, three axes are graded separately:

| Axis | Standard |
| --- | --- |
| **prose** | must stay true across every re-verification — it is the claim; the numbers are its evidence |
| **number** | must stay close *on the aspect it measures* |
| **named instance** | **exact, no tolerance band** — an aggregate may be an estimate, a named row is an assertion |

And a **contract number** — a coverage denominator, a gate verdict, a profile version, a schema
`$id` in a shipped data contract — *is* the claim. Trajectory-grade tolerance is never extended
to one: those are exact and gate-held, or they are not published.

One rider that cuts both ways: when a re-derivation disagrees with a published number, **the
re-derivation carries the heavier burden of proof.** It has been run once; the thing it
contradicts has at least been read.
