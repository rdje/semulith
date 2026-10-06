addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
fmv.d.x f1, x0               #: f1 = +0.0. | RVI-D §21.1.5
lui x5, 0x80000              #: build 0x8000000000000000: the upper word 0x80000000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f2, x5
fmin.d f3, f1, f2            #: min(+0, -0) = -0. | RVI-D §21.1.4
fmv.x.d x6, f3
fmax.d f4, f2, f1            #: max(-0, +0) = +0. | RVI-D §21.1.4
fmv.x.d x7, f4
lui x8, 0x7ff80              #: build 0x7ff8000000000000: the upper word 0x7ff80000 first. | RVI-RV32I §1.1.4
slli x8, x8, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f5, x8
lui x9, 0x3ff00              #: build 0x3ff0000000000000: the upper word 0x3ff00000 first. | RVI-RV32I §1.1.4
slli x9, x9, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f6, x9
fmin.d f7, f5, f6            #: one quiet NaN: the other operand, no flag. | RVI-D §21.1.4
fmv.x.d x10, f7
csrrs x11, fflags, x0        #: x11 = the accrued flags so far. | RVI-F §20.1.2
lui x12, 0x7ff40             #: build 0x7ff4000000000123: the upper word 0x7ff40000 first. | RVI-RV32I §1.1.4
slli x12, x12, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 291            #: the lower word 0x00000123. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x12, x12, x28             #: x12 = 0x7ff4000000000123. | RVI-RV32I §1.1.4
fmv.d.x f8, x12
fmax.d f9, f8, f6            #: a signaling NaN: the other operand — and INVALID. | RVI-D §21.1.4
fmv.x.d x13, f9
fmin.d f10, f5, f8           #: two NaNs: the canonical NaN. | RVI-D §21.1.4
fmv.x.d x14, f10
csrrs x15, fflags, x0        #: x15 = the accrued flags so far. | RVI-F §20.1.2 #|end
