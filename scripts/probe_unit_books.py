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

    def test_missing_include_fails_in_project_and_unit(self):
        for relative in ['docs/book/src/intro.md', 'docs/models/u1/src/intro.md']:
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_text()
                path.write_text(original + '\n{{#include absent.txt}}\n')
                findings, _, _ = B.check_books(self.root)
                self.assertTrue(any('BOOK DOES NOT BUILD' in f and
                                    'missing include/source file' in f for f in findings), findings)
                path.write_text(original)

    def test_missing_duplicate_and_inverted_anchor_fail_before_expansion(self):
        bodies = ['// ANCHOR: other\ncontract\n// ANCHOR_END: other\n',
                  '// ANCHOR: part\ncontract\n// ANCHOR_END: part\n' * 2,
                  '// ANCHOR_END: part\ncontract\n// ANCHOR: part\n']
        for relative in ['docs/book/src/intro.md', 'docs/models/u1/src/intro.md']:
            path = self.root / relative
            original = path.read_text()
            for body in bodies:
                with self.subTest(relative=relative, body=body):
                    (path.parent / 'fragment.txt').write_text(body)
                    path.write_text(original + '\n{{#include fragment.txt:part}}\n')
                    findings, _, _ = B.check_books(self.root)
                    self.assertTrue(any('missing/ambiguous anchor' in f for f in findings), findings)
            path.write_text(original)

    def test_unsafe_or_unreadable_include_refuses_in_both_books(self):
        for relative in ['docs/book/src/intro.md', 'docs/models/u1/src/intro.md']:
            path = self.root / relative
            original = path.read_text()
            fragment = path.parent / 'fragment.txt'
            for kind in ['symlink', 'utf8']:
                with self.subTest(relative=relative, kind=kind):
                    if kind == 'symlink':
                        fragment.symlink_to(path.name)
                    else:
                        fragment.write_bytes(b'\xff')
                    path.write_text(original + '\n{{#include fragment.txt}}\n')
                    with self.assertRaises(B.BookRefused):
                        B.check_books(self.root)
                    fragment.unlink()
            path.write_text(original)

    def test_guard_overrides_disabled_or_reordered_source_processor(self):
        prefix = 'MDBOOK_PREPROCESSOR__SOURCE_CHECK__'
        disabled = {prefix + 'COMMAND': 'false', prefix + 'BEFORE': '[]',
                    prefix + 'AFTER': '["links"]', prefix + 'RENDERERS': '["pdf"]',
                    prefix + 'OPTIONAL': 'true'}
        path = self.root / 'docs/models/u1/src/intro.md'
        path.write_text('{{#include absent.txt}}\n')
        with mock.patch.dict(os.environ, disabled):
            findings, _, _ = B.check_books(self.root)
        self.assertTrue(any('missing include/source file' in f for f in findings), findings)

    def test_missing_duplicate_or_refused_success_witness_refuses(self):
        witness = 'BOOK-INCLUDES: checked 1 chapters / 0 include edges\n'
        for stderr in ['', witness * 2, 'BOOK-INCLUDES: REFUSED — controlled\n',
                       witness + 'BOOK-INCLUDES: unknown status\n']:
            with self.subTest(stderr=stderr), self.assertRaises(B.BookRefused):
                B.require_include_execution(subprocess.CompletedProcess([], 0, '', stderr), 'fixture')
        B.require_include_execution(subprocess.CompletedProcess([], 0, '', witness), 'fixture')

    def test_unavailable_or_invalid_include_protocol_metadata_refuses(self):
        for module in [types.SimpleNamespace(PREFIX='BOOK-INCLUDES: '),
                       types.SimpleNamespace(PREFIX=None, DEFECT_PREFIX='defect',
                                             REFUSED_PREFIX='refused', CHECKED=object())]:
            with self.subTest(module=module), mock.patch.dict(sys.modules, {'book_includes': module}):
                with self.assertRaises(B.BookRefused):
                    B.require_include_execution(subprocess.CompletedProcess([], 0, '', ''), 'fixture')

    def test_named_processor_protocol_failures_refuse_but_toml_defect_stays(self):
        for stderr in ['ERROR Unable to parse the preprocessed book from "source-check" processor\n',
                       'ERROR The "source-check" preprocessor exited unsuccessfully with exit status: 2 status\n']:
            with self.subTest(stderr=stderr), self.assertRaises(B.BookRefused):
                B.require_include_execution(subprocess.CompletedProcess([], 101, '', stderr), 'fixture')
        B.require_include_execution(subprocess.CompletedProcess([], 101, '', 'ERROR invalid TOML\n'), 'fixture')
        B.require_include_execution(subprocess.CompletedProcess([], 101, '',
            'BOOK-INCLUDES: DEFECT — missing include/source file absent.txt\n'
            'ERROR The "source-check" preprocessor exited unsuccessfully with exit status: 1 status\n'), 'fixture')

    def test_real_build_is_fresh_and_removed(self):
        parent = B.PROJECT / 'target/unit-books'
        allocate = B.tempfile.TemporaryDirectory
        allocated = []

        def observed(*args, **kwargs):
            directory = allocate(*args, **kwargs)
            allocated.append(Path(directory.name))
            return directory

        with mock.patch.object(B.tempfile, 'TemporaryDirectory', observed):
            findings, count, links = B.check_books(self.root)
        self.assertEqual(findings, [])
        self.assertEqual(count, 1)
        self.assertGreater(links, 0)
        self.assertEqual(len(allocated), 1)
        self.assertEqual(allocated[0].parent, parent)
        self.assertFalse(allocated[0].exists())
        self.assertFalse((self.root / 'docs/book/book').exists())
        self.assertFalse((self.root / 'docs/models/u1/book').exists())

    def reference_navigation(self, book_page, reference_pages):
        """A book page plus an `api/` reference tree inside the same output (RUSTDOC.2)."""
        output = self.root / 'web/book'
        self.write('web/book/index.html', book_page)
        for name, body in reference_pages.items():
            self.write('web/book/api/' + name, body)
        return B.navigation_findings(self.root / 'web', [output], [output / 'api'])

    def test_reference_pages_are_not_scanned_but_links_into_them_resolve(self):
        """rustdoc's own links (line ranges, encoded ids, a missing root index) are API-DOCS's business."""
        findings, checked = self.reference_navigation(
            '<h1>Book</h1><a href="api/crate/index.html">reference</a>',
            {'crate/index.html': '<a href="../src/lib.rs.html#3-9">src</a><a href="#impl-From%3CT%3E">impl</a>'
                                 '<a href="./index.html">help</a><a href="../../missing.html">gone</a>'})
        self.assertEqual(findings, [])
        self.assertEqual(checked, 1)

    def test_link_into_the_reference_must_land_on_a_page(self):
        findings, _ = self.reference_navigation(
            '<h1>Book</h1><a href="api/crate/missing.html">reference</a>', {'crate/index.html': '<h1>crate</h1>'})
        self.assertTrue(any('missing-path index.html -> api/crate/missing.html' in f or
                            'missing-path book/index.html -> api/crate/missing.html' in f for f in findings), findings)

    def test_fresh_bundle_builds_the_api_reference(self):
        """A workspace manifest makes the checker document it fresh; a book link into it resolves."""
        self.write('Cargo.toml', '[workspace]\nresolver = "2"\nmembers = ["probecrate"]\n')
        self.write('probecrate/Cargo.toml', '[package]\nname = "probecrate"\nversion = "0.1.0"\nedition = "2021"\n')
        self.write('probecrate/src/lib.rs', '//! A documented probe crate.\n/// One.\npub fn one() -> u32 { 1 }\n')
        self.write('docs/book/src/intro.md', '# Intro\n\n[the reference](api/probecrate/index.html)\n')
        findings, _, links = B.check_books(self.root)
        self.assertEqual(findings, [])
        self.write('docs/book/src/intro.md', '# Intro\n\n[the reference](api/probecrate/fn.absent.html)\n')
        findings, _, _ = B.check_books(self.root)
        self.assertTrue(any('missing-path' in f and 'api/probecrate/fn.absent.html' in f for f in findings), findings)
        self.assertFalse((self.root / 'target').exists())

    def test_stale_success_output_cannot_supply_missing_fresh_render(self):
        self.write('docs/book/book/index.html', '<h1>Stale project</h1>')
        self.write('docs/models/u1/book/index.html', '<h1>Stale model</h1>')
        with mock.patch.object(B.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', 'BOOK-INCLUDES: checked 1 chapters / 0 include edges\n')):
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
            raise SystemExit('usage: probe_unit_books.py [--mutation scan-reference|no-reference-check|no-api-build|no-catalogue|no-navigation|no-path-guard|reuse-stale|no-include-env|no-include-witness|no-include-refusal]')
        mode = args[1]
        if mode == 'no-catalogue':
            B.catalogue_findings = lambda *args: []
        elif mode == 'no-navigation':
            B.navigation_findings = lambda *args: ([], 0)
        elif mode == 'no-path-guard':
            B.book_path = lambda root, value: root / value.rstrip('/')
        elif mode in {'no-include-env', 'no-include-witness', 'no-include-refusal'}:
            source = Path(B.__file__).read_text()
            old, new = {
                'no-include-env': ('text=True, env=env)', 'text=True)'),
                'no-include-witness': ('if len(tagged) != 1 or checked.fullmatch(tagged[0]) is None:',
                                       'if False:'),
                'no-include-refusal': ('            require_include_execution(result, uid)',
                                       '            if not result.returncode: require_include_execution(result, uid)'),
            }[mode]
            if source.count(old) != 1:
                raise SystemExit('nonunique include mutation seam ' + mode)
            source = source.replace(old, new, 1)
            mutant = types.ModuleType('unit_books_mutant')
            mutant.__file__ = B.__file__
            exec(compile(source, mutant.__file__, 'exec'), mutant.__dict__)
            B = mutant
        elif mode in {'scan-reference', 'no-reference-check', 'no-api-build'}:
            source = Path(B.__file__).read_text()
            old, new = {
                'scan-reference': ("            if inside_reference(page.resolve()):\n                continue  # rustdoc's own pages",
                                   "            if False:\n                continue  # rustdoc's own pages"),
                'no-reference-check': ("            if not target.is_relative_to(web_root):\n                findings.append('BOOK-LINK unsafe-destination ' + label)\n                continue\n            if target.is_dir():",
                                       "            if not target.is_relative_to(web_root):\n                findings.append('BOOK-LINK unsafe-destination ' + label)\n                continue\n            if inside_reference(target):\n                continue\n            if target.is_dir():"),
                'no-api-build': ("    if not source_path(root, 'Cargo.toml').is_file():\n        return [], []",
                                 "    if True:\n        return [], []"),
            }[mode]
            if source.count(old) != 1:
                raise SystemExit('nonunique reference mutation seam ' + mode)
            mutant = types.ModuleType('unit_books_mutant')
            mutant.__file__ = B.__file__
            exec(compile(source.replace(old, new, 1), mutant.__file__, 'exec'), mutant.__dict__)
            B = mutant
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
    import probe_book_includes as includes
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BookTests)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(includes.IncludeTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
