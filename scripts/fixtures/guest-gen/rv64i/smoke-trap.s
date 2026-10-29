# smoke-trap.s — the access/trap half of the P0-PROFILE.6 matched-profile experiment.
#
# `G0` requires the evidence path to carry a failure/event case and not only arithmetic, because
# a model that computes correctly and misreports faults is the failure mode differential testing
# on arithmetic alone cannot see.
#
# This program performs a MISALIGNED 4-byte load, which `profile.toml` decision D-MISALIGN-DATA
# resolves: this laboratory does NOT handle misaligned accesses invisibly; the access raises an
# address-misaligned exception delivered as a contained trap. The specification delegates the
# choice to the execution environment, so a reference configured the other way is a PROFILE
# DIFFERENCE and not a defect — which is exactly what this experiment is written to observe.

addi x10, x0, 1          # build the main-memory base 0x8000_0000 arithmetically
slli x10, x10, 31
lw   x1, x10, 1025       # 0x8000_0401 — not 4-byte aligned. The instruction before this one
                         # proves the base itself is fine, so the fault is the misalignment.
