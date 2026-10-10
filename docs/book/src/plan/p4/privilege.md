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

The leaf runs in eight checkpoints; slice (c) split cleanly into (c1) — zero Rust — and
(c2). Slice (a): the upstream census measured what the brief delegated — Zicsr's
six instructions are real rows in riscv-opcodes' `rv_zicsr`, mret/wfi live in `rv_system`,
sret/sfence.vma in `rv_s`, and Zicntr's rdcycle/rdtime/rdinstret exist **only as
pseudo-ops of csrrs** — Zicntr adds no encodings, so the fragment layer gained a
`(pseudo …)` construct (assembler spellings the disjointness gate decides under a
specialization rule, never instructions). The new tables are pinned in the unit's own
`references.sexp`; the fetch route follows upstream's move of the tables to `extensions/`
(byte-identical, measured). The assembler gained the csr operand field (positions derived
from the pinned `arg_lut.csv`, names from the pinned `csrs.csv`) and profile-derived
IALIGN (32 for rv64i, 16 for rv64gc).

Slice (b): the semantics language learned privilege — eight operators
(`field`, `inst`, `mode`, `csr-state`, `csr-read`, `csr-write`, `trap-deliver`, `xret`),
with the CSR permission model carried uniformly inside `csr-read`/`csr-write` (address
mode bits, read-only bits, counter-enables, STCE, TVM) rather than per instruction, and
the WARL legalization of writes explicitly deferred to the state document's per-field
tables. ECALL/EBREAK are **refined by declaration** — the composition's first real
`(refines …)`, causes 8/9/11 by mode — while rv64i's own rules stand untouched.

Slice (c1): the state layer learned the same shape — a `privilege_mode` element (hart
state, not a CSR) and the `csr` construct with per-field WPRI/WARL/WLRL tables, and the
rv64gc state document itself: all 33 committed CSRs with their disciplines, resets and
locators, the SEM-08 hidden-state census re-earned for the privileged state. Because a
state document inside the unit is a refused route contradiction until the flip, it is
authored and fully validated from a staged path and moves unchanged at the flip — and the
gates gained the two arms the exploration measured missing: the profile's CSR list and the
state document's CSR set must agree exactly, and every CSR (and the mode) must carry a
reset. gen_state now emits both profiles, rv64i byte-identical; its composed-reset
cross-check caught a hand-computed wrong mstatus reset in the document while it was being
written. Slice (c2) recorded the flip-bound rule: a tracked generated module needs a
tracked canonical input, so the rv64gc modules land with the descriptor at the flip.

