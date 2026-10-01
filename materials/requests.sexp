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
