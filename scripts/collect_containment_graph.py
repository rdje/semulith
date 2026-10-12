#!/usr/bin/env python3
"""Collect LC.4i2a evidence; complete semantic graph coverage remains pending.

Reads immutable source objects and working inputs, builds registered books via
mdbook's public CLI into a fresh target directory, and retains a checked census.
No tracked input is written. Run --self-test for finite refusal controls.
"""

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from urllib.parse import urlsplit

import qualify_containment_inventory_inputs as Q
import unit_books as U


ROOT = Path(__file__).resolve().parent.parent
require = Q.require


def digest(body):
    return hashlib.sha256(body).hexdigest()


def blob_contents(rows, wire):
    """Consume exactly one checked Git batch response per regular source member."""
    contents = {}
    position = 0
    for name, (mode, kind, oid) in rows.items():
        if mode == "160000":
            continue
        end = wire.find(b"\n", position)
        require(end >= 0, "incomplete blob header")
        fields = wire[position:end].split(b" ")
        require(len(fields) == 3 and fields[:2] == [oid.encode(), b"blob"]
                and re.fullmatch(rb"[0-9]+", fields[2]), "invalid blob header")
        size = int(fields[2])
        position = end + 1
        body = wire[position:position + size]
        require(len(body) == size and wire[position + size:position + size + 1] == b"\n",
                "incomplete blob body")
        actual_oid = hashlib.sha1(b"blob " + str(size).encode() + b"\0" + body).hexdigest()
        require(actual_oid == oid, "blob identity differs")
        contents[name] = body
        position += size + 1
    require(position == len(wire), "surplus blob batch bytes")
    require(set(contents) == {n for n, row in rows.items() if row[0] != "160000"},
            "incomplete source member expansion")
    return contents


def include_candidates(name, body):
    """Capture every literal prefix, including examples and incomplete directives.

    This deliberately performs no Markdown parsing or include resolution. Offsets
    address encoded bytes, so UTF-8 cannot shift the recorded source position.
    """
    result = []
    for match in re.finditer(rb"\{\{#include", body):
        start = match.start()
        newline = body.find(b"\n", start)
        limit = len(body) if newline < 0 else newline
        closing = body.find(b"}}", start, limit)
        end = closing + 2 if closing >= 0 else limit
        marker = body[start:end]
        result.append({"source": name, "byte_offset": start,
                       "marker": marker.decode("utf-8"), "closed_on_line": closing >= 0,
                       "marker_sha256": digest(marker), "expansion": "unreviewed"})
    reconcile_includes(body, result)
    return result


def reconcile_includes(body, candidates):
    offsets = [record["byte_offset"] for record in candidates]
    require(len(offsets) == body.count(b"{{#include") and offsets == sorted(set(offsets)),
            "literal include population differs")
    for record in candidates:
        start = record["byte_offset"]
        marker = record["marker"].encode("utf-8")
        require(body[start:start + 10] == b"{{#include"
                and body[start:start + len(marker)] == marker
                and digest(marker) == record["marker_sha256"], "include identity differs")


def reconcile_source(rows, members):
    paths = [record["path"] for record in members]
    require(len(paths) == len(set(paths)) and set(paths) == set(rows),
            "source member population differs")
    for record in members:
        require((record["mode"], record["kind"], record["oid"]) == rows[record["path"]],
                "source member identity differs")


def source_census(revision):
    resolved = Q.git("rev-parse", "--verify", revision + "^{commit}").decode().strip()
    require(re.fullmatch(r"[0-9a-f]{40}", resolved), "invalid source revision")
    raw = Q.git("ls-tree", "-rz", "--full-tree", resolved)
    rows = Q.tree_rows(raw)
    requests = b"".join(row[2].encode() + b"\n" for row in rows.values() if row[0] != "160000")
    wire = Q.checked_output(subprocess.run(
        ["git", "--no-optional-locks", "-C", str(ROOT), "cat-file", "--batch"],
        input=requests, capture_output=True, check=False,
    ))
    contents = blob_contents(rows, wire)
    members, includes = [], []
    for name, (mode, kind, oid) in rows.items():
        record = {"path": name, "mode": mode, "kind": kind, "oid": oid}
        if mode != "160000":
            body = contents[name]
            record.update(bytes=len(body), lf_lines=body.count(b"\n"), sha256=digest(body))
            if name.endswith(".md"):
                body.decode("utf-8")
                includes.extend(include_candidates(name, body))
        members.append(record)
    reconcile_source(rows, members)
    return {"revision": resolved, "tree_sha256": digest(raw), "members": members,
            "include_candidates": includes}


def file_identity(name):
    Q.relative_path(name)
    path = U.source_path(ROOT, name)
    require(path.is_file() and not path.is_symlink(), "unavailable regular input: " + name)
    before = path.stat()
    body = path.read_bytes()
    after = path.stat()
    stable = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_mode)
    require(stable(before) == stable(after) and len(body) == before.st_size,
            "input changed during read: " + name)
    return {"sha256": digest(body), "mode": stat.S_IMODE(after.st_mode), "bytes": len(body)}


