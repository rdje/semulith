# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

