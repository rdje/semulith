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
#   5. `references.toml` records REFERENCE CANDIDATES, and a candidate list is the easiest
#      document in a project to fill in from reputation. `SRC-03` forbids recording availability
#      that has not been established, so an `obtained` candidate must name the binary AND its
#      digest AND how it is invoked. ⭐ And every candidate must carry a `lineage` field, because
#      `EVD-04`'s question — do two comparators share semantic ancestry? — is precisely the field
#      that gets skipped when three models are sitting there apparently agreeing.
#   6. An EXPERIMENT that claims agreement must record the CONTROL that was observed failing.
#      ⭐ This is `TOOLBOX.md`'s rule one level up: a gate never seen RED is not known to work,
#      and a *comparison* never seen to diverge is not known to detect divergence. An
#      experiment row saying "the two models agree" with no control is the most convincing
#      wrong record a project can hold, because it is true and worthless at the same time.
#   7. Every PAIR of models an experiment compares must have an INDEPENDENCE row. ⭐ This is the
#      rule with real teeth, and it is `EVD-04` made mechanical: two tools with different names
#      are not two opinions, and the moment a project records "model A and model B agree" it has
#      taken a position on their independence whether or not it has looked. An unexamined pair
#      reads exactly like an independent one, so the gate requires the row to EXIST — it does not
#      require the verdict to be favourable. `not-examined` is a legal, honest answer; silence
#      is not.
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

    # ---- references.toml, when present: the reference candidate dossier ----------------
    refs_path = toml_path.parent / "references.toml"
    if refs_path.is_file():
        STATUSES = {"obtained", "not obtained", "reachable, not acquired"}
        # An `obtained` candidate claims we HAVE it. These are the fields that make the claim
        # checkable rather than remembered.
        OBTAINED_REQUIRED = ("binary", "binary_sha256", "invocation", "trace_granularity",
                             "injection", "terms")
        try:
            rf = tomllib.loads(refs_path.read_text())
        except Exception as e:
            findings.append(f"UNPARSEABLE {name}/references.toml — {e}")
            rf = None
        if rf is not None:
            if rf.get("profile") != d.get("profile", {}).get("id"):
                findings.append(
                    f"REF PROFILE MISMATCH {name}: references.toml profile "
                    f"{rf.get('profile')!r} != profile.toml id {d.get('profile', {}).get('id')!r}")
            cands = rf.get("candidate", [])
            if not cands:
                findings.append(
                    f"NO CANDIDATES {name}/references.toml: a reference dossier with no candidate "
                    f"records nothing — an empty list is not the same as an examined one")
            seen = set()
            for c in cands:
                cid = c.get("id", "<unnamed>")
                if cid in seen:
                    findings.append(f"DUPLICATE CANDIDATE {name}: '{cid}' appears twice")
                seen.add(cid)
                st = c.get("status")
                if st not in STATUSES:
                    findings.append(
                        f"BAD STATUS {name}/{cid}: '{st}' not in {sorted(STATUSES)}")
                if not c.get("role"):
                    findings.append(f"NO ROLE    {name}/{cid}: candidate states no role")
                if not c.get("origin"):
                    findings.append(f"NO ORIGIN  {name}/{cid}: candidate cites no origin")
                if not c.get("lineage"):
                    findings.append(
                        f"NO LINEAGE {name}/{cid}: EVD-04 asks whether two comparators share "
                        f"semantic ancestry; a candidate with no lineage field leaves that "
                        f"unasked, and unasked reads exactly like independent")
                if st == "obtained":
                    for k in OBTAINED_REQUIRED:
                        if not c.get(k):
                            findings.append(
                                f"UNEARNED OBTAINED {name}/{cid}: status is 'obtained' with no "
                                f"'{k}' — SRC-03 forbids recording availability that has not "
                                f"been established")
                elif not c.get("status_reason"):
                    findings.append(
                        f"NO REASON  {name}/{cid}: status is '{st}' with no status_reason; "
                        f"SRC-02 makes an honest 'no route' legitimate, but it has to say why")
            for x in rf.get("experiment", []):
                xid = x.get("id", "<unnamed>")
                for k in ("program", "models", "verdict", "reproduced"):
                    if not x.get(k):
                        findings.append(
                            f"THIN EXPERIMENT {name}/{xid}: no '{k}' — an experiment record "
                            f"without it cannot be re-run or judged")
                if not x.get("control"):
                    findings.append(
                        f"NO CONTROL {name}/{xid}: the experiment reports a verdict with no "
                        f"control that was observed FAILING. A comparison never seen to diverge "
                        f"is not known to detect divergence")
            # 7. every compared pair has an independence row (the verdict may be anything)
            INDEPENDENCE_VERDICTS = {
                "shared", "not-shared", "no-evidence-of-sharing", "not-examined"}
            examined: set[frozenset] = set()
            for ind in rf.get("independence", []):
                pair = ind.get("pair") or []
                label = "/".join(pair) if pair else "<unpaired>"
                if len(pair) != 2:
                    findings.append(
                        f"BAD PAIR   {name}/{label}: an independence record names "
                        f"{len(pair)} model(s); independence is a property of a PAIR")
                else:
                    examined.add(frozenset(pair))
                    for m in pair:
                        if m not in seen:
                            findings.append(
                                f"UNKNOWN MODEL {name}/{label}: '{m}' is not a candidate "
                                f"in this dossier")
                if ind.get("verdict") not in INDEPENDENCE_VERDICTS:
                    findings.append(
                        f"BAD VERDICT {name}/{label}: '{ind.get('verdict')}' not in "
                        f"{sorted(INDEPENDENCE_VERDICTS)}")
                for k in ("subsystem", "evidence", "consequence"):
                    if not ind.get(k):
                        findings.append(
                            f"THIN INDEPENDENCE {name}/{label}: no '{k}' — "
                            f"EVD-04 asks for the examination, not the conclusion")
            for x in rf.get("experiment", []):
                models = x.get("models") or []
                for i in range(len(models)):
                    for j in range(i + 1, len(models)):
                        if frozenset((models[i], models[j])) not in examined:
                            findings.append(
                                f"UNEXAMINED PAIR {name}/{x.get('id','<unnamed>')}: the "
                                f"experiment compares '{models[i]}' with '{models[j]}' and no "
                                f"independence record examines that pair. Recording that two "
                                f"models agree takes a position on their independence whether "
                                f"or not anyone looked; 'not-examined' is a legal verdict, "
                                f"silence is not")
            for dfn in rf.get("difference", []):
                did2 = dfn.get("id", "<unnamed>")
                for k in ("kind", "observed", "resolution"):
                    if not dfn.get(k):
                        findings.append(
                            f"THIN DIFFERENCE {name}/{did2}: no '{k}' — gate G0 asks for "
                            f"differences to be enumerated, which means stated and dispositioned")
            for a in rf.get("attempt", []):
                for k in ("what", "outcome", "consequence"):
                    if not a.get(k):
                        findings.append(
                            f"THIN ATTEMPT {name}/references.toml: an attempt record lacks '{k}' "
                            f"— an attempt without its consequence is a note, not evidence")

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
  # ⛔ STRICT ARITY — docs/knowledge/self-test-arms-that-never-ran.md. A helper that ignores
  # surplus arguments swallows the whole following command when a `;` is missing, silently.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'PROFILE-CONSISTENCY self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # name expected_rc expected_substring
    argc 3 "$#" arm || return
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
  # ---- references.toml: the reference candidate dossier ------------------------------------
  good; printf '[profile]\nid = "p1"\n' >> "$t/p/profile.toml"
  refs() { argc 1 "$#" refs || return; printf '%s\n' "$1" > "$t/p/references.toml"; }
  FULL='profile = "p1"
