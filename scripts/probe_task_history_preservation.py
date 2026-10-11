#!/usr/bin/env python3
"""Independent publishing controls; fixtures never create another Git repository."""
from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import task_history_preservation as G

ROOT = Path(__file__).resolve().parent.parent
NAME = 'docs/tasks/archive/P4-SYSTEM-18.md'
OTHER = 'docs/tasks/archive/P0-PROFILE.md'
BODY = b'# retained history\n3196 links/normal+print\n'


def oid(body):
    return hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest().encode()


class Backend:
    """Emit real Git wire formats from independent literal snapshots."""

    def __init__(self, previous):
        self.previous = dict(previous)
        self.proposed = dict(previous)
        self.objects = {}
        self.damage = ''
        self.head_reads = 0
        self.head_width = 40

    def __call__(self, root, *arguments, data=None):
        if arguments == ('rev-parse', '--verify', 'HEAD'):
            self.head_reads += 1
            return (b'2' if self.damage == 'head-change' and self.head_reads > 1 else b'1') * self.head_width + b'\n'
        if arguments[0] in {'ls-tree', 'ls-files'}:
            staged = arguments[0] == 'ls-files'
            source = self.proposed if staged else self.previous
            rows = []
            for name, (mode, body) in source.items():
                identity = oid(body)
                self.objects[identity] = body
                metadata = (mode.encode() + b' ' + identity + b' 0' if staged else
                            mode.encode() + b' blob ' + identity)
                rows.append(metadata + b'\t' + name.encode() + b'\0')
            result = b''.join(rows)
            if self.damage == 'inventory-tail':
                return result[:-1]
            if self.damage == 'inventory-row':
                return b'not an inventory row\0'
            if self.damage == 'duplicate':
                return result + rows[0]
            if self.damage == 'unmerged' and staged:
                return result.replace(b' 0\t', b' 2\t', 1)
            if self.damage == 'non-utf8':
                return result.replace(NAME.encode(), b'\xff', 1)
            return result
        if arguments == ('cat-file', '--batch-check'):
            result = b''.join(identity + b' blob ' + str(len(self.objects[identity])).encode() + b'\n'
                              for identity in data.splitlines())
            if self.damage == 'size-missing':
                return b''
            if self.damage == 'size-tail':
                return result[:-1]
            if self.damage == 'size-kind':
                return result.replace(b' blob ', b' tree ', 1)
            return result
        if arguments == ('cat-file', '--batch'):
            result = b''.join(identity + b' blob ' + str(len(self.objects[identity])).encode() +
                              b'\n' + self.objects[identity] + b'\n' for identity in data.splitlines())
            if self.damage == 'blob-tail':
                return result + b'extra'
            if self.damage == 'blob-truncated':
                return result[:-2]
            if self.damage == 'blob-identity':
                return result.replace(BODY, BODY.replace(b'3196', b'3197'), 1)
            return result
        raise AssertionError('unhandled fixture Git request ' + repr(arguments))


