#!/usr/bin/env python3
"""Exercise cleanup retention, both publishing views and discriminating omissions."""
from __future__ import annotations

import copy
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

import artifact_task_history as A
import artifact_task_history_preservation as P

FIXTURE_LEDGER = b'''## Acceptance Checklist (leaf ARTIFACT-CLEANUP.19)

- [x] **NO REGRESSION** - independent retention fixture.

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| capture | .19 | fixture | exact |

## Commit Log

fixture completed record

## Changelog

- fixture retained history
'''


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.row, self.bodies, self.files = A.read_terminal(A.PROJECT)
        source = self.bodies['predecessor']
        prefix = source[:self.row['suffix_offset']]
        prefix = prefix.replace(b'- ID: `ARTIFACT-CLEANUP.19`\n  Status: `pending`',
                                b'- ID: `ARTIFACT-CLEANUP.19`\n  Status: `active`', 1)
        self.live = prefix + A.pointer(self.row) + FIXTURE_LEDGER
        self.view = {**self.files, A.LIVE: ('100644', self.live)}
        self.birth = {A.LIVE: ('100644', self.bodies['predecessor'])}
        self.wiring = {name: ('100644', b'owned fixture wiring') for name in P.WIRING}

    def refused(self, reason, function, *arguments):
        with self.assertRaisesRegex(A.Refused, reason):
            function(*arguments)

    def terminal_variant(self, change):
        files, row = copy.deepcopy(self.files), copy.deepcopy(self.row)
        change(files, row)
        raw = (json.dumps(row, indent=2) + '\n').encode()
        files[A.INDEX] = ('100644', raw)
        return files, A.digest(raw)

    def live_variant(self, old, new):
        self.assertEqual(self.live.count(old), 1, 'unique fixture edit')
        return self.live.replace(old, new, 1)

    def fixture(self, root):
        for name, (_, raw) in self.view.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)

    def judge(self, proposed=None, working=None, birth=False, wiring=None):
        return P.judge(self.birth if birth else self.view,
                       self.view if proposed is None else proposed,
                       self.view if working is None else working,
                       {} if birth else self.wiring,
                       self.wiring if wiring is None else wiring, self.wiring)

    def test_retrieval_and_whole_prefix(self):
        row, bodies = A.validate_terminal(self.files)
        self.assertEqual(bodies['predecessor'][row['suffix_offset']:], bodies['retired_suffix'])
        P.first_transition(bodies['predecessor'], self.live, row)
        self.assertEqual(A.validate_live(self.live, row, bodies['predecessor'])['nodes'], 19)

    def test_immutable_descriptor(self):
        files = dict(self.files)
        files[A.INDEX] = ('100644', (json.dumps(self.row, indent=1) + '\n').encode())
        self.refused('immutable cleanup descriptor', A.validate_terminal, files)

    def test_duplicate_json_key(self):
        raw = self.files[A.INDEX][1].replace(b'{', b'{"kind":"duplicate",', 1)
        self.refused('duplicate JSON key', A.descriptor, raw)

    def test_closed_fields(self):
        row = dict(self.row, unknown='field')
        self.refused('unknown cleanup descriptor fields', A.descriptor, json.dumps(row).encode())

    def test_root_object_locator_contract(self):
        for role in ['predecessor', 'retired_suffix']:
            with self.subTest(role=role):
                entry = self.row[role]
                self.assertTrue(entry['object'].startswith(A.PREFIX))
                self.assertNotIn('path', entry, 'fixture path fields have a different base')
                row = copy.deepcopy(self.row)
                row[role]['path'] = row[role].pop('object')
                self.refused('unknown cleanup member fields', A.descriptor, json.dumps(row).encode())

    def test_typed_counts(self):
        for key in ['suffix_offset', 'unretained_bytes', 'narrative_health_bytes',
                    'narrative_ceiling_bytes', 'warning_percent', 'rollover_percent']:
            for value in [True, str(self.row[key])]:
                with self.subTest(key=key, value=value):
                    row = copy.deepcopy(self.row);row[key] = value
                    self.refused('count|contract', A.descriptor, json.dumps(row).encode())
        for role in ['predecessor', 'retired_suffix']:
            for key in ['bytes', 'lines']:
                for value in [True, str(self.row[role][key]), 0, 131073]:
                    with self.subTest(role=role, key=key, value=value):
                        row = copy.deepcopy(self.row);row[role][key] = value
                        self.refused('bounded integer', A.descriptor, json.dumps(row).encode())

    def test_closed_capture(self):
        for key, value in [('source', '0' * 40), ('owner', 'OTHER.1'),
                           ('source_path', '../escape'), ('source_mode', '100755')]:
            with self.subTest(key=key):
                row = dict(self.row);row[key] = value
                self.refused('capture boundary', A.descriptor, json.dumps(row).encode())

    def test_unsafe_member(self):
        row = copy.deepcopy(self.row);row['retired_suffix']['object'] = '../escape.md'
        self.refused('unsafe cleanup member path', A.descriptor, json.dumps(row).encode())

    def test_terminal_coverage(self):
        files = dict(self.files);files[A.PREFIX + 'unknown.md'] = ('100644', b'unknown')
        self.refused('terminal coverage', A.validate_terminal, files)

    def test_terminal_mode(self):
        files = dict(self.files);files[A.FRONT] = ('100755', files[A.FRONT][1])
        self.refused('terminal mode', A.validate_terminal, files)

    def test_corrupt_original(self):
        files = dict(self.files);name = self.row['predecessor']['object']
        files[name] = ('100644', files[name][1] + b'x')
        self.refused('original identity', A.validate_terminal, files)

    def test_exact_suffix(self):
        def change(files, row):
            old = row['retired_suffix']['object'];body = files.pop(old)[1].replace(b'Checklist', b'CHECKLIST', 1)
            row['retired_suffix'].update(sha256=A.digest(body))
            name = A.PREFIX + 'ledger-' + A.digest(body) + '.md'
            row['retired_suffix']['object'] = name;files[name] = ('100644', body)
        files, pin = self.terminal_variant(change)
        with mock.patch.object(A, 'INDEX_SHA256', pin):
            self.refused('exact predecessor suffix', A.validate_terminal, files)

    def test_retention_page(self):
        files = dict(self.files);files[A.FRONT] = ('100644', files[A.FRONT][1] + b'x')
        self.refused('retention page differs', A.validate_terminal, files)

    def test_descriptor_bound(self):
        self.refused('descriptor exceeds bound', A.descriptor, b' ' * (A.MAX_INDEX + 1))

    def test_parent_symlink_before_census(self):
        parent = A.PROJECT / 'target/cleanup-task-history-controls';parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as temporary:
            root = Path(temporary);foreign = root / 'foreign';foreign.mkdir()
            (foreign / 'artifact-cleanup-history').mkdir()
            (root / 'docs').symlink_to(foreign, target_is_directory=True)
            visits = []
            original = Path.iterdir
            def observe(path):
                visits.append(path)
                return original(path)
            with mock.patch.object(Path, 'iterdir', observe):
                with self.assertRaises(A.Refused):
                    A.read_terminal(root)
            self.assertEqual(visits, [], 'known symlink boundary must refuse before any directory census')

    def test_missing_physical_member(self):
        parent = A.PROJECT / 'target/cleanup-task-history-controls';parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as temporary:
            root = Path(temporary);self.fixture(root)
            (root / self.row['retired_suffix']['object']).unlink()
            self.refused('terminal coverage', A.read_terminal, root)

    def test_extra_directory_not_traversed(self):
        parent = A.PROJECT / 'target/cleanup-task-history-controls';parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as temporary:
            root = Path(temporary);self.fixture(root)
            extra = root / A.PREFIX / 'unknown';extra.mkdir()
            original = Path.iterdir;visits = []
            def observe(path):
                visits.append(path)
                return original(path)
            with mock.patch.object(Path, 'iterdir', observe):
                self.refused('coverage|unsafe cleanup terminal member', A.read_terminal, root)
            self.assertNotIn(extra, visits, 'unknown directory must never be traversed')

    def test_leaf_symlink(self):
        parent = A.PROJECT / 'target/cleanup-task-history-controls';parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as temporary:
            root = Path(temporary);self.fixture(root)
            member = root / self.row['retired_suffix']['object']
            retained = root / 'retained-input.md';retained.write_bytes(member.read_bytes())
            member.unlink();member.symlink_to(retained)
            self.refused('unsafe cleanup terminal member', A.read_terminal, root)
            self.assertEqual(retained.read_bytes(), self.bodies['retired_suffix'])

    def test_duplicate_pointer_marker(self):
        raw = self.live + b'<!-- ARTIFACT-CLEANUP-LEDGER: foreign -->\n'
        self.refused('pointer differs or is not unique', A.validate_live,
                     raw, self.row, self.bodies['predecessor'])

    def test_unknown_pointer(self):
        raw = self.live.replace(A.INDEX_SHA256.encode(), b'0' * 64, 1)
        self.refused('pointer differs', A.validate_live, raw, self.row, self.bodies['predecessor'])

    def test_node_retention(self):
        prefix, ledger = self.live.split(A.pointer(self.row))
        start, end = prefix.index(b'- ID: `ARTIFACT-CLEANUP.1`'), prefix.index(b'- ID: `ARTIFACT-CLEANUP.2`')
        prefix = prefix[:start] + prefix[end:]
        prefix = prefix.replace(b'Children: `ARTIFACT-CLEANUP.1`, ', b'Children: ', 1)
        raw = prefix + A.pointer(self.row) + ledger
        self.refused('node order/population', A.validate_live, raw, self.row, self.bodies['predecessor'])

    def test_completed_status(self):
        raw = self.live_variant('- ID: `ARTIFACT-CLEANUP.1` — **the first cleanup, the record, and the registry row**\n  Status: `done`'.encode(),
                                '- ID: `ARTIFACT-CLEANUP.1` — **the first cleanup, the record, and the registry row**\n  Status: `pending`'.encode())
        self.refused('status regressed', A.validate_live, raw, self.row, self.bodies['predecessor'])

    def test_activity_group(self):
        prefix, ledger = self.live.split(A.pointer(self.row));at = prefix.index(b'### Priority1 activity')
        before, activity = prefix[:at], prefix[at:]
        lines = activity.splitlines(keepends=True)
        activity = b''.join(line for line in lines if not line.startswith(b'  Children:'))
        self.refused('child group was lost', A.validate_live,
                     before + activity + A.pointer(self.row) + ledger, self.row, self.bodies['predecessor'])

    def test_raw_markup_section_bound(self):
        raw = self.live + b'<!--' + b'x' * 4096 + b'-->\n'
        self.refused('section exceeds ceiling', A.validate_live, raw, self.row, self.bodies['predecessor'])

    def test_rollover_stops_ordinary_growth(self):
        raw = self.live
        for marker, count in [(b'## Verification Log', 9500), (b'## Commit Log', 3100),
                              (b'## Changelog', 2200)]:
            raw = raw.replace(marker, b'<!--' + b'x' * count + b'-->\n\n' + marker, 1)
        self.refused('requires owned rollover', A.validate_live, raw, self.row, self.bodies['predecessor'])

    def test_hidden_narrative_prefix(self):
        raw = self.live.replace(A.pointer(self.row), b'## Verification Log\n\n' + A.pointer(self.row), 1)
        self.refused('narrative precedes', A.validate_live, raw, self.row, self.bodies['predecessor'])

    def test_live_ledger_utf8(self):
        self.refused('live task is not UTF-8', A.validate_live,
                     self.live + b'\xff', self.row, self.bodies['predecessor'])

    def test_first_publication(self):
        self.assertTrue(self.judge(birth=True))

    def test_first_prefix_preserved(self):
        raw = self.live_variant(b'bounded, evidenced artifact cleanup on a ~24 h cadence', b'changed historical goal')
        view = {**self.view, A.LIVE: ('100644', raw)}
        self.refused('lost or changed predecessor prefix', self.judge, view, view, True)

    def test_first_source_mode(self):
        previous = {A.LIVE: ('100755', self.bodies['predecessor'])}
        self.refused('source bytes/mode', P.judge, previous, self.view, self.view,
                     {}, self.wiring, self.wiring)

    def test_first_live_mode(self):
        view = {**self.view, A.LIVE: ('100755', self.live)}
        self.refused('live task missing/mode differs', self.judge, view, view, True)

    def test_published_missing_live(self):
        previous = dict(self.view);del previous[A.LIVE]
        try:
            P.judge(previous, self.view, self.view, self.wiring, self.wiring, self.wiring)
        except Exception as error:
            self.assertIsInstance(error, A.Refused, 'unavailable published data must refuse, not crash')
            self.assertIn('published cleanup live task missing/mode differs', str(error))
        else:
            self.fail('missing published live root was accepted')

    def test_first_partial_wiring(self):
        self.refused('wiring incomplete', self.judge, None, None, True,
                     {key: value for key, value in self.wiring.items() if key != P.WIRING[0]})

    def test_first_partial_staging(self):
        proposed = dict(self.view);del proposed[self.row['retired_suffix']['object']]
        self.refused('staged/working views differ', self.judge, proposed, None, True)

    def test_published_unchanged(self):
        self.assertFalse(self.judge())

    def test_staged_terminal_hidden_by_working(self):
        proposed = dict(self.view);proposed[A.FRONT] = ('100644', b'changed staged page')
        self.refused('staged terminal changed', self.judge, proposed)

    def test_working_terminal_corrupt(self):
        working = dict(self.view);working[A.FRONT] = ('100644', b'changed working page')
        self.refused('retention page differs', self.judge, None, working)

    def test_published_live_history(self):
        raw = self.live_variant(b'fixture completed record', b'published history changed')
        self.assertNotEqual(raw, self.live)
        proposed = {**self.view, A.LIVE: ('100644', raw)}
        self.refused('published cleanup commits history changed', self.judge, proposed)

    def test_new_entries_prepend(self):
        raw = self.live.replace(b'## Commit Log\n\n', b'## Commit Log\n\nnew completed unit\n\n', 1)
        view = {**self.view, A.LIVE: ('100644', raw)}
        self.assertFalse(self.judge(view, view))

    def test_cold_reader_without_git(self):
        parent = A.PROJECT / 'target/cleanup-task-history-controls';parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as temporary:
            root = Path(temporary)
            self.fixture(root)
            scripts = root / 'scripts';scripts.mkdir()
            for name in ['artifact_task_history.py', 'qualification_history_archive.py',
                         'task_history_archive.py', 'task_source.py']:
                shutil.copyfile(A.PROJECT / 'scripts' / name, scripts / name)
            before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            for role in ['ledger', 'predecessor']:
                result = subprocess.run([sys.executable, '-B', str(scripts / 'artifact_task_history.py'),
                                         '--read', role], cwd=parent, capture_output=True,
                                        env={'PATH': '', 'PYTHONDONTWRITEBYTECODE': '1',
                                             'TMPDIR': str(A.PROJECT / 'target/tmp')}, timeout=30)
                self.assertEqual((result.returncode, result.stderr), (0, b''))
                self.assertEqual(result.stdout, self.bodies['retired_suffix' if role == 'ledger' else role])
            after = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before, after, 'reader must not extract or generate files')
            (root / A.LIVE).write_bytes(self.live.replace(A.INDEX_SHA256.encode(), b'0' * 64, 1))
            result = subprocess.run([sys.executable, '-B', str(scripts / 'artifact_task_history.py'),
                                     '--read', 'ledger'], capture_output=True, timeout=30,
                                    env={'PATH': '', 'PYTHONDONTWRITEBYTECODE': '1'})
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b'', 'refusal must precede all original output')
            self.assertIn(b'pointer differs', result.stderr)


