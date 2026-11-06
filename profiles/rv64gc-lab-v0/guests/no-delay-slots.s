addi x7, x0, 1               #: 1, the lesser operand. | RVI-RV32I §1.1.4
addi x8, x0, 2               #: 2, the greater operand. | RVI-RV32I §1.1.4
jal x1, 8                    #: JAL is taken, so control leaves at once. | RVI-RV32I §1.1.5
addi x20, x0, 99             #: the instruction after the transfer: no delay slot, so this never runs. | RVI-RV32I §1.1.5
addi x10, x20, 10            #: landed, and x20 is still 0, so nothing ran in between: {new} = 10. | RVI-RV32I §1.1.5 (boundary: JAL has no delay slot)
auipc x2, 0                  #: the base for the JALR below: {new}. | RVI-RV64I §3.1.2.1
jalr x3, x2, 12              #: JALR is taken, so control leaves at once. | RVI-RV32I §1.1.5
addi x20, x0, 99             #: the instruction after the transfer: no delay slot, so this never runs. | RVI-RV32I §1.1.5
addi x11, x20, 11            #: landed, and x20 is still 0, so nothing ran in between: {new} = 11. | RVI-RV32I §1.1.5 (boundary: JALR has no delay slot)
beq x7, x7, 8                #: BEQ is taken, so control leaves at once. | RVI-RV32I §1.1.5
addi x20, x0, 99             #: the instruction after the transfer: no delay slot, so this never runs. | RVI-RV32I §1.1.5
addi x12, x20, 12            #: landed, and x20 is still 0, so nothing ran in between: {new} = 12. | RVI-RV32I §1.1.5 (boundary: BEQ has no delay slot)
bne x7, x8, 8                #: BNE is taken, so control leaves at once. | RVI-RV32I §1.1.5
addi x20, x0, 99             #: the instruction after the transfer: no delay slot, so this never runs. | RVI-RV32I §1.1.5
addi x13, x20, 13            #: landed, and x20 is still 0, so nothing ran in between: {new} = 13. | RVI-RV32I §1.1.5 (boundary: BNE has no delay slot)
blt x7, x8, 8                #: BLT is taken, so control leaves at once. | RVI-RV32I §1.1.5
addi x20, x0, 99             #: the instruction after the transfer: no delay slot, so this never runs. | RVI-RV32I §1.1.5
addi x14, x20, 14            #: landed, and x20 is still 0, so nothing ran in between: {new} = 14. | RVI-RV32I §1.1.5 (boundary: BLT has no delay slot)
bge x8, x7, 8                #: BGE is taken, so control leaves at once. | RVI-RV32I §1.1.5
addi x20, x0, 99             #: the instruction after the transfer: no delay slot, so this never runs. | RVI-RV32I §1.1.5
addi x15, x20, 15            #: landed, and x20 is still 0, so nothing ran in between: {new} = 15. | RVI-RV32I §1.1.5 (boundary: BGE has no delay slot)
bltu x7, x8, 8               #: BLTU is taken, so control leaves at once. | RVI-RV32I §1.1.5
addi x20, x0, 99             #: the instruction after the transfer: no delay slot, so this never runs. | RVI-RV32I §1.1.5
addi x16, x20, 16            #: landed, and x20 is still 0, so nothing ran in between: {new} = 16. | RVI-RV32I §1.1.5 (boundary: BLTU has no delay slot)
bgeu x8, x7, 8               #: BGEU is taken, so control leaves at once. | RVI-RV32I §1.1.5
addi x20, x0, 99             #: the instruction after the transfer: no delay slot, so this never runs. | RVI-RV32I §1.1.5
addi x17, x20, 17            #: landed, and x20 is still 0, so nothing ran in between: {new} = 17. | RVI-RV32I §1.1.5 (boundary: BGEU has no delay slot)
bne x7, x7, 8                #: BNE on equal operands is not taken, so the next instruction runs, once. | RVI-RV32I §1.1.5
addi x18, x20, 18            #: the next instruction after a transfer not taken: {new} = 18. | RVI-RV32I §1.1.5 (boundary: a branch not taken falls through)