def working_snapshot(additions):
    raw = Q.git("ls-files", "--stage", "-z")
    require(raw.endswith(b"\0"), "incomplete index inventory")
    rows = {}
    for line in raw[:-1].split(b"\0"):
        metadata, name = line.split(b"\t", 1)
        fields = metadata.split(b" ")
        require(len(fields) == 3 and fields[2] == b"0", "ambiguous index entry")
        name = Q.relative_path(name.decode("utf-8"))
        require(name not in rows, "duplicate index entry")
        mode, oid = fields[:2]
        require(re.fullmatch(rb"[0-9a-f]{40}", oid), "invalid index identity")
        if mode == b"160000":
            rows[name] = {"gitlink": oid.decode()}
        else:
            require(mode in {b"100644", b"100755"}, "unsupported index mode")
            rows[name] = file_identity(name)
    require(len(additions) == len(set(additions)), "duplicate declared addition")
    for name in additions:
        require(name not in rows or "gitlink" not in rows[name], "addition is a Gitlink")
        rows[name] = file_identity(name)
    index = Path(Q.git("rev-parse", "--git-path", "index").decode().strip())
    if not index.is_absolute():
        index = ROOT / index
    require(index.stat().st_dev == ROOT.stat().st_dev, "index is on another volume")
    return {"head": Q.git("rev-parse", "HEAD").decode().strip(),
            "index_sha256": digest(index.read_bytes()), "members": rows}


class RenderedLinks(HTMLParser):
    """Independent anchor extraction; resource attributes remain candidates."""

    def __init__(self, body):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.resources = []
        self.feed(body)
        self.close()

    def handle_starttag(self, tag, attrs):
        hrefs = [value for key, value in attrs if key == "href"]
        if tag == "a" and hrefs:
            require(len(hrefs) == 1 and hrefs[0] is not None, "ambiguous rendered hyperlink")
            href = hrefs[0]
            url = urlsplit(href)
            kind = "remote" if url.scheme or url.netloc else "fragment" if not url.path else "local"
            self.links.append({"href": href, "kind": kind, "line": self.getpos()[0]})
        for key, value in attrs:
            if key in {"src", "srcset", "action", "data", "cite"} or key == "href" and tag != "a":
                self.resources.append({"tag": tag, "attribute": key, "value": value,
                                       "line": self.getpos()[0], "route_review": "pending"})


def html_population(outputs):
    """A second traversal reconciles the collector's rglob expansion."""
    found = set()
    for output in outputs:
        for directory, directories, files in os.walk(output, followlinks=False):
            require(not any((Path(directory) / n).is_symlink() for n in directories + files),
                    "symlink in rendered output")
            for name in files:
                if name.endswith(".html"):
                    path = Path(directory) / name
                    require(path.is_file() and path.stat().st_dev == ROOT.stat().st_dev,
                            "unsafe rendered member")
                    require(path not in found, "overlapping output roots")
                    found.add(path)
    return found


def reconcile_rendered(pages, expected, checked):
    require(set(pages) == expected, "rendered output population differs")
    require(sum(len(p["links"]) for p in pages.values()) == checked,
            "rendered hyperlink population differs")


def collect_rendered(web_root, outputs):
    expected = html_population(outputs)
    pages = {}
    for output in outputs:
        for path in sorted(output.rglob("*.html")):
            require(path not in pages and path in expected, "ambiguous rendered output")
            body = path.read_bytes()
            parsed = RenderedLinks(body.decode("utf-8"))
            pages[path] = {"path": path.relative_to(web_root).as_posix(),
                           "sha256": digest(body), "bytes": len(body),
                           "links": parsed.links, "resource_candidates": parsed.resources}
    findings, checked = U.navigation_findings(web_root, outputs)
    require(not findings, "rendered navigation refuses: " + repr(findings))
    reconcile_rendered(pages, expected, checked)
    require(html_population(outputs) == expected, "rendered output changed during verification")
    for path, record in pages.items():
        require(file_identity(path.relative_to(ROOT).as_posix())["sha256"] == record["sha256"],
                "rendered bytes changed during verification")
    return [pages[p] for p in sorted(pages)], checked


