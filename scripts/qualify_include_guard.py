#!/usr/bin/env python3
"""Qualify public include-guard integration in fresh repository-owned workspaces.

Use --mode protocol, original, public, faults, books, omissions, concurrency or
original-concurrency and a fresh
--output target/PATH. Generated evidence is ignored; the recipes are tracked.
Historical execution is restricted to the reviewed LC0029 integration baseline.
No Gitlink implementation, external repository writes, fetching or Git init.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

import book_includes as I
import collect_containment_graph as C
import qualify_book_includes as Q

ROOT = C.ROOT
SOURCE = 'aacaee98b02292bfcee8f139fad28530bcfe4e95'
require = C.require
write_json = Q.write_json


def environment(tmp: Path) -> dict:
    env = Q.environment()
    env['TMPDIR'] = str(tmp)
    if sys.flags.optimize:
        env['PYTHONOPTIMIZE'] = '1'
    return env


def run(command, env, *, cwd=None):
    return subprocess.run(command, env=env, cwd=cwd, capture_output=True, check=False)


def record_streams(root: Path, label: str, result) -> None:
    (root / (label + '.stdout')).write_bytes(result.stdout)
    (root / (label + '.stderr')).write_bytes(result.stderr)


def capture_command(path: Path, when='raw') -> str:
    return shlex.join([sys.executable, str(ROOT / 'scripts/qualify_book_includes.py'),
                       '--capture', when, '--capture-output', path.relative_to(ROOT).as_posix()])


def protocol(output: Path) -> dict:
    helper = output / 'processor.py'
    helper.write_text('''import json, os, sys
with open(os.environ['PROTOCOL_LOG'], 'a') as stream:
    stream.write(' '.join(sys.argv[1:]) + '\\n')
kind = os.environ['PROTOCOL_KIND']
if len(sys.argv) > 1:
    sys.exit(1 if kind == 'supports-reject' else 0)
context, book = json.load(sys.stdin)
if kind in ['defect', 'refuse']:
    print('BOOK-INCLUDES: ' + ('REFUSED — controlled input' if kind == 'refuse'
                              else 'DEFECT — missing controlled input'), file=sys.stderr)
    sys.exit(2 if kind == 'refuse' else 1)
if kind == 'invalid-json':
    sys.stdout.write('not JSON')
    sys.exit(0)
json.dump(book, sys.stdout)
print('BOOK-INCLUDES: checked 1 chapters / 0 include edges', file=sys.stderr)
''')
    records = []
    for explicit in [False, True]:
        for kind in ['valid', 'supports-reject', 'defect', 'refuse', 'invalid-json', 'absent-script']:
            root = output / str(explicit) / kind
            (root / 'src').mkdir(parents=True)
            (root / 'src/SUMMARY.md').write_text('# Summary\n\n[One](one.md)\n')
            (root / 'src/one.md').write_text('# One\n')
            executable = helper if kind != 'absent-script' else output / 'absent.py'
            command = shlex.join(['python3', os.path.relpath(executable, root)])
            (root / 'book.toml').write_text('[book]\ntitle="Protocol"\n[preprocessor.source-check]\n'
                'command=' + json.dumps(command) + '\nbefore=["links"]\noptional=false\n'
                + ('renderers=["html"]\n' if explicit else ''))
            log = root / 'invocations'
            env = environment(output / 'tmp')
            env.update(PROTOCOL_LOG=str(log), PROTOCOL_KIND=kind)
            result = run(['mdbook', 'build', str(root), '-d', str(root / 'site')], env)
            record_streams(root, 'build', result)
            calls = log.read_text().splitlines() if log.exists() else []
            expected = 0 if kind == 'valid' or (kind == 'supports-reject') or (
                not explicit and kind == 'absent-script') else 101
            require(result.returncode == expected, 'public processor verdict changed: ' + kind)
            if kind != 'absent-script':
                expected_calls = [''] if explicit else ['supports html'] + (
                    [] if kind == 'supports-reject' else [''])
                require(calls == expected_calls, 'public renderer invocation changed: ' + kind)
            records.append({'explicit_renderer': explicit, 'case': kind,
                            'returncode': result.returncode, 'calls': calls,
                            'stderr_sha256': C.digest(result.stderr)})
    return {'protocol_cases': records}


def fixture(root: Path, scripts: Path, *, role: str, marker: str, body: bytes | None):
    (root / 'materials').mkdir(parents=True)
    (root / 'materials/units.sexp').write_text(
        '(unit (id "u1") (kind processor) (layer processor) (book "docs/models/u1"))\n')
    target = None
    for label, book in [('project', 'docs/book'), ('unit', 'docs/models/u1')]:
        (root / book / 'src').mkdir(parents=True)
        (root / book / 'book.toml').write_text('[book]\ntitle="Owned fixture"\nsrc="src"\n')
        chapter = 'models.md' if label == 'project' else 'intro.md'
        (root / book / 'src/SUMMARY.md').write_text('# Summary\n\n[One](' + chapter + ')\n')
        path = root / book / 'src' / chapter
        path.write_text('# One\n' + ('- **`u1`** (kind: processor)\n' if label == 'project' else '')
                        + ('\n' + marker + '\n' if label == role else ''))
        if label == role:
            target = path
            if body is not None:
                (path.parent / 'fragment.txt').write_bytes(body)
    (root / 'scripts').symlink_to(os.path.relpath(scripts, root), target_is_directory=True)
    (root / 'bin').mkdir()
    git = root / 'bin/git'
    git.write_text('#!/usr/bin/env bash\nif [ "$#" -eq 2 ] && [ "$1" = rev-parse ] && '
                   '[ "$2" = --show-toplevel ]; then pwd; else exit 73; fi\n')
    git.chmod(0o755)
    (root / 'target/tmp').mkdir(parents=True)
    require(target is not None, 'unknown fixture book role')
    return target


def public_matrix(output: Path, *, original=False) -> dict:
    valid = b'// ANCHOR: selected\nretained contract\n// ANCHOR_END: selected\n'
    duplicate = valid + b'// ANCHOR: selected\nsecond contract\n// ANCHOR_END: selected\n'
    cases = [('valid', 'unit', '{{#include fragment.txt:selected}}', valid, 0)]
    for role in ['project', 'unit']:
        cases.extend([(kind, role, marker, body, 1) for kind, marker, body in [
            ('missing-file', '{{#include absent.txt}}', None),
            ('missing-anchor', '{{#include fragment.txt:absent}}', valid),
            ('duplicate-anchor', '{{#include fragment.txt:selected}}', duplicate)]])
        if not original:
            cases.extend([('utf8', role, '{{#include fragment.txt}}', b'\xff', 2),
                          ('symlink', role, '{{#include fragment.txt}}', None, 2)])
    code = ROOT
    source = None
    population = output / 'fixtures'
    if original:
        source = C.source_census(SOURCE)
        code, _ = Q.copy_source(source, output)
        population = code / 'target/include-guard-fixtures'
    records = []
    for kind, role, marker, body, expected in cases:
        root = population / (role + '-' + kind)
        target = fixture(root, code / 'scripts', role=role, marker=marker, body=body)
        if kind == 'symlink':
            (target.parent / 'fragment.txt').symlink_to(target.name)
        env = environment(root / 'target/tmp')
        command = [sys.executable, *(['-O'] if sys.flags.optimize else []),
                   str(code / 'scripts/unit_books.py'), str(root)]
        cli = run(command, env)
        record_streams(root, 'cli', cli)
        env['PATH'] = str(root / 'bin') + os.pathsep + env['PATH']
        shell = run(['bash', str(code / 'scripts/check_unit_books.sh')], env, cwd=root)
        record_streams(root, 'shell', shell)
        verdict = 0 if original else expected
        require(cli.returncode == shell.returncode == verdict,
                'actual public verdict differs: ' + role + ' ' + kind)
        if verdict == 2:
            require(b'REFUSED' in cli.stdout and b'REFUSED' in shell.stderr,
                    'public refusal reason missing')
        records.append({'case': kind, 'role': role, 'cli_rc': cli.returncode,
                        'shell_rc': shell.returncode,
                        'cli_stdout_sha256': C.digest(cli.stdout),
                        'shell_stderr_sha256': C.digest(shell.stderr)})
    if original:
        Q.verify_copy(source, code)
    return {'source': SOURCE if original else 'working', 'public_cases': records}


FAULT_HOOK = '''import os
original_open = os.open
original_fstat = os.fstat
watched = None
checks = 0
def marker():
    with open(os.environ['FAULT_LOG'], 'a') as stream: stream.write('1\\n')
def opened(path, flags, *args, **kwargs):
    global watched
    if os.fspath(path) == os.environ['FAULT_TARGET']:
        if os.environ['FAULT_KIND'] == 'read':
            marker()
            raise PermissionError('controlled owned read refusal')
        watched = original_open(path, flags, *args, **kwargs)
        return watched
    return original_open(path, flags, *args, **kwargs)
def statted(fd):
    global checks
    if fd == watched:
        checks += 1
        if checks == 2:
            marker()
            with open(os.environ['FAULT_TARGET'], 'w') as stream: stream.write('changed source\\n')
    return original_fstat(fd)
os.open = opened
os.fstat = statted
'''


def faults(output: Path) -> dict:
    records = []
    for role in ['chapter', 'include']:
        for kind in ['read', 'changed']:
            root = output / (role + '-' + kind)
            chapter = fixture(root, ROOT / 'scripts', role='unit',
                              marker='{{#include fragment.txt}}', body=b'contract\n')
            target = chapter if role == 'chapter' else chapter.parent / 'fragment.txt'
            original = target.read_bytes()
            injection = root / 'injection'
            injection.mkdir()
            (injection / 'sitecustomize.py').write_text(FAULT_HOOK)
            for interface in ['cli', 'shell']:
                target.write_bytes(original)
                log = root / (interface + '.injections')
                env = environment(root / 'target/tmp')
                env.update(PYTHONPATH=str(injection), FAULT_TARGET=str(target),
                           FAULT_LOG=str(log), FAULT_KIND=kind)
                if interface == 'cli':
                    command = [sys.executable, *(['-O'] if sys.flags.optimize else []),
                               str(ROOT / 'scripts/unit_books.py'), str(root)]
                    cwd = ROOT
                else:
                    env['PATH'] = str(root / 'bin') + os.pathsep + env['PATH']
                    command = ['bash', str(ROOT / 'scripts/check_unit_books.sh')]
                    cwd = root
                result = run(command, env, cwd=cwd)
                record_streams(root, interface, result)
                count = log.read_text().count('1\n') if log.exists() else 0
                require(result.returncode == 2 and count == 1
                        and b'REFUSED' in result.stdout + result.stderr,
                        'actual public source fault did not refuse once')
                records.append({'role': role, 'fault': kind, 'interface': interface,
                                'returncode': result.returncode, 'injections': count})
    return {'public_faults': records}


def books(corpus: Path, output: Path) -> dict:
    """Observe defaults without overriding source-check; compare pass-through."""
    units = C.U.registered_units(corpus)
    names = ['docs/book', *[u['book'].rstrip('/') for u in units]]
    require(not C.U.catalogue_findings(corpus, units), 'actual catalogue refused')
    reports, versions, output_files = {}, set(), None
    for stage in ['default', 'passthrough']:
        site = output / stage / 'site'
        log = output / stage
        log.mkdir(parents=True)
        for number, name in enumerate(names):
            env = environment(output / 'tmp')
            if stage == 'default':
                for label, when in [('raw-witness', 'raw'), ('expanded-witness', 'expanded')]:
                    destination = output / 'captures' / name / (when + '.json')
                    prefix = 'MDBOOK_PREPROCESSOR__' + label.replace('-', '_').upper() + '__'
                    env[prefix + 'COMMAND'] = capture_command(destination, when)
                    env[prefix + 'RENDERERS'] = '["html"]'
                    if when == 'raw':
                        env[prefix + 'BEFORE'] = '["source-check", "links"]'
                    else:
                        env[prefix + 'AFTER'] = '["source-check", "links"]'
                        env[prefix + 'BEFORE'] = '["project-record-links"]'
            else:
                env['MDBOOK_PREPROCESSOR__SOURCE_CHECK__COMMAND'] = capture_command(
                    output / 'passthrough-inputs' / (str(number) + '.json'))
                prefix = 'MDBOOK_PREPROCESSOR__EXPANDED_WITNESS__'
                env[prefix + 'COMMAND'] = capture_command(
                    output / 'baseline-expanded' / name / 'expanded.json', 'expanded')
                env[prefix + 'RENDERERS'] = '["html"]'
                env[prefix + 'AFTER'] = '["source-check", "links"]'
                env[prefix + 'BEFORE'] = '["project-record-links"]'
            result = run(['mdbook', 'build', str(corpus / name), '-d', str(site / name / 'book')], env)
            record_streams(log, str(number), result)
            require(result.returncode == 0, 'actual default build failed: ' + name)
            if stage == 'default':
                raw = json.loads((output / 'captures' / name / 'raw.json').read_text())
                expanded = json.loads((output / 'captures' / name / 'expanded.json').read_text())
                expected_root = (corpus / name).relative_to(ROOT).as_posix()
                require(raw['root'] == expanded['root'] == expected_root, 'actual default root differs')
                versions.update([raw['mdbook_version'], expanded['mdbook_version']])
                context = {'root': str(corpus / name), 'renderer': raw['renderer'],
                           'config': {'book': raw['config_book']}}
                unchanged, report = I.preprocess(context, raw['book'], corpus)
                require(unchanged == raw['book'], 'complete book object changed')
                observed = re.findall(rb'BOOK-INCLUDES: checked ([0-9]+) chapters / ([0-9]+) include edges',
                                      result.stderr)
                require(observed == [(str(len(report['chapters'])).encode(),
                                      str(len(report['include_edges'])).encode())],
                        'default execution witness differs from actual before-links inputs: ' + name)
                reports[name] = report
            else:
                validated = json.loads((output / 'captures' / name / 'expanded.json').read_text())
                baseline = json.loads((output / 'baseline-expanded' / name / 'expanded.json').read_text())
                require(validated['book'] == baseline['book'],
                        'complete expanded book differs from pass-through: ' + name)
        files = Q.file_set(site)
        if stage == 'default':
            output_files = files
        else:
            Q.same_files(output_files, files)
    require(len(versions) == 1, 'ambiguous public mdbook version')
    write_json(output / 'output-files.json', output_files)
    write_json(output / 'input-report.json', reports)
    return {'books': names, 'chapters': sum(len(r['chapters']) for r in reports.values()),
            'includes': sum(len(r['include_edges']) for r in reports.values()),
            'output_files': len(output_files), 'mdbook_version': next(iter(versions))}


def working_copy(output: Path, snapshot: dict) -> Path:
    """Copy the actual regular working inputs; Gitlinks remain unmaterialized."""
    source = C.source_census(SOURCE)
    copied, _ = Q.copy_source(source, output)
    for name, pin in snapshot['members'].items():
        if 'gitlink' in pin:
            require(not (copied / name).exists(), 'Gitlink materialized')
            continue
        path = copied / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())
        path.chmod(pin['mode'])
        require(C.file_identity(path.relative_to(ROOT).as_posix()) == pin,
                'working-copy input differs: ' + name)
    return copied


def omissions(output: Path, snapshot: dict) -> dict:
    records = []
    for mode in ['no-include-env', 'no-include-witness', 'no-include-refusal']:
        env = environment(output / 'tmp')
        result = run([sys.executable, *(['-O'] if sys.flags.optimize else []),
                      str(ROOT / 'scripts/probe_unit_books.py'), '--mutation', mode], env)
        record_streams(output, mode, result)
        require(result.returncode == 1 and b'FAILED (' in result.stderr
                and b'SyntaxError' not in result.stderr and b'ImportError' not in result.stderr,
                'actual guard omission escaped controls: ' + mode)
        records.append({'mutation': mode, 'returncode': result.returncode,
                        'stderr_sha256': C.digest(result.stderr)})
    for mode in ['before-links', 'renderer', 'processor']:
        root = output / mode
        root.mkdir()
        copied = working_copy(root, snapshot)
        config = copied / 'docs/book/book.toml'
        original = config.read_text()
        if mode == 'before-links':
            old, new = 'before = ["links"]\n', ''
        elif mode == 'renderer':
            old, new = '[preprocessor.source-check]\n', '[preprocessor.source-check]\n'
            # Narrow the source-check renderer only, preserving other processors.
            at = original.index(old)
            original_prefix, tail = original[:at], original[at:]
            require(tail.count('renderers = ["html"]') == 1, 'source renderer seam')
            changed = original_prefix + tail.replace('renderers = ["html"]', 'renderers = ["pdf"]', 1)
        else:
            old = '\n[preprocessor.source-check]\n' + original.split('\n[preprocessor.source-check]\n', 1)[1]
            new = '\n'
        if mode != 'renderer':
            require(original.count(old) == 1, 'nonunique config mutation seam')
            changed = original.replace(old, new, 1)
        config.write_text(changed)
        observed = root / 'actual'
        observed.mkdir()
        (observed / 'tmp').mkdir()
        try:
            books(copied, observed)
        except C.Q.Refused as exc:
            reason = str(exc)
            require('default execution witness differs' in reason, 'wrong default mutation refusal: ' + reason)
        else:
            raise C.Q.Refused('default config omission escaped actual builds: ' + mode)
        for name, pin in snapshot['members'].items():
            if 'gitlink' in pin or name == 'docs/book/book.toml':
                continue
            require(C.file_identity((copied / name).relative_to(ROOT).as_posix()) == pin,
                    'protected working copy changed')
        records.append({'mutation': mode, 'returncode': 2, 'reason': reason,
                        'config_sha256': C.digest(config.read_bytes())})
    return {'actual_omissions': records}


def concurrency(output: Path, *, original=False) -> dict:
    """Exercise actual shell calibration with eight overlapping invocations."""
    code, source = ROOT, None
    root = output / 'fixture'
    if original:
        source = C.source_census(SOURCE)
        code, _ = Q.copy_source(source, output)
        root = code / 'target/concurrent-fixture'
    fixture(root, code / 'scripts', role='unit', marker='', body=None)
    env = environment(root / 'target/tmp')
    env['PATH'] = str(root / 'bin') + os.pathsep + env['PATH']

    def invoke(number):
        result = run(['bash', str(code / 'scripts/check_unit_books.sh'), '--self-test'], env, cwd=root)
        record_streams(output, 'shell-' + str(number), result)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(invoke, range(8)))
    if original:
        failing = [r for r in results if r.returncode]
        require(failing and all(r.returncode == 1 and
                b'FAIL: test_real_build_is_fresh_and_removed' in r.stderr for r in failing),
                'original concurrent cleanup race not reproduced')
        Q.verify_copy(source, code)
    else:
        require(all(r.returncode == 0 and b'22 pass / 0 fail' in r.stdout for r in results),
                'current concurrent shell calibration failed')
    return {'source': SOURCE if original else 'working',
            'concurrent_shells': [{'returncode': r.returncode,
                                  'stdout_sha256': C.digest(r.stdout),
                                  'stderr_sha256': C.digest(r.stderr)} for r in results]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', required=True,
                        choices=['protocol', 'original', 'public', 'faults', 'books', 'omissions',
                                 'concurrency', 'original-concurrency'])
    parser.add_argument('--output', required=True)
    parser.add_argument('--addition', action='append', default=[])
    args = parser.parse_args(argv)
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    try:
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'output must be under target/')
        output = C.U.source_path(ROOT, args.output)
        require(not output.exists(), 'fresh output required')
        before = C.working_snapshot(args.addition)
        output.mkdir(parents=True)
        (output / 'tmp').mkdir()
        if args.mode == 'protocol':
            result = protocol(output)
        elif args.mode in {'original', 'public'}:
            result = public_matrix(output, original=args.mode == 'original')
        elif args.mode == 'faults':
            result = faults(output)
        elif args.mode == 'books':
            result = books(ROOT, output)
        elif args.mode in {'concurrency', 'original-concurrency'}:
            result = concurrency(output, original=args.mode == 'original-concurrency')
        else:
            result = omissions(output, before)
        require(before == C.working_snapshot(args.addition), 'actual source/index/modes changed')
        write_json(output / 'working-before.json', before)
        write_json(output / 'working-after.json', before)
        result = dict(result, mode='optimized' if sys.flags.optimize else 'normal')
        write_json(output / 'result.json', result)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (C.Q.Refused, C.U.BookRefused, OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        print('INCLUDE-GUARD: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
