#!/usr/bin/env bash
# scripts/check_board_gen.sh — shim (XTASK.6 slice 6v): the BOARD-GEN doctrine's driver is now
# `cargo xtask check-board-gen [--self-test]` (xtask/src/check_board_gen.rs). A board's manifest, composed catalogues,
# hardware description and map are GENERATED from the canonical definition by scripts/gen_board.py; the check regenerates
# them through the generator, spawned as this driver spawned it (not ported), and refuses the day a committed artifact
# stops byte-matching its derivation; the controls run over a scratch copy of the real definition. The same verdict
# lines and exit statuses (0 ok, 1 out of sync, 2 refused). Kept because the project doctrine slot registers this path;
# a unit test holds it to this one command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-board-gen "$@"
