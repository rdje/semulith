<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `584bcc4201aafcd3c1c582718e96c2341beb3eb70aec84f8bb1951c923921854`
     Generator: `scripts/gen_model_book.py` (sha256 `42b24f528fa0752c31faa6ad1e21d0bbcf36beed710c827c54421006fadcec07`) -->

A board has no specification of its own: it **composes** pinned units. The canonical definition pins versions, not names — the processor by unit id + version + the GATE-REPORT-gated dossier content digest, each device by its datasheet's material id + revision + sha256.

| Pin | Identity | Revision / version | sha256 |
| --- | --- | --- | --- |
| processor | `rv64i-lab-v0` v0 (contract `rv64i-lab-env-v0` v0) | the unit's dossier | `95ebca2f0ee0518e43a24088f070642120c45ef72d8b35a7379c4d0101cf8001` |
| device `uart0` (unit `sifive-uart-lab-v0`) | **SIFIVE-FU540-C000** | v1p5 | `5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c` |
| device `eth0` (unit `lan9118-lab-v0`) | **MICROCHIP-LAN9118** | DS00002266B 2018-11-30 | `72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee` |