def refusal_controls():
    names = Q.refusal_controls()
    body = b"source\n"
    oid = hashlib.sha1(b"blob 7\0" + body).hexdigest()
    rows = {"README.md": ("100644", "blob", oid)}
    wire = oid.encode() + b" blob 7\n" + body + b"\n"
    require(blob_contents(rows, wire) == {"README.md": body}, "valid batch control refused")
    page = RenderedLinks('<a href="https://example.invalid/?a=1&amp;b=2">x</a><a href="#x">y</a>')
    require([p["kind"] for p in page.links] == ["remote", "fragment"]
            and page.links[0]["href"].endswith("a=1&b=2"), "valid HTML control refused")
    resources = RenderedLinks('<link href="a.css"><img src="a.png" srcset="b.png 2x">'
                              '<form action="go"><object data="v"><blockquote cite="s">')
    require([r["attribute"] for r in resources.resources]
            == ["href", "src", "srcset", "action", "data", "cite"],
            "valid resource control refused")
    marker = include_candidates("x.md", "é {{#include x.md}}\n{{#include unfinished".encode())
    require([p["byte_offset"] for p in marker] == [3, 21]
            and [p["closed_on_line"] for p in marker] == [True, False], "UTF-8/include control")
    cases = {
        "missing blob header": lambda: blob_contents(rows, b""),
        "truncated blob body": lambda: blob_contents(rows, wire[:-2]),
        "wrong blob identity": lambda: blob_contents(rows, wire.replace(b"source", b"Source")),
        "surplus blob response": lambda: blob_contents(rows, wire + wire),
        "wrong blob type": lambda: blob_contents(rows, wire.replace(b" blob ", b" tree ")),
        "omitted source member": lambda: reconcile_source(rows, []),
        "omitted literal include": lambda: reconcile_includes(b"{{#include x}}", []),
        "omitted rendered output": lambda: reconcile_rendered({}, {Path("page.html")}, 0),
        "omitted rendered hyperlink": lambda: reconcile_rendered({Path("page.html"): {"links": []}}, {Path("page.html")}, 1),
        "duplicate href attribute": lambda: RenderedLinks('<a href="a" href="b">x</a>'),
    }
    for name, run in cases.items():
        try:
            run()
        except Q.Refused:
            names.append(name)
            continue
        raise Q.Refused("control accepted: " + name)
    return names


def collect(args, controls):
    Q.relative_path(args.output)
    require(args.output.startswith("target/"), "output must be under target/")
    output = U.source_path(ROOT, args.output)
    require(not output.exists(), "output already exists; use a fresh evidence directory")
    source = source_census(args.revision)
    before = working_snapshot(args.addition)
    units = U.registered_units(ROOT)
    require(not U.catalogue_findings(ROOT, units), "unit catalogue refuses")
    books = [ROOT / "docs/book"] + [U.book_path(ROOT, unit["book"]) for unit in units]
    output.mkdir(parents=True, exist_ok=False)
    temporary = output / "tmp"
    temporary.mkdir()
    environment = dict(os.environ, TMPDIR=str(temporary))
    site = output / "site"
    outputs = []
    for number, book in enumerate(books):
        destination = site / book.relative_to(ROOT) / "book"
        result = subprocess.run(["mdbook", "build", str(book), "-d", str(destination)],
                                capture_output=True, env=environment, check=False)
        (output / f"build-{number}.stdout").write_bytes(result.stdout)
        (output / f"build-{number}.stderr").write_bytes(result.stderr)
        require(result.returncode == 0, "book build failed: " + book.relative_to(ROOT).as_posix())
        outputs.append(destination)
    pages, checked = collect_rendered(site / "docs", outputs)
    after = working_snapshot(args.addition)
    require(before == after, "source/index changed across collection")
    prefixes = [book.relative_to(ROOT).as_posix() + "/src/" for book in books]
    markdown = [r["path"] for r in source["members"] if r["path"].endswith(".md")]
    result = {"schema_version": 1, "source": source,
              "working_inputs": before, "working_inputs_after": after,
              "books": [b.relative_to(ROOT).as_posix() for b in books],
              "rendered_pages": pages, "hyperlinks": checked,
              "markdown_outside_book_sources": [n for n in markdown if not any(n.startswith(p) for p in prefixes)],
              "refusal_controls": controls,
              "semantic_graph_coverage": "pending LC.4i2b-d; directory membership is not include coverage"}
    encoded = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    (output / "census.json").write_bytes(encoded)
    print(json.dumps({"source": source["revision"], "members": len(source["members"]),
                      "markdown": len(markdown), "include_candidates": len(source["include_candidates"]),
                      "books": len(books), "rendered_pages": len(pages), "hyperlinks": checked,
                      "refusal_controls": len(result["refusal_controls"]),
                      "census_sha256": digest(encoded), "source_unchanged": True}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--revision")
    parser.add_argument("--output")
    parser.add_argument("--addition", action="append", default=[])
    args = parser.parse_args()
    controls = refusal_controls()
    if args.self_test:
        require(not args.revision and not args.output and not args.addition,
                "self-test does not accept collection arguments")
        print(json.dumps({"refusal_controls": controls}))
    else:
        require(bool(args.revision and args.output), "--revision and --output are required")
        collect(args, controls)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError, U.BookRefused) as exc:
        print("graph census: cannot qualify: " + str(exc), file=sys.stderr)
        sys.exit(2)
