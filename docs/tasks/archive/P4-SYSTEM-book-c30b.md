# P4-SYSTEM.13 c30b — historical book verification receipts

Finite immutable capture from source commit
`0e9949bc4151f9f6f9033e4123e3309d1d55744f`, SEMULITH-P4-0174.
Dated verification, pre-bind identity and provenance chronology remain exact
here. Current feature explanations, commands, tables, worked values, controls,
links and finite limits remain in the book. No later payload is appended.

For each chapter, remove only the exact footer below, undo replacements in
descending new_offset order using the marked original payloads, then check
source_bytes/source_sha256 against the named source commit. This inverse
binds the complete source, not just the removed text. Each payload includes
its original paragraph separator. Every numeric offset/length is a byte count.

## Inverse map

```json
[
  {
    "path": "docs/book/src/plan/p4/contract-runtime.md",
    "name": "contract-runtime",
    "source_bytes": 31904,
    "source_sha256": "ad6344d260f45fcbdec8ede9d8feeb7ed6166efe6ccad1056e9d27608780e25f",
    "proposed_bytes": 31190,
    "proposed_sha256": "85cff2e69551dd3fc21770a09172796cd0248bae189ba97b618ae3cf2afee3c6",
    "footer": "\nFurther exact chronology and pre-bind identity receipts are preserved in\n`docs/tasks/archive/P4-SYSTEM-book-c30b.md`, section `contract-runtime`.\nCurrent feature explanations, examples, controls and limits remain here.\n",
    "spans": [
      {
        "paragraph": 52,
        "old_offset": 14775,
        "new": "For w-timer, WFI retires at boundary 12, boundaries 13–14 remain halted, and\nboundary 15 delivers STI without fetching or retiring. The handler reads\ninstret=13 at boundary 16 and time=17 at boundary 17. It then observes cause\n0x8000000000000005 and mepc=0x80000034, the WFI continuation.\n\n",
        "old_sha256": "8144d711596b0d4cfa1006a9ae1653ebacb6ea0c51ccd8e54d72c21c20513244",
        "new_offset": 14775
      },
      {
        "paragraph": 53,
        "old_offset": 15236,
        "new": "Author budgets are fixed in the author, never read from expected output.\n`--check-owned` rejects count, observation, comment and line-ending drift in\nhistorical and fresh records. Wrong-budget and word-route controls fail.\nmm-stimecmp retains its deliberately closed gates.\n\n",
        "old_sha256": "1c2e4a05fe2cf4574785a6400fb53d3f66610a06e84f17c805c40018f45547ab",
        "new_offset": 15067
      },
      {
        "paragraph": 54,
        "old_offset": 15694,
        "new": "Pinned public Sail observations agree on w-sw but differ at declared\ninterrupt/comparator/wait behavior for c-irq, env-irq-sources, i-prio, i-timer,\nmm-wfi and w-deleg. w-notrap and w-timer refuse after Zicntr-disabled reads.\nThe corrected public timer diagnostic verifies STCE read-back before comparing\npending state; its earlier STCE-clear result was confounded by the overlay\ndefect. Configuration validation refuses Zicntr without a time source and CLINT\nwithout a mapped region. Failed processes receive no agreement credit. Exact\nattempt receipts remain below; structured experiments belong to P4-SYSTEM.14.\n\n",
        "old_sha256": "67672bd80fa1bf09a83bac0e5666a0ca3f8fa1f356a834501e1208bdecaf43db",
        "new_offset": 15342
      },
      {
        "paragraph": 63,
        "old_offset": 19416,
        "new": "Open v2 supersedes OB-GC-ENV-INTERRUPT-SOURCES with\nOB-GC-ENV-INTERRUPT-SOURCES-V2. The event record refers to that source rule;\nthe cold-reset record now states pending zero. The frozen v1 statement remains\nhistorical exact text. The registry retains its old checks as historical test\nbindings and adds the replacement's direct POS/NEG pair. Twelve v2 members remain open.\nCoverage counts only registered checks whose records remain effective. The\nreport's independent recount and synthetic realized-record supersession control\nverify this distinction; removing that filter fails both controls.\n\n",
        "old_sha256": "d79fab9699757074d812c3def3047ccf84d36ffe00b51fae86fd89355fef8a59",
        "new_offset": 18688
      },
      {
        "paragraph": 65,
        "old_offset": 20856,
        "new": "Four new core regressions first failed on the old processor; after repair they\npass, including 48 actual instruction cases over all six CSR forms, two raw\nsoftware states, both compare conditions and both STCE settings. Five-bit CSR\nimmediates cannot set bit 5; their other pending writes still obey the selected\nmask. The independent author tests eight literal source/write combinations and\nretention; four deliberate source/write/retention mutations each fail. The original public CSR\nreproduction changes from rc101 to rc0; the corrected public Sail diagnostic\nstill reports its qualified comparator-platform difference with STCE verified.\n\n",
        "old_sha256": "ac0fbe51d3acd9ad71790cd3a3aeebf6121da3b7eeecb10c4d57a907f69655a8",
        "new_offset": 19984
      }
    ]
  },
  {
    "path": "docs/book/src/plan/p4/contract-v2.md",
    "name": "contract-v2",
    "source_bytes": 30716,
    "source_sha256": "603f9cf43f4c72caea8617a5a843f414287a7a9df83c11d07e01b9df8cb9d3a4",
    "proposed_bytes": 30062,
    "proposed_sha256": "5fc7eb833d84d7706f4f0b70207704d643dc384546cc1762ba92d01490b816c7",
    "footer": "\nFurther exact chronology and pre-bind identity receipts are preserved in\n`docs/tasks/archive/P4-SYSTEM-book-c30b.md`, section `contract-v2`.\nCurrent feature explanations, examples, controls and limits remain here.\n",
    "spans": [
      {
        "paragraph": 3,
        "old_offset": 534,
        "new": "The effective contract contains 57 obligations and 114 checks. The\n[runtime witness summary](#runtime-guarantee-witnesses) gives the current realized\ncount, derived from the canonical catalog and executable registry by the GS report.\nInstruction guarantees require executable observations. Scope choices require\npredicates over canonical declarations and violating negative fixtures; an\nunrelated passing program cannot establish a scope declaration.\n\n",
        "old_sha256": "792164b5ca40fdb8bd498129f18bee4f811c5326df45c309c963d4cbb752b149",
        "new_offset": 534
      },
      {
        "paragraph": 15,
        "old_offset": 4666,
        "new": "Revoking delegation hides a bit without erasing its owner. Re-delegating makes\nthe current owner value visible immediately. The independent expectation author\nnow applies the same specified rule and reads `sip` through its sole `mip`\nowner. Eight masks in both modes and all six CSR instruction forms exercise\nthe repair; five author mutations distinguish the missing masks and owner.\n\n",
        "old_sha256": "cfe48939fa056ad87df62e599965095659eca599e999a0167cb12f57113b3a52",
        "new_offset": 4311
      },
      {
        "paragraph": 41,
        "old_offset": 11773,
        "new": "The catalog separates its current v2 records from frozen v0/v1 parts,\nincluded in version order:\n\n",
        "old_sha256": "952f912276a633b0e5f5c57320d7d4ddd54cead698046de5dfed71190855b61e",
        "new_offset": 11274
      },
      {
        "paragraph": 43,
        "old_offset": 12137,
        "new": "Paths start at the repository root. Frozen parts retain their original\ncontiguous record bytes; expansion reproduces catalog order and frozen pins\nwithout a duplicate materialized catalog or a larger cap. The split's exact\nsource identity and reconstruction receipt remain below.\n\n",
        "old_sha256": "e1a3fa8201562fe46c36d969b2c264ca345c487800c378d60934baff7dde1d32",
        "new_offset": 11551
      },
      {
        "paragraph": 79,
        "old_offset": 21968,
        "new": "The negative pair attempts delivery while answering each of Fetch, FetchParcel,\nLoad, Store and WalkAccess. Every real-engine path returns the exact typed\nlocation violation, preserving PC, mode, destination, trap state, counters and\nmemory. Fetch uses the public legacy table seam over the same GC evaluator.\nDisabling the location guard lets every bad schedule escape and makes each\nnegative fixture fail.\n\n",
        "old_sha256": "fd35109e7eb051fd9ed2c1f54570af42b05df8bdcb8d05188e40bbcb5fd92e14",
        "new_offset": 21352
      },
      {
        "paragraph": 82,
        "old_offset": 22999,
        "new": "The pinned RVWMO chapter defines global order, preserved program order and the\nload-value, atomicity and progress constraints. Selecting the one-hart program\norder and latest preceding stores meets those constraints here. The pinned\nFENCE.I chapter separately orders preceding stores before later instruction\nfetches. The laboratory's coherent reads provide immediate visibility even\nwithout that synchronization, a stronger choice than the architectural minimum.\n\n",
        "old_sha256": "fcc20e7b3fa565e8eb3272a5be871c5b4d40b9e67eb33ea2e49abde1458e444b",
        "new_offset": 22265
      },
      {
        "paragraph": 98,
        "old_offset": 29554,
        "new": "P4.13 c13a2 supersedes the frozen v1 interrupt-source assumption with a twelfth\nopen-v2 member: STCE=0 software STIP versus STCE=1 comparator pending, with\nexplicit raw-software retention. Cold pending is zero; v2 event/reset records\nfollow that rule;\n[the runtime chapter](contract-runtime.md#stce-dependent-pending-and-the-v2-source-contract)\ngives the selection table, worked transitions, instruction witnesses and limits.\nFrozen v0/v1 records and pins stay exact. Sstc now binds a direct Execution pair:\n31 boundaries / 62 parcels, S programming/read-back and handler-visible refusals,\nplus original timer guests. [Worked values and controls](contract-runtime.md#observable-s-mode-timer-programming-and-refusals)\nclose the terminal-zero witness hole; v2 remains open.\n\n",
        "old_sha256": "d7d2c740ac607806627771d291651756c6fff8988460eaad8c62ae541efa71b7",
        "new_offset": 28748
      }
    ]
  },
  {
    "path": "docs/book/src/plan/p4/contract-integer.md",
    "name": "contract-integer",
    "source_bytes": 25637,
    "source_sha256": "31f8a5d0ccdd24611e1c474e0c00f68b8ff843b5eb4ee6ea7aff8810457cccbd",
    "proposed_bytes": 22322,
    "proposed_sha256": "dd567bcf0d095cea28fda57a1adb6a0f30209980db5cbec839ca2dbae19ad400",
    "footer": "\n## Historical verification receipts\n\nFurther exact chronology and pre-bind identity receipts are preserved in\n`docs/tasks/archive/P4-SYSTEM-book-c30b.md`, section `contract-integer`.\nCurrent feature explanations, examples, controls and limits remain here.\n",
    "spans": [
      {
        "paragraph": 6,
        "old_offset": 1823,
        "new": "Five in-memory author copies are deliberately wrong. Zero-extended SLTIU fails\nscope-alu, step 17; unsigned SLTI fails at step 14; zero-extended ANDI fails at step 8; zero-extended XORI\nfails at step 10; saturating ADDI fails bound-arith, step 8. The existing integer-author sign\ncontrol also refuses.\n\n",
        "old_sha256": "04aa1f436b9d18e309bef461f2f9cda9a1e3362e125d381ad426f31fec43d0a6",
        "new_offset": 1823
      },
      {
        "paragraph": 12,
        "old_offset": 3986,
        "new": "Eight deliberately incorrect author copies fail exact steps: saturation at\nbound-arith steps 5/6; swapped comparison signedness at scope-alu steps 11/13; wrong AND/OR/XOR\noperators at scope-alu steps 5/6/7; cleared aliased ADD sources at bound-alias step 24. The\nexisting integer-author controls and full normal corpus comparison retain their\nauthority. NEG rejects these semantic alternatives, not a required trap for\nvalid register arithmetic.\n\n",
        "old_sha256": "86e3e229abfdc36bebfc23785aaf6ed625ed91500e0cd57ea0d8e4a02b248f27",
        "new_offset": 3778
      },
      {
        "paragraph": 18,
        "old_offset": 5947,
        "new": "Seven in-memory wrong author copies fail intended observations: LUI zero\nextension or missing shift at scope step 3; AUIPC zero extension, missing shift\nor unsigned saturation at bound step 29; next-PC or sign-extended base-PC at\nchase step 0. The whole programs and their intermediate observations matter.\nNEG rejects wrong legal arithmetic, not a required architectural exception.\n\n",
        "old_sha256": "bf82e5427754006943a639e1ef1b9a2dd9088ddb469a956f3b9d0e5d6a0bcdb4",
        "new_offset": 5620
      },
      {
        "paragraph": 27,
        "old_offset": 8861,
        "new": "At c17b, both bound-shiftw programs append SRAW x16,x8,x10 at address\n0x800000dc, after all 55 original instructions. Its literal word is 0x40a4583b.\nThe existing x8=0xffffffff80000001 and x10=96 make rs2[4:0]=0: low32 remains\n0x80000001, sign-extended to x16=0xffffffff80000001. That expected value was\nrecorded before either engine ran.\n\n",
        "old_sha256": "a07e586842fe5541abfef2220cb0bf63073cc4bd7868b9bde88bb82a9c5106d5",
        "new_offset": 7786
      },
      {
        "paragraph": 28,
        "old_offset": 9403,
        "new": "The previously surviving six-bit SRAW author fails only at new boundary 55.\nThe same public processor bad-table diagnostic also fails exactly there: its\nall-ones result disagrees with the committed identity. The correct core corpus\npasses. A durable hand-encoded author case uses garbage upper bits\n0x1234567880000001 and count 96, requiring the same sign-extended low word.\nIts isolated sraw-count mutation fails with the named five-bit-count reason\nbefore a new GUEST-GEN control is registered.\n\n",
        "old_sha256": "43a185937561385406fb04645a494a6fb0bcbda91dafd44d29b9ad679c5608ac",
        "new_offset": 8126
      },
      {
        "paragraph": 30,
        "old_offset": 10477,
        "new": "The count-mask diagnostic also matched 56 declared Sail boundary rows with\ntwo identical fresh traces. This is finite integer evidence, subject to the\nreference/platform and FP-independence limits. Its provenance propagation and\ndated corpus/contract counts are retained in the receipts below.\n\n",
        "old_sha256": "aed4d853319dd32c517ea6fc3de82beae087effa5da2b97d3e9ca4c32a0c433f",
        "new_offset": 9016
      },
      {
        "paragraph": 38,
        "old_offset": 12955,
        "new": "The arithmetic low word is -2147483647. Shifting it right by one rounds down to\n-1073741824, whose word is 0xc0000000; sign extension supplies the required\n64-bit value. The wrong full-width read instead sees positive 2147483649 and\nyields 0x40000000. Each isolated bad author now disagrees only at its new boundary\n(58 for SRAW, 59 for SRAIW); public engine bad tables first fail at those same\nboundaries.\n\n",
        "old_sha256": "b3504acba7f52fbebcc7cb0a21570b69c9d89597dbdf9006be170cebbe778d2b",
        "new_offset": 11082
      },
      {
        "paragraph": 39,
        "old_offset": 13436,
        "new": "The durable probe's existing garbage-upper-word hand cases also distinguish both\nrules. New sraw-width and sraiw-width controls were observed RED with their named\narithmetic-word reasons before registration.\n\n",
        "old_sha256": "b774cb5703733759b060e787a7af63e840f8632192da033baed317b50a8be39f",
        "new_offset": 11490
      },
      {
        "paragraph": 40,
        "old_offset": 13816,
        "new": "The completed source-width program has 60 boundaries: 60 base word requests\nor120 GC parcels. Pinned Sail matches its declared rows/change observations\nand repeats identically; the base live smoke compares both Sail and Spike.\nThese finite observations close the source-width evidence gaps without\nchanging production rules; the standing reference/platform limits apply.\n\n",
        "old_sha256": "5db1ff615c00c933d4daf259f9563c35b01e8ac1ff517dc7b7b50b05df712ab7",
        "new_offset": 11699
      },
      {
        "paragraph": 46,
        "old_offset": 16330,
        "new": "The selected observations and complete independent corpus agree. This is\nfinite evidence for these inputs; standing independence/platform limits apply.\nDated registry/corpus and pre-bind identity receipts remain below.\n\n",
        "old_sha256": "3fa5a1a23b6358448c397e89e1f240e1b59aece8887d7e22471b24df0b3c8371",
        "new_offset": 13896
      },
      {
        "paragraph": 47,
        "old_offset": 16864,
        "new": "The scoped review also found incomplete requirement metadata: REQ-D-SHAMT's\nstatement names all twelve forms, while its base and GC insns fields omit\nSLLW/SRLW/SRAW. The original base association commit added nine, and GC copied\nthat list. The aggregate extraction gate still sees the three forms through\nWSUFFIX; it does not establish each requirement's association completeness.\nThe frozen statement and the twelve-form execution evidence above are correct.\nThe association repair below closes that metadata defect; implementation-status\nand experiment work remains P4-SYSTEM.14.\n\n",
        "old_sha256": "37d5f10fd435dfee65be54afa5e529bb08e92203396f0fa9457fd20711e710d8",
        "new_offset": 14116
      },
      {
        "paragraph": 49,
        "old_offset": 18030,
        "new": "Requirement associations propagate through the base dossier pin into board\nmetadata, platform provenance and generated model/report outputs. This changes\nmetadata, not instruction behavior or observations; its exact propagation\nreceipt is preserved below.\n\n",
        "old_sha256": "fb989cdec382393ca71cc6155e7b38890c25d188a494f312672407f94cbb59ae",
        "new_offset": 15251
      },
      {
        "paragraph": 57,
        "old_offset": 21432,
        "new": "Normal author/core observations agree. Negative fixtures are legal semantic\ncounterexamples, with no invented target traps. Standing finite-evidence,\nreference and platform limits remain; dated progress receipts are below.\n\n",
        "old_sha256": "b9d52532d121333581e9bc3ce137550fd80e21c681095a90974e426821ae714b",
        "new_offset": 18455
      },
      {
        "paragraph": 66,
        "old_offset": 24824,
        "new": "The independent author confirms the literal words, canonical mappings, GPR/PC/U/\ncounter/memory values and fetch/walk logs. It does not log data boundary requests;\nthe public CPU observer separately checks those. The declaration test first\nrefused the missing binding. Unchanged companion guests are POS scope-alu\n(31/62) and NEG bound-arith/sv39-fault-canonical (89/178). Including the direct\ncases, the pair runs **128 boundaries / 256 parcels**. This is finite width evidence under the selected\ntranslation and provider rules.\n\n\n",
        "old_sha256": "5aa69229eaaea5772c3062b5d36c4ba65582b379418a7dbbb8bc604826eac69c",
        "new_offset": 21533
      }
    ]
  },
  {
    "path": "docs/book/src/plan/p4/contract-control.md",
    "name": "contract-control",
    "source_bytes": 10013,
    "source_sha256": "9fe64b62f74cbe165461b721ab77e30564c38ec86831cdcd938b3200f520d8ac",
    "proposed_bytes": 9080,
    "proposed_sha256": "914d3062e961eeefdbeebcd3ce6dd4deea3d58919272d14569424836fd7c2bd1",
    "footer": "\n## Historical verification receipts\n\nFurther exact chronology and pre-bind identity receipts are preserved in\n`docs/tasks/archive/P4-SYSTEM-book-c30b.md`, section `contract-control`.\nCurrent feature explanations, examples, controls and limits remain here.\n",
    "spans": [
      {
        "paragraph": 7,
        "old_offset": 2002,
        "new": "All thirteen variants fail; the unmodified driver matches all five programs,\nincluding never-written registers and parcel counts. These observations\nconstrain architectural effects, not processor pipelines or untested target\nfaults. Exact pre-bind identity and dated verification receipts remain below.\n\n",
        "old_sha256": "0fc08283f50853f156f0659e989dd12135868e52c34639536641322ead3a3d39",
        "new_offset": 2002
      },
      {
        "paragraph": 14,
        "old_offset": 5464,
        "new": "This was an observation gap: the direct witness below adds literal post-step\ntarget/link/request checks for low-bit carry, negative immediates, wrapping and\nsource/link aliasing. Wrong public tables must fail before registration. The\nannotation repair's exact identity and full-CI receipt is preserved below.\n\n",
        "old_sha256": "fbcb2c8ca6a34fa3d94aa306c5af000421c65b70788e9d8d14e9e0739a6a0003",
        "new_offset": 4963
      },
      {
        "paragraph": 21,
        "old_offset": 9322,
        "new": "The declaration test first refused the missing binding. POS also runs unchanged\nguest-control/dir-chase (30 boundaries/60 parcels); NEG runs fault-jalr-mis/\nit-prio-jump (6/11). Together with the direct cases the pair runs **53/103**.\nThe independent author reproduces every literal case and the full unchanged\n167/5365/10524 corpus. These finite witnesses establish no universal ISA claim.\n\n",
        "old_sha256": "48c293edb38c22172f5766b765c07645100c871bd66633c0ceff6221aa9932d4",
        "new_offset": 8431
      }
    ]
  },
  {
    "path": "docs/book/src/plan/p4/contract-memory.md",
    "name": "contract-memory",
    "source_bytes": 24596,
    "source_sha256": "70ad010db28165d210b5bf8e56580d2e36ca0ec4e0e0197e6b77cc3ffd50f0d5",
    "proposed_bytes": 23696,
    "proposed_sha256": "623448374c278b51ff0a2d446d30ab9ad7f340952ad4c8c8cd35ca4d3d853805",
    "footer": "\n## Historical verification receipts\n\nFurther exact chronology and pre-bind identity receipts are preserved in\n`docs/tasks/archive/P4-SYSTEM-book-c30b.md`, section `contract-memory`.\nCurrent feature explanations, examples, controls and limits remain here.\n",
    "spans": [
      {
        "paragraph": 10,
        "old_offset": 3062,
        "new": "These finite legal counterexamples require no target traps and establish no\nuntested memory-system behavior. Address faults, x0 side effects and selected\nbyte order retain separate obligations. Pre-bind failure, exact prior-input\nidentity and dated progress receipts remain below.\n\n",
        "old_sha256": "b8827220975b5e614b327e2c2b4145685a2d07f86ca576003e198e66c9533ef7",
        "new_offset": 3062
      },
      {
        "paragraph": 19,
        "old_offset": 7377,
        "new": "Request logs establish that discarded-result accesses occur; they add no\ndevice or unimplemented MMIO behavior. Byte-order selection and other\nobligations retain their own witnesses. Exact prior-input and dated verification\nreceipts remain below.\n\n",
        "old_sha256": "915f4cbe594a9c4db322fa94692c176c78f727cabfdcbecd33fe8183bb60995c",
        "new_offset": 6916
      },
      {
        "paragraph": 26,
        "old_offset": 10232,
        "new": "These observations establish the selected ordinary-memory byte order. They\nadd no selectable big-endian execution or device model. Missing-binding,\nprior-input identity and dated verification receipts remain below.\n\n",
        "old_sha256": "55700587c2f540a6f5b5d5195c0c15284deae63840e1ed52d2455b785842b6b5",
        "new_offset": 9411
      }
    ]
  }
]
```

