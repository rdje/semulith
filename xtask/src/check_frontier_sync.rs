//! The `FRONTIER-SYNC` doctrine's driver, ported from `scripts/check_frontier_sync.sh` (`XTASK.6` slice `6ab`), which is
//! now a shim of `cargo xtask check-frontier-sync`.
//!
//! The task-tree index (`docs/TASK_TREE.md`) and the closed-tree register (`docs/TASK_TREE_CLOSED.md`) must mirror the
//! trees they index — status, frontier leaf, every count in a cell — and every tree must have exactly one row; the TREE
//! is authoritative, the row is fixed to agree. The judge is the driver's inline Python, reading every tree through the
//! shared `task_source` reader (archived ranges qualified); it runs verbatim through `python3 -`, as the script ran it,
//! and is not ported. The controls write the script's synthetic trees, index and register (its heredocs verbatim, its
//! `source_edit` as the same single replacement). Each self-test arm is one `tally.arm(` call, the idiom the
//! `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::scratch;

/// The judge, verbatim: `python3 - <docs root> <scripts dir>`.
const JUDGE: &str = r###"import re, sys, pathlib
sys.path.insert(0, sys.argv[2])
try:
    from task_source import TaskSourceError, read_task
except ImportError as error:
    print("UNAVAILABLE TASK READER " + str(error)); print("__CHECKED__ 0"); sys.exit(2)


