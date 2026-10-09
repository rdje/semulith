# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.
c.li x8, 2
loop: c.addi x8, -1
c.bnez x8, loop
c.mv x9, x8
