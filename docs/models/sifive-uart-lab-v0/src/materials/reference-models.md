<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/sifive-uart-lab-v0/profile.sexp`  `8ee37e508222834a9271739b3a3d59abd37a6495a98dc3dbfb0f4e21c12a721c`
     Generator: `scripts/gen_model_book.py` (sha256 `100cb1b47e94428bce6af762e34fa1546e4b3f16690a4195d80d774929f852ed`) -->

This unit pins **no reference models**: it declares `(comparison register-expectations)` — the comparison surface is the dossier's own datasheet-derived register-read expectations (`expectations/`), recorded before any model exists (EVD-05 at the device layer). A reference that shares an ancestor with the datasheet would not be a second opinion; an independent implementation may be pinned here the day one is acquired through the materials channel.
