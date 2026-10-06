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
;;
;; `P5-BOARD.2` (`2026-10-02`): `entry` and `instructions` are OPTIONAL (the `xlen`
;; precedent) — case sifive-uart-lab-v0: a device register-read-expectation (a reset or
;; stimulus expectation) has no program entry and no instruction count. `step.insn`
;; carries the stimulus name, and the observed registers travel as data in
;; `writes`/`never_written`, exactly as before.
;;
;; `P4-SYSTEM.3` (`2026-10-04`): `fetches` is OPTIONAL — the corpus's no-extraneous-fetch
;; witness is "exactly one fetch request per executed step", and a step whose FETCH
;; faults in the page-table walk (an instruction page fault) issues walk accesses but
;; NO fetch request, so such a guest declares its expected fetch count explicitly
;; rather than letting the witness read a real architectural event as extraneous.

(schema (id "expectations"))

(construct (name expectations)
  (field (name program) (type string) (min-length 1))
  (field (name entry) (type string) (min-length 1) (optional yes))
  (field (name instructions) (type integer) (optional yes))
  (field (name fetches) (type integer) (optional yes))
  (field (name never_written) (type string) (repeat yes))
  (field (name refuse) (type form) (head refuse) (repeat yes) (optional yes))
  (field (name cross_model) (type symbol) (values true) (values false) (optional yes))
  (field (name expect_divergence) (type form) (head expect_divergence) (optional yes))
  (field (name step) (type form) (head step) (repeat yes) (min 1)))

;; `refuse` (P4-SYSTEM.8 slice c) is TYPED FAULT INJECTION, environment-shaped: the corpus
;; environment answers every boundary request of `kind` whose bytes intersect
;; [base, base + size) with an access fault — a region readable but not writable (`store`),
;; not readable (`load`), whose page-table entries cannot be read (`walk`), or not
;; fetchable (`fetch`). It is part of the guest's EXPERIMENT, declared beside its expected
;; observations, and honoured alike by the runner and the spec-side authoring model — never a
;; hook inside an instruction: "a fault injected after the Nth suboperation" is the Nth
;; suboperation's own access refused (an AMO's store after its load completed).
(construct (name refuse)
  (field (name kind) (type symbol) (values fetch) (values load) (values store) (values walk))
  (field (name base) (type string) (min-length 1))
  (field (name size) (type string) (min-length 1)))

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
