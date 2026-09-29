;; expectations.sexp — the schema for a guest expectation document (*.expected.sexp).
;;
;; `SOT-FORMAT.4`: the retired *.expected.toml files are one document form each. Every
;; expected value was derived from the pinned specification prose BEFORE the program was
;; run (EVD-05); `derivation` carries the reasoning and `source` the locator, and both are
;; required — an expectation without its derivation is a number nobody can re-derive.
;; `writes` names the registers a step must write; the EMPTY writes table — a store writes
;; no register — is the marker form (writes), distinct from an absent table. A register a
;; step must never write (never_written) is the negative observation that catches a control
;; transfer that silently did not happen. Register names are dynamic, so they travel as
;; data in (write (reg "…") (value "…")) entry forms.

(schema (id "expectations"))

(construct (name expectations)
  (field (name program) (type string) (min-length 1))
  (field (name entry) (type string) (min-length 1))
  (field (name instructions) (type integer))
  (field (name never_written) (type string) (repeat yes))
  (field (name cross_model) (type symbol) (values true) (values false) (optional yes))
  (field (name expect_divergence) (type form) (head expect_divergence) (optional yes))
  (field (name step) (type form) (head step) (repeat yes) (min 1)))

;; `expect_divergence` (P2-SCALAR.4) declares that the cross-model comparison MUST diverge in
;; exactly one named way: `difference` is a `[[difference]]` id in references.sexp, `at_step`
;; the aligned step where the first divergence must land. It is the opposite act from
;; `cross_model false` — not a comparison DISABLED but a comparison that must fail in exactly
;; the declared way; an AGREE verdict against it is the RED case (the recorded difference no
;; longer exists, so the pin is stale, not the comparison good).
(construct (name expect_divergence)
  (field (name difference) (type string) (min-length 1))
  (field (name at_step) (type integer)))

(construct (name step)
  (field (name n) (type integer))
  (field (name insn) (type string) (min-length 1))
  (field (name writes) (type form) (head writes))
  (field (name derivation) (type string) (min-length 1))
  (field (name source) (type string) (min-length 1))
  (field (name limit) (type string) (optional yes)))

(construct (name writes)
  (field (name write) (type form) (head write) (repeat yes)))

(construct (name write)
  (field (name reg) (type string) (min-length 1))
  (field (name value) (type string) (min-length 1)))
