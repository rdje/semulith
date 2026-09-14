# CHANGELOG.md

## SEMULITH-MM-0043 (leaf MODEL-METHOD.12) — a citation that is present is not a citation that resolves

**The challenge.** An external investigation reported that this profile's pinned source does not
exist: `riscv/riscv-isa-manual` has no `2026-01-20` tag (the tags jump `01-17` → `01-21`), its
January release PDFs number **RV32I §2 and RV64I §4**, and the `§1.1` / `§3.1` numbering used by all
52 semantic citations is what you get only when `Introduction` is unnumbered front matter rather
than Chapter 1 — which no build it checked does. Conclusion: the pin matches no public build.

**Re-derived from the primary artifact before defending or conceding.** Every observation in the
report is true. The conclusion is not, and the difference is one word: **publication**.

```
github.com/riscv/riscv-isa-manual   numbers Introduction as Chapter 1  -> RV32I §2,    RV64I §4
docs.riscv.org  (pinned here)       Introduction is front matter       -> RV32I §1.1,  RV64I §3.1
```

`docs.riscv.org` is the RISC-V **Ratified Specifications Library**, a different publication of the
same specification, and it applies exactly the numbering rule the report deduced. Verified end to
end:

```
$ curl …/reference/isa/v20260120/unpriv/{intro,rv32,rv64}.html   -> HTTP 200 ×3
  and byte-identical to the pinned copies AND to the digests committed in sources.toml
$ python3 scripts/check_citations.py
  52 of 52 instruction citations resolve in the pinned artifact
```

⭐ **The investigation was not sloppy — it was under-informed by me.** What I had published was the
bare string `v20260120` with no publication attached, and given only that, searching the source
repository is the *reasonable* first move. The report even reconstructed the numbering rule that
explains the discrepancy; it lacked only the fact that some publication applies it.

**The real defect, which the challenge exposed and which was not the pin.** Nothing could have
settled this mechanically. `check_semantics.py` asks whether a rule *carries* a citation, and a
citation pointing nowhere still carries. `scripts/check_citations.py` now resolves every locator
against the pinned bytes — 10 self-test arms, and it **refuses rather than passing** when the
artifacts are absent, which matters because they are untracked and need the network:

```
$ mv target/sources/riscv-v20260120 … && python3 scripts/check_citations.py ; echo $?
REFUSED: the pinned artifacts are not present at target/sources/riscv-v20260120 … exit=1
```

`sources.toml` now names its publication **and the one it is not**, because the next person to
check this will start where the last one did.

**The interim substitution is declined**, recorded as `GAP-RISCV-JAN-2026-PDF`. Adopting the
January PDFs would turn 52 resolving citations into 52 unresolvable ones — a strictly worse
position reached by acquiring *more* material. They may be catalogued later under their own ids;
acquiring a document and repointing a pin are two decisions and only the first is cheap.

**Also measured:** the docs.riscv.org rendering carries only `Copyright © RISC-V International®` —
**no CC-BY statement**, unlike the GitHub PDF. So `OQ-4` (redistribution terms) stays open for the
rendering, and the pinned HTML is still read, never redistributed.

**Knowledge.** [`a-version-string-is-not-an-identity`](docs/knowledge/a-version-string-is-not-an-identity.md)
— a version names a point in time within one publication; across publications it identifies
nothing, and section numbers are exactly the part that will not survive the crossing.

## SEMULITH-MM-0042 (leaf MODEL-METHOD.11) — materials get an identity, and no path that breaks on a move

**What changed.** A curated corpus of vendor ISA and architecture manuals became available —
3,684 files, 1.5 GB, 196 PDFs across 23 vendors, curated in its own words *"to build software
emulators (ISS) that run real C/C++/Rust software"*. This repository had no form in which to say
that a material exists and where a copy of it is (`git ls-files | grep -ci materials` → 0).

The obvious route is the wrong one. The corpus lives **outside** the repository, so writing its
path into a tracked file plants an absolute path — which Policy 12 forbids, because the repository
must survive being moved to another filesystem. And it fails *quietly*: after a move the path stops
existing and every tool reports "not found" about a document sitting right there.

