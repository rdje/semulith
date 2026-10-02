# Device-unit applicability is derived by the declared vehicle — the first device dossier rides the same rule as the DSP

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** `P5-BOARD.2` (the first device dossier, `sifive-uart-lab-v0`);
  extends [`decision_gate-applicability-by-declared-vehicle.md`](decision_gate-applicability-by-declared-vehicle.md)
  (P3-BREADTH.7) to device units.

## Context

A device unit has no instruction pipeline: no encoding space, no semantics corpus, no
guest programs, and — until the probe leaves land — no interaction matrix. The glob-driven
gates attach to its dossier the day the documents land, so the gates need a mechanical
answer to "what applies to a device?" that is *derived from a declaration*, never presumed
— the rule P3-BREADTH.7 established for the DSP's sibling-crate route.

## Decision

The `vehicle` block declares the device shape: `(route device-model)` +
`(comparison register-expectations)` (the evidence is datasheet-derived register-read
expectations under `expectations/`, EVD-05's shape at the device layer). The schema and
the gates were extended together, each change fired against a RED arm before acceptance:

- `schema/profile.sexp`: `architecture`, `base`, `harts`, `ilen`, `ialign` and
  `state.program_counter` are optional (a UART has none of them; forcing one records a
  lie — the P3-BREADTH.5 `xlen` precedent); `chapter_version`/`spec_revision` stay
  mandatory (the manual carries honest values); the scope gains `mmio_registers`.
- `schema/contract-obligations.sexp`: `direction` gains `device-guarantee`. The discharge
  rule (`scripts/discharge_assumptions.py`) keys on "not an environment-assumption", so a
  device guarantee discharges a CPU assumption **by construction** — pinned by a new GREEN
  self-test arm so a future narrowing fires RED instead of drifting.
- `schema/expectations.sexp`: `entry`/`instructions` optional (a reset/stimulus
  expectation has neither); `step.insn` carries the stimulus name. The mapping owner
  (`scripts/dossier_sexp.py`) moved in the same breath, both directions, with round-trip
  arms.
- EXTRACTION: a `device-model` unit answers the two legs a device honestly answers —
  every state element carries a reset (register families included, route-scoped so the
  DSP's reset-less families never fire), every obligation its positive AND negative checks
  — and refuses an `encoding.sexp` beside the declaration as a contradiction.
- EXERCISE-COVERAGE: the denominator census still runs (a device scope must not
  contradict its own register enumeration); the composition and guest legs are n/a by
  declaration; a `guests/` corpus beside the declaration is RED — **anti-drift: the day
  probes land (P5-BOARD.5), the gate refuses until taught the device exercise leg**.
- INTERACTION-MATRIX: no matrix is n/a by declaration (the matrix attaches with the probe
  corpus); a device unit that *has* a matrix answers the full contract unchanged.
- PROFILE-CONSISTENCY needed **no** conditional: its arms key on document presence, not
  processor shape — verified by a new GREEN device-shaped self-test arm, not by argument.

Registration-day consequences (UNIT-BOOKS, MATERIALS-BILL, SCOPE-COVERAGE, the
`materials/units.sexp` `kind` edit, the materials-bill generator's `sibling-crate`
conditionals and processor-shaped INTERNAL_CONTRACTS) are `P5-BOARD.11`'s — one
registration day for all three units.

## Consequences

- A device dossier is fully gated the day it lands — the same machinery, not a lower tier
  (`docs/EVIDENCE_AND_GATES.md` §8), and every "not applicable" is a declaration the gates
  re-derive, with contradiction = RED in both directions.
- The `profiles/*/*.sexp` git pathspec sweeps `expectations/` (depth 3) because git's
  default pathspec matching crosses `/`; DOSSIER-SCHEMA validates the device expectations
  the day they land. Device expectations live in `expectations/`, NOT `guests/` — the
  guest-corpus rules (EXERCISE-COVERAGE's exercised census, INTERACTION-MATRIX's orphan
  rule) stay guest-shaped by construction.
- The device model (Rust) is NOT this leaf's scope: the dossier is the documents the
  model route consumes. Offsets and access widths travel as prose in `state.sexp`'s
  `holds`; if the model leaf needs them machine-checkable, that is a day-of-need schema
  construct, not a silent widening.
