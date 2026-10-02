# DOSSIER — `lan9118-lab-v0` (EXPERIMENTAL)

The second device unit: the **Microchip LAN9118** 10/100 Ethernet controller of datasheet
DS00002266B, modelled as the wired NIC `eth0` of
[`netboard-lab-v0`](../netboard-lab-v0/DOSSIER.md). Dossiered by `P5-BOARD.10` from the
design brief recorded `2026-10-02`
([`docs/tasks/P5-BOARD.md`](../docs/tasks/P5-BOARD.md), Decisions), inheriting the
device-dossier shape `P5-BOARD.2` hardened on the SiFive UART — no machinery edit was
needed; the by-declaration generalization
(`decision_device-applicability-by-declared-vehicle`) covers the NIC.

> **Claim scope.** The unit is EXPERIMENTAL: it inherits the board's and processor's status,
> and every claim reads as conditional on the CPU's acceptance trajectory. This dossier is
> the device's **contract** — no device model exists yet, and nothing here is a probe
> result. Expected results are datasheet-derived predictions, recorded before any
> implementation exists (EVD-05's shape at the device layer).

## The source

One source, one datasheet: [`sources.sexp`](sources.sexp) pins `MICROCHIP-LAN9118`
DS00002266B (sha256 `72fe68f2…91bf6ee`, re-verified from the materials cache
`2026-10-02`). Two extraction disciplines were measured and are recorded: the two
`pdftotext` modes **disagree on Table 5-1's Default column** (two-column page layout
scrambles row pairing), so every reset value here is taken from each register's own
§5.3.x/§5.4.x/§5.5.x section and cross-checked arithmetically where an independent
statement exists (TX_FIFO_INF.TDFREE = `1200h` = Table 5-3's 4608-byte row at the
TX_FIF_SZ = 5 default — two statements, one number); and §3.11's soft-reset/PHY-reset
completion times render as `2 s`/`100 s` in the PDF's **own text layer** (hexdump-verified —
a mis-mapped micro sign, not an extraction drop), contradicted by §5.3.13's clean "minimum
of 100us" and by §3.11.4's own 100 ms error bound, so the dossier pins the cleanly stated
figures only (`REQ-D-NIC-RESETS`).

## The register contract

The direct host-bus map spans `00h`–`FCh` — exactly the board's 256-byte `eth0` window
(`D-BOARD-MEMORY-MAP`): four FIFO port groups (RX data aliased `00h`–`1Ch`,
destructive-read; TX data aliased `20h`–`3Ch`, write-only; RX/TX status pops at `40h`/`48h`
with non-destructive PEEKs at `44h`/`4Ch`), 24 named CSRs at `50h`–`B4h`, and RESERVED
slots at `60h`, `94h`, `B8h`–`FCh`. Behind the map sit 12 MAC CSRs indexed through
`MAC_CSR_CMD`/`MAC_CSR_DATA` and 13 PHY registers indexed one level deeper through
`MII_ACC`/`MII_DATA` (PHY address `00001b`). The load-bearing semantics, each a mirrored
requirement/obligation pair in [`requirements.sexp`](requirements.sexp) and
[`contract-obligations.sexp`](contract-obligations.sexp) (contract `lan9118-v0` v0):

- **The FIFO ports move state.** Every RX data read pops a DWORD; every status port read
  pops a status word; the PEEKs read the top without popping (§5.2). The RX path's hardest
  discipline: the host must never read more than the FIFOs report — an underrun asserts
  RXE and **requires a soft reset to regain host synchronization** (§3.13, §3.13.5).
- **The synchronizers are protocols, not windows.** A MAC CSR access is write Busy + R/nW
  + index, poll Busy clear, then read data — the registers must not be modified while Busy
  holds (§5.3.20/§5.3.21); the MII access adds the pinned PHY address and the same busy
  discipline (§5.4.6/§5.4.7).