**The shape that solves it.** Paths compose from two roots, and the catalogue knows only one:

```
cache      <repo root>/<cache-root>/<cache-path>    both halves tracked and relative
corpus     $<env-var>/<corpus-path>                 the left half NEVER tracked
```

The environment variable is the seam. The operator sets it once; git never sees it. Measured on
the tracked tree, with a control proving the probe can see such a path:

```
$ git grep -c -I --cached -e 'livework' -- .    ->  0 tracked files name the corpus root
```

**What is catalogued.** 22 materials — RISC-V (unified ISA + ELF psABI), Arm (A-profile,
Armv7-A/R, Armv8-M, Armv7-M, Armv6-M), Intel SDM Volumes 2-4, Power ISA 3.1C, SPARC 2015,
OpenRISC 1000, six TI DSP CPU guides, MSP430, Z80, W65C02S — each with revision, page count,
sha256, licence and what it supplies. All 22 fetched and digest-verified into the gitignored
`.materials/` (233 MB, same volume as the repository). The repository catalogues identity and
redistributes nothing.

⭐ **Two measured gaps, recorded as first-class `(gap …)` records rather than remembered:**

- **No AMD instruction-set manual.** `amd/` holds exactly one document, an IOMMU specification. An
  x86-64 unit built from this corpus would rest on Intel's description of the architecture alone.
- **No Intel SDM Volume 1.** Volumes 2, 3 and 4 are present; Volume 1 — Basic Architecture, the
  execution environment, data types and register overview — is absent. An x86 unit could not state
  its architectural **state** from this corpus.

⭐ **And the RISC-V PDF is not our RISC-V.** It is `20260911: Intermediate Release`; the profile
pins `v20260120`. It also numbers RV32I §2.1 and RV64I §2.2, where the pinned HTML numbers them
§1.1 and §3.1 — so **not one of our 52 semantic citations resolves in it**. Catalogued
`reference-only`, never as the authority a requirement cites. Its licence, read from the document,
is **CC-BY-4.0**, which bears directly on `OQ-4` and rule `SRC-01`.

⭐ **Scale, as an argument rather than an opinion.** The Arm A-profile manual is **17,145 pages and
126 MB** — eighteen times the RISC-V manual. Beside it sit Armv6-M at 374 pages and the W65C02S
datasheet at 32, both complete architectures. That spread is `start small and grow` stated in page
counts.

**Housekeeping in lockstep.** `materials/` registered in `doctrine/readme_routes.tsv` in the commit
that creates it, ceilings derived from its own measured size. `CHANGELOG.md` had 1,326 B of
headroom against its 64 KiB ceiling and was sharded first: 64,210 → 28,188 B, 11 entries moved to
`docs/changelog/2026-09-p0-to-mirror.md`.

## SEMULITH-SF-0041 (leaf SOT-FORMAT.7) — the reader corrupted every citation it read

**What changed.** `scripts/sexp.py` decoded string escapes by handing the assembled string to
`.encode().decode("unicode_escape")`. That codec is **Latin-1**: it reads each byte as one
character, so the two UTF-8 bytes of `§` came back as `Â§` and an em dash came back as three
characters of noise.

**All 52 specification citations** in `definitions/riscv/rv64i.sem.sexp` were corrupted on read —
every locator committed one leaf earlier as *"52 of 52, every rule cited"*. The claim was true of
the file and false of what any consumer received:

```
raw bytes in file : b'RVI-RV64I \xc2\xa73.1.2.1 \xe2\x80\x94 D-LUI-AUIP'
as the reader sees: 'RVI-RV64I Â§3.1.2.1 â\x80\x94 D-LUI-AUIP'
```

**Why nothing caught it.** The reader that every source of truth in this repository depends on had
**no self-test at all**. Downstream, every instrument asked about structure or behaviour —
`check_semantics.py` asks whether a citation is *present*, and a corrupted string is still present.
None was pointed at **fidelity**, which is a separate property and has to be asserted separately.

