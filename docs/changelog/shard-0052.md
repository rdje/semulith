# CHANGELOG shard — SEMILITH-MC-0042 … SEMILITH-MC-0042

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

