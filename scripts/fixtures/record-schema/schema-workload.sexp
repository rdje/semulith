;; workload.sexp — the schema for a workload campaign record (profiles/<unit>/workload.sexp).
;;
;; `P4-SYSTEM.15` slice f (`G-REGRESSION`'s `workload` kind): compiled, self-checking, freestanding C
;; workloads built by the pinned toolchain on the laboratory's HTIF and signature conventions and run
;; three-way as the ACT4 external campaign is — semulith judged against the Sail-derived signature
;; (`EVD-04`), spike against sail as the control pair. The record is a RECORDED experiment, not a
;; regenerated artifact: the reference binaries are untracked by design, so the commit gate checks shape
;; and internal consistency — never re-execution. One `workload` row per tracked source (`wl-<name>.c`):
;; the ELF's instruction census (instructions, compressed, the extension families present — the
;; compiler's fact, not the source's), the Sail step count, the measured signature-slot count, the three
;; HTIF verdicts and the two comparison verdicts. The `run` block's counts are RE-DERIVED from the rows by
;; RECORD-SCHEMA rule 15 — a carried count that disagrees with its own rows fails by name.

(schema (id "workload"))

(construct (name workload-campaign)
  (field (name profile) (type string) (min-length 1))
  (field (name toolchain) (type form) (head toolchain))
  (field (name run) (type form) (head run))
  (field (name evidence_note) (type string) (min-length 1))
  (field (name workload) (type form) (head workload) (repeat yes) (min 1)))

(construct (name toolchain)
  (field (name compiler) (type string) (min-length 1))
  (field (name linker) (type string) (min-length 1)))

(construct (name run)
  (field (name date) (type string) (min-length 1))
  (field (name workloads) (type integer))
  (field (name signature_slots) (type integer))
  (field (name verdicts) (type string) (min-length 1)))

(construct (name workload)
  (field (name file) (type string) (pattern "^wl-[a-z]+\\.c\\Z"))
  (field (name instructions) (type integer))
  (field (name compressed) (type integer))
  (field (name families) (type string) (min-length 1))
  (field (name sail_steps) (type integer))
  (field (name signature_slots) (type integer))
  (field (name verdict_semulith) (type string) (min-length 1))
  (field (name verdict_sail) (type string) (min-length 1))
  (field (name verdict_spike) (type string) (min-length 1))
  (field (name signature) (type string) (min-length 1))
  (field (name control) (type string) (min-length 1)))
