#!/usr/bin/env python3
"""Replay LC0025's immutable task-source assessment; this is not a live gate.

Reads only this repository's Git objects and writes JSON to stdout. Requires the
named objects locally; does not fetch, inspect Gitlink contents or render books.
The supported explicit task syntax is finite, not general Markdown semantics.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

import collect_containment_graph as C
import qualify_containment_inventory_inputs as Q

SOURCE = "5bdaa1443601f806e2070f49ce7cee27cc18bbfc"
TREE_SHA256 = "603ef1a2163e6e8d7aef3b38fb6b3ceac307e6c41fe5609379d93196a0ddb955"
STATUSES = {"done", "pending", "proposed", "active", "in_progress", "blocked", "slice-gated"}
STATUS = re.compile(r"^\s*Status:\s*(?:`([a-z_-]+)`|\*\*([a-z_-]+)\*\*)(?:\s|$)")
ARCHIVE = re.compile(
    r"^_Leaves `\.(\d+)`–`\.(\d+)` \(done `[0-9-]+`\)(.*?)_\s*$", re.M | re.S,
)
require = Q.require


def direct_leaves(tree, text):
    """Decode explicitly declared direct IDs and their immediate status fields."""
    lines = text.splitlines()
    identifier = re.compile(r"^- ID:\s*`(" + re.escape(tree) + r"\.\d+)`")
    result = {}
    for i, line in enumerate(lines):
        match = identifier.match(line)
        if not match:
            continue
        leaf = match[1]
        require(leaf not in result, "duplicate leaf " + leaf)
        status = None
        for following in lines[i + 1:i + 8]:
            if following.startswith("- ID:") or following.startswith("## "):
                break
            if following.lstrip().startswith("Status:"):
                token = STATUS.match(following)
                require(token is not None, "unsupported status spelling " + leaf)
                status = token[1] or token[2]
                require(status in STATUSES, "unknown status " + leaf)
                break
        require(status is not None, "missing status " + leaf)
        result[leaf] = {"status": status, "line": i + 1}
    return result


def task_facts(name, text, read_archive):
    """Reconcile a root with its explicit, checked whole-leaf archive declaration."""
    tree = PurePosixPath(name).stem
    metadata = re.search(r"^- Tree ID:\s*`([A-Z0-9-]+)`\s*$", text, re.M)
    require(metadata is not None and metadata[1] == tree, "task identity " + name)
    root_status = re.search(r"^- Status:\s*`([a-z_-]+)`(?:\s|$)", text, re.M)
    require(root_status is not None and root_status[1] in STATUSES, "root status " + name)
    leaves = direct_leaves(tree, text)
    declarations = list(ARCHIVE.finditer(text))
    require(len(declarations) == len(re.findall(r"^_Leaves ", text, re.M)),
            "unsupported archived-leaf declaration " + name)
    archives = []
    for declaration in declarations:
        first, last = int(declaration[1]), int(declaration[2])
        links = re.findall(r"\]\((archive/[^()]+\.md)\)", declaration[3])
        require(len(links) == 1, "archive locator arity " + name)
        relative = Q.relative_path(links[0])
        archive_name = str(PurePosixPath(name).parent / relative)
        archived = direct_leaves(tree, read_archive(archive_name))
        require(0 < first <= last and last - first + 1 <= len(archived),
                "archive range " + name)
        expected = {tree + "." + str(n) for n in range(first, last + 1)}
        require(set(archived) == expected, "archive leaf population " + name)
        require(all(row["status"] == "done" for row in archived.values()),
                "archive completion differs " + name)
        require(not set(leaves) & set(archived), "root/archive leaf overlap " + name)
        for row in archived.values():
            row["source"] = archive_name
        leaves.update(archived)
        archives.append({"path": archive_name, "first": first, "last": last})
    require(bool(leaves), "no declared leaves " + name)
    for row in leaves.values():
        row.setdefault("source", name)
    return {"status": root_status[1], "done": sum(r["status"] == "done" for r in leaves.values()),
            "total": len(leaves), "leaves": leaves, "whole_leaf_archives": archives}


def refusal_controls():
    root = "# T\n- Tree ID: `T`\n- Status: `active`\n- ID: `T.2`\n  Status: **done**\n"
    declaration = "_Leaves `.1`–`.1` (done `2026-10-01`) — live in [archive](archive/T.md)._\n"
    archive = "- ID: `T.1`\n  Status: `done`\n"
    valid = root + declaration
    def read(name):
        require(name == "docs/tasks/archive/T.md", "unexpected archive locator")
        return archive
    def unavailable(_):
        raise Q.Refused("archive unavailable")
    cases = {
        "duplicate direct ID": lambda: task_facts("docs/tasks/T.md", root + root, read),
        "missing leaf status": lambda: task_facts("docs/tasks/T.md", root.replace("  Status: **done**\n", ""), read),
        "unknown leaf status": lambda: task_facts("docs/tasks/T.md", root.replace("**done**", "`invented`"), read),
        "unsupported status spelling": lambda: task_facts("docs/tasks/T.md", root.replace("**done**", "done"), read),
        "wrong task identity": lambda: task_facts("docs/tasks/U.md", root, read),
        "missing root status": lambda: task_facts("docs/tasks/T.md", root.replace("- Status: `active`\n", ""), read),
        "unavailable archive": lambda: task_facts("docs/tasks/T.md", valid, unavailable),
        "archive missing member": lambda: task_facts("docs/tasks/T.md", valid, lambda _: ""),
        "archive extra member": lambda: task_facts("docs/tasks/T.md", valid, lambda _: archive + "- ID: `T.3`\n  Status: `done`\n"),
        "archive not done": lambda: task_facts("docs/tasks/T.md", valid, lambda _: archive.replace("`done`", "`pending`")),
        "root archive overlap": lambda: task_facts("docs/tasks/T.md", valid.replace("`T.2`", "`T.1`"), read),
        "escaping archive": lambda: task_facts("docs/tasks/T.md", valid.replace("archive/T.md", "archive/../../T.md"), read),
        "duplicate declaration": lambda: task_facts("docs/tasks/T.md", valid + declaration, read),
        "reversed range": lambda: task_facts("docs/tasks/T.md", valid.replace("`.1`–`.1`", "`.2`–`.1`"), read),
    }
    for label, run in cases.items():
        try:
            run()
        except Q.Refused:
            continue
        raise Q.Refused("control accepted: " + label)
    require(task_facts("docs/tasks/T.md", valid, read)["done"] == 2, "valid archive/bold control")
    conditional = root.replace("**done**", "`slice-gated`")
    require(task_facts("docs/tasks/T.md", conditional, read)["done"] == 0,
            "conditional status is not completed")
    return list(cases)


def qualify():
    raw = Q.git("ls-tree", "-rz", "--full-tree", SOURCE)
    source = Q.tree_rows(raw)
    require(len(source) == 1416 and C.digest(raw) == TREE_SHA256,
            "immutable source population differs")
    requests = b"".join(row[2].encode() + b"\n" for row in source.values() if row[0] != "160000")
    wire = Q.checked_output(subprocess.run(
        ["git", "--no-optional-locks", "-C", str(Q.ROOT), "cat-file", "--batch"],
        input=requests, capture_output=True, check=False,
    ))
    contents = C.blob_contents(source, wire)
    def read(name):
        require(name in contents and source[name][0] in {"100644", "100755"},
                "source member unavailable " + name)
        return contents[name].decode("utf-8")
    roots = [n for n in source if n.startswith("docs/tasks/") and n.count("/") == 2
             and n.endswith(".md") and n != "docs/tasks/TEMPLATE.md"]
    facts = {PurePosixPath(n).stem: task_facts(n, read(n), read) for n in roots}
    require(len(facts) == 33, "immutable task-root population differs")
    dependencies = set(roots)
    for fact in facts.values():
        dependencies.update(a["path"] for a in fact["whole_leaf_archives"])
    pins = {n: {"mode": source[n][0], "oid": source[n][2], "sha256": C.digest(contents[n])}
            for n in sorted(dependencies)}
    return {"source": SOURCE, "tracked_identities": len(source), "source_tree_sha256": C.digest(raw),
            "opaque_gitlinks": [n for n, r in source.items() if r[0] == "160000"],
            "tasks": facts, "source_pins": pins, "scope": "immutable supported source forms; no live gate verdict"}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    controls = refusal_controls()
    result = {"refusal_controls": controls} if args.self_test else qualify()
    result["refusal_controls"] = controls
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError) as exc:
        print("task inputs: cannot qualify: " + str(exc), file=sys.stderr)
        sys.exit(2)
