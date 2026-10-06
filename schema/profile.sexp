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

;; `P5-BOARD.6` (`2026-10-02`): `endianness` joins the optional processor-only fields —
;; the platform capability manifest (schema `platform.sexp`) must EXPOSE the value
;; (docs/ARCHOGEN_INTEGRATION.md §3), and the value's one owner is the CPU dossier
;; (`D-ENDIAN` carried it as prose only). Optional for the same reason as `xlen`: a
;; device unit has no endianness concept. `(values little)` today; `big` joins the day a
;; big-endian profile needs one (the sanctioned `(values …)` edit).

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
  (field (name endianness) (type symbol) (values little) (optional yes))
  (field (name extensions) (type string) (repeat yes))
  (field (name privilege_modes) (type string) (repeat yes))
  (field (name sources) (type string) (repeat yes) (min 1))
  (field (name state) (type form) (head state))
  (field (name scope) (type form) (head scope))
  (field (name vehicle) (type form) (head vehicle) (optional yes))
  (field (name decision) (type form) (head decision) (repeat yes) (min 1)))

;; P3-BREADTH.7 slice 1 — case dsp56300-lab-v0: the unit's model route and comparison
;; shape, declared as data so gates derive applicability rather than presume it.
;; `P4-SYSTEM.1` (`2026-10-02`): the vehicle `route` gains `profile-resolution` — a
;; unit whose SELECTION is resolved and citable but whose definition pipeline has not
;; started (case rv64gc-lab-v0). The definition-pipeline gates (EXTRACTION,
;; EXERCISE-COVERAGE, INTERACTION-MATRIX) report the stage by declaration and refuse a
;; contradiction (an encoding, state census, guest corpus or interaction matrix beside
;; the declaration is a finding, never a drift) — the same by-declaration discipline as
;; the device-model route. `comparison` goes optional: a resolution has no comparison
;; shape yet; the processor and device routes keep declaring it by convention.

(construct (name vehicle)
  (field (name route) (type symbol)
         (values generated-definition) (values sibling-crate) (values device-model)
         (values profile-resolution))
  (field (name comparison) (type symbol) (optional yes)
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
  (field (name mmio_registers) (type string) (repeat yes) (optional yes))
  ;; `P4-SYSTEM.2` slice (e) (`2026-10-03`): the rv64gc scope-census growth (52 → 65), case
  ;; rv64gc-lab-v0 — three families: the Zicsr CSR access forms, the privileged system
  ;; forms (mret/sret/wfi/sfence.vma — RVP-INSNS 18.1), and the Zicntr counter reads. The
  ;; Zicntr names are the SPEC's instruction listings (RVI-ZICNTR §6.1.1); the encoding
  ;; realizes them as csrrs specializations (definitions/riscv/zicntr.sexp's pseudos) — the
  ;; census is the profile's spec-facing form set, the pseudo relation is the realization's.
  (field (name zicsr_csrs) (type string) (repeat yes) (optional yes))
  (field (name system_privileged) (type string) (repeat yes) (optional yes))
  (field (name zicntr_counters) (type string) (repeat yes) (optional yes))
  ;; `P4-SYSTEM.4` slice (e) (`2026-10-05`): the A extension binds — the census grows
  ;; 65 → 87. The 22 names are the pinned RVWMO chapter's Tables 6/7 enumeration (the
  ;; nine Zaamo operations and the Zalrsc pair, each .W and .D, RVI-A §12.1), realized
  ;; by the rv_a/rv64_a tables (definitions/riscv/a.sexp).
  (field (name a_atomics) (type string) (repeat yes) (optional yes))
  ;; `P4-SYSTEM.6` slice (b) (`2026-10-05`): Zifencei binds — the census grows 87 → 88.
  ;; The one name is the pinned chapter's own instruction (FENCE.I, RVI-ZIFENCEI §4.1,
  ;; Version 2.0), realized by the rv_zifencei table's single row
  ;; (definitions/riscv/zifencei.sexp).
  (field (name zifencei_fencei) (type string) (repeat yes) (optional yes))
  ;; `P4-SYSTEM.7` slice (c6) (`2026-10-06`): F binds — the census grows 88 → 118. The
  ;; 30 names are the pinned chapter's single-precision forms (RVI-F §20.1.5–§20.1.9,
  ;; Version 2.2: the FLW/FSW transfers, the four fused multiply-adds, the arithmetic,
  ;; sign injection, min/max, the conversions and moves, the compares, FCLASS.S),
  ;; realized by the rv_f/rv64_f tables (definitions/riscv/f.sexp).
  (field (name f_single) (type string) (repeat yes) (optional yes))
  ;; `P4-SYSTEM.7` slice (d5) (`2026-10-06`): D binds — the census grows 118 → 150. The
  ;; 32 names are the pinned chapter's double-precision forms (RVI-D §21.1.3–§21.1.7,
  ;; Version 2.2: FLD/FSD, the fused four, the arithmetic, sign injection, min/max, the
  ;; two format conversions, the compares, FCLASS.D, the integer conversions, the
  ;; FMV.X.D/FMV.D.X moves), realized by the rv_d/rv64_d tables (definitions/riscv/d.sexp).
  (field (name d_double) (type string) (repeat yes) (optional yes)))

(construct (name decision)
  (field (name id) (type string) (pattern "^D-[A-Z0-9-]+$"))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name statement) (type string) (min-length 1))
  (field (name source) (type string) (min-length 1))
  (field (name note) (type string) (optional yes)))
