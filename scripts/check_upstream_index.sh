#!/usr/bin/env bash
# scripts/check_upstream_index.sh — UPSTREAM-INDEX (project doctrine).
#
# A defect we raise against a dependency is work THIS project owns until it is verified fixed, so
# it is tracked like our own work: an id, a state, a dated history. `docs/upstream/` holds one
# directory per issue, and that directory is the whole issue — a maintainer copies it out and can
# reproduce and validate without this repository.
#
# ⛔ SELF-CONTAINMENT AND A SECOND SOURCE OF TRUTH CANNOT BOTH HOLD. If the subtree carries its own
# state, then the vendor index and the top-level index are MIRRORS, and a mirror that nobody checks
# drifts — which is the whole reason `FRONTIER-SYNC` and `REGISTRY-MIRROR` exist facing inwards.
# This is the same doctrine facing outwards. The record is `<issue>/issue.sexp`; everything else
# that states an id, a title, a severity or a state is checked against it.
#
# What it checks:
#   1. RECORD       every issue directory has an issue.sexp with the required fields
#   2. VOCABULARY   state and severity come from the declared sets, never invented
#   3. REPORT       REPORT.md's own metadata table agrees with the record beside it
#   4. VENDOR       the vendor index has exactly one row per issue and agrees with each record
#   5. TOP          the top-level index agrees too
#   6. ORPHANS      a row with no issue, or an issue with no row, is a breach in both directions
#   7. CONTAINED    no file in an issue subtree references a path outside that subtree
#   8. VERIFIED     a `verified` state must name the pin it was verified against
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
UP="docs/upstream"
STATES="draft reported acknowledged disputed fixed-upstream verified closed wontfix"
SEVERITIES="high medium low"

scan() {
python3 - "$1" "$2" "$3" <<'PY'
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(sys.argv[1]) / "scripts"))
import sexp as S

root = pathlib.Path(sys.argv[1]); up = root / sys.argv[2]
STATES = set(sys.argv[3].split()); SEV = {"high", "medium", "low"}
REQUIRED = ("id", "project", "title", "component", "severity", "state")
bad, checked = [], 0

if not up.is_dir():
    print("NO TRACKER  docs/upstream/ does not exist — this check cannot judge"); sys.exit(2)

issues = {}
for d in sorted(p for p in up.glob("*/*") if p.is_dir()):
    rec = d / "issue.sexp"
    if not rec.is_file():
        bad.append(f"NO RECORD   {d.relative_to(root)} is an issue directory with no issue.sexp. "
                   f"Without one the indices have nothing to be checked against.")
        continue
    try:
        form = S.read_file(rec)[0]
        if S.head(form, str(rec)) != "issue":
            bad.append(f"BAD RECORD  {rec.relative_to(root)}: expected one (issue …) form"); continue
        f = {k: str(S.field(form, k, str(rec))) for k in REQUIRED}
    except Exception as exc:                                  # noqa: BLE001
        bad.append(f"BAD RECORD  {rec.relative_to(root)}: {exc}"); continue
    checked += 1
    if f["state"] not in STATES:
        bad.append(f"BAD STATE   {f['id']}: {f['state']!r} is not one of: {' '.join(sorted(STATES))}")
    if f["severity"] not in SEV:
        bad.append(f"BAD SEV     {f['id']}: {f['severity']!r} is not one of: {' '.join(sorted(SEV))}")
    if f["id"] in issues:
        bad.append(f"DUP ID      {f['id']} declared by two directories")
    if not d.name.startswith(f["id"] + "-"):
        bad.append(f"NAME DRIFT  {d.relative_to(root)} does not start with its id {f['id']!r}")
    # a verified state must name what it was verified against
    if f["state"] == "verified":
        pins = [c for c in S.children(form, "history") for c in S.children(c, "event")]
        text = rec.read_text()
        if "verified-against" not in text:
            bad.append(f"UNEARNED    {f['id']}: state is `verified` but the record names no "
                       f"(verified-against …) pin. A fix we have not re-run is a claim.")
    f["dir"] = d
    issues[f["id"]] = f

