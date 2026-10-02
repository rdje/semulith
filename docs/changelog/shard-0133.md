# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — a second profile walks into the gates (P3-BREADTH.4, slice 2)

The dossier slice's first job was a measurement, not a file: how do the auto-discovering
gates treat a second, deliberately partial profile? The answer, read from the gate sources
and then confirmed by a green `make gate` with the dossier present, is better than hoped:
every one of them keys on `profiles/*/profile.sexp` or `profiles/*/encoding.sexp`, so a
dossier whose schema-deferred documents do not exist yet is simply invisible — and the day
those documents land (the model slice, then `.5`), the gates attach with no gate edit at
all. The discipline that made this boring is the same one that made the deferrals explicit:
DOSSIER.md carries a deferral table in which every absent document names its owning leaf,
so "invisible to the gates" never reads as "forgotten". Two smaller facts earned their
keep: `fetch_references.sh` processed candidates only by hardcoded id, so the dsp56300
ledger needed a generic source-tarball leg (the discriminator — asset + source_commit +
asset_sha256 — was chosen so the rv64 ledger provably never reaches it, then re-verified
identical); and the FM manual's pin gained a second acquisition route when NXP's own
locator served byte-identical bytes to the chipdoc-cached copy — a version string is not an
identity, but a digest match from two independent routes is close to one. Promotion:
declined in the leaf (the census lives where the next profile meets it; the durable output
is the measured answer, not a method).

