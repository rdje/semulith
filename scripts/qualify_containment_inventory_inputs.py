#!/usr/bin/env python3
"""Replay LC-0022's immutable input boundary; not a live containment verdict.

Run from any directory. Reads only Git objects in this repository; no external
policy checkout, submodule implementation, cache or generated output is read.
Exit 0 qualifies these inputs; exit 2 means they cannot be qualified.
"""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "36155475680a564236d93462e7513490872f1d34"
TREE_SHA256 = "5b3b6169261648d9c09901879cc7a895606a59f2d8c5947cbf2ff7a25133190b"
REGISTRY_SHA256 = "b4404eab92bc5b1050ff695dc357d6a37a77cb80474014483f7893c35039037f"


class Refused(ValueError):
    """A required input is unavailable, ambiguous or outside its contract."""


def require(condition, reason):
    if not condition:
        raise Refused(reason)


def checked_output(result):
    require(result.returncode == 0 and not result.stderr, "Git read unavailable")
    return result.stdout


def git(*args):
    return checked_output(subprocess.run(
        ["git", "--no-optional-locks", "-C", str(ROOT), *args],
        capture_output=True, check=False,
    ))


def relative_path(name):
    path = PurePosixPath(name)
    require(bool(path.parts) and not path.is_absolute() and ".." not in path.parts
            and str(path) == name and not any(ord(c) < 32 or ord(c) == 127 for c in name),
            "unsafe or non-normalized path")
    return name


def tree_rows(raw):
    require(raw.endswith(b"\0"), "incomplete NUL inventory")
    rows = {}
    for record in raw[:-1].split(b"\0"):
        fields = record.split(b"\t")
        require(len(fields) == 2, "ambiguous inventory record")
        metadata, name = fields
        name = relative_path(name.decode("utf-8"))
        parts = metadata.decode("ascii").split(" ")
        require(len(parts) == 3, "malformed inventory metadata")
        mode, kind, oid = parts
        require((mode, kind) in {("100644", "blob"), ("100755", "blob"),
                                ("160000", "commit")}, "unsupported inventory member")
        require(re.fullmatch(r"[0-9a-f]{40}", oid) is not None, "invalid object identity")
        require(name not in rows, "duplicate inventory path")
        rows[name] = (mode, kind, oid)
    return rows


def registry_rows(raw, source):
    text = raw.decode("utf-8")
    require(not any(ord(c) < 32 and c not in "\t\n\r" or ord(c) == 127 for c in text),
            "registry control character")
    text = text.replace("\r\n", "\n")
    require("\r" not in text, "registry bare carriage return")
    rows = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        require(len(fields) == 9, "registry arity")
        destination, route, lifecycle, owner, *limits = fields
        relative_path(destination[:-1] if destination.endswith("/") else destination)
        require(destination not in rows, "duplicate registry destination")
        require(route in {"reader_navigation", "author_overflow", "both"}, "route class")
        require(lifecycle in {"hot_live", "partitioned", "generated_index", "append_history",
                              "frozen", "normative", "archive_terminal"}, "local lifecycle")
        require(bool(owner.strip()), "missing registry owner")
        require(all(re.fullmatch(r"[0-9]+", n) and int(n) <= 9223372036854775807
                    for n in limits), "registry numeric limit")
        if destination.endswith("/"):
            present = any(name.startswith(destination) for name in source)
        else:
            present = destination in source
        require(present, "registry destination outside source")
        rows[destination] = fields
    return rows


def refusal_controls():
    record = b"100644 blob " + b"0" * 40 + b"\tREADME.md\0"
    source = {"README.md": ("100644", "blob", "0" * 40)}
    row = b"README.md\tboth\thot_live\towner\t1\t1\t2\t2\t0\n"
    cases = {
        "truncated inventory": lambda: tree_rows(record[:-1]),
        "duplicate inventory": lambda: tree_rows(record + record),
        "escaping inventory": lambda: tree_rows(record.replace(b"README.md", b"../README.md")),
        "symlink inventory": lambda: tree_rows(record.replace(b"100644", b"120000")),
        "failed Git status": lambda: checked_output(subprocess.CompletedProcess([], 73, record, b"")),
        "Git diagnostic": lambda: checked_output(subprocess.CompletedProcess([], 0, record, b"partial read")),
        "registry partial row": lambda: registry_rows(row.replace(b"\t0\n", b"\n"), source),
        "registry duplicate": lambda: registry_rows(row + row, source),
        "registry negative limit": lambda: registry_rows(row.replace(b"\t2\t2", b"\t-1\t2"), source),
        "registry unknown lifecycle": lambda: registry_rows(row.replace(b"hot_live", b"guess"), source),
        "registry missing target": lambda: registry_rows(row.replace(b"README.md", b"MISSING.md"), source),
        "registry NUL": lambda: registry_rows(row + b"\0", source),
    }
    for name, run in cases.items():
        try:
            run()
        except Refused:
            continue
        raise Refused("control accepted: " + name)
    require(len(tree_rows(record)) == 1 and len(registry_rows(row, source)) == 1,
            "valid control refused")
    return list(cases)


def main():
    controls = refusal_controls()
    raw = git("ls-tree", "-rz", "--full-tree", SOURCE)
    source = tree_rows(raw)
    require(len(source) == 1408 and hashlib.sha256(raw).hexdigest() == TREE_SHA256,
            "immutable source boundary differs")
    raw = git("show", SOURCE + ":doctrine/readme_routes.tsv")
    require(hashlib.sha256(raw).hexdigest() == REGISTRY_SHA256, "source registry differs")
    rows = registry_rows(raw, source)
    require(len(rows) == 39, "source route boundary differs")
    print(json.dumps({
        "source": SOURCE, "tracked_identities": len(source), "destinations": len(rows),
        "opaque_gitlinks": [n for n, r in source.items() if r[0] == "160000"],
        "source_tree_sha256": TREE_SHA256, "registry_sha256": REGISTRY_SHA256,
        "refusal_controls": controls, "semantic_graph_coverage": "pending LC.4i2",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError) as exc:
        print("inventory inputs: cannot qualify: " + str(exc), file=sys.stderr)
        sys.exit(2)
