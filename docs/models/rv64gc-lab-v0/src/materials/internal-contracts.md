<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64gc-lab-v0/profile.sexp`  `305565b8c58231baa6d53416db2e13ae7ec9cb75cec46b90b02fe3bf5192b06a`
     `profiles/rv64gc-lab-v0/state.sexp`  `9e679b9f3cc652a3a3361628734d6c768baeb62804bbd6a8369fc18344c1fbca`
     `profiles/rv64gc-lab-v0/encoding.sexp`  `8b77378df968f9687c370f0f9128c31531853b11bccc9a68abdbe8b91e3df5a0`
     `profiles/rv64gc-lab-v0/requirements.sexp`  `56563429ebc0fb923b599bbdf9c92bd29cfca2e17949bd020f06204b3c84b605`
     `profiles/rv64gc-lab-v0/contract-obligations.sexp`  `dd4184d6ebc1ec15658855e6b0c199494db9f5851eb6efd4ac538fc1e9978633`
     `profiles/rv64gc-lab-v0/interactions.sexp`  `4e07ec00d9e47a145b597920ca7b229041703b4a7acd746ba97eef76e32de164`
     Generator: `scripts/gen_model_book.py` (sha256 `100cb1b47e94428bce6af762e34fa1546e4b3f16690a4195d80d774929f852ed`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `profile.sexp` | the unit's declaration: scope, decisions, authorities | 25 decisions, 200 declared instruction forms |
| `state.sexp` | the architectural-state census, including the hidden-state census | 32 integer registers, XLEN 64, hidden state: No - for the complete selected single-hart laboratory profile: all twelve candidates below are answered. The consequence enumerates every state owner; a new extension or environment contract must reopen this census. |
| `encoding.sexp` | the composed encoding space (fragments resolved, collision-free, gated by UNIT-COMPOSITION) | composes `riscv/rv64i`, `riscv/zicsr`, `riscv/zicntr`, `riscv/system`, `riscv/a`, `riscv/zifencei`, `riscv/f`, `riscv/d`, `riscv/m`, `riscv/c` |
| `requirements.sexp` | the requirement catalogue; RECORD-SCHEMA cross-checks declared decision mirrors verbatim | 48 requirements |
| `contract-obligations.sexp` | the declared environment-obligation catalogue (`rv64gc-lab-env-v0`, `rv64gc-lab-env-v1`, `rv64gc-lab-env-v2`, `rv64gc-lab-env-v3`, `rv64gc-lab-env-v4`): positive AND negative checks per record; counts include historical records | 73 catalogue obligations, 146 declared checks |
| `guests/` | the EVD-05 guest corpus: canonically encoded programs and specification-derived expectations | 210 guests, 10091 expected steps |
| `interactions.sexp` | the unit's declared interaction matrix, gated by INTERACTION-MATRIX | 28 cells over 7 axes |
