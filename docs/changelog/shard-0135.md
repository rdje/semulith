# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — the first DSP instruction executes (P3-BREADTH.4, slice 3)

A bounded model earns its keep in the details nobody warns you about. Three earned their
record this slice. (1) The manual's own extraction lies: FM Table 5-1's U-bit row says
"set if the two MSBs are identical" in prose and prints "U = (Bit 47 xor Bit 46)" as the
equation — an inversion (the equation should read xnor), proven by the reference's
`sr c00310`, which agrees with the prose. The differential harness exists for exactly
this class of question: when the document disagrees with itself, the measured machine is
the arbiter, and the arbitration is recorded where the next reader meets it (`exec.rs`'s
module docs). (2) A naming convention is a fact with an owner: the crate's state module
was born `state.rs`, and FACT-OWNERSHIP refused the commit because this repo has already
decided that `crates/*/src/state.rs` means "a GENERATED mirror of a profile's
`state.sexp`". Renaming to `machine.rs` was not routing around the gate — it was
learning that the name was already taken by a stronger claim. (3) The honest dump has a
hole in it: the runner emits no `cyc` line, because the reference's cycle counts are
base-table informational and a fabricated number would be a timing claim by stealth. The
comparator skips `cyc` by a recorded rule with the reason in its header — an absence
with a name, like every other exclusion in this subset. The reward: the demo guest's
dump is byte-identical between the two engines, 53 fields, on the crate's first run.
Promotion: declined in the leaf (the crate, the comparator, and the recorded inversion
are the durable outputs, living where the next evaluator meets them).

