;; sources.sexp — the pinned specification source for `lan9118-lab-v0` (P5-BOARD.10,
;; 2026-10-02). One document form; validate with
;;   python3 scripts/check_sexp_schema.py profiles/lan9118-lab-v0/sources.sexp schema/sources.sexp

(comment "profiles/lan9118-lab-v0/sources.sexp — the pinned specification source for the"
         "LAN9118 wired-NIC device dossier. One source, one datasheet: Microchip's LAN9118"
         "High Performance Single-Chip 10/100 Non-PCI Ethernet Controller datasheet,"
         "DS00002266B. This dossier cites the whole document — the host-bus contract (§1.10,"
         "§3.6), the FIFO data paths (§3.12/§3.13), the reset architecture (§3.11), the"
         "register descriptions (chapter 5) and the EEPROM interface (§3.9) are all the"
         "device's own contract; what is NOT this unit's business is the board's memory map"
         "and the wire itself (the environment's recorded-trace replay)."
         ""
         "⛔ THE ACQUISITION ROUTE IS THE MATERIALS CORPUS, NOT HTTP. The artifact was adopted"
         "into materials/catalog.sexp through the chipdoc channel (P5-BOARD.8/.9 — corpus-path"
         "network/ethernet-lan9118/current/LAN9118_datasheet.pdf) and is fetched into the"
         "untracked, repo-volume cache .materials/ by scripts/materials.py. `base_url` below"
         "records the corpus locator — the identity we actually acquired against — and"
         "`http_status` is 0 by declaration: 0 means 'no HTTP fetch was performed by this"
         "project', never a server response. The pin was re-verified from the cache on"
         "`retrieved`: sha256 72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee,"
         "836,922 bytes (scripts/materials.py --verify). A fresh-fetch route from the"
         "publisher is not established; guessing a CDN locator is not an acquisition."
         ""
         "⛔ NAME THE ISSUE, NOT JUST THE PART. The LAN9118 datasheet circulates as"
         "DS00002266A (2005, SMSC) and DS00002266B (2018, Microchip). This pin is the B"
         "issue; every locator in this dossier was read against it. One measured"
         "documentation defect in this issue is recorded with REQ-D-NIC-RESETS: §3.11's"
         "soft-reset/PHY-reset completion times render as '2 s'/'100 s' in the PDF's own"
         "text layer (a mis-mapped micro sign) — the dossier pins only the cleanly stated"
         "figures."
         ""
         "Terms: unrecorded in the materials catalog (`licence-evidence` there says why)."
         "The artifact is READ, not redistributed — the cache is untracked and no copy is"
         "committed. SRC-01 requires the actual terms before the artifact is relied on for"
         "anything shipped; that obligation stands.")

(sources (publication "Microchip LAN9118 High Performance Single-Chip 10/100 Non-PCI Ethernet Controller datasheet (chipdoc materials corpus)")
  (not_this_publication "the DS00002266A (SMSC, 2005) issue and third-party mirrors — the pin is DS00002266B via the corpus")
  (revision "DS00002266B 2018-11-30")
  (base_url "chipdoc corpus: network/ethernet-lan9118/current/LAN9118_datasheet.pdf")
  (retrieved "2026-10-02")
  (work_dir ".materials/network")
  (comment "repo-volume, untracked; scripts/materials.py owns the cache")
  (source (id "MICROCHIP-LAN9118") (file "lan9118.pdf")
    (title "LAN9118 High Performance Single-Chip 10/100 Non-PCI Ethernet Controller datasheet") (chapter_version "DS00002266B")
    (sha256 "72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee")
    (bytes 836922) (http_status 0)
    (supplies "the complete LAN9118 register-level contract — the host bus interface (§1.10, §3.6: PIO only, 32/16-bit), the direct register map (Figure 5-1, Table 5-1), the FIFO port semantics (§5.2), every system CSR (§5.3), the indexed MAC CSRs (§5.4), the PHY registers (§5.5), the TX/RX data paths with their command and status formats (§3.12/§3.13), the five reset sources (§3.11), the EEPROM interface and MAC-address auto-load (§3.9), power management (§3.10) and the flow-control machinery (§5.3.22, §5.4.8). It does NOT supply: the values of the configuration straps (D32/nD16, SPEED_SEL — the board's to choose), the PHY ID2 model/revision nibbles (blank in the datasheet), reserved-location read values (§5.1's 'random value'), behaviour for access widths other than 32/16-bit, or a clean unit for §3.11's soft-reset completion time (the text layer's measured '2 s' defect).")))
