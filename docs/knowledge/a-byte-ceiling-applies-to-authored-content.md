# When does a byte ceiling apply to a generated file?

**Short answer:** only to authored content. A size ceiling's founding failure mode is
silent accretion in hand-maintained files; a regeneration-gated derived file cannot
accrete silently — every byte is re-derived from its canonical input on every commit —
so the ceiling taxes a property the file cannot have. Exempt it **as a checked
property** (never a declaration), and keep the aggregate bounds, which measure the
population rather than one file's character.

## The principle: the instrument must match the failure mode

Before reaching for a bound, name the failure it catches and ask whether the target can
present it. Measured counterexample (P5-BOARD.3, 2026-10-02): a board's *composed*
catalogues — the byte-exact merge of three already-bounded unit dossiers, re-derived by
a registered doctrine on every commit — fired the authored per-part ceiling and forced
a reviewed raise **one day after** the previous one. The raise reviewed a number; the
property that mattered was the derivation, which the number says nothing about.
Composition depth (computer → board → soc → …) would have made the ceremony recur per
level.

## The pattern that works

- The exemption must itself be **checked**, or an authored file will smuggle under it.
  The working rule (README-ROUTING-CLOSURE, P5-BOARD.12): a family member over the
  authored ceiling must be registered in `doctrine/fact_ownership.tsv` as a *mirror*
  with a **regeneration-doctrine** governor (a closed set, each re-deriving bytes
  byte-exact). The registry is already completeness-checked, so consuming it adds no
  second declaration surface.
- The discriminating line is **byte-re-derived vs authored-and-cross-checked**: a
  mirror governed by a *validation* gate (RECORD-SCHEMA & kin) keeps the authored
  ceiling — the content is human-authored even where cross-checked.
- **Aggregates still apply** to derived members: population surprises (a generator
  writing an unexpected *set* of files) are census-level, and no per-part rule sees
  them.
- If the governor leaves the doctrine registry, the exemption decays into a breach the
  same commit — never into a blind spot.

The ruling in full: `docs/decisions/decision_derived-members-of-bounded-families.md`.
