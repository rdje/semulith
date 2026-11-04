addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x3f800              #: build the pattern 0x3f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f1, x5
lui x6, 0x40000              #: build the pattern 0x40000000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f2, x6
addi x7, x0, 7               #: preload so a 0 result is a visible write. | RVI-RV32I §1.1.4
feq.s x7, f1, f2
flt.s x8, f1, f2
fle.s x9, f2, f1
fmv.w.x f3, x0               #: +0.0. | RVI-F §20.1.7
lui x10, 0x80000             #: build the pattern 0x80000000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f4, x10
feq.s x11, f3, f4            #: −0.0 = +0.0 for a compare. | RVI-F §20.1.8
csrrs x12, fflags, x0        #: x12 = the accrued flags so far. | RVI-F §20.1.2
lui x13, 0x7fc00             #: build the pattern 0x7fc00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f5, x13
addi x14, x0, 7              #: preload. | RVI-RV32I §1.1.4
feq.s x14, f5, f1            #: FEQ is quiet: a quiet NaN gives 0 and NO flag. | RVI-F §20.1.8
csrrs x15, fflags, x0        #: x15 = the accrued flags so far. | RVI-F §20.1.2
flt.s x16, f5, f1            #: FLT is signaling: a quiet NaN raises NV. | RVI-F §20.1.8
csrrs x17, fflags, x0        #: x17 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x18, 0x7fa00             #: build the pattern 0x7fa00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f6, x18
feq.s x19, f6, f6            #: FEQ with a signaling NaN: NV. | RVI-F §20.1.8
csrrs x20, fflags, x0        #: x20 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
fle.s x21, f1, f5
csrrs x22, fflags, x0        #: x22 = the accrued flags so far. | RVI-F §20.1.2 #|end
