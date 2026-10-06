# ARTIFACT CLEANUP — last run

- `2026-10-06`: 192 cargo incremental-cache `.bin` files deleted (607 MB), every one under a
  cargo `*/incremental/*` directory of `target/` (the project's own debug profile, 144; the
  wasm32 profile, 36; the `.7` slice-(b) scratch probe's own cargo build, 12) — exactly the
  session-directive's enumerated scope; per-directory census recorded in
  `docs/tasks/ARTIFACT-CLEANUP.md` (Verification Log). Post-delete re-census: 0 incremental
  `.bin`; `target` 4.8 G → 4.2 G; `.app-data` unchanged at 1.4 G. Kept deliberately: the 7
  crate test fixtures under `.app-data/cargo-home/` (dependency source data, inputs, not
  artifacts) and 62 `target/refs/**/*.log` (2.2 MB, evidence trails of the last reference
  run — standing policy).
