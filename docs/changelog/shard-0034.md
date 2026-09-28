# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

