# P4-SYSTEM.13 c29d — historical book verification receipts

Finite immutable payload, captured from source commit
`6addc986810de6d913a1c9389c58f1866cf771aa` by SEMULITH-P4-0167.
These are dated execution receipts, not current dependency or coverage claims.
Current features, commands, worked examples and limits stay in the book.
Each original span includes its exact paragraph separator. The map records
source and replacement byte offsets. Remove the chapter footer, undo spans
in descending replacement-offset order, then authenticate full source bytes/SHA.
No later receipts are appended to this payload.

## Inverse map

```json
[
  {
    "path": "docs/book/src/plan/p4/c.md",
    "name": "c",
    "source_bytes": 32593,
    "source_sha256": "c258ed830d6bf04b5cfea0916d518d6323bd636fdda2f3bc929af5d35df96d5f",
    "proposed_bytes": 29216,
    "proposed_sha256": "9b5a2b0e9de88eebc917e745d5d0ac755fd0edf737cd058d83100ea1c9254fcc",
    "footer": "\n## Historical verification receipts\n\nDated progress counts, pre-bind identity checks and exact provenance receipts\nare preserved in `docs/tasks/archive/P4-SYSTEM-book-c29d.md`, section `c`.\nThat record authenticates the original chapter and every removed span; all\ncurrent feature examples and commands remain here.\n",
    "spans": [
      {
        "paragraph": 8,
        "old_offset": 3507,
        "new": "Slice (c1) adds an exact two-byte instruction request to\nthe environment boundary. The old request always read four bytes, even when the processor\nkept only the first two; it could not fetch a compressed instruction at the end of a two-byte\nmemory region. The new request succeeds there, keeps the same alignment and code-visibility\nrules, and lets fault injection distinguish the requested parcel from its neighbor.\n\n",
        "old_sha256": "499d905f23ed4bf62dc1cb593d327fca1c9e0408810804ffe70565ff1a785257",
        "new_offset": 3507
      },
      {
        "paragraph": 9,
        "old_offset": 4053,
        "new": "For C-enabled execution, the processor requests one parcel first and requests another\nonly when the instruction needs it. This replaces the earlier coalescing plan: a four-byte\nrequest cannot distinguish a failure in an unnecessary upper half from a failure in the\ninstruction itself. Fetch counts measure physical parcels.\n\n",
        "old_sha256": "eb0e636e82ebce1efb8431a0e092460a8a9c705e6d035ef1206733b574acd08b",
        "new_offset": 3925
      },
      {
        "paragraph": 13,
        "old_offset": 6337,
        "new": "Slice (d2) carries exact byte images through guest generation and the rv64gc runner.\nThe generator's byte mode emits u8 arrays and the runner loads them directly. The scalar\nfixture keeps its word API for replay and reduction. A generated 14-byte mixed program runs\non the temporary C composition, checking the actual loaded bytes, a four-byte instruction at\na two-byte offset, a jump over an illegal parcel and a trailing halfword. Its five executed\nsteps request six parcels. Padding the image or moving the loader's offset makes the checks\nfail.\n\n",
        "old_sha256": "bc3c075c74709a51bb645222896f61bf8b7f41816987bf26ff3b5b063ccd1155",
        "new_offset": 6126
      },
      {
        "paragraph": 14,
        "old_offset": 6967,
        "new": "The independent expectation author computes spec-side values and offers\nnon-writing checks. Reserved upper bits interpreted as ordinary operations and missing\nSUM/MXR/U permissions in its data walk were repaired. Direct permission fixtures and deliberate mutations guard\nthese repairs without using the instruction engine as an oracle. Historical\nrecords retain their original provenance.\n\n",
        "old_sha256": "7b129bd2fd644627db7fc665d135ae0d16c76f855c5c546f300dc034e4a98f55",
        "new_offset": 6676
      },
      {
        "paragraph": 16,
        "old_offset": 8154,
        "new": "",
        "old_sha256": "3b8c68faac5cc9b42dd3c0fcf97fc089fca0de0be5f31fd9646ccc8c57de1142",
        "new_offset": 7556
      },
      {
        "paragraph": 18,
        "old_offset": 9309,
        "new": "The permanent probe checks every form and its effect, immediate extremes,\n79 individual scattered bits, hints and reserved cases. A permutation of two\nimmediate bits can pass an all-ones limit, so individual-bit checks matter.\nMutations include a wrong two-byte link and reporting the expanded word as\nthe trap value.\n\n",
        "old_sha256": "5fcb02eeacdf9c4f0aefd58c46599335c2551b78ab847e4c4731216ba0fcff8f",
        "new_offset": 8184
      },
      {
        "paragraph": 21,
        "old_offset": 11118,
        "new": "The new fixtures exposed four older walk defects: an inconsistent Sv39 sign extension\nwas accepted, reserved high PTE bits were ignored, a bottom-level pointer refused instead\nof page-faulting, and MPRV did not select effective data privilege. These are repaired,\nincluding reserved non-leaf U/A/D bits and effective SUM/U permissions. Odd instruction\naddresses exposed a fifth defect in the author: saved exception and interrupt PCs retained\nbit zero. Both M and S delivery now clear that bit while preserving bit one. Nine deliberate\nmutations fail on these guards and fetch schedules.\n\n",
        "old_sha256": "68046dd5e261128f4b9715153847427edfbc261417773788b33fd93417fcfc24",
        "new_offset": 9780
      },
      {
        "paragraph": 24,
        "old_offset": 13197,
        "new": "These are finite component observations. The\n[assembler chapter](../../annex/assembler.md) documents the explicit authoring\ncommand and its budget semantics.\n\n",
        "old_sha256": "adbe2c5a725335b4b618496f6479c1ff77fbdb07c7a5e278108a6122fe540807",
        "new_offset": 11640
      },
      {
        "paragraph": 25,
        "old_offset": 13555,
        "new": "The pre-bind census identified prerequisites in the independent author:\nfixed `misa` fields, privileged legality, base vocabulary and the selected\ntranslation cache. These were repaired before staging adopted parcel counts.\n\n",
        "old_sha256": "c69deb98d9307e8065074c1d60186579074a685b9144ce6ca597ba5ea46f95de",
        "new_offset": 11799
      },
      {
        "paragraph": 26,
        "old_offset": 14087,
        "new": "Slice (e1b1) adds the base integer vocabulary:\ncomparisons and XORI, XLEN and word shifts, signed/unsigned branches, and narrow memory\nstock derivations. Word shifts use five count bits and sign-extend their 32-bit result;\nXLEN shifts use six. A named reserved-word outcome lets parcel execution deliver the\ndeclared diagnostic before effects, keeping the full raw word and no retirement.\nUnknown valid vocabulary continues to refuse. Its permanent controls now use an\nunmodeled real CSR because XORI and byte loads have become supported operations.\n\n",
        "old_sha256": "1e5defa4685419b80e25750708945f1357f3514ea55bc9965cccba4d95d88d3a",
        "new_offset": 12024
      },
      {
        "paragraph": 27,
        "old_offset": 14677,
        "new": "Hand arithmetic/alias/x0, branch, narrow-memory and reserved fixtures guard\nthe base vocabulary, with deliberate mutations. Historical production records\nwere preserved during prerequisite repairs.\n\n",
        "old_sha256": "1a3401794ebe026e8e8944ddbd28da5eb7584fe7ff572be05a9c31c37126c956",
        "new_offset": 12575
      },
      {
        "paragraph": 28,
        "old_offset": 15159,
        "new": "Slice (e1b2) completes the CSR/directive vocabulary. The independent author now\nregisters and legalizes the selected counter-enable and STCE fields. Supervisor timer\ncompare access needs both enable gates before effects, while machine mode bypasses\nthem. Source annotations can contain quotes and backslashes; every emitted literal\nfield uses the canonical renderer and round-trips through the reader and schema.\n\n",
        "old_sha256": "9e5287aa96efa97755041062c999b5f4af4152f02d543ef2ca2aee539eafd4f5",
        "new_offset": 12774
      },
      {
        "paragraph": 29,
        "old_offset": 15578,
        "new": "Mode-gate, mask/alias and literal-text fixtures guard the CSR/directive\nvocabulary, with deliberate mutations. The translation cache was the final\nprerequisite before count adoption.\n\n",
        "old_sha256": "04dbbdf15e661ed1daed5add637f57004239ce07cb1fcb734699d6e28f78d410",
        "new_offset": 13188
      },
      {
        "paragraph": 30,
        "old_offset": 16006,
        "new": "Reviewing that cache prerequisite exposed an older production fence defect (e1c0).\nThe fence used operand values to choose broad scope, confusing a nonzero register\nholding zero with register x0. The semantic effect now carries register-identity\nselectors separately from the address and ASID. Three parent-failing regressions pass,\nincluding page/ASID zero and masked ASID bits; the earlier fence fixture is corrected\nand armed with an occupied cache. The [Sv39 chapter](sv39.md) explains the four cases.\n\n",
        "old_sha256": "6ab659cc169e2bf570a216c2a8f689abb88f029ea55f114d9f0ab2333b93e37b",
        "new_offset": 13372
      },
      {
        "paragraph": 32,
        "old_offset": 17224,
        "new": "Hand page-table fixtures check replacement order, permissions, roots, ASIDs,\nglobals, zero selections and illegal/invalid fences. Deliberate mutations and\nthe uncached parent fail the stale-mapping fixture. Historical parcel\nobservations and a cold repeat of the cache request schedule agree; no\nproduction record was overwritten during staging.\n\n",
        "old_sha256": "16f20fb6a23e4e3f4c3bb84bbaa23071f0ce9d65467ac2bc7fe74a34354be15e",
        "new_offset": 14453
      },
      {
        "paragraph": 44,
        "old_offset": 23508,
        "new": "The production composition contains 197 instruction rules plus three counter\npseudos, with all 200 spellings exercised. The 28 new C programs brought the\ncorpus to 167. Binding migrated the 139 older records from 4,888 word requests\nto 9,770 parcels across 4,913 boundaries, preserving every other record byte\nand the old engine PC/mode/register-write traces. Five public-CLI C controls\ndistinguish the unbound parent from the bound model.\n\n",
        "old_sha256": "6e2c30887a85e442ad49dd3fd96c2029ca80b0abbbaee83e877e7ca6712d805e",
        "new_offset": 20399
      },
      {
        "paragraph": 45,
        "old_offset": 24165,
        "new": "Open v2 includes C's guarantee and exact two-byte physical fetch supply,\nwith their four positive/negative check IDs realized. Frozen v0/v1 records and\npins remain unchanged. The seven-axis matrix includes compressed faults and\ninterrupt return in place of the earlier boundary/restart degeneracy; two\nother declared degeneracies remain.\n\n",
        "old_sha256": "40e3fa3aeb3c475ad91aac297375337f2e5202785ffacf4ae61e8337aa59f767",
        "new_offset": 20840
      },
      {
        "paragraph": 51,
        "old_offset": 26912,
        "new": "The experiment also exposed an adapter defect: it recognized the historical author’s\ninterrupt description but not the parcel author’s numeric-cause description. Both\nexact spellings now require the matching trace event. Missing/wrong events and an\ninstruction row at that delivery boundary fail; disabling the new spelling fails the\npermanent control.\n\n",
        "old_sha256": "8d651bee20a29ea67b978ea55416a94e671aa096533e2d0fa0b3616e37da6053",
        "new_offset": 23527
      },
      {
        "paragraph": 52,
        "old_offset": 27301,
        "new": "These comparisons judge declared GPR changes and witnessed delivery gaps. They do\nnot independently compare unrecorded PCs, words, FP registers, memory, CSRs or physical\nrequest counts. The trap CSR values read back into GPRs are within the comparison.\nThe ninth experiment is recorded in the reference dossier; structured experiment and\nindependence records remain `.14`'s work.\n\n",
        "old_sha256": "8480902d2889dbfe08d985319e1fb7f55611545c559e114684ed66a255a9bfe0",
        "new_offset": 23885
      },
      {
        "paragraph": 53,
        "old_offset": 27727,
        "new": "The C leaf closed after full local CI: Rust format, strict Clippy and all\ntests, every doctrine, wasm bench, headless bench smoke and all books. Its\nexpansion citations, compiled mappings/decoder, complete scope/corpus, parcel\nfaults and qualified public reference observations meet its acceptance. The\ntimer-platform limit remains explicit. P4 is 12/18 and CPU-SYSTEM remains\nincomplete; contract v2 completion is P4.13's work.\n\n",
        "old_sha256": "a90faa0d1109185553f53df14ddf7f7b4f8c63816f2c93b193f3ba6e73e8ba47",
        "new_offset": 24266
      }
    ]
  },
  {
    "path": "docs/book/src/plan/p4/floating-point.md",
    "name": "floating-point",
    "source_bytes": 14661,
    "source_sha256": "ac982cf887ed4088f1cc359f8f731662b75e0210b637ab428282d50f1bad0574",
    "proposed_bytes": 13909,
    "proposed_sha256": "529f3383aed936655a0ee09be5f3041857d3247f68d5ebcf74d30b1360b9662b",
    "footer": "\n## Historical verification receipts\n\nDated progress counts, pre-bind identity checks and exact provenance receipts\nare preserved in `docs/tasks/archive/P4-SYSTEM-book-c29d.md`, section `floating-point`.\nThat record authenticates the original chapter and every removed span; all\ncurrent feature examples and commands remain here.\n",
    "spans": [
      {
        "paragraph": 14,
        "old_offset": 9015,
        "new": "Eleven double-precision programs were authored from the specification\nbefore any processor-engine run.\n\n",
        "old_sha256": "c0b46fbb5df4e00ed6bab5b35b161a4c64ddefa3003be72347a359ad57772cb1",
        "new_offset": 9015
      },
      {
        "paragraph": 15,
        "old_offset": 9370,
        "new": "The profile composes D, and all 32 double-precision forms execute in the\ntracked engine alongside F. Both extensions are part of the processor.\n\n",
        "old_sha256": "0056627a4edacc261505cc9d71ad3ce6f1023078ed21f8b26d1c236fe347be02",
        "new_offset": 9119
      },
      {
        "paragraph": 25,
        "old_offset": 13255,
        "new": "The Machine/F/D pages are authenticated through their dossier source pins.\nC29c corrects the\nstate descriptor and F requirement detail to state the same selected policy;\nthe current requirement statement and frozen obligation remain identical. The\nstatement promises Dirty whenever values change, without excluding unchanged\nwrites. Numerical contract realization and structured experiment registration\nremain separate work.\n\n",
        "old_sha256": "66e6e0a964079abc5640617b1743b969526660d643c345f4e0184005f0ac878a",
        "new_offset": 12665
      },
      {
        "paragraph": 26,
        "old_offset": 13944,
        "new": "The descriptor also supplies read-only census explanations in generated\ninspection metadata. A prose change therefore requires published regeneration\nand exact provenance/metadata checks. C29c changed one source hash and two\nexplanations in the state module, and two hashes in the definition; state\nlayout, CSR owners, resets, accessors and instructions stayed byte-identical.\nIts stale-provenance refusals and complete source identities are retained\nwith the historical receipts below.\n\n",
        "old_sha256": "73d631d95704eae1e045f5217be384fd7d04ec5d0debe525bcb569e59f36bcb6",
        "new_offset": 13091
      }
    ]
  },
  {
    "path": "docs/book/src/plan/p4/contract-v2.md",
    "name": "contract-v2",
    "source_bytes": 31527,
    "source_sha256": "9e6a05cadeafab77988f2440240681d0c6454ad44cd04116ea5c4c83cbe9a514",
    "proposed_bytes": 30251,
    "proposed_sha256": "23a4648352a84ef5924ea54e2bc64a4cc0187d5f96b0f62ad9caaa65100efce9",
    "footer": "\n## Historical verification receipts\n\nDated progress counts, pre-bind identity checks and exact provenance receipts\nare preserved in `docs/tasks/archive/P4-SYSTEM-book-c29d.md`, section `contract-v2`.\nThat record authenticates the original chapter and every removed span; all\ncurrent feature examples and commands remain here.\n",
    "spans": [
      {
        "paragraph": 11,
        "old_offset": 3584,
        "new": "The inventory correction updates generated inspection metadata and source\nprovenance without changing storage, reset values, accessors or execution.\nSnapshot and replay serialization belong to P4.16; the inventory does not\nclaim those features are implemented.\n\n",
        "old_sha256": "d11f45584c2e550a39af9e0f32e7b05faef091a2a94cdb874a36a891dc1254f6",
        "new_offset": 3584
      },
      {
        "paragraph": 19,
        "old_offset": 6032,
        "new": "Selection evidence comes from these explicit predicates, rather than an\nunrelated passing program. Version 2 remains open.\n\n",
        "old_sha256": "50b319d24ff0962808121b6ce72441c5b2b91ca67f6ef5e78f078bda09ba8c2b",
        "new_offset": 5914
      },
      {
        "paragraph": 24,
        "old_offset": 7272,
        "new": "These are selection and consistency checks. CSR field behavior and\ninstruction semantics retain their execution evidence; firmware is future work.\nDated progress and containment receipts remain available below.\n\n",
        "old_sha256": "f6f34f5916b6b28d4786bb1c6ad593ce7862605d550ac4a0f7aa1ac3691f1fbd",
        "new_offset": 6997
      },
      {
        "paragraph": 31,
        "old_offset": 9034,
        "new": "Four pairs check ABI, firmware, ordering and privileged selections, each\nwith a positive predicate and specific violating copies:\n\n",
        "old_sha256": "833f0e8d806c213c5ef7a23adc4f8b03a9cdb49dc73bd7373d7cfec9293618e3",
        "new_offset": 8578
      },
      {
        "paragraph": 40,
        "old_offset": 12199,
        "new": "",
        "old_sha256": "f5edd4b364485267bae871c8c5eb018d26cf0a8c4e2ef33fb60289632a1bae4f",
        "new_offset": 11715
      },
      {
        "paragraph": 44,
        "old_offset": 12769,
        "new": "Paths start at the repository root, so moving the checkout keeps them valid.\nThe frozen parts contain their original contiguous record bytes. Expansion at\nthe split reproduced the original 63,014 bytes, order, 58 mappings and frozen\npins exactly. No ceiling was raised or duplicate materialized catalog added.\n\n",
        "old_sha256": "2d1fd49e8a97dd74bbef7501cb07711a969ab7f6b3ab0cc61775a6702109124e",
        "new_offset": 12137
      },
      {
        "paragraph": 55,
        "old_offset": 16117,
        "new": "The registry has explicit `Evidence::Boundary` entries. Its normal tests\nrun both fixtures; every post-v0 declaration is born realized. These finite\ncases do not prove correctness for every possible address or environment.\n\n",
        "old_sha256": "e215a89e6c38e21bea01fd09d382dacd3b5317e620adfcc6d214b3e956258cfb",
        "new_offset": 15336
      },
      {
        "paragraph": 62,
        "old_offset": 18309,
        "new": "Four permanent core tests exercise all 25 request/response-kind combinations,\nnarrow-width edges, full-width values, unchanged target failures and existing\nviolations, and actual GC/scalar/translation paths.\n\n",
        "old_sha256": "633a942456b1462a70d4ac971b36f81a1d9bd5bcb82d0b3d28548e6899146bba",
        "new_offset": 17357
      },
      {
        "paragraph": 89,
        "old_offset": 26136,
        "new": "",
        "old_sha256": "fd4caa495c829a2a0507b20b89ae640f8bfc017682364e7c1419bfc7877f63fc",
        "new_offset": 24996
      },
      {
        "paragraph": 96,
        "old_offset": 28591,
        "new": "Only cold reset is supported. Snapshot restoration and warm/retained-state\nordering need their own implementation and contract.\n\n",
        "old_sha256": "74f82936314f7d471da42c745a70ef72d4bd18a258e6b8f918f6673d91198511",
        "new_offset": 27212
      },
      {
        "paragraph": 98,
        "old_offset": 28995,
        "new": "The [runtime contract chapter](contract-runtime.md)\ncontains privilege-mode, Sv39, Svade, IALIGN-16, Zicntr, Sstc and direct implicit\nwalk/fetch/data request evidence.\nThe [integer runtime chapter](contract-integer.md) retains immediate/register ALU,\nU-immediate, twelve-form shift, nine-form RV64I word-result and direct 64-bit\nregister/user-address bindings, worked\nvalues, SRAW/SRAIW count-mask/source-width repairs and SHAMT requirement correction.\nThe [control transfer chapter](contract-control.md) retains immediate transfers,\nJALR's inherited-annotation diagnosis and direct target/link/request witnesses.\nThe [memory runtime chapter](contract-memory.md) retains eleven-form load/store\nextension, discarded-load requests/faults, selected byte-order observations and\nFENCE field/no-effect and atomic pre-translation alignment observations.\nThese chapters preserve independent controls and finite evidence limits. Current G-CONTRACT is\n102/114; six runtime pairs and final freeze remain. The\n[instruction-visibility chapter](fence-i.md#direct-contract-observations) adds\nignored-field and patched-parcel FENCE.I witnesses. The [atomics chapter](atomics.md#direct-contract-observations) adds literal A-operation, alias, reservation-effect and translated-fault witnesses. The earlier runtime split preserved every section byte-for-byte; dated\nverification receipts are now routed below.\n\n",
        "old_sha256": "50084ad74efb3bfe284991fdf8a887c2434109349a81b21a3d9ef1a6f4dc67ab",
        "new_offset": 27374
      }
    ]
  },
  {
    "path": "docs/book/src/plan/p4/contract-runtime.md",
    "name": "contract-runtime",
    "source_bytes": 27898,
    "source_sha256": "aa64d6c882d6b8b17c0fd12c65cccb89014e910583b5ef49ed6139ad177aa582",
    "proposed_bytes": 26600,
    "proposed_sha256": "cf221e073577f42b66f2acedaf534b3a5c83ec954adf35ed85cea4e6dbae2b8b",
    "footer": "\n## Historical verification receipts\n\nDated progress counts, pre-bind identity checks and exact provenance receipts\nare preserved in `docs/tasks/archive/P4-SYSTEM-book-c29d.md`, section `contract-runtime`.\nThat record authenticates the original chapter and every removed span; all\ncurrent feature examples and commands remain here.\n",
    "spans": [
      {
        "paragraph": 7,
        "old_offset": 1464,
        "new": "",
        "old_sha256": "a934bf788544939c75e05af1e9982a05848fd4fc94cee1c065cacdd15cb99a1f",
        "new_offset": 1464
      },
      {
        "paragraph": 10,
        "old_offset": 2212,
        "new": "The independent expectation author already inherited G correctly and remains\nunchanged. This fixes the declared retention policy rather than broadening the\nISA claim.\n\n",
        "old_sha256": "5a2bdc38f5092d1df817ad745a3cd3a8f73f3940160b804035dcf9b27ae22770",
        "new_offset": 1971
      },
      {
        "paragraph": 14,
        "old_offset": 3332,
        "new": "The matrix spans 1,417 execution boundaries and 2,832 physical parcel\nrequests. Re-executing the independent parcel author reproduces every\ncommitted register-change sequence and fetch count exactly. Neither the\nprograms nor their expectations changed. This is finite translation evidence,\nnot universal Sv39 or Linux acceptance.\n\n",
        "old_sha256": "819ba605b7232cfbbebeb714f82f94d87119c31032a2d2b14d294d0e1d07458f",
        "new_offset": 3016
      },
      {
        "paragraph": 19,
        "old_offset": 4837,
        "new": "These witnesses retain the existing ISA observation vocabulary and finite scope.\nThe selected policy faults instead of updating A/D; Svadu is excluded.\n\n",
        "old_sha256": "c03cc9cd4bcbd602a07d71a5594a784cfe73de7fc2d1953413528b983f5da9cd",
        "new_offset": 4425
      },
      {
        "paragraph": 27,
        "old_offset": 6939,
        "new": "",
        "old_sha256": "6f1ad3f8f90cf84a9bfaee93b309aa460547aaa172fb8002d329c47059eb9f48",
        "new_offset": 6437
      },
      {
        "paragraph": 33,
        "old_offset": 8962,
        "new": "",
        "old_sha256": "dc46f11b004ea0c54ff0968120b25b16efa47241ed8729ecd38dda87187f6e32",
        "new_offset": 8302
      },
      {
        "paragraph": 41,
        "old_offset": 11211,
        "new": "Fresh pinned Sail attempts agree on w-sw (19 boundaries, two identical traces).\nSix inputs diverge: c-irq at 11, env-irq-sources at 12, i-prio at 26,\ni-timer at 5, mm-wfi at 11 and w-deleg at 14. The trace witnesses absent\ncomparator pending or continued execution instead of declared delivery/wait.\nw-notrap and w-timer processes refuse (rc1): their time/instret reads trap with\nZicntr disabled and enter trap loops. Old inputs reproduce those refusals.\nThe public timer diagnostic now enables STCE and reads back bit 63 on both\nsides before comparing pending state (ten boundaries, repeat traces identical).\nIts old seven-boundary STCE-clear result was confounded by the overlay defect\nand cannot alone establish a reference cause. Public configuration validation\nstill rejects Zicntr without a time source and\nCLINT without a mapped region. These are qualified reference-platform limits;\nfailed processes are never counted as agreement. Structured experiments remain\nP4-SYSTEM.14's work.\n\n",
        "old_sha256": "79007d341efdd27ccf2d21242d823105ea801287bf78d3862e5b4a4b5e504ead",
        "new_offset": 10390
      },
      {
        "paragraph": 53,
        "old_offset": 17216,
        "new": "The direct S-mode witnesses below earn the SSTC pair; neither prerequisite\nrepair nor this pair establishes firmware/Linux capability.\n\n",
        "old_sha256": "1c4aed19f0f340721c67a941e49daac8b13dbbd6bb1341106352dfbb5e214e31",
        "new_offset": 16258
      },
      {
        "paragraph": 61,
        "old_offset": 20936,
        "new": "",
        "old_sha256": "6b05750134bbad39ce3e1feeb2205bcc286d64aa085bbcea3b6bfa025d93e950",
        "new_offset": 19956
      },
      {
        "paragraph": 62,
        "old_offset": 21253,
        "new": "The registry self-test creates its synthetic declaration only in scratch\ndata and measures its own registration, so real ALU registration cannot break\nits assumptions. Controls reject duplicate credit and distinguish full\neffective coverage from a newly missing check. A duplicate-counting mutant\nfails. This gate repair grants no CPU credit.\n\n",
        "old_sha256": "fc81b57f81b83e108b4444bb5a2fa883d5a718c825b270c6a96b950c460c1e6a",
        "new_offset": 19956
      }
    ]
  }
]
```

