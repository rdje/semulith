# CHANGELOG.md

## SEMILITH-MM-0048 (leaf MODEL-METHOD.4) — the run-real-code set is acquired, and the PDF question is answered

What the ISA chapters do not own is now pinned: the RISC-V psABI canonical render, the System V
ELF specification, the generic syscall header (the hosted exit convention), and the LLVM
compiler-rt builtins inventory — the last carrying `__muldi3 (di_int a, di_int b); // a * b`,
the soft-multiply intrinsic a no-`M` target calls. Each is digest-pinned in the owning leaf,
cached on-volume under `.materials/run-real-code/`, and re-derivable from the recorded curl
commands; the bytes stay out of git, per the no-redistribution doctrine — the tracked record is
the digest table, not the documents. The startup/runtime contract needed no acquisition: the
harness contract already owns entry state and the ECALL/EBREAK exit convention.

⭐ The PDF question (MODEL-BOOKS.2) is answered **YES**: the specification's PDF rendering carries
the instruction-format tables as selectable text — `pdftotext` extracts 1.96 MB from the
release asset, and the RV32I format-table region yields `funct7 / rs2 / rs1 / funct3` as clean
cells. Encodings can be re-sourced from the primary document. SRC-02 records: the pinned
revision's release PDF was not located in three pages of releases; the chipdoc corpus route was
unavailable here (`$SEMULITH_CHIPDOC_ROOT` unset) — the psABI came from its canonical public
render instead.

## SEMILITH-MM-0047 (leaf MODEL-METHOD.3) — the census sweeps the snapshot, and missing changes its meaning

The coverage census for `rv64i-lab-v0` did what a first pass cannot: it opened the pinned
snapshot and checked. Every covered category's subject matter is present in the pinned pages —
and, the measured surprise, so are the excluded subsystems' chapters (a/d/f/q/v-st-ext, rvwmo,
counters, zicsr, zifencei). `missing` therefore never meant "material absent"; it means the
profile EXCLUDES the subsystem, and all six missing rows now name what would close them: a
profile revision against snapshot chapters (C07/C08/C16), the separate Privileged Architecture
manual (C12/C14/C15), the Debug specification (C18). Device and interconnect categories became
the new `deferred-to-board` disposition — P5-BOARD's to own, with the CPU recording an
environment assumption in their place. Final census: 10 covered, 4 partial, 6 missing with
closers, 3 deferred-to-board, 1 out-of-scope. RECORD-SCHEMA rule 12 (UNRESOLVED MATERIAL) keeps
every named material honest against the catalogue; 33 arms.

## SEMILITH-MM-0046 (leaf MODEL-METHOD.2) — the materials requirement: what each unit owes its model

The catalogue of documents gains the requirement layer: `schema/units.sexp` +
`schema/category-needs.sexp` declare two record families (zero kernel lines), and
`materials/units.sexp` + `materials/category-needs.sexp` carry the one-row registry and all 24
INFORMATION_CATALOG categories for `rv64i-lab-v0` — each bound to the material kind that
supplies it, at its layer, with an honest disposition. The vocabulary distinguishes ABSENT from
NEVER-NEEDED: `missing` (a reason is owed — C07/C08/C12/C15/C16/C18, excluded subsystems) versus
`out-of-scope` (C17/C19–C21, board-layer facts a processor never owed). RECORD-SCHEMA rules 10–11
enforce it — the acceptance's shape, a board-layer `missing` for a processor, refuses as
`LAYER LIE` — 6 new arms, 32 total, 7 record files green. The DSP-specific questions of the
catalog's §5 ride as their own D-category ids, admitted by the schema and pre-built for nobody.

## SEMILITH-MM-0045 (leaf MODEL-METHOD.7) — the no-duplicated-fact rule is a registry, and every mirror is governed

"Single source of truth" now means one owner per fact, mechanized. `doctrine/fact_ownership.tsv`
names the one owning file per fact kind (8 kinds — configuration, state, encodings, semantics,
requirements, obligations, pinned sources, materials), each legal derived mirror, and the
doctrine governing every owner→mirror pair; `FACT-OWNERSHIP` (18th doctrine, 8 arms) verifies one
owner each, owners exist, every governor is a registered doctrine that runs, and the corpus's four
restatement pairs are all named. The acceptance's shape — a fact stated in two, refused — fires as
`UNGOVERNED MIRROR` and `UNREGISTERED MIRROR PAIR`.

⭐ The inventory found what the rule exists to catch: the corpus's mirrors were mostly governed
(decision↔requirement by RECORD-SCHEMA; state↔profile by PROFILE-CONSISTENCY; composition↔fragments
by UNIT-COMPOSITION), but 28 obligations restate their requirement's statement — all matching
today, nothing refusing the day one drifts. RECORD-SCHEMA gains rule 9 (MIRROR) with 3 arms; 26
total. An ungoverned mirror is how one fact quietly becomes two; the registry makes that a verdict.

## SEMILITH-MM-0044 (leaf MODEL-METHOD.10) — the extraction contract: one set, four ways

*"The engine can extract all it needs"* is a verdict now. `scripts/check_extraction.py` requires
SCOPE (the profile's declared instruction set), ENCODING (the composed union), SEMANTICS, and
REQUIREMENTS to be ONE set — every declared instruction with all three — plus every state element
with a reset and every obligation with a positive and a negative check. The real corpus passes:
`SUFFICIENT for an engine: 52 instructions, each with encoding + semantics + requirement`.

⭐ The contract as stated first fired RED on the real corpus — measured, not assumed: no
requirement↔instruction link existed, and the whole ALU family (13 instructions) had no
requirement at all. The leaf fixed the corpus, not the contract: `(insns …)` on the schema
(kind-agnostic — FENCE names one instruction, ECALL-EBREAK two), two new decision/requirement/
obligation triples grounded in the corpus's own §1.1.4 semantics (SLTIU's sign-then-unsigned quirk
included), and the count-bearing docs re-derived (28 decisions, 28 requirements, 36 obligations,
72 checks; G0-REPORT regenerated in the commit). RECORD-SCHEMA caught a wrong obligation id
mid-curation and was fixed before commit. The acceptance fired RED on a real-corpus copy with one
instruction's semantics removed. `EXTRACTION` is the 17th project doctrine — **P1's start
condition is now fully met**, and P1-LAB cites a check that runs.

