addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x40491              #: build the pattern 0x40490fdb (upper 20 bits). | RVI-RV32I §1.1.4
addi x5, x5, -37             #: … its low 12 bits (-37). | RVI-RV32I §1.1.4
fmv.w.x f1, x5
lui x6, 0xbf800              #: build the pattern 0xbf800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f2, x6
fsgnj.s f3, f1, f2
fmv.x.w x7, f3
fsgnjn.s f4, f1, f2
fmv.x.w x8, f4
fsgnjx.s f5, f3, f2
fmv.x.w x9, f5
fsgnjn.s f6, f2, f2          #: the FNEG.S spelling (rs2 = rs1). | RVI-F §20.1.7
fmv.x.w x10, f6
fsgnjx.s f7, f2, f2          #: the FABS.S spelling. | RVI-F §20.1.7
fmv.x.w x11, f7
lui x12, 0xffa00             #: build the pattern 0xffa00123 (upper 20 bits). | RVI-RV32I §1.1.4
addi x12, x12, 291           #: … its low 12 bits (291). | RVI-RV32I §1.1.4
fmv.w.x f8, x12
fsgnjx.s f9, f8, f8          #: the absolute value of a signaling NaN: the payload kept, the sign cleared — no flag, no canonical NaN. | RVI-F §20.1.7
fmv.x.w x13, f9
csrrs x14, fflags, x0        #: x14 = the accrued flags so far. | RVI-F §20.1.2 #|end
