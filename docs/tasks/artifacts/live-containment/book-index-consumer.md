# Project-book index consumer — LC0032

Source32f9c31eba83ccfc15c2c875ba14bb5851b9a543; all1443 identities pinned;
Gitlinks stay opaque. This records a measured consumer and its defects; it is
not complete index/query graph coverage or a processor qualification.

D73, priority1, owned by LIVE-CONTAINMENT.4i2b4b1r / LC0033 immediately next:
normal public generator and guard both return1 with traceback on an actual
injected source read failure; invalid UTF-8 gives generator traceback1.
The declared generator contract requires unjudgeable inputs refuse2. The
wrapper loses the generator status at its actual failure branch and calls it
drift. Missing chapter/SUMMARY/glossary/acronym inputs already refuse2.
No original generator/guard behavior is changed by LC0032.

Reproduction uses local source objects and the tracked public probe:

```sh
python3 scripts/qualify_book_index.py --output target/live-containment/book-index-replay/normal
python3 -O scripts/qualify_book_index.py --output target/live-containment/book-index-replay/optimized
```

Choose fresh output paths. Exit0 means measurement completed; observations
retain actual child verdicts. No Git repository, remote fetch, foreign cache or
Gitlink implementation is needed. Git's public GIT_WORK_TREE/GIT_DIR inputs
select isolated on-volume fixture roots while using this repository's read-only
metadata; HEAD/index/working identities must remain exact.

## Complete source and consumer capture

All54 fixture input pins,49 declared chapters,40 terms/aliases/discussion hits,
24 public observations, three copied omissions and two ledger controls follow.
Normal/O and actual-working-code executions agree on semantic data and all
source identities. Each of ten public read injections fires exactly once.
The original12 defective observations per mode remain D73; no repair claim is
made here. Both valid public baselines return0 without output drift. Actual
index source reads are53; full immutable input bytes authenticate each one.

The public index reads raw chapter text, not mdBook's expanded includes.
That is this measured consumer's boundary; include expansion and seven native
books were qualified separately. Other query/index readers remain .4i2b4b2–3;
no complete graph/adoption or semantic truth verdict is claimed.

