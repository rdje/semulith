#!/usr/bin/env python3
"""Head/index preservation controls; no secondary Git repositories are created."""
from __future__ import annotations

import hashlib
from contextlib import redirect_stdout
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

import history_predecessor as P
import shard_history as SH

CEILINGS = {'CHANGELOG.md': 65536, 'DEV_NOTES.md': 49152}


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


class PredecessorTests(unittest.TestCase):
    def setUp(self):
        self.previous = {
            'CHANGELOG.md': b'# CHANGELOG.md\n\n## C-new\nfirst\n\n## C-old\nFocused11\n\n',
            'DEV_NOTES.md': '# DEV_NOTES.md\n\n## D-new\nλ\n\n## D-old\nFocused11\n\n'.encode(),
            'docs/changelog/shard-0001.md': b'# Old shard\n\n## frozen\noriginal\n',
        }
        self.previous[P.H.MANIFEST] = (digest(self.previous['docs/changelog/shard-0001.md']) +
                                       '  docs/changelog/shard-0001.md\n').encode()
        self.current = dict(self.previous)
        parent = P.ROOT / 'target/history-predecessor-probe'
        parent.mkdir(parents=True, exist_ok=True)
        self.fixture = tempfile.TemporaryDirectory(prefix='case-', dir=parent)
        self.addCleanup(self.fixture.cleanup)
        self.root = Path(self.fixture.name)

    def check(self):
        return P.verify(self.previous, self.current, CEILINGS)

    def new_shard(self, head, records, number=2):
        name = f'docs/changelog/shard-{number:04d}.md'
        wrapper = P.S.SHARD_HEADER.format(head=head[:-3], kib=CEILINGS[head] // 1024,
                                         first=records[0][0].split()[0],
                                         last=records[-1][0].split()[0]).encode()
        self.current[name] = wrapper + b''.join(body for _, body in records)
        self.current[P.H.MANIFEST] += (digest(self.current[name]) + '  ' + name + '\n').encode()
        return name

    def split(self, head='DEV_NOTES.md'):
        return P.entries(self.previous[head])

    def move_oldest(self):
        preamble, records = self.split()
        self.current['DEV_NOTES.md'] = preamble + records[0][1]
        return self.new_shard('DEV_NOTES.md', records[1:])

    def refreeze_new(self, name, before):
        self.current[P.H.MANIFEST] = self.current[P.H.MANIFEST].replace(
            digest(before).encode(), digest(self.current[name]).encode(), 1)

    def judge(self):
        (self.root / 'judgment').mkdir()
        P.judge_index(self.previous, self.current, self.root / 'judgment')

    def test_unchanged_heads(self):
        self.assertEqual(self.check(), (2, 4))

    def test_new_correction_entry_preserves_old_body(self):
        for head in P.HEADS:
            preamble, records = self.split(head)
            self.current[head] = preamble + ('## correction ' + head + '\nOld count corrected here.\n\n').encode() + b''.join(b for _, b in records)
        self.assertEqual(self.check(), (2, 4))

    def test_original_changelog_count_edit_refuses(self):
        self.current['CHANGELOG.md'] = self.current['CHANGELOG.md'].replace(b'Focused11', b'Focused12')
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_original_notes_count_edit_refuses(self):
        self.current['DEV_NOTES.md'] = self.current['DEV_NOTES.md'].replace(b'Focused11', b'Focused12')
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_preamble_edit_refuses(self):
        self.current['DEV_NOTES.md'] = self.current['DEV_NOTES.md'].replace(b'# DEV_NOTES.md', b'# notes')
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_removed_head_refuses(self):
        del self.current['DEV_NOTES.md']
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_reordered_entries_refuse(self):
        preamble, records = self.split()
        self.current['DEV_NOTES.md'] = preamble + b''.join(body for _, body in reversed(records))
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_new_entry_between_old_records_refuses(self):
        preamble, records = self.split()
        self.current['DEV_NOTES.md'] = preamble + records[0][1] + b'## inserted\nnew\n\n' + records[1][1]
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_duplicate_old_entry_refuses(self):
        preamble, records = self.split()
        self.current['DEV_NOTES.md'] = preamble + records[0][1] + b''.join(body for _, body in records)
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_whole_oldest_suffix_move(self):
        self.move_oldest()
        self.assertEqual(self.check(), (2, 4))

    def test_multiple_moves_reconstruct_in_reverse_shard_order(self):
        self.previous['DEV_NOTES.md'] += b'## D-older\noldest\n\n'
        self.current['DEV_NOTES.md'] = self.previous['DEV_NOTES.md']
        preamble, records = self.split()
        self.current['DEV_NOTES.md'] = preamble + records[0][1]
        self.new_shard('DEV_NOTES.md', records[2:], 2)
        self.new_shard('DEV_NOTES.md', records[1:2], 3)
        self.assertEqual(self.check(), (2, 5))

    def test_new_entries_can_also_move_in_published_shards(self):
        preamble, records = self.split()
        self.current['DEV_NOTES.md'] = preamble + b'## newest\nnow\n\n'
        self.new_shard('DEV_NOTES.md', [('newer', b'## newer\nnew\n\n'), *records])
        self.assertEqual(self.check(), (2, 4))

    def test_changed_moved_body_refuses_even_with_new_digest(self):
        name = self.move_oldest()
        before = self.current[name]
        self.current[name] = before.replace(b'Focused11', b'Focused12')
        self.refreeze_new(name, before)
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_new_shard_digest_refuses(self):
        name = self.move_oldest()
        self.current[P.H.MANIFEST] = self.current[P.H.MANIFEST].replace(digest(self.current[name]).encode(), b'0' * 64)
        with self.assertRaisesRegex(P.HistoryChanged, 'digest'):
            self.check()

    def test_wrong_head_wrapper_refuses(self):
        name = self.move_oldest()
        before = self.current[name]
        self.current[name] = before.replace(b'48 KiB', b'47 KiB')
        self.refreeze_new(name, before)
        with self.assertRaisesRegex(P.HistoryChanged, 'wrapper'):
            self.check()

    def test_new_unpublished_shard_name_refuses(self):
        name = self.move_oldest()
        renamed = 'docs/changelog/arbitrary.md'
        self.current[renamed] = self.current.pop(name)
        self.current[P.H.MANIFEST] = self.current[P.H.MANIFEST].replace(name.encode(), renamed.encode())
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_missing_new_shard_refuses(self):
        del self.current[self.move_oldest()]
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_duplicate_manifest_row_refuses(self):
        self.current[P.H.MANIFEST] *= 2
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_empty_live_head_refuses(self):
        preamble, records = self.split()
        self.current['DEV_NOTES.md'] = preamble
        self.new_shard('DEV_NOTES.md', records)
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_newline_conversion_refuses(self):
        self.previous['DEV_NOTES.md'] = self.previous['DEV_NOTES.md'].replace(b'\n', b'\r\n')
        with self.assertRaises(P.HistoryChanged):
            self.check()

    def test_healthy_staged_partition(self):
        self.move_oldest()
        self.judge()

    def test_bad_staged_shard_cannot_hide_behind_restored_working_bytes(self):
        self.assertEqual(P.verify(self.previous, dict(self.previous), CEILINGS), (2, 4))
        self.current['docs/changelog/shard-0001.md'] += b'edited'
        with self.assertRaisesRegex(P.HistoryChanged, 'staged partition:.*THAWED'):
            self.judge()

    def test_removed_staged_manifest_row_refuses(self):
        name = self.move_oldest()
        self.current[P.H.MANIFEST] = (digest(self.current[name]) + '  ' + name + '\n').encode()
        del self.current['docs/changelog/shard-0001.md']
        with self.assertRaisesRegex(P.HistoryChanged, 'staged partition:.*REMOVED ROW'):
            self.judge()

    def test_failed_git_inventory_is_not_absence(self):
        failure = subprocess.CompletedProcess([], 128, b'', b'injected read failure')
        with mock.patch.object(P.subprocess, 'run', return_value=failure), self.assertRaisesRegex(P.HistoryRefused, 'Git read failed'):
            P.git_snapshot(P.ROOT)

    def test_genuinely_empty_closed_inventory(self):
        success = subprocess.CompletedProcess([], 0, b'', b'')
        with mock.patch.object(P.subprocess, 'run', return_value=success):
            self.assertEqual(P.git_snapshot(P.ROOT), {})

    def test_failed_blob_read_is_not_absence(self):
        oid = 'a' * 40
        results = [subprocess.CompletedProcess([], 0, f'100644 blob {oid}\tDEV_NOTES.md\0'.encode(), b''),
                   subprocess.CompletedProcess([], 0, f'{oid} blob 3\n'.encode(), b''),
                   subprocess.CompletedProcess([], 128, b'', b'injected blob failure')]
        with mock.patch.object(P.subprocess, 'run', side_effect=results), self.assertRaisesRegex(P.HistoryRefused, 'Git read failed'):
            P.git_snapshot(P.ROOT)

    def test_git_size_bound_precedes_payload_read(self):
        oid = 'a' * 40
        results = [subprocess.CompletedProcess([], 0, f'100644 blob {oid}\tDEV_NOTES.md\0'.encode(), b''),
                   subprocess.CompletedProcess([], 0, f'{oid} blob {P.MAX_SNAPSHOT_BYTES + 1}\n'.encode(), b'')]
        with mock.patch.object(P.subprocess, 'run', side_effect=results) as run, self.assertRaisesRegex(P.HistoryRefused, 'byte bound'):
            P.git_snapshot(P.ROOT)
        self.assertEqual(run.call_count, 2)

    def test_git_file_bound_precedes_blob_queries(self):
        oid = 'a' * 40
        inventory = ''.join(f'100644 blob {oid}\t{head}\0' for head in P.HEADS).encode()
        success = subprocess.CompletedProcess([], 0, inventory, b'')
        with mock.patch.object(P.subprocess, 'run', return_value=success) as run, \
                mock.patch.object(P, 'MAX_SNAPSHOT_FILES', 1), \
                self.assertRaisesRegex(P.HistoryRefused, 'file bound'):
            P.git_snapshot(P.ROOT)
        self.assertEqual(run.call_count, 1)

    def test_unsafe_snapshot_names_refuse(self):
        for name in ['docs/history/../escape', '/absolute', 'docs/history/a\n',
                     'docs/history/' + 'x' * 257, 'docs/history/a\\b']:
            with self.subTest(name=name), self.assertRaises(P.HistoryRefused):
                P.owned_path(self.root, name)

    def test_partial_git_blob_refuses(self):
        oid = 'a' * 40
        results = [subprocess.CompletedProcess([], 0, f'100644 blob {oid}\tDEV_NOTES.md\0'.encode(), b''),
                   subprocess.CompletedProcess([], 0, f'{oid} blob 3\n'.encode(), b''),
                   subprocess.CompletedProcess([], 0, f'{oid} blob 3\nab'.encode(), b'')]
        with mock.patch.object(P.subprocess, 'run', side_effect=results), self.assertRaises(P.HistoryRefused):
            P.git_snapshot(P.ROOT)

    def test_unmerged_and_symlinked_index_paths_refuse(self):
        for mode, stage in [('100644', '1'), ('120000', '0')]:
            result = subprocess.CompletedProcess([], 0, f'{mode} {"a" * 40} {stage}\tDEV_NOTES.md\0'.encode(), b'')
            with mock.patch.object(P.subprocess, 'run', return_value=result), self.assertRaises(P.HistoryRefused):
                P.git_snapshot(P.ROOT, ':')

    def test_working_symlink_and_synthetic_git_boundary_refuse(self):
        (self.root / 'source.md').write_text('source')
        (self.root / 'DEV_NOTES.md').symlink_to('source.md')
        with self.assertRaises(P.HistoryRefused):
            P.working_snapshot(self.root)
        (self.root / 'DEV_NOTES.md').unlink()
        directory = self.root / 'docs/history'
        directory.mkdir(parents=True)
        marker = directory / '.git'
        marker.write_text('synthetic boundary')
        self.addCleanup(marker.unlink)
        with self.assertRaises(P.HistoryRefused):
            P.working_snapshot(self.root)

    def test_working_snapshot_bound(self):
        (self.root / 'DEV_NOTES.md').write_bytes(b'12345')
        with mock.patch.object(P, 'MAX_SNAPSHOT_BYTES', 3), self.assertRaises(P.HistoryRefused):
            P.working_snapshot(self.root)

    def test_main_refuses_git_failure_without_success_output(self):
        output = io.StringIO()
        with mock.patch.object(P, 'run_git', side_effect=P.HistoryRefused('injected read failure')), \
                mock.patch.object(sys, 'argv', ['history_predecessor.py']), redirect_stdout(output):
            rc = P.main()
        self.assertEqual(rc, 2)
        self.assertIn('REFUSED', output.getvalue())
        self.assertNotIn(': ok', output.getvalue())

    def test_guard_import_performs_no_git_reads(self):
        code = '''from unittest import mock
import subprocess, sys
sys.path.insert(0, 'scripts')
with mock.patch.object(subprocess, 'run', side_effect=RuntimeError('unexpected Git read')):
    import history_predecessor
'''
        result = subprocess.run([sys.executable, '-c', code], cwd=P.ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIs(SH.split_entries, P.S.split_entries)
        self.assertEqual(SH.SHARD_HEADER, P.S.SHARD_HEADER)

    def test_main_checks_bad_index_despite_good_working_bytes(self):
        self.current['DEV_NOTES.md'] = self.current['DEV_NOTES.md'].replace(b'Focused11', b'Focused12')
        output = io.StringIO()
        with mock.patch.object(P, 'git_snapshot', side_effect=[self.previous, self.current]), \
                mock.patch.object(P, 'working_snapshot', return_value=self.previous), \
                mock.patch.object(sys, 'argv', ['history_predecessor.py']), redirect_stdout(output):
            rc = P.main()
        self.assertEqual(rc, 1)
        self.assertIn('changed', output.getvalue())
        self.assertNotIn(': ok', output.getvalue())

    def test_main_checks_bad_working_bytes_despite_good_index(self):
        self.current['DEV_NOTES.md'] = self.current['DEV_NOTES.md'].replace(b'Focused11', b'Focused12')
        output = io.StringIO()
        with mock.patch.object(P, 'git_snapshot', return_value=self.previous), \
                mock.patch.object(P, 'working_snapshot', return_value=self.current), \
                mock.patch.object(sys, 'argv', ['history_predecessor.py']), redirect_stdout(output):
            rc = P.main()
        self.assertEqual(rc, 1)
        self.assertIn('changed', output.getvalue())
        self.assertNotIn(': ok', output.getvalue())

    def test_published_sharder_integration_and_snapshot_cleanup(self):
        for name, blob in self.previous.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
        registry = self.root / 'doctrine/readme_routes.tsv'
        registry.parent.mkdir()
        registry.write_text('DEV_NOTES.md\tauthor_overflow\tappend_history\towner\t0\t0\t0\t49152\t0\n')
        preamble, records = self.split()
        target = len(preamble + records[0][1])
        SH.shard(self.root, 'DEV_NOTES.md', 'docs/changelog', P.H.MANIFEST, target, CEILINGS['DEV_NOTES.md'])
        self.assertEqual(P.verify(self.previous, P.working_snapshot(self.root), CEILINGS), (2, 4))
        self.assertEqual(P.working_snapshot(self.root)['DEV_NOTES.md'] +
                         P.entries(P.working_snapshot(self.root)['docs/changelog/shard-0002.md'])[1][0][1],
                         self.previous['DEV_NOTES.md'])



def main():
    global P
    args = sys.argv[1:]
    if args:
        if len(args) != 2 or args[0] != '--mutation':
            raise SystemExit('usage: probe_history_predecessor.py [--mutation no-predecessor|no-order|no-staged-partition|ignore-git-error|no-shard-wrapper]')
        mode = args[1]
        if mode == 'no-predecessor':
            P.verify = lambda previous, *args: (sum(head in previous for head in P.HEADS),
                                                 sum(len(P.entries(previous[head])[1]) for head in P.HEADS if head in previous))
        elif mode == 'no-staged-partition':
            P.judge_index = lambda *args: None
        else:
            source = Path(P.__file__).read_text()
            replacements = {
                'no-order': ('logical[-len(old_entries):] != old_entries', 'set(logical[-len(old_entries):]) != set(old_entries)'),
                'ignore-git-error': ('if result.returncode:', 'if False:'),
                'no-shard-wrapper': ('if preamble != wrapper:', 'if False:'),
            }
            if mode not in replacements:
                raise SystemExit('unknown mutation ' + mode)
            before, after = replacements[mode]
            if source.count(before) != 1:
                raise SystemExit('mutation seam drift')
            mutant = types.ModuleType('history_predecessor_mutant')
            mutant.__file__ = P.__file__
            source = source.replace(before, after, 1)
            exec(compile(source, mutant.__file__, 'exec'), mutant.__dict__)
            P = mutant
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PredecessorTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
