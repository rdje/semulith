# P4.12 — Compressed instructions (C)

**Status:** Landed and closed (2026-10-09; final signoff e2e)

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

At slice (d3d2), the production profile still declared C unbound. The staged
specification-derived corpus and count derivation preceded the C bind at (e2c),
with the matched Sail experiment next. These probes
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

Slice (e1b2) resolves the last three vocabulary refusals. The independent author now
registers and legalizes the selected counter-enable and STCE fields. Supervisor timer
compare access needs both enable gates before effects, while machine mode bypasses
them. Source annotations can contain quotes and backslashes; every emitted literal
field uses the canonical renderer and round-trips through the reader and schema.

Thirty mode-gate cases, mask/alias and literal-text fixtures pass; eight deliberate
mutations fail. Three formerly refused guests match 117 architectural steps, and all
121 prior word texts and 42 owned records remain byte-identical. The parcel census
reaches 138 exact traces with no vocabulary refusals. The remaining guest exercises
the declared translation cache, which must be modeled independently before count adoption.

Reviewing that cache prerequisite exposed an older production fence defect (e1c0).
The fence used operand values to choose broad scope, confusing a nonzero register
holding zero with register x0. The semantic effect now carries register-identity
selectors separately from the address and ASID. Three parent-failing regressions pass,
including page/ASID zero and masked ASID bits; the earlier fence fixture is corrected
and armed with an occupied cache. The [Sv39 chapter](sv39.md) explains the four cases.
This repair precedes the independent cache author; no evaluator output supplies its
expected values and the staged C bind remains ahead.

Slice (e1c1) completes the independent translation-cache prerequisite. The author
now retains four FIFO translations keyed by 4 KiB page and the selected 16-bit ASID.
A cache hit rechecks current privilege, SUM and MXR against the cached leaf bits;
software PTE edits remain stale until the appropriate fence. Global status propagates
from non-leaf PTEs, and ASID-selective fences preserve those entries. The four scopes
use register identity, including a nonzero register holding zero. Failed translations
install nothing; Bare and machine-mode accesses bypass the cache.

Hand page-table fixtures check replacement order, permissions, roots, ASIDs, globals,
zero selections and illegal/invalid fences. Thirteen deliberate mutations fail, and
the uncached parent fails the stale-mapping fixture. All 139 historical parcel runs
now reproduce their committed architectural observations, with a cold repeat of the
cache guest's request schedule. All 42 owned records remain byte-identical. The known
incorrect cache guest is the only changed text among 121 earlier word-route outputs;
no production record is overwritten. Staging can now derive C observations and actual
parcel counts independently, after resolving the documentation archive's owned pressure.

Before staging the C corpus, slice (e1d0) repairs the author's provenance headers.
New derivations name the tracked spec-side author and the route actually executed:
word execution or explicit-budget parcel execution. A filename does not establish
which earlier corpus produced a record. The 42 canonical historical word records
keep their exact capture headers; copied names and new parcel derivations receive
new provenance. Generic and compressed examples, schema checks and four deliberate
mutations guard this distinction. No existing expectation record changes.

Slice (e1d1) makes the historical count migration reproducible before adopting it.
The tracked census executes all 139 programs through the independent parcel author,
using each record's already-declared boundary budget. All architectural register
observations match across 4,913 boundaries. The actual request logs total 9,770
parcels; the historical records count 4,888 word requests. Doubling is insufficient:

| Guest | Historical requests | Derived parcels |
| --- | --- | --- |
| dir-runoff | 3 | 5 |
| fault-fetch | 3 | 5 |
| it-prio-jump | 4 | 7 |
| mm-mret | 43 | 85 |
| sv39-straddle | 53 | 104 |

A zero-filled runoff instruction needs one parcel, while a failed translation can
prevent a physical fetch. The census counts the requests that actually occur. It
checks every derived architectural write and reconciles the per-step count with
the complete request log. Its staging manifest fingerprints the source records,
metadata, definitions and producing tools. A changed observation, incorrect extent
or damaged stored count is rejected. Existing production records remain unchanged;
the bind will adopt the derived extent alongside C and its new corpus.

