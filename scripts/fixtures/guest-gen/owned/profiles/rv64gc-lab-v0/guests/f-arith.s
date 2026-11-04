addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x3f800              #: build the pattern 0x3f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f1, x5
lui x6, 0x40400              #: build the pattern 0x40400000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f2, x6
fdiv.s f3, f1, f2, 0
fmv.x.w x7, f3
csrrs x8, fflags, x0         #: x8 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
fdiv.s f4, f1, f2, 1
fmv.x.w x9, f4
fdiv.s f4, f1, f2, 3
fmv.x.w x10, f4
fadd.s f5, f1, f2, 0
fmv.x.w x11, f5
fsub.s f6, f1, f2, 2
fmv.x.w x12, f6
fmul.s f7, f2, f2, 4
fmv.x.w x13, f7
csrrs x14, fflags, x0        #: x14 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
fsqrt.s f8, f2, 0
fmv.x.w x15, f8
fsqrt.s f8, f2, 3
fmv.x.w x16, f8
csrrs x17, fflags, x0        #: x17 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x18, 0x7f800             #: build the pattern 0x7f7fffff (upper 20 bits). | RVI-RV32I §1.1.4
addi x18, x18, -1            #: … its low 12 bits (-1). | RVI-RV32I §1.1.4
fmv.w.x f9, x18
fadd.s f10, f9, f9, 1        #: MAX+MAX in RTZ: clamped to MAX — and STILL an overflow (the unbounded rounding exceeds MAX). | IEEE 754-2008 §7.4; RVI-F §20.1.6
fmv.x.w x19, f10
csrrs x20, fflags, x0        #: x20 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
fdiv.s f11, f1, f0, 0        #: 1 ÷ f0 — f0 unboxes to the canonical NaN, so the result is NaN, no flag. | RVI-D §21.1.2
fmv.x.w x21, f11
fmv.w.x f12, x0              #: f12 = +0.0. | RVI-F §20.1.7
fdiv.s f13, f1, f12, 0       #: 1 ÷ +0: +∞, divide-by-zero. | RVI-F §20.1.6
fmv.x.w x22, f13
csrrs x23, fflags, x0        #: x23 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
fsqrt.s f14, f5, 0
fmv.x.w x24, f14
lui x25, 0xbf800             #: build the pattern 0xbf800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f15, x25
fsqrt.s f16, f15, 0          #: √−1: invalid — the canonical NaN, NV. | RVI-F §20.1.6
fmv.x.w x26, f16
csrrs x27, fflags, x0        #: x27 = the accrued flags so far. | RVI-F §20.1.2 #|end
