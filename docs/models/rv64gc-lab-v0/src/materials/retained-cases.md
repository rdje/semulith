<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `evidence/rv64gc-csr-set-v1/case.sexp`  `6b45c94b94408be618bb509fa011837708477da59ca1c2246d52cda990d69910`
     `evidence/rv64gc-csr-set-v2/case.sexp`  `90a04d87453670e6ed40a34ce5a18950049a8cff6ee1f612af2f77d8c12885a8`
     `evidence/rv64gc-sstc-v1/case.sexp`  `fd934b35766d8b084aab97735049fedcb6526a539aa58942fb6098d2f5174406`
     `evidence/rv64gc-xlen-forms-v1/case.sexp`  `a65f2eef8f4914b969e3547d4344061d3760364bd8d9ff525a8a9875508d1f37`
     `evidence/rv64gc-xlen-forms-v2/case.sexp`  `9f650cb513b49d03d95ae844cbd3331f6907dee9901caa8b84c4ef6cacd8cf67`
     `evidence/rv64gc-xlen-forms-v3/case.sexp`  `4413bd45d71c18f7a8578a7a73502b4825c518876cb5d9aa6a2e2e036160c5b7`
     `evidence/rv64gc-zicntr-v1/case.sexp`  `023bcfe4483801354c55c6857cd7f3698e0ba5f81803a66c0d0b0b00c59659c3`
     `evidence/rv64gc-zicntr-v2/case.sexp`  `82392e36a6a6e3cdcbba9e04127b6921cede895ad5970d73c7ac8ba618361589`
     `evidence/rv64gc-m-forms-v3/case.sexp`  `c1ec1d6555e01108a3cad5139573b4074a83af75f99a501b4b4f27f97cbfb214`
     `evidence/rv64gc-m-forms-v4/case.sexp`  `5e5eba6f4ef2921243371f2fd2b8d030426620286af771b4c769721e461e1e72`
     `evidence/rv64gc-m-forms-v5/case.sexp`  `eb5570b3ceaa812897068a078fe7dc1c1f3eaa6334b0cf96c3b8cb1f96e628f7`
     `evidence/rv64gc-m-forms-v6/case.sexp`  `f4e5adb006ea051599576422792c1efc40d85baa9188c8a01c15102256d57261`
     `evidence/rv64gc-signed-div-truncation-v2/case.sexp`  `66771e68a7a57ea3f87b1cb593e3aa450e09e2c72c58f1cdf779e92ba2ed3d1f`
     `profiles/rv64gc-lab-v0/credits.sexp`  `3f606965ee0192a263980e313f917b89dbd4176367eae713d6698695783f2ac8`
     Generator: `scripts/gen_model_book.py` (sha256 `37c536b0129a0a722773286177f09bf50d623ae65e118bfac58a8b8c345131b2`) -->

| Case | Requirement | Program | Steps | Witnesses | Configuration | State |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-csr-set-v1` | `REQ-D-CSR-SET` | `csr-set.s` | 157 | 53 | its own | history: `rv64gc-csr-set-v2` holds the credit |
| `rv64gc-csr-set-v2` | `REQ-D-CSR-SET` | `csr-set.s` | 157 | 53 | its own | credited, `CR-D-CSR-SET-2` |
| `rv64gc-sstc-v1` | `REQ-D-SSTC` | `sstc-timer.s` | 315 | 39 | its own | credited, `CR-D-SSTC-1` |
| `rv64gc-xlen-forms-v1` | `REQ-D-XLEN` | `xlen-forms.s` | 25 | 17 | the override | history: `rv64gc-xlen-forms-v3` holds the credit |
| `rv64gc-xlen-forms-v2` | `REQ-D-XLEN` | `xlen-forms.s` | 25 | 17 | the override | history: `rv64gc-xlen-forms-v3` holds the credit |
| `rv64gc-xlen-forms-v3` | `REQ-D-XLEN` | `xlen-forms.s` | 25 | 17 | the override | credited, `CR-D-XLEN-3` |
| `rv64gc-zicntr-v1` | `REQ-D-ZICNTR` | `zicntr.s` | 292 | 44 | its own | history: `rv64gc-zicntr-v2` holds the credit |
| `rv64gc-zicntr-v2` | `REQ-D-ZICNTR` | `zicntr.s` | 292 | 44 | its own | credited, `CR-D-ZICNTR-2` |
| `rv64gc-m-forms-v3` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | history: `rv64gc-m-forms-v6` holds the credit |
| `rv64gc-m-forms-v4` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | history: `rv64gc-m-forms-v6` holds the credit |
| `rv64gc-m-forms-v5` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | history: `rv64gc-m-forms-v6` holds the credit |
| `rv64gc-m-forms-v6` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | credited, `CR-GC-M-4` |
| `rv64gc-signed-div-truncation-v2` | `REQ-GC-M` | `m-div.s` | 27 | 1 | the override | history: `rv64gc-m-forms-v6` holds the credit |
