auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
auipc x1, 0                    #: the base for S's handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: S's handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, stvec, x1            #: stvec = S's handler; no GPR written. | RVP-SUPERVISOR §11.1.1.3
jal x0, 20                     #: past S's handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x22, scause, x0          #: S's handler reads scause: {new}. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.8
csrrs x23, stval, x0           #: and stval: {new}. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.9
csrrw x0, sepc, x27            #: sepc = where x27 says; no GPR written. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.7
sret                           #: on, there, still in S. | RVP-MACHINE §2.1.3.2
lui x2, 6                      #: mstatus.FS's two bits: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x2          #: FS cleared; no GPR written. | RVP-MACHINE §2.1.1.6.5
lui x2, 2                      #: FS = Initial: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x2          #: FS = 1, so a write to F state would show as Dirty; no GPR written. | RVP-MACHINE §2.1.1.6.5
addi x5, x0, 127               #: single-precision 1.0: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 23                #: single-precision 1.0: {new}. | RVI-RV64I §3.1.2.1
fmv.w.x f1, x5                 #: f1 holds 1.0, and FS goes Dirty. | RVI-F §20.1
addi x5, x0, 1                 #: NX's flag: {new}. | RVI-RV32I §1.1.4
csrrw x0, fflags, x5           #: fflags = NX; no GPR written. | RVI-F §20.1
lui x2, 6                      #: FS's two bits again: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x2          #: FS cleared; no GPR written. | RVP-MACHINE §2.1.1.6.5
lui x2, 4                      #: FS = Clean: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x2          #: FS = 2, so a write to F state would make it Dirty; no GPR written. | RVP-MACHINE §2.1.1.6.5
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x6, mhartid, x0          #: M reads its hartid first: {new}. | RVP-MACHINE §2.1.1.5
addi x10, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x5, x0, 5                 #: a value a refused write would commit: {new}. | RVI-RV32I §1.1.4
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
csrrw x10, mhartid, x5         #: a write to a read-only CSR, whose read half would write rd: illegal, and rd keeps its value. | RVI-INTRO Exceptions, Traps, and Interrupts; RVP-CSR §1.1.1
addi x12, x0, 1                #: a reader other than the sentinel: {new}. | RVI-RV32I §1.1.4
add x12, x10, x0               #: x10, which the read half did not commit: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-RV32I §1.1.4 (boundary: rd not committed)
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 66                #: what the data page holds: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x1                   #: the data page holds 66. | RVI-RV64I §3.1.3
lui x2, 0xB                    #: medeleg's page-fault bits: {new}. | RVI-RV64I §3.1.2.1
csrrw x0, medeleg, x2          #: the page faults reach S; no GPR written. | RVP-MACHINE §2.1.1.8
lui x11, 3                     #: 0x3000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the root table: {new}. | RVI-RV32I §1.1.4
lui x12, 0x20001               #: the pointer's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: root[0] points at base+0x4000: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 0, x11                 #: root[0] written. | RVI-RV64I §3.1.3
lui x12, 0x20000               #: the leaf's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 207             #: root[2] is a 1 GiB leaf, VA = PA, R, W, X, A and D: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 16, x11                #: root[2] written. | RVI-RV64I §3.1.3
lui x11, 4                     #: 0x4000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the level-1 table: {new}. | RVI-RV32I §1.1.4
lui x12, 0x20001               #: the pointer's upper bits: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1025            #: level-1[2] points at base+0x5000: {new}. | RVP-SUPERVISOR §11.1.4.1
sd x12, 16, x11                #: level-1[2] written. | RVI-RV64I §3.1.3
lui x11, 5                     #: 0x5000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the level-0 table: {new}. | RVI-RV32I §1.1.4
addi x12, x0, 1                #: level-0[0] maps VA 0x400000 to the data page, writable: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[0] maps VA 0x400000 to the data page, writable: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[0] maps VA 0x400000 to the data page, writable: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[0] maps VA 0x400000 to the data page, writable: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -825            #: level-0[0] maps VA 0x400000 to the data page, writable: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x11                 #: level-0[0] written. | RVI-RV64I §3.1.3
addi x12, x0, 1                #: level-0[1] maps VA 0x401000 there, read-only: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[1] maps VA 0x401000 there, read-only: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[1] maps VA 0x401000 there, read-only: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[1] maps VA 0x401000 there, read-only: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -957            #: level-0[1] maps VA 0x401000 there, read-only: {new}. | RVI-RV32I §1.1.4
sd x12, 8, x11                 #: level-0[1] written. | RVI-RV64I §3.1.3
addi x5, x0, 8                 #: raw material for satp.MODE: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 60                #: MODE = Sv39: {new}. | RVI-RV64I §3.1.2.1
lui x2, 128                    #: the root's page number: {new}. | RVI-RV64I §3.1.2.1
addi x2, x2, 3                 #: 0x80003, the root: {new}. | RVI-RV32I §1.1.4
or x2, x2, x5                  #: satp's value: {new}. | RVI-RV32I §1.1.4
csrrw x0, satp, x2             #: translation armed for S; M is not translated. | RVI-ZICSR §5.1.1
addi x3, x0, 3                 #: both MPP bits: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrc x0, mstatus, x3          #: MPP cleared; no GPR written. | RVI-ZICSR §5.1.1
addi x3, x0, 1                 #: MPP = S: {new}. | RVI-RV32I §1.1.4
slli x3, x3, 11                #: at bit 11: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x3          #: MPP = S; no GPR written. | RVI-ZICSR §5.1.1
auipc x4, 0                    #: the base for S's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: S's entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = S's entry; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to S, with translation on. | RVP-MACHINE §2.1.3.2
lui x13, 0x400                 #: VA 0x400000, writable: {new}. | RVI-RV64I §3.1.2.1
lui x16, 0x401                 #: VA 0x401000, read-only: {new}. | RVI-RV64I §3.1.2.1
lui x17, 0x402                 #: VA 0x402000, not mapped: {new}. | RVI-RV64I §3.1.2.1
addi x7, x0, 11                #: a value a refused store would write: {new}. | RVI-RV32I §1.1.4
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ld x6, x17, 0                  #: a load of an unmapped page: rd keeps its value. | RVI-INTRO Exceptions, Traps, and Interrupts; RVP-MACHINE §2.1.1.15
addi x18, x0, 1                #: a reader other than the sentinel: {new}. | RVI-RV32I §1.1.4
add x18, x6, x0                #: x6, which the load did not commit: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts (boundary: load rd)
fmv.x.d x19, f1                #: f1 before: {new}. | RVI-F §20.1
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
flw f1, x17, 0                 #: a float load of an unmapped page: f1 keeps its value. | RVI-INTRO Exceptions, Traps, and Interrupts; RVP-MACHINE §2.1.1.15
addi x19, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
fmv.x.d x19, f1                #: f1, which the load did not commit: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-F §20.1 (boundary: f rd)
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x18, fflags, x0          #: fflags, which the load did not touch: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-F §20.1
lui x19, 6                     #: FS's two bits: {new}. | RVI-RV64I §3.1.2.1
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x18, sstatus, x0         #: sstatus: {new}. | RVP-SUPERVISOR §11.1.1.1
and x18, x18, x19              #: FS alone: {new}. | RVI-RV32I §1.1.4
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x16                  #: a store to the read-only page: memory keeps its value. | RVI-INTRO Exceptions, Traps, and Interrupts; RVP-MACHINE §2.1.1.15
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x18, x13, 0                 #: the page, through the writable mapping: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-RV64I §3.1.3 (boundary: memory)
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
amoadd.d x8, x7, (x16)         #: an AMO on the read-only page: its load completes, its store is refused, and rd keeps its value. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-A §12.1.3
addi x18, x0, 1                #: a reader other than the sentinel: {new}. | RVI-RV32I §1.1.4
add x18, x8, x0                #: x8, which the AMO did not commit: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-A §12.1.3 (boundary: AMO rd)
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x18, x13, 0                 #: and the page: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-RV64I §3.1.3
lr.d x9, (x13)                 #: a reservation on the writable mapping: {new}. | RVI-A §12.1.3
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sc.d x15, x7, (x16)            #: an SC faulting on the read-only page: rd keeps its value and the reservation stays. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-A §12.1.3
addi x18, x0, 1                #: a reader other than the sentinel: {new}. | RVI-RV32I §1.1.4
add x18, x15, x0               #: x15, which the SC did not commit: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-A §12.1.3 (boundary: SC rd)
addi x14, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.d x14, x7, (x13)            #: and the reservation is still there: this SC pairs: {new}. | RVI-INTRO Exceptions, Traps, and Interrupts; RVI-A §12.1.3 (boundary: reservation kept)
c.nop                          #: the end of the program. | RVI-C §27.1.8
