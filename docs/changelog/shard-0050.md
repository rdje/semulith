# CHANGELOG shard — SEMILITH-MC-0041 … SEMILITH-MC-0040

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

