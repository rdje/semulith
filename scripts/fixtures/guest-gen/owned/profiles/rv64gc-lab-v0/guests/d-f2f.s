addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x3fd55              #: build 0x3fd5555555555555: the upper word 0x3fd55555 first. | RVI-RV32I §1.1.4
addi x5, x5, 1365            #: … its low 12 bits (1365). | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
lui x28, 0x55555             #: the lower word 0x55555555. | RVI-RV32I §1.1.4
addi x28, x28, 1365          #: … its low 12 bits (1365). | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x5, x5, x28               #: x5 = 0x3fd5555555555555. | RVI-RV32I §1.1.4
fmv.d.x f1, x5
fcvt.s.d f2, f1, 0           #: 1/3 to single in RNE: inexact, NaN-boxed. | RVI-D §21.1.5
fmv.x.d x6, f2
fcvt.s.d f3, f1, 1           #: … in RTZ: truncated — one ulp below RNE's (which rounded up). | RVI-D §21.1.5
fmv.x.d x7, f3
csrrs x8, fflags, x0         #: x8 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x9, 0x7ff00              #: build 0x7fefffffffffffff: the upper word 0x7fefffff first. | RVI-RV32I §1.1.4
addi x9, x9, -1              #: … its low 12 bits (-1). | RVI-RV32I §1.1.4
slli x9, x9, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, -1             #: the lower word 0xffffffff. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x9, x9, x28               #: x9 = 0x7fefffffffffffff. | RVI-RV32I §1.1.4
fmv.d.x f4, x9
fcvt.s.d f5, f4, 1           #: double MAX to single in RTZ: clamped to the single MAX — an OVERFLOW. | RVI-D §21.1.5
fmv.x.d x10, f5
csrrs x11, fflags, x0        #: x11 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x12, 0x38100             #: build 0x380fffffe0000000: the upper word 0x380fffff first. | RVI-RV32I §1.1.4
addi x12, x12, -1            #: … its low 12 bits (-1). | RVI-RV32I §1.1.4
slli x12, x12, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
lui x28, 0xe0000             #: the lower word 0xe0000000. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x12, x12, x28             #: x12 = 0x380fffffe0000000. | RVI-RV32I §1.1.4
fmv.d.x f6, x12
fcvt.s.d f7, f6, 0           #: 2^-126·(1-2^-24): tiny unbounded, rounds up to the smallest normal — still an UNDERFLOW. | RVI-D §21.1.5
fmv.x.d x13, f7
csrrs x14, fflags, x0        #: x14 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x15, 0x7ff40             #: build 0x7ff4000000000123: the upper word 0x7ff40000 first. | RVI-RV32I §1.1.4
slli x15, x15, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 291            #: the lower word 0x00000123. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x15, x15, x28             #: x15 = 0x7ff4000000000123. | RVI-RV32I §1.1.4
fmv.d.x f8, x15
fcvt.s.d f9, f8, 0           #: a signaling NaN narrowed: the canonical single, boxed — and INVALID. | RVI-D §21.1.5
fmv.x.d x16, f9
csrrs x17, fflags, x0        #: x17 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x18, 0x3dccd             #: build the pattern 0x3dcccccd (upper 20 bits). | RVI-RV32I §1.1.4
addi x18, x18, -819          #: … its low 12 bits (-819). | RVI-RV32I §1.1.4
fmv.w.x f10, x18
fcvt.d.s f11, f10, 0         #: a boxed single widened: exact, no flag. | RVI-D §21.1.5
fmv.x.d x19, f11
fcvt.d.s f12, f1, 0          #: a register holding a DOUBLE is not a boxed single: it unboxes to the canonical NaN — no flag. | RVI-D §21.1.2
fmv.x.d x20, f12
lui x21, 0x7fa00             #: build the pattern 0x7fa00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f13, x21
fcvt.d.s f14, f13, 0         #: a signaling single widened: the canonical double — and INVALID. | RVI-D §21.1.5
fmv.x.d x22, f14
csrrs x23, fflags, x0        #: x23 = the accrued flags so far. | RVI-F §20.1.2 #|end
