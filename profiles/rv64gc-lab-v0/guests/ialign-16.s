auipc x1, 0                  #: the base: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 14              #: base + 14, on a halfword: {new}. | RVI-RV32I §1.1.4
jalr x2, x1, 0               #: JALR to a halfword target raises no misaligned exception: the link is {new}. | RVI-C §27.1 (boundary: JALR to a halfword)
c.nop                        #: skipped: JALR landed past it. | RVI-C §27.1
auipc x3, 0                  #: a 32-bit instruction starting on a halfword: {new}. | RVI-C §27.1 (boundary: a 32-bit instruction on a halfword)
c.li x4, 5                   #: a 16-bit instruction, two bytes on: {new}. | RVI-C §27.1
beq x0, x0, 6                #: BEQ to a halfword target raises no misaligned exception. | RVI-C §27.1
c.nop                        #: skipped: BEQ landed past it. | RVI-C §27.1
auipc x5, 0                  #: landed on a halfword: {new}. | RVI-C §27.1 (boundary: a branch to a halfword)
jal x6, 8                    #: JAL to a halfword target raises no misaligned exception: the link is {new}. | RVI-C §27.1 (boundary: JAL to a halfword)
c.nop                        #: skipped: JAL landed past it. | RVI-C §27.1
c.nop                        #: skipped: JAL landed past it. | RVI-C §27.1
auipc x7, 0                  #: landed on a halfword: {new}. | RVI-C §27.1 (boundary: the landing after JAL)
c.addi x4, 1                 #: 16 bits again: {new}. | RVI-C §27.1
auipc x8, 0                  #: two bytes on, on a word: {new}. | RVI-C §27.1 (boundary: a 16-bit form advances the PC by two)
