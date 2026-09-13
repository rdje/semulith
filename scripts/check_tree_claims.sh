#!/usr/bin/env bash
# scripts/check_tree_claims.sh — TREE-CLAIMS (project doctrine).
#
# The third hop of the resume path. `FRONTIER-SYNC` gates `docs/TASK_TREE.md` against the trees;
# this gates the other LIVE documents that state facts about a tree — how many leaves it has,
# how many are done, which tree is active, which leaf is next. Those are not opinions. Each is a
# function of `docs/tasks/`, and `docs/CLAIM_VERIFICATION.md` §5B is explicit that a constant
# which is a function of the repository is derived or gated, never carried.
#
# ⭐ THE SCOPE IS DATA, NOT A HARDCODED LIST. Which documents are LIVE is already declared, once,
# in `doctrine/readme_routes.tsv`'s `lifecycle` column — this check reads `hot_live` from there.
# That matters in both directions:
#   • a new live surface is covered on the day it is registered, with no edit here;
#   • `append_history` surfaces (`CHANGELOG.md`, `DEV_NOTES.md`) are excluded ON PURPOSE. A
#     changelog entry saying "2 of 9 leaves" was TRUE when it was written and must never be
#     rewritten to match today. Gating history would corrupt the record it exists to keep.
# `docs/TASK_TREE.md` is excluded too — `FRONTIER-SYNC` owns it, and two gates reporting one
# breach twice is noise, not depth.
#
# What is compared, per live document:
#   1. COUNT      `A of B leaves` and `B leaves` beside a tree reference match that tree.
#   2. FRONTIER   a line whose LABEL is `Frontier leaf:` names the leaf the tree's own Current
#                 Frontier names first, and never a leaf the tree records as `done`. Anchored on
#                 the label so that prose merely mentioning the words is not a claim.
#   3. ACTIVE     an `Active tree(s):` line names trees whose Metadata status is `active`, and
#                 omits no tree that IS active — a forgotten active tree is a lost lane.
#
# ⚠️ HONEST LIMIT: it proves the numbers and ids are current. It cannot tell whether the prose
# around them still describes the work; that is a reading, not a computation.
#
# ⛔ REFUSES (exit 2) if the routes registry yields no live documents, or if `docs/tasks/` yields
# no trees. A claim checker that finds no claims must say so rather than report agreement.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "TREE-CLAIMS: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

