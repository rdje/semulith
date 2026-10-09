# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.
c.li x8, 0
c.beqz x8, zero
addi x9, x0, 99
zero: c.li x9, 1
c.bnez x9, one
addi x10, x0, 99
one: c.bnez x8, finish
c.beqz x9, finish
c.li x10, 7
finish: c.nop
