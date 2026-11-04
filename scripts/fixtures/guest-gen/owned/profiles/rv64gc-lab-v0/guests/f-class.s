addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0xff800              #: build the pattern 0xff800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f1, x5
fclass.s x6, f1
lui x5, 0xbf800              #: build the pattern 0xbf800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f2, x5
fclass.s x7, f2
lui x5, 0x80000              #: build the pattern 0x80000001 (upper 20 bits). | RVI-RV32I §1.1.4
addi x5, x5, 1               #: … its low 12 bits (1). | RVI-RV32I §1.1.4
fmv.w.x f3, x5
fclass.s x8, f3
lui x5, 0x80000              #: build the pattern 0x80000000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f4, x5
fclass.s x9, f4
addi x5, x0, 0               #: the pattern 0x0. | RVI-RV32I §1.1.4
fmv.w.x f5, x5
fclass.s x10, f5
addi x5, x0, 1               #: the pattern 0x1. | RVI-RV32I §1.1.4
fmv.w.x f6, x5
fclass.s x11, f6
lui x5, 0x3f800              #: build the pattern 0x3f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f7, x5
fclass.s x12, f7
lui x5, 0x7f800              #: build the pattern 0x7f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f8, x5
fclass.s x13, f8
lui x5, 0x7fa00              #: build the pattern 0x7fa00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f9, x5
fclass.s x14, f9
lui x5, 0x7fc00              #: build the pattern 0x7fc00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f10, x5
fclass.s x15, f10
csrrs x16, fflags, x0        #: x16 = the accrued flags so far. | RVI-F §20.1.2 #|end
