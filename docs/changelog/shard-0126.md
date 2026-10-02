# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — F2's honest limit, retired (P3-BREADTH.1, slice 1)

The findings report graded itself and flagged F2 — register grouping with fill
semantics — as the one finding whose NEEDS-A-CHANGE classification rested on the state
document's shape rather than a measured refusal, and named the remedy: a grouping probe
in the synth suite. The probe is the real scalar profile's state document plus one
synthetic `register_groups` form under `integer_registers` (an odd:even pair with the
TI C64x zero-fill readout rule, locator in the descriptor's header comment), reduced
until the schema layer's ONLY refusal is the grouping shape:
`undeclared field "register_groups"`, rc 1 — the checker recurses into nested
constructs, so the pin measures the file's nesting, not just its top level. The wider
result is the routing determination: applying the findings meant measuring that the
required-unconditional set is empty. F4/F5 carry the review's own VLIW condition, F2's
implementation idles unless `.3` picks TI, F6 is per-profile work whose method already
exists and is gated. Implementing any of them today would add unexercised abstraction
surface — precisely what the tree's gate refuses ("stabilize only what has been
demonstrated"). `.1` is slice-gated, not closed: the implementation legs stay owned by
name and reopen with `.3`'s slice decision. Scalar regression re-run green across the
board (`make check` 180/180, gen_state rc 0, DEF-GEN ok, G1 `passed` re-derived).

## _(2026-10-01)_ — the routing method held (DSP-REVIEW.7, tree closed)

The tree pre-committed to its routing method before the first finding existed —
locator, executable demonstration, scalar reproduction check — and the capstone leaf
graded itself against exactly that. The payoff: the one finding that could not meet the
method (F2, register grouping, never pushed through the pipeline as a probe) is visible
as a labeled honest limit instead of passing as measured. The scalar controls did real
work too: the same generator that refuses a 24-bit state document with rc 2 emits the
scalar profile's 64-bit one with rc 0 — "the limitation does not fire for
`rv64i-lab-v0`" is a pasted command, not an argument. Six findings routed to
`P3-BREADTH`, five non-findings classified out as semantics data, and the review's
lasting discipline — a TI absence is never a DSP absence — is now the receiver's
inheritance, not just this tree's rule.

