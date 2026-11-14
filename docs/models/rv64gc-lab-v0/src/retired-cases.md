# Cases retired from the tree

A superseded case credits nothing. The credit moved to its re-capture, no tool reads the old directory, and each one cost a pass of every doctrine that walks `evidence/`. So when the window that carries fetch faults closed, `P4-SYSTEM.14` a49-4 (2026-11-06) took 23 of them out of the tree, with the 16 overlay and effect files named for them: 3,700,566 B and 118,103 B. Two more had left at a49-1, when their guests changed in place. In version 1's window, `P4-SYSTEM.20` slice f1 (2026-11-14) took 40 more out, with the 40 configuration, effect and walk files named for them, 7,214,757 B and 193,715 B, in the commit that declared their successors. Two leave once their successors are captured, since a tool reads what they captured: `rv64gc-m-forms-v7`, the review tools' default case, and `rv64gc-csr-set-v3`, whose trace the configuration-effect probe replays.

Nothing was lost. Every byte stays in this repository's history, and `scripts/probe_div_capture_inputs.py` reads each row below back from it on every run: the directory's Git tree, which covers all 22 files, and the measured record's digest. The first 25 left once the new credits were current (`decision_superseded-cases-retired.md`). Since version 1's window a case leaves in the commit that declares its successor, and its history holds it just the same (`decision_a-predecessor-leaves-when-its-successor-is-declared.md`).

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

"Holds it now" is the case that answers the same requirement now: its credit, or, until slice f3 re-issues the credits of version 1's window, its declaration.

