# P4.9 — The environment contract, version 1

**Status:** Underway (slice a, 2026-10-06)

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
