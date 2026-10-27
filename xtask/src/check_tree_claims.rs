//! The `TREE-CLAIMS` doctrine's driver, ported from `scripts/check_tree_claims.sh` (`XTASK.6` slice `6aa`), which is
//! now a shim of `cargo xtask check-tree-claims`.
//!
//! A live document (the routes registry's `hot_live` rows) may state a tree fact — an active tree's leaf count, a
//! frontier pointer, a leading progress ratio — only if the tree it names says the same: the TREE is authoritative, and
//! a number is re-derived, never edited to match a summary. The judge is the driver's inline Python, reading every tree
//! through the shared `task_source` reader (archived ranges included, their declarations qualified); it runs verbatim
//! through `python3 -`, as the script ran it, and is not ported. The controls write the script's synthetic registry,
//! live document and trees (its `tree` heredoc and `archive_fixture` verbatim, its `source_edit` as the same single
//! replacement). Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::scratch;

/// The judge, verbatim: `python3 - <root> <routes> <tasks> <scripts dir>`.
const JUDGE: &str = r###"import re, sys, pathlib
sys.path.insert(0, sys.argv[4])
try:
    from task_source import TaskSourceError, read_task
except ImportError as error:
    print("UNAVAILABLE TASK READER " + str(error)); print("__CHECKED__ 0"); sys.exit(2)


def task_source(path):
    try:
        return read_task(path)
    except TaskSourceError as error:
        print("UNAVAILABLE TASK SOURCE " + str(error)); print("__CHECKED__ 0"); sys.exit(2)

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
    facts = task_source(path)
    status, leaves, lines = facts.status, facts.leaves, facts.text.splitlines()
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

TREEREF  = re.compile(r"\[[^\]\n]+\]\((?:docs/)?tasks/(?P<id2>[A-Za-z0-9._-]+)\.md\)|`(?P<id>[A-Z][A-Za-z0-9-]*)`")
LEADING_RATIO = re.compile(r"^[ \t]*(?:[—–-][ \t]*)?\(?(?P<a>\d+)\s*/\s*(?P<b>\d+)(?=$|[\s;,):—–|])")
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
        for reference in TREEREF.finditer(line):
            tree = reference.group("id") or reference.group("id2")
            ratio = LEADING_RATIO.match(line[reference.end():])
            if tree not in trees or ratio is None:
                continue
            _, leaves, _ = trees[tree]
            real = (sum(status == "done" for status in leaves.values()), len(leaves))
            if (int(ratio["a"]), int(ratio["b"])) != real:
                findings.append(
                    f"COUNT DRIFT {rel}: '{ratio.group(0).strip()}' for {tree}; "
                    f"the tree has {real[0]} of {real[1]}")
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
"###;

/// The script's `tree` heredoc: `<id> <status> <leaf1> <leaf2> <frontier leaf n>`.
fn tree_text(id: &str, status: &str, leaf1: &str, leaf2: &str, n: &str) -> String {
    format!(
        "# {id}\n\n## Metadata\n\n- Status: `{status}`\n\n## Task Tree\n\n- ID: `{id}.1`\n  Status: `{leaf1}`\n\n- ID: `{id}.2`\n  Status: `{leaf2}`\n\n## Current Frontier\n\n| Order | Leaf | Status | Why next |\n| --- | --- | --- | --- |\n| 1 | `{id}.{n}` | `pending` | because |\n"
    )
}

/// The script's `archive_fixture` root, verbatim.
const ARCHIVED_ROOT: &str = "# ALPHA\n- Tree ID: `ALPHA`\n- Status: `active`\n_Leaves `.1`–`.1` (done `2026-10-01`) — live in [archive](archive/ALPHA.md)._\n- ID: `ALPHA.2`\n  Status: `pending`\n## Current Frontier\n| Order | Leaf | Status | Why next |\n| --- | --- | --- | --- |\n| 1 | `ALPHA.2` | `pending` | next |\n";

