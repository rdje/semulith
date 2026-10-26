<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64gc-lab-v0/references.sexp`  `c06a4aef7fa762e120edb4ef7b6abf4d70c88f511e257cf088be647e1da6d158`
     Generator: `scripts/gen_model_book.py` (sha256 `ceee0c7f5d535eac700536827bcac2c6563d69b982fe132ba7fff0bd0cbd7afc`) -->

Encoding source **`RISCV-OPCODES`** — https://github.com/riscv/riscv-opcodes (BSD-3-Clause (RISC-V International, 2022)), retrieved 2026-10-03 into `target/refs/riscv-opcodes/`.

Supplies: instruction fixed bits and operand lists for Zicsr (rv_zicsr: csrrw/csrrs/csrrc and their immediate forms), the Zicntr counter reads (rv_zicntr: rdcycle/rdtime/rdinstret as pinned pseudo-op rows of csrrs), the privileged system instructions (rv_system: mret, wfi; rv_s: sret, sfence.vma — RVP-INSNS 18.1), the A extension (rv_a: lr.w/sc.w and the nine amo*.w; rv64_a: the eleven .D forms), Zifencei (rv_zifencei: fence.i), the F extension (rv_f: the 26 RV32F forms; rv64_f: the four 64-bit integer conversions) and the D extension (rv_d: the 26 RV32D forms; rv64_d: the four 64-bit integer conversions and the two 64-bit bit moves); the csr and zimm5 operand field positions plus the aq/rl ordering-field positions and F's rs3/rm positions (arg_lut.csv); the CSR name-to-address map (csrs.csv); the CSR field masks (encoding.h — mstatus.TSR/TW/TVM/MPRV, the xIE/xPIE/xPP positions); and the trap cause codes (causes.csv).; the M multiply/divide forms (rv_m/rv64_m: the 13 instructions, re-pinned at P4-SYSTEM.11 slice b — the same bytes definitions/riscv/m.sexp names); the compressed forms at RV64 with D (rv_c 23 + rv64_c 10 = Zca, rv_c_d 4 = Zcd — the RV32-only rv32_c/rv32_c_f deliberately not pinned), re-pinned at P4-SYSTEM.12 slice a, fetched from upstream master and pinned by content: the bytes definitions/riscv/c.sexp names

| Pinned file | sha256 | Bytes |
| --- | --- | --- |
| `rv_zicsr` | `dd8cc0e2c32fb5658d4aa719cef6ab1b714e2145ba071c9aeb382d9963e4901f` | 940 |
| `rv_zicntr` | `34ed6bb1cf98448c7c40abbd6f67cbccee0788bd42429a2b1a9538952f6cca8c` | 298 |
| `rv_system` | `4a58b5f0c908d7b748abbeb9df8335dbc53650ea284b738e4351afd49755e646` | 141 |
| `rv_s` | `e9d509a3a46de9024547fa75f76bf3c2839910ebc9af81d106cc46bc0ac6eb78` | 132 |
| `rv_a` | `d9eaa988c4779ca352d9da9eabacf6c71771d0b81e04b234302627f69e0863d9` | 858 |
| `rv64_a` | `819e0487131bc97cfc0b6f3de62390f2f9936b43e80aef7c6cec14fbe7c7a1b6` | 885 |
| `rv_zifencei` | `be2d8f7286e06fadafffbde14656e6adb3f923ce704ea0829229d3a3b5f35758` | 73 |
| `rv_f` | `227e09504c0d758add114d5a77ac06d7e2ffab9c6a9509633c4f531db58b3e3e` | 3,050 |
| `rv64_f` | `5c01c243ccd8a1c0e24a48a1ffcf62eecb10aa36fd6bdcedf7392e670cd46cf9` | 320 |
| `rv_d` | `24bc7c6384f9a009dbafb3f177ec68b0d4f8fb1c2c2b7b07767320fdd7d4acbc` | 2,091 |
| `rv64_d` | `883e668be4c536d0dfdb8c02bd1f3eb959801eb953f1fb7a4b4e5e623cbf19a9` | 465 |
| `rv_m` | `1a53ea03820b7044de4f0f04d207c1e4fc0ced46deb2c6ed4a3ca268fa37ddbe` | 432 |
| `rv64_m` | `112bf223a31b7cc51761ce1572a8a35c2502ab2c5a6e318db80c0601b587480e` | 297 |
| `rv_c` | `f97db59ffe15873bf4af8ab53694f703a90d582c2602ee876d8578824b1feda8` | 1,499 |
| `rv64_c` | `1c51536f890d0ab1dec9b75980ef1e71ce03194eeb99f294c86d1b337807f284` | 673 |
| `rv_c_d` | `c52a9107d44ba9edb39d8fda880779f46cf648351cb9a666008ddbe8c1e0ca7a` | 249 |
| `csrs.csv` | `caf7f732356167cbc5a93eeb6b37ddbaf5c8483229b50ee7cb7a56bb6d29d493` | 6,101 |
| `encoding.h` | `6ce1b7caafd51379ad1f775cbb59f978eda8cdae35bc19ffd0ee00482543d944` | 22,687 |
| `causes.csv` | `237491f164e0818afcacb8853f665a97dedb585e21c64d784433b80ae870ee69` | 554 |
| `arg_lut.csv` | `cdc61339ffe379c0cd24ad2dc20e57deda95e1da663f94fccb5969d191a8e136` | 1,971 |
