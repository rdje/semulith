#!/usr/bin/env python3
"""Judge the RV64I -> RV64GC mirror, including the declared parcel-count migration.

Before C composes, unchanged files must be byte-identical. With C, independently
derive every supplied guest's writes and parcel requests, then transform only the
owner's direct fetches field for comparison. Seven historical semantic/comment
re-derivations remain explicit; count changes cannot keep a stale exception alive.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys
import tempfile

import derive_gc_parcel_counts as Counts
import dossier_sexp as D
import records_sexp as R
from riscv_asm import Assembler, AsmError
import sexp as S
from expectations_text import with_fetches

REPO = Path(__file__).resolve().parent.parent
OWNER = REPO / 'profiles/rv64i-lab-v0/guests'
MIRROR = REPO / 'profiles/rv64gc-lab-v0/guests'
ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
REDERIVED = frozenset(('fault-jal-mis', 'fault-jalr-mis', 'it-prio-jump',
                       'it-fencei', 'min-fencei', 'dir-selfmod-fence', 'fault-selfmod'))


def judge(owner, mirror, asm, *, parcels, rederived=REDERIVED, mutation=None):
    if not owner.is_dir() or not mirror.is_dir():
        raise Counts.CensusRefused('owner and mirror must be guest directories')
    if parcels:
        rows = Counts.derive_counts(mirror, asm)
        for row in rows:
            if row['prior_fetches'] != row['parcel_fetches'] and mutation != 'ignore-counts':
                raise Counts.CensusRefused(f'{row["guest"]}: declared parcel count differs from actual requests')
    count = adjusted = different = 0
    for source in sorted(owner.glob('*.s')):
        paired = mirror / source.name
        if not paired.is_file():
            continue  # only the selected mirror subset is required (c-scope.c)
        if source.read_bytes() != paired.read_bytes() and mutation != 'ignore-source':
            raise Counts.CensusRefused(f'{source.name}: source mirror is not byte-identical')
        count += 1
    seen = set()
    for record in sorted(mirror.glob('*.expected.sexp')):
        original = owner / record.name
        if not original.is_file():
            continue
        name = record.name.removesuffix('.expected.sexp')
        seen.add(name)
        # read_text() normalizes CRLF: that would silently exempt a non-count edit.
        before = original.read_bytes().decode('utf-8')
        after = record.read_bytes().decode('utf-8')
        baseline = before
        if parcels:
            expected = D.load_expectations(record)
            baseline = with_fetches(before, expected.get('fetches', expected['instructions']))
        if baseline == after:
            if name in rederived and mutation != 'ignore-stale':
                raise Counts.CensusRefused(f'{name}: recorded re-derivation is stale after count normalization')
            if before == after:
                count += 1
            else:
                adjusted += 1
        elif name in rederived:
            different += 1
        elif mutation != 'ignore-noncount':
            raise Counts.CensusRefused(f'{name}: non-count mirror drift is not a recorded re-derivation')
    missing = rederived - seen
    if missing:
        raise Counts.CensusRefused(f'recorded re-derivation has no mirror pair: {sorted(missing)}')
    return (f'the base mirror holds: {count} file(s) byte-identical, '
            f'{adjusted} independently checked count-only migration(s), '
            f'{different} recorded re-derivation(s)')


def judge_unit(owner, mirror, encoding, *, rederived=REDERIVED):
    asm = Assembler(encoding)
    return judge(owner, mirror, asm, parcels='c.nop' in asm.insns, rederived=rederived)


def self_test(asm, mutation):
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='mirror-', dir=parent) as td:
        owner, mirror = Path(td) / 'owner', Path(td) / 'mirror'
        owner.mkdir(); mirror.mkdir()
        cases = [('word', 'addi x1, x0, 1\naddi x2, x0, 2\n', [{1: 1}, {2: 2}], 4),
                 ('mixed', '.half 0x0085\naddi x2, x0, 2\n', [{1: 1}, {2: 2}], 3),
                 ('runoff', 'addi x1, x0, 1\n', [{1: 1}, {}], 3)]
        for name, source, writes, fetches in cases:
            (owner / (name + '.s')).write_text(source)
            doc = {'program': name + '.s', 'entry': '0x0000000080000000',
                   'instructions': len(writes),
                   'step': [{'n': i, 'insn': 'hand observation',
                             'writes': {f'x{r}': f'{v:#018x}' for r, v in w.items()},
                             'derivation': 'Independent hand ADDI or reserved-zero observation.',
                             'source': 'RVI-RV32I 1.1.4; RVI-C 27.1.5'} for i, w in enumerate(writes)]}
            text = ';; literal (fetches 99)\n' + R.render_forms([D.expectations_to_form(doc)])
            (owner / (name + '.expected.sexp')).write_text(text)
        shutil.copytree(owner, mirror, dirs_exist_ok=True)
        check = lambda: judge(owner, mirror, asm, parcels=True, rederived=frozenset(), mutation=mutation)

        def refused(fn, reason):
            try:
                fn()
            except Counts.CensusRefused as exc:
                assert reason in str(exc), str(exc)
            else:
                raise AssertionError(f'accepted {reason}')

        assert '6 file(s) byte-identical' in judge(owner, mirror, asm, parcels=False, rederived=frozenset())
        for name, _, _, fetches in cases:
            path = mirror / (name + '.expected.sexp')
            path.write_text(with_fetches(path.read_text(), fetches))
        assert '3 independently checked count-only' in check()
        assert check() == check(), 'mirror repeat differs'
        refused(lambda: judge(owner, mirror, asm, parcels=False, rederived=frozenset()), 'non-count mirror drift')
        # Exercise the same composition selection as the public command, regardless
        # of whether the live unit has reached its bind yet.
        root = Path(td) / 'composition'
        shutil.copytree(REPO / 'definitions', root / 'definitions')
        unit = root / 'profiles/rv64gc-lab-v0'
        unit.mkdir(parents=True)
        for name in ('profile.sexp', 'state.sexp'):
            shutil.copyfile(ENCODING.parent / name, unit / name)
        original = ENCODING.read_text()
        full = original.replace('(slot (id c) (requires "riscv/c"))', '(extensions "riscv/c")')
        (unit / 'encoding.sexp').write_text(full)
        assert '3 independently checked count-only' in judge_unit(owner, mirror, unit / 'encoding.sexp', rederived=frozenset())
        (unit / 'encoding.sexp').write_text(full.replace('(extensions "riscv/c")', ''))
        refused(lambda: judge_unit(owner, mirror, unit / 'encoding.sexp', rederived=frozenset()), 'non-count mirror drift')
        path = mirror / 'word.expected.sexp'
        saved = path.read_text()
        path.write_text(with_fetches(saved, 3))
        refused(check, 'declared parcel count')
        path.write_text(saved + ';; silent comment edit\n')
        refused(check, 'non-count mirror drift')
        path.write_bytes(saved.replace('\n', '\r\n').encode('utf-8'))
        refused(check, 'non-count mirror drift')
        path.write_text(saved.replace('0x0000000000000001', '0x0000000000000009'))
        refused(check, 'architectural observations differ')
        path.write_text(saved)
        source = mirror / 'word.s'
        source.write_text(source.read_text() + '# source comment drift\n')
        refused(check, 'source mirror is not byte-identical')
        shutil.copyfile(owner / 'word.s', source)
        path.write_text(saved + ';; declared historical semantic/comment re-derivation\n')
        special = lambda: judge(owner, mirror, asm, parcels=True, rederived=frozenset(('word',)), mutation=mutation)
        assert '1 recorded re-derivation' in special()
        path.write_text(saved)
        refused(special, 're-derivation is stale')
        # Both textual traps survive, while only the direct count changes.
        tricky = '(comment "escaped \\" (fetches 99)")\n(expectations (program "x.s") (entry "0x80000000") (instructions 1) (fetches 2) (nested (fetches 33)))\n'
        assert with_fetches(tricky, 4) == tricky.replace('(fetches 2)', '(fetches 4)')
        try:
            with_fetches(tricky.replace('(fetches 2)', '(fetches 2) (fetches 3)'), 4)
        except S.SexpError as exc:
            assert 'expected exactly one (fetches' in str(exc), str(exc)
        else:
            raise AssertionError('duplicate field accepted')
        for value in (-1, True, '2) (extra 1'):
            try:
                with_fetches(tricky, value)
            except S.SexpError as exc:
                assert 'nonnegative integer' in str(exc), str(exc)
            else:
                raise AssertionError('invalid count accepted')
    print('GC mirror self-test: hand extents, repeat, count/comment/write/source/stale controls and literal fields pass')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', type=Path, default=OWNER)
    parser.add_argument('--mirror', type=Path, default=MIRROR)
    parser.add_argument('--encoding', type=Path, default=ENCODING)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--mutation', choices=['ignore-counts', 'ignore-noncount', 'ignore-source', 'ignore-stale'])
    args = parser.parse_args()
    if args.mutation and not args.self_test:
        parser.error('--mutation requires --self-test')
    try:
        if args.self_test:
            self_test(Assembler(args.encoding), args.mutation)
        else:
            print(judge_unit(args.owner, args.mirror, args.encoding))
    except (Counts.CensusRefused, AssertionError) as exc:
        print(f'GUEST-GEN: MIRROR DRIFT — {exc}', file=sys.stderr)
        return 1
    except (Counts.Q.Refusal, D.DossierError, AsmError, S.SexpError, OSError, ValueError) as exc:
        print(f'GUEST-GEN: MIRROR CANNOT JUDGE — {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
