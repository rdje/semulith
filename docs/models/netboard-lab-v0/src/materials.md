# The materials bill

Everything `netboard-lab-v0` is built from, in one place: the composed units' pins and
the board's own definition — each pinned by exact identity, each with what it supplies
**and what it does not**.

The two standing rules: **the tables are generated** (`scripts/gen_model_book.py` reads
the canonical definition and emits the identity tables; `MATERIALS-BILL` regenerates them
in memory on every commit and refuses drift), and **the prose is authored** — every
material below carries its negative statement.

## The composition pins

A board has no specification of its own — it composes pinned units, and the pins below
are the bill's specification surface.

{{#include materials/pinned-specifications.md}}

### `rv64i-lab-v0`

The processor: pinned by unit id + version `0` + the dossier content digest recorded in
its GATE-REPORT-gated `GC-REPORT.md`. Its CPU/environment contract (`rv64i-lab-env-v0`
v0) is the contract this board must satisfy — the eight environment assumptions the
composition verdict (`P5-BOARD.4`, **ACCEPTED**) matched against board and device
guarantees.

**Does not supply:** the devices, the map, or the board's absences — the processor's own
C19/C20/C21 categories are deferred to this board by its census; and the digest pins the
dossier's *content*, not its future: a processor re-release moves the pin deliberately.

### `SIFIVE-FU540-C000`

The SiFive FU540-C000 Manual v1p5 — the serial device *material*, pinned by revision +
sha256. Its §13 supplies the UART's whole register contract (dossiered in the
[`sifive-uart-lab-v0` book](../../sifive-uart-lab-v0/src/introduction.md)) and Table 58
supplies the board map's `0x1001_0000` instance address.

**Does not supply:** the 16550 contract — the label was measured false against this
artifact (zero occurrences; `D-BOARD-UART-KIND`) — nor anything beyond §13 that this
board relies on: the SoC's memory map, other peripherals and boot flow are not this
board's composition.

### `MICROCHIP-LAN9118`

The LAN9118 datasheet DS00002266B — the network device *material*, pinned by revision +
sha256. Chapter 5 supplies the NIC's register contract (dossiered in the
[`lan9118-lab-v0` book](../../lan9118-lab-v0/src/introduction.md)) and Table 5-1's
`00h`–`FCh` span supplies the board map's 256-byte `eth0` window.

**Does not supply:** the strap values (D32/nD16, SPEED_SEL — the composition's choice,
decided by the `.4` verdict: `D-BOARD-NIC-STRAPS`), a bus-master DMA contract (the
device is programmed-I/O only — which is why the CPU contract tolerates it), or the
wire: the recorded-trace backend is the board's declaration, not the datasheet's.

## The encoding and reference surfaces, honestly absent

{{#include materials/encoding-tables.md}}

{{#include materials/reference-models.md}}

## The internal contracts

{{#include materials/internal-contracts.md}}

### `board.sexp`

The canonical board definition: the composition pins, the memory map (2 GiB RAM at the
harness's existing base, the UART at its sourced instance address, the NIC in its
datasheet span), cold-only reset, the serial console, and the two declared absences —
timers and interrupt controllers, each carrying its reason and the obligation it
satisfies (`OB-ENV-VIRTUAL-TIME`, `OB-ENV-EVENT-DELIVERY`) — with `satisfies` fields
pre-wiring the composition verdict. Gated by `schema/board.sexp` via DOSSIER-SCHEMA.

**Does not supply:** the verdict itself — a definition declares; it does not discharge.
An unmatched CPU assumption in `.4` is a rejection, not a note, and this document's
declarations are what that verdict will test.

### `DOSSIER.md`

The board's narrative: what the definition means, what it does not claim, the measured
16550 correction, and the design's rationale in reviewable prose.

**Does not supply:** any fact not in `board.sexp` — the narrative narrates the data; the
data is the contract. Where the two could drift, DOSSIER-SCHEMA and the generated
fragments are the drifts' refusals.
