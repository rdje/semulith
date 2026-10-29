# guest-control.s — the control-flow representative program for P0-PROFILE.8.
#
# Arithmetic (`smoke-arith.s`) and a fault boundary (`smoke-trap.s`) were written for the matched
# -profile experiment. This is the third: control transfer, which `P0-PROFILE.6` could not write
# because the B and J immediate layouts live in specification FIGURES the project cannot read.
# They are now DERIVED from riscv-opcodes' machine-readable descriptor table, and the derivation
# refuses any layout whose bits do not total its field width — see `scripts/riscv_asm.py`.
#
# ⭐ Two of this program's observations are NEGATIVE: x6 and x13 must never be written. A jump
# that fails to skip is invisible to a checker that only looks at the registers it expects to
# change, which is exactly why `docs/CPU_ENVIRONMENT.md` §4 asks for negative fixtures.

start:  addi  x1, x0, 3        # loop counter
loop:   addi  x1, x1, -1       # 3 -> 2 -> 1 -> 0
        bne   x1, x0, loop     # D-NO-DELAY-SLOTS: taken twice, then falls through at zero

        jal   x5, over         # link = pc+4 (the SKIPPED instruction's address), then jump
        addi  x6, x0, 1365     # NEVER EXECUTED — this is the negative observation
        addi  x6, x6, 1        # NEVER EXECUTED

over:   addi  x7, x0, 7
        auipc x9, 0            # D-LUI-AUIPC: x9 = the address of THIS instruction
        jalr  x10, x9, 13      # D-JALR-LSB: x9+13 is ODD; the low bit is cleared, so the target
                               # is x9+12 and control lands on `end`, not one byte before it
        addi  x13, x0, 999     # NEVER EXECUTED — the second negative observation
end:    addi  x11, x0, 42
        addi  x12, x0, 1
