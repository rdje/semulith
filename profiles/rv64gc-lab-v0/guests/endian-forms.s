auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x5, x0, 1097              #: a doubleword whose bytes all differ: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: a doubleword whose bytes all differ: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, -1843             #: a doubleword whose bytes all differ: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 14                #: a doubleword whose bytes all differ: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1109              #: a doubleword whose bytes all differ: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: a doubleword whose bytes all differ: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1639              #: a doubleword whose bytes all differ: {new}. | RVI-RV32I §1.1.4
slli x5, x5, 12                #: a doubleword whose bytes all differ: {new}. | RVI-RV64I §3.1.2.1
addi x5, x5, 1928              #: a doubleword whose bytes all differ: {new}. | RVI-RV32I §1.1.4
sd x5, 0, x1                   #: stored at the cell. | RVI-RV64I §3.1.3
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lbu x6, x1, 0                  #: byte 0 is the least significant: {new}. | RVI-RV32I §1.1.6; RVI-RV64I §3.1.3 (boundary: byte 0 is the least significant)
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lbu x6, x1, 7                  #: byte 7 is the most significant: {new}. | RVI-RV32I §1.1.6; RVI-RV64I §3.1.3 (boundary: byte 7 is the most significant)
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lhu x6, x1, 0                  #: the low halfword, its low byte first: {new}. | RVI-RV32I §1.1.6; RVI-RV64I §3.1.3 (boundary: the low halfword, its low byte first)
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lwu x6, x1, 4                  #: the high word, at offset 4: {new}. | RVI-RV32I §1.1.6; RVI-RV64I §3.1.3 (boundary: the high word, at offset 4)
addi x7, x0, 171               #: a byte: {new}. | RVI-RV32I §1.1.4
sb x7, 3, x1                   #: stored at offset 3. | RVI-RV64I §3.1.3
addi x8, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lbu x8, x1, 3                  #: that address reads the same byte: {new}. | RVI-RV32I §1.1.6; RVI-RV64I §3.1.3 (boundary: byte-address invariant)
addi x9, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x9, x1, 0                   #: and the doubleword around it: {new}. | RVI-RV32I §1.1.6; RVI-RV64I §3.1.3
addi x10, x0, 3                #: mstatus.MBE and SBE: {new}. | RVI-RV32I §1.1.4
slli x10, x10, 36              #: mstatus.MBE and SBE: {new}. | RVI-RV64I §3.1.2.1
csrrs x0, mstatus, x10         #: M tries to set both; no GPR written. | RVP-MACHINE §2.1.1.6
addi x11, x0, 64               #: mstatus.UBE: {new}. | RVI-RV32I §1.1.4
csrrs x0, mstatus, x11         #: and UBE; no GPR written. | RVP-MACHINE §2.1.1.6
addi x12, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
csrrs x12, mstatus, x0         #: none holds: {new}. | RVP-MACHINE §2.1.1.6; RVI-RV32I §1.1.6 (boundary: no big-endian bit holds)
addi x13, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
lbu x13, x1, 0                 #: and byte 0 still reads the low byte: {new}. | RVI-RV32I §1.1.6; RVI-RV64I §3.1.3
c.nop                          #: the end of the program. | RVI-C §27.1.8
