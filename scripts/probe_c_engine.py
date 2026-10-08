#!/usr/bin/env python3
"""Compile the tracked engine against a temporary C composition and run extent/width probes.

The probe is finite engine evidence, not a profile acceptance result. All generated inputs,
Cargo outputs and temporary workspaces stay under target/p4-system-12. --engine-revision
replaces only the evaluator with a committed predecessor for the RED control.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib

import gen_definition as G

REPO = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    control = parser.add_mutually_exclusive_group()
    control.add_argument('--engine-revision')
    control.add_argument('--mutation', choices=['erase-expansion-widths', 'word-parcel-read'])
    args = parser.parse_args()
    parent = REPO / 'target/p4-system-12'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='c-engine-', dir=parent) as td:
        root = Path(td)
        unit = root / 'profiles/rv64gc-lab-v0'
        unit.mkdir(parents=True)
        shutil.copytree(REPO / 'definitions', root / 'definitions')
        encoding = (REPO / 'profiles/rv64gc-lab-v0/encoding.sexp').read_text()
        slot = '(slot (id c) (requires "riscv/c"))'
        if slot in encoding:
            encoding = encoding.replace(slot, '(extensions "riscv/c")')
        elif '(extensions "riscv/c")' not in encoding:
            raise RuntimeError('the unit declares neither the C slot nor the C composition')
        (unit / 'encoding.sexp').write_text(encoding)
        src = root / 'src'
        shutil.copytree(REPO / 'crates/semulith-core/src', src)
        data = G.load_inputs(unit / 'encoding.sexp', REPO / 'profiles/rv64gc-lab-v0/state.sexp')
        (src / 'definition_rv64gc.rs').write_text(G.emit(data, G.sha256(REPO / 'scripts/gen_definition.py')))
        if args.engine_revision:
            (src / 'exec_rv64gc.rs').write_bytes(subprocess.check_output([
                'git', 'show', f'{args.engine_revision}:crates/semulith-core/src/exec_rv64gc.rs'], cwd=REPO))
        if args.mutation:
            engine = src / 'exec_rv64gc.rs'
            text = engine.read_text()
            changes = {
                'erase-expansion-widths': [('(binding.name, value, width)', '(binding.name, value, 64)')],
                'word-parcel-read': [
                    ('Request::FetchParcel { addr: pa }', 'Request::Fetch { addr: pa }'),
                    ('Ok(Response::FetchParcel(parcel)) => Ok(parcel)',
                     'Ok(Response::Fetch(parcel)) => Ok(parcel as u16)'),
                ],
            }
            for old, new in changes[args.mutation]:
                if text.count(old) != 1:
                    raise RuntimeError(f'mutation seam must match once: {old}')
                text = text.replace(old, new)
            engine.write_text(text)
        with (src / 'lib.rs').open('a') as lib:
            lib.write('\n#[cfg(test)] mod c_engine;\n')
        shutil.copyfile(REPO / 'scripts/probes/c_engine.rs', src / 'c_engine.rs')
        manifest = tomllib.loads((REPO / 'crates/semulith-core/Cargo.toml').read_text())
        dep = manifest['dependencies']['rustc_apfloat']
        assert isinstance(dep, str), 'probe must follow the core dependency declaration'
        (root / 'Cargo.toml').write_text('[package]\nname = "c-engine-probe"\nversion = "0.0.0"\nedition = "2021"\n'
                                      '[workspace]\n[dependencies]\nrustc_apfloat = "' + dep + '"\n')
        env = dict(os.environ, CARGO_HOME=str(REPO / '.app-data/cargo-home'),
                   CARGO_TARGET_DIR=str(parent / 'c-engine-build'), TMPDIR=str(parent))
        run = subprocess.run(['cargo', 'test', '--offline', '--manifest-path', str(root / 'Cargo.toml'),
                              '--lib', 'c_engine::', '--', '--nocapture'], cwd=REPO, env=env,
                             capture_output=True, text=True)
        print(run.stdout)
        if run.returncode:
            print(run.stderr)
            print('C engine probe: FAIL')
            return 1
        print('C engine probe: exact parcel and expansion execution checks passed')
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
