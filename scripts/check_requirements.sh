#!/usr/bin/env bash
# scripts/check_requirements.sh — RECORD-SCHEMA (project doctrine).
#
# `schemas/` holds this project's data contracts and `EVD-01` makes machine-readable requirement,
# evidence and obligation records the spine of traceability. A record file that has drifted from
# its schema, or that cites a source the project never pinned, is worse than no catalogue: it is a
# catalogue that looks checkable and is not.
#
# Two tracks, since `SOT-FORMAT.3` moved the profile catalogues behind the schema layer:
#
#   JSONL — every tracked `.jsonl` record file validates against its declared JSON schema
#           (the frozen `examples/` delivery artifacts stay JSONL on purpose). Power: structural.
#   SEXP  — every `requirements.sexp` / `contract-obligations.sexp` catalogue validates against
#           its schema-layer schema (`schema/requirements.sexp`, `schema/contract-obligations.sexp`)
#           AND carries the cross-checks, now read through scripts/records_sexp.py:
#     2. CITED      every `source_refs.source_id` names a source the profile's `sources.sexp` pins.
#                   `SRC-03` again, one layer up: a locator into a document nobody acquired is
#                   not a citation.
#     3. RESOLVED   a record claiming `research_status: resolved` may not also carry an `OPEN:` note.
#                   ⭐ "Resolved with a known open question" is the single most convenient lie a
#                   requirements catalogue can tell, because both halves are individually true.
#     4. COVERAGE   every (decision …) in `profile.sexp` has a requirement, and the requirement's
#                   statement is IDENTICAL to the decision's. Two files stating the same rule in
#                   different words is how a catalogue quietly stops describing its profile.
#     5. LINKED     every id in `dependencies` names a record that exists in the same file.
#     6. OBLIGED    every `obligation_ids` entry names an obligation the profile's contract defines,
#                   and every obligation carries BOTH a positive and a negative required check.
#                   ⭐ Positive-only checks are how a contract comes to describe only the cases
#                   that already work: `docs/CPU_ENVIRONMENT.md` §4 asks for negative fixtures that
#                   must be reported as CONTRACT VIOLATIONS rather than target exceptions.
#     7. AUTHORITY  an obligation whose requirement is architecturally `defined` must itself carry
#                   `authority: architecture`. ⛔ This is the mechanical form of the contract's
#                   first rule — *laboratory policy cannot override an architectural requirement* —
#                   and it bites in the direction that matters: labelling an ISA rule as a harness
#                   choice is what turns a defect into a "profile difference" and makes it
#                   unfalsifiable.
#     8. UNIQUE-ID  a catalogue may not carry two records with the same id. Found by SOT-FORMAT.5
#                   (design probe, `target/doctrine_scratch/dupprobe`): the id → record map used
#                   for the cross-checks silently collapsed duplicates (last wins), so a catalogue
#                   could contradict itself — same id, different content — and stay green, rc=0.
#                   A catalogue that repeats an id is a catalogue lying about its own identity,
#                   and every rule below would have checked only the survivor.
#     9. MIRROR     an obligation carrying parameters.requirement_id restates that requirement's
#                   statement, so the pair must state EXACTLY the same fact — the obligation is a
#                   derived mirror, and a mirror that drifts is a fact stated in two ungoverned
#                   (MODEL-METHOD.7). The 8 environment-assumptions keep their own statements:
#                   the arm keys on the parameter, not the direction.
#
# ✅ The gap `P0-PROFILE.3` declared here — obligation ids checked against nothing — is CLOSED by
# rules 6 and 7, which `P0-PROFILE.4` added along with the contract that defines them.
#
# ⛔ Both validators REFUSE rather than guess: the JSON one on any keyword it does not implement;
# the schema layer by name on an undeclared construct, field, arity, value type or FACET
# (pattern / min-length / min / unique — SOT-FORMAT.3). A schema gaining power breaks the gate
# loudly rather than silently widening what passes.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "RECORD-SCHEMA: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_records() {
python3 - "$1" <<'PY'
import json, pathlib, sys
sys.path.insert(0, "scripts")
from validate_records import validate_jsonl, UnsupportedSchema
import sexp as S
import records_sexp as R
import dossier_sexp as D
import check_sexp_schema as K

root = pathlib.Path(sys.argv[1])
findings, checked = [], []

# which JSON schema governs which JSONL record file, by basename
SCHEMA_FOR = {
    "requirements.jsonl": "requirement.schema.json",
    "evidence.jsonl": "evidence.schema.json",
    "contract-obligations.jsonl": "contract-obligation.schema.json",
}
# which schema-layer schema governs which converted catalogue, by basename
SEXP_SCHEMA_FOR = {
    "requirements.sexp": "schema/requirements.sexp",
    "contract-obligations.sexp": "schema/contract-obligations.sexp",
}
ARCH_AUTHORITY = "architecture"

