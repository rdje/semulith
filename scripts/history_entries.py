#!/usr/bin/env python3
"""Pure entry grammar/wrapper/ceiling owner shared by sharding and preservation.

The published sharder re-exports these names. Importing this module performs no
Git reads, writes, fixture allocation or repository discovery.
"""
from pathlib import Path
import re

REGISTRY = "doctrine/readme_routes.tsv"
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


SHARD_HEADER = (
    "# {head} shard — {first} … {last}\n"
    "\n"
    "> Sharded from `{head}.md` under its {kib} KiB ceiling "
    "(`doctrine/readme_routes.tsv`).\n"
    "> Entries in a shard are **never edited after the shard** — git history is canonical.\n"
    "\n"
)
