addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x3ff00              #: build 0x3ff0000000000001: the upper word 0x3ff00000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 1              #: the lower word 0x00000001. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x5, x5, x28               #: x5 = 0x3ff0000000000001. | RVI-RV32I §1.1.4
fmv.d.x f1, x5
lui x6, 0x3ff00              #: build 0x3feffffffffffffe: the upper word 0x3fefffff first. | RVI-RV32I §1.1.4
addi x6, x6, -1              #: … its low 12 bits (-1). | RVI-RV32I §1.1.4
slli x6, x6, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, -2             #: the lower word 0xfffffffe. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x6, x6, x28               #: x6 = 0x3feffffffffffffe. | RVI-RV32I §1.1.4
fmv.d.x f2, x6
lui x7, 0xbff00              #: build 0xbff0000000000000: the upper word 0xbff00000 first. | RVI-RV32I §1.1.4
slli x7, x7, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f3, x7
fmadd.d f4, f1, f2, f3, 0    #: (1+2^-52)(1-2^-53)-1 with ONE rounding: exact where two roundings would give 0. | RVI-D §21.1.4
fmv.x.d x8, f4
fmsub.d f5, f1, f2, f3, 0
fmv.x.d x9, f5
fnmsub.d f6, f1, f2, f3, 0
fmv.x.d x10, f6
fnmadd.d f7, f1, f2, f3, 0
fmv.x.d x11, f7
csrrs x12, fflags, x0        #: x12 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
lui x13, 0x7ff00             #: build 0x7ff0000000000000: the upper word 0x7ff00000 first. | RVI-RV32I §1.1.4
slli x13, x13, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f8, x13
fmv.d.x f9, x0               #: +0.0. | RVI-D §21.1.5
lui x14, 0x7ff80             #: build 0x7ff8000000000000: the upper word 0x7ff80000 first. | RVI-RV32I §1.1.4
slli x14, x14, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f10, x14
fmadd.d f11, f8, f9, f10, 0  #: ∞×0 + a quiet NaN: INVALID even with the quiet addend. | RVI-F §20.1.6
fmv.x.d x15, f11
csrrs x16, fflags, x0        #: x16 = the accrued flags so far. | RVI-F §20.1.2 #|end
