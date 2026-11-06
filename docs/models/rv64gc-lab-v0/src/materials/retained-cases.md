<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `evidence/rv64gc-alu-imm-v1/case.sexp`  `262519d1dfce9569a250113fc9f59617cb8a800f496abfd5181284e4f77a6319`
     `evidence/rv64gc-alu-reg-v1/case.sexp`  `60eef262735606a23e1773732bca9ed10e0ab4bcf6fe1a528008d7ca146e4168`
     `evidence/rv64gc-csr-set-v1/case.sexp`  `6b45c94b94408be618bb509fa011837708477da59ca1c2246d52cda990d69910`
     `evidence/rv64gc-csr-set-v2/case.sexp`  `90a04d87453670e6ed40a34ce5a18950049a8cff6ee1f612af2f77d8c12885a8`
     `evidence/rv64gc-ecall-ebreak-v1/case.sexp`  `aec8c544b1dbaaaef68da593fd022ab190b9a8385452bf6d8f44c29e270da349`
     `evidence/rv64gc-ialign-16-v1/case.sexp`  `33836ad08c7c2a100b82e98180f4a8eed9a3e8d2c65789682a8f92e8174c8e27`
     `evidence/rv64gc-jalr-lsb-v1/case.sexp`  `222cf99e678db3f3faa3d05758a8d524d64598b618cf8516a5cabdd7cc698dcb`
     `evidence/rv64gc-load-ext-v1/case.sexp`  `e4fd0c831a3feda3b8f4c2c73566399a91f67c51bce0d4950cc66561dab20a19`
     `evidence/rv64gc-load-x0-v1/case.sexp`  `208dc0975d51b30279effdb9ffcaa7176eb440dff5d8b4da06cc90f0a06aa583`
     `evidence/rv64gc-lui-auipc-v1/case.sexp`  `a7ef50652adfb5eeb0032ba4ae078a9b9d014591b94ed877eceae31caf785d9b`
     `evidence/rv64gc-no-delay-slots-v1/case.sexp`  `a5d1c997e6d2d77842a8144bf07668b334303eb01b48f7c186996cf6c913bc01`
     `evidence/rv64gc-shamt-v1/case.sexp`  `fed58b54a83bed46d67782922e62991d38418dac409fc3223da9e07184c8b885`
     `evidence/rv64gc-sstc-v1/case.sexp`  `fd934b35766d8b084aab97735049fedcb6526a539aa58942fb6098d2f5174406`
     `evidence/rv64gc-wsuffix-v1/case.sexp`  `1fc8d98feddd82cacd4b8b4f179db2f53b7a943a37aaf256aa895a2c57cfed4f`
     `evidence/rv64gc-xlen-forms-v1/case.sexp`  `a65f2eef8f4914b969e3547d4344061d3760364bd8d9ff525a8a9875508d1f37`
     `evidence/rv64gc-xlen-forms-v2/case.sexp`  `9f650cb513b49d03d95ae844cbd3331f6907dee9901caa8b84c4ef6cacd8cf67`
     `evidence/rv64gc-xlen-forms-v3/case.sexp`  `4413bd45d71c18f7a8578a7a73502b4825c518876cb5d9aa6a2e2e036160c5b7`
     `evidence/rv64gc-zicntr-v1/case.sexp`  `023bcfe4483801354c55c6857cd7f3698e0ba5f81803a66c0d0b0b00c59659c3`
     `evidence/rv64gc-zicntr-v2/case.sexp`  `82392e36a6a6e3cdcbba9e04127b6921cede895ad5970d73c7ac8ba618361589`
     `evidence/rv64gc-counters-v1/case.sexp`  `0fc939f641407083c14fdf2362720c1093ff933b71325ed65fc823eb0326eb84`
     `evidence/rv64gc-csr-access-v1/case.sexp`  `da3c11618dfb76eec9d6c6699558041f6b8de28172efd9764f56e5ea75fa9175`
     `evidence/rv64gc-fencei-v1/case.sexp`  `62dcfe58656842d5d056c110d0fd65c50e1c9396767e197b8c4af1fc01ea1371`
     `evidence/rv64gc-m-forms-v3/case.sexp`  `c1ec1d6555e01108a3cad5139573b4074a83af75f99a501b4b4f27f97cbfb214`
     `evidence/rv64gc-m-forms-v4/case.sexp`  `5e5eba6f4ef2921243371f2fd2b8d030426620286af771b4c769721e461e1e72`
     `evidence/rv64gc-m-forms-v5/case.sexp`  `eb5570b3ceaa812897068a078fe7dc1c1f3eaa6334b0cf96c3b8cb1f96e628f7`
     `evidence/rv64gc-m-forms-v6/case.sexp`  `f4e5adb006ea051599576422792c1efc40d85baa9188c8a01c15102256d57261`
     `evidence/rv64gc-signed-div-truncation-v2/case.sexp`  `66771e68a7a57ea3f87b1cb593e3aa450e09e2c72c58f1cdf779e92ba2ed3d1f`
     `profiles/rv64gc-lab-v0/credits.sexp`  `3406409acb8819cd3965b80fa8c2f5727b55ef5c1fdc954f00f39b29885a325d`
     Generator: `scripts/gen_model_book.py` (sha256 `37c536b0129a0a722773286177f09bf50d623ae65e118bfac58a8b8c345131b2`) -->