## c

Source `docs/book/src/plan/p4/c.md`: 32593 bytes; SHA-256
`c258ed830d6bf04b5cfea0916d518d6323bd636fdda2f3bc929af5d35df96d5f`.

### c paragraph 8

<!-- c29d payload: c:8 -->
````text
The session crashed during slice (b); the task-tree and surviving files recovered its exact
frontier. PNT resumed on October 8. Slice (c1) adds an exact two-byte instruction request to
the environment boundary. The old request always read four bytes, even when the processor
kept only the first two; it could not fetch a compressed instruction at the end of a two-byte
memory region. The new request succeeds there, keeps the same alignment and code-visibility
rules, and lets fault injection distinguish the requested parcel from its neighbor.

````

### c paragraph 9

<!-- c29d payload: c:9 -->
````text
For C-enabled execution, the processor requests one parcel first and requests another
only when the instruction needs it. This replaces the earlier coalescing plan: a four-byte
request cannot distinguish a failure in an unnecessary upper half from a failure in the
instruction itself. Fetch counts will therefore count parcels when C binds, and the next
environment-contract version will state that extent.

````

### c paragraph 13

<!-- c29d payload: c:13 -->
````text
Slice (d2) carries exact byte images through guest generation and the rv64gc runner.
The generator's byte mode emits u8 arrays and the runner loads them directly. The scalar
fixture keeps its word API for replay and reduction. A generated 14-byte mixed program runs
on the temporary C composition, checking the actual loaded bytes, a four-byte instruction at
a two-byte offset, a jump over an illegal parcel and a trailing halfword. Its five executed
steps request six parcels. Padding the image or moving the loader's offset makes the checks
fail. All 139 existing rv64gc images and observations remain unchanged in this slice.

