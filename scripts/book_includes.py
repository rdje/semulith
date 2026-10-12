#!/usr/bin/env python3
"""Validate owned mdBook include inputs before the built-in links preprocessor.

The supported selection grammar is whole text, an ASCII named anchor, one
one-based line, and the three documented inclusive/open-ended line ranges.
Fences do not suppress include expansion. Only selected text is followed for
nested includes. This validates source integrity, not the meaning of prose.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

from book_paths import PROJECT, BookRefused, owned_root, source_path

HELPER = re.compile(r'\{\{\s*#\s*(include|rustdoc_include|playground)\b')
INCLUDE = re.compile(r'\{\{\s*#include\s+([^\s{}]+)[ \t]*}}')
ANCHOR = re.compile(r'ANCHOR(_END)?:[ \t]*([\w-]+)(?![\w-]|[^\x00-\x7f])')
NAME = re.compile(r'[A-Za-z0-9_-]+\Z')
DECIMAL = re.compile(r'[0-9]+\Z')
PREFIX = 'BOOK-INCLUDES: '
DEFECT_PREFIX = PREFIX + 'DEFECT — '
REFUSED_PREFIX = PREFIX + 'REFUSED — '
CHECKED = re.compile(re.escape(PREFIX) + r'checked ([0-9]+) chapters / ([0-9]+) include edges\Z')


class IncludeDefect(ValueError):
    """An owned source has a missing or ambiguous include selection."""


class IncludeRefused(ValueError):
    """The validator cannot qualify an input safely or unambiguously."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise IncludeRefused(message)


def relative(value: str) -> PurePosixPath:
    require(isinstance(value, str) and bool(value), 'expected a relative source path')
    require(not any(ord(c) < 32 or ord(c) == 127 for c in value) and '\\' not in value,
            'unsafe source path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and '.git' not in path.parts,
            'absolute or Git metadata source path')
    return path


def line_number(value: str, maximum: int, label: str) -> int:
    # Compare with the real file population before decoding. This handles huge
    # ranges consistently without depending on Python's integer digit limit.
    clean = value.lstrip('0') or '0'
    bound = str(maximum)
    if len(clean) > len(bound) or (len(clean) == len(bound) and clean > bound):
        raise IncludeDefect('missing line range ' + label)
    return int(clean)


def selection(text: str, fields: tuple[str, ...], label: str) -> str:
    """Select only the text whose nested directives mdBook will expand."""
    if not fields:
        return text.removesuffix('\n')
    lines = text.removesuffix('\n').split('\n') if text else []
    if len(fields) == 1 and fields[0] and not DECIMAL.fullmatch(fields[0]):
        name = fields[0]
        require(NAME.fullmatch(name) is not None, 'unsupported anchor selector: ' + label)
        markers = [(n, m.group(1), m.group(2)) for n, line in enumerate(lines)
                   for m in ANCHOR.finditer(line)]
        starts = [n for n, end, tag in markers if tag == name and end is None]
        ends = [n for n, end, tag in markers if tag == name and end is not None]
        if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
            raise IncludeDefect('missing/ambiguous anchor ' + label)
        return '\n'.join(line for line in lines[starts[0] + 1:ends[0]]
                         if not ANCHOR.search(line))
    require(len(fields) in {1, 2} and
            all(not f or DECIMAL.fullmatch(f) for f in fields) and
            any(fields), 'unsupported line selector: ' + label)
    if len(fields) == 1:
        start = end = line_number(fields[0], len(lines), label)
    else:
        start = line_number(fields[0], len(lines), label) if fields[0] else 1
        end = line_number(fields[1], len(lines), label) if fields[1] else len(lines)
    if not 1 <= start <= end <= len(lines):
        raise IncludeDefect('missing/inverted line range ' + label)
    return '\n'.join(lines[start - 1:end])


