# P4.13 — Runtime contract witnesses

[Contract completion](contract-v2.md) tracks the effective count and freeze.

## Privilege-mode guarantees through the existing matrix

The next runtime pair is OB-PRIV-MODES. Both checks now execute the complete
thirteen-guest P4.2 matrix, totaling 481 declared execution boundaries. This
reuses specification-derived expectations without changing instructions or
expected results.

The positive group runs mm-csr-rw, mm-ebreak, mm-ecall-modes, mm-ecall-deleg
and mm-counters. The negative group runs mm-csr-legality-s/u, mm-mret,
mm-readonly, mm-stimecmp, mm-wfi, mm-sfence and mm-sret. These are whole
programs with legal setup and both legal/refused cells; the labels describe
which behavior each group witnesses.

For a concrete mode observation, mm-ecall-modes reads mcause into x7:
M-mode ECALL yields 11 at step 8, S-mode yields 9 at step 28, and U-mode
yields 8 at step 53 (steps start at zero). The S/U CSR-legality programs
observe illegal-instruction cause 2 at steps 11/10. Other cells read trap
EPC/status and exercise delegation, return and counter/timer gates.

The shared comparison rule checks exact register changes at each step,
never-written registers and physical fetch counts. Mode and trap state are
observed through instructions and handler reads; this does not introduce a
direct comparison of trace PC/mode fields. Finite matrix evidence does not
prove every possible mode-dependent execution or Linux capability.

At c8 the census was 60/114 realized: thirteen scope pairs, twelve guest
pairs and five typed boundary pairs. At that slice, twenty-seven runtime pairs
and final freeze remained. All previous bindings and frozen declarations are unchanged.


## Sv39 prerequisite: inherited global translations

Before binding OB-SV39, review exposed a mismatch between the CPU walk and
its selected cache policy. The CPU remembered only leaf G; an ancestor's G
was lost. Literal PTE regressions reproduced an access fault after an ASID/root
change and premature invalidation by an actual ASID-selective SFENCE.VMA.
The walker now accumulates G along the path. Root/middle/leaf combinations,
no-G controls and all four actual fence scopes discriminate the repair.

The independent expectation author already inherited G correctly and remains
unchanged. This fixes the declared retention policy rather than broadening the
ISA claim. At c9a G-CONTRACT remained 60/114 until the runtime pairs themselves bind.


## Sv39 runtime checks

After the inherited-global prerequisite, OB-SV39's two checks now execute
all fourteen P4.3 translation programs. The positive group covers 4 KiB,
2 MiB and 1 GiB leaves, MPRV's effective mode, stale/fenced mappings and
an instruction straddling noncontiguous physical pages. The negative group
covers noncanonical addresses, invalid/reserved PTEs, misaligned superpages,
R/W/X and U/SUM/MXR permissions, Svade faults and delegated fault delivery.
ENVIRONMENT.md lists every binding.

For example, sv39-perm-rwx reads page-fault causes 15, 13 and 12 into x7
at steps 94, 101 and 109: store, load and instruction faults respectively.
The canonical-address guest reads cause 13 at step 51 and the original
address through mtval. Register changes, expected absent writes, handler
reads and continuation markers retain the existing comparison vocabulary.

The matrix spans 1,417 execution boundaries and 2,832 physical parcel
requests. Re-executing the independent parcel author reproduces every
committed register-change sequence and fetch count exactly. Neither the
programs nor their expectations changed. This is finite translation evidence,
not universal Sv39 or Linux acceptance. At c9b the registry realized
62/114 checks; twenty-six runtime pairs and final freeze remained.


## Svade: fault delivery and unchanged PTEs

OB-SVADE now runs its own positive and negative checks. The three successful
translation programs cover 4 KiB, 2 MiB and 1 GiB leaves and read back each
original 64-bit PTE after translation. The negative program, sv39-svade,
observes A=0 and D=0 behavior separately:

| Step | Result |
| --- | --- |
| 94 | A=0 load: x7 observes page-fault cause 13 |
| 100 | D=0 load: x14 receives 0x42424242 |
| 107 | D=0 store: x7 observes page-fault cause 15 |
| 133 | A=0 PTE read-back: x17 remains 0x2000188f |
| 134 | D=0 PTE read-back: x18 remains 0x2000184f |

A correct trap alone would miss an unintended PTE update. An in-memory control
sets A while still delivering the expected fault: its trap observations agree,
but step 133 reads 0x200018cf and fails. Disabling A/D refusal instead fails
at the first load. The normal independent author agrees with all four programs,
434 boundaries and 868 parcels; the existing core test also compares the whole
byte image across both faults. Guest inputs and production behavior are unchanged.

These witnesses retain the existing ISA observation vocabulary and finite scope.
The selected policy faults instead of updating A/D; Svadu is excluded. Current
G-CONTRACT is 64/114, with twenty-five runtime pairs and final freeze remaining.