````

### c paragraph 14

<!-- c29d payload: c:14 -->
````text
Slice (d3a) promotes the expectation author into tracked code. It computes values from
spec-side rules and offers non-writing checks. Its 42 declared historical records re-derive
byte-for-byte. The broader census caught reserved upper bits being interpreted as ordinary
operations, and missing SUM/MXR/U permissions in its data walk; both are fixed. The affected
permission guest now matches all 169 committed step observations. Direct permission fixtures
and six mutations guard the repairs, without using the instruction engine as an oracle.
The author still has a bounded vocabulary. C expansion and instruction-fetch
translation follow below. Existing records keep their original provenance.

````

### c paragraph 16

<!-- c29d payload: c:16 -->
````text
The audit inspected 95 cached corpus traces. All 79 from previously agreeing cells pass
the stricter comparison; their gaps are nine declared interrupt deliveries and one fetch
page fault, each witnessed by an event. The sixteen known not-matches keep their named
limitations. Cached process statuses were not retained. A fresh run of all four M programs
checks successful status and agrees on 99 steps, with identical repeat traces. A temporary
mixed C image also agrees on its five hand-derived addresses, words and writes.

````

### c paragraph 18

<!-- c29d payload: c:18 -->
````text
The permanent probe checks every form and its effect, immediate extremes, 79 individual
scattered bits, hints and reserved cases. A permutation of two immediate bits can pass an
all-ones limit, so those individual-bit checks matter. Six deliberate mutations fail,
including a wrong two-byte link and reporting the expanded word as the trap value. The
42 owned records and all 91 previously emitted texts stay exact. The guest author still
uses its earlier word fetch route; C component execution is ready for parcel fetch/budgets.

