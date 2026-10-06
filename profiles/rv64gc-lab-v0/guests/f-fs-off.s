auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 64              #: the trap handler sits at entry + 0x40 — after the 16-instruction main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec <- the handler. | RVI-ZICSR §5.1.1
addi x6, x0, 3               #: an integer to convert. | RVI-RV32I §1.1.4
flw f1, x0, 0                #: FS=Off (reset): illegal-instruction — the load is never attempted (x0+0 is outside the region, and still cause 2, not 5). | RVP-MACHINE §2.1.1.6.7
fadd.s f2, f1, f1, 0
fmv.x.w x7, f1
fmv.w.x f3, x6
fcvt.s.w f4, x6, 0
feq.s x8, f1, f1
addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
fcvt.s.w f4, x6, 0
fmv.x.w x9, f4
csrrs x10, mstatus, x0       #: FS=Dirty with SD — the conversion wrote an f-register. | RVP-MACHINE §2.1.1.6.7 #|end
csrrs x29, mcause, x0        #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x30, mepc, x0          #: mepc is the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x30, x30, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x30          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back to M at mepc. | RVP-INSNS §3.3.2 (mret)