def directives(content: str):
    for prefix in HELPER.finditer(content):
        require(prefix.group(1) == 'include', 'unsupported file helper: ' + prefix.group(1))
        match = INCLUDE.match(content, prefix.start())
        require(match is not None and '\n' not in match.group(),
                'unsupported or incomplete include directive')
        fields = match.group(1).split(':')
        require(len(fields) <= 3, 'unsupported include selector')
        yield prefix.start(), fields[0], tuple(fields[1:])


class Inputs:
    """Read only regular, owned inputs; retain and recheck their identities."""

    def __init__(self, root: Path):
        self.root = owned_root(root)
        self.bodies: dict[str, str] = {}
        self.pins: dict[str, dict] = {}

    def locate(self, base: Path, value: str) -> Path:
        # Preserve the original component route for symlink/Git checks before
        # resolving '..'; reject even a route that leaves and later re-enters.
        cursor = base
        require(base.is_relative_to(self.root), 'source base outside corpus')
        for part in relative(value).parts:
            if part == '..':
                require(cursor != self.root, 'include leaves its owned corpus')
                cursor = cursor.parent
            else:
                cursor = source_path(self.root, (cursor / part).relative_to(self.root).as_posix())
        require(cursor.is_relative_to(self.root), 'source outside corpus')
        return cursor

    @staticmethod
    def identity(value):
        return (value.st_dev, value.st_ino, value.st_mode, value.st_size,
                value.st_mtime_ns, value.st_ctime_ns)

    def read(self, path: Path) -> str:
        name = path.relative_to(self.root).as_posix()
        if name in self.bodies:
            return self.bodies[name]
        path = source_path(self.root, name)
        try:
            before = path.lstat()
        except FileNotFoundError as exc:
            raise IncludeDefect('missing include/source file ' + name) from exc
        require(stat.S_ISREG(before.st_mode), 'non-regular source: ' + name)
        require(before.st_dev == self.root.stat().st_dev, 'source on another volume: ' + name)
        flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
        with os.fdopen(os.open(path, flags), 'rb') as opened:
            require(self.identity(os.fstat(opened.fileno())) == self.identity(before),
                    'source changed before read: ' + name)
            body = opened.read()
            after = os.fstat(opened.fileno())
        require(self.identity(before) == self.identity(after) == self.identity(path.lstat())
                and len(body) == after.st_size, 'source changed during read: ' + name)
        text = body.decode('utf-8').replace('\r\n', '\n')
        self.bodies[name] = text
        self.pins[name] = {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                           'mode': stat.S_IMODE(after.st_mode), 'identity': self.identity(after)}
        return text

    def unchanged(self):
        for name, pin in self.pins.items():
            path = source_path(self.root, name)
            require(self.identity(path.lstat()) == pin['identity'],
                    'source changed after validation: ' + name)


def preprocess(context: dict, book: dict, root: Path = PROJECT) -> tuple[dict, dict]:
    """Validate actual chapter/include inputs and return the unchanged book."""
    try:
        return _preprocess(context, book, root)
    except (BookRefused, OSError, UnicodeError, RecursionError) as exc:
        raise IncludeRefused(str(exc)) from exc