````

### c paragraph 21

<!-- c29d payload: c:21 -->
````text
The new fixtures exposed four older walk defects: an inconsistent Sv39 sign extension
was accepted, reserved high PTE bits were ignored, a bottom-level pointer refused instead
of page-faulting, and MPRV did not select effective data privilege. These are repaired,
including reserved non-leaf U/A/D bits and effective SUM/U permissions. Odd instruction
addresses exposed a fifth defect in the author: saved exception and interrupt PCs retained
bit zero. Both M and S delivery now clear that bit while preserving bit one. Nine deliberate
mutations fail on these guards and fetch schedules. All 97 earlier emitted texts, including
the 42 owned records, remain byte-identical; this component still leaves the older guest
execution route in place until the next slice explicitly adds byte execution and budgets.

````

### c paragraph 24

<!-- c29d payload: c:24 -->
````text
At slice (d3d2), the production profile still declared C unbound. The staged
specification-derived corpus and count derivation preceded the C bind at (e2c),
with the matched Sail experiment next. These probes
are finite component evidence. The [assembler chapter](../../annex/assembler.md) documents
the explicit authoring command and its budget semantics.

````

### c paragraph 25

<!-- c29d payload: c:25 -->
````text
The full pre-bind census exposed prerequisites in that independent author: fixed `misa`
fields, privileged legality, a bounded base vocabulary and the declared translation cache.
Slice (e1a) repairs the fields and permission guards; five mode-matrix guests now match
140 committed architectural steps and nine mutations fail. The census reaches 118 exact
of 139 historical traces, with twenty named vocabulary refusals and one owned cache-policy
disagreement. Each prerequisite is scheduled before staging can adopt parcel counts.

