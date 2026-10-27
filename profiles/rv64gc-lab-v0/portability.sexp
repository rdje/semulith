;; portability.sexp — the recorded G-PORTABILITY evidence of rv64gc-lab-v0 (P4-SYSTEM.17 slice a): one
;; measurement session on one named host, frozen as data by `scripts/check_portability.sh --profile rv64gc-lab-v0
;; --record` from the run's own logs and digests. The x86-64 leg runs under Rosetta 2 translation on an arm64
;; host (decision_release-route-x86-64-leg: the CI two-host matrix carries the bare-metal leg).
;; Re-run (on any host — the legs report THAT host's capabilities):
;;   bash scripts/check_portability.sh --profile rv64gc-lab-v0

(portability
  (for-gate G-PORTABILITY)
  (unit "rv64gc-lab-v0")
  (recorded "2026-10-27")
  (recorded-by "scripts/check_portability.sh --profile rv64gc-lab-v0 --record (P4-SYSTEM.17 slice a)")
  (rederive "bash scripts/check_portability.sh --profile rv64gc-lab-v0")
  (host
    (cpu "Apple M4 Pro")
    (kernel "Darwin 27.0.0")
    (arch "arm64")
    (rustc "rustc 1.95.0 (59807616e 2026-04-14)")
    (nightly "cargo 1.100.0-nightly (7941be6fb 2026-09-11)")
    (miri "miri 0.1.0 (809936eac6 2026-09-12)"))
  (verdict "passed")
  (legs
    (leg (id "native-arm64") (verdict "green")
         (evidence "cargo test --all — the commit gate's own run: 503 suites passed, 0 failed")
         (note "the offline differential against the pinned expectations; runs on every commit"))
    (leg (id "fixture-digest-manifest") (verdict "green")
         (evidence "sha256 2e0835dd325c0834915be74b27ad8cefdfd187e4f11227fad27daf442d67f6ab over the 168 tracked guests' demo outputs")
         (note "the cross-host contract: a second host's run must reproduce this digest BYTE-IDENTICALLY — it is recomputed, never carried"))
    (leg (id "native-x86-64") (verdict "green (Rosetta translation; the manifest agrees byte-identically)")
         (evidence "cargo test --all --target x86_64-apple-darwin: 503 suites passed, 0 failed; the x86-64 manifest equals the native digest")
         (note "MANDATORY per docs/EVIDENCE_AND_GATES.md §7 — met VIA TRANSLATION (Rosetta 2) on this host; the bare-metal leg is the CI matrix's"))
    (leg (id "miri") (verdict "green")
         (evidence "cargo +nightly-2026-09-13 miri test -p semulith-core — 178 suites passed, 0 failed, interpreted")
         (note "the model's safe-Rust core; the one unsafe island (bench.rs's counting allocator) is excluded by name"))
    (leg (id "cross-endian") (verdict "green")
         (evidence "the same suites under Miri on powerpc64-unknown-linux-gnu (big-endian): 178 passed, 0 failed")
         (note "the little-endian guest semantics hold on a big-endian host"))))
