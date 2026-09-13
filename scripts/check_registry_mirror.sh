#!/usr/bin/env bash
# scripts/check_registry_mirror.sh — REGISTRY-MIRROR (project doctrine).
#
# The doctrine registry lives in two shell arrays: the universal one in
# `scripts/check_doctrines.sh` and this project's own in `scripts/check_doctrines.project.sh`.
# Two documents RESTATE it for humans — `DOCTRINE_ENFORCEMENT.md` (which calls itself "the
# human-readable mirror of the enforcer registry") and the mdBook chapter
# `docs/book/src/working/doctrines.md`. Neither restatement was compared with the arrays.
#
# ⭐ WHY THE BOOK MATTERS MOST HERE. The book is this project's review surface — the director
# reads the book, not the code. A registry mirror that falls behind does not merely go stale: it
# under-reports the project's own guarantees to the only person checking them, and it does so
# in the direction that looks fine. Measured at registration: 3 project doctrines listed, 5
# registered.
#
# What is compared:
#   1. COVERAGE   every registered id has a table row in BOTH mirrors.
#   2. PHANTOM    every id-shaped table row in a mirror is actually registered.
#   3. SECTION    a project doctrine is listed under the project heading, a universal one is not.
#   4. EXECUTABLE every registered entry names a file that exists and is executable — a registry
#                 row pointing at nothing is a doctrine that silently does not run.
#   5. COUNT      a sentence of the form "<N> checks run today" states the real universal count,
#                 spelled or in digits. A hand-typed count is a constant that is a function of
#                 the repository (`docs/CLAIM_VERIFICATION.md` §5B).
#
# ⚠️ HONEST LIMIT: it proves the two documents list the same doctrines the drivers register. It
# says nothing about whether each row's PROSE still describes what its check does — that drift is
# real, and it is a human reading.
#
# ⛔ REFUSES (exit 2) if either driver yields zero registry entries. The registry format is a
# quoted "ID|proves|path" triple; if that ever changes, this check must stop judging rather than
# report that every mirror is complete because it found nothing to mirror.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "REGISTRY-MIRROR: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

# $1 universal driver, $2 project driver, $3.. mirrors
check_mirror() {
python3 - "$@" <<'PY'
import re, sys, pathlib

universal_p, project_p = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
mirrors = [pathlib.Path(a) for a in sys.argv[3:]]
findings = []

# A registry entry is a quoted "ID|what it proves|path/to/check.sh". Comment lines are excluded
# so the format's own documentation line is not mistaken for a registration.
ENTRY = re.compile(r'"(?P<id>[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)\|(?P<proves>[^"|]*)\|(?P<path>[^"|]*\.sh)"')

def registry(path):
    out = {}
    if not path.is_file():
        return out
    for line in path.read_text().splitlines():
        if line.lstrip().startswith("#"):
            continue
        m = ENTRY.search(line)
        if m:
            out[m.group("id")] = m.group("path")
    return out

universal, project = registry(universal_p), registry(project_p)
if not universal or not project:
    print(f"NO REGISTRY universal={len(universal)} project={len(project)} — "
          f"the registry format changed; this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

registered = {**universal, **project}

# 4. EXECUTABLE ------------------------------------------------------------------
for did, rel in sorted(registered.items()):
    p = pathlib.Path(rel)
    if not p.is_file():
        findings.append(f"NO CHECK   {did}: registry names {rel}, which does not exist")
    elif not p.stat().st_mode & 0o111:
        findings.append(f"NOT EXECUTABLE {did}: {rel} is registered but not executable")

ROW  = re.compile(r"^\|\s*`(?P<id>[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)`\s*\|", re.M)
NUM  = re.compile(r"\b(?P<n>[A-Za-z]+|\d+)\s+checks\s+run\s+today\b", re.I)
WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty twentyone twentytwo twentythree "
    "twentyfour twentyfive".split())}

