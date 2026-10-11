# DEV_NOTES shard — _(2026-10-11)_ … _(2026-10-11)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-11)_ — bounded source-byte image construction (P4-SYSTEM.14 a42c)

Extract encode_elf64 as the sole pure owner; legacy write_elf64 constructs then
writes once/returns None. Whole-source inverse recovers repaired93525ac exactly,
all216 guest ELF bytes stay exact and all167 GC source-byte builds match normal/O.
New frozen builder accepts plain immutable UTF8 bytes1..1MiB, program1..65536 and
unsigned64 entry; preflights8192 exact Python splitlines before list allocation/
canonical I/O, caps payload32KiB/image64KiB. Known canonical GC file/IALIGN16 only;
source never reopened, no pathwrite/process. Retain only imagebytes and exact
program/route/entry/IALIGN plus source/payload/image sizes/hashes. Caller owns
source authentication, parent selection and complete current tool adequacy;
canonical tool reads are outside supplied-artifact budgets. This is construction,
not source semantics, correspondence, CPU acceptance or qualification.

D44-WRITER-ORDER: initial one-line path.write_bytes(encode_elf64(...)) looks up
output method before validation. Exact93525ac gives AsmError/no lookup forentry1;
draft51834B/c36aa80fe71ab6c5830eae2b0157f86684f6c444ef6c9e1cdc77983b4681e5cb
gives getter OSError/one lookup. First32 controls/sixteen omissions and all216
byte comparisons missed it. Own before repair; separate encode statement restores
legacy order. Exact draft inverse/hash recovered; added33rd test and17th omission
lose1 assertion/zeroerrors normal/O.33 controls green; all17 omissions lose
7/1/6/6/1/8/1/3/4/1/1/1/1/2/6/1/1 without errors in both modes.
Preserve old ELF15/eight; register36 literal arms with all222 old arms exact.
Source/metadata/assembly refusals have fixed bounded ImageError diagnostics;
unavailable/malformed canonical context is distinct ImageUnavailable. Bounds
are not RAM/time claims; nonempty comments can produce empty payload, raw directives
are not instruction-semantic proof. Full runnable book example teaches these limits.

Focused17/sharder12/0/seven books/3140 links/all13 literal examples and normal/print teaching
green; whole source/API/normative/book/task guards,340 raw forms/243 maps,
104 old entries/1332 other files/modes/Gitlinks exact normal/O. Real original/
moved/published receipt rewrites refuse with updated digests. Derive GUEST258/0,
39 doctrines1267 arms, PROFILE390/0 retained. Initial main-book54B overflow
refused/corrected by tightening current explanation. Fixed caps/seals unchanged.
DEV4006B to0253(4239B/9bde028021b6d96fae40dc7a178960ea18c2111fc10f9eacea6b98949e568646),
CH771B to0254(1008B/692a564a4cda7f1dc955b944bc7fedd5ab5cebabb6c361d12ad97fd1288f00ee);
46live+210sealed256logical. Only two inherited whole-entry EOF blanks, no trimming;
ephemeral Git whitespace exception. Final docs/hooks/hash equality/brief0/censuses.
Final diagnostic first matched the new current PROFILE390 lesson rather than
history; anchored its mutation in the exact complete committed entry and repeated
all real receipt/digest negatives normal/O. No guard or historical bytes changed.
Preceding clean93525ac full CI all5 legs green:443 Rust/smoke53/seven books,
18 sources unchanged; log40159B/19491814401b0281d45c2c30f8e96e888c59c0babe4cb6c3012c07775999e625.
D45 preflight diagnostic expected an extra newline; Python failed, then a shell
message write masked its status and unconditional orchestration started commit.
Interrupted rc130 before commit; HEAD93525ac and both censuses clean. Correct exact
whitespace comparison/already-staged census; enforce successful tool exits before
each mutation, recreate19 hashes and prove stage equality before retry. No source,
history or COMMIT contract defect.
Corrected19-file preflight rc0; actual stale stage and old warning mismatch
controls refuse rc1 normal/O, the latter creates no hash receipt.
Evidence target/p4-system-14/a42c. Next a42d authenticated correspondence within
existing aggregate budgets, then complete closure/impact/collector provenance.

## _(2026-10-11)_ — repair inherited ELF alignment and flags (P4-SYSTEM.14 a42b)

D43-ELF-ALIGNMENT owns a source/image prerequisite defect. Exact da627ff writer
50548B/884a42ee615c98570617a650b57bdf4035601ae9bd94e21f0b53c54f1e1e5d87
reproduces all four failures normal/O: PT_LOAD offset120 with alignment4096;
section table139 for a2-byte payload; text alignment4 at entry0x80000002;
RVC flag0 for IALIGN16. Invalid IALIGN0 divides by zero. Own history shows compact
layout/alignment in b8d09f5377c093f2e96eaddf49c968b6074a40d1;831a179fcefcdc34551530fcd804e81f71c00488
added profile IALIGN while preserving those fields. This is input-container drift,
not a CPU result or a reason to alter historical artifacts.

Pinned ratified RVI-PSABI1.0 PDF273939B/a8d06bdcaa82a6a4567a1904dc27ef1ca1043ebaa1f523558c927a9d72bc23d9
§8.1 confirms C alignment/RVC and separates internal FP from calling-convention
flags. Primary gABI1.2/3.2/7.1 confirms natural structure/text/load congruence.
Choose the first header-following file offset congruent with entry modulo4096;
zero padding remains outside PT_LOAD. Align section table8, text2/4 by IALIGN,
set RVC1/0, retain soft-float bits0. Validate known IALIGN, unsigned64 entry and
load extent before writing. Preserve payload, addresses, RWX, names and None
return, including empty/odd payloads and legacy bytearray. Clarify the Rust parser
fixture's synthetic scope/name; it never executed the actual Python writer.

15 controls normal/O pass; eight isolated omissions lose1/2/1/1/1/9/6/1 clean
assertions in each mode. All3072 legal IALIGN16/32 page offsets checked. All49
RV64I/167 GC payloads match exact old-source assembly; invert only authorized
layout/metadata and recover each complete old ELF byte-for-byte. Register18
literal GUEST-GEN arms, keeping all204 prior arms:222/0;39 doctrines1231 arms.
Rust443/focused17/sharder12/0/seven books/3138 links/all12 literal examples and
normal/print teaching pass. Real Python-produced ELF runs through public Rust CLI
in both profiles with two exact hand-derived PC/write observations. Initial GC
diagnostic wrongly used the scalar word-bearing parser; the published GC route
prints PCs/writes, so the corrected oracle checks that complete literal output.
Initial index drift/source-link failures were caught and corrected before signoff.
Whole original source/checker204 arms/Rust fixture/book/task inverses,340 raw
forms/243 maps,103 old entries and1330 other files/Git links stay exact normal/O.
Actual original/moved/published receipt edits refuse even with updated digests.
DEV16=15+1/2722B into0252 (2955B, SHA256
49a4796d11355d281fa5a7751ba5126a83e0f6eadfc53dd34079732b5ec985bb);
44live+210sealed254logical. Staged hashes/hooks/brief0/censuses finish COMMIT;
full CI follows the clean repair milestone before a42c. Teach literal field decoding/limits and
historical loader tolerance without ABI/CPU/qualification overclaim. No canonical,
reference, schema, seal or cap change. Evidence target/p4-system-14/a42b.