# --- 3. REPORT.md agrees with the record beside it
for iid, f in issues.items():
    rep = f["dir"] / "REPORT.md"
    if not rep.is_file():
        bad.append(f"NO REPORT   {iid}: no REPORT.md in its subtree"); continue
    t = rep.read_text()
    for key, want in (("State", f["state"]), ("Severity", f["severity"]), ("ID", f["id"])):
        m = re.search(rf"^\|\s*\*\*{key}\*\*\s*\|(.*)$", t, re.M)
        if not m:
            bad.append(f"REPORT GAP  {iid}: REPORT.md has no **{key}** row"); continue
        if f"`{want}`" not in m.group(1):
            bad.append(f"REPORT DRIFT {iid}: REPORT.md's **{key}** row says "
                       f"{m.group(1).strip()[:40]!r}; issue.sexp says `{want}`")

# --- 4/5/6. the two indices mirror the records, both directions
def rows(path):
    if not path.is_file():
        return None
    out = {}
    for line in path.read_text().splitlines():
        m = re.match(r"\|\s*\[?`(LS-\d+|[A-Z]+-\d+)`\]?", line)
        if m:
            out[m.group(1)] = line
    return out

for label, path in (("VENDOR", up / "linkedspec" / "README.md"), ("TOP", up / "README.md")):
    r = rows(path)
    if r is None:
        bad.append(f"NO INDEX    {label}: {path.relative_to(root)} is missing"); continue
    for iid in issues:
        if iid not in r:
            bad.append(f"MISSING ROW {label}: {path.relative_to(root)} lists no row for {iid}")
    for iid in r:
        if iid not in issues:
            bad.append(f"ORPHAN ROW  {label}: {path.relative_to(root)} lists {iid}, which has no "
                       f"issue directory")
    for iid, f in issues.items():
        if iid in r and f"`{f['state']}`" not in r[iid]:
            bad.append(f"STATE DRIFT {label}: the row for {iid} does not carry its state "
                       f"`{f['state']}`")
        if iid in r and f"`{f['severity']}`" not in r[iid]:
            bad.append(f"SEV DRIFT   {label}: the row for {iid} does not carry `{f['severity']}`")

# --- 7. self-containment: nothing in a subtree may point outside it
ESCAPE = re.compile(r"(\.\./\.\./|/Volumes/|/Users/|\bdocs/tasks/|\bscripts/|\bprofiles/|\bdefinitions/)")
for iid, f in issues.items():
    for p in sorted(f["dir"].rglob("*")):
        if not p.is_file() or p.suffix in (".patch",):
            continue
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            m = ESCAPE.search(line)
            if m and "docs/.../" not in line:
                bad.append(f"NOT CONTAINED {iid}: {p.relative_to(root)}:{n} references "
                           f"{m.group(1)!r} — outside its own subtree. A maintainer who copies "
                           f"this directory out would get a broken issue.")
                break

for b in bad:
    print(f"  {b}")
print(f"__CHECKED__ {checked}")
sys.exit(1 if bad else 0)
PY
}

