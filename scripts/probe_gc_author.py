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
import re
import sys
import tempfile

import derive_rv64gc_expectations as Q
import frozen_owned as Frozen

REPO = Path(__file__).resolve().parent.parent
RESERVED = [0x04000033, 0x04004033, 0x04006033, 0x04007033,
            0x04001013, 0x04005013, 0x0000200F]


def check_directive_keys(author):
    """`{new}` resolves on both routes, even for a write the writes table drops; nothing unresolved reaches a record."""
    asm = author.Assembler(Frozen.ENCODING)
    own_value = ['addi x5, x0, 0  #: x5 already holds {new}. | RVI-RV32I §1.1.4',
                 'addi x5, x0, 7  #: now {new}. | RVI-RV32I §1.1.4']
    words = ['0x0000000000000000', '0x0000000000000007']

    def word_route(lines):
        parent = REPO / 'target/p4-system-12'
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='gc-author-keys-', dir=parent) as td:
            guest = Path(td) / 'keys.s'
            guest.write_text('\n'.join(lines + ['ebreak']) + '\n')
            return re.findall(r'\(derivation "(.*?)"\)', author.run_guest(guest, asm)[0])

    def parcel_route(lines):
        run = author._derive_parcel_lines(lines, asm, len(lines), program='keys.s')
        return [step.deriv for step in run.steps]

    for name, route in (('word', word_route), ('parcel', parcel_route)):
        derived = route(own_value)
        assert derived[:2] == [f'x5 already holds {words[0]}.', f'now {words[1]}.'], f'{name} route: {derived[:2]}'
        for directive, key in (('addi x0, x0, 1  #: x0 takes no write, {new}. | RVI-RV32I §1.1.4', '{new}'),
                               ('addi x5, x0, 1  #: there is no such key, {old}. | RVI-RV32I §1.1.4', '{old}')):
            try:
                derived = route([directive])
            except author.Refusal as exc:
                assert f'{key} has no value' in str(exc), str(exc)
            else:
                raise AssertionError(f'{name} route: an unresolved {key} reached a record: {derived[0]}')


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
        author.execute(hart, 0xB0009073)  # CSRRW x0,mcycle,x1: a CSR the profile has, a write the author does not model
    except author.Refusal as exc:
        assert 'csr mcycle write' in str(exc), str(exc)
    else:
        raise AssertionError('unmodeled CSR write did not refuse by name')
    # P4-SYSTEM.20 slice b2: a CSR the state table does not declare is reserved, so the access traps with the word.
    hart = author.Hart()
    author.execute(hart, 0xF1102273)  # CSRRS x4,mvendorid,x0
    assert (hart.csr['mcause'], hart.csr['mtval'], hart.x[4]) == (2, 0xF1102273, 0), 'undeclared CSR did not trap'
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
    hart.mode = author.M
    author.execute(hart, 0x12000073)  # legal full fence after the explicit PTE edit
    hart.mode = 0
    assert hart.walk(va, 'load') == ('fault', 13), 'U mode cannot read an S page'
    hart.mode = author.S
    hart.write(root_pte, 8, ((author.ENTRY >> 12) << 10) | 0xC9)  # V/X/A/D, R=0
    assert hart.walk(va, 'load') == ('fault', 13), 'MXR=0 rejects an X-only load'
    hart.csr['mstatus'] |= 1 << 19
    assert hart.walk(va, 'load') == ('pa', author.ENTRY), 'MXR=1 permits an X-only load'
    check_directive_keys(author)
    assert Frozen.check_owned(author) == 0, 'owned expectation corpus drift'
    print('GC author probe: 7 reserved words, named refusal, permissions, directive keys and owned corpus passed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', choices=['reserved-op', 'reserved-shift', 'division-rounding',
                                              'ignore-sum', 'ignore-mxr', 'ignore-user',
                                              'no-new', 'new-after-dropping', 'parcel-new-after-dropping',
                                              'unresolved-kept'])
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
            'no-new': ('text = text.replace("{new}", sx(next(iter(written.values()))))', 'pass'),
            'new-after-dropping': ('written = dict(st.writes)', 'written = st.writes'),
            'parcel-new-after-dropping': ('written = dict(step.writes)', 'written = step.writes'),
            'unresolved-kept': ('raise Refusal(f"{where}: {left.group()} has no value on this step")', 'pass'),
        }
        old, new = changes[args.mutation]
        assert source.count(old) == 1, 'author mutation must match once'
        path = Path(td) / 'author_control.py'
        path.write_text(source.replace(old, new))
        spec = importlib.util.spec_from_file_location('author_control', path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        module.REPO = REPO
        module.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        check(module)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
