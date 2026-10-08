#!/usr/bin/env python3
"""Check C guest generation and the tracked runner on a temporary full composition.

Words, image bytes, pc addresses and writes below are hand-derived from RVI-C 27.1
and RVI-RV32I 1.1.4. They do not come from the engine's output. All temporary inputs,
dependency stores and Cargo artifacts stay on the repository volume.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib

import dossier_sexp as D
import gen_definition as G
import gen_guests as Q
import records_sexp as R
from riscv_asm import Assembler

REPO = Path(__file__).resolve().parent.parent
MIXED = ['c.li x1, -32', 'addi x2, x1, 1', 'c.addi x2, 1',
         'c.j end', '.half 0xffff', 'end: c.mv x3, x2']
# 5081, 00108113, 0105, a011, ffff, 818a, little-endian, 14 bytes.
IMAGE = bytes.fromhex('8150 13811000 0501 11a0 ffff 8a81')
WRITES = [{'x1': '0xFFFFFFFFFFFFFFE0'}, {'x2': '0xFFFFFFFFFFFFFFE1'},
          {'x2': '0xFFFFFFFFFFFFFFE2'}, {}, {'x3': '0xFFFFFFFFFFFFFFE2'}]
DERIVATIONS = [
    'C.LI expands to ADDI rd,x0,imm; signed six-bit -32 becomes XLEN -32.',
    'ADDI sign-extends one and adds to -32, yielding -31.',
    'C.ADDI expands to ADDI rd,rd,imm; -31 plus one is -30.',
    'C.J expands to JAL x0,offset; +4 skips the explicit illegal parcel and writes no register.',
    'C.MV expands to ADD rd,x0,rs2; x3 becomes x2 (-30).',
]


def expectations(guests, name, lines, writes, derivations, fetches):
    (guests / f'{name}.s').write_text('\n'.join(lines) + '\n')
    executed = [line for line in lines if not line.startswith('.half')]
    doc = {'program': name + '.s', 'entry': '0x0000000000001000',
           'instructions': len(writes), 'fetches': fetches, 'cross_model': False,
           'step': [{'n': i, 'insn': executed[i].split(': ')[-1], 'writes': w,
                     'derivation': derivations[i], 'source': 'RVI-C 27.1; RVI-RV32I 1.1.4'}
                    for i, w in enumerate(writes)]}
    (guests / f'{name}.expected.sexp').write_text(R.render_forms([D.expectations_to_form(doc)]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--generator-revision')
    control.add_argument('--mutation', choices=['padding', 'runner-offset'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='c-guest-image-', dir=parent) as td:
        root = Path(td)
        unit = root / 'profiles/rv64gc-lab-v0'
        guests = unit / 'guests'
        guests.mkdir(parents=True)
        shutil.copytree(REPO / 'definitions', root / 'definitions')
        for name in ('profile.sexp', 'state.sexp'):
            shutil.copyfile(REPO / 'profiles/rv64gc-lab-v0' / name, unit / name)
        text = (REPO / 'profiles/rv64gc-lab-v0/encoding.sexp').read_text()
        text = text.replace('(slot (id c) (requires "riscv/c"))', '(extensions "riscv/c")')
        (unit / 'encoding.sexp').write_text(text)
        expectations(guests, 'mixed', MIXED, WRITES, DERIVATIONS, 6)
        expectations(guests, 'word', ['addi x5, x0, 7'], [{'x5': '0x0000000000000007'}],
                     ['ADDI adds sign-extended seven to hardwired x0.'], 2)
        (guests / 'run-order.txt').write_text('mixed\nword\n')
        generator = Q
        if args.generator_revision or args.mutation == 'padding':
            path = root / 'gen_guests_control.py'
            source = (subprocess.check_output(['git', 'show',
                      f'{args.generator_revision}:scripts/gen_guests.py'], cwd=REPO).decode()
                      if args.generator_revision else (REPO / 'scripts/gen_guests.py').read_text())
            if args.mutation == 'padding':
                old, new = 'u.value.to_bytes(u.length, "little")', 'u.value.to_bytes(4, "little")'
                assert source.count(old) == 1, 'padding mutation must match once'
                source = source.replace(old, new)
            path.write_text(source)
            spec = importlib.util.spec_from_file_location('gen_guests_control', path)
            generator = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(generator)
        asm = Assembler(unit / 'encoding.sexp')
        data = [generator.load_guest(name, guests, asm) for name in ('mixed', 'word')]
        assert data[0]['image'] == IMAGE, 'exact generated image bytes'
        try:
            generator.emit(data, unit / 'encoding.sexp')
        except generator.GenError as exc:
            assert 'word fixture refuses padding' in str(exc), str(exc)
        else:
            raise AssertionError('word fixture silently accepted a compressed guest')
        src = root / 'src'
        src.mkdir()
        (src / 'guests_rv64gc.rs').write_text(generator.emit(data, unit / 'encoding.sexp', 'bytes'))
        for name in ('fixtures.rs', 'run_rv64gc.rs'):
            shutil.copyfile(REPO / 'crates/semulith-verify/src' / name, src / name)
        shutil.copytree(REPO / 'crates/semulith-verify/src/fixtures', src / 'fixtures')
        if args.mutation == 'runner-offset':
            path = src / 'run_rv64gc.rs'
            source = path.read_text()
            old = 'env.load_image(0, guest.image);'
            assert source.count(old) == 1, 'runner mutation must match once'
            path.write_text(source.replace(old, 'env.load_image(2, guest.image);'))
        (src / 'lib.rs').write_text('pub mod fixtures;\npub mod guests_rv64gc;\npub mod run_rv64gc;\n')
        (src / 'run_rv64gc').mkdir()
        (src / 'run_rv64gc/tests.rs').write_text('''
use super::{assert_guest_observations, guest, run_guest};

#[test]
fn mixed_image_reaches_byte_addressed_targets_and_retains_the_trailing_parcel() {
    assert_guest_observations("mixed");
    let g = guest("mixed");
    let (trace, env) = run_guest(g);
    assert_eq!(trace.steps.iter().map(|s| s.pc).collect::<Vec<_>>(),
               [0x1000, 0x1002, 0x1006, 0x1008, 0x100c]);
    assert_eq!(g.image.len(), 14);
    assert_eq!(&env.bytes()[..16],
               &[0x81,0x50,0x13,0x81,0x10,0x00,0x05,0x01,0x11,0xa0,0xff,0xff,0x8a,0x81,0,0]);
}

#[test]
fn a_word_image_keeps_its_bytes_and_reads_two_parcels_when_c_binds() {
    assert_guest_observations("word");
    let (_, env) = run_guest(guest("word"));
    assert_eq!(&env.bytes()[..4], &[0x93,0x02,0x70,0x00]);
}
''')
        core = root / 'core'
        shutil.copytree(REPO / 'crates/semulith-core/src', core / 'src')
        definition = G.load_inputs(unit / 'encoding.sexp', unit / 'state.sexp')
        (core / 'src/definition_rv64gc.rs').write_text(G.emit(definition, G.sha256(REPO / 'scripts/gen_definition.py')))
        dep = tomllib.loads((REPO / 'crates/semulith-core/Cargo.toml').read_text())['dependencies']['rustc_apfloat']
        assert isinstance(dep, str), 'probe must follow the core dependency declaration'
        (core / 'Cargo.toml').write_text('[package]\nname="semulith-core"\nversion="0.1.0"\nedition="2021"\n'
                                       '[dependencies]\nrustc_apfloat="' + dep + '"\n')
        (root / 'Cargo.toml').write_text('[package]\nname="c-guest-image-probe"\nversion="0.0.0"\nedition="2021"\n'
                                       '[workspace]\n[dependencies]\nsemulith-core={path="core"}\n')
        env = dict(os.environ, CARGO_HOME=str(REPO / '.app-data/cargo-home'),
                   CARGO_TARGET_DIR=str(parent / 'c-guest-image-build'), TMPDIR=str(parent))
        run = subprocess.run(['cargo', 'test', '--offline', '--manifest-path', str(root / 'Cargo.toml'),
                              '--lib', 'run_rv64gc::tests::', '--', '--nocapture'],
                             cwd=REPO, env=env, capture_output=True, text=True)
        print(run.stdout)
        if run.returncode:
            print(run.stderr)
            print('C guest image probe: FAIL')
            return 1
        print('C guest image probe: mixed bytes, labels, writes and parcel counts passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