- **TX is command-driven.** Each buffer begins with command A + B (§3.12.2); command B is
  stored in the FIFO only on First Segment and must be identical per packet, and the
  cumulative byte count must match Packet Length — else TXE (§3.12.5, §3.12.7). The
  free-space arithmetic is exact enough to derive expectations from
  ([`expectations/tx-fifo-space.expected.sexp`](expectations/tx-fifo-space.expected.sexp)).
- **Interrupts exist as status, not signals, on this board.** The IRQ pin is unconnected
  and declared so (`D-BOARD-NO-TIMER-IRQ`); INT_STS bits set regardless of INT_EN masks
  (§5.3.4), which is exactly what a polled driver reads.
- **Stated resets are concrete** — ID_REV = `01180001h`, BYTE_TEST = `87654321h`,
  FIFO_INT = `48000000h`, HW_CFG = `0005_0000h` + strap, TX_FIFO_INF = `00001200h`,
  GPT_CFG/GPT_CNT = `0000FFFFh`, MAC_CR = `00040000h` (PRMS set out of reset) — and two
  post-reset transients are recorded: EPC Busy reads 1 until the EEPROM auto-load attempt
  completes (§5.3.23 note), and the device **must be read at least once after power-up,
  reset, or return from a power-saving state or write operations will not function**
  (Note 3-4, stated three times in the datasheet — `REQ-D-NIC-FIRST-READ`).

## What the datasheet does NOT say

The measured silences and deferrals, recorded as requirements of non-commitment rather
than papered over:

| Silence / deferral | Locator | Disposition |
| --- | --- | --- |
| Reserved bit read values "not supported"; RESERVED locations return "a random value", must not be written | §5.1 | `REQ-D-NIC-RESERVED` — a model never pins a reserved read value |
| Access widths other than 32/16-bit have no stated effect | §1.10, §3.6 | `REQ-D-NIC-WIDTH` — the board makes them a board-reported contract violation (`D-BOARD-ACCESS-POLICY`) |
| Strap-determined resets: HW_CFG bit 2 (D32/nD16), PHY 0.13/0.12, PHY 4.8/7/6/5, PHY 31.4:2 | Notes 5-1/5-3/5-4, Table 2-2 | `REQ-D-NIC-STRAP-RESETS` — the strap values are the board's composition choice; **answered** by `D-BOARD-NIC-STRAPS` (the `.4` verdict): D32 tied high, SPEED_SEL at its internal pull-up |
| PHY ID2 model/revision nibbles | §5.5.4 (blank default column) | `REQ-D-NIC-PHY-ID` — only bits [15:10] = `C0D1h` pin |
| ADDRH/ADDRL "undefined until loaded from the EEPROM" vs Table 5-6's listed defaults | §5.4.2/§5.4.3, Table 5-6 | `REQ-D-NIC-MAC-ADDR` — both statements recorded, nothing pinned at reset; no EEPROM on this board, the host programs the address |
| §3.11's SRST/PHY-reset completion times ("2 s"/"100 s" in the PDF's own text layer) | §3.11.4/§3.11.5.1 vs §5.3.13 | `REQ-D-NIC-RESETS` — the cleanly stated 22 ms POR and 100 µs PHY-hold pin; the SRST completion time does not |

## The measured composition tensions (answered by the `.4` verdict)

Two findings the dossier records so the composition verdict cannot overlook them — and
the verdict's answers, landed `2026-10-02` (`P5-BOARD.4`,
[`../netboard-lab-v0/COMPOSITION-VERDICT.md`](../netboard-lab-v0/COMPOSITION-VERDICT.md)):

