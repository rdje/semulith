;; The recorded P1 performance baseline (`P1-LAB.11`, RUST-04) — one measurement session on
;; one named host, frozen as data. This is NOT a regression threshold: RUST-04 requires the
;; noise to be characterized before any threshold exists, and this record is that
;; characterization. A future threshold is set FROM these spreads, never ahead of them.
;; Re-derive (on any host — the numbers will be that host's, not these):
;;   cargo run --release -p semulith-cli -- bench
;; Consumed by `scripts/gate_report.py --gate G1` (criterion 5); plain atoms and strings so
;; every tracked reader (`scripts/sexp.py`, Lispish, SExprDocumentV1) parses it.
(baseline
  (for-gate G1)
  (recorded "2026-09-28")
  (recorded-by "semulith bench (P1-LAB.11)")
  (rederive "cargo run --release -p semulith-cli -- bench")
  (host
    (cpu "Apple M4 Pro")
    (kernel "Darwin 27.0.0")
    (rustc "rustc 1.95.0 (59807616e 2026-04-14)"))
  (config (iterations 10000) (warmup 2) (reps 12))
  ;; ns-per-step/min/max are nanoseconds per executed step (medians over the 12 timed
  ;; repetitions); spread-ppm is (max-min)/median in parts per million; allocs and bytes
  ;; per step come from the process-wide counting allocator.
  (mix
    (name arithmetic)
    (steps 280003)
    (census (fetches 280003) (loads 0) (stores 0) (faults 0))
    (cell (mode untraced) (ns-per-step "52.1") (min "51.5") (max "52.4") (spread-ppm 17000) (allocs-per-step "1.00") (bytes-per-step "126.9"))
    (cell (mode instrumented) (ns-per-step "69.6") (min "69.1") (max "70.3") (spread-ppm 16600) (allocs-per-step "1.19") (bytes-per-step "379.0"))
    (cell (mode instrumented-dyn) (ns-per-step "69.6") (min "68.8") (max "71.3") (spread-ppm 36200) (allocs-per-step "1.19") (bytes-per-step "379.0"))
    (cell (mode diagnostic) (ns-per-step "73.4") (min "72.1") (max "74.1") (spread-ppm 26700) (allocs-per-step "1.19") (bytes-per-step "648.6"))
    (static-dyn-ratio "0.999"))
  (mix
    (name control)
    (steps 95004)
    (census (fetches 95004) (loads 0) (stores 0) (faults 0))
    (cell (mode untraced) (ns-per-step "47.2") (min "45.8") (max "48.0") (spread-ppm 46200) (allocs-per-step "1.00") (bytes-per-step "126.3"))
    (cell (mode instrumented) (ns-per-step "65.4") (min "63.0") (max "66.3") (spread-ppm 50800) (allocs-per-step "1.42") (bytes-per-step "329.9"))
    (cell (mode instrumented-dyn) (ns-per-step "65.5") (min "64.2") (max "68.1") (spread-ppm 59600) (allocs-per-step "1.42") (bytes-per-step "329.9"))
    (cell (mode diagnostic) (ns-per-step "70.1") (min "67.6") (max "147.0") (spread-ppm 1133900) (allocs-per-step "1.42") (bytes-per-step "528.5"))
    (static-dyn-ratio "1.002"))
  (mix
    (name memory)
    (steps 170006)
    (census (fetches 170006) (loads 70000) (stores 40000) (faults 0))
    (cell (mode untraced) (ns-per-step "54.1") (min "52.8") (max "55.1") (spread-ppm 41100) (allocs-per-step "1.00") (bytes-per-step "137.4"))
    (cell (mode instrumented) (ns-per-step "71.0") (min "68.7") (max "73.1") (spread-ppm 61300) (allocs-per-step "1.23") (bytes-per-step "349.6"))
    (cell (mode instrumented-dyn) (ns-per-step "70.9") (min "69.5") (max "74.1") (spread-ppm 65300) (allocs-per-step "1.23") (bytes-per-step "349.6"))
    (cell (mode diagnostic) (ns-per-step "76.9") (min "75.8") (max "78.8") (spread-ppm 38800) (allocs-per-step "1.23") (bytes-per-step "793.7"))
    (static-dyn-ratio "0.998"))
  (mix
    (name fault)
    (steps 50010)
    (census (fetches 50010) (loads 10000) (stores 0) (faults 10000))
    (cell (mode untraced) (ns-per-step "50.9") (min "50.3") (max "53.4") (spread-ppm 60100) (allocs-per-step "1.00") (bytes-per-step "140.8"))
    (cell (mode instrumented) (ns-per-step "69.4") (min "66.9") (max "71.3") (spread-ppm 63200) (allocs-per-step "1.20") (bytes-per-step "321.3"))
    (cell (mode instrumented-dyn) (ns-per-step "67.5") (min "65.4") (max "70.4") (spread-ppm 74000) (allocs-per-step "1.20") (bytes-per-step "321.3"))
    (cell (mode diagnostic) (ns-per-step "71.0") (min "69.6") (max "72.8") (spread-ppm 45500) (allocs-per-step "1.20") (bytes-per-step "510.0"))
    (static-dyn-ratio "0.974"))
  (agreement "RUST-02 held: on every mix all modes agreed on step count, stop classification, final architectural state and the crossing census, and every recorded observation stream was identical")
  (thresholds none)
  (noise-note "per-cell spread 1.7-7.4%; one 113% scheduler outlier on a millisecond-scale cell (control/diagnostic max) — the honest spread a future threshold must be set from"))
