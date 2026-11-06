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
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x2, x1, 8                 #: address B, the next doubleword: {new}. | RVI-RV32I §1.1.4
addi x3, x1, 4                 #: the word beside A, in A's eight-byte set: {new}. | RVI-RV32I §1.1.4
addi x20, x1, 2                #: two bytes in, misaligned: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 17                #: the word the cells hold: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x1                   #: A holds 17. | RVI-RV64I §3.1.3
sd x7, 0, x2                   #: B holds 17. | RVI-RV64I §3.1.3
addi x6, x0, 42                #: the value a pairing SC stores: {new}. | RVI-RV32I §1.1.4
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x3)             #: the word beside the reservation: {new}. | RVI-A §12.1.3 (boundary: beside the reservation)
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x16, x1, 0                  #: A and the word beside it, untouched: {new}. | RVI-RV64I §3.1.3
addi x6, x0, 1097              #: a value wider than a word: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 12                #: a value wider than a word: {new}. | RVI-RV64I §3.1.2.1
addi x6, x6, -1843             #: a value wider than a word: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 14                #: a value wider than a word: {new}. | RVI-RV64I §3.1.2.1
addi x6, x6, 1109              #: a value wider than a word: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 12                #: a value wider than a word: {new}. | RVI-RV64I §3.1.2.1
addi x6, x6, 1639              #: a value wider than a word: {new}. | RVI-RV32I §1.1.4
slli x6, x6, 12                #: a value wider than a word: {new}. | RVI-RV64I §3.1.2.1
addi x6, x6, 1928              #: a value wider than a word: {new}. | RVI-RV32I §1.1.4
addi x8, x0, -1                #: all ones: {new}. | RVI-RV32I §1.1.4
sd x8, 0, x1                   #: A's doubleword is all ones. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the pair succeeds: {new}. | RVI-A §12.1.3 (boundary: low width bytes)
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x16, x1, 0                  #: the doubleword: {new}. | RVI-RV64I §3.1.3
addi x8, x0, -1                #: all ones: {new}. | RVI-RV32I §1.1.4
sd x8, 0, x1                   #: all ones again. | RVI-RV64I §3.1.3
lr.d x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.d x15, x6, (x1)             #: the doubleword pair: {new}. | RVI-A §12.1.3
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x16, x1, 0                  #: all sixty-four bits: {new}. | RVI-RV64I §3.1.3
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.d x15, x7, (x1)             #: the pair is gone: {new}. | RVI-A §12.1.3 (boundary: completed SC clears)
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x16, x1, 0                  #: unchanged: {new}. | RVI-RV64I §3.1.3
addi x5, x0, 119               #: rs2's value: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x1                   #: A holds 17. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
sc.w x5, x5, (x1)              #: rd is rs2: the store takes the original value, and rd takes the result: {new}. | RVI-A §12.1.3 (boundary: rd = rs2)
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x16, x1, 0                  #: the store took the original value: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: A holds 17. | RVI-RV64I §3.1.3
addi x4, x1, 0                 #: a copy of A's address: {new}. | RVI-RV32I §1.1.4
lr.w x14, (x4)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
sc.w x4, x6, (x4)              #: rd is rs1: the address is the original, and rd takes the result: {new}. | RVI-A §12.1.3 (boundary: rd = rs1)
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x16, x1, 0                  #: stored at the original address: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: A holds 17. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
sc.w x0, x6, (x1)              #: rd is x0: only the result is discarded. | RVI-A §12.1.3
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x16, x1, 0                  #: the store still happened: {new}. | RVI-RV64I §3.1.3 (boundary: rd = x0)
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x7, (x1)             #: and that SC completed: {new}. | RVI-A §12.1.3
addi x21, x0, 1                #: a bit to place at 2^40: {new}. | RVI-RV32I §1.1.4
slli x21, x21, 40              #: 2^40, outside every region: {new}. | RVI-RV64I §3.1.2.1
addi x24, x0, 41               #: a sentinel: {new}. | RVI-RV32I §1.1.4
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sc.w x24, x6, (x21)            #: no reservation, and no write permission: permission is checked first, so a trap rather than a failure code. | RVI-A §12.1.3
addi x25, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x25, x24, 0               #: copied: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x1                   #: A holds 17. | RVI-RV64I §3.1.3
lui x2, 0x8                    #: medeleg's store page-fault bit: {new}. | RVI-RV64I §3.1.2.1
csrrw x0, medeleg, x2          #: store page faults reach S; no GPR written. | RVP-MACHINE §2.1.1.8
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
addi x12, x0, 1                #: level-0[0] maps VA 0x400000 to the data page: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[0] maps VA 0x400000 to the data page: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[0] maps VA 0x400000 to the data page: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[0] maps VA 0x400000 to the data page: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -825            #: level-0[0] maps VA 0x400000 to the data page: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x11                 #: level-0[0] written. | RVI-RV64I §3.1.3
addi x12, x0, 1                #: level-0[1] maps VA 0x401000 there, writable with D clear: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[1] maps VA 0x401000 there, writable with D clear: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[1] maps VA 0x401000 there, writable with D clear: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[1] maps VA 0x401000 there, writable with D clear: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -953            #: level-0[1] maps VA 0x401000 there, writable with D clear: {new}. | RVI-RV32I §1.1.4
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
addi x26, x11, 8               #: level-0[1]'s address, through the identity leaf: {new}. | RVI-RV32I §1.1.4
auipc x4, 0                    #: the base for S's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: S's entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = S's entry; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to S, with translation on. | RVP-MACHINE §2.1.3.2
lui x13, 0x400                 #: VA 0x400000: {new}. | RVI-RV64I §3.1.2.1
lui x16, 0x401                 #: VA 0x401000, D clear: {new}. | RVI-RV64I §3.1.2.1
lr.w x14, (x13)                #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sc.w x24, x6, (x16)            #: store translation needs an update Svade will not make: a page fault, and the SC does not complete. | RVI-A §12.1.3
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x13)            #: and the prior reservation is still there: {new}. | RVI-A §12.1.3 (boundary: reservation over the target fault)
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x18, x26, 0                 #: the PTE it faulted on: {new}. | RVP-SUPERVISOR §11.1.3.1
addi x24, x0, 43               #: a new sentinel: {new}. | RVI-RV32I §1.1.4
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sc.w x24, x6, (x16)            #: no reservation, and still no store permission: the trap again, not a failure code. | RVI-A §12.1.3
c.nop                          #: the end of the program. | RVI-C §27.1.8
