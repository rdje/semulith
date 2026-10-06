auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 72              #: the trap handler sits at entry + 0x48 — after the 18-instruction main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec <- the handler. | RVI-ZICSR §5.1.1
addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any D instruction. | RVP-MACHINE §2.1.1.6.7
addi x5, x0, 5               #: 5. | RVI-RV32I §1.1.4
fcvt.d.w f1, x5, 5           #: rm = 101, a reserved static mode: illegal even though the conversion is exact — the rm field is decoded as usual. | RVI-F §20.1.2
fcvt.d.w f1, x5, 0
fmv.x.d x6, f1
fcvt.d.s f2, f1, 6           #: rm = 110 on the never-rounding widening: illegal. | RVI-F §20.1.2
addi x7, x0, 6               #: the pattern 110. | RVI-RV32I §1.1.4
csrrw x0, frm, x7            #: frm <- 110 (frm holds any 3-bit value). | RVI-F §20.1.2
fadd.d f3, f1, f1, 7         #: DYN with frm = 110: a reserved dynamic mode — illegal. | RVI-F §20.1.2
fadd.d f4, f1, f1, 0         #: a static RNE is unaffected by frm's reserved value. | RVI-F §20.1.2
fmv.x.d x8, f4
fcvt.s.d f5, f1, 7           #: DYN on the narrowing conversion: illegal too. | RVI-F §20.1.2
csrrs x9, fflags, x0         #: x9 = the accrued flags so far. | RVI-F §20.1.2 #|end
csrrs x29, mcause, x0        #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x30, mepc, x0          #: mepc is the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x30, x30, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x30          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back to M at mepc. | RVP-INSNS §3.3.2 (mret)
