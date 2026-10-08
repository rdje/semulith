#!/usr/bin/env python3
"""Independent CSR enable, timer permission and literal-string author controls.

RVP-MACHINE 2.1.1.11/2.1.1.18 and RVP-SUPERVISOR 11.1.1.5 define
accessibility; selected state fields fix masks. No instruction engine is used.
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
import records_sexp as R
import sexp as S
from riscv_asm import Assembler

REPO = Path(__file__).resolve().parent.parent


def check(author, root):
    for name, mask in (('mcounteren', 7), ('scounteren', 7), ('menvcfg', 1 << 63)):
        hart = author.Hart()
        for value in (0xffffffffffffffff, 0, 2):
            author.csr_write_value(hart, name, value)
            assert author.csr_read_value(hart, name) == value & mask, 'CSR enable legalization'
        # WPRI preserves an existing high bit, never imports a proposed one.
        hart.csr[name] = 1 << (40 if name != 'menvcfg' else 20)
        author.csr_write_value(hart, name, 0)
        assert hart.csr[name] == 1 << (40 if name != 'menvcfg' else 20), 'CSR WPRI retention'

    # CSRRS x5,mcounteren,x5 reads its source before returning the old enable mask.
    hart = author.Hart()
    hart.x[5] = 2
    try:
        pc, info = author.execute(hart, 0x3062a2f3)
    except author.Refusal as exc:
        raise AssertionError('enable CSR address vocabulary') from exc
    assert pc == Q.ENTRY + 4 and info['writes'] == {5: 0}
    assert hart.x[5] == 2 and hart.csr['mcounteren'] == 2, 'CSR alias reads pre-state'

    def access(word, mode, m_enable, s_enable, env, legal, message):
        hart = author.Hart()
        hart.mode = mode
        hart.time, hart.instret = 17, 11
        hart.csr.update(mcounteren=m_enable, scounteren=s_enable, menvcfg=env,
                        stimecmp=101, mtvec=Q.ENTRY + 0x100)
        hart.x[5] = 0x55
        before = hart.x.copy(), hart.csr['stimecmp'], hart.mem.copy()
        pc, info = author.execute(hart, word)
        if legal:
            assert not hart.trapped and pc == Q.ENTRY + 4, message
            expected = {0xc00: 17, 0xc01: 17, 0xc02: 11, 0x14d: 101}[word >> 20]
            assert info['writes'] == {5: expected}, message
        else:
            assert hart.trapped and hart.csr['mcause'] == 2 and hart.csr['mtval'] == word, message
            assert hart.csr['mepc'] == Q.ENTRY and pc == Q.ENTRY + 0x100, message
            assert not info.get('writes') and (hart.x, hart.csr['stimecmp'], hart.mem) == before, message
        assert (hart.time, hart.instret) == (17, 11), 'access gate changed counter progress'

    for csr, bit in ((0xc00, 0), (0xc01, 1), (0xc02, 2)):
        word = (csr << 20) | 0x22f3  # CSRRS x5,csr,x0
        for mode, m, s, legal in ((author.M, 0, 0, True), (author.S, 0, 7, False),
                                  (author.S, 1 << bit, 0, True), (0, 0, 7, False),
                                  (0, 1 << bit, 0, False), (0, 1 << bit, 1 << bit, True)):
            access(word, mode, m, s, 0, legal, 'counter mode enable gate')
    for word in (0x14d022f3, 0x14d292f3):  # stimecmp read / CSRRW x5,stimecmp,x5
        for mode, m, env, legal in ((author.M, 0, 0, True), (author.S, 0, 0, False),
                                    (author.S, 0, 1 << 63, False), (author.S, 2, 0, False),
                                    (author.S, 2, 1 << 63, True), (0, 7, 1 << 63, False)):
            reason = 'stimecmp TM gate' if not m and env else 'stimecmp STCE gate'
            access(word, mode, m, 7, env, legal, reason)
    # A legal enabled write changes only the declared compare field, not the old source.
    hart = author.Hart()
    hart.mode = author.S
    hart.csr.update(mcounteren=2, menvcfg=1 << 63, stimecmp=101)
    hart.x[5] = 0x55
    _, info = author.execute(hart, 0x14d292f3)
    assert info['writes'] == {5: 101} and hart.csr['stimecmp'] == 0x55 and hart.x[5] == 0x55

    asm = Assembler(REPO / 'profiles/rv64gc-lab-v0/encoding.sexp')
    source = root / 'quoted.s'
    source.write_text('addi x1, x0, 1 #: quoted "rule" and path\\part §27 | source "label" \\ locator\n')
    run = author.derive_parcel_guest(source, asm, 1)
    expected_deriv = 'quoted "rule" and path\\part §27'
    expected_source = 'source "label" \\ locator'
    out = root / 'quoted.expected.sexp'
    out.write_text(author.emit(source, run.steps, 1, []))
    doc = D.load_expectations(out)
    assert doc['step'][0]['derivation'].count('"') == 2, 'quoted directive lost literal text'
    assert doc['step'][0]['derivation'] == expected_deriv, 'backslash directive lost literal text'
    assert doc['step'][0]['source'] == expected_source, 'backslash directive lost literal text'
    # All string fields, including program and instruction, use the same escape path.
    st = author.Step(Q.ENTRY, 'instruction "x"\\tail\n\t\r§')
    st.deriv, st.source = expected_deriv + '\n\t\r', expected_source
    path = Path('program"\\name.s')
    out.write_text(author.emit(path, [st], 1, []))
    doc = D.load_expectations(out)
    assert doc['program'] == path.name and doc['step'][0]['insn'] == st.insn, 'string fields lost literal text'
    assert doc['step'][0]['derivation'] == st.deriv and doc['step'][0]['source'] == st.source, 'string fields lost literal text'
    rendered = R.render_forms([[S.Symbol('literal'), expected_deriv + '\n\t\r']])
    assert S.parse(rendered)[0][1] == expected_deriv + '\n\t\r', 'canonical renderer round-trip'
    try:
        R.quote_string(123)
    except R.RecordRefused:
        pass
    else:
        raise AssertionError('non-string literal was rendered')
    judged = subprocess.run(['python3', 'scripts/check_sexp_schema.py', str(out.relative_to(REPO)),
                             'schema/expectations.sexp'], cwd=REPO, capture_output=True, text=True)
    assert judged.returncode == 0, judged.stderr

    total = 0
    for name in ('a-lrsc-mustfail', 'mm-counters', 'mm-stimecmp'):
        path = REPO / 'profiles/rv64gc-lab-v0/guests' / (name + '.s')
        expected = D.load_expectations(path.with_suffix('.expected.sexp'))
        run = author.derive_parcel_guest(path, asm, expected['instructions'])
        writes = [{int(k[1:]): int(v, 16) for k, v in st['writes'].items()} for st in expected['step']]
        assert [st.writes for st in run.steps] == writes, f'{name}: CSR/directive architectural observations differ'
        total += len(run.steps)
    assert author.main(['probe', '--check-owned']) == 0
    print(f'GC counter author probe: enable masks/aliases, 30 mode gates, quoted text/schema; 3 corpus refusals / {total} steps')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--author-revision')
    changes = {
        'enable-mask': ('(old & ~0xffffffff) | (v & 7)', 'v'),
        'stce-mask': ('(old & ~(1 << 63)) | (v & (1 << 63))', 'v'),
        'timer-tm': ('if not tm or not stce:', 'if not stce:'),
        'timer-stce': ('if not tm or not stce:', 'if not tm:'),
        'counter-enable': ('if h.mode != 3 and not open_s and not open_u:', 'if False:'),
        'u-counter-enable': ('and (h.csr["scounteren"] >> bit) & 1)', ')'),
        'quote-text': ('quote = R.quote_string', 'quote = lambda value: R.quote_string(value.replace(chr(34), ""))'),
        'backslash-text': ('quote = R.quote_string', 'quote = lambda value: R.quote_string(value.replace(chr(92), ""))'),
    }
    control.add_argument('--mutation', choices=changes)
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-counter-author-', dir=parent) as td:
        author = Q
        if args.author_revision or args.mutation:
            source = (subprocess.check_output(['git', 'show', f'{args.author_revision}:scripts/derive_rv64gc_expectations.py'], cwd=REPO).decode()
                      if args.author_revision else (REPO / 'scripts/derive_rv64gc_expectations.py').read_text())
            if args.mutation:
                old, new = changes[args.mutation]
                assert source.count(old) == 1, 'counter mutation must match once'
                source = source.replace(old, new)
            path = Path(td) / 'counter_control.py'
            path.write_text(source)
            spec = importlib.util.spec_from_file_location('counter_control', path)
            author = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = author
            spec.loader.exec_module(author)
            author.REPO = REPO
            author.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        check(author, Path(td))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