## SEMILITH-MC-0043 (leaf MODEL-COMPOSE.5) — a composition is an ordinary unit, and the tree closes

Nesting, materialized: `schema/composition.sexp` — `(composition (id …) (part …))`, zero kernel
lines — and `scripts/compose_units.py` turn a board manifest into an ordinary unit directory.
The parts merge through `merge_units(…)` — the same code the verdicts consume, not a fork — the
three catalogues write through the single mapping owners, provenance kept (`profile_ids` stay
with their origin units), and an `encoding.sexp` derives when exactly one part carries one. The
acceptance is the run: a board materialized from the real profile's parts (26 requirements, 34
obligations, 3 sources, the 52-instruction encoding) self-merges, discharges 8/8, and resolves
through the encoding read path — every check the unmodified one-level tools already own.
Two ISA-carrying parts refuse with the multiprocessor boundary named (the address-space operator
stays earned-from-a-real-case). **`MODEL-COMPOSE` closes at 6/6** — composition is now a verdict,
a discharge, and a materializable unit.

## SEMILITH-MC-0042 (leaf MODEL-COMPOSE.6) — a silent override is refused, and the execution authority gets its gate

The hard axis has its first mechanical form. `schema/semantics.sexp` gains `(refines (insn "name"))` —
zero kernel lines — and `check_semantics.py --compose` decides the rule over a unit's fragments in
composition order: an instruction whose semantics appear in more than one file is an override,
legal only when the extending file declares the refinement. The acceptance fired RED on a
real-shaped composition (a fake extension redefining `add` → `SILENT REDEFINITION`,
rc=1); a declared refinement is accepted and reported; both lies (a declaration naming nothing the
file defines, refining nothing an earlier file defines) are refused by name.

⭐ The third orphan of the family `MODEL-COMPOSE.4` closed for encodings: `check_semantics.py`
and `check_citations.py` were invoked by NOTHING — the semantics corpus, which `ROADMAP.md`
names the execution authority, was healthy only by hand. `SEMANTICS` (16th project doctrine) now
runs the per-fragment checks and the 52/52 citation resolution in every gate, with a NAMED SKIP —
never a green lie — when the offline cache cannot judge. The IALIGN-class (global-behaviour)
refinement stays named-and-deferred: per-instruction is the granularity the corpus writes.

## SEMILITH-MC-0041 (leaf MODEL-COMPOSE.4) — slots are data, and the unit's union is decided again

Top-down composition with holes is real, and it is declared, never inferred: `compose`
gains `(status complete|partial)` and `(slot (id …) (requires …))` in
`schema/encoding.sexp` — zero kernel lines. A partial composition passes the checks
that apply and is reported partial (`PARTIAL — 1 slot(s) unbound: clint requires riscv/timer`);
a composition claiming completeness while a hole is open is refused, and a partial declaration
with nothing unbound is refused too — both directions of the silence rule.

⭐ The substrate was two measured defects, not one. Since `MODEL-COMPOSE.2` moved the
instructions into fragments, nothing decided the unit's composed encoding space — the disjointness
checker read compositions its own way and could no longer read a unit at all. And it never
schema-validated its input (a planted `(widget "x")` passed silently). Both are closed:
one resolver (`riscv_asm.resolve_composition`) now serves the assembler and the
checker, the composition document and each resolved fragment validate against the schema layer
before unioning, and `UNIT-COMPOSITION` (15th project doctrine) decides every tracked
unit — the profile composes 52/52. Two more latent bugs of the same family surfaced in the
resolver itself (`[0]`-indexed children the 0-or-more grammar does not guarantee) and are
fixed with arms proving the absent-marker paths. Nothing observable moved: every guest still
assembles, matches, and reproduces.

## SEMILITH-MC-0040 (leaf MODEL-COMPOSE.3) — assumption/guarantee discharge is a verdict

The composition claim is conditional no longer in name only. `scripts/discharge_assumptions.py` is
the mechanical form of `docs/CPU_ENVIRONMENT.md` §5: every `environment-assumption` in
the merged obligation set must be discharged by named guarantees — every dependency resolving
to an obligation whose direction is a guarantee — or the composition is rejected naming the
assumption and the reason. The profile's own 8 assumptions discharge 8/8 today, every edge
printed (`OB-ENV-RESET -> 'OB-ENTRY-STATE' (cpu-guarantee)`, and kin); a unit
carrying only the reset guarantee discharges `OB-ENV-RESET` across the boundary; and
removing that one guarantee rejects the composition from both halves of the corpus (`DANGLING DEP`
on the assumption, `UNDEFINED OBLIGATION` on the requirement). Discharge-specific refusals
proven on fixtures: a demand pointing at a demand (`UNDISCHARGED CHAIN`), an assumption
naming no guarantee (`UNDISCHARGEABLE`) — and the complement, stated so nobody reverses
it: an unclaimed guarantee is not an error.

`SOT-FORMAT`'s census did the design work: the discharge edge already existed in the
corpus as obligation dependencies — the operator made it a verdict instead of a hope.

## SEMILITH-SF-0061 (leaf SOT-FORMAT.6) — the split cannot return: SOURCE-FORMAT registers, SOT-FORMAT closes

The 14th project doctrine is registered: `scripts/check_source_format.sh` refuses a source of
truth outside the one format — a tracked `.toml` / `.json` / `.jsonl` / `.yaml` under
`definitions/`, `schema/`, `profiles/`, `materials/` is named and refused (the FORMAT arm,
fired RED before registration against a scratch copy of the real corpus with one planted
`profile.toml`), and every `.sexp` there must parse with the one reader (PARSES). The real
corpus — 28 source-of-truth files — is green. Retirement in prose decays; the gate is the
decay's answer. Both doctrine mirrors (`DOCTRINE_ENFORCEMENT.md`, the mdBook) carry the row in
the registering commit; LIVE_STATUS's 14 doctrines / 184 arms are re-derived, not remembered.

