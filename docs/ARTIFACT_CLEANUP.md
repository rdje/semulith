# ARTIFACT CLEANUP — last run

- `2026-10-03`: 0 cargo incremental-cache `.bin` files present to delete (none accumulated
  since the `2026-10-02` run — no cargo builds with incremental output in between);
  per-directory census recorded in `docs/tasks/ARTIFACT-CLEANUP.md` (Verification Log).
  Post-delete re-census: 0 incremental `.bin`; `target` 3.9 G, `.app-data` unchanged at
  1.4 G. Kept deliberately: the 7 crate test fixtures under `.app-data/cargo-home/`
  (dependency source data, inputs, not artifacts) and 62 `target/refs/*.log` (2.2 MB,
  evidence trails of the last reference run — standing policy).
