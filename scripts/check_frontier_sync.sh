#!/usr/bin/env bash
# scripts/check_frontier_sync.sh — FRONTIER-SYNC (project doctrine).
#
# `docs/TASK_TREE.md` is a HAND-KEPT MIRROR of the task-trees under `docs/tasks/`. `COMMIT.md`
# updates it "only if the frontier changes" — a CONDITIONAL manual step, and a conditional
# manual step is the shape that rots. When it rots it rots silently, because both files read
# perfectly: the index says one leaf, the tree says another, and nothing compares them.
#
# ⭐ WHY THIS PARTICULAR MIRROR IS LOAD-BEARING. It is the second hop of the documented resume
# path: `MEMORY.md` → the index row → the tree's frontier → the next action. A session that
# crashed is told by `CLAUDE.md` to resume through it. A stale frontier cell therefore does not
# mislead a reader browsing the repository — it misdirects the recovery procedure itself, and it
# does so on the ONE row that is followed, because only an `active` tree's row is ever read.
#
# What is compared, all of it derivable from the trees:
#   1. FRONTIER   the leaf the index names == the leaf the tree's own Current Frontier names first,
#                 in both directions: an index behind the tree (STALE FRONTIER) and an index that
#                 retires a tree still carrying a frontier (PREMATURE COMPLETE) are both breaches.
#   2. DONE       neither of them names a leaf the tree records as `done`.
#   3. STATUS     the index's status cell == the tree's Metadata status.
#   4. COUNT      an index cell claiming `(A/B leaves complete)` or `A of B leaves done` matches
#                 the tree's real A and B — a count typed by hand is a constant, and a constant
#                 that is a function of the repository is derived or gated, never carried.
#   5. CLOSURE    every tree file has exactly one row — in the index while it is open, in the
#                 closed-tree register (`docs/TASK_TREE_CLOSED.md`) once it is `done` — and every
#                 row names a tree file. The index's registered pressure control is "one row per
#                 active tree; completed trees leave the index" (LIVE-CONTAINMENT.1): a `done`
#                 tree still in the index, an open tree in the register, and a tree in both are
#                 breaches. Every other check runs on the register's rows too.
#   6. EXISTS     every leaf id either file names is a leaf the tree actually declares.
#
# ⚠️ HONEST LIMIT, stated rather than implied: this proves the two documents AGREE and that
# their numbers are functions of the tree. It cannot prove the tree's own frontier ordering is
# the right engineering choice — that is a judgement, and it is the author's.
#
# ⛔ It REFUSES (exit 2) rather than passing if it parses no index rows or no leaves. A mirror
# checker that silently matches nothing is worse than no checker, because it reports agreement.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "FRONTIER-SYNC: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

