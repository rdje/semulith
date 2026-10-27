#!/usr/bin/env bash
# scripts/check_board_verdict.sh — shim (XTASK.6 slice 6u): the BOARD-VERDICT doctrine's driver is now
# `cargo xtask check-board-verdict [--self-test]` (xtask/src/check_board_verdict.rs). P5-BOARD.4: a board's composition
# verdict is DECIDED, not narrated — for every tracked profiles/*/board.sexp, scripts/board_verdict.py (spawned as this
# driver spawned it, not ported) decides the three legs over the board's own data and REJECTS by name; the controls run
# over scratch copies of the real board. The same verdict lines and exit statuses (0 ok, 1 the composition does not
# hold, 2 refused). Kept because the project doctrine slot registers this path; a unit test holds it to this one
# command, and the DERIVED-COUNTS arm total counts the module's arms through it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec cargo xtask check-board-verdict "$@"
