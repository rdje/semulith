; issue.sexp — see LS-001's copy for why this file, and not an index, owns the state.

(issue
  (id "LS-002")
  (project "linkedspec")
  (title "quoted and bare atoms are indistinguishable")
  (component "specs/Lispish.spec parent rules, as documented")
  (severity medium)
  (state verified)
  (blocks "")

  (affects
    (pin "linkedspec" "ad290bdb427bc19a5af81de0f0b07e119c8999ff"))

  (fix
    (available yes)
    (validated-by-us yes)
    (patch "")
    (upstream-fix "77d7b3db1 (kind-strict document grammar) and df845ce61 (native file adapter), shipped at a8d34c845")
    (evidence "the document grammar returns tagged kinds - number, string, symbol - so a
               consumer can round-trip the source token kind; verified on this subtree's own
               four cases and on the consumer's whole tracked corpus"))

  (history
    (event (date "2026-09-20") (state draft)
           (note "documented behaviour; raised for its consequence on a format that is written as
                  well as read, which the documentation does not draw out"))
    (event (date "2026-09-26") (state acknowledged)
           (note "upstream took ownership: the fix commit for LS-001 (8259719f8) records 'LS-002
                  and related kind/strict requirements remain .83.1 owned' — acknowledged by
                  name, scheduled in their own task system"))
    (event (date "2026-09-26") (state verified)
           (verified-against "a8d34c84595d46c24cd1820d5fc0414261706412")
           (repro "evidence/verified-a8d34c845.txt")
           (note "upstream confirmed the kind-strict grammar (77d7b3db1) and the native adapter
                  (df845ce61) are ancestors of the published pin, verified by merge-base here;
                  re-running this subtree's four cases through sexpr_file with
                  SExprDocumentV1.spec - upstream's prescribed instrument - returns distinct
                  kinds for every quoted/bare pair; the consumer's whole corpus additionally
                  agrees with its canonical reader through the document layer with zero
                  classified residue"))))
