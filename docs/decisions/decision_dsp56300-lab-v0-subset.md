# The dsp56300-lab-v0 subset and vehicle decision: a bounded experimental subset in a sibling crate, differentially evidenced

- **Type:** `decision`
- **Date:** `2026-10-01`
- **Status:** `active`
- **Owner / source:** `P3-BREADTH.4` slice 1, applying the leaf acceptance (the claim names
  the exact subset; no inherited differential claim — `docs/EVIDENCE_AND_GATES.md` §1) to
  the measured reference coverage and gaps
  (`docs/tasks/artifacts/p3-breadth/2026-10-01-subset-selection.md`).

## The decision

The bounded real subset is unit **`dsp56300-lab-v0`, subset v0**: non-parallel moves
(including the A2/B2 extension readout), the immediate/register data-ALU core, signed
`mpy`/`mac`, `nop/jmp/jsr/rts`, and `do`/`enddo`/`rep`, over linear addressing only —
evidenced as checkpoint-level canonical end-state equality (registers, bounded X/Y memory
windows, hardware stack slots; `steps` compared, `cyc` never) against
`mborgerson/dsp56300@c60aeedb`'s difftest. Parallel moves, the condition-code family,
rounding multiplies, bit-field ops, modulo/reverse-carry addressing, interrupts, operating
modes, stack extension, and all timing are **excluded by name**, each with its reason in the
selection record.

The implementation vehicle is a new sibling crate, `crates/semulith-dsp56300`, decode and
semantics derived from the pinned family manual (`NXP-DSP56300-FAMILY-MANUAL`) with
per-form citations, labelled EXPERIMENTAL. The generator/schema generalization (F1 masked
widths, F3 memory spaces, the special-register census, the scope taxonomy) stays `.5`'s
work, justified then by this exercised target — the pipeline is not extended ahead of its
exercising case.

## Why

- The reference's instruction coverage is complete (measured on the pinned source), so the
  bound comes from honest implementability and the reference's documented gaps
  (LIMITATIONS: modes inert, stack extension absent, interrupts partially unverified, cycle
  counts base-table only) — the exclusions map one-to-one onto those gaps or onto bounded
  scope.
- Extending the generator first would build abstraction ahead of its exercising target —
  the speculative generality P3 exists to refuse — and would touch the gated scalar model's
  regression surface. A sibling crate leaves `rv64i-lab-v0` byte-untouched.
- The comparison surface is per-case end-state, not the RISC-V per-instruction commit walk;
  the comparator is a new, simpler shape owned by `.4`.

## Consequences

- The claim, when `.4` completes, is functional agreement on the declared guest corpus for
  the named subset — never a DSP56300 family compatibility claim.
- The parallel-move (dual-operand-feed) axis stays unexercised in v0 and is the first named
  extension candidate; a future subset reopens this record rather than quietly growing.
- `.5` inherits the measured extension list: masked fixed-width storage, memory spaces with
  per-space units, special registers beyond `pc`, the profile scope taxonomy — each now has
  its exercising target and case.