**The fix.** Escapes are decoded from a closed five-entry table written in the file, and an escape
outside it is refused rather than guessed — the same soundness stance the module already claimed
for structure. A UTF-8 file needs no escape for non-ASCII at all. The reader now carries 18 arms,
three of them fired RED before the fix:

```
$ python3 scripts/sexp.py --self-test     # BEFORE → 15 pass / 3 fail
$ python3 scripts/sexp.py --self-test     # AFTER  → 18 pass / 0 fail
$ round-trip: each citation verbatim in the file's own bytes → 52 / 52, mojibake 0
```

No tracked file's content changed. The files were always right.

**Direction (director, `2026-09-14`).** Two instructions landed and are now durable records rather
than conversation:

- *Every source of truth is one format* — S-expression, composable, and **extensible to new
  constructs in the same format**. This supersedes the per-file format split in
  `decision_canonical-definition-input`: composition is a merge, and three formats are three merge
  semantics, so under the split a board composing two processors could union their encodings and
  nothing else. New tree `SOT-FORMAT`, 9 leaves.
- *The parser is not written here.* The Rust reader comes from **LinkedSpec**
  (`specs/Lispish.spec` on its Rust backend), added as a **git submodule** pinned to a commit.
  ⛔ I first inferred `pgen` from the capability description — *many backends, Rust among them,
  parses many formats* — and was corrected. The failure mode is general and worth keeping: a
  capability description matches several repositories; only a named artifact identifies one.
  ⛔ **Blocked:** LinkedSpec is preparing its integration document for downstream consumers and it
  is not finished, so `SOT-FORMAT.9` waits for it rather than integrating against internals.

**Also measured, and owned rather than logged.** The mdBook chapter *"Architecture and canonical
definitions"* includes `docs/ARCHITECTURE.md`, which names no format, no `definitions/` directory
and no composition operator — all three introduced over the four preceding commits. The director's
only window into the project shows none of the work. `SOT-FORMAT.8`, at frontier order 2.

**Knowledge.** [`a-parse-without-error-is-not-a-faithful-read`](docs/knowledge/a-parse-without-error-is-not-a-faithful-read.md)
— a parser's error paths are all about structure; it proves nothing about content until a test
compares what it returned with what it read. A test corpus of `foo` and `bar` cannot tell a correct
decoder from a Latin-1 one.

## SEMULITH-MM-0040 (leaf MODEL-METHOD.9) — the semantics: 52 of 52, every rule cited

**What changed.** Nothing machine-executable existed. A generator engine reading the canonical
definition found configuration, state, provenance, assumptions and encodings — and still could not
produce an interpreter, because what each instruction *does* lived only as English prose in a
decision's `statement` field. 26 rules, all prose, none executable.

`definitions/riscv/rv64i.sem.sexp` now carries **52 of 52** declared instructions as expressions,
each citing the specification locator it was derived from.

⭐ **Widths are always explicit**, because an implicit width is where two models silently disagree:

```
(sem (insn addiw) (source "RVI-RV64I §3.1.2 — D-WSUFFIX …")
     (effect (set (reg rd) (sext 64 (trunc 32 (add (trunc 32 (reg rs1)) (sext 32 (imm imm12))))))))
```

That is the whole of `D-WSUFFIX` in one line, and it can be checked against the sentence that
produced it — which is the entire evidence argument for a hand-derived semantics.

⛔ **Generated and authored content live in different files on purpose.** `rv64i.sexp` is generated
from a machine-readable table and regenerated whenever that table moves; hand-derived semantics in
the same file would be destroyed by a regeneration. Different provenance, different file.

**The language is 32 forms**, each added because an RV64I instruction needed it, none in
anticipation — and the checker refuses everything else. Four controls fired on the real file: a
missing instruction (`sraw`), an unknown operator (`multiply`), an operand the instruction does not
have (`imm12` in `sub`), and a rule citing nothing. Each refused by name.

⚠️ **What `52 of 52` does not mean.** It says the semantics are well-formed, complete and *cited*.
It does **not** say they are **correct**. Proving that is a differential experiment against a
reference model — what `P0-PROFILE.6` does for three guest programs today and what `P1-LAB` must do
at scale. A definition that says something checkable is not yet one that says something true.

