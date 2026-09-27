;; units.sexp — the modelled-unit registry (MODEL-METHOD.2). One (unit …) per unit;
;; validate with `python3 scripts/check_sexp_schema.py units.sexp schema/units.sexp`.
;; Nothing is pre-built for kinds that have never been exercised — `kind` admits exactly
;; what the corpus holds today.

(unit (id "rv64i-lab-v0") (kind processor) (layer processor) (book "docs/book/src/profiles/rv64i-lab-v0.md") (requires "C01") (requires "C02") (requires "C03") (requires "C04") (requires "C05") (requires "C06") (requires "C09") (requires "C10") (requires "C11") (requires "C13") (requires "C14") (requires "C22") (requires "C23") (requires "C24"))
