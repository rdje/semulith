#|never: x27
#|refuse: store 0x80000400 0x10
#|refuse: load 0x80000420 0x10
auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 116             #: the trap handler sits at entry + 0x74 — after the 29-instruction main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec <- the handler. | RVI-ZICSR §5.1.1
addi x10, x0, 1              #: the data block: 1 … | RVI-RV32I §1.1.4
slli x10, x10, 31            #: … << 31 = the region base … | RVI-RV64I §3.1.2
addi x10, x10, 1024          #: … + 0x400: A (stores refused); A+0x20 = L (loads refused); A+0x40 = M (untouched). | RVI-RV32I §1.1.4
addi x7, x0, 119             #: the value every write tries to write (0x77). | RVI-RV32I §1.1.4
addi x28, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x28, x28, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x28       #: FS := Initial. | RVP-MACHINE §2.1.1.6.7
addi x15, x10, 32            #: x15 = L, the load-refused doubleword. | RVI-RV32I §1.1.4
addi x12, x0, 12             #: a read-back sentinel the load of A must REPLACE. | RVI-RV32I §1.1.4
addi x5, x0, -3              #: a known double pattern … | RVI-RV32I §1.1.4
fmv.d.x f2, x5               #: … in f2 (an f-register write: FS Dirty). | RVI-D §21.1.5
addi x6, x0, 3               #: both FS bits … | RVI-RV32I §1.1.4
slli x6, x6, 13              #: … 3 << 13. | RVP-CSR
csrrc x0, mstatus, x6        #: FS := Off … | RVI-ZICSR §5.1.1
addi x8, x0, 1               #: the Clean pattern … | RVI-RV32I §1.1.4
slli x8, x8, 14              #: … 1 << 14. | RVP-CSR
csrrs x0, mstatus, x8        #: … then Clean: FS = 2. | RVI-ZICSR §5.1.1
fld f2, x15, 0               #: an FLD whose load is REFUSED: the load access fault 5 — f2 is NOT written, so FS is NOT dirtied. | RVI-D §21.1.3; the experiment's refusal (load, L)
fmv.x.d x9, f2               #: f2 still holds its pattern. | RVI-D §21.1.5
csrrs x11, mstatus, x0       #: FS still Clean, SD 0 — the faulting load committed no FP state. | RVP-MACHINE §2.1.1.6.7
fsd f2, 0, x10               #: an FSD whose store is REFUSED: the store access fault 7, A unchanged. | RVI-D §21.1.3; the experiment's refusal (store, A)
ld x12, x10, 0               #: A still reads 0. | RVI-RV64I §3.1.3
flw f3, x15, 4               #: an FLW inside L's refused bytes: cause 5, f3 untouched. | RVI-F §20.1.5; the experiment's refusal (load, L)
fsw f2, 8, x10               #: an FSW inside A's refused bytes: cause 7. | RVI-F §20.1.5; the experiment's refusal (store, A)
csrrs x13, mstatus, x0       #: FS STILL Clean after four refused FP transfers. | RVP-MACHINE §2.1.1.6.7
csrrs x14, mcause, x0        #: the last delivered cause (7). | RVP-MACHINE §2.1.3.1 #|end
csrrs x29, mcause, x0        #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x30, mtval, x0         #: the faulting address. | RVP-MACHINE §2.1.4
csrrs x31, mepc, x0          #: the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x31, x31, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x31          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back at mepc, in the mode the trap came from (MPP). | RVP-INSNS §3.3.2 (mret)
