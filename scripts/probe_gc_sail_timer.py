#!/usr/bin/env python3
"""Reproduce the pinned Sail timer-platform limit through its public interface.

Live diagnostic, not an offline CI gate. The laboratory derives its ten-boundary
expectations before the reference executes; no expectation is fitted to the output.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

import derive_rv64gc_expectations as Q
import dossier_sexp as D
from riscv_asm import Assembler, AsmError, write_elf64
import run_rv64gc_sail as S

SOURCE = """lui x31, 0x80000
csrrs x0, menvcfg, x31
csrrs x9, menvcfg, x0
addi x3, x0, 0
csrrw x0, stimecmp, x3
c.nop
csrrs x10, mip, x0
csrrs x11, stimecmp, x0
c.nop
csrrs x12, mip, x0
"""


def run(output: Path) -> dict:
    binary = S.reference_binary()
    config = D.materialize_sail_override(S.REPO, 'rv64gc-lab-v0')
    output.mkdir(parents=True, exist_ok=True)
    source = output / 'timer.s'
    source.write_text(SOURCE)
    asm = Assembler(S.UNIT / 'encoding.sexp')
    record, _ = Q.run_parcel_guest(source, asm, 10)
    expected_path = output / 'timer.expected.sexp'
    expected_path.write_text(record)
    expected = D.load_expectations(expected_path)
    elf = output / 'timer.elf'
    write_elf64(elf, int(expected['entry'], 16),
                asm.assemble_image(SOURCE.splitlines(), base=int(expected['entry'], 16)), asm.ialign)

    base, validations = json.loads(config.read_text()), []
    for clint in (False, True):
        for counters in (False, True):
            variant = json.loads(json.dumps(base))
            variant['platform']['clint']['supported'] = clint
            variant['extensions']['Zicntr']['supported'] = counters
            path = output / f'clint-{int(clint)}-zicntr-{int(counters)}.json'
            path.write_text(json.dumps(variant, indent=2) + '\n')
            proc = subprocess.run([str(binary), '--config-override', str(path), '--validate-config'],
                                  capture_output=True, text=True)
            validations.append({'clint': clint, 'zicntr': counters, 'rc': proc.returncode,
                                'output': proc.stdout + proc.stderr})
    if validations[0]['rc'] != 0:
        raise S.SailError('the declared baseline configuration did not validate')

    traces = []
    for repetition in range(2):
        trace = output / f'timer.{repetition}.trace'
        trace.unlink(missing_ok=True)
        proc = subprocess.run([str(binary), '--config-override', str(config), '--inst-limit', '10',
                               '--trace-instr', '--trace-gpr', '--trace-csr', '--trace-interrupt',
                               '--trace-exception', '--trace-output', str(trace), str(elf)],
                              capture_output=True, text=True)
        (output / f'timer.{repetition}.log').write_text(proc.stdout + proc.stderr)
        if proc.returncode != 0 or not trace.is_file():
            raise S.SailError(f'timer probe failed to produce fresh evidence: rc={proc.returncode}')
        traces.append(trace.read_bytes())
    if traces[0] != traces[1]:
        raise S.SailError('timer probe repeat traces differ')
    text = traces[0].decode()
    verdict, detail = S.compare_trace(expected, text)
    rows, _ = S.parse_trace(text)
    if set(rows) != set(range(10)):
        raise S.SailError('timer probe did not execute exactly ten instruction rows')
    # Read-back guards the selected comparator view on both independent sides.
    if (rows[2].writes.get('x9') != 1 << 63
            or expected['step'][2]['writes'] != {'x9': '0x8000000000000000'}):
        raise S.SailError('STCE setup/read-back did not establish the comparator view')
    # The reference logs destinations even when their values do not change.
    observed = {reg: rows[n].writes.get(reg) for n, reg in ((6, 'x10'), (9, 'x12'))}
    wanted = {reg: int(expected['step'][n]['writes'][reg], 16)
              for n, reg in ((6, 'x10'), (9, 'x12'))}
    if (verdict != 'DIVERGE' or rows[7].writes.get('x11') != 0
            or observed != {'x10': 0, 'x12': 0} or wanted != {'x10': 32, 'x12': 32}):
        raise S.SailError(f'timer-platform observation changed: {verdict}; {observed}; {wanted}')
    result = {'verdict': 'NAMED-PLATFORM-DIFFERENCE', 'detail': detail,
              'stce_readback': '0x8000000000000000', 'mip_reads_sail': observed, 'mip_reads_laboratory': wanted,
              'repeat': 'byte-identical', 'config_validations': validations}
    (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=Path('target/rv64gc-sail-timer'))
    args = parser.parse_args()
    try:
        result = run(S.project_path(args.out_dir))
    except (S.SailError, Q.Refusal, AsmError, D.DossierError, OSError, ValueError, KeyError) as exc:
        print(f'REFUSED: {exc}')
        return 2
    print('NAMED-PLATFORM-DIFFERENCE: STCE=1, stimecmp=0, Sail mip.STIP=0 at both reads; '
          'laboratory mip.STIP=1; two fresh traces byte-identical')
    print(result['detail'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
