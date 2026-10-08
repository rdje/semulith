#!/usr/bin/env python3
"""Shard an append-history head when it approaches its byte ceiling.

`CHANGELOG.md` is an `append_history` surface (`doctrine/readme_routes.tsv`): its pressure
control is *shard when the ceiling fires*, never a raised cap. This tool is the sharder the
registry's owner column names. It moves the OLDEST whole entries (`^## ` blocks, newest-first
file) into a new `docs/changelog/shard-NNNN.md`, rewrites the head under its target, and
regenerates `docs/changelog/SHARDS.sha256` — the freeze proof consumed by
`scripts/check_changelog_shards.sh` (`SHARD-FREEZE`).

TWO HEADS, ONE PARTITION FAMILY (DOC-SHARDING.2). `docs/changelog/` carries the shards of
every append-history head, today `CHANGELOG.md` and `DEV_NOTES.md` (the registry row says so).
The shard header names the head it was cut from and that head's registry ceiling — a shard's
provenance is its first line, not folklore.

WHY WHOLE ENTRIES, BYTE-VERBATIM. A sharded history is only trustworthy if the partition is
provably lossless, so a file is treated as preamble + concatenated entry blocks, and every
moved block keeps its exact bytes (a block includes the blank-line separation after it, so
reassembly is identity). At the shard event the tool asserts, and prints, the ordered entry-id
proof: head-before == head-after + shard, exactly, in both bytes and order. The durable half of
the guarantee — nothing changes after the shard — is the manifest plus the freeze check, not
this tool.

DETERMINISM. Same input, same output; a re-run is a no-op (head under target, manifest already
current -> nothing written). `--max-bytes` may target below the registry ceiling to leave room
for an imminent entry; the registry ceiling remains the enforced bound.

Usage:
  scripts/shard_history.py [--root DIR] [--head PATH] [--shard-dir DIR]
                           [--manifest PATH] [--max-bytes N] [--dry-run] [--self-test]
Defaults: the repository root, `CHANGELOG.md`, `docs/changelog/`, its `SHARDS.sha256`, and the
ceiling the routes registry declares for the head.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())

REGISTRY = "doctrine/readme_routes.tsv"
DEFAULT_HEAD = "CHANGELOG.md"
DEFAULT_SHARD_DIR = "docs/changelog"
MANIFEST_NAME = "SHARDS.sha256"
ENTRY = re.compile(r"^## ", re.M)


class ShardRefused(Exception):
    """A refusal with a reason, never a partial shard."""


def split_entries(text: str) -> tuple[str, list[tuple[str, str]]]:
    """A history file as (preamble, entries): preamble is everything before the first `## `,
    each entry is (id, bytes) with the id taken from its heading line. Concatenating preamble +
    entry bytes reproduces the file exactly."""
    marks = list(ENTRY.finditer(text))
    if not marks:
        raise ShardRefused("the head holds no '## ' entries — there is nothing to shard")
    preamble = text[: marks[0].start()]
    entries: list[tuple[str, str]] = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        block = text[m.start():end]
        eid = block.splitlines()[0][3:].strip()
        entries.append((eid, block))
    return preamble, entries


def registry_ceiling(root: Path, head_rel: str) -> int:
    row_re = re.compile(rf"^{re.escape(head_rel)}\t[^\t]*\t[^\t]*\t[^\t]*\t\d+\t\d+\t\d+\t(\d+)\t\d+$")
    reg = root / REGISTRY
    if not reg.is_file():
        raise ShardRefused(f"{REGISTRY} does not exist — the ceiling is owned by the registry, "
                           f"and this tool refuses to invent one")
    for line in reg.read_text().splitlines():
        m = row_re.match(line)
        if m:
            return int(m.group(1))
    raise ShardRefused(f"{REGISTRY} has no row declaring a byte ceiling for {head_rel} — "
                       f"sharding an ungoverned head would move pressure into the dark")


def manifest_rows(shard_dir: Path, root: Path) -> list[str]:
    """One sha256sum-format row per *.md in the shard dir, sorted by path. Paths are
    repo-root-relative so `sha256sum -c docs/changelog/SHARDS.sha256` works from the root."""
    rows = []
    for p in sorted(shard_dir.glob("*.md")):
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        rows.append(f"{digest}  {p.relative_to(root).as_posix()}")
    return rows


def next_shard_name(shard_dir: Path, root: Path) -> str:
    n = 0
    from history_archive import load_archives
    _, archived = load_archives(root)
    for p in list(shard_dir.glob("shard-*.md")) + [Path(name) for name in archived]:
        m = re.fullmatch(r"shard-(\d+)\.md", p.name)
        if m:
            n = max(n, int(m.group(1)))
    return f"shard-{n + 1:04d}.md"


SHARD_HEADER = (
    "# {head} shard — {first} … {last}\n"
    "\n"
    "> Sharded from `{head}.md` under its {kib} KiB ceiling "
    "(`doctrine/readme_routes.tsv`).\n"
    "> Entries in a shard are **never edited after the shard** — git history is canonical.\n"
    "\n"
)


def shard(root: Path, head_rel: str, shard_dir_rel: str, manifest_rel: str,
          max_bytes: int, ceiling_bytes: int, dry_run: bool = False) -> list[str]:
    from history_archive import ArchiveRefused, load_archives
    try:
        load_archives(root)
    except (ArchiveRefused, OSError) as exc:
        raise ShardRefused(f"archive cannot be authenticated: {exc}") from exc
    log: list[str] = []
    head = root / head_rel
    shard_dir = root / shard_dir_rel
    manifest = root / manifest_rel
    if not head.is_file():
        raise ShardRefused(f"{head_rel} does not exist")
    shard_dir.mkdir(parents=True, exist_ok=True)

    text = head.read_text()
    before_bytes = len(text.encode())
    preamble, entries = split_entries(text)
    moved: list[tuple[str, str]] = []
    kept = list(entries)
    while len((preamble + "".join(b for _, b in kept)).encode()) > max_bytes and len(kept) > 1:
        moved.insert(0, kept.pop())
    if not moved:
        if before_bytes > max_bytes:
            raise ShardRefused(
                f"the head is {before_bytes} bytes over the {max_bytes} target but holds a "
                f"single entry — a shard cannot cut into an entry; the head needs a human")
        log.append(f"no shard needed: {head_rel} is {before_bytes} bytes, target {max_bytes}")
    else:
        if len(kept) == 1 and len((preamble + kept[0][1]).encode()) > max_bytes:
            raise ShardRefused(
                f"even the newest single entry leaves the head over {max_bytes} bytes — "
                f"a shard cannot cut into an entry; the head needs a human")
        shard_name = next_shard_name(shard_dir, root)
        body = "".join(b for _, b in moved)
        first_id = moved[0][0].split()[0]
        last_id = moved[-1][0].split()[0]
        head_stem = head_rel[:-3] if head_rel.endswith(".md") else head_rel
        shard_text = SHARD_HEADER.format(head=head_stem,
                                         kib=ceiling_bytes // 1024,
                                         first=first_id, last=last_id) + body
        after_text = preamble + "".join(b for _, b in kept)
        # The completeness proof, at the shard event, in both directions and both axes:
        # order (kept prefix + moved suffix == original sequence) and bytes (reassembly exact).
        if [e for e, _ in entries] != [e for e, _ in kept] + [e for e, _ in moved]:
            raise ShardRefused("internal: the partition does not preserve entry order — "
                               "refusing to write a history it cannot prove")
        if after_text + body != text:
            raise ShardRefused("internal: head-after + shard bytes != head-before — "
                               "refusing to write a history it cannot prove")
        if not dry_run:
            (shard_dir / shard_name).write_text(shard_text)
            head.write_text(after_text)
        log.append(f"sharded {len(moved)} entr(ies) {moved[0][0]!r} … {moved[-1][0]!r} "
                   f"into {shard_dir_rel}/{shard_name}")
        log.append(f"completeness: {len(entries)} entries before == {len(kept)} kept + "
                   f"{len(moved)} moved, order and bytes exact")
        after_bytes = len(after_text.encode())
        log.append(f"head: {before_bytes} -> {after_bytes} bytes (target {max_bytes})")

    rows = manifest_rows(shard_dir, root)
    new_manifest = "".join(r + "\n" for r in rows)
    old_manifest = manifest.read_text() if manifest.is_file() else None
    if old_manifest != new_manifest:
        if not dry_run:
            manifest.write_text(new_manifest)
        log.append(f"manifest: {len(rows)} shard row(s) written to {manifest_rel}")
    else:
        log.append(f"manifest: {manifest_rel} already current ({len(rows)} row(s))")
    return log


def self_test() -> int:
    passed = failed = 0

    def arm(label: str, fn) -> None:
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:  # noqa: BLE001 — an arm must not abort the run
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    def fixture(entries: list[str], preamble: str = "# CHANGELOG.md\n\n") -> str:
        return preamble + "\n".join(f"## {e}\nbody of {e}\n" for e in entries)

    def eq(x, y): assert x == y, f"got {x!r}, want {y!r}"

    with tempfile.TemporaryDirectory(dir=REPO / "target") as td:
        td = Path(td)
        (td / "docs/changelog").mkdir(parents=True)
        # the registry row the default ceiling is read from
        reg = td / "doctrine"; reg.mkdir()
        (reg / "readme_routes.tsv").write_text(
            "# registry\nCHANGELOG.md\tauthor_overflow\tappend_history\towner\t0\t49152\t0\t1024\t0\n")

        def run(root: Path, max_bytes: int, dry: bool = False):
            return shard(root, "CHANGELOG.md", "docs/changelog",
                         "docs/changelog/SHARDS.sha256", max_bytes, 1024, dry_run=dry)

        def mkroot(text: str) -> Path:
            (td / "CHANGELOG.md").write_text(text)
            return td

        base = fixture(["newest", "middle", "oldest"])
        mkroot(base)
        arm("GREEN a head under target is left alone, manifest written",
            lambda: (
                eq(any(l.startswith("no shard needed") for l in run(td, 65536)), True),
                eq((td / "CHANGELOG.md").read_text(), base),
                eq((td / "docs/changelog/SHARDS.sha256").read_text(), "")))
        (td / "docs/changelog/SHARDS.sha256").unlink()

        mkroot(base)
        out = run(td, 50)  # preamble + newest entry is 42 bytes; 50 forces two moves
        arm("GREEN sharding moves oldest entries, head ends under target",
            lambda: (
                eq(len(list((td / "docs/changelog").glob("*.md"))), 1),
                eq(len((td / "CHANGELOG.md").read_text().encode()) <= 50, True),
                eq("newest" in (td / "CHANGELOG.md").read_text(), True),
                eq("middle" in (td / "CHANGELOG.md").read_text(), False),
                eq(any(l.startswith("completeness:") for l in out), True)))
        arm("GREEN the shard holds the moved entries verbatim, in order",
            lambda: (
                eq(len(list((td / "docs/changelog").glob("shard-*.md"))), 1),
                (lambda s: (eq("## middle" in s, True), eq("## oldest" in s, True),
                            eq(s.index("## middle") < s.index("## oldest"), True),
                            eq("## newest" in s, False)))(
                    list((td / "docs/changelog").glob("shard-*.md"))[0].read_text())))
        head_now = (td / "CHANGELOG.md").read_text()
        shard_now = list((td / "docs/changelog").glob("shard-*.md"))[0].read_text()
        arm("GREEN completeness: head-after + shard bytes == head-before, order exact",
            lambda: eq(head_now + shard_now.split("\n\n", 2)[2], base))
        arm("GREEN the manifest covers the shard and hashes to its bytes",
            lambda: (
                eq(len((td / "docs/changelog/SHARDS.sha256").read_text().splitlines()), 1),
                (lambda row: (
                    eq(hashlib.sha256(list((td / "docs/changelog").glob("shard-*.md"))[0]
                                      .read_bytes()).hexdigest(), row.split()[0]),
                    eq(row.split()[1], "docs/changelog/" +
                       list((td / "docs/changelog").glob("shard-*.md"))[0].name)))(
                    (td / "docs/changelog/SHARDS.sha256").read_text().splitlines()[0])))
        arm("GREEN re-running is a no-op",
            lambda: (
                eq(all("no shard needed" in l for l in run(td, 1024)[:1]), True),
                eq((td / "CHANGELOG.md").read_text(), head_now),
                eq(list((td / "docs/changelog").glob("shard-*.md"))[0].read_text(), shard_now),
                eq(len(list((td / "docs/changelog").glob("shard-*.md"))), 1)))
        arm("GREEN numbering continues: a second shard is shard-0002",
            lambda: (
                mkroot(fixture(["n2", "m2", "o2"])),
                eq([l for l in run(td, 50) if l.startswith("sharded")][0]
                   .split("into docs/changelog/")[1], "shard-0002.md"),
                eq(len(list((td / "docs/changelog").glob("shard-*.md"))), 2)))
        mkroot(fixture(["one"]))
        arm("RED   a refusal when a single entry cannot fit the target",
            lambda: (lambda r: eq(isinstance(r, ShardRefused), True))(
                _caught(lambda: run(td, 10))))
        mkroot(fixture(["one"]))
        arm("RED   a one-entry head over target is not 'no shard needed'",
            lambda: eq("single entry" in str(_caught(lambda: run(td, 10))), True))
        (td / "CHANGELOG.md").write_text("# CHANGELOG.md\n\nno entries here\n")
        arm("RED   a head with no entries is refused",
            lambda: eq("no '## ' entries" in str(_caught(lambda: run(td, 1024))), True))

        # DOC-SHARDING.2 — the header names the head it was cut from and that head's own
        # registry ceiling (two heads share docs/changelog/; provenance is the first line).
        (td / "doctrine/readme_routes.tsv").write_text(
            "# registry\n"
            "CHANGELOG.md\tauthor_overflow\tappend_history\towner\t0\t49152\t0\t65536\t0\n"
            "DEV_NOTES.md\tauthor_overflow\tappend_history\towner\t0\t36864\t0\t49152\t0\n")
        # heads are newest-first files, like the real DEV_NOTES.md
        (td / "DEV_NOTES.md").write_text(
            "# DEV_NOTES.md\n\n## _(2026-09-28)_ — new note (X.2)\nbody\n"
            "## _(2026-09-27)_ — old note (X.1)\nbody\n")
        out = shard(td, "DEV_NOTES.md", "docs/changelog",
                    "docs/changelog/SHARDS.sha256", 70, 49152)
        dev_shard = [p for p in sorted((td / "docs/changelog").glob("shard-*.md"))
                     if "# DEV_NOTES shard" in p.read_text()]
        arm("GREEN a DEV_NOTES shard is named and headed as DEV_NOTES, 48 KiB",
            lambda: (
                eq(len(dev_shard), 1),
                (lambda s: (
                    eq(s.startswith("# DEV_NOTES shard — _(2026-09-27)_"), True),
                    eq("`DEV_NOTES.md`" in s, True),
                    eq("under its 48 KiB ceiling" in s, True),
                    eq("when it crossed" in s, False),
                    eq("64 KiB" in s, False)))(
                    dev_shard[0].read_text())))
        arm("GREEN re-sharding CHANGELOG keeps the .1 header shape (64 KiB, named CHANGELOG)",
            lambda: (
                mkroot(fixture(["n3", "o3"])),
                (lambda logs: (
                    eq(any("sharded" in l for l in logs), True),
                    (lambda p: (
                        eq(p.read_text().startswith("# CHANGELOG shard — o3"), True),
                        eq("under its 64 KiB ceiling" in p.read_text(), True),
                        eq("when it crossed" in p.read_text(), False)))(
                        sorted((td / "docs/changelog").glob("shard-*.md"))[-1])))(
                    shard(td, "CHANGELOG.md", "docs/changelog",
                          "docs/changelog/SHARDS.sha256", 50, 65536))))

    print(f"shard_history --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _caught(fn) -> Exception:
    try:
        fn()
    except ShardRefused as exc:
        return exc
    raise AssertionError("expected ShardRefused, got none")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(REPO))
    ap.add_argument("--head", default=DEFAULT_HEAD)
    ap.add_argument("--shard-dir", default=DEFAULT_SHARD_DIR)
    ap.add_argument("--manifest", default=f"{DEFAULT_SHARD_DIR}/{MANIFEST_NAME}")
    ap.add_argument("--max-bytes", type=int, default=None,
                    help="target for the rewritten head (default: the registry ceiling)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return self_test()
    root = Path(args.root)
    try:
        ceiling = registry_ceiling(root, args.head)
        target = args.max_bytes if args.max_bytes is not None else ceiling
        for line in shard(root, args.head, args.shard_dir, args.manifest, target,
                          ceiling, dry_run=args.dry_run):
            print(line)
    except ShardRefused as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
