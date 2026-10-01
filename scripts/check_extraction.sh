#!/usr/bin/env bash
# scripts/check_extraction.sh — EXTRACTION (project doctrine).
#
# WHY THIS EXISTS. `MODEL-METHOD.10` turns "the engine can extract all it needs" from an
# intention into a verdict: every declared instruction has an encoding AND semantics AND a
# requirement, every state element a reset, every obligation its checks. P1-LAB cites THIS
# CHECK as the precondition for writing model code — and a check that runs nowhere cannot be
# cited. The doctrine discovers every tracked unit (profiles/*) and runs the contract on each;
# the day it fires, model code does not start on a definition that quietly lacks something.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "EXTRACTION: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_units() { # $1 = root; $2 = "git" (tracked units only) or "fs"
python3 - "$1" "$2" <<'PY'
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", "profiles/*/profile.sexp"],
                         capture_output=True, text=True, check=True).stdout
    units = [root / p for p in out.splitlines() if p.strip()]
    units = [u.parent for u in units]
else:
    units = sorted(p.parent for p in root.glob("profiles/*/profile.sexp"))

if not units:
    print("EXTRACTION: REFUSED — no unit found; this check cannot judge an empty corpus")
    print("__CHECKED__ 0"); sys.exit(2)

findings, checked = [], 0
for u in units:
    checked += 1
    r = subprocess.run([sys.executable, "scripts/check_extraction.py", str(u)],
                       capture_output=True, text=True)
    if r.returncode == 2:
        findings.append(f"CANNOT JUDGE {u.relative_to(root)}: {r.stderr.strip()}")
    elif r.returncode != 0:
        gap = [l for l in r.stderr.splitlines() if l.strip()][-1:]
        findings.append(f"INSUFFICIENT {u.relative_to(root)}: {gap[0] if gap else r.stderr.strip()}")
    else:
        print(f"  {u.relative_to(root)}: {r.stdout.strip()}")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/definitions/riscv" "$t/profiles/good" "$t/profiles/bad"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'EXTRACTION self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_units "$t" fs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'EXTRACTION self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'EXTRACTION self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  frag() { printf '%s\n' '(fragment (id "riscv/t") (kind extension)' \
      '(insn (name add) (fixed (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2))' \
      '(insn (name sub) (fixed (6 2 0x13) (1 0 0x3)) (operands rd rs1 rs2)))' \
      > "$t/definitions/riscv/t.sexp"; }
  sem() { printf '%s\n' '(semantics (fragment "riscv/t") (xlen 64)' "$1" ')' \
      > "$t/definitions/riscv/t.sem.sexp"; }
  RULE='(sem (insn add) (source "S §1 — why") (effect (set (reg rd) (add (reg rs1) (reg rs2)))))'
  RULE2='(sem (insn sub) (source "S §2 — why") (effect (set (reg rd) (sub (reg rs1) (reg rs2)))))'
  unit_docs() { # $1 = unit dir
    printf '%s\n' '(encoding (profile "p") (ilen 32)' \
        '  (compose (base "riscv/t") (extensions))' '  (fragment-root "definitions"))' \
        > "$1/encoding.sexp"
    printf '%s\n' '(profile (id "p") (version "0") (status "development") (architecture "R")' \
        '  (scope (count_base 2) (count_total 2) (demo "ADD" "SUB"))' \
        '  (decision (id "D-X") (authority architecture) (statement "s") (source "S §1")))' \
        > "$1/profile.sexp"
    python3 - "$1" <<'PY2'
import sys, pathlib
sys.path.insert(0, "scripts")
import records_sexp as R
u = pathlib.Path(sys.argv[1])
req = {"id": "REQ-D-X", "profile_ids": ["p"], "kind": "instruction", "statement": "s",
       "insns": ["add", "sub"],
       "source_refs": [{"source_id": "S", "locator": "§1"}],
       "applicability": "included", "research_status": "resolved",
       "implementation_status": "planned",
       "source_semantics": {"category": "defined", "detail": "d"}, "risk": "low",
       "obligation_ids": ["OB-X"], "dependencies": [],
       "implementation_refs": [], "evidence_ids": []}
ob = {"id": "OB-X", "contract_id": "c", "contract_version": "0", "profile_ids": ["p"],
      "direction": "cpu-guarantee", "statement": "s", "authority": "architecture",
      "source_refs": [{"source_id": "S", "locator": "§1"}], "parameters": {},
      "dependencies": [], "required_checks": ["CHK-X-POS", "CHK-X-NEG"]}
(u / "requirements.sexp").write_text(R.dump([req]))
(u / "contract-obligations.sexp").write_text(R.dump([ob]))
(u / "state.sexp").write_text(
    '(state (profile_id "p") (xlen 64)\n'
    '  (integer_registers (count 32) (width_bits 64) '
    '(reset (value "0") (authority laboratory) (source "S") (statement "r"))))\n')
PY2
  }

  frag; sem "$RULE
$RULE2"; unit_docs "$t/profiles/good"
  sem "$RULE
$RULE2"; unit_docs "$t/profiles/bad"
  arm "GREEN a sufficient unit is discovered and judged" 0 "SUFFICIENT"

  sem "$RULE"; unit_docs "$t/profiles/bad"   # bad loses sub's semantics
  arm "RED   a unit missing one instruction's semantics" 1 "does not cover: sub"

  # ── the sibling-crate leg (P3-BREADTH.7, case dsp56300-lab-v0) ──
  sem "$RULE
$RULE2"   # restore the shared fragment's full semantics — good/bad are green again
  mkdir -p "$t/profiles/sibling"
  printf '%s\n' '(profile (id "s") (version "0") (status "experimental") (architecture "D")' \
      '  (vehicle (route sibling-crate) (comparison checkpoint-end-state) (authority laboratory) (source "s"))' \
      '  (scope (count_base 2) (count_total 2) (demo "MOV" "NOP"))' \
      '  (decision (id "D-X") (authority laboratory) (statement "s") (source "S §1")))' \
      > "$t/profiles/sibling/profile.sexp"
  arm "GREEN a declared sibling-crate unit is reported by name" 0 "sibling-crate route declared"

  printf '%s\n' '(encoding (profile "s") (ilen 24)' \
      '  (compose (base "riscv/t") (extensions))' '  (fragment-root "definitions"))' \
      > "$t/profiles/sibling/encoding.sexp"
  arm "RED   a sibling-crate declaration contradicted by an encoding.sexp" 1 "contradicts the documents"
  rm -rf "$t/profiles/sibling"

  rm -rf "$t/profiles/good" "$t/profiles/bad"
  arm "REFUSE an empty corpus, never pass it" 2 "cannot judge"

  rm -rf "$t"
  printf 'EXTRACTION --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "EXTRACTION: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_units "$ROOT" git)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "EXTRACTION: REFUSED — the unit corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "EXTRACTION: a unit's definition is not sufficient for an engine."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The definition is the authority. Fix the corpus, or model code does not start."; } >&2
  exit 1
fi
printf 'EXTRACTION: ok (%s unit(s) sufficient — P1-LAB may cite this)\n' "${count:-0}"
exit 0
