#!/usr/bin/env bash
# scripts/check_fact_ownership.sh — FACT-OWNERSHIP (project doctrine).
#
# The no-duplicated-fact rule, mechanized (MODEL-METHOD.7): "single source of truth" means one
# OWNER PER FACT, not one file — the corpus legitimately DERIVES facts into mirrors (a
# requirement restating a profile decision; the profile dossier restating state; an obligation
# restating its requirement; a unit composition restating its fragments), and each owner→mirror
# pair is governed by a doctrine that refuses the day the two drift. `doctrine/fact_ownership.tsv`
# names, per fact kind: the one owning file, the legal mirrors, the governing doctrine. This
# gate verifies the registry HOLDS: exactly one owner per fact kind, owners exist, every mirror
# names a governor, every governor is a REGISTERED doctrine that actually runs, and the corpus's
# enumerated restatement pairs are all named here — a restatement the registry does not know
# about is the refusal, because an ungoverned mirror is how one fact quietly becomes two.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

TSV="doctrine/fact_ownership.tsv"

# The corpus's ACTUAL restatement pairs, as "restater<TAB>source" (the restater restates the
# source's fact). Each must appear in the registry as a row whose owner matches the source and
# mirror matches the restater — enumerated here because a completeness claim needs a census.
CORPUS_MIRRORS=$'profiles/*/requirements.sexp\tprofiles/*/profile.sexp\nprofiles/*/profile.sexp\tprofiles/*/state.sexp\nprofiles/*/contract-obligations.sexp\tprofiles/*/requirements.sexp\nprofiles/*/encoding.sexp\tdefinitions/\ncrates/*/src/state.rs\tprofiles/*/state.sexp\ncrates/*/src/definition.rs\tdefinitions/\ncrates/*/src/definition.rs\tprofiles/*/state.sexp'

