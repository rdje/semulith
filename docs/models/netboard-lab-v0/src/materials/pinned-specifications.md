<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `accb4e78fbacdae5e1905c3068f5a0072229707a2982a29443df67f7402ffc03`
     Generator: `scripts/gen_model_book.py` (sha256 `ceee0c7f5d535eac700536827bcac2c6563d69b982fe132ba7fff0bd0cbd7afc`) -->

A board has no specification of its own: it **composes** pinned units. The canonical definition pins versions, not names — the processor by unit id + version + the GATE-REPORT-gated dossier content digest, each device by its datasheet's material id + revision + sha256.

| Pin | Identity | Revision / version | sha256 |
| --- | --- | --- | --- |
| processor | `rv64i-lab-v0` v0 (contract `rv64i-lab-env-v0` v0) | the unit's dossier | `f025af0b338a820ab7166c3b336752f1e36c1769800887e73b16b8b8ad78171b` |
| device `uart0` (unit `sifive-uart-lab-v0`) | **SIFIVE-FU540-C000** | v1p5 | `5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c` |
| device `eth0` (unit `lan9118-lab-v0`) | **MICROCHIP-LAN9118** | DS00002266B 2018-11-30 | `72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee` |
