# The composition verdict — `netboard-lab-v0` v0 against `rv64i-lab-env-v0` v0

**Verdict: ACCEPTED** (`P5-BOARD.4`, `2026-10-02`). Every environment assumption in the
accepted CPU contract is satisfied by a named board or device guarantee — decided
mechanically by the **BOARD-VERDICT** doctrine (`scripts/board_verdict.py`, re-run on
every commit by `scripts/check_board_verdict.sh`), which rejects the composition by name
the day an assumption goes unmatched or an edge dangles. An unmatched assumption is a
rejection, never a note.

> **Status.** The board is EXPERIMENTAL: it inherits the status of its processor
> (`rv64i-lab-v0` v0, the EXPERIMENTAL release), and every claim here reads as conditional
> on the CPU's own acceptance trajectory — the composition can never outrank its
> processor (`D-BOARD-STATUS`). This verdict is a contract-design result: no device is
> modelled in Rust yet, and nothing here is a firmware-probe result (probes are
> `P5-BOARD.5`'s).

This document is the authored half of the verdict, and it is the board unit's evidence
chapter — the board's own book includes it. The mechanical half is re-decided on every
commit; the canonical inputs are `board.sexp` (the definition, with the `satisfies` and
`answers` edges) and the composed catalogues (generated, BOARD-GEN-fresh).

## The three mechanical legs

1. **Discharge.** All 8 environment-assumptions in the composed unit are discharged by
   named guarantees (`scripts/discharge_assumptions.py` over the composed catalogues —
   the same verdict `MODEL-COMPOSE.3` defined, consumed, never re-implemented):

   ```
   OB-ENV-ADDRESS-UNITS    -> 'OB-ADDR-WRAP' (cpu-guarantee)
   OB-ENV-ACCESS-WIDTHS    -> 'OB-LOAD-EXT' (cpu-guarantee)
   OB-ENV-VIRTUAL-TIME     -> 'OB-PLATFORM' (cpu-guarantee)
   OB-ENV-EVENT-DELIVERY   -> 'OB-ECALL-EBREAK', 'OB-MISALIGN-REPORT', 'OB-PLATFORM' (cpu-guarantee)
   OB-ENV-ORDERING         -> 'OB-FENCE' (cpu-guarantee)
   OB-ENV-FETCH-SUPPLY     -> 'OB-FETCH-IMPLICIT', 'OB-FETCH-MAP' (cpu-guarantee)
   OB-ENV-RESET            -> 'OB-ENTRY-STATE' (cpu-guarantee)
   OB-ENV-PARTIAL-PROGRESS -> 'OB-LOAD-X0' (cpu-guarantee)
   ```

2. **Satisfies.** Every `satisfies` edge in the board definition resolves to a
   discharged environment-assumption: `reset` → `OB-ENV-RESET`,
   `timers` → `OB-ENV-VIRTUAL-TIME`, `interrupt-controller` → `OB-ENV-EVENT-DELIVERY`.

3. **Dispositions.** Every device obligation the dossier defers to the composing board
   (marked `composition_disposition "required"`) is answered by exactly one board
   decision: `D-BOARD-NIC-STRAPS` → `OB-NIC-STRAP-RESETS`,
   `D-BOARD-NIC-TIME-FROZEN` → `OB-NIC-TIME-SOURCES`,
   `D-BOARD-NIC-LINK-SCENE` → `OB-NIC-PHY-LINK`,
   `D-BOARD-NIC-PIN-TIEOFFS` → `OB-NIC-GPIO-PINS`.

## Per assumption: what satisfies it on this board

The discharge edges above are obligation-graph edges; this table is the content half —
the guarantee *on this board* behind each assumption, and how the verdict knows.

| Assumption | Satisfied by | How the verdict knows |
| --- | --- | --- |
| `OB-ENV-RESET` (reset wiring) | The board's cold-only reset (`board.sexp` `reset` block, `satisfies` edge); both device dossiers pin POR/nRESET semantics for a cold reset (`REQ-D-NIC-RESETS`; the UART's stated resets); the entry state is the CPU contract's, cited, not restated | The `reset` block carries `(kinds cold)` only, and the generator refuses a definition whose wiring is inconsistent |
| `OB-ENV-ADDRESS-UNITS` (memory attributes) | One 64-bit byte space; regions resolved with computed ends in `hardware.sexp`; an access outside every declared region is `AccessFault` (the harness rule, unchanged — the board only adds regions) | The regions are data, overlap-refused by the generator |
| `OB-ENV-ACCESS-WIDTHS` | Per-device declared widths — 32-bit (UART, FU540-C000 §13.3) and 32-bit (NIC, D32 strapped); any other width is a board-reported contract violation, never silently serviced (`D-BOARD-ACCESS-POLICY`); a misaligned access never reaches a device — the CPU raises `AlignmentException` first (`OB-MISALIGN-DATA`) | The `access-widths` declarations are data, mirrored into `hardware.sexp` |
| `OB-ENV-VIRTUAL-TIME` (counter units, time progress) | No timer device exists (`timers (present false)`, `satisfies` edge); the NIC's guest-readable time sources are **frozen** (`D-BOARD-NIC-TIME-FROZEN`); the UART carries no counter (`div` is a programmed divisor latch, not a counting register); the CPU profile's CSR exclusion is unchanged — the same digest-pinned unit | The absence is declared data; the freeze is a BOARD-VERDICT-bound disposition |
| `OB-ENV-EVENT-DELIVERY` (source priorities) | No interrupt controller exists (`interrupt-controller (present false)`, `satisfies` edge); both devices' interrupt lines are **unconnected and declared so** — drivers poll. No interrupt sources exist, so no source-priority question arises; device status bits still set per datasheet (MMIO-visible, §5.3.4's discipline) | The absences and the per-device `interrupt unconnected` declarations are data |
| `OB-ENV-ORDERING` | One hart, sequential, in-order — the board adds no concurrency: both devices are programmed-I/O slaves with no bus-master DMA, so every device effect is guest-initiated and completes at the guest's own access | The no-DMA shape is datasheet-measured (`REQ-D-NIC-HBI`; the UART has no DMA) |
| `OB-ENV-FETCH-SUPPLY` (instruction visibility) | Fetch is served from RAM only: every MMIO region is declared non-executable and the generator *refuses* an executable MMIO region; no extraneous fetch exists to perform; no cache exists anywhere — stores and fetches hit the same RAM, so code visibility is coherent by construction | The executability flags are data, generator-enforced (`D-BOARD-FETCH`) |
| `OB-ENV-PARTIAL-PROGRESS` (reservation invalidations) | The profile's encoding is rv64i only — no A extension, no `LR`/`SC`, so **no reservations exist to invalidate**; device side effects (FIFO pops, self-clearing bits) complete at the access, so no partially committed external effect is observable | The composed encoding derives from the rv64i fragment alone (BOARD-GEN-fresh) |

