addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0xfff00              #: build 0xfff0000000000000: the upper word 0xfff00000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
fclass.d x6, f1
lui x5, 0xbff00              #: build 0xbff0000000000000: the upper word 0xbff00000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
fclass.d x7, f1
lui x5, 0x80100              #: build 0x800fffffffffffff: the upper word 0x800fffff first. | RVI-RV32I §1.1.4
addi x5, x5, -1              #: … its low 12 bits (-1). | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, -1             #: the lower word 0xffffffff. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x5, x5, x28               #: x5 = 0x800fffffffffffff. | RVI-RV32I §1.1.4
fmv.d.x f1, x5
fclass.d x8, f1
lui x5, 0x80000              #: build 0x8000000000000000: the upper word 0x80000000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
fclass.d x9, f1
addi x5, x0, 0               #: build 0x0000000000000000: the upper word 0x00000000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
fclass.d x10, f1
lui x5, 0x100                #: build 0x000fffffffffffff: the upper word 0x000fffff first. | RVI-RV32I §1.1.4
addi x5, x5, -1              #: … its low 12 bits (-1). | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, -1             #: the lower word 0xffffffff. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x5, x5, x28               #: x5 = 0x000fffffffffffff. | RVI-RV32I §1.1.4
fmv.d.x f1, x5
fclass.d x11, f1
lui x5, 0x3ff00              #: build 0x3ff0000000000000: the upper word 0x3ff00000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
fclass.d x12, f1
lui x5, 0x7ff00              #: build 0x7ff0000000000000: the upper word 0x7ff00000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
fclass.d x13, f1
lui x5, 0x7ff40              #: build 0x7ff4000000000123: the upper word 0x7ff40000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 291            #: the lower word 0x00000123. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x5, x5, x28               #: x5 = 0x7ff4000000000123. | RVI-RV32I §1.1.4
fmv.d.x f1, x5
fclass.d x14, f1
lui x5, 0x7ff80              #: build 0x7ff8000000000000: the upper word 0x7ff80000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
fclass.d x15, f1
csrrs x16, fflags, x0        #: x16 = the accrued flags so far. | RVI-F §20.1.2 #|end