- **The NIC carries guest-readable time sources** — `FREE_RUN` (a 25 MHz free-running
  counter, running in every power state, §5.3.18), `GPT_CNT` (a 100 µs timer readout,
  §5.3.16) and the 10 µs-granularity INT_DEAS interval (§5.3.2) — and `OB-ENV-VIRTUAL-TIME`
  excludes every guest-reachable time source. A faithful wall-clock wiring would falsify the
  composition from *inside* a device, exactly as a CLINT would from beside one.
  `REQ-D-NIC-TIME-SOURCES` records the disposition direction: frozen or
  guest-deterministic, never wall-clock, never the harness's retired-instruction count.
  **The verdict:** frozen — `D-BOARD-NIC-TIME-FROZEN` (FREE_RUN reads its reset value
  forever; GPT_CNT never advances; INT_DEAS never runs).
- **The PHY's link state is wire-domain, and the wire is a recording.** Note 3-11 makes
  Link Status load-bearing (drivers wait for it after any PHY reset); on this board the
  replay backend declares the link scene — never a live host link (`REQ-D-NIC-PHY-LINK`).
  GPIO pin reads are the same class on a board that wires no pins (`REQ-D-NIC-GPIO-PINS`).
  **The verdict:** the scene is static and complete — 100BASE-TX full-duplex,
  auto-negotiation complete, from before the guest's first access
  (`D-BOARD-NIC-LINK-SCENE`); the pin reads are tied off at 0 (`D-BOARD-NIC-PIN-TIEOFFS`).

## The state inventory, and why the census matters here

[`state.sexp`](state.sexp) carries the 24 direct CSRs, the 12 MAC CSRs, the 13 PHY
registers and the four FIFOs, and its hidden-state census asks SEM-08's question of this
device. The measured answer: **the registers, the four FIFOs with occupancies, and the TX
command-parser state (the TXE length check and the §3.12.5 accounting observes it) — and
nothing else.** The MIL FIFOs are "not visible to the host processor" by the datasheet's
own words; the wire-domain machines (link training, auto-negotiation) surface only as PHY
register bits whose scene the replay backend declares; the WUFF load pointer is write-only
with no MMIO-readable effect. The 16-bit-mode pairing latch was censused **absent** at the
`.4` verdict: the board straps D32 (32-bit native mode, `D-BOARD-NIC-STRAPS`), §3.6's
pairing is 16-bit-mode operation, and a 16-bit access never reaches the device — so no
pending half is observable. Unlike the UART, FIFO occupancy at reset **is** pinned here —
empty, by the INF registers' stated resets (`REQ-D-NIC-FIFO-INF`, the measured contrast).

## Scope

The dossier models **one instance** — the board's `eth0` at `0x1002_0000`, a 256-byte
window spanning exactly the direct register map. The Ethernet wire itself is environment:
RX arrives from recorded-trace replay, TX leaves to a recording sink, and a live host
socket stays laboratory play at the `Environment` boundary (`D-BOARD-NET-BACKEND`). No
EEPROM is wired — the auto-load's absent path (§3.9.1) is this board's defined path.

## Dossier status

| Document | Status |
| --- | --- |
| `sources.sexp` | **present** — the DS00002266B pin, schema-validated |
| `requirements.sexp` | **present** — 52 records: 46 defined + 1 reserved + 1 unspecified + 4 implementation-defined (the strap and composition deferrals) |
| `contract-obligations.sexp` | **present** — 52 obligations, contract `lan9118-v0` v0, `device-guarantee` direction |
| `state.sexp` | **present** — 49 registers + 4 FIFO families + the earned census |
| `profile.sexp` | **present** — 52 decision mirrors; scope = the 28-member direct host-bus surface |
| expected results (register-read expectations) | **present** — 3 documents: cold-reset reads, TX free-space accounting, the RX replay path — all datasheet-derived, pre-implementation |
| unit registration (`materials/units.sexp`), the per-unit book | **deferred, owned** — registration day is `P5-BOARD.11` (all three units together) |
| device model (Rust), firmware probes | **absent, owned** — the model route follows the dossier; probes are `P5-BOARD.5`, gated on the CPU's acceptance trajectory |
