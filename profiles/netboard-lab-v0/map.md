<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_board.py`; drift between this map and the canonical
     board definition is refused by the BOARD-GEN doctrine
     (`scripts/check_board_gen.sh`). -->
<!-- Canonical input: `profiles/netboard-lab-v0/board.sexp` (sha256 `93b087cb65842cd43ce63e24853f4a7c9778a9278d3a8d6458a606f1a6122333`)
     Generator: `scripts/gen_board.py` (sha256 `887649166b6c832f6d7d3a552fe6cba85f00dfad2a1acc1b140ccaabd58c671a`) -->

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
| `eth0` | `lan9118-lab-v0` | lan9118 | `eth0` | 16/32-bit | unconnected | recorded-trace-replay | recording-sink |

Serial console: `uart0`. Reset: cold only.

## Declared absences

| Element | Present | Satisfies |
| --- | --- | --- |
| timers | no — absent by contract | `OB-ENV-VIRTUAL-TIME` |
| interrupt controller | no — absent by contract | `OB-ENV-EVENT-DELIVERY` |
