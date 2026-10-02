<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64i-lab-v0/references.sexp`  `dc971396a462888776dbbe8ebc1935c0e2fa1d8692a3aeb614e34178bb3b781b`
     Generator: `scripts/gen_model_book.py` (sha256 `b1524b0982e891ec679cb622686eb0a23aa2e6a7259735a3ad976e482d26fda0`) -->

Encoding source **`RISCV-OPCODES`** — https://github.com/riscv/riscv-opcodes (BSD-3-Clause (RISC-V International, 2022)), retrieved 2026-09-14 into `target/refs/riscv-opcodes/`.

Supplies: instruction fixed bits and operand lists for the RV64I base (rv_i, rv64_i) and the M extension (rv_m, rv64_m); operand field positions (arg_lut.csv); and the B/J scrambled-immediate layouts (constants.py). The M files are pinned because MODEL-COMPOSE.1 composed them against the base and MODEL-COMPOSE.2 made the result a tracked fragment — a fragment composed from an unpinned source would be a model built on something nobody can re-derive.

| Pinned file | sha256 | Bytes |
| --- | --- | --- |
| `rv_i` | `146e297ddbe346f325d993aaf56d7006f1bfde39df584b888b221543def17b97` | 4,415 |
| `rv64_i` | `262cbd0884fe1383fcb7c42070cbc73e309d0452ff8d00b38452a4dee7cfa7f5` | 947 |
| `arg_lut.csv` | `cdc61339ffe379c0cd24ad2dc20e57deda95e1da663f94fccb5969d191a8e136` | 1,971 |
| `rv_m` | `1a53ea03820b7044de4f0f04d207c1e4fc0ced46deb2c6ed4a3ca268fa37ddbe` | 432 |
| `rv64_m` | `112bf223a31b7cc51761ce1572a8a35c2502ab2c5a6e318db80c0601b587480e` | 297 |
| `constants.py` | `101c5b8a4169a47f80ff6175a19339cf332eb09f3b09489df6ccabd40afe629b` | 8,950 |
