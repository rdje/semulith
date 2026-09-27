# DEV_NOTES.md

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

Every dated entry here must reach the retrievable layer: a card under
[`docs/knowledge/`](docs/knowledge/INDEX.md), or a decision record, or an explicit decline in
the owning task leaf. That is the `LESSON-PROMOTION` doctrine, and the reason for it is that a
lesson nobody can retrieve by question is a lesson nobody has.

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

## _(2026-09-14)_ — derive the layout, and report the control that passed

- The B/J immediate scramble is **derived** from a pinned descriptor table, not typed. The
  derivation validates itself: the bits a descriptor accounts for must total its field width
  (7, 5, 20, 20) or the table is refused. A layout the assembler cannot reconcile is one it will
  not use — which is the same shape as the validator's refusal rule from the previous leaf.
- ⭐ **Negative observations earn their place.** `never_written` catches a jump that failed to
  skip, which a checker watching only the registers it expects to change cannot see. Fired RED by
  breaking the PROGRAM (jump to the next instruction), not the expectation.
- ⛔ **A control that passed is still a result.** `jalr +13` vs `+12` land identically *because*
  the low bit is cleared, so the landing address does not discriminate D-JALR-LSB. Both references
  clear the bit, so the failing branch was never observed. Recorded as a `limit` in the
  expectations file rather than letting a green result imply a discrimination it did not make.
  Owner of a real control: P1-LAB's mutation suite, which can mutate OUR model.
- Assembled instructions are not executed steps. Equal for straight-line code; wrong the moment a
  loop exists. The run bound now comes from the expectations file.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a "none" that is merely absent is one nobody considered

- The environment contract's two most useful obligations are the ones whose answer is **none**:
  no virtual time is architecturally readable, and no asynchronous event is deliverable *by
  construction*. Both record WHY. Absent from the contract, they would be indistinguishable from
  boundaries nobody thought about; written down, a later profile has to reopen them deliberately.
  Same for the six of ten §2 boundary items that are out of scope, each with its reason.
- ⭐ *Laboratory policy cannot override an architectural requirement* is now mechanical: an
  obligation whose requirement is architecturally `defined` must carry `authority: architecture`.
  Mislabelling an ISA rule as a harness choice is how a defect becomes an unfalsifiable "profile
  difference" and stops being looked at.
- The new rules fired first on the SHIPPED examples, not on our profile: both example requirements
  name obligations that do not exist. They are `frozen-in-place` delivery artifacts, so they are
  not edited to satisfy a rule written later — routed to `P1-LAB`'s graph checker, with `--audit`
  keeping the finding a command rather than a paragraph.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a partial validator must refuse, not skip

- No JSON Schema library exists on this host and installing one would put a dependency store off
  the repository volume, so the validator is 180 tracked lines covering exactly the 17 keywords a
  census of `schemas/*.json` found. ⛔ **The soundness property is the REFUSAL.** A partial
  validator that silently ignores an unimplemented keyword reports `valid` for a document it never
  fully checked — so this one raises `UnsupportedSchema`, and a schema gaining a keyword breaks
  the gate loudly instead of widening what passes.
- ⭐ `source_semantics.category` is **not** a function of the profile's `authority`. `laboratory`
  covers both "the spec says UNSPECIFIED and we chose" and "the spec delegates to the EEI and we
  chose"; collapsing them records a laboratory policy as an architectural rule.
- The sharpest gate rule this leaf adds: `research_status: resolved` may not coexist with an
  `OPEN:` note. Both halves are true separately, which is what makes the pair convenient.
- ⛔ Two defects in the new gate were found by its own arms, not by review. It excluded `target/`
  by ABSOLUTE path — and its own fixtures live under `target/doctrine-selftest/`, so all ten arms
  failed with "no .jsonl record file found". And the cross-checks re-parsed a file that had
  already failed to parse, crashing the gate rather than failing it: a traceback is not a verdict.
- Promotion is explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — a running total is a memory of a measurement, not a measurement

- ⛔ Two derived counts were committed WRONG in a single session, both as running totals:
  `24 destinations governed` against a 25-row registry, and `107 self-test arms` against 112. The
  method was identical each time — take the written number, add your delta, write the sum back —
  and nothing recomputed either. Gated by `DERIVED-COUNTS`, which re-derives each from the
  population it summarises and prints the enumerator alongside the value.
- ⭐ The new gate caught its own registration: adding it made the project hold 9 doctrines where
  the page said 8, and the commit was blocked until the number was re-derived rather than bumped.
- ⛔ Its first cut was wrong in the *dangerous* direction. `sed -nE "s/.*([0-9]+) widgets.*/\1/p"`
  is greedy: on `12 widgets` the leading `.*` eats the `1` and the capture is `2`. A stale count
  could have matched a wrong extraction and read as correct. Found by a GREEN arm going red.
  Extraction is now off the front of a `grep -o` match, and a pattern not beginning with its
  number group is refused.
