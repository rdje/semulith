#!/usr/bin/env bash
# scripts/check_contract_freeze.sh — CONTRACT-FREEZE (project doctrine; P4-SYSTEM.9 slice a).
#
# An environment contract is VERSIONED, NOT EDITED IN PLACE. Each unit that versions its
# contract keeps `profiles/<unit>/contract.sexp` — one (contract …) form per version, listing
# the obligation records the version adds (schema/contract.sexp). This check judges every such
# unit against its `contract-obligations.sexp`:
#   - every member names a real record, of THAT version (contract_id and contract_version);
#   - every obligation record belongs to exactly one version (no unversioned record);
#   - a FROZEN version pins each member's record line by sha256 — an edited record is refused
#     (the fix is a later version superseding it, never a rewrite);
#   - `extends` names an existing version, one number lower; a `supersede` replaces a record
#     the version inherits, by one of its own members.
# Founding gap (P4-SYSTEM.9's brief): the version was a string repeated on every record that
# nothing checked, and records were added under v0 by seven leaves.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
command -v python3 >/dev/null 2>&1 || {
  echo "CONTRACT-FREEZE: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

judge() { # judge <root> — prints findings, exits 1 on any, 0 when clean
python3 - "$1" <<'PY'
import hashlib, re, sys
from pathlib import Path
sys.path.insert(0, "scripts")
import sexp as S

root = Path(sys.argv[1])
findings, units, versions_seen = [], 0, 0
for cdoc in sorted(root.glob("profiles/*/contract.sexp")):
    units += 1
    unit = cdoc.parent.name
    obs = {}
    for line in (cdoc.parent / "contract-obligations.sexp").read_text(encoding="utf-8").splitlines():
        m = re.match(r'\(obligation \(id "([^"]+)"\) \(contract_id "([^"]+)"\) \(contract_version "([^"]+)"\)', line)
        if m:
            obs[m.group(1)] = (line, m.group(2), m.group(3))
    versions = {}
    for form in S.read_file(cdoc):
        if not isinstance(form, list) or str(form[0]) != "contract":
            continue
        f = {str(c[0]): c for c in form[1:] if isinstance(c, list)}
        vid, ver = str(f["id"][1]), str(f["version"][1])
        members = []
        for c in form[1:]:
            if isinstance(c, list) and str(c[0]) == "member":
                mf = {str(x[0]): str(x[1]) for x in c[1:]}
                members.append((mf["id"], mf.get("sha256")))
        sups = [{str(x[0]): str(x[1]) for x in c[1:]} for c in form[1:]
                if isinstance(c, list) and str(c[0]) == "supersede"]
        versions[vid] = {"version": ver, "status": str(f["status"][1]), "members": members,
                         "extends": str(f["extends"][1]) if "extends" in f else None, "sups": sups}
    versions_seen += len(versions)
    owner = {}
    for vid, v in versions.items():
        for oid, pin in v["members"]:
            if oid in owner:
                findings.append(f"RECORD IN TWO VERSIONS {unit}: {oid} is a member of {owner[oid]} and {vid}")
            owner[oid] = vid
            rec = obs.get(oid)
            if rec is None:
                findings.append(f"MEMBER WITHOUT RECORD {unit} [{vid}]: {oid} names no obligation record")
                continue
            line, cid, cver = rec
            if (cid, cver) != (vid, v["version"]):
                findings.append(f"MEMBER OF ANOTHER VERSION {unit} [{vid}]: {oid} carries contract_id "
                                f"{cid} version {cver}")
            if v["status"] == "frozen":
                if pin is None:
                    findings.append(f"FROZEN WITHOUT PIN {unit} [{vid}]: {oid} carries no sha256")
                elif hashlib.sha256(line.encode("utf-8")).hexdigest() != pin:
                    findings.append(f"FROZEN RECORD EDITED {unit} [{vid}]: {oid} no longer matches its "
                                    f"pin — a frozen version is superseded by a later one, never rewritten")
        if v["extends"] is not None:
            parent = versions.get(v["extends"])
            if parent is None:
                findings.append(f"EXTENDS NOTHING {unit} [{vid}]: no version {v['extends']}")
            elif int(parent["version"]) + 1 != int(v["version"]):
                findings.append(f"VERSION GAP {unit} [{vid}]: version {v['version']} extends "
                                f"{parent['version']}")
        inherited, p = set(), v["extends"]
        while p in versions:
            inherited |= {oid for oid, _ in versions[p]["members"]}
            p = versions[p]["extends"]
        own = {oid for oid, _ in v["members"]}
        for s in v["sups"]:
            if s["record"] not in inherited:
                findings.append(f"SUPERSEDES NOTHING {unit} [{vid}]: {s['record']} is not inherited")
            if s["by"] not in own:
                findings.append(f"SUPERSEDED BY A STRANGER {unit} [{vid}]: {s['by']} is not this "
                                f"version's member")
    for oid in sorted(set(obs) - set(owner)):
        findings.append(f"UNVERSIONED RECORD {unit}: {oid} belongs to no version in contract.sexp")
for f in findings:
    print("  " + f)
print(f"CONTRACT-FREEZE: {'FAIL' if findings else 'ok'} ({units} versioned unit(s), "
      f"{versions_seen} version(s), {len(findings)} finding(s))")
sys.exit(1 if findings else 0)
PY
}

# ── self-test ────────────────────────────────────────────────────────────────────────────────
SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
self_test() {
  local t pass=0 fail=0 out rc u
  t="$(SELFTEST_TMP)"
  # ⛔ STRICT ARITY (docs/knowledge/self-test-arms-that-never-ran.md).
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'CONTRACT-FREEZE self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }
  arm() { # arm <name> <rc> <expected-rc> <output> <reason substring>
    argc 5 "$#" arm || return
    if [ "$2" = "$3" ] && printf '%s' "$4" | grep -qF -- "$5"; then
      pass=$((pass+1))
    else
      fail=$((fail+1))
      printf 'CONTRACT-FREEZE self-test MISS: %s — expected rc=%s (reason: %s), got rc=%s\n%s\n' \
        "$1" "$3" "$5" "$2" "$4" >&2
    fi
  }
  fresh() { rm -rf "$t/profiles"; mkdir -p "$t/profiles/u"; cp profiles/rv64gc-lab-v0/contract.sexp \
      profiles/rv64gc-lab-v0/contract-obligations.sexp "$t/profiles/u/"; ln -sfn "$ROOT/scripts" "$t/scripts"; }
  u="$t/profiles/u"
  fresh
  out="$(cd "$t" && judge "$t" 2>&1)"; rc=$?
  arm "GREEN the real contract and its records agree" "$rc" 0 "$out" "0 finding(s)"
  fresh; sed -i '0,/^(obligation (id "OB-SV39")/s/selects the minimal/selects the MINIMAL/' "$u/contract-obligations.sexp"
  out="$(cd "$t" && judge "$t" 2>&1)"; rc=$?
  arm "RED an edited frozen record is refused" "$rc" 1 "$out" "FROZEN RECORD EDITED"
  fresh; sed -i '/(member (id "OB-SVADE")/d' "$u/contract.sexp"
  out="$(cd "$t" && judge "$t" 2>&1)"; rc=$?
  arm "RED a record dropped from every version is refused" "$rc" 1 "$out" "UNVERSIONED RECORD"
  fresh; sed -i 's/(member (id "OB-SVADE")/(member (id "OB-NOWHERE")/' "$u/contract.sexp"
  out="$(cd "$t" && judge "$t" 2>&1)"; rc=$?
  arm "RED a member naming no record is refused" "$rc" 1 "$out" "MEMBER WITHOUT RECORD"
  fresh; sed -i '0,/^(obligation (id "OB-SV39")/s/(contract_version "0")/(contract_version "1")/' "$u/contract-obligations.sexp"
  out="$(cd "$t" && judge "$t" 2>&1)"; rc=$?
  arm "RED a member of another version is refused" "$rc" 1 "$out" "MEMBER OF ANOTHER VERSION"
  fresh; printf '(contract (id "rv64gc-lab-env-v1") (version "1") (profile_ids "u") (extends "rv64gc-lab-env-v7") (status open) (statement "x") (member (id "OB-X")) (supersede (record "OB-NOT-INHERITED") (by "OB-X") (why "y")))\n' >> "$u/contract.sexp"
  printf '(obligation (id "OB-X") (contract_id "rv64gc-lab-env-v1") (contract_version "1"))\n' >> "$u/contract-obligations.sexp"
  out="$(cd "$t" && judge "$t" 2>&1)"; rc=$?
  arm "RED an extension of no version is refused" "$rc" 1 "$out" "EXTENDS NOTHING"
  arm "RED a supersession of a record not inherited is refused" "$rc" 1 "$out" "SUPERSEDES NOTHING"
  rm -rf "$t"
  printf 'CONTRACT-FREEZE --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}
if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi
# Judge FIRST: a finding is a verdict on its own. Only a PASS needs the controls' proof that
# the check discriminates — and the GREEN control copies the live files, so running it first
# would let a broken tree mask its own finding behind "does not discriminate" (measured at
# P4-SYSTEM.9 slice d with a frozen v1 record edited).
out="$(judge "$ROOT" 2>&1)"; rc=$?
if [ "$rc" -ne 0 ]; then
  printf '%s\n' "$out" >&2
  exit 1
fi
self_test >/dev/null 2>&1 || {
  echo "CONTRACT-FREEZE: REFUSED — the check does not discriminate (self-test failed)." >&2
  exit 2; }
printf '%s\n' "$out"
