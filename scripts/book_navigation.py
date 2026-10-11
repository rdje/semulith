#!/usr/bin/env python3
"""Resolve declared inline record and sibling-book links after include expansion.

This is an HTML-only mdBook preprocessor, not a general Markdown parser. It
rewrites simple inline links to existing task records, task-history reading
surfaces and registered sibling chapters. Labels, examples and canonical inputs stay
unchanged. Unsupported link syntax is left for rendered navigation verification.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import sys
from urllib.parse import urlsplit, urlunsplit

import unit_books as B

ROOT = Path(__file__).resolve().parent.parent
INLINE = re.compile(r'(?<!!)\[[^\]\n]*\]\((?P<target>[^\s()]+)\)')
TASK = re.compile(r'(?:docs/)?tasks/([A-Z0-9-]+)\.md\Z')
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')


class NavigationRefused(ValueError):
    """A declared route or mdBook protocol value is invalid."""


def code_mask(content: str) -> str:
    """Keep offsets while hiding fenced code and closed backtick code spans.

    The resolver's supported input is ordinary inline destinations. It deliberately
    does not expand reference links, HTML, link titles or arbitrary CommonMark.
    """
    chars = list(content)
    offset = 0
    fence = None
    for line in content.splitlines(keepends=True):
        match = FENCE.match(line.rstrip('\r\n'))
        fenced = fence is not None
        if match:
            ticks, tail = match.groups()
            if fence is None:
                # Backticks in a backtick fence's info string make it ordinary text.
                if ticks[0] != '`' or '`' not in tail:
                    fence = ticks
                    fenced = True
            elif ticks[0] == fence[0] and len(ticks) >= len(fence) and not tail.strip():
                fence = None
        if fenced:
            chars[offset:offset + len(line)] = [' ' if c not in '\r\n' else c for c in line]
        offset += len(line)
    masked = ''.join(chars)
    cursor = 0
    while match := re.search(r'`+', masked[cursor:]):
        start = cursor + match.start()
        width = len(match.group())
        # An escaped opening delimiter is ordinary text.
        back = start - 1
        while back >= 0 and masked[back] == '\\':
            back -= 1
        if (start - back - 1) % 2:
            cursor = start + width
            continue
        closing = re.search(r'(?<!`)' + '`' * width + r'(?!`)', masked[start + width:])
        if closing is None:
            cursor = start + width
            continue
        end = start + width + closing.end()
        chars[start:end] = [' ' if c not in '\r\n' else c for c in content[start:end]]
        cursor = end
    masked = ''.join(chars)
    # Preserve explicit HTML literal/example containers and comments as well.
    html = r'<!--.*?-->|<(code|pre|script|style|textarea)\b[^>]*>.*?</\1\s*>'
    for match in re.finditer(html, masked, re.I | re.S):
        chars[match.start():match.end()] = [' ' if c not in '\r\n' else c
                                          for c in content[match.start():match.end()]]
    return ''.join(chars)


def destination(root: Path, chapter: str, target: str,
                book_root: Path | None = None) -> str | None:
    """Map declared records to the guide, or sibling chapters to built HTML."""
    url = urlsplit(target)
    if book_root is not None and book_root != root / 'docs/book':
        if url.scheme or url.netloc or not url.path or '\\' in url.path:
            return None
        source = (book_root / 'src' / PurePosixPath(chapter).parent / url.path).resolve()
        for unit in B.registered_units(root):
            other = B.book_path(root, unit['book'])
            if other == book_root or not source.is_relative_to(other / 'src'):
                continue
            leaf = source.relative_to(other / 'src')
            if leaf.suffix != '.md':
                return None
            original = book_root / 'src' / PurePosixPath(chapter).parent / url.path
            # Resolve for matching, then validate the original route's components.
            # A symlink must not turn an unrelated source into a declared chapter.
            if original.is_symlink() or not source.is_file():
                raise NavigationRefused('declared model chapter is missing or symlinked: ' + target)
            B.source_path(root, original.relative_to(root).as_posix())
            relative = posixpath.relpath(other / 'book' / leaf.with_suffix('.html'),
                                        book_root / 'book' / PurePosixPath(chapter).parent)
            return urlunsplit(('', '', relative, url.query, url.fragment))
        return None
    if url.scheme or url.netloc or url.query or url.fragment or not url.path:
        return None
    task = TASK.fullmatch(url.path)
    if task:
        source = root / 'docs/tasks' / (task.group(1) + '.md')
    else:
        source = (root / 'docs/book/src' / PurePosixPath(chapter).parent / url.path).resolve()
        history = {root / 'docs/tasks/archive/P4-SYSTEM-reference-c29e.md',
                   root / 'docs/task-history/README.md'}
        if source not in history:
            return None
    if not source.is_file() or source.is_symlink():
        raise NavigationRefused('declared record is missing or symlinked: ' + target)
    relative = posixpath.relpath('working/task-trees.md', str(PurePosixPath(chapter).parent))
    return relative + '#read-task-history'


def rewrite_links(root: Path, chapter: str, content: str,
                  book_root: Path | None = None) -> tuple[str, int]:
    edits = []
    for match in INLINE.finditer(code_mask(content)):
        before = match.start() - 1
        while before >= 0 and content[before] == '\\':
            before -= 1
        if (match.start() - before - 1) % 2:
            continue
        replacement = destination(root, chapter, match.group('target'), book_root)
        if replacement is not None:
            edits.append((*match.span('target'), replacement))
    for start, end, replacement in reversed(edits):
        content = content[:start] + replacement + content[end:]
    return content, len(edits)


def preprocess(context: dict, book: dict, root: Path = ROOT) -> tuple[dict, int]:
    try:
        return _preprocess(context, book, root)
    except B.BookRefused as exc:
        raise NavigationRefused(str(exc)) from exc


def _preprocess(context: dict, book: dict, root: Path) -> tuple[dict, int]:
    if not isinstance(context, dict) or not isinstance(book, dict):
        raise NavigationRefused('expected context and book objects')
    if context.get('renderer') != 'html':
        raise NavigationRefused('only the HTML renderer is supported')
    root = B.owned_root(root)
    supplied_root = context.get('root')
    if not isinstance(supplied_root, str):
        raise NavigationRefused('expected a declared book root')
    book_root = Path(supplied_root).resolve()
    if book_root != root / 'docs/book':
        declared = [B.book_path(root, unit['book']) for unit in B.registered_units(root)]
        if book_root not in declared:
            raise NavigationRefused('expected a declared book root')
    B.source_path(root, book_root.relative_to(root).as_posix())
    result = copy.deepcopy(book)
    total = 0

    def visit(items):
        nonlocal total
        if not isinstance(items, list):
            raise NavigationRefused('expected mdBook items')
        for item in items:
            if item == 'Separator' or (isinstance(item, dict) and set(item) == {'PartTitle'}):
                continue
            if not isinstance(item, dict) or set(item) != {'Chapter'}:
                raise NavigationRefused('unknown mdBook item')
            chapter = item['Chapter']
            if not isinstance(chapter, dict):
                raise NavigationRefused('expected a chapter object')
            path, content = chapter.get('path'), chapter.get('content')
            if not isinstance(content, str):
                raise NavigationRefused('expected chapter content')
            if path is not None:
                if (not isinstance(path, str) or not path or '\\' in path or
                        PurePosixPath(path).is_absolute() or '..' in PurePosixPath(path).parts):
                    raise NavigationRefused('unsafe chapter path')
                chapter['content'], count = rewrite_links(root, path, content, book_root)
                total += count
            visit(chapter.get('sub_items'))

    visit(result.get('items'))
    return result, total


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args:
        return 0 if args == ['supports', 'html'] else 1
    try:
        incoming = json.load(sys.stdin)
        if not isinstance(incoming, list) or len(incoming) != 2:
            raise NavigationRefused('expected [context, book]')
        result, count = preprocess(*incoming)
        output = json.dumps(result, ensure_ascii=False)
    except (NavigationRefused, ValueError, OSError, TypeError) as exc:
        print('BOOK-NAVIGATION: REFUSED — ' + str(exc), file=sys.stderr)
        return 2
    print(output)
    print(f'BOOK-NAVIGATION: resolved {count} declared book links', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
