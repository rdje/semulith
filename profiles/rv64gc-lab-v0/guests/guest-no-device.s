# guest-no-device.s — a NEGATIVE platform fixture, added by P0-PROFILE.10.
#
# ⛔ This program exists because the claim it tests was once asserted and was FALSE. The
# environment contract said no I/O region and no time source existed; the matched reference
# happily serviced a load from the core-local interruptor and returned an ADVANCING mtime. The
# override had configured the instruction set and never the platform.
#
# The fixture is the repair made permanent: if a device ever becomes reachable again, this
# program stops faulting and the run goes red.
#
# It reads CLINT mtime at 0x0200_BFF8 — reachable by a PLAIN LOAD, with no CSR instruction, which
# is why excluding Zicsr never excluded reading time.

addi x10, x0, 1
slli x10, x10, 25        # 0x0200_0000 — the core-local interruptor base in the model's default platform
lui  x11, 0xc
addi x11, x11, -8        # 0xBFF8 — the mtime offset
add  x10, x10, x11       # 0x0200_BFF8
ld   x1, x10, 0          # MUST FAULT. If it returns a value, the platform is not matched.