class Preservation(unittest.TestCase):
    work: Path
    guard = G

    def setUp(self):
        self.fixture = tempfile.TemporaryDirectory(prefix='case-', dir=self.work)
        self.addCleanup(self.fixture.cleanup)
        self.root = Path(self.fixture.name)
        self.previous = {NAME: ('100644', BODY), OTHER: ('100644', b'# older record\n')}
        for name, (_, body) in self.previous.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            path.chmod(0o644)
        self.backend = Backend(self.previous)
        self.original_read = self.guard.git_read
        patch = mock.patch.object(self.guard, 'git_read', self.backend)
        patch.start()
        self.addCleanup(patch.stop)

    def check(self):
        return self.guard.check(self.root)

    def changed(self, view):
        with self.assertRaisesRegex(self.guard.Changed, view + ':.*' + NAME):
            self.check()

    def refused(self, reason):
        with self.assertRaisesRegex(self.guard.Refused, reason):
            self.check()

    def test_unchanged_both_views(self):
        self.assertEqual(self.check(), (2, len(BODY) + len(self.previous[OTHER][1])))

    def test_new_archive_is_permitted(self):
        self.backend.proposed['docs/tasks/archive/new.md'] = ('100644', b'# new record\n')
        self.assertEqual(self.check()[0], 2)

    def test_sha256_git_objects(self):
        self.backend.head_width = 64

        def sha256_oid(body):
            return hashlib.sha256(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest().encode()

        with mock.patch(__name__ + '.oid', sha256_oid):
            self.assertEqual(self.check(), (2, len(BODY) + len(self.previous[OTHER][1])))

    def test_altered_index_with_original_working_file(self):
        self.backend.proposed[NAME] = ('100644', BODY.replace(b'3196', b'3197'))
        self.changed('index')

    def test_altered_working_with_original_index(self):
        (self.root / NAME).write_bytes(BODY.replace(b'3196', b'3197'))
        self.changed('working')

    def test_removed_index_file(self):
        del self.backend.proposed[NAME]
        self.changed('index')

    def test_removed_working_file(self):
        (self.root / NAME).unlink()
        self.changed('working')

    def test_changed_index_mode(self):
        self.backend.proposed[NAME] = ('100755', BODY)
        self.changed('index')

    def test_changed_working_mode(self):
        (self.root / NAME).chmod(0o755)
        self.changed('working')

    def test_changed_receipt_with_updated_declared_digest(self):
        original = BODY + hashlib.sha256(BODY).hexdigest().encode() + b'\n'
        replacement = BODY.replace(b'3196', b'3197')
        changed = replacement + hashlib.sha256(replacement).hexdigest().encode() + b'\n'
        self.backend.previous[NAME] = ('100644', original)
        self.backend.proposed[NAME] = ('100644', changed)
        (self.root / NAME).write_bytes(original)
        self.changed('index')

    def test_empty_baseline_refuses(self):
        self.backend.previous.clear()
        self.refused('empty published archive inventory')

    def test_empty_index_cannot_hide_deletion(self):
        self.backend.proposed.clear()
        self.changed('index')

    def test_incomplete_inventory_refuses(self):
        self.backend.damage = 'inventory-tail'
        self.refused('incomplete archive inventory')

    def test_malformed_inventory_row_refuses(self):
        self.backend.damage = 'inventory-row'
        self.refused('malformed archive inventory row')

    def test_duplicate_inventory_refuses(self):
        self.backend.damage = 'duplicate'
        self.refused('unsafe/duplicate archive identity')

    def test_unmerged_index_refuses(self):
        self.backend.damage = 'unmerged'
        self.refused('unmerged archive path')

    def test_symlink_index_refuses(self):
        self.backend.proposed[NAME] = ('120000', BODY)
        self.refused('unsafe/duplicate archive identity')

    def test_gitlink_index_refuses(self):
        self.backend.proposed[NAME] = ('160000', BODY)
        self.refused('unsafe/duplicate archive identity')

    def test_escaping_inventory_path_refuses(self):
        self.backend.previous['docs/tasks/archive/../escape.md'] = ('100644', BODY)
        self.refused('unsafe archive path')

    def test_non_utf8_inventory_refuses(self):
        self.backend.damage = 'non-utf8'
        self.refused('non-UTF-8 archive path')

    def test_missing_sizes_refuse(self):
        self.backend.damage = 'size-missing'
        self.refused('incomplete archive size response')

    def test_incomplete_size_framing_refuses(self):
        self.backend.damage = 'size-tail'
        self.refused('incomplete archive size response')

    def test_non_blob_size_refuses(self):
        self.backend.damage = 'size-kind'
        self.refused('invalid archive blob size')

    def test_wrong_blob_identity_refuses(self):
        self.backend.damage = 'blob-identity'
        with self.assertRaisesRegex(self.guard.Refused, 'archive object identity differs'):
            self.guard.git_snapshot(self.root)

    def test_truncated_blob_refuses(self):
        self.backend.damage = 'blob-truncated'
        self.refused('incomplete archive blob')

    def test_surplus_blob_refuses(self):
        self.backend.damage = 'blob-tail'
        self.refused('surplus archive blob response')

    def test_oversized_blob_refuses_before_read(self):
        self.backend.previous[NAME] = ('100644', b'x' * (128 * 1024 + 1))
        self.refused('archive blob exceeds file bound')

    def test_excess_inventory_refuses(self):
        self.backend.previous = {f'docs/tasks/archive/{i}.md': ('100644', BODY) for i in range(97)}
        self.refused('archive inventory exceeds file bound')

    def test_aggregate_size_refuses_before_read(self):
        self.backend.previous = {f'docs/tasks/archive/{i}.md': ('100644', b'x' * (128 * 1024)) for i in range(25)}
        self.refused('archive snapshot exceeds byte bound')

    def test_working_symlink_refuses(self):
        path = self.root / NAME
        path.unlink()
        path.symlink_to(self.root / OTHER)
        self.refused('symlink in archive path')

    def test_parent_symlink_refuses(self):
        parent = self.root / 'docs/tasks/archive'
        parent.rename(self.root / 'retained')
        parent.symlink_to(self.root / 'retained', target_is_directory=True)
        self.refused('symlink in archive path')

    def test_nested_git_marker_refuses(self):
        (self.root / 'docs/tasks/.git').mkdir()
        self.refused('Git boundary in archive path')

    def test_nonregular_working_file_refuses(self):
        path = self.root / NAME
        path.unlink()
        path.mkdir()
        self.refused('nonregular working archive')

    def test_off_volume_identity_refuses(self):
        original = Path.lstat
        target = self.root / 'docs/tasks/archive'

        def other_device(path):
            identity = original(path)
            if path == target:
                values = list(identity)
                values[2] += 1
                return type(identity)(values)
            return identity

        with mock.patch.object(Path, 'lstat', other_device):
            self.refused('off-volume archive path')

    def test_published_head_change_refuses(self):
        self.backend.damage = 'head-change'
        self.refused('published HEAD changed during check')

    def test_git_status_failure_with_partial_stdout_refuses(self):
        result = subprocess.CompletedProcess(['git'], 73, stdout=b'partial', stderr=b'')
        with mock.patch.object(self.guard.subprocess, 'run', return_value=result):
            with self.assertRaisesRegex(self.guard.Refused, 'Git read failed.*ls-tree'):
                self.original_read(self.root, 'ls-tree', 'HEAD')

    def test_git_stderr_with_success_refuses(self):
        result = subprocess.CompletedProcess(['git'], 0, stdout=b'partial', stderr=b'fixture denied')
        with mock.patch.object(self.guard.subprocess, 'run', return_value=result):
            with self.assertRaisesRegex(self.guard.Refused, 'Git read failed.*fixture denied'):
                self.original_read(self.root, 'ls-tree', 'HEAD')

    def test_git_success_preserves_output_and_request(self):
        result = subprocess.CompletedProcess(['git'], 0, stdout=b'wire\n', stderr=b'')
        with mock.patch.object(self.guard.subprocess, 'run', return_value=result) as run:
            self.assertEqual(self.original_read(self.root, 'cat-file', '--batch', data=b'oid\n'), b'wire\n')
            arguments = run.call_args
            self.assertEqual(arguments.args[0], ['git', '--no-pager', '--no-optional-locks',
                                               '--no-replace-objects', '-C', str(self.root),
                                               'cat-file', '--batch'])
            self.assertEqual(arguments.kwargs['input'], b'oid\n')
            self.assertTrue(arguments.kwargs['capture_output'])

    def cli(self):
        output = io.StringIO()
        with mock.patch.object(self.guard, 'ROOT', self.root), redirect_stdout(output):
            code = self.guard.main([])
        return code, output.getvalue()

    def test_public_cli_green(self):
        code, output = self.cli()
        self.assertEqual(code, 0)
        self.assertIn('2 published files', output)
        self.assertIn('index/working exact', output)

    def test_public_cli_changed(self):
        self.backend.proposed[NAME] = ('100644', BODY + b'changed\n')
        code, output = self.cli()
        self.assertEqual(code, 1)
        self.assertIn('changed — index: published archive changed ' + NAME, output)

    def test_public_cli_refuses_invalid_head(self):
        with mock.patch.object(self.guard, 'git_read', return_value=b''):
            code, output = self.cli()
        self.assertEqual(code, 2)
        self.assertIn('REFUSED — invalid published HEAD identity', output)

    def test_public_cli_refuses_missing_git(self):
        with mock.patch.object(self.guard, 'git_read', self.original_read), \
                mock.patch.object(self.guard.subprocess, 'run', side_effect=FileNotFoundError('fixture missing Git')):
            code, output = self.cli()
        self.assertEqual(code, 2)
        self.assertIn('REFUSED — fixture missing Git', output)

    def test_public_cli_refuses_timeout(self):
        with mock.patch.object(self.guard, 'git_read', self.original_read), \
                mock.patch.object(self.guard.subprocess, 'run', side_effect=subprocess.TimeoutExpired('git', 30)):
            code, output = self.cli()
        self.assertEqual(code, 2)
        self.assertIn('REFUSED', output)


MUTATIONS = {
    'index': ("verify(previous, proposed, 'index')", '# omitted index comparison'),
    'working': ("counts = verify(previous, working_snapshot(root, previous), 'working')",
                'counts = (len(previous), sum(len(body) for _, body in previous.values()))'),
    'mode': ('if current.get(name) != identity:',
             'if current.get(name) is None or current[name][1] != identity[1]:'),
    'read-status': ('result.returncode == 0 and not result.stderr', 'not result.stderr'),
    'read-stderr': ('result.returncode == 0 and not result.stderr', 'result.returncode == 0'),
    'empty-baseline': ("require(staged or bool(inventory), 'empty published archive inventory')",
                       '# omitted empty baseline check'),
    'blob-identity': ("require(actual.encode('ascii') == oid, 'archive object identity differs ' + name)",
                      '# omitted blob identity check'),
    'blob-tail': ("require(cursor == len(stream), 'surplus archive blob response')",
                  '# omitted surplus output check'),
    'inventory-frame': ("require(not inventory or inventory.endswith(b'\\0'), 'incomplete archive inventory')",
                        '# omitted inventory framing check'),
}


def work_parent():
    parent = ROOT
    for part in ('target', 'task-preservation-probe'):
        parent /= part
        if parent.is_symlink():
            raise ValueError('symlink in probe output path')
        if parent.exists():
            if not parent.is_dir() or parent.stat().st_dev != ROOT.stat().st_dev:
                raise ValueError('probe output is not an on-volume directory')
        else:
            parent.mkdir()
    return parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', choices=sorted(MUTATIONS))
    arguments = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='run-', dir=work_parent()) as directory:
        Preservation.work = Path(directory)
        if arguments.mutation:
            source = (ROOT / 'scripts/task_history_preservation.py').read_text()
            before, after = MUTATIONS[arguments.mutation]
            if source.count(before) != 1:
                raise ValueError('mutation seam is not unique: ' + arguments.mutation)
            candidate = Preservation.work / 'candidate.py'
            candidate.write_text(source.replace(before, after, 1))
            spec = importlib.util.spec_from_file_location('task_preservation_candidate', candidate)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            Preservation.guard = module
        result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Preservation))
        print(f'TASK-PRESERVATION-PROBE: {result.testsRun} tests / '
              f'{len(result.failures)} failures / {len(result.errors)} errors')
        return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print('TASK-PRESERVATION-PROBE: REFUSED — ' + str(error))
        raise SystemExit(2)
