;; units.sexp — the modelled-unit registry (MODEL-METHOD.2). One (unit …) per unit;
;; validate with `python3 scripts/check_sexp_schema.py units.sexp schema/units.sexp`.
;; Nothing is pre-built for kinds that have never been exercised — `kind` admits exactly
;; what the corpus holds today. The `book` field is the unit's OWN mdBook
;; (`decision_one-definition-one-book`; `docs/models/<unit-id>/` since MODEL-BOOKS.1 —
;; it earlier pointed at a project-book page that was never created).

(unit (id "rv64i-lab-v0") (kind processor) (layer processor) (book "docs/models/rv64i-lab-v0/") (requires "C01") (requires "C02") (requires "C03") (requires "C04") (requires "C05") (requires "C06") (requires "C09") (requires "C10") (requires "C11") (requires "C13") (requires "C14") (requires "C22") (requires "C23") (requires "C24"))
;; dsp56300-lab-v0 registered by P3-BREADTH.6 slice 2 (2026-10-01) — the second unit and the
;; first non-scalar-CPU one. C17 replaces C14 in the requires set against rv64i's: reset is
;; this unit's own decision (D-RESET-STATE), while interrupts are a named subset exclusion
;; (C14 stays a census row with disposition missing, never a required category).
(unit (id "dsp56300-lab-v0") (kind processor) (layer processor) (book "docs/models/dsp56300-lab-v0/") (requires "C01") (requires "C02") (requires "C03") (requires "C04") (requires "C05") (requires "C06") (requires "C09") (requires "C10") (requires "C11") (requires "C13") (requires "C17") (requires "C22") (requires "C23") (requires "C24"))
