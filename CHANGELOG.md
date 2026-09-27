# CHANGELOG.md

## SEMILITH-PL-0005 (leaf P1-LAB.5) — four typed outcome families, SEM-01 made structural

- `semulith-core::outcome`: `TargetEvent` (`Exception` with the unprivileged cause vocabulary, each cause named by its rule; `RequestedTrap` for ECALL/EBREAK — delivery is a data event, not a stop command), `Advance` (`Completed`, `Stop{reason}` — no waiting/partial advance, platform facts recorded in the docs), `ModelError` (`Unimplemented`/`InvalidDescription`/`InconsistentState`/`ContractViolation` — `.4`'s boundary-local violation re-homed), `UndefinedCase` (`ReservedDecode` — REQ-D-RESERVED-DECODE's case carried as its own outcome, never auto-converted to an exception). `StepOutcome` is the step-level sum `.8` produces and the harness matches.
- The acceptance proven by a stub stepper (test code, not production semantics): `a_delivered_exception_lets_execution_continue` (harness records the `Breakpoint` trap, the next instruction still runs, pc advances past all three); `an_unimplemented_instruction_is_not_an_illegal_instruction_trap` (the `Failed` arm has no typed expression that reaches an `IllegalInstruction` `Exception`). Plus family distinctness, the `ContractViolation` re-home round trip, and `UndefinedCase` ≠ `Exception`.
- Verification: 5 new suites green; `make check` 5 suites / 43 tests / 0 warnings; wasm build green; `make gate` green.
- Lockstep: MEMORY/LIVE_STATUS/TASK_TREE/book P1 chapter and this tree; frontier moves to `.6` (canonical definition skeleton).

## SEMILITH-PL-0004 (leaf P1-LAB.4) — the environment boundary, and fixtures that answer it

