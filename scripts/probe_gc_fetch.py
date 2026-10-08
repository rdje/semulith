#!/usr/bin/env python3
"""Spec-side Sv39 and exact-parcel controls, without an instruction engine.

PTE fixtures follow RVP-SUPERVISOR 11.1.3.2/11.1.4.1 with Svade; MPRV follows
RVP-MACHINE 2.1.1.6.4. Hand parcels follow RVI-C and the ILEN=32 profile. The
ordered request observations distinguish page walks from actual fetch attempts.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

import derive_rv64gc_expectations as Q

REPO = Path(__file__).resolve().parent.parent


def leaf(author, va=0, flags=0xcf):
    h = author.Hart()
    h.mode = author.S
    h.csr['satp'] = (8 << 60) | (author.ENTRY >> 12)
    h.write(author.ENTRY + ((va >> 30) & 511) * 8, 8,
            ((author.ENTRY >> 12) << 10) | flags)
    return h


def translated(author, parcel):
    h = author.Hart()
    base = author.ENTRY
    h.mode, h.pc = author.S, 0x4ffe
    h.csr['satp'] = (8 << 60) | ((base + 0x1000) >> 12)
    h.write(base + 0x1000, 8, (((base + 0x2000) >> 12) << 10) | 1)
    h.write(base + 0x2000, 8, (((base + 0x3000) >> 12) << 10) | 1)
    h.write(base + 0x3020, 8, (((base + 0x4000) >> 12) << 10) | 0x4b)
    h.write(base + 0x4ffe, 2, parcel)
    return h


def fetches(h):
    return [record for record in h.log if record[0] == 'fetch']


def check(author):
    base = author.ENTRY
    for va in (1 << 38, 0xffffff8000000000):
        h = leaf(author, va)
        assert h.walk(va, 'fetch') == ('fault', 12), 'Sv39 sign bit and upper bits disagree'
        assert not h.log, 'non-canonical VA must fault before any page-table request'
    for va in (0, 0xffffffc000000000):
        h = leaf(author, va)
        assert h.walk(va, 'fetch') == ('pa', base), 'canonical sign extension rejected'
    for bit in range(54, 64):
        h = leaf(author)
        h.write(base, 8, h.read(base, 8) | (1 << bit))
        before = h.mem.copy()
        for kind, cause in (('fetch', 12), ('load', 13), ('store', 15), ('atomic', 15)):
            assert h.walk(0, kind) == ('fault', cause), f'reserved PTE bit {bit} accepted'
        assert h.mem == before, 'Svade walk wrote a PTE'
    for bit in (8, 9):  # RSW belongs to software; G is not reserved either
        h = leaf(author, flags=0xcf | (1 << bit) | 0x20)
        assert h.walk(0, 'fetch') == ('pa', base)
    for bit in (4, 6, 7):
        h = leaf(author, flags=1 | (1 << bit))  # non-leaf U/A/D are reserved
        assert h.walk(0, 'fetch') == ('fault', 12), f'non-leaf reserved bit {bit} accepted'
        assert len(h.log) == 1, 'non-leaf reserved bit must fault before descending'
    h = leaf(author, flags=1)
    h.write(base, 8, (((base + 0x1000) >> 12) << 10) | 1)
    h.write(base + 0x1000, 8, (((base + 0x2000) >> 12) << 10) | 1)
    h.write(base + 0x2000, 8, (((base + 0x3000) >> 12) << 10) | 1)
    try:
        outcome = h.walk(0, 'fetch')
    except (author.Refusal, AssertionError) as exc:
        raise AssertionError('bottom-level pointer must page-fault') from exc
    assert outcome == ('fault', 12), 'bottom-level pointer must page-fault'
    assert h.log == [('walk', base, 8), ('walk', base + 0x1000, 8), ('walk', base + 0x2000, 8)]
    h = leaf(author, flags=1 | 0x20)
    h.write(base, 8, (((base + 0x1000) >> 12) << 10) | 1 | 0x20)
    h.write(base + 0x1000, 8, ((base >> 12) << 10) | 0xcf)
    assert h.walk(0, 'fetch') == ('pa', base), 'non-leaf G must remain valid'
    # MPRV modifies data privilege, including the associated SUM/U checks; fetch ignores it.
    h = leaf(author)
    h.mode = author.M
    h.csr['mstatus'] |= (1 << 17) | (author.S << 11)
    for kind in ('load', 'store', 'atomic'):
        assert h.walk(0, kind) == ('pa', base), 'MPRV data access must use MPP'
    h.log.clear()
    assert h.walk(0, 'fetch') == ('pa', 0) and not h.log, 'MPRV affected instruction fetch'
    h.write(base, 8, ((base >> 12) << 10) | 0xdf)  # user leaf
    author.execute(h, 0x12000073)  # M-mode full fence exposes the edited PTE
    assert h.walk(0, 'load') == ('fault', 13), 'MPRV must apply effective S SUM=0'
    h.csr['mstatus'] |= 1 << 18
    assert h.walk(0, 'load') == ('pa', base), 'MPRV must apply effective S SUM=1'
    h.csr['mstatus'] &= ~(3 << 11)  # MPP=U
    assert h.walk(0, 'load') == ('pa', base)
    h.write(base, 8, ((base >> 12) << 10) | 0xcf)
    author.execute(h, 0x12000073)
    assert h.walk(0, 'load') == ('fault', 13), 'MPRV must apply effective U permission'
    # Exact physical extent and implicit zero bytes beyond the payload.
    h = author.Hart()
    h.pc = base + author.REGION - 2
    h.write(h.pc, 2, 0x0085)
    assert h.fetch_instruction() == ('insn', 0x0085, 2), 'compressed region-end fetch inspected its neighbor'
    assert h.log == [('fetch', h.pc, 2)] and not h.trapped
    h = author.Hart()
    assert h.fetch_instruction() == ('insn', 0, 2), 'implicit in-region zero parcel lost'
    assert h.log == [('fetch', base, 2)]
    h = author.Hart()
    h.pc = base + 2
    h.write(h.pc, 4, 0x00100093)
    assert h.fetch_instruction() == ('insn', 0x00100093, 4)
    assert h.log == [('fetch', base + 2, 2), ('fetch', base + 4, 2)]
    h = author.Hart()
    h.write(base, 4, 0x1234ffff)
    assert h.fetch_instruction() == ('insn', 0x1234ffff, 4), 'wider prefix lost ILEN bits'
    assert len(fetches(h)) == 2
    h = author.Hart()
    h.pc = base + author.REGION - 2
    start = h.pc
    h.write(start, 2, 0x0093)
    assert h.fetch_instruction() == ('fault', 1, start + 2)
    assert h.csr['mepc'] == start and h.csr['mtval'] == start + 2, 'second parcel lost fault VA/start EPC'
    assert len(fetches(h)) == 2 and h.instret == h.time == 0
    for pc, cause in ((base + 1, 0), (base + 3, 0), (base - 2, 1)):
        h = author.Hart()
        h.pc = pc
        assert h.fetch_instruction() == ('fault', cause, pc)
        assert h.csr['mepc'] == pc & ~1 and h.csr['mtval'] == pc, 'EPC bit zero was not masked'
        assert h.log == [('fetch', pc, 2)], 'failed physical request was not counted'
    h = author.Hart()
    h.mode, h.pc = author.S, base + 3
    h.csr['medeleg'], h.csr['stvec'] = 1, base + 0x100
    assert h.fetch_instruction() == ('fault', 0, base + 3)
    assert h.csr['sepc'] == base + 2 and h.csr['stval'] == base + 3
    assert h.pc == base + 0x100
    for to_s in (False, True):
        h = author.Hart()
        h.pc = base + 3
        h.deliver_interrupt(1, to_s)
        assert h.csr['sepc' if to_s else 'mepc'] == base + 2
    h = author.Hart()
    h.write(base, 4, 0x00100093)
    h.refusals = [('fetch', base + 2, 1)]
    assert h.fetch_instruction() == ('fault', 1, base + 2)
    assert h.csr['mtval'] == base + 2, 'second parcel lost fault VA/start EPC'
    assert h.log == [('fetch', base, 2), ('fetch', base + 2, 2)]
    h = author.Hart()
    h.write(base, 2, 0x0001)
    h.refusals = [('fetch', base + 2, 1)]
    assert h.fetch_instruction() == ('insn', 1, 2) and len(fetches(h)) == 1
    # Translated straddles: never walk a compressed neighbor; a needed page fault
    # issues no request for that parcel, while a physical refusal does count one.
    h = translated(author, 0x0085)
    assert h.fetch_instruction() == ('insn', 0x0085, 2)
    assert h.log == [('walk', base + 0x1000, 8), ('walk', base + 0x2000, 8),
                     ('walk', base + 0x3020, 8), ('fetch', base + 0x4ffe, 2)]
    h = translated(author, 0x0093)
    assert h.fetch_instruction() == ('fault', 12, 0x5000)
    assert h.csr['mepc'] == 0x4ffe and h.csr['mtval'] == 0x5000, 'second parcel lost fault VA/start EPC'
    assert h.log[-3:] == [('walk', base + 0x1000, 8), ('walk', base + 0x2000, 8), ('walk', base + 0x3028, 8)]
    assert len(fetches(h)) == 1
    h = translated(author, 0x0093)
    h.write(base + 0x3028, 8, (((base + 0x8000) >> 12) << 10) | 0x4b)
    h.write(base + 0x8000, 2, 0x0010)
    assert h.fetch_instruction() == ('insn', 0x00100093, 4)
    assert fetches(h) == [('fetch', base + 0x4ffe, 2), ('fetch', base + 0x8000, 2)]
    h = translated(author, 0x0085)
    h.refusals = [('walk', base + 0x3020, 8)]
    assert h.fetch_instruction() == ('fault', 1, 0x4ffe) and not fetches(h)
    assert h.log[-1] == ('walk', base + 0x3020, 8), 'failed walk request was not counted'
    h = translated(author, 0x0085)
    h.write(base + 0x3020, 8, (((base + author.REGION) >> 12) << 10) | 0x4b)
    assert h.fetch_instruction() == ('fault', 1, 0x4ffe)
    assert fetches(h) == [('fetch', base + author.REGION + 0xffe, 2)]
    assert h.csr['mtval'] == 0x4ffe, 'physical refusal must report the virtual address'
    assert author.main(['probe', '--check-owned']) == 0
    print('GC fetch probe: canonical/PTE/MPRV repairs and exact parcel schedules passed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    controls = parser.add_mutually_exclusive_group()
    controls.add_argument('--author-revision')
    controls.add_argument('--mutation', choices=['canonical-sign', 'reserved-pte', 'nonleaf-bits',
                                              'bottom-pointer', 'mprv', 'eager-second',
                                              'fault-tval', 'short-ilen', 'unaligned-epc'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-fetch-control-', dir=parent) as td:
        author = Q
        if args.author_revision or args.mutation:
            source = (subprocess.check_output(['git', 'show', f'{args.author_revision}:scripts/derive_rv64gc_expectations.py'], cwd=REPO).decode()
                      if args.author_revision else (REPO / 'scripts/derive_rv64gc_expectations.py').read_text())
            changes = {
                'canonical-sign': ('if va >> 39 != expected_upper:', 'if False:'),
                'reserved-pte': ('or pte >> 54:', ':'),
                'nonleaf-bits': ('if pte & 0xd0:', 'if False:'),
                'bottom-pointer': ('if level == 0:', 'if False:'),
                'mprv': ("if kind != 'fetch' and (self.csr['mstatus'] >> 17) & 1:", 'if False:'),
                'eager-second': ('if low[1] & 3 != 3:', 'if False:'),
                'fault-tval': ('self.deliver(high[1], high[2])', 'self.deliver(high[1], pc)'),
                'unaligned-epc': ('self.csr["mepc"] = self.pc & ~1\n            self.csr["mcause"] = cause',
                                  'self.csr["mepc"] = self.pc\n            self.csr["mcause"] = cause'),
                'short-ilen': ('if low[1] & 3 != 3:', 'if low[1] & 3 != 3 or low[1] & 0x1f == 0x1f:'),
            }
            if args.mutation:
                old, new = changes[args.mutation]
                assert source.count(old) == 1, 'fetch mutation must match once'
                source = source.replace(old, new)
            path = Path(td) / 'fetch_control.py'
            path.write_text(source)
            spec = importlib.util.spec_from_file_location('fetch_control', path)
            author = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = author
            spec.loader.exec_module(author)
            author.REPO = REPO
            author.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        check(author)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
