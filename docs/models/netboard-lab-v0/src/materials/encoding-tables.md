<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `93b087cb65842cd43ce63e24853f4a7c9778a9278d3a8d6458a606f1a6122333`
     Generator: `scripts/gen_model_book.py` (sha256 `b1524b0982e891ec679cb622686eb0a23aa2e6a7259735a3ad976e482d26fda0`) -->

A board adds no encoding space: the instruction encodings a guest can execute are exactly its processor's — pinned by unit id + version + dossier digest in `board.sexp` and billed in the processor unit's own book. The board's contract surface is the memory map, the device windows and the declared absences.
