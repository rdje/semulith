;; board.sexp — the schema for a board definition (board.sexp).
;;
;; `P5-BOARD.1` (`2026-10-02`): the first non-processor source-of-truth document. A board
;; definition composes EXACT versions — a processor by unit id + version + dossier content
;; digest, each device by its datasheet's material id + revision + sha256 — never names
;; (OWN-05; the leaf's acceptance). The memory map, the reset behaviour, and the three
;; platform absences/presences the CPU contract makes load-bearing (timers, the interrupt
;; controller, the serial console) are data here; `DOSSIER.md` narrates them and every
;; generated map is downstream (`.3`), gated against drift.
;;
;; An absence the CPU contract depends on is DECLARED, never omitted: `timers` and
;; `interrupt-controller` carry `(present false)` with the reason and the obligation ids
;; they satisfy — an undocumented absence reads as an oversight, and an oversight is how a
;; CLINT slips in as a "feature" and becomes a composition rejection (ENV-02).
;;
;; `satisfies` fields pre-wire the composition verdict (`.4`): they declare which CPU
;; environment assumption a board element answers. The verdict is computed by
;; scripts/discharge_assumptions.py; the declaration here is the intent it checks.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown field,
;; a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "board"))

(construct (name board)
  (field (name id) (type string) (min-length 1))
  (field (name version) (type string) (min-length 1))
  (field (name status) (type symbol) (values experimental))
  (field (name processor) (type form) (head processor))
  (field (name device) (type form) (head device) (repeat yes) (min 1))
  (field (name memory-map) (type form) (head memory-map))
  (field (name reset) (type form) (head reset))
  (field (name timers) (type form) (head timers))
  (field (name interrupt-controller) (type form) (head interrupt-controller))
  (field (name serial-console) (type form) (head serial-console))
  (field (name decision) (type form) (head decision) (repeat yes) (min 1)))

;; The processor pin: unit id + version + the dossier content digest the unit's gate
;; report records (GATE-REPORT-gated) — the board inherits the processor's status, so a
;; digest match against a NEWER dossier is a finding, not a silent upgrade.
(construct (name processor)
  (field (name unit) (type string) (min-length 1))
  (field (name version) (type string) (min-length 1))
  (field (name dossier-sha256) (type string) (pattern "^[0-9a-f]{64}$"))
  (field (name contract) (type string) (min-length 1))
  (field (name contract-version) (type string) (min-length 1)))

;; A device pin: the datasheet's material id + revision + sha256 from materials/catalog.sexp.
;; `unit` names the device unit whose dossier `P5-BOARD.2` owns — declared here before that
;; dossier exists, with the owner named (the WAIVER-ROUTING shape: honesty with an owner).
;; `access-widths` are the datasheet-legal MMIO widths in bits; any other width is a
;; contract violation, never silently serviced. `interrupt` is a declared state — today
;; exactly `unconnected`, because the CPU contract admits no asynchronous event.
(construct (name device)
  (field (name id) (type string) (min-length 1))
  (field (name unit) (type string) (min-length 1))
  (field (name kind) (type symbol) (values sifive-uart) (values lan9118))
  (field (name material) (type string) (min-length 1))
  (field (name revision) (type string) (min-length 1))
  (field (name sha256) (type string) (pattern "^[0-9a-f]{64}$"))
  (field (name access-widths) (type integer) (repeat yes) (min 1) (unique yes))
  (field (name interrupt) (type symbol) (values unconnected))
  (field (name backend) (type form) (head backend)))

;; Where the device's effects go. The evidence leg is recorded and deterministic; a live
;; host socket is laboratory play at the Environment boundary and may never enter an
;; evidence claim — declared so it is a choice on record, not an accident of wiring.
(construct (name backend)
  (field (name rx) (type symbol) (values recorded-input) (values recorded-trace-replay))
  (field (name tx) (type symbol) (values host-console) (values recording-sink))
  (field (name live-host-socket) (type symbol) (values laboratory-only) (optional yes)))

;; The one memory map — the map `.3` generates every downstream map from. Addresses are
;; 64-bit values written 0x-prefixed, underscore-grouped by nibble-quads (the house style).
(construct (name memory-map)
  (field (name region) (type form) (head region) (repeat yes) (min 1)))

(construct (name region)
  (field (name name) (type string) (min-length 1))
  (field (name base) (type string) (pattern "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*$"))
  (field (name size) (type string) (pattern "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*$"))
  (field (name kind) (type symbol) (values ram) (values mmio))
  (field (name executable) (type symbol) (values true) (values false))
  (field (name device) (type string) (optional yes)))

;; Reset: cold only for this board — the entry state is the CPU contract's, cited, not
;; restated (one owner per fact).
(construct (name reset)
  (field (name kinds) (type symbol) (values cold) (repeat yes) (min 1))
  (field (name entry) (type string) (min-length 1))
  (field (name retained-state) (type symbol) (values none))
  (field (name satisfies) (type string) (pattern "^OB-[A-Z0-9-]+$") (repeat yes) (min 1)))

;; The declared absences. `present` admits exactly `false` today: the day a board carries
;; a timer or an interrupt controller, its CPU contract has counter/interrupt assumptions
;; to satisfy instead, and the schema grows a `true` vocabulary with that board — never
;; ahead of it (the units-registry doctrine applied to platform elements).
(construct (name timers)
  (field (name present) (type symbol) (values false))
  (field (name reason) (type string) (min-length 1))
  (field (name satisfies) (type string) (pattern "^OB-[A-Z0-9-]+$") (repeat yes) (min 1)))

(construct (name interrupt-controller)
  (field (name present) (type symbol) (values false))
  (field (name reason) (type string) (min-length 1))
  (field (name satisfies) (type string) (pattern "^OB-[A-Z0-9-]+$") (repeat yes) (min 1)))

(construct (name serial-console)
  (field (name device) (type string) (min-length 1)))

;; The decision idiom of schema/profile.sexp, unchanged: every element of the spec that
;; was a choice carries its authority and its source. `answers` (`P5-BOARD.4`) binds a
;; decision to the device obligation it dispositions: a device dossier may defer a value
;; to the composing board (an obligation marked composition_disposition "required" — the
;; LAN9118's strap values, frozen time sources, replay link scene and pin tie-offs), and
;; the BOARD-VERDICT doctrine checks the binding both ways — every marked obligation is
;; answered by exactly one decision, and every `answers` names a marked obligation.
(construct (name decision)
  (field (name id) (type string) (pattern "^D-[A-Z0-9-]+$"))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name statement) (type string) (min-length 1))
  (field (name source) (type string) (min-length 1))
  (field (name note) (type string) (optional yes))
  (field (name answers) (type string) (pattern "^OB-[A-Z0-9-]+$")
         (repeat yes) (unique yes) (optional yes)))
