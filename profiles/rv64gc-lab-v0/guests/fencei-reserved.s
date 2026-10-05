#|never: x28, x29
# fencei-reserved.s — the reserved-fields cell (P4-SYSTEM.6 decision 5): a fence.i
# word with NONZERO funct12/rs1/rd EXECUTES as the declared nop — the chapter's
# forward-compatibility rule ("base implementations shall ignore these fields") is a
# DECODE property, exercised end-to-end: the word matches the generated decode table's
# funct3+opcode mask with its fields never consulted, and the continuation marker
# retires.

      .word 0x0011118F           #: fence.i with imm12=1, rs1=x2, rd=x3 — decoded-and-IGNORED (the mask covers funct3 and the opcode only): the word retires as the declared nop, never raises. | RVI-ZIFENCEI §4.1; the .6 brief's decision 5
      addi  x9, x0, 42           #: the continuation marker: execution passed the reserved-fields word — proof the fields were ignored, never legalization-rejected. | RVI-RV32I §1.1.4 #|end
