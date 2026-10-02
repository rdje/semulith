;; platform.sexp — the schema for a GENERATED platform capability manifest (platform.sexp).
;;
;; `P5-BOARD.6` (`2026-10-02`): the read-only derived export of the accepted
;; processor/device/board profile and its boot contract, for a compatibility checker
;; (docs/ARCHOGEN_INTEGRATION.md §3; OWN-06 — derived, never handwritten, so eADL-side
;; consumers import facts rather than becoming a second hardware implementation).
;; Emitted by `scripts/gen_platform.py` from the canonical inputs named in the
;; document's fingerprint header — the board definition (board.sexp, which pins the
;; processor by unit id + version + dossier digest), the pinned processor's profile
;; dossier, and the composed contract obligations (BOARD-GEN-fresh) — never handwritten.
;; The PLATFORM-GEN doctrine (`scripts/check_platform_gen.sh`) re-derives the document
;; and refuses drift: the schema decides the SHAPE, the gate decides the BYTES.
;;
;; The content mirrors §3's six bullets: processor identity and ISA facts; the memory
;; map; device identity and wiring; the declared absences; the composition dispositions;
;; the boot contract; time, events and ordering; the test-control surface; versions and
;; fingerprints (the pins and the header); limitations; and the non-claims. Every
;; facility carries an explicit `presence` marker — offered / absent-by-contract /
;; limited — so a checker reads exactly what is on offer, and an absence is a declared
;; fact, never an omission.
;;
;; The consumer-absence boundary is recorded in the document itself (the non-claims):
;; archogen is actively developed and has no functional eADL interface today, so this
;; export is validated by derivation freshness, schema conformance and §3 coverage —
;; never by archogen acceptance.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown field,
;; a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "platform"))

(construct (name platform)
  (field (name id) (type string) (min-length 1))
  (field (name version) (type string) (min-length 1))
  (field (name export-version) (type string) (min-length 1))
  (field (name status) (type symbol) (values experimental))
  (field (name processor) (type form) (head processor))
  (field (name memory) (type form) (head memory))
  (field (name device) (type form) (head device) (repeat yes) (min 1))
  (field (name absence) (type form) (head absence) (repeat yes) (min 1))
  (field (name disposition) (type form) (head disposition) (repeat yes) (optional yes))
  (field (name boot) (type form) (head boot))
  (field (name time) (type form) (head time))
  (field (name events) (type form) (head events))
  (field (name ordering) (type form) (head ordering))
  (field (name test-control) (type form) (head test-control))
  (field (name limitations) (type form) (head limitations))
  (field (name non-claims) (type form) (head non-claims)))

;; The processor: the board's pin (unit id + version + dossier digest + contract) plus
;; the ISA facts derived from the pinned unit's profile dossier. `isa` is the base
;; lowered plus any extensions; `extensions` empty means the base only. The digest is
;; verified against the live dossier by the generator — a stale pin is a refusal.
(construct (name processor)
  (field (name unit) (type string) (min-length 1))
  (field (name version) (type string) (min-length 1))
  (field (name dossier-sha256) (type string) (pattern "^[0-9a-f]{64}$"))
  (field (name contract) (type string) (min-length 1))
  (field (name contract-version) (type string) (min-length 1))
  (field (name architecture) (type string) (min-length 1))
  (field (name isa) (type string) (pattern "^[a-z0-9_]+$"))
  (field (name xlen) (type integer))
  (field (name ilen) (type integer))
  (field (name ialign) (type integer))
  (field (name harts) (type integer))
  (field (name privilege-modes) (type string) (repeat yes) (min 1))
  (field (name extensions) (type string) (repeat yes) (empty yes))
  (field (name endianness) (type symbol) (values little))
  (field (name spec) (type form) (head spec)))

(construct (name spec)
  (field (name chapter-version) (type string) (min-length 1))
  (field (name revision) (type string) (min-length 1)))

;; The resolved memory map: every region with its computed end (base + size, exclusive),
;; in the house hex style. A device's region names it; RAM serves no device.
(construct (name memory)
  (field (name region) (type form) (head region) (repeat yes) (min 1)))

(construct (name region)
  (field (name name) (type string) (min-length 1))
  (field (name base) (type string) (pattern "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*$"))
  (field (name size) (type string) (pattern "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*$"))
  (field (name end) (type string) (pattern "^0x[0-9a-f]{1,4}(_[0-9a-f]{4})*$"))
  (field (name kind) (type symbol) (values ram) (values mmio))
  (field (name executable) (type symbol) (values true) (values false))
  (field (name device) (type string) (optional yes))
  (field (name presence) (type symbol) (values offered)))

