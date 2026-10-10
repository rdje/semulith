<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `profiles/dsp56300-lab-v0/profile.sexp`  `dc42143565a8a6c65087a2834456df32b0a8eddcf8c216c247e2e7bbb75442dd`
     `profiles/dsp56300-lab-v0/state.sexp`  `ae4aa72dd8114d5de5828845d36b34f885de071eea3850324e3ce195ca738ff9`
     `profiles/dsp56300-lab-v0/requirements.sexp`  `b4650fe0e1cf39417182f0c82893d1abfd3686eccf0893b8902403be240ce386`
     `profiles/dsp56300-lab-v0/contract-obligations.sexp`  `6b6bcbaec05d0056f7e1dfee4e46d3f4e0c2d0b66e17244b623d6314b0e52773`
     `profiles/dsp56300-lab-v0/interactions.sexp`  `c44ad7ee3953a43bf5b5a09ff85bedd8d3224bc4aaf4c65245d54d48c5947b33`
     Generator: `scripts/gen_model_book.py` (sha256 `ceee0c7f5d535eac700536827bcac2c6563d69b982fe132ba7fff0bd0cbd7afc`) -->

| Document | Role | Derived contents |
| --- | --- | --- |
| `profile.sexp` | the unit's declaration: scope, decisions, authorities | 7 decisions, 19 declared instruction forms |
| `state.sexp` | the architectural-state census, including the hidden-state census | 5 register families (masked widths, per-part readouts), 3 memory spaces, the hardware stack declared, hidden state: No — for subset v0, and only because of what it excludes. The canonical end-state dump is the complete architectural state; every exclusion reopens its candidate row. |
| `encoding.sexp` | DEFERRED — the encoding/definition generalization was measured a lane, not an extension (`P3-BREADTH.5` slice 3); the sibling crate is the declared, exercised vehicle | no document — the reopening conditions are named in the tree |
| `requirements.sexp` | the requirement catalogue; RECORD-SCHEMA cross-checks declared decision mirrors verbatim | 7 requirements |
| `contract-obligations.sexp` | the declared environment-obligation catalogue (`dsp56300-lab-env-v0`): positive AND negative checks per record; counts include historical records | 13 catalogue obligations, 26 declared checks |
| `guests/` | the synthetic guest corpus: checkpoint-compared `.a56` programs, canonical end-state dumps against the pinned reference (`cyc` never compared) | 6 guests |
| `interactions.sexp` | the unit's declared interaction matrix, gated by INTERACTION-MATRIX | 21 cells over 6 axes |
