# P4.12 — Compressed instructions (C)

**Status:** Underway (tools done; author prerequisites, staged corpus and bind next)

The C extension lets a program use 16-bit instructions alongside the usual 32-bit ones. Linux
software is built to use them. They save space, and each one is simply a shorter spelling of an
ordinary instruction: the specification says every compressed instruction "expands into" a
single standard one. This leaf adds the 37 compressed instructions this profile selects (the
64-bit integer set, plus the four double-precision loads and stores).

Supporting C means teaching the processor model that instructions come in two lengths. It has
to read the first 16 bits, decide how long the instruction is, and only then read more. It also
has to step the program counter by 2 or 4. The plan treats each compressed instruction as data:
the ordinary instruction it expands into, how its operands map, and the specification's own
sentence saying so. The one exception, the compressed jump-and-link, is the one the
specification itself calls out.

Slice (a) brought in the official encoding tables for the 37 instructions, fingerprinted so they
cannot change silently, and generated the model's description of them. Six pairs of compressed
instructions overlap on purpose: for example, the no-operation instruction is a special case of
"add immediate" with every field zero. The upstream tables list these pairs. Each is now
recorded as a deliberate special case that the decoder must try first. The composition checker
still refuses any overlap that has not been declared this way, and any declaration that isn't
genuinely a special case.

Reading how the model takes instructions apart turned up an older bug (slice a2). A jump's
target is the instruction's own address plus a signed offset. For the jump-and-link
instruction, the model took the offset's sign from the wrong bit. So a jump of more than 512 KB
forward went backward, and the reverse. This had been true in both processor models since the
first phase. No test program jumps that far, so every check passed. It surfaced because the
compressed jump has the same shape. It is now fixed in both models, tested at exactly the
boundary and at both extremes, and recorded against the earlier scalar release. That release's
recorded results are unaffected: each one is a pass, and any test that had reached this range
would have failed.

Slice (b) gives each of the 37 compressed forms its declared expansion. A compact register
field, for example, maps its three bits to registers x8 through x15 by adding eight. Scattered
immediate pieces are put back together with their own signed width; a load's unsigned offset
is zero-extended first. The checker requires every operand the ordinary instruction reads to
be supplied exactly once, and requires the specification's quoted expansion sentence to name
that instruction. C.JALR carries the exception's own rule: its return address is pc+2.

Reserved code points are declared from the specification's sentences. Hints can execute their
ordinary expansion: writing register x0 changes nothing. The generated table tries the most
specific encoding first, so a compressed breakpoint wins over the jump-and-link and add forms
that also match its bits. A permanent probe checks all 37 forms and the immediate limits, then
compiles the generated Rust and checks the mappings, effects and eight decoder cases. Giving a
compact register the wrong offset, or reversing the table's order, makes the checks fail.

The session crashed during slice (b); the task-tree and surviving files recovered its exact
frontier. PNT resumed on October 8. Slice (c1) adds an exact two-byte instruction request to
the environment boundary. The old request always read four bytes, even when the processor
kept only the first two; it could not fetch a compressed instruction at the end of a two-byte
memory region. The new request succeeds there, keeps the same alignment and code-visibility
rules, and lets fault injection distinguish the requested parcel from its neighbor.

For C-enabled execution, the processor requests one parcel first and requests another
only when the instruction needs it. This replaces the earlier coalescing plan: a four-byte
request cannot distinguish a failure in an unnecessary upper half from a failure in the
instruction itself. Fetch counts will therefore count parcels when C binds, and the next
environment-contract version will state that extent.

Slice (c2) executes each expansion's ordinary rule after evaluating its operand mappings
against the original compressed fields. The mapped values keep their signed widths; otherwise
an immediate of −32 could become +32 before the ordinary rule sign-extends it. The program
counter advances by two or four, and an illegal compressed instruction reports its own sixteen
bits. Hints execute without changing registers, while the declared reserved code points trap
without retiring or leaving a partial write.

