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


def timer_step(author, hart, word):
    hart.trapped = False
    assert hart.pending() is None, 'timer witness unexpectedly enables delivery'
    assert hart.fetch_instruction() == ('insn', word, 4), 'timer literal parcel fetch'
    hart.pc, info = author.execute(hart, word)
    for reg, value in info.get('writes', {}).items():
        hart.x[reg] = value
    hart.time += 1
    if not hart.trapped:
        hart.instret += 1


def timer_hart(author):
    hart = author.Hart()
    hart.mode = author.S
    hart.csr.update(mcounteren=2, menvcfg=1 << 63, mideleg=32)
    for reg in range(6, 12):
        hart.x[reg] = 0x55
    hart.x[12], hart.x[13] = 0x8000000000000020, 0x55
    return hart


def sstc_positive(author):
    # Literal words and observations are independently specified before engine runs.
    rows = [
        (0x01000293, (5, 16), 0), (0x14d29373, (6, 0), 16),
        (0x14d023f3, (7, 16), 16), (0x14402473, (8, 0), 16),
        (0x00000293, (5, 0), 16), (0x14d29073, None, 0),
        (0x144024f3, (9, 32), 0), (0x02000293, (5, 32), 0),
        (0x14d29073, None, 32), (0x14d02573, (10, 32), 32),
        (0x144025f3, (11, 0), 32),
        (0x14d61073, None, 0x8000000000000020),
        (0x14d026f3, (13, 0x8000000000000020), 0x8000000000000020),
    ]
    hart = timer_hart(author)
    for i, (word, _, _) in enumerate(rows):
        hart.write(Q.ENTRY + i * 4, 4, word)
    expected = hart.x.copy()
    for i, (word, write, compare) in enumerate(rows, 1):
        if write:
            expected[write[0]] = write[1]
        timer_step(author, hart, word)
        assert (hart.x, hart.mode, hart.pc, hart.csr['stimecmp'], hart.time, hart.instret) == (
            expected, author.S, Q.ENTRY + i * 4, compare, i, i), f'Sstc positive boundary {i}'
        assert len(hart.log) == 2 * i, 'Sstc positive parcel count'


def sstc_negative(author):
    word = 0x14d29373
    handler = [0x342023f3, 0x34302473, 0x341024f3, 0x14d02573, 0x02a00593]
    for mode, tm, stce in [(author.S, 0, 1 << 63), (author.S, 2, 0), (0, 2, 1 << 63)]:
        hart = timer_hart(author)
        hart.mode = mode
        hart.csr.update(mcounteren=tm, menvcfg=stce, stimecmp=101, mtvec=Q.ENTRY + 0x100)
        hart.x[5] = 33
        hart.write(Q.ENTRY, 4, word)
        for i, instruction in enumerate(handler):
            hart.write(Q.ENTRY + 0x100 + i * 4, 4, instruction)
        expected = hart.x.copy()
        observations = [None, (7, 2), (8, word), (9, Q.ENTRY), (10, 101), (11, 42)]
        for i, (instruction, write) in enumerate(zip([word] + handler, observations)):
            if write:
                expected[write[0]] = write[1]
            timer_step(author, hart, instruction)
            assert (hart.x, hart.mode, hart.pc, hart.csr['stimecmp'], hart.time, hart.instret) == (
                expected, author.M, Q.ENTRY + 0x100 + i * 4, 101, i + 1, i), 'Sstc refusal before effects'
            assert (hart.csr['mcause'], hart.csr['mtval'], hart.csr['mepc']) == (2, word, Q.ENTRY), 'Sstc refusal trap owners'
            assert len(hart.log) == 2 * (i + 1), 'Sstc negative parcel count'


