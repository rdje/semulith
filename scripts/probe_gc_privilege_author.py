#!/usr/bin/env python3
"""Spec-side fixed misa and privileged legality controls, without an engine run.

RVP-CSR 1.1.1 defines CSR address privilege and ignored read-only fields;
RVP-MACHINE 2.1.1.6.6/2.1.3.2 supplies TVM/TSR and xRET legality. Five
committed spec-derived mode-matrix guests discriminate the repaired corpus paths.
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


def check(author):
    hart = author.Hart()
    assert author.csr_read_value(hart, 'misa') == 0x800000000014112d, 'misa lost the fixed selected reset'
    for value in (0, 1, 0xffffffffffffffff):
        author.csr_write_value(hart, 'misa', value)
        assert author.csr_read_value(hart, 'misa') == 0x800000000014112d, 'misa accepted a write to read-only fields'
    # CSRRW x5,misa,x5 must read the old register value before returning the fixed CSR.
    hart.x[5] = 1
    pc, info = author.execute(hart, 0x301292f3)
    assert pc == Q.ENTRY + 4 and info['writes'] == {5: 0x800000000014112d}
    assert hart.x[5] == 1 and author.csr_read_value(hart, 'misa') == 0x800000000014112d

    def illegal(word, mode, status, message):
        hart = author.Hart()
        hart.mode, hart.csr['mstatus'] = mode, status
        hart.csr['mtvec'], hart.csr['sepc'] = Q.ENTRY + 0x100, Q.ENTRY + 0x80
        hart.x[5] = 0x55
        before = hart.x.copy(), hart.mem.copy(), hart.csr['satp'], hart.csr['sepc']
        try:
            pc, info = author.execute(hart, word)
        except author.Refusal as exc:
            raise AssertionError(message) from exc
        assert hart.trapped and hart.csr['mcause'] == 2, message
        assert hart.csr['mtval'] == word and hart.csr['mepc'] == Q.ENTRY, message
        assert pc == Q.ENTRY + 0x100 and not info.get('writes'), message
        assert (hart.x, hart.mem, hart.csr['satp'], hart.csr['sepc']) == before, message

    for mode in (0, author.S):
        illegal(0x300022f3, mode, 0, 'CSR privilege fault lost its unit discipline')
    for word in (0x180022f3, 0x180292f3):
        illegal(word, author.S, 1 << 20, 'S-mode satp ignored TVM')
    for mode in (0, author.S):
        illegal(0x30200073, mode, 0, 'MRET below M popped the stack')
    illegal(0x10200073, 0, 0, 'U-mode SRET popped the stack')
    illegal(0x10200073, author.S, 1 << 22, 'S-mode SRET ignored TSR')
    illegal(0x12000073, 0, 0, 'U-mode SFENCE.VMA executed')
    illegal(0x12000073, author.S, 1 << 20, 'S-mode SFENCE.VMA ignored TVM')
    # Higher privilege ignores S interception; ordinary legal returns still pop.
    for mode, status in ((author.M, 1 << 20), (author.S, 0)):
        hart = author.Hart()
        hart.mode, hart.csr['mstatus'] = mode, status
        pc, _ = author.execute(hart, 0x12000073)
        assert pc == Q.ENTRY + 4 and not hart.trapped
        pc, info = author.execute(hart, 0x180022f3)
        assert pc == Q.ENTRY + 4 and not hart.trapped and info['writes'] == {5: 0}
    for mode, status, target_mode in ((author.M, 1 << 22, 0), (author.S, 1 << 8, author.S)):
        hart = author.Hart()
        hart.mode, hart.csr['mstatus'], hart.csr['sepc'] = mode, status, Q.ENTRY + 2
        pc, _ = author.execute(hart, 0x10200073)
        assert pc == Q.ENTRY + 2 and hart.mode == target_mode and not hart.trapped
    hart = author.Hart()
    hart.csr['mstatus'], hart.csr['mepc'] = author.S << 11, Q.ENTRY + 2
    pc, _ = author.execute(hart, 0x30200073)
    assert pc == Q.ENTRY + 2 and hart.mode == author.S and not hart.trapped
    asm = Assembler(REPO / 'profiles/rv64gc-lab-v0/encoding.sexp')
    total = 0
    for name in ('mm-readonly', 'mm-sfence', 'mm-sret', 'mm-csr-legality-s', 'mm-csr-legality-u'):
        path = REPO / 'profiles/rv64gc-lab-v0/guests' / (name + '.s')
        expected = D.load_expectations(path.with_suffix('.expected.sexp'))
        run = author.derive_parcel_guest(path, asm, expected['instructions'])
        writes = [{int(k[1:]): int(v, 16) for k, v in st['writes'].items()} for st in expected['step']]
        assert [st.writes for st in run.steps] == writes, f'{name}: privileged architectural observations differ'
        total += len(run.steps)
    assert author.main(['probe', '--check-owned']) == 0
    print(f'GC privilege author probe: fixed misa, CSR/xRET/TVM/TSR legality passed; 5 corpus repairs / {total} steps')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--author-revision')
    control.add_argument('--mutation', choices=['misa-reset', 'misa-write', 'csr-privilege',
                                              'satp-tvm', 'mret-mode', 'sret-mode',
                                              'sret-tsr', 'sfence-mode', 'sfence-tvm'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-privilege-author-', dir=parent) as td:
        author = Q
        if args.author_revision or args.mutation:
            source = (subprocess.check_output(['git', 'show', f'{args.author_revision}:scripts/derive_rv64gc_expectations.py'], cwd=REPO).decode()
                      if args.author_revision else (REPO / 'scripts/derive_rv64gc_expectations.py').read_text())
            changes = {
                'misa-reset': ('"misa": MISA', '"misa": 0'),
                'misa-write': ('if name == "misa":\n        return', 'if False:\n        return'),
                'csr-privilege': ('if (csr >> 8) & 0b11 > h.mode:', 'if False:'),
                'satp-tvm': ('if name == "satp" and h.mode == S and (h.csr["mstatus"] >> 20) & 1:', 'if False:'),
                'mret-mode': ('if h.mode != M:\n                h.deliver(2, raw)', 'if False:\n                h.deliver(2, raw)'),
                'sret-mode': ('if h.mode < S or (h.mode == S and (h.csr["mstatus"] >> 22) & 1):', 'if h.mode == S and (h.csr["mstatus"] >> 22) & 1:'),
                'sret-tsr': ('if h.mode < S or (h.mode == S and (h.csr["mstatus"] >> 22) & 1):', 'if h.mode < S:'),
                'sfence-mode': ('if h.mode < S or (h.mode == S and (h.csr["mstatus"] >> 20) & 1):', 'if h.mode == S and (h.csr["mstatus"] >> 20) & 1:'),
                'sfence-tvm': ('if h.mode < S or (h.mode == S and (h.csr["mstatus"] >> 20) & 1):', 'if h.mode < S:'),
            }
            if args.mutation:
                old, new = changes[args.mutation]
                assert source.count(old) == 1, 'privilege mutation must match once'
                source = source.replace(old, new)
            path = Path(td) / 'privilege_control.py'
            path.write_text(source)
            spec = importlib.util.spec_from_file_location('privilege_control', path)
            author = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = author
            spec.loader.exec_module(author)
            author.REPO = REPO
            author.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        check(author)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
