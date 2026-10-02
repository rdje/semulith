;; profile.sexp — the schema for a profile decision dossier (profile.sexp).
;;
;; `SOT-FORMAT.4`: the [profile]/[state]/[scope] tables and the [[decision]] records of the
;; retired profile.toml are one document form. Keys are field names verbatim; `authority` is
;; the one project-owned closed enum and travels as a symbol — a typo is refused by name.
;; Booleans are the symbols true/false. PROFILE-CONSISTENCY remains the owner of the
;; dossier's completeness (its 39 arms); this schema type-checks the document.
;;
;; A profile.toml carries human commentary; every one of those lines survives conversion as
;; a (comment "…") form — the format's reserved annotation head, allowed anywhere.
;;
;; `P3-BREADTH.5` slice 2 (`2026-10-01`): the scope taxonomy generalizes for the exercised
;; dsp56300-lab-v0 profile (the scope-taxonomy case). `xlen`, the state block's integer-file
;; scalars, and `count_rv64i_additions` are OPTIONAL — the DSP has no XLEN concept, no
;; x0-anchored integer file, and no RV64I base/additions split; forcing any of them would
;; record a lie. The scope gains the DSP's five group fields (moves, alu_core, multiplies,
;; flow, loops), each naming its case here; the gate readers were already generic over
;; group names (EXERCISE-COVERAGE unions every non-count field; PROFILE-CONSISTENCY sums
;; list values), so no reader changed. `dossier_sexp._SCOPE_LISTS` is the other closed
;; place the taxonomy lives — the two are extended together.
;;
;; `P3-BREADTH.7` slice 1 (`2026-10-01`): the optional `vehicle` block declares the unit's
;; model route and comparison shape (case dsp56300-lab-v0:
;; `decision_gate-applicability-by-declared-vehicle`). Gates derive per-unit applicability
;; from this declaration plus the unit's documents; a declaration that contradicts the
;; documents is a finding, never a drift. Absence means the generated-definition /
;; per-step-trace contract, exactly as before.
;;
;; `P5-BOARD.2` (`2026-10-02`): the taxonomy generalizes for the drafted sifive-uart-lab-v0
;; device dossier (the device-register case). A DEVICE unit (vehicle route `device-model`)
;; is not an ISA: `architecture`, `base`, `harts`, `ilen`, `ialign`, and the state block's
;; `program_counter` are OPTIONAL — the UART has no ISA chapter, no harts, and no
;; instruction-length/alignment concept; forcing any of them would record a lie.
;; `chapter_version`/`spec_revision` stay MANDATORY — the SiFive manual carries honest
;; values for both. The scope gains `mmio_registers`, the device's register census (the
;; exercise/consistency gates sum it like every other group field — the readers were
;; already generic). The vehicle `route` gains `device-model` and `comparison` gains
;; `register-expectations`. `dossier_sexp._SCOPE_LISTS` is extended in the same breath.

(schema (id "profile"))

(construct (name profile)
  (field (name id) (type string) (min-length 1))
  (field (name version) (type string) (min-length 1))
  (field (name status) (type string) (min-length 1))
  (field (name architecture) (type string) (min-length 1) (optional yes))
  (field (name base) (type string) (min-length 1) (optional yes))
  (field (name chapter_version) (type string) (min-length 1))
  (field (name spec_revision) (type string) (min-length 1))
  (field (name harts) (type integer) (optional yes))
  (field (name xlen) (type integer) (optional yes))
  (field (name ilen) (type integer) (optional yes))
  (field (name ialign) (type integer) (optional yes))
  (field (name extensions) (type string) (repeat yes))
  (field (name privilege_modes) (type string) (repeat yes))
  (field (name sources) (type string) (repeat yes) (min 1))
  (field (name state) (type form) (head state))
  (field (name scope) (type form) (head scope))
  (field (name vehicle) (type form) (head vehicle) (optional yes))
  (field (name decision) (type form) (head decision) (repeat yes) (min 1)))

;; P3-BREADTH.7 slice 1 — case dsp56300-lab-v0: the unit's model route and comparison
;; shape, declared as data so gates derive applicability rather than presume it.
(construct (name vehicle)
  (field (name route) (type symbol)
         (values generated-definition) (values sibling-crate) (values device-model))
  (field (name comparison) (type symbol)
         (values per-step-trace) (values checkpoint-end-state) (values register-expectations))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1)))

(construct (name state)
  (field (name integer_registers) (type integer) (optional yes))
  (field (name x0_hardwired_zero) (type symbol) (values true) (values false) (optional yes))
  (field (name register_width_bits) (type integer) (optional yes))
  (field (name program_counter) (type string) (min-length 1) (optional yes))
  (field (name csrs) (type string) (repeat yes))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1)))

(construct (name scope)
  (field (name count_base) (type integer))
  (field (name count_rv64i_additions) (type integer) (optional yes))
  (field (name count_total) (type integer))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name base_u_type) (type string) (repeat yes))
  (field (name base_jumps) (type string) (repeat yes))
  (field (name base_branches) (type string) (repeat yes))
  (field (name base_loads) (type string) (repeat yes))
  (field (name base_stores) (type string) (repeat yes))
  (field (name base_op_imm) (type string) (repeat yes))
  (field (name base_op) (type string) (repeat yes))
  (field (name base_misc_mem) (type string) (repeat yes))
  (field (name base_system) (type string) (repeat yes))
  (field (name rv64_loads) (type string) (repeat yes))
  (field (name rv64_stores) (type string) (repeat yes))
  (field (name rv64_op_imm_32) (type string) (repeat yes))
  (field (name rv64_op_32) (type string) (repeat yes))
  (field (name moves) (type string) (repeat yes) (optional yes))
  (field (name alu_core) (type string) (repeat yes) (optional yes))
  (field (name multiplies) (type string) (repeat yes) (optional yes))
  (field (name flow) (type string) (repeat yes) (optional yes))
  (field (name loops) (type string) (repeat yes) (optional yes))
  (field (name mmio_registers) (type string) (repeat yes) (optional yes)))

(construct (name decision)
  (field (name id) (type string) (pattern "^D-[A-Z0-9-]+$"))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name statement) (type string) (min-length 1))
  (field (name source) (type string) (min-length 1))
  (field (name note) (type string) (optional yes)))
