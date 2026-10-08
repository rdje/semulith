#!/usr/bin/env python3
"""Independent byte-guest, boundary-budget and code-visibility controls (EVD-05).

Hand image/PC/write fixtures come from the pinned C and base chapters. Five legacy
budgets were declared in P4-SYSTEM.12 before this experiment; their committed
spec-derived writes check the repaired fetch/end route, without engine outputs.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import derive_rv64gc_expectations as Q
import dossier_sexp as D
from riscv_asm import Assembler

REPO = Path(__file__).resolve().parent.parent
IMAGE = bytes.fromhex('8150 13811000 0501 11a0 ffff 8a81')
LEGACY = {'dir-runoff': (3, 5), 'fault-fetch': (3, 5), 'it-prio-jump': (4, 7),
          'sv39-straddle': (52, 104), 'sv39-perm-rwx': (114, 226)}


def check(author, root):
    assert hasattr(author, 'derive_parcel_guest'), 'explicit parcel guest API is absent'
    unit = root / 'profiles/rv64gc-lab-v0'
    unit.mkdir(parents=True)
    shutil.copytree(REPO / 'definitions', root / 'definitions')
    source = (REPO / 'profiles/rv64gc-lab-v0/encoding.sexp').read_text()
    source = source.replace('(slot (id c) (requires "riscv/c"))', '(extensions "riscv/c")')
    encoding = unit / 'encoding.sexp'
    encoding.write_text(source)
    asm = Assembler(encoding)

    def guest(name, source):
        path = root / (name + '.s')
        path.write_text(source)
        return path

    mixed = guest('mixed', '''c.li x1, -32 #: first parcel | RVI-C §27.1.2
addi x2, x1, 1 #: word at byte two | RVI-RV32I §1.1.4
c.addi x2, 1 #: second increment | RVI-C §27.1.2
c.j end
.half 0xffff
end: c.mv x3, x2 #: final marker | RVI-C §27.1.2
''')
    first = author.derive_parcel_guest(mixed, asm, 1)
    assert first.hart.read(Q.ENTRY, len(IMAGE)) == int.from_bytes(IMAGE, 'little'), 'byte guest image acquired padding'
    run = author.derive_parcel_guest(mixed, asm, 5)
    assert [st.pc for st in run.steps] == [Q.ENTRY + n for n in (0, 2, 6, 8, 12)], 'mixed byte PCs changed'
    assert [st.writes for st in run.steps] == [{1: 0xffffffffffffffe0}, {2: 0xffffffffffffffe1},
                                             {2: 0xffffffffffffffe2}, {}, {3: 0xffffffffffffffe2}]
    assert [run.steps[n].deriv for n in (0, 1, 2, 4)] == ['first parcel', 'word at byte two',
                                                        'second increment', 'final marker'], 'directives lost their byte PCs'
    assert [st.fetch for st in run.steps] == [1, 2, 1, 1, 1], 'byte guest lost actual parcel counts'
    assert (run.hart.time, run.hart.instret, run.hart.pc) == (5, 5, Q.ENTRY + 14)
    text, count = author.run_parcel_guest(mixed, asm, 5)
    out = root / 'mixed.expected.sexp'
    out.write_text(text)
    doc = D.load_expectations(out)
    assert count == doc['instructions'] == 5 and doc['fetches'] == 6, 'emitter lost parcel counts'
    # Same spelling at two different byte PCs still carries its own annotation.
    repeated = guest('repeated', 'c.nop #: first | RVI-C §27.1.2\nc.nop #: second | RVI-C §27.1.2\n')
    repeated_run = author.derive_parcel_guest(repeated, asm, 2)
    assert [st.deriv for st in repeated_run.steps] == ['first', 'second'], 'directives lost their byte PCs'
    end = guest('end', 'addi x1, x0, 1 #|end\naddi x2, x0, 2\n')
    run = author.derive_parcel_guest(end, asm, 3)
    assert len(run.steps) == 3, 'explicit budget stopped at the source end'
    assert run.steps[2].pc == Q.ENTRY + 8 and run.steps[2].fetch == 1
    assert run.hart.csr['mcause'] == 2 and run.hart.csr['mtval'] == 0
    assert run.hart.csr['mepc'] == Q.ENTRY + 8
    assert (run.hart.time, run.hart.instret) == (3, 2), 'fault boundary retired an instruction'
    for budget in (0, -1, 10001, True, 1.0):
        try:
            author.derive_parcel_guest(end, asm, budget)
        except author.Refusal as exc:
            assert 'budget' in str(exc)
        else:
            raise AssertionError('invalid parcel budget accepted')
    upper = guest('upper', '#|refuse: fetch 0x80000002 1\n.word 0x00100093\n')
    run = author.derive_parcel_guest(upper, asm, 1)
    assert run.steps[0].fetch == 2 and run.hart.csr['mtval'] == Q.ENTRY + 2
    assert run.hart.csr['mepc'] == Q.ENTRY and run.hart.csr['mcause'] == 1
    assert (run.hart.time, run.hart.instret) == (1, 0), 'fault boundary retired an instruction'
    wider = guest('wider', '.word 0x1234ffff\n')
    run = author.derive_parcel_guest(wider, asm, 1)
    assert run.hart.csr['mtval'] == 0x1234ffff and run.hart.csr['mcause'] == 2
    assert run.steps[0].fetch == 2 and run.hart.instret == 0
    # SW patches two originally compressed units; the next fetched parcel is C.LI x3,7.
    patch = guest('patch', '''auipc x1, 0
addi x1, x1, 24
lui x2, 4
addi x2, x2, 413
sw x2, 0, x1
jal x0, 4
c.nop
c.nop
''')
    run = author.derive_parcel_guest(patch, asm, 7)
    assert run.steps[-1].pc == Q.ENTRY + 24 and run.steps[-1].writes == {3: 7}, 'next parcel ignored the code patch'
    assert run.hart.read(Q.ENTRY + 24, 4) == 0x419d
    assert sum(st.fetch for st in run.steps) == 13 and run.hart.instret == 7
    pending = guest('pending', '''auipc x1, 0
addi x1, x1, 36
csrrw x0, mtvec, x1
addi x2, x0, 2
csrrw x0, mip, x2
csrrw x0, mie, x2
csrrsi x0, mstatus, 8
addi x5, x0, 1
c.nop
''')
    run = author.derive_parcel_guest(pending, asm, 8)
    assert run.steps[-1].fetch == 0 and run.hart.x[5] == 0, 'pending interrupt fetched the instruction'
    assert run.hart.csr['mcause'] == (1 << 63) | 1 and run.hart.csr['mepc'] == Q.ENTRY + 28
    assert (run.hart.time, run.hart.instret, run.hart.pc) == (8, 7, Q.ENTRY + 36)
    wait = guest('wait', 'wfi\n')
    run = author.derive_parcel_guest(wait, asm, 3)
    assert [st.fetch for st in run.steps] == [2, 0, 0] and run.hart.waiting
    assert [st.insn for st in run.steps] == ['wfi', '<halted>', '<halted>']
    assert (run.hart.time, run.hart.instret, run.hart.pc) == (3, 1, Q.ENTRY + 4)
    unknown = guest('unknown', 'xori x1, x0, 1\n')  # valid ISA, outside this bounded author
    try:
        author.derive_parcel_guest(unknown, asm, 1)
    except author.Refusal as exc:
        assert 'xori' in str(exc)
    else:
        raise AssertionError('unknown valid vocabulary became an illegal trap')
    # Derive every requested source before writing the first one.
    good = guest('good', 'addi x1, x0, 7\n')
    with contextlib.redirect_stderr(io.StringIO()):
        rc = author.main(['probe', '--encoding', str(encoding), '--parcels', '--steps', '1', str(good), str(unknown)])
    assert rc == 2 and not good.with_suffix('.expected.sexp').exists(), 'refused batch wrote a partial record'
    with contextlib.redirect_stdout(io.StringIO()):
        assert author.main(['probe', '--encoding', str(encoding), '--parcels', '--steps', '5', '--check', str(mixed)]) == 0
    base_asm = Assembler(REPO / 'profiles/rv64gc-lab-v0/encoding.sexp')
    checked = 0
    for name, (budget, parcels) in LEGACY.items():
        path = REPO / 'profiles/rv64gc-lab-v0/guests' / (name + '.s')
        run = author.derive_parcel_guest(path, base_asm, budget)
        previous = D.load_expectations(path.with_suffix('.expected.sexp'))
        expected = [{int(reg[1:]): int(value, 16) for reg, value in st['writes'].items()}
                    for st in previous['step']]
        assert len(run.steps) == len(expected) == budget, f'{name}: explicit budget stopped at the source end'
        assert [st.writes for st in run.steps] == expected, f'{name}: legacy architectural observations changed'
        assert sum(st.fetch for st in run.steps) == parcels, f'{name}: derived parcel count changed'
        checked += budget
    assert author.main(['probe', '--check-owned']) == 0
    print(f'GC parcel guest probe: mixed bytes, budgets, visibility and head boundaries passed; 5 legacy repairs / {checked} steps')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--author-revision')
    control.add_argument('--mutation', choices=['byte-directives', 'padded-image', 'source-end',
                                              'fetch-count', 'fault-retirement', 'head-pending',
                                              'code-visibility', 'unknown-valid'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-parcel-guest-', dir=parent) as td:
        root = Path(td)
        author = Q
        if args.author_revision or args.mutation:
            source = (subprocess.check_output(['git', 'show', f'{args.author_revision}:scripts/derive_rv64gc_expectations.py'], cwd=REPO).decode()
                      if args.author_revision else (REPO / 'scripts/derive_rv64gc_expectations.py').read_text())
            mutations = {
                'byte-directives': ('directives[unit.pc] =', 'directives[Q_ENTRY + 4 * units.index(unit)] ='),
                'padded-image': ("unit.value.to_bytes(unit.length, 'little')", "unit.value.to_bytes(4, 'little')"),
                'source-end': ('for _ in range(budget):\n        pc = hart.pc', 'for _ in range(budget):\n        if hart.pc not in program:\n            break\n        pc = hart.pc'),
                'fetch-count': ("step.fetch = sum(record[0] == 'fetch' for record in hart.log[log_start:])", 'step.fetch = 1'),
                'fault-retirement': ('if not hart.trapped:', 'if True:'),
                'head-pending': ('pending = hart.pending()', 'pending = None'),
                'code-visibility': ("info.pop('stored', None)  # every later fetch reads the updated memory directly",
                                    "stored = info.pop('stored', None)\n        if stored is not None:\n            for original in units:\n                if stored[0] <= original.pc < stored[0] + stored[1]:\n                    hart.write(original.pc, original.length, original.value)"),
                'unknown-valid': ('                hart.pc, info = execute(hart, bits)',
                                  "                try:\n                    hart.pc, info = execute(hart, bits)\n                except Refusal:\n                    hart.deliver(2, bits)\n                    info = {'deriv': 'illegal', 'source': 'mutation'}"),
            }
            if args.mutation:
                old, new = mutations[args.mutation]
                assert source.count(old) == 1, 'parcel guest mutation must match once'
                source = source.replace(old, new.replace('Q_ENTRY', 'ENTRY'))
            path = root / 'parcel_control.py'
            path.write_text(source)
            spec = importlib.util.spec_from_file_location('parcel_control', path)
            author = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = author
            spec.loader.exec_module(author)
            author.REPO = REPO
            author.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        check(author, root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
