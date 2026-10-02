# The evidence shape: expectations before a model

A device's evidence cannot be a per-step instruction trace — there are no instructions.
This unit's evidence shape is the one its `vehicle` block declares: `(comparison
register-expectations)`.

**What exists today** is the corpus under `profiles/lan9118-lab-v0/expectations/`: three
documents, each step carrying its derivation and its datasheet locator, recorded before
any implementation exists. The TX free-space document is the strongest of the three:
§3.12.5's usage rules are closed arithmetic, so the expected TDFREE values are
*computed* from the datasheet (4608 → 4540 → 4528 → 4416 across three queued packets,
back to 4608 after TXD_DUMP) with no wire and no implementation involved. The RX
document derives a declared 64-byte broadcast frame's status word (`0x00402000`) from
§3.13.3's field definitions, and pins the underrun → RXE → soft-reset discipline
(§3.13/§3.13.5) as the path's hardest rule. The reset document pins the stated resets
and — just as load-bearing — refuses to pin the strap-dependent bits, the blank PHY ID2
nibbles, and the EEPROM-less MAC address.

**What consumes them** comes later, with named owners: the device model is checked
against these expectations; the firmware probes (`P5-BOARD.5`, gated on the CPU's
acceptance trajectory) exercise the real accesses — and the recorded-trace replay
backend (`D-BOARD-NET-BACKEND`) makes the RX expectations reproducible in a fresh clone,
because the stimulus is a declared trace, never a live network.

**What this unit's evidence never is:** a live host link's behaviour, or another
emulator's register choices adopted as truth. The datasheet is the architecture
authority; the straps and the wire scene are the composition's declared choices; nothing
else is evidence.