The supersession chain was verified, not assumed: `decision_canonical-definition-input` has
carried its replacement since `SEMILITH-SF-0041`. Two stale lines surfaced while reading for
this leaf — the replacement record's own *How to apply* still said "write the EBNF in `pgen`"
against its director-corrected body (LinkedSpec), and both INDEX descriptions repeated it —
corrected in passing, with the reason recorded in the record. **SOT-FORMAT closes at 10/10.**

## SEMILITH-SF-0060 (leaf SOT-FORMAT.5) — the record merge is definable, and it decides

The union this tree exists for is now checked: `scripts/merge_records.py` merges two units'
requirements, obligations and pinned sources by id — the same id must carry the same content
(`profile_ids` excepted: it is membership, and it unions), a source id must pin the same
bytes, and every dependency, obligation link and citation must resolve across the union. Two
units compose, or the refusal names the conflicting fact, both values, both units. The real
profile composes with itself (26 + 34 + 3); one edited statement in a copied unit is refused
naming the field; an extension unit whose requirement depends on the base's `REQ-D-XLEN`
composes — and is refused by name when the base is withheld. `MODEL-COMPOSE.3` reads the merged
view (`merge_units(…)` plus the direction census: 26 cpu-guarantee, 8 environment-assumption).

⭐ **Two defects found by probe before any code, both closed.** RECORD-SCHEMA never refused
duplicate record ids — its id → record map collapsed them last-wins, so a catalogue could
contradict itself and stay green (`rc=0`, measured) — rule 8 (UNIQUE-ID) now refuses, 23 arms.
And obligation `dependencies` were checked against nothing: the corpus's cpu-guarantees depend
on requirements while its environment-assumptions depend on guarantees — a mixed namespace the
new closure resolves against requirements ∪ obligations, measured on all 42 records, zero
dangling.

## SEMILITH-SF-0059 (leaf SOT-FORMAT.4) — the dossier moves behind the schema layer, commentary and all

The profile dossier retires its last TOML/JSON: `profile.toml` (26 decisions), `state.json`,
`sources.toml`, `references.toml`, the matched Sail override and the four guest expectation
files are now one S-expression document form each — `profile.sexp`, `state.sexp`,
`sources.sexp`, `references.sexp`, `reference/sail-rv64i-lab-v0.override.sexp`,
`guests/*.expected.sexp` — validated by six new schemas (`schema/{profile,state,sources,
references,override,expectations}.sexp`). `convert_dossier.py --verify` proves the migration
the way `.3` did: every document re-derives field-for-field from its source, and the comment
census is exact line by line.

⭐ **Comments became first-class forms.** The schema kernel reserves one head — `(comment "…")`,
inert at any position, never declared, never forbidden — and the dossier's 158 comment lines
(the warnings, the provenance, the "why" of 26 decisions) survive as data a merge can carry
instead of syntax a parser drops. A typo'd `commment` is still refused by name; a construct,
operator or field named `comment` is refused as dead vocabulary. The open question the tree
carried — do comments belong to the form or the file — is answered: to the file, as an ordered
annotation stream.

**Consumers changed at the seam, not in their logic.** Every gate and tool keeps receiving the
exact dicts `tomllib`/`json` produced, now through the single mapping owner
`scripts/dossier_sexp.py` — which is what makes the verdicts mechanical rather than hopeful:
`PROFILE-CONSISTENCY`'s 39 arms re-fire on converted fixtures (rule 5b included), `run_smoke`
and `compare_platforms` are unmoved, the regenerated G0 report's diff is input names only, and
the Sail override's JSON is *derived* from the tracked `.sexp` on every run — byte-identical to
the original it replaces, the `.sexp` the single source of truth. `compare_readers` sweeps 28
of 28 files across all three readers. Measured en route: the DOSSIER's "no gate has been run"
was stale (`G0` has run; verdict `incomplete`) — corrected; `schema/` reached its file-count
ceiling at exactly 12 and was re-derived to 24, grounds recorded in the registry; the
`profiles/` per-part re-derivation `.3` carried open was not needed (`references.sexp` is
30,012 B against 32,768).

====

## SEMILITH-SF-0058 (leaf SOT-FORMAT.3) — the records move behind the schema layer

`profiles/rv64i-lab-v0/{requirements,contract-obligations}.jsonl` (26 + 34 records) retire into
`{requirements,contract-obligations}.sexp`, one form per record, JSON keys verbatim as field
names. The losslessness the acceptance demands is a comparison, not a review:
`convert_records.py --verify` re-derives the JSONL from the converted files **byte-identical**,
field by field, both catalogues.

⭐ **The schema layer grew four field facets rather than go weaker than the contract it
replaces** — `(pattern …)`, `(min-length N)`, `(min N)`, `(unique yes)` on `(field …)`, the
`.2` boundary one level down (a new declaration KIND would change the kernel; facets on the
existing kind are the language; the fixpoint declares them). And `parameters` stopped being a
lie: the old JSON schema's `additionalProperties` banned the very arrays three obligations
write and the validator never descended into it — the new format types every value
(`(int …)/(str …)/(true)/(false)/(null)/(ints …)/(strs …)`) and refuses a float, a mixed list
or a nested value by name.

**`RECORD-SCHEMA` reads both tracks now**: the frozen `examples/` JSONL on the tracked JSON
validator; the converted catalogues through the single mapping owner `scripts/records_sexp.py`,
validated by the schema layer plus every cross-check (CITED / RESOLVED / COVERAGE / LINKED /
OBLIGED / AUTHORITY) re-fired against the converted form — 22 arms where 15 stood, each RED arm
naming its reason. `gate_report.py` reads the same mapping; the G0 report diff is input names
only (26 requirements, 34 obligations, 68 checks, verdict untouched). `compare_readers` sweeps
13 of 13 with the catalogues and the two new schemas in corpus; `run_smoke` and the 52-of-52
verdict are unmoved. Measured en route: `LIVE_STATUS.md` had carried the contract as 33
obligations / 66 checks since before `P0-PROFILE.10`; re-derived to 34 / 68.


## SEMULITH-DS-0002 (leaf DOC-SHARDING.1) — the fired ceiling gets its sharder, and the freeze gets its proof