# $1 = a directory holding TASK_TREE.md and tasks/. Prints findings, then __CHECKED__ <n>.
check_frontier() {
python3 - "$1" <<'PY'
import re, sys, pathlib

root = pathlib.Path(sys.argv[1])
index_path = root / "TASK_TREE.md"
tasks_dir  = root / "tasks"
findings = []

if not index_path.is_file():
    print(f"NO INDEX   {index_path} does not exist"); print("__CHECKED__ 0"); sys.exit(2)

text = index_path.read_text()
# The index rows live between the anchors when they exist; otherwise every table row counts.
m = re.search(r"<!-- ANCHOR: trees -->(.*?)<!-- ANCHOR_END: trees -->", text, re.S)
block = m.group(1) if m else text
# The closed-tree register (LIVE-CONTAINMENT.1) — optional: a repository whose trees are all
# open has none. Its rows live between their own anchors.
closed_path = root / "TASK_TREE_CLOSED.md"
closed_block = ""
if closed_path.is_file():
    mc_ = re.search(r"<!-- ANCHOR: closed -->(.*?)<!-- ANCHOR_END: closed -->",
                    closed_path.read_text(), re.S)
    if not mc_:
        print(f"NO ANCHORS {closed_path.name} has no `<!-- ANCHOR: closed -->` block — the "
              f"register cannot be read"); print("__CHECKED__ 0"); sys.exit(2)
    closed_block = mc_.group(1)

ROW  = re.compile(r"^\|(?P<cells>.*)\|\s*$", re.M)
LINK = re.compile(r"\(tasks/(?P<id>[A-Za-z0-9][A-Za-z0-9._-]*)\.md\)")
# A leaf reference is `.N` or `TREE.N`, always inside backticks in both documents.
LEAF = re.compile(r"`(?P<leaf>[A-Za-z0-9._-]*\.\d+)`")
# Both spellings the index actually uses for a derived leaf count.
DONE_COUNTS = (re.compile(r"\((?P<a>\d+)\s*/\s*(?P<b>\d+)\s+leaves?\s+complete\)"),
               re.compile(r"(?P<a>\d+)\s+of\s+(?P<b>\d+)\s+leaves?\s+done"))

def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def unticks(s):
    t = re.findall(r"`([^`]+)`", s)
    return t[0] if t else s.strip()

def suffix(leaf):
    """`.5` and `P0-PROFILE.5` both denote leaf 5 — compare on the numeric tail."""
    return "." + leaf.rsplit(".", 1)[1]

# ---------------------------------------------------------------- parse the index rows
def table_rows(blk):
    out = {}
    for line in ROW.findall(blk):
        line = "|" + line + "|"
        c = cells(line)
        if len(c) < 3 or set("".join(c)) <= set("- :"):
            continue                                # separator or malformed
        link = LINK.search(c[0])
        if not link:
            continue                                # the header row, or a non-tree row
        out[link.group("id")] = (c[1], c[2] if len(c) > 2 else "")
    return out

rows = table_rows(block)            # tree id -> (status cell, frontier cell): the open trees
closed = table_rows(closed_block)   # the same shape, for the completed trees

if not rows:
    print("NO ROWS    the index parsed to zero tree rows — the checker cannot judge")
    print("__CHECKED__ 0"); sys.exit(2)

# ---------------------------------------------------------------- parse each tree file
def parse_tree(path):
    t = path.read_text()
    status = None
    ms = re.search(r"^- Status:\s*(.+)$", t, re.M)
    if ms:
        status = unticks(ms.group(1))
    # leaves: "- ID: `TREE.N`" followed (within its block) by "Status: `x`"
    leaves = {}
    lines = t.splitlines()
    for i, ln in enumerate(lines):
        mi = re.match(r"^- ID:\s*`([A-Za-z0-9._-]+\.\d+)`", ln)
        if not mi:
            continue
        leaf = mi.group(1)
        st = None
        for ln2 in lines[i + 1 : i + 8]:
            if re.match(r"^- ID:\s*`", ln2):
                break
            m2 = re.search(r"^\s*Status:\s*`([a-z_]+)`", ln2)
            if m2:
                st = m2.group(1); break
        leaves[leaf] = st
    # the Current Frontier table's data rows, in file order
    frontier = []
    inside = False
    for ln in lines:
        if ln.startswith("## "):
            inside = ln.strip() == "## Current Frontier"
            continue
        if not inside or not ln.startswith("|"):
            continue
        c = cells(ln)
        if len(c) < 3 or c[0].lower() in ("order",) or set("".join(c)) <= set("- :"):
            continue
        order = c[0].strip("`")
        leaf_m = LEAF.search(c[1])
        frontier.append((order, leaf_m.group("leaf") if leaf_m else None, unticks(c[2])))
    return status, leaves, frontier

checked = 0
for tree_id in sorted(set(rows) & set(closed)):
    findings.append(f"DUPLICATE ROW {tree_id}: the tree has a row in the index AND in "
                    f"{closed_path.name} — exactly one home, by its status")
every = [(t, v, "index") for t, v in rows.items()] + [(t, v, "closed") for t, v in closed.items()]
for tree_id, (status_cell, frontier_cell), home in sorted(every):
    path = tasks_dir / f"{tree_id}.md"
    if not path.is_file():
        findings.append(f"NO TREE FILE {tree_id}: the index links tasks/{tree_id}.md, which does not exist")
        continue
    checked += 1
    tree_status, leaves, frontier = parse_tree(path)

    if not leaves:
        findings.append(f"NO LEAVES  {tree_id}: the tree declares no `- ID:` leaf — the index mirrors nothing")
        continue

    # 3. STATUS ------------------------------------------------------------------
    idx_status = unticks(status_cell)
    if tree_status is None:
        findings.append(f"NO STATUS  {tree_id}: the tree has no `- Status:` line in its Metadata")
    elif idx_status != tree_status:
        findings.append(
            f"STATUS DRIFT {tree_id}: index says '{idx_status}', tree Metadata says '{tree_status}'")
    if home == "index" and tree_status == "done":
        findings.append(
            f"COMPLETED IN INDEX {tree_id}: the tree is `done` — completed trees leave the index "
            f"(its registered pressure control); move the row, verbatim, to {closed_path.name}")
    if home == "closed" and tree_status is not None and tree_status != "done":
        findings.append(
            f"OPEN TREE IN REGISTER {tree_id}: {closed_path.name} holds a tree whose Metadata "
            f"says '{tree_status}' — an open tree's row lives in the index, where resume reads it")

    # the tree's own next frontier leaf: the first row carrying a numeric order
    tree_next = None
    for order, leaf, st in frontier:
        if order.isdigit() and leaf:
            tree_next = (leaf, st); break

    idx_leaves = [m.group("leaf") for m in LEAF.finditer(frontier_cell)]

    # 6. EXISTS ------------------------------------------------------------------
    known = {suffix(k) for k in leaves}
    for leaf in idx_leaves:
        if suffix(leaf) not in known:
            findings.append(
                f"UNKNOWN LEAF {tree_id}: the index names '{leaf}', which the tree does not declare")
    for _, leaf, _ in frontier:
        if leaf and suffix(leaf) not in known:
            findings.append(
                f"UNKNOWN LEAF {tree_id}: its Current Frontier names '{leaf}', which the tree does not declare")

    # 1. FRONTIER ----------------------------------------------------------------
    if tree_next is None:
        if idx_leaves:
            findings.append(
                f"STALE FRONTIER {tree_id}: the index still points at '{idx_leaves[0]}', "
                f"but the tree's Current Frontier names no next leaf")
    else:
        want = suffix(tree_next[0])
        got = [suffix(x) for x in idx_leaves]
        if not got:
            findings.append(
                f"PREMATURE COMPLETE {tree_id}: the tree's frontier is '{tree_next[0]}', "
                f"but the index row retires it — naming no leaf at all")
        elif want not in got:
            findings.append(
                f"FRONTIER DRIFT {tree_id}: index says '{idx_leaves[0]}', "
                f"tree's Current Frontier says '{tree_next[0]}'")

        # 2. DONE --------------------------------------------------------------
        real = None
        for k, st in leaves.items():
            if suffix(k) == want:
                real = st; break
        if real == "done":
            findings.append(
                f"DONE FRONTIER {tree_id}: the frontier points at '{tree_next[0]}', "
                f"which the tree records as `done` — a finished leaf is not a next action")

    for leaf in idx_leaves:
        s = suffix(leaf)
        for k, st in leaves.items():
            if suffix(k) == s and st == "done" and (tree_next is None or suffix(tree_next[0]) != s):
                findings.append(
                    f"DONE FRONTIER {tree_id}: the index points at '{leaf}', "
                    f"which the tree records as `done`")

    # 4. COUNT -------------------------------------------------------------------
    mc = next((m for m in (r.search(frontier_cell) for r in DONE_COUNTS) if m), None)
    if mc:
        a, b = int(mc.group("a")), int(mc.group("b"))
        real_b = len(leaves)
        real_a = sum(1 for st in leaves.values() if st == "done")
        if (a, b) != (real_a, real_b):
            findings.append(
                f"COUNT DRIFT {tree_id}: the index claims {a}/{b} leaves complete; "
                f"the tree has {real_a}/{real_b}")

# 5. CLOSURE ---------------------------------------------------------------------
if tasks_dir.is_dir():
    for path in sorted(tasks_dir.glob("*.md")):
        if path.stem == "TEMPLATE":
            continue
        if path.stem not in rows and path.stem not in closed:
            findings.append(
                f"UNLISTED TREE {path.stem}: tasks/{path.name} exists with no row in the index "
                f"or the closed-tree register — a tree nobody can reach is a tree nobody resumes")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"; mkdir -p "$t/tasks"

  # ⛔ STRICT ARITY. A fixture helper that ignores its extra arguments will swallow a whole
  # following command when a `;` is missing — `index a b arm NAME 1 WHY` is ONE call, and the
  # arm vanishes with no error. That measured defect ran 4 of 14 arms and reported `0 fail`.
  # See docs/knowledge/self-test-arms-that-never-ran.md.
  argc() { # argc <expected> <got> <helper>
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf '%s self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' \
      "FRONTIER-SYNC" "$3" "$2" "$1" >&2
    return 1
  }


  tree() { # tree() <id> <metadata-status> <frontier-leaf-or-dash> <frontier-status> <leaf1-status> <leaf2-status>
    argc 6 "$#" tree || return
    cat > "$t/tasks/$1.md" <<EOF
# $1: synthetic

## Metadata

- Tree ID: \`$1\`
- Status: \`$2\`

## Task Tree

- ID: \`$1.1\`
  Status: \`$5\`
  Goal: first

- ID: \`$1.2\`
  Status: \`$6\`
  Goal: second

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| $( [ "$3" = "-" ] && echo "—" || echo 1 ) | $( [ "$3" = "-" ] && echo "—" || echo "\`$1.$3\`" ) | \`$4\` | because |
EOF
  }
  index() { # index() <status-cell> <frontier-cell>
    argc 2 "$#" index || return
    cat > "$t/TASK_TREE.md" <<EOF
# index

<!-- ANCHOR: trees -->
| Tree | Status | Frontier (next leaf) | Owner |
| --- | --- | --- | --- |
| [\`T\`](tasks/T.md) | \`$1\` | $2 | repo-local |
<!-- ANCHOR_END: trees -->
EOF
  }
  index_for() { # index_for() <id> <status-cell> <frontier-cell> — a one-row index for tree <id>
    argc 3 "$#" index_for || return
    cat > "$t/TASK_TREE.md" <<EOF
# index

<!-- ANCHOR: trees -->
| Tree | Status | Frontier (next leaf) | Owner |
| --- | --- | --- | --- |
| [\`$1\`](tasks/$1.md) | \`$2\` | $3 | repo-local |
<!-- ANCHOR_END: trees -->
EOF
  }
  closed() { # closed() <id> <status-cell> <frontier-cell> — a one-row closed-tree register
    argc 3 "$#" closed || return
    cat > "$t/TASK_TREE_CLOSED.md" <<EOF
# closed

<!-- ANCHOR: closed -->
| Tree | Status | Outcome | Owner |
| --- | --- | --- | --- |
| [\`$1\`](tasks/$1.md) | \`$2\` | $3 | repo-local |
<!-- ANCHOR_END: closed -->
EOF
  }
  arm() { # arm <name> <expected-rc> <expected-substring>
    out="$(check_frontier "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'FRONTIER-SYNC self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'FRONTIER-SYNC self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  tree T active 2 pending done pending
  index active '`.2` — second';                arm "GREEN index mirrors the tree"    0 "__CHECKED__ 1"

  index active '`.1` — first';                 arm "RED   index names another leaf"  1 "FRONTIER DRIFT"
  index active 'second, no leaf id';           arm "RED   index names no leaf at all"  1 "PREMATURE COMPLETE"
  index proposed '`.2` — second';              arm "RED   status cell disagrees"     1 "STATUS DRIFT"
  index active '`.9` — ninth';                 arm "RED   index names a nonexistent leaf" 1 "UNKNOWN LEAF"
  index active '— (2/2 leaves complete)';      arm "RED   index retires a tree that has a frontier" 1 "PREMATURE COMPLETE"

  tree T active 1 pending done pending
  index active '`.1` — first';                 arm "RED   frontier points at a done leaf" 1 "DONE FRONTIER"

  # Completed trees live in the closed-tree register (LIVE-CONTAINMENT.1); an open companion A
  # keeps the index non-empty.
  tree A active 2 pending done pending
  index_for A active '`.2` — second'
  tree T done - done done done
  closed T done '— (2/2 leaves complete)';     arm "GREEN completed tree in the register" 0 "__CHECKED__ 2"
  closed T done '— (1/3 leaves complete)';     arm "RED   completed count drifts"   1 "COUNT DRIFT"
  closed T done '— (0 of 7 leaves done)';      arm "RED   the prose spelling drifts too" 1 "COUNT DRIFT"
  closed T done '`.2` — second';               arm "RED   register points at a retired frontier" 1 "STALE FRONTIER"
  rm -f "$t/TASK_TREE_CLOSED.md"
  index done '— (2/2 leaves complete)';        arm "RED   a completed tree left in the index" 1 "COMPLETED IN INDEX"
  tree A active 2 pending done pending
  index_for A active '`.2` — second'
  closed T done '— (2/2 leaves complete)'
  tree T active 2 pending done pending;        arm "RED   an open tree in the register" 1 "OPEN TREE IN REGISTER"
  index active '`.2` — second';                arm "RED   a tree with a row in both files" 1 "DUPLICATE ROW"
  printf '# closed\n\nno anchors here\n' > "$t/TASK_TREE_CLOSED.md"
                                              arm "REFUSE a register with no anchors" 2 "NO ANCHORS"
  rm -f "$t/TASK_TREE_CLOSED.md" "$t/tasks/A.md"

  tree T active 9 pending done pending
  index active '`.9` — ninth';                 arm "RED   the tree's own frontier leaf does not exist" 1 "UNKNOWN LEAF"

  tree T active 2 pending done pending
  index active '`.2` — second'
  printf '# U\n\n## Metadata\n\n- Status: `active`\n' > "$t/tasks/U.md"
                                              arm "RED   a tree with no index row"  1 "UNLISTED TREE"
  rm -f "$t/tasks/U.md"

  rm -f "$t/tasks/T.md";                      arm "RED   the index links a missing tree file" 1 "NO TREE FILE"

  printf '# index\n\nno table here\n' > "$t/TASK_TREE.md"
                                              arm "REFUSE no parseable rows"       2 "NO ROWS"
  rm -f "$t/TASK_TREE.md";                    arm "REFUSE no index at all"         2 "NO INDEX"

  rm -rf "$t"
  printf 'FRONTIER-SYNC --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

[ -f docs/TASK_TREE.md ] || { echo "FRONTIER-SYNC: ok (no docs/TASK_TREE.md yet)"; exit 0; }
self_test >/dev/null 2>&1 || {
  echo "FRONTIER-SYNC: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_frontier docs)"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "FRONTIER-SYNC: REFUSED — the index could not be parsed, so agreement cannot be judged."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "FRONTIER-SYNC: the task-tree index no longer mirrors the trees it indexes."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  The TREE is authoritative. Fix the index row — never the tree, to make them agree."; } >&2
  exit 1
fi
printf 'FRONTIER-SYNC: ok (%s tree(s) mirrored by docs/TASK_TREE.md)\n' "${count:-0}"
exit 0
