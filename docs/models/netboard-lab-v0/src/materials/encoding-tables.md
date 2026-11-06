<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `accb4e78fbacdae5e1905c3068f5a0072229707a2982a29443df67f7402ffc03`
     Generator: `scripts/gen_model_book.py` (sha256 `45ca77489c2e5070b090ce3e8c7f078d2520a12679412f55c7c62899b39e3e5a`) -->

A board adds no encoding space: the instruction encodings a guest can execute are exactly its processor's — pinned by unit id + version + dossier digest in `board.sexp` and billed in the processor unit's own book. The board's contract surface is the memory map, the device windows and the declared absences.
