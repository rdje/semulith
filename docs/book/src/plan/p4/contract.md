# P4.9 — The environment contract, version 1

**Status:** Underway (slices a–c, 2026-10-06)

The processor model does not stand alone: it relies on its environment — memory that
answers reads and writes, page tables that can be walked, a supply of time, events that may
arrive. The *contract* writes those relationships down as numbered obligations: what the
processor guarantees, and what it assumes. This leaf adds the assumptions the Linux-capable
profile introduced — how address translation reads its tables, where interrupts come from,
how counters advance, and what may invalidate a load-reserved reservation — and it does so
as a new *version*, without rewriting the old one.

Slice (a) made "a version" mean something checkable. Until now the version number was just a
label repeated on every obligation; nothing said which obligations made up version 0, and
seven earlier steps had added to it. A contract document now lists each version's members,
version 0 is recorded exactly as it stands and frozen — every obligation's text pinned by a
hash — and a new gate refuses any change to a frozen obligation. A statement that turns out to
be wrong is replaced in the next version; the old one stays on the record.

Slice (b) wrote version 1's four assumptions — the first things this processor's contract
*assumes* of its environment rather than promises: page tables are read from the same memory
the processor writes, and never written behind its back; this laboratory supplies no
interrupt sources of its own (the timer interrupt comes from the processor's own comparison);
time advances exactly one tick per step, even while the processor waits; and nothing outside
the processor ever cancels a load-reserved reservation. Each assumption has a test that shows
it holding and a test that shows what breaking it would look like, and a registry runs them
all on every build.

Slice (c) put the versioning to its first real use. Two version-0 statements had become
wrong as the processor grew — one still described the wait-for-interrupt instruction and the
translation-cache flush as doing nothing, another still said environment calls stop the run
— and version 1 replaces them with correct statements while the originals stay, frozen, on
the record, each replacement saying what it replaces and why.
