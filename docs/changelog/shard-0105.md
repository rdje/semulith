# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — the ACT4 RV64I campaign: 51/51 three-way, recorded and gated (P2-SCALAR.5, strand 2c)

The fleet run was green on the first attempt — and the first obligation was to prove the
green was real, not an extraction artifact. The cross-check: the extracted slot census
(17,017) reconciles EXACTLY against the measured static counts — 18,092 RVTEST_SIGUPD
instances, minus 1,530 dead-path instances in the six branch tests (255 each: sigupds sit
on both paths, one executes), plus 414 store-test read-back slots (sb/sd/sh/sw record
2n+1), plus 51 final_sig_offset words. Per-file deltas are uniform (+1 everywhere except
the ten explained files), and all three models agree on every count. The record is
`act4.sexp`, emitted by the runner from measured rows; RECORD-SCHEMA rule 13 re-derives
its three carried counts and closes the verdict vocabulary (self-test +5 arms, 39/0).
Two in-flight REDs, both authoring-side, both caught by the schema layer before any
commit: `(min N)` is a repeat-occurrence facet, not an integer bound (the kernel refused
it by name), and atom fields are exactly `(name value)` — the emitter's multi-value
`sparse_paths`/`evidence_note` failed uniform arity; fixed at the emitter, the record
regenerated. Ceiling re-derivations (profiles/ 99→104 files, bytes untouched at 0.83×;
schema/ health 16→18) are recorded in the registry with grounds. The campaign's standing
is stated everywhere it appears: external tests with Sail-derived expectations — EVD-04's
shared-ancestry row already forbids reading them as a second opinion.

Lesson: `promotion: declined` — the reconciliation arithmetic and the two REDs are in the
leaf's verification log where they bite.

