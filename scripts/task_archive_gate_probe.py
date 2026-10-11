#!/usr/bin/env python3
"""Measure the real doctrine gate against one isolated ordinary-history edit.

The real index and working files must remain exact. A scoped Git facade exposes
the proposed index only to reads of this checkout; child test repos keep theirs.
Exit 0 means the measurement completed; gate_rc in result.json is the gate verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
PREFIX = 'SEMULITH_ARCHIVE_PROBE_'
READS = {'diff', 'diff-index', 'diff-files', 'ls-files', 'ls-tree', 'show',
         'status', 'grep', 'cat-file', 'check-attr', 'check-ignore', 'rev-parse'}
VALUES = {'-C', '-c', '--git-dir', '--work-tree', '--namespace', '--config-env'}
FLAGS = {'--no-pager', '-P', '--paginate', '-p', '--bare', '--no-optional-locks',
         '--literal-pathspecs', '--no-literal-pathspecs', '--glob-pathspecs',
         '--noglob-pathspecs', '--icase-pathspecs', '--no-replace-objects'}


class Refused(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise Refused(reason)


def git_prefix(arguments):
    offset = 0
    while offset < len(arguments) and arguments[offset].startswith('-'):
        option = arguments[offset]
        if option in VALUES:
            require(offset + 1 < len(arguments), 'missing global Git option value')
            offset += 2
        elif option in FLAGS or any(option.startswith(name + '=') for name in VALUES
                                    if name.startswith('--')):
            offset += 1
        elif option in {'--version', '--help', '-h'} and offset == len(arguments) - 1:
            return arguments, None
        else:
            raise Refused('unhandled global Git option: ' + option)
    return arguments[:offset], arguments[offset] if offset < len(arguments) else None


def trace(path, row):
    data = (json.dumps(row, sort_keys=True) + '\n').encode()
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        require(os.write(descriptor, data) == len(data), 'short facade trace write')
    finally:
        os.close(descriptor)


def facade(arguments):
    backend = os.environ[PREFIX + 'GIT']
    expected = Path(os.environ[PREFIX + 'GIT_DIR']).resolve()
    proposed = os.environ[PREFIX + 'INDEX']
    log = os.environ[PREFIX + 'LOG']
    mutation = os.environ.get(PREFIX + 'MUTATION', '')
    environment = dict(os.environ)
    environment.pop('GIT_INDEX_FILE', None)
    environment['GIT_OPTIONAL_LOCKS'] = '0'
    row = {'arguments': arguments, 'injected': False}
    try:
        prefix, command = git_prefix(arguments)
        if command in READS:
            context = subprocess.run([backend, *prefix, 'rev-parse', '--absolute-git-dir'],
                                     env=environment, capture_output=True, text=True)
            valid = (context.returncode == 0 and not context.stderr
                     and bool(context.stdout.strip())
                     and len(context.stdout.splitlines()) == 1
                     and Path(context.stdout.strip()).is_absolute())
            require(valid or mutation == 'discovery', 'cannot identify Git index owner')
            actual = Path(context.stdout.strip()).resolve()
            row['git_dir'] = str(actual)
            if (actual == expected or mutation == 'unscoped') and mutation != 'missing':
                environment['GIT_INDEX_FILE'] = proposed
                row['injected'] = True
        trace(log, row)
        os.execve(backend, [backend, *arguments], environment)
    except (Refused, OSError, subprocess.SubprocessError) as error:
        row['refused'] = str(error)
        trace(log, row)
        print('ARCHIVE-GATE-PROBE: ' + str(error), file=sys.stderr)
        return 2


FAKE_GIT = '''#!/usr/bin/env python3
import json, os, pathlib, sys
root = pathlib.Path(__file__).resolve().parent
case = json.loads((root / 'case.json').read_text())
args = sys.argv[1:]
if args[-2:] == ['rev-parse', '--absolute-git-dir']:
    foreign = '-C' in args
    path = root / ('foreign.git' if foreign else 'main.git')
    mode = case.get('discovery', '')
    print(path) if mode != 'empty' else None
    if mode == 'stderr': print('fixture visibility failure', file=sys.stderr)
    sys.exit(1 if mode == 'status' else 0)
if args[-1:] == [':missing']:
    print('fixture missing object', file=sys.stderr)
    sys.exit(73)
print(json.dumps({'index': os.environ.get('GIT_INDEX_FILE')}))
'''


class FacadeTests(unittest.TestCase):
    work: Path
    mutation: str

    def invoke(self, arguments, discovery=''):
        with tempfile.TemporaryDirectory(dir=self.work) as scratch:
            root = Path(scratch)
            backend = root / 'git'
            backend.write_text(FAKE_GIT)
            backend.chmod(0o755)
            (root / 'case.json').write_text(json.dumps({'discovery': discovery}))
            index = root / 'proposed.index'
            index.write_bytes(b'controlled fixture index\n')
            environment = {**os.environ, PREFIX + 'GIT': str(backend),
                           PREFIX + 'GIT_DIR': str(root / 'main.git'),
                           PREFIX + 'INDEX': str(index), PREFIX + 'LOG': str(root / 'trace'),
                           PREFIX + 'MUTATION': self.mutation}
            environment.pop('GIT_INDEX_FILE', None)
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                     '--git-facade', *arguments], env=environment,
                                    capture_output=True, text=True, timeout=10)
            return result, str(index)

    def test_checkout_read_uses_proposed_index(self):
        result, index = self.invoke(['show', ':receipt.md'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'index': index})

    def test_child_repository_keeps_its_index(self):
        for prefix in (['-C', 'fixture'], ['-c', 'core.x=y', '-C', 'fixture']):
            with self.subTest(prefix=prefix):
                result, _ = self.invoke([*prefix, 'show', ':receipt.md'])
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), {'index': None})

    def test_non_index_command_does_not_receive_override(self):
        result, _ = self.invoke(['version'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'index': None})

    def check_discovery(self, mode):
        result, _ = self.invoke(['show', ':receipt.md'], mode)
        self.assertEqual(result.returncode, 2)
        self.assertIn('cannot identify Git index owner', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_failed_context_with_partial_output_refuses(self):
        self.check_discovery('status')

    def test_stderr_context_with_success_refuses(self):
        self.check_discovery('stderr')

    def test_empty_context_refuses(self):
        self.check_discovery('empty')

    def test_unknown_global_option_refuses(self):
        result, _ = self.invoke(['--unknown-probe-option', 'show', ':receipt.md'])
        self.assertEqual(result.returncode, 2)
        self.assertIn('unhandled global Git option', result.stderr)

    def test_original_status_and_stderr_survive(self):
        result, _ = self.invoke(['show', ':missing'])
        self.assertEqual(result.returncode, 73)
        self.assertEqual(result.stderr, 'fixture missing object\n')
        self.assertEqual(result.stdout, '')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def raw_git(backend, arguments, *, environment=None, data=None):
    return subprocess.run([backend, *arguments], cwd=ROOT, env=environment,
                          input=data, capture_output=True, check=True).stdout


def working_snapshot(backend):
    files = raw_git(backend, ['ls-files', '--stage', '-z']).split(b'\0')
    result = {}
    for entry in files:
        if not entry:
            continue
        metadata, encoded = entry.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        require(stage == b'0', 'unmerged real index')
        name = os.fsdecode(encoded)
        path = ROOT / name
        if mode == b'160000':
            result[name] = (mode.decode(), oid.decode())
        elif path.is_symlink():
            result[name] = ('symlink', digest(os.fsencode(os.readlink(path))))
        else:
            require(path.is_file() and path.stat().st_dev == ROOT.stat().st_dev
                    and not any(parent.is_symlink() for parent in path.parents
                                if parent.is_relative_to(ROOT)), 'unsafe tracked file: ' + name)
            result[name] = (path.stat().st_mode & 0o777, digest(path.read_bytes()))
    script = Path(__file__).resolve()
    result[str(script.relative_to(ROOT))] = (script.stat().st_mode & 0o777,
                                           digest(script.read_bytes()))
    return result


def assess(output):
    require(not any(os.environ.get(name) for name in ('GIT_INDEX_FILE', 'GIT_DIR',
                                                     'GIT_WORK_TREE')), 'ambient Git redirection')
    backend = shutil.which('git')
    require(backend is not None, 'git unavailable')
    backend = str(Path(backend).resolve())
    require(Path(raw_git(backend, ['rev-parse', '--show-toplevel']).decode().strip()).resolve()
            == ROOT, 'run in this project checkout')
    head = raw_git(backend, ['rev-parse', 'HEAD']).decode().strip()
    git_dir = raw_git(backend, ['rev-parse', '--absolute-git-dir']).decode().strip()
    real_index = Path(raw_git(backend, ['rev-parse', '--git-path', 'index']).decode().strip())
    if not real_index.is_absolute():
        real_index = ROOT / real_index
    require(real_index.is_file() and not real_index.is_symlink()
            and real_index.stat().st_dev == ROOT.stat().st_dev, 'unsafe real index')
    index_before = digest(real_index.read_bytes())
    working_before = working_snapshot(backend)
    logical = 'docs/tasks/archive/P4-SYSTEM-18.md'
    original = raw_git(backend, ['show', 'HEAD:' + logical])
    require((ROOT / logical).is_file() and not (ROOT / logical).is_symlink()
            and (ROOT / logical).stat().st_dev == ROOT.stat().st_dev, 'unsafe ordinary input')
    require((ROOT / logical).read_bytes() == original, 'ordinary working source differs')
    before, after = b'3196 links/normal+print', b'3197 links/normal+print'
    require(original.count(before) == 1, 'receipt mutation is absent or ambiguous')
    changed = original.replace(before, after, 1)
    (output / 'proposed-receipt.md').write_bytes(changed)
    state = {'state': 'in-flight', 'head': head, 'path': logical,
             'original_sha256': digest(original), 'proposed_sha256': digest(changed),
             'real_index_sha256': index_before, 'instrument_sha256': digest(Path(__file__).read_bytes())}
    (output / 'state.json').write_text(json.dumps(state, indent=2) + '\n')
    with tempfile.TemporaryDirectory(dir=output) as scratch:
        work = Path(scratch)
        proposed = work / 'index'
        environment = {**os.environ, 'GIT_INDEX_FILE': str(proposed)}
        raw_git(backend, ['read-tree', head], environment=environment)
        oid = raw_git(backend, ['hash-object', '-w', '--stdin'], data=changed).decode().strip()
        raw_git(backend, ['update-index', '--cacheinfo', '100644,' + oid + ',' + logical],
                environment=environment)
        entries = raw_git(backend, ['ls-files', '--stage', '-z'], environment=environment)
        require(raw_git(backend, ['diff', '--cached', '--name-only'], environment=environment)
                == (logical + '\n').encode(), 'proposed effect set differs')
        tools = work / 'bin'
        tools.mkdir()
        wrapper = tools / 'git'
        wrapper.write_text('#!/usr/bin/env bash\nexec ' + shlex.quote(sys.executable) + ' '
                           + shlex.quote(str(Path(__file__).resolve()))
                           + ' --git-facade "$@"\n')
        wrapper.chmod(0o755)
        trace_path = output / 'git-trace.jsonl'
        environment = {**os.environ, 'PATH': str(tools) + os.pathsep + os.environ['PATH'],
                       'TMPDIR': str(output / 'tmp'), 'PYTHONDONTWRITEBYTECODE': '1',
                       PREFIX + 'GIT': backend,
                       PREFIX + 'GIT_DIR': git_dir, PREFIX + 'INDEX': str(proposed),
                       PREFIX + 'LOG': str(trace_path)}
        environment.pop(PREFIX + 'MUTATION', None)
        (output / 'tmp').mkdir()
        result = subprocess.run([str(wrapper), 'show', ':' + logical], cwd=ROOT,
                                env=environment, capture_output=True, check=True)
        require(result.stdout == changed and not result.stderr, 'facade did not expose proposed blob')
        with (output / 'gate.log').open('wb') as log:
            gate = subprocess.run(['bash', 'scripts/check_doctrines.sh'], cwd=ROOT,
                                  env=environment, stdout=log, stderr=subprocess.STDOUT)
        require(raw_git(backend, ['rev-parse', 'HEAD']).decode().strip() == head, 'HEAD changed')
        require(digest(real_index.read_bytes()) == index_before, 'real index changed')
        require(working_snapshot(backend) == working_before, 'tracked working bytes/modes changed')
        require(raw_git(backend, ['ls-files', '--stage', '-z'], environment={
            **os.environ, 'GIT_INDEX_FILE': str(proposed)}) == entries, 'proposed index changed')
        rows = [json.loads(line) for line in trace_path.read_text().splitlines()]
        require(not any('refused' in row for row in rows), 'facade refused; cannot classify gate')
        require(b'ARCHIVE-GATE-PROBE:' not in (output / 'gate.log').read_bytes(),
                'facade reported an error; cannot classify gate')
        require(gate.returncode in (0, 1), 'gate could not judge')
        state.update(state='complete', gate_rc=gate.returncode,
                     gate_accepted_altered_receipt=gate.returncode == 0,
                     real_index_unchanged=True, working_files_unchanged=len(working_before),
                     proposed_index_unchanged=True,
                     scoped_reads=sum(row['injected'] for row in rows),
                     delegated_calls=sum(not row['injected'] for row in rows))
    state['owned_index_residue'] = 0
    (output / 'result.json').write_text(json.dumps(state, indent=2) + '\n')
    print(json.dumps(state, indent=2))


def main():
    if sys.argv[1:2] == ['--git-facade']:
        return facade(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path,
                        help='new repository-relative target directory owned by the task')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--mutation', choices=['unscoped', 'missing', 'discovery'])
    args = parser.parse_args()
    require(not args.mutation or args.self_test, 'mutations require controlled self-test fixtures')
    relative = args.output
    require(not relative.is_absolute() and relative.parts and relative.parts[0] == 'target'
            and '..' not in relative.parts, 'output must be a relative target path')
    output = ROOT / relative
    require(not output.exists() and not any(path.is_symlink() for path in [output, *output.parents]),
            'output exists or has a symlink ancestor')
    ancestor = next(path for path in output.parents if path.exists())
    require(ancestor.is_dir() and ancestor.stat().st_dev == ROOT.stat().st_dev,
            'output parent is on another volume')
    output.mkdir(parents=True)
    require(output.stat().st_dev == ROOT.stat().st_dev, 'output is on another volume')
    if args.self_test:
        FacadeTests.work = output
        FacadeTests.mutation = args.mutation or ''
        result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(FacadeTests))
        print(f'ARCHIVE-GATE-PROBE: {result.testsRun} tests / {len(result.failures)} failures / '
              f'{len(result.errors)} errors')
        return 0 if result.wasSuccessful() else 1
    assess(output)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (Refused, OSError, subprocess.SubprocessError) as error:
        print('ARCHIVE-GATE-PROBE: REFUSED — ' + str(error), file=sys.stderr)
        raise SystemExit(2)
