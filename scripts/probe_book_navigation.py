#!/usr/bin/env python3
"""Public preprocessor/API controls; all fixtures stay on the repository volume."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest

import book_navigation as N


def chapter(path, content, children=None):
    return {'Chapter': {'path': path, 'source_path': path, 'content': content,
                        'name': 'étiquette', 'sub_items': [] if children is None else children}}


class NavigationTests(unittest.TestCase):
    def setUp(self):
        parent = N.ROOT / 'target/book-navigation-probe'
        parent.mkdir(parents=True, exist_ok=True)
        self.fixture = tempfile.TemporaryDirectory(prefix='case-', dir=parent)
        self.addCleanup(self.fixture.cleanup)
        self.root = Path(self.fixture.name)
        for name in ['docs/tasks/P4-SYSTEM.md', 'docs/tasks/CI-RECOVERY.md',
                     'docs/tasks/archive/P4-SYSTEM-reference-c29e.md',
                     'docs/task-history/README.md']:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# Source\n')
        (self.root / 'docs/book').mkdir()
        self.context = {'root': str(self.root / 'docs/book'), 'renderer': 'html'}

    def models(self):
        registry = self.root / 'materials/units.sexp'
        registry.parent.mkdir()
        registry.write_text(''.join('(unit (id "' + uid + '") (kind processor) '
                                   '(layer processor) (book "docs/models/' + uid + '/"))\n'
                                   for uid in ['u1', 'u2']))
        for uid in ['u1', 'u2']:
            source = self.root / 'docs/models' / uid / 'src'
            source.mkdir(parents=True)
            (source / 'intro.md').write_text('# Intro\n')
        return self.root / 'docs/models/u1'

    def model_rewrite(self, book_root, text, path='intro.md'):
        context = {'root': str(book_root), 'renderer': 'html'}
        actual, count = N.preprocess(context, {'items': [chapter(path, text)]}, self.root)
        return actual['items'][0]['Chapter']['content'], count

    def test_model_sibling_route_and_suffixes(self):
        book = self.models()
        self.assertEqual(self.model_rewrite(book, '[Other](../../u2/src/intro.md?q=1#intro)'),
                         ('[Other](../../u2/book/intro.html?q=1#intro)', 1))

    def test_nested_model_route(self):
        book = self.models()
        self.assertEqual(self.model_rewrite(book, '[Other](../../../u2/src/intro.md)', 'deep/page.md'),
                         ('[Other](../../../u2/book/intro.html)', 1))

    def test_model_examples_and_unregistered_destinations_unchanged(self):
        book = self.models()
        for text in ['`[Other](../../u2/src/intro.md)`', '[Own](intro.md)',
                     '[Unknown](../../unknown/src/intro.md)',
                     '[Web](https://example.org/u2/src/intro.md)', '[Here](#intro)']:
            self.assertEqual(self.model_rewrite(book, text), (text, 0))

    def test_model_missing_source_refused(self):
        book = self.models()
        with self.assertRaisesRegex(N.NavigationRefused, 'missing or symlinked'):
            self.model_rewrite(book, '[Missing](../../u2/src/missing.md)')

    def test_model_symlink_source_and_ancestor_refused(self):
        book = self.models()
        source = self.root / 'docs/models/u2/src'
        (source / 'alias.md').symlink_to('intro.md')
        with self.assertRaises(N.NavigationRefused):
            self.model_rewrite(book, '[Alias](../../u2/src/alias.md)')
        (source / 'alias').symlink_to('.', target_is_directory=True)
        with self.assertRaises(N.NavigationRefused):
            self.model_rewrite(book, '[Alias](../../u2/src/alias/intro.md)')

    def test_unregistered_model_context_refused(self):
        self.models()
        context = {'root': str(self.root / 'docs/models/unknown'), 'renderer': 'html'}
        with self.assertRaises(N.NavigationRefused):
            N.preprocess(context, {'items': []}, self.root)

    def test_cli_model_json_protocol(self):
        context = {'root': str(N.ROOT / 'docs/models/lan9118-lab-v0'), 'renderer': 'html'}
        book = {'items': [chapter('introduction.md', '[Board](../../netboard-lab-v0/src/introduction.md)')]}
        result = self.cli(payload=json.dumps([context, book]))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['items'][0]['Chapter']['content'],
                         '[Board](../../netboard-lab-v0/book/introduction.html)')

    def rewrite(self, text, path='status.md'):
        return N.rewrite_links(self.root, path, text)

    def test_root_relative_task_keeps_label(self):
        self.assertEqual(self.rewrite('[`P4` é](docs/tasks/P4-SYSTEM.md)\n'),
                         ('[`P4` é](working/task-trees.md#read-task-history)\n', 1))

    def test_include_relative_task_uses_chapter_context(self):
        self.assertEqual(self.rewrite('[Task](tasks/CI-RECOVERY.md)', 'working/task-trees.md'),
                         ('[Task](task-trees.md#read-task-history)', 1))

    def test_both_declared_history_routes(self):
        self.assertEqual(self.rewrite('[Original](../../../tasks/archive/P4-SYSTEM-reference-c29e.md)', 'plan/p0.md'),
                         ('[Original](../working/task-trees.md#read-task-history)', 1))
        self.assertEqual(self.rewrite('[Reader](../../../task-history/README.md)', 'working/task-trees.md'),
                         ('[Reader](task-trees.md#read-task-history)', 1))

    def test_other_destinations_and_unsupported_forms_stay_exact(self):
        for text in ['[Web](https://example.org/tasks/P4-SYSTEM.md)', '[Mail](mailto:user@example.org)',
                     '[Here](#anchor)', '[Local](introduction.md)', '[Task](docs/tasks/P4-SYSTEM.md#goal)',
                     '[Task](docs/tasks/P4-SYSTEM.md?q=1)', '[Title](docs/tasks/P4-SYSTEM.md "title")',
                     '[Ref][task]\n[task]: docs/tasks/P4-SYSTEM.md',
                     '![Image](docs/tasks/P4-SYSTEM.md)',
                     '[Future archive](../../../tasks/archive/P4-SYSTEM-13.md)']:
            with self.subTest(text=text):
                self.assertEqual(self.rewrite(text), (text, 0))

    def test_fences_preserve_examples(self):
        for opening, closing in [('```python', '```'), ('~~~text', '~~~~'), ('   ```', '   ```')]:
            with self.subTest(opening=opening):
                code = opening + '\n[Task](docs/tasks/P4-SYSTEM.md)\n' + closing + '\n'
                self.assertEqual(self.rewrite(code + '[Live](docs/tasks/P4-SYSTEM.md)'),
                                 (code + '[Live](working/task-trees.md#read-task-history)', 1))

    def test_inline_code_delimiters_preserve_examples(self):
        for code in ['`[Task](docs/tasks/P4-SYSTEM.md)`', '``a`[Task](docs/tasks/P4-SYSTEM.md)``',
                     '`line\n[Task](docs/tasks/P4-SYSTEM.md)`']:
            with self.subTest(code=code):
                self.assertEqual(self.rewrite(code + ' [Live](docs/tasks/P4-SYSTEM.md)'),
                                 (code + ' [Live](working/task-trees.md#read-task-history)', 1))

    def test_html_examples_and_comments_stay_exact(self):
        for code in ['<code>[Task](docs/tasks/P4-SYSTEM.md)</code>',
                     '<pre>\n[Task](docs/tasks/P4-SYSTEM.md)\n</pre>',
                     '<!-- [Task](docs/tasks/P4-SYSTEM.md) -->']:
            with self.subTest(code=code):
                self.assertEqual(self.rewrite(code + '\n[Live](docs/tasks/P4-SYSTEM.md)'),
                                 (code + '\n[Live](working/task-trees.md#read-task-history)', 1))

    def test_escaped_link_opening_stays_literal(self):
        text = r'\[Literal](docs/tasks/P4-SYSTEM.md)'
        self.assertEqual(self.rewrite(text), (text, 0))
        self.assertEqual(self.rewrite(r'\\[Live](docs/tasks/P4-SYSTEM.md)'),
                         (r'\\[Live](working/task-trees.md#read-task-history)', 1))

    def test_nested_book_and_metadata_preserved(self):
        child = chapter('working/deep/page.md', '[Other](tasks/CI-RECOVERY.md)')
        book = {'items': [{'PartTitle': 'Start'}, 'Separator',
                         chapter('status.md', '[Task](docs/tasks/P4-SYSTEM.md)', [child])],
                'metadata': {'opaque': [1, 'λ']}}
        before = copy.deepcopy(book)
        actual, count = N.preprocess(self.context, book, self.root)
        expected = copy.deepcopy(before)
        expected['items'][2]['Chapter']['content'] = '[Task](working/task-trees.md#read-task-history)'
        expected['items'][2]['Chapter']['sub_items'][0]['Chapter']['content'] = '[Other](../task-trees.md#read-task-history)'
        self.assertEqual(actual, expected)
        self.assertEqual(book, before)
        self.assertEqual(count, 2)

    def test_draft_and_empty_book_preserved(self):
        for book in [{'items': []}, {'items': [chapter(None, '[Draft](tasks/P4-SYSTEM.md)')]}]:
            self.assertEqual(N.preprocess(self.context, book, self.root), (book, 0))

    def test_deep_nesting_refused_by_api_and_public_cli(self):
        book = {'items': []}
        children = book['items']
        for _ in range(1200):
            node = chapter(None, '')
            children.append(node)
            children = node['Chapter']['sub_items']
        with self.subTest(interface='api'):
            with self.assertRaisesRegex(N.NavigationRefused, 'book nesting exceeds supported depth'):
                N.preprocess(self.context, book, self.root)

        context = {'root': str(N.ROOT / 'docs/book'), 'renderer': 'html'}
        node = '{"Chapter":{"path":null,"content":"","sub_items":['
        payload = ('[' + json.dumps(context) + ',{"items":[' + node * 1200
                   + ']}}' * 1200 + ']}]')
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        for flags in [[], ['-O']]:
            with self.subTest(flags=flags):
                result = subprocess.run([sys.executable, *flags, N.__file__],
                                        input=payload, text=True, capture_output=True,
                                        env=env, timeout=60)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
                self.assertEqual(result.stderr, 'BOOK-NAVIGATION: REFUSED — '
                                 'book nesting exceeds supported depth\n')

    def test_invalid_context_refused(self):
        for context in [[], {'renderer': 'pdf', 'root': self.context['root']},
                        {'renderer': 'html', 'root': None},
                        {'renderer': 'html', 'root': str(self.root)}]:
            with self.subTest(context=context), self.assertRaises(N.NavigationRefused):
                N.preprocess(context, {'items': []}, self.root)

    def test_unsafe_chapter_paths_refused(self):
        for path in ['../escape.md', '/absolute.md', 'a\\b.md', '', True]:
            with self.subTest(path=path), self.assertRaises(N.NavigationRefused):
                N.preprocess(self.context, {'items': [chapter(path, 'text')]}, self.root)

    def test_malformed_book_nodes_refused(self):
        for book in [[], {}, {'items': {}}, {'items': [{'Unknown': 1}]},
                     {'items': [{'Chapter': None}]}, {'items': [chapter('x.md', 1)]},
                     {'items': [chapter('x.md', 'x', 'bad-children')]}]:
            with self.subTest(book=book), self.assertRaises(N.NavigationRefused):
                N.preprocess(self.context, book, self.root)

    def test_missing_declared_record_refused(self):
        with self.assertRaisesRegex(N.NavigationRefused, 'missing or symlinked'):
            self.rewrite('[Missing](tasks/NO-SUCH-TREE.md)')
        (self.root / 'docs/task-history/README.md').unlink()
        with self.assertRaisesRegex(N.NavigationRefused, 'missing or symlinked'):
            self.rewrite('[Missing](../../../task-history/README.md)', 'working/task-trees.md')

    def test_symlinked_record_refused(self):
        path = self.root / 'docs/tasks/P4-SYSTEM.md'
        path.unlink()
        path.symlink_to('CI-RECOVERY.md')
        with self.assertRaisesRegex(N.NavigationRefused, 'missing or symlinked'):
            self.rewrite('[Symlink](tasks/P4-SYSTEM.md)')

    def cli(self, args=(), payload=''):
        return subprocess.run([sys.executable, str(N.ROOT / 'scripts/book_navigation.py'), *args],
                              input=payload, text=True, capture_output=True)

    def test_cli_supports_and_arity(self):
        for args, rc in [(('supports', 'html'), 0), (('supports', 'pdf'), 1),
                         (('supports',), 1), (('unknown',), 1)]:
            with self.subTest(args=args):
                result = self.cli(args)
                self.assertEqual(result.returncode, rc)
                self.assertEqual(result.stdout, '')

    def test_cli_actual_json_protocol(self):
        context = {'root': str(N.ROOT / 'docs/book'), 'renderer': 'html'}
        book = {'items': [chapter('status.md', '[Task](docs/tasks/P4-SYSTEM.md)')]}
        result = self.cli(payload=json.dumps([context, book]))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['items'][0]['Chapter']['content'],
                         '[Task](working/task-trees.md#read-task-history)')
        self.assertIn('resolved 1', result.stderr)

    def test_cli_refuses_without_partial_stdout(self):
        for payload in ['{', '{}', '[{}, {}, {}]', '[null, {}]',
                        json.dumps([{'root': str(N.ROOT / 'docs/book'), 'renderer': 'pdf'}, {'items': []}])]:
            with self.subTest(payload=payload):
                result = self.cli(payload=payload)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
                self.assertIn('BOOK-NAVIGATION: REFUSED', result.stderr)

    def test_short_and_unclosed_fences(self):
        for code in ['```\n[Task](docs/tasks/P4-SYSTEM.md)\n``\n[Still code](tasks/CI-RECOVERY.md)',
                     '~~~\n[Task](docs/tasks/P4-SYSTEM.md)\n~~~ extra\n[Still code](tasks/CI-RECOVERY.md)']:
            self.assertEqual(self.rewrite(code), (code, 0))


def main():
    global N
    args = sys.argv[1:]
    if args:
        if len(args) != 2 or args[0] != '--mutation':
            raise SystemExit('usage: probe_book_navigation.py [--mutation no-route|no-code-mask|wrong-relative|no-source-guard]')
        mode = args[1]
        if mode == 'no-route':
            N.destination = lambda *args: None
        elif mode == 'no-code-mask':
            N.code_mask = lambda text: text
        elif mode == 'wrong-relative':
            N.posixpath.relpath = lambda *args: 'task-trees.md'
        elif mode == 'no-source-guard':
            source = Path(N.__file__).read_text().replace('if not source.is_file() or source.is_symlink():', 'if False:')
            mutant = types.ModuleType('navigation_mutant')
            mutant.__file__ = N.__file__
            exec(compile(source, mutant.__file__, 'exec'), mutant.__dict__)
            N = mutant
        else:
            raise SystemExit('unknown mutation ' + mode)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(NavigationTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
