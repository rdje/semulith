// wl-start.S — the workload start shim on the ACT4 DUT conventions (P4-SYSTEM.15 slice f).
// rvtest_entry_point: stack, FS=Initial, call main; the return value is the verdict.
#include "rvmodel_macros.h"
    .section .text.init
    .globl rvtest_entry_point
rvtest_entry_point:
    la   sp, __stack_top
    li   t0, 1 << 13            // mstatus.FS = Initial (the FP state is enabled before any F/D instruction)
    csrs mstatus, t0
    call main
    bnez a0, 1f
    RVMODEL_HALT_PASS
1:  RVMODEL_HALT_FAIL
    .section .data
    .globl begin_signature, end_signature, wl_signature
    .align 4
begin_signature:
wl_signature:
    .rept 64
    .dword 0xdeadbeefdeadbeef          // 64 slots, canaries the workload overwrites
    .endr
end_signature:
    .section .tohost,"aw",@progbits
    .align 6
    .globl tohost
tohost:
    .dword 0
    .dword 0
