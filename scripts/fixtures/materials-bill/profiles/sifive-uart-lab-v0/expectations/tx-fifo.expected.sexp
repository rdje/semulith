;; tx-fifo.expected.sexp — transmit-FIFO expectations for `sifive-uart-lab-v0`
;; (P5-BOARD.2, 2026-10-02). Datasheet-derived before any model exists. Stimulus: writes
;; to txdata with the FIFO initially able to accept; observation: the full flag in bit 31
;; of txdata reads (data field reads zero, §13.4). txen stays 0 throughout — the
;; expectations are MMIO-observable only; transmission itself is the wire's business.

(expectations
  (program "tx FIFO enqueue/full behaviour — sifive-uart-lab-v0 (uart0 on netboard-lab-v0)")
  (step (n 1) (insn "write 0x41 to txdata (entry 1 of 8); read txdata")
    (writes (write (reg "txdata") (value "0x00000000")))
    (derivation "The FIFO holds 8 entries (§13.1, Table 58); after 1 enqueue it can still accept new entries, so the full flag reads 0 and the data field reads zero (§13.4).")
    (source "FU540-C000 v1p5 §13.4, Table 60; §13.1, Table 58"))
  (step (n 2) (insn "writes 2–7 to txdata (entries 2–7 of 8); read txdata")
    (writes (write (reg "txdata") (value "0x00000000")))
    (derivation "After each of enqueues 2–7 at least one entry remains free, so full still reads 0 — enqueue 7 is the boundary case before saturation.")
    (source "FU540-C000 v1p5 §13.4, Table 60; §13.1, Table 58")
    (limit "one step stands for writes 2–7: the flag depends on occupancy only, so the intermediate writes add no new observation"))
  (step (n 3) (insn "write 0x48 (entry 8 of 8); read txdata")
    (writes (write (reg "txdata") (value "0x80000000")))
    (derivation "The eighth enqueue fills the FIFO; it can no longer accept new entries, so full reads 1 (bit 31) and the data field reads zero.")
    (source "FU540-C000 v1p5 §13.4, Table 60; §13.1, Table 58"))
  (step (n 4) (insn "write 0x49 while full; read txdata")
    (writes (write (reg "txdata") (value "0x80000000")))
    (derivation "§13.4: 'when set, writes to data are ignored' — the ninth write changes nothing, and the read still reports full = 1. That the ignored character never surfaces is a consequence of the same sentence plus the FIFO's order preservation, observable only after dequeues — and dequeues are the wire's, out of MMIO scope here.")
    (source "FU540-C000 v1p5 §13.4, Table 60")))