def task_source(path):
    try:
        return read_task(path)
    except TaskSourceError as error:
        print("UNAVAILABLE TASK SOURCE " + str(error)); print("__CHECKED__ 0"); sys.exit(2)

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
DONE_COUNTS = (re.compile(r"\((?P<a>\d+)\s*/\s*(?P<b>\d+)\s+leaves?\s+complete(?=\s*[;,)])"),
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
    facts = task_source(path)
    status, leaves, lines = facts.status, facts.leaves, facts.text.splitlines()
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
    for mc in (m for pattern in DONE_COUNTS for m in pattern.finditer(frontier_cell)):
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
"###;

/// The script's `archive_fixture` root, verbatim.
const ARCHIVED_ROOT: &str = "# T\n- Tree ID: `T`\n- Status: `active`\n_Leaves `.1`–`.1` (done `2026-10-01`) — live in [archive](archive/T.md)._\n- ID: `T.2`\n  Status: `pending`\n## Current Frontier\n| Order | Leaf | Status | Why next |\n| --- | --- | --- | --- |\n| 1 | `T.2` | `pending` | next |\n";

/// `check_frontier <root>`: the judge on stdin, the scripts directory as its reader's path; with `both`, stdout and
/// stderr together as `2>&1` joined them, else stdout alone with stderr passing through.
fn check_frontier(repo: &Path, root: &str, both: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .arg(root)
        .arg(repo.join("scripts"))
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(if both {
            Stdio::piped()
        } else {
            Stdio::inherit()
        });
    let Ok(mut child) = command.spawn() else {
        return (-1, "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(JUDGE.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            text.push_str(&String::from_utf8_lossy(&o.stderr));
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

fn write(path: &Path, text: &str) {
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    let _ = fs::write(path, text);
}

fn append(path: &Path, text: &str) {
    let mut bytes = fs::read(path).unwrap_or_default();
    bytes.extend_from_slice(text.as_bytes());
    let _ = fs::write(path, bytes);
}

/// The script's `tree` heredoc: `<id> <metadata-status> <frontier-leaf-or-dash> <frontier-status> <leaf1> <leaf2>`.
fn tree_text(
    id: &str,
    status: &str,
    frontier: &str,
    fstatus: &str,
    leaf1: &str,
    leaf2: &str,
) -> String {
    let (order, leaf) = if frontier == "-" {
        ("—".to_owned(), "—".to_owned())
    } else {
        ("1".to_owned(), format!("`{id}.{frontier}`"))
    };
    format!(
        "# {id}: synthetic\n\n## Metadata\n\n- Tree ID: `{id}`\n- Status: `{status}`\n\n## Task Tree\n\n- ID: `{id}.1`\n  Status: `{leaf1}`\n  Goal: first\n\n- ID: `{id}.2`\n  Status: `{leaf2}`\n  Goal: second\n\n## Current Frontier\n\n| Order | Leaf | Status | Why next |\n| --- | --- | --- | --- |\n| {order} | {leaf} | `{fstatus}` | because |\n"
    )
}

/// The script's `index_for` heredoc (`index` is `index_for T`).
fn index_text(id: &str, status: &str, frontier: &str) -> String {
    format!(
        "# index\n\n<!-- ANCHOR: trees -->\n| Tree | Status | Frontier (next leaf) | Owner |\n| --- | --- | --- | --- |\n| [`{id}`](tasks/{id}.md) | `{status}` | {frontier} | repo-local |\n<!-- ANCHOR_END: trees -->\n"
    )
}

/// The script's `closed` heredoc.
fn closed_text(id: &str, status: &str, outcome: &str) -> String {
    format!(
        "# closed\n\n<!-- ANCHOR: closed -->\n| Tree | Status | Outcome | Owner |\n| --- | --- | --- | --- |\n| [`{id}`](tasks/{id}.md) | `{status}` | {outcome} | repo-local |\n<!-- ANCHOR_END: closed -->\n"
    )
}

struct Tally<'a> {
    repo: &'a Path,
    root: &'a Path,
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally<'_> {
    /// One arm: judging the fixture tree must give `expected` and contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let (rc, out) = check_frontier(self.repo, &self.root.display().to_string(), true);
        let out = captured(&out);
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("FRONTIER-SYNC self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}");
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("FRONTIER-SYNC self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }

    /// The script's `source_edit`: exactly one occurrence replaced in the T tree, or the fixture seam is a failure.
    fn source_edit(&mut self, from: &str, to: &str) {
        let path = self.root.join("tasks/T.md");
        let text = fs::read_to_string(&path).unwrap_or_default();
        if text.matches(from).count() != 1 {
            self.fail += 1;
            if self.verbose {
                eprintln!("source fixture edit failed rc=1");
            }
            return;
        }
        let _ = fs::write(&path, text.replacen(from, to, 1));
    }
}

/// The RED/GREEN controls over the script's synthetic trees, index and register.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "frontiersync") else {
        eprintln!("FRONTIER-SYNC self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let _ = fs::create_dir_all(t.join("tasks"));
    let tree = |id: &str, status: &str, frontier: &str, fstatus: &str, l1: &str, l2: &str| {
        write(
            &t.join(format!("tasks/{id}.md")),
            &tree_text(id, status, frontier, fstatus, l1, l2),
        )
    };
    let index = |status: &str, frontier: &str| {
        write(&t.join("TASK_TREE.md"), &index_text("T", status, frontier))
    };
    let index_for = |id: &str, status: &str, frontier: &str| {
        write(&t.join("TASK_TREE.md"), &index_text(id, status, frontier))
    };
    let closed = |id: &str, status: &str, outcome: &str| {
        write(
            &t.join("TASK_TREE_CLOSED.md"),
            &closed_text(id, status, outcome),
        )
    };
    let archive_fixture = || {
        let _ = fs::create_dir_all(t.join("tasks/archive"));
        write(&t.join("tasks/T.md"), ARCHIVED_ROOT);
        write(
            &t.join("tasks/archive/T.md"),
            "- ID: `T.1`\n  Status: `done`\n",
        );
    };
    let mut tally = Tally {
        repo,
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
    };
    tree("T", "active", "2", "pending", "done", "pending");
    index("active", "`.2` — second");
    tally.arm("GREEN index mirrors the tree", 0, "__CHECKED__ 1");
    index("active", "`.1` — first");
    tally.arm("RED   index names another leaf", 1, "FRONTIER DRIFT");
    index("active", "second, no leaf id");
    tally.arm("RED   index names no leaf at all", 1, "PREMATURE COMPLETE");
    index("proposed", "`.2` — second");
    tally.arm("RED   status cell disagrees", 1, "STATUS DRIFT");
    index("active", "`.9` — ninth");
    tally.arm("RED   index names a nonexistent leaf", 1, "UNKNOWN LEAF");
    index("active", "— (2/2 leaves complete)");
    tally.arm(
        "RED   index retires a tree that has a frontier",
        1,
        "PREMATURE COMPLETE",
    );
    tree("T", "active", "1", "pending", "done", "pending");
    index("active", "`.1` — first");
    tally.arm("RED   frontier points at a done leaf", 1, "DONE FRONTIER");
    // Completed trees live in the closed-tree register (LIVE-CONTAINMENT.1); an open companion A keeps the index non-empty.
    tree("A", "active", "2", "pending", "done", "pending");
    index_for("A", "active", "`.2` — second");
    tree("T", "done", "-", "done", "done", "done");
    closed("T", "done", "— (2/2 leaves complete)");
    tally.arm("GREEN completed tree in the register", 0, "__CHECKED__ 2");
    closed("T", "done", "— (1/3 leaves complete)");
    tally.arm("RED   completed count drifts", 1, "COUNT DRIFT");
    closed("T", "done", "— (0 of 7 leaves done)");
    tally.arm("RED   the prose spelling drifts too", 1, "COUNT DRIFT");
    closed("T", "done", "`.2` — second");
    tally.arm(
        "RED   register points at a retired frontier",
        1,
        "STALE FRONTIER",
    );
    let _ = fs::remove_file(t.join("TASK_TREE_CLOSED.md"));
    index("done", "— (2/2 leaves complete)");
    tally.arm(
        "RED   a completed tree left in the index",
        1,
        "COMPLETED IN INDEX",
    );
    tree("A", "active", "2", "pending", "done", "pending");
    index_for("A", "active", "`.2` — second");
    closed("T", "done", "— (2/2 leaves complete)");
    tree("T", "active", "2", "pending", "done", "pending");
    tally.arm(
        "RED   an open tree in the register",
        1,
        "OPEN TREE IN REGISTER",
    );
    index("active", "`.2` — second");
    tally.arm("RED   a tree with a row in both files", 1, "DUPLICATE ROW");
    write(
        &t.join("TASK_TREE_CLOSED.md"),
        "# closed\n\nno anchors here\n",
    );
    tally.arm("REFUSE a register with no anchors", 2, "NO ANCHORS");
    let _ = fs::remove_file(t.join("TASK_TREE_CLOSED.md"));
    let _ = fs::remove_file(t.join("tasks/A.md"));
    tree("T", "active", "9", "pending", "done", "pending");
    index("active", "`.9` — ninth");
    tally.arm(
        "RED   the tree's own frontier leaf does not exist",
        1,
        "UNKNOWN LEAF",
    );
    tree("T", "active", "2", "pending", "done", "pending");
    index("active", "`.2` — second");
    write(
        &t.join("tasks/U.md"),
        "# U\n\n## Metadata\n\n- Status: `active`\n",
    );
    tally.arm("RED   a tree with no index row", 1, "UNLISTED TREE");
    let _ = fs::remove_file(t.join("tasks/U.md"));
    let _ = fs::remove_file(t.join("tasks/T.md"));
    tally.arm(
        "RED   the index links a missing tree file",
        1,
        "NO TREE FILE",
    );
    write(&t.join("TASK_TREE.md"), "# index\n\nno table here\n");
    tally.arm("REFUSE no parseable rows", 2, "NO ROWS");
    let _ = fs::remove_file(t.join("TASK_TREE.md"));
    tally.arm("REFUSE no index at all", 2, "NO INDEX");
    // Shared-source qualification. The original controls above remain verbatim.
    let reset = || {
        tree("T", "active", "2", "pending", "done", "pending");
        index("active", "`.2` — 1 of 2 leaves done");
    };
    reset();
    tally.source_edit("Status: `done`", "Status: **done**");
    tally.arm("GREEN bold source status", 0, "__CHECKED__");
    reset();
    tally.source_edit("Status: `done`", "Status: `slice-gated`");
    index("active", "`.2` — 0 of 2 leaves done");
    tally.arm(
        "GREEN conditional source is not completed",
        0,
        "__CHECKED__",
    );
    reset();
    tally.source_edit("Status: `done`", "Status: `invented`");
    tally.arm("REFUSE unknown source status", 2, "UNAVAILABLE TASK SOURCE");
    reset();
    tally.source_edit("Status: `done`", "Missing: `done`");
    tally.arm("REFUSE missing source status", 2, "UNAVAILABLE TASK SOURCE");
    reset();
    append(&t.join("tasks/T.md"), "- ID: `T.1`\n  Status: `done`\n");
    tally.arm("REFUSE duplicate source ID", 2, "UNAVAILABLE TASK SOURCE");
    reset();
    tally.source_edit("Status: `done`", "Status: `done`\n  Status: `pending`");
    tally.arm("REFUSE duplicate leaf status", 2, "UNAVAILABLE TASK SOURCE");
    reset();
    append(&t.join("tasks/T.md"), "- Status: `active`\n");
    tally.arm("REFUSE duplicate root status", 2, "UNAVAILABLE TASK SOURCE");
    reset();
    let _ = fs::write(t.join("tasks/T.md"), [0xFFu8]);
    tally.arm(
        "REFUSE invalid UTF8 task source",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset();
    archive_fixture();
    tally.arm("GREEN checked whole archived range", 0, "__CHECKED__");
    reset();
    archive_fixture();
    let _ = fs::remove_file(t.join("tasks/archive/T.md"));
    tally.arm("REFUSE missing archive", 2, "UNAVAILABLE TASK SOURCE");
    reset();
    archive_fixture();
    write(
        &t.join("tasks/archive/T.md"),
        "- ID: `T.1`\n  Status: `pending`\n",
    );
    tally.arm(
        "REFUSE archive is not completed",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset();
    archive_fixture();
    write(
        &t.join("tasks/archive/T.md"),
        "- ID: `T.3`\n  Status: `done`\n",
    );
    tally.arm(
        "REFUSE archive has wrong population",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset();
    archive_fixture();
    append(&t.join("tasks/T.md"), "- ID: `T.1`\n  Status: `done`\n");
    tally.arm("REFUSE root archive overlap", 2, "UNAVAILABLE TASK SOURCE");
    reset();
    archive_fixture();
    append(
        &t.join("tasks/T.md"),
        "_Leaves `.1`–`.1` (done `2026-10-01`) — live in [archive](archive/T.md)._\n",
    );
    tally.arm(
        "REFUSE repeated archive declaration",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset();
    archive_fixture();
    tally.source_edit("archive/T.md", "archive/../T.md");
    tally.arm(
        "REFUSE unsafe archive locator",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset();
    archive_fixture();
    tally.source_edit("_Leaves", "_Leaves unsupported");
    tally.arm(
        "REFUSE unsupported archive declaration",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset();
    index("active", "`.2` — (0/2 leaves complete; scope)");
    tally.arm("RED semicolon annotated count drifts", 1, "COUNT DRIFT");
    reset();
    index("active", "`.2` — (0/2 leaves complete, scope)");
    tally.arm("RED comma annotated count drifts", 1, "COUNT DRIFT");
    reset();
    index(
        "active",
        "`.2` — (1/2 leaves complete); (0/2 leaves complete)",
    );
    tally.arm("RED every count in a cell is checked", 1, "COUNT DRIFT");
    reset();
    index("active", "`.2` — (1/2 leaves complete; scope)");
    tally.arm("GREEN annotated count agrees", 0, "__CHECKED__");
    archive_fixture();
    let _ = fs::rename(t.join("tasks/archive"), t.join("archive-source"));
    #[cfg(unix)]
    let _ = std::os::unix::fs::symlink(t.join("archive-source"), t.join("tasks/archive"));
    tally.arm(
        "REFUSE linked archive directory",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "FRONTIER-SYNC --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-frontier-sync [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !root.join("docs/TASK_TREE.md").is_file() {
        println!("FRONTIER-SYNC: ok (no docs/TASK_TREE.md yet)");
        return ExitCode::SUCCESS;
    }
    if !self_test(root, false) {
        eprintln!("FRONTIER-SYNC: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let (rc, out) = check_frontier(root, "docs", false);
    let out = captured(&out);
    let count = out
        .lines()
        .find_map(|l| l.strip_prefix("__CHECKED__ "))
        .unwrap_or("0");
    let body: Vec<&str> = out
        .lines()
        .filter(|l| !l.starts_with("__CHECKED__ "))
        .collect();
    match rc {
        2 => {
            eprintln!("FRONTIER-SYNC: REFUSED — the index could not be parsed, so agreement cannot be judged.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!("FRONTIER-SYNC: ok ({count} tree(s) mirrored by docs/TASK_TREE.md)");
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("FRONTIER-SYNC: the task-tree index no longer mirrors the trees it indexes.");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!("  The TREE is authoritative. Fix the index row — never the tree, to make them agree.");
            ExitCode::from(1)
        }
    }
}
