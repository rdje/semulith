;; override.sexp — the schema for a matched-profile reference override (override.sexp).
;;
;; `SOT-FORMAT.4`: the Sail model reads JSON, so this document is the tracked truth and the
;; JSON is derived from it (dossier_sexp.materialize_sail_override) — one source of truth,
;; one foreign-tool rendering. Extension names are dynamic (a hundred ratified Z-names and
;; counting), so they travel as data in (extension (name "…") …) entry forms rather than as
;; field names a schema would have to enumerate; the fixed keys of each entry stay
;; schema-checked. The Rust Option shapes the Sail config schema writes as {"Some": …} /
;; {"None": null} are the constructs (some (value …)) / (none). Booleans are the symbols
;; true/false. Plural containers (regions, extensions) are wrapper constructs, one form per
;; entry — the kernel's repetition rule, the same shape as (writes …) in expectations.

(schema (id "override"))

(construct (name override)
  (field (name base) (type form) (head base))
  (field (name platform) (type form) (head platform))
  (field (name memory) (type form) (head memory))
  (field (name extensions) (type form) (head extensions)))

(construct (name base)
  (field (name mstatus) (type form) (head mstatus))
  ;; P4-SYSTEM.2 slice h (the rv64gc matched override): the privileged pin, the misa
  ;; writability, the delegation masks, all optional — the rv64i override predates them.
  (field (name privileged_isa_version) (type string) (min-length 1) (optional yes))
  (field (name writable_misa) (type symbol) (values true) (values false) (optional yes))
  (field (name medeleg) (type form) (head medeleg) (optional yes))
  (field (name mideleg) (type form) (head mideleg) (optional yes)))

(construct (name medeleg)
  (field (name delegatable_bits) (type form) (head int64)))

(construct (name mideleg)
  (field (name delegatable_bits) (type form) (head int64)))

(construct (name mstatus)
  (field (name fs_legal_states) (type string) (min-length 1))
  (field (name vs_legal_states) (type string) (min-length 1)))

(construct (name platform)
  (field (name clint) (type form) (head clint))
  (field (name simple_interrupt_generator) (type form) (head simple_interrupt_generator))
  (field (name interrupts) (type form) (head interrupts))
  ;; P4-SYSTEM.2 slice h (the rv64gc matched override): the WFI policy pair — a nop
  ;; everywhere but U-mode (the laboratory's WFI-in-U refusal, the config's own keys).
  (field (name wfi_is_nop) (type symbol) (values true) (values false) (optional yes))
  (field (name wfi_available_to_user_mode) (type symbol) (values true) (values false)
         (optional yes)))

(construct (name clint)
  (field (name supported) (type symbol) (values true) (values false)))

(construct (name simple_interrupt_generator)
  (field (name supported) (type symbol) (values true) (values false)))

(construct (name interrupts)
  (field (name machine) (type form) (head machine)))

(construct (name machine)
  (field (name software) (type form) (head software))
  (field (name external) (type form) (head external))
  (field (name timer) (type form) (head timer)))

(construct (name software)
  (field (name supported) (type symbol) (values true) (values false)))

(construct (name external)
  (field (name supported) (type symbol) (values true) (values false)))

(construct (name timer)
  (field (name supported) (type symbol) (values true) (values false)))

(construct (name memory)
  (field (name misaligned) (type form) (head misaligned))
  (field (name regions) (type form) (head regions))
  ;; P4-SYSTEM.2 slice h (the rv64gc matched override): no PMP (D-NO-PMP).
  (field (name pmp) (type form) (head pmp) (optional yes)))

(construct (name pmp)
  (field (name grain) (type integer))
  (field (name count) (type integer))
  (field (name usable_count) (type integer))
  (field (name tor_supported) (type symbol) (values true) (values false))
  (field (name na4_supported) (type symbol) (values true) (values false))
  (field (name napot_supported) (type symbol) (values true) (values false)))

(construct (name regions)
  (field (name region) (type form) (head region) (repeat yes) (min 1)))

(construct (name misaligned)
  (field (name exceptions) (type form) (head exceptions)))

(construct (name exceptions)
  (field (name load_store) (type form) (head some) (head none)))

(construct (name some)
  (field (name value) (type string) (min-length 1)))

(construct (name none))

(construct (name region)
  (field (name base) (type form) (head int64))
  (field (name size) (type form) (head int64))
  (field (name attributes) (type form) (head attributes))
  (field (name include_in_device_tree) (type symbol) (values true) (values false)))

(construct (name int64)
  (field (name len) (type integer))
  (field (name value) (type string) (min-length 1)))

(construct (name attributes)
  (field (name mem_type) (type string) (min-length 1))
  (field (name cacheable) (type symbol) (values true) (values false))
  (field (name coherent) (type symbol) (values true) (values false))
  (field (name executable) (type symbol) (values true) (values false))
  (field (name readable) (type symbol) (values true) (values false))
  (field (name writable) (type symbol) (values true) (values false))
  (field (name read_idempotent) (type symbol) (values true) (values false))
  (field (name write_idempotent) (type symbol) (values true) (values false))
  (field (name misaligned_exceptions) (type form) (head misaligned_exceptions))
  (field (name atomic_support) (type string) (min-length 1))
  (field (name misaligned_atomicity_granule_size_exp) (type integer))
  (field (name vector_misaligned_atomicity_granule_size_exp) (type integer))
  (field (name reservability) (type string) (min-length 1))
  (field (name supports_cbo_zero) (type symbol) (values true) (values false))
  (field (name supports_pte_read) (type symbol) (values true) (values false))
  (field (name supports_pte_write) (type symbol) (values true) (values false)))

(construct (name misaligned_exceptions)
  (field (name load_store) (type form) (head some) (head none))
  (field (name vector) (type form) (head some) (head none))
  (field (name amo) (type string) (min-length 1))
  (field (name lrsc) (type string) (min-length 1)))

(construct (name extensions)
  (field (name extension) (type form) (head extension) (repeat yes) (min 1)))

(construct (name extension)
  (field (name name) (type string) (min-length 1))
  (field (name supported) (type symbol) (values true) (values false) (optional yes))
  (field (name support_level) (type string) (optional yes))
  (field (name vlen_exp) (type integer) (optional yes))
  (field (name elen_exp) (type integer) (optional yes))
  (field (name max_index_eew_exp) (type integer) (optional yes))
  (field (name extension) (type form) (head extension) (repeat yes)
         (optional yes)))
