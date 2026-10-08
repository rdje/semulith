#!/usr/bin/env python3
"""Re-derive the owned author corpus and judge reserved words without running an engine.

The reserved fixtures come from the RVI-RV32I/RV64I opcode maps. Mutations remove
fixed-bit guards or change signed division's rounding; committed spec-derived records
must discriminate. Temporary control modules stay under target/p4-system-12.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import tempfile

import derive_rv64gc_expectations as Q

REPO = Path(__file__).resolve().parent.parent
RESERVED = [0x04000033, 0x04004033, 0x04006033, 0x04007033,
            0x04001013, 0x04005013, 0x0000200F]


def check(author):
    # Refusal must not commit a target effect.
    for word in RESERVED:
        hart = author.Hart()
        before = (hart.pc, hart.x.copy(), hart.csr.copy(), hart.mem.copy())
        try:
            author.execute(hart, word)
        except author.Refusal as exc:
            assert 'reserved' in str(exc), str(exc)
        else:
            raise AssertionError(f'reserved word {word:#010x} accepted')
        assert (hart.pc, hart.x, hart.csr, hart.mem) == before, 'refusal changed the hart'
    hart = author.Hart()
    try:
        author.execute(hart, 0xF1102273)  # CSRRS x4,mvendorid,x0: real, unmodeled CSR
    except author.Refusal as exc:
        assert 'csr 0xf11' in str(exc), str(exc)
    else:
        raise AssertionError('unmodeled CSR did not refuse by name')
    # A 1-GiB leaf keeps this permission fixture independent of the instruction engine.
    hart = author.Hart()
    hart.mode = author.S
    hart.csr['satp'] = (8 << 60) | (author.ENTRY >> 12)
    va = 0x80000000
    root_pte = author.ENTRY + 2 * 8
    hart.write(root_pte, 8, ((author.ENTRY >> 12) << 10) | 0xDF)  # V/R/W/X/U/A/D
    assert hart.walk(va, 'load') == ('fault', 13), 'SUM=0 must reject S data on U pages'
    hart.csr['mstatus'] |= 1 << 18
    assert hart.walk(va, 'load') == ('pa', author.ENTRY), 'SUM=1 permits S data on U pages'
    assert hart.walk(va, 'fetch') == ('fault', 12), 'SUM never permits S fetch on U pages'
    hart.mode = 0
    assert hart.walk(va, 'load') == ('pa', author.ENTRY), 'U mode can read a U page'
    hart.write(root_pte, 8, ((author.ENTRY >> 12) << 10) | 0xCB)  # V/R/X/A/D, U=0
    assert hart.walk(va, 'load') == ('fault', 13), 'U mode cannot read an S page'
    hart.mode = author.S
    hart.write(root_pte, 8, ((author.ENTRY >> 12) << 10) | 0xC9)  # V/X/A/D, R=0
    assert hart.walk(va, 'load') == ('fault', 13), 'MXR=0 rejects an X-only load'
    hart.csr['mstatus'] |= 1 << 19
    assert hart.walk(va, 'load') == ('pa', author.ENTRY), 'MXR=1 permits an X-only load'
    assert author.main(['probe', '--check-owned']) == 0, 'owned expectation corpus drift'
    print('GC author probe: 7 reserved words, named refusal, permissions and owned corpus passed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', choices=['reserved-op', 'reserved-shift', 'division-rounding',
                                              'ignore-sum', 'ignore-mxr', 'ignore-user'])
    args = parser.parse_args()
    if not args.mutation:
        check(Q)
        return 0
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-author-control-', dir=parent) as td:
        source = (REPO / 'scripts/derive_rv64gc_expectations.py').read_text()
        changes = {
            'reserved-op': (
                'if funct7 != 0 and not (funct7 == 0x20 and f3 in (0, 5)):',
                'if False:'),
            'reserved-shift': (
                'if ((f3 == 1 and word >> 26 != 0)\n'
                '                or (f3 == 5 and word >> 26 not in (0, 0x10))):',
                'if False:'),
            'division-rounding': ('q = abs(a) // abs(b)',
                                  'q = (abs(a) + abs(b) - 1) // abs(b)'),
            'ignore-sum': ('kind == "fetch" or not (self.csr["mstatus"] >> 18) & 1', 'True'),
            'ignore-mxr': ('r or (x and (self.csr["mstatus"] >> 19) & 1)', 'r'),
            'ignore-user': ('if mode == 0 and not u:', 'if False:'),
        }
        old, new = changes[args.mutation]
        assert source.count(old) == 1, 'author mutation must match once'
        path = Path(td) / 'author_control.py'
        path.write_text(source.replace(old, new))
        spec = importlib.util.spec_from_file_location('author_control', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.REPO = REPO
        module.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        check(module)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
