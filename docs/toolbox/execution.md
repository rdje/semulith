# Toolbox — execution

Execution and evidence — the engines, the guests, coverage, references, bench, materials. Part
of the partitioned toolbox: the doctrine and the bounded index are `TOOLBOX.md`; every
diagnostic is tracked so a number it produced can be re-derived (`LIVE-CONTAINMENT.3`).

| Tool | Answers | How to invoke |
| --- | --- | --- |
| `scripts/gate_report.py` | what does the gate actually say right now, and why is it not `passed`? | `scripts/gate_report.py <profile> [--gate G0|G1] [--stdout]` |
| `scripts/compare_platforms.py` | what platform does each reference actually advertise, and where does it differ from the profile and from the other model? | `scripts/compare_platforms.py` |
| `scripts/materials.py` | which primary sources does this project rely on, and is each one present and the document it claims to be? | `scripts/materials.py [--list \| --resolve <id> \| --fetch \| --verify]` |
| `scripts/check_wasm_build.sh` | does the workspace still build for the browser target — or did a host-only API slip into the engine? | `scripts/check_wasm_build.sh [--self-test]` (PORT-WEB doctrine; fired RED against a unix-only import before registration) |
| `scripts/check_exercise_coverage.sh` | which declared forms has no guest EXECUTED — coverage with its denominator? | `scripts/check_exercise_coverage.sh [--self-test]` (EXERCISE-COVERAGE) |
| `scripts/check_interaction_matrix.sh` | is the declared interaction matrix complete and resolved — every derived cell declared, every disposition resolving, no orphan guest, every named difference recorded? | `scripts/check_interaction_matrix.sh [--self-test]` (INTERACTION-MATRIX; fired RED against the real corpus before registration, `P2-SCALAR.4`) |
| `semulith run <elf>` | what does the definitional interpreter observe on a guest — the same `(pc, word, writes, trap)` vocabulary the references reduce to? | `cargo run -p semulith-cli -- run <elf> [--steps N]` (`P1-LAB.8`) |
| `semulith bench` | what does each execution mix cost in each mode — and how noisy is that number on THIS host? (RUST-04: the noise table exists so a future threshold can be set from it; none is set) | `cargo run --release -p semulith-cli -- bench [--iterations N] [--reps R]` (`P1-LAB.11`; also checks RUST-02 mode agreement as it measures, exit 1 on disagreement) |
| `semulith demo` | what does a tracked guest do under the real or a mutated model — and where does the differential catch it? | `cargo run -p semulith-cli -- demo --guest=NAME [--mutate=NAME] [--json]` (`LAB-BENCH.1`; exit 0 clean, 1 caught mutant, 2 usage) |
| `scripts/build_bench.sh` | is the browser bench's wasm module the current engine, built from the verify cdylib? | `make bench` (`LAB-BENCH.1`; writes the gitignored `bench/semulith_verify.wasm`) |
| `scripts/smoke_bench.js` | does the bench page's engine, over its wire-exact wasm exports, meet the pinned expectations and catch each exposed mutant where the `.9` suite pins it? | `make smoke-bench` (after `make bench`; node) |
| `scripts/run_semulith_smoke.py` | does semulith agree with the pinned references and the specification-derived expectations, live? | `python3 scripts/run_semulith_smoke.py` — NOT a commit gate; needs `target/refs/` |
| `scripts/fetch_references.sh` | is the reference model I am comparing against the one the dossier pins, and is it still configured to this profile? | `scripts/fetch_references.sh [--verify-only] [<profile>]` |
| `scripts/run_smoke.py` | does the matched-profile evidence path actually work — do two models agree with each other, with the specification, and with themselves on a re-run? | `scripts/run_smoke.py` |
| `scripts/compare_traces.py` | where do two reference models FIRST disagree, in aligned steps? | `scripts/compare_traces.py <sail-trace> <spike-log> <entry>` |
| `scripts/fetch_sources.sh` | is the specification artifact I am reading the one the locators were written against? | `scripts/fetch_sources.sh [--verify-only] <profile>` |
| `make check` | does the workspace build, lint clean at `-D warnings`, and pass its tests? | `make check` |
