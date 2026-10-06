addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x3ff00              #: build 0x3ff0000000000000: the upper word 0x3ff00000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
lui x6, 0x40000              #: build 0x4000000000000000: the upper word 0x40000000 first. | RVI-RV32I §1.1.4
slli x6, x6, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f2, x6
feq.d x7, f1, f1
flt.d x8, f1, f2
fle.d x9, f2, f1
fmv.d.x f3, x0               #: +0.0. | RVI-D §21.1.5
lui x10, 0x80000             #: build 0x8000000000000000: the upper word 0x80000000 first. | RVI-RV32I §1.1.4
slli x10, x10, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f4, x10
feq.d x11, f3, f4            #: +0 = -0. | RVI-D §21.1.6
csrrs x12, fflags, x0        #: x12 = the accrued flags so far. | RVI-F §20.1.2
lui x13, 0x7ff80             #: build 0x7ff8000000000000: the upper word 0x7ff80000 first. | RVI-RV32I §1.1.4
slli x13, x13, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f5, x13
feq.d x14, f5, f1            #: a quiet NaN: 0 and no flag — FEQ is quiet. | RVI-D §21.1.6
csrrs x15, fflags, x0        #: x15 = the accrued flags so far. | RVI-F §20.1.2
flt.d x16, f5, f1            #: a quiet NaN: 0 and INVALID — FLT is signaling. | RVI-D §21.1.6
csrrs x17, fflags, x0        #: x17 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x18, 0x7ff40             #: build 0x7ff4000000000123: the upper word 0x7ff40000 first. | RVI-RV32I §1.1.4
slli x18, x18, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 291            #: the lower word 0x00000123. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x18, x18, x28             #: x18 = 0x7ff4000000000123. | RVI-RV32I §1.1.4
fmv.d.x f6, x18
feq.d x19, f6, f1            #: a signaling NaN: INVALID even for FEQ. | RVI-D §21.1.6
csrrs x20, fflags, x0        #: x20 = the accrued flags so far. | RVI-F §20.1.2 #|end
