;; The recorded G-PORTABILITY evidence (`P2-SCALAR.8`; re-measured `2026-09-30` at
;; `P2-SCALAR.9` slice b) — one measurement session on one named host, frozen as data.
;; The verdict is `passed`: all four legs green — the x86-64 leg ran under Rosetta 2
;; translation (the director's route, decision_release-route-x86-64-leg: the CI two-host
;; matrix is the permanent home and carries the BARE-METAL x86-64 leg at the next
;; approved push; Rosetta is the time-bounded local bridge — Apple phases it out fall
;; 2027, and nothing may be built on it beyond the bridge).
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
  (verdict "passed")
  (legs
    (leg (id "native-aarch64") (verdict "green")
         (evidence "cargo test --all — the commit gate's own run: 180 verify + 65 core suites, 0 failed")
         (note "the offline differential against the pinned expectations; runs on every commit"))
    (leg (id "fixture-digest-manifest") (verdict "green")
         (evidence "sha256 0670a01b96de28f9e65837295064b825300b22d54ba6d033696f42e254c5bb52 over the 49 tracked guests' demo --json outputs (trace + census verdicts)")
         (note "the cross-host contract: a second host's run must reproduce this digest BYTE-IDENTICALLY — it is recomputed, never carried"))
    (leg (id "native-x86-64") (verdict "green")
         (evidence "measured 2026-09-30 (second measurement, after the director's Rosetta install): `cargo test --all --target x86_64-apple-darwin` green under Rosetta 2 translation, and the digest manifest agrees with the aarch64 recording BYTE-IDENTICALLY (0670a01b…5bb52). First measurement the same day, before activation: present-but-inert (binaries at /usr/libexec/rosetta/, the x86-64 cache in the cryptex, oahd off, `Bad CPU type in executable`) — the instrument's probe text records both states")
         (note "MANDATORY per docs/EVIDENCE_AND_GATES.md §7 — now met VIA TRANSLATION (Rosetta 2, time-bounded: Apple phases it out fall 2027 — the bridge, never the foundation). The BARE-METAL x86-64 leg is the CI matrix's ubuntu-latest job (decision_release-route-x86-64-leg), whose evidence lands at the next approved push; until then the translation leg is the recorded proof."))
    (leg (id "miri") (verdict "green")
         (evidence "cargo +nightly miri test -p semulith-core — 65/65 suites, interpreted")
         (note "the model's safe-Rust core; the one unsafe island (bench.rs's counting allocator, RUST-03's instrument) is excluded by name — harness instrumentation, not model"))
    (leg (id "cross-endian") (verdict "green")
         (evidence "the same 65/65 under Miri on powerpc64-unknown-linux-gnu (big-endian)")
         (note "the little-endian guest semantics (D-ENDIAN) hold on a big-endian host; provision: rustup target add --toolchain nightly powerpc64-unknown-linux-gnu"))))
