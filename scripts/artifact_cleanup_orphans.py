#!/usr/bin/env python3
"""Remove orphan incremental sessions: the recorded class of `decision_orphan-incremental-sessions.md`, under ruling 4 of 2026-10-28 (class C, record-anchored).

A crate-hash directory D, directly under a cargo `incremental` directory in `target/`, is an orphan when:
  1. it has cargo's shape: every entry is a session directory `s-*` or its `s-*.lock`;
  2. nothing in it, directories included, changed since the last recorded cleanup act (`docs/ARTIFACT_CLEANUP.md`);
  3. everything in it is a regular file or a directory, on the repository's device, and none of it is tracked.
The whole of D goes: the sessions' `.bin`, `.o` and `.rmeta` files, their locks, and the emptied directories. Rule 2 is the class's safety: a configuration the gates still build keeps its
caches between daily acts, and one that rustc will never collect goes. Removing a live one only costs a rebuild, and rustc starts fresh silently on a missing dep-graph.

This is its own act, before the strict plan, because the strict tools record cache-named files only and every past act's journal authenticates that shape.

  --plan --workdir target/artifact-cleanup/NEW    the census, written exclusively as orphans.json; removes nothing
  --delete --workdir target/artifact-cleanup/NEW  a fresh green host census, then each planned directory re-decided immediately before it goes; a directory that moved since the plan is kept and named
  --inspect --workdir target/artifact-cleanup/NEW the plan and the journal

Exit: 0 complete or nothing to do; 1 a refused act or a failed removal; the receipt is one JSON line. Redirect it, and never pipe through `tee` into the work directory: a process holding a repository file makes the host census refuse.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import datetime as dt
import json
import os
from pathlib import Path
import re
import stat
import sys

import artifact_cleanup as A
import artifact_cleanup_operator as Op

ROOT = Path(__file__).resolve().parent.parent
RECORD = "docs/ARTIFACT_CLEANUP.md"
PLAN, JOURNAL = "orphans.json", "orphans.jsonl"
OWNED_FIXTURES = ("target/artifact-cleanup",)  # the cleanup tools' own retained fixtures are never a cargo root
CRATE = re.compile(r"[A-Za-z0-9_]+-[a-z0-9]+")
SESSION = re.compile(r"s-[A-Za-z0-9_-]+(\.lock)?")


class Refused(Exception):
    """The act cannot be judged: nothing was removed by this refusal."""


@dataclass(frozen=True)
class Orphan:
    path: str
    files: int
    bytes: int
    newest_ns: int
    identity: str  # every member's (relative path, inode, size, mtime), so a later touch is visible


def anchor_ns(root: Path) -> int:
    """The last recorded act's time, in nanoseconds: the class's one clock, and it is on record rather than a threshold."""
    try:
        text = (root / RECORD).read_text(encoding="utf-8")
    except OSError as error:
        raise Refused(f"{RECORD} is unreadable: {type(error).__name__}") from None
    found = re.search(r"- `(\d{4}-\d\d-\d\dT\d\d:\d\d)Z`", text)
    if found is None:
        raise Refused(f"{RECORD} names no last act")
    moment = dt.datetime.strptime(found.group(1), "%Y-%m-%dT%H:%M").replace(tzinfo=dt.timezone.utc)
    return int(moment.timestamp()) * 1_000_000_000


def incremental_roots(root: Path) -> list[Path]:
    """Every cargo `incremental` directory under `target/`, no symlink followed, nothing beneath one descended into."""
    found = []
    for current, directories, _ in os.walk(root / "target", followlinks=False):
        here = Path(current)
        if here.relative_to(root).as_posix().startswith(OWNED_FIXTURES):
            directories[:] = []
        elif here.name == "incremental":
            found.append(here)
            directories[:] = []
    return sorted(found)


def judge(root: Path, crate: Path, anchor: int, tracked: frozenset[str]) -> Orphan | None:
    """The class's definition: an Orphan, or None for anything it does not cover."""
    device = os.lstat(root / "target").st_dev
    entries = sorted(os.listdir(crate))
    if not CRATE.fullmatch(crate.name) or not entries or not all(SESSION.fullmatch(name) for name in entries):
        return None
    members, files, size, newest = [], 0, 0, os.lstat(crate).st_mtime_ns
    for current, directories, names in os.walk(crate, followlinks=False):
        for name in directories + names:
            path = Path(current) / name
            info = os.lstat(path)
            if info.st_dev != device or not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)):
                return None
            relative = path.relative_to(root).as_posix()
            if relative in tracked:
                return None
            newest = max(newest, info.st_mtime_ns)
            members.append(f"{relative}:{info.st_ino}:{info.st_size}:{info.st_mtime_ns}")
            if stat.S_ISREG(info.st_mode):
                files, size = files + 1, size + info.st_size
    if newest >= anchor:
        return None
    return Orphan(crate.relative_to(root).as_posix(), files, size, newest, "\n".join(sorted(members)))


