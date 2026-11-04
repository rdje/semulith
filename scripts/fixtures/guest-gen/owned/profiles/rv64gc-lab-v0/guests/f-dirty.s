addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x3f800              #: build the pattern 0x3f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f1, x5
lui x6, 0x40400              #: build the pattern 0x40400000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f2, x6
addi x7, x0, 1               #: the FS=Clean pattern starts as 1. | RVI-RV32I §1.1.4
slli x7, x7, 14              #: bit 14: with bit 13 cleared, FS = 2 (Clean). | RVP-CSR (the mstatus field table)
addi x8, x0, 3               #: both FS bits. | RVI-RV32I §1.1.4
slli x8, x8, 13              #: 3 << 13. | RVP-CSR
csrrc x0, mstatus, x8        #: FS := Off … | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x7        #: … then Clean. | RVI-ZICSR §5.1.1
fmv.x.w x9, f1
csrrs x10, mstatus, x0       #: FMV.X.W only READS the FP state: FS stays Clean, SD 0. | RVP-MACHINE §2.1.1.6.7
feq.s x11, f1, f2            #: a compare raising no flag leaves fflags unaltered. | RVI-F §20.1.8
csrrs x12, mstatus, x0       #: … so FS stays Clean (the declared Precise rule). | RVP-MACHINE §2.1.1.6.7
fdiv.s f3, f1, f2, 0         #: an f-register write (and NX): FS Dirty. | RVP-MACHINE §2.1.1.6.7
csrrs x13, mstatus, x0       #: FS Dirty, SD 1. | RVP-MACHINE §2.1.1.6.7
csrrc x0, mstatus, x8        #: FS := Off … | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x7        #: … then Clean again. | RVI-ZICSR §5.1.1
lui x14, 0x7fc00             #: build the pattern 0x7fc00000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f4, x14
csrrc x0, mstatus, x8        #: FS := Off … (the fmv.w.x above wrote an f-register) | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x7        #: … then Clean. | RVI-ZICSR §5.1.1
flt.s x15, f4, f1            #: NV is NEW in fflags: the accrual changes it — FS Dirty without any f-register write. | RVP-MACHINE §2.1.1.6.7
csrrs x16, mstatus, x0       #: FS Dirty. | RVP-MACHINE §2.1.1.6.7
csrrc x0, mstatus, x8        #: FS := Off … | RVI-ZICSR §5.1.1
csrrs x0, mstatus, x7        #: … then Clean. | RVI-ZICSR §5.1.1
flt.s x17, f4, f1            #: NV again — already set: fflags unaltered, so FS stays Clean. | RVP-MACHINE §2.1.1.6.7
csrrs x18, mstatus, x0       #: FS Clean. | RVP-MACHINE §2.1.1.6.7
csrrs x19, fflags, x0        #: x19 = the accrued flags so far. | RVI-F §20.1.2 #|end
