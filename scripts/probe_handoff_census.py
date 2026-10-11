#!/usr/bin/env python3
"""Exercise the public Bash handoff census with controlled host-tool responses."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / 'scripts/check_no_background_jobs.sh'
MUTATIONS = {
    'status': ('if [ "$rc" -ne 0 ]; then', 'if false; then'),
    'stderr': ('if [ -s "$CENSUS_ERROR" ]; then', 'if false; then'),
    'empty': ('if ! [[ "$output" =~ [^[:space:]] ]]; then', 'if false; then'),
    'signal': ("trap 'exit 143' TERM", "# omitted TERM cleanup trap"),
}
WRAPPER = '''#!/usr/bin/env python3
import json, pathlib, sys, time
root = pathlib.Path(__file__).resolve().parent.parent
kind = pathlib.Path(sys.argv[0]).name
case = json.loads((root / 'case.json').read_text())
if kind == 'ps' and sys.argv[1:2] != ['-Ao']:
    sys.exit(1)  # End the caller's ancestry walk; synthetic PIDs are unrelated.
row = case[kind]
if row.get('pause'):
    (root / 'census-ready').touch()
    deadline = time.monotonic() + 15
    while not (root / 'census-release').exists():
        if time.monotonic() > deadline:
            sys.exit(75)
        time.sleep(0.01)
sys.stdout.write(row['stdout'].replace('{root}', str(root)))
sys.stderr.write(row['stderr'])
sys.exit(row['rc'])
'''


def base_case():
    return {
        'ps': {'stdout': '2147001 00:01 fixture-worker\n', 'stderr': '', 'rc': 0},
        'lsof': {'stdout': 'p2147001\nfcwd\nn/fixture/external\n', 'stderr': '', 'rc': 0},
    }


class Census(unittest.TestCase):
    source: bytes
    sanctioned: bytes
    work: Path

    def invoke(self, case, args=(), interrupt=False):
        with tempfile.TemporaryDirectory(dir=self.work) as scratch:
            root = Path(scratch)
            (root / 'scripts').mkdir()
            (root / 'doctrine').mkdir()
            (root / 'bin').mkdir()
            script = root / 'scripts/check_no_background_jobs.sh'
            script.write_bytes(self.source)
            (root / 'doctrine/sanctioned_processes.tsv').write_bytes(self.sanctioned)
            (root / 'case.json').write_text(json.dumps(case))
            for name in ('ps', 'lsof'):
                path = root / 'bin' / name
                path.write_text(WRAPPER)
                path.chmod(0o755)
            command = ['bash', str(script), *args]
            environment = {**os.environ, 'PATH': str(root / 'bin') + os.pathsep + os.environ['PATH']}
            if interrupt:
                process = subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, text=True, env=environment)
                try:
                    deadline = time.monotonic() + 5
                    while not (root / 'census-ready').exists() and process.poll() is None:
                        if time.monotonic() > deadline:
                            self.fail('host-tool fixture did not reach its checkpoint')
                        time.sleep(0.01)
                    self.assertIsNone(process.poll(), 'census exited before interruption')
                    process.terminate()
                    (root / 'census-release').touch()
                    stdout, stderr = process.communicate(timeout=20)
                    result = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
                finally:
                    (root / 'census-release').touch()
                    if process.poll() is None:
                        process.kill()
                    process.communicate(timeout=20)
            else:
                result = subprocess.run(command, cwd=root, capture_output=True, text=True,
                                        env=environment, timeout=20)
            self.assertEqual(list((root / 'target/handoff-census').glob('*')), [],
                             'owned stderr file leaked after exit')
            return result

    def expect(self, case, rc, phrase, args=()):
        result = self.invoke(case, args)
        self.assertEqual(result.returncode, rc, result.stdout + result.stderr)
        self.assertIn(phrase, result.stdout + result.stderr)
        if rc:
            self.assertNotIn('handoff: OK', result.stdout + result.stderr)
        return result

    def test_external_process(self):
        self.expect(base_case(), 0, 'handoff: OK')

    def test_inherited_cwd_is_advisory(self):
        case = base_case()
        case['lsof']['stdout'] = 'p2147001\nfcwd\nn{root}\n'
        self.expect(case, 0, 'advisory: 1 session process')

    def test_all_lists_advisory_without_changing_verdict(self):
        case = base_case()
        case['lsof']['stdout'] = 'p2147001\nfcwd\nn{root}\n'
        self.expect(case, 0, '[inherited cwd, 0 repo handles]', ('--all',))

    def test_read_only_handle_without_repository_cwd(self):
        case = base_case()
        case['lsof']['stdout'] += 'f83r\nn{root}/AGENTS.md\n'
        self.expect(case, 1, '1 project-owned process(es) STILL RUNNING')

    def test_command_names_checkout_without_handles(self):
        case = base_case()
        case['ps']['stdout'] = '2147001 00:01 fixture-worker {root}/job.py\n'
        self.expect(case, 1, '1 project-owned process(es) STILL RUNNING')

    def sanctioned_case(self, child=False):
        prefix = next(line.split('\t', 1)[0] for line in self.sanctioned.decode().splitlines()
                      if line and not line.startswith('#'))
        case = base_case()
        case['ps']['stdout'] = '2147001 00:01 /fixture/' + prefix + '\n'
        case['lsof']['stdout'] += 'f83r\nn{root}/AGENTS.md\n'
        if child:
            case['ps']['stdout'] += '2147002 00:01 fixture-child\n'
            case['lsof']['stdout'] += 'p2147002\nf4w\nn{root}/result.log\n'
        return case

    def test_existing_director_exemption(self):
        self.expect(self.sanctioned_case(), 0, 'handoff: OK')

    def test_exemption_does_not_cover_other_processes(self):
        self.expect(self.sanctioned_case(child=True), 1,
                    '1 project-owned process(es) STILL RUNNING')

    def test_help_includes_usage_and_failure_contract(self):
        result = self.expect(base_case(), 0, 'Usage:', ('--help',))
        self.assertIn('2 = usage/census failure', result.stdout)

    def test_term_cleans_owned_stderr(self):
        case = base_case()
        case['ps']['pause'] = True
        result = self.invoke(case, interrupt=True)
        self.assertEqual(result.returncode, 143, result.stdout + result.stderr)
        self.assertNotIn('handoff: OK', result.stdout + result.stderr)

    def test_unknown_option(self):
        self.expect(base_case(), 2, 'usage:', ('--unknown',))

    def test_surplus_arguments(self):
        self.expect(base_case(), 2, 'usage:', ('--all', 'unexpected'))


def failure_case(tool, failure):
    def check(self):
        case = base_case()
        if failure == 'status':
            case[tool]['rc'] = 1  # Valid partial stdout must not hide failure.
            reason = 'failed (exit 1)'
        elif failure == 'stderr':
            case[tool]['stderr'] = 'fixture: visibility unavailable\n'
            reason = 'reported stderr'
        else:
            case[tool]['stdout'] = '' if failure == 'empty' else ' \t\n'
            reason = 'returned no data'
        self.expect(case, 2, tool + ' census ' + reason)
    return check


for _tool in ('ps', 'lsof'):
    for _failure in ('status', 'stderr', 'empty', 'whitespace'):
        setattr(Census, 'test_' + _tool + '_' + _failure, failure_case(_tool, _failure))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SCRIPT,
                        help='trusted implementation source for predecessor comparison')
    parser.add_argument('--mutation', choices=sorted(MUTATIONS))
    args = parser.parse_args()
    source = args.source.read_bytes()
    if args.mutation:
        before, after = (value.encode() for value in MUTATIONS[args.mutation])
        if source.count(before) != 1:
            parser.error('mutation seam is missing or ambiguous')
        source = source.replace(before, after, 1)
    Census.source = source
    Census.sanctioned = (ROOT / 'doctrine/sanctioned_processes.tsv').read_bytes()
    Census.work = ROOT / 'target/handoff-selftest'
    Census.work.mkdir(parents=True, exist_ok=True)
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(Census))
    print(f'HANDOFF-CENSUS: {result.testsRun} tests / {len(result.failures)} failures / '
          f'{len(result.errors)} errors; synthetic host-tool responses')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
