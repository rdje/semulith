#!/usr/bin/env bash
# scripts/build_bench.sh — build the browser bench's wasm module and copy it next to the page.
# LAB-BENCH.1: the module is semulith-verify's cdylib (std-only extern "C" surface in
# src/wasm.rs); the copy under bench/ is gitignored, so this script is the one way it appears.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

cargo build --release -p semulith-verify --target wasm32-unknown-unknown
cp target/wasm32-unknown-unknown/release/semulith_verify.wasm bench/semulith_verify.wasm
echo "bench: bench/semulith_verify.wasm ($(wc -c < bench/semulith_verify.wasm | tr -d ' ') bytes)"
echo "bench: serve with 'python3 -m http.server -d bench 8000' and open http://localhost:8000/"
