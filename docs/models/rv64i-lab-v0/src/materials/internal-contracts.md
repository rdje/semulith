<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/rv64i-lab-v0/profile.sexp`  `63f0aa1e36fe731ef6dcabc7b63a3fe7250c84063944e47e9f4066d5d2648e3d`
     `profiles/rv64i-lab-v0/state.sexp`  `ff53fb04f3ed7ac25e4db78e6e92cc3e0caa086df438e221350627194cbea5a4`
     `profiles/rv64i-lab-v0/encoding.sexp`  `93a2d4718a50b60c23c3b5e64afa64499b09fcf41a906d46d83e63eebab2e5e9`
     `profiles/rv64i-lab-v0/requirements.sexp`  `9a7840edb4ad32493253ba353828d0fee5b1f09da45101ce6a52124cf3a301e1`
     `profiles/rv64i-lab-v0/contract-obligations.sexp`  `28d6f8fb2c74fce030f27d6b6d4102e32b7c62776cd713cbe2279b0845b6ccce`
     `profiles/rv64i-lab-v0/interactions.sexp`  `d0e9b94a55066cf2c80fbcc17bbab3fe6b590ee4d6e8d2a4a6453026028cd159`
     Generator: `scripts/gen_model_book.py` (sha256 `42b24f528fa0752c31faa6ad1e21d0bbcf36beed710c827c54421006fadcec07`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `profile.sexp` | the unit's declaration: scope, decisions, authorities | 28 decisions, 52 declared instruction forms |
| `state.sexp` | the architectural-state census, including the hidden-state census | 32 integer registers, XLEN 64, hidden state: No — for this profile, and only because of what it excludes. |
| `encoding.sexp` | the composed encoding space (fragments resolved, collision-free, gated by UNIT-COMPOSITION) | composes `riscv/rv64i` |
| `requirements.sexp` | the predeclared requirements, one per decision (RECORD-SCHEMA cross-checks the statements verbatim) | 28 requirements |
| `contract-obligations.sexp` | the environment contract (`rv64i-lab-env-v0`): every obligation with positive AND negative checks | 36 obligations, 72 declared checks |
| `guests/` | the EVD-05 guest corpus: independently encoded programs and specification-derived expectations | 49 guests, 643 expected steps |
| `interactions.sexp` | the declared interaction matrix (P2-SCALAR.4), gated by INTERACTION-MATRIX | 21 cells over 6 axes |