## contract-runtime

<!-- c30b payload: contract-runtime:52 -->
````text
For w-timer, WFI retires at boundary 12, boundaries 13–14 remain halted, and
boundary 15 delivers STI without fetching or retiring. The handler reads
instret=13 at boundary 16 and time=17 at boundary 17. It then observes cause
0x8000000000000005 and mepc=0x80000034, the WFI continuation. The earlier
source comment's 0x80000044 was incorrect: its old assembled continuation and
observation were 0x8000002c. The added setup moves that continuation by eight.

````

<!-- c30b payload: contract-runtime:53 -->
````text
Fresh records name the actual parcel route without inheriting capture chronology.
`--check-owned` now checks 41 unchanged historical captures and the fresh
13-boundary env-irq-sources record. Its budget is fixed in the author, never
read from the expected output. Wrong-budget and word-route controls fail; both
historical and fresh records reject count, observation, comment and line-ending
drift. mm-stimecmp's deliberately closed gates remain unchanged.

````

<!-- c30b payload: contract-runtime:54 -->
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
P4-SYSTEM.14's work.

````

<!-- c30b payload: contract-runtime:63 -->
````text
Open v2 supersedes OB-GC-ENV-INTERRUPT-SOURCES with
OB-GC-ENV-INTERRUPT-SOURCES-V2. The event record refers to that source rule;
the cold-reset record now states pending zero. The frozen v1 statement remains
historical exact text. The registry retains its old checks as historical test
bindings and adds the replacement's direct POS/NEG pair. The effective census
stays 57 obligations / 114 checks, 68 realized: thirteen scope pairs, fifteen
guest pairs and six direct assumption pairs. Twelve v2 members remain open.
Coverage counts only registered checks whose records remain effective. The
report's independent recount and synthetic realized-record supersession control
verify this distinction; removing that filter fails both controls.

