#!/usr/bin/env bash
# scripts/check_definition_gen.sh — DEF-GEN (project doctrine).
#
# `crates/semulith-core/src/definition.rs` is GENERATED from the unit's canonical
# definition by `scripts/gen_definition.py` (P1-LAB.6; OWN-03: generated artifacts are
# changed by regeneration, never by direct editing, and identify their canonical inputs,
# generator, configuration, and source fingerprints). This check regenerates the module
# in memory and refuses the day it stops byte-matching the committed file — a
# hand-edited decode table or effect tree is how the definition and its executable half
# quietly become two facts (OWN-01's duplicate owner, arriving as drift).
#
# ⭐ WHAT THIS ACTUALLY PROTECTS: not tidiness — the DERIVATION. The encoding data, the
# semantics data, and the state descriptor are the authorities; the module is their
# lowered mirror, carrying OWN-03's manifest so a reviewer can name the exact bytes and
# the exact generator behind every table. Both the module and the doctrine exist so
# "generated" stays a claim with a governor (doctrine/fact_ownership.tsv names the
# pairs).
#
# ⚠️ HONEST LIMIT: it proves the module is still the function of the input bytes. It
# says nothing about whether the DEFINITION is true — the semantics have their own gate
# (SEMANTICS: well-formed, complete, cited), and correctness is a differential
# experiment against a reference model (P1-LAB.8+), never a regeneration.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "DEF-GEN: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

ENCODING="profiles/rv64i-lab-v0/encoding.sexp"
STATE="profiles/rv64i-lab-v0/state.sexp"
OUT="crates/semulith-core/src/definition.rs"

# ── self-test ────────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # The generator resolves fragments as <encoding's parent^3>/<fragment-root>, so the
  # surgical unit mirrors the real layout: tmp/profiles/<unit>/encoding.sexp composes
  # tmp/definitions/riscv/*. The state descriptor is fingerprinted, not read — the real
  # one answers.
  mkdir -p "$t/profiles/rv64i-lab-v0" "$t/definitions/riscv"
  cp "$ENCODING" "$t/profiles/rv64i-lab-v0/encoding.sexp"
  cp definitions/riscv/rv64i.sexp "$t/definitions/riscv/rv64i.sexp"
  cp definitions/riscv/rv64i.sem.sexp "$t/definitions/riscv/rv64i.sem.sexp"
  GEN() { python3 scripts/gen_definition.py --encoding "$t/profiles/rv64i-lab-v0/encoding.sexp" \
          --state "$STATE" --out "$t/definition.rs" "$@"; }

  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md): a missing `;` before
  # an arm call swallows it silently; the guard makes that a loud failure.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'DEF-GEN self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
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
      printf 'DEF-GEN self-test MISS: %s — expected rc=%s and no output, got rc=%s\n%s\n' \
        "$1" "$3" "$2" "$4" >&2
      return
    fi
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'DEF-GEN self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }

  # GREEN: the generator emits a module from the real definition.
  out="$(GEN 2>&1)"; rc=$?
  arm "GREEN the generator emits a module from the real definition" "$rc" 0 "$out" "wrote"

  # GREEN: the drift check passes on a faithful regeneration.
  out="$(GEN --check 2>&1)"; rc=$?
  arm "GREEN a faithful regeneration is judged in sync" "$rc" 0 "$out" ""

  # RED: a hand-edit of the generated module is detected, named, and refused.
  printf '\n// hand edit\n' >> "$t/definition.rs"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a hand-edited module is refused, naming DRIFT" "$rc" 1 "$out" "DRIFT"

  # RED: a unit with an instruction length this generator cannot emit is refused by name.
  sed 's/(ilen 32)/(ilen 64)/' "$ENCODING" > "$t/profiles/rv64i-lab-v0/encoding.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an unsupported instruction length is refused by name" "$rc" 2 "$out" "ilen 64"
  cp "$ENCODING" "$t/profiles/rv64i-lab-v0/encoding.sexp"

  # RED: a unit other than the laboratory profile is refused by name.
  sed 's/(profile "rv64i-lab-v0")/(profile "rv64i-other-v0")/' "$ENCODING" \
    > "$t/profiles/rv64i-lab-v0/encoding.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED another unit is refused by name" "$rc" 2 "$out" "rv64i-other-v0"
  cp "$ENCODING" "$t/profiles/rv64i-lab-v0/encoding.sexp"

  # RED: an instruction the semantics do not cover is refused, naming the instruction.
  python3 - "$t/definitions/riscv/rv64i.sexp" <<'PY'
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
add = '(insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))'
assert add in text
ghost = add.replace('(name add)', '(name zzz9)')
open(path, "w", encoding="utf-8").write(text.replace(add, add + "\n  " + ghost))
PY
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an encoding instruction without semantics is refused, naming it" "$rc" 2 "$out" "zzz9"
  cp definitions/riscv/rv64i.sexp "$t/definitions/riscv/rv64i.sexp"

  # RED: a semantics rule referencing an operand the encoding does not provide is refused.
  sed 's/(add (reg rs1) (reg rs2))/(add (reg rs1) (reg rs3))/' definitions/riscv/rv64i.sem.sexp \
    > "$t/definitions/riscv/rv64i.sem.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an undeclared operand reference is refused, naming it" "$rc" 2 "$out" "'rs3'"
  cp definitions/riscv/rv64i.sem.sexp "$t/definitions/riscv/rv64i.sem.sexp"

  # RED: an instruction declaring an operand that names no field is refused, naming it —
  # extraction for it would be silent, and silence is the guessed translation
  # ARCHITECTURE §2 forbids (P3-BREADTH.2).
  python3 - "$t/definitions/riscv/rv64i.sexp" <<'PY'
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
add = '(insn (name add) (fixed (31 25 0x0) (14 12 0x0) (6 2 0xc) (1 0 0x3)) (operands rd rs1 rs2) (from "rv_i"))'
assert add in text
open(path, "w", encoding="utf-8").write(
    text.replace(add, add.replace("(operands rd rs1 rs2)", "(operands rd rs1 rs2 rs9)")))