- `semulith-core::env` owns the request/response contract the CPU crosses: `Request` (Fetch — width pinned to 32 by construction, OB-ENV-FETCH-SUPPLY; Load/Store at `AccessWidth` B/H/W/D, OB-ENV-ACCESS-WIDTHS — an unofferable width cannot be formed), `Response` (raw bits, no extension — REQ-D-LOAD-EXT stays instruction-layer), and two failure families kept apart by construction: `Failure` (target-facing: AccessFault, Misaligned — the profile's "not substituted" rule) and `ContractViolation` (the environment broke a rule; SEM-01's separation, boundary-local until `.5`). One trait, `Environment::request`, drives every crossing. Addresses are bare `u64` (SEM-05).
- `semulith-verify::fixtures` implements it: `FlatMemory` — one little-endian main-memory region, no side effects (OB-MAIN-VS-IO), re-read per fetch so stores are immediately visible (OB-CODE-VISIBILITY), fetch counter as the no-extraneous witness, alignment judged before region membership (stated, tested); `ScriptedEnv` — the conversation pinned in advance, faults scriptable, and a request the script does not cover reports `ResponseMismatch`/`ScriptExhausted` instead of inventing data (§4.1.4's negative-fixture rule, exercised for real).
- Verification: 16 new suites green (12 fixture + 4 contract-property), all without an instruction handler; `make check` 5 suites / 42 tests / 0 warnings; wasm build green; `make gate` green.
- Lockstep: MEMORY/LIVE_STATUS/TASK_TREE/book P1 chapter and this tree; frontier moves to `.5` (typed outcome families).

## SEMILITH-PL-0003 (leaf P1-LAB.3) — architectural state, generated from the descriptor

- `semulith-core::state` exists, and it is generated: `scripts/gen_state.py` derives `state.rs` from `profiles/rv64i-lab-v0/state.sexp` through `dossier_sexp` (the single mapping owner), byte-deterministically, with the input's sha256 in the module header (OWN-03). The generator is deliberately narrow — it refuses, naming the construct, any descriptor shape it cannot emit (another profile, a non-64 width, an unmapped special register, a missing SEM-08 census). The 21st registered doctrine, `STATE-GEN` (`scripts/check_state_gen.sh`), re-runs its 6-arm self-test before judging and refuses drift with the regeneration command; fired RED against a hand-edited module before registration. The owner→mirror pair is registered in `doctrine/fact_ownership.tsv`.
- The state: 32 × 64-bit integer registers + pc, 264 bytes inline, no heap (RUST-03); x0 hardwired zero (write discarded, read yields 0); the three ISA-chapter-named roles (x1 return address, x2 stack pointer, x5 alternate link) emitted as alias views over the one storage — C02's "does writing one alias affect every other view" answered by 10 test suites; laboratory reset per REQ-D-ENTRY-STATE/OB-ENV-RESET (x1..x31 = 0, pc = environment-supplied entry); SEM-08's hidden-state census carried as data (7 candidates checked, none present).
- Verification: 22 test suites green (12 arithmetic + 10 state); `cargo clippy --all-targets --all-features -- -D warnings` clean; workspace still builds for `wasm32-unknown-unknown`; `make gate` green with the doctrine registered and both mirrors (DOCTRINE_ENFORCEMENT.md, the book's doctrines chapter) in sync.
- Lockstep: `LIVE_STATUS.md` re-derived (21 registered, 237 self-test arms; P1 3/12); the name list in the doctrines row completed (STATE-GEN added; SCOPE-COVERAGE, omitted when it landed, restored); `MEMORY.md`, `docs/TASK_TREE.md`, the book's P1 chapter, and this tree updated. The frontier moves to `.4` (environment boundary and fixtures).

## SEMILITH-PL-0002 (leaf P1-LAB.2) — target arithmetic primitives, verified exhaustively at reduced width

- `semulith-core::arith`: 18 SEM-03 primitives — ALU register/immediate ops, shifts with the REQ-D-SHAMT masks as named functions, the `*W` word ops (REQ-D-WSUFFIX), `sext`/`bits` extraction and extension, LUI/AUIPC offset formation. Each contract states width, signedness, intermediate precision, truncation, exceptional behavior; each doc comment source-links the requirement record and pinned locator (REQ-D-ALU-REG/IMM, REQ-D-SHAMT, REQ-D-WSUFFIX, REQ-D-LUI-AUIPC, REQ-D-LOAD-EXT, REQ-D-XLEN). Unmasked shift amounts panic in debug instead of silently wrapping.
- Verification, the acceptance's shape: boundary suites at full XLEN; an **8-bit exhaustive layer** (every `(x, y)` for the binary ops, every `(x, shamt)`, every `(x, from_bits)`, every `(lo, hi)` window) against references formulated on a different host width; a 100k-draw boundary-heavy sweep of the word ops against a u64-width reference. 12 suites green; clippy `-D warnings` clean.
- The exhaustive layer failed on its first run for exactly the reason the acceptance exists: `slt`/`sar` are width-sensitive, and the naive low-byte comparison of signed ops is wrong — fixed by embedding the narrow signed view at XLEN. The lesson is promoted to `docs/knowledge/reduced-width-verification-of-signed-ops.md` (LESSON-PROMOTION satisfied in-commit).
- Scope, stated: the requirements' `implementation_status` stays `planned` — these are the executable halves; instruction-level obligation checks need the interpreter slice (`.8`). The frontier moves to `.3` (architectural state).

Validation: `cargo test -p semulith-core` 12/0; `cargo clippy --all-targets --all-features -- -D warnings` clean; `make gate` → `=== all doctrines green ===`.

## SEMILITH-PL-0001 (leaf P1-LAB.1, PORT-WEB.1) — the laboratory gets its three crates, and the browser target gets its gate

- `P1-LAB.1`: `crates/app` (the `semulith` placeholder) replaced by the three laboratory crates, wired per `docs/ARCHITECTURE.md` §4 — `semulith-core` depends on nothing (`Cargo.lock` carries no dependencies block for it), `semulith-verify` holds the fixtures home and depends on core only, `semulith-cli` (binary name `semulith`, ROADMAP.md §8) calls both. `make check` green at `-D warnings`; `cargo tree` shows the one-directional edges.
- `PORT-WEB.1` (same commit, as its acceptance requires): the workspace builds for `wasm32-unknown-unknown` from the first slice, enforced by the 20th registered doctrine, `scripts/check_wasm_build.sh` — it refuses with install instructions when the rustup target is absent, re-runs its 4-arm self-test before every judgement, and was fired RED against the real workspace (a `std::os::unix` import in `semulith-core`, refused naming `lib.rs:13`) before registration. CI's doctrines workflow now installs the Wasm target. No host-only API exists yet; the build itself is the standing proof.
- Docs in lockstep: mirrors in `DOCTRINE_ENFORCEMENT.md`, the book's doctrines chapter, `TOOLBOX.md`; `LIVE_STATUS.md` re-derived (20 registered, 231 self-test arms; P1 In Progress, 1/12) with a stale MODEL-METHOD row corrected; the book's P1 chapter now states the crates exist and build for host and Wasm. Fixed in passing: a layer-A typo (`sexr_file` → `sexpr_file`); the `DOCTRINE_ENFORCEMENT.md` ceiling re-derived 20 → 24 KiB in the routes registry (the 20th doctrine row is the surface's contract expanding, the same grounds as the TOOLBOX raise). Both append heads sharded again the day they were sharded — the pressure valve working as designed; the `docs/changelog/` file-count ceiling re-derived 20 → 40 in the same commit (the family now carries shards for two append heads — the derivation is recorded in the registry).

Validation: `make gate` green (20 doctrines); `make check` green (fmt + clippy -D warnings + 5 test suites); `bash scripts/check_wasm_build.sh --self-test` → 4 pass / 0 fail.

## SEMILITH-AC-0051 (leaf ARTIFACT-CLEANUP.2) — the sanctioned watcher is a ruling, not a false positive

The director ruled CHIPDOC's ChipdocWatcher ("it will stay there — do not worry about it from
now on"), and the ruling is now data: `doctrine/sanctioned_processes.tsv` carries the
executable substring, the ruling, and its date, and `check_no_background_jobs.sh` exempts
matching processes from both census arms — with the detection itself untouched, because the
census's whole design is that a list of things you thought of cannot see the thing you did not.
An agent proposes a row; only the director's ruling lands one. Verified both directions: the
live check prints `handoff: OK` with the watcher running, and the control probe (row absent)
flags the same process again. Tracked-content gates are unaffected.

## SEMILITH-MM-0050 (leaf MODEL-METHOD.6) — no coding without the source of truth, and MODEL-METHOD closes

The director's rule is a gate now. The unit registry gains `(requires …)` — the categories a
unit's scope declares — and `SCOPE-COVERAGE` (19th doctrine, 7 arms) refuses the day a required
category is `missing` or has no census row, fired RED before registration on a scratch unit whose
required category was absent. A unit with an undeclared scope refuses too: code may not start
against a scope never declared. `rv64i-lab-v0` declares its 14 in-scope categories, and the
verdict reads `1 unit(s) may code — every required category covered` — P1-LAB's precondition is a
verdict, composed with EXTRACTION (coverage says the facts are OWNED; extraction says they are
EXTRACTABLE). **`MODEL-METHOD` closes at 13/13**: the method in prose, the census, the
acquisitions, and the coding gate all landed; every P1 precondition is mechanical.

## SEMILITH-MM-0049 (leaf MODEL-METHOD.5) — the method, in prose, written to be learned from

`docs/METHOD.md` is the method this project actually exercised this session, written to be
carried: document → decision → requirement → obligation → check, with the ORDER justified at
each step and the rejected alternatives kept — a version string is not an identity, a laboratory
policy must never read as an architectural rule, one fact has one owner and every mirror is
governed, positive-AND-negative checks carry derived-not-copied values, and a check that cannot
judge never reports green over an absence. One rule — the shift-amount rule — is walked end to
end by name, its two non-mechanical steps flagged inside the walk. A closing section names the
four steps no gate can take (choosing the publication, classing the fact, judging the authority,
classifying the disagreement) and declares everything else mechanical — which is the method's
discipline, stated as a rule. The mdBook carries it verbatim under The contracts; the
carryability probe confirms the body depends on no tool, path, or id this project owns.

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

