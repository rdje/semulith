; issue.sexp — see LS-001's copy for why this file, and not an index, owns the state.

(issue
  (id "LS-003")
  (project "linkedspec")
  (title "three first-consumer papercuts in the integration guide")
  (component "docs/linkedspec-book/src/public-api/integration-rust.md")
  (severity low)
  (state verified)
  (blocks "")

  (affects
    (pin "linkedspec" "ad290bdb427bc19a5af81de0f0b07e119c8999ff"))

  (fix
    (available yes)
    (validated-by-us yes)
    (patch "")
    (evidence "documentation observations; two of the three are our own reading failures and are
               reported because the next consumer will arrive the same way; the guide at the
               adopted pin remedies all three and each remedy was exercised during the pin update")
    (upstream-fix "BACKEND-INTEGRATION-GUIDES and CONSUMER-REPORT-DELIVERY series, shipped at a8d34c845"))

  (history
    (event (date "2026-09-20") (state draft)
           (note "each cost one failed attempt during the first integration"))
    (event (date "2026-09-26") (state verified)
           (verified-against "a8d34c84595d46c24cd1820d5fc0414261706412")
           (repro "evidence/verified-a8d34c845.txt")
           (note "guide at the new pin re-read section by section: workspace exclusion, the
                  'if you arrived directly at this section' prerequisite chain, and the local
                  storage wrapper each remedied; the pin update then followed exactly those
                  sections and every step completed — exit statuses captured in the repro
                  artifact, per the guide's own warning that a progress banner is not a result"))))
