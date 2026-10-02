<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `ab64ccfb004e074d3c4939e6490c10357b8f1998f73a322347fd5db47c875e4e`
     `profiles/netboard-lab-v0/DOSSIER.md`  `27f67618b9d8ddbde9fcda4fe70637d01f49735440504a0e78e263e3ec9df498`
     Generator: `scripts/gen_model_book.py` (sha256 `42b24f528fa0752c31faa6ad1e21d0bbcf36beed710c827c54421006fadcec07`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `board.sexp` | the canonical board definition (schema `board.sexp`): composition pins, memory map, reset, declared absences | processor `rv64i-lab-v0` v0, 2 devices, 3 memory regions, 12 recorded board decisions |
| `DOSSIER.md` | the board's narrative — what the definition means and what it does not claim | 6,529 bytes |

A board dossier carries no profile/requirements/obligations of its own: the CPU contract it must satisfy is its processor's, the device guarantees it relies on are its devices'. The composition verdict that matches them (`COMPOSITION-VERDICT.md`, P5-BOARD.4) is the unit's evidence — decided by the BOARD-VERDICT doctrine and included in the book's verdict chapter.