Slice (e1d2) stages 28 new guest programs and their independent observations before
any processor-engine run. They cover all 37 selected compressed forms across 429
declared boundaries and 708 parcel requests. The producer records each budget,
checks hand-derived register values and selected PCs, validates all 28 expectation
schemas, and fingerprints its inputs. Repeating staging is byte-exact. Changing an
observation, request extent or saved budget is rejected.

After the STCE source repair at [.13 c13a2](contract-runtime.md#stce-dependent-pending-and-the-v2-source-contract),
the maintained staging blueprint explicitly enables the comparator, matching the
adopted c-irq body and observations. Its deadline/budget increase by two, saved
PC by eight and retired count by two. Current staging totals are 431 boundaries /
712 parcels; the historical e1d2 totals above describe its original inputs.
Deterministic staging and observation/extent refusal controls still pass.

The programs cover signed and scaled immediate limits, 64-bit shifts, 32-bit
wrap/sign extension, overlapping operands, x0 and hints, compact and stack-relative
integer/D memory, both branch outcomes, backward branches and extreme jumps. The
mixed call returns through C.JALR with its source also serving as the link register;
its saved link is exactly pc+2. A timer interrupts between two compressed
instructions and returns to the saved two-byte boundary. A constrained LR/SC pair
with compressed arithmetic stores the incremented value successfully.

Reserved operands preserve their original sixteen bits in the delivered diagnostic;
C.EBREAK instead takes the breakpoint cause and the declared PC trap value. All four
compressed D memory forms are illegal with FS off before any data access. An
all-ones instruction retains the full ILEN=32 diagnostic, rather than stopping at
its first parcel.

Two translated programs reuse the public Sv39 guest's page tables with execute
permission removed from the second page. A C.NOP in the first page's final halfword
executes with one request; the following boundary faults on the next page. A 32-bit
instruction at that same halfword faults while fetching its required second parcel,
before any instruction effect. Both runs issue 101 physical parcel requests, but
use 52 and 51 declared boundaries respectively. Their trap values name the next
page; the saved instruction PCs distinguish a new fetch from a straddling one.
At (e1d2), production composition and records remained unchanged pending the atomic bind.

Slice (e2a) prepares the production mirror check for that migration. Once C is
composed, it first re-derives every supplied guest's architectural writes and actual
parcel requests. It then changes only the RV64I owner's direct `fetches` field for
comparison. Every other byte, including comments and line endings, remains checked.
The seven historical re-derivations must still differ after count normalization;
a count change alone cannot preserve a stale exception. With C unbound, the original
byte-exact rule still applies. Wrong counts, changed writes, comment/source drift,
textual field lookalikes and stale exceptions have permanent refusing controls.

Slice (e2b) applies the same separation to the 42 historical author-owned records.
With C composed, `--check-owned` regenerates the original word-derived capture text,
then independently executes the fixed budget through the parcel author. Every
architectural write must agree, and the extent must match the actual request log.
Only the direct count changes; capture headers and derivation prose stay exact.
With C unbound, the historical check keeps its original byte-exact route. A default
word-route write to a canonical C-composed record refuses before any output changes;
new authoring requires explicit `--parcels --steps N`, which records that route.


Slice (e2c) binds C in production as one coherent change. The composition is complete:
197 instruction rules plus three counter pseudos, with all 200 spellings exercised.
The 28 staged C programs and their specification-derived records land byte-exact;
the directed corpus grows from 139 to 167. The old records change only their direct
fetch counts, from 4,888 word requests to 9,770 parcels across 4,913 boundaries.
Every other byte and every historical source stays exact. All 139 historical engine
PC/mode/register-write traces also remain byte-identical to the unbound parent;
five public-CLI C controls distinguish that parent from the bound model.

The open v2 contract now includes C's guarantee and exact two-byte physical fetch
supply. Their four positive/negative check IDs are realized, bringing the registry
to 20 checks. Frozen v0/v1 records and pins remain unchanged. All new guests join
the seven-axis matrix; compressed faults and interrupt return replace the earlier
boundary/restart degeneracy. Two other declared degeneracies remain.

Integration exposed two checker gaps and a scope grammar omission. The profile
grammar, its loader and the consistency part-sum now agree on the C family;
good-C and wrong-part controls check the latter. Extraction counts expansions
only after the existing semantic composition validator accepts their base and
operand mappings; absent bases, missing operands and unknown mappings refuse.
The mirror stale-exception control now reaches that predicate with otherwise valid
observations and counts. The Rust checks pass, GUEST-GEN passes 127 controls, and
EXERCISE-COVERAGE reports 200/200. These are finite laboratory results; matched
Sail verification precedes closing `.12`, and CPU-SYSTEM remains incomplete on
its other axes.


Slice (e2d) runs the pinned Sail binary through its public interface over all 28 C
guests. Twenty-seven agree over 412 declared boundaries, with two complete traces
byte-identical for each. Actual Sail instruction rows include all 37 selected C
spellings. The matched set includes C.JALR's old-source link alias, hints, reserved
operands, FS-Off memory, ILEN=32 diagnostics, LR/SC and both translated page-edge
programs. A fresh run with C.LI's expected value changed by one fails at boundary 0.

The remaining guest, `c-irq`, differs at boundary 9: Sail executes C.ADDI while the
laboratory delivers its virtual-time-driven supervisor timer interrupt. The public
reproducer is:

```sh
python3 scripts/probe_gc_sail_timer.py
```

The current corrected reproducer first enables STCE and reads back bit 63,
then sets `stimecmp=0`, reads it back, and reads `mip` at two later boundaries. Sail
returns STIP=0 both times; the laboratory's independent derivation gives STIP=1.
Two fresh reference traces repeat exactly. The public configuration validator refuses
Zicntr without a time source and refuses CLINT in the existing memory map because no
CLINT region is declared. Adding a device would change the selected platform. This
is a measured reference-platform limit with STCE enabled; the committed timer
expectation is retained. The earlier seven-boundary probe left STCE clear,
confounding its laboratory result with the later-discovered overlay defect.
P4.13 c13a1 corrects that probe to ten boundaries and checks STCE read-back
on both independent sides; the earlier observation alone did not establish the cause.

The experiment also exposed an adapter defect: it recognized the historical author’s
interrupt description but not the parcel author’s numeric-cause description. Both
exact spellings now require the matching trace event. Missing/wrong events and an
instruction row at that delivery boundary fail; disabling the new spelling fails the
permanent control. GUEST-GEN passes 128 controls.

These comparisons judge declared GPR changes and witnessed delivery gaps. They do
not independently compare unrecorded PCs, words, FP registers, memory, CSRs or physical
request counts. The trap CSR values read back into GPRs are within the comparison.
The ninth experiment is recorded in the reference dossier; structured experiment and
independence records remain `.14`'s work. Full CI and leaf acceptance follow at (e2e).


Slice (e2e) closes the C leaf after the named full local suite passes: Rust format,
strict Clippy, all tests (153 core, 17 DSP, 193 verification), every doctrine,
the wasm bench, headless bench smoke and all books. The source expansion citations,
compiled mappings/decoder, complete scope/corpus, precise parcel-fault behavior and
public reference results meet the leaf's acceptance. The timer-platform limit remains
explicit. P4 is now 12/18; CPU-SYSTEM remains incomplete, with contract v2 completion
and realization next at `.13`. Closed planning and detailed receipts remain verbatim
in the task-tree archives; this chapter is the current review narrative.

P4.13 c13a1 later re-derives c-irq after explicit STCE setup: its budget is now
19 boundaries / 32 parcels; the timer delivery is at boundary 11. The historical
receipts above retain their original inputs. The owned-author protocol now keeps
41 historical captures plus freshly derived env-irq-sources with a fixed
13-boundary parcel budget; new provenance never borrows a capture header.
[The runtime chapter](contract-runtime.md#explicit-comparator-setup-before-fallback-repair)
records the current nine-program preparation and reference qualifications.
