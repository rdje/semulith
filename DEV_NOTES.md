# DEV_NOTES.md

## _(2026-10-03)_ — a latent bug censused to extinction; the mirror is a closure, not a list (P4-SYSTEM.2 slice e)

Execution of the `.2` brief's checkpoint (e) measured:

- **The dropped-`(extensions …)`-form bug had SIX readers, not four.** Slice (a) fixed the
  resolver; slice (b) the corpus gate; slice (d) gen_definition. Writing slice (e)'s
  checklist with the claim "the pattern is gone" sent me to `git grep -n 'ext\[0\]\[1:\]'`
  — which found TWO more (check_exercise_coverage.sh's scope closure, gen_model_book.py's
  ISA derivation), each silent until a composition carries a second extensions form. The
  fix pattern is uniform (every form contributes), the census command is in the leaf, and
  the pattern is now extinct. The lesson the family already owns
  (a checklist claim is a measurement you re-run) fired on my own sentence before commit.
- **The mirror's extent is a closure, not a list.** "The 52 base forms' instruction
  requirements" reads as "the instruction-kind records" — measured, those 9 records cover
  49 of 52: ecall/ebreak ride the event record and fence the memory record, and the
  dependency closure pulls REQ-D-XLEN and REQ-D-ENDIAN. The probe derives the closure from
  the owner's catalogue at gate time, so the mirror's extent can never go stale when the
  owner's corpus grows. The governor is RECORD-SCHEMA's rule 14, registry-driven by the
  FACT-OWNERSHIP rows — the registration IS the wiring.
- **The MIRROR rule caught my own authored obligations.** The new obligations condensed
  their requirements' statements — rule 9 (the obligation restates its requirement
  EXACTLY) refused them, and the fix was verbatim restatement, not a weaker gate.
- **The fetch leg's census needed the profile's own pin list.** Extending the
  encoding-tables-vs-scope check from the hard-coded base tables to the ledger's pinned
  tables would have counted rv64i's M tables (pinned for the fragment test case, not the
  scope) — the exclusion is BY NAME, recorded; and a pseudo-only table (rv_zicntr)
  contributes its pseudo names, because the spec's Zicntr listings ARE those rows.
