; issue.sexp — see LS-001's copy for why this file, and not an index, owns the state.

(issue
  (id "LS-003")
  (project "linkedspec")
  (title "three first-consumer papercuts in the integration guide")
  (component "docs/linkedspec-book/src/public-api/integration-rust.md")
  (severity low)
  (state draft)
  (blocks "")

  (affects
    (pin "linkedspec" "ad290bdb427bc19a5af81de0f0b07e119c8999ff"))

  (fix
    (available no)
    (validated-by-us no)
    (patch "")
    (evidence "documentation observations; two of the three are our own reading failures and are
               reported because the next consumer will arrive the same way"))

  (history
    (event (date "2026-09-20") (state draft)
           (note "each cost one failed attempt during the first integration"))))
