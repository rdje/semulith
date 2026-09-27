#!/usr/bin/env bash
# scripts/check_unit_composition.sh — UNIT-COMPOSITION (project doctrine).
#
# WHY THIS EXISTS, measured rather than argued. `MODEL-COMPOSE.1` made a unit's encoding union a
# verdict, and `MODEL-COMPOSE.2` moved the instructions into reusable fragments — and the verdict
# silently stopped running on the unit: the disjointness checker read compositions its own way
# and could no longer read a unit's encoding.sexp at all (probe: REFUSED, "yielded no
# instructions", rc=2), and no gate invoked it on the unit's fragments. The unit's composed
# encoding space was being assembled on every smoke run but never DECIDED anywhere. This
# doctrine is the decision's home: every tracked unit's composition document is
# schema-conformant (`MODEL-COMPOSE.4`, the undeclared-field refusal), its fragments resolve
# with dependencies met through the ONE shared resolver, its union is collision-free, and a
# partial composition is DECLARED — slots without `(status partial)` claim completeness while a
# hole is open, which this gate refuses.
#
# ⛔ Restored capability that no gate invokes is the defect restated — a check that runs
# nowhere is prose with a shebang.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "UNIT-COMPOSITION: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_units() { # $1 = root to scan; $2 = "git" (tracked only) or "fs" (everything there)
python3 - "$1" "$2" <<'PY'
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
sys.path.insert(0, "scripts")               # the gate always runs from the repository root

if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", "profiles/*/encoding.sexp"],
                         capture_output=True, text=True, check=True).stdout
    docs = [root / p for p in out.splitlines() if p.strip()]
else:
    docs = sorted(root.glob("profiles/*/encoding.sexp"))

if not docs:
    print("UNIT-COMPOSITION: REFUSED — no unit composition document found; "
          "this check cannot judge an empty corpus")
    print("__CHECKED__ 0"); sys.exit(2)

import check_encoding_disjoint as C
findings, checked = [], 0
for doc in docs:
    checked += 1
    try:
        insns = C.load_fragment(doc)              # schema + resolve + read
        slots = C.composition_slots(__import__("sexp").read_file(doc)[0])[1]
        C.check_slot_rules(doc, __import__("sexp").read_file(doc)[0])
    except (C.CompositionError, Exception) as exc:  # noqa: BLE001 — name the document, not a traceback
        findings.append(f"REFUSED {doc}: {exc}")
        continue
    bad = C.collisions(insns)
    dupes = [n for n in {i.name for i in insns} if sum(1 for i in insns if i.name == n) > 1]
    if bad or dupes:
        findings.append(f"REJECTED {doc}: {len(bad)} collision(s), {len(dupes)} duplicate name(s) "
                        f"— a decoder cannot be generated from a set in which one word matches "
                        f"two instructions")
        continue
    suffix = f"; partial: {len(slots)} slot(s) unbound" if slots else ""
    print(f"  {doc}: {len(insns)} instruction(s) compose{suffix}")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/definitions/riscv" "$t/profiles/p"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'UNIT-COMPOSITION self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_units "$t" fs 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'UNIT-COMPOSITION self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'UNIT-COMPOSITION self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  base_frag() { printf '%s\n' '(fragment (id "riscv/t-base") (kind extension)' \
      '(insn (name "add") (fixed (31 25 0x0) (14 12 0x0) (6 2 0x13) (1 0 0x3)))' \
      '(insn (name "sub") (fixed (31 25 0x0) (14 12 0x1) (6 2 0x13) (1 0 0x3))))' \
      > "$t/definitions/riscv/t-base.sexp"; }
  enc() { printf '%s\n' "(encoding (profile \"p\") (ilen 32)" \
      "  (compose (base \"riscv/t-base\")$1)" \
      '  (fragment-root "definitions"))' > "$t/profiles/p/encoding.sexp"; }

  base_frag; enc ' (extensions)';         arm "GREEN a complete unit composes" 0 "instruction(s) compose"
  base_frag; enc ' (extensions) (status partial) (slot (id clint) (requires "riscv/t-timer"))'
                                          arm "GREEN a declared slot is reported partial" 0 "1 slot(s) unbound"
  base_frag; enc ' (extensions) (slot (id clint))'
                                          arm "RED   slots claiming completeness" 1 "claiming completeness while a hole is open"
  base_frag; enc ' (extensions) (status partial)'
                                          arm "RED   a partial declaration with nothing unbound" 1 "a hole is declared that is not there"
  base_frag; enc ' (extensions) (widget "x")'
                                          arm "RED   an undeclared compose field" 1 'undeclared field "widget"'
  enc ' (extensions "riscv/t-ghost")';   arm "RED   a fragment the composition names but does not have" 1 "does not exist"
  printf '%s\n' '(fragment (id "riscv/t-clash") (kind extension)' \
      '(insn (name "add") (fixed (31 25 0x0) (14 12 0x0) (6 2 0x13) (1 0 0x3))))' \
      > "$t/definitions/riscv/t-clash.sexp"
  base_frag; enc ' (extensions "riscv/t-clash")'
                                          arm "RED   a collision in the composed union" 1 "collision(s)"
  rm -f "$t/profiles/p/encoding.sexp";    arm "RED   no composition document at all" 2 "cannot judge"

  rm -rf "$t"
  printf 'UNIT-COMPOSITION --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "UNIT-COMPOSITION: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_units "$ROOT" git)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "UNIT-COMPOSITION: REFUSED — the unit composition corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "UNIT-COMPOSITION: a unit's composition does not hold."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The composition is authoritative. Fix the unit, or it does not compose."; } >&2
  exit 1
fi
printf 'UNIT-COMPOSITION: ok (%s unit composition(s) decided)\n' "${count:-0}"
exit 0
