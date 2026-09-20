; issue.sexp — see LS-001's copy for why this file, and not an index, owns the state.

(issue
  (id "LS-002")
  (project "linkedspec")
  (title "quoted and bare atoms are indistinguishable")
  (component "specs/Lispish.spec parent rules, as documented")
  (severity medium)
  (state draft)
  (blocks "")

  (affects
    (pin "linkedspec" "ad290bdb427bc19a5af81de0f0b07e119c8999ff"))

  (fix
    (available no)
    (validated-by-us no)
    (patch "")
    (evidence "no patch proposed: this is a design question for the upstream, not a defect in
               what they document"))

  (history
    (event (date "2026-09-20") (state draft)
           (note "documented behaviour; raised for its consequence on a format that is written as
                  well as read, which the documentation does not draw out"))))
