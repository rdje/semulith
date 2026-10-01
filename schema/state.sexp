;; state.sexp — the schema for an architectural-state document (state.sexp).
;;
;; `SOT-FORMAT.4`: the retired state.json is one document form. Identifiers stay strings;
;; `authority` is a symbol, and `software-convention` is legal ONLY here — for the ABI roles
;; the ISA chapter itself names (PROFILE-CONSISTENCY carries the same rule; docs/
;; INFORMATION_CATALOG.md §6 names the mistake). Booleans are the symbols true/false. The
;; empty hidden_state list is absence (`.3` rule): the census beside it is what earns the
;; universal claim, and PROFILE-CONSISTENCY gates that.
;;
;; `P3-BREADTH.5` slice 1 (`2026-10-01`): the schema learns the shapes the exercised
;; dsp56300-lab-v0 profile's state census measured (docs/tasks/artifacts/p3-breadth/
;; 2026-10-01-dsp56300-state-census.md) — each construct names its target and case:
;; - register_family (+ parts with per-part readout) — case dsp56300-lab-v0, F1 masked
;;   widths and census candidate 1 (the A2/B2 sign-extended extension readout, A1/B1 raw);
;; - memory_spaces — case dsp56300-lab-v0, F3 (the X/Y/P spaces);
;; - hardware_stack — case dsp56300-lab-v0, census candidates 4/6 (16 levels × 48 bits,
;;   pre-incremented SP, stale popped slots observable);
;; - xlen and integer_registers are OPTIONAL — case dsp56300-lab-v0: no XLEN concept (the
;;   data word is 24-bit, FM §3.1) and no x0-anchored integer file. A document still
;;   declares at least one register block; that completeness check belongs to the
;;   consistency/generator layer, stated here rather than implied.

(schema (id "state"))

(construct (name state)
  (field (name profile_id) (type string) (min-length 1))
  (field (name xlen) (type integer) (optional yes))
  (field (name note) (type string) (min-length 1))
  (field (name integer_registers) (type form) (head integer_registers) (optional yes))
  (field (name register_family) (type form) (head register_family) (repeat yes) (optional yes))
  (field (name special_registers) (type form) (head register) (repeat yes))
  (field (name memory_spaces) (type form) (head space) (repeat yes) (optional yes))
  (field (name hardware_stack) (type form) (head hardware_stack) (optional yes))
  (field (name hidden_state_census) (type form) (head hidden_state_census)))

(construct (name integer_registers)
  (field (name count) (type integer))
  (field (name width_bits) (type integer))
  (field (name ids) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name x0) (type form) (head x0))
  (field (name named_by_the_isa_chapter) (type form) (head named-register)
         (repeat yes) (min 1))
  (field (name reset) (type form) (head reset)))

(construct (name x0)
  (field (name hardwired_zero) (type symbol) (values true) (values false))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name statement) (type string) (min-length 1)))

(construct (name named-register)
  (field (name reg) (type string) (min-length 1))
  (field (name role) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory)
         (values software-convention))
  (field (name source) (type string) (min-length 1)))

(construct (name reset)
  (field (name value) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name statement) (type string) (min-length 1)))

;; P3-BREADTH.5 slice 1 — case dsp56300-lab-v0 (F1 + the census's register classes):
;; a named register family with a masked nonstandard width, optional named parts whose
;; per-part readout rules are data (the census's candidate 1), and an optional reset.
(construct (name register_family)
  (field (name id) (type string) (min-length 1))
  (field (name count) (type integer))
  (field (name width_bits) (type integer))
  (field (name ids) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name parts) (type form) (head part) (repeat yes) (optional yes))
  (field (name reset) (type form) (head reset) (optional yes)))

(construct (name part)
  (field (name id) (type string) (min-length 1))
  (field (name bit_hi) (type integer))
  (field (name bit_lo) (type integer))
  (field (name readout) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1)))

;; P3-BREADTH.5 slice 1 — case dsp56300-lab-v0 (F3): a distinct memory space.
(construct (name space)
  (field (name id) (type string) (min-length 1))
  (field (name word_bits) (type integer))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1)))

;; P3-BREADTH.5 slice 1 — case dsp56300-lab-v0 (the census's candidates 4/6): the
;; hardware stack. `indexing` carries the push/pop discipline in prose (e.g. SP
;; pre-increments, slot 0 unwritable); `stale_slots_observable` records whether popped
;; content persists where an observer can read it — the DSP56300's does.
(construct (name hardware_stack)
  (field (name levels) (type integer))
  (field (name width_bits) (type integer))
  (field (name indexing) (type string) (min-length 1))
  (field (name stale_slots_observable) (type symbol) (values true) (values false))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1)))

(construct (name register)
  (field (name id) (type string) (min-length 1))
  (field (name width_bits) (type integer))
  (field (name holds) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name reset) (type string) (min-length 1))
  (field (name reset_authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory)))

(construct (name hidden_state_census)
  (field (name question) (type string) (min-length 1))
  (field (name answer) (type string) (min-length 1))
  (field (name candidates) (type form) (head checked) (repeat yes) (min 1))
  (field (name consequence) (type string) (min-length 1)))

(construct (name checked)
  (field (name candidate) (type string) (min-length 1))
  (field (name present) (type symbol) (values true) (values false))
  (field (name why) (type string) (min-length 1)))
