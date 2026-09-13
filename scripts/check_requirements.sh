#!/usr/bin/env bash
# scripts/check_requirements.sh — RECORD-SCHEMA (project doctrine).
#
# `schemas/` holds this project's data contracts and `EVD-01` makes machine-readable requirement,
# evidence and obligation records the spine of traceability. A record file that has drifted from
# its schema, or that cites a source the project never pinned, is worse than no catalogue: it is a
# catalogue that looks checkable and is not.
#
# What is checked, beyond schema validity:
#   1. SCHEMA     every tracked `.jsonl` record file validates against its declared schema.
#   2. CITED      every `source_refs.source_id` in a profile's requirements names a source that
#                 profile's `sources.toml` actually pins. `SRC-03` again, one layer up: a locator
#                 into a document nobody acquired is not a citation.
#   3. RESOLVED   a record claiming `research_status: resolved` may not also carry an `OPEN:` note.
#                 ⭐ "Resolved with a known open question" is the single most convenient lie a
#                 requirements catalogue can tell, because both halves are individually true.
#   4. COVERAGE   every `[[decision]]` in `profile.toml` has a requirement, and the requirement's
#                 statement is IDENTICAL to the decision's. Two files stating the same rule in
#                 different words is how a catalogue quietly stops describing its profile.
#   5. LINKED     every id in `dependencies` names a requirement that exists in the same file.
#   6. OBLIGED    every `obligation_ids` entry names an obligation the profile's contract defines,
#                 and every obligation carries BOTH a positive and a negative required check.
#                 ⭐ Positive-only checks are how a contract comes to describe only the cases that
#                 already work: `docs/CPU_ENVIRONMENT.md` §4 asks for negative fixtures that must
#                 be reported as CONTRACT VIOLATIONS rather than target exceptions.
#   7. AUTHORITY  an obligation whose requirement is architecturally `defined` must itself carry
#                 `authority: architecture`. ⛔ This is the mechanical form of the contract's first
#                 rule — *laboratory policy cannot override an architectural requirement* — and it
#                 bites in the direction that matters: labelling an ISA rule as a harness choice
#                 is what turns a defect into a "profile difference" and makes it unfalsifiable.
#
# ✅ The gap `P0-PROFILE.3` declared here — obligation ids checked against nothing — is CLOSED by
# rules 6 and 7, which `P0-PROFILE.4` added along with the contract that defines them.
#
# ⛔ The validator it calls REFUSES on any JSON Schema keyword it does not implement, so a schema
# gaining a new keyword breaks this gate loudly rather than silently widening what passes.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "RECORD-SCHEMA: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_records() {
python3 - "$1" <<'PY'
import json, re, sys, pathlib, tomllib
sys.path.insert(0, "scripts")
from validate_records import validate_jsonl, UnsupportedSchema

root = pathlib.Path(sys.argv[1])
findings, checked = [], 0

# which schema governs which record file, by basename
SCHEMA_FOR = {
    "requirements.jsonl": "requirement.schema.json",
    "evidence.jsonl": "evidence.schema.json",
    "contract-obligations.jsonl": "contract-obligation.schema.json",
}
# contract authority vocabulary, for rule 7
ARCH_AUTHORITY = "architecture"

# ⛔ Exclude `target/` only when it is the FIRST component RELATIVE TO ROOT. A first cut wrote
# `"target" not in p.parts`, which tests the ABSOLUTE path — and this check's own self-test
# fixtures live under `target/doctrine-selftest/`, so every fixture was filtered away and ten
# arms failed with "no .jsonl record file found". The arms caught it; a reviewer would not have.
def _excluded(p):
    rel = p.relative_to(root).parts
    return bool(rel) and rel[0] == "target"

