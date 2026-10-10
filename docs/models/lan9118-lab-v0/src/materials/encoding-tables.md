<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/lan9118-lab-v0/profile.sexp`  `dab007291ac812efc71c500e774cdf823240f296e86636cc49f76429c0adb288`
     Generator: `scripts/gen_model_book.py` (sha256 `ceee0c7f5d535eac700536827bcac2c6563d69b982fe132ba7fff0bd0cbd7afc`) -->

This unit declares its vehicle as `(route device-model)`: there is no encoding space because a device has no instructions — its **register map** is the contract, dossiered as requirement records with the datasheet's locators (`profiles/` … `requirements.sexp`), and its evidence shape is datasheet-derived register-read expectations, not encoded guest programs.
