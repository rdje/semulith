#!/usr/bin/env python3
"""Check author provenance without inferring a record's history from its filename.

The 41 historical word records keep their capture headers; env-irq-sources is fresh. New derivations
name the tracked author and actual route; no engine or reference output is used.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

import derive_rv64gc_expectations as Q
import dossier_sexp as D
from riscv_asm import Assembler

REPO = Path(__file__).resolve().parent.parent


def check(author, root):
    asm = Assembler(REPO / 'profiles/rv64gc-lab-v0/encoding.sexp')

    def neutral(text, route):
        header = text.split('(expectations ', 1)[0]
        assert 'floating-point corpus' not in header, 'generic output inherited FP provenance'
        assert 'BEFORE any engine run' not in header, 'new output invented capture chronology'
        assert 'scripts/derive_rv64gc_expectations.py' in header, 'new output omitted its author'
        assert route in header, 'new output omitted its execution route'

    source = root / 'generic.s'
    source.write_text('addi x1, x0, 1\n')
    text, count = author.run_guest(source, asm)
    neutral(text, 'word route')
    assert count == 1

    # A copied historical basename does not carry the canonical record's history.
    for name in ('f-arith', 'd-arith', 'fp-fs-off', 'a-lrsc-pair', 'env-irq-sources',
                 'm-alias', 'mm-csr-ro-write', 'prio-sv39', 'inj-fp'):
        borrowed = root / (name + '.s')
        borrowed.write_text(source.read_text())
        text, _ = author.run_guest(borrowed, asm)
        neutral(text, 'word route')

    # Raw C.ADDI x1,1 runs through the independent decoder even before C binds.
    source = root / 'c-example.s'
    source.write_text('.half 0x0085\n')
    text, count = author.run_parcel_guest(source, asm, 1)
    neutral(text, 'explicit-budget parcel route (C-capable)')
    out = root / 'c-example.expected.sexp'
    out.write_text(text)
    doc = D.load_expectations(out)
    assert count == doc['instructions'] == 1
    assert doc['step'][0]['writes'] == {'x1': '0x0000000000000001'}, 'C observation changed'
    judged = subprocess.run(['python3', 'scripts/check_sexp_schema.py',
                             str(out.relative_to(REPO)), 'schema/expectations.sexp'],
                            cwd=REPO, capture_output=True, text=True)
    assert judged.returncode == 0, judged.stderr

    # The same owned source on a NEW route is a re-derivation, not its old capture.
    owned = REPO / 'profiles/rv64gc-lab-v0/guests/f-arith.s'
    text, _ = author.run_parcel_guest(owned, asm, 1)
    neutral(text, 'explicit-budget parcel route (C-capable)')
    try:
        author.emit(source, [], 0, [], route='unknown')
    except author.Refusal as exc:
        assert 'unknown expectation author route' in str(exc)
    else:
        raise AssertionError('unknown author route was accepted')
    assert len(author.OWNED_GUESTS) == 41
    assert author.PARCEL_OWNED_GUESTS == {'env-irq-sources': 13}
    fresh = REPO / 'profiles/rv64gc-lab-v0/guests/env-irq-sources.s'
    text, count = author.check_owned_guest(fresh, asm)
    neutral(text, 'explicit-budget parcel route (C-capable)')
    assert count == 13 and text == fresh.with_suffix('.expected.sexp').read_text()
    assert author.main(['probe', '--check-owned']) == 0
    print('GC provenance probe: generic/9 borrowed names/C/schema/new owned route; 41 historical captures + one fresh record exact')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--author-revision')
    changes = {
        'filename-history': ("and path.resolve() == (REPO / 'profiles/rv64gc-lab-v0/guests' / path.name).resolve())", ")"),
        'parcel-history': ("route == 'word' and path.stem in OWNED_GUESTS",
                           "path.stem in OWNED_GUESTS"),
        'parcel-route': ("route='parcels'), len(run.steps)", "route='word'), len(run.steps)"),
        'fp-fallback': ("if not historical:", "if not historical and path.stem != 'generic':"),
    }
    control.add_argument('--mutation', choices=changes)
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-provenance-', dir=parent) as td:
        author = Q
        if args.author_revision or args.mutation:
            source = (subprocess.check_output(['git', 'show',
                       f'{args.author_revision}:scripts/derive_rv64gc_expectations.py'], cwd=REPO).decode()
                      if args.author_revision else (REPO / 'scripts/derive_rv64gc_expectations.py').read_text())
            if args.mutation:
                old, new = changes[args.mutation]
                assert source.count(old) == 1, 'provenance mutation must match once'
                source = source.replace(old, new)
            path = Path(td) / 'provenance_control.py'
            path.write_text(source)
            spec = importlib.util.spec_from_file_location('provenance_control', path)
            author = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = author
            spec.loader.exec_module(author)
            author.REPO = REPO
        check(author, Path(td))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
