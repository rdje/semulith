# CHANGELOG shard — SEMULITH-AC-0058 … SEMULITH-AC-0058

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-AC-0058 (tree ARTIFACT-CLEANUP) — the 2026-10-04 §8 run: 90 incremental caches deleted (245 MB)

- The ~24 h trigger fired (the `2026-10-03` record was a day old). The census found
  90 cargo incremental `.bin` caches (245 MB; 72 `target/debug`, 18 wasm32), all under
  the enumerated `*/incremental/*` scope, deleted; 0 stray `.bin`/`.log` in
  `target/release`/`target/debug/deps`. 62 `target/refs/*.log` (2.2 M, evidence trails)
  and the 7 cargo-home crate fixtures (inputs) kept by standing policy.
  `docs/ARTIFACT_CLEANUP.md` overwritten with the dated one-line record; `target`
  4.2 G → 4.0 G, `.app-data` 1.4 G unchanged.

