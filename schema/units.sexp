;; units.sexp — the schema for the modelled-unit registry (materials/units.sexp).
;;
;; A UNIT is one thing this project models: a processor, a device, a board, a computer.
;; The registry is
;; deliberately small — one row per unit, id / kind / layer / book — and nothing is pre-built
;; for kinds that have never been exercised (MODEL-METHOD.2): `kind` admits exactly what the
;; corpus holds today, and a new kind is a `(values …)` edit the day a real unit needs one.
;;
;; `P5-BOARD.11` (`2026-10-02`): registration day — `kind` gains `board` and `device`,
;; and `layer` gains `device`, the day three real units need them (case
;; netboard-lab-v0, sifive-uart-lab-v0, lan9118-lab-v0). A device is the board's
;; constituent, not the board layer — the taxonomy extends by the measured unit kinds,
;; never ahead of them.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown field,
;; a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "units"))

(construct (name unit)
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name kind) (type symbol) (values processor) (values board) (values device))
  (field (name layer) (type symbol) (values processor) (values board) (values system)
         (values device))
  (field (name book) (type string) (min-length 1))
  (field (name requires) (type string) (repeat yes) (optional yes)
         (pattern "^(C|D)[0-9]{2}$")))
