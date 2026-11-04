addi x5, x0, 6               #: 6. | RVI-RV32I §1.1.4
mul x5, x5, x5               #: rd = rs1 = rs2: the reads see the PRE-instruction value - 6 x 6 = {new}. | RVI-M §11.1.1
addi x6, x0, -9              #: -9. | RVI-RV32I §1.1.4
div x6, x6, x6               #: -9 / -9 into its own source: {new}. | RVI-M §11.1.2
addi x7, x0, 13              #: 13. | RVI-RV32I §1.1.4
rem x7, x7, x7               #: 13 rem 13 into its own source: {new}. | RVI-M §11.1.2
mul x0, x5, x5               #: an x0 destination: the product is discarded - no register changes. | RVI-RV32I §1.1.1 (x0 is hardwired to 0); RVI-M §11.1.1
div x0, x5, x0               #: a division by zero into x0: no trap, and nothing is written. | RVI-M §11.1.2 (Table 1)
mulhu x0, x5, x5             #: the high half into x0: discarded. | RVI-M §11.1.1
divu x8, x8, x0              #: x8 (still 0) / 0, written over its own source: all bits set, {new}. | RVI-M §11.1.2 (Table 1)
remu x9, x5, x9              #: 36 rem x9 (still 0): division by zero - the dividend, {new}. | RVI-M §11.1.2 (Table 1)
addi x10, x0, 10             #: a sentinel the zero product must replace. | RVI-RV32I §1.1.4
mulh x10, x6, x7             #: 1 x 0 - a zero product: {new}. | RVI-M §11.1.1
divw x11, x5, x6             #: 36 / 1 as words: {new}. | RVI-M §11.1.2
