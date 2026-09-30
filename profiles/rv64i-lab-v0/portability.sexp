;; The recorded G-PORTABILITY evidence (`P2-SCALAR.8`) — one measurement session on one
;; named host, frozen as data. The verdict is `incomplete` BY DESIGN: the x86-64 leg is
;; mandatory (docs/EVIDENCE_AND_GATES.md §7) and its infrastructure is measured ABSENT
;; here — recorded, never waived; the profile stays experimental until the leg runs or an
;; explicit narrower host-support policy is adopted and labeled.
;; Re-run (on any host — the legs report THAT host's capabilities):
;;   bash scripts/check_portability.sh        # the full four-leg run (Miri legs ~3 min)
;; Plain atoms and strings so every tracked reader (`scripts/sexp.py`, Lispish,
;; SExprDocumentV1) parses it.

(portability
  (for-gate G-PORTABILITY)
  (recorded "2026-09-30")
  (recorded-by "scripts/check_portability.sh (P2-SCALAR.8)")
  (rederive "bash scripts/check_portability.sh")
  (host
    (cpu "Apple M4 Pro")
    (kernel "Darwin 27.0.0")
    (arch "arm64")
    (rustc "rustc 1.95.0 (59807616e 2026-04-14)")
    (nightly "cargo 1.100.0-nightly (7941be6fb 2026-09-11)")
    (miri "miri 0.1.0 (809936eac6 2026-09-12)"))
  (verdict "incomplete")
  (legs
    (leg (id "native-aarch64") (verdict "green")
         (evidence "cargo test --all — the commit gate's own run: 180 verify + 65 core suites, 0 failed")
         (note "the offline differential against the pinned expectations; runs on every commit"))
    (leg (id "fixture-digest-manifest") (verdict "green")
         (evidence "sha256 0670a01b96de28f9e65837295064b825300b22d54ba6d033696f42e254c5bb52 over the 49 tracked guests' demo --json outputs (trace + census verdicts)")
         (note "the cross-host contract: a second host's run must reproduce this digest BYTE-IDENTICALLY — it is recomputed, never carried"))
    (leg (id "native-x86-64") (verdict "unavailable")
         (evidence "measured 2026-09-30: `arch -x86_64 /usr/bin/true` -> `Bad CPU type in executable` (Rosetta PRESENT BUT INERT — binaries at /usr/libexec/rosetta/, the x86-64 dyld cache in the Rosetta cryptex, the oahd daemon not running; activation is an admin act, pending); no qemu-x86_64 user-mode runner exists (qemu-system-x86_64 is a full-system emulator; a guest-OS VM is infrastructure, not a probe)")
         (note "MANDATORY per docs/EVIDENCE_AND_GATES.md §7 — the acceptance's honest arm: the profile stays experimental until this leg runs. NOT waived. The route (decision_release-route-x86-64-leg, director 2026-09-30): the CI two-host matrix is the permanent home; Rosetta is the local bridge — Apple phases Rosetta out fall 2027, so nothing may be built on it beyond the bridge."))
    (leg (id "miri") (verdict "green")
         (evidence "cargo +nightly miri test -p semulith-core — 65/65 suites, interpreted")
         (note "the model's safe-Rust core; the one unsafe island (bench.rs's counting allocator, RUST-03's instrument) is excluded by name — harness instrumentation, not model"))
    (leg (id "cross-endian") (verdict "green")
         (evidence "the same 65/65 under Miri on powerpc64-unknown-linux-gnu (big-endian)")
         (note "the little-endian guest semantics (D-ENDIAN) hold on a big-endian host; provision: rustup target add --toolchain nightly powerpc64-unknown-linux-gnu"))))
