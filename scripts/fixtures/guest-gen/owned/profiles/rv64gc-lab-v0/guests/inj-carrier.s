#|refuse: store 0x80000400 0x8
#|refuse: load 0x80000408 0x8
auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 84              #: the trap handler sits at entry + 0x54 — after the 21-instruction main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec <- the handler. | RVI-ZICSR §5.1.1
addi x10, x0, 1              #: the data block's address: 1 … | RVI-RV32I §1.1.4
slli x10, x10, 31            #: … << 31 = the region base … | RVI-RV64I §3.1.2
addi x10, x10, 1024          #: … + 0x400: A, the store-refused doubleword. | RVI-RV32I §1.1.4
addi x5, x0, 85              #: the value every store tries to write (0x55). | RVI-RV32I §1.1.4
addi x6, x0, 3               #: a sentinel the read-back of A must REPLACE (A still holds 0). | RVI-RV32I §1.1.4
addi x7, x0, 4               #: a sentinel the refused load must leave untouched. | RVI-RV32I §1.1.4
addi x8, x0, 5               #: another sentinel a refused load must leave untouched. | RVI-RV32I §1.1.4
addi x11, x0, 6              #: the sentinel the refused AMO must leave untouched. | RVI-RV32I §1.1.4
sd x5, 0, x10                #: a store to A: the environment REFUSES it — the store access fault 7, memory unchanged. | the experiment's refusal (store, A)
ld x6, x10, 0                #: loads of A are allowed: A still reads 0 — the refused store wrote nothing. | RVI-RV64I §3.1.3
sd x5, 8, x10                #: a store to B is allowed: B <- 0x55. | RVI-RV64I §3.1.3
ld x7, x10, 8                #: a load of B: REFUSED — the load access fault 5, x7 untouched. | the experiment's refusal (load, B)
lw x8, x10, 12               #: a word inside B's refused bytes: refused too — cause 5, x8 untouched. | the experiment's refusal (load, B)
sd x5, 16, x10               #: C = A+16, refused for nothing: the store lands. | RVI-RV64I §3.1.3
ld x9, x10, 16               #: and reads back 0x55 — the carrier refuses only the declared bytes and kinds. | RVI-RV64I §3.1.3
amoswap.d x11, x5, (x10)     #: an AMO on A: its LOAD half is allowed and completes, its STORE half is refused — the fault after the first suboperation: cause 7, x11 untouched, A unchanged (the completed read is not rolled back, SEM-06; it changed nothing). | RVI-A §12.1.4; the experiment's refusal (store, A)
ld x12, x10, 0               #: A still reads 0 — the AMO wrote nothing. | RVI-RV64I §3.1.3
csrrs x13, mcause, x0        #: the last delivered cause (the AMO's 7). | RVP-MACHINE §2.1.3.1 #|end
csrrs x29, mcause, x0        #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x30, mtval, x0         #: the faulting address. | RVP-MACHINE §2.1.4
csrrs x31, mepc, x0          #: the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x31, x31, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x31          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back to M at mepc. | RVP-INSNS §3.3.2 (mret)
