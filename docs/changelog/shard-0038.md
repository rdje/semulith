# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

