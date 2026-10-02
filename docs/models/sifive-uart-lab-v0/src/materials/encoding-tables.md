<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/sifive-uart-lab-v0/profile.sexp`  `a44a7ddbff330cdec752e2541f95b2288e4bf4c333878c910a7d25be4695f401`
     Generator: `scripts/gen_model_book.py` (sha256 `42b24f528fa0752c31faa6ad1e21d0bbcf36beed710c827c54421006fadcec07`) -->

This unit declares its vehicle as `(route device-model)`: there is no encoding space because a device has no instructions — its **register map** is the contract, dossiered as requirement records with the datasheet's locators (`profiles/` … `requirements.sexp`), and its evidence shape is datasheet-derived register-read expectations, not encoded guest programs.
