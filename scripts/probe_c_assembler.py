#!/usr/bin/env python3
"""Spec-side C word fixtures and image/label controls for P4-SYSTEM.12 d1.

Every word below is hand-encoded from the RVC formats, not derived from c.sexp or the
assembler's output. The engine probe shares selected words as a cross-check. This is
finite encoding evidence, not independent ISA conformance (riscv-opcodes ancestry remains).
All temporary inputs stay on-volume under target/p4-system-12.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile

import riscv_asm as R

REPO = Path(__file__).resolve().parent.parent
CASES = [
    ('c.add', ['x1', 'x2'], 0x908a),
    ('c.addi', ['x1', '-32'], 0x1081),
    ('c.addi16sp', ['16'], 0x6141),
    ('c.addi4spn', ['x8', '4'], 0x0040),
    ('c.addiw', ['x1', '-32'], 0x3081),
    ('c.addw', ['x8', 'x9'], 0x9c25),
    ('c.and', ['x8', 'x9'], 0x8c65),
    ('c.andi', ['x8', '-32'], 0x9801),
    ('c.beqz', ['x8', '-256'], 0xd001),
    ('c.bnez', ['x8', '-256'], 0xf001),
    ('c.ebreak', [], 0x9002),
    ('c.fld', ['f8', 'x8', '0'], 0x2000),
    ('c.fldsp', ['f1', '0'], 0x2082),
    ('c.fsd', ['x8', 'f9', '0'], 0xa004),
    ('c.fsdsp', ['f1', '0'], 0xa006),
    ('c.j', ['-2'], 0xbffd),
    ('c.jalr', ['x1'], 0x9082),
    ('c.jr', ['x1'], 0x8082),
    ('c.ld', ['x8', 'x8', '0'], 0x6000),
    ('c.ldsp', ['x1', '0'], 0x6082),
    ('c.li', ['x1', '-32'], 0x5081),
    ('c.lui', ['x3', '-32'], 0x7181),
    ('c.lw', ['x8', 'x8', '124'], 0x5c60),
    ('c.lwsp', ['x1', '0'], 0x4082),
    ('c.mv', ['x1', 'x2'], 0x808a),
    ('c.nop', [], 0x0001),
    ('c.or', ['x8', 'x9'], 0x8c45),
    ('c.sd', ['x8', 'x9', '0'], 0xe004),
    ('c.sdsp', ['x1', '0'], 0xe006),
    ('c.slli', ['x1', '1'], 0x0086),
    ('c.srai', ['x8', '1'], 0x8405),
    ('c.srli', ['x8', '1'], 0x8005),
    ('c.sub', ['x8', 'x9'], 0x8c05),
    ('c.subw', ['x8', 'x9'], 0x9c05),
    ('c.sw', ['x8', 'x9', '0'], 0xc004),
    ('c.swsp', ['x1', '0'], 0xc006),
    ('c.xor', ['x8', 'x9'], 0x8c25),
]
REFUSALS = [
    ('c.li', ['x1', '-33'], 'range'), ('c.li', ['x1', '32'], 'range'),
    ('c.lw', ['x8', 'x8', '128'], 'range'), ('c.lw', ['x8', 'x8', '2'], 'multiple'),
    ('c.lw', ['x7', 'x8', '0'], 'compact'), ('c.fld', ['f16', 'x8', '0'], 'compact'),
    ('c.fld', ['x8', 'x8', '0'], 'f-register'), ('c.fsd', ['x8', 'x9', '0'], 'f-register'),
    ('c.fld', ['f8', 'f8', '0'], 'x-register'),
    ('c.addi4spn', ['x8', '0'], 'reserved'), ('c.addi16sp', ['0'], 'reserved'),
    ('c.lui', ['x3', '0'], 'reserved'), ('c.addiw', ['x0', '0'], 'reserved'),
    ('c.lwsp', ['x0', '0'], 'reserved'), ('c.ldsp', ['x0', '0'], 'reserved'),
    ('c.jr', ['x0'], 'reserved'),
    ('c.lui', ['x2', '1'], 'specialization'), ('c.mv', ['x1', 'x0'], 'specialization'),
    ('c.j', ['3'], 'multiple'), ('c.addi', ['x1'], 'expects'),
    ('c.li', ['x1', 'bad'], 'numeric literal'),
]


def check(asm, module):
    for name, args, expected in CASES:
        got = asm.encode(name, args)
        assert got == expected, f'{name}: 0x{got:04x}, expected 0x{expected:04x}'
    assert len(CASES) == len({name for name, _, _ in CASES}) == 37
    assert {name for name, _, _ in CASES} == {name for name in asm.insns if name.startswith('c.')}
    for name, args, reason in REFUSALS:
        try:
            asm.encode(name, args)
        except module.AsmError as exc:
            assert reason in str(exc), f'{name}: wrong refusal reason: {exc}'
        else:
            raise AssertionError(f'{name}: illegal operands accepted: {args}')
    # HINTs with their own mnemonic remain accepted; aliases need their special spelling.
    for name, args, expected in [('c.addi', ['x1', '0'], 0x0081),
                                 ('c.li', ['x0', '1'], 0x4005), ('c.nop', ['1'], 0x0005)]:
        assert asm.encode(name, args) == expected
    lines = ['start: c.nop', 'addi x1, x0, 1', 'c.j start', '.half 0xffff', '.word 0x13']
    units = asm.assemble_units(lines, base=0x1000)
    assert [u.pc for u in units] == [0x1000, 0x1002, 0x1006, 0x1008, 0x100a], 'byte label addresses'
    assert [u.length for u in units] == [2, 4, 2, 2, 4]
    assert units[2].value == asm.encode('c.j', ['-6'])
    assert asm.assemble_image(lines) == bytes.fromhex('0100 93001000 edbf ffff 13000000'), 'exact byte image'
    for line, reason in [('.half -1', 'outside 16 bits'), ('.half 0x10000', 'outside 16 bits'),
                         ('.half 1, 2', 'exactly one'), ('.half bad', 'numeric literal')]:
        try:
            asm.assemble_image([line])
        except module.AsmError as exc:
            assert reason in str(exc), str(exc)
        else:
            raise AssertionError(f'accepted {line}')
    try:
        asm.assemble(['.half 1'])
    except module.AsmError as exc:
        assert 'refuses padding' in str(exc)
    else:
        raise AssertionError('legacy word API silently padded a short unit')
    print('C assembler probe: 37 spec-side words, 21 operand refusals, hints and exact image/labels passed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    controls = parser.add_mutually_exclusive_group()
    controls.add_argument('--assembler-revision')
    controls.add_argument('--mutation', choices=['compact-base', 'label-stride', 'padding'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='c-assembler-', dir=parent) as td:
        root = Path(td)
        unit = root / 'profiles/rv64gc-lab-v0'
        unit.mkdir(parents=True)
        shutil.copytree(REPO / 'definitions', root / 'definitions')
        for name in ('profile.sexp', 'state.sexp'):
            shutil.copyfile(REPO / 'profiles/rv64gc-lab-v0' / name, unit / name)
        text = (REPO / 'profiles/rv64gc-lab-v0/encoding.sexp').read_text()
        text = text.replace('(slot (id c) (requires "riscv/c"))', '(extensions "riscv/c")')
        (unit / 'encoding.sexp').write_text(text)
        module = R
        if args.assembler_revision or args.mutation:
            import sys
            path = root / 'riscv_asm_before.py'
            text = (subprocess.check_output(['git', 'show', f'{args.assembler_revision}:scripts/riscv_asm.py'], cwd=REPO).decode()
                    if args.assembler_revision else (REPO / 'scripts/riscv_asm.py').read_text())
            changes = {
                'compact-base': ('index -= 8', 'index -= 7'),
                'label-stride': ('pc += 2 if mnemonic.lower() == ".half" or mnemonic.lower().startswith("c.") else 4', 'pc += 4'),
                'padding': ('unit.value.to_bytes(unit.length, "little")', 'unit.value.to_bytes(4, "little")'),
            }
            if args.mutation:
                old, new = changes[args.mutation]
                if text.count(old) != 1:
                    raise RuntimeError(f'mutation seam must match once: {old}')
                text = text.replace(old, new)
            path.write_text(text)
            spec = importlib.util.spec_from_file_location('riscv_asm_before', path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
        check(module.Assembler(unit / 'encoding.sexp'), module)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
