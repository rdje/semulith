# `synth24` — the synthetic stress fixture (DSP-REVIEW.6, task card T010)

⛔ **SYNTHETIC.** The descriptors in this directory describe **no real processor**. They
exist to measure where Semulith's pipeline (the state generator, the schema layer) refuses
the shapes a real DSP would need: nonstandard widths, a second address space, packets, and
delayed effects. **Its passing evidence may never be cited for a real DSP claim** — that
is the leaf's acceptance rule, and it applies to every file here.

## What it is

Four descriptors, each carrying exactly one synthetic shape, and
`run_synth_probes.sh`, which pushes each through the real pipeline and pins the measured
refusal:

| Probe | Shape | Measured refusal (pinned) |
| --- | --- | --- |
| `state.sexp` | 24-bit registers | `gen_state.py`: "masked fixed-width storage for nonstandard widths is generator work (docs/ARCHITECTURE.md §4)…" (rc 2) |
| `state-spaces.sexp` | a second address space | schema: `undeclared field "memory_spaces"` (rc 1) |
| `packet.sexp` | an instruction packet | schema: `undeclared field "packet"` (rc 1) |
| `delayed.sem.sexp` | a delayed effect | schema: `undeclared operator "delay"` (rc 1) |

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
