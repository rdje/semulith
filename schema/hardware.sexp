;; hardware.sexp — the schema for a GENERATED hardware description (hardware.sexp).
;;
;; `P5-BOARD.3` (`2026-10-02`): the board's generated map, wiring and hardware-description
;; data — emitted by `scripts/gen_board.py` from the canonical board definition
;; (`profiles/<board-id>/board.sexp`, schema `board.sexp`), never handwritten (OWN-05).
;; The BOARD-GEN doctrine (`scripts/check_board_gen.sh`) re-derives the document and
;; refuses drift, so this schema and that gate are its two governors: the schema decides
;; the SHAPE (every consumer — the composition verdict, the model route, P6's boot
;; contract — reads a validated form), the gate decides the BYTES.
;;
;; The document is a flattened, resolved rendering of the board definition: every region
;; carries its computed `end`; every device its region, access widths, interrupt state and
;; backend wiring; the declared absences (timers, interrupt controller) stay present as
;; data with the obligations they satisfy — an absence that disappears between the
;; definition and its generated rendering is exactly the drift BOARD-GEN exists to catch.
;; Addresses keep the house hex style (0x-prefixed, underscore-grouped nibble-quads), the
;; same pattern `schema/board.sexp` declares, so one reading rule covers both.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown field,
;; a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "hardware"))

(construct (name hardware)
  (field (name board) (type string) (min-length 1))
  (field (name version) (type string) (min-length 1))
  (field (name processor) (type form) (head processor))
  (field (name region) (type form) (head region) (repeat yes) (min 1))
  (field (name wiring) (type form) (head wiring) (repeat yes) (min 1))
  (field (name serial-console) (type form) (head serial-console))
  (field (name reset) (type form) (head reset))
  (field (name absence) (type form) (head absence) (repeat yes) (min 1)))

;; The processor the board composes: the unit id + version + the environment contract the
;; composition verdict (`.4`) discharges against. The dossier digest stays in board.sexp —
;; one owner per fact.
(construct (name processor)
  (field (name unit) (type string) (min-length 1))
  (field (name version) (type string) (min-length 1))
  (field (name contract) (type string) (min-length 1))
  (field (name contract-version) (type string) (min-length 1)))

;; One region per memory-map entry, resolved: `end` = base + size, computed by the
;; generator (never hand-carried). An mmio region names its device; a ram region does not.
(construct (name region)
  (field (name name) (type string) (min-length 1))
  (field (name base) (type string) (pattern "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*$"))
  (field (name size) (type string) (pattern "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*$"))
  (field (name end) (type string) (pattern "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*$"))
  (field (name kind) (type symbol) (values ram) (values mmio))
  (field (name executable) (type symbol) (values true) (values false))
  (field (name device) (type string) (optional yes)))

;; The wiring, one form per device: which region serves it, the datasheet-legal access
;; widths, the declared interrupt state, and where its effects go (the evidence leg is
;; recorded and deterministic; a live host socket is laboratory play and appears nowhere
;; here — it may never enter an evidence claim).
(construct (name wiring)
  (field (name device) (type string) (min-length 1))
  (field (name unit) (type string) (min-length 1))
  (field (name kind) (type symbol) (values sifive-uart) (values lan9118))
  (field (name region) (type string) (min-length 1))
  (field (name access-widths) (type integer) (repeat yes) (min 1) (unique yes))
  (field (name interrupt) (type symbol) (values unconnected))
  (field (name backend-rx) (type symbol) (values recorded-input) (values recorded-trace-replay))
  (field (name backend-tx) (type symbol) (values host-console) (values recording-sink)))

(construct (name serial-console)
  (field (name device) (type string) (min-length 1)))

(construct (name reset)
  (field (name kinds) (type symbol) (values cold) (repeat yes) (min 1)))

;; A declared absence, carried from the board definition with the obligation ids it
;; satisfies — the composition verdict's pre-wired edges, preserved through generation.
(construct (name absence)
  (field (name element) (type symbol) (values timers) (values interrupt-controller))
  (field (name satisfies) (type string) (pattern "^OB-[A-Z0-9-]+$") (repeat yes) (min 1)))
