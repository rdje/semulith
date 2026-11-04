auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 84              #: the trap handler sits at entry + 0x54 — after the 21-instruction main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec <- the handler. | RVI-ZICSR §5.1.1
addi x5, x0, 7               #: the sentinel each refused instruction must leave untouched. | RVI-RV32I §1.1.4
addi x6, x0, 9               #: a value to (try to) write. | RVI-RV32I §1.1.4
addi x7, x0, 11              #: another sentinel. | RVI-RV32I §1.1.4
addi x8, x0, 13              #: another sentinel. | RVI-RV32I §1.1.4
addi x9, x0, 15              #: another sentinel. | RVI-RV32I §1.1.4
addi x10, x0, 17             #: another sentinel. | RVI-RV32I §1.1.4
addi x11, x0, 19             #: a sentinel the legal read must REPLACE. | RVI-RV32I §1.1.4
addi x12, x0, 21             #: another sentinel the legal read must replace. | RVI-RV32I §1.1.4
csrrw x5, mhartid, x6        #: a write to the read-only mhartid: illegal — and the instruction faults as a unit, so rd keeps 7. | RVI-ZICSR §5.1.1
csrrs x7, mhartid, x6        #: set bits (rs1 nonzero): a write, illegal, rd untouched. | RVI-ZICSR §5.1.1
csrrsi x8, mhartid, 1        #: set with a nonzero uimm: a write, illegal, rd untouched. | RVI-ZICSR §5.1.1
csrrci x9, mhartid, 2        #: clear with a nonzero uimm: a write, illegal, rd untouched. | RVI-ZICSR §5.1.1
csrrwi x10, mhartid, 3       #: csrrwi always writes: illegal, rd untouched. | RVI-ZICSR §5.1.1
csrrw x0, mhartid, x6        #: rd = x0 skips the READ, not the write: still illegal. | RVI-ZICSR §5.1.1
csrrs x11, mhartid, x0       #: rs1 = x0: no write, so a legal read — rd <- hart 0. | RVI-ZICSR §5.1.1
csrrci x12, mhartid, 0       #: uimm = 0: no write, so a legal read — rd <- hart 0. | RVI-ZICSR §5.1.1
csrrs x13, mcause, x0        #: the last delivered cause. | RVP-MACHINE §2.1.3.1
csrrs x14, mtval, x0         #: the last delivered xtval: the refused instruction's own word. | RVP-MACHINE §2.1.4 #|end
csrrs x29, mcause, x0        #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x30, mepc, x0          #: mepc is the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x30, x30, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x30          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back to M at mepc. | RVP-INSNS §3.3.2 (mret)
