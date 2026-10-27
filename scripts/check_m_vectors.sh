#!/usr/bin/env bash
# scripts/check_m_vectors.sh — shim (XTASK.6 slice 6s): the M-VECTORS doctrine's driver is now
# `cargo xtask check-m-vectors [--self-test]` (xtask/src/check_m_vectors.rs). The M-extension vector table
# (crates/semulith-verify/src/m_vectors/vectors.txt) must be the generator's output and the generator's reference must
# obey the chapter — judged by the driver's inline Python judge, run verbatim through `python3 -` (not ported), on an
# operand set the table does not use; the controls run over copies of the generator. The same verdict lines and exit
# statuses (0 ok, 1 a finding or drift, 2 refused). Kept because the project doctrine slot registers this path; a unit
# test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-m-vectors "$@"