**Measured trigger.** `CHANGELOG.md` sat at 65,527 of 65,536 bytes — 9 bytes of headroom, recorded
at adoption as transition debt with this leaf as its named owner. The registry's owner column
promised *shard when the ceiling fires*; this slice is the sharder, not another compressed entry.

**What landed.** `scripts/shard_history.py` moves the oldest whole `## ` entries — byte-verbatim,
a file is preamble plus concatenated blocks, so head-after + shard == head-before exactly,
asserted and printed at the event (29 entries: 28 kept + 1 moved, order and bytes exact). One
entry moved (`SEMILITH-P0-0031`, 3.4 KiB); the head rewrote 65,527 → 62,086 bytes, under target
with room for this entry. Re-running is a no-op. The two existing date-named shards stay
untouched — a shard's entries are never edited — and join the new freeze manifest
`docs/changelog/SHARDS.sha256` (3 rows, sha256sum format, paths repo-root-relative).

**`SHARD-FREEZE`** — the 13th project doctrine, 12 self-test arms, each RED arm naming its reason —
proves the durable half: every shard hashes to its manifest row (one edited byte after the event
fails with both digests named); the manifest only grows against `git show HEAD:…`; no `## `
heading appears twice across head and shards. ⛔ Fired RED on the real tree before registration:
with no manifest yet, both existing shards reported `UNMANIFESTED` — the adoption gap itself, not
a synthetic stand-in. ⭐ The completeness proof belongs to the shard event (the tool holds both
sides exactly once); the freeze proof belongs to the manifest (it holds every side forever) —
splitting the two halves is what makes each half checkable.

**Lockstep, because mirrors rot.** Both doctrine mirrors gain the row (`DOCTRINE_ENFORCEMENT.md`
and the book chapter, per `REGISTRY-MIRROR`); `LIVE_STATUS.md`'s derived counts move 12 → 13
doctrines and 157 → 169 self-test arms — re-derived by `check_derived_counts.sh --list`, never
incremented by hand; `README_POLICY.md`'s transition-debt note records the discharged half and
leaves `DEV_NOTES.md` its still-live trigger for the day its ceiling fires.

## SEMULITH-RM-0060 — browser/Wasm target

`decision_browser-wasm-target`; lane `PORT-WEB` (consumed by `P1-LAB`).

## SEMILITH-SF-0057 (leaf SOT-FORMAT.2) — the constructs already in use, declared as data

The schema layer leaves paper: `schema/encoding.sexp`, `schema/fragment.sexp` and
`schema/semantics.sexp` declare every construct the three corpus families write — records and
positional mini-languages alike. The schema language gains exactly one new declaration kind,
`(operator (name SYM) (fixed N) | (variadic) [(min N)] [(arg SPEC)])`, for the shapes no record
grammar can state: `(fixed (31 25 0x0) …)` triples, `(operands rd rs1 rs2)` lists, the
`(pieces (12 12) …)` pairs, and the semantics effect expressions. `scripts/check_semantics.py`
now loads its 32-form table from `schema/semantics.sexp` — a new semantic form is a schema
edit, zero lines of Python (demonstrated with a 33rd form, then reverted). The `52 of 52`
verdict is byte-identical; the four MODEL-METHOD.9 controls still fire RED. Kernel self-test
`16 → 31 arms`; the whole corpus validates against its schema; `compare_readers` sweeps the
three new files the moment they are tracked (`9 of 9 agree`, document layer zero class notes).
The layer that never reads a second file: operand scoping stays in the checker. Gate
registration stays deferred to `SOT-FORMAT.6` per the tree's frontier. Tree `SOT-FORMAT` at
5/10.

## SEMULITH-RM-0059 (leaf ROADMAP-V3.3) — ROADMAP v0.3: the star gets a start condition

`ROADMAP.md` supersedes v0.2 (the house pattern: the delivery manifest and git carry the old
bytes; v0.2 was `live`, so no disposition change was needed). v0.3 lands the adopted package:
P1's start condition (`SOT-FORMAT.2` constructs + `MODEL-METHOD.10` extraction contract — the
remaining format-migration leaves are consumed by later milestones, not by P1's start); the
execution-authority row in the §1 decision table (semantics are data and the data executes);
the lane-consumption rule in §1; P1's G1 sharpened to the star-facing proof — a compiled
freestanding guest program retires under first-divergence comparison, C named as the first
guest path, and the first mdBook increment ships in the same milestone; the v0.4 trigger moves
to P1 first-slice completion. Under review, `LIVE_STATUS.md`'s `MODEL-METHOD` count was
re-derived: `3/10` (a spelling no gate can see) → `6 of 13` (the gated spelling). File: 24,065
bytes against the 24,576 ceiling. Tree `ROADMAP-V3` complete, 3/3.

## SEMILITH-RM-0058 (leaf ROADMAP-V3.2) — every lane names the milestone that consumes it

The sequencing vacuum, measured rather than asserted: `27` commits since any milestone tree
was last touched, and that touch was P0 closure. The roadmap's warning ("evidence tooling does
not become an unrelated research product") becomes an operational rule: every cross-cutting
tree's Metadata declares `Consumed by:` — milestone plus latest consumption point; lanes
without a named consumer are descoped at the next roadmap revision; new lanes must name a
consumer at proposal. First application covers all seven current lanes. The mechanical census
gate is **proposed to the director, not registered** — new governance is announced before it is
tasked. Record: `docs/decisions/decision_lane-consumption.md`; tree `ROADMAP-V3` at 2/3.

## SEMULITH-RM-0057 (leaf ROADMAP-V3.1) — the semantics data is the execution authority

