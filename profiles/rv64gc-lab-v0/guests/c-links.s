# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.
auipc x1, 0
addi x1, x1, 14
c.jalr x1
c.j after
.half 0
sub: c.addi x10, 1
c.jr x1
after: c.mv x11, x1
addi x12, x0, 7
c.j finish
.half 0
finish: c.nop
