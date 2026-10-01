# `synth24` — the synthetic stress fixture (DSP-REVIEW.6, task card T010)

⛔ **SYNTHETIC.** The descriptors in this directory describe **no real processor**. They
exist to measure where Semulith's pipeline (the state generator, the schema layer) refuses
the shapes a real DSP would need: nonstandard widths, a second address space, packets,
delayed effects, and register grouping. **Its passing evidence may never be cited for a
real DSP claim** — that is the leaf's acceptance rule, and it applies to every file here.

## What it is

Five descriptors, each carrying exactly one synthetic shape, and
`run_synth_probes.sh`, which pushes each through the real pipeline and pins the measured
refusal:

| Probe | Shape | Measured refusal (pinned) |
| --- | --- | --- |
| `state.sexp` | 24-bit registers | `gen_state.py`: "masked fixed-width storage for nonstandard widths is generator work (docs/ARCHITECTURE.md §4)…" (rc 2) |
| `state-spaces.sexp` | a second address space | schema: **accepts** (`conforms to state.sexp`, rc 0) — the shape was declared `2026-10-01` (P3-BREADTH.5 slice 1, case dsp56300-lab-v0 / F3); the refusal moved one layer down: `gen_state.py`: "memory_spaces declared — … is generator work" (rc 2) |
| `packet.sexp` | an instruction packet | schema: `undeclared field "packet"` (rc 1) |
| `delayed.sem.sexp` | a delayed effect | schema: `undeclared operator "delay"` (rc 1) |
| `state-groups.sexp` | register grouping with fill semantics | schema: `undeclared field "register_groups"` (rc 1) |

Probe 5 was added by `P3-BREADTH.1` (`2026-10-01`): finding F2 (register grouping with
fill semantics, TI C64x §2.2) was the one finding in the `DSP-REVIEW.7` report classified
without an executable demonstration; the report named this probe as the honest way to get
one. The descriptor is the real scalar profile's state document plus exactly one synthetic
`register_groups` form — its only refusal is the grouping shape (measured `2026-10-01`,
rc 1, the pin above).

**Probe 2 re-pinned `2026-10-01` (P3-BREADTH.5 slice 1), and the suite did what it exists
to do: the pin went stale and the suite turned RED** when the schema learned
`memory_spaces` for the exercised dsp56300-lab-v0 profile (F3; the census record is
`docs/tasks/artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md`). The boundary moved
one layer down, not away: the descriptor now carries full `space` forms (word_bits,
authority, source), validates at the schema layer, and is refused **by name** at the
generator (`memory_spaces declared …`, rc 2 — emitting spaces is generator work). The same
slice pinned the sibling constructs the census measured — `register_family` with part
readouts (F1) and `hardware_stack` — with RED arms in `check_state_gen.sh`'s self-test.

**Green means the boundary is where the pins say.** The day the pipeline genuinely
supports one of these shapes, its pin goes stale and the suite turns RED — that is the
fixture's purpose: measuring the boundary moving. Every refusal was measured before the
pin was written (`target/dsp-review/probes/`, `2026-09-30`), and each probe descriptor was
reduced until its ONLY refusal is the shape under test.

## What it is not

Not evidence about any real DSP, not a claim that the shapes are unimplementable ("refused
by name" is a generator/schema boundary, not a theorem — each refusal message names the
work that would lift it), and not an endorsement of `synth24` as a design. The DSP review
never claims DSP compatibility (the tree's non-goals).
