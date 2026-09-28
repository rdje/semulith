# DEV_NOTES shard — _(2026-09-27)_ … _(2026-09-27)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

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

