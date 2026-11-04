#|never: x27
#|refuse: store 0x80000400 0x10
#|refuse: load 0x80000420 0x10
auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 92              #: the trap handler sits at entry + 0x5c — after the 23-instruction main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec <- the handler. | RVI-ZICSR §5.1.1
addi x10, x0, 1              #: the data block: 1 … | RVI-RV32I §1.1.4
slli x10, x10, 31            #: … << 31 = the region base … | RVI-RV64I §3.1.2
addi x10, x10, 1024          #: … + 0x400: A (stores refused); A+0x20 = L (loads refused); A+0x40 = M (untouched). | RVI-RV32I §1.1.4
addi x7, x0, 119             #: the value every write tries to write (0x77). | RVI-RV32I §1.1.4
addi x5, x0, 5               #: sentinels: x5 … | RVI-RV32I §1.1.4
addi x11, x0, 11             #: … x11 … | RVI-RV32I §1.1.4
addi x13, x0, 13             #: … x13 — each left untouched by the instruction that faults. | RVI-RV32I §1.1.4
addi x8, x0, 8               #: read-back sentinels the loads must REPLACE: x8 … | RVI-RV32I §1.1.4
addi x12, x0, 12             #: … and x12. | RVI-RV32I §1.1.4
addi x15, x10, 32            #: x15 = L, the load-refused doubleword. | RVI-RV32I §1.1.4
addi x16, x10, 64            #: x16 = M, refused for nothing. | RVI-RV32I §1.1.4
lr.d x5, (x15)               #: an LR whose load is REFUSED: the load access fault 5 (an LR is a load), x5 untouched — and no reservation is registered (it is registered only on a completed load). | RVI-A §12.1.2; the experiment's refusal (load, L)
sc.d x6, x7, (x16)           #: so an SC (to M, allowed) finds no reservation: it FAILS — x6 <- 1, nothing stored. | RVI-A §12.1.2; state.sexp's deterministic SC policy
ld x8, x16, 0                #: M still reads 0: the failed SC wrote nothing. | RVI-RV64I §3.1.3
lr.d x9, (x10)               #: an LR on A (loads of A are allowed): x9 <- 0, the reservation registered on A. | RVI-A §12.1.2
sc.d x11, x7, (x10)          #: the SC's store to A is REFUSED: the store access fault 7, x11 untouched, A unchanged — the trap clears nothing (the declared policy). | RVI-A §12.1.2; the experiment's refusal (store, A)
amoadd.w x13, x7, (x10)      #: an AMO on A: its LOAD half completes, its STORE half is refused — cause 7 after the first suboperation, x13 untouched, A unchanged (the completed read is not rolled back, and it changed nothing). | RVI-A §12.1.4; the experiment's refusal (store, A)
ld x12, x10, 0               #: A still reads 0. | RVI-RV64I §3.1.3
amoor.d x13, x7, (x15)       #: an AMO on L: its LOAD half is refused, so its store is never issued — cause 7 (an AMO's access faults are store/AMO faults), x13 untouched. | RVI-A §12.1.4; the experiment's refusal (load, L)
csrrs x14, mcause, x0        #: the last delivered cause (7). | RVP-MACHINE §2.1.3.1 #|end
csrrs x29, mcause, x0        #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x30, mtval, x0         #: the faulting address. | RVP-MACHINE §2.1.4
csrrs x31, mepc, x0          #: the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x31, x31, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x31          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back at mepc, in the mode the trap came from (MPP). | RVP-INSNS §3.3.2 (mret)
