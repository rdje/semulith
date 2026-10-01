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

(request
  (id "REQ-NET-LAN9118")
  (status open)
  (wanted "Microchip (SMSC) LAN9118 datasheet — the high-performance 10/100 Ethernet MAC+PHY with variable-voltage I/O (LAN9220 acceptable as the same family)")
  (why "P5-BOARD.1: a wired-NIC device dossier candidate with a simple public register contract; QEMU's lan9118 model is a potential second implementation for differential checking")
  (doc "LAN9118 datasheet (Microchip/SMSC)")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-E1000")
  (status open)
  (wanted "Intel 82540EM Gigabit Ethernet Controller Software Developer's Manual (the e1000 device)")
  (why "P5-BOARD.1: QEMU's e1000 is the most-exercised emulated NIC in existence — the strongest oracle shape for a wired NIC dossier")
  (doc "Intel 82540EM Software Developer's Manual")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-RTL8139")
  (status open)
  (wanted "Realtek RTL8139C+/RTL8139D datasheet")
  (why "P5-BOARD.1: a third wired candidate — old, simple, fully documented, QEMU-modeled (rtl8139); three candidates let .1 pick on documentation quality and oracle availability, measured")
  (doc "Realtek RTL8139 datasheet")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-EC25")
  (status open)
  (wanted "Quectel EC25 AT Commands Manual (and its TCP/IP AT commands volume)")
  (why "P5-BOARD.1: the LTE modem-module route — the CPU-facing surface is a documented AT-command interface over UART/USB, so the wireless dossier rests on the module's public command manual, never the NDA baseband")
  (doc "Quectel EC25 AT Commands Manual")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-SIM7600")
  (status open)
  (wanted "SIMCom SIM7600 series AT Command Manual")
  (why "P5-BOARD.1: a second LTE modem vendor — two vendors' AT manuals let the device dossier separate the documented contract from one vendor's dialect")
  (doc "SIMCom SIM7600 AT Command Manual")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-SARA-R4")
  (status open)
  (wanted "u-blox SARA-R4 series AT Commands Manual")
  (why "P5-BOARD.1: a third modem vendor (LTE-M/NB-IoT); u-blox's public AT documentation is unusually complete")
  (doc "u-blox SARA-R4 AT Commands Manual")
  (updated "2026-10-01"))

(request
  (id "REQ-NET-ESP-AT")
  (status open)
  (wanted "Espressif ESP-AT User Guide — the AT firmware command set for ESP32 modules (WiFi)")
  (why "P5-BOARD.1: the WiFi-via-module route — the ESP32 runs ESP-AT firmware and presents a documented command surface; the corpus already holds the ESP32 register maps (SVD-ESPRESSIF), this is the missing command-layer document")
  (doc "ESP-AT User Guide (docs.espressif.com, PDF)")
  (updated "2026-10-01"))

(request
  (id "REQ-RFIC-NRF52840")
  (status open)
  (wanted "Nordic nRF52840 Product Specification (register-level documentation of the BLE/802.15.4 radio)")
  (why "P5-BOARD.1: the true-RFIC candidate — a radio whose register map is genuinely public, so an RFIC device model would have a primary source (most radios are NDA; this one is the measured exception)")
  (doc "nRF52840 Product Specification")
  (updated "2026-10-01"))

(request
  (id "REQ-RFIC-AT86RF233")
  (status open)
  (wanted "Microchip (Atmel) AT86RF233 datasheet — the 802.15.4 transceiver")
  (why "P5-BOARD.1: a second register-documented radio, so the RFIC leg's evidence does not rest on one vendor")
  (doc "AT86RF233 datasheet")
  (updated "2026-10-01"))

(request
  (id "REQ-RFIC-AR9271-PROBE")
  (status open)
  (wanted "Atheros AR9271 / AR7010 (ath9k_htc family) register-level programming documentation — a PROBE: measure whether any public register-level WiFi baseband documentation exists at all (the open firmware 'openFW' and community driver knowledge are the fallback evidence)")
  (why "P5-BOARD.1: the one plausible exception to 'WiFi basebands are NDA'; if absent, record the measured negative honestly — the corpus already holds the same negative for Cadence GEM / DesignWare GMAC")
  (doc "any AR9271/AR7010 register-level programming document, or a measured negative")
  (updated "2026-10-01"))