# $1 = repo-ish root holding the routes tsv, the tasks dir and the live docs.
check_claims() {
python3 - "$1" "$2" "$3" <<'PY'
import re, sys, pathlib

root      = pathlib.Path(sys.argv[1])
routes    = root / sys.argv[2]
tasks_dir = root / sys.argv[3]
findings  = []

if not routes.is_file():
    print(f"NO ROUTES  {routes} does not exist"); print("__CHECKED__ 0"); sys.exit(2)

live = []
for line in routes.read_text().splitlines():
    if line.startswith("#") or not line.strip():
        continue
    cols = line.split("\t")
    if len(cols) > 2 and cols[2].strip() == "hot_live":
        dest = cols[0].strip()
        if dest.endswith("/") or dest == "docs/TASK_TREE.md":
            continue                     # families have no claims; the index is FRONTIER-SYNC's
        live.append(dest)
if not live:
    print("NO LIVE DOCS the routes registry declares no hot_live file — cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

# ---------------------------------------------------------------- the trees are the source
def parse_tree(path):
    t = path.read_text(); lines = t.splitlines()
    status = None
    ms = re.search(r"^- Status:\s*(.+)$", t, re.M)
    if ms:
        tk = re.findall(r"`([^`]+)`", ms.group(1))
        status = tk[0] if tk else ms.group(1).strip()
    leaves = {}
    for i, ln in enumerate(lines):
        mi = re.match(r"^- ID:\s*`([A-Za-z0-9._-]+\.\d+)`", ln)
        if not mi:
            continue
        st = None
        for ln2 in lines[i + 1 : i + 8]:
            if re.match(r"^- ID:\s*`", ln2):
                break
            m2 = re.search(r"^\s*Status:\s*`([a-z_]+)`", ln2)
            if m2:
                st = m2.group(1); break
        leaves[mi.group(1)] = st
    nxt = None
    inside = False
    for ln in lines:
        if ln.startswith("## "):
            inside = ln.strip() == "## Current Frontier"; continue
        if not inside or not ln.startswith("|"):
            continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) < 2 or not c[0].strip("` ").isdigit():
            continue
        lm = re.search(r"`([A-Za-z0-9._-]*\.\d+)`", c[1])
        if lm:
            nxt = lm.group(1); break
    return status, leaves, nxt

trees = {}
if tasks_dir.is_dir():
    for p in sorted(tasks_dir.glob("*.md")):
        if p.stem == "TEMPLATE":
            continue
        trees[p.stem] = parse_tree(p)
if not trees:
    print(f"NO TREES   {tasks_dir} yields no task-trees — cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

TREEREF  = re.compile(r"`(?P<id>[A-Z][A-Za-z0-9-]*)`|\(?[^()]*tasks/(?P<id2>[A-Za-z0-9._-]+)\.md\)")
A_OF_B   = re.compile(r"(?P<a>\d+)\s+of\s+(?P<b>\d+)\s+leaves?\b")
B_ONLY   = re.compile(r"(?<![\w/])(?P<b>\d+)\s+leaves?\b")
LEAFREF  = re.compile(r"`(?P<leaf>[A-Za-z0-9._-]+\.\d+)`")

def tree_at(line, pos):
    """The tree this claim is about: the nearest tree reference to its LEFT on the same line."""
    best = None
    for m in TREEREF.finditer(line):
        if m.start() >= pos:
            break
        name = m.group("id") or m.group("id2")
        if name in trees:
            best = name
    return best

checked = 0
for rel in live:
    path = root / rel
    if not path.is_file():
        findings.append(f"NO LIVE DOC {rel} is registered hot_live but does not exist")
        continue
    checked += 1
    for line in path.read_text().splitlines():
        # 1. COUNT ---------------------------------------------------------------
        spans = []
        for m in A_OF_B.finditer(line):
            spans.append((m.start(), m.end()))
            t = tree_at(line, m.start())
            if not t:
                continue
            _, leaves, _ = trees[t]
            real_b = len(leaves)
            real_a = sum(1 for s in leaves.values() if s == "done")
            if (int(m.group("a")), int(m.group("b"))) != (real_a, real_b):
                findings.append(
                    f"COUNT DRIFT {rel}: '{m.group(0)}' for {t}; the tree has {real_a} of {real_b}")
        for m in B_ONLY.finditer(line):
            if any(s <= m.start() < e for s, e in spans):
                continue                          # already covered by the A-of-B form
            t = tree_at(line, m.start())
            if not t:
                continue
            _, leaves, _ = trees[t]
            if int(m.group("b")) != len(leaves):
                findings.append(
                    f"COUNT DRIFT {rel}: '{m.group(0)}' for {t}; the tree has {len(leaves)}")
        # 2. FRONTIER ------------------------------------------------------------
        # ⛔ Anchored on the LABEL, not on the words. A first cut matched any line mentioning
        # "frontier leaf" and fired twice on MEMORY.md — once on the pointer and once on a
        # sentence that merely described it. A rule that fires on prose teaches its reader to
        # re-word the prose.
        if re.match(r"^\s*[-*]?\s*\**\s*Frontier\s+leaf\s*\**\s*:", line, re.I):
            for m in LEAFREF.finditer(line):
                leaf = m.group("leaf")
                t = leaf.rsplit(".", 1)[0]
                if t not in trees:
                    findings.append(f"UNKNOWN TREE {rel}: frontier leaf '{leaf}' names no tree")
                    continue
                _, leaves, nxt = trees[t]
                if leaves.get(leaf) == "done":
                    findings.append(
                        f"DONE FRONTIER {rel}: names '{leaf}' as the frontier; the tree records it `done`")
                elif nxt and leaf != nxt:
                    findings.append(
                        f"FRONTIER DRIFT {rel}: names '{leaf}'; the tree's Current Frontier says '{nxt}'")
        # 3. ACTIVE --------------------------------------------------------------
        if re.search(r"active\s+trees?\s*:", line, re.I):
            named = {m.group("id") or m.group("id2") for m in TREEREF.finditer(line)}
            named = {n for n in named if n in trees}
            for n in sorted(named):
                if trees[n][0] != "active":
                    findings.append(
                        f"NOT ACTIVE {rel}: names '{n}' as active; its Metadata says '{trees[n][0]}'")
            for n, (st, _, _) in sorted(trees.items()):
                if st == "active" and n not in named:
                    findings.append(
                        f"MISSING ACTIVE {rel}: '{n}' is `active` and the pointer does not name it")

# One breach reported once: the same finding can be reachable by more than one line.
seen = set()
for f in findings:
    if f not in seen:
        seen.add(f); print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/tasks"

  # ⛔ STRICT ARITY — see docs/knowledge/self-test-arms-that-never-ran.md. A helper that ignores
  # surplus arguments swallows a whole following command when a `;` is missing, silently.
  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'TREE-CLAIMS self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "$3" "$2" "$1" >&2
    return 1
  }

  tree() { # tree <id> <status> <leaf1-status> <leaf2-status> <frontier-leaf-n>
    argc 5 "$#" tree || return
    cat > "$t/tasks/$1.md" <<EOF
# $1

## Metadata

- Status: \`$2\`

## Task Tree

- ID: \`$1.1\`
  Status: \`$3\`

- ID: \`$1.2\`
  Status: \`$4\`

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | \`$1.$5\` | \`pending\` | because |
EOF
  }
  doc() { argc 1 "$#" doc || return; printf '%s\n' "$1" > "$t/L.md"; }
  routes() { printf '#c1\tc2\tc3\nL.md\tboth\thot_live\towner\t0\t0\t0\t0\t0\n' > "$t/r.tsv"; }
  arm() { # arm <name> <expected-rc> <expected-substring>
    argc 3 "$#" arm || return
    out="$(check_claims "$t" r.tsv tasks 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'TREE-CLAIMS self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'TREE-CLAIMS self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  routes; tree ALPHA active done pending 2
  doc '- **Active trees:** `ALPHA` (1 of 2 leaves).
- **Frontier leaf:** `ALPHA.2` — second.';                  arm "GREEN every claim re-derived"    0 "__CHECKED__ 1"

  doc '- **Active trees:** `ALPHA` (1 of 3 leaves).
- **Frontier leaf:** `ALPHA.2` — second.';                  arm "RED   the A-of-B count drifts"   1 "COUNT DRIFT"
  doc '- **Active trees:** `ALPHA` — 7 leaves.
- **Frontier leaf:** `ALPHA.2` — second.';                  arm "RED   the bare total drifts"     1 "COUNT DRIFT"
  doc '- **Active trees:** `ALPHA` (1 of 2 leaves).
- **Frontier leaf:** `ALPHA.1` — first.';                   arm "RED   the pointer names a done leaf" 1 "DONE FRONTIER"

  tree ALPHA active pending pending 1
  doc '- **Active trees:** `ALPHA` (0 of 2 leaves).
- **Frontier leaf:** `ALPHA.2` — second.';                  arm "RED   the pointer names the wrong leaf" 1 "FRONTIER DRIFT"
  doc '- **Active trees:** `ALPHA` (0 of 2 leaves).
- **Frontier leaf:** `BETA.1` — nonexistent.';              arm "RED   the pointer names no tree" 1 "UNKNOWN TREE"

  tree ALPHA proposed pending pending 1
  doc '- **Active trees:** `ALPHA` (0 of 2 leaves).
- **Frontier leaf:** `ALPHA.1` — first.';                   arm "RED   a named tree is not active" 1 "NOT ACTIVE"

  tree ALPHA active pending pending 1; tree BETA active pending pending 1
  doc '- **Active trees:** `ALPHA` (0 of 2 leaves).
- **Frontier leaf:** `ALPHA.1` — first.';                   arm "RED   an active tree is unnamed" 1 "MISSING ACTIVE"
  rm -f "$t/tasks/BETA.md"

  doc '- **Active trees:** `ALPHA` (0 of 2 leaves).
- **Frontier leaf:** `ALPHA.1` — first.'
  rm -f "$t/L.md";                                          arm "RED   a live doc does not exist" 1 "NO LIVE DOC"
  doc '- **Active trees:** `ALPHA` (0 of 2 leaves).
- **Frontier leaf:** `ALPHA.1` — first.'

  printf '#c1\tc2\tc3\nCHANGELOG.md\tboth\tappend_history\towner\t0\t0\t0\t0\t0\n' > "$t/r.tsv"
                                                            arm "REFUSE history is not a live doc" 2 "NO LIVE DOCS"
  routes; rm -f "$t/tasks/ALPHA.md";                        arm "REFUSE no trees to check against" 2 "NO TREES"
  tree ALPHA active pending pending 1
  rm -f "$t/r.tsv";                                         arm "REFUSE the routes registry is gone" 2 "NO ROUTES"

  rm -rf "$t"
  printf 'TREE-CLAIMS --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -f doctrine/readme_routes.tsv ] || { echo "TREE-CLAIMS: ok (no routes registry yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "TREE-CLAIMS: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_claims . doctrine/readme_routes.tsv docs/tasks)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "TREE-CLAIMS: REFUSED — the live-document scope could not be established."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "TREE-CLAIMS: a live document states a tree fact that the tree contradicts."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The TREE is authoritative. Re-derive the number — never edit a tree to match a summary."; } >&2
  exit 1
fi
printf 'TREE-CLAIMS: ok (%s live document(s) state nothing the trees contradict)\n' "${count:-0}"
exit 0