| Case | Requirement | Holds it now | Bytes | Last commit | Git tree | `measured-experiment.sexp` sha256 |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-alu-imm-v1` | `REQ-D-ALU-IMM` | `rv64gc-alu-imm-v3` | 107,997 | `8a40a249` | `98af6a7fabd3368862806da71a67c695d870e781` | `27bf858df65b21f4d50eb8b0392baba6b9d99774c9b7327c83d7006fb1e14680` |
| `rv64gc-alu-reg-v1` | `REQ-D-ALU-REG` | `rv64gc-alu-reg-v3` | 103,087 | `8a40a249` | `05a25554e843a040292945fe2ba5bdfe76d15295` | `41ec7ae6db63f83e1269e3803e4c2dcdc2f44c4b1ccf3ad2be348dc87bd094e1` |
| `rv64gc-counters-v1` | `REQ-GC-COUNTERS` | `rv64gc-counters-v3` | 148,286 | `3eb61efd` | `273df4791204506f773e1b97805a2a5f8d45abb2` | `76d4a37bb94ae910f6817a66ae73eca2951e48f98e7fed14a3dfeceee6e108b6` |
| `rv64gc-csr-access-v1` | `REQ-GC-CSR-ACCESS` | `rv64gc-csr-access-v3` | 150,661 | `3eb61efd` | `9d581186ba61a0574c7630f8c9b016e3e5d15b8e` | `b6f7c30b7275e3b0187707d4653f8a2e4c1f450ebf459649747dc5fb7ebc41ee` |
| `rv64gc-csr-set-v1` | `REQ-D-CSR-SET` | `rv64gc-csr-set-v4` | 260,121 | `a6f7d8fd` | `9fa7044bfac67429e7538691991524c253bbe47a` | `a0de4f8c848085eee2534fb7cdaf8a610420ed9866f0cbb7a9e470de38d84ce2` |
| `rv64gc-csr-set-v2` | `REQ-D-CSR-SET` | `rv64gc-csr-set-v4` | 260,135 | `178f9c6c` | `a7bc4ee33954305bf3d128603ad7dee5218841e2` | `d8f18593b02019d49be142daaaac1cfc295c21e5cb4e3256d5507adb98db3b19` |
| `rv64gc-ecall-ebreak-v1` | `REQ-D-ECALL-EBREAK` | `rv64gc-ecall-ebreak-v3` | 190,200 | `3eb61efd` | `d9d92be00c7805e185f36841b2cb6d9cb12efaf1` | `61742b70513c85f5cda60ef4cdb12227f24147649642ee579c439a560cbf68aa` |
| `rv64gc-fencei-v1` | `REQ-GC-FENCEI` | `rv64gc-fencei-v3` | 90,818 | `3eb61efd` | `1116a1ddcf8313933777d0de2a9e9a8bc92e0eac` | `9fc3b954fa305809fe4b65580f3d0d583fe025572b8710aaaf5bb8f9fb99481f` |
| `rv64gc-ialign-16-v1` | `REQ-D-IALIGN-16` | `rv64gc-ialign-16-v3` | 95,282 | `3eb61efd` | `14e0094f750456e5d3e286e2bbd8084daf13bfd9` | `bad8453d8c2f03806ab44d7d85e4cdf6b925eb597cde58e13da2577cccfed19b` |
| `rv64gc-jalr-lsb-v1` | `REQ-D-JALR-LSB` | `rv64gc-jalr-lsb-v3` | 103,443 | `8a40a249` | `30acd5a4ffe8178a240012e7924c5e4c6e30b7e1` | `04ff5c6f8e876365d04f9c7cdd213bec13d8b085b7f0c83941c23abdaf4816ed` |
| `rv64gc-load-ext-v1` | `REQ-D-LOAD-EXT` | `rv64gc-load-ext-v3` | 115,333 | `8a40a249` | `8e6070045a4ba3c2ce2984467806507decae9100` | `bc4b2d3b214f09316a136fbab9ddbd3036581b7326b25563d9c30b13bf0d20a7` |
| `rv64gc-load-x0-v1` | `REQ-D-LOAD-X0` | `rv64gc-load-x0-v3` | 151,917 | `8a40a249` | `5e83a5c14913aac70d3308ba8d5d6e8e5e997edc` | `d5fda2b4c63c5cbcafd88484256046f5b56ee982255961d77c1a1dd493798394` |
| `rv64gc-lui-auipc-v1` | `REQ-D-LUI-AUIPC` | `rv64gc-lui-auipc-v3` | 97,790 | `8a40a249` | `8654ea3ccb9c7941665601f7100fbb899cc77f4c` | `c9e17ce26016f2ffeb8d4a2270391e7d1fa95c0bfdcaa944014c93b966d4775c` |
| `rv64gc-m-forms-v4` | `REQ-GC-M` | `rv64gc-m-forms-v8` | 129,776 | `3c464095` | `8231ce5905fcf1bd4b4aff3cc0a805bb931c79d5` | `aadb5ef3360f1d14a79258522eea098802d492889a747d5be41eeed69e106e08` |
| `rv64gc-m-forms-v5` | `REQ-GC-M` | `rv64gc-m-forms-v8` | 129,869 | `2988d6a2` | `228a6a22686bac607f281e636ca3429341e33b82` | `1530832dd74c83297543d5fb5d1d150633cc3deeb46df7afcac11802ff657f8f` |
| `rv64gc-m-forms-v6` | `REQ-GC-M` | `rv64gc-m-forms-v8` | 129,886 | `178f9c6c` | `9f508dedd1edca08602e44b0d44553fcfa49523c` | `7998edb104616fff0980b41c3ec86eddd675a8ee8c782b6c682639e836497b4d` |
| `rv64gc-no-delay-slots-v1` | `REQ-D-NO-DELAY-SLOTS` | `rv64gc-no-delay-slots-v3` | 109,142 | `8a40a249` | `e96b3d5e83ec49507b079a21f4db07b2b5456007` | `e8d3d2756bba09c615fe016a1c61d3ffd710963f6e15b46112df99d497a0f44e` |
| `rv64gc-shamt-v1` | `REQ-D-SHAMT` | `rv64gc-shamt-v3` | 111,074 | `8a40a249` | `979c3232e724f9ae88b7f909debdf1160d3eb0c2` | `8fad52b38fce525ff8d0a9cce8461cc7cfe93310776f3c1ceb990be858a41120` |
| `rv64gc-sstc-v1` | `REQ-D-SSTC` | `rv64gc-sstc-v3` | 334,066 | `178f9c6c` | `7f9d44d1c946f8b171b8045078c2124684ef6fe8` | `801b9383ea21b40d582b662233dfc5f8abb3660aa1ed0e2db557261ec20a4396` |
| `rv64gc-wsuffix-v1` | `REQ-D-WSUFFIX` | `rv64gc-wsuffix-v3` | 106,748 | `8a40a249` | `a4aebb10f7e4d0237c2b034cd6272354dcd160a5` | `961ce2c73a953c70d1754176b51bf1ae6e0094075fabacef304fffeb53838503` |
| `rv64gc-xlen-forms-v1` | `REQ-D-XLEN` | `rv64gc-xlen-forms-v5` | 118,204 | `e32cc645` | `8687a2d15ac9786b1da07422f181d23a593455fa` | `d39825b0b4d7ccbada20d4d0545f26bb5fce1a79b5003b16dd99997cce041e41` |
| `rv64gc-xlen-forms-v2` | `REQ-D-XLEN` | `rv64gc-xlen-forms-v5` | 118,365 | `2988d6a2` | `95f6db518d74fde9f2089001aa744a499bc825e9` | `3e536d08b739ffd8a1ffd75d9dcf8ca438b4f7f77cb99475718cb41984f58fad` |
| `rv64gc-xlen-forms-v3` | `REQ-D-XLEN` | `rv64gc-xlen-forms-v5` | 118,925 | `178f9c6c` | `d616e5d1a54e414ccd14d761605fe76a0a5dd2d4` | `db2728201e01b4cccb0b51e37ec7f8f29f77d4af22513f16bd400846a520475f` |
| `rv64gc-zicntr-v1` | `REQ-D-ZICNTR` | `rv64gc-zicntr-v4` | 330,453 | `e5814f18` | `ede2ec8c87287540666d0468fe1f281ca8229418` | `723c296705e3aa140c3e4bf13cd22e30e85aa0deef741e3c8aaec7dd212c5b43` |
| `rv64gc-zicntr-v2` | `REQ-D-ZICNTR` | `rv64gc-zicntr-v4` | 330,467 | `178f9c6c` | `3558a240471e4ec8294fa19fb529fbe54986b03e` | `c2b55c2396067f9663ef61a4d9df029ae9261f0af57dbced2133937d5840620f` |
| `rv64gc-alu-imm-v2` | `REQ-D-ALU-IMM` | `rv64gc-alu-imm-v3` | 107,997 | `228c9d76` | `3ade7ba788431f10c8945d9bd74549db3f4485b4` | `d8159cefb9e8ddd209d8aa9205be6499a69b99c00ee9600b6547bf4bd91c7624` |
| `rv64gc-alu-reg-v2` | `REQ-D-ALU-REG` | `rv64gc-alu-reg-v3` | 103,087 | `228c9d76` | `7a3a08a41a1335563bf073009465e6f1c5c6bef8` | `fc17ca34d3ca147cff3bd1812f184b16a398555a02e244385a5e02086001f1de` |
| `rv64gc-c-forms-v1` | `REQ-GC-C` | `rv64gc-c-forms-v2` | 300,837 | `228c9d76` | `6af6d3bf1d64991e1f205176a25ce118553bad0f` | `a8795ba63d55ec942cb8786f99651b90bb09addc0a0633be6d8a16e20f6362c5` |
| `rv64gc-atomic-misalign-v1` | `REQ-D-ATOMIC-MISALIGN` | `rv64gc-atomic-misalign-v2` | 240,573 | `228c9d76` | `77fd9430fa5161a37fbe548ebb51ed58b9123caa` | `a78b331867bc0ca445acee6039303d7f2fe1eccf01f167a9fd44a29a8449c5e1` |
| `rv64gc-composition-v1` | `REQ-D-GC-COMPOSITION` | `rv64gc-composition-v2` | 120,409 | `228c9d76` | `a4fc7a5776d8ab44112597d49d3ff0aa1b5cecf1` | `d6a4446a9d07fc5933a2cc276973b6d89e56193370ae0b3e032c42773111395c` |
| `rv64gc-atomics-v1` | `REQ-GC-ATOMICS` | `rv64gc-atomics-v2` | 310,003 | `228c9d76` | `88b79e9ef90aa48281d8e219f75f26f5d703c6a9` | `a9c6a2f0256b40fa38c8c42661b7840cc0abc75b727d6469bbaa7331e24f2896` |
| `rv64gc-counters-v2` | `REQ-GC-COUNTERS` | `rv64gc-counters-v3` | 148,286 | `228c9d76` | `1da458a5aa00526526cb038c6bf4da68805b5e48` | `3aa72b511c401a619fb37085218c754629020a156b5e90fa459ecec9bec7e364` |
| `rv64gc-csr-access-v2` | `REQ-GC-CSR-ACCESS` | `rv64gc-csr-access-v3` | 165,757 | `228c9d76` | `9acf16c02df8ecf00f9968a20d9ec2a3ea842174` | `20f7d58dabe54d5636d6abbfeec581a6c0a2c50eb91b660232d81773383b2b9c` |
| `rv64gc-d-forms-v1` | `REQ-GC-D` | `rv64gc-d-forms-v2` | 401,449 | `228c9d76` | `269cfe9aa74a9e94ea66b941e27e741205fe4bd3` | `ab0630356bad8822b6d18a0bda62619680fff9091f32a6a1e1e9aeb7c57acb9b` |
| `rv64gc-ext-closure-v1` | `REQ-D-EXT-CLOSURE` | `rv64gc-ext-closure-v2` | 135,924 | `228c9d76` | `4b1830f86f5f84bd64af3022ba428fa29a1674de` | `c74bf7c641c3dffa13fb8070b06f3fdf5c8e97c92385bd53ff1e42666fd6cd82` |
| `rv64gc-ecall-ebreak-v2` | `REQ-D-ECALL-EBREAK` | `rv64gc-ecall-ebreak-v3` | 190,200 | `228c9d76` | `b5799578021e3da0cbc9f7dafddabeabc53080da` | `ed55336b939390102d1b8956e67f7b8a4cd3e56c924dbc1326e2096a735e0134` |
| `rv64gc-endian-v1` | `REQ-D-ENDIAN` | `rv64gc-endian-v2` | 118,060 | `228c9d76` | `d5ad1c55c3638291e6ad292b62a77ae61e903a1e` | `f1519eb530e37b0ebf23216ad579fcf2fa894b9f52c17af7a90e6e74c9b22bbb` |
| `rv64gc-f-forms-v1` | `REQ-GC-F` | `rv64gc-f-forms-v2` | 389,704 | `228c9d76` | `71b1114e8bff4a0c8c6d52d329350e70bdc5d085` | `098f2565f8045da5eaf1f5f75b6a2fd2b942c275175cabfa7fdf378894da9f99` |
| `rv64gc-fencei-v2` | `REQ-GC-FENCEI` | `rv64gc-fencei-v3` | 99,195 | `228c9d76` | `a8015efa3e4fbe4209af99129fa0fda905bb2ffe` | `bf596e7c7944ed142d09c4201b0e60622f920a2f82befacecc1b676c37bbf963` |
| `rv64gc-fence-v1` | `REQ-D-FENCE` | `rv64gc-fence-v2` | 119,327 | `228c9d76` | `10cd23a3ef20053c93aaffc9641f17a5e6e3359f` | `ba631299a09d72809a3f04ceea00aac23b159f42b298b1f41603b93639fb9ef9` |
| `rv64gc-fault-priority-v1` | `REQ-D-FAULT-PRIORITY` | `rv64gc-fault-priority-v2` | 316,861 | `228c9d76` | `7ae3c9f208204f9d69295c60271ee30ddee75ee2` | `884f71918f6fecca4042341d0973668244b0b3ee4990f89847769520f62cc440` |
| `rv64gc-ialign-16-v2` | `REQ-D-IALIGN-16` | `rv64gc-ialign-16-v3` | 95,393 | `228c9d76` | `cc169675ea3f47b97bd1ac35af4d67860ab14d12` | `3a6a0f30be5173c6f7b9b99c59d7f843098bb25264e5404f654edbc86a29d387` |
| `rv64gc-load-x0-v2` | `REQ-D-LOAD-X0` | `rv64gc-load-x0-v3` | 151,917 | `228c9d76` | `79d2de03d2f43bad6f273aded54caa2d76e56a1a` | `de9b732a58b0f1f69690fa4ee6b892796db1fb881d1845dcf29408622d4f184b` |
| `rv64gc-load-ext-v2` | `REQ-D-LOAD-EXT` | `rv64gc-load-ext-v3` | 115,333 | `228c9d76` | `f87f7a8c97b0aa2f2422e5114eab4048085d1ca7` | `c93bdd565a20a629e7e311b2a083833a2973b7ddcfb371904ee50d9fda6c80ba` |
| `rv64gc-jalr-lsb-v2` | `REQ-D-JALR-LSB` | `rv64gc-jalr-lsb-v3` | 103,443 | `228c9d76` | `b33e083c220289143ebc63a4e3058c00f2ea22a9` | `c4856561e770ab01887f80e227d08fb3158c2e790782c6747e5cc57a5680dbc0` |
| `rv64gc-lui-auipc-v2` | `REQ-D-LUI-AUIPC` | `rv64gc-lui-auipc-v3` | 97,790 | `228c9d76` | `782e4b7ec1ffab2a65a29b6abd801f69fbb13c92` | `3bd11dba2f5b9e7bad63cc4e30af7bba7a8751c5b83ee138aa35679a9f17e520` |
| `rv64gc-no-delay-slots-v2` | `REQ-D-NO-DELAY-SLOTS` | `rv64gc-no-delay-slots-v3` | 109,142 | `228c9d76` | `bae6001296f9911e2087b66debfa4244253fa3a9` | `6c12cb8b6adff8049d57518bd08eac50bf79d680ff9257d40acc60ade530397e` |
| `rv64gc-no-h-v1` | `REQ-D-NO-H` | `rv64gc-no-h-v2` | 100,119 | `228c9d76` | `7143bab1f8f172f088a7342b288843e67c16c186` | `0f6a17552aedb68de0aeb09af4d2f8d11d8815e0baa0da08957678738e00c158` |
| `rv64gc-partial-progress-v1` | `REQ-GC-PARTIAL-PROGRESS` | `rv64gc-partial-progress-v2` | 220,174 | `228c9d76` | `7e9d4982b79425d08a82f7b68352e57d0ed7e76a` | `e6ae0e6a333fc3f6566aa759d9c86121a9c5a231ed5d4a8b08df17e6c0e9e09d` |
| `rv64gc-priv-forms-v1` | `REQ-GC-PRIV-INSNS` | `rv64gc-priv-forms-v2` | 347,089 | `228c9d76` | `07506db43d6029e44ec429d5749fa03fbb57ac6c` | `79e752e4f8976dd39bf5bacc92012e85b783bbfde3c8aedfe297d6c2055193f5` |
| `rv64gc-no-pmp-v1` | `REQ-D-NO-PMP` | `rv64gc-no-pmp-v2` | 113,145 | `228c9d76` | `8efd761f70818eea500c74f04bbc96381edc317a` | `8e6da2e5d1cf7f598704b0c019cb48b57d9812e4f114ec5b11bf03270c334f5e` |
| `rv64gc-priv-insns-v1` | `REQ-D-PRIV-INSNS` | `rv64gc-priv-insns-v2` | 104,564 | `228c9d76` | `cd6a6676d2dfc8526dfb160079ad7dac05044644` | `5aaf71559610c6d61b04a883d969a51b29fb44ffd943aed0e7fd31dd043c2192` |
| `rv64gc-reservation-v1` | `REQ-D-RESERVATION` | `rv64gc-reservation-v2` | 235,568 | `228c9d76` | `7d4e9eb4c4d9a4632a5fba91195f2156d8447de4` | `9704f8d4b35857ea7006fcb0f863ca055f18cb12b67f9c4e997776e36d3da5b3` |
| `rv64gc-priv-revision-v1` | `REQ-D-PRIV-REVISION` | `rv64gc-priv-revision-v2` | 111,537 | `228c9d76` | `2702b3cf52b2e263eb7db4a2b7f1605f8e48a9d2` | `224522d8f20effca248ba8233c1060589241977f5ec9b641fbb8a87783776ea2` |
| `rv64gc-priv-modes-v1` | `REQ-D-PRIV-MODES` | `rv64gc-priv-modes-v2` | 173,693 | `228c9d76` | `3f4082d3464d6c8d7381a49dd53be5157b496633` | `c25f84eab25b567be5174fe56ea5b7ae857fcc9f5d6600a307a7d84a6594159a` |
| `rv64gc-rvwmo-v1` | `REQ-D-RVWMO` | `rv64gc-rvwmo-v2` | 113,333 | `228c9d76` | `ef21a0206d002e5ef01442bd1a0cc3d0f234fa51` | `889d11ea2aa3912049e976970792410f68f0b8e9f98c0c9ecbcf9e6c26ad33e4` |
| `rv64gc-shamt-v2` | `REQ-D-SHAMT` | `rv64gc-shamt-v3` | 111,074 | `228c9d76` | `40e056c478b56d752f6a34f93aa6a32b611060ac` | `84c147cd2a7aeac6cfcba8fb99530ecdfa0fd8a00afe03bfa1fab855136e26e8` |
| `rv64gc-sc-deterministic-v1` | `REQ-D-SC-DETERMINISTIC` | `rv64gc-sc-deterministic-v2` | 214,599 | `228c9d76` | `b7d63c75353ec7f5f9ae298a83dfe6a4cc1a17d2` | `d956f455bbaff00e22184e4c1fc884f5f7dbcf5915b3fcfad1fdc63f2ce224dd` |
| `rv64gc-walk-implicit-v1` | `REQ-D-WALK-IMPLICIT` | `rv64gc-walk-implicit-v2` | 155,701 | `228c9d76` | `7cd66c1044d44dd3c3286b395e3a35b1fe6e66c4` | `a1652370c5748e2bbafe5d797d380d1c1b24cfe71011a20a599f5cfa6978ce7f` |
| `rv64gc-svade-v1` | `REQ-D-SVADE` | `rv64gc-svade-v2` | 193,146 | `228c9d76` | `99011bb2a0ebff3cafaa194923e94acd63863f93` | `d0ad7094446b2caaf54b471d5ce55aaf115c2a9bc59349e5e91bc622c41e8116` |
| `rv64gc-sv39-v1` | `REQ-D-SV39` | `rv64gc-sv39-v2` | 190,113 | `228c9d76` | `b4a7bbba5971abaec9d0621ea2653d50cf5f4cf2` | `62ea14c63686b70c5761ba046967ecca485b70eafb8ed3bb0994014828ed79f7` |
| `rv64gc-sstc-v2` | `REQ-D-SSTC` | `rv64gc-sstc-v3` | 334,069 | `228c9d76` | `7757da93bfe32846b7079cae1b039507f01e1f7d` | `0c84e833b2862001263d74210105dabb36219483f5d6e7bf65fb69477a2ed1a8` |
| `rv64gc-zicntr-v3` | `REQ-D-ZICNTR` | `rv64gc-zicntr-v4` | 330,470 | `228c9d76` | `83c77ffae845b3cd3d7471d7ea6a6257103c64f4` | `88b6adfb8b78c0bbba0ffafc8709784242fd24415bb36e411434733501f90a6a` |
| `rv64gc-xlen-forms-v4` | `REQ-D-XLEN` | `rv64gc-xlen-forms-v5` | 118,928 | `228c9d76` | `f68afa630d2b708ff930a58eb28c33871ac99f5f` | `0b87cbce6ce388e25523a05262ab432d77625a3242c201b51a72504a98cd5342` |
| `rv64gc-wsuffix-v2` | `REQ-D-WSUFFIX` | `rv64gc-wsuffix-v3` | 106,748 | `228c9d76` | `8c4a44659bf9ebda2351736e1a74c6423de0f253` | `e036103d04a959701f571058d2a566da09db0123d75218cdf34cd8eb488a9475` |

## Their configurations and effects

These sat beside the profile override, named for their cases. The re-captures carry their own. Each of the first 16 effects was byte-identical to its predecessor's; version 1's window measures its effects and its walk again at slice f2.

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
| `profiles/rv64gc-lab-v0/reference/rv64gc-atomic-misalign-v1.alternative.sexp` | 477 | `228c9d76` | `7f522ba7573cad18fce652d2593cd11958f3259d716494c40a750ada7aaa13ea` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-atomic-misalign-v1.effect.sexp` | 778 | `228c9d76` | `d2182596f148c7b86453d89165cb915b181228d7fc4e9e34ecbd31148e8d7944` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-atomic-misalign-v1.effect.trace` | 16,635 | `228c9d76` | `85b509da3bc0c171a208755c36c27e65785dec2d29cecb0ef311792475c6bee5` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-composition-v1.overlay.sexp` | 574 | `228c9d76` | `bb4576940e8134eccc53bf9c284f8b639ed5fa5b0de41f4ded34e26fe70f314f` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-counters-v2.overlay.sexp` | 602 | `228c9d76` | `a522f5f26e3788d20fb2104ca3f4888dd017a7a64392d5f3c787bb1ad546b96e` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-fault-priority-v1.alternative.sexp` | 420 | `228c9d76` | `88fbcb6ecfb08eaeb89fa627927cd973e5ddaf9b5e7338527e86232693bc9581` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-fault-priority-v1.effect.sexp` | 776 | `228c9d76` | `f87b1be56d1a9ffe27c6dbb573234c24705508706fd29397c3d986ca5463b5ea` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-fault-priority-v1.effect.trace` | 24,896 | `228c9d76` | `143925c3dded74208406f106a7b11489e6d1c09bf7666c1ab1d0289ef76980b8` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-no-h-v1.alternative.sexp` | 424 | `228c9d76` | `77e0625ce91186c871fcfbf4365718afe9819b8f248f19a7f0f980f55aee8d3b` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-no-h-v1.effect.sexp` | 754 | `228c9d76` | `b2da41a6b7245f0ee172e566c55bed132e63fb6a92692d45235389236d3d806f` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-no-h-v1.effect.trace` | 1,631 | `228c9d76` | `da7e2d3ec2310825c7415db8432a330855b2dd9b08c8a561c0d807ad72837abb` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-priv-forms-v1.overlay.sexp` | 448 | `228c9d76` | `d6a2ff66acbac4d8ca326109fd3b2c35e8d24643dc9e472049d6d676e138425e` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-no-pmp-v1.alternative.sexp` | 497 | `228c9d76` | `fb72c3e1d296a982a6b9b9f730213551bd9157281ae9018a6a2815154d2451fe` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-no-pmp-v1.effect.sexp` | 758 | `228c9d76` | `26c79b889177319b05a97381d6af5b743509bf189a5a8d420558324175295369` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-no-pmp-v1.effect.trace` | 3,433 | `228c9d76` | `81f8cc9309da7f2057b1f83d4e57665682eaee50d2df88375610ee307ceb9bc4` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-priv-insns-v1.overlay.sexp` | 413 | `228c9d76` | `d736c3fd2166954e5fe6c6ff93912acc669bdf14f233097946af2ab9a04eb5e0` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-reservation-v1.effect.sexp` | 770 | `228c9d76` | `81ceb99d557b21a4c5979032a2237126f18d99b58068e82ed265b4eff1e8d118` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-reservation-v1.effect.trace` | 15,676 | `228c9d76` | `2cd31190af0b199ea576e6d0f4f998c1904b8b0ca0adf72e2edc229d79a640d3` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-reservation-v1.overlay.sexp` | 470 | `228c9d76` | `e989d0e4d2c45796961b53c26b5575e12507e54b76be51f143796742ae2d609b` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-priv-modes-v1.alternative.sexp` | 510 | `228c9d76` | `05ed8480b198528f60ec9433702efceb5eac0380c3d05c761dbbf9316b91c3a8` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-priv-modes-v1.effect.sexp` | 767 | `228c9d76` | `f05197ea07f1e023afb2e10b7e91a1a66a62cf2c5e9365d1c3ec5e37215428a2` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-priv-modes-v1.effect.trace` | 9,448 | `228c9d76` | `7fb9123be3e36d04fbba596322fe49f975f68953f9719248fda441f07eba9a13` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sc-deterministic-v1.effect.sexp` | 780 | `228c9d76` | `b5a958c505d68dcf368325c173d2f59b2f8d456ad5f7e2c81b799e3185842a95` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sc-deterministic-v1.effect.trace` | 13,331 | `228c9d76` | `9be4b6b43a009dc89c80077c77779658fbbef46841342c65f958d92078c9bd82` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sc-deterministic-v1.overlay.sexp` | 467 | `228c9d76` | `4ebcad03db78b60b7e6e5b880be0567ad26f288a2f982f45134a0e909550e8e2` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-walk-implicit-v1.walk.lab` | 598 | `228c9d76` | `9d81e28145455324bf7819eb658b63f47993775593d27eda02e514de8f939178` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-walk-implicit-v1.walk.sexp` | 743 | `228c9d76` | `b37cccfb9a46f845dfb7eb042db8b766f10aaf2826cd884ea71629b318c9dd47` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-walk-implicit-v1.walk.trace` | 15,352 | `228c9d76` | `a7ff24bfe57587c8dd938c6e4afbf714a9128f14b25d164e4a6fffeabedc64ec` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-svade-v1.alternative.sexp` | 415 | `228c9d76` | `d59aa11ddd0f0d7f415991129498ba14269641514d85584555122dd165a91277` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-svade-v1.effect.sexp` | 758 | `228c9d76` | `c0be97c26a5916ab3077c8da4ec782f483b576cce99d98a045bf3606e98ebd79` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-svade-v1.effect.trace` | 11,302 | `228c9d76` | `3d0543a9628307bd33c855d0ac6a223bdd0fdea9d8b57194612b13fba611342d` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sv39-v1.alternative.sexp` | 426 | `228c9d76` | `be7a6ee2fb0de63a4a73c33fa8b11af892fe082341f7fd41366571c74e973abf` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sv39-v1.effect.sexp` | 756 | `228c9d76` | `e3fcb81dfd18842a640668e557a9462400393a636988c20ec33356b7efcbbe8e` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sv39-v1.effect.trace` | 11,144 | `228c9d76` | `63511c3c2af28882586cbbcaa48a4953ff25b860cab3c05e36727b2c5563d11c` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sstc-v2.effect.sexp` | 756 | `228c9d76` | `00d12501bf11812960cef101cc06259f2f9694f07ad3e49f7943076f13c83a4a` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sstc-v2.effect.trace` | 25,773 | `228c9d76` | `2b6738588b6160695e1f3296e0f19fb17c3bc3851d52689404b02e4048806f33` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-sstc-v2.overlay.sexp` | 794 | `228c9d76` | `d7339892462ec7c7c5df6ee737ac1cb9a5e67f11ecc2fca67c10ac965cb5e513` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v3.effect.sexp` | 760 | `228c9d76` | `f88c7702baa48e9d363eb2283f4e88eba559fb00e95b9d17e334ce0402436b05` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v3.effect.trace` | 27,617 | `228c9d76` | `896814f3f54e1a2bf9af3de7a61e4dac6f831921e7e946c67c28c39362913570` |
| `profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v3.overlay.sexp` | 786 | `228c9d76` | `166549fa4649e49f271e51d97f04ed508c7ded578fa4f18aa10de010752042d1` |
