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
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its failure code in x15: {new}. | RVI-A §12.1.2 (boundary: cold)
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x3)             #: the SC, its failure code in x15: {new}. | RVI-A §12.1.2 (boundary: exact)
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
lr.d x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.d x15, x6, (x1)             #: the doubleword pairs: {new}. | RVI-A §12.1.2
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
lr.w x14, (x2)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its failure code in x15: {new}. | RVI-A §12.1.2 (boundary: replaced)
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
lr.w x14, (x2)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x2)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2
sd x7, 0, x2                   #: B holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x2)             #: the SC, its failure code in x15: {new}. | RVI-A §12.1.2 (boundary: SC at another address)
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its failure code in x15: {new}. | RVI-A §12.1.2 (boundary: invalidated by failure)
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its failure code in x15: {new}. | RVI-A §12.1.2 (boundary: invalidated by success)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x24, x0, 41               #: a sentinel a trapped SC must leave: {new}. | RVI-RV32I §1.1.4
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sc.w x24, x6, (x20)            #: a misaligned SC does not complete: a trap, not a failure. | RVI-A §12.1.2
addi x25, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x25, x24, 0               #: copied: {new}. | RVI-RV32I §1.1.4
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: retained over a misaligned SC)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
addi x21, x0, 1                #: a bit to place at 2^40: {new}. | RVI-RV32I §1.1.4
slli x21, x21, 40              #: 2^40, outside every region: {new}. | RVI-RV64I §3.1.2.1
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sc.w x24, x6, (x21)            #: an SC where nothing is writable does not complete: a trap. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: retained over a permission fault)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
addi x8, x0, 1                 #: mstatus.FS = Initial: {new}. | RVI-RV32I §1.1.4
slli x8, x8, 13                #: mstatus.FS = Initial: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x8          #: FS on, for FSD; no GPR written. | RVP-MACHINE §2.1.1.6.7
fmv.d.x f1, x7                 #: f1 holds 17; no GPR written. | RVI-D §21.1.7
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
sw x7, 0, x1                   #: SW, on this hart, between the LR and the SC. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: SW preserves)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
sd x7, 0, x1                   #: SD, on this hart, between the LR and the SC. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: SD preserves)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
fsd f1, 0, x1                  #: FSD, on this hart, between the LR and the SC. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: FSD preserves)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
amoadd.w x0, x0, (x1)          #: AMOADD, on this hart, between the LR and the SC. | RVI-A §12.1.4
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: AMOADD preserves)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x9, x9, 1                 #: ADDI, on this hart, between the LR and the SC. | RVI-RV32I §1.1.4
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: ADDI preserves)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x1)                 #: LR registers the reservation: {new}. | RVI-A §12.1.2
fence 0, 15, 15, x0, x0        #: FENCE, on this hart, between the LR and the SC. | RVI-RV32I §1.1.7
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: FENCE preserves)
sd x7, 0, x1                   #: A holds 17 again. | RVI-RV64I §3.1.3
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
addi x12, x0, 1                #: level-0[1] maps VA 0x401000 there too, an alias: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[1] maps VA 0x401000 there too, an alias: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[1] maps VA 0x401000 there too, an alias: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[1] maps VA 0x401000 there too, an alias: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -825            #: level-0[1] maps VA 0x401000 there too, an alias: {new}. | RVI-RV32I §1.1.4
sd x12, 8, x11                 #: level-0[1] written. | RVI-RV64I §3.1.3
addi x12, x0, 1                #: level-0[2] maps VA 0x402000 there, read-only: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[2] maps VA 0x402000 there, read-only: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[2] maps VA 0x402000 there, read-only: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[2] maps VA 0x402000 there, read-only: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -957            #: level-0[2] maps VA 0x402000 there, read-only: {new}. | RVI-RV32I §1.1.4
sd x12, 16, x11                #: level-0[2] written. | RVI-RV64I §3.1.3
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
lui x13, 0x400                 #: VA 0x400000: {new}. | RVI-RV64I §3.1.2.1
lui x16, 0x401                 #: VA 0x401000, its alias: {new}. | RVI-RV64I §3.1.2.1
lui x17, 0x402                 #: VA 0x402000, read-only: {new}. | RVI-RV64I §3.1.2.1
lr.w x14, (x13)                #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x16)            #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: aliases pair)
sd x7, 0, x13                  #: A holds 17 again. | RVI-RV64I §3.1.3
lr.w x14, (x13)                #: LR registers the reservation: {new}. | RVI-A §12.1.2
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sc.w x24, x6, (x17)            #: store translation does not pass: a page fault, and the SC does not complete. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x13)            #: the SC, its result in x15: {new}. | RVI-A §12.1.2 (boundary: retained over a page fault)
c.nop                          #: the end of the program. | RVI-C §27.1.8