Director-delegated decision (`2026-09-27`: "the decision is yours to make but it got to be sota,
signoff and production-grade") resolving the open contradiction between `docs/ARCHITECTURE.md`
§1.1 (semantics are data) and §2 (canonical Rust semantic functions): P1 executes the 32-form
semantics data directly — a definitional interpreter, keeping exactly one owned implementation
per rule (OWN-01); compiled or IR handlers enter only as generated, fingerprinted artifacts
behind an observational-equivalence regression. The pattern is the one this project's own pinned
Sail reference uses: the interpreter is the reference behaviour; compilation of the same
semantics is a derived artifact that must agree with it. Revisit conditions named: a measured
P2/P4 performance need, or the explicit semantic-IR migration decision. Record:
`docs/decisions/decision_interpreter-before-compiler.md`; tree `ROADMAP-V3` registered (1/3).

## LS-002 → `verified` — the design question closes with a re-run, not a changelog

Upstream confirmed the kind-strict grammar (`77d7b3db1`) and the native adapter (`df845ce61`)
are ancestors of the published pin `a8d34c845` — checked mechanically here with
`merge-base --is-ancestor`, not taken on their word — and prescribed the verification
instrument: `sexpr_file` with `SExprDocumentV1.spec` (the old `lispish_file` adapter is
insufficient). That instrument is exactly what `SOT-FORMAT.10` just added: LS-002's own four
cases re-run through the document layer return distinct kinds for every quoted/bare pair, and
the consumer's whole corpus agrees with its canonical reader there with zero classified
residue. The record gains the `verified-against` pin and the captured transcript; `VERIFIED.md`
carries the reply to upstream in the same envelope as the report. All three of this project's
LinkedSpec issues are now `verified`.

## SEMULITH-SF-0056 (leaf SOT-FORMAT.10) — the document grammar joins the agreement sweep

Director decision on the recorded candidate: adopt SExprDocumentV1 **additively** — a third
reader in `compare_readers.py`, never a replacement. The Lispish layer stays as what it is (the
LS-001/LS-002 regression guard, CLASS notes and all); the new document layer answers both CLASS
families by construction — tagged kinds keep `"20260911"` a `string` (quoted-numeric cannot
arise), raw lexemes decoded on OUR side with sexp.py's own escape table (escape-retention
cannot arise) — and it compares **every** form in every file, not the first. 28 self-test arms
(7 new), and the falsifiable acceptance was exceeded: **6 of 6** tracked files agree in the
document layer with ZERO class notes, because `schema/schema.sexp` itself joined the corpus and
passes both layers — the schema language's fixpoint now also verifies through the document
grammar. Upstream's instruction for LS-002 verification ("use `sexpr_file` with
`SExprDocumentV1.spec`; the lispish_file adapter is insufficient") describes exactly this
layer — which is what the next commit uses to close LS-002.

## SEMULITH-UT-0055 (leaf UPSTREAM-TRACK.4) — the reply travels in the same envelope

Director instruction `2026-09-26`: the verification acknowledgment to LinkedSpec is a
git-tracked note inside the bug's own directory. The subtree was already the envelope a
maintainer copies out — `VERIFIED.md` is now the reply inside that envelope, beside the report
it answers: what shipped, what we re-ran against which pin, the result, what it unblocks, and
where the residue lives (for LS-001: classified under LS-002, not this defect).

The note is gated, not just written: `UPSTREAM-INDEX` refuses a `verified` state whose subtree
carries no `VERIFIED.md`, and refuses a note that does not name the pin the record was verified
against — the note and the record must agree the way the indices and the record must agree.
Fired RED on the real tracker against both LS-001 and LS-003 before the notes existed; 17 arms
(16 → 17) with the wrong-pin refusal; green after, both notes self-contained and pin-consistent.

## SEMULITH-SF-0054 (leaf SOT-FORMAT.1) — the schema language, written in itself

The gap was "it parses": an S-expression reader accepts anything syntactically, so a mistyped
head or field was invisible. `schema/schema.sexp` now declares the language in itself —
`(construct (name …) (field …)…)`, atom fields, form fields in the corpus's two house shapes
(`(source (file …) …)` whole-list and `(effect (set …))` value-held), `(empty yes)` markers
for the corpus's `(requires)`/`(extensions)` idiom, `(values …)` spellings, sibling repetition —
and `scripts/check_sexp_schema.py` (16 arms, 13 RED, each naming its construct, field and
reason) validates any file against any schema. The fixpoint is the proof, not a slogan:
`schema.sexp` conforms to `schema.sexp`.

⭐ The first design assumed a tidy uniform `(name value)` pair grammar — and the real corpus
refuted it before it shipped. Reading `rv64i.sexp`/`rv64i.sem.sexp` first is what made the
language fit the files `.2` must declare; an invented grammar would have met the corpus as an
argument. `schema/` is registered in `doctrine/readme_routes.tsv` in its creating commit, and
`TOOLBOX.md` gains the row.

## SEMULITH-SF-0053 (leaf SOT-FORMAT.8) — the contract names its format at last

The mdBook chapter *"Architecture and canonical definitions"* includes `docs/ARCHITECTURE.md`
verbatim, and that document named no format, no `definitions/` directory and no composition —
four commits had introduced all three, and the director's only window showed none of it
(`grep -c 'S-expression'` → 0). The drift is closed at the source document: §1.1 records the
one-format decision and what exists in it today (fragments, cited semantics at 52 of 52, the
two-reader agreement check), §1.2 defines the fragment and the composition operator that is
*decided, not hoped* (`check_encoding_disjoint.py`), §1.3 states the schema layer's contract and
labels it specified-not-built. Built claims name their instruments; pending layers say pending;
the one count that moves (`5 of 5`) was rephrased to "agreement file by file" so the prose
cannot drift. `make book` builds; the chapter preface needed no edit — that was the point.

Also: a knowledge card for the session's other lesson — a director-named action runs first,
right after context recovery; standing cadences queue behind it.

## SEMULITH-UT-0052 (leaf UPSTREAM-TRACK.2) — `verified` must carry the re-run that earned it

The tracker already refused a `verified` with no pin. It now refuses the next hole too: a
`verified` whose event names a pin but captures no `(repro …)` output **inside the subtree** —
the pin retires upstream's changelog claim, but only the captured run retires ours. Four new
self-test arms (pin-without-repro, artifact missing, artifact escaping the subtree, pin+artifact
accepted); `16 pass / 0 fail`.

⛔ **Fired RED on the real tracker before any artifact existed** — the strengthened gate refused
LS-001's just-committed `verified` ("captures no (repro …) re-run output", rc=1). Then the
evidence landed and every state became earned, not asserted:

