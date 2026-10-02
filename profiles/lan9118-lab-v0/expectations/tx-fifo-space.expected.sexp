;; tx-fifo-space.expected.sexp — TX FIFO free-space accounting expectations for
;; `lan9118-lab-v0` (P5-BOARD.10, 2026-10-02). Datasheet-derived before any model exists.
;; Stimulus: TX command/payload writes to the TX data FIFO port (0x20) with TX_ON = 0
;; throughout — the transmitter never runs, so no wire is needed and every observation is
;; MMIO-visible free-space arithmetic under §3.12.5's usage rules. The RESETS record's
;; first-read discipline (REQ-D-NIC-FIRST-READ) is satisfied by the step-1 reads.

(expectations
  (program "TX FIFO free-space accounting — lan9118-lab-v0 (eth0 on netboard-lab-v0)")
  (step (n 1) (insn "cold reset; read tx_fifo_inf")
    (writes (write (reg "tx_fifo_inf") (value "0x00001200")))
    (derivation "TDFREE resets to 1200h = 4608 — the default allocation's whole TX data FIFO (§5.3.12, Table 5-3 row TX_FIF_SZ = 5); TXSUSED = 0. This is the baseline the accounting steps derive from.")
    (source "DS00002266B §5.3.12, Table 5-3"))
  (step (n 2) (insn "queue a 60-byte packet in one buffer: write cmd A = 0x0000303C (FS=1, LS=1, Buffer Size = 60, no offset/alignment), cmd B = 0x0000003C (Packet Length = 60), then 15 payload DWORDs; read tx_fifo_inf")
    (writes (write (reg "tx_fifo_inf") (value "0x000011BC")))
    (derivation "§3.12.5: command A is stored for every buffer (4 B), command B is stored because First Segment is set (4 B), and the 60-byte payload is 15 whole DWORDs with no offset or padding to strip — 68 bytes consumed. TDFREE = 4608 − 68 = 4540 = 0x11BC; TXSUSED stays 0 (TX_ON = 0: nothing transmits, no status is produced).")
    (source "DS00002266B §3.12.5, §3.12.2, Table 3-11, Table 3-12"))
  (step (n 3) (insn "queue a 4-byte packet in one buffer: cmd A = 0x00003004 (FS=1, LS=1, size 4), cmd B = 0x00000004, one payload DWORD; read tx_fifo_inf")
    (writes (write (reg "tx_fifo_inf") (value "0x000011B0")))
    (derivation "Same accounting: 4 + 4 + 4 = 12 bytes consumed (one DWORD of payload, both commands stored). TDFREE = 4540 − 12 = 4528 = 0x11B0.")
    (source "DS00002266B §3.12.5"))
  (step (n 4) (insn "queue a 100-byte packet in TWO buffers: buffer 1 cmd A = 0x00002040 (FS=1, LS=0, size 64) + cmd B = 0x00000064 (Packet Length 100) + 64 payload bytes; buffer 2 cmd A = 0x00001024 (FS=0, LS=1, size 36) + 36 payload bytes; read tx_fifo_inf")
    (writes (write (reg "tx_fifo_inf") (value "0x00001140")))
    (derivation "Buffer 1 stores command A, command B (FS=1) and 64 payload bytes = 72; buffer 2 stores command A and 36 payload bytes but NOT command B — command B is written into the TX data FIFO only when First Segment is set (§3.12.5) — = 40. TDFREE = 4528 − 112 = 4416 = 0x1140. The identical command B and matching Packet Length keep TXE deasserted (§3.12.7).")
    (source "DS00002266B §3.12.5, §3.12.2"))
  (step (n 5) (insn "write tx_cfg = 0x00004000 (TXD_DUMP); read tx_fifo_inf")
    (writes (write (reg "tx_fifo_inf") (value "0x00001200")))
    (derivation "TXD_DUMP (bit 14, self-clearing) clears the TX data FIFO of all pending data — the TX data pointers are cleared to zero (§5.3.8) — so the whole 4608-byte allocation reports free again: 0x1200.")
    (source "DS00002266B §5.3.8"))
  (step (n 6) (insn "negative: write more TX data than TDFREE reports (a command sequence declaring a 4096-byte buffer, then payload past the free space); read int_sts")
    (writes (write (reg "int_sts") (value "bit13=1 (TXE)")))
    (derivation "§3.12: the host must check the available TX FIFO space and must not overfill it, 'or the TX Error (TXE) flag will be asserted'; §3.12.7 lists host overrun of the TX data FIFO as a TXE condition. Only the flag pins — what happens to the excess data is not stated, so nothing beyond bit 13 is pinned.")
    (source "DS00002266B §3.12, §3.12.7")))