check_ownership() { # $1 = registry path; $2 = project driver; $3 = corpus pairs (restater<TAB>source per line)
python3 - "$1" "$2" "$3" <<'PY'
import glob as _glob
import re
import sys
from pathlib import Path

tsv = Path(sys.argv[1])
project_driver = Path(sys.argv[2])
corpus_spec = sys.argv[3]

lines = tsv.read_text().splitlines()
rows = []
for n, raw in enumerate(lines, 1):
    line = raw.rstrip("\n")
    if not line.strip() or line.startswith("#"):
        continue
    cells = line.split("\t")
    if len(cells) != 4:
        print(f"BAD ROW {tsv}:{n}: expected 4 tab-separated cells, got {len(cells)}")
        print("__CHECKED__ 0"); sys.exit(2)
    rows.append((n, cells[0], cells[1], cells[2], cells[3]))

if not rows:
    print(f"EMPTY REGISTRY {tsv}: no fact kind is owned by anything — this check cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

driver = project_driver.read_text()
registered = set(re.findall(r'^  "([A-Z-]+)\|', driver, re.M))

def matches(path_str: str, pattern: str) -> bool:
    # symmetric directory-prefix matching: 'definitions/' names 'definitions/riscv/', and
    # 'definitions/riscv/' answers for 'definitions/'
    p = pattern.rstrip("/")
    s = path_str.rstrip("/")
    return s == p or s.startswith(p + "/") or p.startswith(s + "/")

findings = []
checked = len(rows)
kinds: dict[str, list[tuple[str, str, str]]] = {}
for n, kind, owner, mirror, governor in rows:
    kinds.setdefault(kind, []).append((owner, mirror, governor))
    if not owner.strip() or owner == "-":
        findings.append(f"OWNERLESS {kind}: no owning file — a fact kind nobody owns is a "
                        f"fact nobody may state")
        continue
    if not Path(owner).exists():
        findings.append(f"MISSING OWNER {kind}: '{owner}' does not exist")
    if mirror != "-" and governor == "-":
        findings.append(f"UNGOVERNED MIRROR {kind}: '{mirror}' restates '{owner}' with no "
                        f"governing doctrine — one fact stated in two, free to drift")
    if governor != "-" and mirror == "-":
        findings.append(f"GOVERNOR WITHOUT MIRROR {kind}: '{governor}' governs nothing — "
                        f"the registry claims a check that has no pair to check")
    if governor != "-" and governor not in registered:
        findings.append(f"UNREGISTERED GOVERNOR {kind}: '{governor}' is named as a mirror "
                        f"governor but is not a registered project doctrine")

for kind, entries in sorted(kinds.items()):
    owners = {o for o, _, _ in entries}
    if len(owners) > 1:
        findings.append(f"TWO OWNERS {kind}: {sorted(owners)} both claim ownership — "
                        f"exactly one file owns a fact kind")

def expand(pat: str) -> list[str]:
    if pat.endswith("/"):
        found = [p for p in _glob.glob(pat + "**/*.sexp", recursive=True)]
        return [pat] if found else []           # a family: present iff it holds files
    return sorted(_glob.glob(pat))

# the corpus's actual restatement pairs must all be NAMED in the registry
pairs = []
cross_lines = []
for line in corpus_spec.splitlines():
    if not line.strip():
        continue
    restater, source = line.split("\t")
    rs, ss = expand(restater), expand(source)
    if restater.startswith("profiles/*/") and source.startswith("profiles/*/"):
        # Same-family patterns pair WITHIN one unit (P3-BREADTH.7): a unit's documents
        # restate that unit's facts. The cross product was exact while one unit existed
        # and invented cross-unit pairs the day a second landed — measured with
        # profiles/dsp56300-lab-v0/ (rv64's requirements "restating" the DSP's profile).
        for r in rs:
            for s in ss:
                if r.split("/")[1] == s.split("/")[1]:
                    pairs.append((r, s))
    else:
        cross_lines.append((restater, source, rs, ss))
for r, s in pairs:
    named = any(matches(s, owner) and matches(r, mirror)
                for _, _, owner, mirror, _ in rows)
    if not named:
        findings.append(f"UNREGISTERED MIRROR PAIR: '{r}' restates '{s}' in the corpus but no "
                        f"registry row names this pair — the no-duplicated-fact rule is only "
                        f"as good as the registry's completeness")

# Cross-family patterns (crates/ ↔ profiles/, profiles/ ↔ definitions/): the true pairs
# are not mechanically derivable — a crate's generated mirror belongs to exactly one unit
# and the crate↔unit binding is the registry's own content. So the census runs in the two
# directions that are checkable: every registered row naming a cross-family pair must be
# LIVE (both sides exist in the corpus), and every corpus file matching a RESTATER
# pattern must be registered as a mirror against a source of that family (a generated
# mirror nobody registered is the duplication this gate exists to catch). An owner-side
# document legitimately has no mirror of a given kind (the DSP's state.sexp has no
# generated state.rs — the naming convention reserves that path for generated mirrors),
# so owner-side participation is NOT required.
for restater, source, rs, ss in cross_lines:
    for _, kind, owner, mirror, _ in rows:
        if mirror == "-":
            continue
        if any(matches(mirror, r) for r in rs) and any(matches(owner, s) for s in ss):
            if not Path(mirror).exists() or (not ss[0].endswith("/") and not Path(owner).exists()):
                findings.append(f"PHANTOM PAIR {kind}: the registry names '{mirror}' ← "
                                f"'{owner}' but the corpus does not carry the pair")
    for r in rs:
        if not any(matches(r, mirror) and any(matches(owner, s) for s in ss)
                   for _, _, owner, mirror, _ in rows if mirror != "-"):
            findings.append(f"UNPAIRED RESTATER: '{r}' matches a restatement pattern but no "
                            f"registry row registers it as a mirror — a restatement nobody "
                            f"governs is how one fact becomes two")

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

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'FACT-OWNERSHIP self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_ownership "$t/reg.tsv" scripts/check_doctrines.project.sh "$FIXTURE_PAIRS" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'FACT-OWNERSHIP self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'FACT-OWNERSHIP self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  # fixture corpus pair: obligations restate requirements — named in the GREEN fixture
  # registry, omitted from the RED one, so the completeness arm has something to catch
  FIXTURE_PAIRS=$'profiles/*/contract-obligations.sexp\tprofiles/*/requirements.sexp'

  cat > "$t/reg.tsv" <<'EOF'
# fixture registry
configuration	profiles/rv64i-lab-v0/profile.sexp	-	-
state	profiles/rv64i-lab-v0/state.sexp	profiles/rv64i-lab-v0/profile.sexp	PROFILE-CONSISTENCY
requirements	profiles/rv64i-lab-v0/profile.sexp	profiles/rv64i-lab-v0/requirements.sexp	RECORD-SCHEMA
encodings	definitions/riscv/	profiles/rv64i-lab-v0/encoding.sexp	UNIT-COMPOSITION
obligations	profiles/rv64i-lab-v0/requirements.sexp	profiles/rv64i-lab-v0/contract-obligations.sexp	RECORD-SCHEMA
EOF
  arm "GREEN a well-formed registry naming every fixture pair" 0 "__CHECKED__ 5"

  cat > "$t/reg.tsv" <<'EOF'
state	profiles/rv64i-lab-v0/state.sexp	profiles/rv64i-lab-v0/profile.sexp	NOT-A-DOCTRINE
EOF
  arm "RED   a governor that is not a registered doctrine" 1 "UNREGISTERED GOVERNOR"

  cat > "$t/reg.tsv" <<'EOF'
state	profiles/rv64i-lab-v0/state.sexp	profiles/rv64i-lab-v0/profile.sexp	-
EOF
  arm "RED   a mirror with no governor — the ungoverned duplication" 1 "UNGOVERNED MIRROR"

  cat > "$t/reg.tsv" <<'EOF'
state	profiles/rv64i-lab-v0/ghost.sexp	-	-
EOF
  arm "RED   an owner that does not exist" 1 "MISSING OWNER"

  cat > "$t/reg.tsv" <<'EOF'
state	profiles/rv64i-lab-v0/state.sexp	-	RECORD-SCHEMA
EOF
  arm "RED   a governor named over nothing" 1 "GOVERNOR WITHOUT MIRROR"

  cat > "$t/reg.tsv" <<'EOF'
state	profiles/rv64i-lab-v0/state.sexp	-	-
state	profiles/rv64i-lab-v0/profile.sexp	-	-
EOF
  arm "RED   one fact kind, two owning files" 1 "TWO OWNERS"

  cat > "$t/reg.tsv" <<'EOF'
state	profiles/rv64i-lab-v0/state.sexp	-	-
EOF
  arm "RED   a fixture pair the registry does not name" 1 "UNREGISTERED MIRROR PAIR"

  printf 'bad row without enough cells\n' > "$t/reg.tsv"
  arm "REFUSE a malformed registry, never judge it" 2 "BAD ROW"

  rm -rf "$t"
  printf 'FACT-OWNERSHIP --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -f "$TSV" ] || { echo "FACT-OWNERSHIP: REFUSED — $TSV is missing; the registry this doctrine judges is gone." >&2; exit 2; }
self_test >/dev/null 2>&1 || {
  echo "FACT-OWNERSHIP: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_ownership "$TSV" scripts/check_doctrines.project.sh "$CORPUS_MIRRORS")"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "FACT-OWNERSHIP: REFUSED — the registry could not be judged."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "FACT-OWNERSHIP: the no-duplicated-fact rule is breached."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The registry is the authority. Name the owner, or govern the mirror."; } >&2
  exit 1
fi
printf 'FACT-OWNERSHIP: ok (%s fact kind(s): one owner each, every mirror governed)\n' "${count:-0}"
exit 0
