auipc x1, 0                  #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16              #: the handler, at its offset from the start: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 24                   #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0        #: the handler reads mcause, replacing a sentinel: {new}. | RVP-CSR §1.1.1; RVP-MACHINE §2.1.1.15 (boundary: a refused access reads cause 2)
csrrs x29, mepc, x0          #: the refused instruction's own address: {new}. | RVP-MACHINE §2.1.1.14
addi x29, x29, 4             #: the instruction after it: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x29          #: resume there; no GPR written. | RVP-MACHINE §2.1.1.14
mret                         #: back in the mode it came from. | RVP-MACHINE §2.1.3.2
addi x5, x0, 85              #: 0x55, the first value. | RVI-RV32I §1.1.4
addi x6, x0, 77              #: a sentinel, so reading the old 0 is a change. | RVI-RV32I §1.1.4
csrrw x6, mscratch, x5       #: CSRRW swaps: x6 <- the old 0, mscratch <- 0x55. | RVI-ZICSR §5.1.1 (boundary: CSRRW reads the old value)
csrrs x7, mscratch, x0       #: with rs1 = x0 CSRRS only reads: {new}. | RVI-ZICSR §5.1.1 (boundary: CSRRW wrote the new one)
addi x8, x0, 15              #: 0x0f, the bits to set. | RVI-RV32I §1.1.4
csrrs x9, mscratch, x8       #: CSRRS reads the old value, 0x55, and sets rs1's bits. | RVI-ZICSR §5.1.1
csrrs x10, mscratch, x0      #: 0x55 | 0x0f: {new}. | RVI-ZICSR §5.1.1 (boundary: CSRRS sets only rs1's bits)
addi x11, x0, 80             #: 0x50, the bits to clear. | RVI-RV32I §1.1.4
csrrc x12, mscratch, x11     #: CSRRC reads the old value, 0x5f, and clears rs1's bits. | RVI-ZICSR §5.1.1
csrrs x13, mscratch, x0      #: 0x5f & ~0x50: {new}. | RVI-ZICSR §5.1.1 (boundary: CSRRC clears only rs1's bits)
csrrwi x14, mscratch, 31     #: CSRRWI reads the old value, 0x0f, and writes the immediate. | RVI-ZICSR §5.1.1
csrrs x15, mscratch, x0      #: the zero-extended 5-bit immediate: {new}. | RVI-ZICSR §5.1.1 (boundary: CSRRWI's immediate is zero-extended)
csrrci x16, mscratch, 1      #: CSRRCI reads the old value, 31, and clears bit 0. | RVI-ZICSR §5.1.1
csrrs x17, mscratch, x0      #: 31 & ~1: {new}. | RVI-ZICSR §5.1.1
csrrsi x18, mscratch, 1      #: CSRRSI reads the old value, 30, and sets bit 0. | RVI-ZICSR §5.1.1
csrrs x19, mscratch, x0      #: 30 | 1: {new}. | RVI-ZICSR §5.1.1
addi x20, x0, 77             #: a sentinel, so reading mhartid's 0 is a change. | RVI-RV32I §1.1.4
csrrs x20, mhartid, x0       #: mhartid is read-only, but rs1 = x0 attempts no write, so no trap: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.5 (boundary: CSRRS with rs1 = x0 on a read-only CSR)
addi x21, x0, 77             #: a sentinel, so reading mhartid's 0 is a change. | RVI-RV32I §1.1.4
csrrsi x21, mhartid, 0       #: uimm = 0 attempts no write, so no trap: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.5 (boundary: CSRRSI with zero on a read-only CSR)
addi x22, x0, 77             #: a sentinel, so reading mhartid's 0 is a change. | RVI-RV32I §1.1.4
csrrc x22, mhartid, x0       #: rs1 = x0 attempts no write, so no trap here either: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.4
addi x19, x0, 77             #: a sentinel, so reading mhartid's 0 is a change. | RVI-RV32I §1.1.4
csrrci x19, mhartid, 0       #: uimm = 0 attempts no write: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.4
addi x24, x0, 41             #: a sentinel: a refused access must leave it. | RVI-RV32I §1.1.4
addi x30, x0, 77             #: a sentinel for the cause. | RVI-RV32I §1.1.4
csrrw x24, mhartid, x5       #: a write to a read-only CSR is illegal, so rd keeps its value. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1
addi x25, x24, 0             #: copied: {new}, nothing committed. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1 (boundary: a refused CSRRW keeps rd)
addi x30, x0, 77             #: a sentinel for the cause. | RVI-RV32I §1.1.4
csrrs x24, mhartid, x5       #: rs1 is not x0, so this attempts a write: illegal. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1
addi x26, x24, 0             #: copied: {new}, nothing committed. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1 (boundary: a refused CSRRS keeps rd)
addi x30, x0, 77             #: a sentinel for the cause. | RVI-RV32I §1.1.4
csrrsi x24, mhartid, 1       #: uimm is not zero, so this attempts a write: illegal. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1
addi x27, x24, 0             #: copied: {new}, nothing committed. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1 (boundary: a refused CSRRSI keeps rd)
addi x3, x0, 1               #: 1, for the MPP field. | RVI-RV32I §1.1.4
slli x3, x3, 11              #: at bit 11: mstatus.MPP = S: {new}. | RVI-RV64I §3.1.2.1
addi x2, x0, 1               #: 1, for mstatus.TVM. | RVI-RV32I §1.1.4
slli x2, x2, 20              #: at bit 20: {new}. | RVI-RV64I §3.1.2.1
or x3, x3, x2                #: MPP = S, and TVM set: {new}. | RVI-RV32I §1.1.4
csrrw x0, mstatus, x3        #: MPP <- S, TVM <- 1; no GPR written. | RVP-MACHINE §2.1.1.6.6
auipc x4, 0                  #: the base for the drop: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16              #: the instruction after mret: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4           #: mepc <- that address; no GPR written. | RVP-MACHINE §2.1.1.14
mret                         #: drop to S. | RVP-MACHINE §2.1.3.2
addi x30, x0, 77             #: a sentinel for the cause. | RVI-RV32I §1.1.4
csrrs x24, mscratch, x0      #: S is below mscratch's privilege: illegal. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1
addi x28, x24, 0             #: copied: {new}, nothing committed. | RVP-CSR §1.1.1; RVI-ZICSR §5.1.1 (boundary: S refused an M CSR keeps rd)
csrrw x31, sscratch, x5      #: S reaches sscratch: the old 0 replaces nothing, and sscratch <- 0x55. | RVI-ZICSR §5.1.1
csrrs x31, sscratch, x0      #: S reads what it wrote: {new}. | RVI-ZICSR §5.1.1; RVP-CSR §1.1.1 (boundary: S reaches its own CSR)
addi x30, x0, 77             #: a sentinel for the cause. | RVI-RV32I §1.1.4
csrrs x24, satp, x0          #: with mstatus.TVM set, S's access to satp is illegal. | RVP-MACHINE §2.1.1.6.6; RVP-CSR §1.1.1
addi x23, x24, 0             #: copied: {new}, nothing committed. | RVP-MACHINE §2.1.1.6.6; RVP-CSR §1.1.1 (boundary: S's satp with TVM set)
