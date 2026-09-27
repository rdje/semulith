# ARTIFACT CLEANUP — last run

- `2026-09-28`: 132 cargo incremental-cache `.bin` files deleted (720 MB), every one under a
  cargo `*/incremental/*` directory of `target/` or `.app-data/target/` (semulith's own debug and
  wasm32 profiles plus the vendored-consumer builds) — exactly the session-directive's enumerated
  scope; per-directory census recorded in `docs/tasks/ARTIFACT-CLEANUP.md` (Verification Log).
  Post-delete re-census: 0 incremental `.bin`; `.app-data` 2.0 G → 1.4 G. Kept deliberately: the
  7 crate test fixtures under `.app-data/cargo-home/` (dependency source data, inputs, not
  artifacts) and, by standing policy, `target/refs/*.log` (none present in this clone today).