⛔ `riscv/m`'s semantics are absent and that is correct: `rv64i-lab-v0` does not compose `M`, and
writing semantics for a fragment no unit uses would be inventory.


## SEMULITH-MC-0039 (leaf MODEL-COMPOSE.2) — fragments get a form and a home

**What changed.** The unit carried all 52 instructions **inside itself**. A base ISA is shared by
every profile that composes it, so a second RV64 profile would have copied 52 instructions that
then had to be kept equal — the exact duplication the no-duplicated-fact rule exists to prevent,
in the one place most tempting to copy.

- `definitions/riscv/rv64i.sexp` — the base: 52 instructions, plus the operand fields and
  scattered-immediate layouts a base owes its extensions.
- `definitions/riscv/m.sexp` — the M extension: 13 instructions, `(requires "riscv/rv64i")`.
- The unit now **names** what it composes and owns nothing: `(compose (base "riscv/rv64i")
  (extensions))`. Census: instructions in the unit `52 → 0`; in `definitions/` `0 → 65`.

⭐ **The acceptance test is that nothing observable moved.** A refactor of the source of truth must
not perturb the evidence, so all four guests were re-assembled and re-run: the `elf sha256` values
are **byte-identical** to before the split, across two reference models, all reproducing.

**Two refusals, both fired.** Composing `riscv/m` without its base →
`requires 'riscv/rv64i', which this composition does not provide before it. A fragment with an
unmet dependency composes by luck, not by construction.` Composing a fragment that does not exist →
`composes 'riscv/nope', but definitions/riscv/nope.sexp does not exist`.

**The `M` fragment is now pinned** (`rv_m`, `rv64_m` digests) — a fragment composed from an
unpinned source is a model built on something nobody can re-derive. Fragments are re-derived
against the pinned tables and fired RED on a one-nibble `funct3` edit to `mul`. The tracked
generator reproduces them **byte-for-byte**, so it is the owner and the files are not a
hand-maintained copy of its output.

⚠️ `definitions/` was **registered in the routes registry in the same commit that created it** — a
new tracked family that nothing governs is how pressure escapes, which this project has already
measured once.

⚠️ Three references to the generator's old name survive in this file and in `MODEL-METHOD.8`'s
completed checklist. They are left alone deliberately: both are historical records, true when
written, and rewriting them to match today is what the `append_history` lifecycle prevents.


## SEMULITH-MC-0038 (leaf MODEL-COMPOSE.1) — encoding composition is a verdict, not a hope

**What changed, and what it replaces.** I proposed tiering models into `exploratory` (ungated) and
`accepted` (gated) to buy breadth. That was rejected, and rightly: it buys breadth by creating a
second class of model nobody can trust. The correct lever is **composition** — every model stays
signoff-grade, and complexity is reached by *assembling proven small models*. Breadth by **reuse of
evidence**, never by absence of it. Recorded as
[`decision_composition-model`](docs/decisions/decision_composition-model.md).

**The design, grounded rather than invented.** Both pinned references already compose definitions
from fragments — `riscv-opcodes` ships **111** extension files, `sail-riscv` **34** extension
directories and **59** encoding files — and this project already carries the other half: an empty
`extensions = []` seam and **8 environment-assumptions** stating what something else must
guarantee. Two operators, one port mechanism:

- **intra-unit: union with conflict detection** — decidable, and therefore a verdict;
- **inter-unit: assumption/guarantee discharge** — `CPU_ENVIRONMENT` §5, made mechanical;
- **direction falls out of ports** — an unbound *slot* makes top-down composition checkable before
  its parts exist, and compositions nest, so `computer → board → soc → {cpu, device}` is one record
  shape at every level.

⭐ **Proven, not asserted.** The owned RV64I encodings composed with an `M` fragment they had never
seen: **52 + 8 + 5 = 65 instructions, no collision, no duplicate name.** Two instructions collide
exactly when `(value_a ^ value_b) & mask_a & mask_b == 0`, searched exhaustively — a sampled answer
would not be a decision.

