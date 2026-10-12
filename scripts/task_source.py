"""Decode the explicit numeric-leaf syntax shared by the two progress guards.

This is a finite source contract, not a Markdown parser. Only a declared whole
archive range contributes archived leaves; narrative references do not. A
missing, ambiguous or unsupported source cannot establish a progress verdict.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re
import stat
from types import MappingProxyType


STATUSES = frozenset({"done", "pending", "proposed", "active", "in_progress",
                      "blocked", "slice-gated"})
STATUS = re.compile(r"(?:`([a-z_-]+)`|\*\*([a-z_-]+)\*\*)(?:\s|$)")
IDENTIFIER = re.compile(r"^- ID:\s*`([A-Za-z0-9._-]+\.\d+)`")
ARCHIVE = re.compile(
    r"^_Leaves `\.(\d+)`–`\.(\d+)` \(done `[0-9-]+`\)(.*?)_\s*$", re.M | re.S,
)


class TaskSourceError(ValueError):
    """The declared task source cannot support a count or frontier verdict."""


@dataclass(frozen=True)
class TaskFacts:
    status: str
    leaves: Mapping[str, str]
    text: str


def require(condition, reason):
    if not condition:
        raise TaskSourceError(reason)


def read_text(path):
    """A failed read is unavailable evidence, never an empty set of leaves."""
    try:
        require(stat.S_ISREG(path.lstat().st_mode), "non-regular task source " + str(path))
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise TaskSourceError("unavailable task source " + str(path)) from error


def status_token(value, identity):
    token = STATUS.match(value)
    require(token is not None, "unsupported status spelling " + identity)
    status = token[1] or token[2]
    require(status in STATUSES, "unknown status " + identity)
    return status


def direct_leaves(tree, text):
    """Status fields occupy the seven lines immediately after a numeric ID."""
    leaves = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = IDENTIFIER.match(line)
        if match is None:
            continue
        leaf = match[1]
        require(leaf.rsplit(".", 1)[0] == tree, "foreign leaf " + leaf)
        require(leaf not in leaves, "duplicate leaf " + leaf)
        statuses = []
        for following in lines[i + 1:i + 8]:
            if following.startswith("- ID:") or following.startswith("## "):
                break
            field = re.match(r"^\s*Status:\s*(.*)$", following)
            if field:
                statuses.append(status_token(field[1], leaf))
        require(len(statuses) == 1, "missing or duplicate status " + leaf)
        leaves[leaf] = statuses[0]
    return leaves


def read_task(path):
    """Read a live root plus its explicit, disjoint completed archive ranges."""
    path = Path(path)
    tree = path.stem
    text = read_text(path)
    identities = re.findall(r"^- Tree ID:\s*`([A-Za-z0-9_-]+)`\s*$", text, re.M)
    # Legacy synthetic fixtures have no Tree ID field; the filename still binds
    # their IDs. A declared identity must be unique and agree with that filename.
    declared = re.findall(r"^- Tree ID:", text, re.M)
    require(not declared or identities == [tree], "task identity " + tree)
    roots = re.findall(r"^- Status:\s*(.*)$", text, re.M)
    require(len(roots) == 1, "missing or duplicate root status " + tree)
    root_status = status_token(roots[0], tree)
    leaves = direct_leaves(tree, text)
    declarations = list(ARCHIVE.finditer(text))
    require(len(declarations) == len(re.findall(r"^_Leaves ", text, re.M)),
            "unsupported archived-leaf declaration " + tree)
    for declaration in declarations:
        first, last = int(declaration[1]), int(declaration[2])
        links = re.findall(r"\]\((archive/[^()]+\.md)\)", declaration[3])
        require(len(links) == 1, "archive locator arity " + tree)
        relative = PurePosixPath(links[0])
        require(str(relative) == links[0] and not relative.is_absolute() and
                ".." not in relative.parts and "\\" not in links[0] and
                all(ord(c) >= 32 and ord(c) != 127 for c in links[0]),
                "unsafe archive locator " + tree)
        parent = path.parent
        try:
            for part in relative.parts[:-1]:
                parent = parent / part
                require(stat.S_ISDIR(parent.lstat().st_mode),
                        "non-directory archive component " + str(parent))
        except OSError as error:
            raise TaskSourceError("unavailable archive directory " + str(parent)) from error
        archived = direct_leaves(tree, read_text(path.parent / relative))
        require(0 < first <= last and last - first + 1 <= len(archived),
                "archive range " + tree)
        expected = {tree + "." + str(n) for n in range(first, last + 1)}
        require(set(archived) == expected, "archive leaf population " + tree)
        require(all(status == "done" for status in archived.values()),
                "archive completion differs " + tree)
        require(not set(leaves) & set(archived), "root/archive leaf overlap " + tree)
        leaves.update(archived)
    require(bool(leaves), "no declared leaves " + tree)
    return TaskFacts(root_status, MappingProxyType(leaves), text)
