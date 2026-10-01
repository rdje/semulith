# Introduction

`dsp56300-lab-v0` is the repository's **second modelled unit** and its first non-scalar-CPU
one: a bounded, EXPERIMENTAL subset of the Motorola/NXP DSP56300, a 24-bit digital signal
processor with 56-bit accumulators, three memory spaces (X, Y and P), a hardware loop stack,
and zero-overhead `do`/`rep` looping. It exists because `P3-BREADTH` demanded the public
abstraction be pushed on by something that breaks the scalar CPU's assumptions — and the
oracle census (`P3-BREADTH.3`) measured the DSP56300 the only DSP family with a complete,
license-clean evidence path.

> **Claim scope.** No DSP56300 compatibility is claimed. The claim is functional
> canonical-end-state agreement with the pinned reference on the declared synthetic guest
> corpus for the named subset — never a family compatibility claim, and nothing inherited
> from `rv64i-lab-v0`'s evidence.

## The subset (v0), in one paragraph

Non-parallel moves including the A2/B2 accumulator-extension readout; the
immediate/register data-ALU core (`add/sub/cmp/and/or/eor`, `asl/asr/lsr`); signed
`mpy`/`mac`; `nop/jmp/jsr/rts`; `do`/`enddo`/`rep`; linear addressing only. Every exclusion
— parallel moves (the dual-feed axis, the named first extension candidate), condition-code
branches, rounding/iterative multiplies, bit-field operations, modulo and reverse-carry
addressing, interrupts and traps, operating modes, stack extension, peripherals, and all
timing — is named with its reason in the selection record
(`docs/tasks/artifacts/p3-breadth/2026-10-01-subset-selection.md`).

## The vehicle

The model is the sibling crate `crates/semulith-dsp56300`: hand-written Rust whose every
decode mask and semantic rule is cited per form to the pinned family manual. This is a
declared vehicle (`profile.sexp`'s `vehicle` block), not an accident: the definition
pipeline refuses a second unit by name, building that generator work first would have been
the speculative generality `P3-BREADTH` exists to refuse, and the encoding/definition
generalization was later measured a lane, not an extension (`P3-BREADTH.5` slice 3), and
deferred with named reopening conditions.

## How to read this book

The arc is the same five-part one every unit's book follows: the **materials bill** (what
the unit is built from, and what each material does *not* supply), the **gaps** (what the
materials do not contain), the **method** (how documents became a model), the
**reference** (what agreement with it is worth), and the **evidence** (what was measured,
and the gates that keep it honest).