- The `TASK-ACCEPTANCE` recipient-tree boundary is **documented, not relaxed**. Requiring only one
  staged leaf to pass would reopen the co-staged-leaf hole that box-scoping exists to close, so a
  routed annotation lands as its own doc-only commit instead. The lesson's promotion is
  explicitly declined in the owning leaf, with the reason.

## _(2026-09-14)_ — 184 of 199 files are the same file, and an instrument that answered blind

- ⛔ **The two reference models run the SAME floating-point source.** Both vendor Berkeley
  SoftFloat; 199 `.c` files exist in both copies and **184 are byte-identical** once the release
  comment is normalized (sail 3e, spike 3d; `f64_add.c` differs by one line). A Sail-vs-Spike FP
  comparison executes one implementation twice. No current evidence is affected — this profile
  has no floating point — so it is routed to `P4-SYSTEM.7` with its measurement. Recorded:
  [`reference_softfloat-shared-ancestry`](docs/decisions/reference_softfloat-shared-ancestry.md).
- ⛔ **`strings | grep -c softfloat` returned 0 for both binaries and that was BLINDNESS, not
  absence.** `nm -a` showed why: spike carries 649,743 symbols, the Sail release binary 400. A
  stripped binary cannot answer the question. The `0` was one step away from being written down
  as a finding; the source was cloned instead, at the exact commit the binary's `--build-info`
  reports. Pick the instrument that can see, then read it.
- ⭐ Independence cuts in unexpected directions. Encoding is **not** shared — spike generates
  `encoding.h` from `riscv-opcodes` while the Sail model hand-writes 59 `encdec` files and never
  mentions it — so *our* assembler shares an ancestor with spike and not with sail, which makes
  sail decoding our bytes an independent confirmation and spike doing so not one.
- `docs/tasks/P0-PROFILE.md` hit the per-part **ceiling** (73,317 B > 65,536) and the completed-leaf
  evidence was split to `docs/tasks/archive/`, unedited. The ceiling was obeyed, not raised, which
  is what the registry's own header prescribes. Checked that the split did not move pressure
  somewhere ungoverned: `git ls-files -- docs/tasks` is recursive, so the archive still counts
  toward the family aggregate (240,293 B against a 393,216 ceiling).
- 🔎 **A new mirror-drift instance, outside what `MIRROR-DRIFT` gated.** `LIVE_STATUS.md` claimed
  "24 destinations governed" while `doctrine/readme_routes.tsv` holds 25 rows and the gate prints
  25 — stale since `SEMULITH-P0-0013` added the `profiles/` row. Corrected here; the *class*
  (a live document restating a count that a registry owns) is not yet mechanized, and `TREE-CLAIMS`
  only covers task-tree facts. Owner: `MIRROR-DRIFT.4`, opened next.
- 🔎 `TASK-ACCEPTANCE` requires every staged `docs/tasks/*.md` to carry a ticked checklist. It
  cannot tell the leaf that OWNS a change from a tree that RECEIVES a routed finding, so
  annotating `P4-SYSTEM.7` had to be split into its own commit — P4 has not started and ticking
  its template would be a lie. Splitting is the right answer; the gate not distinguishing the two
  roles is the defect. Owner: `MIRROR-DRIFT.4` alongside the registry-count class.
- Promoted: [`docs/knowledge/zero-hits-absence-or-blindness.md`](docs/knowledge/zero-hits-absence-or-blindness.md).

## _(2026-09-14)_ — the pinned spec has no encodings, and a shorter trace is not agreement

- ⛔ **The specification we pinned does not contain instruction encodings.** Census over all six
  artifacts: `grep -cE '[01]{7}'` -> 0 every time; the format diagrams are images (31 in the
  RV32I chapter). The SEMANTICS are all present in prose, which is the half expected values need,
  so encodings were pinned separately from `riscv-opcodes` and recorded as a *different*
  provenance. That source is upstream of both models, so encoding agreement is not independent
  evidence — only semantic agreement is, and that is what the experiment tests.
- ⭐ Unplanned corroboration: the encoding table holds exactly 52 instructions for this extension
  set, and `P0-PROFILE.1` enumerated exactly 52 by hand from the prose without it. Symmetric
  difference: none. Two independent routes to the same closed set.
- ⛔ **The comparator reported a false pass and running it is what found that.** Walking only the
  overlapping prefix, it printed `AGREE over 2 aligned step(s)` for a run where one model trapped
  and the other stopped. The prefixes agreed; the observation did not. Promoted:
  [`docs/knowledge/a-shorter-trace-is-not-agreement.md`](docs/knowledge/a-shorter-trace-is-not-agreement.md).
- ⭐ **Two models agreeing means nothing until the agreement is shown to be doing work.** Flipping
  one configuration key — the misaligned policy — with the same binary produced a real first
  divergence. That control is why "matched profile" is now a measurement. The project gate now
  refuses an experiment record that claims agreement without naming such a control.
- 🔎 `docs/tasks/` crossed its advisory health target (214,002 B against 196,608). Not a ceiling
  (393,216 aggregate, 65,536 per part) and nothing is breached, but `P0-PROFILE.md` is at 49,521 B
  — 76% of the per-part ceiling — because completed-leaf evidence accumulates in-tree by design.
  The mechanism intended for this is archive compaction, and no tree has needed it yet.

