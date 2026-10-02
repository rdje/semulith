# What the materials do not contain

A materials bill that lists only what things provide is how a project comes to believe
it has information it never acquired. This chapter is the bill's other half: the gaps,
each with its owner.

## The datasheet's own silences

Six requirements record what FU540-C000 v1p5 §13 does **not** say — Reserved-bit
behaviour, the X-marked reset values, the FIFOs' reset state, off-map and non-32-bit
access effects, and the watermark mode (`REQ-D-UART-WM-MODE`: §13.8 gives each watermark
bit a strict-inequality *raised* condition and a strict-inequality *cleared* condition,
and never says whether the bit is a pure level of occupancy or holds between them — the
`==` boundary and any pre-first-condition value are undetermined). These are not bugs in
the dossier; they are the dossier being honest about the source. A model that invents
behaviour here is describing a device the source does not define.

## The deferred and the absent, with their owners

- **The device model (Rust)** — absent, owned: the dossier is the contract the model
  route consumes; implementation follows it, gated by EXTRACTION's device leg.
- **Firmware probes** — absent, owned: `P5-BOARD.5`, gated on the CPU's acceptance
  trajectory. The expectations corpus is recorded *before* any model exists precisely so
  the probes have something independent to be measured against.
- **A second, independent source for the watermark mode** — absent: QEMU's sifive_uart
  computes the bits combinationally, an independent reading but not a *source*; the
  dossier records the gap rather than adopting the reading.
- **The 16550 register contract** — not a gap but a measured negative: the label was
  false against the pinned artifact (`D-BOARD-UART-KIND`), corrected wherever recorded.

## What the unit never owed

Instruction encodings, a guest corpus, an interaction matrix (the `device-model`
declaration derives those gates' applicability — the matrix attaches with the probe
corpus, `P5-BOARD.5`), and the serial wire itself: RX arrives from the board's recorded
input, TX leaves to the host console, and a live socket stays laboratory play at the
`Environment` boundary.