- **LS-001 → `verified`** — the reproduction re-ran and was captured into the subtree itself:
  `evidence/verified-a8d34c845.txt`, `8 matched / 0 differed`. A maintainer copying the issue
  directory out now carries the proof with it.
- **LS-003 → `verified`** — the three first-consumer papercuts are remedied in the guide at the
  adopted pin, and each remedy was *exercised* during the pin update (workspace exclusion,
  prerequisite chain, maintained wrapper), transcript captured — exit statuses, not banners,
  per the guide's own warning.
- **LS-002 → `acknowledged`** — upstream took ownership by name: the LS-001 fix commit records
  "LS-002 and related kind/strict requirements remain .83.1 owned". No re-run owed; the design
  question is theirs until it ships.

## SEMULITH-SF-0051 (leaf SOT-FORMAT.9) — the pin moves, the readers agree, the loop closes

Director instruction `2026-09-26`: upstream fixed and pushed the reported bugs, so the LinkedSpec
pin advances `ad290bdb4` → `a8d34c845` (`origin/main` tip, ~120 commits). The update followed the
guide's own flow — fetch, check out the reviewed revision, re-verify, THEN commit the pointer.
RGX stays at `8763a0e6` on both pins (bootstrap: "already generated", a no-op); the consumer
rebuilt in 20.39 s.

**LS-001 is `verified`, not just `fixed-upstream`.** Our self-contained reproduction re-ran
against the new binary and grammar: `8 matched / 0 differed` (was 4/4), and both readers now
agree on **all five** tracked `.sexp` files, including the 43-form catalogue that had read as 6.
The issue record, both index mirrors and the REPORT carry the `verified-against` pin the
UPSTREAM-INDEX gate requires.

**The fix moved the disagreement one layer down, and that layer is enumerated, not hidden.**
The corpus census found exactly four residue atoms in `materials/catalog.sexp`: two
quoted-numeric strings (`"20260911"`, `"1992"` — Lispish discards quote-kind, LS-002) and two
escape-retained strings (`\"` kept verbatim — the guide documents this). Both are CLASS families
in `compare_readers.py` now: each is anchored to exact byte meaning (`sexp._atom(A) == B`
exactly; decoding B with sexp.py's own escape table reproduces A exactly), with 9 new self-test
arms (4 GREEN classification, 5 RED masking) and a fired RED proof — the pre-fix grammar still
makes the comparator report the original 43-vs-6 defect, rc=1. "Agree" still means same structure.

**Named departure, one.** The guide now prescribes copying the consumer source into the
application's crate; semulith builds the vendored example workspace in place (virtual root
manifest has no package to own it) — recorded in the tree, to revisit when the engine adopts the
reader. Upstream's document grammar (SExprDocumentV1, tagged kinds) is the durable answer to both
CLASS families when that day comes.

## SEMULITH-AC-0050 (leaf ARTIFACT-CLEANUP.1) — the first §8 cleanup, measured and recorded

Session-directive §8 requires an artifact cleanup roughly every 24 h, tracked in
`docs/ARTIFACT_CLEANUP.md`. The file did not exist — the "no file → clean this session" trigger
fired — so the cleanup owns a task-tree now, the same as any other change.

**Census before deleting anything** — 22 `.bin` under `target/`, 18 under `.app-data/target/`,
all of them cargo incremental caches in the directive's enumerated scope; 7 crate **source**
fixtures under `.app-data/cargo-home/` (inputs, not artifacts — kept); 13 reference-run logs
under `target/refs/` (kept: evidence trails, 1.3 MB, outside the enumerated cargo dirs).

**Measured, not asserted:** 40 files / 341 MB deleted (`.app-data` 1.4 G → 1.1 G); zero after;
`git status` shows only the intended tracked files. The record is overwrite-only — one date and
one line per run, so the file can never become the changelog it exists to prevent — and it is a
governed live surface from its first commit (registered in `doctrine/readme_routes.tsv`).

## SEMULITH-UT-0048 (leaf UPSTREAM-TRACK.1) — the issue owns its state, the indices are mirrors

**Two director instructions that turn out to be one design.** *"For each vendor keep an index of
all the bugs you reported, their state"* and *"the subtree for each bug shall be self-contained"*
cannot both be satisfied by a maintained index: if the subtree carries its own state, then every
index is **derived**, and a derived thing that nobody checks drifts. That is exactly why
`FRONTIER-SYNC` and `REGISTRY-MIRROR` exist facing inwards. This is the same doctrine facing out.

Measured before building — the same facts in three places, and nothing checking them:

```
$ grep -c 'LS-00' docs/upstream/README.md                      -> 4  rows
$ grep -c 'LS-00' docs/upstream/linkedspec/README.md           -> 5  rows
$ grep -l 'State' docs/upstream/linkedspec/*/REPORT.md | wc -l -> 3  reports
$ grep -c upstream scripts/check_doctrines.project.sh          -> 0  gates
```

**Each issue now carries `issue.sexp`** — the single owner of its id, severity, state, affected
pins, fix status and dated history, living inside the subtree it describes. An S-expression,
because an issue record is a source of truth like any other
(`decision_one-format-every-source-of-truth`).

**`UPSTREAM-INDEX`** (12 arms, 10 of them RED) checks both indices and each `REPORT.md` against
the records, in both directions: stale state, stale severity, an issue with no row, a row with no
issue, an invented state or severity, a directory with no record, a report disagreeing with the
record beside it, a `verified` claim with no pin, and a directory whose name does not carry its id.

⛔ **It caught three real violations in the tracker it was written for**, which is the only
evidence worth having that a gate discriminates:

```
NOT CONTAINED LS-001: …/evidence/patched.txt:1 references '/Volumes/' — outside its own subtree
NOT CONTAINED LS-001: …/evidence/shipped.txt:1 references '/Volumes/' — outside its own subtree
NOT CONTAINED LS-001: …/issue.sexp:4      references 'scripts/'  — outside its own subtree
```

A maintainer copying that directory out would have got a machine path from my disk and a pointer
to this repository's tooling. Fixed in the content, not in the gate.

