#!/usr/bin/env bash
# scripts/check_profile_consistency.sh — PROFILE-CONSISTENCY (project doctrine).
#
# A profile dossier is a set of claims about a specification. Two of them can go wrong quietly:
#
#   1. A DECLARED COUNT drifts from the ENUMERATION it summarises. `count_total = 52` beside a
#      list of 51 mnemonics is a contract number that is simply false, and nothing about the
#      file's appearance reveals it. `CLAIM_VERIFICATION.md` §5B: a constant that is a function
#      of the repository is derived or gated, never carried.
#   2. A DECISION loses its authority or its source. The whole point of the `authority` field is
#      that a `laboratory` policy must never be mistaken for an `architecture` rule — an
#      unsourced decision is exactly how that mistake becomes permanent.
#
# ⚠️ HONEST LIMIT, stated rather than implied: this proves the file is INTERNALLY consistent and
# that every decision cites something. It cannot check the citation against the specification —
# that is a human reading, and `scripts/fetch_sources.sh` exists to make the artifact being read
# identifiable.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "PROFILE-CONSISTENCY: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_profiles() {
python3 - "$1" <<'PY'
import sys, pathlib, tomllib

root = pathlib.Path(sys.argv[1])
AUTHORITIES = {"architecture", "execution-environment", "laboratory"}
findings, checked = [], 0

for toml_path in sorted(root.glob("*/profile.toml")):
    name = toml_path.parent.name
    checked += 1
    try:
        d = tomllib.loads(toml_path.read_text())
    except Exception as e:
        findings.append(f"UNPARSEABLE {name}/profile.toml — {e}")
        continue

    scope = d.get("scope")
    if not isinstance(scope, dict):
        findings.append(f"NO SCOPE   {name}: profile.toml has no [scope] table")
    else:
        listed = sum(len(v) for v in scope.values() if isinstance(v, list))
        declared = scope.get("count_total")
        if declared is None:
            findings.append(f"NO COUNT   {name}: [scope] declares no count_total to check")
        elif listed != declared:
            findings.append(
                f"COUNT DRIFT {name}: [scope] enumerates {listed} mnemonic(s), "
                f"count_total = {declared}")
        # the two part-counts must also add up to the whole
        a, b = scope.get("count_base"), scope.get("count_rv64i_additions")
        if a is not None and b is not None and declared is not None and a + b != declared:
            findings.append(
                f"PARTS DRIFT {name}: count_base {a} + count_rv64i_additions {b} != {declared}")

    decisions = d.get("decision", [])
    if not decisions:
        findings.append(f"NO DECISIONS {name}: a profile with no recorded decision records nothing")
    ids = set()
    for dec in decisions:
        did = dec.get("id", "<unnamed>")
        if did in ids:
            findings.append(f"DUPLICATE ID {name}: decision id '{did}' appears twice")
        ids.add(did)
        auth = dec.get("authority")
        if auth not in AUTHORITIES:
            findings.append(
                f"BAD AUTHORITY {name}/{did}: '{auth}' not in {sorted(AUTHORITIES)}")
        if not dec.get("source"):
            findings.append(f"NO SOURCE  {name}/{did}: decision cites nothing")
        if not dec.get("statement"):
            findings.append(f"NO STATEMENT {name}/{did}: decision states nothing")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/p"
  good() { cat > "$t/p/profile.toml" <<EOF
[scope]
count_base = 2
count_rv64i_additions = 1
count_total = 3
a = ["X", "Y"]
b = ["Z"]
[[decision]]
id = "D-1"
authority = "architecture"
statement = "s"
source = "§1"
EOF
  }
  arm() { # name expected_rc expected_substring
    out="$(check_profiles "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'PROFILE-CONSISTENCY self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'PROFILE-CONSISTENCY self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }
  good;                                                       arm "GREEN consistent profile"  0 "__CHECKED__ 1"
  good; sed -i.bak 's/count_total = 3/count_total = 4/' "$t/p/profile.toml"
                                                              arm "RED   count drifts from enumeration" 1 "COUNT DRIFT"
  good; sed -i.bak 's/count_base = 2/count_base = 9/' "$t/p/profile.toml"
                                                              arm "RED   parts do not sum"     1 "PARTS DRIFT"
  good; sed -i.bak 's/authority = "architecture"/authority = "vibes"/' "$t/p/profile.toml"
                                                              arm "RED   unknown authority"    1 "BAD AUTHORITY"
  good; sed -i.bak '/source = /d' "$t/p/profile.toml"
                                                              arm "RED   decision cites nothing" 1 "NO SOURCE"
  good; printf '[[decision]]\nid = "D-1"\nauthority = "laboratory"\nstatement = "s"\nsource = "x"\n' >> "$t/p/profile.toml"
                                                              arm "RED   duplicate decision id" 1 "DUPLICATE ID"
  good; python3 - "$t/p/profile.toml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
p.write_text(s.split("[[decision]]")[0])
PY
                                                              arm "RED   no decisions at all"  1 "NO DECISIONS"
  printf 'not = toml = at = all\n' > "$t/p/profile.toml";     arm "RED   unparseable profile"  1 "UNPARSEABLE"
  rm -rf "$t"
  printf 'PROFILE-CONSISTENCY --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -d profiles ] || { echo "PROFILE-CONSISTENCY: ok (no profiles/ yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "PROFILE-CONSISTENCY: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_profiles profiles)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -ne 0 ]; then
  { echo "PROFILE-CONSISTENCY: a profile dossier contradicts itself or cites nothing."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  Fix the enumeration or the count — never the count alone to make them agree."; } >&2
  exit 1
fi
printf 'PROFILE-CONSISTENCY: ok (%s profile dossier(s) internally consistent)\n' "${count:-0}"
exit 0
