# P4.8 — Faults, restart and partial progress

**Status:** Underway (slice a, 2026-10-06)

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
