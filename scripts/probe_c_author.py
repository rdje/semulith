#!/usr/bin/env python3
"""Finite spec-side C author controls, independent of engine execution.

Parcel fixtures share the hand-encoded RVC ancestry of probe_c_assembler.py; base
words/effects below are derived from the pinned C and I/D sentences. No engine or
generated expansion tables supply answers. Temporary mutations stay in target/.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

import derive_rv64gc_expectations as Q
import spec_c as C

REPO = Path(__file__).resolve().parent.parent
# name, original parcel, expanded base word
CASES = [
    ('c.add', 0x908a, 0x002080b3), ('c.addi', 0x1081, 0xfe008093),
    ('c.addi16sp', 0x6141, 0x01010113), ('c.addi4spn', 0x0040, 0x00410413),
    ('c.addiw', 0x3081, 0xfe00809b), ('c.addw', 0x9c25, 0x0094043b),
    ('c.and', 0x8c65, 0x00947433), ('c.andi', 0x9801, 0xfe047413),
    ('c.beqz', 0xd001, 0xf00400e3), ('c.bnez', 0xf001, 0xf00410e3),
    ('c.ebreak', 0x9002, 0x00100073), ('c.fld', 0x2000, 0x00043407),
    ('c.fldsp', 0x2082, 0x00013087), ('c.fsd', 0xa004, 0x00943027),
    ('c.fsdsp', 0xa006, 0x00113027), ('c.j', 0xbffd, 0xfffff06f),
    ('c.jalr', 0x9082, 0x000080e7), ('c.jr', 0x8082, 0x00008067),
    ('c.ld', 0x6000, 0x00043403), ('c.ldsp', 0x6082, 0x00013083),
    ('c.li', 0x5081, 0xfe000093), ('c.lui', 0x7181, 0xfffe01b7),
    ('c.lw', 0x5c60, 0x07c42403), ('c.lwsp', 0x4082, 0x00012083),
    ('c.mv', 0x808a, 0x002000b3), ('c.nop', 0x0001, 0x00000013),
    ('c.or', 0x8c45, 0x00946433), ('c.sd', 0xe004, 0x00943023),
    ('c.sdsp', 0xe006, 0x00113023), ('c.slli', 0x0086, 0x00109093),
    ('c.srai', 0x8405, 0x40145413), ('c.srli', 0x8005, 0x00145413),
    ('c.sub', 0x8c05, 0x40940433), ('c.subw', 0x9c05, 0x4094043b),
    ('c.sw', 0xc004, 0x00942023), ('c.swsp', 0xc006, 0x00112023),
    ('c.xor', 0x8c25, 0x00944433),
]
# All scattered pieces set, signed limits and the sixth shift bit.
LIMITS = [
    (0x1ffc, 0x3fc10793), (0x3ffc, 0x0f87b787), (0x5ffc, 0x07c7a783),
    (0x7ffc, 0x0f87b783), (0xbffc, 0x0ef7bc27), (0xdffc, 0x06f7ae23),
    (0xfffc, 0x0ef7bc23), (0x7101, 0xe0010113), (0x617d, 0x1f010113),
    (0x61fd, 0x0001f1b7), (0x907d, 0x03f45413), (0x947d, 0x43f45413),
    (0x10fe, 0x03f09093), (0xb001, 0x801ff06f), (0xaffd, 0x7fe0006f),
    (0xcc7d, 0x0e040f63), (0x50fe, 0x0fc12083), (0x70fe, 0x1f813083),
    (0x30fe, 0x1f813087), (0xdf86, 0x0e112e23), (0xff86, 0x1e113c23),
    (0xbf86, 0x1e113c27),
]
# One-hot immediate controls transcribed from each pinned diagram field. All-ones
# limits alone cannot distinguish a permutation of two scattered bits.
SCATTERS = [
    (0x0000, 'i', ((12, 32), (11, 16), (10, 512), (9, 256), (8, 128), (7, 64), (6, 4), (5, 8))),
    (0x2000, 'i', ((12, 32), (11, 16), (10, 8), (6, 128), (5, 64))),
    (0x4000, 'i', ((12, 32), (11, 16), (10, 8), (6, 4), (5, 64))),
    (0x0081, 'i', ((12, -32), (6, 16), (5, 8), (4, 4), (3, 2), (2, 1))),
    (0x6101, 'i', ((12, -512), (6, 16), (5, 64), (4, 256), (3, 128), (2, 32))),
    (0x6181, 'u', ((12, -131072), (6, 65536), (5, 32768), (4, 16384), (3, 8192), (2, 4096))),
    (0xa001, 'j', ((12, -2048), (11, 16), (10, 512), (9, 256), (8, 1024),
                    (7, 64), (6, 128), (5, 8), (4, 4), (3, 2), (2, 32))),
    (0xc001, 'b', ((12, -256), (11, 16), (10, 8), (6, 128), (5, 64), (4, 4), (3, 2), (2, 32))),
    (0x4082, 'i', ((12, 32), (6, 16), (5, 8), (4, 4), (3, 128), (2, 64))),
    (0x6082, 'i', ((12, 32), (6, 16), (5, 8), (4, 256), (3, 128), (2, 64))),
    (0xc006, 's', ((12, 32), (11, 16), (10, 8), (9, 4), (8, 128), (7, 64))),
    (0xe006, 's', ((12, 32), (11, 16), (10, 8), (9, 256), (8, 128), (7, 64))),
]


def base_immediate(word, kind):
    def sign(value, width):
        return value - (1 << width) if value & (1 << (width - 1)) else value
    if kind == 'i':
        return sign(word >> 20, 12)
    if kind == 's':
        return sign((word >> 25) << 5 | ((word >> 7) & 31), 12)
    if kind == 'u':
        return sign(word & 0xfffff000, 32)
    if kind == 'b':
        return sign((word >> 31) << 12 | ((word >> 7) & 1) << 11
                    | ((word >> 25) & 63) << 5 | ((word >> 8) & 15) << 1, 13)
    assert kind == 'j'
    return sign((word >> 31) << 20 | ((word >> 12) & 255) << 12
                | ((word >> 20) & 1) << 11 | ((word >> 21) & 1023) << 1, 21)


RESERVED = (0x0000, 0x0004, 0x8000, 0x2001, 0x6001, 0x6101,
            0x4002, 0x6002, 0x8002, 0x9c41, 0x9c61)
HINTS = (0x0005, 0x0081, 0x4005, 0x6005, 0x0006, 0x0082,
         0x8001, 0x8401, 0x8006, 0x9006)


def check(author, decoder):
    assert len(CASES) == len({n for n, _, _ in CASES}) == 37
    for name, parcel, word in CASES:
        got = decoder.decode(parcel)
        assert (got.name, got.word) == (name, word), f'{name}: C expansion mismatch {got}'
    for parcel, word in LIMITS:
        got = decoder.decode(parcel)
        assert got.word == word, f'limit {parcel:#06x}: {got.word:#010x} != {word:#010x}'
    for base, kind, fields in SCATTERS:
        for bit, value in fields:
            word = decoder.decode(base | (1 << bit)).word
            assert base_immediate(word, kind) == value, f'scattered bit {base:#x}/{bit} misplaced'
    for parcel in RESERVED:
        hart = author.Hart()
        hart.csr['mtvec'] = author.ENTRY + 0x100
        before = (hart.x.copy(), hart.f.copy(), hart.mem.copy())
        pc, info = author.execute_c(hart, parcel)
        assert hart.trapped and hart.csr['mcause'] == 2, f'reserved parcel {parcel:#06x} accepted'
        assert hart.csr['mtval'] == parcel and hart.csr['mepc'] == author.ENTRY
        assert pc == author.ENTRY + 0x100 and not info.get('writes')
        assert (hart.x, hart.f, hart.mem) == before
    for parcel in (0x0003, 0xffff, -1, 0x10001):
        hart = author.Hart()
        try:
            author.execute_c(hart, parcel)
        except author.Refusal as exc:
            assert 'complete 16-bit compressed' in str(exc)
        else:
            raise AssertionError(f'incomplete/wider parcel {parcel} accepted')
        assert not hart.trapped and not any(hart.x)
    for parcel in HINTS:
        hart = author.Hart()
        hart.x[1] = 0x1234
        before = (hart.x.copy(), hart.csr.copy(), hart.f.copy(), hart.mem.copy())
        pc, info = author.execute_c(hart, parcel)
        for reg, value in info.get('writes', {}).items():
            hart.x[reg] = value
        assert pc == author.ENTRY + 2 and not hart.trapped, 'C parcel advanced by wrong length'
        assert (hart.x, hart.csr, hart.f, hart.mem) == before, f'HINT {parcel:#06x} changed state'
    # Independent integer/control observations for the selected hand parcels.
    arithmetic = {
        'c.add': {1: 16}, 'c.addi': {1: author.u(-25)}, 'c.addi16sp': {2: 25},
        'c.addi4spn': {8: 13}, 'c.addiw': {1: author.u(-25)},
        'c.addw': {8: author.u(-4)}, 'c.and': {8: 1}, 'c.andi': {8: author.u(-32)},
        'c.li': {1: author.u(-32)}, 'c.lui': {3: author.u(-131072)},
        'c.mv': {1: 9}, 'c.nop': {}, 'c.or': {8: author.u(-5)},
        'c.slli': {1: 14}, 'c.srai': {8: author.u(-4)},
        'c.srli': {8: 0x7ffffffffffffffc}, 'c.sub': {8: author.u(-10)},
        'c.subw': {8: author.u(-10)}, 'c.xor': {8: author.u(-6)},
        'c.beqz': {}, 'c.bnez': {}, 'c.j': {}, 'c.jalr': {1: author.ENTRY + 2},
        'c.jr': {}, 'c.ebreak': {},
    }
    for name, parcel, _ in CASES:
        if name not in arithmetic:
            continue
        hart = author.Hart()
        hart.x[1], hart.x[2], hart.x[8], hart.x[9] = 7, 9, author.u(-7), 3
        pc, info = author.execute_c(hart, parcel)
        assert info.get('writes', {}) == arithmetic[name], f'{name}: integer effect mismatch'
        target = {'c.bnez': author.ENTRY - 256, 'c.j': author.ENTRY - 2,
                  'c.jalr': 6, 'c.jr': 6, 'c.ebreak': 0}.get(name, author.ENTRY + 2)
        assert pc == target, f'{name}: length/link/target mismatch'
        assert info['source'].startswith('RVI-C §27.1.')
        if name == 'c.ebreak':
            assert hart.csr['mcause'] == 3 and hart.csr['mtval'] == author.ENTRY
    for parcel, target in ((0xd001, author.ENTRY - 256), (0xf001, author.ENTRY + 2)):
        hart = author.Hart()  # zero source reverses the branch outcomes above
        assert author.execute_c(hart, parcel)[0] == target
    # Load/store and FP observations; signed word versus unmodified doubleword.
    address, payload = author.ENTRY + 0x400, 0x8000000000000001
    for name, parcel, _ in CASES:
        if name in arithmetic:
            continue
        hart = author.Hart()
        hart.x[1], hart.x[2], hart.x[8], hart.x[9] = 7, address, address, 3
        hart.csr['mstatus'] |= 1 << 13  # FS Initial; FP accesses set Dirty
        hart.f[1] = hart.f[9] = payload
        at = address + (124 if name == 'c.lw' else 0)
        hart.write(at, 8, payload if name != 'c.lw' else 0x80000001)
        pc, info = author.execute_c(hart, parcel)
        assert pc == author.ENTRY + 2 and not hart.trapped, f'{name}: memory length/effect mismatch'
        if name.startswith(('c.l', 'c.fl')):
            if name.startswith('c.fl'):
                assert hart.f[1 if name.endswith('sp') else 8] == payload
                assert (hart.csr['mstatus'] >> 13) & 3 == 3
                assert not info.get('writes')
            else:
                reg = 1 if name.endswith('sp') else 8
                value = author.u(-2147483647) if name == 'c.lw' else 1 if name == 'c.lwsp' else payload
                assert info['writes'] == {reg: value}, f'{name}: load extension mismatch'
        else:
            floating = name.startswith('c.fs')
            value = payload if floating else 7 if name.endswith('sp') else 3
            width = 4 if name.startswith('c.sw') else 8
            assert hart.read(address, width) == value, f'{name}: store effect mismatch'
            assert not info.get('writes')
            if floating:
                assert (hart.csr['mstatus'] >> 13) & 3 == 1  # Precise: a read-only FP store
    # FS-Off faults retain the C parcel, not its expanded word; misalignment retains VA.
    for parcel in (0x2000, 0x2082, 0xa004, 0xa006):
        hart = author.Hart()
        pc, info = author.execute_c(hart, parcel)
        assert hart.trapped and hart.csr['mcause'] == 2 and hart.csr['mtval'] == parcel, 'FP illegal trap lost original C parcel'
        assert not info.get('writes') and not any(hart.f)
    hart = author.Hart()
    hart.x[2] = address + 1
    _, info = author.execute_c(hart, 0x6082)
    assert hart.csr['mcause'] == 4 and hart.csr['mtval'] == address + 1
    assert not info.get('writes')
    # Word truncation/sign extension at overflow and at imm=0 (not a HINT).
    for parcel, a, b, value in ((0x2081, 0x180000001, 0, author.u(-2147483647)),
                               (0x9c25, 0x7fffffff, 1, author.u(-2147483648)),
                               (0x9c05, 0x80000000, 1, 0x7fffffff)):
        hart = author.Hart()
        hart.x[1] = hart.x[8] = a
        hart.x[9] = b
        _, info = author.execute_c(hart, parcel)
        assert list(info['writes'].values()) == [value], 'word result extension mismatch'
    for word in (0x0400003b, 0x00001067):
        try:
            author.execute(author.Hart(), word)
        except author.Refusal as exc:
            assert 'reserved' in str(exc)
        else:
            raise AssertionError(f'reserved base word {word:#x} accepted')
    assert author.main(['probe', '--check-owned']) == 0
    print('C author probe: 37 expansions/effects, 22 limits, 79 one-hot bits, 11 reserved, 10 hints and 42 owned records passed')


def import_control(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    controls = parser.add_mutually_exclusive_group()
    controls.add_argument('--author-revision')
    controls.add_argument('--mutation', choices=['compact-base', 'signed-immediate', 'link-length', 'reserved-guard',
                                              'scattered-bits', 'expanded-trap'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='c-author-control-', dir=parent) as td:
        root = Path(td)
        author, decoder = Q, C
        if args.author_revision:
            path = root / 'author_before.py'
            path.write_bytes(subprocess.check_output(['git', 'show', f'{args.author_revision}:scripts/derive_rv64gc_expectations.py'], cwd=REPO))
            author = import_control(path, 'author_before')
        elif args.mutation:
            source_path = REPO / 'scripts' / ('derive_rv64gc_expectations.py' if args.mutation in ('link-length', 'expanded-trap') else 'spec_c.py')
            source = source_path.read_text()
            changes = {
                'compact-base': ('rp, sp = 8 + ((c >> 7) & 7), 8 + ((c >> 2) & 7)',
                                 'rp, sp = 7 + ((c >> 7) & 7), 7 + ((c >> 2) & 7)'),
                'signed-immediate': ('ci = signed(((c >> 12) & 1) << 5 | ((c >> 2) & 31), 6)',
                                     'ci = ((c >> 12) & 1) << 5 | ((c >> 2) & 31)'),
                'link-length': ('execute(h, expansion.word, length=2, raw=parcel)',
                                'execute(h, expansion.word, length=4, raw=parcel)'),
                'reserved-guard': ('if imm == 0:', 'if False:'),
                'scattered-bits': ('((c >> 6) & 1) << 2 | ((c >> 5) & 1) << 6',
                                   '((c >> 6) & 1) << 6 | ((c >> 5) & 1) << 2'),
                'expanded-trap': ('execute(h, expansion.word, length=2, raw=parcel)',
                                  'execute(h, expansion.word, length=2, raw=expansion.word)'),
            }
            old, new = changes[args.mutation]
            assert source.count(old) == 1, 'C author mutation must match once'
            path = root / 'control.py'
            path.write_text(source.replace(old, new))
            module = import_control(path, 'c_author_control')
            if args.mutation in ('link-length', 'expanded-trap'):
                author = module
            else:
                decoder = module
        original_decoder = author.C if hasattr(author, 'C') else None
        if original_decoder is not None:
            author.C = decoder
        author.REPO = REPO
        author.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        try:
            check(author, decoder)
        finally:
            if original_decoder is not None:
                author.C = original_decoder
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