## _(2026-09-14)_ — availability is not identity, and a budget can be wrong in your favour

- ⛔ **The package manager had a formula called `sail`. It deploys WordPress sites to
  DigitalOcean.** An exact name collision with the Sail ISA specification language: the lookup
  succeeded, the version was current, the licence was real, and the referent was wrong. Had the
  check been `brew info sail >/dev/null && echo available`, the dossier would carry a sentence
  that is false, sourced and reproducible. Identity needs a field only the real thing can
  produce — here `--build-info`, which prints an upstream release, a git sha and the compiler.
  Promoted: [`docs/knowledge/availability-is-not-identity.md`](docs/knowledge/availability-is-not-identity.md).
- The roadmap priced reference acquisition as the first activity whose cost was *not obviously
  bounded*, assuming an OCaml/opam build of Sail. Release 0.14 ships a native binary for this
  host's architecture, so Sail was the **cheapest** candidate, not the dearest. Three models
  obtained in one leaf. The estimate was wrong; the reasoning behind it ("acquisition is work
  with observable outcomes") was right and is untouched.
- ⛔ **The Sail model will not tell you what configuration it ran with.**
  `--print-default-config` ignores `--config-override` — byte-identical dumps. `EVIDENCE_AND_GATES`
  §5 wants the *effective* configuration, so it is recorded as (default) + (tracked override)
  with the merge explicitly labelled **ours**. The model's one self-description is
  `--print-isa-string`, which is why `rv64i_zvl32b` is pinned and re-derived.
- Having three binaries is not having three opinions. The gate now refuses a candidate whose
  `lineage` field is missing, because an unasked independence question reads exactly like an
  answered one.

## _(2026-09-14)_ — a self-test reports the arms it ran, not the arms you wrote

- `docs/TASK_TREE.md` and the tree it indexes disagreed about which leaf was next: the index
  said `P0-PROFILE.2`, the tree said `.5`, and `.2` was `done`. `COMMIT.md` updates that index
  "only if the frontier changes" — a CONDITIONAL manual step, which is the shape that rots. One
  row of fourteen had drifted, and it was the only `active` tree: the single row the documented
  resume path (`MEMORY.md` → index → frontier) actually reads. A 1-in-14 drift rate is not the
  number that matters; a 1-in-1 rate on the followed row is. Gated by `FRONTIER-SYNC`.
- ⛔ **The new gate's own self-test printed `4 pass / 0 fail` while running four of fourteen
  arms.** Ten `arm` calls sat on the same physical line as the fixture call before them with no
  `;`, so bash passed `arm` and its three arguments as extra positional parameters to a function
  reading only `$1` and `$2` — discarded in silence, no error of any kind. Adding the separator
  gave `13 pass / 1 fail`, and that one failure was a real defect: two opposite drift directions
  shared a single message. Caught by counting the arms written against the arms reported, not by
  reading the code. Promoted:
  [`docs/knowledge/self-test-arms-that-never-ran.md`](docs/knowledge/self-test-arms-that-never-ran.md).
- Two blank lines inside `DOCTRINE_ENFORCEMENT.md`'s project-doctrine table split it into three
  GFM fragments, so two registered doctrines rendered as literal `| … |` text instead of rows.
  Right in the file, wrong on the page — one column over from what `TABLE-ARITY-RATCHET`
  catches, and no gate sees a blank line.

- The same mechanism, one document over: `docs/book/src/working/doctrines.md` listed 3 project
  doctrines while 5 were registered. A mirror that falls behind never **invents** a guarantee —
  it **withholds** one, on the surface a reviewer reads instead of the code. Gated by
  `REGISTRY-MIRROR`, which also caught the opposite direction unprompted (`PHANTOM`: a row added
  one step before its registration).
- The durable fix for the swallowed arms is a strict-arity guard on every self-test fixture
  helper, fired RED by deleting one `;`. A helper that ignores surplus arguments is what made the
  swallow silent; refusing them is what makes it loud.

- The third mirror had **not** drifted, and the leaf says so instead of manufacturing a defect.
  For a prevention leaf the falsification is the load-bearing box: four controls, each breaking a
  real claim in `MEMORY.md`/`LIVE_STATUS.md` and restored with `git checkout --`.
- A gate's scope can be data someone already wrote down. `TREE-CLAIMS` reads the `hot_live` rows
  of `doctrine/readme_routes.tsv` rather than carrying a file list — which also gets the
  `append_history` exclusion right for free: history must never be rewritten to match today.
- ⭐ The gates now catch each other. Registering a doctrine without mirroring it failed inside the
  same commit; the same omission had survived two prior registrations unnoticed.
- A rule keyed on words fires on prose about the rule. The frontier check matched any line
  mentioning "frontier leaf" and double-reported; anchoring it on the label fixed it, and the
  narrowing was re-fired RED — narrowing a gate is precisely the edit that can silently disable it.

