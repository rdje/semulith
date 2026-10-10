# P4.2 — Privilege and mode transitions

**Status:** Landed, flipped, and closed (slices a–h, 2026-10-03)

The later independent expectation author now checks the same declared permissions
(P4.12 slice e1a). Its pre-bind census found accepted paths missing fixed `misa` fields,
TVM checks and SRET legality. Those author defects are repaired: known permission failures
deliver illegal-instruction before own side effects, higher privilege ignores supervisor
interception, and writes retain the selected read-only `misa` fields. Five mode-matrix
guests reproduce 140 committed architectural steps; nine deliberate mutations fail.
This repairs the author used to predict guest results; the production CPU's existing
mode-matrix results remain unchanged.

P4.13's cold-reset review later found and repaired a production CSR-view defect:
`sie` and `sip` must hide every interrupt bit not delegated by `mideleg`
(RVP-MACHINE §2.1.1.9). Hidden bits read zero and ignore writes, while the
underlying `mie`/`mip` state remains intact. The shared CSR read/write machinery
now applies that rule in both M and S modes. The independent author also uses
`mip` as `sip`'s sole owner. Eight delegation masks, all six CSR instruction
forms, revocation and five deliberate author mutations discriminate the repair;
the existing guest records remain unchanged. See the
[reset prerequisite examples](contract-v2.md#supervisor-interrupt-views-before-cold-reset).

The later [satp whole-write repair](sv39.md#unsupported-satp-mode-ignores-the-whole-write)
checks permissions before ignoring unsupported MODE writes. MODE retention alone
cannot implement that rule: ASID and PPN must also remain unchanged. The core
uses canonical field metadata; literal instruction/read-back controls independently
guard the processor and expectation author.

The current privilege machinery is driven by the profile's canonical encoding,
state and semantic definitions. Zicsr supplies six real instruction forms.
Zicntr's rdcycle/rdtime/rdinstret are assembler pseudo-operations of CSRRS;
they add no decoder instructions. Pseudo specialization is checked separately
from encoding disjointness. CSR operand positions and names derive from the
profile's encoding and state, and fetch alignment derives from its IALIGN
selection: 32 bits for rv64i and 16 for this composed profile. The ELF loader
uses that same profile alignment. CLI run and demo accept explicit profile
selection; rv64i remains the default, and commands whose machinery is still
rv64i-specific refuse rv64gc by name.

The state definition owns M/S/U mode, 33 CSR names with 26 underlying storage
owners, resets and field disciplines. Views share their owners. WPRI/WARL/WLRL
and computed fields are explicit metadata; instruction accesses use the same
permission and legalization machinery in every mode. The selected satp MODE
rule additionally ignores an entire unsupported write, after permission checks,
as the prerequisite above explains. No state is silently added by a view.

The executor interprets generated privilege effects over that metadata. Trap
delivery records cause/value/EPC, applies delegation and the privilege stack,
and selects the handler PC. xRET restores the declared stack and saved PC.
ECALL's cause depends on the originating mode; EBREAK delivers its declared
breakpoint exception. A delivered trap ends the instruction's own effects.
Atomic CSR read/write checks preserve the destination on refusal; the worked
matrix below checks both successful and refused boundaries.

SRET, WFI and SFENCE.VMA retain their mode and interception rules. Counter
access uses the M/S enable gates; stimecmp additionally uses STCE, and S satp
access obeys TVM. The [runtime contract chapter](contract-runtime.md) gives
mode, counter, timer and trap examples; [Sv39](sv39.md) explains translation,
protection and TLB behavior. WFI's wait state and wake behavior are documented
in the [interrupt and wait chapter](interrupts.md). Uniform permission checks do not imply that
all instructions or all platform configurations have been independently
accepted: the profile's GS report still names its open evidence axes.

The original ten checkpoint paragraphs, including pre-bind instruction/guest
counts, staged generation proofs and historical Sail attempts, are preserved
byte-verbatim in `docs/tasks/archive/P4-SYSTEM-book-c32b0.md`. Its inverse map
reconstructs this entire source chapter at the named commit. Current features,
all worked CSR examples, controls and finite limits remain here.


## Direct CSR access contract observations

`OB-GC-CSR-ACCESS` now binds two direct execution witnesses and the existing
`mm-csr-rw`, `mm-csr-ro-write`, `mm-csr-legality-s` and `mm-csr-legality-u`
companions. All six Zicsr forms operate on the pre-instruction source and old
CSR value, including `rd=rs1` aliases. Immediate sources are unsigned five-bit
values. A refused access delivers illegal-instruction atomically: neither the
CSR nor the destination changes before the trap.

| Forms | Read | Write |
| --- | --- | --- |
| CSRRW / CSRRWI | Only when rd is nonzero | Always, even with a zero source |
| CSRRS / CSRRC | Always | Only when the rs1 **field** is nonzero |
| CSRRSI / CSRRCI | Always | Only when the five-bit immediate is nonzero |

For example, starting with `mscratch=0x80` and `x6=0x05`:

```asm
csrrw x6, mscratch, x6   # x6=0x80; mscratch=0x05 (the old x6 is the source)
csrrsi x5, mscratch, 31  # x5=0x05; mscratch=0x1f (31 is zero-extended)
csrrci x0, mscratch, 6   # mscratch=0x19; x0 stays zero
csrrw x0, mscratch, x0   # mscratch=0; the CSR is not read
```

A nonzero source register **containing zero** still requests a write. This
matters for read-only counters and for the selected conservative FP policy:

```asm
# FS=Initial, fcsr=0, x6=0:
csrrs x0, fcsr, x0   # no write; FS remains Initial
csrrs x0, fcsr, x6   # explicit unchanged-value write; FS becomes Dirty
# A permitted cycle read is legal, but the corresponding write is not:
csrrs x5, cycle, x0  # reads the pre-boundary count
csrrs x5, cycle, x6  # illegal-instruction; x5 is preserved even though x6=0
```

The finite matrix crosses M/S/U, six forms, source fields 0/6/31,
register values zero/high/all-ones (one input per immediate), destinations
0/5/6/31 and two initial patterns. Its 15 contexts are M/S scratch, cycle
under all four CY enable combinations, stimecmp under all four TM/STCE
combinations, satp with TVM clear/set, fcsr with FS Off/Initial, and one
unimplemented M-level address. The result is **4,480 legal and 8,480 refused
boundaries**, with exactly 25,920 instruction parcels. High and wrapping
counter seeds distinguish pre-boundary reads, retirement and nonretirement.

Below the CSR's address privilege, any access traps. Writes to cycle trap in
all modes. S counter reads need the M enable; U additionally needs the S enable.
S stimecmp needs both TM and STCE; M bypasses those gates. S satp access traps
under TVM, while M bypasses TVM. U cannot access either supervisor address.
FS Off refuses fcsr in every mode. Satp starts Bare so S/U fetch is valid;
the [whole-write prerequisite](sv39.md#unsupported-satp-mode-ignores-the-whole-write)
separately covers prior Sv39 values and unsupported MODE. These cases do not
claim exhaustive legalization of every CSR field.

Expectations exist before execution. Each observation compares all GPRs/FPRs,
26 raw CSR storage owners, PC/mode, reservation, TLB entries and FIFO cursor,
wait state, the full memory image, request order, parcel count and outcome.
Refusals check cause 2, the original word in mtval, instruction-start mepc,
M privilege-stack delivery, one cycle increment and no retirement. Only the
two necessary fetch requests are allowed. Thirteen wrong instruction effects,
sixteen corrupted observations and actual disabled permission/suppression/
observer predicates discriminate the witness. The independent author agrees
on 12,096 cases; its 864 unknown-address cases are named vocabulary refusals,
not independent confirmation of a trap. The core witness checks those traps
directly against the literal address-map rule.

**No-read evidence limit.** None of these selected CSRs has a read side effect.
A deliberately added same-CSR read on CSRRW/CSRRWI with rd=x0 passes the full
dynamic observation. That passing control is retained. A separate inspection
of the published compiled semantic table checks that the selected rd=0 branch
is a write-only CSR action with operands that cannot read a CSR. It rejects
the extra-read table, and disabling the inspection makes its control fail.
This is table evidence for suppression, not an observable read count at the
memory boundary. No tracing API or fictional environment request is implied.
