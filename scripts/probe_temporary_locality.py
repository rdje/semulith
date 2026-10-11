#!/usr/bin/env python3
"""Guard actual temporary allocations without permitting a foreign-volume write.

Shell sites execute only their mktemp expressions, never acquisition/push/update
workflows. Python controls execute the actual two self-tests with an allocator
that refuses before an unqualified allocation and checks complete cleanup.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent

SHIM = '''#!/usr/bin/env python3
import os, pathlib, sys
root = pathlib.Path(os.environ['SEMULITH_LOCALITY_ROOT']).resolve() / 'target'
args = sys.argv[1:]
try:
    template = pathlib.Path(args[-1])
    if not (template.is_absolute() and template.resolve().is_relative_to(root)
            and 'XXXXXX' in template.name):
        raise ValueError('unqualified template')
    ancestor = template.parent
    while not ancestor.exists():
        ancestor = ancestor.parent
    if ancestor.stat().st_dev != root.parent.stat().st_dev:
        raise ValueError('foreign volume')
except (IndexError, ValueError):
    print('TMP-LOCALITY: unqualified shell allocation', file=sys.stderr)
    sys.exit(1)
template.parent.mkdir(parents=True, exist_ok=True)
os.execv(os.environ['SEMULITH_REAL_MKTEMP'], ['mktemp', *args])
'''

PYTHON_GUARD = '''
import inspect, os, pathlib, sys, tempfile
root = pathlib.Path(os.environ['SEMULITH_LOCALITY_ROOT']).resolve()
script = sys.argv[1]
source = sys.stdin.read()
real = tempfile.mkdtemp
allocated = []
def qualified(*args, **kwargs):
    directory = inspect.signature(real).bind_partial(*args, **kwargs).arguments.get('dir')
    if directory is None or not pathlib.Path(directory).resolve().is_relative_to(root / 'target'):
        raise RuntimeError('TMP-LOCALITY: unqualified Python allocation')
    if pathlib.Path(directory).stat().st_dev != root.stat().st_dev:
        raise RuntimeError('TMP-LOCALITY: Python parent is on a foreign volume')
    path = real(*args, **kwargs)
    allocated.append(pathlib.Path(path))
    if pathlib.Path(path).stat().st_dev != root.stat().st_dev:
        raise RuntimeError('TMP-LOCALITY: Python allocation is on a foreign volume')
    return path
tempfile.mkdtemp = qualified
sys.argv = [script, '--self-test']
status = 0
try:
    exec(compile(source, script, 'exec'), {'__file__': script, '__name__': '__main__'})
except SystemExit as exc:
    status = exc.code or 0
except RuntimeError as exc:
    print(exc, file=sys.stderr)
    status = 1
finally:
    tempfile.mkdtemp = real
residue = [path for path in allocated if path.exists()]
if residue:
    print('TMP-LOCALITY: fixture residue', file=sys.stderr)
    # Only directories allocated by this controlled invocation; never a shared cache.
    import shutil
    for path in residue:
        if path.exists(): shutil.rmtree(path)
    status = 1
if not allocated and status == 0:
    print('TMP-LOCALITY: no allocation observed', file=sys.stderr)
    status = 1
sys.exit(status)
'''


def source(name, revision):
    if revision:
        return subprocess.check_output(['git', 'show', f'{revision}:{name}'], cwd=ROOT).decode()
    return (ROOT / name).read_text()


def require(condition, message):
    if not condition:
        raise RuntimeError('TMP-LOCALITY: ' + message)


def shell_sites(revision):
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    for name in paths:
        if not (name.endswith('.sh') or name.startswith('.githooks/')):
            continue
        if name.startswith('vendor/'):
            continue
        for number, line in enumerate(source(name, revision).splitlines(), 1):
            if line.lstrip().startswith('#'):
                continue
            # Include stdout-producing helper calls as well as $(mktemp ...).
            # Each current site has zero/one -d and a quoted explicit template.
            # Unsupported call syntax is not silently reclassified as qualified.
            pattern = r'(?<![\w-])mktemp(?:[ \t]+-d)?(?:[ \t]+(?:"[^"]*"|[^ \t;)}]+))?'
            for expression in re.findall(pattern, line):
                yield name, number, expression


def run_shell(expression, fixture):
    real = shutil.which('mktemp')
    require(real, 'mktemp is required to check actual allocation behavior')
    bin_dir = fixture / 'bin'
    bin_dir.mkdir(exist_ok=True)
    shim = bin_dir / 'mktemp'
    # Use the current interpreter, not an interpreter found through the modified PATH.
    shim.write_text(SHIM.replace('#!/usr/bin/env python3', '#!' + sys.executable, 1))
    shim.chmod(0o755)
    env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ.get('PATH', ''),
               TMPDIR=str(ROOT.parent / '__semulith_forbidden_temp__'),
               SEMULITH_LOCALITY_ROOT=str(ROOT), SEMULITH_REAL_MKTEMP=real)
    for name in ('tmp', 'doctrine-selftest', 'history-check', 'push-selftest'):
        (ROOT / 'target' / name).mkdir(parents=True, exist_ok=True)
    command = (f'ROOT={shlex.quote(str(ROOT))}; REPO_ROOT="$ROOT"; d="$ROOT/target/doctrine-selftest"; '
               'test_temp_root="$ROOT/target/push-selftest"; ' + expression)
    result = subprocess.run(['bash', '-c', command], env=env, capture_output=True, text=True)
    if result.returncode:
        return result.returncode, result.stderr.strip()
    path = Path(result.stdout.strip())
    require(path.resolve().is_relative_to(ROOT / 'target'), 'allocation escaped target')
    require(path.stat().st_dev == ROOT.stat().st_dev, 'allocation is on a foreign volume')
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    require(not path.exists(), 'shell fixture residue')
    return 0, ''


def run_python(name, text):
    env = dict(os.environ, SEMULITH_LOCALITY_ROOT=str(ROOT),
               TMPDIR=str(ROOT.parent / '__semulith_forbidden_temp__'))
    return subprocess.run([sys.executable, '-c', PYTHON_GUARD, str(ROOT / name)],
                          input=text, text=True, capture_output=True, env=env)


def child_environment(broken=False):
    names = ('scripts/check_doctrines.sh', '.githooks/pre-commit',
             'scripts/check_delivery_provenance.sh', 'scripts/check_readme_routes.sh',
             'scripts/check_seam_integrity.sh', 'scripts/check_task_acceptance.sh',
             'scripts/check_upstream_index.sh', 'scripts/check_waiver_routing.sh',
             'scripts/fetch_references.sh', 'scripts/update_scaffold.sh',
             'docs/tasks/artifacts/task_acceptance/run_task_acceptance_probes.sh',
             'docs/tasks/artifacts/waiver_routing/run_waiver_routing_probes.sh',
             'docs/tasks/artifacts/dsp-review/synth/run_synth_probes.sh')
    fragments = []
    for name in names:
        text = source(name, None)
        marker = '# Project-owned temporary data' if name in names[:2] else '# All scratch,'
        lines = text[text.index(marker):].splitlines()
        require(lines[1] == 'mkdir -p "$ROOT/target/tmp" || exit 2', 'unknown child parent setup')
        require(lines[2] == 'export TMPDIR="$ROOT/target/tmp"', 'unknown child environment setup')
        fragments.append((name, '\n'.join(lines[1:3])))
    text = source('scripts/pre_push.sh', None)
    start = text.index('  local TMPDIR="$root/target/tmp"')
    fragment = '\n'.join(text[start:].splitlines()[:3])
    fragments.append(('scripts/pre_push.sh', fragment))
    if broken:
        fragments = [('controlled-negative', '')]
    count = 0
    for name, fragment in fragments:
        for inherited in (None, str(ROOT.parent / '__semulith_forbidden_temp__')):
            env = dict(os.environ)
            env.pop('TMPDIR', None)
            if inherited:
                env['TMPDIR'] = inherited
            command = (f'ROOT={shlex.quote(str(ROOT))}; '
                       'probe() { local root="$ROOT";\n' + fragment + '\n' +
                       f'{shlex.quote(sys.executable)} -c '
                       + shlex.quote('import os; print(os.environ.get("TMPDIR", ""))')
                       + '\n}; probe')
            result = subprocess.run(['bash', '-c', command], env=env, capture_output=True, text=True)
            if result.returncode or result.stdout.strip() != str(ROOT / 'target/tmp'):
                print(f'TMP-LOCALITY: child temporary root differs: {name}')
                return 1
            count += 1
    print(f'TMP-LOCALITY: {count} unset/foreign child environments constrained')
    return 0


def scratch_parent(fixture, revision):
    name = 'docs/tasks/artifacts/dsp-review/synth/run_synth_probes.sh'
    lines = source(name, revision).splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith('SCRATCH="$(mktemp'))
    block = lines[index]
    if lines[index - 1].startswith('mkdir -p '):
        block = lines[index - 1] + '\n' + block
    command = f'ROOT={shlex.quote(str(fixture))}\n' + block + '\ntest -d "$SCRATCH"'
    result = subprocess.run(['bash', '-c', command], capture_output=True, text=True,
                            env=dict(os.environ, TMPDIR=str(ROOT.parent / '__semulith_forbidden_temp__')))
    if result.returncode:
        print('TMP-LOCALITY: scratch parent allocation unavailable')
        return 1
    print('TMP-LOCALITY: scratch parent created before guarded allocation')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', required=True,
                        choices=('shell', 'python', 'bare-shell', 'bare-python', 'residue',
                                 'children', 'unconstrained-child', 'parent'))
    parser.add_argument('--revision', help='read-only predecessor source for before/after proof')
    args = parser.parse_args()
    if args.mode in ('children', 'unconstrained-child'):
        return child_environment(args.mode == 'unconstrained-child')
    parent = ROOT / 'target/doctrine-selftest'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='locality-', dir=parent) as temporary:
        fixture = Path(temporary)
        if args.mode == 'parent':
            return scratch_parent(fixture, args.revision)
        if args.mode in ('shell', 'bare-shell'):
            sites = [('controlled-negative', 1, 'mktemp -d')] if args.mode == 'bare-shell' else list(shell_sites(args.revision))
            failures = []
            for name, line, expression in sites:
                rc, reason = run_shell(expression, fixture)
                if rc:
                    failures.append(f'{name}:{line}: {reason}')
            for finding in failures:
                print(finding)
            print(f'TMP-LOCALITY: {len(sites) - len(failures)}/{len(sites)} shell sites qualified and cleaned')
            return 1 if failures else 0
        if args.mode in ('bare-python', 'residue'):
            text = 'import tempfile\ntempfile.mkdtemp()\n'
            if args.mode == 'residue':
                text = ('import tempfile\nfrom pathlib import Path\n'
                        'root = Path(__file__).resolve().parent.parent\n'
                        'tempfile.mkdtemp(dir=root / "target/doctrine-selftest")\n')
            result = run_python('scripts/controlled-negative.py', text)
            print(result.stdout + result.stderr, end='')
            return result.returncode
        names = ('scripts/materials.py', 'scripts/compare_dumps.py')
        failed = 0
        for name in names:
            result = run_python(name, source(name, args.revision))
            if result.returncode:
                failed += 1
                print(name + ': ' + result.stdout + result.stderr)
        print(f'TMP-LOCALITY: {len(names) - failed}/{len(names)} Python self-tests qualified and cleaned')
        return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
