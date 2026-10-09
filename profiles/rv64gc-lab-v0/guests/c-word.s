# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.
lui x8, 524288
addi x8, x8, -1
c.li x9, 1
c.addw x8, x9
c.subw x8, x9
c.addiw x8, 1
c.addiw x8, 0
c.addiw x8, -32
c.addw x9, x9
c.subw x9, x9