- **The aggregate ceiling fired on mandated content.** docs/tasks/ at 63 files /
  1,575,182 B over the 1.5 MiB ceiling by 0.15% — the P4-SYSTEM tree's per-slice
  checklists; re-derived to 3 MiB by decision record (the family's documented lifecycle),
  per-part and count axes unmoved.

Promotion: declined — the governor runs (rule 14), the census is recorded in the leaf, and
the ceiling lifecycle has its decision records. Recorded in the owning leaf's checklist
(LOCKSTEP).

## _(2026-10-03)_ — the byte-frozen enum wall; a rotated digest exposes an arm's assumed first digit (P4-SYSTEM.2 slice d)

Execution of the `.2` brief's checkpoint (d) measured:

- **The two-profile shape has a hard wall, measured by construction.** The tracked
  evaluator matches on rv64i's generated `Sem` enum, which DEF-GEN freezes byte-exact and
  which lacks the slice-(b) variants — so the new operators' evaluation arms cannot exist
  in tracked code until the rv64gc definition module is tracked (the flip). Three shapes
  were measured and rejected before the chosen one: parameterizing the evaluator over the
  tree (Rust enums don't extend); a shared evaluator over both Sem types (a second
  evaluator is the OWN-01 failure); moving the Sem vocabulary to a hand-authored module
  (changes rv64i's frozen bytes). What lands tracked instead: `privilege.rs`, the
  MACHINERY over a `PrivilegedHart` trait — the generated rv64gc state module implements
  the trait with the descriptor's tables, and the scratch proof compiles the tracked file
  byte-identically (cmp-verified) against the scratch-generated modules. The evaluator's
  new-variant arms are proven at scratch (the harness's tree-walker) and port at the flip.
- **The WARL seam needed structured data.** Slice (c1)'s prose legalization could not be
  applied mechanically; it became the `(legalize …)` mini-language (`(any)`,
  `(read-only V)`, `(one-of V…)`, `(computed)`) across schema, document, mapping and
  generator — with the cross-checks (a WARL field without one is refused; a read-only
  constant must equal the field's reset). The proof caught my own defect: a CSR with no
  field table (an atomic register) had every write preserve every bit — `covered=0` masked
  the whole word; atomic registers write wholesale.
- **The digest cascade works, and it exposed a fragile arm.** Adding the tracked
  `run-order.txt` rotated the dossier digest; the designed cascade re-derived (reports →
  board pin → board artifacts → platform manifest → both model books). PLATFORM-GEN's
  stale-pin self-test arm mutated the pin by flipping its FIRST CHARACTER — which stopped
  mutating the day the digest rotated to a different leading hex digit; the arm passed a
  mutation that wasn't one. It now rewrites to a fixed wrong value of the same shape.
- **The brief's "51-name list" was 49** (measured); the guest set is now
  directory-derived with the run order as recorded data, cross-checked both directions.
  And gen_definition's composition name list carried the third copy of slice (a)'s
  dropped-`(extensions …)`-form bug — "4 declared instruction(s) have NO semantics: mret,
  sfence.vma, sret, wfi" named it instantly. Three copies of one latent defect across
  three readers of one schema shape — the fix pattern is now uniform (every form
  contributes), and the corpus gates' arms prove it.

Promotion: declined — the digest cascade is machinery with its own gates, the arm fix is
its own evidence, and the wall's reasoning has its decision record. Recorded in the owning
leaf's checklist (LOCKSTEP).

## _(2026-10-03)_ — one reset, one value: the composed-field cross-check fired on the document being written (P4-SYSTEM.2 slice c1)

Execution of the `.2` brief's checkpoint (c) — split into (c1)/(c2), the seam recorded in
the tree — measured:

- **The staging problem is the design.** A state.sexp under `profiles/rv64gc-lab-v0/` is a
  refused route contradiction until the flip, so the 33-CSR document is authored at
  `target/p4-system-2/state.sexp` and validated from there — the gates that discover by
  path were measured first (DOSSIER-SCHEMA scans `profiles/*/*.sexp`, PROFILE-CONSISTENCY
  reads a sibling state.sexp, EXTRACTION the unit dir; none sees target/), and the
  validations were given scratch-path forms (`check_sexp_schema.py` takes the path, the
  new `--csr-cross` probe, `_state_resets` on the scratch dir).
- **The house shape decides the nesting.** The schema kernel's form-field rule refused my
  first draft's `(fields (field …) (field …))` and the 11-child `(candidates …)` wrapper
  by name; the construct repeats bare `(field …)` under `(csr …)`, exactly the
  `register_family` shape. The first draft also overlapped full-width `wpri_rest` rows
  with named bits — an ambiguous legalization table; a coverage probe computed the true
  gap sets.
- **One reset, stated twice, must agree — mechanically.** gen_state composes a CSR's reset
  from its per-field resets and cross-checks the csr-level declared value. It fired RED
  *naturally*, on this very document: mstatus's composite is 0xA0000000 (UXL=2 | SXL=2),
  not the hand-computed 0x300000000. The descriptor was wrong; the check named it; the
  fix was re-derivation, and the self-test arm now keeps it repeatable.
- **gen_state parameterizes, never forks** — the rv64i emission path is untouched (the
  module re-derives byte-identical under the extended generator), and the rv64gc branch
  validates by refusal (undeclared view, duplicate address, uncovered field bits, a
  privileged construct under rv64i — each named) and emits to a scratch out until (c2)
  wires the consumer. The csr name↔address ownership migration is deferred to the flip
  with its probe recorded (33/33 exact against the pinned csrs.csv).

Promotion: declined — the consistency rules are armed by self-test REDs (STATE-GEN 17,
PROFILE-CONSISTENCY 44, EXTRACTION 9), and the natural RED is recorded in the leaf.
Recorded in the owning leaf's checklist (LOCKSTEP).

## _(2026-10-03)_ — a swap forces the language's reads contract; a checker hard-coded to one file checks the other three never (P4-SYSTEM.2 slice b)

Execution of the `.2` brief's checkpoint (b) measured five things:

- **The register-swap hazard decides the reads contract.** csrrw exchanges a register with
  a CSR; a state-threaded `(reg rs1)` after `(set (reg rd) …)` is wrong exactly when
  rd==rs1. No RV64I rule reads a register after writing one, so the language adopted the
  contract without changing any existing meaning: register reads see the PRE-INSTRUCTION
  register file; memory and CSR reads see state at their evaluation point (the
  self-modifying-code discipline is untouched); `(pc)`/`(inst)` are frame constants. It is
  stated once in schema/semantics.sexp, the language's own home.
- **A pseudo's semantics specialize by NAME.** rdcycle ≠ csrrs, so the compose rule's
  `(refines …)` mechanism does not apply and none is needed — the pseudo's own rule IS the
  specialization (rs1=x0 → no write; the row's fixed address), exact because the counter
  gating lives in csr-read's uniform permission model rather than per-instruction. The
  checker indexes `(pseudo …)` operand rows: checked, never demanded nor coverage-counted.
- **The corpus gate's COMPOSE leg had slice (a)'s dropped-form bug.** A silent override in
  the SECOND `(extensions …)` form was invisible — the new self-test arm was proven RED
  pre-fix ("right verdict, wrong reason") before the one-hunk repair, the `.1` discipline.
- **check_citations was a single-file tool.** Its main() hard-coded rv64i.sem.sexp, so the
  three new sem files' locators resolved against nothing. The `--corpus` mode derives the
  binding — each sem file checks against every profile pinning all its cited source-ids,
  and a file no profile fully pins is named. rv64i.sem now resolves under THREE profiles
  (netboard pins the same unpriv pages — a resolution never previously run); the new files
  resolve 8/8, 3/3, 4/4 under rv64gc's 21 pins.
- **The mstatus field positions are figure images again.** The specification's encodings-
  as-images pattern recurs one level down: TSR/TW/TVM/MPRV exist in the pinned chapters
  only as figures, so upstream's checked-in `encoding.h` (masks) and `causes.csv` (trap
  causes — in the cache since the rv64i era, never pinned, measured byte-identical) joined
  the rv64gc ledger. Also measured: `(xret m)`'s bare mode symbol read as an operand
  reference — x is the architectural mode code (3=M, 1=S), the xPP encoding itself.

Promotion: declined — the contracts are data in the schema and the pins, and every new
rule is armed by self-test REDs (semantics 8→15, citations 10→13, corpus 7→8). Recorded
in the owning leaf's checklist (LOCKSTEP).

## _(2026-10-03)_ — the first multi-extension composition exposed two latent gate defects; a pseudo-op is not an encoding (P4-SYSTEM.2 slice a)

Execution of the `.2` brief's checkpoint (a) measured four things the brief did not know:

- **Upstream restructured without changing a byte.** riscv-opcodes moved every instruction
  table from the repository root to `extensions/`; rv_i/rv64_i/rv_m/rv64_m hash
  byte-identical to the rv64i pins. The fetch route's `master/<file>` would have 404'd any
  fresh fetch — verify-only never noticed because it only hashes what is on disk. The route
  now maps `rv_*` under `extensions/` and a scripted fresh re-fetch proved it live.
- **Zicntr adds no encodings.** rdcycle/rdtime/rdinstret exist upstream only as `$pseudo_op`
  rows of csrrs; emitting them as instructions collides with csrrs by mask math. The
  fragment layer gained the `(pseudo …)` construct — assembler spellings the disjointness
  gate decides under a specialization rule (every word a pseudo assembles must already be a
  composed instruction's word; an unrealized pseudo "extends the encoding space it is
  declared not to touch", a partial overlap is "the collision rule one level down"). The
  fragment declares the dependency the rows state: `(requires "riscv/rv64i")
  (requires "riscv/zicsr")`.
- **Two latent defects, no reproducer until today.** `resolve_composition` read only the
  FIRST `(extensions …)` form (`ext[0][1:]`) — every later form was silently dropped, and no
  tracked composition had ever carried two. And the disjointness checker printed
  `DUPLICATE NAME(S)` while returning 0 — the verdict text even claimed "no duplicate
  names". Both fixed at root and armed by new self-test RED arms (disjointness 8→12,
  unit-composition 8→9); the `.1` discipline held: measured in execution, fixed at root.
- **IALIGN was a hard-code; csr was a label.** The assembler's label pass resolved names
  for EVERY operand position and ate `csrrw x1, cycle, x2`'s csr name; labels now resolve
  only where a label is legal (B/J scrambled offsets), and a csr name falls through to the
  operand parser, which resolves it through the pinned csrs.csv. IALIGN is derived from the
  unit's `profile.sexp` (rv64i 32, rv64gc 16). The operand spelling order (`csrrw rd, csr,
  rs1` — the pinned table lists fields `rd rs1 csr`) is proven by the module's documented
  second decoder: spike-dasm disassembles every emitted word back to the requested
  spelling, all 13 forms exact.

Promotion: declined — the durability is the machinery (the fixes are armed by self-test
REDs; the pseudo and IALIGN designs are data in the schema and the pins). Recorded in the
owning leaf's checklist (LOCKSTEP). Intra-tree follow-ups named there: the Rust-side
IALIGN=32 entry check (slice d), csr-name resolution's migration to the tracked state
document (slice c/f), rdcycle's coverage naming (slice e/f).

## _(2026-10-03)_ — the dossier machinery had no lifecycle stage for "resolved but no definition yet" (P4-SYSTEM.1)

The `.1` brief assumed the schema already supported the resolution's fields; measured in
execution, the real gap was lifecycle, not fields: EXTRACTION discovers every tracked
`profiles/*/profile.sexp` and refuses a bare processor unit (no encoding.sexp → CANNOT
JUDGE), so a new CPU unit could not be tracked below engine-readiness without a dodge.
The fix followed the by-declaration discipline (the device-model precedent): a fourth
vehicle route, `profile-resolution`, which the three definition-pipeline gates honor as
"nothing to judge yet" — and refuse when contradicted by an encoding, state census, or
guest corpus (the anti-drift property is the point: the route flips to
`generated-definition` the day the pipeline starts, and the full contract attaches).
Two adjacent fixes measured the same day: `check_citations.py` assumed bare page
filenames under the snapshot's `unpriv/` (the privileged pages need subdirectory `file`
fields; the cache root now derives from the declaration, and the declared cache-only
pins are skipped by name), and `gen_platform.py`'s ISA derivation sorted the extension
letters — canonical order is the declaration's, preserved.

Promotion: declined — the by-declaration discipline has its decision records
(`decision_device-applicability-by-declared-vehicle` and kin), and the route's behavior
is armed by self-test REDs in three gates. Recorded in the owning leaf's checklist
(LOCKSTEP).

## _(2026-10-02)_ — the frozen contract is not a live doc, and a pin nothing re-derives is display only (P5-BOARD.6)

Two findings from the platform-manifest leaf, both caught by the gates rather than by
review:

- **The delivered contract is frozen — route announcements to the live surfaces.** The
  `.6` design brief planned a paragraph in `docs/ARCHOGEN_INTEGRATION.md` §3 noting the
  manifest now exists. The file is a `frozen-in-place` row of the delivered planning
  package; DELIVERY-PROVENANCE fired RED on the edit and the edit was reverted. The
  announcement lives where project facts live: the task tree, the board DOSSIER, the
  board book's new manifest chapter, and the project book's plan chapter. The design
  input stays the supplied contract — read-only, cited, never amended
  (`docs/provenance/planning-package-v0.2/dispositions.tsv`).
- **A pin nothing re-derives is a display string.** The board's `dossier-sha256` was
  recorded with the right intent ("a digest match against a newer dossier is a
  finding"), but the census showed one consumer and it was the book generator's
  *renderer*. The export generator now re-derives the digest from the live dossier at
  every run (`gate_report.dossier_digest` — the one computation, factored out of the GC
  report builder and measured byte-identical) and refuses a stale pin by name; the
  PLATFORM-GEN self-test arms it RED. The leaf's own `endianness` edit was the first
  real exercise of the cascade: dossier → GC-REPORT → pin → export.

Promotion: declined — both findings' durability is the machinery itself (the doctrine
fired; the refusal is armed by a self-test RED), and the write-down-what-the-gate-
catches discipline already has its cards. Recorded in the owning leaf's checklist
(LOCKSTEP).

## _(2026-10-02)_ — the summary sentence is not the operation chapter: a declaration read from §1.10 failed §3.6's mode exclusivity (P5-BOARD.4)

The board's NIC declaration carried `access-widths 16 32` from the datasheet's §1.10
summary ("supports 32-bit and 16-bit bus transfers") — written at `.1`, inherited by the
dossier (the 16-bit pairing latch joined the model-state census *because the board
declared the width*). The composition verdict's strap decision forced the real question:
§3.6 makes the bus width a strap-selected, mode-exclusive property — 32-bit mode is "the
native environment … no special requirements", and the two-contiguous-access pairing is
16-bit-*mode* operation. With D32 strapped (the obvious choice for a 64-bit host), a
16-bit access has no datasheet-defined behaviour at all, so the declaration was measured
false and narrowed to 32 — and every downstream record justified by it (the census
latch) flipped with its reason stated. The instrument that caught it is the durable
part: the deferral was *data* (an obligation marked `composition_disposition
"required"`), so the verdict could not close without deciding the strap, and deciding
the strap forced re-reading the operation chapter. Decline-to-promote note: the finding
itself lives in the verdict + BOARD-VERDICT, and the measure-against-the-source
discipline already has its knowledge cards — no new card.

Also worth remembering: the per-assumption discharge is the obligation-graph half only —
its platform-dependent edges land on the *laboratory* guarantee (`OB-PLATFORM`), so a
green discharge would pass with a CLINT bolted on. The board-level satisfaction has to
be its own checked data (the `satisfies`/`answers` edges), which is why BOARD-VERDICT
has three legs instead of one.

## _(2026-10-02)_ — the ceiling taxed a property the file could not have: the instrument must match the failure mode (P5-BOARD.12)

The day after the composed-unit bound raise, the director delegated the policy question
it stood on ("yours to decision and act upon … SOTA, SIGNOFF and PRODUCTION-GRADE").
The ruling: a per-part byte ceiling exists to catch silent accretion in
hand-maintained files, and a regeneration-gated derived file cannot accrete silently —
every byte is re-derived on every commit, and its size is a pure function of
already-bounded inputs. So the interim 128 KiB raise (one day old) was the right
stopgap and the wrong instrument, and the gate went two-tier: authored members keep
the 64 KiB ceiling, derived members are exempt **as a checked property** — a
fact_ownership.tsv mirror row with a regeneration-doctrine governor (closed set), never
a declaration. The exemption consuming the FACT-OWNERSHIP registry is the part that
makes it signoff-grade: the registry is already completeness-checked (every governor
registered, every corpus pair named), so no second declaration surface exists to drift,
and an authored file cannot smuggle under the exemption because nothing regenerates it.

Two implementation details worth remembering. The per-part loop previously inspected
only the single biggest member (`sort -rn | head -1`) — a second over-ceiling file was
never even reported; the two-tier rule forced judging EVERY member, which is strictly
stronger for authored content too. And the self-test harness gained the arms in the
real corpus's shape: the RED for an authored file over the ceiling fires on fixtures
because the real corpus's authored members are all (correctly) under the ceiling — a
control that only ever sees GREEN in production is exactly the kind that must be seen
RED in the harness. And a third, caught by DERIVED-COUNTS itself: the regen-set arms
were first written under a new `armregen` helper the enumerator does not count, so 2
of 17 arms were invisible to the arm total (357 ≠ 359) — fixed by folding the probe
into `arm`'s optional `[cmd...]` form rather than teaching the enumerator a third
idiom. New self-test idioms are not free: the arm total is a census, and a census
only counts the shapes it knows.

Lesson: **promoted** — `docs/knowledge/a-byte-ceiling-applies-to-authored-content.md`
(the question form + the checked-exemption pattern; the ruling itself is
`decision_derived-members-of-bounded-families`).

## _(2026-10-02)_ — a freshness gate deferred to "the first tracked board" lands exactly once (P5-BOARD.3)

`compose_units.py` shipped with its freshness proof explicitly deferred — "lands with
the first tracked board" — and P5-BOARD.3 was that board. The shape that landed: one
generator (`gen_board.py`, boards discovered by declaration, never a hardcoded id),
seven artifacts per board, and the BOARD-GEN doctrine re-deriving all seven on every
commit. The compose factorization is the part worth remembering: `compose()` took a
manifest FILE, which pins part resolution to the manifest's location — useless inside a
generator that derives the manifest itself and must compose in scratch. The fix was not
a second materialization path but `compose_resolved(comp_id, part_dirs, out_dir)` — the
manifest-file entry point and the generator both land on it (the refactor measured
byte-identical on the real parts, self-test 9/9).

Two measurements did the design's real work. The FACT-OWNERSHIP probe: placing the
composed catalogues in the board directory tripped the gate's self-test on EXACTLY the
two new restatement pairs — the gate refusing to judge an unregistered corpus is the
registry doing its job; registration (8 rows), not weakening, was the fix. And the
design brief's register-surface containment check turned out NOT implementable: the
device dossiers carry register offsets in prose with datasheet citations (measured in
both `state.sexp` documents and the expectations), never as machine-readable data — so
the generator's refusals are scoped to what board.sexp itself proves (overlap, window ↔
device resolution, executable-mmio, ghost console), and machine-readable offsets arrive
with the device models, where the check belongs. A brief line that says "measured at
execution" is a promise; the honest outcome can be "the data is not there".

Lesson: `promotion: declined` (recorded in the leaf) — derive-from-declaration and
measure-before-design already carry their decision records
(`decision_device-applicability-by-declared-vehicle`, `decision_gate-applicability-by-
declared-vehicle`); the compose factorization is recorded with the leaf and in
`compose_units.py`'s own docstring.

## _(2026-10-02)_ — the channel answered in hours; the survey's excluded layer was our own catalog (MCU-DOCS.2)

The twelve MCU requests came back 12/12 fulfilled the same day — the channel's report
(`build_responses.py --report`, rc 0) is the verification entry point, and the adoption
pattern from P5-BOARD.9 (adopt → fetch with digest re-verification → mark our own file)
carried unchanged. The routes the channel measured are worth reading in the answers:
Arm's documentation-service API works; NXP/Microchip/ST's live URLs 404/403/reset to
automated clients and the Wayback captures of the same official URLs carried the bytes.

The execution's real event: the RP2040 datasheet answer read "already held before this
request" — and it was held **twice**: corpus-side, and in our own tracked catalog as
`RP2040-DS` since 2026-09-14 (digest-identical, cached). The `.1` survey had measured
the corpus's proposals feed, not the corpus tree, and not our catalog — the
survey-sampling failure class from MODEL-METHOD.13 recurring at a second layer. Fixed
at root: no duplicate record adopted, the request's answer records the redundancy, and
the knowledge card gained the three-layer "already held" rule with the cheap
complement-check commands.

Lesson: **promoted** — `docs/knowledge/a-survey-that-found-things-can-still-have-missed-things.md`
(the recurrence + the three-layer rule).

## _(2026-10-02)_ — the reading-experience audit's yield was drift, not style (BOOK-APPARATUS.2)

The first audit pass against `decision_mdbook-incremental-engaging` ran as six parallel
read-only chapter-group reviews with the decision's four criteria operationalized
(incremental build-up; motivation before mechanism; layered density; both-audiences
engagement), each returning per-chapter verdicts with line-level evidence. The signing
discipline: **every flagged item was re-verified against the repository before any edit**
— and that verification caught one audit false-positive class (a `grep -c` miscount of
the rv64i profile's inline decision forms; the real count is 28, verified by enumerating
the ids) and one of my own typos (a search string that silently didn't match —
`grep`-verified after the edit, not assumed).

The measured surprise: the audit's yield was **factual drift**, twelve places where
hand-carried repository facts in the book had gone stale — the class DERIVED-COUNTS was
founded on, living in chapters no enumerator covers. Three genuine style violations
(a duplicated sentence, a cold open, a 68-line accreted list item) were the minority.
Two mermaid blocks rendered as raw source in the book; replaced by text flows rather
than adding `mdbook-mermaid` (a dependency the project hasn't sanctioned).

Lesson: `promotion: declined` — the audit method is the decision record's own
consequence clause (`.2` owns the pass; the pass is recorded); the drift fixes are
per-slice history.

## _(2026-10-02)_ — registration day: the enumeration follows the declaration (P5-BOARD.11)

Registering the first board and the first devices measured exactly where the machinery
was processor-shaped: not only the two `sibling-crate` conditionals the `.2` routing
note had named — the emitters also *load* `references.sexp` (absent from all three new
dossiers; the board has no `profile.sexp` at all), `emit_contracts` reads
`interactions.sexp` and globs `guests/`, and the MATERIALS-BILL gate's COMPLETENESS half
would have reported CANNOT JUDGE for all three. The generalization is one function
(`unit_shape`: `board.sexp` present → board; the vehicle route otherwise) consumed by
both the generator and the gate, with the census per shape (`shape_contracts`) and the
fragments carrying route-honest content — a device has no encoding space and pins no
reference models, and the bill SAYS so rather than omitting the chapters. The board's
pinned-specifications fragment enumerates the composition pins straight from
`board.sexp` — the definition's own data becomes the bill's specification surface.

Two measurement notes worth keeping: the pre-fix refusal was re-verified by running the
parent commit's generator from git (`git show <sha>:scripts/gen_model_book.py`), not by
trusting the code reading; and the processor books' regenerated fragments were proven
byte-identical modulo the embedded generator hash (`diff` with the Generator line
filtered — empty) before regeneration replaced them. The BREADTH report's stale "2
registered units" turned out to live in the GENERATOR's hardcoded prose, so the fix
landed there and the report regenerated (the GATE-REPORT drift gate would have refused
a hand edit — the derived surface was edited at its source).

Lesson: `promotion: declined` (recorded in the leaf) — derive-applicability-from-the-
declaration already has its decision records
(`decision_device-applicability-by-declared-vehicle`,
`decision_gate-applicability-by-declared-vehicle`); the regenerate-vs-edit and
verify-the-parent's-behaviour techniques are the house's standing rules.

## _(2026-10-02)_ — the second device dossier: content only, and the PDF text layer lies (P5-BOARD.10)

The LAN9118 dossier (`lan9118-lab-v0`) needed **no machinery edit** — the `.2`
by-declaration generalization was measured sufficient at the design brief, and the
measurement held: every gate derived the device route from the `vehicle` declaration on
first contact. The leaf's substance was the datasheet itself (109 pages; a real MAC+PHY,
not a UART): 52 mirrored records against the UART's 19, three indexing levels (direct
CSRs → MAC_CSR synchronizer → MII PHY bridge), and mirrors **generated** from
requirements.sexp (`target/gen_nic_mirrors.py`) so the 52/52/52 verbatim discipline is
impossible to break by hand — the gate would refuse drift anyway, but not hand-writing
it is the stronger guarantee.

The two extraction hazards, both measured and both now durable: (1) `pdftotext -layout`
and `-raw` **disagree on Table 5-1's Default column** (two-column pages scramble row
pairing) — per-register sections are the authority, and arithmetic cross-checks confirm
(TDFREE `1200h` = Table 5-3's 4608 B at the default split); (2) §3.11's "2 s"/"100 s"
reset times are **the PDF's own text layer mis-mapping µ to ASCII s** (hexdump-verified —
not an extraction drop), internally contradicted by §5.3.13's clean "100us" and §3.11.4's
own 100 ms bound. Only cleanly stated figures were pinned; the defect is recorded in
`REQ-D-NIC-RESETS`.

The composition findings are the leaf's sharpest output: FREE_RUN/GPT_CNT/INT_DEAS are
guest-readable time sources inside a device whose CPU contract excludes all of them
(`REQ-D-NIC-TIME-SOURCES` — frozen/deterministic, never wall-clock, never the retired-
instruction count; `.4` owns the verdict), and the PHY link scene under a recorded-trace
wire (`REQ-D-NIC-PHY-LINK`). The `profiles/` per-part bound bit for the first time
(32→64 KiB; `decision_profiles-family-five-units`).

Lesson: **promoted** — `docs/knowledge/a-pdf-text-layer-is-not-the-page.md` (the two
text-layer failure modes and the verify-with-hexdump rule).

## _(2026-10-02)_ — a device dossier reuses the machinery by declaration, and a datasheet's silences are requirements (P5-BOARD.2)

The first device unit (`sifive-uart-lab-v0`) taught the dossier machinery its third shape
(after generated-definition and sibling-crate): `vehicle (route device-model) (comparison
register-expectations)`. The load-bearing design choices:

**Applicability is derived, never exempted.** The instruction-shaped gates
(EXTRACTION, EXERCISE-COVERAGE, INTERACTION-MATRIX) read the `vehicle` declaration and
derive what applies: the device answers the legs it honestly can (every state element a
reset — the FIFOs' resets are recorded as *"unspecified", sourced to the measured silence*,
which satisfies the contract without inventing behaviour; every obligation a POS+NEG pair)
and the rest is n/a *by declaration* — with contradiction = RED in both directions (an
`encoding.sexp` or a `guests/` corpus beside the declaration refuses). Anti-drift by
construction: the day P5-BOARD.5's probes land, the gate refuses until taught the device
exercise leg.

**A datasheet's silence is a record, not an oversight.** Six of the nineteen requirements
are `unspecified`-category non-commitments — the sharpest found in execution: §13.8's
watermark bits carry a strict-inequality RAISED and a strict-inequality CLEARED condition
each, and the manual never says whether the bit is a pure level of FIFO occupancy or holds
between the two. The `==` boundary and every pre-first-condition value (including the
X-marked resets) are undetermined (`REQ-D-UART-WM-MODE`), so the expectation documents pin
a watermark bit only when its raised condition holds under *every* reading. The first
draft asserted "level conditions" — the dossier's own expected-results discipline caught
it before it ossified, exactly the failure EVD-05 exists to prevent.

**Naming is contract-shaped.** A private `REQ-U-` id prefix (for the unspecified records)
collided with RECORD-SCHEMA's mechanical `D-X` → `REQ-D-X` decision→requirement mapping —
the mapping is the contract, the prefix was convention. The records are now named by their
`source_semantics` category in prose and carry the house id shape; one fact, three
surfaces (requirement, obligation, decision), one wording, mechanically mirrored.

Validation: all dossier documents schema-validate; the three profile-glob gates decide the
device by declaration; every edited check's self-test green (17/9/14/41/7/14/10 arms, 0
fail); `make gate` all doctrines green; the mdBook builds and its index stays byte-exact.

## _(2026-10-02)_ — a board specification is data with its absences declared, and a label is not a source (P5-BOARD.1)

`netboard-lab-v0` is the first board and `schema/board.sexp` the first non-processor
source-of-truth schema. Two design decisions are worth the ink:

**An absence the contract depends on is data, not prose.** `rv64i-lab-env-v0` v0 admits no
guest-reachable time source and no asynchronous event — and both absences must be *platform*
properties to be real (the CPU contract's own lesson: excluding CSR instructions does not
exclude reading `mtime` over MMIO). So the schema gives `timers` and `interrupt-controller`
explicit `(present false)` forms carrying the reason and the obligation ids they satisfy;
an undocumented absence would read as an oversight, and an oversight is how a CLINT slips
in as a "feature" and becomes a `.4` composition rejection. The `satisfies` fields
pre-wire `scripts/discharge_assumptions.py`'s verdict without computing it — declaration
here, computation there.

**Verify the label against the artifact before you inherit it.** The design brief named the
serial device "16550-compatible (source SIFIVE-FU540-C000 v1p5)". A `pdftotext` census of
the pinned PDF: zero occurrences of "16550"; §13 is the SiFive UART (txdata/rxdata/txctrl/
rxctrl/ie/ip/div, 8-entry FIFOs, 32-bit-aligned only). The pin was the intent, the label
was wrong — so the board adopts the SiFive UART and the label is corrected at every record
(`materials/catalog.sexp`, `D-BOARD-UART-KIND`; the tree keeps the brief's original lines
with a dated correction, per the house pattern). Consequence that mattered: the UART's
sourced instance address (`0x1001_0000`, Table 58) collided with the pre-verification
sketch's NIC address — measuring first caught that too. Memory map: RAM 2 GiB at
`0x8000_0000` (the harness's existing DEFAULT_BASE/SIZE, so laboratory guests run
unchanged), UART at the FU540 instance address, the LAN9118 in a 256-byte window at
`0x1002_0000` (Table 5-1's direct-register span, offsets 0x00–0xFC).

Scope routing: registration of the board unit (`materials/units.sexp`, the `kind` edit,
the per-unit book) is deferred to `.3` — the registry admits a new kind "the day a real
unit needs one", and registration day carries UNIT-BOOKS / MATERIALS-BILL /
book-generator / BREADTH-prose consequences (all censused before deciding) that belong to
the materialization leaf, not to a specification. The third `profiles/` directory
re-derived the family bound to 3× by the standing arithmetic; nothing fired (142 < 240).

## _(2026-10-02)_ — the book's index is a function of the book, not a page someone keeps (BOOK-APPARATUS.1)

The director's apparatus directive audited against the real book: the glossary cannot fork
(`docs/book/src/glossary.md` splices the canonical `docs/GLOSSARY.md` at build time), the two
annexes already match the directive's definition — and the **index was absent**. It now exists
the only way this repository tolerates a fact about a changing population: derived.
`scripts/gen_book_index.py` reads `SUMMARY.md` (the chapter set, in reading order), the
canonical glossary plus the book's acronym table (the term set), and every chapter's text (the
occurrence set, case-insensitive and word-bounded); `scripts/check_book_index.sh` — the 31st
project doctrine, `BOOK-INDEX` — regenerates in memory and refuses drift, with six self-test
arms fired RED before registration (hand-edit DRIFT, stale-behind-edited-chapters DRIFT,
missing chapter and missing SUMMARY refused **by name**). The generator refuses what it cannot
emit rather than guessing, per house style. One build-exposed defect fixed at root: the
generator's printed term count was a fudge factor (`47` against the real `40`) — now derived
from the emitted rows. The annex policy is stated where a reader meets it
(`docs/book/src/introduction.md`): chapters stay readable top to bottom; what is too technical
for the main line lives in an annex. The directive's second half (incremental buildup, both
audiences engaged) became `decision_mdbook-incremental-engaging` + `BOOK-APPARATUS.2`; the TOC
request was withdrawn by the director — the mdBook sidebar is the TOC, and the contents page
built to satisfy it was reverted as redundant.

Validation: `gen_book_index.py` → 15,019 B / 40 terms; `mdbook build docs/book` rc 0;
`check_book_index.sh --self-test` 6/6; `check_doctrines.sh` all green.

## _(2026-10-01)_ — an answered channel still reads `open` until you flip it (P5-BOARD.9)

The second chipdoc incident, from our side: the acquisition agent answered all ten
P5-BOARD.8 requests (5 fulfilled, 5 measured negatives, chipdoc `542a14b`), and
semulith's `requests.sexp` kept saying `open` — because the seam is hard (chipdoc never
writes here) and only WE flip our own statuses. CHANNEL.md §0.3/§0.5 (re-read on the
director's pointer) closes exactly that gap: `catalog/responses.sexp` re-keys every
answer by OUR ids, and `build_responses.py --report` prints the join (run live before
any edit: 5/5, exit 0). The adoption kept the house rules: digests re-verified at
fetch, never trusted from the feed (`materials.py --verify` 52/0); the corpus re-pinned
with the same census (`c4ad8a2`, 5696/293); the proposals feed's records adopted
verbatim in our syntax. The five blocked answers are recorded as RESULTS — each names
what was tried, what returned, and the consequence (LAN9118 is the wired-NIC primary;
SARA-R4 the cellular primary; the AR9271 probe's negative IS its answer) — and the
channel's exactly-once rule means they are never re-filed without a new route. Two
knowledge cards covered the channel with overlapping, drifting scope; the refreshed
split is: `the-chipdoc-request-channel.md` owns the full ask→answer loop,
`the-chipdoc-channel.md` keeps the measured history and cross-links. `P5-BOARD.1`
inherits five sourced network-device candidates plus five closed alternatives.

Validation: `build_responses.py --report` exit 0; `materials.py --fetch` 5× sha256
verified; `materials.py --verify` 52/0; `make gate` all-doctrines-green.

## _(2026-10-01)_ — the capability report is the capstone, and the registry is its claim list (P3-BREADTH.6 slice 3)

The slice order was measured, not planned: a BREADTH report generated before the unit
registration read "1 registered unit" and listed the DSP56300 family — whose evidence
anchors axis 1 had just measured green — as UNCLAIMED. The claim list IS the unit
registry, so the report had to be the leaf's last slice. With slice 2's registration
landed, the builder's three axes are the roadmap's gate text measured from tracked
files by concrete artifact name: axis 1 counts six anchors for the DSP subset (the
declared scope + vehicle, the `.a56`+`.meta` corpus, the crate's 17 tests, the
differential driver, the recorded comparison contract, the registered smoke-agreement
mechanism) plus the scalar unit's GC record; axis 2 requires each of the nine
exercised-case constructs to be DECLARED in its schema AND CARRIED by `dossier_sexp`
(the silent-drop class `.2` eliminated); axis 3 parses the pinned oracle survey for
its per-family verdicts and lists every family no registered unit backs as
**unclaimed**, explicitly — TI C6000 (ABSENT for execution), ADI SHARC (PARTIAL) —
plus the blanket rule: the registry is complete, everything else is unclaimed by
omission. EVD-08's shape holds by construction: no code path to `passed` while an
axis's anchors are absent.

Placement needed a rule, now written in `check_gate_report.sh`'s header: per-profile
reports live under `profiles/<id>/`; a CROSS-ARCHITECTURE gate's report lives at the
repo level (`docs/BREADTH-REPORT.md`) because no profile directory may own it. The
repo-level leg enforces the same regenerate-never-edit rule with the same three
controls; the self-test covers it (12/12; 4 reports in sync — G0/G1/GC regenerate
byte-identical). One cosmetic bug caught by reading the rendered report: doubled
backticks around the probe list (nested f-string quoting). Verdict: `passed` — and
the report's own "what passed does NOT mean" bounds it: exercised cases only, no
DSP56300 family compatibility, no RISC-V conformance upgrade, the slice-gated `.1`
legs named. The tree closes 8/8.

Validation: `gate_report.py --gate BREADTH` → `passed` (5,789 B); GATE-REPORT
self-test 12/12, 4 reports in sync; `make gate` all-doctrines-green.

## _(2026-10-01)_ — the second unit's book, and the ceiling the director raised (P3-BREADTH.6 slice 2)

Registering the unit meant the book generator had to stop refusing the DSP shape. The
three measured walls — exactly one `encoding_source` required (`gen_model_book: REFUSED
— … found 0`, rc=2), `encoding.sexp` required, `state["integer_registers"]` assumed —
each became an extension naming its case: `emit_encoding` emits the declared-vehicle
fragment when the profile declares `(route sibling-crate)` (the refusal stands without
the declaration — applicability derives from the vehicle block, the `.7` decision);
`emit_contracts` treats `encoding.sexp` as the ONE document a sibling-crate unit may
lack (its table row names the deferred lane and the reopening conditions), reads
register families / memory spaces / the hardware stack when there is no integer file,
and counts the `.a56` checkpoint corpus when no `*.expected.sexp` guests exist. The
rv64i regression control is byte-exact: `git diff` over the four regenerated fragments
shows ONLY the generator-digest header line.

The census took judgement, not mechanics: the requires set is C17-in / C14-out against
rv64i's — reset is this unit's own decision (D-RESET-STATE) while interrupts are a named
exclusion — and the 24 rows distinguish `missing` (excluded subsystems with named
closing routes: interrupts, modes, OnCE) from `out-of-scope` (the architecture never
owed them: FP, SIMD, MMU, multicore). SEAM-INTEGRITY caught one under-evidenced ROOT
CAUSE box on the first pass — fixed with the probe's concrete command line, the gate
doing its job (679 boxes re-accepted).

The same slice carries a director ruling, documented on the record: **task-tree growth
is allowed** — the docs/tasks/ per-part rose to 128 KiB
(`decision_task-tree-per-part-growth`) after six forced archive operations in one day,
two of them archiving ACTIVE narratives hours old. The director's invariant stands and
is recorded with it: a bound remains — a file must stay readable in one sitting, growth
is never unbounded; and his standing instruction: **ask for ceiling raises — they are
approved; document everything — requests, rulings, nothing under the radar.** My open
request under it: MEMORY.md (7,168 B) and LIVE_STATUS.md (6,144 B) both needed
fit-trims in three of today's commits — a modest raise (≈ 8 KiB each) would end the
recurring compression of resume-pointer content. Awaiting the director's word; the
fit-trims continue meanwhile.

Validation: UNIT-BOOKS ok (2 units, both build); MATERIALS-BILL ok (12 DSP materials,
every section negative); SCOPE-COVERAGE ok (2 units may code); `mdbook build` rc 0;
`make gate` all-doctrines-green (SEAM-INTEGRITY 679 boxes).

## _(2026-10-01)_ — the second unit's contract records, and the fixture that noticed (P3-BREADTH.6 slice 1)

The DSP profile's `requirements.sexp`/`contract-obligations.sexp` landed as governed
documents, closing the DOSSIER's records row. The shape is RECORD-SCHEMA's rules applied,
not invented: COVERAGE forced each requirement's statement to be its decision's
byte-identical text (seven decisions → seven `REQ-D-*`), MIRROR forced each mirror
obligation to restate it verbatim, AUTHORITY forced `defined` ⇒ `architecture` (the three
laboratory decisions take `laboratory`), and OBLIGED forced the ±POS/NEG pair per
obligation — 26 declared checks over contract `dsp56300-lab-env-v0`. The six `OB-ENV-*`
records carry the laboratory's half of the contract: no guest-reachable time source (`cyc`
is informational and never compared), sequential scalar issue (the F5 pending-writes
window measured ABSENT by the F6 census), cold reset to D-RESET-STATE's values, one 24-bit
P-space word per fetch, no asynchronous events (interrupts are a named subset exclusion),
and instruction-level atomicity. RECORD-SCHEMA attached with zero gate edits — the
catalogue auto-discovery found the new files and every cross-rule passed on the first run
(10 record files).

The interesting failure was FACT-OWNERSHIP's self-test, which did exactly what it exists
to do: its GREEN fixture's pair spec globs the REAL corpus
(`profiles/*/contract-obligations.sexp` × same-unit `requirements.sexp`), so landing the
DSP catalogues turned the fixture RED — `UNREGISTERED MIRROR PAIR`, the fixture registry
named only rv64i's pair. The re-pin names both units (`__CHECKED__ 5 → 6`) with the reason
in the check's comment — the same designed staleness the synth probes carry: a fixture
calibrated to a corpus the work just outgrew. Validation: both catalogues schema-validate
ok; RECORD-SCHEMA ok (10 files); FACT-OWNERSHIP ok (25 kinds), self-test 10/10;
`make gate` all-doctrines-green. The rv64i catalogues are byte-untouched.

## _(2026-10-01)_ — ask through the channel, and write down how asking works (P5-BOARD.8)

The director offered CHIPDOC's web-scorching for the network-connected board's component
documentation. The useful engineering content was the survey BEFORE the ask: the
snapshotted feed already holds a complete register-level Ethernet contract (TI-DP83816),
the ESP32 register maps, both SiFive SoC manuals, and the AM335x TRM — so the ten
requests only cover what is genuinely missing, each with a QEMU-oracle note or an
explicit probe flag (the AR9271 request expects a measured negative, which is itself the
answer to "is any WiFi baseband documented"). The process defect found and fixed: the
filing mechanics (requests.sexp preferred, gaps the false-positive-prone fallback,
exactly-once ids, the watcher firing on file change) lived only in the corpus-side
CHANNEL.md — a session had to re-derive them, and the director noticed. The fix is a
knowledge card, not a complaint: the next session reads
`docs/knowledge/the-chipdoc-request-channel.md` and files in one step. Verification
worth naming: chipdoc's poller was RUN (read-only, its own documented interface) and saw
exactly the ten new ids — the channel measured live, not assumed.

## _(2026-10-01)_ — the landing is the boring part when the measurement came first (P3-BREADTH.7 slice 3)

After slices 1–2 measured every attaching gate against the drafts, the landing itself was
a rename plus the ownership rows: `git mv` semantics for the three documents, five rows
in `fact_ownership.tsv`, and two census arms that only exist post-landing (they measure
the real two-unit corpus: a GREEN pair-registered arm and a RED unregistered-pair arm —
a gate whose arms depend on the corpus they judge is only writable after the corpus
lands, which is why they were scheduled, not forgotten, in slice 2). The one judgment
worth recording: the DSP's `guests/` registered as a fact owner with NO mirror — the
rv64 guest kind has a generated mirror (`guests.rs`, GUEST-GEN), and the DSP's honestly
has none yet; the registry's "mirror `-`" spelling is the honest zero, not a gap. The
DOSSIER's deferral rows now name `.6` for requirements and unit registration — the
earlier "lands with the model slice" wording was stale the day the model slice closed
without them, and two slices carried the correction.

