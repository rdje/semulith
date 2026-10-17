#!/usr/bin/env python3
"""Finite adversarial reader/publishing controls; fixtures stay below target/."""
from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import types
import unittest
from unittest.mock import patch

import qualification_history_archive as A
import qualification_history_preservation as P
from check_task_history_links import check_links


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def pack(items, row, special=None):
    """Independent USTAR producer; deliberately not the reader's encoder."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name, body in items:
            entry = tarfile.TarInfo(name)
            entry.size, entry.mode = len(body), 0o644
            if special:
                special(entry)
            archive.addfile(entry, io.BytesIO(body))
    raw = buffer.getvalue()
    blob = gzip.compress(raw, mtime=0)
    row.update(sha256=A.digest(blob), compressed_bytes=len(blob), tar_bytes=len(raw))
    return blob


class Controls(unittest.TestCase):
    root = A.PROJECT

    @classmethod
    def setUpClass(cls):
        cls.row, cls.originals = A.load_terminal(cls.root)
        cls.files = {n: A.read_file(cls.root, n, A.MAX_OBJECT_BYTES)
                     for n in [A.INDEX, A.FRONT, cls.row['object'], *A.RETIRED]}
        cls.wiring = {n: ('100644', n.encode()) for n in P.WIRING}
        cls.before = {n: ('100644', cls.originals[n]) for n in A.RETIRED}
        cls.before_wiring = {n: v for n, v in cls.wiring.items()
                             if n not in P.WIRING[:3]}
        (A.PROJECT / 'target/qualification-history-probes').mkdir(parents=True, exist_ok=True)

    def fixture(self):
        context = tempfile.TemporaryDirectory(dir=A.PROJECT / 'target/qualification-history-probes')
        self.addCleanup(context.cleanup)
        root = Path(context.name)
        for name, (mode, body) in self.files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            path.chmod(0o644)
        return root

    def refuse(self, callable_, reason):
        with self.assertRaisesRegex(A.ArchiveRefused, reason):
            callable_()

    def judge(self, previous=None, proposed=None, working=None, wp=None):
        return P.judge(self.files if previous is None else previous,
                       self.files if proposed is None else proposed,
                       self.files if working is None else working,
                       self.wiring, self.wiring if wp is None else wp, self.wiring)

    def test_relocated_public_reads_and_tar(self):
        root = self.fixture()
        scripts = root / 'scripts'
        scripts.mkdir()
        for name in ['qualification_history_archive.py', 'task_history_archive.py']:
            (scripts / name).write_bytes((A.PROJECT / 'scripts' / name).read_bytes())
        work = root / 'unrelated'
        work.mkdir()
        census = lambda: {p.relative_to(root).as_posix(): p.read_bytes()
                          for p in root.rglob('*') if p.is_file()}
        before = census()
        reader = scripts / 'qualification_history_archive.py'
        tar = shutil.which('tar')
        self.assertIsNotNone(tar)
        options = ['-O'] if sys.flags.optimize else []
        environment = {'PATH': '', 'PYTHONDONTWRITEBYTECODE': '1'}
        for name in A.PATHS:
            result = subprocess.run([sys.executable, *options, str(reader), '--read', name],
                                    cwd=work, env=environment, capture_output=True)
            other = subprocess.run([tar, '-xOf', str(root / self.row['object']), name],
                                   capture_output=True)
            self.assertEqual((result.returncode, other.returncode), (0, 0))
            self.assertEqual(result.stdout, self.originals[name])
            self.assertEqual(other.stdout, self.originals[name])
            self.assertEqual(result.stderr, b'')
        listing = subprocess.run([sys.executable, *options, str(reader), '--list'],
                                 cwd=work, env=environment, capture_output=True)
        self.assertEqual(listing.returncode, 0)
        self.assertEqual(listing.stdout, ('\n'.join(A.PATHS) + '\n').encode())
        self.assertEqual(before, census())
        self.assertFalse((root / '.git').exists())

    def test_public_unknown_and_corrupt_read_no_output(self):
        root = self.fixture()
        for name in ['../outside', A.PATHS[0]]:
            if name == A.PATHS[0]:
                (root / self.row['object']).write_bytes(b'damaged')
            options = ['-O'] if sys.flags.optimize else []
            result = subprocess.run([sys.executable, *options,
                                     str(A.PROJECT / 'scripts/qualification_history_archive.py'),
                                     '--root', str(root), '--read', name], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, b'')
            self.assertIn(b'QUALIFICATION-HISTORY: REFUSED', result.stderr)
            self.assertNotIn(b'Traceback', result.stderr)

    def test_descriptor_pin_is_discriminating(self):
        changed = copy.deepcopy(self.row)
        changed['recorded_on'] = '2026-10-15'
        files = dict(self.files, **{A.INDEX: ('100644', encode(changed))})
        self.refuse(lambda: A.validate_view(files), 'descriptor identity differs')

    def test_first_publication_and_unstaged_preparation(self):
        birth = P.judge(self.before, self.files, self.files, self.before_wiring,
                        self.wiring, self.wiring)[2]
        self.assertTrue(birth)
        self.assertTrue(P.judge(self.before, self.before, self.files, self.before_wiring,
                               self.before_wiring, self.wiring)[2])
        self.assertFalse(self.judge()[2])

    def test_partial_data_publication(self):
        partial = dict(self.files)
        partial.pop(A.FRONT)
        self.refuse(lambda: P.judge(self.before, partial, self.files,
                                   self.before_wiring, self.wiring, self.wiring), 'view coverage')

    def test_wiring_only_publication(self):
        self.refuse(lambda: P.judge(self.before, self.before, self.files,
                                   self.before_wiring, self.wiring, self.wiring), 'descriptor unavailable')

    def test_missing_first_publication_wiring(self):
        partial = dict(self.wiring)
        partial.pop(P.WIRING[0])
        self.refuse(lambda: P.judge(self.before, self.files, self.files,
                                   self.before_wiring, partial, self.wiring), 'wiring incomplete')

    def test_published_index_independent_from_working(self):
        changed = dict(self.files)
        changed[A.FRONT] = ('100644', b'changed')
        self.refuse(lambda: self.judge(proposed=changed), 'index changed')

    def test_published_working_independent_from_index(self):
        changed = dict(self.files)
        changed[A.FRONT] = ('100644', b'changed')
        # README prose is bounded during retrieval; publication freezes it.
        self.assertEqual(A.validate_view(changed)[1], self.originals)
        self.refuse(lambda: self.judge(working=changed), 'working view changed')

    def test_source_provenance_bytes_modes_and_tree(self):
        source = {n: ('100644', b) for n, b in self.originals.items()}
        digest = self.row['source_tree_sha256']
        P.source_check(self.row, self.originals, source, digest)
        self.refuse(lambda: P.source_check(self.row, self.originals, source, '0' * 64), 'tree differs')
        self.refuse(lambda: P.source_check(self.row, self.originals, {}, digest), 'coverage differs')
        for mode, body in [('100755', self.originals[A.PATHS[0]]), ('100644', b'changed')]:
            changed = dict(source, **{A.PATHS[0]: (mode, body)})
            self.refuse(lambda: P.source_check(self.row, self.originals, changed, digest), 'bytes/mode differ')

    def test_git_transport_no_lazy_fetch_and_failures(self):
        success = subprocess.CompletedProcess([], 0, b'green', b'')
        with patch.object(P.subprocess, 'run', return_value=success) as run:
            self.assertEqual(P.git_read(A.PROJECT, 'read'), b'green')
            self.assertEqual(run.call_args.kwargs['env']['GIT_NO_LAZY_FETCH'], '1')
        for result in [subprocess.CompletedProcess([], 1, b'', b''),
                       subprocess.CompletedProcess([], 0, b'partial', b'diagnostic')]:
            with patch.object(P.subprocess, 'run', return_value=result):
                self.refuse(lambda: P.git_read(A.PROJECT, 'read'), 'Git read unavailable')
        with patch.object(P, 'git_read', return_value=b'incomplete'):
            self.refuse(lambda: P.snapshot(A.PROJECT, 'HEAD', A.PATHS), 'inventory')

    def test_all_heading_links_and_live_include_refusal(self):
        aliases = {e['original_path']: e['anchors'] for e in self.row['members'] if e['original_path'] in A.RETIRED}
        row = {'anchors': aliases}
        originals = {n: self.originals[n] for n in A.RETIRED}
        count = 0
        for name, anchors in aliases.items():
            for anchor in anchors:
                source = {A.BOOK: f'[record]({name}#{anchor})'.encode()}
                count += check_links(A.PROJECT, source, row, originals)
            self.refuse(lambda: check_links(A.PROJECT, {A.BOOK: f'[bad]({name}#lost)'.encode()},
                                           row, originals), 'unretained history link anchor')
            self.refuse(lambda: check_links(A.PROJECT, {A.BOOK: ('{{#include ' + name + '}}').encode()},
                                           row, originals), 'sealed narrative used as live include')
        self.assertEqual(count, 20)

    def test_inner_corruption_with_consistent_outer_identity(self):
        baseline = dict(self.originals)
        manifest = {'schema_version': 1, 'kind': 'qualification-history-source',
                    'source': self.row['source'], 'source_tree_sha256': self.row['source_tree_sha256'],
                    'members': self.row['members']}
        for case, reason in [('member', 'original qualification identity'),
                             ('git-oid', 'Git blob identity'), ('manifest', 'manifest identity'),
                             ('source-bytes', 'source bytes'), ('source-lines', 'source lines'),
                             ('missing', 'member order/census'), ('duplicate', 'duplicate qualification'),
                             ('extra', 'unknown or unsafe'), ('unsafe', 'unknown or unsafe'),
                             ('noncanonical', 'noncanonical qualification tar')]:
            with self.subTest(case=case):
                row, data = copy.deepcopy(self.row), dict(baseline)
                if case == 'member':
                    data[A.PATHS[0]] += b'changed'
                if case == 'git-oid':
                    row['members'][0]['git_oid'] = '0' * 40
                original_manifest = copy.deepcopy(manifest)
                original_manifest['members'] = row['members']
                body = encode(original_manifest)
                row.update(manifest_bytes=len(body), manifest_sha256=A.digest(body))
                data[A.MANIFEST] = body
                if case == 'manifest':
                    data[A.MANIFEST] = body.replace(b'qualification-history-source', b'qualification-history-damage')
                if case in ('source-bytes', 'source-lines'):
                    row[case.replace('-', '_')] += 1
                if case == 'missing':
                    data.pop(A.PATHS[0])
                items = list(data.items())
                if case == 'duplicate':
                    items.append(items[0])
                if case in ('extra', 'unsafe'):
                    items.append(('extra' if case == 'extra' else '../outside', b'bad'))
                special = (lambda entry: setattr(entry, 'uid', 1)) if case == 'noncanonical' else None
                blob = pack(items, row, special)
                self.refuse(lambda: A.inspect_object(blob, row), reason)

    def test_bad_deflate_named_refusal(self):
        row = copy.deepcopy(self.row)
        blob = b'\x1f\x8b\x08\x00' + b'\0' * 6 + b'\x07' + b'\0' * 8
        row.update(sha256=A.digest(blob), compressed_bytes=len(blob))
        self.refuse(lambda: A.inspect_object(blob, row), 'unreadable qualification object')

    def test_expansion_bound(self):
        row = copy.deepcopy(self.row)
        row['tar_bytes'] = 1024
        self.refuse(lambda: A.inspect_object(self.files[row['object']][1], row), 'expansion differs')

    def test_actual_single_guard_omissions(self):
        """Six independently discriminating guards, changed in owned copies only."""
        changed_front = dict(self.files, **{A.FRONT: ('100644', b'changed')})
        source = {n: ('100644', b) for n, b in self.originals.items()}
        changed_source = dict(source, **{A.PATHS[0]: ('100755', self.originals[A.PATHS[0]])})
        row = copy.deepcopy(self.row)
        row['recorded_on'] = '2026-10-15'
        changed_index = dict(self.files, **{A.INDEX: ('100644', encode(row))})
        changed_stub = dict(self.files, **{A.RETIRED[0]: ('100644', b'changed')})
        cases = [
            (P, 'published qualification index changed',
             lambda m: m.judge(self.files, changed_front, self.files,
                               self.wiring, self.wiring, self.wiring)),
            (P, 'published qualification working view changed',
             lambda m: m.judge(self.files, self.files, changed_front,
                               self.wiring, self.wiring, self.wiring)),
            (P, 'qualification source tree differs',
             lambda m: m.source_check(self.row, self.originals, source, '0' * 64)),
            (P, 'qualification original source bytes/mode differ: ',
             lambda m: m.source_check(self.row, self.originals, changed_source,
                                       self.row['source_tree_sha256'])),
            (A, 'captured qualification descriptor identity differs',
             lambda m: m.validate_view(changed_index)),
            (A, 'qualification navigation differs: ', lambda m: m.validate_view(changed_stub)),
        ]
        for module, reason, invoke in cases:
            with self.subTest(guard=reason):
                self.refuse(lambda: invoke(module), reason)
                source_code = Path(module.__file__).read_text()
                statements = [n for n in ast.walk(ast.parse(source_code))
                              if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                              and any(isinstance(v, ast.Constant) and v.value == reason
                                      for argument in n.value.args for v in ast.walk(argument))]
                self.assertEqual(len(statements), 1)
                statement = statements[0]
                lines = source_code.splitlines(keepends=True)
                lines[statement.lineno - 1:statement.end_lineno] = [' ' * statement.col_offset + 'pass\n']
                namespace = {'__file__': module.__file__, '__name__': 'owned_guard_omission'}
                exec(compile(''.join(lines), 'owned_guard_omission', 'exec'), namespace)
                invoke(types.SimpleNamespace(**namespace))


def descriptor_case(case):
    def test(self):
        row = copy.deepcopy(self.row)
        if case == 'unknown': row['unknown'] = 1
        elif case == 'bool': row['source_files'] = True
        elif case == 'string': row['source_files'] = '5'
        elif case == 'object': row['object'] = '../outside'
        elif case == 'date': row['recorded_on'] = '2026-99-99'
        elif case == 'anchors': row['members'][1]['anchors'] = ['bad space']
        elif case == 'role': row['members'][0]['role'] = 'qualification'
        self.refuse(lambda: A.parse_descriptor(encode(row)),
                    {'unknown': 'unknown qualification descriptor', 'bool': 'count exceeds',
                     'string': 'count exceeds', 'object': 'unsafe qualification object',
                     'date': 'invalid archive record date', 'anchors': 'heading aliases',
                     'role': 'unknown qualification member role'}[case])
    return test


def filesystem_case(case):
    def test(self):
        root = self.fixture()
        obj, stub = root / self.row['object'], root / A.RETIRED[0]
        if case == 'missing': obj.unlink()
        elif case == 'digest': obj.write_bytes(b'changed')
        elif case == 'stub': stub.write_bytes(b'changed')
        elif case == 'mode': stub.chmod(0o755)
        elif case == 'extra': (root / 'docs/qualification-history/extra').write_bytes(b'extra')
        elif case == 'directory': (root / 'docs/qualification-history/extra').mkdir()
        elif case == 'symlink': obj.unlink(); obj.symlink_to(self.root / self.row['object'])
        elif case == 'nested-git': (root / 'docs/.git').write_bytes(b'gitdir: elsewhere')
        elif case == 'front-bound': (root / A.FRONT).write_bytes(b'x' * (A.MAX_FRONT_BYTES + 1))
        self.refuse(lambda: A.load_terminal(root),
                    {'missing': 'coverage differs', 'digest': 'object identity differs',
                     'stub': 'navigation differs', 'mode': 'Git mode differs',
                     'extra': 'coverage differs', 'directory': 'unknown qualification directory',
                     'symlink': 'symlink', 'nested-git': 'Git boundary',
                     'front-bound': 'exceeds bound'}[case])
    return test


for name in ['unknown', 'bool', 'string', 'object', 'date', 'anchors', 'role']:
    setattr(Controls, 'test_descriptor_' + name, descriptor_case(name))
for name in ['missing', 'digest', 'stub', 'mode', 'extra', 'directory', 'symlink', 'nested-git', 'front-bound']:
    setattr(Controls, 'test_filesystem_' + name, filesystem_case(name))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=A.PROJECT)
    args = parser.parse_args()
    Controls.root = A.owned_root(args.root)
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    print(f'QUALIFICATION-HISTORY-PROBE: {result.testsRun} tests / '
          f'{len(result.failures)} failures / {len(result.errors)} errors')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
