# DEV_NOTES.md

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

Every dated entry here must reach the retrievable layer: a card under
[`docs/knowledge/`](docs/knowledge/INDEX.md), or a decision record, or an explicit decline in
the owning task leaf. That is the `LESSON-PROMOTION` doctrine, and the reason for it is that a
lesson nobody can retrieve by question is a lesson nobody has.

## _(2026-09-27)_ — architectural state, generated from the descriptor (P1-LAB.3)

Root cause: the state accessors of `docs/ARCHITECTURE.md` §2 existed only as a table row; the descriptor `state.sexp` had no executable half, and the C02 alias question had no code to answer it. Implementation: `scripts/gen_state.py` derives `crates/semulith-core/src/state.rs` from the descriptor via `dossier_sexp.load_state`, emitting fixed-width storage (`[u64; 32]` + pc, 264 bytes inline, RUST-03), the x0 hardwired discipline (write discarded, read masks to 0), the three ISA-chapter-named aliases as views over the one storage, the inspection-metadata table (`ELEMENTS`), and the SEM-08 census as data. Byte-deterministic; the input sha256 rides in the header. The `STATE-GEN` doctrine (`scripts/check_state_gen.sh`) regenerates in memory and refuses drift; self-test 6 pass / 0 fail; fired RED on a hand-edited module (rc=1, naming DRIFT) before registration. Validation: 22 suites green; clippy -D warnings clean; wasm build green; REGISTRY-MIRROR and FACT-OWNERSHIP re-run green after registration. Design notes, kept: (1) generated Rust must be emitted formatter-stable or the drift gate fights `cargo fmt` — the generator's output is the formatted shape, verified by regen-diff after `cargo fmt --all`. (2) `dossier_sexp.family_for` names the dossier family from the file NAME, so self-test descriptor surgery must keep the `state.sexp` basename (per-case directories). (3) The generator binds the descriptor's `xlen` to `arith::XLEN` at generation time — the executable owner of XLEN stays unique, and a descriptor/code disagreement is a refusal, not a choice.

Lessons: declined here (all three notes are P1-LAB-generation specifics; nothing here generalizes past `.6`, where the generation manifest lands).

## _(2026-09-27)_ — target arithmetic primitives, and the width-sensitivity trap (P1-LAB.2)

Implementation: `semulith-core::arith`, one function per semantics-data operation, contracts written to SEM-03 (width/signedness/intermediate precision/truncation/exceptional behavior per function), source links as doc comments naming requirement ids + pinned locators. The first code content in the workspace. Validation: 12 test suites — boundary at XLEN, 8-bit-exhaustive against different-host-width references (multiply-as-shift, De Morgan), 100k-draw word-op sweep; clippy -D warnings clean; gate green. Design notes, kept: (1) the exhaustive layer caught the signed-op width-sensitivity trap on its first run — `slt`/`sar` compared against an `i8` reference without embedding the signed view at XLEN; the primitives were right, the test was wrong, and the trap is now a knowledge card. (2) Unmasked shift amounts panic via `debug_assert` rather than silently wrapping — a decoder bug must not produce a plausible-looking wrong result; the masking rule lives in `shamt64`/`shamt32` next to the REQ-D-SHAMT citation. (3) `implementation_status` on the requirements stays `planned` until the interpreter can exercise instruction-level obligations — do not inflate status to match enthusiasm.

Lessons: promoted to `docs/knowledge/reduced-width-verification-of-signed-ops.md` (the width-sensitivity rule and the per-operation table).

## _(2026-09-27)_ — the laboratory crates and the Wasm gate (P1-LAB.1, PORT-WEB.1)

Root cause: the crate boundary was a `docs/ARCHITECTURE.md` §4 table with no crates behind it, and the browser target was a decision with no instrument. Implementation: three crates with one-directional edges (`cli → {core, verify}`, `verify → core`, `core →` nothing — the wiring IS the deliverable at `.1`; behaviour stays with its owning leaf); `scripts/check_wasm_build.sh` registered as the `PORT-WEB` doctrine — preflight refuses when the rustup target is absent (exit 2), the 4-arm self-test re-runs before every judgement, the verdict is a plain `cargo build --workspace --target wasm32-unknown-unknown`. Validation: `make check` green (5 suites, 0 warnings at `-D warnings`); self-test 4 pass / 0 fail; fired RED on a real `std::os::unix` import (rc=1, naming `lib.rs:13`); `make gate` green after registration. Design notes, kept: (1) the self-test caught my own first cut — bin crates want `src/main.rs`, not `src/bin.rs`, and cargo fails builds with rc=101, not 1; a control never run RED is not known to work. (2) Scratch builds pass `--target-dir` inside the temp dir — the measured family defect is self-test state leaking into the real run through environment variables.

Lessons: declined here (both notes are recorded in the PORT-WEB.1 leaf checklist).

## _(2026-09-27)_ — the sanctioned watcher is a ruling, not a false positive (ARTIFACT-CLEANUP.2)

The director ruled CHIPDOC's ChipdocWatcher stays, and the census stopped crying wolf the
honest way: the exemption is a RULING in data (doctrine/sanctioned_processes.tsv), not a
vocabulary in detection — the pattern-free census is untouched, and only director-ruled
standing processes skip it. Design note worth keeping: a detection list and an exemption list
are different shapes of the same text file; the difference is WHO adds a row and WHY (an agent
proposes, the director disposes, the ruling is quoted). Verified both directions: handoff OK
with PID 36462 alive; the row absent -> the same process flags.

Lessons: declined here (the propose-vs-dispose discipline is stated in the registry header).

