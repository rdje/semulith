#!/usr/bin/env python3
"""Offline controls for the pinned Sail adapter: absence cannot produce agreement."""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile

import dossier_sexp as D
import records_sexp as R
import run_rv64gc_sail as S

REPO = Path(__file__).resolve().parent.parent
NOP = '[0] [M]: 0x0000000080000000 (0x00000013) addi x0,x0,0\n'


def expected(insn='addi x0, x0, 0', derivation='ADDI writes x0, which stays zero.', writes=None):
    return {'program': 'nop.s', 'entry': '0x80000000', 'instructions': 1,
            'step': [{'n': 0, 'insn': insn, 'writes': writes or {},
                      'derivation': derivation, 'source': 'RVI-RV32I 1.1.4'}]}


def refused(fn, reason, failure):
    try:
        fn()
    except S.SailError as exc:
        assert reason in str(exc), str(exc)
    else:
        raise AssertionError(failure)


def check(adapter, root):
    global S
    S = adapter
    assert S.compare_trace(expected(), NOP)[0] == 'AGREE'
    assert S.compare_trace(expected(), NOP + 'x0 <- 0x0000000000000000\n')[0] == 'AGREE'
    refused(lambda: S.compare_trace(expected(), ''), 'missing expected step 0',
            'empty ordinary no-write trace accepted')
    refused(lambda: S.compare_trace(expected(), NOP, 1), 'rc=1',
            'failed reference process accepted')
    zero = expected()
    zero['instructions'], zero['step'] = 0, []
    refused(lambda: S.compare_trace(zero, ''), 'no positive program step budget',
            'empty expectation budget accepted')
    interrupt = expected('addi x7, x0, 0', 'the pending evaluation takes the SSI interrupt in M: no fetch.')
    event = 'handling int#supervisor-software-interrupt at priv M | tval=0x0000000000000000\n'
    assert S.compare_trace(interrupt, event)[0] == 'AGREE'
    refused(lambda: S.compare_trace(interrupt, ''), 'missing expected step 0',
            'unwitnessed delivery gap accepted')
    refused(lambda: S.compare_trace(expected(), event), 'missing expected step 0',
            'interrupt event excused an ordinary instruction')
    refused(lambda: S.compare_trace(interrupt, event.replace('software', 'external')),
            'missing expected step 0', 'wrong interrupt cause accepted')
    fetch = expected('<fetch page fault at 0x403000>', 'The fetch walk denies execute permission.')
    fetch_event = 'handling exc#fetch-page-fault at priv M | tval=0x0000000000403000\n'
    assert S.compare_trace(fetch, fetch_event)[0] == 'AGREE'
    refused(lambda: S.compare_trace(fetch, ''), 'missing expected step 0',
            'unwitnessed fetch gap accepted')
    refused(lambda: S.compare_trace(expected(), NOP + NOP), 'duplicate/out-of-order',
            'duplicate instruction row accepted')
    refused(lambda: S.compare_trace(expected(), NOP.replace('(0x00000013)', '(broken)')),
            'malformed trace', 'malformed instruction row accepted')
    refused(lambda: S.compare_trace(expected(), 'x1 <- 0x0000000000000001\n'),
            'orphan GPR write', 'orphan write accepted')
    refused(lambda: S.compare_trace(expected(), NOP + 'x32 <- 0x0000000000000001\n'),
            'invalid or orphan', 'invalid register index accepted')
    refused(lambda: S.compare_trace(expected(), NOP + 'x0 <- 0x0000000000000001\n'),
            'x0 trace write is nonzero', 'nonzero x0 write accepted')
    refused(lambda: S.compare_trace(expected(), event.replace('supervisor-software-interrupt', 'new-name')),
            'unknown int spelling', 'unknown interrupt spelling accepted')
    changed = NOP + 'x1 <- 0x0000000000000001\n'
    assert S.compare_trace(expected(), changed)[0] == 'DIVERGE'
    assert S.compare_trace(expected(writes={'x1': '0x1'}), changed)[0] == 'AGREE'
    # Real loader/runner orchestration, with a process that writes no new output.
    # Both stale repetitions must be discarded, even if their old observations agree.
    guests, out = root / 'guests', root / 'out'
    guests.mkdir()
    out.mkdir()
    (guests / 'nop.s').write_text('addi x0, x0, 0\n')
    (guests / 'nop.expected.sexp').write_text(R.render_forms([D.expectations_to_form(expected())]))
    for repetition in range(2):
        (out / f'nop.{repetition}.trace').write_text(NOP)
    original_run = S.subprocess.run
    try:
        S.subprocess.run = lambda *a, **k: SimpleNamespace(returncode=0, stdout='', stderr='')
        refused(lambda: S.run_guest('nop', Path('fake-sail'), out,
                                    REPO / 'profiles/rv64gc-lab-v0/encoding.sexp', guests),
                'reference produced no trace', 'stale traces accepted as a new run')
    finally:
        S.subprocess.run = original_run
    print('GC Sail probe: ordinary rows, witnessed gaps, failed processes and stale traces passed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', choices=['permit-missing', 'ignore-status',
                                              'unwitnessed-gap', 'keep-stale'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-sail-control-', dir=parent) as td:
        root = Path(td)
        module = S
        if args.mutation:
            source = (REPO / 'scripts/run_rv64gc_sail.py').read_text()
            changes = {
                'permit-missing': (
                    'raise SailError(f\'missing expected step {n} ({e["insn"]}); absent evidence is not agreement\')',
                    'continue'),
                'ignore-status': ('if returncode != 0:', 'if False:'),
                'unwitnessed-gap': ("declared is not None and event == ('int', INT_LABELS[declared[1]])",
                                   'declared is not None'),
                'keep-stale': ('trace.unlink(missing_ok=True)', 'pass'),
            }
            old, new = changes[args.mutation]
            assert source.count(old) == 1, 'Sail mutation must match once'
            path = root / 'sail_control.py'
            path.write_text(source.replace(old, new))
            spec = importlib.util.spec_from_file_location('sail_control', path)
            module = importlib.util.module_from_spec(spec)
            import sys
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            module.REPO = REPO
            module.UNIT = REPO / 'profiles/rv64gc-lab-v0'
        check(module, root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
