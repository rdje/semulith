<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `accb4e78fbacdae5e1905c3068f5a0072229707a2982a29443df67f7402ffc03`
     Generator: `scripts/gen_model_book.py` (sha256 `37c536b0129a0a722773286177f09bf50d623ae65e118bfac58a8b8c345131b2`) -->

A board adds no encoding space: the instruction encodings a guest can execute are exactly its processor's — pinned by unit id + version + dossier digest in `board.sexp` and billed in the processor unit's own book. The board's contract surface is the memory map, the device windows and the declared absences.