**Fired RED on a genuine mistake, not a synthetic one:** composing the owned encodings with `rv_i`,
a fragment they already contain, produced **37 collisions** each named with its overlapping mask,
and `REJECTED`. A second refusal fired unplanned — an empty fragment file answered
`REFUSED … an empty fragment is not a valid one` rather than "no collisions" over nothing.

⛔ **What this does not claim.** There is **no RV64IM profile**: the `M` fragment is unpinned, no
semantics were composed, nothing was added to `rv64i-lab-v0`. The *decoder* composes. Whether the
*meanings* compose is not decidable in general — an extension can change a base instruction's
behaviour, and `MODEL-COMPOSE.6` treats a silent override as a defect rather than a composition.


## SEMULITH-MM-0037 (leaf MODEL-METHOD.8) — the repository owns its encodings

**What changed.** A single source of truth per unit, from which a generator engine extracts what it
needs, requires the repository to actually **own** that source. It did not. Measured:

```
$ git ls-files | grep -c riscv-opcodes
0                       # the assembler read an untracked, network-acquired directory
$ git ls-files profiles/rv64i-lab-v0 | grep -cE 'encod|semant'
0                       # neither encodings nor semantics were owned
```

A fresh clone could not build a model at all, and the project's own rule — *a constant that is a
function of an external document is derived or gated, never assumed present* — was being broken by
its own tooling.

- `profiles/rv64i-lab-v0/encoding.sexp` — **tracked**: 52 instructions, 12 operand fields, 3
  scattered-immediate layouts, each carrying its upstream file and that file's digest.
- `scripts/sexp.py` — a reader for exactly the shapes these files use, refusing the rest.
- `scripts/gen_encoding.py` — regenerates it; `fetch_references.sh` re-derives and compares.

⭐ **The test that settles it is not that the file exists.** It is that the model builds *without*
the untracked directory, so the upstream was moved aside and the whole evidence path re-run:

```
$ mv target/refs/riscv-opcodes /tmp/ro-hidden && scripts/run_smoke.py
run_smoke: ok — every program matches its specification-derived expectations and reproduces
```

Four guest programs assembled, executed on two references and reproduced, with the source of the
encodings absent from disk.

**Ownership without re-derivation is a copy**, so the agreement is checked: fired RED by changing
**one bit** of one instruction's `funct3` — `and`'s `(14 12 0x7)` to `0x6` — producing
`DIFFERS … no longer matches what the pinned tables generate` with the line quoted.

⛔ **The new reader was caught by its own first real input.** Its tokenizer stripped `;` comments
line by line *before* tokenizing, which is wrong twice over: a `;` **inside a string** truncated
the string, and a string could not span lines. Generating this project's own encoding file hit the
second within minutes. It is now a single stream scan — whether a `;` starts a comment depends on
whether a string is open, which is the only way that question can be answered correctly.

**Also decided:** [`decision_canonical-definition-input`](docs/decisions/decision_canonical-definition-input.md).
The S-expression trigger parked earlier has **fired**: the canonical definition is a **set of
format-fit files** — S-expressions for `encoding.sexp` and `semantics.sexp` because those are
trees, records staying JSON and TOML because they are records and are already gated by instruments
fired RED. "Single source of truth" is preserved by a **no-duplicated-fact** rule, not by
single-file-ness.

⚠️ This makes the repository own its encodings. It does **not** make the canonical definition
sufficient: **semantics are still absent** — the decisions are English prose and nothing
machine-executable exists. `MODEL-METHOD.9` owns that, and `.10` turns *"the engine can extract all
it needs"* from an intention into a verdict that gates writing model code at all.


## SEMULITH-MM-0036: one canonical definition, one book — the unit that grows

**What changed.** The north star, stated and made structural: Semulith models **as much as
possible** — CPUs, MCUs, DSPs, devices, boards, SoCs, eventually whole computers — and **starts
small and grows**. The structural consequence:

