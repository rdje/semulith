# DOSSIER — `sifive-uart-lab-v0` (EXPERIMENTAL)

The first device unit: the **SiFive UART** of FU540-C000 v1p5 §13, modelled as the serial
console `uart0` of [`netboard-lab-v0`](../netboard-lab-v0/DOSSIER.md). Dossiered by
`P5-BOARD.2` from the design brief recorded `2026-10-02`
([`docs/tasks/P5-BOARD.md`](../docs/tasks/P5-BOARD.md), Decisions) — the first device to
reuse the CPU's dossier machinery, and deliberately the simplest contract on the board, so
the machinery is exercised before the LAN9118 inherits it.

> **Claim scope.** The unit is EXPERIMENTAL: it inherits the board's and processor's status,
> and every claim reads as conditional on the CPU's acceptance trajectory. This dossier is
> the device's **contract** — no device model exists yet, and nothing here is a probe
> result. Expected results are datasheet-derived predictions, recorded before any
> implementation exists (EVD-05's shape at the device layer).

## The source

One source, one chapter: [`sources.sexp`](sources.sexp) pins `SIFIVE-FU540-C000` v1p5
(sha256 `5fa68a67…cab79c`, re-verified from the materials cache `2026-10-02`) and cites
**§13 only** — the SoC's memory map, other peripherals and boot flow are the board's and
other devices' business. ⚠️ The UART is **not** a 16550: that label was measured false
against this artifact (zero occurrences; `D-BOARD-UART-KIND`) and is corrected wherever it
was recorded.

## The register contract

Seven 32-bit registers — `txdata 0x00`, `rxdata 0x04`, `txctrl 0x08`, `rxctrl 0x0C`,
`ie 0x10`, `ip 0x14`, `div 0x18` — a map "designed to require only naturally aligned
32-bit memory accesses" (§13.3, Table 59). The load-bearing semantics, each a mirrored
requirement/obligation pair in [`requirements.sexp`](requirements.sexp) and
[`contract-obligations.sexp`](contract-obligations.sexp) (contract `sifive-uart-v0` v0):

- **`rxdata` reads pop.** A read dequeues the head character and reports `empty` (bit 31);
  when `empty` is set the data field is not a valid character (§13.5). This is the map's
  sharpest side effect: the board's polled RX path depends on exactly one dequeue per read.
- **`txdata` writes conditionally enqueue.** A write enqueues only while the FIFO can
  accept; when `full` (bit 31 of a read) is set, writes are ignored (§13.4).
- **Watermarks are strict-inequality raise/clear conditions — with a measured gap.**
  `ip.txwm` becomes raised while the Tx FIFO's occupancy is strictly less than `txcnt` and
  is cleared when enough entries have been enqueued to *exceed* the watermark; `ip.rxwm`
  mirrors it on the Rx side (§13.8). ⚠️ The two strict sentences leave the `==` boundary
  and any pre-first-condition value undetermined — the manual never says whether the bit
  is a pure level of occupancy or holds between the conditions (`REQ-D-UART-WM-MODE`,
  measured in execution). A polled driver may drain `rxdata` to `empty` and fill `txdata`
  to `full` instead of trusting the bit at the boundary — which is how this board's
  drivers work (the interrupt line is unconnected and declared so, `D-BOARD-NO-TIMER-IRQ`).
- **Stated resets:** `txctrl = 0`, `rxctrl = 0`, `ie = 0`, `div = 289` (`div_init`, tuned
  for 115200 baud at the expected `tlclk`; divide ratio = `div` + 1, Table 66's own note).

## What the datasheet does NOT say

Five measured silences, recorded as requirements of non-commitment (the records whose
`source_semantics` category is `unspecified`)
rather than papered over — a dossier that invents behaviour here is describing a device
the source does not define:

| Silence | Locator | Disposition |
| --- | --- | --- |
| Reserved bit fields have no stated read/write semantics | Tables 60–65 | `REQ-D-UART-RESERVED` — an implementation's choice is laboratory, never architecture |
| `txdata.full`, `rxdata.*`, `ip.*` reset values are X | Tables 60, 61, 65 | `REQ-D-UART-RESET-X` — no expected result may pin an X-marked value |
| FIFO contents and occupancy at reset are never stated | §13 (whole chapter) | `REQ-D-UART-FIFO-RESET` — consistent with the X flags, not proof of them |
| Off-map and non-aligned-32-bit access effects are undefined | §13.3 | `REQ-D-UART-OFFMAP` / `REQ-D-UART-WIDTH` — the board dispositions: a board-reported contract violation, never silently serviced (`D-BOARD-ACCESS-POLICY`) |
| Watermark bit mode (pure level vs hold-between-conditions); the `==` boundary | §13.8 | `REQ-D-UART-WM-MODE` — a polled driver drains to `empty` / fills to `full` instead of trusting the bit at the boundary |

## The state inventory, and why the census matters here

[`state.sexp`](state.sexp) carries the seven registers and the two 8-entry FIFOs, and its
hidden-state census asks SEM-08's question of a device: what state beyond the registers
must a model carry to reproduce every MMIO-visible behaviour? The measured answer: **the
FIFO contents and occupancies, and nothing else.** The baud counter phase, the shift
registers, the 16× oversampling sampler and the txd latch are all unreachable from MMIO —
and with the board's byte-granularity backends (recorded input on RX, host console on TX)
wire timing can never become an MMIO observation. The map carries **no** error-status
register (no framing error, overrun or break bits exist in Table 59); that absence is the
datasheet's, not an oversight.

## Scope

The dossier models **one instance** — the board's `uart0` at `0x1001_0000` (the
instance-0 row of Table 58; the manual documents two instances with identical parameters).
The serial wire itself is environment: RX arrives from recorded input, TX leaves to the
host console, and a live host socket stays laboratory play at the `Environment` boundary
(`D-BOARD-NET-BACKEND`'s UART twin).

## Dossier status

| Document | Status |
| --- | --- |
| `sources.sexp` | **present** — the §13 pin, schema-validated |
| `requirements.sexp` | **present** — 13 defined + 6 unspecified records |
| `contract-obligations.sexp` | **present** — contract `sifive-uart-v0` v0; the schema's third `direction` value (`device-guarantee`) lands with this dossier |
| `state.sexp` | **present** — registers, FIFOs, the earned census |
| `profile.sexp` | **present** — the decision dossier; the schema's device-shaped generalization lands with this dossier |
| expected results (register-read expectations) | **present** — datasheet-derived, pre-implementation |
| unit registration (`materials/units.sexp`), the per-unit book | **deferred, owned** — registration day is `P5-BOARD.11` (all three units together) |
| device model (Rust), firmware probes | **absent, owned** — the model route follows the dossier; probes are `P5-BOARD.5`, gated on the CPU's acceptance trajectory |
