#!/usr/bin/env python3
"""Stage the RV64+D C corpus from specification-side rules before the C bind.

Budgets and hand checkpoints below are declared before any processor-engine run.
The independent author supplies observations; the assembler shares riscv-opcodes
ancestry with the engine. This is finite specification-derived test evidence,
not a processor acceptance claim. All outputs stay under target/.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path
import shutil
import sys
import tempfile

import check_sexp_schema as Schema
import derive_gc_parcel_counts as Counts
import derive_rv64gc_expectations as Q
import dossier_sexp as D
import records_sexp as R
from riscv_asm import Assembler, AsmError

REPO = Path(__file__).resolve().parent.parent
UNIT = REPO / 'profiles/rv64gc-lab-v0'
OUT = REPO / 'target/p4-system-12/e1d/corpus'
MASK = (1 << 64) - 1


@dataclass
class Guest:
    name: str
    lines: list[str]
    budget: int
    final: dict[int, int] = field(default_factory=dict)
    check: str = ''


def programs(asm):
    guests = [
        Guest('c-immediates', [
            'c.li x1, -32', 'c.addi x1, 31', 'c.addi x1, 1',
            'c.li x3, 31', 'c.addi x3, -32', 'c.lui x4, -32', 'c.lui x5, 31',
            'c.li x2, 16', 'c.addi16sp -512', 'c.addi16sp 496',
            'c.addi4spn x8, 1020', 'addi x2, x0, -1', 'c.addi16sp 16',
            'c.addi4spn x15, 4', 'c.nop'], 15,
            {1: 0, 2: 15, 3: -1, 4: -131072, 5: 126976, 8: 1020, 15: 19}),
        Guest('c-alu', [
            'c.li x8, -1', 'c.srli x8, 63', 'c.slli x8, 63', 'c.srai x8, 63',
            'c.andi x8, -32', 'c.li x9, 1', 'c.add x8, x9', 'c.sub x8, x9',
            'c.and x8, x9', 'c.or x8, x9', 'c.xor x8, x9', 'c.mv x10, x9',
            'c.add x10, x10', 'c.slli x10, 0', 'c.srli x8, 0', 'c.srai x8, 0',
            'c.li x11, 3', 'c.sub x8, x11'],
            18, {8: -3, 9: 1, 10: 2, 11: 3}),
        Guest('c-word', [
            'lui x8, 524288', 'addi x8, x8, -1', 'c.li x9, 1',
            'c.addw x8, x9', 'c.subw x8, x9', 'c.addiw x8, 1',
            'c.addiw x8, 0', 'c.addiw x8, -32', 'c.addw x9, x9', 'c.subw x9, x9'],
            10, {8: 0x7fffffe0, 9: 0}),
        Guest('c-hints', [
            'c.li x1, 7', 'c.li x8, 9', 'c.addi x1, 0', 'c.li x0, 31',
            'c.lui x0, 1', 'c.slli x0, 1', 'c.mv x0, x1', 'c.add x0, x1',
            'c.srli x8, 0', 'c.srai x8, 0', 'c.nop 1'], 11, {0: 0, 1: 7, 8: 9}),
        Guest('c-memory', [
            'auipc x2, 0', 'addi x2, x2, 1536', 'c.addi4spn x8, 16',
            'c.li x9, -32', 'c.sw x8, x9, 124', 'c.lw x10, x8, 124',
            'c.sd x8, x9, 248', 'c.ld x11, x8, 248', 'c.swsp x9, 252',
            'c.lwsp x1, 252', 'c.sdsp x9, 504', 'c.ldsp x3, 504',
            'addi x5, x0, 3', 'slli x5, x5, 13', 'csrrs x0, mstatus, x5',
            'fmv.d.x f9, x9', 'c.fsd x8, f9, 248', 'c.fld f8, x8, 248',
            'fmv.x.d x12, f8', 'c.fsdsp f9, 504', 'c.fldsp f1, 504',
            'fmv.x.d x13, f1'], 22, {1: -32, 3: -32, 10: -32, 11: -32, 12: -32, 13: -32}, 'fp-memory'),
        Guest('c-links', [
            'auipc x1, 0', 'addi x1, x1, 14', 'c.jalr x1', 'c.j after',
            '.half 0', 'sub: c.addi x10, 1', 'c.jr x1',
            'after: c.mv x11, x1', 'addi x12, x0, 7', 'c.j finish',
            '.half 0', 'finish: c.nop'], 10,
            {1: Q.ENTRY + 10, 10: 1, 11: Q.ENTRY + 10, 12: 7}, 'links'),
        Guest('c-branches', [
            'c.li x8, 0', 'c.beqz x8, zero', 'addi x9, x0, 99',
            'zero: c.li x9, 1', 'c.bnez x9, one', 'addi x10, x0, 99',
            'one: c.bnez x8, finish', 'c.beqz x9, finish',
            'c.li x10, 7', 'finish: c.nop'], 8, {8: 0, 9: 1, 10: 7}),
        Guest('c-backward', ['c.li x8, 2', 'loop: c.addi x8, -1',
                             'c.bnez x8, loop', 'c.mv x9, x8'], 6, {8: 0, 9: 0}),
        Guest('c-j-limits', ['c.li x8, 2', 'c.j 2046'] + ['.half 0x0001'] * 1022
              + ['c.addi x8, -1', 'c.j -2048'], 7, {8: 0}, 'jump-limits'),
        Guest('c-lrsc', ['auipc x8, 0', 'addi x8, x8, 1024', 'c.li x9, 5',
                         'c.sd x8, x9, 0', 'lr.d x10, (x8)', 'c.addi x10, 1',
                         'c.li x11, -1', 'sc.d x11, x10, (x8)', 'c.ld x12, x8, 0'],
              9, {10: 6, 11: 0, 12: 6}, 'lrsc'),
        Guest('c-irq', ['lui x31, 0x80000', 'csrrs x0, menvcfg, x31',
                        'auipc x1, 0', 'addi x1, x1, 40', 'csrrw x0, mtvec, x1',
                        'addi x2, x0, 32', 'csrrw x0, mie, x2', 'addi x3, x0, 11',
                        'csrrw x0, stimecmp, x3', 'csrrsi x0, mstatus, 8',
                        'c.li x10, 1', 'c.addi x10, 1', 'c.j done', 'c.nop',
                        'csrrs x7, mcause, x0', 'csrrs x8, mepc, x0',
                        'csrrw x0, mie, x0', 'mret', 'done: c.nop'],
              19, {7: (1 << 63) | 5, 8: Q.ENTRY + 42, 10: 2}, 'irq'),
        Guest('c-wide-illegal', ['auipc x1, 0', 'addi x1, x1, 24',
                                'csrrw x0, mtvec, x1', '.word 0xffffffff',
                                'addi x20, x0, 7', 'c.j done', 'c.nop',
                                'csrrs x7, mcause, x0', 'csrrs x8, mtval, x0',
                                'csrrs x9, mepc, x0', 'addi x9, x9, 4',
                                'csrrw x0, mepc, x9', 'mret', 'done: c.nop'],
              13, {7: 2, 8: 0xffffffff, 9: Q.ENTRY + 16, 20: 7}, 'trap'),
    ]

    def trap(name, instruction, tval, cause=2, check='trap'):
        # Layout: the short trigger is at +12, handler at +20, done at +44.
        lines = ['auipc x1, 0', 'addi x1, x1, 20', 'csrrw x0, mtvec, x1',
                 instruction, 'addi x20, x0, 7', 'c.j done',
                 'csrrs x7, mcause, x0', 'csrrs x8, mtval, x0', 'csrrs x9, mepc, x0',
                 'addi x9, x9, 2', 'csrrw x0, mepc, x9', 'mret', 'done: c.nop']
        return Guest(name, lines, 13, {7: cause, 8: tval, 9: Q.ENTRY + 14, 20: 7}, check)

    # Reserved operands from 27.1.3.1, 27.1.4, 27.1.5 and the RV64 listing.
    for name, bits in [('zero', 0x0000), ('addi16sp', 0x6101), ('lui', 0x6181),
                       ('addiw', 0x2001), ('lwsp', 0x4002), ('ldsp', 0x6002),
                       ('jr', 0x8002), ('ca', 0x9c41), ('quadrant0', 0x8000)]:
        guests.append(trap('c-res-' + name, f'.half {bits:#06x}', bits))
    guests.append(trap('c-breakpoint', 'c.ebreak', Q.ENTRY + 12, 3))
    for name, insn, bits in [('fld', 'c.fld f8, x8, 0', 0x2000),
                            ('fldsp', 'c.fldsp f1, 0', 0x2082),
                            ('fsd', 'c.fsd x8, f9, 0', 0xa004),
                            ('fsdsp', 'c.fsdsp f1, 0', 0xa006)]:
        guests.append(trap('c-off-' + name, insn, bits, check='off'))

    # Reuse the repository's public guest program, not its expected values. Its
    # first VA page maps to itself; the next maps to PA +0x5000. Remove X from that
    # second leaf. The compressed variant changes only PA +0xffe to C.NOP.
    original = (UNIT / 'guests/sv39-straddle.s').read_text().splitlines()
    units = asm.assemble_units(original, Q.ENTRY)
    assert sum(u.text == 'addi x10, x10, 1099' for u in units) == 1, 'straddle PTE source boundary'
    assert next(u.value for u in units if u.pc == Q.ENTRY + 0xffc) >> 16 == 0x0a93, 'straddle lower parcel boundary'
    for name, compressed, budget in [('c-page-end', True, 52), ('c-page-straddle', False, 51)]:
        lines = []
        for unit in units:
            line = unit.text
            if line == 'addi x10, x10, 1099':
                line = 'addi x10, x10, 1091'  # 0x44b -> 0x443: V/R/A, no X.
            if compressed and unit.pc == Q.ENTRY + 0xffc:
                line = f'.word {((unit.value & 0xffff) | (1 << 16)):#010x}'
            lines.append(line)
        saved = Q.ENTRY + (0x1000 if compressed else 0xffe)
        guests.append(Guest(name, lines, budget, {7: 12, 8: Q.ENTRY + 0x1000,
                                                9: saved + 4, 21: 0, 22: 0}, name))
    return guests


def validate_record(path, run):
    expected = D.load_expectations(path)
    actual = [step.writes for step in run.steps]
    prior = [{int(reg[1:]): int(value, 16) for reg, value in step['writes'].items()}
             for step in expected['step']]
    if actual != prior:
        raise Counts.CensusRefused(f'{path.name}: staged architectural observations differ')
    requests = sum(row[0] == 'fetch' for row in run.hart.log)
    if expected['instructions'] != len(run.steps) or expected.get('fetches', expected['instructions']) != requests:
        raise Counts.CensusRefused(f'{path.name}: staged extent differs from actual requests')


def build(root, *, mutation=None):
    unit = root / 'profiles/rv64gc-lab-v0'
    guests_dir = unit / 'guests'
    guests_dir.mkdir(parents=True)
    shutil.copytree(REPO / 'definitions', root / 'definitions')
    for name in ('profile.sexp', 'state.sexp'):
        shutil.copyfile(UNIT / name, unit / name)
    encoding = (UNIT / 'encoding.sexp').read_text()
    slot = '(slot (id c) (requires "riscv/c"))'
    if slot in encoding:
        encoding = encoding.replace(slot, '(extensions "riscv/c")').replace('(status partial)', '(status complete)')
    elif '(extensions "riscv/c")' not in encoding:
        raise Counts.CensusRefused('production unit declares neither C slot nor C composition')
    (unit / 'encoding.sexp').write_text(encoding)
    asm = Assembler(unit / 'encoding.sexp')
    guests = programs(asm)
    assert len({g.name for g in guests}) == len(guests), 'duplicate staged guest'
    rows, covered = [], set()
    schema = Schema.load_schema(REPO / 'schema/expectations.sexp')
    for guest in guests:
        source = guests_dir / (guest.name + '.s')
        source.write_text('# P4-SYSTEM.12 e1d2: spec-side C corpus, budget declared by the producer.\n'
                          + '\n'.join(guest.lines) + '\n')
        run = Q.derive_parcel_guest(source, asm, guest.budget)
        for reg, value in guest.final.items():
            assert run.hart.x[reg] == value & MASK, f'{guest.name}: hand checkpoint x{reg}'
        if guest.check == 'links':
            assert [s.pc - Q.ENTRY for s in run.steps] == [0, 4, 8, 14, 16, 10, 18, 20, 24, 28], 'mixed links/byte PCs'
        elif guest.check == 'jump-limits':
            assert [s.pc - Q.ENTRY for s in run.steps] == [0, 2, 2048, 2050, 2, 2048, 2050], 'jump signed limits'
        elif guest.check == 'fp-memory':
            assert run.hart.f[8] == run.hart.f[1] == (-32 & MASK) and run.hart.csr['fflags'] == 0, 'D memory raw bits/flags'
        elif guest.check in ('trap', 'off'):
            assert run.hart.instret == 12, 'short trap retired'
            if guest.check == 'off':
                assert not any(r[0] in ('load', 'store') for r in run.hart.log), 'FS Off issued data access'
        elif guest.check.startswith('c-page-'):
            first = run.steps[44]
            assert first.pc == Q.ENTRY + 0xffe and first.fetch == 1, 'page-end first parcel'
            assert sum(s.fetch for s in run.steps) == 101, 'translated parcel attempts'
            if guest.check == 'c-page-end':
                assert first.deriv.startswith('C.NOP') and run.steps[45].fetch == 0, 'compressed neighbor walked early'
            else:
                assert 'fetch cause 12' in first.deriv, 'second parcel did not fault before effects'
        elif guest.check == 'lrsc':
            assert run.hart.reservation is None and run.hart.read(Q.ENTRY + 1024, 8) == 6, 'C constrained LR/SC result'
        elif guest.check == 'irq':
            assert run.steps[11].pc == Q.ENTRY + 42 and run.steps[11].fetch == 0, 'interrupt compressed boundary PC'
            assert run.hart.instret == 18, 'interrupt boundary retired'
        for step in run.steps:
            insn = step.insn.split()[0]
            # A source annotation at an interrupt/fetch-fault boundary is not an
            # executed form. The independent expansion supplies this derivation.
            if insn.startswith('c.') and step.deriv.startswith(insn.upper() + ' uses its declared base operation'):
                covered.add(insn)
        text = Q.emit(source, run.steps, guest.budget, run.never, run.refusals, route='parcels')
        expected = source.with_suffix('.expected.sexp')
        expected.write_text(text)
        if mutation and not rows:
            doc = D.load_expectations(expected)
            if mutation == 'observation':
                doc['step'][0]['writes']['x31'] = '0x0000000000001234'
            else:
                doc['fetches'] = sum(s.fetch for s in run.steps) + 1
            expected.write_text(R.render_forms([D.expectations_to_form(doc)]))
        errors = Schema.validate_file(expected, *schema)
        if errors:
            raise Counts.CensusRefused('; '.join(errors))
        validate_record(expected, run)
        rows.append({'guest': guest.name, 'boundaries': guest.budget,
                     'parcel_fetches': sum(s.fetch for s in run.steps),
                     'source_sha256': Counts.digest(source), 'record_sha256': Counts.digest(expected)})
    forms = {name for name in asm.insns if name.startswith('c.')}
    assert covered == forms and len(forms) == 37, f'C coverage differs: missing {forms - covered}, extra {covered - forms}'
    data = Counts.manifest([])
    data.update(producer='scripts/stage_gc_c_corpus.py',
                route='independent spec-side full-C staging before processor-engine execution',
                guests=rows, compressed_forms=sorted(covered))
    (guests_dir / 'manifest.json').write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    return guests_dir, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--check', action='store_true')
    action.add_argument('--mutation', choices=['observation', 'extent'])
    args = parser.parse_args()
    if not OUT.resolve().is_relative_to(REPO):
        parser.error('staging output must remain inside the repository')
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='c-corpus-', dir=parent) as td:
            guests, rows = build(Path(td), mutation=args.mutation)
            files = sorted(p for p in guests.iterdir() if p.is_file())
            if args.check:
                if not OUT.is_dir() or {p.name for p in OUT.iterdir()} != {p.name for p in files} or any(
                        not (OUT / p.name).is_file() or (OUT / p.name).read_bytes() != p.read_bytes() for p in files):
                    print('C corpus staging: DRIFT — rerun scripts/stage_gc_c_corpus.py', file=sys.stderr)
                    return 1
            else:
                if OUT.exists() and {p.name for p in OUT.iterdir()} - {p.name for p in files}:
                    raise Counts.CensusRefused('staging destination has unexpected files; preserve and inspect them first')
                OUT.mkdir(parents=True, exist_ok=True)
                for path in files:
                    shutil.copyfile(path, OUT / path.name)
    except Counts.CensusRefused as exc:
        print(f'C corpus staging: REFUSED — {exc}', file=sys.stderr)
        return 1
    except (Q.Refusal, D.DossierError, AsmError, OSError, ValueError) as exc:
        print(f'C corpus staging: CANNOT JUDGE — {exc}', file=sys.stderr)
        return 2
    print(f'C corpus staging: {len(rows)} guests, 37 forms, '
          f'{sum(r["boundaries"] for r in rows)} declared boundaries, '
          f'{sum(r["parcel_fetches"] for r in rows)} parcels; no production files written')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
