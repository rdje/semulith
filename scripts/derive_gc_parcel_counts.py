#!/usr/bin/env python3
"""Stage independently derived rv64gc parcel counts without writing guest records.

Each existing record supplies its declared boundary budget and prior observations.
The spec-side author derives all writes and actual fetch attempts independently;
disagreement refuses before a staging manifest can be written. The count migration
remains P4-SYSTEM.12's bind, not an implicit edit by this diagnostic.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import derive_rv64gc_expectations as Q
import dossier_sexp as D
import records_sexp as R
from riscv_asm import Assembler, AsmError

REPO = Path(__file__).resolve().parent.parent
UNIT = REPO / 'profiles/rv64gc-lab-v0'
DEFAULT_OUT = Path('target/p4-system-12/e1d/parcel-counts.json')


class CensusRefused(Exception):
    pass


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive_counts(guests, asm, *, mutation=None):
    sources = sorted(guests.glob('*.s'))
    records = sorted(guests.glob('*.expected.sexp'))
    if not sources or {p.stem for p in sources} != {p.name.removesuffix('.expected.sexp') for p in records}:
        raise CensusRefused('guest sources and expectation records must form a nonempty exact pair set')
    rows = []
    for source in sources:
        record = source.with_suffix('.expected.sexp')
        expected = D.load_expectations(record)
        if expected['program'] != source.name:
            raise CensusRefused(f'{source.name}: expectation program names another source')
        if int(expected['entry'], 0) != Q.ENTRY:
            raise CensusRefused(f'{source.name}: expectation entry differs from the laboratory region')
        run = Q.derive_parcel_guest(source, asm, expected['instructions'])
        if mutation == 'observation':
            run.steps[0].writes[31] = 0x1234
        if mutation == 'extent':
            run.steps[0].fetch += 1
        prior = [{int(reg[1:]): int(value, 16) for reg, value in step['writes'].items()}
                 for step in expected['step']]
        actual = [step.writes for step in run.steps]
        if actual != prior:
            first = next((i for i, (a, b) in enumerate(zip(actual, prior)) if a != b),
                         min(len(actual), len(prior)))
            raise CensusRefused(f'{source.name}: architectural observations differ at boundary {first}')
        fetches = sum(step.fetch for step in run.steps)
        requests = sum(row[0] == 'fetch' for row in run.hart.log)
        if fetches != requests:
            raise CensusRefused(f'{source.name}: parcel count differs from actual request log')
        rows.append({'guest': source.stem, 'boundaries': expected['instructions'],
                     'prior_fetches': expected.get('fetches', expected['instructions']),
                     'parcel_fetches': fetches, 'source_sha256': digest(source),
                     'record_sha256': digest(record)})
    return rows


def manifest(rows):
    # Conservative fingerprint closure: all local Python producers/readers, schema
    # declarations and definition data, plus the unit metadata and paired records.
    # This names instrument inputs as well as inputs to the headline count.
    inputs = set((REPO / 'scripts').glob('*.py'))
    inputs.update((REPO / 'schema').glob('*.sexp'))
    inputs.update((REPO / 'definitions').rglob('*.sexp'))
    inputs.update(UNIT.glob('*.sexp'))
    inputs.update((UNIT / 'guests').glob('*.s'))
    inputs.update((UNIT / 'guests').glob('*.expected.sexp'))
    return {'format_version': 1, 'profile': 'rv64gc-lab-v0',
            'producer': 'scripts/derive_gc_parcel_counts.py',
            'route': 'spec-side explicit-budget parcel execution; no processor engine',
            'inputs': {p.relative_to(REPO).as_posix(): digest(p) for p in sorted(inputs)},
            'guests': rows}


def self_test(asm):
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='parcel-counts-', dir=parent) as td:
        guests = Path(td)
        # Hand-derived counts: two words need four parcels; C + word needs three;
        # a word followed by zero-filled runoff needs two plus one, with no retirement
        # or architectural write for that reserved zero parcel.
        cases = [('word', 'addi x1, x0, 1\naddi x2, x0, 2\n', [{1: 1}, {2: 2}], 4),
                 ('mixed', '.half 0x0085\naddi x2, x0, 2\n', [{1: 1}, {2: 2}], 3),
                 ('runoff', 'addi x1, x0, 1\n', [{1: 1}, {}], 3)]
        for name, source, writes, _ in cases:
            (guests / (name + '.s')).write_text(source)
            doc = {'program': name + '.s', 'entry': f'{Q.ENTRY:#018x}',
                   'instructions': len(writes),
                   'step': [{'n': i, 'insn': 'hand fixture',
                             'writes': {f'x{r}': f'{v:#018x}' for r, v in w.items()},
                             'derivation': 'Hand ADDI/C.ADDI or zero-parcel observation.',
                             'source': 'RVI-RV32I 1.1.4; RVI-C 27.1.5.2/27.1.5.4'}
                            for i, w in enumerate(writes)]}
            (guests / (name + '.expected.sexp')).write_text(
                R.render_forms([D.expectations_to_form(doc)]))
        rows = derive_counts(guests, asm)
        assert {r['guest']: r['parcel_fetches'] for r in rows} == {c[0]: c[3] for c in cases}, 'hand parcel counts'
        assert rows == derive_counts(guests, asm), 'cold repeat changed counts'
        for mutation, reason in [('observation', 'architectural observations differ'),
                                 ('extent', 'parcel count differs from actual request log')]:
            try:
                derive_counts(guests, asm, mutation=mutation)
            except CensusRefused as exc:
                assert reason in str(exc), exc
            else:
                raise AssertionError(f'count census accepted {mutation} mutation')
        out = (guests / 'manifest.json').relative_to(REPO).as_posix()
        assert main(['--out', out]) == 0, 'manifest creation refused'
        assert main(['--check', '--out', out]) == 0, 'fresh manifest drifted'
        path = REPO / out
        damaged = json.loads(path.read_text())
        damaged['guests'][0]['parcel_fetches'] += 1
        path.write_text(json.dumps(damaged, indent=2, sort_keys=True) + '\n')
        assert main(['--check', '--out', out]) == 1, 'incorrect stored count escaped drift check'
    print('GC count self-test: hand word/mixed/runoff counts, repeat, manifest drift and both RED controls pass')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--check', action='store_true', help='compare the existing manifest without writing')
    action.add_argument('--self-test', action='store_true')
    action.add_argument('--mutation', choices=['observation', 'extent'])
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    out = args.out
    if out.is_absolute() or '..' in out.parts or not out.parts or out.parts[0] != 'target':
        parser.error('--out must be a repository-relative target/ path')
    if not (REPO / out).resolve().is_relative_to(REPO):
        parser.error('--out must remain inside the repository')
    try:
        asm = Assembler(UNIT / 'encoding.sexp')
        if args.self_test:
            self_test(asm)
            return 0
        rows = derive_counts(UNIT / 'guests', asm, mutation=args.mutation)
        text = json.dumps(manifest(rows), indent=2, sort_keys=True) + '\n'
        if args.check:
            if not (REPO / out).is_file() or (REPO / out).read_text() != text:
                print('GC parcel counts: DRIFT — rerun scripts/derive_gc_parcel_counts.py', file=sys.stderr)
                return 1
        else:
            (REPO / out).parent.mkdir(parents=True, exist_ok=True)
            (REPO / out).write_text(text)
    except CensusRefused as exc:
        print(f'GC parcel counts: REFUSED — {exc}', file=sys.stderr)
        return 1
    except (Q.Refusal, D.DossierError, AsmError, OSError, ValueError) as exc:
        print(f'GC parcel counts: CANNOT JUDGE — {exc}', file=sys.stderr)
        return 2
    print(f'GC parcel counts: {len(rows)} exact architectural traces; '
          f'{sum(r["boundaries"] for r in rows)} boundaries; '
          f'{sum(r["parcel_fetches"] for r in rows)} actual parcel requests; no guest records written')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
