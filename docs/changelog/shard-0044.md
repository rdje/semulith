# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

