# DOSSIER — `netboard-lab-v0` (EXPERIMENTAL)

The first board: a minimal virtual platform composing **`rv64i-lab-v0` v0** — the
EXPERIMENTAL CPU release — with exactly two devices, both digest-pinned in
[`materials/catalog.sexp`](../materials/catalog.sexp): the **SiFive UART** (serial console)
and the **LAN9118 wired NIC**. Specified by `P5-BOARD.1` from the design brief recorded
`2026-10-02` ([`docs/tasks/P5-BOARD.md`](../docs/tasks/P5-BOARD.md), Decisions).

> **Claim scope.** The board inherits the processor's EXPERIMENTAL status: every board claim
> reads as conditional on the CPU's own acceptance trajectory, and the composition can never
> outrank its processor. The composition verdict has run — **ACCEPTED**, re-decided on every
> commit by the BOARD-VERDICT doctrine ([`COMPOSITION-VERDICT.md`](COMPOSITION-VERDICT.md))
> — but no device is modelled yet, and nothing here is a firmware-probe result.

## The canonical definition

[`board.sexp`](board.sexp) is the source of truth, schema-gated by
[`schema/board.sexp`](../schema/board.sexp) (DOSSIER-SCHEMA pairs them by basename). It
pins **versions, not names** (OWN-05):

| Part | Pin |
| --- | --- |
| Processor | unit `rv64i-lab-v0`, version `0`, dossier content digest `95ebca2f…cf8001` (recorded in [`profiles/rv64i-lab-v0/GC-REPORT.md`](../profiles/rv64i-lab-v0/GC-REPORT.md), GATE-REPORT-gated; verified against the live dossier at export derivation by PLATFORM-GEN, `P5-BOARD.6`), contract `rv64i-lab-env-v0` v0 |
| `uart0` | material `SIFIVE-FU540-C000`, revision `v1p5`, sha256 `5fa68a67…cab79c` |
| `eth0` | material `MICROCHIP-LAN9118`, revision `DS00002266B 2018-11-30`, sha256 `72fe68f2…1bf6ee` |

A digest match against a *newer* processor dossier is a finding, not a silent upgrade —
and since `P5-BOARD.6` the pin is **load-bearing**: the manifest generator re-derives the
digest from the live dossier (`gate_report.dossier_digest`, the one computation) and
refuses a stale pin by name.

The definition also carries the **boot contract** and the **test-control surface** as
data (`boot` / `test-control` blocks, `P5-BOARD.6`) — the platform package owns its boot
contract (`docs/ARCHOGEN_INTEGRATION.md` §2), and the export below derives from them.

## Memory map

The map is **generated, never handwritten**: [`map.md`](map.md) is derived from
`board.sexp` by `scripts/gen_board.py` and drift-gated by the BOARD-GEN doctrine
(`scripts/check_board_gen.sh`) — the address map, the wiring, and the declared absences,
with region ends computed. The machine-readable half is [`hardware.sexp`](hardware.sexp)
(schema [`schema/hardware.sexp`](../schema/hardware.sexp)). This dossier narrates the
choices; it does not restate the table.

RAM is the laboratory harness's existing load base and size, so a guest built for the
laboratory runs unchanged on the board. `uart0`'s base is the FU540-C000 UART0 instance
address (v1p5 Table 58); `eth0`'s 256-byte window is the LAN9118 direct register map span
(DS00002266B Table 5-1, offsets `0x00`–`0xFC`). Instruction fetch is served from RAM only —
every MMIO region is declared non-executable, so no fetch can reach a device and no fetch
has a side effect (`OB-ENV-FETCH-SUPPLY`).

## Reset

Cold reset only. The entry state is the CPU contract's, cited rather than restated:
`pc` at the loaded image's entry address, `x1..x31` zeroed, memory outside the loaded
image unwritten (`rv64i-lab-env-v0` v0, `OB-ENV-RESET`). There is no warm reset and no
retained state to order.

## Serial console

`uart0` is the **SiFive UART** of FU540-C000 v1p5 §13 — `txdata`/`rxdata`/`txctrl`/`rxctrl`/
`ie`/`ip`/`div`, 8-entry transmit and receive FIFOs, a register map designed for naturally
aligned 32-bit accesses. ⚠️ It is **not** a 16550: the design brief's "16550-compatible"
label was measured false against the pinned source (zero occurrences of "16550" in the
document) and is corrected wherever it was recorded — the source pin, not the label, was
the intent (`D-BOARD-UART-KIND`). Backend: transmit to the host console, receive from
recorded input; a live host socket is laboratory play at the `Environment` boundary.

