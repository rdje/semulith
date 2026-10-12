#!/usr/bin/env python3
"""Measure LC0032's project-book index consumer, not complete graph coverage.

Replay immutable source through both public commands in fresh on-volume copies.
No Git repository is created. Gitlinks remain opaque; no fetch is permitted.
Exit0 means measurement completed, including any defects recorded in result.json.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import collect_containment_graph as C
import qualify_book_includes as Q

ROOT = C.ROOT
SOURCE = '32f9c31eba83ccfc15c2c875ba14bb5851b9a543'
GEN = 'scripts/gen_book_index.py'
GUARD = 'scripts/check_book_index.sh'
BOOK = 'docs/book'
OUT = BOOK + '/src/index.md'
require = C.require

HOOK = '''import hashlib,json,os
from pathlib import Path
original=Path.read_text
root=Path(os.environ['INDEX_FIXTURE'])
trace=Path(os.environ['INDEX_TRACE'])
calls={}
def observed(path,*args,**kwargs):
    name=path.absolute().relative_to(root).as_posix()
    calls[name]=calls.get(name,0)+1
    if name==os.environ.get('INDEX_READ_FAULT') and calls[name]==int(os.environ.get('INDEX_READ_FAULT_NTH','1')):
        with trace.open('a') as stream:stream.write(json.dumps({'fault':name})+'\\n')
        raise OSError('LC0032 actual source read failure')
    value=original(path,*args,**kwargs)
    with trace.open('a') as stream:
        stream.write(json.dumps({'path':name,'bytes':len(value.encode()),
          'sha256':hashlib.sha256(value.encode()).hexdigest()})+'\\n')
    return value
Path.read_text=observed
'''


def chapters(bodies):
    """Independent declaration expansion; refuse syntax outside this capture."""
    text = bodies[BOOK + '/src/SUMMARY.md'].decode()
    matches = re.findall(r'^\s*-?\s*\[([^\]]+)\]\(([^)]+)\)\s*$', text, re.M)
    require(len(matches) == text.count(']('), 'unclassified SUMMARY candidate')
    rows = []
    for title, target in matches:
        C.Q.relative_path(target)
        name = BOOK + '/src/' + target
        require(name in bodies and target not in [r['target'] for r in rows],
                'missing/duplicate declared chapter')
        rows.append({'title': title, 'target': target, 'path': name})
    require(len(rows) == 49, 'reviewed complete chapter population')
    return rows


def terms(bodies):
    result = []
    for line in bodies['docs/GLOSSARY.md'].decode().splitlines():
        cells = line.split('|')
        if len(cells) != 4 or cells[0] or cells[-1]:
            continue
        term = cells[1].strip()
        if term == 'Term' or not term.strip('-:'):
            continue
        result.append((term, 'glossary.md', [a.strip() for a in term.split('/') if a.strip()]))
    text = bodies[BOOK + '/src/glossary.md'].decode()
    section = text.split('## The acronyms this book uses\n', 1)[1].split('\n## ', 1)[0]
    for line in section.splitlines():
        cells = line.split('|')
        if len(cells) != 5 or cells[0] or cells[-1]:
            continue
        term = cells[1].strip()
        if term == 'Acronym' or not term.strip('-:'):
            continue
        result.append((term, 'glossary.md#the-acronyms-this-book-uses', [term]))
    require(len(result) == 40, 'reviewed full term population')
    return sorted(result, key=lambda r: r[0].casefold())


def expected_rows(bodies, declared, vocabulary):
    rows, ledger = [], []
    for term, definition, aliases in vocabulary:
        hits = []
        for chapter in declared:
            if chapter['target'] in {'glossary.md', 'index.md', 'SUMMARY.md'}:
                continue
            text = bodies[chapter['path']].decode()
            if any(re.search(r'(?<![A-Za-z0-9_])' + re.escape(alias)
                             + r'(?![A-Za-z0-9_])', text, re.I) for alias in aliases):
                hits.append(chapter)
        links = ', '.join('[' + r['title'] + '](' + r['target'] + ')' for r in hits) or '—'
        rows.append('| ' + term + ' | [Glossary](' + definition + ') | ' + links + ' |')
        ledger.append({'term': term, 'definition': definition, 'aliases': aliases,
                       'chapters': [r['path'] for r in hits]})
    return rows, ledger


def reconcile(output, trace, expected, declared, bodies):
    rows = output.decode().splitlines()
    actual = [line for line in rows if line.startswith('| ')][2:]
    require(actual == expected, 'complete independent term/chapter expansion differs')
    observed = [r['path'] for r in trace if 'path' in r]
    chapter_reads = observed[1:1 + len(declared)]
    require(observed[0] == BOOK + '/src/SUMMARY.md'
            and chapter_reads == [r['path'] for r in declared], 'complete actual chapter reads/order differs')
    require(observed[1 + len(declared):] == ['docs/GLOSSARY.md', BOOK + '/src/glossary.md', OUT],
            'complete actual vocabulary/output reads differ')
    for record in trace:
        require(set(record) == {'path', 'bytes', 'sha256'}
                and record['path'] in bodies, 'actual read identity shape')
        body = bodies[record['path']]
        require(record['bytes'] == len(body) and record['sha256'] == C.digest(body),
                'actual read content differs from immutable input')


def run(command, fixture, output, label, hook, fault=None):
    env = Q.environment()
    env.update(TMPDIR=str(output / 'tmp'), GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0',
               GIT_DIR=str(ROOT / '.git'), GIT_WORK_TREE=str(fixture),
               PYTHONPATH=str(hook), INDEX_FIXTURE=str(fixture),
               INDEX_TRACE=str(output / (label + '.reads.jsonl')))
    if sys.flags.optimize:
        env['PYTHONOPTIMIZE'] = '1'
    if fault is not None:
        env['INDEX_READ_FAULT'], nth = fault
        env['INDEX_READ_FAULT_NTH'] = str(nth)
    result = subprocess.run(command, cwd=fixture, env=env, capture_output=True)
    (output / (label + '.stdout')).write_bytes(result.stdout)
    (output / (label + '.stderr')).write_bytes(result.stderr)
    trace = output / (label + '.reads.jsonl')
    reads = [json.loads(line) for line in trace.read_text().splitlines()] if trace.exists() else []
    return {'returncode': result.returncode, 'stdout_sha256': C.digest(result.stdout),
            'stderr_sha256': C.digest(result.stderr),
            'traceback': b'Traceback (most recent call last)' in result.stderr}, reads


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--addition', action='append', default=[])
    parser.add_argument('--working-code', action='store_true',
                        help='overlay only the actual generator/guard onto immutable book inputs')
    args = parser.parse_args()
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    try:
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'on-volume target output required')
        output = C.U.source_path(ROOT, args.output)
        require(not output.exists(), 'fresh output required')
        before = C.working_snapshot(args.addition)
        source = C.source_census(SOURCE)
        require(len(source['members']) == 1443, 'complete immutable source population')
        rows = C.Q.tree_rows(C.Q.git('ls-tree', '-rz', '--full-tree', SOURCE))
        selected = {n: r for n, r in rows.items() if r[0] != '160000'
                    and (n.startswith(BOOK + '/') or n in {GEN, GUARD, 'docs/GLOSSARY.md'})}
        wire = C.Q.checked_output(subprocess.run(['git', '--no-optional-locks', '-C', str(ROOT),
            'cat-file', '--batch'], input=b''.join(r[2].encode() + b'\n' for r in selected.values()),
            capture_output=True))
        bodies = C.blob_contents(selected, wire)
        if args.working_code:
            for name in [GEN, GUARD]:
                pin = C.file_identity(name)
                require(pin['mode'] == (0o755 if selected[name][0] == '100755' else 0o644),
                        'working code mode differs from reviewed source')
                bodies[name] = (ROOT / name).read_bytes()
        declared, vocabulary = chapters(bodies), terms(bodies)
        expected, ledger = expected_rows(bodies, declared, vocabulary)
        output.mkdir(parents=True)
        (output / 'tmp').mkdir()
        fixture = output / 'source'
        for name, body in bodies.items():
            path = fixture / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            path.chmod(0o755 if selected[name][0] == '100755' else 0o644)
        hook = output / 'hook'
        hook.mkdir()
        (hook / 'sitecustomize.py').write_text(HOOK)
        python = [sys.executable, *(['-O'] if sys.flags.optimize else [])]
        commands = {'generator': python + [GEN, '--check'], 'guard': ['bash', GUARD]}
        results = {}
        for interface, command in commands.items():
            result, trace = run(command, fixture, output, 'baseline-' + interface, hook)
            require(result['returncode'] == 0 and not result['traceback'], 'baseline public command failed')
            if interface == 'generator':
                reconcile((fixture / OUT).read_bytes(), trace, expected, declared, bodies)
                Q.write_json(output / 'actual-reads.json', trace)
            results[interface] = result
        mutations = ['stale-index', 'missing-chapter', 'missing-summary', 'missing-glossary',
                     'missing-acronyms', 'invalid-chapter-utf8', 'invalid-summary-utf8', 'read-fault',
                     'read-summary-fault', 'read-glossary-fault', 'read-acronyms-fault', 'read-index-fault']
        observations = []
        first = declared[0]['path']
        fault_sites = {'read-fault': (first, 1), 'read-summary-fault': (BOOK + '/src/SUMMARY.md', 1),
                       'read-glossary-fault': ('docs/GLOSSARY.md', 1),
                       'read-acronyms-fault': (BOOK + '/src/glossary.md', 2),
                       'read-index-fault': (OUT, 2)}
        for mode in mutations:
            name = {'stale-index': OUT, 'missing-summary': BOOK + '/src/SUMMARY.md',
                    'missing-glossary': 'docs/GLOSSARY.md', 'missing-acronyms': BOOK + '/src/glossary.md',
                    'invalid-summary-utf8': BOOK + '/src/SUMMARY.md'}.get(mode, first)
            path = fixture / name
            original = path.read_bytes()
            if mode.startswith('missing-') and mode != 'missing-acronyms':
                path.unlink()
            elif mode.startswith('invalid-'):
                path.write_bytes(b'\xff')
            elif mode == 'missing-acronyms':
                path.write_bytes(original.replace(b'## The acronyms this book uses', b'## Other acronyms', 1))
            elif mode == 'stale-index':
                path.write_bytes(original + b'\nchanged generated receipt\n')
            try:
                for interface, command in commands.items():
                    result, trace = run(command, fixture, output, mode + '-' + interface, hook,
                                        fault_sites.get(mode))
                    faults = sum('fault' in item for item in trace)
                    require(faults == (1 if mode in fault_sites else 0), 'actual read fault injection count')
                    observations.append({'case': mode, 'interface': interface,
                                         'expected_returncode': 1 if mode == 'stale-index' else 2,
                                         'fault_reads': faults, **result})
            finally:
                path.write_bytes(original)
        omissions = []
        generator = fixture / GEN
        original = generator.read_text()
        replacements = [
            ('omit-chapter', '        path = book / "src" / rel',
             '        if rel == ' + repr(declared[0]['target']) + ':\n            continue\n        path = book / "src" / rel'),
            ('omit-term', '    terms = read_terms(book, glossary)', '    terms = read_terms(book, glossary)[:-1]'),
            ('omit-discussions', '    scannable = [c for c in chapters if c[1] not in SCAN_EXCLUDED]', '    scannable = []')]
        for label, old, new in replacements:
            require(original.count(old) == 1, 'unique actual omission seam')
            generator.write_text(original.replace(old, new, 1))
            result, trace = run(commands['generator'], fixture, output, label, hook)
            require(result['returncode'] == 1 and not result['traceback'], 'actual generator omission escaped')
            omissions.append({'omission': label, **result})
        generator.write_text(original)
        controls = []
        actual_reads = json.loads((output / 'actual-reads.json').read_text())
        damaged = [dict(row) for row in actual_reads]
        damaged[0]['sha256'] = '0' * 64
        for label, reads in [('omitted-read', actual_reads[1:]), ('changed-read-digest', damaged)]:
            try:
                reconcile(bodies[OUT], reads, expected, declared, bodies)
            except C.Q.Refused as exc:
                controls.append({'control': label, 'returncode': 2, 'reason': str(exc)})
            else:
                raise C.Q.Refused('damaged actual-read ledger escaped: ' + label)
        require(before == C.working_snapshot(args.addition), 'actual HEAD/index/source/modes changed')
        Q.write_json(output / 'working-before.json', before)
        Q.write_json(output / 'working-after.json', before)
        result = {'source': SOURCE, 'source_tree_sha256': source['tree_sha256'],
                  'source_members': len(source['members']), 'input_files': len(bodies),
                  'code_source': 'working' if args.working_code else SOURCE,
                  'input_pins': {n: {'bytes': len(b), 'sha256': C.digest(b), 'mode': selected[n][0]}
                                 for n, b in bodies.items()},
                  'chapters': declared, 'terms': ledger, 'excluded_discussions': ['glossary.md', 'index.md'],
                  'include_expansion': False, 'baseline': results, 'observations': observations,
                  'source_defects': [{'case': r['case'], 'interface': r['interface']}
                                     for r in observations if r['returncode'] != r['expected_returncode']
                                     or r['traceback']],
                  'omissions': omissions, 'ledger_controls': controls,
                  'mode': 'optimized' if sys.flags.optimize else 'normal'}
        Q.write_json(output / 'result.json', result)
        summary = {k: result[k] for k in ['source', 'source_members', 'input_files', 'code_source',
                   'mode', 'include_expansion', 'source_defects', 'ledger_controls']}
        summary.update(chapters=len(declared), terms=len(vocabulary), observations=len(observations),
                       actual_omissions=len(omissions))
        print(json.dumps(summary, sort_keys=True))
        return 0
    except (C.Q.Refused, C.U.BookRefused, OSError, UnicodeError, ValueError, KeyError, TypeError, IndexError) as exc:
        print('BOOK-INDEX-CONSUMER: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
