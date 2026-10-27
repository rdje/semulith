#!/usr/bin/env bash
# scripts/check_definition_gen.sh — shim (XTASK.6 slice 6an): the DEF-GEN doctrine's driver is now
# `cargo xtask check-definition-gen [--self-test]` (xtask/src/check_definition_gen.rs). The generated definition modules
# (`crates/semulith-core/src/definition.rs`, `definition_rv64gc.rs`) must still be `scripts/gen_definition.py`'s output of
# the canonical definition (DRIFT otherwise); the generator, the C-expansion and C-engine probes and the controls' inline
# Python edits are spawned as before (not ported); the controls run over scratch copies of the real fragments and staged
# rv64gc compositions. The same verdict lines and exit statuses (0 ok, 1 drift, 2 refused). Kept because the project
# doctrine slot registers this path; a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts
# the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-definition-gen "$@"
