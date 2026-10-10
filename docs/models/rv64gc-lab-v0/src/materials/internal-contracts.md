<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64gc-lab-v0/profile.sexp`  `7afc857ef2f30e88917a11068ebc4ba56a62e428912db3333e6cedbeb00913db`
     `profiles/rv64gc-lab-v0/state.sexp`  `0974ac40ec2915c2867f02c14f15fd8ab92bd028b790de1dca0f3785e32216e8`
     `profiles/rv64gc-lab-v0/encoding.sexp`  `8b77378df968f9687c370f0f9128c31531853b11bccc9a68abdbe8b91e3df5a0`
     `profiles/rv64gc-lab-v0/requirements.sexp`  `0f006fa9bccb664cf461684fd9976fb4cc63ea3ca4272e28c7b731fc52de8802`
     `profiles/rv64gc-lab-v0/contract-obligations.sexp`  `a3111857cc3e749970b0fea3cbaf7a90571f27c98c21d5bd71f8a56197b13f8d`
     `profiles/rv64gc-lab-v0/interactions.sexp`  `55979cddd1958655b12e3cca21ec425e1acc301f1fefa76c8007d38b591ca54a`
     Generator: `scripts/gen_model_book.py` (sha256 `ceee0c7f5d535eac700536827bcac2c6563d69b982fe132ba7fff0bd0cbd7afc`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `profile.sexp` | the unit's declaration: scope, decisions, authorities | 25 decisions, 200 declared instruction forms |
| `state.sexp` | the architectural-state census, including the hidden-state census | 32 integer registers, XLEN 64, hidden state: No - for the complete selected single-hart laboratory profile: all twelve candidates below are answered. The consequence enumerates every state owner; a new extension or environment contract must reopen this census. |
| `encoding.sexp` | the composed encoding space (fragments resolved, collision-free, gated by UNIT-COMPOSITION) | composes `riscv/rv64i`, `riscv/zicsr`, `riscv/zicntr`, `riscv/system`, `riscv/a`, `riscv/zifencei`, `riscv/f`, `riscv/d`, `riscv/m`, `riscv/c` |
| `requirements.sexp` | the requirement catalogue; RECORD-SCHEMA cross-checks declared decision mirrors verbatim | 48 requirements |
| `contract-obligations.sexp` | the declared environment-obligation catalogue (`rv64gc-lab-env-v0`, `rv64gc-lab-env-v1`, `rv64gc-lab-env-v2`): positive AND negative checks per record; counts include historical records | 66 catalogue obligations, 132 declared checks |
| `guests/` | the EVD-05 guest corpus: canonically encoded programs and specification-derived expectations | 167 guests, 5365 expected steps |
| `interactions.sexp` | the unit's declared interaction matrix, gated by INTERACTION-MATRIX | 28 cells over 7 axes |