# ⛔ Exclude `target/` only when it is the FIRST component RELATIVE TO ROOT (the self-test
# fixtures live under target/doctrine-selftest/, and an absolute-path test would filter every
# fixture away and fail the arms with "nothing found"). `vendor` joins it for the same reason
# and a sharper one: a vendored submodule is ANOTHER PROJECT'S tree.
def _excluded(p):
    rel = p.relative_to(root).parts
    return bool(rel) and rel[0] in ("target", "vendor")

# ---------------------------------------------------------------- the JSONL track (unchanged)
jsonl_files = sorted(p for p in root.rglob("*.jsonl") if not _excluded(p))
for rf in jsonl_files:
    schema_name = SCHEMA_FOR.get(rf.name)
    if schema_name is None:
        findings.append(f"UNGOVERNED {rf}: no schema is declared for this record file")
        continue
    schema = root / "schemas" / schema_name
    if not schema.is_file():
        findings.append(f"NO SCHEMA  {rf}: {schema} does not exist")
        continue
    checked.append(str(rf.relative_to(root)))
    try:
        for err in validate_jsonl(rf, schema):
            findings.append(f"INVALID    {err}")
    except UnsupportedSchema as exc:
        print(f"UNSUPPORTED {exc}"); print("__CHECKED__ 0"); sys.exit(2)

# ------------------------------------------------------- the SEXP track (the profile records)
# A file named requirements.sexp / contract-obligations.sexp is a catalogue everywhere EXCEPT
# under schema/ — the schemas themselves carry the same basenames, and judging a schema as its
# own target is how a gate reports its own grammar as a records violation.
schema_dir = root / "schema"
catalogues = sorted({p for name in SEXP_SCHEMA_FOR for p in root.rglob(name)
                     if not _excluded(p) and schema_dir not in p.parents})
