#!/usr/bin/env python3
"""Qualify atomic alignment through the pinned Sail public interface.

This is a live diagnostic, not a CI gate. Expectations are derived before the
reference executes. The paired granule control shows why AccessFault alone is
insufficient to match the laboratory's unconditional atomic-alignment policy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

import derive_rv64gc_expectations as Q
import dossier_sexp as D
from riscv_asm import Assembler, AsmError, write_elf64
import run_rv64gc_sail as S

FORMS = ('lr', 'sc', 'amoswap', 'amoadd', 'amoxor', 'amoand', 'amoor',
         'amomin', 'amomax', 'amominu', 'amomaxu')
BOUNDARIES = 13


def prepare(output: Path, asm: Assembler, form: str, width: int, offset: int) -> dict:
    name = f'{form}-{"w" if width == 4 else "d"}-{offset}'
    mnemonic = f'{form}.{"w" if width == 4 else "d"}'
    instruction = (f'{mnemonic} x5, (x2)' if form == 'lr'
                   else f'{mnemonic} x5, x6, (x2)')
    # Both a completed access and a trap reach instruction 9. CSR/data read-backs
    # distinguish them; the destination sentinel exposes a completed old-value write.
    source = f'''auipc x1, 0
addi x1, x1, 36
csrrw x0, mtvec, x1
addi x10, x0, 1
slli x10, x10, 31
addi x2, x10, {256 + offset}
addi x6, x0, 42
addi x5, x0, 17
{instruction}
csrrs x11, mcause, x0
csrrs x12, mtval, x0
ld x13, x10, 256
ld x14, x10, 264
'''
    path = output / f'{name}.s'
    path.write_text(source)
    record, _ = Q.run_parcel_guest(path, asm, BOUNDARIES)
    expected_path = output / f'{name}.expected.sexp'
    expected_path.write_text(record)
    expected = D.load_expectations(expected_path)
    entry = int(expected['entry'], 16)
    # Explicitly initialize all data bytes on both sides of the granule boundary.
    units = asm.assemble_units(source.splitlines(), entry)
    if len(units) != BOUNDARIES or any(unit.length != 4 for unit in units):
        raise S.SailError(f'{name}: the literal program must have thirteen 32-bit words')
    payload = asm.assemble_image(source.splitlines(), base=entry).ljust(0x200, b'\0')
    elf = output / f'{name}.elf'
    write_elf64(elf, entry, payload, asm.ialign)
    return {'name': name, 'form': form, 'width': width, 'offset': offset,
            'expected': expected, 'elf': elf, 'entry': entry, 'words': [u.value for u in units]}


def validate(binary: Path, config: Path, output: Path, label: str, env: dict) -> None:
    process = subprocess.run([str(binary), '--config-override', str(config), '--validate-config'],
                             capture_output=True, text=True, env=env)
    (output / f'{label}.validate.log').write_text(process.stdout + process.stderr)
    if process.returncode != 0:
        raise S.SailError(f'{label}: public configuration validation failed: rc={process.returncode}')


def observe(binary: Path, config: Path, output: Path, case: dict, label: str, env: dict) -> dict:
    traces = []
    result = {}
    for repetition in range(2):
        stem = f'{label}-{case["name"]}.{repetition}'
        trace = output / f'{stem}.trace'
        trace.unlink(missing_ok=True)
        process = subprocess.run(
            [str(binary), '--config-override', str(config), '--inst-limit', str(BOUNDARIES),
             '--trace-instr', '--trace-gpr', '--trace-csr', '--trace-exception',
             '--trace-output', str(trace), str(case['elf'])],
            capture_output=True, text=True, env=env)
        (output / f'{stem}.process.log').write_text(process.stdout + process.stderr)
        if process.returncode != 0 or not trace.is_file():
            raise S.SailError(f'{stem}: no fresh successful trace: rc={process.returncode}')
        raw = trace.read_bytes()
        traces.append(raw)
        verdict, detail = S.compare_trace(case['expected'], raw.decode(), process.returncode)
        rows, _ = S.parse_trace(raw.decode())
        if set(rows) != set(range(BOUNDARIES)):
            raise S.SailError(f'{stem}: expected exactly thirteen instruction rows')
        for n, row in rows.items():
            if row.pc != case['entry'] + 4 * n or row.word != case['words'][n]:
                raise S.SailError(f'{stem}: instruction PC/word differs at row {n}')
        result = {'verdict': verdict, 'detail': detail, 'destination': rows[8].writes.get('x5'),
                  'cause': rows[9].writes.get('x11'), 'tval': rows[10].writes.get('x12'),
                  'data': [rows[11].writes.get('x13'), rows[12].writes.get('x14')]}
    if traces[0] != traces[1]:
        raise S.SailError(f'{label}-{case["name"]}: repeat traces differ byte-for-byte')
    return result


def run(output: Path, supplied_config: Path | None = None) -> dict:
    binary = S.reference_binary()  # Verifies the dossier's binary SHA256.
    config = supplied_config or D.materialize_sail_override(S.REPO, 'rv64gc-lab-v0')
    output.mkdir(parents=True, exist_ok=True)
    temp = output / 'tmp'
    temp.mkdir(exist_ok=True)
    env = os.environ.copy()
    env['TMPDIR'] = str(temp)
    validate(binary, config, output, 'selected', env)
    asm = Assembler(S.UNIT / 'encoding.sexp')
    cases = []
    for form in FORMS:
        for width in (4, 8):
            for offset in [0, *range(1, width), *range(17 - width, 16)]:
                cases.append(prepare(output, asm, form, width, offset))
    if len(cases) != 242:
        raise S.SailError('the declared 22-form alignment matrix is incomplete')
    results = []
    for case in cases:
        observed = observe(binary, config, output, case, 'selected', env)
        aligned = case['offset'] == 0
        cause = 0 if aligned else (5 if case['form'] == 'lr' else 7)
        tval = 0 if aligned else 0x8000_0100 + case['offset']
        data = [int(case['expected']['step'][n]['writes'].get(reg, '0x0'), 16)
                for n, reg in ((11, 'x13'), (12, 'x14'))]
        if (observed['verdict'] != 'AGREE' or observed['cause'] != cause
                or observed['tval'] != tval or observed['data'] != data):
            raise S.SailError(f'{case["name"]}: alignment mismatch: {observed}')
        results.append({'case': case['name'], **observed})
    # A present 16-byte MAG permits contained AMOs despite amo=AccessFault.
    wrong = json.loads(config.read_text())
    wrong['memory']['regions'][0]['attributes']['misaligned_atomicity_granule_size_exp'] = 4
    wrong_path = output / 'wrong-granule-16.json'
    wrong_path.write_text(json.dumps(wrong, indent=2) + '\n')
    validate(binary, wrong_path, output, 'wrong-granule', env)
    control = next(c for c in cases if c['name'] == 'amoadd-w-1')
    observed = observe(binary, wrong_path, output, control, 'wrong-granule', env)
    if (observed['verdict'] != 'DIVERGE' or not observed['detail'].startswith('step 8 ')
            or observed['destination'] != 0 or observed['cause'] != 0
            or observed['tval'] != 0 or observed['data'] != [0x2a00, 0]):
        raise S.SailError(f'the wrong-granule control stopped distinguishing completion: {observed}')
    result = {'verdict': 'AGREE', 'cases': len(cases), 'boundaries_per_repetition': 3146,
              'repeat': 'two fresh byte-identical traces for each case',
              'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
              'config_sha256': hashlib.sha256(config.read_bytes()).hexdigest(),
              'wrong_granule_control': observed, 'results': results}
    (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=Path('target/rv64gc-sail-atomic-align'))
    parser.add_argument('--config', type=Path, help='project-local public configuration copy for qualification')
    args = parser.parse_args()
    try:
        result = run(S.project_path(args.out_dir), S.project_path(args.config) if args.config else None)
    except (S.SailError, Q.Refusal, AsmError, D.DossierError, OSError, ValueError, KeyError) as exc:
        print(f'REFUSED: {exc}')
        return 2
    print(f'AGREE: {result["cases"]} atomic alignment cases / 3146 boundaries per repetition; '
          'each pair of fresh traces byte-identical; wrong 16-byte granule DIVERGEs at step 8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
