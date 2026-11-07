<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64gc-lab-v0/profile.sexp`  `f553f32cb1c4c48a2bc541a6680594ca21afb364b28a598aea0832683e622a90`
     `profiles/rv64gc-lab-v0/state.sexp`  `0974ac40ec2915c2867f02c14f15fd8ab92bd028b790de1dca0f3785e32216e8`
     `profiles/rv64gc-lab-v0/encoding.sexp`  `8b77378df968f9687c370f0f9128c31531853b11bccc9a68abdbe8b91e3df5a0`
     `profiles/rv64gc-lab-v0/requirements.sexp`  `11a0b2d62f77165955b4900755e5e2e0bed356d908260fad43fcd3269d040e1f`
     `profiles/rv64gc-lab-v0/contract-obligations.sexp`  `32b1218504eacf1a9e1aa154ca855c1290ce5a487ff226fdc39fb860bc0f5ee7`
     `profiles/rv64gc-lab-v0/interactions.sexp`  `e0b992148d29b02dedc63d412570e73ca88277035eddb008518bd3eae490b421`
     Generator: `scripts/gen_model_book.py` (sha256 `100cb1b47e94428bce6af762e34fa1546e4b3f16690a4195d80d774929f852ed`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `profile.sexp` | the unit's declaration: scope, decisions, authorities | 25 decisions, 200 declared instruction forms |
| `state.sexp` | the architectural-state census, including the hidden-state census | 32 integer registers, XLEN 64, hidden state: No - for the complete selected single-hart laboratory profile: all twelve candidates below are answered. The consequence enumerates every state owner; a new extension or environment contract must reopen this census. |
| `encoding.sexp` | the composed encoding space (fragments resolved, collision-free, gated by UNIT-COMPOSITION) | composes `riscv/rv64i`, `riscv/zicsr`, `riscv/zicntr`, `riscv/system`, `riscv/a`, `riscv/zifencei`, `riscv/f`, `riscv/d`, `riscv/m`, `riscv/c` |
| `requirements.sexp` | the requirement catalogue; RECORD-SCHEMA cross-checks declared decision mirrors verbatim | 48 requirements |
| `contract-obligations.sexp` | the declared environment-obligation catalogue (`rv64gc-lab-env-v0`, `rv64gc-lab-env-v1`, `rv64gc-lab-env-v2`, `rv64gc-lab-env-v3`): positive AND negative checks per record; counts include historical records | 70 catalogue obligations, 140 declared checks |
| `guests/` | the EVD-05 guest corpus: canonically encoded programs and specification-derived expectations | 204 guests, 9689 expected steps |
| `interactions.sexp` | the unit's declared interaction matrix, gated by INTERACTION-MATRIX | 28 cells over 7 axes |