def terminal_control(root, positive):
    # Same defect model as c13's diagnosis, using a scratch author copy, never an
    # implementation edit: every S-mode stimecmp access traps, even with open gates.
    source = Path(Q.__file__).read_text()
    old = 'if not tm or not stce:'
    assert source.count(old) == 1
    path = root / 'forced_s_timer.py'
    path.write_text(source.replace(old, 'if True:'))
    spec = importlib.util.spec_from_file_location('forced_s_timer', path)
    forced = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = forced
    spec.loader.exec_module(forced)
    forced.REPO = REPO
    forced.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
    guest = REPO / 'profiles/rv64gc-lab-v0/guests/mm-stimecmp.s'
    doc = D.load_expectations(guest.with_suffix('.expected.sexp'))
    run = forced.derive_parcel_guest(guest, Assembler(forced.ENCODING), 35)
    expected = [{int(k[1:]): int(v, 16) for k, v in st['writes'].items()} for st in doc['step']]
    assert [st.writes for st in run.steps] == expected and sum(st.fetch for st in run.steps) == 70, 'old terminal witness no longer reproduces'
    assert (run.hart.mode, run.hart.csr['mcause'], run.hart.csr['mepc']) == (forced.M, 2, Q.ENTRY + 0x44)
    try:
        positive(forced)
    except AssertionError as exc:
        assert str(exc) == 'Sstc positive boundary 2', f'wrong forced-S refusal: {exc}'
    else:
        raise AssertionError('Sstc terminal control missed: disabled positive witness')


def check(author, root, *, positive=sstc_positive):
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

    # Literal STCE/source combinations: software pending ignores compare when disabled.
    for enabled, compare, raw, visible in (
        (0, 0, 0, 0), (0, 101, 0, 0), (0, 0, 32, 32), (0, 101, 32, 32),
        (1 << 63, 0, 0, 32), (1 << 63, 101, 0, 0),
        (1 << 63, 0, 32, 32), (1 << 63, 101, 32, 0),
    ):
        hart = author.Hart()
        hart.csr.update(menvcfg=enabled, stimecmp=compare, mip=raw, mideleg=32)
        assert author.csr_read_value(hart, 'mip') == visible, 'STIP source selection'
        assert author.csr_read_value(hart, 'sip') == visible, 'delegated STIP source'
        author.csr_write_value(hart, 'sip', 0)
        assert hart.csr['mip'] == raw, 'sip STIP is always read-only'
        author.csr_write_value(hart, 'mip', 0)
        assert hart.csr['mip'] == (raw if enabled else 0), 'STIP write mask'
        author.csr_write_value(hart, 'mip', 0xffffffffffffffff)
        assert hart.csr['mip'] == (0x202 | raw if enabled else 0x222), 'STIP write mask'
    hart = author.Hart()
    hart.csr.update(mip=32, stimecmp=101)
    author.csr_write_value(hart, 'menvcfg', 1 << 63)
    assert author.csr_read_value(hart, 'mip') == 0 and hart.csr['mip'] == 32, 'STIP retained software storage'
    author.csr_write_value(hart, 'menvcfg', 0)
    assert author.csr_read_value(hart, 'mip') == 32, 'STIP retained software storage'

    positive(author)
    sstc_negative(author)
    terminal_control(root, positive)

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
    print(f'GC counter author probe: enable masks/aliases, 30 mode gates, eight STIP source/write cases and retention, Sstc 31 boundaries / 62 parcels; terminal 35/70 misses forced S trap, direct witness refuses; quoted text/schema; 3 corpus refusals / {total} steps')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--author-revision')
    control.add_argument('--disable-sstc-witness', action='store_true', help='deliberate verifier control')
    changes = {
        'stip-source': ('if not (self.csr["menvcfg"] >> 63) & 1:', 'if False:'),
        'stip-fallback-write': ('writable = 0x202 if (h.csr["menvcfg"] >> 63) & 1 else 0x222', 'writable = 0x202'),
        'stip-enabled-write': ('writable = 0x202 if (h.csr["menvcfg"] >> 63) & 1 else 0x222', 'writable = 0x222'),
        'stip-retention': ('h.csr[name] = (old & ~(1 << 63)) | (v & (1 << 63))',
                           'h.csr[name] = (old & ~(1 << 63)) | (v & (1 << 63)); h.csr["mip"] &= ~32'),
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
        positive = (lambda author: None) if args.disable_sstc_witness else sstc_positive
        check(author, Path(td), positive=positive)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
