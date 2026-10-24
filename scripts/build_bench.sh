#!/usr/bin/env bash
# scripts/build_bench.sh — shim (XTASK.4 slice 4a): the browser bench's wasm build is now
# `cargo xtask build-bench` (xtask/src/main.rs, `build_bench`), which builds semulith-verify's
# cdylib (LAB-BENCH.1) and copies it to the gitignored bench/semulith_verify.wasm. Kept so
# `make bench` and every documented path keep working; a unit test holds it to this one command.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask build-bench "$@"
