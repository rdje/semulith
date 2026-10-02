# My new unit isn't a processor — how do the gates know what applies to it?

**Declare the unit's `vehicle` in its `profile.sexp`, and let the gates derive
applicability from the declaration plus the documents — never by exemption, never by
absence.** The unit declares `(vehicle (route …) (comparison …))`; each instruction-shaped
gate (EXTRACTION, EXERCISE-COVERAGE, INTERACTION-MATRIX) reads the route and applies only
the legs the unit honestly answers, and a document that contradicts the declaration is a
finding, not a pass.

Recorded `2026-10-02` from `P5-BOARD.2` (the first device dossier), extending the
P3-BREADTH.7 rule ([`decision_gate-applicability-by-declared-vehicle`](../decisions/decision_gate-applicability-by-declared-vehicle.md);
the device sibling is [`decision_device-applicability-by-declared-vehicle`](../decisions/decision_device-applicability-by-declared-vehicle.md)).

## The shapes that exist

| Route | Comparison | For | The legs that apply |
| --- | --- | --- | --- |
| `generated-definition` (default, undeclared) | `per-step-trace` | rv64i-lab-v0 | the full extraction/composition/guest contract |
| `sibling-crate` | `checkpoint-end-state` | dsp56300-lab-v0 | end-state evidence against a pinned reference; no composition leg |
| `device-model` | `register-expectations` | sifive-uart-lab-v0 | state resets + obligation checks both ways; scope census still runs; no matrix until the probe corpus lands |

## The rules that make it honest

- **Contradiction is RED in both directions.** An `encoding.sexp` beside a non-generated
  route refuses; a `guests/` corpus beside `device-model` refuses — the day P5-BOARD.5's
  probes land, EXERCISE-COVERAGE fails until taught the device exercise leg. A silent pass
  is the drift this refuses.
- **"Not applicable" is derived, not skipped.** The verdict lines name the unit and the
  declaration (`device-model route declared — …`), so a bystander can see WHY a leg did
  not run.
- **The schema and its mapping owner move together.** A scope group is born in
  `schema/profile.sexp` AND `scripts/dossier_sexp.py`'s `_SCOPE_LISTS` in the same commit;
  a schema widening without the mapping owner (or the reverse) is the measured split-brain
  this pairing exists to prevent.
- **Registration is a separate day.** The glob-driven gates (DOSSIER-SCHEMA, RECORD-SCHEMA,
  PROFILE-CONSISTENCY, the three above) decide an UNREGISTERED dossier fully; what
  registration adds (UNIT-BOOKS, MATERIALS-BILL, SCOPE-COVERAGE) waits for its owning leaf
  with the owner named in the dossier's status table — honesty with an owner, not a lower
  tier.
