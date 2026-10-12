#!/usr/bin/env python3
"""Build an owned, fresh documentation bundle; validate includes and navigation.

Registry dictionaries use records_sexp's single mapping. All build outputs are
isolated under target/ and removed; source books are read-only inputs. Local
hyperlink paths and HTML fragments are checked offline, including print pages.
"""
from __future__ import annotations

from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

import records_sexp as R
import sexp as S

from book_paths import PROJECT, BookRefused, book_path, owned_root, source_path


def registered_units(root: Path) -> list[dict]:
    root = owned_root(root)
    try:
        units = R.load(source_path(root, 'materials/units.sexp'), root=root)
    except (R.RecordRefused, S.SexpError, OSError) as exc:
        raise BookRefused('cannot read materials/units.sexp: ' + str(exc)) from exc
    if not units:
        raise BookRefused('unit registry is empty')
    ids, paths = set(), set()
    for unit in units:
        if not {'id', 'kind', 'layer', 'book'} <= unit.keys():
            raise BookRefused('registry contains a non-unit record')
        uid = unit['id']
        if not uid or uid in ids:
            raise BookRefused('duplicate/empty unit id ' + uid)
        path = book_path(root, unit['book'])
        key = path.relative_to(root).as_posix().casefold()
        if key in paths:
            raise BookRefused('duplicate registered book path ' + unit['book'])
        ids.add(uid)
        paths.add(key)
    return units


def catalogue_findings(root: Path, units: list[dict]) -> list[str]:
    path = source_path(root, 'docs/book/src/models.md')
    if not path.is_file() or path.is_symlink():
        return ['MODEL-CATALOGUE missing docs/book/src/models.md']
    entries = re.findall(r'^- \*\*`([^`]+)`\*\* \(kind: ([a-z]+)\)',
                         path.read_text(encoding='utf-8'), re.M)
    listed = dict(entries)
    expected = {unit['id']: unit['kind'] for unit in units}
    findings = []
    if len(entries) != len(listed):
        findings.append('MODEL-CATALOGUE duplicate entry')
    for uid in sorted(expected.keys() - listed.keys()):
        findings.append('MODEL-CATALOGUE missing ' + uid)
    for uid in sorted(listed.keys() - expected.keys()):
        findings.append('MODEL-CATALOGUE unregistered ' + uid)
    for uid in sorted(expected.keys() & listed.keys()):
        if expected[uid] != listed[uid]:
            findings.append('MODEL-CATALOGUE kind ' + uid)
    return findings


