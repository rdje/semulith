#!/usr/bin/env bash
# scripts/check_platform_gen.sh — PLATFORM-GEN (project doctrine).
#
# `P5-BOARD.6`: a board's platform capability manifest
# (`profiles/<board>/platform.sexp`, schema `schema/platform.sexp`) is GENERATED from its
# canonical inputs by `scripts/gen_platform.py` — the board definition, the pinned
# processor's profile dossier, and the composed contract obligations (OWN-06: derived,
# never handwritten; a compatibility checker imports facts rather than becoming a second
# hardware implementation). This check re-derives the manifest per board and refuses the
# day it stops byte-matching the tracked file.
#
# ⭐ WHAT THIS ACTUALLY PROTECTS: not tidiness — the DERIVATION, and with it the board's
# dossier-sha256 PIN: the generator re-derives the pinned digest from the live dossier
# (gate_report.dossier_digest, the ONE computation) and refuses a stale pin. The pin was
# measured display-only before this leaf (rendered by gen_model_book.py, re-derived by
# nothing); this gate is what makes it load-bearing — a dossier edit can no longer
# silently stale the board's processor pin.
#
# ⚠️ HONEST LIMIT: it proves the manifest is still the function of its canonical inputs.
# It says nothing about whether those inputs are TRUE — the pins have their own gates
# (RECORD-SCHEMA, BOARD-GEN, BOARD-VERDICT, GATE-REPORT), and the manifest's own
# non-claims are data inside it: a compatible manifest proves neither OS correctness nor
# manifest-implementation match, and no archogen eADL interface exists today to accept
# it (archogen is actively developed — the consumer side is AG-OS's).
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "PLATFORM-GEN: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

BOARD="profiles/netboard-lab-v0"
# The digest of a dossier directory git does not track (a scratch sibling unit):
# git ls-files yields nothing, so the ONE computation hashes zero inputs.
EMPTY_DIGEST="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): a missing `;` before
  # an arm call swallows it silently; the guard makes that a loud failure.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'PLATFORM-GEN self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
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
      printf 'PLATFORM-GEN self-test MISS: %s — expected rc=%s and no output, got rc=%s\n%s\n' \
        "$1" "$3" "$2" "$4" >&2
      return
    fi
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'PLATFORM-GEN self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  # A scratch copy of the real board: the definition and the composed obligations the
  # export derives from. The processor unit resolves to the repo's real dossier (the
  # fallback), so the digest pin verifies against the live dossier.
  mkdir -p "$t/board"
  cp "$BOARD/board.sexp" "$BOARD/contract-obligations.sexp" "$BOARD/platform.sexp" "$t/board/"

  # GREEN: the generator emits the manifest from the real inputs.
  out="$(python3 scripts/gen_platform.py --board-dir "$t/board" --out-dir "$t/out" 2>&1)"; rc=$?
  arm "GREEN the generator emits the manifest from the real inputs" "$rc" 0 "$out" "platform.sexp generated"

  # GREEN: determinism — a second derivation is byte-identical.
  python3 scripts/gen_platform.py --board-dir "$t/board" --out-dir "$t/out2" >/dev/null 2>&1
  if diff -r "$t/out" "$t/out2" >/dev/null 2>&1; then
    out=""; rc=0
  else
    out="nondeterministic"; rc=1
  fi
  arm "GREEN two derivations are byte-identical" "$rc" 0 "$out" ""

  # GREEN: a faithful generation is judged in sync — derive, then re-derive against it
  # (the scratch paths embed in the fingerprint header, so the comparison is
  # scratch-derived vs scratch-derived; the REAL run judges the tracked board).
  out="$(python3 scripts/gen_platform.py --check --board-dir "$t/board" --out-dir "$t/out" 2>&1)"; rc=$?
  arm "GREEN a faithful generation is judged in sync" "$rc" 0 "$out" "byte-exact"

  # RED: a hand-edited manifest is detected and named.
  mkdir -p "$t/d1"; cp "$t/board/board.sexp" "$t/board/contract-obligations.sexp" "$t/d1/"
  cp "$t/board/platform.sexp" "$t/d1/platform.sexp"
  printf '\n;; hand edit\n' >> "$t/d1/platform.sexp"
  out="$(python3 scripts/gen_platform.py --check --board-dir "$t/d1" 2>&1)"; rc=$?
  arm "RED a hand-edited platform.sexp is refused, naming DRIFT" "$rc" 1 "$out" "platform.sexp: DRIFT"

  # RED: a board.sexp edit against a stale manifest is drift, named — the definition
  # moved, the export did not.
  mkdir -p "$t/d2"; cp "$t/board/contract-obligations.sexp" "$t/board/platform.sexp" "$t/d2/"
  sed 's/(id "netboard-lab-v0")/(id "netboard-lab-v9")/' "$t/board/board.sexp" > "$t/d2/board.sexp"
  out="$(python3 scripts/gen_platform.py --check --board-dir "$t/d2" 2>&1)"; rc=$?
  arm "RED a moved definition against a stale export is refused, naming DRIFT" "$rc" 1 "$out" "DRIFT"

  # RED: a stale dossier pin is refused by name — the pin is load-bearing, not display.
  # The mutation rewrites the digest to a fixed wrong value of the same shape (an earlier
  # form flipped the first character and silently stopped mutating the day the live digest
  # rotated to a different leading hex digit — measured, P4-SYSTEM.2 slice d).
  mkdir -p "$t/d3"; cp "$t/board/contract-obligations.sexp" "$t/d3/"
  sed -E 's/\(dossier-sha256 "[0-9a-f]{64}"\)/(dossier-sha256 "0000000000000000000000000000000000000000000000000000000000000000")/' \
    "$t/board/board.sexp" > "$t/d3/board.sexp"
  out="$(python3 scripts/gen_platform.py --board-dir "$t/d3" --out-dir "$t/d3o" 2>&1)"; rc=$?
  arm "RED a stale dossier-sha256 pin is refused, named" "$rc" 2 "$out" "STALE"

  # RED: a processor profile without endianness is refused by name — §3 requires the
  # value and its one owner is the dossier; a guessed value is a second source of truth.
  # The sibling scratch unit is untracked, so the ONE digest computation hashes zero
  # inputs there — the pin is set to that digest so the arm isolates the endianness
  # refusal from the pin refusal.
  mkdir -p "$t/d4/units/netboard-lab-v0" "$t/d4/units/rv64i-lab-v0"
  cp "$t/board/contract-obligations.sexp" "$t/d4/units/netboard-lab-v0/"
  python3 - "$t/d4/units/rv64i-lab-v0/profile.sexp" <<'PY'
