# Toolbox — composition

Composition and the board — records, assumptions, composed units, the board, its platform
export. Part of the partitioned toolbox: the doctrine and the bounded index are `TOOLBOX.md`;
every diagnostic is tracked so a number it produced can be re-derived (`LIVE-CONTAINMENT.3`).

| Tool | Answers | How to invoke |
| --- | --- | --- |
| `scripts/merge_records.py` | do these two units' records compose — same id, same content; and does every reference resolve across the union? | `scripts/merge_records.py <unit-dir>…` (a unit directory carries `requirements.sexp` / `contract-obligations.sexp` / `sources.sexp` by name; `--self-test` fires the contradiction arms) |
| `scripts/discharge_assumptions.py` | is every environment-assumption discharged by a named guarantee — or does the composition fail, naming it? | `scripts/discharge_assumptions.py <unit-dir>…` (decides over `merge_units(…)`; `--self-test` fires the chain/zero-dep controls) |
| `scripts/compose_units.py` | what does a composition look like as an ordinary unit — and does the materialized board check with the same code? | `scripts/compose_units.py <manifest.sexp> <out-dir>` (`--self-test`; manifest: `(composition (id …) (part …))`, parts manifest-relative) |
| `scripts/gen_board.py` + `scripts/check_board_gen.sh` | what does the canonical board definition lower to (manifest, composed catalogues, hardware description, map) — and is it still byte-exact? | `python3 scripts/gen_board.py [--check]`; BOARD-GEN doctrine (`P5-BOARD.3`; the generator refuses an inconsistent definition by name) |
| `scripts/board_verdict.py` + `scripts/check_board_verdict.sh` | is the board's composition verdict still ACCEPTED — every CPU assumption discharged, every `satisfies` edge resolved, every board-deferred obligation bound? | `python3 scripts/board_verdict.py <board-dir>`; BOARD-VERDICT doctrine (`P5-BOARD.4`) |
| `scripts/gen_platform.py` + `scripts/check_platform_gen.sh` | what does the board export to a compatibility checker (the OWN-06 platform capability manifest) — and is it still byte-exact, the dossier pin verified live? | `python3 scripts/gen_platform.py [--check]`; PLATFORM-GEN doctrine (`P5-BOARD.6`) |