````

### c paragraph 26

<!-- c29d payload: c:26 -->
````text
Slice (e1b1) adds the base integer vocabulary that seventeen of those refusals named:
comparisons and XORI, XLEN and word shifts, signed/unsigned branches, and narrow memory
stock derivations. Word shifts use five count bits and sign-extend their 32-bit result;
XLEN shifts use six. A named reserved-word outcome lets parcel execution deliver the
declared diagnostic before effects, keeping the full raw word and no retirement.
Unknown valid vocabulary continues to refuse. Its permanent controls now use an
unmodeled real CSR because XORI and byte loads have become supported operations.

````

### c paragraph 27

<!-- c29d payload: c:27 -->
````text
Twenty-two hand arithmetic/alias/x0 cases, ten branch cases, narrow memory and reserved
fixtures pass. Eight mutations fail, and all seventeen formerly refused guests match
471 committed architectural steps. The census now reaches 135 exact traces, with three
remaining CSR/directive refusals and the owned cache disagreement. All 105 earlier word
texts and 42 owned records remain byte-identical. No production fixture or count has
been adopted during these prerequisite repairs.

````

### c paragraph 28

<!-- c29d payload: c:28 -->
````text
Slice (e1b2) resolves the last three vocabulary refusals. The independent author now
registers and legalizes the selected counter-enable and STCE fields. Supervisor timer
compare access needs both enable gates before effects, while machine mode bypasses
them. Source annotations can contain quotes and backslashes; every emitted literal
field uses the canonical renderer and round-trips through the reader and schema.