import sys
from pathlib import Path
src = Path("profiles/rv64i-lab-v0/profile.sexp").read_text()
assert "(endianness little) " in src
Path(sys.argv[1]).write_text(src.replace("(endianness little) ", ""))
PY
  sed "s/(dossier-sha256 \"[0-9a-f]*\")/(dossier-sha256 \"$EMPTY_DIGEST\")/" \
    "$t/board/board.sexp" > "$t/d4/units/netboard-lab-v0/board.sexp"
  out="$(python3 scripts/gen_platform.py --board-dir "$t/d4/units/netboard-lab-v0" --out-dir "$t/d4o" 2>&1)"; rc=$?
  arm "RED a profile without endianness is refused, naming the owner" "$rc" 2 "$out" "'endianness' is absent"

  # RED: a boot load-region that is not executable RAM is refused by name.
  mkdir -p "$t/d5"; cp "$t/board/contract-obligations.sexp" "$t/d5/"
  sed 's/(load-region "ram0")/(load-region "eth0")/' "$t/board/board.sexp" > "$t/d5/board.sexp"
  out="$(python3 scripts/gen_platform.py --board-dir "$t/d5" --out-dir "$t/d5o" 2>&1)"; rc=$?
  arm "RED a load-region that is not executable RAM is refused" "$rc" 2 "$out" "executable RAM"

  # RED: a test-control claim the wiring contradicts — console capture over a console
  # device whose TX backend is a recording sink.
  mkdir -p "$t/d6"; cp "$t/board/contract-obligations.sexp" "$t/d6/"
  python3 - "$t/board/board.sexp" "$t/d6/board.sexp" <<'PY'
import sys
from pathlib import Path
src = Path(sys.argv[1]).read_text()
Path(sys.argv[2]).write_text(src.replace('(serial-console\n    (device "uart0"))',
                                         '(serial-console\n    (device "eth0"))'))
PY
  out="$(python3 scripts/gen_platform.py --board-dir "$t/d6" --out-dir "$t/d6o" 2>&1)"; rc=$?
  arm "RED console capture without a host-console backend is refused" "$rc" 2 "$out" "host-console"

  # RED: a composed unit missing the obligation the time facts derive from is refused
  # by name — the export never guesses a platform fact.
  mkdir -p "$t/d7"; cp "$t/board/board.sexp" "$t/d7/"
  grep -v '(id "OB-ENV-VIRTUAL-TIME")' "$t/board/contract-obligations.sexp" \
    > "$t/d7/contract-obligations.sexp"
  out="$(python3 scripts/gen_platform.py --board-dir "$t/d7" --out-dir "$t/d7o" 2>&1)"; rc=$?
  arm "RED a missing time obligation is refused, named" "$rc" 2 "$out" "OB-ENV-VIRTUAL-TIME"

  # RED: a time source other than "none" is a shape the generator cannot emit — the
  # fidelity of a time-bearing platform is a declaration, never an invention.
  mkdir -p "$t/d8"; cp "$t/board/board.sexp" "$t/d8/"
  sed 's/(name time_source) (value (str "none"))/(name time_source) (value (str "host"))/' \
    "$t/board/contract-obligations.sexp" > "$t/d8/contract-obligations.sexp"
  out="$(python3 scripts/gen_platform.py --board-dir "$t/d8" --out-dir "$t/d8o" 2>&1)"; rc=$?
  arm "RED a non-none time source is refused, named" "$rc" 2 "$out" "other than"

  rm -rf "$t"
  printf 'PLATFORM-GEN --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "PLATFORM-GEN: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

if ! ls profiles/*/board.sexp >/dev/null 2>&1; then
  echo "PLATFORM-GEN: ok (no board declares itself yet)"
  exit 0
fi

out="$(python3 scripts/gen_platform.py --check 2>&1)" || {
  printf '%s\n' "$out" >&2
  printf 'PLATFORM-GEN: FAIL — a platform capability manifest is out of sync with its canonical inputs.\n' >&2
  exit 1
}
n="$(ls -d profiles/*/board.sexp 2>/dev/null | wc -l | tr -d ' ')"
printf 'PLATFORM-GEN: ok (%s board(s) — the platform capability manifest is a byte-exact function of its canonical inputs, the dossier pin verified live)\n' "$n"
exit 0