```json
{
  "baseline": {
    "generator": {
      "returncode": 0,
      "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    "guard": {
      "returncode": 0,
      "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "stdout_sha256": "62fa189fd1c1978f86891e2bd080fb0b301ca212ba36531e73f0ef9cc43cf07c",
      "traceback": false
    }
  },
  "chapters": [
    {
      "path": "docs/book/src/introduction.md",
      "target": "introduction.md",
      "title": "Introduction"
    },
    {
      "path": "docs/book/src/claim-scope.md",
      "target": "claim-scope.md",
      "title": "What is claimed, and what is not"
    },
    {
      "path": "docs/book/src/status.md",
      "target": "status.md",
      "title": "Current status"
    },
    {
      "path": "docs/book/src/models.md",
      "target": "models.md",
      "title": "One definition, one book"
    },
    {
      "path": "docs/book/src/models/the-information-a-unit-demands.md",
      "target": "models/the-information-a-unit-demands.md",
      "title": "The information a unit demands \u2014 CPU, DSP, board"
    },
    {
      "path": "docs/book/src/plan/overview.md",
      "target": "plan/overview.md",
      "title": "Milestones and their dependencies"
    },
    {
      "path": "docs/book/src/plan/p0.md",
      "target": "plan/p0.md",
      "title": "P0 \u2014 profile and evidence access"
    },
    {
      "path": "docs/book/src/plan/p1.md",
      "target": "plan/p1.md",
      "title": "P1 \u2014 the processor laboratory"
    },
    {
      "path": "docs/book/src/plan/p2.md",
      "target": "plan/p2.md",
      "title": "P2 \u2014 the first validated profile"
    },
    {
      "path": "docs/book/src/plan/p3.md",
      "target": "plan/p3.md",
      "title": "P3 \u2014 breadth, and the DSP pressure"
    },
    {
      "path": "docs/book/src/plan/p4.md",
      "target": "plan/p4.md",
      "title": "P4 \u2014 the Linux CPU profile"
    },
    {
      "path": "docs/book/src/plan/p4/privilege.md",
      "target": "plan/p4/privilege.md",
      "title": "P4.2 \u2014 Privilege and mode transitions"
    },
    {
      "path": "docs/book/src/plan/p4/sv39.md",
      "target": "plan/p4/sv39.md",
      "title": "P4.3 \u2014 Sv39 translation and protection"
    },
    {
      "path": "docs/book/src/plan/p4/atomics.md",
      "target": "plan/p4/atomics.md",
      "title": "P4.4 \u2014 Atomics and reservations"
    },
    {
      "path": "docs/book/src/plan/p4/interrupts.md",
      "target": "plan/p4/interrupts.md",
      "title": "P4.5 \u2014 Interrupts, counters and wait"
    },
    {
      "path": "docs/book/src/plan/p4/fence-i.md",
      "target": "plan/p4/fence-i.md",
      "title": "P4.6 \u2014 Instruction visibility and fence semantics"
    },
    {
      "path": "docs/book/src/plan/p4/floating-point.md",
      "target": "plan/p4/floating-point.md",
      "title": "P4.7 \u2014 Floating point"
    },
    {
      "path": "docs/book/src/plan/p4/faults.md",
      "target": "plan/p4/faults.md",
      "title": "P4.8 \u2014 Faults, restart and partial progress"
    },
    {
      "path": "docs/book/src/plan/p4/contract.md",
      "target": "plan/p4/contract.md",
      "title": "P4.9 \u2014 The environment contract, version 1"
    },
    {
      "path": "docs/book/src/plan/p4/gate.md",
      "target": "plan/p4/gate.md",
      "title": "P4.10 \u2014 The CPU-SYSTEM gate report"
    },
    {
      "path": "docs/book/src/plan/p4/m.md",
      "target": "plan/p4/m.md",
      "title": "P4.11 \u2014 Integer multiply and divide (M)"
    },
    {
      "path": "docs/book/src/plan/p4/c.md",
      "target": "plan/p4/c.md",
      "title": "P4.12 \u2014 Compressed instructions (C)"
    },
    {
      "path": "docs/book/src/plan/p4/contract-v2.md",
      "target": "plan/p4/contract-v2.md",
      "title": "P4.13 \u2014 Completing the environment contract"
    },
    {
      "path": "docs/book/src/plan/p4/contract-runtime.md",
      "target": "plan/p4/contract-runtime.md",
      "title": "Runtime contract witnesses"
    },
    {
      "path": "docs/book/src/plan/p4/contract-integer.md",
      "target": "plan/p4/contract-integer.md",
      "title": "Integer runtime witnesses"
    },
    {
      "path": "docs/book/src/plan/p4/contract-control.md",
      "target": "plan/p4/contract-control.md",
      "title": "Control transfer witnesses"
    },
    {
      "path": "docs/book/src/plan/p4/contract-memory.md",
      "target": "plan/p4/contract-memory.md",
      "title": "Memory runtime witnesses"
    },
    {
      "path": "docs/book/src/plan/p5-p7.md",
      "target": "plan/p5-p7.md",
      "title": "P5\u2013P7 \u2014 board, Linux, computer"
    },
    {
      "path": "docs/book/src/plan/multicore.md",
      "target": "plan/multicore.md",
      "title": "Multicore and optimization"
    },
    {
      "path": "docs/book/src/contracts/method.md",
      "target": "contracts/method.md",
      "title": "The method"
    },
    {
      "path": "docs/book/src/contracts/rules.md",
      "target": "contracts/rules.md",
      "title": "Engineering rules"
    },
    {
      "path": "docs/book/src/contracts/architecture.md",
      "target": "contracts/architecture.md",
      "title": "Architecture and canonical definitions"
    },
    {
      "path": "docs/book/src/contracts/cpu-environment.md",
      "target": "contracts/cpu-environment.md",
      "title": "The CPU/environment contract"
    },
    {
      "path": "docs/book/src/contracts/evidence-and-gates.md",
      "target": "contracts/evidence-and-gates.md",
      "title": "Evidence, traceability and gates"
    },
    {
      "path": "docs/book/src/contracts/archogen.md",
      "target": "contracts/archogen.md",
      "title": "archogen and eADL"
    },
    {
      "path": "docs/book/src/contracts/information-catalog.md",
      "target": "contracts/information-catalog.md",
      "title": "The information catalog"
    },
    {
      "path": "docs/book/src/contracts/risks.md",
      "target": "contracts/risks.md",
      "title": "Risks and decisions due"
    },
    {
      "path": "docs/book/src/contracts/sources.md",
      "target": "contracts/sources.md",
      "title": "Sources and naming"
    },
    {
      "path": "docs/book/src/contracts/review-disposition.md",
      "target": "contracts/review-disposition.md",
      "title": "Disposition of the v0.1 review"
    },
    {
      "path": "docs/book/src/data/overview.md",
      "target": "data/overview.md",
      "title": "Schemas and fixtures"
    },
    {
      "path": "docs/book/src/data/worked-example.md",
      "target": "data/worked-example.md",
      "title": "A worked example"
    },
    {
      "path": "docs/book/src/working/task-trees.md",
      "target": "working/task-trees.md",
      "title": "Task-trees"
    },
    {
      "path": "docs/book/src/working/claim-verification.md",
      "target": "working/claim-verification.md",
      "title": "What \"checked\" means"
    },
    {
      "path": "docs/book/src/working/doctrines.md",
      "target": "working/doctrines.md",
      "title": "The doctrine gates"
    },
    {
      "path": "docs/book/src/working/provenance.md",
      "target": "working/provenance.md",
      "title": "Provenance and frozen records"
    },
    {
      "path": "docs/book/src/annex/assembler.md",
      "target": "annex/assembler.md",
      "title": "How the tracked assembler works"
    },
    {
      "path": "docs/book/src/annex/building-first-model.md",
      "target": "annex/building-first-model.md",
      "title": "Building the first CPU model, step by step"
    },
    {
      "path": "docs/book/src/glossary.md",
      "target": "glossary.md",
      "title": "Glossary"
    },
    {
      "path": "docs/book/src/index.md",
      "target": "index.md",
      "title": "Index"
    }
  ],
  "code_source": "32f9c31eba83ccfc15c2c875ba14bb5851b9a543",
  "excluded_discussions": [
    "glossary.md",
    "index.md"
  ],
  "include_expansion": false,
  "input_files": 54,
  "input_pins": {
    "docs/GLOSSARY.md": {
      "bytes": 3037,
      "mode": "100644",
      "sha256": "1a613526fd75d43e789f9b37c2bec1be3964c67f17bf598e23cf418329a68916"
    },
    "docs/book/book.toml": {
      "bytes": 575,
      "mode": "100644",
      "sha256": "fc170c2572571723c8ffa9214ea88cbc304f2d03d00c5ee7c03ff8862396229b"
    },
    "docs/book/src/SUMMARY.md": {
      "bytes": 2988,
      "mode": "100644",
      "sha256": "02ee22f09da39ec80312de34ebf68280f80dea1a182f29f5045a99e83f696e9e"
    },
    "docs/book/src/annex/assembler.md": {
      "bytes": 22189,
      "mode": "100644",
      "sha256": "403a0ff90673128620520b023e3f5e9b63cae5933ce2e916c98a1578f5e70f95"
    },
    "docs/book/src/annex/building-first-model.md": {
      "bytes": 22698,
      "mode": "100644",
      "sha256": "05fc91f63ac6b3cbedcd04a88dbc21d61b7e8aee3fc2a2cc486eb35b6eb55123"
    },
    "docs/book/src/claim-scope.md": {
      "bytes": 5030,
      "mode": "100644",
      "sha256": "2983a4afa5cb3112b4edd6eadf5bc12719efbbd30297423d59a1072dcceff491"
    },
    "docs/book/src/contracts/architecture.md": {
      "bytes": 1057,
      "mode": "100644",
      "sha256": "ce664a4c3efe8ccd24bd7f227f947aa3e30bcc359b5542439c65186cf7b3db50"
    },
    "docs/book/src/contracts/archogen.md": {
      "bytes": 1887,
      "mode": "100644",
      "sha256": "bdf8c3e03ee341370166e9b7fea40a1a9456d8eb3cb747f431f49f55303316f5"
    },
    "docs/book/src/contracts/cpu-environment.md": {
      "bytes": 1215,
      "mode": "100644",
      "sha256": "7b7a47af2a8ace9ebc76e7f89822de00d8533a8c243b128ecc9d4089bef431f1"
    },
    "docs/book/src/contracts/evidence-and-gates.md": {
      "bytes": 1552,
      "mode": "100644",
      "sha256": "b3b9bcb658731409ecdbcf24bb34ad34d74d1fbaaf2b8e06992b00dc7dbcacc8"
    },
    "docs/book/src/contracts/information-catalog.md": {
      "bytes": 1266,
      "mode": "100644",
      "sha256": "fd3c64943eeb2e4f3ef2352b4f410b25dc2f9b35ca771754066016a07d6379b3"
    },
    "docs/book/src/contracts/method.md": {
      "bytes": 588,
      "mode": "100644",
      "sha256": "cdf5ff0f3cd6b8fbb312a40dbc56bb5076c648f4422fc82a27620562849c14fb"
    },
    "docs/book/src/contracts/review-disposition.md": {
      "bytes": 1233,
      "mode": "100644",
      "sha256": "5e1dd2d7b14b54821c84866c10a807246b9a1fa551ba210d2a23ac8e00510758"
    },
    "docs/book/src/contracts/risks.md": {
      "bytes": 952,
      "mode": "100644",
      "sha256": "14e3698d15b8b4bca18758ddc563c032aabcdf2a71bcd4f1e2c0f7a3ab29da06"
    },
    "docs/book/src/contracts/rules.md": {
      "bytes": 1111,
      "mode": "100644",
      "sha256": "3a1f5f230e5ed5e799be9e8e6d18606dad5ebe09015bc2398ea8afb465956543"
    },
    "docs/book/src/contracts/sources.md": {
      "bytes": 1026,
      "mode": "100644",
      "sha256": "e84c6d9245eaba672e8bed6c9cdc4f20f247de7452c6f43ea43c0279c4af150a"
    },
    "docs/book/src/data/overview.md": {
      "bytes": 2738,
      "mode": "100644",
      "sha256": "bd5d49a80046e7acd50edbd6481ba5e836a699a34ffd94a63cf26d70074cbb25"
    },
    "docs/book/src/data/worked-example.md": {
      "bytes": 3950,
      "mode": "100644",
      "sha256": "e71962e18d6cc1505d9afb872f78e063f1b7aa3d0b815f2863f494e9de7c2e63"
    },
    "docs/book/src/glossary.md": {
      "bytes": 3495,
      "mode": "100644",
      "sha256": "33585c6b3862fe4769405aea8cab59e6910bb23ec92ad39435c48ab28c81ef58"
    },
    "docs/book/src/index.md": {
      "bytes": 24489,
      "mode": "100644",
      "sha256": "841b078ff0cfe1e03d1b808a0c8e12e7c1f7a92d832b40bc8b7d38b9ecbb18f8"
    },
    "docs/book/src/introduction.md": {
      "bytes": 3246,
      "mode": "100644",
      "sha256": "95a83bbc4a6b7eecc7233efe8cc562210aa8483b5b74dc97ceab455c821255f8"
    },
    "docs/book/src/models.md": {
      "bytes": 3656,
      "mode": "100644",
      "sha256": "a8cfd6f97dc791b62e8703e0275ec2c9b567ef752c6a25324131b4a369cfbfd7"
    },
    "docs/book/src/models/the-information-a-unit-demands.md": {
      "bytes": 13137,
      "mode": "100644",
      "sha256": "abce434fd1014cf11fb7e1113bba8e9bc5b4fd98d0c419f50bce7e89516a46a6"
    },
    "docs/book/src/plan/multicore.md": {
      "bytes": 1557,
      "mode": "100644",
      "sha256": "fde1341970f0e6d5b662827574676b699b363257650a32e9c10ee7cecd055792"
    },
    "docs/book/src/plan/overview.md": {
      "bytes": 3692,
      "mode": "100644",
      "sha256": "06523019a849e5dd70180f54654c608beb3130cd8faeaddd259a17a4c5f670aa"
    },
    "docs/book/src/plan/p0.md": {
      "bytes": 25456,
      "mode": "100644",
      "sha256": "408ce9e09f0fa83ff9965ad33d0828564cf633a9a72547a75d9d477675010db1"
    },
    "docs/book/src/plan/p1.md": {
      "bytes": 30505,
      "mode": "100644",
      "sha256": "c7e0a457423ce772702fa54236871f494fcb104bc44b7ef1f01ceb2fe0693dba"
    },
    "docs/book/src/plan/p2.md": {
      "bytes": 24481,
      "mode": "100644",
      "sha256": "559e84d3b4b8db6743ca97eb0552eed7c9abed8fef9bedae5ee71b78e2c85cd6"
    },
    "docs/book/src/plan/p3.md": {
      "bytes": 7093,
      "mode": "100644",
      "sha256": "178510d5861b71e5662ed4c20aca0004b936dabeb07bea7a229dc9149839dccf"
    },
    "docs/book/src/plan/p4.md": {
      "bytes": 8741,
      "mode": "100644",
      "sha256": "0036fde7c7890734d9bc4cb91938651f8f42ae4359b1f51a0491bc5c8faf7493"
    },
    "docs/book/src/plan/p4/atomics.md": {
      "bytes": 21551,
      "mode": "100644",
      "sha256": "805a81f14aff104f12e07df8543126bae1ccdb91a94c2918e3959e2339da2552"
    },
    "docs/book/src/plan/p4/c.md": {
      "bytes": 12173,
      "mode": "100644",
      "sha256": "7e33f66d6a70983898cd94e0babb4116e0ac0e1c3fa0068c4b43548335672cfa"
    },
    "docs/book/src/plan/p4/contract-control.md": {
      "bytes": 9080,
      "mode": "100644",
      "sha256": "914d3062e961eeefdbeebcd3ce6dd4deea3d58919272d14569424836fd7c2bd1"
    },
    "docs/book/src/plan/p4/contract-integer.md": {
      "bytes": 22322,
      "mode": "100644",
      "sha256": "dd567bcf0d095cea28fda57a1adb6a0f30209980db5cbec839ca2dbae19ad400"
    },
    "docs/book/src/plan/p4/contract-memory.md": {
      "bytes": 23696,
      "mode": "100644",
      "sha256": "623448374c278b51ff0a2d446d30ab9ad7f340952ad4c8c8cd35ca4d3d853805"
    },
    "docs/book/src/plan/p4/contract-runtime.md": {
      "bytes": 31190,
      "mode": "100644",
      "sha256": "85cff2e69551dd3fc21770a09172796cd0248bae189ba97b618ae3cf2afee3c6"
    },
    "docs/book/src/plan/p4/contract-v2.md": {
      "bytes": 32479,
      "mode": "100644",
      "sha256": "b92b48e826ee45ae809c97a905525a4b2836ebb0dedfc7db3821d9457b663731"
    },
    "docs/book/src/plan/p4/contract.md": {
      "bytes": 2824,
      "mode": "100644",
      "sha256": "8fb149b526b7478b5d7a1f8ec1fce47c1ea53b26c76133ea243e5ce65946372e"
    },
    "docs/book/src/plan/p4/faults.md": {
      "bytes": 3888,
      "mode": "100644",
      "sha256": "e928115d582074fe823eec82240b0f6d3cb7936b93eb07e7f6dcb47827251680"
    },
    "docs/book/src/plan/p4/fence-i.md": {
      "bytes": 8745,
      "mode": "100644",
      "sha256": "d72e9f99762ff20f0a8f23660857a1889f615e352c4278361e0a2ef14ae755db"
    },
    "docs/book/src/plan/p4/floating-point.md": {
      "bytes": 24275,
      "mode": "100644",
      "sha256": "1967f7be46fc4f812cabb05d4b116c16589b31729e0f03d6eed49b623c3b2068"
    },
    "docs/book/src/plan/p4/gate.md": {
      "bytes": 4157,
      "mode": "100644",
      "sha256": "d6dcc69b452e90050f23724bd84068e644c81993b73c17c5ab4bdabbf05f90e0"
    },
    "docs/book/src/plan/p4/interrupts.md": {
      "bytes": 6814,
      "mode": "100644",
      "sha256": "b6e019d7b72abbbce164e59fccb0da4b582fa9234f6371747a86b713cc1c4ef2"
    },
    "docs/book/src/plan/p4/m.md": {
      "bytes": 4173,
      "mode": "100644",
      "sha256": "076cae4d29e16e6d7cd4d5ca65ed811a93f5e307e7d2ab533f0eda5968c65c3e"
    },
    "docs/book/src/plan/p4/privilege.md": {
      "bytes": 9221,
      "mode": "100644",
      "sha256": "5acf2e3c670457985fa57cf90ca7841924e6f206f3af91406b6a57ae8a5e6202"
    },
    "docs/book/src/plan/p4/sv39.md": {
      "bytes": 12639,
      "mode": "100644",
      "sha256": "80fe801cd9c3d84c30beb95ac07d5f6f0aca991668e260415e18b17d2fe48479"
    },
    "docs/book/src/plan/p5-p7.md": {
      "bytes": 15751,
      "mode": "100644",
      "sha256": "18548b77292bfed902f64a2734b22bb67c01f3cd349ef2737373e296c5e881f4"
    },
    "docs/book/src/status.md": {
      "bytes": 842,
      "mode": "100644",
      "sha256": "a8bdf5fee364422256f88567420c82f1b90e65bec897be865cc46954cd4ec4b9"
    },
    "docs/book/src/working/claim-verification.md": {
      "bytes": 3616,
      "mode": "100644",
      "sha256": "6946521dcf8c41c333ba1c19e5d9cb875808cd7cfc05eb4eb8570adc47f15060"
    },
    "docs/book/src/working/doctrines.md": {
      "bytes": 32141,
      "mode": "100644",
      "sha256": "def411269492d3d1590ad012c131d19d5401d14fb2d903e5d8ad810d149f642f"
    },
    "docs/book/src/working/provenance.md": {
      "bytes": 4437,
      "mode": "100644",
      "sha256": "06dbd9dc65c56139a7b7511fa4e52d4ac36e205bd15d996a924ddc98996a3d8f"
    },
    "docs/book/src/working/task-trees.md": {
      "bytes": 16120,
      "mode": "100644",
      "sha256": "aba6fcd6f67501248b7ce83c92bb5d369686eaaba7ec26b5007b8a3bf826dd6a"
    },
    "scripts/check_book_index.sh": {
      "bytes": 6373,
      "mode": "100755",
      "sha256": "113341ab3a5763803e7d20415bed59455801b7976b36e7da6e586d98cd1912e5"
    },
    "scripts/gen_book_index.py": {
      "bytes": 7734,
      "mode": "100755",
      "sha256": "8c63e97dc3e2b425ed1f81305791e9d047d7edabfc0c9c74fe309e11f7b35dc7"
    }
  },
  "ledger_controls": [
    {
      "control": "omitted-read",
      "reason": "complete actual chapter reads/order differs",
      "returncode": 2
    },
    {
      "control": "changed-read-digest",
      "reason": "actual read content differs from immutable input",
      "returncode": 2
    }
  ],
  "mode": "normal",
  "observations": [
    {
      "case": "stale-index",
      "expected_returncode": 1,
      "fault_reads": 0,
      "interface": "generator",
      "returncode": 1,
      "stderr_sha256": "67e333d5a58635eb6336990388eb1ff6d8a804ee4b9f0a655e9756d163a071e0",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "stale-index",
      "expected_returncode": 1,
      "fault_reads": 0,
      "interface": "guard",
      "returncode": 1,
      "stderr_sha256": "9c16b738f56a4dd5a5e67f838a43bb42bbea9718519ce9a9ef34815532e3b24f",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "missing-chapter",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "generator",
      "returncode": 2,
      "stderr_sha256": "577300ee6a5e726e6ddffa0abc5bca9960dad087289343726daae2b9dcb6e9a4",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "missing-chapter",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "guard",
      "returncode": 2,
      "stderr_sha256": "40920e1d39acd8ce0c036ad88a0f34de513bef65ad4f3b8c32bddff2b9289591",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "missing-summary",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "generator",
      "returncode": 2,
      "stderr_sha256": "c76f3779c351532a6f489cea6576999405f2a097d580b11f437183ac38cd8913",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "missing-summary",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "guard",
      "returncode": 2,
      "stderr_sha256": "40920e1d39acd8ce0c036ad88a0f34de513bef65ad4f3b8c32bddff2b9289591",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "missing-glossary",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "generator",
      "returncode": 2,
      "stderr_sha256": "7481d3b99f1faa1b2a6f409060f504b5135db91495355072ac68b93717d68ebf",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "missing-glossary",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "guard",
      "returncode": 2,
      "stderr_sha256": "40920e1d39acd8ce0c036ad88a0f34de513bef65ad4f3b8c32bddff2b9289591",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "missing-acronyms",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "generator",
      "returncode": 2,
      "stderr_sha256": "93bd51e194a4a0c6f10f436cb1d9cff90abae12e8e2ef7ce5742a32046541b90",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "missing-acronyms",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "guard",
      "returncode": 2,
      "stderr_sha256": "40920e1d39acd8ce0c036ad88a0f34de513bef65ad4f3b8c32bddff2b9289591",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "invalid-chapter-utf8",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "generator",
      "returncode": 1,
      "stderr_sha256": "43f72ce861b5d094f3ed6b667f8c27c1f0572951d226f4c7bde89f033f0fba40",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "invalid-chapter-utf8",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "guard",
      "returncode": 2,
      "stderr_sha256": "40920e1d39acd8ce0c036ad88a0f34de513bef65ad4f3b8c32bddff2b9289591",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "invalid-summary-utf8",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "generator",
      "returncode": 1,
      "stderr_sha256": "b4f9e0118868bcbe162cd357775e6fc77c7a01435ec6ee8b636d0c623c5a4400",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "invalid-summary-utf8",
      "expected_returncode": 2,
      "fault_reads": 0,
      "interface": "guard",
      "returncode": 2,
      "stderr_sha256": "40920e1d39acd8ce0c036ad88a0f34de513bef65ad4f3b8c32bddff2b9289591",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "case": "read-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "generator",
      "returncode": 1,
      "stderr_sha256": "d271d788b7cce995ebb5a5c4ab02be974d06c1d0c4c6a64267f26135399e49c7",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "guard",
      "returncode": 1,
      "stderr_sha256": "2a3de0cf4b66db38db17c7f4a85163888f068988f07b2e754ef34086d7f3792c",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-summary-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "generator",
      "returncode": 1,
      "stderr_sha256": "bbfccd8f1c8669c8ac6ae481d366996d40d890095fbcdb0ee671ecae5c299ad4",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-summary-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "guard",
      "returncode": 1,
      "stderr_sha256": "32592944575f36623195a6e5247c2091f99df0e184ec3dcb943055db1b062a2a",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-glossary-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "generator",
      "returncode": 1,
      "stderr_sha256": "b41ecdce833fb5679173e8feeb5d78af8171c028c8dbc491f2bf6720cf8128fe",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-glossary-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "guard",
      "returncode": 1,
      "stderr_sha256": "fd08fe5c9e746cd4dea1212222cbdc5f7137283141acf36638a5054e0a932d88",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-acronyms-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "generator",
      "returncode": 1,
      "stderr_sha256": "19d73a3a307bfe21d2168f8a4660d4863baa17c26766b6c8423e5974df268ccd",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-acronyms-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "guard",
      "returncode": 1,
      "stderr_sha256": "955017817fc2ca34ef5951f754e425d38075ce7752f5cdb8b10da9796c8d3af0",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-index-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "generator",
      "returncode": 1,
      "stderr_sha256": "5b298d7f0f2df434db8b4bd959851ddf3d6f0c9ba43e6e8009fcd3f5364177d3",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    },
    {
      "case": "read-index-fault",
      "expected_returncode": 2,
      "fault_reads": 1,
      "interface": "guard",
      "returncode": 1,
      "stderr_sha256": "fc237d3e24891d1a7b2919f36552043d5df22549d2f9d66f9c8efb1b24d315c3",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": true
    }
  ],
  "omissions": [
    {
      "omission": "omit-chapter",
      "returncode": 1,
      "stderr_sha256": "67e333d5a58635eb6336990388eb1ff6d8a804ee4b9f0a655e9756d163a071e0",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "omission": "omit-term",
      "returncode": 1,
      "stderr_sha256": "67e333d5a58635eb6336990388eb1ff6d8a804ee4b9f0a655e9756d163a071e0",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    },
    {
      "omission": "omit-discussions",
      "returncode": 1,
      "stderr_sha256": "67e333d5a58635eb6336990388eb1ff6d8a804ee4b9f0a655e9756d163a071e0",
      "stdout_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "traceback": false
    }
  ],
  "source": "32f9c31eba83ccfc15c2c875ba14bb5851b9a543",
  "source_defects": [
    {
      "case": "invalid-chapter-utf8",
      "interface": "generator"
    },
    {
      "case": "invalid-summary-utf8",
      "interface": "generator"
    },
    {
      "case": "read-fault",
      "interface": "generator"
    },
    {
      "case": "read-fault",
      "interface": "guard"
    },
    {
      "case": "read-summary-fault",
      "interface": "generator"
    },
    {
      "case": "read-summary-fault",
      "interface": "guard"
    },
    {
      "case": "read-glossary-fault",
      "interface": "generator"
    },
    {
      "case": "read-glossary-fault",
      "interface": "guard"
    },
    {
      "case": "read-acronyms-fault",
      "interface": "generator"
    },
    {
      "case": "read-acronyms-fault",
      "interface": "guard"
    },
    {
      "case": "read-index-fault",
      "interface": "generator"
    },
    {
      "case": "read-index-fault",
      "interface": "guard"
    }
  ],
  "source_members": 1443,
  "source_tree_sha256": "cc74552565563ae94d2277baad24197fd1922f5d1bb52139c81d6eed5a4f5c07",
  "terms": [
    {
      "aliases": [
        "ACT"
      ],
      "chapters": [
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/working/provenance.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "ACT"
    },
    {
      "aliases": [
        "ALU"
      ],
      "chapters": [
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p4/contract-memory.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "ALU"
    },
    {
      "aliases": [
        "API"
      ],
      "chapters": [
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/privilege.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "API"
    },
    {
      "aliases": [
        "Architecture",
        "ISA"
      ],
      "chapters": [
        "docs/book/src/claim-scope.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/privilege.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-control.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/plan/multicore.md",
        "docs/book/src/contracts/architecture.md",
        "docs/book/src/data/overview.md",
        "docs/book/src/data/worked-example.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md",
      "term": "Architecture / ISA"
    },
    {
      "aliases": [
        "archogen"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/contracts/archogen.md",
        "docs/book/src/working/provenance.md"
      ],
      "definition": "glossary.md",
      "term": "archogen"
    },
    {
      "aliases": [
        "Canonical definition"
      ],
      "chapters": [
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md",
      "term": "Canonical definition"
    },
    {
      "aliases": [
        "Canonical input fingerprint"
      ],
      "chapters": [],
      "definition": "glossary.md",
      "term": "Canonical input fingerprint"
    },
    {
      "aliases": [
        "CI"
      ],
      "chapters": [
        "docs/book/src/claim-scope.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-control.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/working/task-trees.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/working/provenance.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "CI"
    },
    {
      "aliases": [
        "Conformance"
      ],
      "chapters": [
        "docs/book/src/claim-scope.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p5-p7.md"
      ],
      "definition": "glossary.md",
      "term": "Conformance"
    },
    {
      "aliases": [
        "CPU"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/claim-scope.md",
        "docs/book/src/models.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/privilege.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/interrupts.md",
        "docs/book/src/plan/p4/fence-i.md",
        "docs/book/src/plan/p4/floating-point.md",
        "docs/book/src/plan/p4/gate.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p4/contract-control.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/plan/multicore.md",
        "docs/book/src/contracts/cpu-environment.md",
        "docs/book/src/contracts/archogen.md",
        "docs/book/src/contracts/information-catalog.md",
        "docs/book/src/data/overview.md",
        "docs/book/src/data/worked-example.md",
        "docs/book/src/working/task-trees.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "CPU"
    },
    {
      "aliases": [
        "Diagnostic tracing"
      ],
      "chapters": [],
      "definition": "glossary.md",
      "term": "Diagnostic tracing"
    },
    {
      "aliases": [
        "Dossier"
      ],
      "chapters": [
        "docs/book/src/claim-scope.md",
        "docs/book/src/models.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/floating-point.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md",
      "term": "Dossier"
    },
    {
      "aliases": [
        "DSP"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/models.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/contracts/information-catalog.md",
        "docs/book/src/contracts/sources.md",
        "docs/book/src/data/worked-example.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "DSP"
    },
    {
      "aliases": [
        "eADL"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/contracts/archogen.md"
      ],
      "definition": "glossary.md",
      "term": "eADL"
    },
    {
      "aliases": [
        "ELF"
      ],
      "chapters": [
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p4/privilege.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "ELF"
    },
    {
      "aliases": [
        "Environment contract"
      ],
      "chapters": [
        "docs/book/src/claim-scope.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/contract.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/multicore.md",
        "docs/book/src/contracts/cpu-environment.md",
        "docs/book/src/working/doctrines.md"
      ],
      "definition": "glossary.md",
      "term": "Environment contract"
    },
    {
      "aliases": [
        "Exploration coverage"
      ],
      "chapters": [],
      "definition": "glossary.md",
      "term": "Exploration coverage"
    },
    {
      "aliases": [
        "External authority"
      ],
      "chapters": [],
      "definition": "glossary.md",
      "term": "External authority"
    },
    {
      "aliases": [
        "FM"
      ],
      "chapters": [
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "FM"
    },
    {
      "aliases": [
        "Gate"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/claim-scope.md",
        "docs/book/src/status.md",
        "docs/book/src/models.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/floating-point.md",
        "docs/book/src/plan/p4/contract.md",
        "docs/book/src/plan/p4/gate.md",
        "docs/book/src/plan/p4/m.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/plan/multicore.md",
        "docs/book/src/data/overview.md",
        "docs/book/src/data/worked-example.md",
        "docs/book/src/working/task-trees.md",
        "docs/book/src/working/claim-verification.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/working/provenance.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md",
      "term": "Gate"
    },
    {
      "aliases": [
        "Independent evidence"
      ],
      "chapters": [
        "docs/book/src/plan/p4/c.md"
      ],
      "definition": "glossary.md",
      "term": "Independent evidence"
    },
    {
      "aliases": [
        "ISA"
      ],
      "chapters": [
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/privilege.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-control.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/data/worked-example.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "ISA"
    },
    {
      "aliases": [
        "JSON"
      ],
      "chapters": [
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/data/overview.md",
        "docs/book/src/data/worked-example.md",
        "docs/book/src/working/task-trees.md",
        "docs/book/src/working/provenance.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "JSON"
    },
    {
      "aliases": [
        "Laboratory"
      ],
      "chapters": [
        "docs/book/src/claim-scope.md",
        "docs/book/src/models.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/interrupts.md",
        "docs/book/src/plan/p4/fence-i.md",
        "docs/book/src/plan/p4/floating-point.md",
        "docs/book/src/plan/p4/faults.md",
        "docs/book/src/plan/p4/contract.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/contracts/cpu-environment.md",
        "docs/book/src/data/overview.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md",
      "term": "Laboratory"
    },
    {
      "aliases": [
        "Locked"
      ],
      "chapters": [
        "docs/book/src/plan/p2.md"
      ],
      "definition": "glossary.md",
      "term": "Locked"
    },
    {
      "aliases": [
        "MAC"
      ],
      "chapters": [
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p5-p7.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "MAC"
    },
    {
      "aliases": [
        "Model limitation"
      ],
      "chapters": [
        "docs/book/src/plan/p1.md",
        "docs/book/src/contracts/information-catalog.md"
      ],
      "definition": "glossary.md",
      "term": "Model limitation"
    },
    {
      "aliases": [
        "Observation contract"
      ],
      "chapters": [],
      "definition": "glossary.md",
      "term": "Observation contract"
    },
    {
      "aliases": [
        "Oracle",
        "reference"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/claim-scope.md",
        "docs/book/src/models.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/interrupts.md",
        "docs/book/src/plan/p4/fence-i.md",
        "docs/book/src/plan/p4/floating-point.md",
        "docs/book/src/plan/p4/faults.md",
        "docs/book/src/plan/p4/gate.md",
        "docs/book/src/plan/p4/m.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/multicore.md",
        "docs/book/src/contracts/architecture.md",
        "docs/book/src/contracts/evidence-and-gates.md",
        "docs/book/src/contracts/archogen.md",
        "docs/book/src/contracts/sources.md",
        "docs/book/src/contracts/review-disposition.md",
        "docs/book/src/working/task-trees.md",
        "docs/book/src/working/claim-verification.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md",
      "term": "Oracle / reference"
    },
    {
      "aliases": [
        "OS"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/contracts/archogen.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "OS"
    },
    {
      "aliases": [
        "PC"
      ],
      "chapters": [
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4/privilege.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/interrupts.md",
        "docs/book/src/plan/p4/fence-i.md",
        "docs/book/src/plan/p4/floating-point.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p4/contract-control.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "PC"
    },
    {
      "aliases": [
        "Platform contract"
      ],
      "chapters": [],
      "definition": "glossary.md",
      "term": "Platform contract"
    },
    {
      "aliases": [
        "Profile"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/claim-scope.md",
        "docs/book/src/models.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/privilege.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/floating-point.md",
        "docs/book/src/plan/p4/contract.md",
        "docs/book/src/plan/p4/gate.md",
        "docs/book/src/plan/p4/m.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p4/contract-control.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/plan/multicore.md",
        "docs/book/src/contracts/evidence-and-gates.md",
        "docs/book/src/contracts/sources.md",
        "docs/book/src/data/overview.md",
        "docs/book/src/working/task-trees.md",
        "docs/book/src/working/claim-verification.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md",
      "term": "Profile"
    },
    {
      "aliases": [
        "Proved"
      ],
      "chapters": [
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4/interrupts.md",
        "docs/book/src/plan/p4/fence-i.md",
        "docs/book/src/plan/p4/m.md"
      ],
      "definition": "glossary.md",
      "term": "Proved"
    },
    {
      "aliases": [
        "Requirement"
      ],
      "chapters": [
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/sv39.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/fence-i.md",
        "docs/book/src/plan/p4/floating-point.md",
        "docs/book/src/plan/p4/gate.md",
        "docs/book/src/plan/p4/c.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-runtime.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/contracts/cpu-environment.md",
        "docs/book/src/contracts/evidence-and-gates.md",
        "docs/book/src/data/overview.md",
        "docs/book/src/data/worked-example.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md",
      "term": "Requirement"
    },
    {
      "aliases": [
        "RV64I"
      ],
      "chapters": [
        "docs/book/src/claim-scope.md",
        "docs/book/src/models.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/privilege.md",
        "docs/book/src/plan/p4/contract-v2.md",
        "docs/book/src/plan/p4/contract-integer.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/annex/assembler.md",
        "docs/book/src/annex/building-first-model.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "RV64I"
    },
    {
      "aliases": [
        "Software computer"
      ],
      "chapters": [
        "docs/book/src/introduction.md"
      ],
      "definition": "glossary.md",
      "term": "Software computer"
    },
    {
      "aliases": [
        "SR"
      ],
      "chapters": [
        "docs/book/src/models/the-information-a-unit-demands.md"
      ],
      "definition": "glossary.md#the-acronyms-this-book-uses",
      "term": "SR"
    },
    {
      "aliases": [
        "Validated"
      ],
      "chapters": [
        "docs/book/src/introduction.md",
        "docs/book/src/claim-scope.md",
        "docs/book/src/models/the-information-a-unit-demands.md",
        "docs/book/src/plan/overview.md",
        "docs/book/src/plan/p0.md",
        "docs/book/src/plan/p1.md",
        "docs/book/src/plan/p2.md",
        "docs/book/src/plan/p3.md",
        "docs/book/src/plan/p4.md",
        "docs/book/src/plan/p4/atomics.md",
        "docs/book/src/plan/p4/contract-memory.md",
        "docs/book/src/plan/p5-p7.md",
        "docs/book/src/contracts/cpu-environment.md",
        "docs/book/src/contracts/review-disposition.md",
        "docs/book/src/working/task-trees.md",
        "docs/book/src/working/doctrines.md",
        "docs/book/src/annex/assembler.md"
      ],
      "definition": "glossary.md",
      "term": "Validated"
    },
    {
      "aliases": [
        "Verification disposition"
      ],
      "chapters": [],
      "definition": "glossary.md",
      "term": "Verification disposition"
    }
  ]
}
```

