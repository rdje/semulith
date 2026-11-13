<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/sifive-uart-lab-v0/profile.sexp`  `8ee37e508222834a9271739b3a3d59abd37a6495a98dc3dbfb0f4e21c12a721c`
     Generator: `scripts/gen_model_book.py` (sha256 `100cb1b47e94428bce6af762e34fa1546e4b3f16690a4195d80d774929f852ed`) -->

This unit declares its vehicle as `(route device-model)`: there is no encoding space because a device has no instructions — its **register map** is the contract, dossiered as requirement records with the datasheet's locators (`profiles/` … `requirements.sexp`), and its evidence shape is datasheet-derived register-read expectations, not encoded guest programs.
