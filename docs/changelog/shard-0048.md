# CHANGELOG shard — SEMILITH-SF-0061 … SEMILITH-SF-0061

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-SF-0061 (leaf SOT-FORMAT.6) — the split cannot return: SOURCE-FORMAT registers, SOT-FORMAT closes

The 14th project doctrine is registered: `scripts/check_source_format.sh` refuses a source of
truth outside the one format — a tracked `.toml` / `.json` / `.jsonl` / `.yaml` under
`definitions/`, `schema/`, `profiles/`, `materials/` is named and refused (the FORMAT arm,
fired RED before registration against a scratch copy of the real corpus with one planted
`profile.toml`), and every `.sexp` there must parse with the one reader (PARSES). The real
corpus — 28 source-of-truth files — is green. Retirement in prose decays; the gate is the
decay's answer. Both doctrine mirrors (`DOCTRINE_ENFORCEMENT.md`, the mdBook) carry the row in
the registering commit; LIVE_STATUS's 14 doctrines / 184 arms are re-derived, not remembered.

The supersession chain was verified, not assumed: `decision_canonical-definition-input` has
carried its replacement since `SEMILITH-SF-0041`. Two stale lines surfaced while reading for
this leaf — the replacement record's own *How to apply* still said "write the EBNF in `pgen`"
against its director-corrected body (LinkedSpec), and both INDEX descriptions repeated it —
corrected in passing, with the reason recorded in the record. **SOT-FORMAT closes at 10/10.**