if not jsonl_files and not catalogues:
    print("NO RECORDS no .jsonl record file and no converted catalogue found — "
          "this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

for cat in catalogues:
    schema_rel = SEXP_SCHEMA_FOR[cat.name]
    schema = root / schema_rel
    if not schema.is_file():
        findings.append(f"NO SCHEMA  {cat}: {schema} does not exist")
        continue
    checked.append(str(cat.relative_to(root)))
    # 1. SCHEMA — the schema layer refuses by name: undeclared construct/field, wrong arity,
    #    wrong value type, and every FACET the record contracts carry.
    try:
        constructs, operators = K.load_schema(schema)
        errors = K.validate_file(cat, constructs, operators)
    except (K.SchemaError, S.SexpError) as exc:
        print(f"UNSUPPORTED {schema_rel}: {exc}"); print("__CHECKED__ 0"); sys.exit(2)
    for e in errors:
        findings.append(f"INVALID    {e}")
    if errors:
        continue                    # a catalogue the layer refuses cannot be cross-checked
    try:
        recs = R.load(cat)
    except (R.RecordRefused, S.SexpError) as exc:
        findings.append(f"UNREADABLE {cat.relative_to(root)}: conforms to its schema but does "
                        f"not map to records — {exc}")
        continue
    if not recs:
        findings.append(f"INVALID    {cat.relative_to(root)}: contains no records — an empty "
                        f"catalogue is not a valid one")
        continue
    # 8. UNIQUE-ID — the cross-checks index records by id; a duplicate silently collapses
    #    (last wins) and every rule below would check only the survivor. Refuse, naming both.
    by_id: dict = {}
    for r in recs:
        rid = r.get("id")
        if rid in by_id:
            findings.append(
                f"DUPLICATE ID {cat.relative_to(root)}: record '{rid}' appears more than "
                f"once — a catalogue that contradicts itself cannot be checked; the later "
                f"record silently overwrote the earlier one")
        else:
            by_id[rid] = r

    if cat.name == "requirements.sexp":
        # 2. CITED — beside a profile's sources.sexp (`SOT-FORMAT.4`: read via the mapping)
        sources_sexp = cat.parent / "sources.sexp"
        if sources_sexp.is_file():
            try:
                pinned = {s["id"] for s in D.load_sources(sources_sexp).get("source", [])}
            except D.DossierError:
                pinned = None
            if pinned is None:
                findings.append(
                    f"UNREADABLE {sources_sexp.name}: the pinned-source ledger does not map — "
                    f"a catalogue citing documents a ledger nobody can read proves nothing")
            else:
                for r in recs:
                    for sr in r.get("source_refs", []):
                        if sr["source_id"] not in pinned:
                            findings.append(
                                f"UNPINNED SOURCE {cat.name} [{r['id']}]: cites "
                                f"'{sr['source_id']}', which {sources_sexp.name} does not pin — "
                                f"a locator into a document nobody acquired is not a citation")
        for r in recs:
            # 3. RESOLVED
            detail = (r.get("source_semantics") or {}).get("detail", "")
            if r.get("research_status") == "resolved" and "OPEN:" in detail:
                findings.append(
                    f"RESOLVED WITH AN OPEN QUESTION {cat.name} [{r['id']}]: research_status "
                    f"is 'resolved' and the record still carries an OPEN note. Both halves can "
                    f"be true separately; together they are a catalogue lying about its own "
                    f"completeness")
            # 5. LINKED
            for dep in r.get("dependencies", []):
                if dep not in by_id:
                    findings.append(
                        f"DANGLING DEP {cat.name} [{r['id']}]: depends on '{dep}', which no "
                        f"record in this file defines")

        # 6 + 7. OBLIGED / AUTHORITY — against the contract in the same PROFILE directory
        ob_file = cat.parent / "contract-obligations.sexp"
        if ob_file.is_file() and (cat.parent / "profile.sexp").is_file():
            try:
                obs = R.load(ob_file)
            except (R.RecordRefused, S.SexpError):
                obs = None
            if obs is not None:
                by_ob = {o.get("id"): o for o in obs}
                for o in obs:
                    checks = o.get("required_checks", [])
                    if not any(c.endswith("-POS") for c in checks) or \
                       not any(c.endswith("-NEG") for c in checks):
                        findings.append(
                            f"NO NEGATIVE CHECK contract-obligations.sexp [{o.get('id')}]: "
                            f"required_checks {checks} lack a positive AND a negative fixture — "
                            f"a contract with only positive checks describes the cases that "
                            f"already work")
                for r in recs:
                    for oid in r.get("obligation_ids", []):
                        o = by_ob.get(oid)
                        if o is None:
                            findings.append(
                                f"UNDEFINED OBLIGATION {cat.name} [{r['id']}]: names '{oid}', "
                                f"which contract-obligations.sexp does not define")
                            continue
                        cat_ = (r.get("source_semantics") or {}).get("category")
                        if cat_ == "defined" and o.get("authority") != ARCH_AUTHORITY:
                            findings.append(
                                f"AUTHORITY DOWNGRADE contract-obligations.sexp [{oid}]: its "
                                f"requirement '{r['id']}' is architecturally 'defined', but the "
                                f"obligation claims authority '{o.get('authority')}'. Laboratory "
                                f"policy cannot override an architectural requirement, and "
                                f"mislabelling one is how a defect becomes an unfalsifiable "
                                f"'profile difference'")
                # 9. MIRROR — an obligation that names its requirement restates it; the two must
                #    state the same fact (MODEL-METHOD.7). Keyed on the obligation's own
                #    parameter, not the direction: environment-assumptions keep their statements.
                for o in obs:
                    mirror_rid = (o.get("parameters") or {}).get("requirement_id")
                    if not mirror_rid:
                        continue
                    r = by_id.get(mirror_rid)
                    if r is None:
                        findings.append(
                            f"MIRROR WITHOUT SOURCE contract-obligations.sexp [{o.get('id')}]: "
                            f"names '{mirror_rid}' as its requirement, which "
                            f"{cat.name} does not define — a mirror of nothing")
                    elif o.get("statement") != r.get("statement"):
                        findings.append(
                            f"MIRROR DRIFT contract-obligations.sexp [{o.get('id')}]: names "
                            f"'{mirror_rid}' as its requirement but states a different fact. "
                            f"An obligation is a derived mirror of its requirement; a mirror "
                            f"that drifts is one fact stated two ways")

        # 4. COVERAGE — against the profile this catalogue belongs to
        prof = cat.parent / "profile.sexp"
        if prof.is_file():
            try:
                decisions = D.load_profile(prof).get("decision", [])
            except D.DossierError:
                decisions = None
            if decisions is None:
                findings.append(
                    f"UNREADABLE {prof.name}: the profile's decisions do not map — coverage "
                    f"against a dossier nobody can read proves nothing")
            else:
                for dec in decisions:
                    rid = f"REQ-{dec['id']}"
                    if rid not in by_id:
                        findings.append(
                            f"UNCOVERED DECISION {cat.name}: profile.sexp decision '{dec['id']}' "
                            f"has no requirement '{rid}'")
                    elif by_id[rid].get("statement") != dec.get("statement"):
                        findings.append(
                            f"STATEMENT DRIFT {cat.name} [{rid}]: the requirement no longer "
                            f"states what profile.sexp's '{dec['id']}' states")

    else:  # contract-obligations.sexp — the NO NEGATIVE CHECK arm is fired standalone too
        for o in recs:
            checks = o.get("required_checks", [])
            if not any(c.endswith("-POS") for c in checks) or \
               not any(c.endswith("-NEG") for c in checks):
                findings.append(
                    f"NO NEGATIVE CHECK {cat.name} [{o.get('id')}]: required_checks {checks} "
                    f"lack a positive AND a negative fixture")

for f in findings:
    print(f)
print(f"__CHECKED__ {len(checked)}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/schemas" "$t/p"
  cp schemas/requirement.schema.json schemas/contract-obligation.schema.json "$t/schemas/"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'RECORD-SCHEMA self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  REQ='{"id":"REQ-D-A","profile_ids":["p"],"kind":"state","statement":"S","source_refs":[{"source_id":"SRC-A","locator":"§1"}],"applicability":"included","research_status":"resolved","implementation_status":"planned","source_semantics":{"category":"defined","detail":"d"},"risk":"low","obligation_ids":["OB-A"],"dependencies":[],"implementation_refs":[],"evidence_ids":[]}'
  OB='{"id":"OB-A","contract_id":"c","contract_version":"0","profile_ids":["p"],"direction":"cpu-guarantee","statement":"S","authority":"architecture","source_refs":[{"source_id":"SRC-A","locator":"§1"}],"parameters":{},"dependencies":[],"required_checks":["CHK-A-POS","CHK-A-NEG"]}'

  arm() {
    argc 3 "$#" arm || return
    out="$(check_records "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'RECORD-SCHEMA self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'RECORD-SCHEMA self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  sources() { argc 1 "$#" sources || return; printf '%s\n' "$1" > "$t/p/sources.sexp"; }
  profile() { argc 1 "$#" profile || return; printf '%s\n' "$1" > "$t/p/profile.sexp"; }
  reqs()    { argc 1 "$#" reqs || return; python3 -c "
import json, pathlib, sys
sys.path.insert(0, '$ROOT/scripts')
import records_sexp as R
recs = [json.loads(l) for l in '''$1'''.split('|||') if l.strip()]
pathlib.Path('$t/p/requirements.sexp').write_text(R.dump(recs))"; }
  obs()     { argc 1 "$#" obs || return; python3 -c "
import json, pathlib, sys
sys.path.insert(0, '$ROOT/scripts')
import records_sexp as R
recs = [json.loads(l) for l in '''$1'''.split('|||') if l.strip()]
pathlib.Path('$t/p/contract-obligations.sexp').write_text(R.dump(recs))"; }
  # schema-layer access: the fixture root must SEE schema/ for load_schema — symlink it
  ln -sfn "$ROOT/schema" "$t/schema"

  sources '(sources (source (id "SRC-A") (file "a.html")))'
  profile '(profile (decision (id "D-A") (authority architecture) (statement "S") (source "SRC-A §1")))'
  reqs "$REQ";                                                arm "GREEN a covered, cited, valid record" 0 "__CHECKED__ 1"
  # ---- the schema layer's own refusals, on the converted form -------------------------------
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['risk']='apocalyptic'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a record the schema layer refuses (bad enum symbol)" 1 "is not one of"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['source_refs']=[]; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an empty citation list — min 1 (an empty list is not a citation)" 1 "min is 1"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['obligation_ids']=['OB-A','OB-A']; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a duplicated obligation — unique" 1 "unique"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['id']='1BAD'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an id the pattern refuses" 1 "does not match"
  reqs "$REQ|||$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['risk']='critical'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a catalogue with a duplicated id — last-wins collapses it" 1 "DUPLICATE ID"
  printf '%s\n' '(requirement (id "REQ-D-A") (broken' > "$t/p/requirements.sexp"
                                                              arm "RED   a record that does not even parse" 1 "does not even parse"
  : > "$t/p/requirements.sexp";                               arm "RED   an empty catalogue" 1 "contains no records"
  # ---- the cross-checks on the converted form ------------------------------------------------
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['source_refs']=[{'source_id':'SRC-NOWHERE','locator':'§1'}]; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   cites a source nobody pinned" 1 "UNPINNED SOURCE"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['source_semantics']['detail']='d OPEN: something'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   resolved while carrying an open question" 1 "RESOLVED WITH AN OPEN QUESTION"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['dependencies']=['REQ-D-GHOST']; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   depends on a record that does not exist" 1 "DANGLING DEP"
  reqs "$(printf '%s' "$REQ" | python3 -c "import json,sys; r=json.load(sys.stdin); r['statement']='something else'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   the requirement no longer states the decision" 1 "STATEMENT DRIFT"
  profile '(profile (decision (id "D-B") (authority architecture) (statement "T") (source "SRC-A §2")))'
  reqs "$REQ";                                                arm "RED   a profile decision with no requirement" 1 "UNCOVERED DECISION"
  profile '(profile (decision (id "D-A") (authority architecture) (statement "S") (source "SRC-A §1")))'
  reqs "$REQ"; obs "$OB";                                     arm "GREEN requirement, contract and profile agree" 0 "__CHECKED__ 2"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['required_checks']=['CHK-A-POS']; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an obligation with no negative fixture" 1 "NO NEGATIVE CHECK"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['id']='OB-OTHER'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a requirement names an undefined obligation" 1 "UNDEFINED OBLIGATION"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['authority']='laboratory'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an architectural rule labelled a laboratory choice" 1 "AUTHORITY DOWNGRADE"
  obs "$OB"
  rm -f "$t/p/requirements.sexp";                             arm "RED   an obligation catalogue alone still checks" 0 "__CHECKED__ 1"
  reqs "$REQ"; rm -f "$t/p/contract-obligations.sexp"
  # ---- rule 9 MIRROR: an obligation naming its requirement restates it ------------------------
  reqs "$REQ"; obs "$OB"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-A'}; r['statement']='S'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "GREEN an obligation mirrored on its requirement" 0 "__CHECKED__ 2"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-A'}; r['statement']='something else'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   an obligation that drifted from its requirement" 1 "MIRROR DRIFT"
  obs "$(printf '%s' "$OB" | python3 -c "import json,sys; r=json.load(sys.stdin); r['parameters']={'requirement_id':'REQ-D-GHOST'}; r['statement']='S'; print(json.dumps(r,ensure_ascii=False))")"
                                                              arm "RED   a mirror of a requirement that does not exist" 1 "MIRROR WITHOUT SOURCE"
  rm -f "$t/p/contract-obligations.sexp"
  # ---- the JSONL track (examples stay JSONL) -------------------------------------------------
  printf '%s\n' "$REQ" > "$t/p/requirements.jsonl";           arm "GREEN a JSONL record validates on the old track" 0 "__CHECKED__ 2"
  printf 'not json at all\n' > "$t/p/mystery.jsonl";          arm "RED   a record file no schema governs" 1 "UNGOVERNED"
  rm -f "$t/p/mystery.jsonl"
  printf 'not json at all\n' > "$t/p/requirements.jsonl";     arm "RED   a malformed JSONL line" 1 "not valid JSON"
  : > "$t/p/requirements.jsonl";                              arm "RED   an empty JSONL record file" 1 "contains no records"
  rm -f "$t/p/requirements.jsonl" "$t/p/requirements.sexp" "$t/p/contract-obligations.sexp"
                                                              arm "REFUSE nothing to check at all" 2 "NO RECORDS"

  rm -rf "$t"
  printf 'RECORD-SCHEMA --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

# --audit: report referential problems in record files the gate deliberately does NOT enforce,
# so a known gap stays re-derivable instead of becoming prose someone has to remember.
if [ "${1:-}" = "--audit" ]; then
python3 - <<'AUDITPY'
import json, pathlib, sys
sys.path.insert(0, "scripts")
import records_sexp as R
_SKIP = {"target", "vendor", "schema"}
dirs = sorted({p.parent for p in pathlib.Path(".").rglob("*")
               if p.suffix in (".jsonl", ".sexp") and not _SKIP & set(p.parts)})
for d in dirs:
    rq = d / "requirements.sexp"
    ob = d / "contract-obligations.sexp"
    if not (rq.is_file() or ob.is_file() or (d / "requirements.jsonl").is_file()):
        continue
    enforced = (d / "profile.sexp").is_file()
    def load(p):
        if p.is_file():
            return R.load(p) if p.suffix == ".sexp" else \
                [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
        return None
    reqs = load(rq) or load(d / "requirements.jsonl") or []
    obs = load(ob) or load(d / "contract-obligations.jsonl") or []
    print(f"{d}/  ({'ENFORCED' if enforced else 'advisory - frozen delivery artifacts'})")
    print(f"  requirements {len(reqs)} | obligations {len(obs)}")
    defined = {o["id"] for o in obs}
    named = {oid for r in reqs for oid in r.get("obligation_ids", [])}
    print(f"  named but undefined : {sorted(named - defined) or 'none'}")
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
