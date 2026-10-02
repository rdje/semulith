#!/usr/bin/env bash
# scripts/check_board_verdict.sh — BOARD-VERDICT (project doctrine).
#
# `P5-BOARD.4`: a board's composition verdict is DECIDED, not narrated
# (docs/CPU_ENVIRONMENT.md §5, ENV-02). For every tracked board
# (`profiles/*/board.sexp`), `scripts/board_verdict.py` decides three legs over the
# board's own data: every CPU environment-assumption in the composed unit is discharged
# by named guarantees (the obligation-graph half — its platform-dependent edges land on
# `OB-PLATFORM`, the laboratory guarantee); every `satisfies` edge in the board
# definition resolves to a discharged environment-assumption (the declared intent checked
# against the composed reality); and every device obligation the dossier defers to the
# composing board — marked (composition_disposition "required") — is answered by exactly
# one board decision `answers` edge, with every `answers` naming a marked obligation.
# Any leg failing REJECTS the composition by name: an unmatched assumption is a
# rejection, never a note (the leaf's acceptance).
#
# ⭐ WHAT THIS ACTUALLY PROTECTS: the re-establishment. The discharge edges alone would
# pass with a CLINT bolted on — they key on obligation ids, not on board content. This
# gate is what makes the board's declared absences and the four composition dispositions
# (the strap values, the frozen time sources, the replay link scene, the pin tie-offs)
# load-bearing: delete one, or let an edge dangle, and the verdict fails by name.
#
# ⚠️ HONEST LIMIT: it decides the composition against the DATA — the dossiers' own
# gates (RECORD-SCHEMA, EXTRACTION, the expectations) own whether the device facts are
# true, and BOARD-GEN owns the freshness of the composed catalogues this verdict reads.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "BOARD-VERDICT: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

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
    printf 'BOARD-VERDICT self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring>
    argc 5 "$#" arm || return
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'BOARD-VERDICT self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  # A scratch copy of the real board: the definition plus the composed catalogues the
  # verdict reads (their freshness against the definition is BOARD-GEN's, re-proven above).
  mkdir -p "$t/board"
  cp "$BOARD"/board.sexp "$BOARD"/requirements.sexp \
     "$BOARD"/contract-obligations.sexp "$BOARD"/sources.sexp "$t/board/"

  # GREEN: the real board's composition is ACCEPTED, every edge printed.
  out="$(python3 scripts/board_verdict.py "$t/board" 2>&1)"; rc=$?
  arm "GREEN the real board's composition is ACCEPTED" "$rc" 0 "$out" "composition ACCEPTED"

  # RED: a marked obligation left unanswered is a rejection, named.
  mkdir -p "$t/unanswered"; cp "$t/board"/* "$t/unanswered/"
  python3 - "$t/unanswered/board.sexp" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
p.write_text(p.read_text().replace('(answers "OB-NIC-STRAP-RESETS"))', ')'))
PY
  out="$(python3 scripts/board_verdict.py "$t/unanswered" 2>&1)"; rc=$?
  arm "RED a deferred obligation no decision answers" "$rc" 1 "$out" "UNANSWERED COMPOSITION OBLIGATION 'OB-NIC-STRAP-RESETS'"

  # RED: an answers edge naming nothing marked is a rejection, named.
  mkdir -p "$t/ghost"; cp "$t/board"/* "$t/ghost/"
  python3 - "$t/ghost/board.sexp" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
p.write_text(p.read_text().replace('(answers "OB-NIC-STRAP-RESETS")', '(answers "OB-NIC-GHOST")'))
PY
  out="$(python3 scripts/board_verdict.py "$t/ghost" 2>&1)"; rc=$?
  arm "RED an answers edge to nothing marked" "$rc" 1 "$out" "ANSWERS NOTHING"

  # RED: an obligation answered by two decisions is a rejection, named.
  mkdir -p "$t/twice"; cp "$t/board"/* "$t/twice/"
  python3 - "$t/twice/board.sexp" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
p.write_text(p.read_text().replace('(answers "OB-NIC-TIME-SOURCES")',
                                   '(answers "OB-NIC-TIME-SOURCES") (answers "OB-NIC-STRAP-RESETS")'))
PY
  out="$(python3 scripts/board_verdict.py "$t/twice" 2>&1)"; rc=$?
  arm "RED a deferred obligation answered twice" "$rc" 1 "$out" "ANSWERED TWICE"

  # RED: a satisfies edge naming no environment-assumption is a rejection, named.
  mkdir -p "$t/sghost"; cp "$t/board"/* "$t/sghost/"
  python3 - "$t/sghost/board.sexp" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
p.write_text(p.read_text().replace('(satisfies "OB-ENV-RESET")', '(satisfies "OB-ENV-GHOST")'))
PY
  out="$(python3 scripts/board_verdict.py "$t/sghost" 2>&1)"; rc=$?
  arm "RED a satisfies edge to no environment-assumption" "$rc" 1 "$out" "SATISFIES EDGE 'OB-ENV-GHOST'"

  # RED: the discharge leg armed — a guarantee removed from the composed catalogue
  # rejects the composition (the acceptance's unmatched assumption), named.
  mkdir -p "$t/nog"; cp "$t/board"/* "$t/nog/"
  python3 - "$t/nog/contract-obligations.sexp" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
lines = [l for l in p.read_text().splitlines(keepends=True)
         if '(obligation (id "OB-ENTRY-STATE")' not in l]
p.write_text("".join(lines))
PY
  out="$(python3 scripts/board_verdict.py "$t/nog" 2>&1)"; rc=$?
  arm "RED a guarantee removed — the discharge rejects" "$rc" 1 "$out" "DANGLING DEP"

  rm -rf "$t"
  printf 'BOARD-VERDICT --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "BOARD-VERDICT: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

if ! ls profiles/*/board.sexp >/dev/null 2>&1; then
  echo "BOARD-VERDICT: ok (no board declares itself yet)"
  exit 0
fi

rc=0
for def in profiles/*/board.sexp; do
  out="$(python3 scripts/board_verdict.py "$(dirname "$def")" 2>&1)" || {
    printf '%s\n' "$out" >&2
    printf 'BOARD-VERDICT: FAIL — the composition does not hold.\n' >&2
    rc=1
  }
done
[ "$rc" -eq 0 ] || exit 1
n="$(ls -d profiles/*/board.sexp 2>/dev/null | wc -l | tr -d ' ')"
printf 'BOARD-VERDICT: ok (%s board(s) — every CPU assumption discharged, every satisfies edge resolved, every composition disposition bound)\n' "$n"
exit 0
