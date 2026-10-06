addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
addi x5, x0, 1               #: 1. | RVI-RV32I §1.1.4
fcvt.d.w f1, x5, 0           #: 1.0, exactly. | RVI-D §21.1.5
addi x6, x0, 3               #: 3. | RVI-RV32I §1.1.4
fcvt.d.w f2, x6, 0           #: 3.0, exactly. | RVI-D §21.1.5
fdiv.d f3, f1, f2, 0         #: 1/3 in RNE: inexact. | RVI-D §21.1.4
fmv.x.d x7, f3
fdiv.d f4, f1, f2, 3         #: 1/3 in RUP: one ulp above RNE's result. | RVI-D §21.1.4
fmv.x.d x8, f4
fadd.d f5, f1, f2, 0
fmv.x.d x9, f5
fsub.d f6, f1, f1, 2         #: 1-1 in RDN: the exact zero is -0. | RVI-D §21.1.4
fmv.x.d x10, f6
addi x11, x0, 2              #: 2. | RVI-RV32I §1.1.4
fcvt.d.w f7, x11, 0
fsqrt.d f8, f7, 0            #: the square root of 2 in RNE. | RVI-D §21.1.4
fmv.x.d x12, f8
csrrs x13, fflags, x0        #: x13 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x14, 0x7ff00             #: build 0x7fefffffffffffff: the upper word 0x7fefffff first. | RVI-RV32I §1.1.4
addi x14, x14, -1            #: … its low 12 bits (-1). | RVI-RV32I §1.1.4
slli x14, x14, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, -1             #: the lower word 0xffffffff. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x14, x14, x28             #: x14 = 0x7fefffffffffffff. | RVI-RV32I §1.1.4
fmv.d.x f9, x14
fmul.d f10, f9, f7, 1        #: MAX×2 in RTZ: clamped to MAX — and an OVERFLOW (the magnitude rule). | RVI-D §21.1.4
fmv.x.d x15, f10
csrrs x16, fflags, x0        #: x16 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
addi x17, x0, 0              #: build 0x0000000000000001: the upper word 0x00000000 first. | RVI-RV32I §1.1.4
slli x17, x17, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 1              #: the lower word 0x00000001. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x17, x17, x28             #: x17 = 0x0000000000000001. | RVI-RV32I §1.1.4
fmv.d.x f11, x17
lui x18, 0x3fe00             #: build 0x3fe0000000000000: the upper word 0x3fe00000 first. | RVI-RV32I §1.1.4
slli x18, x18, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f12, x18
fmul.d f13, f11, f12, 0      #: min subnormal × 0.5: a tie to the even zero — tiny and inexact, an UNDERFLOW. | RVI-D §21.1.4
fmv.x.d x19, f13
csrrs x20, fflags, x0        #: x20 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
fmv.d.x f14, x0              #: +0.0. | RVI-D §21.1.5
fdiv.d f15, f1, f14, 0       #: 1/+0: +∞ and DIVIDE-BY-ZERO. | RVI-D §21.1.4
fmv.x.d x21, f15
lui x22, 0x7ff40             #: build 0x7ff4000000000123: the upper word 0x7ff40000 first. | RVI-RV32I §1.1.4
slli x22, x22, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 291            #: the lower word 0x00000123. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x22, x22, x28             #: x22 = 0x7ff4000000000123. | RVI-RV32I §1.1.4
fmv.d.x f16, x22
fadd.d f17, f16, f1, 0       #: a signaling-NaN operand: the canonical NaN and INVALID. | RVI-F §20.1.3
fmv.x.d x23, f17
csrrs x24, fflags, x0        #: x24 = the accrued flags so far. | RVI-F §20.1.2 #|end
