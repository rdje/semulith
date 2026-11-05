#!/usr/bin/env python3
"""Which repository files does a probe actually read? An audit hook names every file it opens, so a claim about a probe's inputs is measured, not read from its code.

usage: python3 -B scripts/live_reads.py scripts/probe_x.py [args...]
       python3 -B scripts/live_reads.py --self-test
prints JSON: `probe`; `rc`; `live`, the repository files read outside tools (scripts/*.py), target/ and scripts/fixtures/; `frozen`, how many it read under scripts/fixtures/;
`spawned`, the argv of each process it started. A spawned process's own reads are NOT traced, so `live` is a floor wherever `spawned` is not empty: name that in the claim.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
TEMPORARY = ROOT / 'target/tmp'


def run_probe(probe: str, args: list[str]) -> dict:
    opened, spawned = set(), []

    def hook(event, details):
        if event == 'open' and isinstance(details[0], (str, bytes, os.PathLike)):
            if details[1] is None or 'r' in str(details[1]):
                opened.add(os.path.abspath(os.fsdecode(details[0])))
        elif event == 'subprocess.Popen':
            spawned.append(' '.join(str(part) for part in details[1])[:200])

    sys.addaudithook(hook)
    sys.argv = [probe, *args]
    sys.path.insert(0, str(Path(probe).resolve().parent))
    saved = sys.stdout, sys.stderr
    rc: int | str = 0
    with open(os.devnull, 'w', encoding='utf-8') as sink:
        sys.stdout = sys.stderr = sink
        try:
            runpy.run_path(probe, run_name='__main__')
        except SystemExit as stop:
            rc = stop.code or 0
        except BaseException as failure:  # pylint: disable=broad-except  # the probe's own failure is the measurement
            rc = repr(failure)
        finally:
            sys.stdout, sys.stderr = saved
    prefix = str(ROOT) + os.sep
    files = sorted(p[len(prefix):] for p in opened if p.startswith(prefix) and os.path.isfile(p))
    live = [p for p in files if not p.startswith(('target/', 'scripts/fixtures/'))
            and '__pycache__' not in p and not (p.startswith('scripts/') and p.endswith('.py'))]
    return dict(probe=probe, rc=rc, live=live, frozen=sum(p.startswith('scripts/fixtures/') for p in files), spawned=spawned)


def self_test() -> int:
    """A probe that reads one tracked file, one frozen file and spawns one process must be reported as exactly that."""
    TEMPORARY.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='live-reads-', dir=TEMPORARY) as scratch:
        probe = Path(scratch) / 'probe.py'
        frozen = next(p for p in sorted((ROOT / 'scripts/fixtures').rglob('*')) if p.is_file())
        probe.write_text(f"import subprocess, sys\nopen({str(ROOT / 'README.md')!r}).read()\nopen({str(frozen)!r}, 'rb').read()\n"
                         "open(sys.argv[1], 'w').write('x')\nsubprocess.run(['true'], check=True)\nsys.exit(3)\n")
        done = subprocess.run([sys.executable, '-B', __file__, str(probe), str(Path(scratch) / 'written')], capture_output=True, text=True, check=False)
    report = json.loads(done.stdout)
    failures = [name for name, good in (('rc', report['rc'] == 3), ('live', report['live'] == ['README.md']), ('frozen', report['frozen'] == 1),
                                        ('spawned', report['spawned'] == ['true'])) if not good]
    print('LIVE-READS --self-test: ' + (f'FAILED {failures}: {report}' if failures else 'ok (a read, a frozen read, a write and a spawn each reported as it is)'))
    return 1 if failures else 0


def main() -> int:
    if sys.argv[1:] == ['--self-test']:
        return self_test()
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    print(json.dumps(run_probe(sys.argv[1], sys.argv[2:]), indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
