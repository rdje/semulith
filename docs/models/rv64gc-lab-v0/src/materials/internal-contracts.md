<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64gc-lab-v0/profile.sexp`  `f553f32cb1c4c48a2bc541a6680594ca21afb364b28a598aea0832683e622a90`
     `profiles/rv64gc-lab-v0/state.sexp`  `0974ac40ec2915c2867f02c14f15fd8ab92bd028b790de1dca0f3785e32216e8`
     `profiles/rv64gc-lab-v0/encoding.sexp`  `8b77378df968f9687c370f0f9128c31531853b11bccc9a68abdbe8b91e3df5a0`
     `profiles/rv64gc-lab-v0/requirements.sexp`  `397d8944a87159a5011a5f7895b2061b3224a7bce4d81320a76524da68180c11`
     `profiles/rv64gc-lab-v0/contract-obligations.sexp`  `32b1218504eacf1a9e1aa154ca855c1290ce5a487ff226fdc39fb860bc0f5ee7`
     `profiles/rv64gc-lab-v0/interactions.sexp`  `54b61c2273e3cf9b818a43231b0c18b3594b488d5dd3930eb2fb60411fedc7d1`
     Generator: `scripts/gen_model_book.py` (sha256 `37c536b0129a0a722773286177f09bf50d623ae65e118bfac58a8b8c345131b2`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `profile.sexp` | the unit's declaration: scope, decisions, authorities | 25 decisions, 200 declared instruction forms |
| `state.sexp` | the architectural-state census, including the hidden-state census | 32 integer registers, XLEN 64, hidden state: No - for the complete selected single-hart laboratory profile: all twelve candidates below are answered. The consequence enumerates every state owner; a new extension or environment contract must reopen this census. |
| `encoding.sexp` | the composed encoding space (fragments resolved, collision-free, gated by UNIT-COMPOSITION) | composes `riscv/rv64i`, `riscv/zicsr`, `riscv/zicntr`, `riscv/system`, `riscv/a`, `riscv/zifencei`, `riscv/f`, `riscv/d`, `riscv/m`, `riscv/c` |
| `requirements.sexp` | the requirement catalogue; RECORD-SCHEMA cross-checks declared decision mirrors verbatim | 48 requirements |
| `contract-obligations.sexp` | the declared environment-obligation catalogue (`rv64gc-lab-env-v0`, `rv64gc-lab-env-v1`, `rv64gc-lab-env-v2`, `rv64gc-lab-env-v3`): positive AND negative checks per record; counts include historical records | 70 catalogue obligations, 140 declared checks |
| `guests/` | the EVD-05 guest corpus: canonically encoded programs and specification-derived expectations | 187 guests, 6751 expected steps |
| `interactions.sexp` | the unit's declared interaction matrix, gated by INTERACTION-MATRIX | 28 cells over 7 axes |
