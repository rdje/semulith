;; units.sexp — the modelled-unit registry (MODEL-METHOD.2). One (unit …) per unit;
;; validate with `python3 scripts/check_sexp_schema.py units.sexp schema/units.sexp`.
;; Nothing is pre-built for kinds that have never been exercised — `kind` admits exactly
;; what the corpus holds today.

(unit (id "rv64i-lab-v0") (kind processor) (layer processor) (book "docs/book/src/profiles/rv64i-lab-v0.md"))
