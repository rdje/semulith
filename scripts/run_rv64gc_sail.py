#!/usr/bin/env python3
"""Run selected rv64gc guests through the pinned Sail 0.14 public interface.

The verdict compares declared GPR change-observations, not unrecorded architectural
state. Every ordinary step must have a row, even if it writes nothing. A declared
interrupt/fetch-delivery gap also needs a matching trace event. Failed processes,
malformed traces and absent evidence refuse. This is a live experiment, not CI;
scripts/probe_gc_sail.py checks the adapter offline through GUEST-GEN.

Examples:
  python3 scripts/run_rv64gc_sail.py m-mul m-div m-word m-alias
  python3 scripts/run_rv64gc_sail.py --check-trace target/experiment/m-div.trace m-div
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
from pathlib import Path
import re
import subprocess

from compare_traces import TRAP_NAMES
import dossier_sexp as D
from riscv_asm import Assembler, AsmError, write_elf64

REPO = Path(__file__).resolve().parent.parent
UNIT = REPO / 'profiles/rv64gc-lab-v0'
STEP_RE = re.compile(r'^\[(\d+)\] \[([MSU])\]: 0x([0-9A-Fa-f]{16}) \(0x([0-9A-Fa-f]{4}|[0-9A-Fa-f]{8})\)(?:\s.*)?$')
WRITE_RE = re.compile(r'^x(\d+) <- 0x([0-9A-Fa-f]{16})$')
EVENT_RE = re.compile(r'^handling (exc|int)#(\S+) at priv ([MSU]) \| tval=0x([0-9A-Fa-f]{16})(?:\s.*)?$')
# Public trace spellings observed on the dossier's binary, mapped by the pinned
# privileged exception/interrupt table (RVP-MACHINE 2.1.1.15/16).
EXCEPTIONS = {**TRAP_NAMES, 'u-call': 8, 's-call': 9, 'fetch-page-fault': 12,
              'load-page-fault': 13, 'store/amo-page-fault': 15}
INTERRUPTS = {'supervisor-software-interrupt': 1, 'machine-software-interrupt': 3,
              'supervisor-timer-interrupt': 5, 'machine-timer-interrupt': 7,
              'supervisor-external-interrupt': 9, 'machine-external-interrupt': 11}
INT_LABELS = {'SSI': 1, 'MSI': 3, 'STI': 5, 'MTI': 7, 'SEI': 9, 'MEI': 11}
DECLARED_INTERRUPT = re.compile(r'^the pending evaluation takes the (SSI|MSI|STI|MTI|SEI|MEI) interrupt in ([MSU]):')


class SailError(Exception):
    """The experiment cannot be judged from the available evidence."""


@dataclass
class Row:
    n: int
    pc: int
    word: int
    writes: dict[str, int] = field(default_factory=dict)


def parse_trace(text: str) -> tuple[dict[int, Row], dict[int, tuple[str, int]]]:
    rows, deliveries = {}, {}
    current = None
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if match := STEP_RE.fullmatch(line):
            n = int(match[1])
            if n in rows or n in deliveries or (current is not None and n <= current.n):
                raise SailError(f'line {number}: duplicate/out-of-order step {n}')
            current = Row(n, int(match[3], 16), int(match[4], 16))
            rows[n] = current
        elif match := WRITE_RE.fullmatch(line):
            index = int(match[1])
            if current is None or index > 31:
                raise SailError(f'line {number}: invalid or orphan GPR write')
            reg = f'x{index}'
            if reg in current.writes:
                raise SailError(f'line {number}: duplicate GPR write {reg}')
            current.writes[reg] = int(match[2], 16)
        elif match := EVENT_RE.fullmatch(line):
            kind, spelling = match[1], match[2]
            table = INTERRUPTS if kind == 'int' else EXCEPTIONS
            if spelling not in table:
                raise SailError(f'line {number}: unknown {kind} spelling {spelling!r}')
            cause = table[spelling]
            if kind == 'int' or cause in (1, 12):
                n = current.n + 1 if current else 0
                if n in deliveries:
                    raise SailError(f'line {number}: duplicate delivery at step {n}')
                deliveries[n] = (kind, cause)
        elif (line.startswith('[') or re.match(r'^x\d+\s*<-', line)
              or line.startswith('handling exc#') or line.startswith('handling int#')):
            raise SailError(f'line {number}: malformed trace record {line!r}')
    return rows, deliveries


def compare_trace(expected: dict, text: str, returncode: int = 0) -> tuple[str, str]:
    if returncode != 0:
        raise SailError(f'reference process failed: rc={returncode}')
    if not isinstance(expected.get('instructions'), int) or expected['instructions'] <= 0:
        raise SailError('expectation record has no positive program step budget')
    steps = expected['step']
    count = expected['instructions']
    if [e['n'] for e in steps] != list(range(count)):
        raise SailError('expectation steps are incomplete, duplicated or out of order')
    rows, deliveries = parse_trace(text)
    registers = {f'x{i}': 0 for i in range(32)}
    for e in steps:
        n = e['n']
        want = {k: int(v, 16) for k, v in e['writes'].items()}
        event = deliveries.get(n)
        declared = DECLARED_INTERRUPT.match(e['derivation'])
        if n not in rows:
            interrupt = declared is not None and event == ('int', INT_LABELS[declared[1]])
            fetch_fault = (e['insn'].startswith('<fetch ') and event is not None
                           and event[0] == 'exc' and event[1] in (1, 12))
            if not want and (interrupt or fetch_fault):
                continue
            raise SailError(f'missing expected step {n} ({e["insn"]}); absent evidence is not agreement')
        if declared or e['insn'].startswith(('<halted>', '<fetch ')):
            return 'DIVERGE', f'step {n}: Sail printed an instruction row for declared delivery/wait'
        changes = {}
        for reg, value in rows[n].writes.items():
            if reg == 'x0' and value != 0:
                raise SailError(f'step {n}: x0 trace write is nonzero')
            if registers[reg] != value:
                changes[reg] = value
            registers[reg] = value
        if changes != want:
            return 'DIVERGE', f'step {n} ({e["insn"]}): Sail {changes}, expectations {want}'
    return 'AGREE', f'{count} declared steps; every change-observation and required row present'


def project_path(path: Path) -> Path:
    result = (REPO / path).resolve()
    if not result.is_relative_to(REPO):
        raise SailError(f'path {path}: project outputs/inputs must stay in this repository')
    for parent in (result, *result.parents):
        if parent == REPO:
            break
        if (parent / '.git').exists():
            raise SailError(f'path {path}: another Git repository is read-only')
    return result


def reference_binary() -> Path:
    references = D.load_references(UNIT / 'references.sexp')
    candidate = next((r for r in references['candidate'] if r['id'] == 'sail-riscv'), None)
    if candidate is None:
        raise SailError('the dossier has no Sail reference pin')
    binary = project_path(Path(candidate['binary']))
    if not binary.is_file():
        raise SailError('the pinned Sail binary is missing; acquire it through scripts/fetch_references.sh')
    if hashlib.sha256(binary.read_bytes()).hexdigest() != candidate['binary_sha256']:
        raise SailError('Sail binary digest differs from the dossier pin')
    return binary


def run_guest(name: str, binary: Path, output: Path, encoding: Path, guests: Path):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise SailError(f'invalid guest name {name!r}')
    expected = D.load_expectations(guests / f'{name}.expected.sexp')
    if 'entry' not in expected or 'instructions' not in expected:
        raise SailError(f'{name}: expectations lack a program entry/step budget')
    if not expected.get('cross_model', True):
        raise SailError(f'{name}: cross-model comparison disabled by the expectation record')
    asm = Assembler(encoding)
    payload = asm.assemble_image((guests / f'{name}.s').read_text().splitlines(),
                                 base=int(expected['entry'], 16))
    elf = output / f'{name}.elf'
    write_elf64(elf, int(expected['entry'], 16), payload, asm.ialign)
    # Use the existing conversion owner; materialization is a derived foreign-tool input.
    config = D.materialize_sail_override(REPO, 'rv64gc-lab-v0')
    traces = []
    for repetition in range(2):
        trace = output / f'{name}.{repetition}.trace'
        trace.unlink(missing_ok=True)  # exactly this adapter's artifact, preventing stale success
        proc = subprocess.run([str(binary), '--config-override', str(config),
                               '--inst-limit', str(expected['instructions'] + 2),
                               '--trace-instr', '--trace-gpr', '--trace-exception',
                               '--trace-output', str(trace), str(elf)],
                              capture_output=True, text=True, check=False)
        (output / f'{name}.{repetition}.stdout.log').write_text(proc.stdout)
        (output / f'{name}.{repetition}.stderr.log').write_text(proc.stderr)
        if proc.returncode != 0:
            raise SailError(f'{name}: reference process failed: rc={proc.returncode}')
        if not trace.is_file():
            raise SailError(f'{name}: reference produced no trace')
        text = trace.read_text()
        verdict, detail = compare_trace(expected, text, proc.returncode)
        if verdict != 'AGREE':
            return verdict, detail
        traces.append(trace.read_bytes())
    if traces[0] != traces[1]:
        return 'DIVERGE', f'{name}: repeat traces differ byte-for-byte'
    return 'AGREE', detail + '; two traces byte-identical'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('guests', nargs='+')
    parser.add_argument('--encoding', type=Path, default=UNIT / 'encoding.sexp')
    parser.add_argument('--guests-dir', type=Path, default=UNIT / 'guests')
    parser.add_argument('--out-dir', type=Path, default=Path('target/rv64gc-sail'))
    parser.add_argument('--check-trace', type=Path, help='offline adapter check of one existing trace')
    args = parser.parse_args(argv)
    failures = 0
    try:
        encoding, guests = project_path(args.encoding), project_path(args.guests_dir)
        if args.check_trace:
            if len(args.guests) != 1:
                raise SailError('--check-trace requires exactly one guest')
            name = args.guests[0]
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
                raise SailError(f'invalid guest name {name!r}')
            expected = D.load_expectations(guests / f'{name}.expected.sexp')
            verdict, detail = compare_trace(expected, project_path(args.check_trace).read_text())
            print(f'{verdict} {name}: {detail} (cached trace; process status unavailable)')
            return 0 if verdict == 'AGREE' else 1
        binary, output = reference_binary(), project_path(args.out_dir)
        output.mkdir(parents=True, exist_ok=True)
        for name in args.guests:
            verdict, detail = run_guest(name, binary, output, encoding, guests)
            print(f'{verdict} {name}: {detail}')
            failures += verdict != 'AGREE'
    except (SailError, AsmError, D.DossierError, OSError, ValueError) as exc:
        print(f'REFUSED: {exc}')
        return 2
    print(f'verdict: {len(args.guests) - failures} AGREE of {len(args.guests)}')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
