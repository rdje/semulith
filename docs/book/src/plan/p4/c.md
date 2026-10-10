# P4.12 — Compressed instructions (C)

**Status:** Landed and closed (2026-10-09; final signoff e2e)

This profile implements 37 compressed forms at RV64 with D. They use two bytes
alongside ordinary four-byte instructions, reducing code size without introducing
a separate execution engine. Each form declares its ordinary instruction and
operand mapping in the canonical definition. The one special link rule is
C.JALR's return address: pc+2.

## Selected forms and operand mappings

| Family | Selected forms |
| --- | --- |
| Constants and stack offsets | `c.nop`, `c.li`, `c.lui`, `c.addi`, `c.addi16sp`, `c.addi4spn` |
| Register, immediate and word arithmetic | `c.addiw`, `c.srli`, `c.srai`, `c.andi`, `c.sub`, `c.xor`, `c.or`, `c.and`, `c.subw`, `c.addw`, `c.slli`, `c.mv`, `c.add` |
| Integer memory | `c.lw`, `c.ld`, `c.sw`, `c.sd`, `c.lwsp`, `c.ldsp`, `c.swsp`, `c.sdsp` |
| Double-precision memory | `c.fld`, `c.fsd`, `c.fldsp`, `c.fsdsp` |
| Control and breakpoint | `c.j`, `c.beqz`, `c.bnez`, `c.jr`, `c.jalr`, `c.ebreak` |

A compact three-bit register field denotes x8–x15 or f8–f15; forms with a
five-bit field can name the corresponding full register set. Scattered
immediate pieces reconstruct one value with its declared width. For example,
`c.addi x1, -32` retains the signed six-bit immediate until the ordinary ADDI
rule sign-extends it. Load/store offsets are unsigned byte offsets, including
their required low zero bits. Word arithmetic truncates to 32 bits and then
sign-extends the result to XLEN.

The composition checker requires every operand read by the expansion to be
supplied exactly once. A reserved encoding traps before effects; a HINT executes
its declared expansion, including writes discarded by x0. Six declared
specializations resolve intentional encoding overlaps, with the most specific
row first: C.EBREAK must win over the broader register-operation encodings.
Reversing that order or changing the compact-register offset fails the compiled
mapping/decoder probe.

C.JALR reads its old source before writing x1's pc+2 link, including when the
source itself is x1. Its ordinary jump rule clears target bit zero, retaining
bit one under IALIGN=16. Integer and D loads/stores use their ordinary rules;
the four D memory forms are illegal with FS=Off before any data request.
C.EBREAK delivers the breakpoint cause with the instruction PC. Other reserved
compressed forms report their original sixteen bits in the illegal diagnostic.

## Exact parcels and fault boundaries

The CPU first issues `FetchParcel` for exactly two bytes. A compressed instruction
needs no second request; an ordinary instruction needs another parcel before
execution. PC advances by two or four according to the original instruction,
even though the evaluator executes an ordinary expansion. Fetch counts measure
physical parcels. The legacy four-byte `Fetch` operation remains a distinct
interface, rather than padding a short instruction behind the caller's back.

A compressed instruction can execute in a two-byte region or a page's final
halfword without touching the next region/page. A four-byte instruction at that
same halfword needs the next page. If the second translation or parcel fails,
there are no instruction effects: the saved exception PC names the start and
the trap value names the failed second parcel. A refused physical request
counts as an attempt; failed translation supplies no physical request.

This profile has ILEN=32. Unsupported wider prefixes still fetch the first
32 diagnostic bits: an all-ones word reports 0xffffffff, not 0xffff. The
second parcel can therefore fault even though the eventual instruction is
unsupported. The earlier short-prefix bug and the earlier large-JAL sign-bit
bug have permanent regressions; the latter affected forward/backward jumps
across the 512 KiB sign boundary in both processor models.

Eighteen engine probes compile the tracked evaluator and check mixed lengths,
register aliases, signed/unsigned mappings, links, FS gating, page edges and
unsupported prefixes. The definition gate runs them with three behavioral
mutations that erase mapped widths, replace parcel reads by word reads or
truncate wider prefixes. A compile failure does not count as a discriminating
behavioral result. The C-only provider explicitly rejects an unexpected SC
permission request after that boundary operation was added.

## Assemble and inspect a mixed program

