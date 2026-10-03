<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/lan9118-lab-v0/sources.sexp`  `eee2e26aac26903c0beec6ae72232bca49b7d79998fa2e01de12a6f244b4479b`
     Generator: `scripts/gen_model_book.py` (sha256 `2f062f639b366734683fc5121779bd446fef1ac3c66b7766326deb9f92b855a2`) -->

Pinned publication: **Microchip LAN9118 High Performance Single-Chip 10/100 Non-PCI Ethernet Controller datasheet (chipdoc materials corpus)**, revision `DS00002266B 2018-11-30`, retrieved 2026-10-02 — explicitly NOT the DS00002266A (SMSC, 2005) issue and third-party mirrors — the pin is DS00002266B via the corpus.

| ID | Document | Chapter version | Pinned artifact | sha256 | Bytes | HTTP |
| --- | --- | --- | --- | --- | --- | --- |
| `MICROCHIP-LAN9118` | LAN9118 High Performance Single-Chip 10/100 Non-PCI Ethernet Controller datasheet | DS00002266B | `lan9118.pdf` | `72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee` | 836,922 | 0 |

What each supplies, as recorded in the pinned ledger:

- **`MICROCHIP-LAN9118`** — the complete LAN9118 register-level contract — the host bus interface (§1.10, §3.6: PIO only, 32/16-bit), the direct register map (Figure 5-1, Table 5-1), the FIFO port semantics (§5.2), every system CSR (§5.3), the indexed MAC CSRs (§5.4), the PHY registers (§5.5), the TX/RX data paths with their command and status formats (§3.12/§3.13), the five reset sources (§3.11), the EEPROM interface and MAC-address auto-load (§3.9), power management (§3.10) and the flow-control machinery (§5.3.22, §5.4.8). It does NOT supply: the values of the configuration straps (D32/nD16, SPEED_SEL — the board's to choose), the PHY ID2 model/revision nibbles (blank in the datasheet), reserved-location read values (§5.1's 'random value'), behaviour for access widths other than 32/16-bit, or a clean unit for §3.11's soft-reset completion time (the text layer's measured '2 s' defect).
