# CHANGELOG shard — SEMILITH-AC-0052 … SEMILITH-AC-0052

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-AC-0052 (tree ARTIFACT-CLEANUP) — the 2026-09-28 cleanup run

- §8 time-triggered run (last record `2026-09-26`): pre-delete census 132 cargo incremental-cache `.bin` files / 720 MB, every one under a cargo `*/incremental/*` directory (`target/` own + wasm32 profiles, `.app-data/target/` vendored-consumer builds); 0 stray `.bin`/`.log` in `target/release` / `target/debug/deps`; the 7 `.app-data/cargo-home/**/tests/data/*.bin` crate-source fixtures classified inputs and kept. Post-delete re-census: 0 incremental `.bin`; `.app-data` 2.0 G → 1.4 G. Record overwritten (latest entry only) and the run evidenced in the tree's Verification Log; enforcer green.

