<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/netboard-lab-v0/board.sexp`  `8a7fce5a87ee354d07fc8a3ce692048c395eb82cb00d35e32405af70d70e3441`
     Generator: `scripts/gen_model_book.py` (sha256 `2f062f639b366734683fc5121779bd446fef1ac3c66b7766326deb9f92b855a2`) -->

A board has no specification of its own: it **composes** pinned units. The canonical definition pins versions, not names — the processor by unit id + version + the GATE-REPORT-gated dossier content digest, each device by its datasheet's material id + revision + sha256.

| Pin | Identity | Revision / version | sha256 |
| --- | --- | --- | --- |
| processor | `rv64i-lab-v0` v0 (contract `rv64i-lab-env-v0` v0) | the unit's dossier | `91b271eaa2346272f7a34358a1fbc399164b081f35437b27d88ca584193785ef` |
| device `uart0` (unit `sifive-uart-lab-v0`) | **SIFIVE-FU540-C000** | v1p5 | `5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c` |
| device `eth0` (unit `lan9118-lab-v0`) | **MICROCHIP-LAN9118** | DS00002266B 2018-11-30 | `72fe68f241b5bc91a861cff98a877ae907339d396e64394b0f5daa2c391bf6ee` |
