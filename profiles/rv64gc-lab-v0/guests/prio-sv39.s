#|never: x28
auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 320             #: the trap handler sits at entry + 0x140. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2037
lui x10, 131073
addi x10, x10, -2047
sd x10, 0, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2015
lui x10, 131073
addi x10, x10, -1023
sd x10, 16, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 1981
lui x10, 131073
addi x10, x10, 1
sd x10, 16, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 1963
lui x10, 131073
addi x10, x10, 1025
sd x10, 0, x11
auipc x11, 0
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 2047
addi x11, x11, 1917
lui x10, 131072
addi x10, x10, 207
sd x10, 0, x11
addi x11, x0, 1              #: L0T's address, absolutely: 1 … | RVI-RV32I §1.1.4
slli x11, x11, 31            #: … << 31 = 0x8000_0000 (the region base) … | RVI-RV64I §3.1.2
lui x12, 3                   #: … + 0x3000 … | RVI-RV32I §1.1.4
add x11, x11, x12            #: x11 = 0x8000_3000, the level-0 table L0T. | RVI-RV32I §1.1.4
lui x10, 0x4000              #: a leaf PTE: PPN 0x10000 (PA 0x1000_0000, OUTSIDE the 64 KiB region) … | RVP-SUPERVISOR §11.1.3.2
addi x10, x10, 207           #: … V R W X A D (0xCF): a valid, permitted mapping. | RVP-SUPERVISOR §11.1.3.2
sd x10, 24, x11              #: L0T[3] <- the leaf: VA 0x0040_3000 now TRANSLATES — to a PA the environment refuses. | RVP-SUPERVISOR §11.1.3.2
lui x2, 128
addi x2, x2, 1
addi x5, x0, 8
slli x5, x5, 60
or x2, x2, x5
csrrw x0, satp, x2
lui x13, 0x403
addi x3, x0, 1
slli x3, x3, 11
csrrw x0, mstatus, x3
auipc x4, 0
addi x4, x4, 16
csrrw x0, mepc, x4
mret
lui x15, 0x404               #: x15 = VA 0x0040_4000: L0T[4] is never written — V=0, a page fault. | RVI-RV32I §1.1.4
ld x14, x15, 4               #: misaligned AND unmapped: misaligned is judged FIRST (the laboratory's one optional choice, .3 decision 7) — cause 4, never 13. | RVP-MACHINE (the synchronous-exception priority table)
sd x14, 4, x15               #: the store twin: cause 6, never 15. | RVP-MACHINE (the priority table)
ld x14, x15, 0               #: aligned and unmapped: the walk's page fault, cause 13 (the control). | RVP-SUPERVISOR §11.1.3.2
ld x14, x13, 4               #: misaligned AND mapped-outside: still misaligned first — cause 4, never 5. | RVP-MACHINE (the priority table)
ld x14, x13, 0               #: aligned and mapped: translation SUCCEEDS, then the physical access is refused — the access fault 5 (translation's faults outrank the physical access's). | RVP-MACHINE (the priority table)
sd x14, 0, x13               #: the store twin: cause 7. | RVP-MACHINE (the priority table)
flw f1, x15, 0               #: FS=Off (reset) AND unmapped: illegal-instruction outranks every explicit-access fault — cause 2, never 13. | RVP-MACHINE (the priority table); §2.1.1.6.7
fld f1, x13, 4               #: FS=Off AND misaligned AND mapped-outside: illegal-instruction first — cause 2. | RVP-MACHINE (the priority table); §2.1.1.6.7
addi x21, x0, 1              #: the continuation proof: every cell above trapped and resumed. | RVP-INSNS §3.3.2 (mret) #|end
csrrs x7, mcause, x0         #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x8, mtval, x0          #: the faulting address (the word, for cause 2). | RVP-MACHINE §2.1.4
csrrs x9, mepc, x0           #: the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x9, x9, 4               #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x9           #: mepc <- the next cell. | RVI-ZICSR §5.1.1
mret                         #: back to S at mepc (MPP = S, the trap came from S). | RVP-INSNS §3.3.2 (mret)