[[candidate]]
id = "c1"
role = "oracle"
status = "obtained"
origin = "https://example.invalid"
lineage = "written independently"
binary = "b"
binary_sha256 = "deadbeef"
invocation = "b --run"
trace_granularity = "per instruction"
injection = "gdb"
terms = "BSD-2-Clause"
[[attempt]]
what = "tried x"
outcome = "failed"
consequence = "recorded"'
  refs "$FULL";                                               arm "GREEN complete reference dossier" 0 "__CHECKED__ 1"
  refs "$(printf '%s' "$FULL" | grep -v '^lineage')";         arm "RED   a candidate with no lineage" 1 "NO LINEAGE"
  refs "$(printf '%s' "$FULL" | grep -v '^binary_sha256')";   arm "RED   obtained with no digest"   1 "UNEARNED OBTAINED"
  refs "$(printf '%s' "$FULL" | grep -v '^invocation')";      arm "RED   obtained with no invocation" 1 "UNEARNED OBTAINED"
  refs "$(printf '%s' "$FULL" | sed 's/^status = "obtained"/status = "rumoured"/')"
                                                              arm "RED   an unknown status"         1 "BAD STATUS"
  refs "$(printf '%s' "$FULL" | sed 's/^status = "obtained"/status = "not obtained"/')"
                                                              arm "RED   not obtained with no reason" 1 "NO REASON"
  refs "$(printf '%s' "$FULL" | grep -v '^role')";            arm "RED   a candidate with no role"  1 "NO ROLE"
  refs "$(printf '%s' "$FULL" | grep -v '^origin')";          arm "RED   a candidate citing nothing" 1 "NO ORIGIN"
  refs "$(printf '%s' "$FULL" | sed 's/^profile = "p1"/profile = "other"/')"
                                                              arm "RED   dossier names another profile" 1 "REF PROFILE MISMATCH"
  refs "$(printf '%s' "$FULL" | grep -v '^consequence')";     arm "RED   an attempt with no consequence" 1 "THIN ATTEMPT"
  refs 'profile = "p1"';                                      arm "RED   a dossier with no candidate" 1 "NO CANDIDATES"
  refs "$FULL