> **The unit of modelling is the unit of documentation.** Every canonical definition gets its own
> mdBook, its own materials bill and its own coverage census, describing how it went **from PDFs,
> specifications and descriptions to a fully functional model**.

`docs/ARCHITECTURE.md` already named the unit — *"later devices and boards receive their own
canonical definitions"* — so this adopts existing vocabulary rather than inventing a parallel one.
What it adds is that a definition is not complete until the book explaining how it was built exists
beside it.

**Kind and layer decide what a unit may own.** A `cpu`/`mcu`/`dsp` owns instruction semantics and
its environment *assumptions*, never devices. A `device` owns one device's contract. A
`board`/`soc` owns composition, never the semantics of the parts it composes.

⭐ **The layer names the OWNER, not merely a deferral** — and that is what makes a coverage census
honest. `C19 Platform, devices and interconnect` is `deferred-to-board` for a CPU and `covered` for
a board: the same category, the same catalogue, a different unit answering it. It is also why the
catalogue is keyed on a **unit** rather than a processor profile — a board's census and a CPU's
census become the same schema answered differently, which is what makes the second unit cheap
instead of a redesign.

**Starting small, deliberately.** Exactly one unit exists: `rv64i-lab-v0`, kind `cpu`. Nothing is
pre-built for units that do not — no board directory, no device schema, no speculative chapters.
⛔ And the kinds table is a **hypothesis** until a second unit tests it; `MCU` and `SoC` in
particular have never been exercised, and the first board or DSP is expected to correct it. That
correction is normal, not a failure of the decision.

⚠️ A book is written for a model that is **not yet finished**, and says so. The first will describe
a model whose gate reads `incomplete` — hiding that until the model is done would make the book a
retrospective rather than a method, and the method is the transferable part.


## SEMULITH-MM-0035: the layer boundary — a UART is not CPU material

**What changed.** A scoping correction that arrived before it could do damage: devices belong to a
**board / SoC / ASIC** model, not to a processor model. This project pipecleans by modelling CPUs
and DSPs first, and the processor layer ends at the CPU/environment boundary — the CPU states what
it *assumes*, and a later board model states what it *guarantees*.

The project's contracts already own this line, so it is cited rather than restated:
`docs/INFORMATION_CATALOG.md` says *"C19–C21 are not all properties of the CPU itself"*, and
`docs/CPU_ENVIRONMENT.md` §5 is the board composition gate.

⭐ **The sharp consequence is for the materials catalogue, which is why this landed before its
schema was written.** A category the processor layer does not own is **not `missing`**. Marking
`C19 Platform, devices and interconnect` as missing for a CPU model would manufacture an
acquisition task for material the model must never contain, and would report a correct scope as a
deficiency. The disposition vocabulary now carries a **layer**, and `deferred-to-board` is a
first-class answer distinct from both `missing` and `not-applicable`.

⚠️ **It also corrects a framing from the previous leaf.** "Capable of running real code" needs a
console and a program-exit convention — and **those are board concerns**. What the *processor*
layer owes real code is narrower and wholly inside it: the psABI, the ELF contract, the
entry/startup state, and the compiler-runtime intrinsics a no-`M` soft-float target calls.

**`DIFF-PLATFORM-SPIKE` is reframed as a layer difference, not a configuration one.** Spike ships a
CPU *and a small board* — an interruptor, a PLIC and a UART — and does not separate them. What that
record measures is **how much board each reference drags in**, which is a more useful thing to know
than "the config would not take".

**Checked rather than assumed:** every device named anywhere in `rv64i-lab-v0` appears in exactly
one role — something a reference brings that the profile excludes. Word-boundary grep over the
profile's own files finds mentions only in notes explaining the exclusion; no decision, no
requirement and no obligation models a device. The earlier apparent hits in `sources.toml` and
`DOSSIER.md` were substrings of *implicit* and *explicit*.


## SEMULITH-MM-0034 — the dual mandate: production-grade **and** a teaching text

