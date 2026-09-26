# ARTIFACT CLEANUP — last run

- `2026-09-26`: 40 cargo incremental-cache `.bin` files deleted (22 under `target/`, 18 under `.app-data/target/`, 341 MB), scope exactly the session-directive's enumerated cargo dirs. Kept deliberately: crate test fixtures under `.app-data/cargo-home/` (dependency source data, not artifacts) and `target/refs/*.log` (reference-run evidence trails, 1.3 MB). Evidence: `docs/tasks/ARTIFACT-CLEANUP.md` (leaf `.1`).