| Case | Requirement | Program | Steps | Witnesses | Configuration | State |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-alu-imm-v1` | `REQ-D-ALU-IMM` | `alu-imm-forms.s` | 19 | 13 | the override | credited, `CR-D-ALU-IMM-1` |
| `rv64gc-alu-reg-v1` | `REQ-D-ALU-REG` | `alu-reg-forms.s` | 18 | 10 | the override | credited, `CR-D-ALU-REG-1` |
| `rv64gc-csr-set-v1` | `REQ-D-CSR-SET` | `csr-set.s` | 157 | 53 | its own | history: `rv64gc-csr-set-v2` holds the credit |
| `rv64gc-csr-set-v2` | `REQ-D-CSR-SET` | `csr-set.s` | 157 | 53 | its own | credited, `CR-D-CSR-SET-2` |
| `rv64gc-ecall-ebreak-v1` | `REQ-D-ECALL-EBREAK` | `ecall-ebreak.s` | 116 | 25 | the override | credited, `CR-D-ECALL-EBREAK-1` |
| `rv64gc-ialign-16-v1` | `REQ-D-IALIGN-16` | `ialign-16.s` | 11 | 6 | the override | credited, `CR-D-IALIGN-16-1` |
| `rv64gc-jalr-lsb-v1` | `REQ-D-JALR-LSB` | `jalr-lsb.s` | 16 | 10 | the override | credited, `CR-D-JALR-LSB-1` |
| `rv64gc-load-ext-v1` | `REQ-D-LOAD-EXT` | `load-ext-forms.s` | 32 | 12 | the override | credited, `CR-D-LOAD-EXT-1` |
| `rv64gc-load-x0-v1` | `REQ-D-LOAD-X0` | `load-x0.s` | 68 | 16 | the override | credited, `CR-D-LOAD-X0-1` |
| `rv64gc-lui-auipc-v1` | `REQ-D-LUI-AUIPC` | `lui-auipc-forms.s` | 10 | 9 | the override | credited, `CR-D-LUI-AUIPC-1` |
| `rv64gc-no-delay-slots-v1` | `REQ-D-NO-DELAY-SLOTS` | `no-delay-slots.s` | 21 | 11 | the override | credited, `CR-D-NO-DELAY-SLOTS-1` |
| `rv64gc-shamt-v1` | `REQ-D-SHAMT` | `shamt-forms.s` | 21 | 15 | the override | credited, `CR-D-SHAMT-1` |
| `rv64gc-sstc-v1` | `REQ-D-SSTC` | `sstc-timer.s` | 315 | 39 | its own | credited, `CR-D-SSTC-1` |
| `rv64gc-wsuffix-v1` | `REQ-D-WSUFFIX` | `wsuffix-forms.s` | 17 | 12 | the override | credited, `CR-D-WSUFFIX-1` |
| `rv64gc-xlen-forms-v1` | `REQ-D-XLEN` | `xlen-forms.s` | 25 | 17 | the override | history: `rv64gc-xlen-forms-v3` holds the credit |
| `rv64gc-xlen-forms-v2` | `REQ-D-XLEN` | `xlen-forms.s` | 25 | 17 | the override | history: `rv64gc-xlen-forms-v3` holds the credit |
| `rv64gc-xlen-forms-v3` | `REQ-D-XLEN` | `xlen-forms.s` | 25 | 17 | the override | credited, `CR-D-XLEN-3` |
| `rv64gc-zicntr-v1` | `REQ-D-ZICNTR` | `zicntr.s` | 292 | 44 | its own | history: `rv64gc-zicntr-v2` holds the credit |
| `rv64gc-zicntr-v2` | `REQ-D-ZICNTR` | `zicntr.s` | 292 | 44 | its own | credited, `CR-D-ZICNTR-2` |
| `rv64gc-counters-v1` | `REQ-GC-COUNTERS` | `counters-reads.s` | 84 | 8 | its own | credited, `CR-GC-COUNTERS-1` |
| `rv64gc-csr-access-v1` | `REQ-GC-CSR-ACCESS` | `csr-access.s` | 66 | 21 | the override | credited, `CR-GC-CSR-ACCESS-1` |
| `rv64gc-fencei-v1` | `REQ-GC-FENCEI` | `fencei-forms.s` | 10 | 2 | the override | credited, `CR-GC-FENCEI-1` |
| `rv64gc-m-forms-v3` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | history: `rv64gc-m-forms-v6` holds the credit |
| `rv64gc-m-forms-v4` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | history: `rv64gc-m-forms-v6` holds the credit |
| `rv64gc-m-forms-v5` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | history: `rv64gc-m-forms-v6` holds the credit |
| `rv64gc-m-forms-v6` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | credited, `CR-GC-M-4` |
| `rv64gc-signed-div-truncation-v2` | `REQ-GC-M` | `m-div.s` | 27 | 1 | the override | history: `rv64gc-m-forms-v6` holds the credit |
