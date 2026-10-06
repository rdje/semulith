addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
fmv.w.x f1, x0               #: f1 = +0.0. | RVI-F §20.1.7
lui x5, 0x80000              #: build the pattern 0x80000000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f2, x5
fmin.s f3, f1, f2            #: −0.0 < +0.0 for these instructions only: min is −0. | RVI-F §20.1.6
fmv.x.w x6, f3
fmax.s f4, f2, f1
fmv.x.w x7, f4
lui x8, 0x7fc00              #: build the pattern 0x7fc00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f5, x8
lui x9, 0x3f800              #: build the pattern 0x3f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f6, x9
fmin.s f7, f5, f6            #: one NaN: the other operand. | RVI-F §20.1.6
fmv.x.w x10, f7
csrrs x11, fflags, x0        #: x11 = the accrued flags so far. | RVI-F §20.1.2
lui x12, 0x7fa00             #: build the pattern 0x7fa00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f8, x12
fmax.s f9, f6, f8            #: a signaling NaN input: NV even though the result (1.0) is not NaN. | RVI-F §20.1.6
fmv.x.w x13, f9
csrrs x14, fflags, x0        #: x14 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
fmin.s f10, f5, f8           #: both NaN: the canonical NaN (and NV — one is signaling). | RVI-F §20.1.6
fmv.x.w x15, f10
csrrs x16, fflags, x0        #: x16 = the accrued flags so far. | RVI-F §20.1.2 #|end
