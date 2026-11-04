#|never: x27
#|refuse: walk 0x80001000 0x8
auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 268             #: the trap handler sits at entry + 0x10c — after the 67-instruction main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec <- the handler. | RVI-ZICSR §5.1.1
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
ld x14, x13, 0               #: VA 0x0040_3000's walk reads root[0] (level 2) — a read the environment REFUSES: the walk ends there with the LOAD ACCESS fault 5 (the original access's kind), never a page fault; x14 untouched. | RVP-SUPERVISOR §11.1.3.2; the experiment's refusal (walk)
sd x14, 0, x13               #: the store's walk meets the same refusal: the STORE access fault 7. | RVP-SUPERVISOR §11.1.3.2; the experiment's refusal (walk)
amoadd.d x15, x14, (x13)     #: an AMO's one translation meets it too: cause 7, x15 untouched. | RVI-A §12.1.4; the experiment's refusal (walk)
addi x21, x0, 1              #: the continuation proof: every cell trapped and resumed. | RVP-INSNS §3.3.2 (mret) #|end
csrrs x29, mcause, x0        #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x30, mtval, x0         #: the faulting address. | RVP-MACHINE §2.1.4
csrrs x31, mepc, x0          #: the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x31, x31, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x31          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back at mepc, in the mode the trap came from (MPP). | RVP-INSNS §3.3.2 (mret)
