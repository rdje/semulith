addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x3f800              #: build the pattern 0x3f800001 (upper 20 bits). | RVI-RV32I §1.1.4
addi x5, x5, 1               #: … its low 12 bits (1). | RVI-RV32I §1.1.4
fmv.w.x f1, x5
lui x6, 0x3f800              #: build the pattern 0x3f7ffffe (upper 20 bits). | RVI-RV32I §1.1.4
addi x6, x6, -2              #: … its low 12 bits (-2). | RVI-RV32I §1.1.4
fmv.w.x f2, x6
lui x7, 0xbf800              #: build the pattern 0xbf800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f3, x7
fmadd.s f4, f1, f2, f3, 0    #: (1+2^-23)(1-2^-23) + (-1) = -2^-46 exactly — fused, ONE rounding (an unfused product would round to 1 and give 0). | RVI-F §20.1.6
fmv.x.w x8, f4
fmsub.s f5, f1, f2, f3, 0
fmv.x.w x9, f5
fnmsub.s f6, f1, f2, f3, 0
fmv.x.w x10, f6
fnmadd.s f7, f1, f2, f3, 0
fmv.x.w x11, f7
csrrs x12, fflags, x0        #: x12 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x13, 0x7f800             #: build the pattern 0x7f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f8, x13
fmv.w.x f9, x0               #: f9 = +0.0. | RVI-F §20.1.7
lui x14, 0x7fc00             #: build the pattern 0x7fc00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f10, x14
fmadd.s f11, f8, f9, f10, 0  #: ∞×0 + qNaN: NV even with the quiet addend. | RVI-F §20.1.6
fmv.x.w x15, f11
csrrs x16, fflags, x0        #: x16 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x17, 0x40000             #: build the pattern 0x40000000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f12, x17
lui x18, 0x40400             #: build the pattern 0x40400000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f13, x18
fnmadd.s f14, f12, f13, f12, 2
fmv.x.w x19, f14
fmsub.s f15, f12, f12, f12, 0
fmv.x.w x20, f15
fmsub.s f15, f9, f12, f9, 2  #: 0×2 − (+0) in RDN: the exact zero sum takes −0 — 'RDN' is the one mode that rounds a cancellation to −0. | IEEE 754-2008 §6.3
fmv.x.w x21, f15
csrrs x22, fflags, x0        #: x22 = the accrued flags so far. | RVI-F §20.1.2 #|end