⛔ **Two failures worth keeping.** Three arms failed at first *for the wrong reason*: the fixture
computed `${1%%-*}` on `LS-001-a` and got `LS`. The fixture was wrong, not the gate — fixing it
took 8/12 to 12/12. And the gate exited 1 printing **nothing**, because `set -e` aborted the
assignment before `rc` could be read: a breach with no reason is indistinguishable from a crash.

**`docs/tasks/` crossed its aggregate ceiling** on the way through, by 3,057 bytes. Raised under
[`decision_task-tree-family-bound`](docs/decisions/decision_task-tree-family-bound.md) — which
records the two rejected alternatives first, because raising a bound because it fired is the
reflex the registry warns against. Compaction was checked (the archive is not a duplicate of its
tree) and a subdirectory was rejected for a mechanical reason: `check_frontier_sync.sh` matches
index links with a **flat** pattern, and breaking a gate to satisfy a bound is a worse trade. The
grounds are real — the family was bounded when the project tracked 17 lanes and now tracks 25,
two of them created this session on instruction. ⛔ **The per-part bound is untouched**: the
aggregate answers "how many lanes", the per-part answers "has one tree become a monolith", and
only the first question changed.

## SEMULITH-SF-0047 (leaf SOT-FORMAT.9) — two readers, one format, and a defect worth reporting

**What landed.** LinkedSpec published its integration document (`ad290bdb4`), discharging the
blocker this tree had carried since `2026-09-14`. `vendor/linkedspec` is now a submodule **pinned
to that exact commit**, with RGX `8763a0e6bea9` and PGEN `db6f8c6836fe` — the revisions the
guide's own evidence section names. The documented PGEN bootstrap produced all four `generated/`
products; the consumer built in 32.15s.

**The point of the leaf was never the submodule — it was the agreement.** Two readers of one
format that disagree is the defect `SOT-FORMAT` exists to prevent, and it hides: each reader is
self-consistent, each passes its own tests, and the disagreement surfaces only as a model that
behaves differently depending on which tool built it. `scripts/compare_readers.py` (11 arms) now
compares both over every tracked `.sexp`:

```
agree   definitions/riscv/m.sexp             438 nodes identical
agree   definitions/riscv/rv64i.sem.sexp    1550 nodes identical
agree   definitions/riscv/rv64i.sexp        1716 nodes identical
agree   profiles/rv64i-lab-v0/encoding.sexp   18 nodes identical
DIFFER  materials/catalog.sexp  <root>: A has 43 element(s), B has 6
```

⛔ **The defect.** A double-quoted string containing **LF** is not read as one string by
`specs/Lispish.spec`. It does not merely lose its newline — it stops being a string, and its
remaining text is re-lexed as syntax, so a `)` in the continuation closes a form that was never
open. Our 43-form catalogue read as 6, with 37 nested inside the fifth, **exit 0, no diagnostic**.

Located by refutation rather than guessing: `;` inside a string and parentheses inside a string
were both hypothesised and both **refuted** — the reader handles them correctly. Spaces, parens,
TAB and CR inside a one-line string all round-trip. Only LF breaks it, which points at
`Lispish.spec:69`, `/"(.*?)(?<!\\)"/` — `.` does not match LF without DOTALL — after which the
text falls through to `others: /[^\s"{}()\[\];]+/` and splits on whitespace.

**The fix was validated before being reported**, on a *copy* of the spec so the pinned submodule
stays clean: `(?s)` on lines 69 and 71 takes the reproduction from `4 matched / 4 differed` to
`8 matched / 0 differed`, and makes all five files agree. It is LinkedSpec's change to make —
patching a pinned submodule is how a pin becomes a fork.

⚠️ **The leaf is `blocked`, not `done`.** Its acceptance says the readers agree on *every* tracked
file; they agree on four of five. Rewriting the criterion to match the result is the only real
failure available here.

**An upstream issue tracker**, `docs/upstream/`, because a defect found in a dependency is work
this project owns until it is verified fixed. Each issue is a **self-contained sub-tree** a
maintainer can copy out and run without this repository — REPORT, VALIDATE, a repro script, one
file per case, an expected-values table, our captured evidence, and where we have one, a candidate
patch. Verified self-contained by copying each sub-tree to a scratch directory and re-running it
there.

Three issues raised, each with an id, a severity and a state:

| ID | Title | Severity | State |
| --- | --- | --- | --- |
| `LS-001` | a double-quoted string containing LF is not one string | `high` | `draft` |
| `LS-002` | quoted and bare atoms are indistinguishable — no consumer can round-trip | `medium` | `draft` |
| `LS-003` | three first-consumer papercuts in the integration guide | `low` | `draft` |

⛔ The state vocabulary keeps `fixed-upstream` and `verified` apart on purpose: **a fix we have not
re-run is a claim**, and adopting a new pin on the strength of a changelog entry is how a consumer
inherits a regression. Severity is graded by whether the consumer is *told* — silence is what makes
`LS-001` high.

⭐ Two integration consequences worth their own line, both measured here. Our doctrine gates now
walk a vendored tree: `check_fixture_fingerprints.sh` **died with RecursionError** on 1.7 GB of
another project's JSON, and `RECORD-SCHEMA` judged their records by our schema. Exactly two gates
walk the filesystem — the other four use `git ls-files`, which sees a submodule as a single entry
— so both were fixed and the reason written beside the exclusion. And the bug reports' own
`cases/*.sexp` are deliberately pathological, so they are excluded from the reader-agreement sweep
with an arm proving it: a corpus and a bug-report fixture must not share a scan.

⛔ **Three departures from the published guide, all mine, all named in the tree.** I jumped to the
line the director pointed at and skipped *Initial PGEN preparation* 100 lines earlier — the guide
says plainly that checkout does not generate PGEN's parser inputs, and I had not read it. I used
`--recursive` where two targeted inits were prescribed, costing 1.7 GB and 30 nested submodules. I
used bare `cargo` instead of `tools/run_cargo_local.sh`. A guide is only followed if you read the
part before the part you were sent to.

## SEMULITH-PD-0046 (leaf PUSH-DISCIPLINE.1) — the push boundary gets a gate that refuses

**Director instruction, `2026-09-14`:** *"Set the push cadence to every 300 commits. Exceptional
push happen from time to time, but they shall require my approval."*

**Measured before writing anything, and the finding is an absence:**

