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
addi x5, x0, 1                 #: menvcfg's ADUE bit: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 61                #: menvcfg's ADUE bit: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, menvcfg, x5          #: M tries to set ADUE; no GPR written. | RVP-MACHINE §2.1.1.18
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x6, menvcfg, x0          #: ADUE stays clear: Svadu is not selected: {new}. | RVP-MACHINE §2.1.1.18 (boundary: ADUE is WPRI)
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x7, x0, 66                #: the word the data page holds: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x1                   #: the data page's first doubleword holds 66. | RVI-RV64I §3.1.3
lui x2, 0xB                    #: medeleg's page-fault bits: 12, 13 and 15, the upper half: {new}. | RVI-RV64I §3.1.2.1
csrrw x0, medeleg, x2          #: the three page faults reach S; no GPR written. | RVP-MACHINE §2.1.1.8
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
addi x12, x0, 1                #: level-0[0] maps VA 0x400000 to the data page with A and D set: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[0] maps VA 0x400000 to the data page with A and D set: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[0] maps VA 0x400000 to the data page with A and D set: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[0] maps VA 0x400000 to the data page with A and D set: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -825            #: level-0[0] maps VA 0x400000 to the data page with A and D set: {new}. | RVI-RV32I §1.1.4
sd x12, 0, x11                 #: level-0[0] written. | RVI-RV64I §3.1.3
addi x12, x0, 1                #: level-0[1] maps VA 0x401000 there with A clear: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[1] maps VA 0x401000 there with A clear: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[1] maps VA 0x401000 there with A clear: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[1] maps VA 0x401000 there with A clear: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -1017           #: level-0[1] maps VA 0x401000 there with A clear: {new}. | RVI-RV32I §1.1.4
sd x12, 8, x11                 #: level-0[1] written. | RVI-RV64I §3.1.3
addi x12, x0, 1                #: level-0[2] maps VA 0x402000 there with A set and D clear: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[2] maps VA 0x402000 there with A set and D clear: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[2] maps VA 0x402000 there with A set and D clear: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[2] maps VA 0x402000 there with A set and D clear: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -953            #: level-0[2] maps VA 0x402000 there with A set and D clear: {new}. | RVI-RV32I §1.1.4
sd x12, 16, x11                #: level-0[2] written. | RVI-RV64I §3.1.3
addi x12, x0, 1                #: level-0[3] maps VA 0x403000 there, executable, with A clear: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 16              #: level-0[3] maps VA 0x403000 there, executable, with A clear: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, 1               #: level-0[3] maps VA 0x403000 there, executable, with A clear: {new}. | RVI-RV32I §1.1.4
slli x12, x12, 13              #: level-0[3] maps VA 0x403000 there, executable, with A clear: {new}. | RVI-RV64I §3.1.2.1
addi x12, x12, -1013           #: level-0[3] maps VA 0x403000 there, executable, with A clear: {new}. | RVI-RV32I §1.1.4
sd x12, 24, x11                #: level-0[3] written. | RVI-RV64I §3.1.3
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
lui x11, 5                     #: 0x5000: {new}. | RVI-RV64I §3.1.2.1
add x11, x11, x10              #: the level-0 table, which S reads through the code's own 1 GiB leaf: {new}. | RVI-RV32I §1.1.4
auipc x4, 0                    #: the base for S's entry: {new}. | RVI-RV64I §3.1.2.1
addi x4, x4, 16                #: S's entry, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mepc, x4             #: mepc = S's entry; no GPR written. | RVI-ZICSR §5.1.1
mret                           #: to S, with translation on. | RVP-MACHINE §2.1.3.2
lui x13, 0x400                 #: VA 0x400000, A and D set: {new}. | RVI-RV64I §3.1.2.1
lui x14, 0x401                 #: VA 0x401000, A clear: {new}. | RVI-RV64I §3.1.2.1
lui x15, 0x402                 #: VA 0x402000, D clear: {new}. | RVI-RV64I §3.1.2.1
lui x16, 0x403                 #: VA 0x403000, executable with A clear: {new}. | RVI-RV64I §3.1.2.1
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x13, 0                  #: both bits set: nothing to update, so the load completes: {new}. | RVI-RV64I §3.1.3
addi x7, x0, 67                #: a new value: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x13                  #: with A and D set, the store completes too. | RVI-RV64I §3.1.3
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x13, 0                  #: read back: {new}. | RVI-RV64I §3.1.3
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
ld x0, x14, 0                  #: A clear: the load needs an update, so a page fault, and never the update. | RVP-SUPERVISOR §11.1.3.1
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x14                  #: A clear: the store needs an update, so a page fault. | RVP-SUPERVISOR §11.1.3.1
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x15, 0                  #: A set, D clear: a load needs no update and completes: {new}. | RVI-RV64I §3.1.3
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
auipc x27, 0                   #: the handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 12              #: the row after the refused instruction: {new}. | RVI-RV32I §1.1.4
sd x7, 0, x15                  #: D clear: the store needs an update, so a page fault. | RVP-SUPERVISOR §11.1.3.1
auipc x27, 0                   #: S's handler resumes relative to here: {new}. | RVI-RV64I §3.1.2.1
addi x27, x27, 20              #: the row after the fetch: {new}. | RVI-RV32I §1.1.4
addi x22, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
addi x23, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
jalr x0, x16, 0                #: to VA 0x403000: A clear, so the fetch faults there, before any decode. | RVI-RV32I §1.1.5.1
addi x8, x11, 8                #: level-0[1]'s address, through the identity leaf: {new}. | RVI-RV32I §1.1.4
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x8, 0                   #: the PTE the load and the store faulted on: {new}. | RVP-SUPERVISOR §11.1.3.1 (boundary: the A bit left clear)
addi x8, x11, 16               #: level-0[2]'s address: {new}. | RVI-RV32I §1.1.4
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x8, 0                   #: the PTE the store faulted on: {new}. | RVP-SUPERVISOR §11.1.3.1 (boundary: the D bit left clear)
addi x8, x11, 24               #: level-0[3]'s address: {new}. | RVI-RV32I §1.1.4
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x8, 0                   #: the PTE the fetch faulted on: {new}. | RVP-SUPERVISOR §11.1.3.1
c.nop                          #: the end of the program. | RVI-C §27.1.8
