# "Checked" means re-derived, falsified, and durable

- **Type:** `decision`
- **Date:** `2026-09-13`
- **Status:** `active`
- **Owner / source:** director standing policy; adopted by task-tree leaf `SEMULITH-PKG.2`

## The fact / decision

Semulith adopts the claim-verification standard as its definition of **checked**, stored as
the project-owned [`docs/CLAIM_VERIFICATION.md`](../CLAIM_VERIFICATION.md). A number or
finding is checked only when three *dimensionally different* questions have answers:
**re-derive** (does one command reproduce it from the source?), **falsify** (what would make
it false, and is there an oracle we did not build?), **durability** (is the producer tracked,
and does anything fail when it goes stale?). A missing leg is **named in the claim**, never
omitted.

## Why

Checking a claim twice does not make it twice as verified — a repeated pass repeats its own
blind spot. That is not a slogan here: this project's deliverable *is* claims about a
processor model, and `docs/EVIDENCE_AND_GATES.md` §1 already refuses a universal letter grade
for exactly this reason. `RULES.md` says what evidence must contain (`EVD-01`…`EVD-10`); this
standard says what must be true *before* a measurement is allowed to enter one.

Two of its rules already bind live work in this repository:

- `EVD-04` and `EVD-01` are leg 2 in Semulith's own vocabulary: Sail-derived ACT4 expected
  results and SoftFloat-derived TestFloat values are *not* independent oracles, and finite
  differential agreement is not a universal theorem.
- The `cited, not re-derivable` finding about `PACKAGE_CHECKS.md` is a leg-1 failure and was
  recorded as one rather than being summarised as "the schemas are validated".

## How to apply

- Publish a claim with its legs named: *"re-derived and falsified; **not durable** — the
  instrument is untracked."* A claim with a named gap is usable; a claim with a hidden gap is
  the defect.
- **Contract numbers are exact.** A coverage denominator, a gate verdict, a profile version,
  or a schema `$id` in a shipped data contract *is* the claim — `SRC-03` forbids inventing
  one, and trajectory-grade tolerance never applies to it.
- **Make every control go RED on purpose** before trusting it. A gate never observed failing
  is not known to work; `EVD-09`'s mutation suite is this rule with a Semulith name.
- **A claim about a set carries its enumeration** in both directions — already mechanized by
  the `GAP-CLAIM-CENSUS` doctrine.
- When a re-derivation disagrees with a published number, the re-derivation carries the
  heavier burden of proof: it has been run once, the thing it contradicts has at least been read.

Related: [[decision_delivery-provenance-is-frozen]], [[decision_public-repository-no-confidential-content]].
