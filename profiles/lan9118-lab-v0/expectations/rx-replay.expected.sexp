;; rx-replay.expected.sexp — receive-path expectations for `lan9118-lab-v0`
;; (P5-BOARD.10, 2026-10-02). Datasheet-derived before any model exists.
;; Stimulus: the board's recorded-trace replay backend (D-BOARD-NET-BACKEND) offers ONE
;; recorded frame when polled: a 64-byte broadcast frame (destination FF:FF:FF:FF:FF:FF),
;; received error-free with the device in its reset configuration (MAC_CR = 0x00040000 —
;; PRMS set, BCAST clear — so the frame passes filtering). Every pinned value derives from
;; the datasheet's status-word format (§3.13.3), FIFO port semantics (§5.2) and INF
;; register fields (§5.3.11) applied to that declared stimulus — nothing is an
;; implementation's output.

(expectations
  (program "RX replay path — lan9118-lab-v0 (eth0 on netboard-lab-v0)")
  (step (n 1) (insn "the recorded frame is offered; read rx_fifo_inf")
    (writes (write (reg "rx_fifo_inf") (value "0x00010040")))
    (derivation "One status word is queued (RXSUSED = 1 in bits [23:16]) and the 64-byte frame is DWORD-aligned, so RXDUSED = 64 = 0x40 (§5.3.11: per frame, the length rounded up to the nearest DWORD).")
    (source "DS00002266B §5.3.11, §3.13"))
  (step (n 2) (insn "read the RX status PEEK (0x44)")
    (writes (write (reg "rx_status_fifo_peek") (value "0x00402000")))
    (derivation "The status word for this frame (§3.13.3): Packet Length 64 in bits [29:16] = 0x00400000; Broadcast Frame (bit 13) = 0x2000; Error Status (15) = 0 — bits 11, 7, 6 and 1 are all clear for an error-free, full-length, collision-free, CRC-valid frame; Filtering Fail (30) = 0 (PRMS is set in the reset MAC_CR, so the frame passes). PEEK is the non-destructive read of the top location (§5.2.1).")
    (source "DS00002266B §3.13.3, §5.2.1, §5.4.1"))
  (step (n 3) (insn "read the RX status PEEK again")
    (writes (write (reg "rx_status_fifo_peek") (value "0x00402000")))
    (derivation "PEEK does not pop: the top (oldest) location reads back identically (§5.2.1).")
    (source "DS00002266B §5.2.1"))
  (step (n 4) (insn "read the RX status FIFO port (0x40); read rx_fifo_inf")
    (writes (write (reg "rx_status_fifo_port") (value "0x00402000")) (write (reg "rx_fifo_inf") (value "0x00000040")))
    (derivation "The status port performs a destructive read — it returns the same top word and pops the FIFO (§5.2.1), so RXSUSED falls to 0 while RXDUSED still reports the unread 64 bytes of frame data.")
    (source "DS00002266B §5.2.1, §5.3.11"))
  (step (n 5) (insn "read the RX data FIFO port 16 times (the 64-byte frame)")
    (writes (write (reg "rx_data_fifo_port") (value "the recorded frame's DWORDs in reception order — read n returns frame bytes 4n..4n+3 with the first-received byte in D[7:0]")))
    (derivation "Each read pops the head DWORD (§5.2.1's destructive reads); the LAN9118 always receives data into the RX data FIFO low-order word first (§5.3.17's preamble), so the first read carries the frame's first four bytes with byte 0 in D[7:0]. The content is the declared trace's; what the datasheet pins is the order and the pop.")
    (source "DS00002266B §5.2.1, §5.3.17")
    (limit "one step stands for all 16 reads: each pops one DWORD in order, and the 16th drains the frame — the intermediate reads add no new observation class"))
  (step (n 6) (insn "read rx_fifo_inf after the 16th data read")
    (writes (write (reg "rx_fifo_inf") (value "0x00000000")))
    (derivation "Status popped (step 4) and all 64 bytes drained (step 5): both used-space fields read 0 (§5.3.11).")
    (source "DS00002266B §5.3.11"))
  (step (n 7) (insn "negative: read the empty RX data FIFO once more; read int_sts")
    (writes (write (reg "int_sts") (value "bit14=1 (RXE)")))
    (derivation "Reading more data than the FIFOs report available is a host underrun (§3.13: 'The host must never read more data than what is available'), and a host underrun of the RX data FIFO asserts RXE (§3.13.5). The same section rules that regaining host synchronization after an underrun requires a soft reset — recorded as the consequence, outside this document's stimulus. Only the flag pins.")
    (source "DS00002266B §3.13, §3.13.5")))