**What changed.** A director instruction that reshapes every model this project will produce:
each must be signoff, production-grade work **and** serve as educational material from which a
student can learn to build production-grade CPU/DSP models capable of running real compiled code
(C, Rust, …). Recorded as
[`decision_dual-mandate-production-and-teaching`](docs/decisions/decision_dual-mandate-production-and-teaching.md),
carried into `MODEL-BOOKS` and `MODEL-METHOD`, and aligned into `ROADMAP.md` §1.

⭐ **What the teaching mandate actually changes** — it is not "add explanation", which would change
nothing. Four concrete things: reasoning becomes recoverable including the rejected alternatives;
**mistakes stay in the record**; the *order* of the work is justified rather than listed; and
"runs real code" becomes a target with stated limits.

⛔ **The mistakes are the most instructive pages.** This project has already found, in its own
work, a matched profile that matched only an instruction set, a comparator that called a truncated
trace agreement, a self-test that ran four of fourteen arms, and a gate report that counted a
*mention* as an implementation. Removing those to look competent would remove the teaching.

**What "runs real code" costs, measured rather than assumed.** The first profile is `RV64I` with
no extensions: no `M` (multiply and divide become runtime calls), no `A` (no atomics), no `F`/`D`
(soft-float ABI), no `C`. Running C or Rust on it needs materials the ISA chapters do not own and
this project has **not pinned** — the psABI, the ELF specification, a startup/runtime contract,
the compiler-runtime intrinsics a no-`M` soft-float target calls, and a program-exit convention.
Those are now acquisition items in `MODEL-METHOD.4` rather than assumptions.

⚠️ It also makes an existing honesty load-bearing: `state.json` records ABI register roles as
`software-convention` because the ISA chapter does not own them. Once real code runs, that
convention stops being background reading and becomes a pinned material with a digest.

⛔ Neither mandate may be traded for the other. Simplifying a contract to make a chapter easier is
a production defect; omitting reasoning to keep a record terse is a teaching defect. Where they
genuinely conflict the production artifact wins and the book explains the complexity — a student
learning from a simplified fiction learns a fiction.


## SEMULITH-MM-0033 (leaf MODEL-METHOD.1) — answer the narrower-instrument sweep, with a wider instrument

**The open question, answered.** `P0-PROFILE.10` fixed one instance of a pattern — a single
confident scalar standing in for a configuration — and left the general question open. The sweep
enumerated every pinned scalar that stands for a configuration and checked each.

⛔ **One further instance, and worse than the first.** `spike.matched_isa_string = "rv64i"` was the
command-line **input** recorded in an observation's slot. Spike has no `--print-isa` option, so
nobody had ever confirmed it configured what it was told. The first instance was a narrow reading;
this one was not a reading at all.

It is now read back from a surface Spike does offer, with a control proving it is an observation
rather than an echo: `--isa=rv64i` → `riscv,isa = "rv64i"`, `--isa=rv64im` → `"rv64im"`.

⭐ **The replacement principle is now an instrument.** A match is claimed against the model's own
self-description at the **widest granularity it offers**, compared field by field. Both references
emit a device tree, so `scripts/compare_platforms.py` compares them:

```
FIELD                  sail (matched)           spike (matched)          agree
riscv,isa              "rv64i_zvl32b"           "rv64i"                  NO
mmu-type               "riscv,none"             "riscv,sv57"             NO
riscv,pmpregions       <absent>                 <0x10>                   NO
timebase-frequency     <500000000>              <0x989680>               NO
devices only spike advertises: clint@2000000, cpu@0, ns16550@10000000, plic@c000000
```

**4 of 4 platform fields disagree, and Spike advertises a UART, a platform interrupt controller,
an interruptor and a CPU node** that Sail does not — none of it visible in an ISA string.

- **New rule 5b** in `PROFILE-CONSISTENCY`: a pinned `matched_isa_string` must declare both what it
  does **not** establish and **where it was read from**. Fired RED on the real dossier.
- All three candidates now carry `matched_scope` — including QEMU, whose emptiness is now visible
  rather than inferred from an absent row.

⚠️ **The wide instrument has its own scope, and says so.** A device tree describes what a platform
*advertises* — not semantics, not memory attributes — and carries residue: Sail's still advertises
a `timebase-frequency` and an `htif` node with no device behind them. **Wider is not complete.**
Recording that is what stops this instrument becoming the next narrow one.