/// `check_claims <root> <routes> <tasks>`: the judge on stdin, the scripts directory as its reader's path; with `both`,
/// stdout and stderr together as `2>&1` joined them, else stdout alone with stderr passing through.
fn check_claims(repo: &Path, root: &str, routes: &str, tasks: &str, both: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .arg(root)
        .arg(routes)
        .arg(tasks)
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

struct Tally<'a> {
    repo: &'a Path,
    root: &'a Path,
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally<'_> {
    /// One arm: judging the fixture tree (`r.tsv`, `tasks`) must give `expected` and contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let (rc, out) = check_claims(
            self.repo,
            &self.root.display().to_string(),
            "r.tsv",
            "tasks",
            true,
        );
        let out = captured(&out);
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "TREE-CLAIMS self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}"
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("TREE-CLAIMS self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }

    /// The script's `source_edit`: exactly one occurrence replaced in the ALPHA tree, or the fixture seam is a failure.
    fn source_edit(&mut self, from: &str, to: &str) {
        let path = self.root.join("tasks/ALPHA.md");
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

/// The RED/GREEN controls over the script's synthetic registry, live document and trees.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "treeclaims") else {
        eprintln!("TREE-CLAIMS self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let _ = fs::create_dir_all(t.join("tasks"));
    let tree = |id: &str, status: &str, l1: &str, l2: &str, n: &str| {
        write(
            &t.join(format!("tasks/{id}.md")),
            &tree_text(id, status, l1, l2, n),
        )
    };
    let doc = |text: &str| write(&t.join("L.md"), &format!("{text}\n"));
    let routes = || {
        write(
            &t.join("r.tsv"),
            "#c1\tc2\tc3\nL.md\tboth\thot_live\towner\t0\t0\t0\t0\t0\n",
        )
    };
    let archive_fixture = || {
        let _ = fs::create_dir_all(t.join("tasks/archive"));
        write(&t.join("tasks/ALPHA.md"), ARCHIVED_ROOT);
        write(
            &t.join("tasks/archive/ALPHA.md"),
            "- ID: `ALPHA.1`\n  Status: `done`\n",
        );
    };
    let mut tally = Tally {
        repo,
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
    };
    routes();
    tree("ALPHA", "active", "done", "pending", "2");
    doc("- **Active trees:** `ALPHA` (1 of 2 leaves).\n- **Frontier leaf:** `ALPHA.2` — second.");
    tally.arm("GREEN every claim re-derived", 0, "__CHECKED__ 1");
    doc("- **Active trees:** `ALPHA` (1 of 3 leaves).\n- **Frontier leaf:** `ALPHA.2` — second.");
    tally.arm("RED   the A-of-B count drifts", 1, "COUNT DRIFT");
    doc("- **Active trees:** `ALPHA` (0 of 2 leaves).\n- **Frontier leaf:** `ALPHA.2` — second.");
    tally.arm("RED   done count drifts with total fixed", 1, "COUNT DRIFT");
    doc("- **Active trees:** `ALPHA` — 7 leaves.\n- **Frontier leaf:** `ALPHA.2` — second.");
    tally.arm("RED   the bare total drifts", 1, "COUNT DRIFT");
    doc("- **Active trees:** `ALPHA` (1 of 2 leaves).\n- **Frontier leaf:** `ALPHA.1` — first.");
    tally.arm("RED   the pointer names a done leaf", 1, "DONE FRONTIER");
    tree("ALPHA", "active", "pending", "pending", "1");
    doc("- **Active trees:** `ALPHA` (0 of 2 leaves).\n- **Frontier leaf:** `ALPHA.2` — second.");
    tally.arm(
        "RED   the pointer names the wrong leaf",
        1,
        "FRONTIER DRIFT",
    );
    doc("- **Active trees:** `ALPHA` (0 of 2 leaves).\n- **Frontier leaf:** `BETA.1` — nonexistent.");
    tally.arm("RED   the pointer names no tree", 1, "UNKNOWN TREE");
    tree("ALPHA", "proposed", "pending", "pending", "1");
    doc("- **Active trees:** `ALPHA` (0 of 2 leaves).\n- **Frontier leaf:** `ALPHA.1` — first.");
    tally.arm("RED   a named tree is not active", 1, "NOT ACTIVE");
    tree("ALPHA", "active", "pending", "pending", "1");
    tree("BETA", "active", "pending", "pending", "1");
    doc("- **Active trees:** `ALPHA` (0 of 2 leaves).\n- **Frontier leaf:** `ALPHA.1` — first.");
    tally.arm("RED   an active tree is unnamed", 1, "MISSING ACTIVE");
    let _ = fs::remove_file(t.join("tasks/BETA.md"));
    doc("- **Active trees:** `ALPHA` (0 of 2 leaves).\n- **Frontier leaf:** `ALPHA.1` — first.");
    let _ = fs::remove_file(t.join("L.md"));
    tally.arm("RED   a live doc does not exist", 1, "NO LIVE DOC");
    doc("- **Active trees:** `ALPHA` (0 of 2 leaves).\n- **Frontier leaf:** `ALPHA.1` — first.");
    write(
        &t.join("r.tsv"),
        "#c1\tc2\tc3\nCHANGELOG.md\tboth\tappend_history\towner\t0\t0\t0\t0\t0\n",
    );
    tally.arm("REFUSE history is not a live doc", 2, "NO LIVE DOCS");
    routes();
    let _ = fs::remove_file(t.join("tasks/ALPHA.md"));
    tally.arm("REFUSE no trees to check against", 2, "NO TREES");
    tree("ALPHA", "active", "pending", "pending", "1");
    let _ = fs::remove_file(t.join("r.tsv"));
    tally.arm("REFUSE the routes registry is gone", 2, "NO ROUTES");
    // Shared-source qualification. The original controls above remain verbatim.
    let reset = |tally: &mut Tally| {
        let _ = tally;
        routes();
        tree("ALPHA", "active", "done", "pending", "2");
        doc("`ALPHA` 1 of 2 leaves");
    };
    reset(&mut tally);
    tally.source_edit("Status: `done`", "Status: **done**");
    tally.arm("GREEN bold source status", 0, "__CHECKED__");
    reset(&mut tally);
    tally.source_edit("Status: `done`", "Status: `slice-gated`");
    doc("`ALPHA` 0 of 2 leaves");
    tally.arm(
        "GREEN conditional source is not completed",
        0,
        "__CHECKED__",
    );
    reset(&mut tally);
    tally.source_edit("Status: `done`", "Status: `invented`");
    tally.arm("REFUSE unknown source status", 2, "UNAVAILABLE TASK SOURCE");
    reset(&mut tally);
    tally.source_edit("Status: `done`", "Missing: `done`");
    tally.arm("REFUSE missing source status", 2, "UNAVAILABLE TASK SOURCE");
    reset(&mut tally);
    append(
        &t.join("tasks/ALPHA.md"),
        "- ID: `ALPHA.1`\n  Status: `done`\n",
    );
    tally.arm("REFUSE duplicate source ID", 2, "UNAVAILABLE TASK SOURCE");
    reset(&mut tally);
    tally.source_edit("Status: `done`", "Status: `done`\n  Status: `pending`");
    tally.arm("REFUSE duplicate leaf status", 2, "UNAVAILABLE TASK SOURCE");
    reset(&mut tally);
    append(&t.join("tasks/ALPHA.md"), "- Status: `active`\n");
    tally.arm("REFUSE duplicate root status", 2, "UNAVAILABLE TASK SOURCE");
    reset(&mut tally);
    let _ = fs::write(t.join("tasks/ALPHA.md"), [0xFFu8]);
    tally.arm(
        "REFUSE invalid UTF8 task source",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset(&mut tally);
    archive_fixture();
    tally.arm("GREEN checked whole archived range", 0, "__CHECKED__");
    reset(&mut tally);
    archive_fixture();
    let _ = fs::remove_file(t.join("tasks/archive/ALPHA.md"));
    tally.arm("REFUSE missing archive", 2, "UNAVAILABLE TASK SOURCE");
    reset(&mut tally);
    archive_fixture();
    write(
        &t.join("tasks/archive/ALPHA.md"),
        "- ID: `ALPHA.1`\n  Status: `pending`\n",
    );
    tally.arm(
        "REFUSE archive is not completed",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset(&mut tally);
    archive_fixture();
    write(
        &t.join("tasks/archive/ALPHA.md"),
        "- ID: `ALPHA.3`\n  Status: `done`\n",
    );
    tally.arm(
        "REFUSE archive has wrong population",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset(&mut tally);
    archive_fixture();
    append(
        &t.join("tasks/ALPHA.md"),
        "- ID: `ALPHA.1`\n  Status: `done`\n",
    );
    tally.arm("REFUSE root archive overlap", 2, "UNAVAILABLE TASK SOURCE");
    reset(&mut tally);
    archive_fixture();
    append(
        &t.join("tasks/ALPHA.md"),
        "_Leaves `.1`–`.1` (done `2026-10-01`) — live in [archive](archive/ALPHA.md)._\n",
    );
    tally.arm(
        "REFUSE repeated archive declaration",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset(&mut tally);
    archive_fixture();
    tally.source_edit("archive/ALPHA.md", "archive/../ALPHA.md");
    tally.arm(
        "REFUSE unsafe archive locator",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset(&mut tally);
    archive_fixture();
    tally.source_edit("_Leaves", "_Leaves unsupported");
    tally.arm(
        "REFUSE unsupported archive declaration",
        2,
        "UNAVAILABLE TASK SOURCE",
    );
    reset(&mut tally);
    doc("`ALPHA` 1/2");
    tally.arm("GREEN leading progress ratio", 0, "__CHECKED__");
    reset(&mut tally);
    doc("`ALPHA` 0/2");
    tally.arm("RED leading completed ratio drifts", 1, "COUNT DRIFT");
    reset(&mut tally);
    doc("`ALPHA` — (1/3)");
    tally.arm("RED leading total ratio drifts", 1, "COUNT DRIFT");
    reset(&mut tally);
    doc("`ALPHA` 1/2; instructions52/52");
    tally.arm("GREEN later instruction ratio excluded", 0, "__CHECKED__");
    reset(&mut tally);
    doc("`ALPHA` instructions52/52");
    tally.arm("GREEN labeled instruction ratio excluded", 0, "__CHECKED__");
    reset(&mut tally);
    doc("[`ALPHA`](tasks/ALPHA.md) 0/2");
    tally.arm("RED Markdown tree link ratio drifts", 1, "COUNT DRIFT");
    reset(&mut tally);
    tree("BETA", "proposed", "pending", "pending", "1");
    doc("`ALPHA` 1/2; `BETA` 0/2");
    tally.arm(
        "GREEN each leading ratio binds to its own tree",
        0,
        "__CHECKED__",
    );
    doc("`ALPHA` 1/2; `BETA` 1/2");
    tally.arm("RED second tree leading ratio drifts", 1, "COUNT DRIFT");
    let _ = fs::remove_file(t.join("tasks/BETA.md"));
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
            "TREE-CLAIMS --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-tree-claims [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !root.join("doctrine/readme_routes.tsv").is_file() {
        println!("TREE-CLAIMS: ok (no routes registry yet)");
        return ExitCode::SUCCESS;
    }
    if !self_test(root, false) {
        eprintln!("TREE-CLAIMS: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let (rc, out) = check_claims(root, ".", "doctrine/readme_routes.tsv", "docs/tasks", false);
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
            eprintln!("TREE-CLAIMS: REFUSED — the live-document scope could not be established.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!(
                "TREE-CLAIMS: ok ({count} live document(s) state nothing the trees contradict)"
            );
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("TREE-CLAIMS: a live document states a tree fact that the tree contradicts.");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!("  The TREE is authoritative. Re-derive the number — never edit a tree to match a summary.");
            ExitCode::from(1)
        }
    }
}
