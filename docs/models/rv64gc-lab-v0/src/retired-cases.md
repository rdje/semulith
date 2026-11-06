# Cases retired from the tree

A superseded case credits nothing. The credit moved to its re-capture, no tool reads the old directory, and each one cost a pass of every doctrine that walks `evidence/`. So when the window that carries fetch faults closed, `P4-SYSTEM.14` a49-4 (2026-11-06) took 23 of them out of the tree, with the 16 overlay and effect files named for them: 3,700,566 B and 118,103 B. Two more had left at a49-1, when their guests changed in place.

Nothing was lost. Every byte stays in this repository's history, and `scripts/probe_div_capture_inputs.py` reads each row below back from it on every run: the directory's Git tree, which covers all 22 files, and the measured record's digest. Nothing here was deleted until the new credits were current (`decision_superseded-cases-retired.md`).

The other pages still name these cases where they say what was measured on them. Those are records of what ran; the commands on the pages that you can run today name cases that are in the tree.

## Read one back

The last commit in the table holds the directory:

```console
$ git ls-tree -r 178f9c6c:evidence/rv64gc-sstc-v1 | wc -l
      22
$ git rev-parse 178f9c6c:evidence/rv64gc-sstc-v1
7f9d44d1c946f8b171b8045078c2124684ef6fe8
$ git show 178f9c6c:evidence/rv64gc-sstc-v1/measured-experiment.sexp | shasum -a 256
801b9383ea21b40d582b662233dfc5f8abb3660aa1ed0e2db557261ec20a4396  -
```

## What stays

`rv64gc-signed-div-truncation-v2` and `rv64gc-m-forms-v3` credit nothing either, and they stay. `scripts/matched_gpr_property.py` names them as `CASE_ID` and `M_FORMS_CASE_ID`, the tools' default case and fixture, and that file is pinned by every case's manifest: changing the two names would lapse every credit. They can leave at the next window that has to move that file anyway.

## The cases

"Holds it now" is the case whose current credit answers the same requirement.

