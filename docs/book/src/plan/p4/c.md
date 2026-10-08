# P4.12 — Compressed instructions (C)

**Status:** Underway (slices a–d1; guest image tools and production bind next)

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

A permanent fifteen-case probe compiles this evaluator against a temporary composition with
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

The production profile still declares C unbound. The next slice carries these exact images
through guest generation and the runner, then promotes and extends the expectation author
and Sail adapter. The specification-derived corpus and C bind land together, followed by the
matched Sail experiment. These probes are finite component evidence.