The aspects the gate names that do not arise are recorded, not skipped: **source
priorities** (no sources), **counter units** (no reachable counters — the NIC's are
frozen), **reservation invalidations** (no reservations).

## The four composition dispositions

The device dossier defers four values to the composing board (each obligation is marked
`composition_disposition "required"`; each answer is a `board.sexp` decision, mirrored
into `hardware.sexp` so the model route consumes it as data):

- **`D-BOARD-NIC-STRAPS`** — the configuration straps: **D32/nD16 tied HIGH** (32-bit
  host bus mode — the datasheet's native mode, "no special requirements", §3.6 — and the
  64-bit host's natural width; EEDIO has no internal pull, Table 2-4, so the tie is an
  explicit board choice) and **SPEED_SEL unwired**, latching its internal pull-up
  (Table 2-3: `I (PU)`) as 1 (Table 2-2: 100 Mbps with auto-negotiation enabled).
  Consequences: `HW_CFG` = `0x00050004` at reset; PHY 0 bits 13/12 = 1/1; PHY 4 =
  `0x01E1`; PHY 31's HCDSPEED default is 100BASE-TX half-duplex (`010b`) pre-negotiation.
  **The verdict narrowed the board:** `.1` had declared 16- and 32-bit accesses for eth0
  from §1.10's summary sentence, but §3.6 makes the bus widths mode-exclusive — with D32
  strapped, a 16-bit access has no datasheet-defined behaviour (`REQ-D-NIC-WIDTH`), so
  the declaration narrows to 32 only and the dossier's 16-bit pairing-latch census entry
  flips to absent. A defect the composition verdict exists to catch.
