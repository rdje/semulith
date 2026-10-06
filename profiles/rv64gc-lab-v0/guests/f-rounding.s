auipc x1, 0                  #: x1 holds this instruction's own address. | RVI-RV32I §1.1.4 (D-LUI-AUIPC)
addi x1, x1, 104             #: the trap handler sits at entry + 0x68 — after the 26-instruction main body. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1          #: mtvec <- the handler. | RVI-ZICSR §5.1.1
addi x31, x0, 1              #: the FS=Initial pattern starts as a 1. | RVI-RV32I §1.1.4
slli x31, x31, 13            #: 1 << 13 — mstatus.FS's low bit. | RVP-CSR (the mstatus field table)
csrrs x0, mstatus, x31       #: FS := Initial: the floating-point state is enabled before any F instruction. | RVP-MACHINE §2.1.1.6.7
lui x5, 0x3f800              #: build the pattern 0x3f800000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f1, x5
lui x6, 0x40400              #: build the pattern 0x40400000 (upper 20 bits). | RVI-RV32I §1.1.4
fmv.w.x f2, x6
addi x7, x0, 3               #: RUP is 3. | RVI-F §20.1.2 (Table 2)
csrrw x0, frm, x7            #: frm <- RUP. | RVI-F §20.1.2
fdiv.s f3, f1, f2, 7         #: rm = 111: DYN — rounds by frm (RUP). | RVI-F §20.1.2
fmv.x.w x8, f3
fdiv.s f4, f1, f2, 1         #: a static RTZ overrides frm. | RVI-F §20.1.2
fmv.x.w x9, f4
csrrw x0, fflags, x0         #: clear the accrued flags (an explicit software write — the only way they clear). | RVI-F §20.1.2
fdiv.s f5, f1, f2, 5
fdiv.s f5, f1, f2, 6
csrrs x10, fflags, x0        #: x10 = the accrued flags so far. | RVI-F §20.1.2
addi x11, x0, 7              #: the pattern 111. | RVI-RV32I §1.1.4
csrrw x0, frm, x11           #: frm <- 111 (frm holds any 3-bit value — the FSRM sentence). | RVI-F §20.1.2
fadd.s f6, f1, f2, 7
fadd.s f7, f1, f2, 0         #: a static RNE is unaffected by frm's reserved value. | RVI-F §20.1.2
fmv.x.w x12, f7
csrrs x13, fcsr, x0          #: fcsr: frm 111 above the flags. | RVI-F §20.1.2 #|end
csrrs x29, mcause, x0        #: the handler: the cause. | RVP-MACHINE §2.1.3.1
csrrs x30, mepc, x0          #: mepc is the trapping instruction's own address. | RVP-MACHINE §2.1.3.1
addi x30, x30, 4             #: step past it. | RVI-RV32I §1.1.4
csrrw x0, mepc, x30          #: mepc <- the next instruction. | RVI-ZICSR §5.1.1
mret                         #: back to M at mepc. | RVP-INSNS §3.3.2 (mret)
