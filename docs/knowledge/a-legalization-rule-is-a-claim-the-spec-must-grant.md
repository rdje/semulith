# A legalization rule is a claim the spec must grant — find the field's own write sentence first

**Short answer:** before declaring a CSR field WARL (or WLRL) with a laboratory legal-value
set, find what the specification says a WRITE to that field does. WARL/WLRL are latitudes
the specification grants by labelling a field; where it instead states the write — "writing
a new value obtained from … into the field" — there is no latitude to take, and a
legalization rule there is a deviation dressed as a choice. A second tell: when the
specification names *reserved values* software can put in the field (and says what happens
when an instruction meets them), the field must be able to hold them.

Measured at P4-SYSTEM.7 slice (c1) (2026-10-06): slice (b) declared `frm` WARL one-of 0..4,
an illegal write retaining the old value, and recorded Sail's "stores anything" as a named
difference to explain away later. The pinned F chapter states FSRM writes "the three
least-significant bits of integer register rs1 into frm" — no legalization — and its
rounding-mode table names 101–111 *dynamic reserved rounding modes*, a state frm can only
reach by holding them (the table's 111 row: "In Rounding Mode register, reserved"). The
guest written against the WARL rule passed, the unit tests passed, the authoring tool agreed
— all three encoded the same misreading. Re-derived from the write sentence, the guest
caught the engine at once (fcsr read `0x45`; the specification gives `0xE5`).

## The pattern that works

- For every field you are about to give a discipline: quote the specification's write
  sentence (or its WARL/WLRL label) in the field's `source`/`statement`. No sentence and no
  label is a question for the specification, never a default to WARL.
- A "named difference" against a reference model is a prompt to re-read, not a place to
  park a choice: Sail storing anything was the specification's own reading.
- When a reserved value has specified consequences elsewhere (an instruction meeting it is
  "reserved behaviour"), legalizing it away makes that consequence untestable — the
  legalization deletes a behaviour the specification describes.

## Evidence

- The leaf's record: `docs/tasks/P4-SYSTEM.md` — the `2026-10-06` slice-(c) split decision
  (the defect, measured) and slice (c1)'s checklist (the RED line against the unfixed engine).
- The corrected declaration: `profiles/rv64gc-lab-v0/state.sexp` (`frm_2_0`, `(legalize (any))`
  with the FSRM sentence quoted).