| Case | Requirement | Holds it now | Bytes | Last commit | Git tree | `measured-experiment.sexp` sha256 |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-alu-imm-v1` | `REQ-D-ALU-IMM` | `rv64gc-alu-imm-v2` | 107,997 | `8a40a249` | `98af6a7fabd3368862806da71a67c695d870e781` | `27bf858df65b21f4d50eb8b0392baba6b9d99774c9b7327c83d7006fb1e14680` |
| `rv64gc-alu-reg-v1` | `REQ-D-ALU-REG` | `rv64gc-alu-reg-v2` | 103,087 | `8a40a249` | `05a25554e843a040292945fe2ba5bdfe76d15295` | `41ec7ae6db63f83e1269e3803e4c2dcdc2f44c4b1ccf3ad2be348dc87bd094e1` |
| `rv64gc-counters-v1` | `REQ-GC-COUNTERS` | `rv64gc-counters-v2` | 148,286 | `3eb61efd` | `273df4791204506f773e1b97805a2a5f8d45abb2` | `76d4a37bb94ae910f6817a66ae73eca2951e48f98e7fed14a3dfeceee6e108b6` |
| `rv64gc-csr-access-v1` | `REQ-GC-CSR-ACCESS` | `rv64gc-csr-access-v2` | 150,661 | `3eb61efd` | `9d581186ba61a0574c7630f8c9b016e3e5d15b8e` | `b6f7c30b7275e3b0187707d4653f8a2e4c1f450ebf459649747dc5fb7ebc41ee` |
| `rv64gc-csr-set-v1` | `REQ-D-CSR-SET` | `rv64gc-csr-set-v3` | 260,121 | `a6f7d8fd` | `9fa7044bfac67429e7538691991524c253bbe47a` | `a0de4f8c848085eee2534fb7cdaf8a610420ed9866f0cbb7a9e470de38d84ce2` |
| `rv64gc-csr-set-v2` | `REQ-D-CSR-SET` | `rv64gc-csr-set-v3` | 260,135 | `178f9c6c` | `a7bc4ee33954305bf3d128603ad7dee5218841e2` | `d8f18593b02019d49be142daaaac1cfc295c21e5cb4e3256d5507adb98db3b19` |
| `rv64gc-ecall-ebreak-v1` | `REQ-D-ECALL-EBREAK` | `rv64gc-ecall-ebreak-v2` | 190,200 | `3eb61efd` | `d9d92be00c7805e185f36841b2cb6d9cb12efaf1` | `61742b70513c85f5cda60ef4cdb12227f24147649642ee579c439a560cbf68aa` |
| `rv64gc-fencei-v1` | `REQ-GC-FENCEI` | `rv64gc-fencei-v2` | 90,818 | `3eb61efd` | `1116a1ddcf8313933777d0de2a9e9a8bc92e0eac` | `9fc3b954fa305809fe4b65580f3d0d583fe025572b8710aaaf5bb8f9fb99481f` |
| `rv64gc-ialign-16-v1` | `REQ-D-IALIGN-16` | `rv64gc-ialign-16-v2` | 95,282 | `3eb61efd` | `14e0094f750456e5d3e286e2bbd8084daf13bfd9` | `bad8453d8c2f03806ab44d7d85e4cdf6b925eb597cde58e13da2577cccfed19b` |
| `rv64gc-jalr-lsb-v1` | `REQ-D-JALR-LSB` | `rv64gc-jalr-lsb-v2` | 103,443 | `8a40a249` | `30acd5a4ffe8178a240012e7924c5e4c6e30b7e1` | `04ff5c6f8e876365d04f9c7cdd213bec13d8b085b7f0c83941c23abdaf4816ed` |
| `rv64gc-load-ext-v1` | `REQ-D-LOAD-EXT` | `rv64gc-load-ext-v2` | 115,333 | `8a40a249` | `8e6070045a4ba3c2ce2984467806507decae9100` | `bc4b2d3b214f09316a136fbab9ddbd3036581b7326b25563d9c30b13bf0d20a7` |
| `rv64gc-load-x0-v1` | `REQ-D-LOAD-X0` | `rv64gc-load-x0-v2` | 151,917 | `8a40a249` | `5e83a5c14913aac70d3308ba8d5d6e8e5e997edc` | `d5fda2b4c63c5cbcafd88484256046f5b56ee982255961d77c1a1dd493798394` |
| `rv64gc-lui-auipc-v1` | `REQ-D-LUI-AUIPC` | `rv64gc-lui-auipc-v2` | 97,790 | `8a40a249` | `8654ea3ccb9c7941665601f7100fbb899cc77f4c` | `c9e17ce26016f2ffeb8d4a2270391e7d1fa95c0bfdcaa944014c93b966d4775c` |
| `rv64gc-m-forms-v4` | `REQ-GC-M` | `rv64gc-m-forms-v7` | 129,776 | `3c464095` | `8231ce5905fcf1bd4b4aff3cc0a805bb931c79d5` | `aadb5ef3360f1d14a79258522eea098802d492889a747d5be41eeed69e106e08` |
| `rv64gc-m-forms-v5` | `REQ-GC-M` | `rv64gc-m-forms-v7` | 129,869 | `2988d6a2` | `228a6a22686bac607f281e636ca3429341e33b82` | `1530832dd74c83297543d5fb5d1d150633cc3deeb46df7afcac11802ff657f8f` |
| `rv64gc-m-forms-v6` | `REQ-GC-M` | `rv64gc-m-forms-v7` | 129,886 | `178f9c6c` | `9f508dedd1edca08602e44b0d44553fcfa49523c` | `7998edb104616fff0980b41c3ec86eddd675a8ee8c782b6c682639e836497b4d` |
| `rv64gc-no-delay-slots-v1` | `REQ-D-NO-DELAY-SLOTS` | `rv64gc-no-delay-slots-v2` | 109,142 | `8a40a249` | `e96b3d5e83ec49507b079a21f4db07b2b5456007` | `e8d3d2756bba09c615fe016a1c61d3ffd710963f6e15b46112df99d497a0f44e` |
| `rv64gc-shamt-v1` | `REQ-D-SHAMT` | `rv64gc-shamt-v2` | 111,074 | `8a40a249` | `979c3232e724f9ae88b7f909debdf1160d3eb0c2` | `8fad52b38fce525ff8d0a9cce8461cc7cfe93310776f3c1ceb990be858a41120` |
| `rv64gc-sstc-v1` | `REQ-D-SSTC` | `rv64gc-sstc-v2` | 334,066 | `178f9c6c` | `7f9d44d1c946f8b171b8045078c2124684ef6fe8` | `801b9383ea21b40d582b662233dfc5f8abb3660aa1ed0e2db557261ec20a4396` |
| `rv64gc-wsuffix-v1` | `REQ-D-WSUFFIX` | `rv64gc-wsuffix-v2` | 106,748 | `8a40a249` | `a4aebb10f7e4d0237c2b034cd6272354dcd160a5` | `961ce2c73a953c70d1754176b51bf1ae6e0094075fabacef304fffeb53838503` |
| `rv64gc-xlen-forms-v1` | `REQ-D-XLEN` | `rv64gc-xlen-forms-v4` | 118,204 | `e32cc645` | `8687a2d15ac9786b1da07422f181d23a593455fa` | `d39825b0b4d7ccbada20d4d0545f26bb5fce1a79b5003b16dd99997cce041e41` |
| `rv64gc-xlen-forms-v2` | `REQ-D-XLEN` | `rv64gc-xlen-forms-v4` | 118,365 | `2988d6a2` | `95f6db518d74fde9f2089001aa744a499bc825e9` | `3e536d08b739ffd8a1ffd75d9dcf8ca438b4f7f77cb99475718cb41984f58fad` |
| `rv64gc-xlen-forms-v3` | `REQ-D-XLEN` | `rv64gc-xlen-forms-v4` | 118,925 | `178f9c6c` | `d616e5d1a54e414ccd14d761605fe76a0a5dd2d4` | `db2728201e01b4cccb0b51e37ec7f8f29f77d4af22513f16bd400846a520475f` |
| `rv64gc-zicntr-v1` | `REQ-D-ZICNTR` | `rv64gc-zicntr-v3` | 330,453 | `e5814f18` | `ede2ec8c87287540666d0468fe1f281ca8229418` | `723c296705e3aa140c3e4bf13cd22e30e85aa0deef741e3c8aaec7dd212c5b43` |
| `rv64gc-zicntr-v2` | `REQ-D-ZICNTR` | `rv64gc-zicntr-v3` | 330,467 | `178f9c6c` | `3558a240471e4ec8294fa19fb529fbe54986b03e` | `c2b55c2396067f9663ef61a4d9df029ae9261f0af57dbced2133937d5840620f` |

## Their configurations and effects

These sat beside the profile override, named for their cases. The re-captures carry their own, and each retained effect is byte-identical to its predecessor's.

| Path | Bytes | Last commit | sha256 |
| --- | --- | --- | --- |
| `profiles/rv64gc-lab-v0/reference/rv64gc-counters-v1.overlay.sexp` | 602 | `507c3017` | `7d2409195650894956d90725be3bb1deb5a7084d69a69ea500c7cf8ba256bb8e` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-csr-set-v1.effect.sexp` | 762 | `a6f7d8fd` | `1545a8d5066c872536185e4a2f6b3115d7397225eca83c7365b0cc44850e902c` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-csr-set-v1.effect.trace` | 14,236 | `a6f7d8fd` | `2a82805291293290c84cdd0e70ed95e0a29e7596610c0f6d5928849902dcb798` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-csr-set-v1.overlay.sexp` | 928 | `b95a8f66` | `99f851c6ff1c716f60271346f71dcd186fd36a493a97a52981982e45d2b7a2f0` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-csr-set-v2.effect.sexp` | 762 | `178f9c6c` | `426315bdc35f39dcd096e033ce6228625ecd54b0b49dae47254e4465668b8769` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-csr-set-v2.effect.trace` | 14,236 | `178f9c6c` | `2a82805291293290c84cdd0e70ed95e0a29e7596610c0f6d5928849902dcb798` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-csr-set-v2.overlay.sexp` | 928 | `18a09566` | `208fe4ccdb18d442e2332e239c863847ba395d652e0db641d83a7d4c4cc22f6a` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sstc-v1.effect.sexp` | 756 | `178f9c6c` | `a81f3c2fb40b97e7526b80d206612a98519bb1ac20690578cf248f365b6bf386` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sstc-v1.effect.trace` | 25,773 | `178f9c6c` | `2b6738588b6160695e1f3296e0f19fb17c3bc3851d52689404b02e4048806f33` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sstc-v1.overlay.sexp` | 794 | `18a09566` | `cd2a2b01a9bb07da645a4e60c1ed001f90753f89694b63ebec49936dcb032a06` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v1.effect.sexp` | 760 | `e5814f18` | `e5318a0ff1fc2e7d237a4e4b59701b819e23b7b9d3ba30f04914b4c2b00e42cd` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v1.effect.trace` | 27,617 | `e5814f18` | `896814f3f54e1a2bf9af3de7a61e4dac6f831921e7e946c67c28c39362913570` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v1.overlay.sexp` | 786 | `cab19894` | `6836d32f1915cccb1e1277ef9196f84149c68aff07c6faa732f2a28318ac1155` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v2.effect.sexp` | 760 | `178f9c6c` | `6a03a2e8f16902d4163f5d30ebb9b19cda47910ec2530e98ab5421b0b5e11759` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v2.effect.trace` | 27,617 | `178f9c6c` | `896814f3f54e1a2bf9af3de7a61e4dac6f831921e7e946c67c28c39362913570` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v2.overlay.sexp` | 786 | `18a09566` | `80133c4fbecbc07c7f7e7ec455840a2323fb6b7bac526f587c44530b37d4e26d` |