## _(2026-09-27)_ — no coding without the source of truth, mechanized (MODEL-METHOD.6)

Root cause this leaf closes: the rule was the director's prose and nothing enforced it. The
design turn: the census already said which categories are missing, but 'missing' alone cannot
block coding — the excluded subsystems (C07/C08/...) are missing and must stay legal. The gate
needs the scope to DECLARE what it requires; the registry gained (requires …) and the refusal
keys on required × missing. rv64i-lab-v0 declares its 14 in-scope categories; the six
excluded ones stay legal because they are not required.

Composed, not duplicated: SCOPE-COVERAGE says the facts are OWNED; EXTRACTION says they are
EXTRACTABLE; both must pass before P1-LAB writes code. MODEL-METHOD closes 13/13 — the
method, the census, the acquisitions, and the coding gate all landed in one session.

Validation: gate 7/0; real run '1 unit(s) may code'; RED fired pre-registration; whole
enforcer green (19 doctrines, 227 arms).

Lessons: declined here (the OWN-vs-EXTRACT composition rule is stated in the gate's header).

## _(2026-09-27)_ — the method, in prose, written to be learned from (MODEL-METHOD.5)

Root cause this leaf closes: the method existed only as the history of its exercise — eleven
leaves of it — and a method that lives only in its own history cannot be learned from. The
document is written against what the session actually did, with the rejections kept, and it
names the four judgement calls (publication, class, authority, disagreement classification)
rather than letting them look like mechanics.

The acceptance probe worth keeping: the body of docs/METHOD.md references no project-owned
tool, path, or id outside the worked example — the carryability claim is checked, not
asserted. The mdBook carries the document verbatim, the house pattern for every source doc.

Lessons: declined here (the framing is the document's own closing section).

## _(2026-09-27)_ — the run-real-code set is acquired, and the PDF question is answered (MODEL-METHOD.4)

Root cause this leaf closes: the census (" + bt + ".3" + bt + ") named the run-real-code set as the
reachable acquisition, and nothing pinned it. Four fetches, four digests, one cache, one
answered question.

Design choices, stated — the home problem consumed the design time, and the answer is worth
keeping: every natural home refused these documents for a MEASURED reason. The profile's
sources.sexp composes base_url/file (one origin; this set is four); the materials catalogue's
fetch seam copies from an $ENV-rooted corpus (no URL kind); docs/provenance manifests list
tracked bytes (third-party documents are not redistributed — the same doctrine that keeps
.materials/ gitignored). So the tracked record is the leaf's digest table plus the cache
README, and a materials.py URL kind is the named candidate only if a second web set arrives.
Two pins are branch-pinned (master/main) — the digest is the protection; locator-stable pins
are P1-LAB's refinement.

The PDF question answered YES with extraction evidence (funct7/rs2/rs1/funct3 as clean text
cells; 1.96 MB extract). SRC-02: the v20260120-tagged release asset was not found (three
release pages searched); chipdoc unavailable here.

Validation: every cached copy re-hashed to the recorded digest; content sanity per document;
RECORD-SCHEMA green on the revised C20 census row; whole gate green.

Lessons: declined here (the home-selection reasoning is stated in the leaf, where the next
acquisition meets it).

## _(2026-09-27)_ — the census sweeps the snapshot, and missing changes its meaning (MODEL-METHOD.3)

Root cause this leaf closes: the .2 first pass wrote dispositions from the profile's
exclusions, and four of its reasons asserted material absence nobody had checked. The census
evidenced every covered row against the cached snapshot and corrected the mistake the
evidence revealed: the excluded subsystems' chapters are IN the snapshot — a-st-ext, rvwmo,
v-st-ext, f/d/q-st-ext, counters, zicsr, zifencei. So `missing` means the profile excludes
the subsystem (the facts are not part of this unit's model), not that the material is absent.
That flip matters downstream: .4's acquisition list is now honestly short — the run-real-code
set and the privileged/debug VOLUMES, not chapters the snapshot already carries.

Design choices, stated: `deferred-to-board` is a new disposition value (zero kernel lines)
because device and interconnect categories are P5-BOARD's to own, and the CPU records an
environment assumption in their place — the leaf's own rule. RECORD-SCHEMA rule 12 keeps every
named material resolvable against catalog.sexp, so a covered-by that names a document nobody
acquired is refused like an unpinned citation. The census counts: 10 covered, 4 partial, 6
missing (closers named), 3 deferred-to-board, 1 out-of-scope (C17 — contract-owned).

Validation: the page-level sweep (each covered category's subject found in its pinned page);
RECORD-SCHEMA 33/0 (was 32) + real run green; whole gate green.

Lessons: declined here (the excluded-vs-absent distinction is stated in the catalogue header
and the owning leaf).

## _(2026-09-27)_ — the materials requirement: what each unit owes its model (MODEL-METHOD.2)

Root cause this leaf closes: the materials side recorded documents (who/what/where) but
nothing recorded what information a unit OWES its model — no category-to-material binding, no
unit registry, no layer. The fix walks the .3 path a third time: schema declares, the mapping
owner carries, RECORD-SCHEMA gates.

Design choices, stated: the disposition vocabulary is the point — `missing` means the unit
REQUIRES the category (a reason is owed), `out-of-scope` means it never owed it, and the
acceptance's rule is the mechanical form of that honesty (a board-layer `missing` for a
processor is a lie about what was required). The unit registry keys the layer rule: layer
claims without a registry prove nothing, so the gate refuses those too. The duplicate-id arm
grew a per-family key — category-need records have no `id`; they key on (category, unit),
and the first cut that assumed `id` reported every need as a duplicate of None. The
`dict_to_form` dispatch also had to move its specific keys first: units and
category-needs both carry a `kind` field, which collided with the requirement
branch until `book`/`disposition` dispatched first — a measured,
not hypothetical, ordering constraint.

Validation: RECORD-SCHEMA 32/0 (was 26); 7 record files green; the 24-row first honest pass
(8 covered, 6 missing-with-reason, 4 partial, 6 out-of-scope). The .3 census revises
dispositions against evidence from here.

Lessons: declined here (the ABSENT-vs-NEVER-NEEDED vocabulary is stated in the schema header
and the owning leaf).

## _(2026-09-27)_ — the no-duplicated-fact rule is a registry, and every mirror is governed (MODEL-METHOD.7)

Root cause this leaf closes: the no-duplicated-fact rule lived only in
`decision_canonical-definition-input` prose, while the corpus it governs had grown
derived mirrors — and one of them (28 obligations restating their requirement's statement,
measured) had NO governor at all. The fix is shaped like the routes registry beside which it
lives: `doctrine/fact_ownership.tsv` names one owner per fact kind, each legal mirror, and
the governing doctrine; the FACT-OWNERSHIP gate verifies the registry holds AND is complete
against the corpus's actual restatement pairs — a completeness claim needs a census, so the
four real pairs are enumerated in the gate.

Design choices, stated: the registry's mirror column means "a file that restates the owner's
fact" — direction matters, and getting it uniform (owner owns; mirror derives) took one
measured failure (the encoding pair's family prefix did not match one way; symmetric
directory-prefix matching fixed it). The governor belongs in the family gate, not the
registry: RECORD-SCHEMA rule 9 keys on the obligation's own `requirement_id` (the 8
environment-assumptions keep their own statements — the arm keys on the parameter, not the
direction).

Validation: RECORD-SCHEMA 26/0 (was 23) + real run green on the 28 real mirrors; gate 8/0;
both acceptance shapes fired. Whole enforcer green.

Lessons: declined here (the govern-every-mirror rule is stated in the gate's header and the
owning leaf).

## _(2026-09-27)_ — the extraction contract: one set, four ways (MODEL-METHOD.10)

Root cause this leaf closes: every per-family check proved its own leg, and nothing proved
the legs described the SAME instruction set. Measured pre-code: no requirement↔instruction
link existed, and the ALU family (13 instructions) had no requirement at all — the contract
as stated failed the real corpus on the requirement leg.

The fix is two-handed, and both halves matter. Corpus: `(insns …)` on the schema
(kind-agnostic — a memory-kind requirement names FENCE, an event-kind names ECALL and
EBREAK), two new D/REQ/OB triples whose statements are grounded in the corpus's own
semantics (the §1.1.4 effects, including SLTIU's sign-then-unsigned quirk — the statements
must match the decisions exactly, `RECORD-SCHEMA` rule 4, and the semantic file is the
corpus's own authority for what the spec says). Tool: `check_extraction.py` requires
SCOPE == ENCODING == SEMANTICS == REQUIREMENTS — one set, four ways — plus resets and
checks. Gating: `EXTRACTION` (17th doctrine), because P1-LAB must cite a verdict that
runs.

Measured en route: `RECORD-SCHEMA` caught a wrong obligation id (`OB-D-ALU-REG`
vs `OB-ALU-REG`) mid-curation — a gate earning its keep on the authoring side, not just
the review side. And `R.dump` drops file headers: a load→modify→dump rewrite must
re-prepend the `;;` header or the diff shows comment loss. The curation script now
does, and the diff is minimal (11 insns additions + 2+2+2 new records).

Validation: tool 6/0, gate 3/0; real corpus SUFFICIENT; the acceptance's RED on a copy with
one sem rule removed (`does not cover: add`). REGRESSION: RECORD-SCHEMA 23/0,
PROFILE-CONSISTENCY 39/0, GATE-REPORT re-derived 28/28/36/72, whole gate green.

Lessons: declined here (the integrative-pattern rule is stated in the tool's docstring and
the owning leaf).

## _(2026-09-27)_ — a composition is an ordinary unit, and the tree closes (MODEL-COMPOSE.5)

Root cause this leaf closes: composition produced verdicts (encoding union, record merge,
assumption/guarantee discharge, slots, refinement) but nothing produced a UNIT from them —
`computer -> board -> soc -> {cpu, device}` had one record shape at level one and no shape at
all above it. The fix is deliberately boring: `compose_units.py` merges the parts with
`merge_units(…)` — the same code, no fork — and writes an ordinary unit directory through the
single mapping owners. Boring is the point: the acceptance is that a two-level composition is
checked by the same code as a one-level one, and the way to get that is to not write new check
code at all.

Design choices, stated: part paths resolve against the manifest's own directory (the way
fragment-root resolves against its document); provenance is kept, not rewritten — merged
records keep their origin units' `profile_ids`, the board overwrites only the encoding
document's own identity field; exactly one ISA-carrying part (two is a multiprocessor — the
address-space operator stays refused-until-earned); no new doctrine gate, because the derived
files are ordinary corpus covered by the existing gates wherever they land. The tracked-board
freshness proof (manifest -> derived bytes, the gen_fragments precedent) is the first tracked
board's job, named in the leaf.

Measured en route: the first implementation read only the first `(part …)` child of the
manifest — every multi-part composition silently halved. The self-test's census arm caught it
(2 obligations where 3 were owed). A census that counts is the cheapest oracle there is.

Validation: `--self-test` 9/0; real corpus board through unmodified `merge_records`,
`discharge_assumptions`, and the encoding read path (26/34/3 + 52 instructions). Regression:
whole guard set green.

Lessons: declined here (the materialize-then-stay-ordinary rule is stated in the tool's
docstring and the owning leaf).

## _(2026-09-27)_ — a silent override is refused, and the execution authority gets its gate (MODEL-COMPOSE.6)

Root cause this leaf closes: two measurements, one design. (1) The refinement edge had no
vocabulary — nothing in `schema/semantics.sexp` could declare "this extension changes that
base behaviour", so a silent override was indistinguishable from a composed corpus. (2) The two
tools that judge the semantics corpus — `check_semantics.py` (well-formed, complete, cited)
and `check_citations.py` (52/52 locators resolve) — were invoked by NOTHING in the gate set;
the corpus the engine will execute was healthy only when someone ran them by hand. The third
orphan of the family `MODEL-COMPOSE.4` closed for encodings — the same probe, the same
shape, the same fix: wire the capability into the gate set or watch it rot.

Design choices, stated: the declaration lives on the AUTHORED side (the `.sem.sexp` files),
never in the generated fragments — generated and hand-derived content have different provenance
and must not share a file, the `rv64i.sem.sexp` header's own rule. The compose mode
schema-validates each file first and refuses a violating FILE as a rejection (rc=1), reserving
rc=2 for a broken language. The citation arm NAMED-SKIPs when neither the fetched area nor the
manifest-verified cache exists — a check that cannot judge never reports green.

Validation: tool `--self-test` 8/0 (declared refinement accepted; silent/double/lie/arity/schema
arms each naming their reason); gate `--self-test` 7/0; real run `ok (3 check(s))` with
52/52 citations inside the gate for the first time; the acceptance's RED on a real-shaped
composition. Per-fragment mode byte-stable.

Lessons: declined here (the "orphaned tool" pattern is now demonstrated three times; a knowledge
card is due on a FOURTH instance — that is the threshold, stated so the count is honest).

## _(2026-09-27)_ — slots are data, and the unit's union is decided again (MODEL-COMPOSE.4)

Root cause this leaf closes: two substrate defects found by probe before any code. (1) Since
`MODEL-COMPOSE.2` moved instructions into fragments, NOTHING decided the unit's composed
encoding space — the disjointness checker read compositions its own way, could no longer read a
unit's `encoding.sexp` at all (probe: REFUSED, "yielded no instructions"), and no gate
invoked the tool on the unit's fragments. (2) The checker never schema-validated its input — a
planted `(widget "x")` in a real `compose` passed silently. A slot verdict on a
document nobody validates, over a union nobody decided, would be a claim without legs.

The fix, in order: data first (`(status …)` and `(slot …)` in `schema/encoding.sexp`,
zero kernel lines); then ONE resolver — `riscv_asm.resolve_composition(…)` extracted and
shared by the assembler and the checker (a second hand-written resolver is how the `.2`
regression happened); then the checker validates the document and each resolved fragment against
the schema layer before unioning; then `UNIT-COMPOSITION` (15th doctrine) wires the
verdict into the gate set — a restored capability that no gate invokes is the defect restated.

⭐ Two more latent bugs of the same family surfaced in the resolver while testing:
`children(…, "extensions")[0]` and `children(…, "requires")[0]` index a
first child the 0-or-more grammar does not guarantee — absence is schema-legal; the corpus
always writes the markers, so both IndexErrors were live but unfired. The self-test's fixtures
omit the markers and prove the paths. The `.2` precedent as no-regression proof: the
resolver is refactored, not rewritten — `run_smoke` ok, nothing observable moved.

Lessons: declined here (the "capability without a re-runner" lesson is stated in the gate's
header, where anyone restoring a capability meets it).

## _(2026-09-27)_ — assumption/guarantee discharge is a verdict (MODEL-COMPOSE.3)

## _(2026-09-27)_ — assumption/guarantee discharge is a verdict (MODEL-COMPOSE.3)

Root cause this leaf closes: a conditional composition claim ("the CPU is validated under
explicit environment assumptions") is only as strong as the demonstration that the assumptions
hold — and the demonstration lived only in `docs/CPU_ENVIRONMENT.md` §5 prose. The
design insight, measured before any code: the discharge edge already exists in the corpus as
obligation dependencies — `SOT-FORMAT.5`'s census showed all 8 environment-assumptions
depending on `cpu-guarantee` obligations. The operator's job was to make that edge a
verdict, not to invent it.

The rule: an assumption is discharged when every dependency resolves in the `merge_units(…)`
union to an obligation whose direction is a guarantee — keying on "not environment-assumption"
so a future device-guarantee value is accepted by construction (the vocabulary extension is
deliberately not this leaf; it is a `(values …)` data change the day a real device
unit exists). Refusals: the missing guarantee fires in the union's closure (`DANGLING DEP`)
— where the acceptance's RED lands is recorded honestly, not re-implemented — while a chain
(demand → demand, `UNDISCHARGED CHAIN`) and a zero-dependency assumption (`UNDISCHARGEABLE`)
are the discharge-specific refusals. Complement stated in the tool: an unclaimed guarantee is
not an error.

Validation: `discharge_assumptions.py --self-test` 6/0; real corpus 8/8 with every edge
printed; cross-unit discharge (a unit carrying only `OB-ENTRY-STATE`); guarantee removed →
rejected naming it, from both the assumption and the requirement side. Regression: merge 18/0,
SOURCE-FORMAT 7/0, sexp 18/0, kernel 50/0, RECORD-SCHEMA 23/0, semantics 52/52, citations
52/52, materials 20/0, smoke ok, readers 28/28; whole gate green.

Lessons: declined here (the "new direction values accepted by construction" rule is stated in
the tool's docstring and the owning leaf, where anyone extending the vocabulary meets it).

## _(2026-09-27)_ — the split cannot return: SOURCE-FORMAT registers, SOT-FORMAT closes (SOT-FORMAT.6)

## _(2026-09-27)_ — the split cannot return: SOURCE-FORMAT registers, SOT-FORMAT closes (SOT-FORMAT.6)

Root cause this leaf closes: retirement recorded only in prose decays. Every source of truth was
converted (`.1`–`.5`), but no check enumerated the source-of-truth families, so one
`profile.toml` copied from an old branch would have re-entered silently and the merge rule `.5`
defines would be meaningless again. The gate (`scripts/check_source_format.sh`) owns exactly one
question — nothing outside the format, nothing unreadable inside it: the FORMAT arm refuses a
tracked `.toml`/`.json`/`.jsonl`/`.yaml` under `definitions/`, `schema/`, `profiles/`,
`materials/` by name; the PARSES arm requires every `.sexp` there to parse with `sexp.py`;
schema coverage is deliberately other gates' lane (two gates reporting one breach is noise).
Fired RED before registration against a scratch copy of the real corpus with one planted
`profile.toml`. The corpus boundary arms matter as much as the refusal arms: `profiles/*.md`
(dossier prose) and `*.s` (guest programs) must NOT be refused — the gate refuses the split's
shapes, never prose or programs.

⭐ Reading for this leaf surfaced two stale lines, both corrected in passing: the replacement
decision's own *How to apply* said "write the EBNF in `pgen`", contradicting its body — the
director corrected the identification on `2026-09-14` (*"Not it is not PGEN. It is LinkedSpec"*).
The lesson: a decision record's summary lines drift before its body does; reading the whole
record, not the header, is what catches it.

Validation: `--self-test` 7/0; real run `ok (28 source-of-truth file(s))`; both mirrors updated
in the registering commit; `REGISTRY-MIRROR` and `DERIVED-COUNTS` (14 doctrines, 184 arms) green;
full enforcer green. `SOT-FORMAT` closes 10/10.

Lessons: declined here (the corpus-boundary lesson is demonstrated by the gate's own census arms
and stated in its header); the pgen-staleness observation is general but thin — one instance,
recorded in the corrected record and this note; a second instance would earn a knowledge card.

## _(2026-09-27)_ — the record merge is definable, and it decides (SOT-FORMAT.5)

Root cause this leaf closes: composition is a merge, and with everything in one format the
records' union finally has a rule. Design (recorded in the leaf, before code): a unit is a
directory carrying `requirements.sexp` / `contract-obligations.sexp` / `sources.sexp` by name,
read through the single mapping owners (`records_sexp.py`, `dossier_sexp.py`) — the merge
parses nothing itself. Merge key is `id`; on collision every field must be equal except
`profile_ids`, which is membership and unions; sources collide on full pins (same id + different
`sha256` = two texts of one specification). After the union, every reference must resolve in
it — requirements' `dependencies`/`obligation_ids`/`source_refs`, obligations' likewise.

Two measured defects, both found by probe before any code was written:

1. **RECORD-SCHEMA never refused duplicate record ids.** The gate built `by_id` as a dict
   comprehension — last wins, silent. A scratch catalogue with two `REQ-D-A` records differing
   in `risk` returned `rc=0`. Fixed as rule 8 (UNIQUE-ID) with a fired RED arm; self-test
   22 → 23.
2. **Obligation `dependencies` were checked against nothing**, and the first closure run on the
   real profile reported `OB-ENV-RESET` → `OB-ENTRY-STATE` as dangling — because the check
   looked only in requirements. Measured truth: every cpu-guarantee depends on its requirement
   (`OB-XLEN` → `REQ-D-XLEN`), every environment-assumption on the guarantees it discharges
   (`OB-ENV-RESET` → `OB-ENTRY-STATE`). An obligation's dependency now resolves against
   requirements ∪ obligations; a requirement's against requirements — inferred from all 42
   real records, zero dangling.

Validation: `merge_records.py --self-test` 18/0 (10 GREEN unions, 8 RED contradictions, each
naming its fact); the real profile self-composes (26 req + 34 ob + 3 src); an edited copy is
refused naming field and both values; a scratch extension unit composes against the base and is
refused by name without it. Regression: sexp 18/0, kernel 50/0, RECORD-SCHEMA 23/0 + real run
green, semantics 52/52, citations 52/52, materials 20/0, smoke ok, readers 28/28, G0 diff
empty, `make check` green.

Lessons: promoted — `docs/knowledge/a-duplicate-id-is-a-contradiction-not-a-shadowing.md`
(the id-keyed dict that collapses duplicates is the same failure in any gate). The
mixed-namespace dependency fact is declined here: measured, owned and enforced by
`merge_records.py`'s closure, where anyone extending the record families meets it.

## _(2026-09-27)_ — the dossier moves behind the schema layer (SOT-FORMAT.4)

- All nine dossier documents converted — `profile.sexp` (26 decisions), `state.sexp`,
  `sources.sexp`, `references.sexp`, the matched override and the four guest expectations —
  each verified field-for-field against its retired TOML/JSON with the comment census exact
  (158 comment lines survive as first-class `(comment …)` forms). Kernel: one reserved comment
  head, 7 new arms (50/0). `PROFILE-CONSISTENCY`: 39 arms re-fired on the converted form.
  Consumers changed at the seam via the new mapping owner `scripts/dossier_sexp.py`; the Sail
  JSON derives from the tracked `.sexp` byte-identically; `run_smoke`/`compare_platforms`
  unmoved.
- ⭐ **A mutation arm and the defect it simulates must fail for the same reason.** Three
  fixture-shape failures while re-firing the 39 arms — a field line carrying its form's close
  paren (a `grep -v` arm unbalanced the fixture), BSD sed refusing multiline replacements
  (CI runs GNU sed; `gsed` on the author's machine is not a dependency the gate may take), and
  `${var/pat/repl}` terminating at an inner quote (the replacement silently never happened).
  Every fix was the same shape: one field per line, closes on their own lines, whole-line
  mutations only. Promoted to
  [`docs/knowledge/portable-shell-fixtures-keep-mutations-whole-line.md`](docs/knowledge/portable-shell-fixtures-keep-mutations-whole-line.md).

## _(2026-09-27)_ — the fired ceiling gets its sharder, and the freeze gets its proof (DOC-SHARDING.1)

- `CHANGELOG.md` crossed its 64 KiB ceiling with 9 bytes of headroom; this slice built the
  remedy the registry's owner column had always named: `scripts/shard_history.py` (moves the
  oldest whole `## ` entries byte-verbatim into `docs/changelog/shard-NNNN.md`, rewrites the
  head under target, regenerates `SHARDS.sha256`), the adoption manifest covering the two
  existing date-named shards, and the `SHARD-FREEZE` doctrine check. One entry (`P0-0031`,
  3.4 KiB) moved; the head went 65,527 → 62,086 bytes — leaving room for this entry itself.
- ⭐ **The completeness proof belongs to the shard event; the freeze proof belongs to the
  manifest.** The tool can assert "head-before == head-after + shard, order and bytes exact"
  because it holds both sides at the event; no later check can, the past head is gone. What the
  durable check can prove is everything after: every shard hashes to its row (an edit fails with
  both digests named), the manifest only grows against `git show HEAD:…`, and no `## ` heading
  appears twice across head and shards. Splitting the two halves is what makes each half
  checkable.
- Fired RED on the real tree before registration — the manifest did not exist yet, so the check
  reported both existing shards `UNMANIFESTED` (rc 1), the exact adoption gap. 12 self-test
  arms; the full gate re-run after registration moved `LIVE_STATUS.md`'s derived counts
  (12 → 13 doctrines, 157 → 169 arms) — re-derived by `check_derived_counts.sh --list`, never
  incremented by hand.

## _(2026-09-27)_ — the records move behind the schema layer, and the schema layer grows facets (SOT-FORMAT.3)

- `profiles/rv64i-lab-v0/{requirements,contract-obligations}.jsonl` are retired;
  `{requirements,contract-obligations}.sexp` (26 + 34 records) validate under
  `schema/{requirements,contract-obligations}.sexp`, and the round-trip is proven byte-identical,
  not reviewed. `RECORD-SCHEMA` re-fires its 15 scenarios on the converted form plus the schema
  layer's own refusals (22 arms); `gate_report.py` reads through `records_sexp.py` and the G0
  report diff is input names only.
- ⭐ **A schema layer must not be weaker than the contract it replaces.** The JSON schemas
  carried `pattern`/`minItems`/`uniqueItems`/`minLength`; a straight conversion would have
  evaporated them, so the `(field …)` kind grew four optional facets instead — the `.2`
  boundary one level down (a new KIND changes the kernel; facets on the existing kind are the
  language). And `parameters` was worse than weak: the JSON schema's own
  `additionalProperties` banned the arrays three obligations write, and the validator never
  descended into it — a lie the green gate could not see. Typed wrappers now refuse a float, a
  mixed list or a nested value by name.
- Two implementation shapes worth keeping: form heads must be `Symbol`, never plain strings —
  a plain-string head renders quoted and reads back as data (the schema layer caught it:
  "expected a form headed by a symbol"); and catalogue discovery must exclude the schema
  directory, because the schemas deliberately share their basenames with the catalogues.
- Measured en route and fixed in passing: `LIVE_STATUS.md` carried the contract at 33
  obligations / 66 checks; the files have said 34 / 68 since `P0-PROFILE.10` — a count in a
  live surface that no gate enumerates. Re-derived, and the row now matches the files.

## _(2026-09-27)_ — the corpus's grammar is not the designed grammar (SOT-FORMAT.2)

- The schema language gained its fourth declaration kind — `(operator …)` for positional
  mini-languages — and `encoding`/`fragment`/`semantics` got schema files. `check_semantics.py`'s
  32-form table is now data in `schema/semantics.sexp`; the 52-of-52 verdict is byte-identical
  and the four MODEL-METHOD.9 controls still fire RED. A 33rd form is a schema edit, demonstrated
  and reverted. Recorded as `SOT-FORMAT.2`, commit `SEMULITH-SF-0057`.
- ⭐ **Designing a grammar from the files already read is sampling, and sampling found the same
  trap twice.** `.1` refuted its own tidy pair grammar by reading the corpus first; `.2` then
  built a record-only language that fit every file consulted and still could not state
  `(fixed (31 25 0x0) …)`, `(operands rd rs1 rs2)`, or the semantics expressions. Promoted as
  [`docs/knowledge/the-corpus-writes-shapes-my-grammar-cannot-state.md`](docs/knowledge/the-corpus-writes-shapes-my-grammar-cannot-state.md).
- The schema layer validates structure and arity; operand scoping stayed in `check_semantics.py`
  because it is a cross-file fact (the encoding provides the operands). Layering rule: the schema
  layer never reads a second file — the moment a check needs two sources of truth, it belongs to
  a consumer, not the schema.

## _(2026-09-27)_ — the star gets a start condition (ROADMAP v0.3)

- ⭐ **A plan that cannot say when its first milestone starts is not yet a plan.** The vacuum
  was measured, not argued: `27` commits since any milestone tree was touched, that touch being
  P0 closure. The fix is not "work faster" — it is to make the sequencing *derivable*: P1's
  start condition (`SOT-FORMAT.2` + `MODEL-METHOD.10`) is now named in the plan itself, and
  every cross-cutting lane must name its consuming milestone (`decision_lane-consumption`).
- ⭐ **Contradictions between contract documents are defects with owners, not interpretations to
  code around.** ARCHITECTURE.md §1.1 (semantics are data) and §2 (canonical Rust handlers)
  disagreed; P1 would have met that ambiguity on day one and picked silently. Recorded and
  resolved in `decision_interpreter-before-compiler`: the data executes; compiled handlers are
  derived artifacts behind an equivalence regression.
- Counts in live documents drift by spelling: `LIVE_STATUS.md` carried `MODEL-METHOD 3/10`
  (stale: 6 of 13) because the gated pattern only matches "of/leaves" phrasing — a count in a
  non-gated spelling is a memory of a measurement. (Fix proposal D3 announced to the director;
  the check extension is pending approval.)

## _(2026-09-14)_ — explicit widths, and never regenerate over hand-derived work

- 52 of 52 RV64I instructions now have machine-checkable semantics, each citing the locator it came
  from. Before: 26 rules, all English prose, none executable.
- ⭐ **Widths are always explicit.** `(sext 64 (trunc 32 …))` says what it means; an implicit width
  is exactly where two models silently disagree, and `D-WSUFFIX` is one line once it is spelled.
- ⛔ **Generated and authored content must not share a file.** `rv64i.sexp` is regenerated whenever
  its upstream table moves; hand-derived semantics in the same file would be destroyed by a
  routine regeneration. Different provenance, different file — a rule worth carrying to any
  project that generates part of its source of truth.
- The language is 32 forms, each added because an instruction needed it, and the checker refuses
  the rest. A notation that quietly accepts an unknown operator produces a definition whose
  meaning nobody can state — worse than none, because it looks like one.
- ⚠️ `52 of 52` = well-formed, complete, cited. NOT correct. That distinction has to survive into
  the book, because the number invites the stronger reading.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a refactor of the source of truth must not move the evidence

- The unit carried 52 instructions inside itself; a base ISA is shared by every profile that
  composes it. Split into `definitions/riscv/{rv64i,m}.sexp`, and the unit now NAMES what it
  composes and owns nothing. Census: instructions in the unit 52 → 0; in `definitions/` 0 → 65.
- ⭐ **The acceptance test was that nothing observable moved**: all four guest ELF digests are
  byte-identical after the split, across two models. A source-of-truth refactor that perturbs the
  evidence has changed the model, whatever the author intended.
- A fragment DECLARES its dependencies; composing the M extension without its base is refused. A
  fragment with a hidden dependency composes by luck, not by construction.
- `definitions/` was registered in the routes registry in the same commit that created it. A new
  tracked family nothing governs is how pressure escapes — measured once already in this project.
- 🔎 Three references to the old generator name survive in CHANGELOG and a completed checklist.
  Left alone: historical records are true as written, and `append_history` exists to stop exactly
  that tidying.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — breadth by composing proven parts, not by gating them less

- ⛔ **I proposed the wrong lever and it was rejected.** Facing "model as much as possible" against
  "signoff-grade", I suggested tiering models into `exploratory` (ungated) and `accepted` (gated).
  That buys breadth by creating a second class of model nobody can trust, and the classes would
  blur the first time one cited the other. The right lever is **composition**: assemble proven
  small models. Breadth by reuse of evidence, never by absence of it.
- Grounded rather than invented: both pinned references already compose from fragments —
  riscv-opcodes 111 extension files, sail-riscv 34 extension dirs / 59 encoding files — and this
  project already had the other half (an empty `extensions = []` seam, 8 environment-assumptions).
- ⭐ **Encoding union is DECIDABLE, so composition is a verdict.** Two instructions collide exactly
  when `(a.value ^ b.value) & a.mask & b.mask == 0`, searched exhaustively. Proven: owned RV64I +
  an unseen `M` fragment = 65 instructions, no collision. Fired RED on a realistic mistake —
  composing a fragment already contained — giving 37 named collisions and a rejection.
- ⚠️ Semantics are the hard axis and are NOT decidable: an extension can change a base
  instruction's meaning. A fragment must *declare* that it refines base behaviour; a silent
  override is a defect, not a composition.
- 🔎 LIVE_STATUS.md went **over its ceiling** because I had been writing narrative into a status
  table whose owner column literally says "rows are states, not prose". Trimmed to states; the
  gate was right and the fix was the one the registry prescribes.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — owning a source means building without it

- ⛔ The repository did not own its model's encodings: the assembler read `target/refs/riscv-opcodes`,
  untracked and network-acquired, so a fresh clone could not build a model. The project's own rule
  was being broken by its own tooling.
- ⭐ **The test that settles ownership is not that a file exists — it is that the build works with
  the source moved aside.** `mv target/refs/riscv-opcodes /tmp/ … && run_smoke.py` → ok: four
  guests assembled, run on two references and reproduced, with the encodings' origin absent.
- Ownership without re-derivation is a copy, so the agreement is gated and was fired RED on a
  one-bit `funct3` edit.
- ⛔ The new S-expression reader was caught by its own first real input: it stripped `;` comments
  line by line before tokenizing, so a `;` INSIDE a string truncated it and a string could not span
  lines. Generating our own encoding file hit that within minutes. Whether a `;` starts a comment
  depends on whether a string is open — that question cannot be answered by a prior pass.
- The S-expression trigger fired and was answered on merit: trees get S-expressions, records keep
  JSON/TOML and their working gates. "Single source of truth" = one owner per fact, not one file.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a category the layer does not own is not "missing"

- Devices are **board / SoC** material, not CPU material. The processor layer ends at the
  CPU/environment boundary: the CPU states assumptions, a board later states guarantees
  (`docs/CPU_ENVIRONMENT.md` §5, and `INFORMATION_CATALOG.md`'s own note that C19–C21 are not all
  properties of the CPU).
- ⭐ The consequence lands on the materials census, and it would have been a real defect: marking
  `C19 Platform, devices and interconnect` as `missing` for a CPU model manufactures an acquisition
  task for material the model must never contain, and reports a **correct scope as a deficiency**.
  The disposition vocabulary now carries a LAYER, and `deferred-to-board` is distinct from both
  `missing` and `not-applicable`. Caught before the schema was written, which is the only cheap
  moment to catch it.
- ⚠️ It also corrected my own framing of "runs real code": the console and the program-exit
  convention are BOARD concerns. What the processor layer owes real code is the psABI, the ELF
  contract, entry/startup state and the compiler-runtime intrinsics — and nothing else.
- `DIFF-PLATFORM-SPIKE` is a LAYER difference, not a configuration one: Spike ships a CPU and a
  small board together. The record now measures how much board each reference drags in.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — answer a narrow instrument with a wider one, and state the wider one's scope

- The sweep found **one further instance**, worse than the founding one: Spike's
  `matched_isa_string` was the command-line INPUT sitting in an observation's slot. Spike has no
  `--print-isa`, so nobody had confirmed it configured what it was told. Now read back from
  `--dump-dts`, with a control (`--isa=rv64im` → `rv64im`) proving it is an observation, not an echo.
- ⭐ The replacement is a principle with a tool behind it: claim a match against the model's own
  self-description at the **widest granularity it offers**. Both models emit a device tree; the
  comparison shows 4 of 4 platform fields disagreeing and four devices only Spike advertises.
- ⚠️ **The wide instrument has its own scope and must say so**, or it becomes the next narrow one.
  A device tree is what a platform ADVERTISES — not semantics, not memory attributes — and Sail's
  still lists a `timebase-frequency` and an `htif` node with no device behind them.
- The durable answer to "are there others?" is not "no". It is that a new one **cannot be added**
  without declaring what it does not establish — rule 5b, fired RED on the real dossier.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — an instrument that answers a narrower question than the one you asked

- ⛔ **The profile was matched on its instruction set and not its platform, for four leaves.** The
  override set `extensions` and left the reference's default platform underneath: a core-local
  interruptor, an interrupt generator, two I/O regions. A guest read CLINT `mtime` with a PLAIN
  LOAD and watched it advance (2 → 3). Excluding `Zicsr` removes the CSR *instructions*, not the
  device — and a device exposes time as ordinary MMIO.
- ⭐ **This is a distinct failure mode from `zero-hits-absence-or-blindness`.** That one was an
  instrument that could not see. This one is an instrument that **answered a different question**:
  `--print-isa-string` returned `rv64i_zvl32b`, which is *true*, and describes an instruction set
  rather than a machine. A confident, correct, narrower answer is harder to doubt than a zero.
- Four committed claims were refuted by one probe. All corrected at source; the repair is held by
  a tracked negative fixture that must fault.
- Spike's platform is irreducible with the available controls, so it is ENUMERATED, and the
  consequence is stated exactly rather than left implicit: the original guests agree because they
  touch neither device region — a stated precondition, not luck.
- 🔎 The general question this raises, and it is not yet answered: **which other "matched"
  claims in this repository rest on an instrument that answers a narrower question?** The pattern
  to look for is a single confident scalar standing in for a configuration. Owner: `MODEL-BOOKS.1`,
  whose materials bill must state for each reference what was matched and by what evidence.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a gate report that cannot tell a mention from an implementation

- Gate `G0` is run and reads **`incomplete`**: 66 declared checks, 0 implemented. The report is
  GENERATED from tracked inputs and gated for staleness, so `passed` is unreachable — the
  generator has no code path to it, and hand-editing the word fails the commit.
- ⛔ **The generator was wrong twice, both times inflating the verdict.** "How many checks are
  implemented?" first counted `EVIDENCE_POLICY.md` (grepping the id PATTERN across the tree — a
  document describing the naming convention), then counted `check_requirements.sh` (which tests
  the `-POS`/`-NEG` suffix while enforcing that ids exist — a gate about checks is not a check).
  Both said `1`; the truth is `0`. The measure is now exact: take the CONCRETE declared ids and
  ask which any tracked executable names. The failure direction is the lesson — an approximate
  measure of "is this done" drifts toward done.
- ⛔ The evidence policy's first draft stated class populations and got two wrong, by reading the
  profile's authority distribution instead of the requirements' category distribution — the exact
  non-mechanical mapping documented two leaves earlier, walked into by the person documenting it.
  Hand-typed populations were removed; the generated report derives them.
- ⭐ `incomplete` is the DELIVERABLE. A milestone whose job was to establish what evidence would
  be required cannot also have produced it. Saying so in the verdict, rather than in a footnote,
  is what stops the next milestone inheriting a claim nobody made.
- Promotion is explicitly declined in the owning leaf, with the reason.

