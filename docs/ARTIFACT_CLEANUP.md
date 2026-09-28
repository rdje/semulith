# ARTIFACT CLEANUP — last run

- `2026-09-29`: 169 cargo incremental-cache `.bin` files deleted (272 MB), every one under a
  cargo `*/incremental/*` directory of `target/` (the project's own debug profile, 139, and the
  wasm32 profile, 30) — exactly the session-directive's enumerated scope; per-directory census
  recorded in `docs/tasks/ARTIFACT-CLEANUP.md` (Verification Log). Post-delete re-census: 0
  incremental `.bin`; `target` 3.4 G → 3.2 G; `.app-data` unchanged at 1.4 G. Kept deliberately:
  the 7 crate test fixtures under `.app-data/cargo-home/` (dependency source data, inputs, not
  artifacts) and, by standing policy, `target/refs/*.log` (spike build logs and smoke guest
  outputs — the last reference run's evidence trail).
