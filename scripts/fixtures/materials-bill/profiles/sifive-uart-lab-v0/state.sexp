;; state.sexp — the device-state document for `sifive-uart-lab-v0` (P5-BOARD.2, 2026-10-02).
;; Validate:
;;   python3 scripts/check_sexp_schema.py profiles/sifive-uart-lab-v0/state.sexp schema/state.sexp
;; A device has no XLEN and no integer file (the P3-BREADTH.5 optionals); its architectural
;; state is the seven MMIO registers plus the two FIFOs, and the census below earns the
;; "and nothing else the MMIO boundary can reach" claim. gen_state.py is rv64i-only by
;; construction (STATE-GEN) — this document is decided by DOSSIER-SCHEMA and
;; PROFILE-CONSISTENCY, never fed to the generator.

(state (profile_id "sifive-uart-lab-v0")
  (note "Device state at the MMIO boundary: the seven 32-bit registers of FU540-C000 v1p5 §13 plus the two 8-entry FIFOs. Resets marked X by the datasheet are recorded as unspecified, never guessed (REQ-D-UART-RESET-X / REQ-D-UART-FIFO-RESET). The wire-timing internals are enumerated in the census and shown unreachable from MMIO.")
  (special_registers
    (register (id "txdata") (width_bits 32) (holds "write: character to enqueue into the Tx FIFO in data[7:0]; read: the full flag (bit 31), zero in data") (authority architecture) (source "FU540-C000 v1p5 §13.4, Table 60") (reset "unspecified — Table 60 marks data and full X") (reset_authority architecture)))
  (special_registers
    (register (id "rxdata") (width_bits 32) (holds "read: dequeued character in data[7:0] and the empty flag (bit 31); writes ignored") (authority architecture) (source "FU540-C000 v1p5 §13.5, Table 61") (reset "unspecified — Table 61 marks data and empty X") (reset_authority architecture)))
  (special_registers
    (register (id "txctrl") (width_bits 32) (holds "txen (bit 0), nstop (bit 1), txcnt (bits [18:16]) — transmit channel control and watermark threshold") (authority architecture) (source "FU540-C000 v1p5 §13.6, Table 62") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "rxctrl") (width_bits 32) (holds "rxen (bit 0), rxcnt (bits [18:16]) — receive channel control and watermark threshold") (authority architecture) (source "FU540-C000 v1p5 §13.7, Table 63") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "ie") (width_bits 32) (holds "txwm (bit 0) and rxwm (bit 1) interrupt enables") (authority architecture) (source "FU540-C000 v1p5 §13.8, Table 64") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "ip") (width_bits 32) (holds "txwm (bit 0) and rxwm (bit 1) interrupt pending — read-only level conditions on FIFO occupancy") (authority architecture) (source "FU540-C000 v1p5 §13.8, Table 65") (reset "unspecified — Table 65 marks both bits X") (reset_authority architecture)))
  (special_registers
    (register (id "div") (width_bits 32) (holds "the baud-rate divisor for both channels; div_width = 20 significant bits, divide ratio = div + 1") (authority architecture) (source "FU540-C000 v1p5 §13.9, Table 58, Table 66") (reset "0x00000121 (div_init = 289 — tuned for 115200 baud at the expected tlclk)") (reset_authority architecture)))
  (register_family (id "tx_fifo") (count 8) (width_bits 8) (ids "tx_fifo[0..7]") (authority architecture) (source "FU540-C000 v1p5 §13.1, Table 58, §13.4")
    (comment "enqueue order preserved; the head character is what transmission consumes. Occupancy is MMIO-visible only as full (bit 31 of txdata reads) and the txwm strict-less-than level.")
    (reset (value "unspecified") (authority architecture) (source "FU540-C000 v1p5 §13 — the measured silence (REQ-D-UART-FIFO-RESET)") (statement "The datasheet never states the FIFOs reset: contents and occupancy at reset are unspecified — recorded as the element's declared start, not guessed. An implementation's choice is laboratory.")))
  (register_family (id "rx_fifo") (count 8) (width_bits 8) (ids "rx_fifo[0..7]") (authority architecture) (source "FU540-C000 v1p5 §13.1, Table 58, §13.5")
    (comment "the head character is what an rxdata read dequeues. Occupancy is MMIO-visible only as empty (bit 31 of rxdata reads) and the rxwm strict-greater-than level.")
    (reset (value "unspecified") (authority architecture) (source "FU540-C000 v1p5 §13 — the measured silence (REQ-D-UART-FIFO-RESET)") (statement "The datasheet never states the FIFOs reset: contents and occupancy at reset are unspecified — recorded as the element's declared start, not guessed. An implementation's choice is laboratory.")))
  (hidden_state_census
    (question "What state beyond the seven MMIO registers must the model carry to reproduce every MMIO-visible behaviour of the SiFive UART — and which hardware state is unreachable at the MMIO boundary? (SEM-08, catalog C02, asked of a device)")
    (answer "The two FIFOs' contents and occupancies, and nothing else. Every other hardware state the chapter implies is invisible at the MMIO boundary: the register map exposes no counter, shift register, sampler or pin-latch readout, and the board's backends (recorded input on RX, host console on TX) move whole bytes, so wire timing can never become an MMIO observation.")
    (candidates
      (checked (candidate "Tx/Rx FIFO contents (the enqueued characters)") (present true) (why "MMIO-visible: rxdata reads return them in order, and txdata's full flag depends on Tx occupancy — the model must carry them.")))
    (candidates
      (checked (candidate "FIFO occupancy (head/tail pointers or counts)") (present true) (why "MMIO-visible as the full/empty flags and the watermark strict-inequality levels (§13.8); the model must carry occupancy, though the pointers themselves never surface.")))
    (candidates
      (checked (candidate "baud-rate divider counter phase") (present false) (why "div sets the ratio but no register reads the counter; with byte-granularity backends its phase is unobservable at MMIO.")))
    (candidates
      (checked (candidate "Tx and Rx shift registers") (present false) (why "wire-timing state; no MMIO access can read them, and the backends move bytes, not bits.")))
    (candidates
      (checked (candidate "16x oversampling sampler and 2/3 majority-vote state") (present false) (why "§13.1's receiver internals; unreachable from MMIO and irrelevant to byte-granularity RX input.")))
    (candidates
      (checked (candidate "txd output latch") (present false) (why "'txd driven high when txen is cleared' (§13.6) is a pin guarantee for the wire domain, not state an MMIO access observes.")))
    (candidates
      (checked (candidate "sticky error/status bits (framing error, overrun, break)") (present false) (why "Table 59 defines no such register — the census measured the whole map: seven registers, none an error status. Their absence is the datasheet's, not an oversight.")))
    (consequence "The model state is exactly: seven 32-bit registers, two 8-byte FIFOs with occupancies. A reset establishes the four stated register resets and leaves the X-marked flags and the FIFOs' contents/occupancy to the declared-unspecified dispositions (the board's cold-only reset, D-BOARD-RESET, records the composition's choice); no hidden register may appear in the implementation without this census changing.")))
