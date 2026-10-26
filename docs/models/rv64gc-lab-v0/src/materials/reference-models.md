<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64gc-lab-v0/references.sexp`  `c06a4aef7fa762e120edb4ef7b6abf4d70c88f511e257cf088be647e1da6d158`
     Generator: `scripts/gen_model_book.py` (sha256 `ceee0c7f5d535eac700536827bcac2c6563d69b982fe132ba7fff0bd0cbd7afc`) -->

| ID | Role | Status | Kind | Version | sha256 | Terms |
| --- | --- | --- | --- | --- | --- | --- |
| `sail-riscv` | primary oracle candidate | obtained | prebuilt release binary | 0.14 | `16de42a86e4ea7a300385092632cd95d153cb3f6c119d31eaa9384953990b7bf` | BSD-2-Clause (the sail-riscv model). Read and executed locally; no copy is committed and nothing is redistributed. |
| `spike` | second implementation | obtained | source build | — | `8fdf43ac80ccafb96ab076c91967adf6df119b05c5b926ed49a033efe57836a3` | BSD-3-Clause (Regents of the University of California). Built and executed locally; no copy is committed. |

How each is invoked when exercised, as recorded:

- **`sail-riscv`** — `sail_riscv_sim --config-override <override.json> [--trace...] <elf>`
- **`spike`** — `spike --isa=<isa> --priv=<modes> --log-commits --instructions=<n> <elf>`
