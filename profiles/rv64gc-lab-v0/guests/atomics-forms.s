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
jal x0, 16                     #: past S's handler. | RVI-RV32I §1.1.5.1
csrrs x22, scause, x0          #: S's handler reads scause: {new}. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.8
csrrs x23, stval, x0           #: and stval: {new}. | RVI-ZICSR §5.1.1; RVP-SUPERVISOR §11.1.1.9
jalr x0, x27, 0                #: on, to where x27 says, still in S. | RVI-RV32I §1.1.5.1
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x7, x0, -5                #: -5: negative as signed, huge as unsigned: {new}. | RVI-RV32I §1.1.4
addi x6, x0, 7                 #: 7, the other operand: {new}. | RVI-RV32I §1.1.4
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoswap.w x5, x6, (x1)         #: AMOSWAP.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOSWAP.W wrote: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoadd.w x5, x6, (x1)          #: AMOADD.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOADD.W wrote: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoxor.w x5, x6, (x1)          #: AMOXOR.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOXOR.W wrote: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoand.w x5, x6, (x1)          #: AMOAND.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOAND.W wrote: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoor.w x5, x6, (x1)           #: AMOOR.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOOR.W wrote: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amomin.w x5, x6, (x1)          #: AMOMIN.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOMIN.W wrote: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amomax.w x5, x6, (x1)          #: AMOMAX.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOMAX.W wrote: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amominu.w x5, x6, (x1)         #: AMOMINU.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOMINU.W wrote: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amomaxu.w x5, x6, (x1)         #: AMOMAXU.W reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: what AMOMAXU.W wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoswap.d x5, x6, (x1)         #: AMOSWAP.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOSWAP.D wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoadd.d x5, x6, (x1)          #: AMOADD.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOADD.D wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoxor.d x5, x6, (x1)          #: AMOXOR.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOXOR.D wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoand.d x5, x6, (x1)          #: AMOAND.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOAND.D wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoor.d x5, x6, (x1)           #: AMOOR.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOOR.D wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amomin.d x5, x6, (x1)          #: AMOMIN.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOMIN.D wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amomax.d x5, x6, (x1)          #: AMOMAX.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOMAX.D wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amominu.d x5, x6, (x1)         #: AMOMINU.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOMINU.D wrote: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amomaxu.d x5, x6, (x1)         #: AMOMAXU.D reads the old value: {new}. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x8, x1, 0                   #: what AMOMAXU.D wrote: {new}. | RVI-RV64I §3.1.3
addi x9, x0, -1                #: all ones: {new}. | RVI-RV32I §1.1.4
sd x9, 0, x1                   #: the whole doubleword set. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoswap.w x5, x0, (x1)         #: AMOSWAP.W writes zero to the low word only. | RVI-A §12.1.4
ld x11, x1, 0                  #: the upper word kept, the lower word zero: {new}. | RVI-RV64I §3.1.3
addi x26, x0, -1               #: all ones: {new}. | RVI-RV32I §1.1.4
slli x26, x26, 32              #: the upper word set: {new}. | RVI-RV64I §3.1.2.1
addi x26, x26, 7               #: and 7 in the low word: {new}. | RVI-RV32I §1.1.4
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
amomin.w x5, x26, (x1)         #: the smaller of the words -5 and 7, ignoring rs2's upper word: -5 stays. | RVI-A §12.1.4
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x1, 0                   #: still -5: {new}. | RVI-RV64I §3.1.3 (boundary: a word AMO ignores rs2's upper word)
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x12, x0, 7                #: 7, in the register about to be both source and destination: {new}. | RVI-RV32I §1.1.4
amoadd.w x12, x12, (x1)        #: rd equals rs2: the old value reaches rd: {new}. | RVI-A §12.1.4 (boundary: rd equals rs2)
lw x13, x1, 0                  #: -5 + 7, so rs2 was read before rd was written: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the doubleword holds -5. | RVI-RV64I §3.1.3
addi x14, x1, 0                #: the cell's address, in the register about to be both address and destination: {new}. | RVI-RV32I §1.1.4
amoadd.d x14, x6, (x14)        #: rd equals rs1: the old value reaches rd: {new}. | RVI-A §12.1.4 (boundary: rd equals rs1)
ld x3, x1, 0                   #: -5 + 7 at the old address: {new}. | RVI-RV64I §3.1.3
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoadd.w.aq x5, x6, (x1)       #: AMOADD.W with the acquire bit: the same result at one hart: {new}. | RVI-A §12.1.1; RVI-A §12.1.4
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoadd.w.rl x5, x6, (x1)       #: AMOADD.W with the release bit: the same result at one hart: {new}. | RVI-A §12.1.1; RVI-A §12.1.4
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoadd.w.aqrl x5, x6, (x1)     #: AMOADD.W with both bits: the same result at one hart: {new}. | RVI-A §12.1.1; RVI-A §12.1.4
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x14, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lr.w.aqrl x14, (x1)            #: LR.W with both bits decodes and reserves: {new}. | RVI-A §12.1.1; RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w.aq x15, x6, (x1)          #: SC.W with the acquire bit pairs with it: {new}. | RVI-A §12.1.1; RVI-A §12.1.2
sw x7, 0, x1                   #: the cell holds -5. | RVI-RV64I §3.1.3
addi x14, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lr.w x14, (x1)                 #: LR.W loads the word, sign-extended, and registers the reservation: {new}. | RVI-A §12.1.2
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the reservation holds: SC.W writes 7 and 0 to rd: {new}. | RVI-A §12.1.2
addi x16, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x16, x1, 0                  #: the store happened: {new}. | RVI-RV64I §3.1.3
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x7, (x1)             #: the last SC consumed the reservation: this one writes the failure code: {new}. | RVI-A §12.1.2 (boundary: a second SC fails)
addi x17, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x17, x1, 0                  #: nothing stored: {new}. | RVI-RV64I §3.1.3
sd x7, 0, x1                   #: the doubleword holds -5. | RVI-RV64I §3.1.3
addi x18, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lr.d x18, (x1)                 #: LR.D loads the doubleword and registers the reservation: {new}. | RVI-A §12.1.2
addi x19, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.d x19, x6, (x1)             #: the reservation holds: SC.D writes 7 and 0 to rd: {new}. | RVI-A §12.1.2
addi x20, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x20, x1, 0                  #: the store happened: {new}. | RVI-RV64I §3.1.3
addi x21, x0, 1                #: 1, the bit to place at 2^40: {new}. | RVI-RV32I §1.1.4
slli x21, x21, 40              #: 2^40, outside every region this laboratory declares: {new}. | RVI-RV64I §3.1.2.1
addi x24, x0, 41               #: a sentinel a faulting atomic must leave: {new}. | RVI-RV32I §1.1.4
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
amoadd.w x24, x6, (x21)        #: a store/AMO access fault: nothing completes. | RVI-A §12.1.4
addi x25, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x25, x24, 0               #: copied: {new}, nothing committed. | RVI-RV32I §1.1.4
addi x30, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x29, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x28, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
lr.w x24, (x21)                #: a load access fault: an LR is a load, and it registers nothing. | RVI-A §12.1.2
addi x25, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x25, x24, 0               #: copied: {new}, nothing committed. | RVI-RV32I §1.1.4
addi x15, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.w x15, x6, (x1)             #: the faulting LR registered nothing, and the last SC consumed the earlier one: {new}. | RVI-A §12.1.2
lui x2, 8                      #: bit 15: {new}. | RVI-RV64I §3.1.2.1
csrrw x0, medeleg, x2          #: store/AMO page faults reach S; no GPR written. | RVP-MACHINE §2.1.1.8
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
addi x12, x0, 1                #: level-0[0] maps VA 0x400000 to the data page, execute-only: unreadable and unwritable: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[0] maps VA 0x400000 to the data page, execute-only: unreadable and unwritable: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[0] maps VA 0x400000 to the data page, execute-only: unreadable and unwritable: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[0] maps VA 0x400000 to the data page, execute-only: unreadable and unwritable: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -823            #: level-0[0] maps VA 0x400000 to the data page, execute-only: unreadable and unwritable: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x11                 #: level-0[0] written. | RVI-RV64I §3.1.3
addi x12, x0, 1                #: level-0[1] maps VA 0x401000 to the data page, readable and writable: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[1] maps VA 0x401000 to the data page, readable and writable: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[1] maps VA 0x401000 to the data page, readable and writable: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[1] maps VA 0x401000 to the data page, readable and writable: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -817            #: level-0[1] maps VA 0x401000 to the data page, readable and writable: {new}. | RVI-RV32I §1.1.4
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
lui x13, 0x400                 #: VA 0x400000, the execute-only page: {new}. | RVI-RV64I §3.1.2.1
lui x15, 0x401                 #: VA 0x401000, the same page, readable and writable: {new}. | RVI-RV64I §3.1.2.1
addi x24, x0, 42               #: a new sentinel: {new}. | RVI-RV32I §1.1.4
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
amoadd.w x24, x6, (x13)        #: an AMO on an unreadable page: a store/AMO page fault, never a load page fault. | RVP-SUPERVISOR §11.1.4.1; RVI-A §12.1.4
sw x7, 0, x15                  #: through the page S may write, the cell holds -5. | RVI-RV64I §3.1.3
addi x5, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
amoadd.w x5, x6, (x15)         #: a translated AMO on a page it may read and write: {new}. | RVI-A §12.1.4; RVP-SUPERVISOR §11.1.4.1 (boundary: a translated AMO completes)
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lw x8, x15, 0                  #: and memory took the sum: {new}. | RVI-RV64I §3.1.3
