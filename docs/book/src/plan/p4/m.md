# P4.11 — Integer multiply and divide (M)

**Status:** Landed and closed (a–d, 2026-10-06)

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

Slice (b) bound M into the processor. Four new test programs exercise all 13 instructions:
mixed signs, the most negative number, division by zero, overflow, the 32-bit forms with junk
in their upper halves, and results written to the always-zero register. Their expected results
were worked out from the specification with exact arithmetic and fingerprinted *before* the
processor could execute M at all. The processor then matched all of them on its first run.
Every one of the 135 older programs produced byte-for-byte the same trace as before, while the
four new ones fail on the previous version, as they should.

Three small problems surfaced along the way, and each was fixed. The tool that works out
expected results would have mistaken multiply for subtract. A few expected results landed in
registers that already held zero, so they proved nothing; marker values now go in first. And
some of the gate report's own self-checks had baked in today's numbers, so they broke as soon
as the contract grew; they now check how a number changes rather than its exact value. The
profile's files also outgrew their size budget, because every new extension adds evidence; a
recorded decision raised the budget a little and proposed a cleaner long-term rule.

Slice (c1) added breadth. A program works out the expected result of every M instruction over
4,485 operand combinations, using exact arithmetic and Table 1's special cases written out by
name, and each one is run through the processor model as a real instruction. A new gate, the
project's 38th rule, refuses the table if anyone edits it by hand. It also checks the program
against the rules the specification itself states, such as "dividend = divisor × quotient +
remainder" and the remainder taking the dividend's sign, so a wrong reference cannot quietly
produce a wrong table.

Slice (c2) ran the four M programs on Sail, the reference RISC-V model, as well. All four
agreed, every value at every step. For integer arithmetic this comparison is genuinely
independent, because the two share no code; that was not true of the floating-point
comparison. The comparison was also shown to catch mistakes: one planted wrong answer was
caught at the exact step.

**The leaf is closed (2026-10-06).** All 13 M instructions are part of the processor model. Each
is exercised by test programs whose expected results were fixed before the processor could run
them, and each was checked on both the project's engine and Sail, with division by zero and
overflow covered at both 64 and 32 bits. On the gate's scoreboard, the "complete profile" axis
now has one gap left: the compressed instructions, which are the next leaf.