MUTATIONS = {
    'live-utf8': ('A', "raw.decode('utf-8')", 'pass', 'test_live_ledger_utf8'),
    'parent': ('A', 'directory = Q.owned_root(root / PREFIX)', 'directory = root / PREFIX', 'test_parent_symlink_before_census'),
    'pin': ('A', "require(digest(raw) == INDEX_SHA256,", "require(True,", 'test_immutable_descriptor'),
    'coverage': ('A', "require(set(files) == names,", "require(True,", 'test_terminal_coverage'),
    'mode': ('A', "require(all(mode == '100644' for mode, _ in files.values()),", "require(True,", 'test_terminal_mode'),
    'suffix': ('A', 'and source[offset:] == suffix,', 'and True,', 'test_exact_suffix'),
    'pointer': ('A', "require(raw.count(b'<!-- ARTIFACT-CLEANUP-LEDGER:') == 1 and raw.count(exact) == 1,", 'require(True,', 'test_duplicate_pointer_marker'),
    'nodes': ('A', "nodes = preserve_graph(source[:row['suffix_offset']], prefix)", "nodes = len(graph(prefix.decode('utf-8'))[0])", 'test_node_retention'),
    'status': ('A', "require(all(current[name] == 'done' for name, status in original.items() if status == 'done'),", 'require(True,', 'test_completed_status'),
    'children': ('A', 'require(all(name in groups and children <= groups[name] for name, children in old_groups.items()),', 'require(True,', 'test_activity_group'),
    'section': ('A', 'require(all(sizes[key] <= SECTIONS[key] for key in sizes),', 'require(True,', 'test_raw_markup_section_bound'),
    'rollover': ('A', "require(len(ledger) * 100 < row['narrative_health_bytes'] * row['rollover_percent'],", 'require(True,', 'test_rollover_stops_ordinary_growth'),
    'prefix': ('P', "first_transition(bodies['predecessor'], working[A.LIVE][1], row)", 'pass', 'test_first_prefix_preserved'),
    'source-mode': ('P', "require(previous.get(A.LIVE) == (row['source_mode'], bodies['predecessor']),", 'require(True,', 'test_first_source_mode'),
    'working-mode': ('P', "require(A.LIVE in working and working[A.LIVE][0] == '100644',", 'require(A.LIVE in working,', 'test_first_live_mode'),
    'previous-live': ('P', "require(A.LIVE in previous and previous[A.LIVE][0] == '100644',", 'require(True,', 'test_published_missing_live'),
    'staged': ('P', "require(terminal(proposed) == terminal(previous),", 'require(True,', 'test_staged_terminal_hidden_by_working'),
    'live-history': ('P', 'preserve_ledger(previous[A.LIVE][1], view[A.LIVE][1], row)', 'pass', 'test_published_live_history'),
}


def main():
    global A, P
    if sys.argv[1:] == ['--list-mutations']:
        print('\n'.join(MUTATIONS))
        return 0
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RetentionTests)
    if len(sys.argv) > 1:
        if len(sys.argv) != 3 or sys.argv[1] != '--mutation' or sys.argv[2] not in MUTATIONS:
            raise SystemExit('usage: probe_artifact_task_history.py [--mutation NAME]')
        target, old, new, test = MUTATIONS[sys.argv[2]]
        original = A if target == 'A' else P
        source = Path(original.__file__).read_text()
        if source.count(old) != 1:
            raise RuntimeError('mutation target differs')
        mutant = types.ModuleType(original.__name__ + '_mutant');mutant.__file__ = original.__file__
        exec(compile(source.replace(old, new, 1), original.__file__, 'exec'), mutant.__dict__)
        if target == 'A':
            A = mutant
        else:
            P = mutant
        suite = unittest.TestSuite([RetentionTests(test)])
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    print(output.getvalue(), end='')
    print(f'CLEANUP-TASK-HISTORY probe: {result.testsRun} tests / '
          f'{len(result.failures)} failures / {len(result.errors)} errors')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
