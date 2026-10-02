<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_board.py`; drift between this map and the canonical
     board definition is refused by the BOARD-GEN doctrine
     (`scripts/check_board_gen.sh`). -->
<!-- Canonical input: `profiles/netboard-lab-v0/board.sexp` (sha256 `ab64ccfb004e074d3c4939e6490c10357b8f1998f73a322347fd5db47c875e4e`)
     Generator: `scripts/gen_board.py` (sha256 `ba8cfca987b85442074ea1db9d46e19f9c93d99aa6fa48edc77963df80098dc9`) -->

# The generated map — `netboard-lab-v0` v0

Derived from the canonical board definition; the DOSSIER narrates it. Region ends are exclusive (base + size).

## Address map

| Region | Base | End | Size | Kind | Executable | Device |
| --- | --- | --- | --- | --- | --- | --- |
| `ram0` | `0x8000_0000` | `0x1_0000_0000` | 2 GiB (`0x8000_0000`) | RAM | yes | — |
| `uart0` | `0x1001_0000` | `0x1001_1000` | 4 KiB (`0x1000`) | MMIO | no | `uart0` |
| `eth0` | `0x1002_0000` | `0x1002_0100` | 256 B (`0x100`) | MMIO | no | `eth0` |

## Wiring

| Device | Unit | Kind | Region | Access widths | Interrupt | RX backend | TX backend |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `uart0` | `sifive-uart-lab-v0` | sifive-uart | `uart0` | 32-bit | unconnected | recorded-input | host-console |
| `eth0` | `lan9118-lab-v0` | lan9118 | `eth0` | 32-bit | unconnected | recorded-trace-replay | recording-sink |

Serial console: `uart0`. Reset: cold only.

## Declared absences

| Element | Present | Satisfies |
| --- | --- | --- |
| timers | no — absent by contract | `OB-ENV-VIRTUAL-TIME` |
| interrupt controller | no — absent by contract | `OB-ENV-EVENT-DELIVERY` |