Producer scripts/qualify_book_index.py, mode644, 15230B, SHA256
84dace38a877b667cf347a9a2f23b0d58e6cd5198686a189f0fa682d53d9386b.

## Complete owned source inverse

Apply these explicit owned seams to the immutable source; all final owned
root/pointer/book bytes must match. Reverse them in reverse order to restore
the complete source, not only selected passages. Toolbox adds exactly one
discovery row; every original byte remains its prefix. Complete old CH/DEV
entries roll only through the published sharder and are jointly authenticated.

```json
{
  "activation": [
    [
      "docs/tasks/LIVE-CONTAINMENT.md",
      ".4i2b4b qualify index/query expansion after LC0031 normal COMMIT",
      ".4i2b4b1 qualify the project-book index consumer; other query readers follow"
    ],
    [
      "docs/tasks/LIVE-CONTAINMENT.md",
      "#### .4i2b4b / SEMULITH-LC-0032 \u2014 qualify index/query expansion (pending)\n\nPin fresh source/current membership and public index/query interfaces; qualify\nactual expansion, exclusions, failed inputs and omissions before repairs.\n",
      "#### .4i2b4b \u2014 qualify index/query expansion (active, decomposed)\n\nProject-book index first (.4i2b4b1/LC0032); orientation/record indexes next\n(.4i2b4b2), then catalogue/archive queries and reconciliation (.4i2b4b3).\nGenerated navigation/resources remain .4i2b5; full graph/adoption stays open.\n\n##### .4i2b4b1 / SEMULITH-LC-0032 \u2014 qualify the project-book index consumer\n\nOwned on clean32f9c31 after normal hooks/exact12-file postcheck/brief0/host0.\nPin all1443 immutable identities and actual HEAD/index/working inputs. Discover\nonly through the owned Git tree; Gitlinks remain opaque. An earlier broad\nfilename search listed Gitlink paths; no implementation content or inferred\nassumption is consumed. All following discovery excludes that boundary.\nOwn scripts/qualify_book_index.py, its toolbox row and the canonical record\n docs/tasks/artifacts/live-containment/book-index-consumer.md. Execute both\npublic project index interfaces in isolated repository-volume fixtures normal/O;\nobserve exact source reads, terms, chapter membership/order, exclusions and\noutput. Qualify missing/changed/invalid inputs, independent membership and real\nomissions before repairs; record every observed defect with a scheduled owner.\nNo existing generator/guard behavior change in this assessment unit. Preserve\nall older receipts/archives/modes, full CH/DEV entries and fixed caps; teach the\nactual index scope in the mdBook. Outputs: target/live-containment/book-index-consumer.\nD72 candidate: BOOK-APPARATUS metadata says done while its root task entry says\nactive and .1 commit says pending. Reconcile with canonical records and tools in\n.4i2b4b2 before classifying or correcting; no historical receipt is rewritten.\n"
    ],
    [
      "MEMORY.md",
      "- next_action: LC.4i2b4b \u2014 qualify index/query consumers after LC0031 COMMIT.",
      "- next_action: LC.4i2b4b1 / LC0032 \u2014 qualify the project-book index consumer."
    ],
    [
      "MEMORY.md",
      "- in_flight_uncommitted: none after LC0031 normal COMMIT; full adoption remains LC.4.",
      "- in_flight_uncommitted: LC0032 assessment owned; full adoption remains LC.4."
    ],
    [
      "docs/tasks/LIVE-CONTAINMENT.md",
      "D72 candidate: BOOK-APPARATUS metadata says done while its root task entry says\nactive and .1 commit says pending. Reconcile with canonical records and tools in\n.4i2b4b2 before classifying or correcting; no historical receipt is rewritten.\n",
      "D72 candidate: BOOK-APPARATUS metadata says done while its root task entry says\nactive and .1 commit says pending. Reconcile with canonical records and tools in\n.4i2b4b2 before classifying or correcting; no historical receipt is rewritten.\n\nD73 verified normal (`2026-10-12`): actual source read failure produces traceback/\nexit1 in both public interfaces; invalid UTF-8 also gives generator traceback1.\nThe generator promises unsupported/unjudgeable inputs refuse2; the wrapper\nclassifies a real failed read as index drift1. Missing-source cases do refuse2.\nReproduce: python3 scripts/qualify_book_index.py --output target/live-containment/book-index-consumer/reproduce.\nExit0 means measurement complete; inspect observations, not a green safety claim.\nRoot cause: uncaught Path.read_text errors in gen_book_index.py; the shell's\nactual generator failure branch rewrites all nonzero results to1. Priority1;\nowner .4i2b4b1r/LC0033 repairs and verifies these boundaries immediately after\nthis assessment COMMIT, before other query readers. Qualification producer\nalso owns actual-read digest/omission controls and a working-code replay mode.\n\n##### .4i2b4b1r / SEMULITH-LC-0033 \u2014 repair D73 public index refusal (pending)\n\nPreserve typed input refusal2 in generator and guard, valid bytes and original\nsix shell controls. Add actual public read/Unicode controls normal/O and copied\nomissions; update book/registry mirrors only where actual scope changes.\n"
    ]
  ],
  "closing": [
    [
      "docs/book/src/working/task-trees.md",
      "### Decision navigation and the record it opens\n",
      "The term index scans raw SUMMARY chapters, glossary terms and acronyms.\nIt excludes glossary/index discussion hits; includes stay unexpanded.\nExit0 below means measurement complete, including D73 failures:\n\n```sh\npython3 scripts/qualify_book_index.py --output target/live-containment/book-index-replay/book\n```\n\n### Decision navigation and the record it opens\n"
    ],
    [
      "docs/tasks/LIVE-CONTAINMENT.md",
      ".4i2b4b1 qualify the project-book index consumer; other query readers follow",
      ".4i2b4b1r repair D73 public index refusal after LC0032 normal COMMIT"
    ],
    [
      "docs/tasks/LIVE-CONTAINMENT.md",
      "##### .4i2b4b1r / SEMULITH-LC-0033 \u2014 repair D73 public index refusal (pending)\n",
      "Verified LC0032 assessment (`2026-10-12`): all1443 source identities pinned,\n54 fixture inputs; independent declaration/term expansion reproduces all49\nchapters/40 terms and53 actual source reads in exact order with full content\nidentities. Both public baselines pass. The index scans raw source chapters,\nnot expanded includes; glossary/index discussion occurrences are deliberately\nexcluded. Complete memberships, terms/aliases/hits, source pins and child\nverdicts: docs/tasks/artifacts/live-containment/book-index-consumer.md.\n\nNormal/O and actual-working-code replay agree. Twelve input cases across both\npublic interfaces produce24 observations per mode. Five real read classes\n(SUMMARY/chapter/canonical glossary/acronyms/generated index) plus two invalid\nUTF-8 generator cases expose12 D73 verdict defects per mode. Every injected\nread fault fires exactly once. Three real copied generator omissions (chapter,\nterm, discussions) return drift1; omitted-read and forged-read-digest ledger\ncontrols refuse2. No actual source/index/mode changes; Gitlinks stay opaque.\n\n- [x] **ROOT CAUSE** \u2014 `python3 scripts/qualify_book_index.py --output target/live-containment/book-index-consumer/final-normal` rc=0 measures12 original D73 child failures with traceback1; exact stack reaches Path.read_text and wrapper's failure branch. Exit0 marks completed measurement, not absence of defects. D73 priority1 repair is owned immediately next.\n- [x] **ADDRESSED** \u2014 tracked producer normal/O and `--working-code` rc=0 reproduce49 chapters/40 terms/53 full actual reads,54 input pins,24 observations, three real omissions and two independent ledger refusals per mode. Complete retained source/consumer record and replay commands are canonical; existing generator/guard semantics are unchanged.\n- [x] **NO REGRESSION** \u2014 focused12/sharder12/seven books plus existing six BOOK-INDEX controls normal/O; whole normal/print teaching and literal tracked replay pass. Whole old CH/DEV entries/order, every older archive/seal and protected source modes/Gitlink remain exact; staged full inverse and normal COMMIT are required before LC0033.\n- [x] **LOCKSTEP** \u2014 task/pointer/CH/DEV/book/toolbox and canonical record align; LIVE1571, all caps, CPU/MCU/DSP/board and full graph/adoption scope unchanged. promotion: declined (existing inventory contract and source-pinned consumer evidence own this assessment).\n\n##### .4i2b4b1r / SEMULITH-LC-0033 \u2014 repair D73 public index refusal (pending)\n"
    ],
    [
      "MEMORY.md",
      "- next_action: LC.4i2b4b1 / LC0032 \u2014 qualify the project-book index consumer.",
      "- next_action: LC.4i2b4b1r / LC0033 \u2014 repair D73 public index refusal."
    ],
    [
      "MEMORY.md",
      "  D65/D68 fixed; full graph/adoption and CPU qualification remain open.",
      "  D73 is priority1; full graph/adoption and CPU qualification remain open."
    ],
    [
      "MEMORY.md",
      "- in_flight_uncommitted: LC0032 assessment owned; full adoption remains LC.4.",
      "- in_flight_uncommitted: none after LC0032 normal COMMIT; full adoption remains LC.4."
    ],
    [
      "docs/tasks/LIVE-CONTAINMENT.md",
      "- [x] **NO REGRESSION** \u2014 focused12/sharder12/seven books plus existing six BOOK-INDEX controls normal/O; whole normal/print teaching and literal tracked replay pass.",
      "- [x] **NO REGRESSION** \u2014 `bash target/live-containment/book-index-consumer/focused.sh` rc=0: focused12/sharder12/seven books; original six BOOK-INDEX controls normal/O, whole normal/print teaching and literal tracked replay also pass."
    ]
  ]
}
```

Preparation: SEAM-INTEGRITY rejected the first NO REGRESSION checklist wording
because it omitted the executed command/rc signature. Add the actual focused
command and rc=0; retain the complete extra seam in the full source inverse.
