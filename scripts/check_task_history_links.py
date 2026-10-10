#!/usr/bin/env python3
"""Check incoming historical links and forbid live includes of sealed narratives.

Git enumerates project-owned Markdown for this gate only. The archive reader
itself remains independent of Git. Archived cross-links are checked as well.
"""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

import task_history_archive as history


def check_links(root, sources, row, originals):
    checked = 0
    for name, data in sources.items():
        text = data.decode('utf-8')
        links = [(value, False) for value in re.findall(r'\]\(([^)\s]+)\)', text)]
        links += [(value.split(':', 1)[0], True)
                  for value in re.findall(r'\{\{#include\s+([^}\s]+)', text)]
        for value, include in links:
            value = unquote(value.strip('<>'))
            path, _, anchor = value.partition('#')
            if not path or '://' in path or path.startswith('mailto:'):
                continue
            candidates = (root / path, root / Path(name).parent / path)
            for candidate in candidates:
                try:
                    logical = candidate.resolve().relative_to(root).as_posix()
                except ValueError:
                    continue
                if logical not in originals:
                    continue
                history.require(not include, f'sealed narrative used as live include: {name}')
                history.require(not anchor or anchor in row['anchors'].get(logical, []),
                                f'unretained history link anchor: {name} -> {logical}#{anchor}')
                checked += 1
                break
    return checked


def main():
    root = Path(__file__).resolve().parent.parent
    try:
        row, _, originals = history.load_terminal(root)
        paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
        sources = {name: (root / name).read_bytes() for name in paths
                   if name.endswith('.md') and not name.startswith('vendor/')}
        sources.update(originals)
        count = check_links(root, sources, row, originals)
        print(f'TASK-HISTORY-LINKS: ok ({count} historical links, no live narrative includes)')
    except (history.ArchiveRefused, OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        print(f'TASK-HISTORY-LINKS: REFUSED — {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