- **`D-BOARD-NIC-TIME-FROZEN`** — the guest-readable time sources are **frozen**:
  `FREE_RUN` reads its reset value 0 forever; `GPT_CNT` never advances (a `TIMER_EN`
  write still loads `GPT_LOAD` — datasheet-defined, deterministic — but the count never
  decrements, so `GPT_INT` never sets); `INT_DEAS` never runs (the interrupt line is
  unconnected, `INT_EN` resets 0). Constant or guest-written-static values carry no time
  information, so `OB-ENV-VIRTUAL-TIME` holds with the NIC present and the harness's
  retired-instruction count never becomes target-visible. The deviation from
  wall-clock-faithful behaviour is deliberate and recorded as data: a polled driver
  never needs these counters; a guest busy-waiting on one would hang.
- **`D-BOARD-NIC-LINK-SCENE`** — the recorded-trace replay's declared link scene is
  **static and complete**: the wire is up at 100BASE-TX full-duplex with auto-negotiation
  complete, from before the guest's first access — the board's cold reset completes
  before any guest access exists (`D-BOARD-RESET`), the same discipline the reset
  expectations already use for READY and EPC_BSY. Every guest-observable read sees the
  completed scene: PHY 1 (Basic Status) = `0x782D` (the `0x7809` reset composition with
  Link Status and Auto-Negotiate Complete; the latch-low Link bit never trips because the
  scene never fails), PHY 17 ENERGYON = 1, PHY 31 Autodone = 1 with HCDSPEED = `110b`,
  PHY 5 = `0x01E1` (the declared partner scene). Note 3-11's wait-for-link succeeds at
  the first read — never a live host link.
- **`D-BOARD-NIC-PIN-TIEOFFS`** — no GPIO/LED/EEPROM pins are wired: `GPIODn` reads 0
  regardless of direction, and the `EEPR_EN`-muxed MII monitor signals read 0 — declared
  tie-offs, never live host signals.

## The `OB-PLATFORM` note — read this before citing the discharge

Two platform-dependent assumptions (`OB-ENV-VIRTUAL-TIME`, `OB-ENV-EVENT-DELIVERY`)
discharge through `OB-PLATFORM`, the **laboratory** platform guarantee ("declares exactly
one region — the MainMemory region — and NO devices"), scoped to `rv64i-lab-v0` by
`profile_ids`. Read alone, that edge is formally true and materially misleading: the
board declares three regions and two devices. The composition holds because the
assumptions' *content* is re-established on the board — no guest-reachable time source
(the declared timer absence plus the frozen NIC counters), no deliverable asynchronous
event (the declared controller absence plus the unconnected-and-declared interrupt
lines). That re-establishment is exactly what the `satisfies` and `answers` edges make
data, and what BOARD-VERDICT's legs 2–3 check. The verdict also answers `MODEL-COMPOSE`'s
open question for this board shape: **no operator beyond union + discharge is needed** —
the declared edges close the gap; a board whose CPU contract has counter/interrupt
assumptions to satisfy instead is where a richer answer would be earned.

## The interface-test leg

The leaf's second acceptance: the laboratory's interface tests re-run against the board
provider where meaningful. There is no board provider in Rust yet (the device models are
the model route), so the meaningful half today is the one the board preserves: the RAM
region — the same base and size (`0x8000_0000`, 2 GiB) as the laboratory harness, so a
guest built for the laboratory runs unchanged on the board (`D-BOARD-MEMORY-MAP`). The
laboratory's boundary and fixture suites — the `Environment` contract tests
(`semulith-core`), the `FlatMemory`/`ScriptedEnv` fixture suites (`semulith-verify`),
and the guest smoke — were re-run with this verdict and are green; they exercise exactly
that RAM half. The MMIO halves attach with the device models (the model route) and are
probed by `P5-BOARD.5` — named owners, never silently skipped.

## What this verdict does not claim

- Not a boot claim, and no Linux anything (`P6-LINUX`).
- Not that any device model exists — the dossiers, the definition and this verdict are
  the contracts the model route consumes.
- Not that the composition outranks its processor: EXPERIMENTAL, conditional on
  `rv64i-lab-v0`'s acceptance trajectory.
- Not that the laboratory's evidence transfers blindly: the laboratory validated the CPU
  under `OB-PLATFORM`'s one-region platform; this verdict is the *board's* demonstration
  that the same assumptions hold here, by named board and device guarantees.
