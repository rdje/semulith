# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-03)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — one reset, one value: the composed-field cross-check fired on the document being written (P4-SYSTEM.2 slice c1)

Execution of the `.2` brief's checkpoint (c) — split into (c1)/(c2), the seam recorded in
the tree — measured:

- **The staging problem is the design.** A state.sexp under `profiles/rv64gc-lab-v0/` is a
  refused route contradiction until the flip, so the 33-CSR document is authored at
  `target/p4-system-2/state.sexp` and validated from there — the gates that discover by
  path were measured first (DOSSIER-SCHEMA scans `profiles/*/*.sexp`, PROFILE-CONSISTENCY
  reads a sibling state.sexp, EXTRACTION the unit dir; none sees target/), and the
  validations were given scratch-path forms (`check_sexp_schema.py` takes the path, the
  new `--csr-cross` probe, `_state_resets` on the scratch dir).
- **The house shape decides the nesting.** The schema kernel's form-field rule refused my
  first draft's `(fields (field …) (field …))` and the 11-child `(candidates …)` wrapper
  by name; the construct repeats bare `(field …)` under `(csr …)`, exactly the
  `register_family` shape. The first draft also overlapped full-width `wpri_rest` rows
  with named bits — an ambiguous legalization table; a coverage probe computed the true
  gap sets.
- **One reset, stated twice, must agree — mechanically.** gen_state composes a CSR's reset
  from its per-field resets and cross-checks the csr-level declared value. It fired RED
  *naturally*, on this very document: mstatus's composite is 0xA0000000 (UXL=2 | SXL=2),
  not the hand-computed 0x300000000. The descriptor was wrong; the check named it; the
  fix was re-derivation, and the self-test arm now keeps it repeatable.
- **gen_state parameterizes, never forks** — the rv64i emission path is untouched (the
  module re-derives byte-identical under the extended generator), and the rv64gc branch
  validates by refusal (undeclared view, duplicate address, uncovered field bits, a
  privileged construct under rv64i — each named) and emits to a scratch out until (c2)
  wires the consumer. The csr name↔address ownership migration is deferred to the flip
  with its probe recorded (33/33 exact against the pinned csrs.csv).

Promotion: declined — the consistency rules are armed by self-test REDs (STATE-GEN 17,
PROFILE-CONSISTENCY 44, EXTRACTION 9), and the natural RED is recorded in the leaf.
Recorded in the owning leaf's checklist (LOCKSTEP).

