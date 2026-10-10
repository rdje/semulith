<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `8a7fce5a87ee354d07fc8a3ce692048c395eb82cb00d35e32405af70d70e3441`
     Generator: `scripts/gen_model_book.py` (sha256 `2f062f639b366734683fc5121779bd446fef1ac3c66b7766326deb9f92b855a2`) -->

A board adds no encoding space: the instruction encodings a guest can execute are exactly its processor's — pinned by unit id + version + dossier digest in `board.sexp` and billed in the processor unit's own book. The board's contract surface is the memory map, the device windows and the declared absences.