The assembler accepts architectural compact-register names and one argument
per scattered immediate. Labels advance by the actual instruction size;
`.half` places a raw parcel. `assemble_units()` exposes each PC/value/length,
and `assemble_image()` joins the little-endian bytes without padding. The
legacy word-only API refuses a short unit. The
[assembler guide](../../annex/assembler.md#compressed-instructions-and-exact-byte-images)
lists stack, compact-memory and floating-point syntax and operand refusals.

For example:

```text
c.li x8, 3
c.addi x8, -1
addi x9, x8, 4
c.mv x10, x9
```

| Byte offset | Instruction size | Visible result |
| --- | --- | --- |
| 0 | 2 | x8=3 |
| 2 | 2 | x8=2 |
| 4 | 4 | x9=6 |
| 8 | 2 | x10=6 |

The exact image is ten bytes. Four retired boundaries consume five parcels at
offsets 0, 2, 4, 6 and 8; the final PC is entry+10. Adding silent padding would
change both the loaded bytes and subsequent addresses. Hand-encoded fixtures
cover all 37 spellings; compact-register, label-stride and padding mutations
fail the authoring checks.

The independent instruction author has its own compressed decoder, built from
the pinned chapter and instruction diagrams rather than the engine's expansion
mappings. It accepts an explicit boundary budget and fetches current memory,
so a code store can alter a later compressed instruction. Leaving the source,
entering a handler or waiting cannot shorten that budget. Unknown valid
vocabulary refuses instead of becoming a fabricated illegal instruction.
[The explicit byte route](../../annex/assembler.md#compressed-instructions-and-exact-byte-images)
and its budget example document the commands and output ownership.

Its component controls include all forms, immediate extremes, 79 individual
scattered bits, hints/reserved cases, old-source C.JALR links, precise parcel
faults, privilege permissions and the selected translation cache. Individual-bit
checks matter: permuting two immediate bits can pass an all-ones limit. These
are finite checks, not universal ISA conformance or independent numeric-backend
qualification.

## Current scope and retained history

The complete composition has 197 instruction rules and three counter pseudos;
all 200 spellings are exercised by the 167-program corpus. C contributed
28 programs covering compact/stack memory, arithmetic limits, aliases, branches,
links, hints, reserved/FS faults, LR/SC and translated page edges. Historical
word-fetch captures keep their original provenance while adopted parcel counts
are checked against the actual request log. Staging and production checks refuse
changed observations, incorrect extents, stale exceptions and borrowed capture
headers. The STCE-aware timer program and source-contract qualifications are
explained in [the runtime chapter](contract-runtime.md#explicit-comparator-setup-before-fallback-repair).

Open v2 includes C's instruction guarantee and exact two-byte physical fetch
supply with their executable positive/negative pairs. Frozen v0/v1 remain exact.
The compressed fault/interrupt-return matrix retains its declared degeneracies;
CPU acceptance still depends on the remaining contract and evidence work.
[The current contract summary](contract-v2.md#runtime-guarantee-witnesses)
owns the realization measure. Public reference observations and their comparison
limits follow below.

The complete earlier chapter, including implementation chronology, discovered
defects, staging/migration counts and original signoff receipts, is preserved
byte-verbatim in `docs/tasks/archive/P4-SYSTEM-book-c34b1.md`. Its source digest
and inverse authenticate the transition; no historical observation was rewritten.

## Bounded reference runs

P4.13 c28c repairs two adapter defects found during the atomic-reference review.
A guest's declared budget counts architectural boundaries, including delivery
attempts that fetch no instruction. The adapter had asked Sail for two additional
attempts. For dir-chase, all 17 declared rows were present, ending in EBREAK;
the extra attempts fetched at the default trap address zero and produced two
fetch-access faults without instruction rows. The strict parser mapped both to
boundary 17 and correctly rejected their duplicate delivery. The runner had
requested evidence outside its claim and then let that tail invalidate the
complete intended run.

The runner now passes the exact declared count to the public --inst-limit option.
The same pinned binary, configuration and ELF produce an agreeing 17-boundary
trace. The parser still reads the whole supplied trace and refuses malformed,
duplicate or out-of-order records. It does not discard a suspicious suffix or
accept a shorter prefix. Cached traces with the old duplicate tail still refuse.

The remaining fault-fetch refusal exposed a second vocabulary mismatch. Its
historical record says "the fetch at 0x40000000 — no word fetched"; later parcel
records use "<fetch ...>". The actual trace contains a fetch-access-fault event at
boundary 2, after LUI/JALR. The adapter now recognizes that exact legacy syntax
with a hexadecimal address. Both spellings still require an actual fetch-class
event and empty declared GPR writes. An instruction row there diverges; missing,
non-fetch or malformed events refuse. Canonical expectations are unchanged.
The adapter compares delivery presence/class; it does not compare event tval
against the expectation prose.

```sh
python3 scripts/run_rv64gc_sail.py dir-chase fault-fetch c-links c-page-end c-page-straddle
python3 scripts/probe_gc_sail.py
```

The offline probe exercises the real runner with a process stub that requires the
exact limit and writes two fresh complete traces. It fails on the former +2
invocation. A separate control fails when legacy syntax is unrecognized. Further
controls retain the complete three-boundary sequence with an interior witnessed
gap and reject a missing final row, an unwitnessed gap, duplicate/malformed
deliveries, invalid legacy syntax and an attempted GPR-write waiver. The five
existing broken-adapter mutations still fail. These checks run in the existing
GUEST-GEN arm; no new registered arm or CPU-contract credit is claimed.

Two fresh exact-limit raw traces per guest assess all 167 existing programs.
All 25 formerly observed tail refusals have complete agreeing declared evidence
after the vocabulary repair. One has cross_model=false and remains refused by
the normal runner; raw diagnostic comparison does not override that guard.
The normal runner records 149 AGREE over 4,566 declared boundaries with fresh
byte-identical pairs, 14 unchanged policy/platform DIVERGE, and four REFUSED:
mm-counters, w-notrap and w-timer still fail without the matched time source;
guest-no-device is disabled. All 125 prior agreements and all 14 prior differences
remain. Required second-parcel and first-parcel page faults, mixed C/32-bit code,
and the historical terminal fetch event retain their evidence.

These are finite GPR change-observations and witnessed delivery gaps. PC/word,
FP registers, direct CSR state, memory and requests remain outside this adapter's
comparison except where read back into declared GPR changes. Requirement statuses,
structured experiment records and independent evidence classification remain
P4.14's work. Contract realization is reported by [the current contract summary](contract-v2.md#runtime-guarantee-witnesses).

## Historical verification receipts

Dated progress counts, pre-bind identity checks and exact provenance receipts
are preserved in `docs/tasks/archive/P4-SYSTEM-book-c29d.md`, section `c`.
That record authenticates the original chapter and every removed span; all
current feature examples and commands remain here.
