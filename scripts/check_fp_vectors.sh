#!/usr/bin/env bash
# scripts/check_fp_vectors.sh — shim (XTASK.6 slice 6ak): the FP-VECTORS doctrine's driver is now
# `cargo xtask check-fp-vectors [--self-test]` (xtask/src/check_fp_vectors.rs). The floating-point model layer's unit
# vectors and fixtures must be `scripts/gen_fp_vectors.py`'s output (DRIFT otherwise), and the spec-side reference
# `scripts/specfp.py` must agree with the host's hardware IEEE in RNE — the generator spawned as before, the hardware
# cross-check's inline Python run verbatim through `python3 -` (not ported); the controls apply the script's edits to
# scratch copies. The same verdict lines and exit statuses (0 ok, 1 a finding, 2 refused). Kept because the project
# doctrine slot registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts
# the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-fp-vectors "$@"