````

### c paragraph 29

<!-- c29d payload: c:29 -->
````text
Thirty mode-gate cases, mask/alias and literal-text fixtures pass; eight deliberate
mutations fail. Three formerly refused guests match 117 architectural steps, and all
121 prior word texts and 42 owned records remain byte-identical. The parcel census
reaches 138 exact traces with no vocabulary refusals. The remaining guest exercises
the declared translation cache, which must be modeled independently before count adoption.

````

### c paragraph 30

<!-- c29d payload: c:30 -->
````text
Reviewing that cache prerequisite exposed an older production fence defect (e1c0).
The fence used operand values to choose broad scope, confusing a nonzero register
holding zero with register x0. The semantic effect now carries register-identity
selectors separately from the address and ASID. Three parent-failing regressions pass,
including page/ASID zero and masked ASID bits; the earlier fence fixture is corrected
and armed with an occupied cache. The [Sv39 chapter](sv39.md) explains the four cases.
This repair precedes the independent cache author; no evaluator output supplies its
expected values and the staged C bind remains ahead.

````

### c paragraph 32

<!-- c29d payload: c:32 -->
````text
Hand page-table fixtures check replacement order, permissions, roots, ASIDs, globals,
zero selections and illegal/invalid fences. Thirteen deliberate mutations fail, and
the uncached parent fails the stale-mapping fixture. All 139 historical parcel runs
now reproduce their committed architectural observations, with a cold repeat of the
cache guest's request schedule. All 42 owned records remain byte-identical. The known
incorrect cache guest is the only changed text among 121 earlier word-route outputs;
no production record is overwritten. Staging can now derive C observations and actual
parcel counts independently, after resolving the documentation archive's owned pressure.

````

### c paragraph 44

<!-- c29d payload: c:44 -->
````text

Slice (e2c) binds C in production as one coherent change. The composition is complete:
197 instruction rules plus three counter pseudos, with all 200 spellings exercised.
The 28 staged C programs and their specification-derived records land byte-exact;
the directed corpus grows from 139 to 167. The old records change only their direct
fetch counts, from 4,888 word requests to 9,770 parcels across 4,913 boundaries.
Every other byte and every historical source stays exact. All 139 historical engine
PC/mode/register-write traces also remain byte-identical to the unbound parent;
five public-CLI C controls distinguish that parent from the bound model.

````

### c paragraph 45

<!-- c29d payload: c:45 -->
````text
The open v2 contract now includes C's guarantee and exact two-byte physical fetch
supply. Their four positive/negative check IDs are realized, bringing the registry
to 20 checks. Frozen v0/v1 records and pins remain unchanged. All new guests join
the seven-axis matrix; compressed faults and interrupt return replace the earlier
boundary/restart degeneracy. Two other declared degeneracies remain.

````

### c paragraph 51

<!-- c29d payload: c:51 -->
````text
The experiment also exposed an adapter defect: it recognized the historical author’s
interrupt description but not the parcel author’s numeric-cause description. Both
exact spellings now require the matching trace event. Missing/wrong events and an
instruction row at that delivery boundary fail; disabling the new spelling fails the
permanent control. GUEST-GEN passes 128 controls.

````

### c paragraph 52

<!-- c29d payload: c:52 -->
````text
These comparisons judge declared GPR changes and witnessed delivery gaps. They do
not independently compare unrecorded PCs, words, FP registers, memory, CSRs or physical
request counts. The trap CSR values read back into GPRs are within the comparison.
The ninth experiment is recorded in the reference dossier; structured experiment and
independence records remain `.14`'s work. Full CI and leaf acceptance follow at (e2e).

````

### c paragraph 53

<!-- c29d payload: c:53 -->
````text

Slice (e2e) closes the C leaf after the named full local suite passes: Rust format,
strict Clippy, all tests (153 core, 17 DSP, 193 verification), every doctrine,
the wasm bench, headless bench smoke and all books. The source expansion citations,
compiled mappings/decoder, complete scope/corpus, precise parcel-fault behavior and
public reference results meet the leaf's acceptance. The timer-platform limit remains
explicit. P4 is now 12/18; CPU-SYSTEM remains incomplete, with contract v2 completion
and realization next at `.13`. Closed planning and detailed receipts remain verbatim
in the task-tree archives; this chapter is the current review narrative.

