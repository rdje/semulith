#!/usr/bin/env bash
# scripts/check_board_gen.sh — BOARD-GEN (project doctrine).
#
# `P5-BOARD.3`: every map a board carries is GENERATED from its canonical definition
# (`profiles/<board>/board.sexp`) by `scripts/gen_board.py` — the composition manifest,
# the four composed catalogues (materialized by `compose_units.compose_resolved`, the one
# code path the verdicts consume), the hardware description, and the human-readable map.
# This check re-derives all seven per board and refuses the day any stops byte-matching
# the tracked file — the freshness proof `compose_units.py` defers to the first tracked
# board (OWN-03/OWN-05: changed by regeneration, never by editing; no handwritten
# duplicate map anywhere).
#
# ⭐ WHAT THIS ACTUALLY PROTECTS: not tidiness — the DERIVATION. The board definition is
# the authority; the manifest, the composed catalogues, the hardware description and the
# map are its mirrors. A hand-edited wiring row or a stale composed catalogue is how the
# definition and its downstream quietly become two facts (doctrine/fact_ownership.tsv
# names the pairs).
#
# ⚠️ HONEST LIMIT: it proves the artifacts are still the function of board.sexp and the
# parts' dossiers. It says nothing about whether the definition is TRUE — the pins have
# their own gates (RECORD-SCHEMA, GATE-REPORT, the materials machinery).
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "BOARD-GEN: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

BOARD="profiles/netboard-lab-v0"

SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): a missing `;` before
  # an arm call swallows it silently; the guard makes that a loud failure.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'BOARD-GEN self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring; empty = expect no output>
    argc 5 "$#" arm || return
    if [ -z "$5" ]; then
      if [ "$2" = "$3" ] && [ -z "$4" ]; then
        pass=$((pass+1)); return
      fi
      fail=$((fail+1))
      printf 'BOARD-GEN self-test MISS: %s — expected rc=%s and no output, got rc=%s\n%s\n' \
        "$1" "$3" "$2" "$4" >&2
      return
    fi
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'BOARD-GEN self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  # A scratch copy of the real board definition; the generator's part resolution falls
  # back to the repo's units, so the copy composes the real parts.
  mkdir -p "$t/board"
  cp "$BOARD/board.sexp" "$t/board/board.sexp"

  # GREEN: the generator emits all seven artifacts from the real definition.
  out="$(python3 scripts/gen_board.py --board-dir "$t/board" --out-dir "$t/out" 2>&1)"; rc=$?
  arm "GREEN the generator emits the artifacts from the real definition" "$rc" 0 "$out" "7 artifact(s)"

  # GREEN: determinism — a second derivation is byte-identical.
  python3 scripts/gen_board.py --board-dir "$t/board" --out-dir "$t/out2" >/dev/null 2>&1
  if diff -r "$t/out" "$t/out2" >/dev/null 2>&1; then
    out=""; rc=0
  else
    out="nondeterministic"; rc=1
  fi
  arm "GREEN two derivations are byte-identical" "$rc" 0 "$out" ""

  # GREEN: a faithful generation is judged in sync.
  out="$(python3 scripts/gen_board.py --check --board-dir "$t/board" --out-dir "$t/out" 2>&1)"; rc=$?
  arm "GREEN a faithful generation is judged in sync" "$rc" 0 "$out" "byte-exact"

  # RED: a hand-edited hardware description is detected and named.
  cp -r "$t/out" "$t/d1"; printf '\n;; hand edit\n' >> "$t/d1/hardware.sexp"
  out="$(python3 scripts/gen_board.py --check --board-dir "$t/board" --out-dir "$t/d1" 2>&1)"; rc=$?
  arm "RED a hand-edited hardware.sexp is refused, naming DRIFT" "$rc" 1 "$out" "hardware.sexp: DRIFT"

  # RED: a hand-edited composed catalogue is detected and named.
  cp -r "$t/out" "$t/d2"; printf '\n;; hand edit\n' >> "$t/d2/requirements.sexp"
  out="$(python3 scripts/gen_board.py --check --board-dir "$t/board" --out-dir "$t/d2" 2>&1)"; rc=$?
  arm "RED a hand-edited composed catalogue is refused, naming DRIFT" "$rc" 1 "$out" "requirements.sexp: DRIFT"

  # RED: a hand-edited manifest is detected and named.
  cp -r "$t/out" "$t/d3"; printf '\n;; hand edit\n' >> "$t/d3/composition.sexp"
  out="$(python3 scripts/gen_board.py --check --board-dir "$t/board" --out-dir "$t/d3" 2>&1)"; rc=$?
  arm "RED a hand-edited manifest is refused, naming DRIFT" "$rc" 1 "$out" "composition.sexp: DRIFT"

  # RED: a board.sexp edit against stale artifacts is drift, named — the definition moved,
  # the map did not.
  cp "$t/board/board.sexp" "$t/board-moved.sexp"
  python3 - "$t/board/board.sexp" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
p.write_text(p.read_text().replace('(base "0x1002_0000")', '(base "0x1002_1000")'))
PY
  out="$(python3 scripts/gen_board.py --check --board-dir "$t/board" --out-dir "$t/out" 2>&1)"; rc=$?
  arm "RED a moved definition against stale artifacts is refused, naming DRIFT" "$rc" 1 "$out" "DRIFT"
  cp "$t/board-moved.sexp" "$t/board/board.sexp"

  # RED: an overlapping region is refused by name, at generation, before any artifact.
  mkdir -p "$t/overlap"; cp "$t/board/board.sexp" "$t/overlap/board.sexp"
  python3 - "$t/overlap/board.sexp" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
p.write_text(p.read_text().replace('(base "0x1002_0000")', '(base "0x1001_0800")'))
PY
  out="$(python3 scripts/gen_board.py --board-dir "$t/overlap" --out-dir "$t/ovo" 2>&1)"; rc=$?
  arm "RED an overlapping region is refused, naming both regions" "$rc" 2 "$out" "overlap"

  # RED: an mmio region naming an undeclared device is refused by name.
  mkdir -p "$t/ghost"; cp "$t/board/board.sexp" "$t/ghost/board.sexp"
  python3 - "$t/ghost/board.sexp" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
p.write_text(p.read_text().replace('(device "eth0")', '(device "eth9")'))
PY
  out="$(python3 scripts/gen_board.py --board-dir "$t/ghost" --out-dir "$t/gho" 2>&1)"; rc=$?
  arm "RED an mmio region naming an undeclared device is refused by name" "$rc" 2 "$out" "undeclared device"

  rm -rf "$t"
  printf 'BOARD-GEN --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "BOARD-GEN: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

if ! ls profiles/*/board.sexp >/dev/null 2>&1; then
  echo "BOARD-GEN: ok (no board declares itself yet)"
  exit 0
fi

out="$(python3 scripts/gen_board.py --check 2>&1)" || {
  printf '%s\n' "$out" >&2
  printf 'BOARD-GEN: FAIL — a generated board artifact is out of sync with its canonical definition.\n' >&2
  exit 1
}
n="$(ls -d profiles/*/board.sexp 2>/dev/null | wc -l | tr -d ' ')"
printf 'BOARD-GEN: ok (%s board(s) — manifest, composed catalogues, hardware description and map all byte-exact functions of the canonical definition)\n' "$n"
exit 0
