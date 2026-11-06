addi x6, x0, 6               #: 6, before the first FENCE.I. | RVI-RV32I §1.1.4
fence.i                      #: FENCE.I retires: no trap and no register written. | RVI-ZIFENCEI §4.1
addi x7, x6, 1               #: the next instruction, in sequence, with nothing in between: {new}. | RVI-ZIFENCEI §4.1 (boundary: FENCE.I has no other effect)
lui x1, 0x00700              #: the upper half of the patch's word: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 0x113           #: 0x00700113, the encoding of addi x2, x0, 7: {new}. | RVI-RV32I §1.1.4
auipc x3, 0                  #: this instruction's own address: {new}. | RVI-RV64I §3.1.2.1
sw x1, 16, x3                #: the patch: the word four instructions on from that AUIPC. | RVI-RV32I §1.1.6
fence.i                      #: orders that store before every later fetch. | RVI-ZIFENCEI §4.1
addi x4, x0, 4               #: an ordinary instruction between. | RVI-RV32I §1.1.4
addi x2, x0, 2               #: fetched after the store and the FENCE.I: this runs as the patch, {new}. | RVI-ZIFENCEI §4.1 (boundary: FENCE.I orders a store before a fetch)
.word 0x0011118F             #: a FENCE.I word with nonzero funct12, rs1 and rd: the fields are ignored, and it never raises. | RVI-ZIFENCEI §4.1
addi x9, x0, 42              #: the next instruction, in sequence: {new}. | RVI-ZIFENCEI §4.1 (boundary: FENCE.I with nonzero fields)
lui x1, 0x00800              #: the upper half of a second patch: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 0x193           #: 0x00800193, the encoding of addi x3, x0, 8: {new}. | RVI-RV32I §1.1.4
auipc x3, 0                  #: this instruction's own address: {new}. | RVI-RV64I §3.1.2.1
sw x1, 12, x3                #: the patch, with no FENCE.I after it. | RVI-RV32I §1.1.6
addi x4, x0, 5               #: an ordinary instruction between: {new}. | RVI-RV32I §1.1.4
addi x3, x0, 3               #: this machine re-reads memory on every fetch, so this runs as the patch: {new}. | RVI-ZIFENCEI §4.1 (boundary: the declared visibility with no FENCE.I)
