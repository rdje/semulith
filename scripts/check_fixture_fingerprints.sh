#!/usr/bin/env bash
# scripts/check_fixture_fingerprints.sh — FIXTURE-FINGERPRINT (project doctrine).
#
# A data record that pins a file's SHA-256 is making a claim about the working tree. Nothing
# re-derives such a claim by itself, so it is true the day it is written and unfalsifiable
# afterwards — the exact shape `docs/CLAIM_VERIFICATION.md` calls a leg-3 (durability) breach,
# and the reason its §5B rule says a constant that is a function of the repository is DERIVED
# or GATED, never carried.
#
# THE RULE, stated without this project's nouns: in every tracked JSON/JSONL record, an object
# carrying BOTH `path` and `sha256` must name a file that exists, resolved relative to the
# record's own directory, whose content hashes to that value.
#
# This covers `examples/sources.json` today and the `inputs`/`artifacts` arrays of
# `schemas/evidence.schema.json` records as soon as real evidence exists — the production
# shape, not a one-off.
#
# ⛔ NOT covered, deliberately: `docs/provenance/**` (owned by check_delivery_provenance.sh,
# which knows about row dispositions), and records naming inputs that are not in this
# repository — `DESIGN_INPUTS.json` uses `file_name`, not `path`, precisely so that an
# unverifiable hash cannot masquerade as a checked one.
#
# ⚠️ HONEST LIMIT: this proves the pinned bytes are the current bytes. It says nothing about
# whether the pinned file is the RIGHT file, or its content correct.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  # A skip is never a pass: with no JSON reader this check cannot judge anything, and
  # returning 0 would report "the fingerprints hold" over an absence.
  echo "FIXTURE-FINGERPRINT: REFUSED — python3 is not on PATH; this check cannot judge." >&2
  exit 2
fi

# $1 = directory to scan. Prints one finding per line; exits nonzero on breach.
scan_tree() {
python3 - "$1" <<'PY'
import hashlib, json, os, sys

root = sys.argv[1]
# ⛔ `vendor` is excluded for a reason worth keeping: when vendor/linkedspec arrived, this scan
# walked 1.7 GB of another project's tree and died with RecursionError on a deeply nested JSON
# document of theirs. It did not mis-report — it crashed, which is the better of the two failures
# but still a gate that stopped judging. Our fixtures are ours; a submodule's are not.
EXCLUDE = ("docs/provenance", ".git", "target", "vendor")
findings, checked = [], 0

def pins(obj, out):
    """Every object carrying BOTH `path` and `sha256`, anywhere in the structure."""
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str) and isinstance(obj.get("sha256"), str):
            out.append((obj["path"], obj["sha256"]))
        for v in obj.values():
            pins(v, out)
    elif isinstance(obj, list):
        for v in obj:
            pins(v, out)

def records(fp):
    text = fp.read_text()
    if fp.suffix == ".jsonl":
        for n, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield n, json.loads(line)
            except json.JSONDecodeError as e:
                findings.append(f"UNPARSEABLE {fp}:{n} — {e}")
    else:
        try:
            yield 1, json.loads(text)
        except json.JSONDecodeError as e:
            findings.append(f"UNPARSEABLE {fp} — {e}")

from pathlib import Path
for dirpath, dirnames, filenames in os.walk(root):
    rel = os.path.relpath(dirpath, root)
    if rel != "." and any(rel == e or rel.startswith(e + os.sep) for e in EXCLUDE):
        dirnames[:] = []
        continue
    dirnames[:] = [d for d in dirnames if d not in (".git", "target")]
    for name in sorted(filenames):
        if not name.endswith((".json", ".jsonl")):
            continue
        fp = Path(dirpath) / name
        shown = os.path.relpath(fp, root)
        for lineno, rec in records(fp):
            found = []
            pins(rec, found)
            for path, want in found:
                checked += 1
                where = f"{shown}:{lineno}"
                if len(want) != 64 or any(c not in "0123456789abcdef" for c in want):
                    findings.append(f"MALFORMED {where} — sha256 '{want}' is not 64 lowercase hex")
                    continue
                target = (fp.parent / path).resolve()
                if not target.is_file():
                    findings.append(f"MISSING   {where} — pins '{path}', which does not exist")
                    continue
                got = hashlib.sha256(target.read_bytes()).hexdigest()
                if got != want:
                    findings.append(
                        f"DRIFTED   {where} — '{path}'\n    pinned  {want}\n    current {got}")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

SELFTEST_TMP() {  # repo-volume scratch: project-created temporary workspaces must not
  # land on another filesystem (and $TMPDIR is one). /target is already untracked.
  local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"
}

self_test() {
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/fix"
  printf 'payload\n' > "$t/fix/spec.md"
  local h; h="$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$t/fix/spec.md")"
  write_ledger() { printf '{"sources":[{"id":"S","path":"spec.md","sha256":"%s"}]}\n' "$1" > "$t/fix/sources.json"; }
  # ⛔ Each arm asserts the verdict AND the reason: a control that goes red for the wrong
  # reason is a control that cannot fail on the thing it was written for.
  arm() { # name expected_rc expected_substring
    out="$(scan_tree "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'FIXTURE-FINGERPRINT self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'FIXTURE-FINGERPRINT self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }
  write_ledger "$h";                      arm "GREEN pinned hash matches"     0 "__CHECKED__ 1"
  printf 'tampered\n' > "$t/fix/spec.md"; arm "RED   pinned file changed"     1 "DRIFTED"
  printf 'payload\n'  > "$t/fix/spec.md"
  write_ledger "${h:0:63}";               arm "RED   malformed hash length"   1 "MALFORMED"
  write_ledger "$(printf '%064d' 0)";     arm "RED   wrong hash, well-formed" 1 "DRIFTED"
  write_ledger "$h"; mv "$t/fix/spec.md" "$t/fix/gone.md"
                                          arm "RED   pinned file absent"      1 "MISSING"
  mv "$t/fix/gone.md" "$t/fix/spec.md"
  printf '{"sources":[{"id":"S"' > "$t/fix/sources.json"
                                          arm "RED   unparseable record"      1 "UNPARSEABLE"
  rm -f "$t/fix/sources.json";            arm "GREEN nothing pinned"          0 "__CHECKED__ 0"
  rm -rf "$t"
  printf 'FIXTURE-FINGERPRINT --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "FIXTURE-FINGERPRINT: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2
}

out="$(scan_tree "$ROOT")"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -ne 0 ]; then
  { echo "FIXTURE-FINGERPRINT: a record pins a fingerprint that no longer describes the tree."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  Re-derive the pin from the file, or fix the file — never edit the pin to silence this."
  } >&2
  exit 1
fi
printf 'FIXTURE-FINGERPRINT: ok (%s pinned fingerprint(s) re-derived)\n' "${count:-0}"
exit 0
