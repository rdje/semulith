;; profile.sexp — the decision dossier for `sifive-uart-lab-v0` (P5-BOARD.2, 2026-10-02).
;; The first DEVICE unit dossier: the schema's device-shaped generalization lands with
;; this document (architecture/base/harts/ilen/ialign and state.program_counter optional,
;; the mmio_registers scope group, vehicle route device-model / comparison
;; register-expectations — each a named case in schema/profile.sexp). Validate by hand:
;;   python3 scripts/check_sexp_schema.py profiles/sifive-uart-lab-v0/profile.sexp schema/profile.sexp
;; Every decision mirrors its requirement's statement EXACTLY (RECORD-SCHEMA rule 4), and
;; every obligation mirrors both (rule 9): one fact, three surfaces, one wording.

(profile (id "sifive-uart-lab-v0") (version "0") (status "experimental") (chapter_version "FU540-C000 Manual v1p5") (spec_revision "v1p5")
  (comment "No architecture/base/harts/ilen/ialign: a UART has no instruction set, no harts and no"
           "fetch width — forcing any of them would record a lie (the P3-BREADTH.5 xlen"
           "precedent). chapter_version/spec_revision name the DOCUMENT's issue, as for"
           "dsp56300-lab-v0. EXPERIMENTAL: the unit inherits the board's and the processor's"
           "status; every claim reads as conditional on the CPU's acceptance trajectory.")
  (sources "SIFIVE-FU540-C000")
  (state (authority architecture) (source "FU540-C000 v1p5 §13, Tables 58–66")
         (comment "No program_counter, no integer file, no CSRs — a device has no"
                  "instruction-execution state. The state census is the seven MMIO registers"
                  "plus the two 8-entry FIFOs, carried in state.sexp with the hidden-state"
                  "census that earns the 'and nothing else' claim."))
  (vehicle (route device-model) (comparison register-expectations) (authority laboratory)
           (source "P5-BOARD .2 design brief (docs/tasks/P5-BOARD.md, Decisions, 2026-10-02); decision_device-applicability-by-declared-vehicle — the evidence shape is datasheet-derived register-read expectations (expectations/), not per-step traces or checkpoints; instruction-shaped gates derive not-applicable from this declaration"))
  (scope (count_base 7) (count_total 7) (authority architecture) (source "FU540-C000 v1p5 §13.3, Table 59")
    (comment "The WHOLE §13 register map, nothing excluded: count_base = count_total = 7 MMIO"
             "registers. The dossier models ONE instance — the board's uart0 (Table 58's"
             "instance-0 row) — and the behaviour each register implies; the SoC's second"
             "instance (identical parameters, 0x10011000) and the serial wire itself are out"
             "of scope, the wire being the environment's (recorded input on RX, host console"
             "on TX).")
    (mmio_registers "txdata")
    (mmio_registers "rxdata")
    (mmio_registers "txctrl")
    (mmio_registers "rxctrl")
    (mmio_registers "ie")
    (mmio_registers "ip")
    (mmio_registers "div"))
  (decision (id "D-UART-MAP") (authority architecture) (statement "The UART register map is seven 32-bit registers — txdata 0x00, rxdata 0x04, txctrl 0x08, rxctrl 0x0C, ie 0x10, ip 0x14, div 0x18 — designed to require only naturally aligned 32-bit memory accesses.") (source "FU540-C000 v1p5 §13.3, Table 59"))
  (decision (id "D-UART-INSTANCE") (authority architecture) (statement "UART instance 0 is at base address 0x10010000 with div_width = 20, div_init = 289 and 8-entry transmit and receive FIFOs; instance 1 at 0x10011000 has identical parameters.") (source "FU540-C000 v1p5 §13.2, Table 58"))
  (decision (id "D-UART-TXDATA-WRITE") (authority architecture) (statement "Writing txdata enqueues the data field's character into the transmit FIFO if the FIFO can accept new entries; when the full flag is set, writes to data are ignored.") (source "FU540-C000 v1p5 §13.4, Table 60"))
  (decision (id "D-UART-TXDATA-READ") (authority architecture) (statement "Reading txdata returns the current value of the full flag (bit 31) and zero in the data field; the full flag indicates whether the transmit FIFO can accept new entries.") (source "FU540-C000 v1p5 §13.4, Table 60"))
  (decision (id "D-UART-RXDATA-READ") (authority architecture) (statement "Reading rxdata dequeues a character from the receive FIFO and returns it in the data field; the empty flag (bit 31) indicates whether the receive FIFO was empty, and when set the data field does not contain a valid character.") (source "FU540-C000 v1p5 §13.5, Table 61"))
  (decision (id "D-UART-RXDATA-WRITE") (authority architecture) (statement "Writes to rxdata are ignored.") (source "FU540-C000 v1p5 §13.5"))
  (decision (id "D-UART-TXCTRL") (authority architecture) (statement "txctrl is read-write: txen (bit 0) controls whether the Tx channel is active — when cleared, transmission of Tx FIFO contents is suppressed and the txd pin is driven high; nstop (bit 1) selects one (0) or two (1) stop bits; txcnt (bits [18:16]) is the transmit watermark threshold. txctrl resets to 0.") (source "FU540-C000 v1p5 §13.6, Table 62"))
  (decision (id "D-UART-RXCTRL") (authority architecture) (statement "rxctrl is read-write: rxen (bit 0) controls whether the Rx channel is active — when cleared, the state of the rxd pin is ignored and no characters are enqueued into the Rx FIFO; rxcnt (bits [18:16]) is the receive watermark threshold. rxctrl resets to 0. Characters are enqueued when a zero (low) start bit is seen.") (source "FU540-C000 v1p5 §13.7, Table 63"))
  (decision (id "D-UART-IE") (authority architecture) (statement "ie is read-write: txwm (bit 0) is the transmit watermark interrupt enable and rxwm (bit 1) is the receive watermark interrupt enable. ie resets to 0.") (source "FU540-C000 v1p5 §13.8, Table 64"))
  (decision (id "D-UART-IP") (authority architecture) (statement "ip is read-only: txwm (bit 0) becomes raised when the number of entries in the transmit FIFO is strictly less than txcnt and is cleared when sufficient entries have been enqueued to exceed the watermark; rxwm (bit 1) becomes raised when the number of entries in the receive FIFO is strictly greater than rxcnt and is cleared when sufficient entries have been dequeued to fall below the watermark.") (source "FU540-C000 v1p5 §13.8, Table 65"))
  (decision (id "D-UART-WM-MODE") (authority architecture) (statement "Whether an ip watermark bit is a pure level function of FIFO occupancy or holds its value between its raised and cleared conditions is not specified: §13.8 gives each bit a strict-inequality raised condition and a strict-inequality cleared condition, so the == boundary and any value before a condition first holds — including after reset, where the bits are X — are undetermined.") (source "FU540-C000 v1p5 §13.8, Table 65 (the two strict sentences per bit; the gap measured against them)"))
  (decision (id "D-UART-DIV") (authority architecture) (statement "div is a read-write div_width-bit register (div_width = 20) specifying the divisor used by baud-rate generation for both channels; its reset value is div_init = 289, tuned to provide 115200 baud out of reset given the expected tlclk frequency, and the divide ratio is one greater than the value stored in div.") (source "FU540-C000 v1p5 §13.9, Table 58, Table 66"))
  (decision (id "D-UART-FIFO-DEPTH") (authority architecture) (statement "The transmit and receive FIFOs are 8 entries each.") (source "FU540-C000 v1p5 §13.1, Table 58"))
  (decision (id "D-UART-FORMAT") (authority architecture) (statement "The UART supports 8-N-1 and 8-N-2 formats — 8 data bits, no parity, 1 start bit, 1 or 2 stop bits — with 16x Rx oversampling and 2/3 majority voting per bit; it does not support hardware flow control, other modem control signals, or synchronous serial data transfers.") (source "FU540-C000 v1p5 §13.1"))
  (decision (id "D-UART-RESERVED") (authority architecture) (statement "The behaviour of the Reserved bit fields (txdata [30:8], rxdata [30:8], txctrl [15:2] and [31:19], rxctrl [15:1] and [31:19], ie [31:2], ip [31:2]) is not specified: the tables mark them Reserved with no read or write semantics.") (source "FU540-C000 v1p5 Tables 60–65"))
  (decision (id "D-UART-RESET-X") (authority architecture) (statement "The reset values of txdata.full, rxdata.data, rxdata.empty, ip.txwm and ip.rxwm are unspecified: the tables mark their reset column X. The stated resets are txctrl = 0, rxctrl = 0, ie = 0 and div = div_init.") (source "FU540-C000 v1p5 Tables 60, 61, 65; §13.6–§13.9"))
  (decision (id "D-UART-FIFO-RESET") (authority architecture) (statement "The transmit and receive FIFO contents and occupancies at reset are not specified: §13 gives register reset values only and no FIFO reset statement.") (source "FU540-C000 v1p5 §13 (the silence measured against §13.6–§13.9's explicit reset statements)"))
  (decision (id "D-UART-OFFMAP") (authority architecture) (statement "The effect of an access at an offset outside Table 59's seven registers within the instance's address window is not specified.") (source "FU540-C000 v1p5 §13.3, Table 59"))
  (decision (id "D-UART-WIDTH") (authority architecture) (statement "The effect of an access that is not a naturally aligned 32-bit access is not specified: the map is 'designed to require only' such accesses, and the manual states no error or truncation behaviour for any other width or alignment.") (source "FU540-C000 v1p5 §13.3")))