record_files = sorted(p for p in root.rglob("*.jsonl") if not _excluded(p))
if not record_files:
    print("NO RECORDS no .jsonl record file found — this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

for rf in record_files:
    schema_name = SCHEMA_FOR.get(rf.name)
    if schema_name is None:
        findings.append(f"UNGOVERNED {rf}: no schema is declared for this record file")
        continue
    schema = root / "schemas" / schema_name
    if not schema.is_file():
        findings.append(f"NO SCHEMA  {rf}: {schema} does not exist")
        continue
    checked += 1
    # 1. SCHEMA
    try:
        for err in validate_jsonl(rf, schema):
            findings.append(f"INVALID    {err}")
    except UnsupportedSchema as exc:
        print(f"UNSUPPORTED {exc}"); print("__CHECKED__ 0"); sys.exit(2)

    if rf.name != "requirements.jsonl":
        continue
    # ⛔ The cross-checks below need parsed records. A file that failed to parse has already been
    # reported by rule 1, and re-parsing it here would CRASH the gate rather than fail it — a
    # traceback is not a verdict. Caught by the malformed-line arm, not by review.
    try:
        recs = [json.loads(l) for l in rf.read_text().splitlines() if l.strip()]
    except json.JSONDecodeError:
        continue
    ids = {r.get("id") for r in recs}

    # 2. CITED — only for a requirements file living inside a profile directory
    sources_toml = rf.parent / "sources.toml"
    if sources_toml.is_file():
        pinned = {s["id"] for s in tomllib.loads(sources_toml.read_text()).get("source", [])}
        for r in recs:
            for sr in r.get("source_refs", []):
                if sr["source_id"] not in pinned:
                    findings.append(
                        f"UNPINNED SOURCE {rf.name} [{r['id']}]: cites '{sr['source_id']}', which "
                        f"{sources_toml.name} does not pin — a locator into a document nobody "
                        f"acquired is not a citation")

    for r in recs:
        # 3. RESOLVED
        detail = (r.get("source_semantics") or {}).get("detail", "")
        if r.get("research_status") == "resolved" and "OPEN:" in detail:
            findings.append(
                f"RESOLVED WITH AN OPEN QUESTION {rf.name} [{r['id']}]: research_status is "
                f"'resolved' and the record still carries an OPEN note. Both halves can be true "
                f"separately; together they are a catalogue lying about its own completeness")
        # 5. LINKED
        for dep in r.get("dependencies", []):
            if dep not in ids:
                findings.append(
                    f"DANGLING DEP {rf.name} [{r['id']}]: depends on '{dep}', which no record "
                    f"in this file defines")

    # 6 + 7. OBLIGED / AUTHORITY — against the contract in the same PROFILE directory.
    # ⛔ Scoped to a catalogue that sits beside a `profile.toml`. The shipped `examples/` files
    # are frozen delivery artifacts illustrating the SCHEMA, not a profile's contract, and they
    # are referentially inconsistent as delivered — which `--audit` reports without failing,
    # because a `frozen-in-place` artifact must not be edited to satisfy a later rule.
    ob_file = rf.parent / "contract-obligations.jsonl"
    if ob_file.is_file() and (rf.parent / "profile.toml").is_file():
        try:
            obs = [json.loads(l) for l in ob_file.read_text().splitlines() if l.strip()]
        except json.JSONDecodeError:
            obs = None
        if obs is not None:
            by_ob = {o.get("id"): o for o in obs}
            for o in obs:
                checks = o.get("required_checks", [])
                if not any(c.endswith("-POS") for c in checks) or \
                   not any(c.endswith("-NEG") for c in checks):
                    findings.append(
                        f"NO NEGATIVE CHECK {ob_file.name} [{o.get('id')}]: required_checks "
                        f"{checks} lack a positive AND a negative fixture — a contract with only "
                        f"positive checks describes the cases that already work")
            for r in recs:
                for oid in r.get("obligation_ids", []):
                    o = by_ob.get(oid)
                    if o is None:
                        findings.append(
                            f"UNDEFINED OBLIGATION {rf.name} [{r['id']}]: names '{oid}', which "
                            f"{ob_file.name} does not define")
                        continue
                    cat = (r.get("source_semantics") or {}).get("category")
                    if cat == "defined" and o.get("authority") != ARCH_AUTHORITY:
                        findings.append(
                            f"AUTHORITY DOWNGRADE {ob_file.name} [{oid}]: its requirement "
                            f"'{r['id']}' is architecturally 'defined', but the obligation claims "
                            f"authority '{o.get('authority')}'. Laboratory policy cannot override "
                            f"an architectural requirement, and mislabelling one is how a defect "
                            f"becomes an unfalsifiable 'profile difference'")

    # 4. COVERAGE — against the profile this catalogue belongs to
    prof = rf.parent / "profile.toml"
    if prof.is_file():
        decisions = tomllib.loads(prof.read_text()).get("decision", [])
        by_id = {r.get("id"): r for r in recs}
        for dec in decisions:
            rid = f"REQ-{dec['id']}"
            if rid not in by_id:
                findings.append(
                    f"UNCOVERED DECISION {rf.name}: profile.toml decision '{dec['id']}' has no "
                    f"requirement '{rid}'")
            elif by_id[rid].get("statement") != dec.get("statement"):
                findings.append(
                    f"STATEMENT DRIFT {rf.name} [{rid}]: the requirement no longer states what "
                    f"profile.toml's '{dec['id']}' states")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/schemas" "$t/p" "$t/scripts"
  cp schemas/requirement.schema.json schemas/contract-obligation.schema.json "$t/schemas/"
  ln -sf "$ROOT/scripts/validate_records.py" "$t/scripts/validate_records.py"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'RECORD-SCHEMA self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  REC='{"id":"REQ-D-A","profile_ids":["p"],"kind":"state","statement":"S","source_refs":[{"source_id":"SRC-A","locator":"§1"}],"applicability":"included","research_status":"resolved","implementation_status":"planned","source_semantics":{"category":"defined","detail":"d"},"risk":"low","obligation_ids":["OB-A"],"dependencies":[],"implementation_refs":[],"evidence_ids":[]}'
  fixture() { argc 1 "$#" fixture || return; printf '%s\n' "$1" > "$t/p/requirements.jsonl"; }
  profile() { argc 1 "$#" profile || return; printf '%s\n' "$1" > "$t/p/profile.toml"; }
  sources() { argc 1 "$#" sources || return; printf '%s\n' "$1" > "$t/p/sources.toml"; }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_records "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'RECORD-SCHEMA self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'RECORD-SCHEMA self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  sources '[[source]]
id = "SRC-A"
file = "a.html"'
  profile '[[decision]]
id = "D-A"
authority = "architecture"
statement = "S"
source = "SRC-A §1"'
  fixture "$REC";                                             arm "GREEN a covered, cited, valid record" 0 "__CHECKED__ 1"
  fixture "$(printf '%s' "$REC" | sed 's/"risk":"low"/"risk":"apocalyptic"/')"
                                                              arm "RED   a record that fails its schema" 1 "INVALID"
  fixture "$(printf '%s' "$REC" | sed 's/"SRC-A"/"SRC-NOWHERE"/')"
                                                              arm "RED   cites a source nobody pinned" 1 "UNPINNED SOURCE"
  fixture "$(printf '%s' "$REC" | sed 's/"detail":"d"/"detail":"d OPEN: something"/')"
                                                              arm "RED   resolved while carrying an open question" 1 "RESOLVED WITH AN OPEN QUESTION"
  fixture "$(printf '%s' "$REC" | sed 's/"dependencies":\[\]/"dependencies":["REQ-D-GHOST"]/')"
                                                              arm "RED   depends on a record that does not exist" 1 "DANGLING DEP"
  fixture "$(printf '%s' "$REC" | sed 's/"statement":"S"/"statement":"something else"/')"
                                                              arm "RED   the requirement no longer states the decision" 1 "STATEMENT DRIFT"
  profile '[[decision]]
id = "D-B"
authority = "architecture"
statement = "T"
source = "SRC-A §2"'
  fixture "$REC";                                             arm "RED   a profile decision with no requirement" 1 "UNCOVERED DECISION"
  profile '[[decision]]
id = "D-A"
authority = "architecture"
statement = "S"
source = "SRC-A §1"'
  printf 'not json at all\n' > "$t/p/requirements.jsonl";      arm "RED   a malformed record line" 1 "not valid JSON"
  : > "$t/p/requirements.jsonl";                               arm "RED   an empty record file"   1 "contains no records"
  # ---- rules 6 and 7: the contract ---------------------------------------------------------
  OB='{"id":"OB-A","contract_id":"c","contract_version":"0","profile_ids":["p"],"direction":"cpu-guarantee","statement":"S","authority":"architecture","source_refs":[{"source_id":"SRC-A","locator":"§1"}],"parameters":{},"dependencies":[],"required_checks":["CHK-A-POS","CHK-A-NEG"]}'
  obligations() { argc 1 "$#" obligations || return; printf '%s\n' "$1" > "$t/p/contract-obligations.jsonl"; }
  fixture "$REC"; obligations "$OB";                          arm "GREEN requirement, contract and profile agree" 0 "__CHECKED__ 2"
  obligations "$(printf '%s' "$OB" | sed 's/"CHK-A-POS","CHK-A-NEG"/"CHK-A-POS"/')"
                                                              arm "RED   an obligation with no negative fixture" 1 "NO NEGATIVE CHECK"
  obligations "$(printf '%s' "$OB" | sed 's/"id":"OB-A"/"id":"OB-OTHER"/')"
                                                              arm "RED   a requirement names an undefined obligation" 1 "UNDEFINED OBLIGATION"
  obligations "$(printf '%s' "$OB" | sed 's/"authority":"architecture"/"authority":"laboratory"/')"
                                                              arm "RED   an architectural rule labelled a laboratory choice" 1 "AUTHORITY DOWNGRADE"
  obligations "$OB"
  rm -f "$t/p/contract-obligations.jsonl"
  fixture "$REC"; cp "$t/p/requirements.jsonl" "$t/p/mystery.jsonl"
                                                              arm "RED   a record file no schema governs" 1 "UNGOVERNED"
  rm -f "$t/p/mystery.jsonl"
  rm -f "$t/p/requirements.jsonl";                             arm "REFUSE nothing to check at all" 2 "NO RECORDS"

  rm -rf "$t"
  printf 'RECORD-SCHEMA --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

# --audit: report referential problems in record files the gate deliberately does NOT enforce,
# so a known gap stays re-derivable instead of becoming prose someone has to remember.
if [ "${1:-}" = "--audit" ]; then
python3 - <<'AUDITPY'
import json, pathlib
for d in sorted({p.parent for p in pathlib.Path(".").rglob("*.jsonl") if "target" not in p.parts}):
    rq, ob = d / "requirements.jsonl", d / "contract-obligations.jsonl"
    if not (rq.is_file() and ob.is_file()):
        continue
    enforced = (d / "profile.toml").is_file()
    reqs = [json.loads(l) for l in rq.read_text().splitlines() if l.strip()]
    obs = [json.loads(l) for l in ob.read_text().splitlines() if l.strip()]
    defined = {o["id"] for o in obs}
    named = {oid for r in reqs for oid in r.get("obligation_ids", [])}
    print(f"{d}/  ({'ENFORCED' if enforced else 'advisory - frozen delivery artifacts'})")
    print(f"  requirements {len(reqs)} | obligations {len(obs)}")
    print(f"  named but undefined : {sorted(named - defined) or 'none'}")
    # An environment ASSUMPTION is a thing the harness must satisfy; no CPU requirement names
    # one, so "unnamed" is correct for it and only a cpu-guarantee going unnamed is a finding.
    by_dir = {o["id"]: o.get("direction") for o in obs}
    unnamed = sorted(defined - named)
    print(f"  unnamed environment-assumptions (expected) : "
          f"{[i for i in unnamed if by_dir.get(i) == 'environment-assumption'] or 'none'}")
    print(f"  unnamed cpu-guarantees (a finding)        : "
          f"{[i for i in unnamed if by_dir.get(i) != 'environment-assumption'] or 'none'}")
    missing_neg = [o["id"] for o in obs
                   if not any(c.endswith("-NEG") for c in o.get("required_checks", []))]
    print(f"  obligations with no negative check : {missing_neg or 'none'}")
AUDITPY
  exit 0
fi

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -d schemas ] || { echo "RECORD-SCHEMA: ok (no schemas/ yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "RECORD-SCHEMA: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_records .)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "RECORD-SCHEMA: REFUSED — the record corpus or a schema could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "RECORD-SCHEMA: a record file contradicts its schema, its sources, or its profile."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The SCHEMA and the PROFILE are authoritative. Fix the record, not the contract."; } >&2
  exit 1
fi
printf 'RECORD-SCHEMA: ok (%s record file(s) validate and agree with their profile)\n' "${count:-0}"
exit 0