⛔ **The honest form of the answer:** one further instance existed, it is fixed, and the pattern is
gated. I am not claiming there are no others — I am claiming a new one cannot be *added* without
declaring its scope, which is the only durable form that answer can take.

**Also opened:** `MODEL-METHOD`, the tree that makes the modelling method and its required
materials explicit, with the format call recorded — JSON Lines under a JSON Schema, not
S-expressions, because the data is records rather than trees and the repository already gates
JSONL. S-expressions are parked for the canonical executable semantics in `P1-LAB`, with a trigger.


## SEMULITH-P0-0031 (leaf P0-PROFILE.10) — the profile was matched on its ISA and not its platform

**What changed.** A challenge to the previous findings turned up a real defect that the first nine
leaves of this tree carried. The matched-profile override configured `base`, `memory.misaligned`
and `extensions` — and **nothing else**. `--print-isa-string` returned `rv64i_zvl32b`, which is
correct, and was read as *"matched"*. It answers a narrower question than that.

Underneath the correct ISA the reference kept its default platform: a core-local interruptor at
`0x0200_0000`, an interrupt generator, machine software/timer/external interrupts all `supported`,
and two IOMemory regions. Established by probe:

```
[5] ld x1, 0x0(x10)      clint[0x…BFF8] -> 0x0000000000000002   x1 <- 0x2
[6] ld x2, 0x0(x10)      clint[0x…BFF8] -> 0x0000000000000003   x2 <- 0x3    # ADVANCING
```

**A guest read a monotonically advancing time source with a plain load — no CSR instruction.**
Four committed claims are refuted by that one measurement: `OB-ENV-VIRTUAL-TIME` ("no time source
is modelled"), `OB-ENV-EVENT-DELIVERY` ("no interrupt controller … no privileged mode"),
`D-MAIN-VS-IO` ("no I/O region is declared"), and `privilege_modes = []` — every trace line in
this repository reads `[M]`, because a hart is always in at least machine mode.

- **Corrected at source, not reworded.** The override now sets `platform.clint.supported = false`,
  the interrupt generator off, all three machine interrupt sources off, and `memory.regions` to
  the single MainMemory region the profile declares. Both probes now raise `load-access-fault`.
- `profile.toml` gains `D-PLATFORM`, corrects `D-MAIN-VS-IO`, and sets `privilege_modes = ["M"]`.
  Decisions 25 → 26, requirements 25 → 26, obligations 33 → 34, checks 66 → 68, differences 4 → 6.
- **The repair is held permanently** by a tracked negative fixture, `guests/guest-no-device.s`,
  which reads CLINT `mtime` and must fault. A device becoming reachable again turns the run red.
- **The three original guests still agree** over 12 / 13 / 3 aligned steps and reproduce
  byte-identically — the repair changed nothing it should not have.

⭐ **Spike is not platform-matched and cannot be**, which is enumerated rather than fixed. Its
interruptor is built in; `--device` only *adds* MMIO plugins; and `-m0x80000000:0x10000` kills its
own reset vector (`trap_instruction_access_fault, epc 0x1000`). `SRC-02` makes that a legitimate
result that **bounds** the claim: any guest touching `0x1000` or `0x0200_0000..0x11ff_ffff`
behaves differently on the two references. The three original guests touch neither — now a
**stated precondition rather than luck**. `guest-no-device` disables its cross-model comparison
for this reason and the runner **prints the skip** rather than applying it silently.

⛔ **The instrument is the lesson.** This is not the `zero-hits` failure — an instrument that could
not see. It is worse and quieter: **an instrument answering a narrower question than the one
asked**. `--print-isa-string` gave one confident string, and the string was true.

**Effect on `G0`.** The verdict stays `incomplete` for the same reason (68 declared checks, 0
implemented). But criterion 3 — *differences enumerated, not assumed absent* — is now met on
evidence rather than on an unexamined configuration, which is a real change in what the gate means.