def _preprocess(context: dict, book: dict, root: Path) -> tuple[dict, dict]:
    require(isinstance(context, dict) and isinstance(book, dict),
            'expected context and book objects')
    require(context.get('renderer') == 'html', 'only the HTML renderer is supported')
    inputs = Inputs(root)
    supplied = context.get('root')
    require(isinstance(supplied, str), 'expected book root')
    book_root = Path(supplied)
    require(book_root.is_absolute() and book_root.is_relative_to(inputs.root),
            'book root outside owned corpus')
    book_root = inputs.locate(inputs.root, book_root.relative_to(inputs.root).as_posix())
    config = context.get('config')
    require(isinstance(config, dict) and isinstance(config.get('book', {}), dict),
            'expected book configuration')
    src = inputs.locate(book_root, config.get('book', {}).get('src', 'src'))
    chapters = []
    edges = []
    complete = set()

    def follow(path: Path, fields: tuple[str, ...]):
        # Explicit DFS avoids the Python recursion limit for nested file inputs.
        active = set()
        stack = [(False, path, fields)]
        while stack:
            leaving, current, selected = stack.pop()
            key = (current, selected)
            if leaving:
                active.remove(key)
                complete.add(key)
                continue
            if key in active:
                raise IncludeDefect('cyclic include ' + current.relative_to(inputs.root).as_posix())
            if key in complete:
                continue
            active.add(key)
            text = inputs.read(current)
            label = current.relative_to(inputs.root).as_posix() + ':' + ':'.join(selected)
            chosen = selection(text, selected, label)
            children = []
            for offset, target, selector in directives(chosen):
                destination = inputs.locate(current.parent, target)
                edges.append({'source': current.relative_to(inputs.root).as_posix(),
                              'selection': list(selected), 'character_offset': offset,
                              'target': destination.relative_to(inputs.root).as_posix(),
                              'target_selection': list(selector)})
                children.append((False, destination, selector))
            stack.append((True, current, selected))
            stack.extend(reversed(children))

    def visit(items):
        require(isinstance(items, list), 'expected mdBook items')
        for item in items:
            if item == 'Separator':
                continue
            if isinstance(item, dict) and set(item) == {'PartTitle'}:
                require(isinstance(item['PartTitle'], str), 'expected part title')
                continue
            require(isinstance(item, dict) and set(item) == {'Chapter'}, 'unknown mdBook item')
            chapter = item['Chapter']
            require(isinstance(chapter, dict) and 'source_path' in chapter and
                    isinstance(chapter.get('content'), str),
                    'expected chapter object/content')
            content = chapter['content']
            source = chapter.get('source_path')
            if source is None:
                require(not list(directives(content)), 'include without chapter source path')
            else:
                path = inputs.locate(src, source)
                inputs.read(path)
                chapters.append(path.relative_to(inputs.root).as_posix())
                for offset, target, selector in directives(content):
                    destination = inputs.locate(path.parent, target)
                    edges.append({'source': path.relative_to(inputs.root).as_posix(),
                                  'selection': None, 'character_offset': offset,
                                  'target': destination.relative_to(inputs.root).as_posix(),
                                  'target_selection': list(selector)})
                    follow(destination, selector)
            visit(chapter.get('sub_items'))

    visit(book.get('items'))
    require(len(chapters) == len(set(chapters)), 'duplicate actual chapter source')
    inputs.unchanged()
    pins = {name: {k: v for k, v in pin.items() if k != 'identity'}
            for name, pin in inputs.pins.items()}
    return book, {'chapters': chapters, 'include_edges': edges, 'inputs': pins}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def invalid_constant(value):
    raise IncludeRefused('non-JSON constant: ' + value)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=PROJECT,
                        help='owned corpus root, derived from this project by default')
    parser.add_argument('action', nargs='?')
    parser.add_argument('renderer', nargs='?')
    args = parser.parse_args(argv)
    if args.action is not None:
        if args.action != 'supports' or args.renderer is None:
            parser.error('expected supports RENDERER or [context, book] on stdin')
        return 0 if args.renderer == 'html' else 1
    try:
        wire = json.load(sys.stdin, object_pairs_hook=unique_object,
                         parse_constant=invalid_constant)
        require(isinstance(wire, list) and len(wire) == 2, 'expected [context, book]')
        book, report = preprocess(wire[0], wire[1], args.root)
    except IncludeDefect as exc:
        print(DEFECT_PREFIX + str(exc), file=sys.stderr)
        return 1
    except (IncludeRefused, UnicodeError, OSError, ValueError, RecursionError) as exc:
        print(REFUSED_PREFIX + str(exc), file=sys.stderr)
        return 2
    json.dump(book, sys.stdout, ensure_ascii=False)
    print(PREFIX + 'checked ' + str(len(report['chapters'])) + ' chapters / ' +
          str(len(report['include_edges'])) + ' include edges', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
