<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64i-lab-v0/references.sexp`  `dc971396a462888776dbbe8ebc1935c0e2fa1d8692a3aeb614e34178bb3b781b`
     Generator: `scripts/gen_model_book.py` (sha256 `9d24f751b8b7cdc1b608927430b60d6312bcdcd66984a4f4d8bf7d9be4f8eea7`) -->

| ID | Role | Status | Kind | Version | sha256 | Terms |
| --- | --- | --- | --- | --- | --- | --- |
| `sail-riscv` | primary oracle candidate | obtained | prebuilt release binary | 0.14 | `16de42a86e4ea7a300385092632cd95d153cb3f6c119d31eaa9384953990b7bf` | BSD-2-Clause (the sail-riscv model). Read and executed locally; no copy is committed and nothing is redistributed. |
| `spike` | second implementation | obtained | source build | Spike RISC-V ISA Simulator 1.1.1-dev | `8fdf43ac80ccafb96ab076c91967adf6df119b05c5b926ed49a033efe57836a3` | BSD-3-Clause (Regents of the University of California). Built and executed locally; no copy is committed. |
| `qemu` | third implementation, discovered during this leaf | obtained | pre-existing host toolchain, used read-only | QEMU emulator version 11.1.1 | `03725d89f81f327c7e95dd6129dc7e9a6440d49d7158ade0d558efa9d6bd56f3` | GPL-2.0-only. Installed on this host before this project existed; used read-only as a toolchain dependency and never modified, copied or redistributed. |
| `act4` | external test suite, not a model | acquired (sparse partial) | test corpus | — | — | Apache-2.0 |

How each is invoked when exercised, as recorded:

- **`sail-riscv`** — `sail_riscv_sim --config-override <override.json> [--trace...] <elf>`
- **`spike`** — `spike --isa=rv64i --priv=m --log-commits --instructions=<n> <elf>`
- **`qemu`** — `qemu-system-riscv64 -machine virt -cpu rv64i -bios none -nographic -d in_asm,cpu,int -D <log> -kernel <elf>`
- **`act4`** — `scripts/run_act4_campaign.py — build, three models, the signature comparison`
