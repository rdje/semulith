# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.
auipc x2, 0
addi x2, x2, 1536
c.addi4spn x8, 16
c.li x9, -32
c.sw x8, x9, 124
c.lw x10, x8, 124
c.sd x8, x9, 248
c.ld x11, x8, 248
c.swsp x9, 252
c.lwsp x1, 252
c.sdsp x9, 504
c.ldsp x3, 504
addi x5, x0, 3
slli x5, x5, 13
csrrs x0, mstatus, x5
fmv.d.x f9, x9
c.fsd x8, f9, 248
c.fld f8, x8, 248
fmv.x.d x12, f8
c.fsdsp f9, 504
c.fldsp f1, 504
fmv.x.d x13, f1
