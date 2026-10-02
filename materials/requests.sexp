;; materials/requests.sexp — acquisition requests to chipdoc (the preferred channel —
;; the watcher fires on this file; docs/knowledge/the-chipdoc-request-channel.md is the
;; semulith-side summary of the protocol). Each request names its consumer: P5-BOARD.1's
;; board choice, per the 2026-10-01 design discussion "boards that touch the world"
;; (docs/tasks/P5-BOARD.md, Design Discussions) — a network-connected board needs its
;; network device to have PUBLIC register documentation, so the device dossier has a
;; source (the tree's own non-goal: no device without a source).
;;
;; Corpus survey before filing (the snapshotted feed, corpus 92a73b6 — measured, so
;; nothing already held is re-requested): the corpus ALREADY HOLDS a complete
;; register-level Ethernet MAC+PHY contract (TI-DP83816), ESP32/C3/S3 register maps
;; (SVD-ESPRESSIF), the SiFive FU540/FU740 manuals and HiFive board docs, and the TI
;; AM335x TRM (on-SoC CPSW Ethernet) — and its own note measures that no standalone
;; Cadence GEM / Synopsys DesignWare GMAC specification is public.
;;
;; ALL TEN ANSWERED `2026-10-01` (P5-BOARD.9): five FULFILLED — adopted into
;; materials/catalog.sexp with digests re-verified at fetch — and five BLOCKED, each a
;; MEASURED NEGATIVE (which routes were tried, what each returned). Answers arrive
;; per-request in chipdoc's catalog/responses.sexp; our statuses below stay `open`
;; until WE flip them — that is the protocol (CHANNEL.md §0.3), not silence. A blocked
;; answer is an answer: P5-BOARD.1 plans around it and it is never re-filed without a
;; new route.

(request
  (id "REQ-NET-LAN9118")
  (status resolved)
  (wanted "Microchip (SMSC) LAN9118 datasheet — the high-performance 10/100 Ethernet MAC+PHY with variable-voltage I/O (LAN9220 acceptable as the same family)")
  (why "P5-BOARD.1: a wired-NIC device dossier candidate with a simple public register contract; QEMU's lan9118 model is a potential second implementation for differential checking")
  (doc "LAN9118 datasheet (Microchip/SMSC)")
  (answer "FULFILLED 2026-10-01 from the official Microchip source (DS00002266B, 109 pp) — adopted as MICROCHIP-LAN9118, sha256 verified into the cache (scripts/materials.py --verify)")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-E1000")
  (status blocked)
  (wanted "Intel 82540EM Gigabit Ethernet Controller Software Developer's Manual (the e1000 device)")
  (why "P5-BOARD.1: QEMU's e1000 is the most-exercised emulated NIC in existence — the strongest oracle shape for a wired NIC dossier")
  (doc "Intel 82540EM Software Developer's Manual")
  (answer "BLOCKED 2026-10-01 (measured negative): intel.com/content/dam and /assets return HTTP 403 to automated clients, and the Wayback CDX index holds no archived copy of the 82540EM/8254x manual — consistent with the prior GAP-ETHERNET-MAC measurement. Consequence: the LAN9118 dossier is the acquired wired-NIC primary; do not re-file without a new route")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-RTL8139")
  (status blocked)
  (wanted "Realtek RTL8139C+/RTL8139D datasheet")
  (why "P5-BOARD.1: a third wired candidate — old, simple, fully documented, QEMU-modeled (rtl8139); three candidates let .1 pick on documentation quality and oracle availability, measured")
  (doc "Realtek RTL8139 datasheet")
  (answer "BLOCKED 2026-10-01 (measured negative): Realtek gates datasheets behind a captcha + submit-request flow (Download/SubmitDownloadRequest); the full RTL8139 datasheet is effectively NDA and not directly served")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-EC25")
  (status blocked)
  (wanted "Quectel EC25 AT Commands Manual (and its TCP/IP AT commands volume)")
  (why "P5-BOARD.1: the LTE modem-module route — the CPU-facing surface is a documented AT-command interface over UART/USB, so the wireless dossier rests on the module's public command manual, never the NDA baseband")
  (doc "Quectel EC25 AT Commands Manual")
  (answer "BLOCKED 2026-10-01 (measured negative): Quectel's download-zone redirects the EC25 document set to /login/ — an account is required, no direct PDF is served. Consequence: the SARA-R4 manual is the acquired LTE AT-command primary")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-SIM7600")
  (status blocked)
  (wanted "SIMCom SIM7600 series AT Command Manual")
  (why "P5-BOARD.1: a second LTE modem vendor — two vendors' AT manuals let the device dossier separate the documented contract from one vendor's dialect")
  (doc "SIMCom SIM7600 AT Command Manual")
  (answer "BLOCKED 2026-10-01 (measured negative): simcom.com product pages return 404 (site restructured); no public direct PDF and no Wayback snapshot located. Consequence: the SARA-R4 manual remains the cellular AT-command primary")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-SARA-R4")
  (status resolved)
  (wanted "u-blox SARA-R4 series AT Commands Manual")
  (why "P5-BOARD.1: a third modem vendor (LTE-M/NB-IoT); u-blox's public AT documentation is unusually complete")
  (doc "u-blox SARA-R4 AT Commands Manual")
  (answer "FULFILLED 2026-10-01 from a Wayback capture (20220121075106) of the official u-blox URL (UBX-17003787, 510 pp; the live URL 404s, content rehomed) — adopted as UBLOX-SARA-R4-AT, sha256 verified into the cache")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-ESP-AT")
  (status resolved)
  (wanted "Espressif ESP-AT User Guide — the AT firmware command set for ESP32 modules (WiFi)")
  (why "P5-BOARD.1: the WiFi-via-module route — the ESP32 runs ESP-AT firmware and presents a documented command surface; the corpus already holds the ESP32 register maps (SVD-ESPRESSIF), this is the missing command-layer document")
  (doc "ESP-AT User Guide (docs.espressif.com, PDF)")
  (answer "FULFILLED 2026-10-01 from docs.espressif.com (esp-at/en/latest/esp32, latest build, 533 pp) — adopted as ESPRESSIF-ESP-AT, sha256 verified into the cache")
  (updated "2026-10-01"))

(request
  (id "REQ-RFIC-NRF52840")
  (status resolved)
  (wanted "Nordic nRF52840 Product Specification (register-level documentation of the BLE/802.15.4 radio)")
  (why "P5-BOARD.1: the true-RFIC candidate — a radio whose register map is genuinely public, so an RFIC device model would have a primary source (most radios are NDA; this one is the measured exception)")
  (doc "nRF52840 Product Specification")
  (answer "FULFILLED 2026-10-01 from a Wayback capture (20240829095752) of the official infocenter URL (v1.7, 631 pp; the live URL returns HTTP 403, v1.9/v1.10 have no archived snapshot) — adopted as NORDIC-NRF52840-PS, sha256 verified into the cache")
  (updated "2026-10-01"))

(request
  (id "REQ-RFIC-AT86RF233")
  (status resolved)
  (wanted "Microchip (Atmel) AT86RF233 datasheet — the 802.15.4 transceiver")
  (why "P5-BOARD.1: a second register-documented radio, so the RFIC leg's evidence does not rest on one vendor")
  (doc "AT86RF233 datasheet")
  (answer "FULFILLED 2026-10-01 from the official Microchip source (Atmel-8351, 225 pp) — adopted as MICROCHIP-AT86RF233, sha256 verified into the cache")
  (updated "2026-10-01"))

(request
  (id "REQ-RFIC-AR9271-PROBE")
  (status blocked)
  (wanted "Atheros AR9271 / AR7010 (ath9k_htc family) register-level programming documentation — a PROBE: measure whether any public register-level WiFi baseband documentation exists at all (the open firmware 'openFW' and community driver knowledge are the fallback evidence)")
  (why "P5-BOARD.1: the one plausible exception to 'WiFi basebands are NDA'; if absent, record the measured negative honestly — the corpus already holds the same negative for Cadence GEM / DesignWare GMAC")
  (doc "any AR9271/AR7010 register-level programming document, or a measured negative")
  (answer "BLOCKED 2026-10-01 (measured negative — the probe's expected outcome, which IS the answer): no public register-level WiFi baseband programming documentation exists for AR9271/AR7010; Qualcomm/Atheros never published one and no Wayback snapshot exists. The open firmware (OpenFWWF) and the community ath9k_htc driver are the only public contract evidence")
  (updated "2026-10-01"))

;; ── Second batch (2026-10-02, MCU-DOCS.1): the MCU documentation set — the director's
;; 2026-10-02 steer ("ARMs as full documentations of MCUs, maybe others vendors too").
;; Consumer for all twelve: the steered MCU-modeling direction — documentation ahead of
;; an MCU milestone; no milestone owns MCU modeling yet, and that is stated, not hidden.
;; Corpus survey before filing (the LIVE feed, corpus c4ad8a2 working tree, read-only —
;; the snapshot was stale against it): HELD — ESP32/C3/S3 SVDs (SVD-ESPRESSIF),
;; RP2040/RP2350 SVDs (SVD-RASPBERRY-PI), nRF52840 PS (adopted at P5-BOARD.9), AM335x
;; TRM (a Cortex-A8 SoC, not an MCU), Arm PrimeCell TRMs + AMBA/GIC (Cortex-A/board
;; class); ABSENT — every Arm M-profile architecture manual, every Cortex-M TRM, and
;; every vendor MCU datasheet/RM beyond the held trio. The CMSIS-SVD format record is
;; the corpus's own tracked `wanted`, not ours to re-file.

(request
  (id "REQ-MCU-ARMV7M-ARM")
  (status resolved)
  (wanted "Armv7-M Architecture Reference Manual (the M-profile MCU architecture: Thumb-2, the exception model, NVIC, SysTick, the optional MPU)")
  (why "MCU-DOCS.1 (the 2026-10-02 MCU steer): the M-profile architecture is the core contract every Cortex-M3/M4-class MCU model is written against — the NVIC/SysTick/exception semantics are architecture, not vendor data")
  (doc "Armv7-M Architecture Reference Manual (Arm)")
  (answer "FULFILLED 2026-10-02 — DDI0403E.e (858 pp), already held corpus-side before the request; adopted as ARM-ARMV7M-DDI0403E, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-ARMV6M-ARM")
  (status resolved)
  (wanted "Armv6-M Architecture Reference Manual (the minimal M profile: Cortex-M0/M0+/M1)")
  (why "MCU-DOCS.1: the smallest MCU cores (incl. the RP2040's Cortex-M0+) run v6-M — the smallest honest MCU processor profile this project could model")
  (doc "Armv6-M Architecture Reference Manual (Arm)")
  (answer "FULFILLED 2026-10-02 — DDI0419E (374 pp), already held corpus-side before the request; adopted as ARM-ARMV6M-DDI0419E, sha256 verified into the cache (scripts/materials.py --fetch)")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-ARMV8M-ARM")
  (status resolved)
  (wanted "Armv8-M Architecture Reference Manual (mainline and baseline; TrustZone-M)")
  (why "MCU-DOCS.1: the current M-profile generation (Cortex-M23/M33/M55 class) — the forward-looking MCU architecture; v8-M mainline supersedes v7-M for new cores")
  (doc "Armv8-M Architecture Reference Manual (Arm)")
  (answer "FULFILLED 2026-10-02 — DDI0553B.z (2149 pp), already held corpus-side before the request; adopted as ARM-ARMV8M-DDI0553B, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-CORTEX-M3-TRM")
  (status resolved)
  (wanted "Arm Cortex-M3 Technical Reference Manual (the canonical v7-M MCU core)")
  (why "MCU-DOCS.1: the most-documented MCU core in history — a Cortex-M3 model has the QEMU lm3s/mps2 precedents as potential second implementations for differential checking")
  (doc "Cortex-M3 Technical Reference Manual (Arm)")
  (answer "FULFILLED 2026-10-02 from the Arm documentation-service API — DDI0337H r2p0 (133 pp); adopted as ARM-CORTEX-M3-DDI0337H, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-CORTEX-M0P-TRM")
  (status resolved)
  (wanted "Arm Cortex-M0+ Technical Reference Manual (the canonical v6-M core — the RP2040's)")
  (why "MCU-DOCS.1: pairs with the RP2040 datasheet request — the core TRM plus the SoC datasheet is the complete MCU documentation pair")
  (doc "Cortex-M0+ Technical Reference Manual (Arm)")
  (answer "FULFILLED 2026-10-02 from the Arm documentation-service API — DDI0484C r0p1 (51 pp); adopted as ARM-CORTEX-M0P-DDI0484C, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-CORTEX-M4-TRM")
  (status resolved)
  (wanted "Arm Cortex-M4 Technical Reference Manual (v7E-M: the DSP-extension and FP-extension MCU core class)")
  (why "MCU-DOCS.1: the most-deployed MCU core class (STM32F4, nRF52840 — whose PS the project already holds — i.MX RT); v7E-M adds the DSP/FP extensions to v7-M")
  (doc "Cortex-M4 Technical Reference Manual (Arm)")
  (answer "FULFILLED 2026-10-02 from the Arm documentation-service API — DDI0439B r0p0 (117 pp); adopted as ARM-CORTEX-M4-DDI0439B, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-RP2040-DS")
  (status resolved)
  (wanted "Raspberry Pi RP2040 datasheet (the prose companion to the corpus's held SVD register maps: dual Cortex-M0+, the PIO state machines, clocks, resets, DMA)")
  (why "MCU-DOCS.1: the best fully-public modern MCU documentation set — the SVD maps are already held (SVD-RASPBERRY-PI), the datasheet is the semantic half (what the registers DO, not just where they are)")
  (doc "RP2040 datasheet (Raspberry Pi)")
  (answer "FULFILLED 2026-10-02 — and measured REDUNDANT: the RP2040 datasheet (642 pp) was already held corpus-side AND adopted in this catalog as RP2040-DS since 2026-09-14 (same sha256, cached). The .1 survey measured the corpus's semulith-facing feed but not this catalog — the defect is recorded in docs/tasks/MCU-DOCS.md and the survey knowledge card; no duplicate record adopted")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-STM32-RM")
  (status resolved)
  (wanted "ST STM32 reference manual + the Cortex-M4 programming manual (RM0394-class RM for the peripheral register contracts; PM0214 for the core's vendor view)")
  (why "MCU-DOCS.1: the dominant MCU vendor line — ST publishes full reference manuals publicly; one representative RM measures the vendor-document class for this project")
  (doc "STM32 reference manual + PM0214 programming manual (ST)")
  (answer "FULFILLED 2026-10-02 from Wayback captures of the official st.com URLs — RM0394 (1600 pp) + PM0214 Rev 10 (262 pp), the RM + programming-manual pair as requested; adopted as ST-STM32L4-RM0394 and ST-STM32-CM4-PM0214, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-FE310")
  (status resolved)
  (wanted "SiFive FE310-G002 manual (the RISC-V MCU: E31 core, CLINT/PLIC, the peripheral set)")
  (why "MCU-DOCS.1: the RISC-V MCU — this project's own spine (the FU540/FU740 manuals are already held; the FE310 is the same vendor's microcontroller, and its CLINT/PLIC are the timer/IRQ contracts netboard-lab-v0 deliberately excludes)")
  (doc "SiFive FE310-G002 manual")
  (answer "FULFILLED 2026-10-02 from the SiFive CDN — FE310-G002 Manual v1p7 (122 pp; the corpus also holds the G003 manual and both datasheets); adopted as SIFIVE-FE310-G002, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-IMXRT-RM")
  (status resolved)
  (wanted "NXP i.MX RT1050 reference manual (the crossover MCU class: Cortex-M7 at 600 MHz)")
  (why "MCU-DOCS.1: NXP publishes full crossover-MCU reference manuals publicly (the DSP56300 Family Manual channel precedent); the crossover class is where MCU and application-processor documentation styles meet")
  (doc "i.MX RT1050 reference manual (NXP)")
  (answer "FULFILLED 2026-10-02 from a Wayback capture of the official NXP URL (the live URL 404s) — i.MX RT1050 RM Rev 0 (3355 pp); adopted as NXP-IMXRT1050RM, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-SAMD21-DS")
  (status resolved)
  (wanted "Microchip SAM D21 datasheet (the classic Cortex-M0+ vendor MCU)")
  (why "MCU-DOCS.1: Microchip/SMSC documentation is a measured-good channel (the LAN9118 acquisition, P5-BOARD.9); the SAM D21 is the classic public Cortex-M0+ vendor datasheet")
  (doc "SAM D21 datasheet (Microchip)")
  (answer "FULFILLED 2026-10-02 from a Wayback capture of ww1.microchip.com (the live URL 403s) — DS40001882 (1160 pp); adopted as MICROCHIP-SAMD21-DS40001882, sha256 verified into the cache")
  (updated "2026-10-02"))

(request
  (id "REQ-MCU-MSP430")
  (status resolved)
  (wanted "TI MSP430FR59xx family user's guide (the ultra-low-power MCU classic — a non-Arm ISA contrast)")
  (why "MCU-DOCS.1: the non-Arm MCU contrast — MSP430 is a distinct 16-bit architecture with full public documentation (the TI DP83816/AM335x channel precedent); a second ISA keeps the MCU direction honest about what is Arm-shaped and what is not")
  (doc "MSP430FR59xx family user's guide (TI)")
  (answer "FULFILLED 2026-10-02 directly from ti.com/lit — SLAU367P Rev P (1024 pp); adopted as TI-MSP430FR59XX-UG, sha256 verified into the cache")
  (updated "2026-10-02"))
