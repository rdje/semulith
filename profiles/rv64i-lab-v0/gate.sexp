;; gate.sexp — rv64i-lab-v0's recorded runs for the CPU-LAB report (P4-SYSTEM.19 slice a).
;; Validate with:
;;   python3 scripts/check_sexp_schema.py profiles/rv64i-lab-v0/gate.sexp schema/gate.sexp
;; Read by scripts/gate_report.py --gate GC, which holds each row to what it covers with the verifier the CPU-SYSTEM
;; report uses: a recorded run stands for the tree only over the paths it was measured on, and once one moves the row
;; is no evidence until the run is repeated (decision_recorded-evidence-states-what-it-covers.md). Each row's covers
;; are the tree's digests at the measurement, as scripts/gate_report.py --covers prints them.

(gate (id "CPU-LAB") (profile "rv64i-lab-v0")
  (statement "The scalar unit's recorded runs: the external campaign and the portability legs. The other CPU-LAB axes are computed from the dossier by the report itself."))

;; The ACT4 campaign, run again 2026-11-10 (P4-SYSTEM.19): its 2026-09-30 record, measured at commit 379a9dd2, read as no
;; evidence here once that commit's covers were stated, because the engine had moved since.
(evidence (axis G-REGRESSION) (kind external) (record "profiles/rv64i-lab-v0/act4.sexp")
  (covers (path "crates/semulith-core/src") (sha256 "10aba3782c29c3a63eb1ef156bcbab67e33d2757e0b089653d30b33630b3f359"))
  (covers (path "definitions") (sha256 "bb41ed1e87971950a5a83991981edfd88c7108dba39007f5f330bbbe4892c16a"))
  (covers (path "profiles/rv64i-lab-v0/act4") (sha256 "12e92ada9952ef2a80eea2165acf361c0859753c50ec5113abfed63bdccde4b6"))
  (statement "The pinned riscv-arch-test RV64I suite, 51 test files built with the laboratory's DUT pieces and run on this unit's model, every signature equal to the Sail-derived one: one semantics answering twice, never a second independent semantics (EVD-04)."))
(evidence (axis G-PORTABILITY) (kind aarch64) (record "profiles/rv64i-lab-v0/portability.sexp")
  (covers (path "crates/semulith-core/src") (sha256 "10aba3782c29c3a63eb1ef156bcbab67e33d2757e0b089653d30b33630b3f359"))
  (covers (path "definitions") (sha256 "bb41ed1e87971950a5a83991981edfd88c7108dba39007f5f330bbbe4892c16a"))
  (covers (path "crates/semulith-verify/src/guests.rs") (sha256 "cfb4ec324cf73933ef2ab16b73e89a1cb64e404b185f3688fd5e1674b4a64f8a"))
  (statement "P4-SYSTEM.19 slice a: the native leg on this host (cargo test --all) and the fixture digest manifest over the unit's guests, frozen from the run's own logs by scripts/check_portability.sh --profile rv64i-lab-v0 --record."))
(evidence (axis G-PORTABILITY) (kind x86-64) (record "profiles/rv64i-lab-v0/portability.sexp")
  (covers (path "crates/semulith-core/src") (sha256 "10aba3782c29c3a63eb1ef156bcbab67e33d2757e0b089653d30b33630b3f359"))
  (covers (path "definitions") (sha256 "bb41ed1e87971950a5a83991981edfd88c7108dba39007f5f330bbbe4892c16a"))
  (covers (path "crates/semulith-verify/src/guests.rs") (sha256 "cfb4ec324cf73933ef2ab16b73e89a1cb64e404b185f3688fd5e1674b4a64f8a"))
  (statement "P4-SYSTEM.19 slice a: the same suites and manifest under x86-64 by Rosetta 2 translation on this host (the native x86-64 leg is the hosted run's, the next row)."))
(evidence (axis G-PORTABILITY) (kind x86-64) (record "profiles/rv64i-lab-v0/hosted-matrix.sexp")
  (covers (path "crates/semulith-core/src") (sha256 "10aba3782c29c3a63eb1ef156bcbab67e33d2757e0b089653d30b33630b3f359"))
  (covers (path "definitions") (sha256 "bb41ed1e87971950a5a83991981edfd88c7108dba39007f5f330bbbe4892c16a"))
  (covers (path "crates/semulith-verify/src/guests.rs") (sha256 "cfb4ec324cf73933ef2ab16b73e89a1cb64e404b185f3688fd5e1674b4a64f8a"))
  (statement "The hosted portability run 42418631491 on commit 12347bc57bab: `cargo test --all` natively on ubuntu-latest (x86_64) and macos-latest (arm64), 519 tests passed on each, and the digest manifest over the unit's 49 guests byte-identical on both and equal to this host's record; Miri and big-endian powerpc64 green in the same run. Frozen from the run's own files by scripts/hosted_matrix.py --record."))
(evidence (axis G-PORTABILITY) (kind miri) (record "profiles/rv64i-lab-v0/portability.sexp")
  (covers (path "crates/semulith-core/src") (sha256 "10aba3782c29c3a63eb1ef156bcbab67e33d2757e0b089653d30b33630b3f359"))
  (covers (path "definitions") (sha256 "bb41ed1e87971950a5a83991981edfd88c7108dba39007f5f330bbbe4892c16a"))
  (statement "P4-SYSTEM.19 slice a: the pinned nightly's Miri over semulith-core, natively and on big-endian powerpc64 (the cross-endian leg)."))
