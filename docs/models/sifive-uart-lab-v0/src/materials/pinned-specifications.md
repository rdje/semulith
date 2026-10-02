<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/sifive-uart-lab-v0/sources.sexp`  `f723943561eba48d768d48be6e668b4998274e8d97f89b4315479bce1cc4a016`
     Generator: `scripts/gen_model_book.py` (sha256 `42b24f528fa0752c31faa6ad1e21d0bbcf36beed710c827c54421006fadcec07`) -->

Pinned publication: **SiFive FU540-C000 Manual — SiFive, Inc. (chipdoc materials corpus)**, revision `v1p5`, retrieved 2026-10-02 — explicitly NOT third-party mirrors and the legacy v1p0/v1p3/v1p4 issues — the pin is v1p5 via the corpus.

| ID | Document | Chapter version | Pinned artifact | sha256 | Bytes | HTTP |
| --- | --- | --- | --- | --- | --- | --- |
| `SIFIVE-FU540-C000` | SiFive FU540-C000 Manual v1p5 | v1p5 | `fu540-c000-v1p5.pdf` | `5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c` | 2,361,460 | 0 |

What each supplies, as recorded in the pinned ledger:

- **`SIFIVE-FU540-C000`** — the SiFive UART contract — §13 only: the instance parameters (Table 58), the register map and the aligned-32-bit access rule (§13.3, Table 59), the per-register semantics of txdata/rxdata/txctrl/rxctrl/ie/ip/div (§13.4–§13.9, Tables 60–66), the FIFO depths and the watermark conditions. It does NOT supply: Reserved-bit behaviour, the effect of accesses outside Table 59's offsets, the effect of accesses that are not naturally aligned 32-bit, or the reset values the tables mark X.
