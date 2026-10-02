<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/sifive-uart-lab-v0/profile.sexp`  `a44a7ddbff330cdec752e2541f95b2288e4bf4c333878c910a7d25be4695f401`
     Generator: `scripts/gen_model_book.py` (sha256 `42b24f528fa0752c31faa6ad1e21d0bbcf36beed710c827c54421006fadcec07`) -->

This unit pins **no reference models**: it declares `(comparison register-expectations)` — the comparison surface is the dossier's own datasheet-derived register-read expectations (`expectations/`), recorded before any model exists (EVD-05 at the device layer). A reference that shares an ancestor with the datasheet would not be a second opinion; an independent implementation may be pinned here the day one is acquired through the materials channel.