selftest() {
  local pass=0 fail=0 tmp; tmp="$(mktemp -d)"
  mk() { # mk <dir> <id> <state> <severity>
    mkdir -p "$tmp/docs/upstream/linkedspec/$1"
    cat > "$tmp/docs/upstream/linkedspec/$1/issue.sexp" <<EOF
(issue (id "$2") (project "linkedspec") (title "t") (component "c")
       (severity $4) (state $3))
EOF
    cat > "$tmp/docs/upstream/linkedspec/$1/REPORT.md" <<EOF
| | |
| --- | --- |
| **ID** | \`$2\` |
| **Severity** | \`$4\` |
| **State** | \`$3\` |
EOF
  }
  idx() { # idx <top-row> <vendor-row>
    mkdir -p "$tmp/docs/upstream/linkedspec"
    printf '| ID |\n| --- |\n%s\n' "$1" > "$tmp/docs/upstream/README.md"
    printf '| ID |\n| --- |\n%s\n' "$2" > "$tmp/docs/upstream/linkedspec/README.md"
  }
  reset() { rm -rf "$tmp/docs"; mkdir -p "$tmp/docs/upstream/linkedspec"; }
  arm() { # arm <label> <want-rc> <needle>
    local out rc; set +e
    out="$(scan "$tmp" "docs/upstream" "$STATES" 2>&1)"; rc=$?; set -e
    if [ "$rc" != "$2" ]; then echo "  FAIL  $1: exit $rc, expected $2 — $(echo "$out" | head -1)"; fail=$((fail+1)); return; fi
    if [ -n "$3" ] && ! printf '%s' "$out" | grep -qF -- "$3"; then
      echo "  FAIL  $1: right exit, wrong reason — wanted '$3', got: $(echo "$out" | head -1)"; fail=$((fail+1)); return; fi
    echo "  ok    $1"; pass=$((pass+1))
  }
  ln_='| [`LS-001`](x) | t | `high` | `draft` |'

  mkdir -p "$tmp/scripts"; cp "$ROOT/scripts/sexp.py" "$tmp/scripts/"

  reset; mk LS-001-a LS-001 draft high; idx "$ln_" "$ln_"
  arm "GREEN a consistent tracker passes" 0 "__CHECKED__ 1"

  reset; mk LS-001-a LS-001 reported high; idx "$ln_" "$ln_"
  arm "RED   the index carries a stale STATE" 1 "STATE DRIFT"

  reset; mk LS-001-a LS-001 draft medium; idx "$ln_" "$ln_"
  arm "RED   the index carries a stale SEVERITY" 1 "SEV DRIFT"

  reset; mk LS-001-a LS-001 draft high; idx "$ln_" '| x |'
  arm "RED   an issue with no row in the vendor index" 1 "MISSING ROW VENDOR"

  reset; mk LS-001-a LS-001 draft high; idx '| [`LS-009`](x) | t | `high` | `draft` |' "$ln_"
  arm "RED   an index row with no issue directory" 1 "ORPHAN ROW"

  reset; mk LS-001-a LS-001 invented high; idx "$ln_" "$ln_"
  arm "RED   a state outside the vocabulary is refused" 1 "BAD STATE"

  reset; mk LS-001-a LS-001 draft catastrophic; idx "$ln_" "$ln_"
  arm "RED   a severity outside the vocabulary is refused" 1 "BAD SEV"

  reset; mk LS-001-a LS-001 draft high; rm "$tmp/docs/upstream/linkedspec/LS-001-a/issue.sexp"; idx "$ln_" "$ln_"
  arm "RED   an issue directory with no record" 1 "NO RECORD"

  reset; mk LS-001-a LS-001 draft high; idx "$ln_" "$ln_"
  printf '| **State** | `closed` |\n' >> "$tmp/docs/upstream/linkedspec/LS-001-a/REPORT.md"
  sed -i.bak 's/| \*\*State\*\* | `draft` |//' "$tmp/docs/upstream/linkedspec/LS-001-a/REPORT.md"
  arm "RED   REPORT.md disagrees with the record beside it" 1 "REPORT DRIFT"

  reset; mk LS-001-a LS-001 draft high; idx "$ln_" "$ln_"
  printf 'see scripts/sexp.py for details\n' > "$tmp/docs/upstream/linkedspec/LS-001-a/VALIDATE.md"
  arm "RED   a file pointing OUTSIDE its own subtree" 1 "NOT CONTAINED"

  reset; mk LS-001-a LS-001 verified high; idx '| [`LS-001`](x) | t | `high` | `verified` |' '| [`LS-001`](x) | t | `high` | `verified` |'
  arm "RED   \`verified\` without the pin it was verified against" 1 "UNEARNED"

  reset; mk wrongly-named-dir LS-001 draft high; idx "$ln_" "$ln_"
  arm "RED   a directory whose name does not carry its id" 1 "NAME DRIFT"

  rm -rf "$tmp"
  echo "UPSTREAM-INDEX --self-test: $pass pass / $fail fail"
  [ "$fail" -eq 0 ]
}

case "${1-}" in
  --self-test) selftest ;;
  *)
    # ⛔ `set -e` would abort on a failing scan BEFORE rc could be read, and the gate would exit 1
    # printing nothing — a breach with no reason is indistinguishable from a crash.
    set +e; out="$(scan "$ROOT" "$UP" "$STATES" 2>&1)"; rc=$?; set -e
    n="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
    if [ "$rc" -ne 0 ]; then
      echo "UPSTREAM-INDEX: an index disagrees with the issues it lists." >&2
      printf '%s\n' "$out" | grep -v '^__CHECKED__' >&2
      echo "  The ISSUE RECORD is authoritative. Fix the index, never the record to match it." >&2
      exit "$rc"
    fi
    echo "UPSTREAM-INDEX: ok (${n:-0} issue record(s) mirrored by both indices)" ;;
esac