## The network device, and why it shapes the platform

`eth0` is the LAN9118 10/100 MAC+PHY (DS00002266B). Its host bus is **programmed I/O —
no bus-master DMA** — so every device effect reaches the guest through the guest's own MMIO
accesses, exactly the shape the CPU contract's eight environment assumptions tolerate. The
director's `2026-10-01` brief — every board touches the world — is satisfied from board v0.
Backend: **recorded-trace replay on receive** (deterministic, evidence-grade) and a
**recording sink on transmit**; a live host-socket backend stays laboratory play and may
never enter an evidence claim (`D-BOARD-NET-BACKEND`).

## Timers and interrupt controllers: absent by contract

This is the design's sharpest edge, and it is declared as data in `board.sexp`, not prose
only. `OB-ENV-VIRTUAL-TIME` and `OB-ENV-EVENT-DELIVERY` are *environment assumptions* the
board must satisfy (`docs/CPU_ENVIRONMENT.md` §5, ENV-02): a CLINT or PLIC would not be a
feature but a **composition rejection** at `P5-BOARD.4`. Both devices' interrupt lines are
**unconnected and declared so**; drivers poll. Without a time source, NIC receive delivery
is pinned to the guest's own polling — the device holds the next recorded packet and offers
it when polled, so the harness's retired-instruction count never becomes target-visible.
Timers and interrupt delivery are deferred to the P4-profile board branch, where the CPU
contract has counter/interrupt assumptions to satisfy instead.

## Access policy

An MMIO access honours exactly the widths the device's datasheet defines — 32-bit for
`uart0` (§13.3), 32-bit for `eth0` (D32 strapped; §3.6 makes the bus widths
mode-exclusive, so `.1`'s 16/32 declaration narrowed to 32 at the `.4` verdict —
`D-BOARD-NIC-STRAPS`); any other width is a board-reported **contract violation**, never
silently serviced. A misaligned MMIO access never reaches a device: the CPU raises
`AlignmentException` first (`OB-MISALIGN-DATA`).

## The platform capability manifest

[`platform.sexp`](platform.sexp) is the board's **read-only derived export** for a
compatibility checker (`docs/ARCHOGEN_INTEGRATION.md` §3; OWN-06): the processor
identity and ISA facts, the resolved memory map, the device pins, the declared absences,
the composition dispositions, the boot contract, the time/event/ordering facts, and the
test-control surface — every facility with an explicit `presence` marker, plus the
limitations and the non-claims as data. Generated by `scripts/gen_platform.py` from the
canonical inputs (the board definition, the pinned processor's profile, the composed
obligations — all fingerprinted in the header), schema-gated by
[`schema/platform.sexp`](../schema/platform.sexp), drift-gated by the PLATFORM-GEN
doctrine (`P5-BOARD.6`). It is never handwritten, so a consumer imports facts rather
than becoming a second hardware implementation. The consumer-absence boundary is stated
in the document itself: archogen is actively developed and has no functional eADL
interface today, so the export's correctness legs are derivation freshness, schema
conformance and §3 coverage — never archogen acceptance.

## Dossier status

| Document | Status |
| --- | --- |
| `board.sexp` | **present** — the canonical definition, schema-validated (`P5-BOARD.1`); boot contract and test-control surface added as data (`P5-BOARD.6`) |
| device unit dossiers (`sifive-uart-lab-v0`, `lan9118-lab-v0`) | **present** — both landed fully gated (`P5-BOARD.2`, `P5-BOARD.10`) |
| unit registration (`materials/units.sexp`), the `kind` edit, the per-unit book | **present** — registration day landed all three units together (`P5-BOARD.11`) |
| composition manifest, generated maps | **present** — `composition.sexp`, the composed catalogues, `hardware.sexp` and `map.md`, all generated from `board.sexp` and drift-gated by BOARD-GEN (`P5-BOARD.3`) |
| composition verdict against the CPU contract | **present** — [`COMPOSITION-VERDICT.md`](COMPOSITION-VERDICT.md): ACCEPTED, every assumption matched to a named board/device guarantee; re-decided on every commit by the BOARD-VERDICT doctrine (`P5-BOARD.4`) |
| platform capability manifest | **present** — [`platform.sexp`](platform.sexp), generated from the canonical inputs and drift-gated by PLATFORM-GEN; the dossier pin verified live at derivation (`P5-BOARD.6`) |
