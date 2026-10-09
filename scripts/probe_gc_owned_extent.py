#!/usr/bin/env python3
"""Exercise historical capture checks before and after a C count migration.

The temporary clone is limited to this project's public definition/author inputs;
all files and subprocess outputs stay on the repository volume. No engine runs.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import derive_gc_parcel_counts as Counts
import derive_rv64gc_expectations as Q
import dossier_sexp as D
from expectations_text import with_fetches
from riscv_asm import Assembler

REPO = Path(__file__).resolve().parent.parent
UNIT = REPO / 'profiles/rv64gc-lab-v0'


def probe(root, mutation):
    shutil.copytree(REPO / 'definitions', root / 'definitions')
    shutil.copytree(REPO / 'schema', root / 'schema')
    scripts = root / 'scripts'
    scripts.mkdir()
    for path in (REPO / 'scripts').glob('*.py'):
        shutil.copyfile(path, scripts / path.name)
    unit = root / 'profiles/rv64gc-lab-v0'
    guests = unit / 'guests'
    guests.mkdir(parents=True)
    for path in UNIT.glob('*.sexp'):
        shutil.copyfile(path, unit / path.name)
    for name in Q.OWNED_GUESTS:
        shutil.copyfile(UNIT / 'guests' / (name + '.s'), guests / (name + '.s'))
    original = (UNIT / 'encoding.sexp').read_text()
    full = original.replace('(slot (id c) (requires "riscv/c"))', '(extensions "riscv/c")')
    encoding = unit / 'encoding.sexp'
    encoding.write_text(full.replace('(extensions "riscv/c")', ''))
    env = dict(os.environ, TMPDIR=str(root), PYTHONPYCACHEPREFIX=str(root / 'pycache'))

    def run(*args):
        return subprocess.run([sys.executable, 'scripts/derive_rv64gc_expectations.py', *args],
                              cwd=root, env=env, text=True, capture_output=True)

    # Reconstruct only this temporary historical word fixture. This works both
    # before and after production adopts its parcel extent; no tracked record writes.
    made = run(*(str(Path('profiles/rv64gc-lab-v0/guests') / (n + '.s')) for n in Q.OWNED_GUESTS))
    assert made.returncode == 0, made.stdout + made.stderr
    unbound = run('--check-owned')
    assert unbound.returncode == 0, 'unbound historical check: ' + unbound.stderr
    encoding.write_text(full)
    unmigrated = run('--check-owned')
    assert unmigrated.returncode == 1 and 'DRIFT' in unmigrated.stderr, 'unmigrated C counts accepted'
    rows = Counts.derive_counts(guests, Assembler(encoding))
    for row in rows:
        path = guests / (row['guest'] + '.expected.sexp')
        path.write_text(with_fetches(path.read_text(), row['parcel_fetches']))
    author = scripts / 'derive_rv64gc_expectations.py'
    changes = {
        'old-counts': ('return with_fetches(text, fetches), budget', 'return text, budget'),
        'parcel-prose': ('return with_fetches(text, fetches), budget',
                         "return emit(path, run.steps, budget, run.never, run.refusals, route='parcels'), budget"),
        'bad-request-log': ('run = derive_parcel_guest(path, asm, budget)\n    original =',
                            'run = derive_parcel_guest(path, asm, budget)\n    run.steps[0].fetch += 1\n    original ='),
        'permit-word-write': ("if ('c.nop' in asm.insns and not (args.parcels or args.check or args.check_owned)",
                              "if (False and not (args.parcels or args.check or args.check_owned)"),
    }
    if mutation:
        text = author.read_text()
        old, new = changes[mutation]
        assert text.count(old) == 1, 'mutation must match exactly once'
        author.write_text(text.replace(old, new))
    bound = run('--check-owned')
    assert bound.returncode == 0, 'bound migrated historical check: ' + bound.stderr
    repeated = run('--check-owned')
    assert repeated.returncode == 0 and repeated.stdout == bound.stdout, 'historical repeat differs'
    path = guests / 'f-arith.expected.sexp'
    saved = path.read_bytes()
    row = next(r for r in rows if r['guest'] == 'f-arith')
    for label, damaged in (
        ('count', with_fetches(saved.decode(), row['parcel_fetches'] + 1).encode()),
        ('observation', saved.replace(b'0x0000000000000001', b'0x0000000000000009', 1)),
        ('comment', saved + b';; silent drift\n'),
        ('line endings', saved.replace(b'\n', b'\r\n')),
    ):
        assert damaged != saved, label + ' mutation did not fire'
        path.write_bytes(damaged)
        refused = run('--check-owned')
        assert refused.returncode == 1 and 'DRIFT' in refused.stderr, label + ' drift accepted'
    path.write_bytes(saved)
    refused = run('profiles/rv64gc-lab-v0/guests/f-arith.s')
    assert refused.returncode == 2 and 'explicit --parcels --steps write' in refused.stderr, 'canonical word write accepted'
    assert path.read_bytes() == saved, 'refused write changed the record'
    explicit = run('--parcels', '--steps', str(row['boundaries']), 'profiles/rv64gc-lab-v0/guests/f-arith.s')
    assert explicit.returncode == 0, 'explicit parcel write refused: ' + explicit.stderr
    doc = D.load_expectations(path)
    assert doc.get('fetches', doc['instructions']) == row['parcel_fetches'], 'explicit route lost parcel extent'
    assert b'explicit-budget parcel route (C-capable)' in path.read_bytes(), 'explicit route provenance lost'
    print('GC owned extent probe: 42 historical records, word/C migration, repeat, byte drift, write guard and explicit route pass')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', choices=['old-counts', 'parcel-prose', 'bad-request-log', 'permit-word-write'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='owned-extent-', dir=parent) as td:
            probe(Path(td).resolve(), args.mutation)
    except AssertionError as exc:
        print(f'GC owned extent probe: REFUSED — {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
