# P4.11 — Integer multiply and divide (M)

**Status:** Underway (slice a, 2026-10-06)

The Linux-capable profile includes M, the standard extension for integer multiplication and
division, but until this leaf the processor model could not execute it. The instruction
encodings were already on file. What to *do* for each of the 13 instructions was not, and the
semantics language had no way to say "multiply" or "divide".

Division needs care because of two awkward cases. RISC-V never traps on division. Dividing by
zero gives a fixed answer: a quotient with every bit set, and a remainder equal to the number
being divided. Dividing the most negative number by −1 overflows, and gives that same number
back with a remainder of zero. Other processors make different choices, often a trap. So the
language's new operators are plain arithmetic, and they leave division by zero undefined. Each
RISC-V rule states, in its own text, what division by zero yields, quoting the specification.
A checker refuses any division that isn't protected by such a statement.

Slice (a) added the eight operators, the 13 rules, the generator support and the checker rule,
plus the arithmetic itself as a small, separately tested module. Its tests compare against
independent methods: a long-multiplication by hand for the high halves, the identities the
specification states for division, and the host's own 32-bit arithmetic for the word-sized
forms. Two deliberately broken versions were each caught.
