# P4.8 — Faults, restart and partial progress

**Status:** Landed and closed (a–e, 2026-10-06)

An instruction can do several things — read a register, access memory, update a control
register, write its result. If something goes wrong part-way, what must the machine look
like afterwards? The specification leaves that to the execution environment, recommending
that traps be *precise*; this laboratory chose precise: **every instruction completes or
faults as a unit**, so a trapping instruction leaves the architectural state as it found
it, apart from the trap report itself. Reads that already reached memory (an address
translation's table walk, the first half of an instruction fetch that crosses a page) are
not undone — they are declared, not hidden. This leaf checks that discipline everywhere,
declares the priority among simultaneous faults, and builds a way to inject a fault at a
chosen step of an instruction.

The design work started by measuring where the engine could break the rule, and found one
place that did. The control-register instructions read the old value into the destination
register *and then* attempted the write — so writing to a read-only register (such as the
hart's ID) trapped *after* the destination register had already changed. The Sail reference
model traps without touching it.

Slice (a) fixed that at the root: the language gained one atomic read-and-write operation,
which judges both halves before anything reaches the destination register. A new test
program tries every writing form against the read-only hart ID: each traps with its
destination untouched, and Sail agrees step for step. A second program does the same
against the counters; Sail cannot run that one under the matched configuration (it has no
time source there, so the counters do not exist), and that limit is recorded rather than
fitted. Two stale texts and one unreachable wrong cause code were corrected on the way.

Slice (b) wrote down which fault wins when one instruction could raise several. The
specification gives a fixed order — fetch problems first, then illegal instructions, then
(at one position the implementation may choose) misalignment, then address-translation
faults, then the physical access — and this laboratory takes misalignment early, before
translation. A new test program builds page tables so that one instruction at a time meets
two problems at once; every case resolves as declared, and Sail agrees on all of them.

Slice (c) built the means to break things on purpose. A test program can now declare regions
of memory the environment refuses — not readable, not writable, page tables not walkable — and
the engine and the specification-side model both answer a refused access as a fault. The
first program to use it shows the leaf's central case: an atomic memory operation whose read
succeeds and whose write is refused traps without changing its destination register or memory.

Slice (d) used it across every instruction that does more than one thing at the memory
boundary: load-reserved and store-conditional, the atomic operations (with either half
refused), the floating-point loads and stores, and an address-translation walk refused at
each of its three levels. In every case the instruction faults cleanly — no register, no
memory, no floating-point status changes — and the reads that already happened are declared
rather than pretended away. The processor's contract now states this as an obligation.

**The leaf is closed (2026-10-06).** On the Sail reference model, the programs it can run
agree step for step; it cannot run the injected ones as designed — it has no way to refuse an
access — and each of those diverges exactly at its first refused access, which is recorded
rather than hidden. Faults, their priority and their restart are now part of the processor's
declared and tested behaviour.
