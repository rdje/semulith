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
  (state verified)
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
    (upstream-fix "8259719f8198a1280c8d91d07a9797ef39e036a8")
    (evidence "8 of 8 reproduction cases pass at the adopted pin; all 5 of our tracked .sexp
               files agree node-for-node; the fix shipped upstream is the reported (?s) form
               verbatim"))

  (history
    (event (date "2026-09-20") (state draft)
           (note "found while integrating the Rust backend; root cause located by refuting two
                  wrong hypotheses first, reproduction reduced to 8 files of a few bytes each"))
    (event (date "2026-09-26") (state verified)
           (verified-against "a8d34c84595d46c24cd1820d5fc0414261706412")
           (repro "evidence/verified-a8d34c845.txt")
           (note "pin advanced on the director's instruction after upstream shipped the fix as
                  8259719f8; our self-contained repro.sh re-ran against the new binary and grammar:
                  8 matched / 0 differed (was 4/4); the consumer's two-reader comparison then
                  agreed on all five of its tracked .sexp files — SOT-FORMAT.9's block discharges"))))