A permanent eighteen-case probe compiles this evaluator against a temporary composition with
C. It checks mixed instruction lengths, compact registers, signed and unsigned offsets,
overlapping operands, jump links, floating-point gating, and faults. A compressed instruction
in a page's final halfword never walks the next page. A 32-bit instruction in the same place
does: if the second page faults, the trap's value names that second parcel, while the saved
program counter names the instruction's start. Both the prior evaluator and deliberate
mutations fail these checks. They run through the definition gate on every commit.

Slice (d1) teaches the assembler all 37 compressed forms. It derives compact register and
floating-point spellings from the declarations, gathers scattered immediate pieces into one
operand, and refuses reserved operands or a spelling that would encode a different special
case. Programs can mix two- and four-byte units; labels count bytes, and `.half` can place an
explicit raw parcel. The byte-image API preserves those lengths exactly. The older word API
refuses short units so they cannot acquire silent padding. The [assembler chapter](../../annex/assembler.md)
gives the syntax and examples. Hand-encoded fixtures check every form, and deliberate compact
register, label-stride and padding mutations fail the permanent checks.

Slice (d2) carries exact byte images through guest generation and the rv64gc runner.
The generator's byte mode emits u8 arrays and the runner loads them directly. The scalar
fixture keeps its word API for replay and reduction. A generated 14-byte mixed program runs
on the temporary C composition, checking the actual loaded bytes, a four-byte instruction at
a two-byte offset, a jump over an illegal parcel and a trailing halfword. Its five executed
steps request six parcels. Padding the image or moving the loader's offset makes the checks
fail. All 139 existing rv64gc images and observations remain unchanged in this slice.

Slice (d3a) promotes the expectation author into tracked code. It computes values from
spec-side rules and offers non-writing checks. Its 42 declared historical records re-derive
byte-for-byte. The broader census caught reserved upper bits being interpreted as ordinary
operations, and missing SUM/MXR/U permissions in its data walk; both are fixed. The affected
permission guest now matches all 169 committed step observations. Direct permission fixtures
and six mutations guard the repairs, without using the instruction engine as an oracle.
The author still has a bounded vocabulary. C expansion and instruction-fetch
translation follow below. Existing records keep their original provenance.

Slice (d3b) tracks the Sail runner and repairs that comparator. Every ordinary expected
instruction needs a row, including instructions that change no register. A declared
interrupt or fetch-fault step instead needs a matching trace event. Failed processes,
stale output and malformed traces refuse. Two executions must reproduce the same trace.
The runner builds exact byte images with the tracked ELF writer, checks the binary pin,
and derives the matched configuration from its source.

The audit inspected 95 cached corpus traces. All 79 from previously agreeing cells pass
the stricter comparison; their gaps are nine declared interrupt deliveries and one fetch
page fault, each witnessed by an event. The sixteen known not-matches keep their named
limitations. Cached process statuses were not retained. A fresh run of all four M programs
checks successful status and agrees on 99 steps, with identical repeat traces. A temporary
mixed C image also agrees on its five hand-derived addresses, words and writes.

Slice (d3c) adds independent C component rules. A separate spec-side decoder reconstructs
all 37 RV64+D forms from the pinned chapter and its instruction diagrams. It reads neither
the engine's expansion declarations nor the assembler's mappings. The ordinary spec-side
rules now accept an instruction length, so sequential addresses and links use two bytes.
C.JALR computes its target from the old register before returning a pc+2 link, even when
both registers are x1. Word arithmetic truncates to 32 bits and sign-extends. Reserved
parcels and floating-point state faults retain the original sixteen bits in the trap value.

The permanent probe checks every form and its effect, immediate extremes, 79 individual
scattered bits, hints and reserved cases. A permutation of two immediate bits can pass an
all-ones limit, so those individual-bit checks matter. Six deliberate mutations fail,
including a wrong two-byte link and reporting the expanded word as the trap value. The
42 owned records and all 91 previously emitted texts stay exact. The guest author still
uses its earlier word fetch route; C component execution is ready for parcel fetch/budgets.

While deriving the independent fetch path, slice (d3d0) found a mistake in the evaluator's
handling of unsupported longer instructions. It stopped after one parcel when the low five
bits were all ones. For this profile, the nonzero illegal-instruction diagnostic must retain
the first ILEN=32 bits. An all-ones instruction was therefore reported as 0xffff instead of
0xffffffff, and faults in its second parcel were missed. The evaluator now reads two parcels
for every wider prefix and stops at this profile's ILEN. Three permanent cases reproduce the
old failures and guard full bits, an access refusal and a second-page fault. The old evaluator
and a deliberate short-ILEN mutation fail all three; the complete probe passes eighteen.

