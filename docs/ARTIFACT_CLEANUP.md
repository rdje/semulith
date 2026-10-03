# ARTIFACT CLEANUP — last run

- `2026-10-04`: 90 cargo incremental-cache `.bin` files deleted (245 MB), every one under a
  cargo `*/incremental/*` directory of `target/` (the project's own debug profile, 72; the
  wasm32 profile, 18) — exactly the session-directive's enumerated scope; per-directory census
  recorded in `docs/tasks/ARTIFACT-CLEANUP.md` (Verification Log). Post-delete re-census: 0
  incremental `.bin`; `target` 4.2 G → 4.0 G; `.app-data` unchanged at 1.4 G. Kept deliberately:
  the 7 crate test fixtures under `.app-data/cargo-home/` (dependency source data, inputs, not
  artifacts) and 62 `target/refs/*.log` (2.2 MB, evidence trails of the last reference run —
  standing policy).
