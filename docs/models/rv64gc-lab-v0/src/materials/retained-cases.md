<!-- GENERATED — do not edit (OWN-03). Regenerate with
     `python3 scripts/gen_model_book.py`; drift between this fragment and the
     pinned dossier is refused by the MATERIALS-BILL doctrine
     (`scripts/check_materials_bill.sh`). -->
<!-- Canonical inputs (sha256):
     `evidence/rv64gc-alu-imm-v2/case.sexp`  `a4b99e6afb752baf69178c47d1ccb010e964030b49678037abf20e834369038b`
     `evidence/rv64gc-alu-reg-v2/case.sexp`  `9910a540f4d2bb13c3e8965c5566ed1404a883eff91576ec4895aaa00848913e`
     `evidence/rv64gc-csr-set-v3/case.sexp`  `7a1fd28c6f114faaea46eab2b0b21ea841cf26ab7aadca502fd9643c42d36d3b`
     `evidence/rv64gc-ecall-ebreak-v2/case.sexp`  `f004f6a35575c926a0ddea8f9695d712aee99b1313366ab14d16b3c160d4afe8`
     `evidence/rv64gc-ialign-16-v2/case.sexp`  `80745a518ea804f74f1d6589b5ef87e2a2f702ba82ac634f88ce4ae76ee1fa67`
     `evidence/rv64gc-jalr-lsb-v2/case.sexp`  `eb24c6f7c9acd56c44693c0dcd5f41a26a583a2ac556da508c749a4469f1b1ab`
     `evidence/rv64gc-load-ext-v2/case.sexp`  `cd0c272fbcfdede63ebca40021baf78f966f312c9efd21b7bf37b0914b84ee97`
     `evidence/rv64gc-load-x0-v2/case.sexp`  `0ff8361b06d1da6b9275be6b128c7dc0dc7081c7234881760e3188ebb975c20f`
     `evidence/rv64gc-lui-auipc-v2/case.sexp`  `d334c6738ec2e09112290058945dded89144ce36981c80af22b344ca53e04271`
     `evidence/rv64gc-no-delay-slots-v2/case.sexp`  `3c50a122924b2e6c9a1c065ffc79f75cf169f2b8e2ce0373cb9aaac3535a8e04`
     `evidence/rv64gc-shamt-v2/case.sexp`  `70a5522615fd915d0c3fa70fe7a0ba994d69448324c08703402d1849e7d769c2`
     `evidence/rv64gc-sstc-v2/case.sexp`  `824b0469a99d4e21d2ded2614f97f9b394b26bd7e2ac3f8640e73f95bb05f2da`
     `evidence/rv64gc-wsuffix-v2/case.sexp`  `b3173ce5533cba9285d1f4be08117d636ef5cb28b8a685907c234e231f90a87f`
     `evidence/rv64gc-xlen-forms-v4/case.sexp`  `e9703d49debc6429e56d5f99cbbd7491f8b13a9ca48a5031503bba7b28c529f7`
     `evidence/rv64gc-zicntr-v3/case.sexp`  `e109f756175cfa6e2c47cd4ca5571a9a34ef58d908ce1c1d27738484cabae7e2`
     `evidence/rv64gc-atomics-v1/case.sexp`  `6eb6381818da766616521b50b54515e57d364e899618c05aa1b4667165390f47`
     `evidence/rv64gc-c-forms-v1/case.sexp`  `a29db3681c31aaac4dae0b903dce48bd3c4ae828d806540254b7a76ab6ba62c6`
     `evidence/rv64gc-counters-v2/case.sexp`  `9ba862ba08f8a1bd5665a50f625b24f99225229a72a198fbbc91dfb6c5e1f31f`
     `evidence/rv64gc-csr-access-v2/case.sexp`  `e080c6bf539a8f99bcc995d58af57e0db916ebfa37945ecfe45784fc554895b4`
     `evidence/rv64gc-d-forms-v1/case.sexp`  `9593235dc5201524892220310da87168dcbb09c7acc7a7a9f7a1f4d7011da504`
     `evidence/rv64gc-f-forms-v1/case.sexp`  `3c70559e6af2a77ea3dd99fc6612612d8a4fbca27b484635f139141cb8d2f6b4`
     `evidence/rv64gc-fencei-v2/case.sexp`  `4c16107a99717b64d7ba8460f5c689ffc8fb0c5c8922fac36c9dbfae03241d62`
     `evidence/rv64gc-m-forms-v3/case.sexp`  `c1ec1d6555e01108a3cad5139573b4074a83af75f99a501b4b4f27f97cbfb214`
     `evidence/rv64gc-m-forms-v7/case.sexp`  `e517eeb6f09d7a0b8e4750309458918ee6c2e2b41740e2d1e2bc029a527d5c3e`
     `evidence/rv64gc-signed-div-truncation-v2/case.sexp`  `66771e68a7a57ea3f87b1cb593e3aa450e09e2c72c58f1cdf779e92ba2ed3d1f`
     `profiles/rv64gc-lab-v0/credits.sexp`  `9dc7f096193cc529e3106cd5c6664830feae10d881217ab79cb79b995376166c`
     Generator: `scripts/gen_model_book.py` (sha256 `100cb1b47e94428bce6af762e34fa1546e4b3f16690a4195d80d774929f852ed`) -->

