;; board.sexp — the canonical board definition of netboard-lab-v0 (P5-BOARD.1, 2026-10-02).
;; Validate: python3 scripts/check_sexp_schema.py profiles/netboard-lab-v0/board.sexp schema/board.sexp
;;
;; The first board: rv64i-lab-v0 v0 (the EXPERIMENTAL release — this board inherits that
;; status and every board claim reads as conditional on the CPU's acceptance trajectory)
;; plus exactly two devices, both digest-pinned in materials/catalog.sexp: the SiFive UART
;; (serial console; FU540-C000 v1p5 §13) and the LAN9118 wired NIC (PIO host bus — no
;; bus-master DMA, so every device effect reaches the guest through its own MMIO accesses,
;; exactly the shape the CPU contract's eight assumptions tolerate). Timers and interrupt
;; controllers are ABSENT BY CONTRACT — declared below, with the obligations they satisfy.
;; The narrative is DOSSIER.md; the composition verdict is .4's; generated maps are .3's.

(board
  (id "netboard-lab-v0")
  (version "0")
  (status experimental)

  (processor
    (unit "rv64i-lab-v0")
    (version "0")
    ;; the dossier content digest recorded in profiles/rv64i-lab-v0/GC-REPORT.md
    ;; (GATE-REPORT-gated): unit id + version + digest is the pin, not the name.
    (dossier-sha256 "1879ba1881038ec460ed059343743c1187e2c8960ee347e496596a2aee5394ad")
    (contract "rv64i-lab-env-v0")
    (contract-version "0"))

  (device
    (id "uart0")
    (unit "sifive-uart-lab-v0")
    (comment "the device UNIT id is declared here; P5-BOARD.2 owns its dossier")
    (kind sifive-uart)
    (material "SIFIVE-FU540-C000")
    (revision "v1p5")
    (sha256 "5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c")
    (access-widths 32)
    (comment "FU540-C000 v1p5 §13.3: the UART memory map is designed to require only"
             "naturally aligned 32-bit memory accesses")
    (interrupt unconnected)
    (backend
      (rx recorded-input)
      (tx host-console)
      (live-host-socket laboratory-only)))

  (device
    (id "eth0")
    (unit "lan9118-lab-v0")
    (comment "the device UNIT id is declared here; P5-BOARD.2 owns its dossier")
    (kind lan9118)
    (material "MICROCHIP-LAN9118")
    (revision "DS00002266B 2018-11-30")
    (sha256 "72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee")
    (access-widths 16)
    (access-widths 32)
    (comment "DS00002266B §1.10: the host bus interface supports 32-bit and 16-bit bus"
             "transfers; programmed I/O only — no bus-master DMA")
    (interrupt unconnected)
    (backend
      (rx recorded-trace-replay)
      (tx recording-sink)
      (live-host-socket laboratory-only)))

  (memory-map
    (region
      (name "ram0")
      (base "0x8000_0000")
      (size "0x8000_0000")
      (kind ram)
      (executable true))
    (region
      (name "uart0")
      (base "0x1001_0000")
      (size "0x1000")
      (kind mmio)
      (executable false)
      (device "uart0"))
    (region
      (name "eth0")
      (base "0x1002_0000")
      (size "0x100")
      (kind mmio)
      (executable false)
      (device "eth0")))

  (reset
    (kinds cold)
    (entry "the loaded image's entry address — rv64i-lab-env-v0 v0, OB-ENV-RESET")
    (retained-state none)
    (satisfies "OB-ENV-RESET"))

  (timers
    (present false)
    (reason "rv64i-lab-env-v0 v0 excludes every guest-reachable time source — no CSR counter AND no memory-mapped one (OB-ENV-VIRTUAL-TIME, both halves required). A timer device here would not be a feature; it would falsify the composition (ENV-02).")
    (comment "without a time source, NIC receive delivery is pinned to the guest's own"
             "polling: the device holds the next recorded packet and offers it when"
             "polled, so the harness's retired-instruction count never becomes"
             "target-visible")
    (satisfies "OB-ENV-VIRTUAL-TIME"))

  (interrupt-controller
    (present false)
    (reason "rv64i-lab-env-v0 v0 admits synchronous exceptions and requested traps only — no asynchronous interrupt is deliverable (OB-ENV-EVENT-DELIVERY), and the absence must be a platform property to be real. Both devices' interrupt lines are therefore unconnected AND DECLARED so; drivers poll.")
    (satisfies "OB-ENV-EVENT-DELIVERY"))

  (serial-console
    (device "uart0"))

  (decision
    (id "D-BOARD-SCOPE")
    (authority laboratory)
    (statement "The board composes rv64i-lab-v0 v0 with exactly two devices — the SiFive UART (serial console) and the LAN9118 wired NIC — and nothing else: memory, reset, serial console present; timers and interrupt controllers absent by contract.")
    (source "P5-BOARD design brief, 2026-10-02 (docs/tasks/P5-BOARD.md, Decisions)"))

  (decision
    (id "D-BOARD-STATUS")
    (authority laboratory)
    (statement "The board is EXPERIMENTAL: it inherits the status of its processor (rv64i-lab-v0 v0, the EXPERIMENTAL release) and every board claim reads as conditional on the CPU's own acceptance trajectory. The composition can never outrank its processor.")
    (source "P5-BOARD tree, Blockers (2026-10-02); ROADMAP.md §P5"))

  (decision
    (id "D-BOARD-NO-TIMER-IRQ")
    (authority execution-environment)
    (statement "No timer and no interrupt controller is modelled. OB-ENV-VIRTUAL-TIME and OB-ENV-EVENT-DELIVERY are environment assumptions the board must satisfy, so a CLINT or PLIC would be a composition REJECTION (P5-BOARD.4's verdict), not a feature. Both devices' interrupt lines are unconnected and declared so; drivers poll.")
    (source "profiles/rv64i-lab-v0/ENVIRONMENT.md; docs/CPU_ENVIRONMENT.md §5 (ENV-02)"))

  (decision
    (id "D-BOARD-ACCESS-POLICY")
    (authority laboratory)
    (statement "An MMIO access honours exactly the widths the device's datasheet defines (declared per device in access-widths); any other width is a board-reported contract violation, never silently serviced. A misaligned MMIO access never reaches a device: the CPU raises AlignmentException first (OB-MISALIGN-DATA).")
    (source "FU540-C000 v1p5 §13.3; DS00002266B §1.10; profiles/rv64i-lab-v0/ENVIRONMENT.md (OB-ENV-ACCESS-WIDTHS)"))

  (decision
    (id "D-BOARD-FETCH")
    (authority laboratory)
    (statement "Instruction fetch is served from RAM only: every MMIO region is declared non-executable, so no fetch can reach a device and no fetch has a side effect (OB-ENV-FETCH-SUPPLY).")
    (source "profiles/rv64i-lab-v0/ENVIRONMENT.md (OB-ENV-FETCH-SUPPLY)"))

  (decision
    (id "D-BOARD-NET-BACKEND")
    (authority laboratory)
    (statement "The network backend is recorded-trace replay on receive (deterministic, evidence-grade, re-runnable in a fresh clone) and a recording sink on transmit. A live host-socket backend stays laboratory play at the Environment boundary and may never enter an evidence claim.")
    (source "P5-BOARD design brief, 2026-10-02; the 2026-10-01 design discussion (docs/tasks/P5-BOARD.md)"))

  (decision
    (id "D-BOARD-UART-KIND")
    (authority laboratory)
    (statement "The serial device is the SiFive UART documented in FU540-C000 v1p5 §13 — txdata/rxdata/txctrl/rxctrl/ie/ip/div, 8-entry FIFOs, naturally aligned 32-bit accesses — not a 16550. The design brief's '16550-compatible' label was measured false against the pinned source (zero occurrences of '16550' in FU540-C000 v1p5); the source pin, not the label, was the intent, and the label is corrected wherever it was recorded.")
    (source "FU540-C000 v1p5 §13 (measured 2026-10-02: pdftotext census of the pinned artifact)"))

  (decision
    (id "D-BOARD-MEMORY-MAP")
    (authority laboratory)
    (statement "RAM is 2 GiB at 0x8000_0000 — the laboratory harness's existing load base and size (crates/semulith-cli DEFAULT_BASE/DEFAULT_SIZE), so a guest built for the laboratory runs unchanged on the board. uart0 sits at 0x1001_0000, the FU540-C000 UART0 instance address (Table 58). eth0 sits at 0x1002_0000 with a 256-byte window, the LAN9118 direct register map span (DS00002266B Table 5-1: offsets 0x00–0xFC).")
    (source "crates/semulith-cli/src/main.rs; FU540-C000 v1p5 Table 58; DS00002266B Table 5-1")))