class Document(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.links = []
        self.anchors = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.anchors.add(values['id'])
        if tag == 'a':
            if 'name' in values:
                self.anchors.add(values['name'])
            if 'href' in values:
                self.links.append(values['href'])


def navigation_findings(web_root: Path, output_dirs: list[Path]) -> tuple[list[str], int]:
    web_root = web_root.resolve()
    documents = {}
    findings = []
    for output in output_dirs:
        pages = sorted(output.rglob('*.html'))
        if not any(p.name not in {'print.html', '404.html'} for p in pages):
            findings.append('NO RENDERED BOOK ' + output.relative_to(web_root).as_posix())
        for page in pages:
            if (page.is_symlink() or not page.is_file() or
                    not page.resolve().is_relative_to(web_root) or
                    page.stat().st_dev != web_root.stat().st_dev):
                findings.append('UNSAFE RENDERED PAGE ' + page.relative_to(web_root).as_posix())
                continue
            documents[page.resolve()] = Document(page.read_text(encoding='utf-8'))
    checked = 0
    for page, document in list(documents.items()):
        for href in document.links:
            checked += 1
            try:
                url = urlsplit(href)
            except ValueError:
                findings.append('BOOK-LINK malformed URL ' + href)
                continue
            if url.scheme or url.netloc:
                continue  # Remote identities and availability are not an offline navigation claim.
            path = unquote(url.path)
            target = (web_root / path.lstrip('/') if path.startswith('/') else page.parent / path)
            target = target.resolve() if path else page
            label = page.relative_to(web_root).as_posix() + ' -> ' + href
            if not target.is_relative_to(web_root):
                findings.append('BOOK-LINK unsafe-destination ' + label)
                continue
            if target.is_dir():
                target = (target / 'index.html').resolve()
                if not target.is_relative_to(web_root):
                    findings.append('BOOK-LINK unsafe-destination ' + label)
                    continue
            if not target.is_file():
                findings.append('BOOK-LINK missing-path ' + label)
                continue
            if target.stat().st_dev != web_root.stat().st_dev:
                findings.append('BOOK-LINK unsafe-destination ' + label)
                continue
            if url.fragment and target.suffix.lower() == '.html':
                if target not in documents:
                    documents[target] = Document(target.read_text(encoding='utf-8'))
                if unquote(url.fragment) not in documents[target].anchors:
                    findings.append('BOOK-LINK missing-anchor ' + label)
    return findings, checked


def include_environment(root: Path) -> dict:
    """Force the owned validator before expansion, including scratch corpora."""
    validator = source_path(PROJECT, 'scripts/book_includes.py')
    if not validator.is_file():
        raise BookRefused('include validator is unavailable')
    env = dict(os.environ)
    prefix = 'MDBOOK_PREPROCESSOR__SOURCE_CHECK__'
    env.update({prefix + 'COMMAND': shlex.join([sys.executable, str(validator), '--root', str(root)]),
                prefix + 'BEFORE': '["links"]', prefix + 'AFTER': '[]',
                prefix + 'RENDERERS': '["html"]', prefix + 'OPTIONAL': 'false'})
    return env


def require_include_execution(result, uid: str) -> None:
    """Require one success witness and retain typed failures across mdBook."""
    try:
        import book_includes as I
        prefix, defect_prefix, refused_prefix, checked = I.PREFIX, I.DEFECT_PREFIX, I.REFUSED_PREFIX, I.CHECKED
    except (ImportError, OSError, SyntaxError, AttributeError) as exc:
        raise BookRefused('include protocol is unavailable: ' + str(exc)) from exc
    if (not all(isinstance(value, str) and value for value in [prefix, defect_prefix, refused_prefix])
            or not isinstance(checked, re.Pattern)):
        raise BookRefused('invalid include protocol metadata')
    lines = result.stderr.splitlines()
    tagged = [line for line in lines if line.startswith(prefix)]
    refused = [line for line in tagged if line.startswith(refused_prefix)]
    if refused:
        raise BookRefused('include inputs ' + uid + ': ' + refused[0])
    if result.returncode == 0:
        if len(tagged) != 1 or checked.fullmatch(tagged[0]) is None:
            raise BookRefused('missing/ambiguous include execution witness ' + uid)
    elif any('"source-check"' in line and
             ('preprocessor' in line or 'processor' in line) for line in lines):
        if len(tagged) != 1 or not tagged[0].startswith(defect_prefix):
            raise BookRefused('include processor failed before a typed verdict ' + uid)


def check_books(root: Path) -> tuple[list[str], int, int]:
    root = owned_root(root)
    units = registered_units(root)
    findings = catalogue_findings(root, units)
    env = include_environment(root)
    books = [source_path(root, 'docs/book')] + [book_path(root, u['book']) for u in units]
    registered = set(books[1:])
    models = root / 'docs/models'
    if models.is_dir():
        for directory, subdirs, files in os.walk(models, followlinks=False):
            path = Path(directory)
            if ((path / '.git').exists() or (path / '.git').is_symlink()
                    or path.stat().st_dev != root.stat().st_dev):
                findings.append('UNSAFE BOOK PATH another Git boundary')
                subdirs[:] = []
                continue
            subdirs[:] = [d for d in subdirs if d not in {'book', '.git'} and not (path / d).is_symlink()]
            if 'book.toml' in files and path not in registered:
                findings.append('ORPHAN BOOK ' + path.relative_to(models).as_posix())
    parent = source_path(PROJECT, 'target/unit-books')
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='bundle-', dir=parent) as allocated:
        scratch = Path(allocated)
        outputs = []
        for book in books:
            uid = next((u['id'] for u in units if book == root / u['book'].rstrip('/')), 'project')
            if not book.is_dir():
                findings.append(('NO PROJECT BOOK' if uid == 'project' else 'NO BOOK ' + uid))
                continue
            missing = [piece for piece in ['book.toml', 'src/SUMMARY.md']
                       if not source_path(root, (book / piece).relative_to(root).as_posix()).is_file()]
            if missing:
                findings.append('INCOMPLETE BOOK ' + uid + ': ' + ', '.join(missing))
                continue
            output = scratch / book.relative_to(root) / 'book'
            result = subprocess.run(['mdbook', 'build', str(book), '-d', str(output)],
                                    capture_output=True, text=True, env=env)
            require_include_execution(result, uid)
            if result.returncode:
                findings.append('BOOK DOES NOT BUILD ' + uid + ': ' + (result.stderr or result.stdout).strip())
                continue
            outputs.append(output)
        navigation, checked = navigation_findings(scratch / 'docs', outputs)
        findings.extend(navigation)
    return findings, len(units), checked


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print('usage: unit_books.py CORPUS_ROOT', file=sys.stderr)
        return 2
    try:
        findings, count, checked = check_books(Path(args[0]))
    except (BookRefused, OSError, UnicodeError) as exc:
        print('UNIT-BOOKS: REFUSED — ' + str(exc))
        print('__CHECKED__ 0')
        return 2
    for finding in findings:
        print(finding)
    print(f'__CHECKED__ {count}')
    print(f'__LINKS__ {checked}')
    return 1 if findings else 0


if __name__ == '__main__':
    raise SystemExit(main())
