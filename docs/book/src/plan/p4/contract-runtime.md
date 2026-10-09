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
The selected policy faults instead of updating A/D; Svadu is excluded. At c10,
G-CONTRACT was 64/114, with twenty-five runtime pairs and final freeze remaining.


## IALIGN-16: legal halfwords and required parcels

OB-IALIGN-16 binds c-links, c-page-end and sv39-straddle positively, and
c-page-straddle negatively. With C, both 16-bit and 32-bit instructions may
start at an address congruent to two modulo four. The instruction-length limit
remains 32 bits. These four programs use 165 boundaries and 319 parcel requests.

In c-links, C.JALR targets 0x8000000e and saves 0x8000000a, its pc+2 link;
the subroutine writes x10=1 and returns through that halfword link. In
sv39-straddle, a 32-bit ADDI starts at 0x80000ffe across noncontiguous physical
pages and writes x21=42 at step 44. The next instruction writes x22=7.

The two page-edge programs distinguish instruction length and fault timing:

| Program | Page-end result | Handler observations |
| --- | --- | --- |
| c-page-end | C.NOP executes at step 44; next instruction fetch faults at 45 | cause 12; mtval and mepc both 0x80001000 |
| c-page-straddle | Required second parcel faults at step 44 before instruction effects | cause 12; mtval 0x80001000, mepc 0x80000ffe |

The negative witness is an instruction page fault, not an alignment exception.
A successful first parcel cannot authorize skipping the second one. Conversely,
a compressed instruction must not fetch an unnecessary second parcel.

The independent author reproduces every committed register change and request
count. Four in-memory controls fail: enforcing four-byte parcel alignment (step
0), enforcing four-byte PC alignment (c-links step 3), over-fetching compressed
instructions (page-end step 45), and substituting the instruction start for the
failed parcel's trap value (straddle step 46). No source or expectation changes.
The existing comparison also checks never-written registers; direct trace PC/mode
comparison is not added. This is finite evidence for the selected contract.

At c11, G-CONTRACT was 66/114: thirteen scope pairs, fifteen guest pairs and five
typed boundary pairs. Twenty-four runtime pairs and final freeze remained.


## Zicntr: included counters and read-only refusals

OB-ZICNTR binds mm-counters positively and mm-csr-ro-counters negatively.
Zicntr adds the cycle, time and instret counter views beyond the G abbreviation;
Zihpm is excluded by the exact profile/CSR scope checks. The three assembler
spellings are read-only CSRRS specializations, not three new instruction encodings.
Counter rate and progress retain the existing virtual-time contract.

In mm-counters, the initial M-mode reads observe cycle=0, time=1 and instret=2.
The zero cycle read causes no register change. A gated S-mode cycle read delivers
cause 2; enabling mcounteren.CY permits x8=25 at step 25. In U, scounteren.CY
must also be enabled before x13=51 at step 51. The program's S-mode cells read
cycle; the existing core permission test separately checks S TIME's TM gate.
The independent author's existing mode matrix checks all three counters in M/S/U.

The negative guest attempts six writes to the read-only counter views through
register/immediate forms, including CSRRW with rd=x0. Every refusal preserves
its destination sentinel. Later legal zero-source reads observe cycle=45 and
instret=40 at steps 45/46; the differing counts retain the declared rule that
trapping instructions do not retire. The handler reads cause 2 and the final
refused instruction bits through ordinary GPR observations.

Independent replay reproduces both programs, 101 boundaries and 202 parcels.
Existing counter-enable and U-enable controls fail the mode-gate assertion.
An in-memory control replaces a forbidden write with a successful read: step 9
clobbers x5 with 9 instead of preserving its sentinel 7, and fails. No guest,
expectation or author source is rewritten. This pair is finite inclusion/refusal
evidence; OB-GC-COUNTERS remains a separate later binding. Firmware and Linux
acceptance are still open.

G-CONTRACT is now 68/114: thirteen scope pairs, sixteen guest pairs and five
typed boundary pairs. Twenty-three runtime pairs and final freeze remain.