Slice (d3d1) gives the independent author its own translated parcel fetch. Each necessary
parcel walks first and requests exactly two bytes from memory. A refused physical request
counts as an attempt; a failed translation issues no instruction request. Memory outside
the assembled payload still follows the declared region, whose unwritten bytes are zero.
The fetch primitive delivers faults without advancing time or retirement; the guest runner
will own those boundaries. Compressed page-end instructions never inspect the next page.

The new fixtures exposed four older walk defects: an inconsistent Sv39 sign extension
was accepted, reserved high PTE bits were ignored, a bottom-level pointer refused instead
of page-faulting, and MPRV did not select effective data privilege. These are repaired,
including reserved non-leaf U/A/D bits and effective SUM/U permissions. Odd instruction
addresses exposed a fifth defect in the author: saved exception and interrupt PCs retained
bit zero. Both M and S delivery now clear that bit while preserving bit one. Nine deliberate
mutations fail on these guards and fetch schedules. All 97 earlier emitted texts, including
the 42 owned records, remain byte-identical; this component still leaves the older guest
execution route in place until the next slice explicitly adds byte execution and budgets.

Slice (d3d2) integrates those components into an explicit byte guest route. The caller
declares a boundary budget. Leaving the source, entering a handler, delivering an
interrupt or waiting cannot silently shorten it. The exact image lives in memory, whose
current bytes supply each instruction; source annotations follow byte PCs. A word store
that patches compressed code is visible to the next fetch. Actual parcel attempts give
the request count, and fault/delivery/wait boundaries never retire. Unknown valid
instruction vocabulary still refuses instead of becoming a fabricated illegal trap.

Five earlier fetch/end gaps now derive all 176 committed architectural observations:
the zero parcel after a program ends, two terminal target fetch faults, a translated
straddle and a fetch-permission handler. Their budgets were declared before this
experiment. Their independently derived parcel counts are 5, 5, 7, 104 and 226; the old
word-request counts remain historical until binding changes the declared extent. Eight
mutations fail on byte annotations, padding, source termination, counts, retirement,
interrupt ordering, code visibility and unknown-valid refusal. The historical word route
still reproduces all 97 earlier texts, including its 42 owned records.

The production profile still declares C unbound. The staged specification-derived corpus
and count derivation precede the C bind, then the matched Sail experiment. These probes
are finite component evidence. The [assembler chapter](../../annex/assembler.md) documents
the explicit authoring command and its budget semantics.

The full pre-bind census exposed prerequisites in that independent author: fixed `misa`
fields, privileged legality, a bounded base vocabulary and the declared translation cache.
Slice (e1a) repairs the fields and permission guards; five mode-matrix guests now match
140 committed architectural steps and nine mutations fail. The census reaches 118 exact
of 139 historical traces, with twenty named vocabulary refusals and one owned cache-policy
disagreement. Each prerequisite is scheduled before staging can adopt parcel counts.

Slice (e1b1) adds the base integer vocabulary that seventeen of those refusals named:
comparisons and XORI, XLEN and word shifts, signed/unsigned branches, and narrow memory
stock derivations. Word shifts use five count bits and sign-extend their 32-bit result;
XLEN shifts use six. A named reserved-word outcome lets parcel execution deliver the
declared diagnostic before effects, keeping the full raw word and no retirement.
Unknown valid vocabulary continues to refuse. Its permanent controls now use an
unmodeled real CSR because XORI and byte loads have become supported operations.

Twenty-two hand arithmetic/alias/x0 cases, ten branch cases, narrow memory and reserved
fixtures pass. Eight mutations fail, and all seventeen formerly refused guests match
471 committed architectural steps. The census now reaches 135 exact traces, with three
remaining CSR/directive refusals and the owned cache disagreement. All 105 earlier word
texts and 42 owned records remain byte-identical. No production fixture or count has
been adopted during these prerequisite repairs.
