;; reset.expected.sexp — cold-reset register-read expectations for `sifive-uart-lab-v0`
;; (P5-BOARD.2, 2026-10-02). Every value derived from the pinned datasheet BEFORE any
;; model exists (EVD-05's shape at the device layer); `derivation` carries the reasoning
;; and `source` the locator. Device reading of the schema (recorded in
;; schema/expectations.sexp): step.insn carries the stimulus, writes the register reads
;; that must yield the value. The X-marked registers get the empty (writes) marker —
;; nothing pinned, with the reason (REQ-D-UART-RESET-X).

(expectations
  (program "cold-reset register reads — sifive-uart-lab-v0 (uart0 on netboard-lab-v0)")
  (step (n 1) (insn "cold reset; read txctrl")
    (writes (write (reg "txctrl") (value "0x00000000")))
    (derivation "§13.6 states 'the txctrl register is reset to 0' — an explicit stated reset, so the read is pinned.")
    (source "FU540-C000 v1p5 §13.6, Table 62"))
  (step (n 2) (insn "cold reset; read rxctrl")
    (writes (write (reg "rxctrl") (value "0x00000000")))
    (derivation "§13.7 states 'the rxctrl register is reset to 0' — an explicit stated reset.")
    (source "FU540-C000 v1p5 §13.7, Table 63"))
  (step (n 3) (insn "cold reset; read ie")
    (writes (write (reg "ie") (value "0x00000000")))
    (derivation "§13.8 states 'ie is reset to 0' — an explicit stated reset.")
    (source "FU540-C000 v1p5 §13.8, Table 64"))
  (step (n 4) (insn "cold reset; read div")
    (writes (write (reg "div") (value "0x00000121")))
    (derivation "§13.9: the reset value is div_init, and Table 58 gives div_init = 289 = 0x121 for both instances — 'tuned to provide a 115200 baud output out of reset given the expected frequency of tlclk'.")
    (source "FU540-C000 v1p5 §13.9, Table 58"))
  (step (n 5) (insn "cold reset; the X-marked flags — nothing pinned")
    (writes)
    (derivation "txdata.full, rxdata.data, rxdata.empty, ip.txwm and ip.rxwm are marked X in the tables' reset columns, and §13 nowhere states the FIFOs reset empty — so NO value is pinned for txdata, rxdata or ip at reset (REQ-D-UART-RESET-X, REQ-D-UART-FIFO-RESET). Plausibility (an empty FIFO implying full = 0) is not a source.")
    (source "FU540-C000 v1p5 Tables 60, 61, 65")))
