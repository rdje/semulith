auipc x1, 0                  #: x1 holds this instruction's own address (entry + 0x0). | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 80              #: the trap handler sits at entry + 0x50. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec is programmed to the handler; rd=x0 discards the old value. | RVI-ZICSR §5.1.1
csrrs x5, fflags, x0         #: FS resets Off (the laboratory's reset row): the fflags access is illegal-instruction — cause 2, xtval the instruction word, mepc this instruction (entry+0x0C). | RVP-MACHINE §2.1.1.6.7 (the Off-state sentence); RVI-F §20.1.2
csrrs x6, frm, x0            #: FS still Off: the frm access traps identically (mepc entry+0x10). | RVP-MACHINE §2.1.1.6.7
csrrs x7, fcsr, x0           #: and fcsr (mepc entry+0x14) — the gate covers all three FP CSRs. | RVP-MACHINE §2.1.1.6.7
addi x8, x0, 1               #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x8, x8, 13              #: 1 << 13 is the FS field's low bit (mstatus[14:13]). | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x8        #: set FS=Initial; rd=x0 discards the old mstatus. | RVI-ZICSR §5.1.1
csrrs x9, fflags, x0         #: legal now: fflags reads its reset 0 (x9 already holds 0 — the step's trap-free passage is the observation). | RVI-F §20.1.2
csrrs x10, frm, x0           #: legal: frm reads 0 (RNE). | RVI-F §20.1.2
csrrs x11, fcsr, x0          #: legal: the composed view reads 0. | RVI-F §20.1.2
csrrs x12, mstatus, x0       #: x12 observes FS=Initial with SD=0 (MPIE=1 is the trap returns' stack). | RVP-MACHINE §2.1.1.6.7
addi x17, x0, 3              #: the FS=Dirty pattern. | RVI-RV32I §1.1.4
slli x17, x17, 13            #: 3 << 13. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x17       #: set FS=Dirty. | RVI-ZICSR §5.1.1
csrrs x13, mstatus, x0       #: x13 observes FS=Dirty with SD computed 1 — SD reacts to the FS write. | RVP-MACHINE §2.1.1.6.7 (SD)
csrrc x0, mstatus, x17       #: clear both FS bits — FS=Off again. | RVI-ZICSR §5.1.1
csrrs x14, fflags, x0        #: the gate closes: fflags at FS=Off traps (mepc entry+0x48). | RVP-MACHINE §2.1.1.6.7
csrrs x19, mstatus, x0       #: x19 observes FS=Off with SD=0 — the gate's pre- and post-state both readable. | RVP-MACHINE §2.1.1.6.7 #|end
csrrs x15, mcause, x0        #: the handler: cause 2 (illegal instruction). | RVP-MACHINE §2.1.3.1
csrrs x16, mepc, x0          #: mepc is the faulting access's own address. | RVP-MACHINE §2.1.3.1
addi x16, x16, 4             #: step mepc past the faulting instruction. | RVI-RV32I §1.1.4
csrrw x0, mepc, x16          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: MPP was set to M by the trap, so the return lands back in M at mepc. | RVP-INSNS §3.3.2 (mret)