PY
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED an operand naming no field is refused, naming it" "$rc" 2 "$out" "rs9"
  cp definitions/riscv/rv64i.sexp "$t/definitions/riscv/rv64i.sexp"

  # RED: a fragment whose semantics document is missing is refused, naming the pairing.
  rm "$t/definitions/riscv/rv64i.sem.sexp"
  out="$(GEN --check 2>&1)"; rc=$?
  arm "RED a fragment without its semantics document is refused" "$rc" 2 "$out" "no semantics document"

  rm -rf "$t"
  printf 'DEF-GEN --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

# Re-run the controls before judging: a check that no longer discriminates must refuse,
# not pass (the project-doctrine contract in scripts/check_doctrines.project.sh).
self_test >/dev/null 2>&1 || {
  echo "DEF-GEN: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }

[ -f "$ENCODING" ] || { echo "DEF-GEN: ok (no encoding composition yet)"; exit 0; }

out="$(python3 scripts/gen_definition.py --check --encoding "$ENCODING" --state "$STATE" \
      --out "$OUT" 2>&1)"; rc=$?
if [ "$rc" -eq 2 ]; then
  printf '%s\n' "$out" >&2
  echo "DEF-GEN: REFUSED — the canonical definition could not be judged." >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  printf '%s\n' "$out" >&2
  printf 'DEF-GEN: FAIL — %s is out of sync with the canonical definition. Regenerate — never edit:\n  python3 scripts/gen_definition.py\n' \
    "$OUT" >&2
  exit 1
fi
sha="$(sha256sum "$ENCODING" | cut -d' ' -f1)"
printf 'DEF-GEN: ok (%s matches the canonical definition, encoding sha256 %s)\n' "$OUT" "${sha:0:16}"
exit 0