checked = 0
for mirror in mirrors:
    if not mirror.is_file():
        findings.append(f"NO MIRROR  {mirror} does not exist")
        continue
    checked += 1
    text = mirror.read_text()
    lines = text.splitlines()

    # which lines sit under a heading that announces the PROJECT's own doctrines
    in_project = []
    flag = False
    for ln in lines:
        if ln.startswith("#"):
            flag = bool(re.search(r"project'?s? own doctrine", ln, re.I))
        in_project.append(flag)

    listed = {}
    for i, ln in enumerate(lines):
        m = ROW.match(ln)
        if m:
            listed[m.group("id")] = in_project[i]

    # 1. COVERAGE ----------------------------------------------------------------
    for did in sorted(registered):
        if did not in listed:
            findings.append(
                f"NOT MIRRORED {mirror.name}: '{did}' is registered and has no row — "
                f"the document under-reports what this repository enforces")
    # 2. PHANTOM -----------------------------------------------------------------
    for did in sorted(listed):
        if did not in registered:
            findings.append(
                f"PHANTOM    {mirror.name}: '{did}' has a row but is registered nowhere")
    # 3. SECTION -----------------------------------------------------------------
    for did, under_project in sorted(listed.items()):
        if did in project and not under_project:
            findings.append(
                f"WRONG SECTION {mirror.name}: '{did}' is a project doctrine listed outside "
                f"the project section")
        if did in universal and did not in project and under_project:
            findings.append(
                f"WRONG SECTION {mirror.name}: '{did}' is universal but listed under the "
                f"project section")
    # 5. COUNT -------------------------------------------------------------------
    for m in NUM.finditer(text):
        raw = m.group("n")
        got = int(raw) if raw.isdigit() else WORDS.get(raw.lower())
        if got is None:
            findings.append(f"UNREADABLE COUNT {mirror.name}: '{raw} checks run today' is not a number")
        elif got != len(universal):
            findings.append(
                f"COUNT DRIFT {mirror.name}: '{raw} checks run today' — "
                f"{len(universal)} are registered in {universal_p.name}")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  # ⛔ STRICT ARITY. A fixture helper that ignores its extra arguments will swallow a whole
  # following command when a `;` is missing — `index a b arm NAME 1 WHY` is ONE call, and the
  # arm vanishes with no error. That measured defect ran 4 of 14 arms and reported `0 fail`.
  # See docs/knowledge/self-test-arms-that-never-ran.md.
  argc() { # argc <expected> <got> <helper>
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf '%s self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "REGISTRY-MIRROR" "$3" "$2" "$1" >&2
    return 1
  }

  : > "$t/a.sh"; : > "$t/b.sh"; chmod +x "$t/a.sh" "$t/b.sh"

  drivers() {
    cat > "$t/u.sh" <<EOF
# "ID|what it proves|relative/path/to/check.sh"   <- format doc, must NOT count
DOCTRINES=(
  "ALPHA|proves alpha|$t/a.sh"
)
EOF
    cat > "$t/p.sh" <<EOF
PROJECT_DOCTRINES=(
  "BETA|proves beta|$t/b.sh"
)
EOF
  }
  mirror() { # mirror() <body>
    argc 1 "$#" mirror || return
    printf '%s\n' "$1" > "$t/M.md"
  }
  arm() { # arm <name> <expected-rc> <expected-substring>
    argc 3 "$#" arm || return
    out="$(check_mirror "$t/u.sh" "$t/p.sh" "$t/M.md" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'REGISTRY-MIRROR self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'REGISTRY-MIRROR self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }
  GOOD='## Registry

| ID | Proves |
| --- | --- |
| `ALPHA` | alpha |

### This project'"'"'s own doctrines

| ID | Proves |
| --- | --- |
| `BETA` | beta |

One checks run today.'

  drivers
  mirror "$GOOD";                                     arm "GREEN both mirrored"        0 "__CHECKED__ 1"
  mirror "$(printf '%s' "$GOOD" | grep -v '`BETA`')"; arm "RED   a registered id has no row" 1 "NOT MIRRORED"
  mirror "$GOOD
| \`GAMMA\` | unregistered |";                        arm "RED   a row nothing registers" 1 "PHANTOM"
  mirror "$(printf '%s' "$GOOD" | sed 's/^One checks/Seven checks/')"
                                                      arm "RED   the count sentence drifts" 1 "COUNT DRIFT"
  mirror "$(printf '%s' "$GOOD" | sed 's/^One checks/Umpteen checks/')"
                                                      arm "RED   the count is not a number" 1 "UNREADABLE COUNT"
  mirror '## Registry

| ID | Proves |
| --- | --- |
| `ALPHA` | alpha |
| `BETA` | beta |

One checks run today.'
                                                      arm "RED   project doctrine outside its section" 1 "WRONG SECTION"
  mirror '### This project'"'"'s own doctrines

| ID | Proves |
| --- | --- |
| `ALPHA` | alpha |
| `BETA` | beta |

One checks run today.'
                                                      arm "RED   universal doctrine inside the project section" 1 "WRONG SECTION"
  drivers; chmod -x "$t/b.sh"
  mirror "$GOOD";                                     arm "RED   a registered check is not executable" 1 "NOT EXECUTABLE"
  chmod +x "$t/b.sh"
  rm -f "$t/b.sh"
  mirror "$GOOD";                                     arm "RED   a registered check does not exist" 1 "NO CHECK"
  : > "$t/b.sh"; chmod +x "$t/b.sh"
  rm -f "$t/M.md";                                    arm "RED   the mirror file is missing"  1 "NO MIRROR"
  mirror "$GOOD"
  printf 'DOCTRINES=(\n)\n' > "$t/u.sh";              arm "REFUSE the registry parses to nothing" 2 "NO REGISTRY"

  rm -rf "$t"
  printf 'REGISTRY-MIRROR --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -f scripts/check_doctrines.sh ] || { echo "REGISTRY-MIRROR: ok (no driver yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "REGISTRY-MIRROR: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

MIRRORS=(DOCTRINE_ENFORCEMENT.md docs/book/src/working/doctrines.md)
out="$(check_mirror scripts/check_doctrines.sh scripts/check_doctrines.project.sh "${MIRRORS[@]}")"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "REGISTRY-MIRROR: REFUSED — the registry could not be read, so its mirrors cannot be judged."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "REGISTRY-MIRROR: a doctrine document no longer mirrors the enforcer registry."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The REGISTRY is authoritative. Add the row — never drop a registration to match a document."; } >&2
  exit 1
fi
printf 'REGISTRY-MIRROR: ok (%s document(s) mirror the registry)\n' "${count:-0}"
exit 0
