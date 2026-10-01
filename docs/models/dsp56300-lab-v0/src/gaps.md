# What the materials do not contain

The gaps chapter is where the unit says, ahead of any reviewer, what its materials will
**not** answer. Each gap is named with its consequence for the claim and the route that
would close it — a gap without an owner is how a limitation quietly becomes an
overclaim.

## The exclusions of subset v0

These are declared in the subset decision, each with its reason; the census
(`materials/category-needs.sexp`) carries their dispositions as data.

- **Parallel moves — the dual operand feed.** The DSP56300's signature form: two data
  moves issued with one ALU operation. Excluded as the **named first extension
  candidate**: it raises the old/new-operand visibility questions (category C09) that
  scalar issue never asks, and the subset exists to be *evidenced*, not broad. Its
  arrival reopens the C09 census row and the encoding lane's first reopening condition.
- **Condition-code branches.** Subset v0's flow is `jmp/jsr/rts` only; the `bcc` family
  and its CCR interactions are unclaimed.
- **Rounding and iterative multiplies; bit-field operations.** `mpy`/`mac` are signed,
  non-rounding forms only.
- **Modulo and reverse-carry addressing.** The seven linear `(Rn)` modes are covered;
  the AGU's circular and bit-reversed arithmetic is excluded (category C10, partial).
- **Interrupts and traps.** None are deliverable in subset v0 (category C14, missing —
  the FM carries the chapters; the reference's peripheral-interrupt shapes are
  *unverified against hardware*, which bounds what an interrupt-admitting revision
  could claim even with the material in hand).
- **Operating modes (SA/SC/DM).** The reference stores the mode bits but treats them as
  inert (its LIMITATIONS); the subset excludes them (category C15, missing).
- **Stack extension.** The hardware stack is modelled at its 16 on-chip levels,
  including the observable stale popped slots; the extension to memory is
  unimplemented upstream and excluded here.
- **Peripherals and devices.** The laboratory declares three memory spaces and no
  devices (categories C19–C21, deferred-to-board).
- **All timing.** `cyc` in the canonical dump is a base-table value (the reference's
  LIMITATIONS §4) and is **never compared** — the comparison contract says so, and the
  environment contract (OB-ENV-VIRTUAL-TIME) makes it an obligation.

## The evidence-shape gaps

- **No per-step comparison.** The reference's comparison surface is per-CASE canonical
  end state, so this unit has no per-instruction trace agreement (the scalar unit's
  shape). The F6 census's consequence — the dump IS the complete architectural state
  for subset v0 — is what makes the checkpoint surface sufficient rather than merely
  convenient; the argument and its surface-completeness legs are recorded in
  `docs/tasks/artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md`.
- **No independent second oracle.** The assembler and emulator share one lineage; the
  family's second implementation (gearmulator) is GPL-3.0 and unexamined. The
  independent confirmations that exist are upstream's proof artifacts (the asm56300
  roundtrip; the silicon-sealed difftest corpus), recorded as EVD-04 legs Semulith has
  not re-run.
- **No exact-toolchain-pinned reference build.** The upstream pins Rust 1.98.1; the
  demonstrated build ran under the host's 1.98.0 (the crate's floor) to keep the rustup
  store off the repository volume. Recorded as an `attempt` row in `references.sexp`;
  owned by this profile's model slice, to resolve before the reference becomes
  evidence-bearing beyond the demonstrated path.
- **No license terms recorded for the family manual.** The materials catalog's
  `licence-evidence` row says why; the artifact is READ, not redistributed — fetched
  into the untracked working area, never committed. `SRC-01` requires the actual terms
  before the artifact is relied on for anything shipped; that obligation stands.

## What no material can supply

No acquisition closes these, because they are properties of the method, not the
library: finite guest corpora are tested evidence, never universal proof (EVD-01); a
synthetic guest says nothing about any real DSP program; and agreement with one
silicon-validated reference is one oracle's word, however good its own validation
story. The claim is shaped to exactly what these bounds leave standing.
