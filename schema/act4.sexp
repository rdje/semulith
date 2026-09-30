;; act4.sexp — the schema for an ACT4 campaign record (profiles/<unit>/act4.sexp).
;;
;; `P2-SCALAR.5` strand 2 (`G-REGRESSION`): the pinned riscv-arch-test RV64I suite, run as
;; EXTERNAL TESTS with Sail-derived expectations (`EVD-04` — never a second independent
;; semantics; the shared ancestry is the recorded `references.sexp` independence row). The
;; dossier is a RECORDED experiment, not a regenerated artifact: its inputs (the sparse
;; clone, the reference binaries) are untracked by design, so the commit gate checks shape
;; and internal consistency — never re-execution. One `test` row per generated test file:
;; the measured signature-slot count, the three HTIF verdicts, and the two comparison
;; verdicts (semulith vs the Sail-derived signature; spike vs sail — the control pair).
;; The `run` block's counts are RE-DERIVED from the rows by RECORD-SCHEMA rule 13 — a
;; carried count that disagrees with its own rows fails by name.

(schema (id "act4"))

(construct (name act4-campaign)
  (field (name profile) (type string) (min-length 1))
  (field (name suite) (type form) (head suite))
  (field (name toolchain) (type form) (head toolchain))
  (field (name run) (type form) (head run))
  (field (name evidence_note) (type string) (min-length 1))
  (field (name test) (type form) (head test) (repeat yes) (min 1)))

(construct (name suite)
  (field (name origin) (type string) (min-length 1))
  (field (name branch) (type string) (min-length 1))
  (field (name pin) (type string) (min-length 40))
  (field (name sparse_paths) (type string) (repeat yes) (min 1)))

(construct (name toolchain)
  (field (name compiler) (type string) (min-length 1))
  (field (name linker) (type string) (min-length 1)))

(construct (name run)
  (field (name date) (type string) (min-length 1))
  (field (name tests) (type integer))
  (field (name signature_slots) (type integer))
  (field (name verdicts) (type string) (min-length 1)))

(construct (name test)
  (field (name file) (type string) (min-length 1) (pattern "^I-[a-z0-9]+-[0-9]+\\.S$"))
  (field (name signature_slots) (type integer))
  (field (name verdict_semulith) (type string) (min-length 1))
  (field (name verdict_sail) (type string) (min-length 1))
  (field (name verdict_spike) (type string) (min-length 1))
  (field (name signature) (type string) (min-length 1))
  (field (name control) (type string) (min-length 1)))
