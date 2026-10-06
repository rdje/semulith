addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x7ff40              #: build 0x7ff4000000000123: the upper word 0x7ff40000 first. | RVI-RV32I §1.1.4
slli x5, x5, 32              #: … shifted into bits 63..32. | RVI-RV64I §3.1.2
addi x28, x0, 291            #: the lower word 0x00000123. | RVI-RV32I §1.1.4
slli x28, x28, 32            #: … zero-extended: up … | RVI-RV64I §3.1.2
srli x28, x28, 32            #: … and back down. | RVI-RV64I §3.1.2
or x5, x5, x28               #: x5 = 0x7ff4000000000123. | RVI-RV32I §1.1.4
fmv.d.x f1, x5
fmv.x.d x6, f1
auipc x11, 0                 #: x11 = this instruction's own address, inside the program region. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x11, x11, 1024          #: 1 KiB further: a data address past the code, inside the 64 KiB region. | RVI-RV32I §1.1.4
andi x11, x11, -8            #: … rounded down to a doubleword boundary (FLD/FSD are naturally aligned here). | RVI-RV32I §1.1.4
fsd f1, 0, x11               #: the signaling payload stored unmodified. | RVI-D §21.1.3
ld x7, x11, 0                #: the stored doubleword reads back through the integer side. | RVI-RV64I §3.1.3
fld f2, x11, 0               #: loaded back unmodified — no canonicalization. | RVI-D §21.1.3
fmv.x.d x8, f2
lui x9, 0x3f800              #: build the pattern 0x3f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f3, x9
fmv.x.d x10, f3
fsgnj.d f4, f3, f3           #: the boxed single is a negative quiet NaN as a double; sign injection keeps its bits. | RVI-D §21.1.2
fmv.x.d x12, f4
fclass.d x13, f3             #: the boxed single classifies as a quiet NaN at format 64. | RVI-D §21.1.7
fmv.x.w x14, f1              #: the low 32 bits of the double, sign-extended: a narrower transfer ignores the upper bits. | RVI-D §21.1.2
csrrs x15, fflags, x0        #: x15 = the accrued flags so far. | RVI-F §20.1.2 #|end
