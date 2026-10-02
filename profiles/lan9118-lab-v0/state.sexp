;; state.sexp — the device-state document for `lan9118-lab-v0` (P5-BOARD.10, 2026-10-02).
;; Validate:
;;   python3 scripts/check_sexp_schema.py profiles/lan9118-lab-v0/state.sexp schema/state.sexp
;; A device has no XLEN and no integer file (the P3-BREADTH.5 optionals); its architectural
;; state is the 24 direct CSRs, the 12 indexed MAC CSRs, the 13 doubly-indexed PHY
;; registers and the four host-accessible FIFOs, and the census below earns the "and
;; nothing else the MMIO boundary can reach" claim. gen_state.py is rv64i-only by
;; construction (STATE-GEN) — this document is decided by DOSSIER-SCHEMA and
;; PROFILE-CONSISTENCY, never fed to the generator. Strap-determined and datasheet-blank
;; reset values are recorded as such, never guessed (REQ-D-NIC-STRAP-RESETS,
;; REQ-D-NIC-PHY-ID).

(state (profile_id "lan9118-lab-v0")
  (note "Device state at the MMIO boundary: the 24 direct 32-bit CSRs at 50h–B4h, the 12 MAC CSRs indexed through MAC_CSR_CMD/DATA, the 13 16-bit PHY registers indexed through MII_ACC/MII_DATA, and the four FIFOs. The FIFO PORTS (00h–4Ch) are access windows, not state — the state is the FIFOs themselves. Strap-dependent resets (HW_CFG bit 2, PHY 0.13/0.12, PHY 4.8/7/6/5, PHY 31.4:2) record the strap, not a guess (REQ-D-NIC-STRAP-RESETS); the time-source registers (free_run, gpt_cnt) carry the composition's frozen disposition (REQ-D-NIC-TIME-SOURCES).")

  ;; ── the 24 direct CSRs (50h–B4h) ─────────────────────────────────────────────
  (special_registers
    (register (id "id_rev") (width_bits 32) (holds "Chip ID 0118h [31:16], Chip Revision 0001h [15:0] — read-only identity") (authority architecture) (source "DS00002266B §5.3.1") (reset "0x01180001") (reset_authority architecture)))
  (special_registers
    (register (id "irq_cfg") (width_bits 32) (holds "INT_DEAS [31:24] (10 µs units), INT_DEAS_CLR [14] SC, INT_DEAS_STS [13] RO, IRQ_INT [12] RO, IRQ_EN [8], IRQ_POL [4] NASR, IRQ_TYPE [0] NASR") (authority architecture) (source "DS00002266B §5.3.2") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "int_sts") (width_bits 32) (holds "the 20 interrupt status bits (SW_INT…GPIO0), R/WC except PHY_INT [18] RO") (authority architecture) (source "DS00002266B §5.3.3") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "int_en") (width_bits 32) (holds "the per-source IRQ masks at INT_STS's bit positions") (authority architecture) (source "DS00002266B §5.3.4") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "byte_test") (width_bits 32) (holds "read-only byte-order constant; a write of any data is the wake-up from D1/D2") (authority architecture) (source "DS00002266B §5.3.5, §3.10.2") (reset "0x87654321") (reset_authority architecture)))
  (special_registers
    (register (id "fifo_int") (width_bits 32) (holds "TX Data Available Level [31:24] (64-byte blocks), TX Status Level [23:16] (DWORDs), RX Status Level [7:0] (DWORDs)") (authority architecture) (source "DS00002266B §5.3.6") (reset "0x48000000") (reset_authority architecture)))
  (special_registers
    (register (id "rx_cfg") (width_bits 32) (holds "RX End Alignment [31:30], RX_DMA_CNT [27:16] (decrementing), RX_DUMP [15] SC, RXDOFF [12:8]") (authority architecture) (source "DS00002266B §5.3.7") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "tx_cfg") (width_bits 32) (holds "TXS_DUMP [15] SC, TXD_DUMP [14] SC, TXSAO [2], TX_ON [1] (auto-cleared on stop), STOP_TX [0] SC") (authority architecture) (source "DS00002266B §5.3.8") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "hw_cfg") (width_bits 32) (holds "MBO [20] must-be-one, TX_FIF_SZ [19:16], D32/nD16 strap [2] RO, SRST_TO [1] RO, SRST [0] SC") (authority architecture) (source "DS00002266B §5.3.9") (reset "0x00050000 with bit 2 = the D32/nD16 strap value (REQ-D-NIC-STRAP-RESETS)") (reset_authority architecture)))
  (special_registers
    (register (id "rx_dp_ctl") (width_bits 32) (holds "RX_FFWD [31] — RX data FIFO fast-forward, holds high until complete") (authority architecture) (source "DS00002266B §5.3.10") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "rx_fifo_inf") (width_bits 32) (holds "RXSUSED [23:16] (DWORDs), RXDUSED [15:0] (bytes, DWORD-rounded per frame) — read-only") (authority architecture) (source "DS00002266B §5.3.11") (reset "0x00000000 — pins the RX FIFOs empty at reset") (reset_authority architecture)))
  (special_registers
    (register (id "tx_fifo_inf") (width_bits 32) (holds "TXSUSED [23:16] (DWORDs), TDFREE [15:0] (bytes free) — read-only") (authority architecture) (source "DS00002266B §5.3.12") (reset "0x00001200 — TDFREE 4608, the default allocation's whole TX data FIFO") (reset_authority architecture)))
  (special_registers
    (register (id "pmt_ctrl") (width_bits 32) (holds "PM_MODE [13:12], PHY_RST [10] SC, WOL_EN [9], ED_EN [8], PME_TYPE [6] NASR, WUPS [5:4] R/WC, PME_IND [3], PME_POL [2] NASR, PME_EN [1], READY [0] RO") (authority architecture) (source "DS00002266B §5.3.13") (reset "0x00000000 — READY (bit 0) reads 0 until the reset/power-up completes (§5.3.13, §3.11.1)") (reset_authority architecture)))
  (special_registers
    (register (id "gpio_cfg") (width_bits 32) (holds "LEDx_EN [30:28], GPIO_INT_POL [26:24], EEPR_EN [22:20], GPIOBUFn [18:16], GPDIRn [10:8], GPODn [4:3], GPIODn [2:0]") (authority architecture) (source "DS00002266B §5.3.14") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "gpt_cfg") (width_bits 32) (holds "TIMER_EN [29], GPT_LOAD [15:0] — the 100 µs GP timer control") (authority architecture) (source "DS00002266B §5.3.15, §3.8") (reset "0x0000FFFF") (reset_authority architecture)))
  (special_registers
    (register (id "gpt_cnt") (width_bits 32) (holds "GPT_CNT [15:0] RO — the current GP timer count; a guest-readable time source, frozen by the composition (REQ-D-NIC-TIME-SOURCES)") (authority architecture) (source "DS00002266B §5.3.16, §3.8") (reset "0x0000FFFF") (reset_authority architecture)))
  (special_registers
    (register (id "word_swap") (width_bits 32) (holds "16-bit-mode word-lane mapping (FFFFFFFFh reverses); NASR") (authority architecture) (source "DS00002266B §5.3.17") (reset "0x00000000 (NASR — unaffected by software reset)") (reset_authority architecture)))
  (special_registers
    (register (id "free_run") (width_bits 32) (holds "FR_CNT [31:0] RO — the free-running 25 MHz counter; a guest-readable time source, frozen by the composition (REQ-D-NIC-TIME-SOURCES)") (authority architecture) (source "DS00002266B §5.3.18") (reset "starts at zero at reset, then increments every 25 MHz cycle (up to 160 ns to clear) — the datasheet pins the behaviour, not a readable value") (reset_authority architecture)))
  (special_registers
    (register (id "rx_drop") (width_bits 32) (holds "RX_DFC [31:0] — dropped-frame counter, cleared on ANY read (RC)") (authority architecture) (source "DS00002266B §5.3.19") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "mac_csr_cmd") (width_bits 32) (holds "CSR Busy [31] SC, R/nW [30], CSR Address [7:0] — the MAC CSR synchronizer command") (authority architecture) (source "DS00002266B §5.3.20") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "mac_csr_data") (width_bits 32) (holds "the MAC CSR synchronizer data") (authority architecture) (source "DS00002266B §5.3.21") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "afc_cfg") (width_bits 32) (holds "AFC_HI [23:16], AFC_LO [15:8] (64-byte multiples), BACK_DUR [7:4], FCMULT/FCBRD/FCADD/FCANY [3:0]") (authority architecture) (source "DS00002266B §5.3.22") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "e2p_cmd") (width_bits 32) (holds "EPC Busy [31] SC, EPC command [30:28], EPC Time-out [9] R/WC, MAC Address Loaded [8] RO, EPC Address [7:0]") (authority architecture) (source "DS00002266B §5.3.23") (reset "0x00000000 — except EPC Busy (bit 31) reads 1 until the post-reset EEPROM auto-load attempt completes (§5.3.23 note)") (reset_authority architecture)))
  (special_registers
    (register (id "e2p_data") (width_bits 32) (holds "EEPROM data byte [7:0]") (authority architecture) (source "DS00002266B §5.3.24") (reset "0x00000000") (reset_authority architecture)))

  ;; ── the 12 MAC CSRs (indexed through mac_csr_cmd/mac_csr_data, Table 5-6) ────
  (special_registers
    (register (id "mac_cr") (width_bits 32) (holds "MAC CSR 1: RXALL [31], RCVOWN [23], LOOPBK [21], FDPX [20], MCPAS [19], PRMS [18], INVFILT [17], PASSBAD [16], HO [15], HPFILT [13], LCOLL [12], BCAST [11], DISRTY [10], PADSTR [8], BOLMT [7:6], DFCHK [5], TXEN [3], RXEN [2]") (authority architecture) (source "DS00002266B §5.4.1") (reset "0x00040000 (PRMS set out of reset — Table 5-6 and §5.4.1's header agree)") (reset_authority architecture)))
  (special_registers
    (register (id "addrh") (width_bits 32) (holds "MAC CSR 2: physical address bits [47:32] in [15:0]") (authority architecture) (source "DS00002266B §5.4.2") (reset "0x0000FFFF per Table 5-6 — 'undefined until loaded from the EEPROM at power-on' (§5.4.2); no EEPROM on this board, so the host programs it (REQ-D-NIC-EEPROM-AUTOLOAD)") (reset_authority architecture)))
  (special_registers
    (register (id "addrl") (width_bits 32) (holds "MAC CSR 3: physical address bits [31:0]") (authority architecture) (source "DS00002266B §5.4.3") (reset "0xFFFFFFFF per Table 5-6 — 'undefined until loaded from the EEPROM at power-on' (§5.4.3)") (reset_authority architecture)))
  (special_registers
    (register (id "hashh") (width_bits 32) (holds "MAC CSR 4: upper 32 bits of the 64-bit multicast hash table") (authority architecture) (source "DS00002266B §5.4.4") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "hashl") (width_bits 32) (holds "MAC CSR 5: lower 32 bits of the multicast hash table") (authority architecture) (source "DS00002266B §5.4.5") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "mii_acc") (width_bits 32) (holds "MAC CSR 6: PHY Address [15:11] (must be 00001b), MIIRINDA [10:6], MIIWnR [1], MIIBZY [0]") (authority architecture) (source "DS00002266B §5.4.6") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "mii_data") (width_bits 32) (holds "MAC CSR 7: the 16-bit MII read/write data in [15:0]") (authority architecture) (source "DS00002266B §5.4.7") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "flow") (width_bits 32) (holds "MAC CSR 8: FCPT [31:16], FCPASS [2], FCEN [1], FCBSY [0]") (authority architecture) (source "DS00002266B §5.4.8") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "vlan1") (width_bits 32) (holds "MAC CSR 9: VLAN1 tag identifier VTI1 [15:0] (8100h if used)") (authority architecture) (source "DS00002266B §5.4.9") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "vlan2") (width_bits 32) (holds "MAC CSR A: VLAN2 tag identifier VTI2 [15:0]") (authority architecture) (source "DS00002266B §5.4.10") (reset "0x00000000") (reset_authority architecture)))
  (special_registers
    (register (id "wuff") (width_bits 32) (holds "MAC CSR B: wake-up frame filter, WRITE-ONLY — eight sequential DWORD writes load filter byte masks 0–7, then the internal pointer wraps") (authority architecture) (source "DS00002266B §5.4.11") (reset "0x00000000 (Table 5-6); the internal load pointer restarts at filter 0 on any reset (§5.4.11)") (reset_authority architecture)))
  (special_registers
    (register (id "wucsr") (width_bits 32) (holds "MAC CSR C: GUE [9], WUFR [6], MPR [5], WUEN [2], MPEN [1]") (authority architecture) (source "DS00002266B §5.4.12") (reset "0x00000000") (reset_authority architecture)))

  ;; ── the 13 PHY registers (16-bit, indexed through mii_acc/mii_data, Table 5-8) ──
  (special_registers
    (register (id "phy_basic_control") (width_bits 16) (holds "PHY 0: Reset [15] SC, Loopback [14], Speed Select [13], Auto-Negotiation Enable [12], Power Down [11], Restart Auto-Negotiate [9] SC, Duplex Mode [8], Collision Test [7]") (authority architecture) (source "DS00002266B §5.5.1") (reset "bits 13/12 = the SPEED_SEL strap (Note 5-1, Table 2-2), all other defined bits 0 (REQ-D-NIC-STRAP-RESETS)") (reset_authority architecture)))
  (special_registers
    (register (id "phy_basic_status") (width_bits 16) (holds "PHY 1: fixed ability bits (100Base-TX FD/HD, 10Base-T FD/HD, Auto-Negotiate Ability, Extended Capabilities = 1; 100Base-T4 = 0), Auto-Negotiate Complete [5], Remote Fault [4] LH, Link Status [2] LL, Jabber Detect [1] LH") (authority architecture) (source "DS00002266B §5.5.2") (reset "per-bit defaults compose 0x7809 with the transient bits (5/4/2/1) clear; the wire-domain bits' post-reset evolution is the replay scene's (REQ-D-NIC-PHY-LINK)") (reset_authority architecture)))
  (special_registers
    (register (id "phy_id1") (width_bits 16) (holds "PHY 2: OUI bits 3–18") (authority architecture) (source "DS00002266B §5.5.3") (reset "0x0007") (reset_authority architecture)))
  (special_registers
    (register (id "phy_id2") (width_bits 16) (holds "PHY 3: OUI bits 19–24 in [15:10], model number [9:4], revision [3:0]") (authority architecture) (source "DS00002266B §5.5.4") (reset "0xC0D1 in bits 15:10; the model/revision nibbles are blank in the datasheet (REQ-D-NIC-PHY-ID) — not pinned") (reset_authority architecture)))
  (special_registers
    (register (id "phy_an_advertisement") (width_bits 16) (holds "PHY 4: Remote Fault [13], Pause Operation [11:10], 100Base-TX FD [8], 100Base-TX [7], 10Base-T FD [6], 10Base-T [5], Selector [4:0]") (authority architecture) (source "DS00002266B §5.5.5") (reset "0x0081 with bits 8/6/5 strap-determined (Note 5-3) — bit 7 fixed 1, selector 00001b") (reset_authority architecture)))
  (special_registers
    (register (id "phy_an_lp_ability") (width_bits 16) (holds "PHY 5: the link partner's advertised abilities; no next-page support") (authority architecture) (source "DS00002266B §5.5.6") (reset "0x0001 per the per-bit defaults (selector 00001b, Acknowledge 'will always read 0'); the partner content is wire-domain (REQ-D-NIC-PHY-LINK)") (reset_authority architecture)))
  (special_registers
    (register (id "phy_an_expansion") (width_bits 16) (holds "PHY 6: Parallel Detection Fault [4] LH, Link Partner Next Page Able [3], Next Page Able [2] (0), Page Received [1] LH, Link Partner Auto-Negotiation Able [0]") (authority architecture) (source "DS00002266B §5.5.7") (reset "0x0000") (reset_authority architecture)))
  (special_registers
    (register (id "phy_mode_control_status") (width_bits 16) (holds "PHY 17: EDPWRDOWN [13], ENERGYON [1]") (authority architecture) (source "DS00002266B §5.5.8") (reset "0x0002 — ENERGYON resets to 1 by hardware reset, unaffected by software reset (§5.5.8)") (reset_authority architecture)))
  (special_registers
    (register (id "phy_special_modes") (width_bits 16) (holds "PHY 18: MODE [7:5] (Table 5-9), PHYAD [4:0] = 00001b — NASR") (authority architecture) (source "DS00002266B §5.5.9, Table 5-9") (reset "NASR; PHYAD 00001b, MODE per Table 5-9's strap-linked defaults (REQ-D-NIC-STRAP-RESETS)") (reset_authority architecture)))
  (special_registers
    (register (id "phy_special_indications") (width_bits 16) (holds "PHY 27: VCOOFF_LP [10], XPOL [4] RO, [3:0] read-only 1011b") (authority architecture) (source "DS00002266B §5.5.10") (reset "0x000B (bits 3:0 fixed 1011b)") (reset_authority architecture)))
  (special_registers
    (register (id "phy_interrupt_source") (width_bits 16) (holds "PHY 29: INT7–INT1 source flags [7:1], latch-high") (authority architecture) (source "DS00002266B §5.5.11") (reset "0x0000") (reset_authority architecture)))
  (special_registers
    (register (id "phy_interrupt_mask") (width_bits 16) (holds "PHY 30: the per-source interrupt masks [7:0]") (authority architecture) (source "DS00002266B §5.5.12") (reset "0x0000") (reset_authority architecture)))
  (special_registers
    (register (id "phy_special_control_status") (width_bits 16) (holds "PHY 31: Autodone [12] RO, HCDSPEED [4:2] RO speed indication") (authority architecture) (source "DS00002266B §5.5.13") (reset "bits 11:5 written 0000010b; HCDSPEED strap-determined (Note 5-4, Table 2-2) (REQ-D-NIC-STRAP-RESETS)") (reset_authority architecture)))

  ;; ── the four host-accessible FIFOs (the ports at 00h–4Ch are their windows) ──
  (register_family (id "rx_data_fifo") (count 2640) (width_bits 32) (ids "rx_data_fifo DWORDs (default allocation: 10560 B at TX_FIF_SZ = 5; size follows HW_CFG, Table 5-3)") (authority architecture) (source "DS00002266B §5.2.1, §5.3.9.1, Table 5-3")
    (comment "destructive-read-only behind the 00h–1Ch aliases; each frame counted DWORD-rounded in RXDUSED. Considered full 4 DWORDs before the configured length (§5.3.9.1 note).")
    (reset (value "occupancy empty") (authority architecture) (source "DS00002266B §5.3.11 (RX_FIFO_INF resets to 0 — the occupancy counters' stated resets pin the FIFOs empty; REQ-D-NIC-FIFO-INF)") (statement "The INF registers' stated resets pin occupancy to empty at reset; the contents themselves are never separately stated and are moot once empty — the measured contrast with the UART dossier's FIFO-RESET silence.")))
  (register_family (id "tx_data_fifo") (count 1152) (width_bits 32) (ids "tx_data_fifo DWORDs (default allocation: 4608 B at TX_FIF_SZ = 5; holds TX commands and payload)") (authority architecture) (source "DS00002266B §5.2.2, §5.3.9.1, Table 5-3")
    (comment "write-only behind the 20h–3Ch aliases; consumption follows §3.12.5's accounting (command A always, command B on First Segment, DWORD-whole offsets/padding stripped).")
    (reset (value "occupancy empty") (authority architecture) (source "DS00002266B §5.3.12 (TDFREE resets to 1200h = the full 4608-byte allocation)") (statement "TDFREE's stated reset pins the TX data FIFO empty at reset.")))
  (register_family (id "rx_status_fifo") (count 176) (width_bits 32) (ids "rx_status_fifo DWORDs (default: 704 B = RX allocation / 16)") (authority architecture) (source "DS00002266B §5.2.1, §5.3.9.1, §3.13.3")
    (comment "one status word per received frame (§3.13.3's format); pop at 40h, non-destructive PEEK at 44h.")
    (reset (value "occupancy empty") (authority architecture) (source "DS00002266B §5.3.11 (RXSUSED resets to 0)") (statement "RXSUSED's stated reset pins the RX status FIFO empty at reset.")))
  (register_family (id "tx_status_fifo") (count 128) (width_bits 32) (ids "tx_status_fifo DWORDs (fixed 512 B)") (authority architecture) (source "DS00002266B §5.2.2, §5.3.9.1, §3.12.4")
    (comment "one status word per transmitted packet (§3.12.4's format); pop at 48h, non-destructive PEEK at 4Ch; a full status FIFO suspends transmission unless TXSAO.")
    (reset (value "occupancy empty") (authority architecture) (source "DS00002266B §5.3.12 (TXSUSED resets to 0)") (statement "TXSUSED's stated reset pins the TX status FIFO empty at reset.")))

  (hidden_state_census
    (question "What state beyond the 49 MMIO registers must the model carry to reproduce every MMIO-visible behaviour of the LAN9118 — and which hardware state is unreachable at the MMIO boundary? (SEM-08, catalog C02, asked of a device)")
    (answer "The four FIFOs' contents and occupancies, the TX command-parser state, and the counter values the composition freezes — and nothing else. Every other hardware state the datasheet implies is either register-carried (the synchronizer busy bits, the dump/fast-forward self-clearing bits) or invisible at the MMIO boundary: the MIL FIFOs are 'not visible to the host processor' by the datasheet's own words, and the wire-domain machines (PHY link training, auto-negotiation, the analog front end) surface only through PHY register bits whose scene the replay backend declares (REQ-D-NIC-PHY-LINK).")
    (candidates
      (checked (candidate "the four host FIFOs' contents and occupancies") (present true) (why "MMIO-visible: the data/status ports move their contents and the INF registers report occupancy — the model must carry them.")))
    (candidates
      (checked (candidate "TX command-parser state (the current buffer's command A/B, the cumulative packet byte count for the TXE length check)") (present true) (why "MMIO-visible through its verdicts: TXE asserts exactly when the cumulative count and Packet Length disagree (§3.12.7), and TDFREE's accounting (§3.12.5) depends on the parse — the model must carry the parse to reproduce both.")))
    (candidates
      (checked (candidate "16-bit-mode pairing latch (the first half of a DWORD transfer held until the second arrives)") (present false) (why "censused present while board.sexp declared 16-bit accesses; the .4 verdict straps D32 (32-bit native mode, D-BOARD-NIC-STRAPS) — §3.6's two-contiguous-accesses rule is 16-bit-mode operation, and a 16-bit access never reaches the device on this board (REQ-D-NIC-WIDTH + D-BOARD-ACCESS-POLICY), so no pending half is observable.")))
    (candidates
      (checked (candidate "FREE_RUN / GPT counter values and the INT_DEAS interval counter") (present true) (why "MMIO-readable (9Ch, 90h, IRQ_CFG bit 13) — carried, but frozen or guest-deterministic per REQ-D-NIC-TIME-SOURCES: never wall-clock, never the retired-instruction count.")))
    (candidates
      (checked (candidate "MIL FIFOs (2 KB TX, 128 B RX) and their pointers") (present false) (why "§5.3.9.1: 'RX and TX MIL FIFO levels are not visible to the host processor' and the data/status FIFO levels 'do not take into consideration the MIL FIFOs' — unreachable at MMIO by the datasheet's own statement.")))
    (candidates
      (checked (candidate "PHY wire-domain state machines (auto-negotiation progress, link training, polarity detection, the analog front end)") (present false) (why "surface only as PHY register bits; on this board the wire is the recorded-trace replay backend, so the scene is declared, not simulated (REQ-D-NIC-PHY-LINK, D-BOARD-NET-BACKEND).")))
    (candidates
      (checked (candidate "EEPROM contents and the EPC state machine") (present false) (why "the board wires no EEPROM (board.sexp); the auto-load's defined absent path ends initialization (§3.9.1) and the controller's observable state (EPC Busy, Time-out, Loaded) is register-carried.")))
    (candidates
      (checked (candidate "WUFF internal load pointer") (present false) (why "WUFF is write-only with no MMIO-readable effect; its sequencing is observable only in the wire domain (wake-up detection), which the replay backend owns.")))
    (candidates
      (checked (candidate "25 MHz reference phase, PLL lock state, GPIO pin levels") (present false) (why "no MMIO readout of the clocks exists except through FREE_RUN (dispositioned); pin levels are the composition's declared tie-offs (REQ-D-NIC-GPIO-PINS), not device state.")))
    (consequence "The model state is exactly: the 49 registers, the four FIFOs with occupancies, and the TX command-parser state — with free_run/gpt_cnt/int_deas carried but frozen by the composition. A cold reset (the board's only kind, D-BOARD-RESET — POR/nRESET semantics) establishes every stated reset above, latches the straps (the composition's declared values), runs the EEPROM auto-load's absent path (EPC Busy high until the attempt completes, MAC Address Loaded clear), and leaves the strap-determined and blank nibbles to their recorded dispositions; no hidden register may appear in the implementation without this census changing.")))
