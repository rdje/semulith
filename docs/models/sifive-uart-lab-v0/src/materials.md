# The materials bill

Everything `sifive-uart-lab-v0` is built from, in one place: the one pinned
specification, and the internal contracts the dossier itself carries — each pinned by
exact identity, each with what it supplies **and what it does not**.

Two rules govern this chapter, and they are why it can be trusted:

- **The tables are generated.** `scripts/gen_model_book.py` reads the pinned dossier and
  emits the identity tables below — digests, byte counts, record counts. Nothing in a
  table is retyped, so a digest cannot rot: the `MATERIALS-BILL` doctrine regenerates the
  tables in memory on every commit and fails if they differ from what is committed.
- **The prose is authored, and it is where the judgement lives.** Every material below
  carries its negative statement, because a bill that lists only what things provide is
  how a project comes to believe it has information it never acquired.

## The pinned specification artifact

One document carries the whole device contract — the UART is §13 of the SoC manual and
nothing else, and the pin names the issue (v1p5), not just the part, because the same
manual circulates as v1p0/v1p3/v1p4 with real differences.

{{#include materials/pinned-specifications.md}}

### `SIFIVE-FU540-C000`

The SiFive FU540-C000 Manual v1p5: §13's instance parameters (Table 58), the register map
and its aligned-32-bit access rule (§13.3, Table 59), the per-register semantics of
txdata/rxdata/txctrl/rxctrl/ie/ip/div (§13.4–§13.9), the FIFO depths and the watermark
conditions. Acquired through the chipdoc channel and re-verified from the materials
cache; the artifact is read, not redistributed.

**Does not supply:** the 16550 contract — the label was measured false against this
artifact (zero occurrences of "16550"; `D-BOARD-UART-KIND`), so nothing 16550-shaped may
be sourced here. It also does not supply Reserved-bit behaviour, off-map or
non-32-bit access effects, the X-marked reset values, or the FIFOs' reset state —
each silence is a dossier record (`REQ-D-UART-RESERVED`, `REQ-D-UART-RESET-X`,
`REQ-D-UART-FIFO-RESET`, `REQ-D-UART-OFFMAP`, `REQ-D-UART-WIDTH`), and §13.8's
watermark mode gap is `REQ-D-UART-WM-MODE`.

## The encoding and reference surfaces, honestly absent

A device has no instruction encodings and pins no reference models — the two fragments
below say so by declaration, because an honest absence in the bill is what keeps the
device dossier from quietly masquerading as a processor-shaped one.

{{#include materials/encoding-tables.md}}

{{#include materials/reference-models.md}}

## The internal contracts

The dossier's own documents, with their record counts derived from the tracked files.

{{#include materials/internal-contracts.md}}

### `profile.sexp`

The unit's declaration: the 7-register scope census (`count_base = count_total = 7`,
the whole §13 map, nothing excluded), the 19 decision mirrors, the `device-model`
vehicle declaration every instruction-shaped gate derives its applicability from.

**Does not supply:** any instruction pipeline — no encoding, no semantics, no guest
corpus; the scope counts MMIO registers, and a reader looking for instruction forms here
is reading the wrong dossier shape.

### `state.sexp`

The device-state document: the seven registers and the two FIFOs, with the hidden-state
census that earns the "and nothing else MMIO can reach" claim — the baud counter phase,
shift registers, sampler and pin latch are enumerated and shown unreachable.

**Does not supply:** the FIFOs' reset state — never stated by the datasheet and recorded
as unspecified, not guessed; and no register the datasheet does not define.

### `requirements.sexp`

The 19 predeclared requirement records: 13 datasheet-defined statements and 6 measured
silences recorded as requirements of non-commitment, each with its §13 locator.

**Does not supply:** latitude — a requirement with `source_semantics` category
`unspecified` is a promise about what the model must NOT invent, not a hole to fill.

### `contract-obligations.sexp`

The device contract `sifive-uart-v0` v0: 19 obligations in the `device-guarantee`
direction — what a composing board may rely on, and (for the silences) what it may not.
Each mirrors its requirement verbatim; RECORD-SCHEMA refuses drift.

**Does not supply:** a discharge by itself — the board definition's `satisfies` fields
and P5-BOARD.4's composition verdict consume these ids; an obligation unread by the
composition is a guarantee nobody cashed.

### `expectations/`

The EVD-05 register-read corpus: three documents (cold reset, TX FIFO enqueue/full, RX
watermark levels) derived from the datasheet **before any model exists** — including the
values deliberately left unpinned (the X-marked resets, the watermark boundary).

**Does not supply:** probe results — nothing here ran against an implementation; and at
the `==` watermark boundary it deliberately supplies nothing, because the datasheet does
not determine the bit there (`REQ-D-UART-WM-MODE`).
