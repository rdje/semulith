# What the materials do not contain

A materials bill that lists only what things provide is how a project comes to believe
it has information it never acquired. This chapter is the bill's other half: the gaps,
each with its owner.

## The datasheet's own silences and deferrals

Six records carry what DS00002266B does not determine: reserved read values (§5.1's
"random value"), non-32/16-bit access effects, the strap-determined resets (D32/nD16,
SPEED_SEL — the board's composition choice, decided by the `.4` verdict:
`D-BOARD-NIC-STRAPS`), the blank PHY ID2
model/revision nibbles, the ADDRH/ADDRL defaults-versus-undefined tension, and §3.11's
reset completion times — mis-rendered in the PDF's own text layer (the µ→s mis-mapping,
hexdump-verified), internally contradicted by §5.3.13's clean "100us", so only the
cleanly stated figures pin. These are the dossier being honest about the source, not
bugs in it.

## The composition tensions, pre-wired to `.4`

The sharpest findings are not silences but conflicts the composition must verdict:

- **Guest-readable time sources.** FREE_RUN (a 25 MHz free-running counter that runs in
  every power state), GPT_CNT (a 100 µs timer readout) and IRQ_CFG's 10 µs deassertion
  interval are MMIO-readable — and the CPU contract excludes every guest-reachable time
  source (`OB-ENV-VIRTUAL-TIME`). `REQ-D-NIC-TIME-SOURCES` records the disposition
  direction: frozen or guest-deterministic, never wall-clock, never the harness's
  retired-instruction count.
- **The wire-domain link scene.** Note 3-11 makes the PHY's Link Status load-bearing
  (drivers wait for it after any PHY reset); on this board the wire is the
  recorded-trace replay backend, so the link scene is declared, never live
  (`REQ-D-NIC-PHY-LINK`). GPIO pin reads are the same class on a board that wires no
  pins (`REQ-D-NIC-GPIO-PINS`).

## The deferred and the absent, with their owners

- **The device model (Rust)** — absent, owned: the dossier is the contract the model
  route consumes.
- **Firmware probes** — absent, owned: `P5-BOARD.5`, gated on the CPU's acceptance
  trajectory.
- **An EEPROM** — absent *by board design* (board.sexp wires none): the auto-load's
  absent path (§3.9.1 — no `A5h` marker, initialization ends, the host programs
  ADDRL/ADDRH) is this board's defined path, not a gap.
- **A bus-master DMA contract** — not a gap but the device's nature: programmed I/O only
  (§1.10), which is exactly why every device effect reaches the guest through its own
  MMIO accesses.

## What the unit never owed

Instruction encodings, a guest corpus, an interaction matrix (derived not-applicable by
the `device-model` declaration until the probe corpus exists), and the Ethernet wire
itself — RX arrives from recorded-trace replay, TX leaves to a recording sink, and a
live host socket stays laboratory play at the `Environment` boundary
(`D-BOARD-NET-BACKEND`).
