; issue.sexp — the single owner of this issue's identity and state.
;
; ⛔ EVERY INDEX IS DERIVED FROM THIS FILE. The vendor index, the top-level index and the metadata
; table in REPORT.md are mirrors, checked by the consumer's UPSTREAM-INDEX gate and never trusted.
; Edit the state HERE; the gate will tell you which mirrors have gone stale.
;
; ⛔ AND THIS FILE STAYS INSIDE THE SUBTREE, like everything else here. A maintainer copies this
; directory out and has the whole issue: the record, the report, the reproduction, the cases, the
; captured evidence and the candidate fix. Nothing in it points anywhere else.

(issue
  (id "LS-001")
  (project "linkedspec")
  (title "a double-quoted string containing LF is not one string")
  (component "specs/Lispish.spec lines 69 and 71")
  (severity high)
  (state draft)
  (blocks "SOT-FORMAT.9")

  (affects
    (pin "linkedspec" "ad290bdb427bc19a5af81de0f0b07e119c8999ff")
    (pin "rgx" "8763a0e6bea97879f027237439d57725f83ead23")
    (pin "pgen" "db6f8c6836fefa5a57b1337d3ffbf6f15774089f")
    (pin "pcre2" "f454e231fe5006dd7ff8f4693fd2b8eb94333429"))

  (fix
    (available yes)
    (validated-by-us yes)
    (patch "fix/dotall.patch")
    (evidence "8 of 8 reproduction cases pass; all 5 of our tracked .sexp files then agree"))

  (history
    (event (date "2026-09-20") (state draft)
           (note "found while integrating the Rust backend; root cause located by refuting two
                  wrong hypotheses first, reproduction reduced to 8 files of a few bytes each"))))