```
$ grep -ci push COMMIT.md          ->  0     the normative commit workflow never mentions pushing
$ ls .githooks/                    ->  commit-msg  pre-commit     (no pre-push)
$ git rev-list --count origin/main..HEAD  ->  45
```

45 commits had exactly one governance rule between them and a server: a human remembering. The
policy was not being broken — it did not exist.

**Why a push is governed differently from a commit.** A commit is local and reversible: reword it,
drop it, rebase it, and nothing outside this disk ever knew. A push sends bytes to a server that
may keep, cache, mirror or index them regardless of what happens here afterwards.

⛔ **And the specific failure this guards against is an agent's.** An assistant asked to "finish
up" will naturally read pushing as tidying, and will reach — reasonably, on its own — the judgement
that this particular push is surely fine. So the hook **refuses rather than warns** (a warning at
an outward-facing boundary is read after the bytes have left), and **the director grants the
exception while the variable only carries it**:

```
$ bash scripts/check_push_cadence.sh --status ; echo $?
PUSH-CADENCE: REFUSED — 45 commits since the last push; the cadence is 300 …
  Two ways forward, and only two:
    1. Wait. The cadence is 300 commits; this is 45.
    2. Ask the director. … SEMULITH_PUSH_APPROVED='<the director's reason>' git push
  ⛔ An agent may not supply this on its own judgement.
1
```

**11 arms, each in a throwaway repository with a real upstream** — a gate about
distance-from-upstream cannot be tested without one. Three were fired RED first and failed: two
because the refusal message wrapped across a newline so a literal match missed it, and one because
`COMMIT.md` did not yet state the cadence — the no-duplicated-fact arm doing its job before the
fact existed.

⛔ The instrument refuses on `DETACHED`, `NO-UPSTREAM` and `NOT-A-REPO` rather than printing a
distance it cannot know. "0 commits ahead" for a detached HEAD is a lie that *permits* a push.

**The accepted exposure is on the record, not discovered later.** 45 commits exist only on one
disk and cadence 300 means they stay there a long while. `decision_push-cadence` states that
plainly, so it remains a decision someone made rather than an oversight nobody revisited.

New tree `PUSH-DISCIPLINE` (3 leaves). `.2` is next and is Policy 16's unenforced half: full CI
runs before a push, and nothing enforces it — the pre-commit hook covers only the "selected checks
for ordinary commits" side.

## SEMULITH-MM-0044 (leaf MODEL-METHOD.13) — the corpus moved, and my survey had sampled rather than swept

**What changed at the source.** The primary-source corpus advanced three commits (`4201f50` →
`3c45e81`) and closed **both gaps this project measured and reported**, three commits after
reporting them: five AMD64 APM volumes imported (`e401a56`), Intel SDM Volume 1 imported
(`98de100`). It also pinned the full `v20260120` docs.riscv.org snapshot and **moved** the RISC-V
PDF — which made a tracked record in this repository false:

```
$ python3 scripts/materials.py --fetch RVI-ISA-PDF-20260911
  REFUSED: not at $SEMULITH_CHIPDOC_ROOT/risc-v/isa/current/riscv-isa-manual_…pdf
```

**What changed in my method, which is the more useful half.** The first survey enumerated by
**guessing vendor directory names** from memory. Every probe returned relevant results, so nothing
signalled absence. Re-swept by path shape instead, eight documents had been missed — including the
**entire M68000 architecture** (filed under `nxp/m68k/`, because NXP inherited Motorola through
Freescale) and **every board-class document in the corpus**: three ESP32 SoC manuals and the
RP2040 and RP2350 datasheets, which is the whole material base for `P5-BOARD`.

⭐ The giveaway I ignored: my own probe named a `motorola/` directory that does not exist. A probe
naming something absent is a signal, and I read it as nothing.

The catalogue now carries a `derivation` field naming the sweep command, so the method can be
judged rather than believed. **22 → 36 materials**, 36 of 36 fetched and digest-verified.

**Both gaps closed with evidence, and kept.** A deleted gap erases the fact that the question was
ever asked, so each carries `(status resolved)`, what closed it, and — for AMD — a `(residual …)`
noting their doc hub is not scriptable, so a newer revision could exist uncaptured. A gap closed is
not a gap that cannot reopen.

⭐ **A material that is not one file.** The pinned snapshot is 72 HTML pages, and a snapshot
identified by the digest of one page is not identified at all. `kind snapshot` names a `manifest`
whose digest is the material's identity and whose entries verify every page — `72 manifest entries
verified` on fetch, and a tampered page inside a verifying snapshot is caught (new RED arm).

⭐ **That ends a real fragility.** The citation evidence lived only in an untracked working area
needing the network — the reason `check_citations.py` could not be a gate. It now runs from the
manifest-verified cache, **offline**, and prints which route it used:

```
via fetched working area target/sources/riscv-v20260120        -> 52 of 52 resolve
via materials cache .materials/riscv/pinned-v20260120/unpriv   -> 52 of 52 resolve
```

⭐ **Independent corroboration of the pin challenged last leaf.** chipdoc acquired the `v20260120`
snapshot by its own route; its digests for `intro`, `rv32` and `rv64` **equal** those committed in
`sources.toml`, and its manifest verifies 72 of 72. Two acquisitions, two parties, one set of bytes
— the one thing an agreement between us could not have produced.

⛔ **The reader refused this leaf's own first draft.** The catalogue generator emitted literal
`\uXXXX` escapes and `scripts/sexp.py` rejected the file by name — `unknown escape '\u'`. That is
`SOT-FORMAT.7`'s closed escape table doing its job one leaf later, on real content rather than a
fixture. The content was fixed; the reader was not touched.

Corpus drift is now **detected rather than discovered**: `--list` and `--verify` compare the
catalogued revision against the checkout's `HEAD`.

**Knowledge.** [`a-survey-that-found-things-can-still-have-missed-things`](docs/knowledge/a-survey-that-found-things-can-still-have-missed-things.md)
— a zero prompts "is my instrument blind?"; twenty-two results prompt nothing at all. Enumerate by
a property of the thing, never a list of names you wrote from memory, and read what your
enumeration excluded before you believe it.

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


