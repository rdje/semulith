<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `b77201f143e2b0dd3b785e2f7750b6828e1cbe9220c755bfe06ea3bf8c983a50`
     Generator: `scripts/gen_model_book.py` (sha256 `2f062f639b366734683fc5121779bd446fef1ac3c66b7766326deb9f92b855a2`) -->

A board adds no encoding space: the instruction encodings a guest can execute are exactly its processor's — pinned by unit id + version + dossier digest in `board.sexp` and billed in the processor unit's own book. The board's contract surface is the memory map, the device windows and the declared absences.