````

## floating-point

Source `docs/book/src/plan/p4/floating-point.md`: 14661 bytes; SHA-256
`ac982cf887ed4088f1cc359f8f731662b75e0210b637ab428282d50f1bad0574`.

### floating-point paragraph 14

<!-- c29d payload: floating-point:14 -->
````text
The fourth checkpoint wrote the double-precision test programs — eleven of them, each
expected value derived from the specification by the authoring model before any engine ran.
On an engine staged outside the tracked tree, all 125 programs pass; the 114 that existed
before run byte-for-byte unchanged, and every new one fails on the previous engine.

````

### floating-point paragraph 15

<!-- c29d payload: floating-point:15 -->
````text
The fifth checkpoint is **the bind** for double precision: the profile composes D, and its
32 instructions execute in the tracked engine. The instruction census grows from 118 to 150,
matching the pinned upstream tables exactly, and all 125 test programs pass — the 114 that
existed before unchanged. Both floating-point extensions now run; what remains of this leaf is
broader numeric evidence, the structural comparison against the Sail reference, and the
leaf's own acceptance.

````

### floating-point paragraph 25

<!-- c29d payload: floating-point:25 -->
````text
The machine chapter is authenticated at271851 bytes/SHA-256
`b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea`;
the F/D pages are authenticated through their existing dossier pins too.
Instruction behavior, generated sources, canonical guests, frozen contracts and
registry bindings remain exact. G-CONTRACT stays102/114. C29c corrects the
state descriptor and F requirement detail to state the same selected policy;
the current requirement statement and frozen obligation remain identical. The
statement promises Dirty whenever values change, without excluding unchanged
writes. Numerical contract realization and structured experiment registration
remain separate work.

````

### floating-point paragraph 26

<!-- c29d payload: floating-point:26 -->
````text
The descriptor is also an inspection source. Published regeneration changes
its source hash from `6f94e9cf…85a094c` to `882483e0…695d8e3`; the generated
state module additionally carries the corrected reservation and FP census
explanations. Exactly those two read-only strings and one hash change there;
exactly two hashes change in the generated instruction definition. State layout,
CSR owners, resets, accessors and instruction definitions remain byte-identical.
Both stale-provenance checks refuse before regeneration. Fresh public FP
observations repeat the24/927 pairs and identical-write12 witness byte-for-byte.
Full source identities and exact replacement proofs are in
`docs/tasks/P4-SYSTEM.md` (c29c).
````

## contract-v2

Source `docs/book/src/plan/p4/contract-v2.md`: 31527 bytes; SHA-256
`9e6a05cadeafab77988f2440240681d0c6454ad44cd04116ea5c4c83cbe9a514`.

### contract-v2 paragraph 11

<!-- c29d payload: contract-v2:11 -->
````text
The initial inventory correction changes the declared inventory and its generated metadata.
The definition module also records the updated state-source hash in its
provenance manifest. Storage, reset values, accessors and execution remain
byte-identical. Snapshot
and replay serialization still belong to P4.16; this inventory does not claim
that those features are implemented.

````

### contract-v2 paragraph 19

<!-- c29d payload: contract-v2:19 -->
````text
This adds two real checks without running an unrelated program as evidence of
selection. All twenty earlier guest bindings stay unchanged. The effective
contract reached 22 of 106 checks at that slice. The following structured
scope checks raise it to 34; version 2 remains open.

````

### contract-v2 paragraph 24

<!-- c29d payload: contract-v2:24 -->
````text
At b3, seven scope pairs plus the twenty existing guest checks realized 34 of
106 checks. These are selection and consistency checks. CSR field behavior and
instruction semantics retain their execution evidence; firmware is still future
work. Older notes and changelog entries were archived verbatim with exact
reconstruction, so their history remains available within the fixed size limits.

````

### contract-v2 paragraph 31

<!-- c29d payload: contract-v2:31 -->
````text
Four further pairs bring the effective contract to 42 of 106 realized checks.
They check selections, with a positive predicate and specific violating copies:

````

### contract-v2 paragraph 40

<!-- c29d payload: contract-v2:40 -->
````text
Those six checks brought the effective census to 48 of 104 checks at c1. The
address-unit pair below brings it to 50 of 106. Version 2 stays open.

````

### contract-v2 paragraph 44

<!-- c29d payload: contract-v2:44 -->
````text
Paths start at the repository root, so moving the checkout keeps them valid.
The v0 and v1 parts contain their original contiguous record bytes. At c2, expansion
reproduced all 63,014 pre-split bytes exactly, including order and blank lines;
all 58 record mappings and frozen pins were unchanged. At that split the root was
9,003 bytes, the v0 part 47,168 and the v1 part 7,009. No size ceiling was raised and no duplicate
materialized catalog is maintained.

````

### contract-v2 paragraph 55

<!-- c29d payload: contract-v2:55 -->
````text
The registry now has explicit `Evidence::Boundary` entries. Its normal tests run
both fixtures and retain the rule that every post-v0 declaration is born realized.
Frozen records and all earlier registry entries are unchanged. Four boundary
assumptions and the remaining execution pairs still need work; these finite
fixtures do not prove correctness for every possible address or environment.

````

### contract-v2 paragraph 62

<!-- c29d payload: contract-v2:62 -->
````text
Four permanent core tests exercise all 25 request/response-kind combinations,
narrow-width edges, full-width values, unchanged target failures and existing
violations, and actual GC/scalar/translation paths. Normal guest observations
still pass. At c4a this repair added no contract-check credit: the census stayed
50 of 106 realized, with four boundary assumptions still to declare and realize.

````

### contract-v2 paragraph 89

<!-- c29d payload: contract-v2:89 -->
````text
All earlier registry entries and frozen records remain exact. The effective
census reached 56 obligations, 112 declared checks and 56 realized checks at c6.
Full cold reset follows below; remaining instruction checks keep version 2 open.

````

### contract-v2 paragraph 96

<!-- c29d payload: contract-v2:96 -->
````text
Only cold reset is supported. Snapshot restoration and warm/retained-state
ordering need their own implementation and contract. The pair brings the
c7b census to 57 effective obligations, 114 declared checks and 58 realized
checks: thirteen scope pairs, eleven guest pairs and five direct boundary pairs.
At c7b, 28 runtime pairs remained before version 2 could freeze.