````

<!-- c30b payload: contract-runtime:65 -->
````text
Four new core regressions first failed on the old processor; after repair they
pass, including 48 actual instruction cases over all six CSR forms, two raw
software states, both compare conditions and both STCE settings. Five-bit CSR
immediates cannot set bit 5; their other pending writes still obey the selected
mask. The independent author tests eight literal source/write combinations and
retention; four deliberate source/write/retention mutations each fail. All 167
guest observations and 42 owned records remain exact. The original public CSR
reproduction changes from rc101 to rc0; the corrected public Sail diagnostic
still reports its qualified comparator-platform difference with STCE verified.

````

## contract-v2

<!-- c30b payload: contract-v2:3 -->
````text
The original census found 53 effective obligations and 106 checks. Early
declaration slices replaced four old records with three current guarantees and
added five boundary assumptions, bringing the effective census to 57 obligations
and 114 checks. The later interrupt-source replacement preserves that size. The
[runtime witness summary](#runtime-guarantee-witnesses) gives the current realized
count, derived from the canonical catalog and executable registry by the GS report.
A check receives credit only when its actual
fixture runs: instruction guarantees use executable observations; a scope choice
such as the selected firmware ABI uses a predicate over the canonical documents
and a negative fixture that violates that predicate. Running an unrelated program
cannot establish a scope declaration.

````

<!-- c30b payload: contract-v2:15 -->
````text
Revoking delegation hides a bit without erasing its owner. Re-delegating makes
the current owner value visible immediately. The independent expectation author
now applies the same specified rule and reads `sip` through its sole `mip`
owner. Eight masks in both modes and all six CSR instruction forms exercise
the repair; five author mutations distinguish the missing masks and owner.
The existing guest records remain byte-identical. This prerequisite kept contract
credits at 56/112; the full-cold-reset pair below follows it.

````

<!-- c30b payload: contract-v2:41 -->
````text
The catalog reached 63,014 bytes against its fixed 65,536-byte authored-part cap.
It now retains the six current v2 records and explicitly includes two frozen
parts, in version order:

````

<!-- c30b payload: contract-v2:43 -->
````text
Paths start at the repository root, so moving the checkout keeps them valid.
The frozen parts contain their original contiguous record bytes. Expansion at
the split reproduced the original 63,014 bytes, order, 58 mappings and frozen
pins exactly. No ceiling was raised or duplicate materialized catalog added.

````

<!-- c30b payload: contract-v2:79 -->
````text
The negative pair attempts delivery while answering each of Fetch, FetchParcel,
Load, Store and WalkAccess. Every real-engine path returns the exact typed
location violation, preserving PC, mode, destination, trap state, counters and
memory. Fetch uses the public legacy table seam over the same GC evaluator.
Disabling the location guard lets every bad schedule escape and makes each
negative fixture fail. At c5 these finite checks brought the effective census to
55 obligations, 110 declared checks and 54 realized checks.

````

<!-- c30b payload: contract-v2:82 -->
````text
The pinned RVWMO chapter defines global order, preserved program order and the
load-value, atomicity and progress constraints. Selecting the one-hart program
order and latest preceding stores meets those constraints here. The pinned
FENCE.I chapter separately orders preceding stores before later instruction
fetches. The laboratory's coherent reads provide immediate visibility even
without that synchronization, a stronger choice than the architectural minimum.
Both source artifacts were digest-verified when this pair was authored.

````

<!-- c30b payload: contract-v2:98 -->
````text
P4.13 c13a2 supersedes the frozen v1 interrupt-source assumption with a twelfth
open-v2 member: STCE=0 software STIP versus STCE=1 comparator pending, with
explicit raw-software retention. Cold pending is zero; v2 event/reset records
follow that rule. The replacement direct pair preserves effective 68/114 credit;
[the runtime chapter](contract-runtime.md#stce-dependent-pending-and-the-v2-source-contract)
gives the selection table, worked transitions, instruction witnesses and limits.
Frozen v0/v1 records and pins stay exact. Sstc now binds a direct Execution pair:
31 boundaries / 62 parcels, S programming/read-back and handler-visible refusals,
plus original timer guests. [Worked values and controls](contract-runtime.md#observable-s-mode-timer-programming-and-refusals)
close the terminal-zero witness hole; v2 remains open.

````

## contract-integer

<!-- c30b payload: contract-integer:6 -->
````text
Five in-memory author copies are deliberately wrong. Zero-extended SLTIU fails
scope-alu, step 17; unsigned SLTI fails at step 14; zero-extended ANDI fails at step 8; zero-extended XORI
fails at step 10; saturating ADDI fails bound-arith, step 8. The existing integer-author sign
control also refuses. No source, expectation, frozen record, production author
or processor semantics changes. All 72 prior registry entries remain exact.
The repaired gate oracle passes with the ALU pair now actually registered.

````

<!-- c30b payload: contract-integer:12 -->
````text
Eight deliberately incorrect author copies fail exact steps: saturation at
bound-arith steps 5/6; swapped comparison signedness at scope-alu steps 11/13; wrong AND/OR/XOR
operators at scope-alu steps 5/6/7; cleared aliased ADD sources at bound-alias step 24. The
existing integer-author controls and full normal corpus comparison retain their
authority. NEG rejects these semantic alternatives, not a required trap for
valid register arithmetic. All 74 earlier registry entries and every old input
remain exact; no processor or production-author semantics changes.

````

<!-- c30b payload: contract-integer:18 -->
````text
Seven in-memory wrong author copies fail intended observations: LUI zero
extension or missing shift at scope step 3; AUIPC zero extension, missing shift
or unsigned saturation at bound step 29; next-PC or sign-extended base-PC at
chase step 0. The whole programs and their intermediate observations matter.
NEG rejects wrong legal arithmetic, not a required architectural exception.
The existing independent integer probe remains green; no production rule or
expected value changes. Both smoke-arith headers now name profile.sexp and the
assembler's implemented B/J support; each still assembles to the same twelve
instructions / 48 bytes. Generated guest data is exact, with only those source
fingerprint comments regenerated. That base-profile comment also changes the dossier
digest: the commit hook refused the stale board processor pin. The pin was deliberately
rederived through the shared digest owner, then board/platform artifacts and model-book
materials regenerated. Their semantic data, map and text stay exact except that identity
pin and provenance fingerprints. Frozen records and all 76 earlier entries stay exact.

````

<!-- c30b payload: contract-integer:27 -->
````text
At c17b, both bound-shiftw programs append SRAW x16,x8,x10 at address
0x800000dc, after all 55 original instructions. Its literal word is 0x40a4583b.
The existing x8=0xffffffff80000001 and x10=96 make rs2[4:0]=0: low32 remains
0x80000001, sign-extended to x16=0xffffffff80000001. That expected value was
recorded before either engine ran. The independent author matches every old
observation and the new boundary; all old instruction bytes and positions remain.
The base program now takes 56 word requests; the GC program takes 112 parcels.

````

<!-- c30b payload: contract-integer:28 -->
````text
The previously surviving six-bit SRAW author fails only at new boundary 55.
The same public processor bad-table diagnostic also fails exactly there: its
all-ones result disagrees with the committed identity. The correct core corpus
passes. A durable hand-encoded author case uses garbage upper bits
0x1234567880000001 and count 96, requiring the same sign-extended low word.
Its isolated sraw-count mutation fails with the named five-bit-count reason
before a new GUEST-GEN control is registered. The ordinary probe now has 23
arithmetic/10 branch cases, 17 corpus gaps / 472 steps and 42 owned records exact.
GUEST-GEN has 143 controls; the registered doctrine total becomes 647.

````

<!-- c30b payload: contract-integer:30 -->
````text
The full independent GC corpus matches 167 guests / 5,361 boundaries / 10,516
parcels. Pinned Sail 0.14 agrees on all 56 declared boundary-program rows and
change observations, with two fresh traces byte-identical. This is finite integer
evidence; the standing reference/platform and FP-independence limits still apply.
Only the selected guest data, diagnostic control and their provenance change.
The base dossier digest and dependent board/platform/model-book pins are rederived;
all other generated guest/board semantics and all 78 registry entries stay exact.
The SRAW count-mask coverage and SRLW explanation defects are closed. Contract
credit stays 76/114; nineteen runtime pairs and freeze remain.

````

<!-- c30b payload: contract-integer:38 -->
````text
The arithmetic low word is -2147483647. Shifting it right by one rounds down to
-1073741824, whose word is 0xc0000000; sign extension supplies the required
64-bit value. The wrong full-width read instead sees positive 2147483649 and
yields 0x40000000. Each isolated bad author now disagrees only at its new boundary
(58 for SRAW, 59 for SRAIW); public engine bad tables first fail at those same
boundaries. All 56 prior positions, bytes, expectations and observations stay exact.

````

<!-- c30b payload: contract-integer:39 -->
````text
The durable probe's existing garbage-upper-word hand cases also distinguish both
rules. New sraw-width and sraiw-width controls were observed RED with their named
arithmetic-word reasons before registration. The probe retains 23 arithmetic/10
branch cases and 42 owned records, with 17 corpus gaps / 476 steps. GUEST-GEN
now has 145 controls, and the doctrine total becomes 649.

````

<!-- c30b payload: contract-integer:40 -->
````text
The correct engine passes the full corpus. The independent author matches all
167 guests / 5,365 boundaries / 10,524 parcels. Pinned Sail agrees on the changed
60-step program's declared rows/change observations and repeats byte-identically;
the base live smoke also compares it against both Sail and Spike. The base budget
is 60 word requests, the GC budget 120 parcels. These source-width evidence defects
are closed; production rules and all 78 registry entries remain unchanged.
G-CONTRACT stays 76/114 with nineteen runtime pairs and freeze remaining. c17d
may now register SHAMT after its independent mask controls. The finite-reference
and platform limits above continue to apply.

````

<!-- c30b payload: contract-integer:46 -->
````text
The correct engine and author match all selected observations and the complete
167 / 5,365 / 10,524 corpus. All canonical inputs, guest data, production author,
core, frozen records and prior 78 bindings remain exact. Registry entries become
80; effective G-CONTRACT becomes **78/114**: thirteen scope pairs, nineteen guest
pairs, six boundary pairs and one direct-execution pair. Eighteen runtime pairs
and final freeze remain. This credit is finite evidence for these inputs; the
standing independence/platform limits still apply.

````

<!-- c30b payload: contract-integer:47 -->
````text
The scoped review also found incomplete requirement metadata: REQ-D-SHAMT's
statement names all twelve forms, while its base and GC insns fields omit
SLLW/SRLW/SRAW. The original base association commit added nine, and GC copied
that list. The aggregate extraction gate still sees the three forms through
WSUFFIX; it does not establish each requirement's association completeness.
The frozen statement and the twelve-form execution evidence above are correct.
At c17d this metadata defect was OPEN and owned priority-next by c17e, before
word-result registration. Implementation-status/experiment work stays .14.

````

<!-- c30b payload: contract-integer:49 -->
````text
The change propagates through the base dossier pin into the composed board's
requirement metadata, platform provenance and model/report outputs. It adds no
instruction or observation and changes no runtime behavior. All guest data,
production rules, frozen records and 80 registry entries stay exact; effective
G-CONTRACT remains 78/114. c17f now reviews all nine word-result forms before
binding WSUFFIX. Eighteen runtime pairs and final freeze remain.

````

<!-- c30b payload: contract-integer:57 -->
````text
The normal author/core matches all selected observations and the full
167 / 5,365 / 10,524 corpus. Canonical inputs, generated data, production rules,
frozen records and all prior 80 bindings remain exact. Registry entries become
82; effective G-CONTRACT becomes **80/114**: thirteen scope, twenty guest, six
boundary and one direct-execution pairs. Seventeen runtime pairs and freeze
remain. Negative fixtures are legal semantic counterexamples, with no invented
target traps. Standing finite-evidence/reference/platform limits remain.

````

<!-- c30b payload: contract-integer:66 -->
````text
The independent author confirms the literal words, canonical mappings, GPR/PC/U/
counter/memory values and fetch/walk logs. It does not log data boundary requests;
the public CPU observer separately checks those. The declaration test first
refused the missing binding. Unchanged companion guests are POS scope-alu
(31/62) and NEG bound-arith/sv39-fault-canonical (89/178). Including the direct
cases, the pair runs **128 boundaries / 256 parcels**. The full independent
167/5365/10524 corpus and all prior inputs/runtime/frozen data remain exact.
Rust 167/17/210 passes. Registry 94 realizes **92/114** effective checks:
thirteen scope, 23 guest, six boundary and four execution pairs. Eleven runtime
pairs and final freeze remain. This is finite width evidence under the selected
translation and provider rules.
````

## contract-control

<!-- c30b payload: contract-control:7 -->
````text
All thirteen variants fail before credit. The unmodified public driver matches
all five guests, including never-written registers and parcel counts. Independent
normal replay matches the entire 167-program corpus, 5,365 boundaries / 10,524
parcels. The declaration test first fails on the missing binding, then all Rust
checks pass (167 core / 17 DSP / 206 verify). All prior 88 bindings, canonical/
guest inputs, core, author, generated data and frozen records remain exact.
At c21b, registry entries reach 90, effective G-CONTRACT **88/114**: thirteen scope,
twenty-three guest, six boundary and two direct-execution pairs. Thirteen runtime
pairs/freeze remain. These observations constrain architectural effects; they do
not prescribe a processor pipeline or establish untested target-fault behavior.

````

<!-- c30b payload: contract-control:14 -->
````text
This is an evidence gap, not a newly observed CPU defect. c22b2 owns the priority
repair: literal post-step target/link/request witnesses, including low-bit carry,
negative immediates, wrap and source/link aliasing, with deliberately wrong public
tables before registration. JALR remains uncredited until that work passes.
The annotation repair passes Rust 167/17/206, GUEST-GEN (147 self-test arms),
independent normal 167/5365/10524 replay and full local CI (check, doctrines,
bench, bench smoke, main and five model books). All protected runtime/canonical/frozen data and 90 prior
bindings remain exact; effective G-CONTRACT stays **88/114**, thirteen runtime
pairs and final freeze outstanding.

````

<!-- c30b payload: contract-control:21 -->
````text
The declaration test first refused the missing binding. POS also runs unchanged
guest-control/dir-chase (30 boundaries/60 parcels); NEG runs fault-jalr-mis/
it-prio-jump (6/11). Together with the direct cases the pair runs **53/103**.
The independent author reproduces every literal case and the full unchanged
167/5365/10524 corpus. Prior 90 registry entries, all canonical inputs, CPU,
author, generated fixtures and frozen contracts stay exact. Rust 167/17/208
passes. Registry 92 realizes **90/114** effective checks: thirteen scope,
23 guest, six boundary and three execution pairs. Twelve runtime pairs and
final freeze remain; these finite witnesses establish no universal ISA claim.
````

## contract-memory

<!-- c30b payload: contract-memory:10 -->
````text
The declaration test first fails with CHK-LOAD-EXT-POS missing, then passes when
both exact bindings are registered. Normal independent replay matches the entire
167-program corpus, 5,365 boundaries/10,524 parcels. All earlier 82 bindings,
canonical and guest inputs, generated data, production rules/author and frozen
records remain exact. Registry entries become 84, effective G-CONTRACT **82/114**:
thirteen scope, twenty-one guest, six boundary and one direct-execution pairs.
Sixteen runtime pairs and freeze remain. These finite, legal counterexamples do
not require target traps and do not establish untested memory-system behavior.
Address faults, x0 side effects and the selected endian policy retain their own
contract obligations.

````

<!-- c30b payload: contract-memory:19 -->
````text
Normal Rust checks pass 167 core / 17 DSP / 206 verify tests. Independent normal
replay and all prior 84 bindings, 112 base / 348 GC canonical and guest inputs,
production rules, author, generated data and frozen records remain exact.
Registry entries become 86; effective G-CONTRACT is **84/114**: thirteen scope,
twenty-one guest, six boundary and two direct-execution pairs. Fifteen runtime
pairs and final freeze remain. Request logs prove the access occurs; they do not
add a device or claim unimplemented MMIO behavior. Byte-order selection and other
remaining obligations retain their own witnesses.

````

<!-- c30b payload: contract-memory:26 -->
````text
The declaration check first fails on the missing ENDIAN binding, then passes.
Normal Rust checks and independent full 167/5365/10524 replay pass. All prior 86
bindings and canonical/guest/core/author/generated/frozen data remain exact.
At c20, registry entries reach 88, effective G-CONTRACT **86/114**: thirteen scope,
twenty-two guest, six boundary and two direct-execution pairs. Fourteen runtime
pairs/freeze remain. This is evidence for the selected ordinary-memory byte
order; it does not add selectable big-endian execution or a device model.

````