Slice (d): the engine learned the machinery. `semulith-core`'s new `privilege` module owns
trap delivery (delegation, the privilege stack, the trap record, pc←xtvec), `xret`, the
uniform CSR permission model, and the WPRI/WARL/WLRL legalization — as engine code over
the generated tables, never per-instruction. Both generators parameterize to the second
unit (rv64i's surfaces regenerate with only the embedded generator fingerprint changed),
the ELF loader's IALIGN is the profile's data (32/16), and the guest corpus's set is
directory-derived. The scratch execution proof runs six assembled guests through the
generated rv64gc modules and the tracked machinery — the CSR disciplines, trap delivery
with and without delegation, the mode pops, the per-mode legality of wfi/sret/sfence.vma,
the counter and TVM gates — 26/26.

Slice (e): the unit's documents grew to the flip's shape. The instruction census is the
full 65 forms by the mandated dual edit — the Zicntr counter reads are census forms (the
specification's listings name them) realized as csrrs specializations in the encoding, a
decision recorded in the profile itself. The requirements and obligations catalogues carry
the base corpus as a derivation-proven mirror of rv64i's (a new RECORD-SCHEMA rule is the
governor, registered in the fact-ownership registry) plus the new forms' authored records.
And the flip's encoding composition — base plus Zicsr, Zicntr and the privileged system
fragment, the unbound extensions declared as slots, partial declared rather than inferred —
is authored, collision-checked and staged, its bytes exactly the flip's bytes.

Slice (f): the corpus runs. All 49 rv64i guests execute on the rv64gc engine through a
scratch runner that wires the declared memory map, fault delivery on the pinned cause
vocabulary, and the verify runner's per-step register-change comparison — 49/49, with
exactly three expectations re-derived **by design**: under IALIGN 16 the misaligned-jump
guests' 2-mod-4 targets are legal (the C extension), a declared profile difference, never
a soundness contradiction. Thirteen mode-matrix guests then exercise the new forms in
each mode — CSR access semantics and per-mode legality, trap delivery and delegation,
the xRET mode pops and the MPRV/TSR/TVM/TW gates, counter and stimecmp enables,
read-only and WARL behaviour — every expectation derived from the pinned chapters before
the run and falsified against it (62/62 green). The coverage rehearsal reads 65/65: every
declared form is executed by at least one guest. Execution itself caught fourteen stale
vector deltas and two mode-discipline bugs in the guests — re-derived, never fitted.

Slice (g): the interaction matrix, declared. Seven axes from the leaf's own vocabulary —
the four layers the mirrored corpus already carries (fault, alias, boundary, progress),
plus legality (mode-dependent permission and refusal), delegation (interception routing),
and restart reframed guest-shaped: the xret/xepc return discipline is observable by
guests, where rv64i needed a mechanism. All 28 cells are dispositioned across the 62
staged guests — three honestly reported as not composed in this corpus — and the check
rehearsed green against the staged unit (28 cells, every disposition resolves). The
difference-id rule measured two mirrored files whose rv64i divergence pin is false for
this profile (Zifencei is declared, its slot unbound); they were re-derived with the
reason recorded, steps unchanged.

Slice (h), part 1 — **the atomic flip**: everything the staging proved now stands
tracked. The unit carries its encoding composition (partial, its six unbound
extensions declared as slots), the 33-CSR state document, the 62-guest corpus and the
interaction matrix; the dossier's route is `generated-definition`; and the tracked
engine runs the whole corpus — a new `exec_rv64gc` evaluator (with the trap-END
discipline the scratch runner measured: a delivered trap ends the step) drives all 62
guests through the verify crate's tests, 62/62 against the specification-derived
expectations. The generated mirrors are tracked because their inputs are tracked in
the same commit; rv64i keeps its default and its byte-exact behavior, with the CLI's
profile now an explicit runtime selection (rv64gc wired for run and demo, honest
refusals elsewhere). The flip measured and closed four gate gaps on the way — a
refinement relation one checker didn't honor, a pseudo-blind coverage leg, the
one-pair generator censuses, and a generated module that had to become the code
formatter's fixed point. Part 2 attempts the Sail privileged matched experiment and
closes the leaf.

Slice (h), part 2 — **the Sail experiment and the leaf's close**. A matched Sail 0.14
configuration (privileged 1.13, the declared selection, no devices, WFI a nop except
in U) runs the mode-matrix guests, and **11 of 12 agree step-for-step against the
specification-derived expectations** — including the mstatus all-ones WARL read-back,
bit-exact. The two honest boundaries are named with their evidence: Sail does not
implement mstatus.TW's effect on WFI legality (the one divergent cell, routed to the
wfi leaf), and its Zicntr requires a CLINT time source our no-device platform
forbids (mm-counters not matchable — the counter rate is the environment's own
declaration). The leaf's acceptance — the same instruction's behaviour tested in
each supported mode — stands on the mode matrix itself: thirteen guests, every cell
a mode crossing, falsified by the tracked engine and differentially confirmed.
Next: `.3` — Sv39 translation and protection.

rv64i's generated surfaces re-derive byte-identical through every slice, and all thirteen
new forms assemble and round-trip through the second decoder exactly. The route flip to
`generated-definition` remains the leaf's last, atomic commit.

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