[[candidate]]
id = \"c1\"
role = \"dup\"
status = \"not obtained\"
status_reason = \"r\"
origin = \"o\"
lineage = \"l\"";                                             arm "RED   a duplicate candidate id" 1 "DUPLICATE CANDIDATE"
  refs 'not = toml = at = all';                               arm "RED   an unparseable dossier"    1 "UNPARSEABLE"
  EXP="$FULL
[[experiment]]
id = \"e1\"
program = \"g.s\"
models = [\"c1\"]
verdict = \"AGREE\"
reproduced = \"yes\"
control = \"observed failing when a value was falsified\"
[[difference]]
id = \"d1\"
kind = \"harness\"
observed = \"they differ\"
resolution = \"normalized\""
  refs "$EXP";                                                arm "GREEN a complete experiment record" 0 "__CHECKED__ 1"
  refs "$(printf '%s' "$EXP" | grep -v '^control = ')";       arm "RED   agreement with no control" 1 "NO CONTROL"
  refs "$(printf '%s' "$EXP" | grep -v '^reproduced = ')";    arm "RED   an experiment that never reproduced" 1 "THIN EXPERIMENT"
  refs "$(printf '%s' "$EXP" | grep -v '^observed = ')";      arm "RED   a difference with nothing observed" 1 "THIN DIFFERENCE"
  # ---- independence (EVD-04) -------------------------------------------------------------
  C2='
[[candidate]]
id = "c2"
role = "second"
status = "not obtained"
status_reason = "not needed for this fixture"
origin = "https://example.invalid/2"
lineage = "unknown"'
  IND_ROW='
[[independence]]
subsystem = "integer"
pair = ["c1", "c2"]
verdict = "not-examined"
evidence = "none"
consequence = "owner named"'
  refs "$EXP$C2$IND_ROW";                                     arm "GREEN an independence record parses" 0 "__CHECKED__ 1"
  refs "$EXP$C2$(printf '%s' "$IND_ROW" | sed 's/not-examined/probably fine/')"
                                                              arm "RED   an unknown independence verdict" 1 "BAD VERDICT"
  refs "$EXP$C2$(printf '%s' "$IND_ROW" | sed 's/pair = \["c1", "c2"\]/pair = ["c1"]/')"
                                                              arm "RED   independence claimed of one model" 1 "BAD PAIR"
  refs "$EXP$C2$(printf '%s' "$IND_ROW" | sed '/^evidence = /d')"
                                                              arm "RED   an independence verdict with no examination" 1 "THIN INDEPENDENCE"
  refs "$EXP$C2$(printf '%s' "$IND_ROW" | sed 's/pair = \["c1", "c2"\]/pair = ["c1", "c9"]/')"
                                                              arm "RED   independence names a model that is not a candidate" 1 "UNKNOWN MODEL"
  # an experiment comparing TWO models with no independence record for that pair
  refs "$(printf '%s' "$EXP" | sed 's/^models = \["c1"\]/models = ["c1", "c2"]/')$C2"
                                                              arm "RED   two models compared, pair never examined" 1 "UNEXAMINED PAIR"
  rm -f "$t/p/references.toml"

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
    echo "  The SOURCE is authoritative: fix the enumeration, the citation or the evidence —"
    echo "  never the summary alone to make the two agree."; } >&2
  exit 1
fi
printf 'PROFILE-CONSISTENCY: ok (%s profile dossier(s) internally consistent)\n' "${count:-0}"
exit 0
