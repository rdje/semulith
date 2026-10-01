# Gates derive per-unit applicability from the declared vehicle — no deferral machinery

- **Type:** `decision`
- **Date:** `2026-10-01`
- **Status:** `active`
- **Owner / source:** `P3-BREADTH.7` (land the dsp56300-lab-v0 dossier as governed
  documents); the fork was framed by `P3-BREADTH.5` slice 2's measured attachment table
  and delegated to the executing engineer by the director (`2026-10-01`).

## The question

Landing `profiles/dsp56300-lab-v0/{profile,state}.sexp` attaches three gates whose
contracts presume the rv64 evidence shape (measured, `.5` slice 2): EXTRACTION (an
encoding composition + semantics corpus), EXERCISE-COVERAGE (composition closure +
per-step `*.expected.sexp` guests), INTERACTION-MATRIX (an `interactions.sexp`). How do
the gates stay green honestly for a unit whose model is a hand-written sibling crate and
whose comparison is checkpoint-level end-state equality?

## Rejected: named deferrals

A per-unit "this gate is deferred, owner leaf X" declaration with expiry teeth (RED when
X closes). Rejected: it is a **weakening surface** — machinery whose only function is to
let a gate not apply — built for exactly one unit, once: the speculative generality P3
exists to refuse, one layer up. Its expiry discipline also answers the wrong question:
the gates' contracts do not become applicable when a leaf closes; they become applicable
when the unit's DOCUMENTS exist — which the gates already re-derive per commit.

## Rejected: the full evidence-shape machinery

Teach every gate the DSP's evidence shape whole: per-step expectation documents for the
DSP guests, a 21-cell rv64-style exercised matrix, the extraction contract applied to the
hand-written crate. Rejected: it builds evidence artifacts the subset's claim never cites
(the claim is canonical end-state agreement on six synthetic guests) — machinery without
a consuming claim, and the per-step shape would be a fiction over a checkpoint-compared
target.

## Adopted: applicability derived from declaration + documents

Each unit's `profile.sexp` may declare its **vehicle**: `(vehicle (route …) (comparison
…))` — `generated-definition|sibling-crate` and `per-step-trace|checkpoint-end-state`,
authority `laboratory`, with a source. Gates then apply the contracts that match the
declaration, and nothing is ever silently skipped:

- **EXTRACTION**: a `sibling-crate` route is reported by name; the composition contract
  applies iff `encoding.sexp` exists. A declaration contradicting the documents (a
  sibling-crate declaration beside an `encoding.sexp`, or vice versa) is a finding —
  applicability is re-derived per commit, so a stale declaration fails instead of
  drifting.
- **EXERCISE-COVERAGE**: a `checkpoint-end-state` comparison runs the guest census both
  directions — every declared scope mnemonic must appear in a tracked guest source, and
  every guest instruction must be inside the declared scope — over the unit's actual
  guest format (`.a56` for the DSP). The composition leg applies iff `encoding.sexp`
  exists. The claim "every declared form is exercised" is measured, not waived.
- **INTERACTION-MATRIX**: no gate change. The schema is shape-generic and dispositions
  include `mechanism` (a closed artifact+needle registry, extended by two DSP entries,
  each naming its case) and `degenerate` — subset v0 carries a real minimal matrix: six
  axes (progress, stop, loop, stack, alias, state), 21 cells, every disposition resolving
  to the smoke driver, the typed-stop type, or a cannot-arise reason.

Plus the surfaced gap, closed in the same leaf: a **dossier schema-validation gate** —
every tracked `profiles/*/*.sexp` whose basename has a same-named `schema/*.sexp`
validates against it (the D-FENCE double-note drift lived unseen without it).

## Bounds

- The vehicle declaration is laboratory data about THIS unit's evidence route, never a
  claim about what the unit proves. The claim surface is unchanged: the smoke (not a
  commit gate) and the crate's tests (the commit-level proof).
- A unit that declares neither vehicle field is treated exactly as today (the rv64 path
  is byte-untouched in behavior — measured by the gates' self-tests and the rv64
  regression re-run).
- When the DSP's encoding route is later built (the `.5` slice-3 reopening conditions),
  the declaration is removed and the full contracts attach — no expiry machinery needed,
  because the contradiction findings above fire the day the documents and the
  declaration disagree.

Related: [[decision_dsp56300-lab-v0-subset]], [[decision_lane-consumption]],
[[decision_interpreter-before-compiler]].
