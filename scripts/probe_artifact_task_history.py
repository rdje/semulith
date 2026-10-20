#!/usr/bin/env python3
"""Exercise cleanup retention, both publishing views and discriminating omissions."""
from __future__ import annotations

import copy
import io
import json
import re
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

FIXTURE_LEDGER = b'''## Acceptance Checklist (leaf ARTIFACT-CLEANUP.23)

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
        self.chain = self.row['generations']
        self.first, self.latest, self.count = self.chain[0], self.chain[-1], len(self.row['generations'])
        source = self.bodies[-1]['predecessor']
        prefix = source[:self.latest['suffix_offset']]
        owner = self.latest['owner'].encode()
        pending = re.compile(rb'(- ID: `' + re.escape(owner) + rb'`[^\n]*\n  Status: )`pending`\n')
        self.assertEqual(len(pending.findall(prefix)), 1, 'unique owner state in the predecessor')
        prefix = pending.sub(rb'\g<1>`active`\n', prefix, count=1)
        self.live = prefix + A.pointer(self.latest) + FIXTURE_LEDGER
        self.view = {**self.files, A.LIVE: ('100644', self.live)}
        newest = {self.latest['predecessor']['object'], self.latest['retired_suffix']['object'], A.INDEX, A.FRONT}
        earlier = {name: value for name, value in self.files.items() if name not in newest}
        self.previous = {**earlier, A.INDEX: ('100644', A.encoding(self.row, self.count - 1)),
                         A.FRONT: ('100644', b'superseded retention page'), A.LIVE: ('100644', source)}
        self.wiring = {name: ('100644', b'owned fixture wiring') for name in P.WIRING}

    def refused(self, reason, function, *arguments, **named):
        with self.assertRaisesRegex(A.Refused, reason):
            function(*arguments, **named)

    def terminal_variant(self, change):
        files, row = copy.deepcopy(self.files), copy.deepcopy(self.row)
        change(files, row)
        raw = A.encoding(row, len(row['generations']))
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

    def judge(self, proposed=None, working=None, transition=False, wiring=None):
        return P.judge(self.previous if transition else self.view,
                       self.view if proposed is None else proposed,
                       self.view if working is None else working,
                       {} if transition else self.wiring,
                       self.wiring if wiring is None else wiring, self.wiring)

    def test_retrieval_and_whole_prefix(self):
        row, bodies = A.validate_terminal(self.files)
        for entry, originals in zip(row['generations'], bodies):
            self.assertEqual(originals['predecessor'][entry['suffix_offset']:], originals['retired_suffix'])
        P.first_transition(bodies[-1]['predecessor'], self.live, self.latest)
        self.assertEqual(A.validate_live(self.live, row, bodies)['nodes'], 23)

    def test_generation_chain_reproduces_the_superseded_descriptor(self):
        self.assertEqual(A.digest(A.encoding(self.row, self.count - 1)), self.latest['predecessor_pointer'])
        self.assertTrue(self.bodies[-1]['retired_suffix'].startswith(
            A.pointer(self.chain[-2], self.latest['predecessor_pointer'])))
        self.assertEqual(A.generation_count(A.encoding(self.row, 1)), 1)
        self.assertEqual(A.generation_count(self.files[A.INDEX][1]), self.count)
        def change(files, row):
            row['generations'][-1]['predecessor_pointer'] = '0' * 64
        files, pin = self.terminal_variant(change)
        with mock.patch.object(A, 'INDEX_SHA256', pin):
            self.refused('generation chain differs', A.validate_terminal, files)

    def test_noncanonical_descriptor(self):
        raw = (json.dumps(json.loads(self.files[A.INDEX][1]), indent=1) + '\n').encode()
        files = dict(self.files);files[A.INDEX] = ('100644', raw)
        with mock.patch.object(A, 'INDEX_SHA256', A.digest(raw)):
            self.refused('noncanonical cleanup descriptor', A.validate_terminal, files)

    def test_immutable_descriptor(self):
        files = dict(self.files)
        files[A.INDEX] = ('100644', (json.dumps(json.loads(self.files[A.INDEX][1]), indent=1) + '\n').encode())
        self.refused('immutable cleanup descriptor', A.validate_terminal, files)

    def test_duplicate_json_key(self):
        raw = self.files[A.INDEX][1].replace(b'{', b'{"kind":"duplicate",', 1)
        self.refused('duplicate JSON key', A.descriptor, raw)

    def test_closed_fields(self):
        row = dict(self.row, unknown='field')
        self.refused('unknown cleanup descriptor fields', A.descriptor, json.dumps(row).encode())
        row = copy.deepcopy(self.row);row['generations'][0]['unknown'] = 'field'
        self.refused('unknown cleanup generation fields', A.descriptor, json.dumps(row).encode())
        legacy = json.loads(A.encoding(self.row, 1));legacy['unknown'] = 'field'
        self.refused('unknown cleanup descriptor fields', A.descriptor, json.dumps(legacy).encode(), 1)

    def test_generation_count(self):
        self.refused('generation count differs', A.descriptor, self.files[A.INDEX][1], self.count - 1)
        self.refused('generation count differs', A.descriptor, A.encoding(self.row, 1), self.count)
        self.refused('generation count differs', A.descriptor, self.files[A.INDEX][1], A.MAX_GENERATIONS + 1)

    def test_root_object_locator_contract(self):
        for role in ['predecessor', 'retired_suffix']:
            with self.subTest(role=role):
                entry = self.first[role]
                self.assertTrue(entry['object'].startswith(A.PREFIX))
                self.assertNotIn('path', entry, 'fixture path fields have a different base')
                row = copy.deepcopy(self.row)
                row['generations'][0][role]['path'] = row['generations'][0][role].pop('object')
                self.refused('unknown cleanup member fields', A.descriptor, json.dumps(row).encode())

    def test_typed_counts(self):
        for key in ['narrative_health_bytes', 'narrative_ceiling_bytes', 'warning_percent', 'rollover_percent']:
            for value in [True, str(self.row[key])]:
                with self.subTest(key=key, value=value):
                    row = copy.deepcopy(self.row);row[key] = value
                    self.refused('contract', A.descriptor, json.dumps(row).encode())
        for key in ['suffix_offset', 'unretained_bytes']:
            for value in [True, str(self.latest[key])]:
                with self.subTest(key=key, value=value):
                    row = copy.deepcopy(self.row);row['generations'][-1][key] = value
                    self.refused('count', A.descriptor, json.dumps(row).encode())
        for role in ['predecessor', 'retired_suffix']:
            for key in ['bytes', 'lines']:
                for value in [True, str(self.first[role][key]), 0, 131073]:
                    with self.subTest(role=role, key=key, value=value):
                        row = copy.deepcopy(self.row);row['generations'][0][role][key] = value
                        self.refused('bounded integer', A.descriptor, json.dumps(row).encode())

    def test_closed_capture(self):
        for index in range(self.count):
            for key, value in [('source', '0' * 40), ('owner', 'OTHER.1'),
                               ('source_path', '../escape'), ('source_mode', '100755'),
                               ('recorded_on', '2026-01-01')]:
                with self.subTest(index=index, key=key):
                    row = copy.deepcopy(self.row);row['generations'][index][key] = value
                    self.refused('capture boundary', A.descriptor, json.dumps(row).encode())
        row = copy.deepcopy(self.row);row['live_path'] = 'docs/tasks/OTHER.md'
        self.refused('capture boundary', A.descriptor, json.dumps(row).encode())
        row = copy.deepcopy(self.row);row['generations'][0]['predecessor_pointer'] = '0' * 64
        self.refused('generation chain differs', A.descriptor, json.dumps(row).encode())

    def test_unsafe_member(self):
        row = copy.deepcopy(self.row);row['generations'][-1]['retired_suffix']['object'] = '../escape.md'
        self.refused('unsafe cleanup member path', A.descriptor, json.dumps(row).encode())

    def test_terminal_coverage(self):
        files = dict(self.files);files[A.PREFIX + 'unknown.md'] = ('100644', b'unknown')
        self.refused('terminal coverage', A.validate_terminal, files)

    def test_terminal_mode(self):
        files = dict(self.files);files[A.FRONT] = ('100755', files[A.FRONT][1])
        self.refused('terminal mode', A.validate_terminal, files)

    def test_corrupt_original(self):
        for entry in self.chain:
            name = entry['predecessor']['object']
            files = dict(self.files);files[name] = ('100644', files[name][1] + b'x')
            self.refused('original identity', A.validate_terminal, files)

    def test_exact_suffix(self):
        def change(files, row):
            entry = row['generations'][-1]
            old = entry['retired_suffix']['object'];body = files.pop(old)[1].replace(b'Checklist', b'CHECKLIST', 1)
            entry['retired_suffix'].update(sha256=A.digest(body))
            name = A.PREFIX + 'ledger-' + A.digest(body) + '.md'
            entry['retired_suffix']['object'] = name;files[name] = ('100644', body)
        files, pin = self.terminal_variant(change)
        with mock.patch.object(A, 'INDEX_SHA256', pin):
            self.refused('exact predecessor suffix', A.validate_terminal, files)

    def test_retention_page(self):
        files = dict(self.files);files[A.FRONT] = ('100644', files[A.FRONT][1] + b'x')
        self.refused('retention page differs', A.validate_terminal, files)
        A.validate_terminal(files, front=False)

    def test_descriptor_bound(self):
        self.refused('descriptor exceeds bound', A.descriptor, b' ' * (A.MAX_INDEX + 1))
        self.refused('descriptor exceeds bound', A.generation_count, b' ' * (A.MAX_INDEX + 1))

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
            (root / self.latest['retired_suffix']['object']).unlink()
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
            member = root / self.first['retired_suffix']['object']
            retained = root / 'retained-input.md';retained.write_bytes(member.read_bytes())
            member.unlink();member.symlink_to(retained)
            self.refused('unsafe cleanup terminal member', A.read_terminal, root)
            self.assertEqual(retained.read_bytes(), self.bodies[0]['retired_suffix'])

    def test_duplicate_pointer_marker(self):
        raw = self.live + b'<!-- ARTIFACT-CLEANUP-LEDGER: foreign -->\n'
        self.refused('pointer differs or is not unique', A.validate_live, raw, self.row, self.bodies)

    def test_unknown_pointer(self):
        raw = self.live.replace(A.INDEX_SHA256.encode(), b'0' * 64, 1)
        self.refused('pointer differs', A.validate_live, raw, self.row, self.bodies)

    def test_node_retention(self):
        prefix, ledger = self.live.split(A.pointer(self.latest))
        start, end = prefix.index(b'- ID: `ARTIFACT-CLEANUP.1`'), prefix.index(b'- ID: `ARTIFACT-CLEANUP.2`')
        prefix = prefix[:start] + prefix[end:]
        prefix = prefix.replace(b'Children: `ARTIFACT-CLEANUP.1`, ', b'Children: ', 1)
        raw = prefix + A.pointer(self.latest) + ledger
        self.refused('node order/population', A.validate_live, raw, self.row, self.bodies)

    def test_completed_status(self):
        raw = self.live_variant('- ID: `ARTIFACT-CLEANUP.1` — **the first cleanup, the record, and the registry row**\n  Status: `done`'.encode(),
                                '- ID: `ARTIFACT-CLEANUP.1` — **the first cleanup, the record, and the registry row**\n  Status: `pending`'.encode())
        self.refused('status regressed', A.validate_live, raw, self.row, self.bodies)

    def test_activity_group(self):
        prefix, ledger = self.live.split(A.pointer(self.latest));at = prefix.index(b'### Priority1 activity')
        before, activity = prefix[:at], prefix[at:]
        lines = activity.splitlines(keepends=True)
        activity = b''.join(line for line in lines if not line.startswith(b'  Children:'))
        self.refused('child group was lost', A.validate_live,
                     before + activity + A.pointer(self.latest) + ledger, self.row, self.bodies)

    def test_raw_markup_section_bound(self):
        raw = self.live + b'<!--' + b'x' * 4096 + b'-->\n'
        self.refused('section exceeds ceiling', A.validate_live, raw, self.row, self.bodies)

    def test_rollover_stops_ordinary_growth(self):
        raw = self.live
        for marker, count in [(b'## Verification Log', 9500), (b'## Commit Log', 3100),
                              (b'## Changelog', 2200)]:
            raw = raw.replace(marker, b'<!--' + b'x' * count + b'-->\n\n' + marker, 1)
        self.refused('requires owned rollover', A.validate_live, raw, self.row, self.bodies)

    def test_hidden_narrative_prefix(self):
        raw = self.live.replace(A.pointer(self.latest), b'## Verification Log\n\n' + A.pointer(self.latest), 1)
        self.refused('narrative precedes', A.validate_live, raw, self.row, self.bodies)

    def test_live_ledger_utf8(self):
        self.refused('live task is not UTF-8', A.validate_live, self.live + b'\xff', self.row, self.bodies)

    def test_generation_transition(self):
        self.assertTrue(self.judge(transition=True))

    def test_transition_count_must_grow_by_one(self):
        previous = {A.LIVE: self.previous[A.LIVE]}
        self.refused('generation count differs from the committed terminal', P.judge, previous,
                     self.view, self.view, {}, self.wiring, self.wiring)

    def test_transition_prefix_preserved(self):
        raw = self.live_variant(b'bounded, evidenced artifact cleanup on a ~24 h cadence', b'changed historical goal')
        view = {**self.view, A.LIVE: ('100644', raw)}
        self.refused('lost or changed predecessor prefix', self.judge, view, view, True)

    def test_transition_source_mode(self):
        previous = {**self.previous, A.LIVE: ('100755', self.previous[A.LIVE][1])}
        self.refused('source bytes/mode', P.judge, previous, self.view, self.view,
                     {}, self.wiring, self.wiring)

    def test_transition_live_mode(self):
        view = {**self.view, A.LIVE: ('100755', self.live)}
        self.refused('live task missing/mode differs', self.judge, view, view, True)

    def test_transition_keeps_earlier_generation(self):
        name = self.first['retired_suffix']['object']
        changed = {**self.view, name: ('100644', self.view[name][1] + b'x')}
        self.refused('original identity', self.judge, changed, changed, True)
        previous = {**self.previous, name: ('100644', self.previous[name][1] + b'x')}
        self.refused('original identity', P.judge, previous, self.view, self.view,
                     {}, self.wiring, self.wiring)
        def change(files, row):
            row['generations'][0]['front_sha256'] = '0' * 64  # retained metadata only; the chain digest pins it
        files, pin = self.terminal_variant(change)
        with mock.patch.object(A, 'INDEX_SHA256', pin):
            self.refused('generation chain differs', A.validate_terminal, files)

    def test_published_missing_live(self):
        previous = dict(self.view);del previous[A.LIVE]
        try:
            P.judge(previous, self.view, self.view, self.wiring, self.wiring, self.wiring)
        except Exception as error:
            self.assertIsInstance(error, A.Refused, 'unavailable published data must refuse, not crash')
            self.assertIn('published cleanup live task missing/mode differs', str(error))
        else:
            self.fail('missing published live root was accepted')

    def test_transition_partial_wiring(self):
        self.refused('wiring incomplete', self.judge, None, None, True,
                     {key: value for key, value in self.wiring.items() if key != P.WIRING[0]})

    def test_transition_partial_staging(self):
        proposed = dict(self.view);del proposed[self.latest['retired_suffix']['object']]
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
            environment = {'PATH': '', 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(A.PROJECT / 'target/tmp')}
            for generation in range(1, self.count + 1):
                for role in ['ledger', 'predecessor']:
                    selector = [] if generation == self.count else ['--generation', str(generation)]
                    result = subprocess.run([sys.executable, '-B', str(scripts / 'artifact_task_history.py'),
                                             '--read', role, *selector], cwd=parent, capture_output=True,
                                            env=environment, timeout=30)
                    self.assertEqual((result.returncode, result.stderr), (0, b''))
                    self.assertEqual(result.stdout, self.bodies[generation - 1]['retired_suffix' if role == 'ledger' else role])
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
    'pin': ('A', "require(digest(raw) == pin,", "require(True,", 'test_immutable_descriptor'),
    'canonical': ('A', "require(encoding(row, generations) == raw,", "require(True,", 'test_noncanonical_descriptor'),
    'coverage': ('A', "require(len(names) == 2 + len(objects) and set(files) == names,", "require(True,", 'test_terminal_coverage'),
    'mode': ('A', "require(all(mode == '100644' for mode, _ in files.values()),", "require(True,", 'test_terminal_mode'),
    'suffix': ('A', 'and source[offset:] == suffix,', 'and True,', 'test_exact_suffix'),
    'pointer': ('A', "require(raw.count(b'<!-- ARTIFACT-CLEANUP-LEDGER:') == 1 and raw.count(exact) == 1,", 'require(True,', 'test_duplicate_pointer_marker'),
    'nodes': ('A', "nodes = preserve_graph(source[:latest['suffix_offset']], prefix)", "nodes = len(graph(prefix.decode('utf-8'))[0])", 'test_node_retention'),
    'status': ('A', "require(all(current[name] == 'done' for name, status in original.items() if status == 'done'),", 'require(True,', 'test_completed_status'),
    'children': ('A', 'require(all(name in groups and children <= groups[name] for name, children in old_groups.items()),', 'require(True,', 'test_activity_group'),
    'section': ('A', 'require(all(sizes[key] <= SECTIONS[key] for key in sizes),', 'require(True,', 'test_raw_markup_section_bound'),
    'rollover': ('A', "require(len(ledger) * 100 < row['narrative_health_bytes'] * row['rollover_percent'],", 'require(True,', 'test_rollover_stops_ordinary_growth'),
    'prefix': ('P', "first_transition(bodies[-1]['predecessor'], working[A.LIVE][1], latest)", 'pass', 'test_transition_prefix_preserved'),
    'source-mode': ('P', "require(previous.get(A.LIVE) == (latest['source_mode'], bodies[-1]['predecessor']),", 'require(True,', 'test_transition_source_mode'),
    'working-mode': ('P', "require(A.LIVE in working and working[A.LIVE][0] == '100644',", 'require(A.LIVE in working,', 'test_transition_live_mode'),
    'previous-live': ('P', "require(A.LIVE in previous and previous[A.LIVE][0] == '100644',", 'require(True,', 'test_published_missing_live'),
    'staged': ('P', "require(terminal(proposed) == held,", 'require(True,', 'test_staged_terminal_hidden_by_working'),
    'live-history': ('P', 'preserve_ledger(previous[A.LIVE][1], view[A.LIVE][1], latest)', 'pass', 'test_published_live_history'),
    'count': ('P', "require(previous_count in {count, count - 1},", 'require(True,', 'test_transition_count_must_grow_by_one'),
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
