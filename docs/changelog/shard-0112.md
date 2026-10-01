# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — mid-execution snapshots (P2-SCALAR.7)

The design question was completeness, and the answer was already pinned: state.sexp's
hidden-state census (SEM-08) measured all seven candidates absent, so the snapshot is
registers + pc + memory — the sparse encoding (non-zero runs, digested over the whole
region) plus the bundle's definition-pin check (extracted as `check_definition_pins`,
shared, not duplicated) plus `run_state[_over]` (the state-returning runner form) plus
`FlatMemory::bytes_mut` for the resume rebuild. The proof suite splits all 49 guests at
three points each through the JSON round-trip — continuations identical, crossing logs
included; the memory-state guests are the load-bearing arms. RED arms refuse by name:
corrupted run (digest), foreign definition (pin), at_step>budget, a run past the region,
a partial register file, a mutant model (not offered). In-flight RED: my own test
arithmetic — the encoding splits runs at zero bytes, so "the image's first run" is ONE
byte and the overrun tamper fit; re-aimed one-past-the-end. A genuine surprise measured:
the CLI's 2 GiB region makes snapshot capture hash 2 GiB per call — seconds, acceptable
for a CLI tool, noted for the record (the suite's region is 64 KiB). Validation: 180/180
verify suites; make check/gate/book green.

Lesson: `promotion: declined` (recorded in the leaf).

