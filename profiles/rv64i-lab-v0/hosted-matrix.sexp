;; hosted-matrix.sexp — the recorded hosted run of rv64i-lab-v0's portability matrix: G-PORTABILITY's native
;; x86-64 and arm64 legs, on the service's own hardware. Frozen from one run's description, job logs and
;; artifacts by `scripts/hosted_matrix.py --record`, never typed. The service keeps those files for a
;; limited time; this record is what stays. `gate.sexp` names it with what it covers.
;; Re-derive, while the service still holds the run:
;;   python3 -B scripts/hosted_matrix.py --fetch 42418631491 --out target/hosted-matrix/42418631491
;;   python3 -B scripts/hosted_matrix.py --verify target/hosted-matrix/42418631491 --profile rv64i-lab-v0

(hosted-matrix
  (for-gate G-PORTABILITY)
  (unit "rv64i-lab-v0")
  (recorded "2026-11-10")
  (recorded-by "scripts/hosted_matrix.py --record DIR --profile rv64i-lab-v0")
  (run (id "42418631491") (workflow "portability") (event "push") (head "12347bc57bab1a1fc149606f9e93fc93b76f2a8b") (completed "2026-11-07T23:40:44Z"))
  (verdict "passed")
  (hosts
    (host (runner "macos-latest") (arch "arm64") (image "macos-26-arm64") (rustc "rustc 1.99.1 (58cf8f9c3 2026-10-13)")
          (tests "519 passed, 0 failed, in 14 suites")
          (manifest "sha256 3fbc498e29da169243f0ed0f018d539ce409f55027824a889f4ea3f178aa33f9 over 49 guests"))
    (host (runner "ubuntu-latest") (arch "x86_64") (image "ubuntu-24.04") (rustc "rustc 1.99.1 (58cf8f9c3 2026-10-13)")
          (tests "519 passed, 0 failed, in 14 suites")
          (manifest "sha256 3fbc498e29da169243f0ed0f018d539ce409f55027824a889f4ea3f178aa33f9 over 49 guests")))
  (agreement "the two hosts' manifests are byte-identical, and equal the digest profiles/rv64i-lab-v0/portability.sexp records over the same guests")
  (miri (verdict "green") (tests "178 passed, 0 failed"))
  (cross-endian (verdict "green") (tests "178 passed, 0 failed")))
