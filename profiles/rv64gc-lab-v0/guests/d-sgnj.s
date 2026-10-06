addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x40092              #: build 0x400921fb54442d18: the upper word 0x400921fb first. | RVI-RV32I §1.1.4
addi x5, x5, 507             #: … its low 12 bits (507). | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
lui x28, 0x54443             #: the lower word 0x54442d18. | RVI-RV32I §1.1.4
addi x28, x28, -744          #: … its low 12 bits (-744). | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x5, x5, x28               #: x5 = 0x400921fb54442d18. | RVI-RV32I §1.1.4
fmv.d.x f1, x5
lui x6, 0xbff00              #: build 0xbff0000000000000: the upper word 0xbff00000 first. | RVI-RV32I §1.1.4
slli x6, x6, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f2, x6
fsgnj.d f3, f1, f2
fmv.x.d x7, f3
fsgnjn.d f4, f1, f2
fmv.x.d x8, f4
fsgnjx.d f5, f3, f2
fmv.x.d x9, f5
fsgnjn.d f6, f2, f2          #: the FNEG.D spelling (rs2 = rs1). | RVI-D §21.1.5
fmv.x.d x10, f6
fsgnjx.d f7, f2, f2          #: the FABS.D spelling. | RVI-D §21.1.5
fmv.x.d x11, f7
lui x12, 0xfff40             #: build 0xfff4000000000123: the upper word 0xfff40000 first. | RVI-RV32I §1.1.4
slli x12, x12, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 291            #: the lower word 0x00000123. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x12, x12, x28             #: x12 = 0xfff4000000000123. | RVI-RV32I §1.1.4
fmv.d.x f8, x12
fsgnjx.d f9, f8, f8          #: the absolute value of a signaling NaN: the payload kept, the sign cleared — no flag, no canonical NaN. | RVI-D §21.1.5
fmv.x.d x13, f9
csrrs x14, fflags, x0        #: x14 = the accrued flags so far. | RVI-F §20.1.2 #|end
