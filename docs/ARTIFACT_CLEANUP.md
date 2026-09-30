# ARTIFACT CLEANUP — last run

- `2026-10-01`: 96 cargo incremental-cache `.bin` files deleted (248 MB), every one under a
  cargo `*/incremental/*` directory of `target/` (the project's own debug profile, 48; the
  wasm32 profile, 12; the x86_64 profile, 18; the two miri profiles, 9+9) — exactly the
  session-directive's enumerated scope; per-directory census recorded in
  `docs/tasks/ARTIFACT_CLEANUP.md` (Verification Log). Post-delete re-census: 0 incremental
  `.bin`; `target` 3.7 G → 3.5 G; `.app-data` unchanged at 1.4 G. Kept deliberately: the 7
  crate test fixtures under `.app-data/cargo-home/` (dependency source data, inputs, not
  artifacts). No `target/refs/*.log` present this run (none to keep or delete).
