# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

