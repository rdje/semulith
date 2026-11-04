addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
fmv.x.w x6, f0
fsgnj.s f1, f0, f0           #: fsgnj.s is NOT a transfer: f0 (reset 0 — the upper 32 bits are not all 1s) unboxes to the canonical NaN. | RVI-D §21.1.2
fmv.x.w x7, f1
lui x5, 0x7fa00              #: build the pattern 0x7fa00001 (upper 20 bits). | RVI-RV32I §1.1.4
addi x5, x5, 1               #: … its low 12 bits (1). | RVI-RV32I §1.1.4
fmv.w.x f2, x5
fmv.x.w x8, f2
fsgnj.s f3, f2, f2           #: sign injection does not canonicalize: the signaling payload survives. | RVI-F §20.1.7
fmv.x.w x9, f3
auipc x11, 0                 #: x11 = this instruction's own address, inside the program region. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x11, x11, 1024          #: 1 KiB further: a word-aligned data address past the code, inside the 64 KiB region. | RVI-RV32I §1.1.4
fsw f2, 0, x11
lw x12, x11, 0               #: the stored word reads back through the integer side, sign-extended. | RVI-RV64I §3.1.3
flw f4, x11, 0
fmv.x.w x13, f4
lui x14, 0xbf800             #: build the pattern 0xbf800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f5, x14
fmv.x.w x15, f5  #|end
