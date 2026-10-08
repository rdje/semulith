#!/usr/bin/env python3
"""Independent fixtures for the selected Sv39 cache and SFENCE policy.

RVP-SUPERVISOR 11.1.2.1/11.1.3.2/11.1.4.1 supplies permissions and fence
scopes; state.sexp SEM-08 selects four FIFO slots, 4-KiB keys and ASIDLEN=16.
No instruction engine, production cache implementation or generated rules are read.
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


def table(author, flags=0xcf, ancestor_global=False):
    h = author.Hart()
    base = author.ENTRY
    h.mode = author.S
    h.csr['satp'] = (8 << 60) | ((base + 0x1000) >> 12)
    h.write(base + 0x1000, 8, (((base + 0x2000) >> 12) << 10) | 1 | (0x20 if ancestor_global else 0))
    h.write(base + 0x2000, 8, (((base + 0x3000) >> 12) << 10) | 1)
    for page in range(6):
        edit(h, page, base + 0x4000 + page * 0x1000, flags)
    return h


def edit(h, page, pa, flags=0xcf):
    h.write(Q.ENTRY + 0x3000 + page * 8, 8, ((pa >> 12) << 10) | flags)


def tags(h):
    return {(e[0], e[1], e[2]) for e in h.translation_cache if e is not None}


def fence(author, h, word=0x12000073):
    _, info = author.execute(h, word)
    assert not h.trapped and not info.get('writes'), 'legal fence changed architectural registers'


def check(author):
    base = author.ENTRY
    h = table(author)
    assert h.walk(7, 'load') == ('pa', base + 0x4007)
    edit(h, 0, base + 0xe000)
    h.log.clear()
    assert h.walk(7, 'load') == ('pa', base + 0x4007), 'cache must retain stale mapping until fence'
    assert not h.log, 'cache hit performed a page-table request'
    assert h.translation_cursor == 1, 'FIFO hit must not refresh replacement order'
    cursor = h.translation_cursor
    fence(author, h)
    assert h.translation_cursor == cursor == 1, 'fence changed FIFO cursor'
    assert h.walk(7, 'load') == ('pa', base + 0xe007), 'full fence did not expose PTE edit'

    # Four distinct cache keys. A nonzero register holding zero selects only
    # page/ASID zero. The words encode rs1=x3 and/or rs2=x4, without an assembler.
    def seeded():
        h = table(author)
        edit(h, 1, base + 0x5000, 0xef)  # global leaf
        for page, asid in ((0, 0), (1, 0), (2, 1), (3, 0)):
            h.csr['satp'] = (h.csr['satp'] & ~(0xffff << 44)) | (asid << 44)
            assert h.walk(page * 0x1000, 'load') == ('pa', base + 0x4000 + page * 0x1000)
        h.x[3], h.x[4] = 0, 0
        return h

    cases = ((0x12000073, set()),
             (0x12400073, {(1, 0, True), (2, 1, False)}),
             (0x12018073, {(1, 0, True), (2, 1, False), (3, 0, False)}),
             (0x12418073, {(1, 0, True), (2, 1, False), (3, 0, False)}))
    for word, expected in cases:
        h = seeded()
        cursor = h.translation_cursor
        fence(author, h, word)
        assert tags(h) == expected, 'fence must use register identity and exact scope'
        assert h.translation_cursor == cursor, 'fence changed FIFO cursor'
    h = seeded()
    h.x[4] = 1 << 16
    fence(author, h, 0x12400073)
    assert tags(h) == cases[1][1], 'fence must mask ASIDLEN without selecting x0 scope'
    h = seeded()
    before = h.translation_cache.copy()
    h.x[3] = 1 << 38
    fence(author, h, 0x12018073)
    assert h.translation_cache == before, 'invalid fence VA must have no effect'
    h = seeded()
    h.x[3] = 0x1007  # page selection ignores byte offset, but preserves globals for ASID scope
    fence(author, h, 0x12418073)
    assert (1, 0, True) in tags(h), 'ASID fence must preserve global entries'
    fence(author, h, 0x12018073)
    assert (1, 0, True) not in tags(h), 'address-only fence must invalidate global entries'
    for mode, status in ((0, 0), (author.S, 1 << 20)):
        h = seeded()
        before = h.translation_cache.copy(), h.translation_cursor
        h.mode, h.csr['mstatus'] = mode, status
        author.execute(h, 0x12000073)
        assert h.trapped and h.csr['mcause'] == 2 and h.csr['mtval'] == 0x12000073
        assert (h.translation_cache, h.translation_cursor) == before, 'illegal fence must not change cache'

    h = table(author, ancestor_global=True)
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    edit(h, 0, base + 0xe000)
    h.csr['satp'] |= 1 << 44
    h.log.clear()
    assert h.walk(0, 'load') == ('pa', base + 0x4000) and not h.log, 'non-leaf G must propagate to cache entry'
    h.x[4] = 1
    fence(author, h, 0x12400073)
    assert tags(h) == {(0, 0, True)}, 'per-ASID fence removed inherited global'
    fence(author, h)
    assert h.walk(0, 'load') == ('pa', base + 0xe000)

    # Ordinary ASID changes select another translation; switching back can hit.
    h = table(author)
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    edit(h, 0, base + 0xe000)
    h.csr['satp'] |= 1 << 44
    assert h.walk(0, 'load') == ('pa', base + 0xe000), 'ASID change must be immediately visible'
    h.csr['satp'] &= ~(0xffff << 44)
    assert h.walk(0, 'load') == ('pa', base + 0x4000), 'ASID switch implicitly flushed cache'
    # Root changes are observed on misses; same-ASID cached translations survive.
    h.csr['satp'] = (8 << 60) | ((base + 0x6000) >> 12)  # zero/invalid new root
    assert h.walk(0, 'load') == ('pa', base + 0x4000), 'satp root change implicitly flushed cache'
    assert h.walk(0x2000, 'load') == ('fault', 13), 'cache miss ignored new root'
    fence(author, h)
    assert h.walk(0, 'load') == ('fault', 13)

    h = table(author)
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    saved = h.csr['satp']
    h.csr['satp'] = 0
    assert h.walk(0, 'load') == ('pa', 0), 'Bare must bypass cache'
    h.csr['satp'], h.mode = saved, author.M
    assert h.walk(0, 'fetch') == ('pa', 0), 'M fetch must bypass cache'
    h.csr['mstatus'] |= (1 << 17) | (author.S << 11)
    assert h.walk(0, 'load') == ('pa', base + 0x4000), 'MPRV must select effective mode before cache lookup'
    h.mode = author.S
    h.log.clear()
    assert h.walk(1 << 38, 'load') == ('fault', 13) and not h.log, 'canonical check must precede cache lookup'

    # Current privilege/SUM/MXR apply to hits; permissions and A/D remain cached.
    h = table(author, flags=0xdf)
    h.csr['mstatus'] |= 1 << 18
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    h.log.clear()
    h.csr['mstatus'] &= ~(1 << 18)
    assert h.walk(0, 'load') == ('fault', 13) and not h.log, 'cache hit must recheck live SUM'
    h.mode = 0
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    h.mode = author.S
    h.csr['mstatus'] |= 1 << 18
    assert h.walk(0, 'fetch') == ('fault', 12), 'SUM must never permit S fetch from cached U page'
    h.mode = author.M
    h.csr['mstatus'] |= (1 << 17) | (author.S << 11)
    h.csr['mstatus'] &= ~(1 << 18)
    assert h.walk(0, 'load') == ('fault', 13), 'cache hit must recheck effective MPRV privilege'
    h = table(author, flags=0xc9)
    assert h.walk(0, 'fetch') == ('pa', base + 0x4000)
    h.log.clear()
    assert h.walk(0, 'load') == ('fault', 13) and not h.log, 'cache hit must recheck live MXR'
    h.csr['mstatus'] |= 1 << 19
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    h = table(author)
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    h.mode = 0
    assert h.walk(0, 'load') == ('fault', 13), 'cache hit must recheck current U permission'
    h = table(author, flags=0x4f)  # A=1,D=0; load succeeds and installs
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    edit(h, 0, base + 0xe000)
    h.log.clear()
    assert h.walk(0, 'store') == ('fault', 15) and not h.log, 'cached D=0 must fault without rewalking'
    fence(author, h)
    assert h.walk(0, 'store') == ('pa', base + 0xe000)
    h = table(author, flags=0x0f)  # A=0 faults; never installs or writes a PTE
    before = h.mem.copy()
    assert h.walk(0, 'load') == ('fault', 13) and not tags(h), 'fault must not install cache entry'
    assert h.mem == before, 'Svade fault wrote PTE'
    edit(h, 0, base + 0xe000)
    assert h.walk(0, 'load') == ('pa', base + 0xe000), 'fault installed a stale entry'

    # Four fills wrap FIFO to slot zero. A hit does not refresh age. A selective
    # fence frees slot one, but the next miss still replaces slot zero.
    h = table(author)
    for page in range(4):
        assert h.walk(page * 0x1000, 'load') == ('pa', base + 0x4000 + page * 0x1000)
    assert h.walk(0, 'load') == ('pa', base + 0x4000)
    assert h.walk(0x4000, 'load') == ('pa', base + 0x8000)
    assert tags(h) == {(i, 0, False) for i in (1, 2, 3, 4)}, 'FIFO hit must not refresh replacement order'
    h = table(author)
    for page in range(4):
        h.walk(page * 0x1000, 'load')
    h.x[3] = 0x1000
    fence(author, h, 0x12018073)
    h.walk(0x4000, 'load')
    assert tags(h) == {(i, 0, False) for i in (2, 3, 4)}, 'FIFO must retain cursor through selective fence'
    # Superpages are cached as separate 4-KiB keys, not one broad entry.
    h = author.Hart()
    h.mode = author.S
    h.csr['satp'] = (8 << 60) | (base >> 12)
    h.write(base, 8, ((base >> 12) << 10) | 0xcf)
    for va in (7, 0x1007):
        assert h.walk(va, 'load') == ('pa', base + va)
    assert tags(h) == {(0, 0, False), (1, 0, False)}, 'superpage must use independent 4-KiB cache keys'

    asm = Assembler(REPO / 'profiles/rv64gc-lab-v0/encoding.sexp')
    path = REPO / 'profiles/rv64gc-lab-v0/guests/sv39-tlb-fence.s'
    expected = D.load_expectations(path.with_suffix('.expected.sexp'))
    runs = [author.derive_parcel_guest(path, asm, expected['instructions']) for _ in range(2)]
    writes = [{int(k[1:]): int(v, 16) for k, v in st['writes'].items()} for st in expected['step']]
    assert [st.writes for st in runs[0].steps] == writes, 'cached corpus architectural observations differ'
    assert runs[0].hart.log == runs[1].hart.log, 'cold cache repeat request trace differs'
    assert author.main(['probe', '--check-owned']) == 0
    print('GC cache author probe: FIFO/scopes/ASIDs/globals/live permissions; cached corpus exact and cold repeat')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--author-revision')
    changes = {
        'bypass-hit': ('if page == va >> 12 and (global_mapping or tag == asid):', 'if False:'),
        'fence-value': ('None if rs1 == 0 else x[rs1]', 'None if x[rs1] == 0 else x[rs1]'),
        'fence-asid-value': ('None if rs2 == 0 else x[rs2]', 'None if x[rs2] == 0 else x[rs2]'),
        'global-inheritance': ('global_mapping = global_mapping or bool(pte & 0x20)', 'global_mapping = bool(pte & 0x20)'),
        'asid-tag': ('(global_mapping or tag == asid)', 'True'),
        'cached-permission': ('if not self.permits_translation(leaf_pte, mode, kind):', 'if False:'),
        'fault-install': ('if not self.permits_translation(pte, mode, kind):\n                    return',
                          'if not self.permits_translation(pte, mode, kind):\n                    self.translation_cache[0] = (va >> 12, asid, global_mapping, 0, pte)\n                    return'),
        'fifo-hit': ('return ("pa", physical_page | (va & 0xfff))',
                     'self.translation_cursor = (self.translation_cursor + 1) % 4\n                return ("pa", physical_page | (va & 0xfff))'),
        'fence-cursor': ('selected_asid = None if asid is None else asid & 0xffff',
                         'self.translation_cursor = 0\n        selected_asid = None if asid is None else asid & 0xffff'),
        'asid-mask': ('None if asid is None else asid & 0xffff', 'asid'),
        'global-retention': ('not global_mapping and tag == selected_asid', 'tag == selected_asid'),
        'invalid-fence': ('if va >> 39 != upper:\n                return',
                          'if va >> 39 != upper:\n                va = None'),
        'illegal-fence': ('if (word & 0xFE007FFF) == 0x12000073:  # sfence.vma',
                          'if (word & 0xFE007FFF) == 0x12000073:  # sfence.vma\n'
                          '            if h.mode < S or (h.mode == S and (h.csr["mstatus"] >> 20) & 1):\n'
                          '                h.invalidate_translation()'),
    }
    control.add_argument('--mutation', choices=changes)
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gc-cache-author-', dir=parent) as td:
        author = Q
        if args.author_revision or args.mutation:
            source = (subprocess.check_output(['git', 'show', f'{args.author_revision}:scripts/derive_rv64gc_expectations.py'], cwd=REPO).decode()
                      if args.author_revision else (REPO / 'scripts/derive_rv64gc_expectations.py').read_text())
            if args.mutation:
                old, new = changes[args.mutation]
                assert source.count(old) == 1, 'cache mutation must match once'
                source = source.replace(old, new)
            path = Path(td) / 'cache_control.py'
            path.write_text(source)
            spec = importlib.util.spec_from_file_location('cache_control', path)
            author = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = author
            spec.loader.exec_module(author)
            author.REPO = REPO
            author.ENCODING = REPO / 'profiles/rv64gc-lab-v0/encoding.sexp'
        check(author)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
