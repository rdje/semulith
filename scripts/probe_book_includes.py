#!/usr/bin/env python3
"""Discriminating source/selector and public-protocol controls for book_includes."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import book_includes as I


class IncludeTests(unittest.TestCase):
    def setUp(self):
        parent = I.PROJECT / 'target/book-includes-probe'
        parent.mkdir(parents=True, exist_ok=True)
        allocated = tempfile.TemporaryDirectory(prefix='case-', dir=parent)
        self.addCleanup(allocated.cleanup)
        self.root = Path(allocated.name)
        self.book_root = self.root / 'book'
        self.write('book/src/one.md', '# One\n')
        self.context = {'root': str(self.book_root), 'renderer': 'html',
                        'config': {'book': {'src': 'src'}}}
        self.chapter = {'source_path': 'one.md', 'path': 'one.md',
                        'content': '# One\n', 'sub_items': []}
        self.book = {'items': [{'Chapter': self.chapter}]}

    def write(self, name, body):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body.encode() if isinstance(body, str) else body)
        return path

    def include(self, argument, target='alpha\nbeta\n'):
        self.chapter['content'] = '{{#include ' + argument + '}}\n'
        self.write('book/src/fragment.txt', target)

    def run_public(self, wire=None, args=()):
        command = [sys.executable, *(['-O'] if sys.flags.optimize else []),
                   str(Path(I.__file__).resolve()), '--root', str(self.root), *args]
        raw = json.dumps([self.context, self.book]).encode() if wire is None else wire
        return subprocess.run(command, input=raw, capture_output=True)

    def test_all_selection_forms_preserve_whole_protocol_object(self):
        for field in ['', ':2', '::2', ':2:', ':1:2', ':part']:
            with self.subTest(field=field):
                self.include('fragment.txt' + field,
                             '// ANCHOR: part\nα contract\n// ANCHOR_END: part\n')
                original = copy.deepcopy(self.book)
                output, report = I.preprocess(self.context, self.book, self.root)
                self.assertEqual(output, original)
                self.assertEqual(self.book, original)
                self.assertEqual(len(report['chapters']), 1)
                self.assertEqual(len(report['include_edges']), 1)
                self.assertEqual(set(report['inputs']), {'book/src/one.md', 'book/src/fragment.txt'})

    def test_named_nested_and_fenced_inputs_follow_selected_region_only(self):
        self.include('dir/first.txt:part')
        self.chapter['content'] = '```text\n' + self.chapter['content'] + '```\n'
        self.write('book/src/dir/first.txt', '{{#include absent-outside.txt}}\n'
                   '// ANCHOR: part\n// ANCHOR: nested\n{{#include second.txt}}\n'
                   '// ANCHOR_END: nested\n// ANCHOR_END: part\n')
        self.write('book/src/dir/second.txt', 'nested contract\n')
        _, report = I.preprocess(self.context, self.book, self.root)
        self.assertEqual([e['target'] for e in report['include_edges']],
                         ['book/src/dir/first.txt', 'book/src/dir/second.txt'])
        self.assertNotIn('book/src/fragment.txt', report['inputs'])
        self.assertIn('book/src/dir/second.txt', report['inputs'])
        (self.book_root / 'src/dir/second.txt').unlink()
        with self.assertRaises(I.IncludeDefect):
            I.preprocess(self.context, self.book, self.root)

    def test_whole_anchor_comments_do_not_create_selection_constraints(self):
        self.include('fragment.txt', '// ANCHOR: same\na\n// ANCHOR: same\nb\n')
        I.preprocess(self.context, self.book, self.root)

    def test_missing_file_and_anchor_fail_public_interface(self):
        for selector, body in [('absent.txt', ''), ('fragment.txt:absent', 'text\n')]:
            with self.subTest(selector=selector):
                self.include(selector, body)
                result = self.run_public()
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(result.stdout, b'')
                self.assertTrue(result.stderr.startswith(I.DEFECT_PREFIX.encode()), result.stderr)

    def test_duplicate_missing_end_and_inverted_anchors_fail(self):
        for body in ['// ANCHOR: part\na\n// ANCHOR_END: part\n' * 2,
                     '// ANCHOR: part\na\n',
                     '// ANCHOR_END: part\na\n// ANCHOR: part\n']:
            with self.subTest(body=body):
                self.include('fragment.txt:part', body)
                with self.assertRaises(I.IncludeDefect):
                    I.preprocess(self.context, self.book, self.root)

    def test_absent_inverted_and_zero_line_ranges_fail(self):
        for field in ['0', '3', '2:1', '1:3', ':0', '3:']:
            with self.subTest(field=field):
                self.include('fragment.txt:' + field)
                with self.assertRaises(I.IncludeDefect):
                    I.preprocess(self.context, self.book, self.root)

    def test_unsupported_and_incomplete_helper_refuses(self):
        self.write('book/src/fragment.txt', 'text\n')
        for content in ['{{#include}}', '{{#include fragment.txt',
                        '{{#include fragment.txt:}}', '{{#include fragment.txt:α}}',
                        '{{#rustdoc_include fragment.txt}}', '{{#playground fragment.txt}}']:
            with self.subTest(content=content):
                self.chapter['content'] = content
                with self.assertRaises(I.IncludeRefused):
                    I.preprocess(self.context, self.book, self.root)

    def test_cycles_fail_and_duplicate_acyclic_includes_pass(self):
        self.include('fragment.txt', '{{#include second.txt}}\n')
        self.write('book/src/second.txt', '{{#include fragment.txt}}\n')
        with self.assertRaises(I.IncludeDefect):
            I.preprocess(self.context, self.book, self.root)
        self.write('book/src/second.txt', 'terminal\n')
        self.chapter['content'] *= 2
        _, report = I.preprocess(self.context, self.book, self.root)
        self.assertEqual(len(report['include_edges']), 3)

    def test_relative_corpus_escape_and_absolute_include_refuse(self):
        for argument in ['../../../escape.txt', '/etc/passwd', '.git/config']:
            with self.subTest(argument=argument):
                self.include(argument)
                result = self.run_public()
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, b'')

    def test_book_root_lexical_escape_refuses_before_reading_sibling(self):
        corpus = self.root / 'corpus'
        corpus.mkdir()
        self.context['root'] = str(corpus / '..' / 'book')
        with self.assertRaises(I.IncludeRefused):
            I.preprocess(self.context, self.book, corpus)

    def test_symlink_leaf_and_ancestor_and_git_boundary_refuse(self):
        self.include('fragment.txt')
        original = self.book_root / 'src/fragment.txt'
        original.unlink()
        original.symlink_to('one.md')
        with self.assertRaises(I.IncludeRefused):
            I.preprocess(self.context, self.book, self.root)
        original.unlink()
        self.write('book/src/dir/fragment.txt', 'contract\n')
        (self.book_root / 'src/alias').symlink_to('dir', target_is_directory=True)
        self.chapter['content'] = '{{#include alias/fragment.txt}}'
        with self.assertRaises(I.IncludeRefused):
            I.preprocess(self.context, self.book, self.root)
        self.chapter['content'] = '{{#include dir/fragment.txt}}'
        marker = self.write('book/src/dir/.git', 'synthetic boundary\n')
        self.addCleanup(marker.unlink)
        with self.assertRaises(I.IncludeRefused):
            I.preprocess(self.context, self.book, self.root)

    def test_invalid_utf8_and_read_failure_refuse(self):
        self.include('fragment.txt', b'\xff')
        result = self.run_public()
        self.assertEqual((result.returncode, result.stdout), (2, b''))
        self.assertTrue(result.stderr.startswith(I.REFUSED_PREFIX.encode()), result.stderr)
        self.write('book/src/fragment.txt', 'text\n')
        original = I.os.open
        target = self.book_root / 'src/fragment.txt'
        count = 0

        def failed(path, *args, **kwargs):
            nonlocal count
            if path == target:
                count += 1
                raise PermissionError('owned read-failure fixture')
            return original(path, *args, **kwargs)

        with mock.patch.object(I.os, 'open', failed), self.assertRaises(I.IncludeRefused):
            I.preprocess(self.context, self.book, self.root)
        self.assertEqual(count, 1)

    def test_crlf_and_terminal_line_forms(self):
        for body in [b'alpha\r\nbeta\r\n', b'alpha\nbeta', b'alpha\nbeta\n\n']:
            with self.subTest(body=body):
                self.include('fragment.txt:2', body)
                I.preprocess(self.context, self.book, self.root)

    def test_missing_source_field_and_malformed_protocol_refuse(self):
        del self.chapter['source_path']
        result = self.run_public()
        self.assertEqual((result.returncode, result.stdout), (2, b''))
        context = json.dumps(self.context).encode()
        duplicate = b'[' + context + b', {"items":[],"items":[]}]'
        non_json = b'[' + context + b', {"items":[],"ignored":NaN}]'
        for wire in [b'{}', b'[{}, {}]', duplicate, non_json, b'\xff']:
            with self.subTest(wire=wire):
                result = self.run_public(wire)
                self.assertEqual((result.returncode, result.stdout), (2, b''))

    def test_public_line_contract_preserves_bare_cr_and_unicode_separators(self):
        # Captured mdbook0.5.4 output, not Python's broader splitlines rules.
        for separator in ['\u2028', '\u0085']:
            body = 'alpha' + separator + 'beta\ngamma\n'
            self.assertEqual(I.selection(body, ('2',), 'fragment'), 'gamma')
            self.include('fragment.txt:3', body)
            with self.assertRaises(I.IncludeDefect):
                I.preprocess(self.context, self.book, self.root)
        self.include('fragment.txt:2', b'alpha\rbeta\n')
        with self.assertRaises(I.IncludeDefect):
            I.preprocess(self.context, self.book, self.root)

    def test_another_volume_and_changed_input_refuse(self):
        self.include('fragment.txt')
        target = self.book_root / 'src/fragment.txt'
        original_stat = Path.stat
        calls = 0

        def foreign(path, *args, **kwargs):
            nonlocal calls
            result = original_stat(path, *args, **kwargs)
            if path == target:
                calls += 1
                fields = list(result)
                fields[2] += 1
                return os.stat_result(fields)
            return result

        opened = []
        original_open = os.open

        def spy_open(path, *args, **kwargs):
            if Path(path) == target:
                opened.append(path)
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, 'stat', foreign), mock.patch.object(os, 'open', spy_open), \
                self.assertRaises(I.IncludeRefused) as refused:
            I.preprocess(self.context, self.book, self.root)
        # How many pathlib calls reach Path.stat is the interpreter's business (3.11 routes is_symlink, exists and stat
        # there, 3.14 stat alone: 3 calls against 1, the hosted refusal of 2026-10-28), so the test holds the property —
        # the foreign volume is the reason, and the source is refused before it is ever opened — not a call count.
        self.assertGreaterEqual(calls, 1)
        self.assertIn('another volume', str(refused.exception))
        self.assertEqual(opened, [])
        original_lstat = Path.lstat
        calls = 0

        def changed(path, *args, **kwargs):
            nonlocal calls
            result = original_lstat(path, *args, **kwargs)
            if path == target:
                calls += 1
                if calls > 1:
                    fields = list(result)
                    fields[6] += 1
                    return os.stat_result(fields)
            return result

        with mock.patch.object(Path, 'lstat', changed), self.assertRaises(I.IncludeRefused) as refused:
            I.preprocess(self.context, self.book, self.root)
        # As above: the change is the reason, whichever lstat the interpreter routes first observes it.
        self.assertGreaterEqual(calls, 2)
        self.assertIn('changed', str(refused.exception))

    def test_change_after_selected_read_refuses(self):
        self.include('fragment.txt')
        target = self.book_root / 'src/fragment.txt'
        original = I.directives
        changes = 0

        def changed(content):
            nonlocal changes
            if content == 'alpha\nbeta':
                changes += 1
                target.write_text('mutated after selected read\n')
            yield from original(content)

        with mock.patch.object(I, 'directives', changed), self.assertRaises(I.IncludeRefused):
            I.preprocess(self.context, self.book, self.root)
        self.assertEqual(changes, 1)

    def test_all_item_kinds_nested_chapters_and_drafts(self):
        self.write('book/src/two.md', '# Two\n')
        self.chapter['sub_items'] = [{'Chapter': {'source_path': 'two.md',
            'content': '# Two\n', 'sub_items': []}}]
        self.book['items'].extend(['Separator', {'PartTitle': 'Part'},
            {'Chapter': {'source_path': None, 'content': '', 'sub_items': []}}])
        _, report = I.preprocess(self.context, self.book, self.root)
        self.assertEqual(report['chapters'], ['book/src/one.md', 'book/src/two.md'])
        self.book['items'].append({'Unexpected': 'item'})
        with self.assertRaises(I.IncludeRefused):
            I.preprocess(self.context, self.book, self.root)

    def test_empty_file_empty_anchor_and_non_ascii_anchor_alias(self):
        for argument, body in [('fragment.txt', ''), ('fragment.txt:part',
                               '// ANCHOR: part\n// ANCHOR_END: part\n')]:
            self.include(argument, body)
            I.preprocess(self.context, self.book, self.root)
        self.include('fragment.txt:part',
                     '// ANCHOR: part\u0301\ncontract\n// ANCHOR_END: part\u0301\n')
        with self.assertRaises(I.IncludeDefect):
            I.preprocess(self.context, self.book, self.root)

    def test_oversized_line_range_fails_without_integer_decoder_dependency(self):
        self.include('fragment.txt:' + '9' * 5000)
        with self.assertRaises(I.IncludeDefect):
            I.preprocess(self.context, self.book, self.root)

    def test_unexpanded_hash_spacing_refuses(self):
        self.write('book/src/fragment.txt', 'contract\n')
        for marker in ['{{# include fragment.txt}}', '{{ # include fragment.txt}}']:
            with self.subTest(marker=marker):
                self.chapter['content'] = marker + '\n'
                result = self.run_public()
                self.assertEqual((result.returncode, result.stdout), (2, b''))

    def test_supports_and_invalid_action_contract(self):
        for args, expected in [(('supports', 'html'), 0), (('supports', 'pdf'), 1),
                               (('not-supports',), 2)]:
            with self.subTest(args=args):
                result = self.run_public(args=args)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertEqual(result.stdout, b'')


def main():
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(IncludeTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
