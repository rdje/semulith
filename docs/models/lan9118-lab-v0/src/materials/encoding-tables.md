<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/lan9118-lab-v0/profile.sexp`  `61e5b560358f6701b9935414c6776ea38c6577abe5cf02dd398b37f4f371ec19`
     Generator: `scripts/gen_model_book.py` (sha256 `100cb1b47e94428bce6af762e34fa1546e4b3f16690a4195d80d774929f852ed`) -->

This unit declares its vehicle as `(route device-model)`: there is no encoding space because a device has no instructions — its **register map** is the contract, dossiered as requirement records with the datasheet's locators (`profiles/` … `requirements.sexp`), and its evidence shape is datasheet-derived register-read expectations, not encoded guest programs.
