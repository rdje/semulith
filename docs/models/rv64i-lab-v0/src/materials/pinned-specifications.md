<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64i-lab-v0/sources.sexp`  `e0daeebff645e8bd92690dd5c36ce795370da0a164be33ac973b1158b1dcbffc`
     Generator: `scripts/gen_model_book.py` (sha256 `9d24f751b8b7cdc1b608927430b60d6312bcdcd66984a4f4d8bf7d9be4f8eea7`) -->

Pinned publication: **RISC-V Ratified Specifications Library (docs.riscv.org)**, revision `v20260120`, retrieved 2026-09-13 — explicitly NOT github.com/riscv/riscv-isa-manual releases — different section numbering.

| ID | Document | Chapter version | Pinned artifact | sha256 | Bytes | HTTP |
| --- | --- | --- | --- | --- | --- | --- |
| `RVI-INTRO` | Introduction :: RISC-V Ratified Specifications Library | — | `intro.html` | `3d65f713115bfd58f783fcebcce3f243f508d0af71bbac79a59e5ff79e13bf0c` | 69,772 | 200 |
| `RVI-RV32I` | 1.1. RV32I Base Integer Instruction Set, Version 2.1 | 2.1 | `rv32.html` | `3b20e92f067509535f95883832e84b32dbea43a29e1347b7925c374213ad75ec` | 107,630 | 200 |
| `RVI-RV64I` | 3.1. RV64I Base Integer Instruction Set, Version 2.1 | 2.1 | `rv64.html` | `6eadb316c2d535ccb87a7a6feb03ff54af6f4b5bbeb5c1a5102a02af81f13abd` | 49,246 | 200 |

What each supplies, as recorded in the pinned ledger:

- **`RVI-INTRO`** — execution-environment interface (EEI) and hart definitions; the four trap effects; the meaning of UNSPECIFIED
- **`RVI-RV32I`** — the base integer ISA that RV64I modifies: register state, formats, control transfer, load/store, FENCE, ECALL/EBREAK, HINTs
- **`RVI-RV64I`** — the RV64I deltas: XLEN=64, the *W instruction family, 6-bit shift amounts, LWU/LD/SD, RV64I HINT table
