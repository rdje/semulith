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
#   3. An EMPTY `hidden_state` list in `state.json` is a universal claim over a set — "nothing
#      else can influence a future observation" — and it is false the moment one such thing
#      exists. So an empty list must be backed by a CENSUS that enumerates what was considered
#      and found absent. This is `GAP-CLAIM-CENSUS` applied to data rather than to prose: an
#      unearned "none" is indistinguishable from a "none" nobody looked for.
#   4. `state.json` and `profile.toml` must AGREE. Two files describing the same processor is
#      the cheapest place for a contradiction to hide.
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
# `software-convention` is legal only in state.json, for ABI roles: the calling convention is
# neither architecture nor an EEI choice, and recording an ABI name as architectural is the
# mistake `docs/INFORMATION_CATALOG.md` §6 names explicitly.
STATE_AUTHORITIES = AUTHORITIES | {"software-convention"}
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

    # ---- state.json, when present: agreement with profile.toml, and an earned census ----
    state_path = toml_path.parent / "state.json"
    if state_path.is_file():
        import json
        try:
            st = json.loads(state_path.read_text())
        except Exception as e:
            findings.append(f"UNPARSEABLE {name}/state.json — {e}")
            st = None
        if st is not None:
            if st.get("profile_id") != d.get("profile", {}).get("id"):
                findings.append(
                    f"ID MISMATCH {name}: state.json profile_id "
                    f"{st.get('profile_id')!r} != profile.toml id {d.get('profile', {}).get('id')!r}")
            if st.get("xlen") != d.get("profile", {}).get("xlen"):
                findings.append(
                    f"XLEN MISMATCH {name}: state.json {st.get('xlen')} != profile.toml "
                    f"{d.get('profile', {}).get('xlen')}")
            want_regs = d.get("state", {}).get("integer_registers")
            got_regs = (st.get("integer_registers") or {}).get("count")
            if want_regs is not None and got_regs != want_regs:
                findings.append(
                    f"REG COUNT MISMATCH {name}: state.json {got_regs} != profile.toml {want_regs}")
            def authorities(o):
                if isinstance(o, dict):
                    if "authority" in o and isinstance(o["authority"], str):
                        yield o["authority"]
                    for v in o.values():
                        yield from authorities(v)
                elif isinstance(o, list):
                    for v in o:
                        yield from authorities(v)
            for a in authorities(st):
                if a not in STATE_AUTHORITIES:
                    findings.append(
                        f"BAD AUTHORITY {name}/state.json: '{a}' not in {sorted(STATE_AUTHORITIES)}")
            if "hidden_state" in st and not st["hidden_state"]:
                census = st.get("hidden_state_census")
                cands = (census or {}).get("candidates_checked") or []
                if not cands:
                    findings.append(
                        f"UNEARNED NONE {name}/state.json: hidden_state is empty with no census. "
                        f"'nothing else can influence a future observation' is a claim over a set, "
                        f"false the moment one exists — enumerate what was considered.")
                else:
                    for c in cands:
                        if "present" not in c or not c.get("why"):
                            findings.append(
                                f"THIN CENSUS {name}/state.json: candidate "
                                f"{c.get('candidate','<unnamed>')!r} lacks present/why")

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
  # state.json arms
  good; cat > "$t/p/state.json" <<'EOF'
{"profile_id": "p1", "xlen": 64, "integer_registers": {"count": 4},
 "hidden_state": [], "hidden_state_census": {"candidates_checked": [{"candidate": "c", "present": false, "why": "w"}]}}
EOF
  printf '[profile]\nid = "p1"\nxlen = 64\n[state]\ninteger_registers = 4\n' >> "$t/p/profile.toml"
                                                              arm "GREEN state agrees with profile" 0 "__CHECKED__ 1"
  python3 -c "
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text()); d.pop('hidden_state_census'); p.write_text(json.dumps(d))" "$t/p/state.json"
                                                              arm "RED   empty hidden_state, no census" 1 "UNEARNED NONE"
  python3 -c "
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text()); d['xlen']=32; p.write_text(json.dumps(d))" "$t/p/state.json"
                                                              arm "RED   xlen disagrees"        1 "XLEN MISMATCH"
  python3 -c "
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text()); d['xlen']=64; d['integer_registers']={'count':9}; p.write_text(json.dumps(d))" "$t/p/state.json"
                                                              arm "RED   register count disagrees" 1 "REG COUNT MISMATCH"
  python3 -c "
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text()); d['integer_registers']={'count':4,'authority':'vibes'}; p.write_text(json.dumps(d))" "$t/p/state.json"
                                                              arm "RED   state authority unknown" 1 "BAD AUTHORITY"
  rm -f "$t/p/state.json"
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