| Case | Requirement | Program | Steps | Witnesses | Configuration | State |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-alu-imm-v2` | `REQ-D-ALU-IMM` | `alu-imm-forms.s` | 19 | 13 | the override | credited, `CR-D-ALU-IMM-2` |
| `rv64gc-alu-reg-v2` | `REQ-D-ALU-REG` | `alu-reg-forms.s` | 18 | 10 | the override | credited, `CR-D-ALU-REG-2` |
| `rv64gc-csr-set-v3` | `REQ-D-CSR-SET` | `csr-set.s` | 157 | 53 | its own | credited, `CR-D-CSR-SET-3` |
| `rv64gc-ecall-ebreak-v2` | `REQ-D-ECALL-EBREAK` | `ecall-ebreak.s` | 116 | 25 | the override | credited, `CR-D-ECALL-EBREAK-2` |
| `rv64gc-ialign-16-v2` | `REQ-D-IALIGN-16` | `ialign-16.s` | 11 | 6 | the override | credited, `CR-D-IALIGN-16-2` |
| `rv64gc-jalr-lsb-v2` | `REQ-D-JALR-LSB` | `jalr-lsb.s` | 16 | 10 | the override | credited, `CR-D-JALR-LSB-2` |
| `rv64gc-load-ext-v2` | `REQ-D-LOAD-EXT` | `load-ext-forms.s` | 32 | 12 | the override | credited, `CR-D-LOAD-EXT-2` |
| `rv64gc-load-x0-v2` | `REQ-D-LOAD-X0` | `load-x0.s` | 68 | 16 | the override | credited, `CR-D-LOAD-X0-2` |
| `rv64gc-lui-auipc-v2` | `REQ-D-LUI-AUIPC` | `lui-auipc-forms.s` | 10 | 9 | the override | credited, `CR-D-LUI-AUIPC-2` |
| `rv64gc-no-delay-slots-v2` | `REQ-D-NO-DELAY-SLOTS` | `no-delay-slots.s` | 21 | 11 | the override | credited, `CR-D-NO-DELAY-SLOTS-2` |
| `rv64gc-shamt-v2` | `REQ-D-SHAMT` | `shamt-forms.s` | 21 | 15 | the override | credited, `CR-D-SHAMT-2` |
| `rv64gc-sstc-v2` | `REQ-D-SSTC` | `sstc-timer.s` | 315 | 39 | its own | credited, `CR-D-SSTC-2` |
| `rv64gc-wsuffix-v2` | `REQ-D-WSUFFIX` | `wsuffix-forms.s` | 17 | 12 | the override | credited, `CR-D-WSUFFIX-2` |
| `rv64gc-xlen-forms-v4` | `REQ-D-XLEN` | `xlen-forms.s` | 25 | 17 | the override | credited, `CR-D-XLEN-4` |
| `rv64gc-zicntr-v3` | `REQ-D-ZICNTR` | `zicntr.s` | 292 | 44 | its own | credited, `CR-D-ZICNTR-3` |
| `rv64gc-atomics-v1` | `REQ-GC-ATOMICS` | `atomics-forms.s` | 246 | 64 | the override | credited, `CR-GC-ATOMICS-1` |
| `rv64gc-c-forms-v1` | `REQ-GC-C` | `c-forms.s` | 251 | 52 | the override | credited, `CR-GC-C-1` |
| `rv64gc-counters-v2` | `REQ-GC-COUNTERS` | `counters-reads.s` | 84 | 8 | its own | credited, `CR-GC-COUNTERS-2` |
| `rv64gc-csr-access-v2` | `REQ-GC-CSR-ACCESS` | `csr-access.s` | 81 | 25 | the override | credited, `CR-GC-CSR-ACCESS-2` |
| `rv64gc-d-forms-v1` | `REQ-GC-D` | `d-forms.s` | 350 | 93 | the override | credited, `CR-GC-D-1` |
| `rv64gc-f-forms-v1` | `REQ-GC-F` | `f-forms.s` | 338 | 90 | the override | credited, `CR-GC-F-1` |
| `rv64gc-fencei-v2` | `REQ-GC-FENCEI` | `fencei-forms.s` | 18 | 4 | the override | credited, `CR-GC-FENCEI-2` |
| `rv64gc-m-forms-v3` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | history: `rv64gc-m-forms-v7` holds the credit |
| `rv64gc-m-forms-v7` | `REQ-GC-M` | `m-forms.s` | 33 | 25 | the override | credited, `CR-GC-M-5` |
| `rv64gc-signed-div-truncation-v2` | `REQ-GC-M` | `m-div.s` | 27 | 1 | the override | history: `rv64gc-m-forms-v7` holds the credit |
