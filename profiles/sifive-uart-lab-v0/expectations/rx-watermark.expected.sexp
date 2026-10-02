;; rx-watermark.expected.sexp — receive-FIFO and watermark expectations for
;; `sifive-uart-lab-v0` (P5-BOARD.2, 2026-10-02). Datasheet-derived before any model
;; exists. Stimulus: three recorded-input characters ("ABC" = 0x41 0x42 0x43) enqueued
;; into the Rx FIFO with rxctrl = 0's rxcnt = 0, then the ip/rxdata observations below.
;;
;; ⛔ THE WATERMARK BITS PIN ONLY WHAT BOTH READINGS OF §13.8 AGREE ON. The manual gives
;; each bit a strict-inequality RAISED condition and a strict-inequality CLEARED condition
;; and never says whether the bit is a pure level of occupancy or holds between the two —
;; the == boundary and any value before a condition first holds are undetermined
;; (REQ-D-UART-WM-MODE), and the reset values are X (REQ-D-UART-RESET-X). A bit is pinned
;; here only when its raised condition holds (true under every reading); everything else
;; is deliberately NOT pinned, with the reason in the derivation.

(expectations
  (program "rx FIFO and watermark levels — sifive-uart-lab-v0 (uart0 on netboard-lab-v0)")
  (step (n 1) (insn "3 recorded characters enqueued (rxcnt = 0, txcnt = 0, TX empty); read ip")
    (writes (write (reg "ip") (value "bit1=1; bit0 not pinned")))
    (derivation "rxwm's raised condition holds: Rx occupancy 3 is strictly greater than rxcnt 0 — true under every reading of §13.8, so bit 1 pins to 1. txwm's raised condition (0 < 0) is false and no clear has occurred since reset (and reset is X), so bit 0 is NOT pinned (REQ-D-UART-WM-MODE).")
    (source "FU540-C000 v1p5 §13.8, Table 65"))
  (step (n 2) (insn "read rxdata (first dequeue)")
    (writes (write (reg "rxdata") (value "0x00000041")))
    (derivation "A read dequeues the head character and returns it in data[7:0]; the FIFO was non-empty, so empty reads 0 — one dequeue per read, the map's sharpest side effect.")
    (source "FU540-C000 v1p5 §13.5, Table 61"))
  (step (n 3) (insn "read rxdata (second dequeue)")
    (writes (write (reg "rxdata") (value "0x00000042")))
    (derivation "FIFO order is preserved: the second read returns the second recorded character with empty = 0.")
    (source "FU540-C000 v1p5 §13.5, Table 61"))
  (step (n 4) (insn "read rxdata (third dequeue)")
    (writes (write (reg "rxdata") (value "0x00000043")))
    (derivation "The third read drains the FIFO; the character is valid, so empty still reads 0 — empty reports the FIFO was empty AT THIS read, and it was not.")
    (source "FU540-C000 v1p5 §13.5, Table 61"))
  (step (n 5) (insn "read rxdata (FIFO empty)")
    (writes (write (reg "rxdata") (value "bit31=1; data not a valid character (unspecified)")))
    (derivation "The FIFO is now empty, so empty reads 1; §13.5 says only that 'the data field does not contain a valid character' — it does not say zero, so the data bits are deliberately NOT pinned.")
    (source "FU540-C000 v1p5 §13.5, Table 61"))
  (step (n 6) (insn "read ip (Rx drained, rxcnt = 0) — nothing pinned")
    (writes)
    (derivation "Under the level reading both bits are 0; under the hold reading rxwm has never met its clear condition (the occupancy cannot fall BELOW 0) and txwm has never been raised or cleared. The two readings disagree here, so nothing pins (REQ-D-UART-WM-MODE) — this is exactly the case a polled driver must not trust the bit for.")
    (source "FU540-C000 v1p5 §13.8, Table 65"))
  (step (n 7) (insn "write txctrl = 0x00010000 (txcnt = 1, txen = 0), TX empty; read ip")
    (writes (write (reg "ip") (value "bit0=1; bit1 not pinned")))
    (derivation "txcnt is bits [18:16], so 1 << 16 = 0x00010000 (Table 62); with the TX FIFO empty, txwm's raised condition (0 < 1) holds under every reading, so bit 0 pins to 1. rxwm's raised condition is false and its clear condition may never have held, so bit 1 is NOT pinned (REQ-D-UART-WM-MODE).")
    (source "FU540-C000 v1p5 §13.8, Table 65; §13.6, Table 62"))
  (step (n 8) (insn "write 0x41 to txdata (occupancy 1 == txcnt); read ip — nothing pinned")
    (writes)
    (derivation "At occupancy == txcnt the raised condition (1 < 1) is false AND the cleared condition ('enqueued to exceed the watermark', 1 > 1) is false — the == boundary is precisely what §13.8's two strict sentences leave undetermined (REQ-D-UART-WM-MODE). Nothing pins.")
    (source "FU540-C000 v1p5 §13.8, Table 65")))
