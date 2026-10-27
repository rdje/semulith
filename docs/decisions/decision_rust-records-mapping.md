# The harness reads record catalogues with its own mapping, measured equal to the pinned `scripts/records_sexp.py`; the pinned mapping stays

- **Type:** `decision`
- **Date:** `2026-10-27`
- **Status:** `active`
- **Owner / source:** `XTASK.6` slice 6o, `SEMULITH-XTASK-0023` (a tooling slice taken while every feature leaf waits on a
  ruling — the alternation of [`decision_alternate-port-and-features.md`](decision_alternate-port-and-features.md) resumes
  with features the day one lands); continues [`decision_rust-sexp-reader.md`](decision_rust-sexp-reader.md) and
  [`decision_rust-schema-validator.md`](decision_rust-schema-validator.md).
answers: How do the two remaining drivers that read records as dictionaries move to the harness without a second definition of the JSON key ↔ field correspondence?

## The fact / decision

1. **One mapping in Rust, `xtask/src/records.rs`**, equal to the pinned `scripts/records_sexp.py` by measurement: the same
   four record shapes (requirement, obligation, unit, category-need) read into ordered JSON-shaped records with the same keys
   in the same order, the same typed parameter values (`int`, `str`, `true`, `false`, `null`, `ints`, `strs`), the same
   refusals for values the corpus does not write, and the same writer (`dict_to_form`, the closed string escapes, one form
   per line). The loader goes through the catalogue reader's include expansion (`record_catalog.text`, ported with its
   refusals: cycle, duplicate part, unreadable part, include family, catalogue root, part form, include shape, include
   path, include escape), so a composed obligation catalogue reads exactly as the pinned tool reads it.
2. **The equality is held by tests, permanently.** `the_catalogues_read_as_the_pinned_mapping_reads_them` lists every tracked
   catalogue the mapping serves (the RECORD-SCHEMA map's requirements, obligations, units and category-needs files plus the
   obligation parts: 16 today) and requires the two readers' JSON dumps identical line for line through one `python3 -I`
   comparator process; `the_renderer_round_trips_the_rendered_catalogues` holds the three catalogues the pinned renderer
   itself round-trips byte for byte. `cargo xtask records <catalogue> [--dump]` is the by-hand surface.
3. **What the mapping does not claim.** Thirteen of the sixteen catalogues do not round-trip through either renderer —
   they carry comments and layout the compact renderer drops; that is the pinned tool's own behaviour, measured, and the
   writer is equal to it, not to the files. The `credits.sexp` catalogue is not a record form for this mapping in either
   tool (its reader is `credit_records.py`); it is out of scope here.
4. **Nothing is ported and nothing is shimmed by this slice.** `scripts/records_sexp.py` is untouched — a pinned input of the
   retained M case's manifest — and all fifty-one of its callers still run it. The mapping exists so that `check_scope_coverage.sh`
   and `check_extraction.sh`, the two uncoupled drivers that read records as dictionaries, can be ported (slice 6p) without
   a second definition of the correspondence.

## Why

- The mapping is the single owner of the JSON key ↔ field name correspondence (`SOT-FORMAT.3`); a port that re-derived it
  from the schema would be a second owner, which is exactly the drift the pinned module exists to prevent. Equality by
  measurement, re-run on every `cargo test`, keeps one owner.

## How to apply

- xtask doctrine modules read catalogues through `records::load` and write through `records::dump`; the pinned Python mapping
  is never edited for the port's sake.
- A new record shape or parameter value kind the corpus adopts must land in the pinned module first (it is the definition) and
  then here, with the corpus-equality test as the witness that the two agree.
