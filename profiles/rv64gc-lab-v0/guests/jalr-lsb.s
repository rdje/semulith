auipc x5, 0                  #: the base, this instruction's own address: {new}. | RVI-RV64I §3.1.2.1
addi x6, x5, 21              #: base + 21, odd: {new}. | RVI-RV32I §1.1.4
jalr x1, x6, 0               #: JALR: base + 21 with its least-significant bit set to zero lands at base + 20; the link is {new}. | RVI-RV32I §1.1.5.1 (boundary: an odd rs1)
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
auipc x7, 0                  #: landed at base + 20, not base + 21: {new}. | RVI-RV32I §1.1.5.1 (boundary: the landing after an odd rs1)
addi x8, x5, 40              #: base + 40, even: {new}. | RVI-RV32I §1.1.4
jalr x9, x8, 1               #: base + 40 + 1 with its least-significant bit set to zero lands at base + 40; the link is {new}. | RVI-RV32I §1.1.5.1 (boundary: an odd immediate)
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
auipc x10, 0                 #: landed at base + 40: {new}. | RVI-RV32I §1.1.5.1 (boundary: the landing after an odd immediate)
addi x11, x5, 57             #: base + 57, odd: {new}. | RVI-RV32I §1.1.4
jalr x12, x11, -1            #: base + 57 - 1 is even, so there is nothing to clear: it lands at base + 56; the link is {new}. | RVI-RV32I §1.1.5.1 (boundary: an odd rs1 and an odd immediate)
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
auipc x13, 0                 #: landed at base + 56: {new}. | RVI-RV32I §1.1.5.1 (boundary: the landing after an even sum)
addi x14, x5, 121            #: base + 121: {new}. | RVI-RV32I §1.1.4
jalr x15, x14, -40           #: -40 sign-extends: base + 81, its least-significant bit set to zero, lands at base + 80; the link is {new}. | RVI-RV32I §1.1.5.1 (boundary: a negative immediate)
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
auipc x16, 0                 #: landed at base + 80: {new}. | RVI-RV32I §1.1.5.1 (boundary: the landing after a negative immediate)
addi x17, x5, 101            #: base + 101: {new}. | RVI-RV32I §1.1.4
jalr x17, x17, 0             #: rd is rs1: the target reads the old value, landing at base + 100, and the link overwrites it: {new}. | RVI-RV32I §1.1.5.1 (boundary: rd equals rs1)
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
addi x20, x0, 99             #: skipped: JALR landed past it. | RVI-RV32I §1.1.5.1
auipc x18, 0                 #: landed at base + 100: {new}. | RVI-RV32I §1.1.5.1 (boundary: the landing when rd equals rs1)
