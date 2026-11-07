auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x5, misa, x0             #: misa names the base and each letter: {new}. | RVP-MACHINE §2.1.1.1; RVI-NAMING §36.1 (boundary: misa names the composition)
addi x6, x0, -1                #: all ones: {new}. | RVI-RV32I §1.1.4
srli x6, x6, 32                #: a 64-bit register keeps the upper half's zeros and the lower half's ones: {new}. | RVI-RV64I §3.1.2.1 (boundary: the base is RV64I)
addi x8, x0, 6                 #: six: {new}. | RVI-RV32I §1.1.4
addi x9, x0, 7                 #: seven: {new}. | RVI-RV32I §1.1.4
mul x12, x8, x9                #: M is here: {new}. | RVI-M §11.1.1
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
sd x8, 0, x1                   #: the cell holds six. | RVI-RV64I §3.1.3
amoadd.d x13, x9, (x1)         #: A is here, and rd takes the old value: {new}. | RVI-A §12.1.3
ld x14, x1, 0                  #: and memory took the sum: {new}. | RVI-RV64I §3.1.3
lui x2, 6                      #: mstatus.FS's two bits: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x2          #: FS = Dirty, so the floating-point forms may run; no GPR written. | RVP-MACHINE §2.1.1.6.5
addi x15, x0, 127              #: single-precision 1.0: {new}. | RVI-RV32I §1.1.4
slli x15, x15, 23              #: single-precision 1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f1, x15                #: into f1, boxed. | RVI-F §20.1
fadd.s f2, f1, f1, 0           #: F is here: 1.0 + 1.0, written to f2. | RVI-F §20.1
fmv.x.w x16, f2                #: its bits: {new}. | RVI-F §20.1
addi x17, x0, 1023             #: double-precision 1.0: {new}. | RVI-RV32I §1.1.4
slli x17, x17, 52              #: double-precision 1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.d.x f3, x17                #: into f3. | RVI-D §21.1
fadd.d f4, f3, f3, 0           #: D is here: 1.0 + 1.0, written to f4. | RVI-D §21.1
fmv.x.d x18, f4                #: its bits: {new}. | RVI-D §21.1
addi x19, x0, 1                #: one: {new}. | RVI-RV32I §1.1.4
c.addi x19, 1                  #: C is here, on a two-byte parcel: {new}. | RVI-C §27.1.5.1
csrrw x20, mscratch, x9        #: Zicsr is here: the old value is 0: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.13
csrrs x21, mscratch, x0        #: and the new one reads back: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.13
fence.i                        #: Zifencei is here: it retires. | RVI-ZIFENCEI §4.1
addi x22, x0, 9                #: the row after FENCE.I ran: {new}. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
rdinstret x23                  #: Zicntr is here: instret counts what has retired: {new}. | RVI-ZICNTR §6.1.1 (boundary: Zicntr, on the unprivileged side)
csrrw x0, stimecmp, x9         #: Sstc is here: M writes the compare; no GPR written. | RVP-SSTC §12.1
csrrs x24, stimecmp, x0        #: and it reads back: {new}. | RVP-SSTC §12.1 (boundary: Sstc, on the privileged side)
c.nop                          #: the end of the program. | RVI-C §27.1.8