;; A wired device: the datasheet pin (material + revision + sha256), its region, the
;; datasheet-legal access widths, the declared interrupt state and the backend wiring.
(construct (name device)
  (field (name id) (type string) (min-length 1))
  (field (name unit) (type string) (min-length 1))
  (field (name kind) (type symbol) (values sifive-uart) (values lan9118))
  (field (name material) (type string) (min-length 1))
  (field (name revision) (type string) (min-length 1))
  (field (name sha256) (type string) (pattern "^[0-9a-f]{64}$"))
  (field (name region) (type string) (min-length 1))
  (field (name access-widths) (type integer) (repeat yes) (min 1) (unique yes))
  (field (name interrupt) (type symbol) (values unconnected))
  (field (name backend-rx) (type symbol) (values recorded-input) (values recorded-trace-replay))
  (field (name backend-tx) (type symbol) (values host-console) (values recording-sink))
  (field (name presence) (type symbol) (values offered)))

;; A declared absence is a fact with its evidence edge, not an omission.
(construct (name absence)
  (field (name element) (type symbol) (values timers) (values interrupt-controller))
  (field (name presence) (type symbol) (values absent-by-contract))
  (field (name satisfies) (type string) (pattern "^OB-[A-Z0-9-]+$") (repeat yes) (min 1)))

;; A composition disposition: the board's binding of a device obligation the dossier
;; deferred to the composing board (BOARD-VERDICT-checked both ways in the definition).
(construct (name disposition)
  (field (name decision) (type string) (pattern "^D-[A-Z0-9-]+$"))
  (field (name answers) (type string) (pattern "^OB-[A-Z0-9-]+$") (repeat yes) (min 1))
  (field (name statement) (type string) (min-length 1)))

;; The boot contract, mirrored from the board definition (its owner) — §3's third
;; bullet: image format, load placement, entry address/state, argument convention,
;; firmware services, ABI, and the hardware-description format this platform offers.
(construct (name boot)
  (field (name image-format) (type symbol) (values elf64))
  (field (name load-region) (type string) (min-length 1))
  (field (name entry) (type symbol) (values image-entry))
  (field (name register-state) (type symbol) (values zeroed-x1-x31))
  (field (name argument-convention) (type symbol) (values none))
  (field (name firmware-services) (type symbol) (values none))
  (field (name abi) (type symbol) (values freestanding))
  (field (name hardware-description) (type symbol) (values hardware-sexp-internal))
  (field (name presence) (type symbol) (values offered)))

;; Counter/time meaning and the declared timing fidelity — §3's fourth bullet, first
;; half. Derived from the composed obligations' parameters: `none` is a measured value
;; (`OB-ENV-VIRTUAL-TIME` pins `time_source "none"`), and a platform with no time source
;; declares functional-only fidelity by construction — the generator refuses any shape
;; it cannot judge rather than guessing a fidelity.
(construct (name time)
  (field (name time-source) (type symbol) (values none))
  (field (name frozen-counter-disposition) (type string) (pattern "^D-[A-Z0-9-]+$") (optional yes))
  (field (name timing-fidelity) (type symbol) (values functional-only))
  (field (name presence) (type symbol) (values absent-by-contract)))

;; Event delivery — §3's fourth bullet, second half. Synchronous exceptions and
;; requested traps are offered; nothing asynchronous is deliverable.
(construct (name events)
  (field (name synchronous-exceptions) (type symbol) (values yes))
  (field (name requested-traps) (type symbol) (values yes))
  (field (name asynchronous-interrupts) (type symbol) (values no))
  (field (name interrupt-controller) (type symbol) (values none))
  (field (name presence) (type symbol) (values limited)))

;; Ordering and scheduling — one hart, sequential, no memory-ordering claim, and no
;; scheduling policies on offer (nothing preempts: no timer, no interrupts, one hart).
(construct (name ordering)
  (field (name harts) (type integer))
  (field (name execution) (type symbol) (values sequential-in-order))
  (field (name memory-model-claim) (type symbol) (values none))
  (field (name scheduling-policies) (type symbol) (values none)))

;; The test-control surface, mirrored from the board definition — §3's fifth bullet.
;; Declared capabilities of the platform package, evidenced by the runner's own suites,
;; never by this document.
(construct (name test-control)
  (field (name console-capture) (type symbol) (values host-console))
  (field (name completion) (type symbol) (values typed-outcome-stop))
  (field (name reset) (type symbol) (values cold-reload))
  (field (name input-injection) (type symbol) (values recorded-backends))
  (field (name execution-budget) (type symbol) (values step-budget))
  (field (name trace-selection) (type symbol) (values step-and-store))
  (field (name snapshots) (type symbol) (values snapshot-resume))
  (field (name presence) (type symbol) (values offered)))

;; What a consumer must NOT take from this platform, and what this document does not
;; prove — both derived from the definition's data, both part of the export.
(construct (name limitations)
  (field (name limitation) (type string) (min-length 1) (repeat yes) (min 1)))

(construct (name non-claims)
  (field (name non-claim) (type string) (min-length 1) (repeat yes) (min 1)))
