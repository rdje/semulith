# P4-SYSTEM.13 c32b0 — historical privilege implementation timeline

Finite immutable capture from source commit `21a997fbc565598101a7c0f7b2b82391e1c3862d`, SEMULITH-P4-0178.
The ten whole original checkpoint paragraphs remain in their original order.
Current privilege features and all examples/controls remain in the book.

To reconstruct the entire source chapter, verify its current proposed bytes/SHA,
replace exactly the replacement bytes at offset with the marked original
payload, then verify source bytes/SHA against the named commit. All offsets and
lengths count bytes. The payload retains its exact original separators.
No later payload is appended here.

## Inverse map

```json
{
  "source": "docs/book/src/plan/p4/privilege.md",
  "commit": "21a997fbc565598101a7c0f7b2b82391e1c3862d",
  "source_bytes": 14486,
  "source_sha256": "bc97a1b69d515c5a9b0af2dd9022084bac7c08e8dc8955720e2901756595382f",
  "proposed_bytes": 8763,
  "proposed_sha256": "b2b80c0d140ec69226f767ca166e1ebaa45672248b03133ea63da830040b74b6",
  "offset": 1828,
  "payload_bytes": 8436,
  "payload_sha256": "a5cfb573a4ac410eb612f88f9a61f6263994990baa0b84aeeb01d7e34642b626",
  "replacement": "The current privilege machinery is driven by the profile's canonical encoding,\nstate and semantic definitions. Zicsr supplies six real instruction forms.\nZicntr's rdcycle/rdtime/rdinstret are assembler pseudo-operations of CSRRS;\nthey add no decoder instructions. Pseudo specialization is checked separately\nfrom encoding disjointness. CSR operand positions and names derive from the\nprofile's encoding and state, and fetch alignment derives from its IALIGN\nselection: 32 bits for rv64i and 16 for this composed profile. The ELF loader\nuses that same profile alignment. CLI run and demo accept explicit profile\nselection; rv64i remains the default, and commands whose machinery is still\nrv64i-specific refuse rv64gc by name.\n\nThe state definition owns M/S/U mode, 33 CSR names with 26 underlying storage\nowners, resets and field disciplines. Views share their owners. WPRI/WARL/WLRL\nand computed fields are explicit metadata; instruction accesses use the same\npermission and legalization machinery in every mode. The selected satp MODE\nrule additionally ignores an entire unsupported write, after permission checks,\nas the prerequisite above explains. No state is silently added by a view.\n\nThe executor interprets generated privilege effects over that metadata. Trap\ndelivery records cause/value/EPC, applies delegation and the privilege stack,\nand selects the handler PC. xRET restores the declared stack and saved PC.\nECALL's cause depends on the originating mode; EBREAK delivers its declared\nbreakpoint exception. A delivered trap ends the instruction's own effects.\nAtomic CSR read/write checks preserve the destination on refusal; the worked\nmatrix below checks both successful and refused boundaries.\n\nSRET, WFI and SFENCE.VMA retain their mode and interception rules. Counter\naccess uses the M/S enable gates; stimecmp additionally uses STCE, and S satp\naccess obeys TVM. The [runtime contract chapter](contract-runtime.md) gives\nmode, counter, timer and trap examples; [Sv39](sv39.md) explains translation,\nprotection and TLB behavior. WFI's wait state and wake behavior are documented\nin the [interrupt and wait chapter](interrupts.md). Uniform permission checks do not imply that\nall instructions or all platform configurations have been independently\naccepted: the profile's GS report still names its open evidence axes.\n\nThe original ten checkpoint paragraphs, including pre-bind instruction/guest\ncounts, staged generation proofs and historical Sail attempts, are preserved\nbyte-verbatim in `docs/tasks/archive/P4-SYSTEM-book-c32b0.md`. Its inverse map\nreconstructs this entire source chapter at the named commit. Current features,\nall worked CSR examples, controls and finite limits remain here.\n\n"
}
```

## Original timeline

<!-- c32b0 original timeline -->
````text
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
````
