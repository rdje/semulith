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

(schema (id "profile"))

(construct (name profile)
  (field (name id) (type string) (min-length 1))
  (field (name version) (type string) (min-length 1))
  (field (name status) (type string) (min-length 1))
  (field (name architecture) (type string) (min-length 1))
  (field (name base) (type string) (min-length 1))
  (field (name chapter_version) (type string) (min-length 1))
  (field (name spec_revision) (type string) (min-length 1))
  (field (name harts) (type integer))
  (field (name xlen) (type integer) (optional yes))
  (field (name ilen) (type integer))
  (field (name ialign) (type integer))
  (field (name extensions) (type string) (repeat yes))
  (field (name privilege_modes) (type string) (repeat yes))
  (field (name sources) (type string) (repeat yes) (min 1))
  (field (name state) (type form) (head state))
  (field (name scope) (type form) (head scope))
  (field (name decision) (type form) (head decision) (repeat yes) (min 1)))

(construct (name state)
  (field (name integer_registers) (type integer) (optional yes))
  (field (name x0_hardwired_zero) (type symbol) (values true) (values false) (optional yes))
  (field (name register_width_bits) (type integer) (optional yes))
  (field (name program_counter) (type string) (min-length 1))
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
  (field (name loops) (type string) (repeat yes) (optional yes)))

(construct (name decision)
  (field (name id) (type string) (pattern "^D-[A-Z0-9-]+$"))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name statement) (type string) (min-length 1))
  (field (name source) (type string) (min-length 1))
  (field (name note) (type string) (optional yes)))
