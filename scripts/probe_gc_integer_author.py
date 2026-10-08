#!/usr/bin/env python3
"""Hand-encoded integer author controls; no engine or generated decode table.

RVI-RV32I 1.1.4–1.1.6 and RVI-RV64I 3.1.2 define the comparisons,
branches, narrow memory effects, XLEN shifts and sign-extended W results.
Reserved W-immediate bits use the separately declared laboratory diagnostic.
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
MASK = 0xffffffffffffffff
HIGH = 0x8000000000000000
CORPUS = ('bound-alias', 'bound-arith', 'bound-ext', 'bound-shift', 'bound-shiftw',
          'dir-chain', 'dir-cmp-branch', 'dir-ext-matrix', 'dir-x0-writes',
          'fault-branch-nt', 'fault-hints', 'fault-shiftw-res', 'it-alias-bound',
          'scope-alu', 'scope-branch', 'scope-mem', 'smoke-arith')


def immediate(op, f3, value, rd=3):
    return ((value & 0xfff) << 20) | (1 << 15) | (f3 << 12) | (rd << 7) | op


def register(op, f3, upper=0, rd=3):
    return (upper << 25) | (2 << 20) | (1 << 15) | (f3 << 12) | (rd << 7) | op


def check(author, parent):
    cases = [
        (immediate(0x13, 4, -1), MASK, 0, 0, 'XORI sign extension'),
        (immediate(0x13, 2, -2048), HIGH, 0, 1, 'SLTI signed comparison'),
        (immediate(0x13, 2, -1), 0, 0, 0, 'SLTI signed comparison'),
        (immediate(0x13, 3, -1), MASK - 1, 0, 1, 'SLTIU sign extension'),
        (immediate(0x13, 3, -1), MASK, 0, 0, 'SLTIU sign extension'),
        (register(0x33, 2), MASK, 0, 1, 'SLT signed comparison'),
        (register(0x33, 3), MASK, 0, 0, 'SLTU unsigned comparison'),
        (register(0x33, 1), 1, 63, HIGH, 'XLEN shift count'),
        (register(0x33, 1), 1, 64, 1, 'XLEN shift count'),
        (register(0x33, 5), HIGH, 63, 1, 'XLEN logical shift'),
        (register(0x33, 5, 0x20), HIGH, 63, MASK, 'XLEN arithmetic shift'),
        (register(0x3b, 1), 1, 31, 0xffffffff80000000, 'word shift extension'),
        (register(0x3b, 1), 1, 32, 1, 'word shift count'),
        (register(0x3b, 5), 0x1234567880000000, 0, 0xffffffff80000000, 'word shift extension'),
        (register(0x3b, 5), 0x1234567880000000, 31, 1, 'word logical shift'),
        (register(0x3b, 5, 0x20), 0x1234567880000000, 31, MASK, 'word arithmetic shift'),
        (immediate(0x1b, 1, 31), 1, 0, 0xffffffff80000000, 'immediate word extension'),
        (immediate(0x1b, 5, 31), 0x1234567880000000, 0, 1, 'immediate word logical shift'),
        (immediate(0x1b, 5, 0x400 | 31), 0x1234567880000000, 0, MASK, 'immediate word arithmetic shift'),
        (register(0x33, 1, rd=1), 3, 2, 12, 'alias reads pre-state'),
        (register(0x3b, 5, 0x20, rd=1), 0x80000000, 31, MASK, 'alias reads pre-state'),
        (immediate(0x13, 4, -1, rd=0), MASK, 0, 0, 'x0 discards integer writes'),
    ]
    for word, a, b, expected, message in cases:
        hart = author.Hart()
        hart.x[1], hart.x[2] = a, b
        before = hart.x.copy(), hart.csr.copy(), hart.mem.copy()
        try:
            pc, info = author.execute(hart, word)
        except author.Refusal as exc:
            raise AssertionError(message) from exc
        rd = (word >> 7) & 31
        assert info['writes'] == ({rd: expected} if rd else {}), message
        assert pc == Q.ENTRY + 4 and not hart.trapped, message
        assert (hart.x, hart.csr, hart.mem) == before, 'integer effect did not retain pre-state'

    for f3, a, b, taken in ((4, MASK, 0, True), (4, 0, MASK, False),
                           (5, MASK, 0, False), (5, 0, MASK, True),
                           (6, MASK, 0, False), (6, 0, MASK, True),
                           (7, MASK, 0, True), (7, 0, MASK, False),
                           (5, 7, 7, True), (7, 7, 7, True)):
        # B-immediate -2: every encoded sign/offset bit except bit zero is one.
        word = 0xfe000f80 | (2 << 20) | (1 << 15) | (f3 << 12) | 0x63
        hart = author.Hart()
        hart.x[1], hart.x[2] = a, b
        before = hart.x.copy(), hart.csr.copy(), hart.mem.copy()
        pc, info = author.execute(hart, word)
        assert pc == Q.ENTRY + (-2 if taken else 4), 'branch signed/unsigned decision'
        assert not info.get('writes') and not hart.trapped, 'branch acquired a target effect'
        assert (hart.x, hart.csr, hart.mem) == before, 'branch mutated pre-state'

    for f3, expected in ((0, 0xffffffffffffff80), (1, 0xffffffffffff8080),
                         (4, 0x80), (5, 0x8080)):
        hart = author.Hart()
        hart.x[1] = Q.ENTRY + 0x100
        hart.write(hart.x[1], 2, 0x8080)
        pc, info = author.execute(hart, immediate(0x03, f3, 0))
        assert info['writes'] == {3: expected}, 'narrow load extension'
        assert pc == Q.ENTRY + 4 and not hart.trapped
    for f3, n in ((0, 1), (1, 2)):
        hart = author.Hart()
        hart.x[1], hart.x[2] = Q.ENTRY + 0x100, 0x123456789abcdef0
        hart.write(hart.x[1], 4, 0xaabbccdd)
        before = hart.x.copy()
        pc, info = author.execute(hart, (2 << 20) | (1 << 15) | (f3 << 12) | 0x23)
        expected = [0xf0, 0xcc, 0xbb, 0xaa] if n == 1 else [0xf0, 0xde, 0xbb, 0xaa]
        assert [hart.read(hart.x[1] + i, 1) for i in range(4)] == expected, 'narrow store width'
        assert not info.get('writes') and hart.x == before and pc == Q.ENTRY + 4
    for word, cause in ((immediate(0x03, 1, 1), 4),
                        ((2 << 20) | (1 << 15) | (1 << 12) | (1 << 7) | 0x23, 6)):
        hart = author.Hart()
        hart.x[1] = Q.ENTRY + 0x100
        before = hart.mem.copy(), hart.x.copy()
        _, info = author.execute(hart, word)
        assert hart.trapped and hart.csr['mcause'] == cause and hart.csr['mtval'] == Q.ENTRY + 0x101
        assert not info.get('writes') and (hart.mem, hart.x) == before

    asm = Assembler(REPO / 'profiles/rv64gc-lab-v0/encoding.sexp')
    for word in (0x0210911b, 0x0210d11b, 0x4210d11b):
        hart = author.Hart()
        before = hart.x.copy(), hart.pc, hart.csr.copy(), hart.mem.copy()
        try:
            author.execute(hart, word)
        except author.ReservedInstruction:
            pass
        else:
            raise AssertionError('reserved word shift acquired an effect')
        assert (hart.x, hart.pc, hart.csr, hart.mem) == before
        path = parent / 'reserved.s'
        path.write_text(f'.word {word:#010x}\n')
        run = author.derive_parcel_guest(path, asm, 1)
        assert (run.hart.trapped and run.hart.csr['mcause'] == 2
                and run.hart.csr['mtval'] == word), 'reserved diagnostic lost raw word'
        assert run.hart.instret == 0 and run.steps[0].fetch == 2
    total = 0
    for name in CORPUS:
        path = REPO / 'profiles/rv64gc-lab-v0/guests' / (name + '.s')
        expected = D.load_expectations(path.with_suffix('.expected.sexp'))
        run = author.derive_parcel_guest(path, asm, expected['instructions'])
        writes = [{int(k[1:]): int(v, 16) for k, v in st['writes'].items()} for st in expected['step']]
        assert [st.writes for st in run.steps] == writes, f'{name}: integer architectural observations differ'
        total += len(run.steps)
    assert author.main(['probe', '--check-owned']) == 0
    print(f'GC integer author probe: {len(cases)} arithmetic, 10 branches, narrow memory and reserved diagnostics; {len(CORPUS)} corpus gaps / {total} steps')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--author-revision')
    changes = {
        'sltiu-sign': ('x[rs1] < u(imm_i)', 'x[rs1] < imm_i'),
        'xlen-count': ('u(x[rs1] << (x[rs2] & 63)), "sll"', 'u(x[rs1] << (x[rs2] & 31)), "sll"'),
        'word-count': ('shamt = x[rs2] & 31', 'shamt = x[rs2] & 63'),
        'word-sign': ('sext(u(x[rs1], 32), 32) >> shamt, "sraw"', 'u(x[rs1], 32) >> shamt, "sraw"'),
        'branch-sign': ('4: sext(x[rs1], 64) < sext(x[rs2], 64)', '4: x[rs1] < x[rs2]'),
        'load-sign': ('mn in ("lb", "lh", "lw")', 'mn in ("lh", "lw")'),
        'store-width': ('widths = {0: (1, "sb")', 'widths = {0: (2, "sb")'),
        'reserved-word': ('if (f3 == 1 and upper != 0) or (f3 == 5 and upper not in (0, 0x20)):', 'if False:'),
    }
    control.add_argument('--mutation', choices=changes)
    args = parser.parse_args()
    root = REPO / 'target/p4-system-12'
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-integer-author-', dir=root) as td:
        author = Q
        if args.author_revision or args.mutation:
            source = (subprocess.check_output(['git', 'show', f'{args.author_revision}:scripts/derive_rv64gc_expectations.py'], cwd=REPO).decode()
                      if args.author_revision else (REPO / 'scripts/derive_rv64gc_expectations.py').read_text())
            if args.mutation:
                old, new = changes[args.mutation]
                assert source.count(old) == 1, 'integer mutation must match once'
                source = source.replace(old, new)
            path = Path(td) / 'integer_control.py'
            path.write_text(source)
            spec = importlib.util.spec_from_file_location('integer_control', path)
            author = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = author
            spec.loader.exec_module(author)
            author.REPO = REPO
            author.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        check(author, Path(td))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
