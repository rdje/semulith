addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x40040              #: build 0x4004000000000000: the upper word 0x40040000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f1, x5
fcvt.w.d x6, f1, 0           #: 2.5 in RNE: 2 (ties to even), NX. | RVI-D §21.1.5
fcvt.w.d x7, f1, 4           #: 2.5 in RMM: 3. | RVI-D §21.1.5
lui x8, 0xbff00              #: build 0xbff0000000000000: the upper word 0xbff00000 first. | RVI-RV32I §1.1.4
slli x8, x8, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f2, x8
fcvt.wu.d x9, f2, 1          #: -1.0 to unsigned: out of range — 0 and INVALID. | RVI-D §21.1.5
lui x10, 0x43e00             #: build 0x43e0000000000000: the upper word 0x43e00000 first. | RVI-RV32I §1.1.4
slli x10, x10, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f3, x10
fcvt.l.d x11, f3, 0          #: 2^63 to a signed 64-bit integer: clipped to the maximum, INVALID. | RVI-D §21.1.5
lui x12, 0x7ff80             #: build 0x7ff8000000000000: the upper word 0x7ff80000 first. | RVI-RV32I §1.1.4
slli x12, x12, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
fmv.d.x f4, x12
fcvt.lu.d x13, f4, 0         #: a NaN to unsigned 64: the maximum, INVALID (Table 5). | RVI-D §21.1.5
csrrs x14, fflags, x0        #: x14 = the accrued flags so far. | RVI-F §20.1.2
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
addi x15, x0, -7             #: -7. | RVI-RV32I §1.1.4
fcvt.d.w f5, x15, 1          #: -7 to double: exact, whatever the (legal) mode. | RVI-D §21.1.5
fmv.x.d x16, f5
fcvt.d.wu f6, x15, 0         #: 0xFFFFFFF9 as unsigned 32: exact. | RVI-D §21.1.5
fmv.x.d x17, f6
lui x18, 0x200               #: build 0x0020000000000001: the upper word 0x00200000 first. | RVI-RV32I §1.1.4
slli x18, x18, 32            #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 1              #: the lower word 0x00000001. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x18, x18, x28             #: x18 = 0x0020000000000001. | RVI-RV32I §1.1.4
fcvt.d.l f7, x18, 0          #: 2^53+1: not representable — rounds to even, NX. | RVI-D §21.1.5
fmv.x.d x19, f7
addi x20, x0, -1             #: 2^64-1 as unsigned. | RVI-RV32I §1.1.4
fcvt.d.lu f8, x20, 1         #: 2^64-1 in RTZ: the largest double below 2^64, NX. | RVI-D §21.1.5
fmv.x.d x21, f8
csrrs x22, fflags, x0        #: x22 = the accrued flags so far. | RVI-F §20.1.2 #|end
