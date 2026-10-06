# P4.2 — Privilege and mode transitions

**Status:** Landed, flipped, and closed (slices a–h, 2026-10-03)

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
