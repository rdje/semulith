#!/usr/bin/env python3
"""Discriminating UNIT-BOOKS controls on owned, disposable fixtures."""
from __future__ import annotations

from pathlib import Path
import os
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

import unit_books as B


class BookTests(unittest.TestCase):
    def setUp(self):
        parent = B.PROJECT / 'target/unit-books-probe'
        parent.mkdir(parents=True, exist_ok=True)
        self.fixture = tempfile.TemporaryDirectory(prefix='case-', dir=parent)
        self.addCleanup(self.fixture.cleanup)
        self.root = Path(self.fixture.name)
        self.write('materials/units.sexp', '(unit (id "u1") (kind processor) '
                   '(layer processor) (book "docs/models/u1/"))\n')
        for relative in ['docs/book', 'docs/models/u1']:
            self.write(relative + '/book.toml', '[book]\ntitle = "fixture"\nsrc = "src"\n')
            self.write(relative + '/src/SUMMARY.md', '# Summary\n\n[Intro](intro.md)\n')
            self.write(relative + '/src/intro.md', '# Intro\n')
        self.catalogue = '- **`u1`** (kind: processor)\n'
        self.write('docs/book/src/models.md', self.catalogue)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def catalogue_result(self, text):
        self.write('docs/book/src/models.md', text)
        return B.catalogue_findings(self.root, B.registered_units(self.root))

    def navigation(self, text, extra=None):
        output = self.root / 'web/book'
        self.write('web/book/index.html', text)
        for name, body in (extra or {}).items():
            self.write('web/' + name, body)
        return B.navigation_findings(self.root / 'web', [output])

    def test_canonical_registry_and_catalogue(self):
        units = B.registered_units(self.root)
        self.assertEqual([(u['id'], u['book']) for u in units], [('u1', 'docs/models/u1/')])
        self.assertEqual(B.catalogue_findings(self.root, units), [])

    def test_missing_catalogue_entry(self):
        self.assertIn('MODEL-CATALOGUE missing u1', self.catalogue_result('# Models\n'))

    def test_extra_catalogue_entry(self):
        self.assertIn('MODEL-CATALOGUE unregistered u2',
                      self.catalogue_result(self.catalogue + '- **`u2`** (kind: board)\n'))

    def test_duplicate_catalogue_entry(self):
        self.assertIn('MODEL-CATALOGUE duplicate entry', self.catalogue_result(self.catalogue * 2))

    def test_wrong_catalogue_kind(self):
        self.assertIn('MODEL-CATALOGUE kind u1', self.catalogue_result(self.catalogue.replace('processor', 'board')))

    def test_absolute_traversal_and_noncanonical_paths_refused(self):
        for value in [str(self.root / 'docs/models/u1'), '../escape', 'docs/models/../u1',
                      'docs//models/u1', 'docs/models/./u1', 'docs\\models\\u1',
                      'C:/books/u1', 'docs/models/u1\n', 'profiles/u1']:
            with self.subTest(value=value), self.assertRaises(B.BookRefused):
                B.book_path(self.root, value)

    def test_book_ancestor_symlink_refused(self):
        (self.root / 'docs/models/alias').symlink_to('u1', target_is_directory=True)
        with self.assertRaises(B.BookRefused):
            B.book_path(self.root, 'docs/models/alias')

    def test_nested_git_marker_refused(self):
        marker = self.root / 'docs/models/u1/.git'
        marker.write_text('synthetic boundary fixture\n')
        self.addCleanup(marker.unlink)
        with self.assertRaises(B.BookRefused):
            B.book_path(self.root, 'docs/models/u1')
        with self.assertRaises(B.BookRefused):
            B.owned_root(marker.parent)

    def test_source_component_on_another_volume_refused(self):
        original = Path.stat
        foreign = self.root / 'docs/models/u1'

        def stat(path, *args, **kwargs):
            result = original(path, *args, **kwargs)
            if path == foreign:
                fields = list(result)
                fields[2] += 1
                return os.stat_result(fields)
            return result

        with mock.patch.object(Path, 'stat', stat), self.assertRaises(B.BookRefused):
            B.book_path(self.root, 'docs/models/u1')

    def test_duplicate_ids_and_book_paths_refused(self):
        original = (self.root / 'materials/units.sexp').read_text()
        for second in [original, original.replace('"u1"', '"u2"')]:
            self.write('materials/units.sexp', original + second)
            with self.assertRaises(B.BookRefused):
                B.registered_units(self.root)

    def test_symlinked_registry_refused(self):
        self.write('materials/source.sexp', (self.root / 'materials/units.sexp').read_text())
        (self.root / 'materials/units.sexp').unlink()
        (self.root / 'materials/units.sexp').symlink_to('source.sexp')
        with self.assertRaises(B.BookRefused):
            B.registered_units(self.root)

    def test_outside_project_root_refused(self):
        with self.assertRaises(B.BookRefused):
            B.owned_root(B.PROJECT.parent)

    def test_healthy_paths_fragments_queries_and_remote_urls(self):
        text = '<h1 id="here">Here</h1><a href="#here">same</a><a href="../other/?q=x#there">other</a>'
        text += '<a href="/other/index.html#there">root</a><a href="https://example.org/no">web</a>'
        text += '<a href="mailto:x@example.org">mail</a>'
        findings, checked = self.navigation(text, {'other/index.html': '<a name="there"></a>'})
        self.assertEqual(findings, [])
        self.assertEqual(checked, 5)

    def test_percent_encoded_path_and_anchor(self):
        findings, _ = self.navigation('<a href="space%20name.html#%CE%BB">read</a>',
                                     {'book/space name.html': '<h1 id="λ">λ</h1>'})
        self.assertEqual(findings, [])

    def test_missing_local_path(self):
        findings, _ = self.navigation('<a href="missing.html">missing</a>')
        self.assertTrue(any('missing-path' in f for f in findings), findings)

    def test_missing_html_anchor(self):
        findings, _ = self.navigation('<a href="index.html#missing">missing</a>')
        self.assertTrue(any('missing-anchor' in f for f in findings), findings)

    def test_print_page_links_are_checked(self):
        findings, _ = self.navigation('<h1>Intro</h1>',
                                     {'book/print.html': '<a href="absent.html">broken print</a>'})
        self.assertTrue(any('print.html -> absent.html' in f for f in findings), findings)

    def test_escaped_destination_and_symlinked_directory_index_refused(self):
        self.write('outside.html', '<h1 id="outside">Outside</h1>')
        for href in ['../../outside.html', '../other/#outside']:
            if href.startswith('../other'):
                self.write('web/other/placeholder', '')
                (self.root / 'web/other/index.html').symlink_to('../../outside.html')
            findings, _ = self.navigation('<a href="' + href + '">escape</a>')
            self.assertTrue(any('unsafe-destination' in f for f in findings), findings)

    def test_malformed_url_refused(self):
        findings, _ = self.navigation('<a href="http://[">bad URL</a>')
        self.assertTrue(any('malformed URL' in f for f in findings), findings)

    def test_no_rendered_book_refuses(self):
        self.write('web/book/print.html', '<h1>Only print</h1>')
        findings, _ = B.navigation_findings(self.root / 'web', [self.root / 'web/book'])
        self.assertTrue(any('NO RENDERED BOOK' in f for f in findings), findings)

    def test_real_build_is_fresh_and_removed(self):
        parent = B.PROJECT / 'target/unit-books'
        before = set(parent.iterdir()) if parent.exists() else set()
        findings, count, links = B.check_books(self.root)
        self.assertEqual(findings, [])
        self.assertEqual(count, 1)
        self.assertGreater(links, 0)
        self.assertEqual(set(parent.iterdir()), before)
        self.assertFalse((self.root / 'docs/book/book').exists())
        self.assertFalse((self.root / 'docs/models/u1/book').exists())

    def test_stale_success_output_cannot_supply_missing_fresh_render(self):
        self.write('docs/book/book/index.html', '<h1>Stale project</h1>')
        self.write('docs/models/u1/book/index.html', '<h1>Stale model</h1>')
        with mock.patch.object(B.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
            findings, _, _ = B.check_books(self.root)
        self.assertEqual(sum('NO RENDERED BOOK' in f for f in findings), 2, findings)

    def test_build_failure_cannot_use_stale_output(self):
        self.write('docs/models/u1/book/index.html', '<h1>Stale</h1>')
        self.write('docs/models/u1/book.toml', 'not TOML [[[\n')
        findings, _, _ = B.check_books(self.root)
        self.assertTrue(any('BOOK DOES NOT BUILD u1' in f for f in findings), findings)


def main():
    global B
    args = sys.argv[1:]
    if args:
        if len(args) != 2 or args[0] != '--mutation':
            raise SystemExit('usage: probe_unit_books.py [--mutation no-catalogue|no-navigation|no-path-guard|reuse-stale]')
        mode = args[1]
        if mode == 'no-catalogue':
            B.catalogue_findings = lambda *args: []
        elif mode == 'no-navigation':
            B.navigation_findings = lambda *args: ([], 0)
        elif mode == 'no-path-guard':
            B.book_path = lambda root, value: root / value.rstrip('/')
        elif mode == 'reuse-stale':
            source = Path(B.__file__).read_text()
            source = source.replace("output = scratch / book.relative_to(root) / 'book'", "output = book / 'book'")
            source = source.replace("navigation_findings(scratch / 'docs', outputs)", "navigation_findings(root / 'docs', outputs)")
            mutant = types.ModuleType('unit_books_mutant')
            mutant.__file__ = B.__file__
            sys.modules[mutant.__name__] = mutant
            exec(compile(source, mutant.__file__, 'exec'), mutant.__dict__)
            B = mutant
        else:
            raise SystemExit('unknown mutation ' + mode)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(BookTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
