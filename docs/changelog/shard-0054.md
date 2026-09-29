# CHANGELOG shard — SEMILITH-MM-0044 … SEMILITH-MC-0043

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

