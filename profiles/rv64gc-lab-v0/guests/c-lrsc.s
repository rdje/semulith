# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.
auipc x8, 0
addi x8, x8, 1024
c.li x9, 5
c.sd x8, x9, 0
lr.d x10, (x8)
c.addi x10, 1
c.li x11, -1
sc.d x11, x10, (x8)
c.ld x12, x8, 0