````

### contract-v2 paragraph 98

<!-- c29d payload: contract-v2:98 -->
````text
The [runtime contract chapter](contract-runtime.md)
contains privilege-mode, Sv39, Svade, IALIGN-16, Zicntr, Sstc and direct implicit
walk/fetch/data request evidence.
The [integer runtime chapter](contract-integer.md) retains immediate/register ALU,
U-immediate, twelve-form shift, nine-form RV64I word-result and direct 64-bit
register/user-address bindings, worked
values, SRAW/SRAIW count-mask/source-width repairs and SHAMT requirement correction.
The [control transfer chapter](contract-control.md) retains immediate transfers,
JALR's inherited-annotation diagnosis and direct target/link/request witnesses.
The [memory runtime chapter](contract-memory.md) retains eleven-form load/store
extension, discarded-load requests/faults, selected byte-order observations and
FENCE field/no-effect and atomic pre-translation alignment observations.
These chapters preserve independent controls and finite evidence limits. Current G-CONTRACT is
102/114; six runtime pairs and final freeze remain. The
[instruction-visibility chapter](fence-i.md#direct-contract-observations) adds
ignored-field and patched-parcel FENCE.I witnesses. The [atomics chapter](atomics.md#direct-contract-observations) adds literal A-operation, alias, reservation-effect and translated-fault witnesses. The split retains
all runtime sections byte-verbatim under the book's fixed per-chapter ceiling.

````

## contract-runtime

Source `docs/book/src/plan/p4/contract-runtime.md`: 27898 bytes; SHA-256
`aa64d6c882d6b8b17c0fd12c65cccb89014e910583b5ef49ed6139ad177aa582`.

### contract-runtime paragraph 7

<!-- c29d payload: contract-runtime:7 -->
````text
At c8 the census was 60/114 realized: thirteen scope pairs, twelve guest
pairs and five typed boundary pairs. At that slice, twenty-seven runtime pairs
and final freeze remained. All previous bindings and frozen declarations are unchanged.

````

### contract-runtime paragraph 10

<!-- c29d payload: contract-runtime:10 -->
````text
The independent expectation author already inherited G correctly and remains
unchanged. This fixes the declared retention policy rather than broadening the
ISA claim. At c9a G-CONTRACT remained 60/114 until the runtime pairs themselves bind.

````

### contract-runtime paragraph 14

<!-- c29d payload: contract-runtime:14 -->
````text
The matrix spans 1,417 execution boundaries and 2,832 physical parcel
requests. Re-executing the independent parcel author reproduces every
committed register-change sequence and fetch count exactly. Neither the
programs nor their expectations changed. This is finite translation evidence,
not universal Sv39 or Linux acceptance. At c9b the registry realized
62/114 checks; twenty-six runtime pairs and final freeze remained.

````

### contract-runtime paragraph 19

<!-- c29d payload: contract-runtime:19 -->
````text
These witnesses retain the existing ISA observation vocabulary and finite scope.
The selected policy faults instead of updating A/D; Svadu is excluded. At c10,
G-CONTRACT was 64/114, with twenty-five runtime pairs and final freeze remaining.

````

### contract-runtime paragraph 27

<!-- c29d payload: contract-runtime:27 -->
````text
At c11, G-CONTRACT was 66/114: thirteen scope pairs, fifteen guest pairs and five
typed boundary pairs. Twenty-four runtime pairs and final freeze remained.

````

### contract-runtime paragraph 33

<!-- c29d payload: contract-runtime:33 -->
````text
At c12, G-CONTRACT reached 68/114: thirteen scope pairs, sixteen guest pairs
and five typed boundary pairs. Twenty-three runtime pairs and final freeze remain.

````

### contract-runtime paragraph 41

<!-- c29d payload: contract-runtime:41 -->
````text
Fresh pinned Sail attempts agree on w-sw (19 boundaries, two identical traces).
Six inputs diverge: c-irq at 11, env-irq-sources at 12, i-prio at 26,
i-timer at 5, mm-wfi at 11 and w-deleg at 14. The trace witnesses absent
comparator pending or continued execution instead of declared delivery/wait.
w-notrap and w-timer processes refuse (rc1): their time/instret reads trap with
Zicntr disabled and enter trap loops. Old inputs reproduce those refusals.
The public timer diagnostic now enables STCE and reads back bit 63 on both
sides before comparing pending state (ten boundaries, repeat traces identical).
Its old seven-boundary STCE-clear result was confounded by the overlay defect
and cannot alone establish a reference cause. Public configuration validation
still rejects Zicntr without a time source and
CLINT without a mapped region. These are qualified reference-platform limits;
failed processes are never counted as agreement. Structured experiments remain
P4-SYSTEM.14's work. The full independent corpus now spans 5,360 boundaries and
10,514 parcel requests over the same 167 programs; the contract stays 68/114.

````

### contract-runtime paragraph 53

<!-- c29d payload: contract-runtime:53 -->
````text
At c13a2, G-CONTRACT stayed 68/114 with v2 open. Direct S-mode witnesses below
then earn the SSTC pair; neither slice establishes firmware/Linux capability.

````

### contract-runtime paragraph 61

<!-- c29d payload: contract-runtime:61 -->
````text
At c13b, G-CONTRACT reached **70/114**: thirteen scope pairs, fifteen guest pairs,
six direct assumption pairs and one direct execution pair. The registry keeps
72 entries, including the two superseded historical source checks. Twenty-two
runtime pairs and final freeze then remained; v2 and CPU-SYSTEM stayed open.

````

### contract-runtime paragraph 62

<!-- c29d payload: contract-runtime:62 -->
````text
Before ALU-immediate binding, c14a repairs a gate self-test that assumed its
example check was still unregistered. That assumption failed under a simulated
valid binding even though production coverage stayed correct. The test now adds
a synthetic declaration only in scratch data and measures its own registration.
Duplicate registration cannot add credit; the controls also fill every effective
check and then add a new declaration, distinguishing full coverage from a newly
missing check. All twenty controls pass, including the previously failing ALU
binding. A duplicate-counting mutant fails. Production measure and reports stay
exact; this repair grants no CPU credit.

````