def census(root: Path, anchor: int, tracked: frozenset[str]) -> list[Orphan]:
    found = []
    for directory in incremental_roots(root):
        for name in sorted(os.listdir(directory)):
            path = directory / name
            if path.is_dir() and not path.is_symlink():
                orphan = judge(root, path, anchor, tracked)
                if orphan is not None:
                    found.append(orphan)
    return found


def work_directory(root: Path, workdir: str) -> Path:
    path = (root / workdir)
    if not workdir.startswith("target/artifact-cleanup/") or ".." in Path(workdir).parts:
        raise Refused("the work directory must be under target/artifact-cleanup/")
    return path


def plan(root: Path, workdir: str, tracked: frozenset[str]) -> dict:
    directory = work_directory(root, workdir)
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    anchor = anchor_ns(root)
    orphans = census(root, anchor, tracked)
    document = dict(format="artifact-orphans-v1", anchor_ns=anchor, orphans=[asdict(item) for item in orphans])
    with open(directory / PLAN, "x", encoding="utf-8") as stream:  # exclusive: a plan is never reused
        json.dump(document, stream, indent=0, sort_keys=True)
    return dict(disposition="planned", orphans=len(orphans), files=sum(o.files for o in orphans), bytes=sum(o.bytes for o in orphans),
                reason="exclusive plan published; nothing removed")


def remove_tree(crate: Path) -> None:
    """Exactly this directory, bottom up; `rmdir` refuses anything that appeared in it."""
    for current, directories, names in os.walk(crate, topdown=False, followlinks=False):
        for name in names:
            os.unlink(Path(current) / name)
        for name in directories:
            os.rmdir(Path(current) / name)
    os.rmdir(crate)


def delete(root: Path, workdir: str, tracked: frozenset[str], host_census=Op.census) -> dict:
    directory = work_directory(root, workdir)
    try:
        document = json.loads((directory / PLAN).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise Refused(f"no readable plan: {type(error).__name__}") from None
    if (directory / JOURNAL).exists():
        raise Refused("this work directory already ran; plan into a new one")
    verdict = host_census(root)
    removed, kept, removed_bytes, failure = [], [], 0, None
    with open(directory / JOURNAL, "x", encoding="utf-8") as journal:
        for row in document["orphans"]:
            crate = root / row["path"]
            current = judge(root, crate, document["anchor_ns"], tracked) if crate.is_dir() else None
            if current is None or current.identity != row["identity"]:
                kept.append(row["path"])
                journal.write(json.dumps(dict(kind="kept", path=row["path"])) + "\n")
                continue
            journal.write(json.dumps(dict(kind="intent", path=row["path"])) + "\n")
            journal.flush()
            try:
                remove_tree(crate)
            except OSError as error:
                failure = dict(path=row["path"], error=type(error).__name__, detail=str(error)[:200])
                journal.write(json.dumps(dict(kind="failed", **failure)) + "\n")
                break
            journal.write(json.dumps(dict(kind="removed", path=row["path"], files=row["files"], bytes=row["bytes"])) + "\n")
            removed.append(row["path"])
            removed_bytes += row["bytes"]
    residue = sum(1 for path in removed if (root / path).exists())
    return dict(disposition="failed" if failure or residue else "complete", census=verdict.verdict, planned=len(document["orphans"]), removed=len(removed),
                removed_bytes=removed_bytes, kept=kept, residue=residue, failure=failure)


def inspect(root: Path, workdir: str) -> dict:
    directory = work_directory(root, workdir)
    document = json.loads((directory / PLAN).read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in (directory / JOURNAL).read_text(encoding="utf-8").splitlines()] if (directory / JOURNAL).exists() else []
    return dict(disposition="inspected", planned=len(document["orphans"]), planned_bytes=sum(o["bytes"] for o in document["orphans"]),
                removed=sum(r["kind"] == "removed" for r in rows), kept=sum(r["kind"] == "kept" for r in rows), failed=sum(r["kind"] == "failed" for r in rows))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--plan", action="store_true")
    action.add_argument("--delete", action="store_true")
    action.add_argument("--inspect", action="store_true")
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args(argv)
    try:
        if args.inspect:
            report = inspect(ROOT, args.workdir)
        else:
            tracked = frozenset(A.tracked_paths(ROOT))
            report = plan(ROOT, args.workdir, tracked) if args.plan else delete(ROOT, args.workdir, tracked)
    except (Refused, A.CleanupError, OSError, ValueError) as error:
        print(json.dumps(dict(disposition="refused", reason=str(error)[:400])))
        return 1
    print(json.dumps(report, sort_keys=True))
    return 0 if report["disposition"] in ("planned", "complete", "inspected") else 1


if __name__ == "__main__":
    sys.exit(main())
