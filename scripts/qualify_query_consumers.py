#!/usr/bin/env python3
"""Qualify LC0036's catalogue and sealed-history query consumers.

Use fresh --output target/PATH. Default exit0 means measurement complete,
including recorded source defects; --require-clean fails1 on wrong verdicts.
Qualification failures refuse2. No Gitlink implementation or seal is changed.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

import collect_containment_graph as C

ROOT = C.ROOT
SOURCE = '23fdb8ad765cd21cf77bbc895edddc14af6b94da'
CATALOG = 'scripts/record_catalog.py'
HISTORY = 'scripts/history_archive.py'
TASK = 'scripts/task_history_archive.py'
CODE = [CATALOG, HISTORY, TASK, 'scripts/sexp.py']
HI = 'docs/history/archives.json'
TI = 'docs/task-history/descriptor.json'
HM = 'docs/changelog/SHARDS.sha256'
TM = 'docs/history/task-history-manifest.json'
require = C.require

HOOK = '''import hashlib,json,os
from pathlib import Path
original=Path.open
root=Path(os.environ['QUERY_FIXTURE'])
trace=os.environ['QUERY_TRACE']
def log(value):
    with open(trace,'a') as stream:stream.write(json.dumps(value)+'\\n')
class Read:
    def __init__(self,stream,name):self.stream,self.name=stream,name
    def __enter__(self):self.stream.__enter__();return self
    def __exit__(self,*args):return self.stream.__exit__(*args)
    def __getattr__(self,name):return getattr(self.stream,name)
    def read(self,*args,**kwargs):
        value=self.stream.read(*args,**kwargs)
        body=value.encode('utf-8') if isinstance(value,str) else value
        log({'path':self.name,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
        return value
def opened(path,*args,**kwargs):
    try:name=path.absolute().relative_to(root).as_posix()
    except ValueError:return original(path,*args,**kwargs)
    if name==os.environ.get('QUERY_FAULT'):
        log({'fault':name})
        raise OSError('LC0036 controlled actual input open failure')
    return Read(original(path,*args,**kwargs),name)
Path.open=opened
'''


def blobs(revision, names=None):
    rows = C.Q.tree_rows(C.Q.git('ls-tree', '-rz', '--full-tree', revision))
    if names is not None:
        require(set(names) <= set(rows), 'source members unavailable')
        rows = {n: r for n, r in rows.items() if n in names}
    require(all(r[0] != '160000' for r in rows.values()), 'opaque Gitlink selected')
    wire = C.Q.checked_output(subprocess.run(
        ['git', '--no-optional-locks', '-C', str(ROOT), 'cat-file', '--batch'],
        input=b''.join(r[2].encode() + b'\n' for r in rows.values()),
        capture_output=True, check=False))
    return rows, C.blob_contents(rows, wire)


def top_forms(text):
    """Independent balanced-span scan for the immutable catalogue grammar.

    This is a byte/order oracle, not the production S-expression/schema reader.
    Strings, escapes and semicolon comments cannot introduce include directives.
    """
    spans, depth, quoted, escaped, comment, start = [], 0, False, False, False, None
    for i, char in enumerate(text):
        if comment:
            if char == '\n':
                comment = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == ';':
            comment = True
        elif char == '"':
            require(depth > 0, 'unsupported top-level catalogue string')
            quoted = True
        elif char == '(':
            if depth == 0:
                start = i
            depth += 1
        elif char == ')':
            depth -= 1
            require(depth >= 0, 'unbalanced catalogue close')
            if depth == 0:
                spans.append((start, i + 1))
        elif depth == 0:
            require(char.isspace(), 'unsupported top-level catalogue atom')
    require(depth == 0 and not quoted, 'unclosed catalogue form/string')
    return spans


def catalogues(bodies, roots):
    outputs, reads = {}, {}

    def expand(name, visited, order):
        require(name not in visited and name in bodies, 'missing/repeated oracle source')
        visited.add(name)
        order.append(name)
        text = bodies[name].decode('utf-8')
        pieces, cursor = [], 0
        for start, end in top_forms(text):
            form = text[start:end]
            if not re.match(r'^\(include-obligations\b', form):
                continue
            match = re.fullmatch(r'\(include-obligations \(path "([^"\\]+)"\)\)', form)
            require(match is not None, 'unsupported immutable include syntax')
            target = C.Q.relative_path(match[1])
            value = expand(target, visited, order)
            if value.endswith('\n') and text[end:end + 1] == '\n':
                value = value[:-1]
            pieces.extend([text[cursor:start], value])
            cursor = end
        pieces.append(text[cursor:])
        return ''.join(pieces)

    for name in roots:
        order = []
        text = expand(name, set(), order)
        outputs[name] = text.encode('utf-8')
        reads[name] = order
    require(len(roots) == 6 and len(set(n for v in reads.values() for n in v)) == 8,
            'complete six-root/two-part catalogue population')
    return outputs, reads


def tar_members(blob):
    members = {}
    with tarfile.open(fileobj=io.BytesIO(gzip.decompress(blob)), mode='r:') as archive:
        for member in archive:
            require(member.isfile() and member.name not in members, 'ambiguous source archive')
            members[member.name] = archive.extractfile(member).read()
    return members


def original_members(revision, names, archived):
    rows, bodies = blobs(revision, names)
    records = []
    for name in names:
        body = bodies[name]
        require(body == archived[name], 'whole original capture differs: ' + name)
        records.append({'path': name, 'mode': rows[name][0], 'oid': rows[name][2],
                        'bytes': len(body), 'lines': body.count(b'\n'),
                        'sha256': C.digest(body)})
    return records


def independent_archives(bodies):
    h = json.loads(bodies[HI])['archives']
    require(len(h) == 1, 'one approved history object expected')
    h = h[0]
    t = json.loads(bodies[TI])
    hm, tm = tar_members(bodies[h['object']]), tar_members(bodies[t['object']])
    all_h = C.Q.tree_rows(C.Q.git('ls-tree', '-rz', '--full-tree', h['capture']))
    hnames = sorted(n for n in all_h if n.startswith('docs/changelog/')
                    and '/' not in n[len('docs/changelog/'):]
                    and n.endswith('.md'))
    tnames = ['docs/tasks/archive/P4-SYSTEM.md'] + [
        f'docs/tasks/archive/P4-SYSTEM-{n}.md' for n in range(2, 13)]
    require(len(hnames) == 210 and set(hm) == set(hnames) | {HM}, 'whole history membership')
    require(set(tm) == set(tnames) | {TM}, 'whole P4 membership')
    hrecords = original_members(h['capture'], hnames, hm)
    trecords = original_members(t['capture'], tnames, tm)
    _, old_manifest = blobs(h['capture'], [HM])
    require(old_manifest[HM] == hm[HM], 'complete original history manifest')
    hrows = [(line.split('  ', 1)[1], line.split('  ', 1)[0])
             for line in hm[HM].decode().splitlines()]
    require(hrows == [(r['path'], r['sha256']) for r in hrecords], 'history manifest/capture order')
    task_manifest = json.loads(tm[TM])
    require(task_manifest['members'] == [
        {k: r[k] for k in ['path', 'sha256', 'bytes', 'lines']} for r in trecords],
        'P4 manifest/capture order')
    require(sum(map(len, hm.values())) == h['source_bytes']
            and sum(b.count(b'\n') for b in hm.values()) == h['source_lines'],
            'whole history aggregate')
    require(sum(r['bytes'] for r in trecords) == t['source_bytes']
            and sum(r['lines'] for r in trecords) == t['source_lines'], 'whole P4 aggregate')
    return h, t, hm, tm, hrecords, trecords


def write_fixture(directory, bodies, modes):
    require(not directory.exists(), 'fresh query fixture required')
    for name, body in bodies.items():
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        path.chmod(0o755 if modes[name] == '100755' else 0o644)


def repack(members):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name, body in members.items():
            info = tarfile.TarInfo(name)
            info.mode, info.size = 0o644, len(body)
            archive.addfile(info, io.BytesIO(body))
    return gzip.compress(buffer.getvalue(), mtime=0), len(buffer.getvalue())


def changed_byte(body):
    value = bytearray(body)
    position = next(i for i, b in enumerate(value) if 65 <= b <= 90 or 97 <= b <= 122)
    value[position] ^= 1
    return bytes(value)


def forged_terminal(fixture, family, descriptor, members, victim):
    """Change one original and outer identities only in an owned disposable copy."""
    changed = dict(members)
    changed[victim] = changed_byte(changed[victim])
    row = copy.deepcopy(descriptor)
    if family == 'task':
        manifest = json.loads(changed[TM])
        entry = next(r for r in manifest['members'] if r['path'] == victim)
        entry['sha256'] = C.digest(changed[victim])
        changed[TM] = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
        row['manifest_sha256'] = C.digest(changed[TM])
        row['manifest_bytes'] = len(changed[TM])
        stub = fixture / victim
        original_sha = C.digest(members[victim]).encode()
        require(stub.read_bytes().count(original_sha) == 1, 'one navigation original identity')
        stub.write_bytes(stub.read_bytes().replace(original_sha, entry['sha256'].encode(), 1))
    blob, tar_bytes = repack(changed)
    old_object = row['object']
    sha = C.digest(blob)
    row['object'] = ('docs/history/sealed/' if family == 'history'
                     else 'docs/task-history/sealed/') + sha + '.tar.gz'
    row['sha256'] = sha
    if family == 'history':
        row['bytes'] = len(blob)
        encoded = (json.dumps({'schema_version': 1, 'archives': [row]}, indent=2) + '\n').encode()
        index = HI
    else:
        row['compressed_bytes'], row['tar_bytes'] = len(blob), tar_bytes
        encoded = (json.dumps(row, indent=2, sort_keys=True) + '\n').encode()
        index = TI
    (fixture / old_object).unlink()
    (fixture / row['object']).write_bytes(blob)
    (fixture / index).write_bytes(encoded)
    return {'family': family, 'changed_original': victim,
            'old_original_sha256': C.digest(members[victim]),
            'new_original_sha256': C.digest(changed[victim]),
            'object': row['object'], 'object_sha256': sha,
            'index_sha256': C.digest(encoded), 'tar_bytes': tar_bytes}


def reconcile_trace(trace, names, bodies):
    expected = [{'path': n, 'bytes': len(bodies[n]), 'sha256': C.digest(bodies[n])} for n in names]
    require(trace == expected, 'complete actual input reads/order/digests differ')


def invalid_deflate(fixture, descriptor):
    """Retain valid outer metadata while corrupting the actual gzip stream."""
    bad = b'\x1f\x8b\x08\x00' + b'\x00' * 6 + b'\x07' + b'\x00' * 8
    row = dict(descriptor)
    row.update(sha256=C.digest(bad), bytes=len(bad),
               object='docs/history/sealed/' + C.digest(bad) + '.tar.gz')
    (fixture / descriptor['object']).unlink()
    (fixture / row['object']).write_bytes(bad)
    (fixture / HI).write_text(json.dumps({'schema_version': 1, 'archives': [row]}) + '\n')
    return {'case': 'invalid-deflate', 'gzip_hex': bad.hex(), 'descriptor': row}


def reconcile_queries(observations, expected):
    queries = [r for r in observations if r.get('original')]
    require(len(queries) == len(expected), 'complete original query count differs')
    actual = {(r['family'], r['original']): r for r in queries}
    require(len(actual) == len(queries) and set(actual) == set(expected),
            'complete original query membership differs')
    for key, record in actual.items():
        target = expected[key]
        require(record['returncode'] == 0 and not record['traceback']
                and record['git_calls'] == 0
                and record['stdout_bytes'] == target['bytes']
                and record['stdout_sha256'] == target['sha256'], 'whole original output differs')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--addition', action='append', default=[])
    parser.add_argument('--working-code', action='store_true')
    parser.add_argument('--require-clean', action='store_true')
    args = parser.parse_args()
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    try:
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'on-volume target output required')
        output = C.U.source_path(ROOT, args.output)
        require(not output.exists(), 'fresh output required')
        before = C.working_snapshot(args.addition)
        source = C.source_census(SOURCE)
        require(len(source['members']) == 1454, 'complete immutable source population')
        all_rows = C.Q.tree_rows(C.Q.git('ls-tree', '-rz', '--full-tree', SOURCE))
        roots = sorted(n for n in all_rows if re.fullmatch(r'profiles/[^/]+/contract-obligations\.sexp', n))
        names = {n for n, r in all_rows.items() if r[0] != '160000' and
                 (n in CODE or n.startswith(('docs/history/', 'docs/task-history/'))
                  or re.fullmatch(r'docs/tasks/archive/P4-SYSTEM(?:-(?:[2-9]|1[0-2]))?\.md', n)
                  or n in roots or (n.startswith('profiles/') and n.endswith('.obligations.sexp')))}
        selected, bodies = blobs(SOURCE, names)
        if args.working_code:
            for n in CODE:
                require(C.file_identity(n)['mode'] == (0o755 if selected[n][0] == '100755' else 0o644),
                        'working query code mode differs')
                bodies[n] = (ROOT / n).read_bytes()
        expanded, catalog_reads = catalogues(bodies, roots)
        h, t, hm, tm, hrecords, trecords = independent_archives(bodies)
        modes = {n: r[0] for n, r in selected.items()}
        output.mkdir(parents=True)
        (output / 'tmp').mkdir()
        hook = output / 'hook'
        hook.mkdir()
        (hook / 'sitecustomize.py').write_text(HOOK)
        tools = output / 'tools'
        tools.mkdir()
        (tools / 'git').write_text('#!/bin/bash\nprintf \'git\\n\' >> "$QUERY_GIT_LOG"\nexit 97\n')
        (tools / 'git').chmod(0o755)
        observations, protocols = [], []
        traces = {}
        sequence = 0

        def fixture(label):
            directory = output / label
            write_fixture(directory, bodies, modes)
            return directory

        def observe(directory, family, case, extra, expected_rc, expected_stdout=None,
                    read_names=None, fault=None, original=None, collect=True):
            nonlocal sequence
            sequence += 1
            label = f'{sequence:04d}-{case}'
            trace_file = output / (label + '.reads.jsonl')
            trace_file.write_bytes(b'')
            git_log = output / (label + '.git-calls')
            git_log.write_bytes(b'')
            env = dict(os.environ)
            env.update(TMPDIR=str(output / 'tmp'), PYTHONDONTWRITEBYTECODE='1',
                       PYTHONPATH=str(hook), QUERY_FIXTURE=str(directory), QUERY_TRACE=str(trace_file),
                       PATH=str(tools) + os.pathsep + env['PATH'], QUERY_GIT_LOG=str(git_log))
            if sys.flags.optimize:
                env['PYTHONOPTIMIZE'] = '1'
            else:
                env.pop('PYTHONOPTIMIZE', None)
            if fault:
                env['QUERY_FAULT'] = fault
            else:
                env.pop('QUERY_FAULT', None)
            script = {'catalogue': CATALOG, 'history': HISTORY, 'task': TASK}[family]
            command = [sys.executable, script, *extra, '--root', '.']
            result = subprocess.run(command, cwd=directory, env=env, capture_output=True,
                                    check=False, timeout=60)
            (output / (label + '.stdout')).write_bytes(result.stdout)
            (output / (label + '.stderr')).write_bytes(result.stderr)
            trace = [json.loads(line) for line in trace_file.read_text().splitlines()]
            if fault:
                require([r for r in trace if 'fault' in r] == [{'fault': fault}],
                        'actual source open fault must fire exactly once')
            if read_names is not None:
                reconcile_trace(trace, read_names, bodies)
            prefix = {'catalogue': b'RECORD-CATALOG: REFUSED', 'history': b'HISTORY-ARCHIVE: REFUSED',
                      'task': b'TASK-HISTORY: REFUSED'}[family]
            traceback = b'Traceback' in result.stderr
            git_calls = len(git_log.read_text().splitlines())
            good = (result.returncode == expected_rc and not traceback and git_calls == 0
                    and (expected_stdout is None or result.stdout == expected_stdout)
                    and (expected_rc == 0 or (not result.stdout and result.stderr.startswith(prefix))))
            record = {'family': family, 'case': case, 'command': ['python3', *command[1:]],
                      'expected_returncode': expected_rc, 'returncode': result.returncode,
                      'stdout_bytes': len(result.stdout), 'stdout_sha256': C.digest(result.stdout),
                      'stderr_sha256': C.digest(result.stderr), 'traceback': traceback,
                      'expected_contract': good, 'fault_calls': int(bool(fault)),
                      'read_events': len(trace), 'git_calls': git_calls}
            if original:
                record['original'] = original
            if collect:
                observations.append(record)
            return record, trace

        baseline = fixture('baseline')
        for name in roots:
            result, trace = observe(baseline, 'catalogue', 'catalogue-stdout', [name, '--stdout'],
                                    0, expanded[name], catalog_reads[name])
            result['catalogue'] = name
            traces[name] = trace
            forms = top_forms(expanded[name].decode())
            count = sum(expanded[name].decode()[a:b].startswith('(obligation ') for a, b in forms)
            report = f'RECORD-CATALOG: ok ({count} obligations, {len(expanded[name])} expanded bytes)\n'.encode()
            result, _ = observe(baseline, 'catalogue', 'catalogue-report', [name], 0,
                                report, catalog_reads[name])
            result['catalogue'] = name
        hreads, treads = [HI, h['object']], [TI, 'docs/task-history/README.md', t['object'],
                                          *[r['path'] for r in trecords]]
        _, traces['history'] = observe(baseline, 'history', 'history-verify', [], 0,
            b'HISTORY-ARCHIVE: ok (1 sealed object(s), 210 authenticated shards)\n', hreads)
        _, traces['task'] = observe(baseline, 'task', 'task-verify', [], 0,
            f'TASK-HISTORY: ok (12 originals, {t["source_bytes"]} authenticated bytes)\n'.encode(), treads)
        observe(baseline, 'task', 'task-list', ['--list'], 0,
                ('\n'.join(r['path'] for r in trecords) + '\n').encode(), treads)
        expected_queries = {}
        for family, records, members, reads in [('history', hrecords, hm, hreads),
                                                 ('task', trecords, tm, treads)]:
            for record in records:
                name = record['path']
                expected_queries[(family, name)] = record
                observe(baseline, family, 'original-read', ['--read', name], 0,
                        members[name], reads, original=name)
        reconcile_queries(observations, expected_queries)

        for family, path in [('history', HM), ('history', 'docs/changelog/shard-0313.md'),
                             ('task', TM), ('task', 'docs/tasks/P4-SYSTEM.md')]:
            observe(baseline, family, 'excluded-query', ['--read', path], 1)
        gc = 'profiles/rv64gc-lab-v0/contract-obligations.sexp'
        part = catalog_reads[gc][1]
        mutations = [
            ('missing-catalogue', 'catalogue', roots[0], None, [roots[0], '--stdout']),
            ('missing-part', 'catalogue', part, None, [gc, '--stdout']),
            ('invalid-part-utf8', 'catalogue', part, b'\xff', [gc, '--stdout']),
            ('missing-history-index', 'history', HI, None, []),
            ('invalid-history-index-utf8', 'history', HI, b'\xff', []),
            ('deep-history-index', 'history', HI, b'[' * 8000 + b']' * 8000, []),
            ('corrupt-history-object', 'history', h['object'], changed_byte(bodies[h['object']]), []),
            ('missing-task-navigation', 'task', trecords[-1]['path'], None, []),
            ('invalid-task-descriptor-utf8', 'task', TI, b'\xff', []),
            ('corrupt-task-object', 'task', t['object'], changed_byte(bodies[t['object']]), []),
        ]
        for case, family, name, body, extra in mutations:
            directory = fixture(case)
            path = directory / name
            if body is None:
                path.unlink()
            else:
                path.write_bytes(body)
            protocols.append({'case': case, 'changed_path': name,
                              'body_sha256': C.digest(body) if body is not None else None})
            observe(directory, family, case, extra, 1)
        for case, suffix in [('duplicate-part', f'(include-obligations (path "{part}"))\n'),
                             ('include-cycle', f'(include-obligations (path "{gc}"))\n'),
                             ('escaping-part', '(include-obligations (path "../outside.sexp"))\n')]:
            directory = fixture(case)
            (directory / gc).write_bytes(bodies[gc] + suffix.encode())
            protocols.append({'case': case, 'changed_path': gc, 'appended': suffix})
            observe(directory, 'catalogue', case, [gc, '--stdout'], 1)
        directory = fixture('invalid-deflate')
        protocols.append(invalid_deflate(directory, h))
        observe(directory, 'history', 'invalid-deflate', [], 1)
        for family, paths in [('catalogue', [gc, part]), ('history', [HI, h['object']]),
                              ('task', [TI, trecords[-1]['path']])]:
            for name in paths:
                observe(baseline, family, 'actual-open-failed', [gc, '--stdout'] if family == 'catalogue' else [],
                        1, fault=name)

        forgeries = {}
        for family, descriptor, members, records in [('history', h, hm, hrecords),
                                                     ('task', t, tm, trecords)]:
            directory = fixture('forged-' + family)
            protocol = forged_terminal(directory, family, descriptor, members, records[-1]['path'])
            forgeries[family] = protocol
            observe(directory, family, 'forged-' + family, ['--read', records[0]['path']], 1)

        omissions = []
        seams = [
            ('catalogue', CATALOG, 'for form, start, end in forms:', 'for form, start, end in ():'),
            ('history', HISTORY, "require(digest(members[name]) == sha, 'archived shard digest differs')", 'pass # LC0036 omitted whole-member authentication'),
            ('task', TASK, "require(digest(encoded) == INDEX_SHA256, 'approved descriptor identity differs')", 'pass # LC0036 omitted approved descriptor authentication'),
        ]
        for family, script, old, new in seams:
            directory = fixture('omit-' + family)
            require(bodies[script].count(old.encode()) == 1, 'unique actual query omission')
            changed = bodies[script].replace(old.encode(), new.encode(), 1)
            (directory / script).write_bytes(changed)
            if family == 'catalogue':
                extra, want, code = [gc, '--stdout'], expanded[gc], 0
            else:
                descriptor, members, records = (h, hm, hrecords) if family == 'history' else (t, tm, trecords)
                forged_terminal(directory, family, descriptor, members, records[-1]['path'])
                extra, want, code = ['--read', records[0]['path']], None, 1
            actual, _ = observe(directory, family, 'actual-omission', extra, code, want, collect=False)
            require(actual['returncode'] == 0 and not actual['traceback'] and not actual['expected_contract'],
                    'actual query omission did not discriminate')
            omissions.append({'family': family, 'source_old': old, 'source_new': new,
                              'mutated_code_sha256': C.digest(changed), 'observation': actual,
                              'qualification_returncode': 1})

        refusal_omission = None
        if args.working_code:
            old = 'except (OSError, EOFError, zlib.error, tarfile.TarError) as exc:'
            new = 'except (OSError, EOFError, tarfile.TarError) as exc:'
            require(bodies[HISTORY].count(old.encode()) == 1, 'unique repaired deflate catch')
            directory = fixture('omit-deflate-catch')
            changed = bodies[HISTORY].replace(old.encode(), new.encode(), 1)
            (directory / HISTORY).write_bytes(changed)
            invalid_deflate(directory, h)
            actual, _ = observe(directory, 'history', 'actual-refusal-omission', [],
                                1, collect=False)
            require(actual['returncode'] == 1 and actual['traceback']
                    and not actual['stdout_bytes'] and not actual['expected_contract'],
                    'actual deflate catch omission did not discriminate')
            refusal_omission = {'source_old': old, 'source_new': new,
                               'mutated_code_sha256': C.digest(changed),
                               'observation': actual, 'qualification_returncode': 1}

        controls = []
        for name in ['omitted-query', 'duplicate-query', 'forged-query-digest',
                     'forbidden-query-git-call', 'omitted-catalogue-read',
                     'omitted-history-read', 'forged-task-read-digest']:
            try:
                changed = copy.deepcopy(observations)
                if name == 'omitted-query':
                    changed.remove(next(r for r in changed if r.get('original')))
                elif name == 'duplicate-query':
                    changed.append(copy.deepcopy(next(r for r in changed if r.get('original'))))
                elif name == 'forged-query-digest':
                    next(r for r in changed if r.get('original'))['stdout_sha256'] = '0' * 64
                elif name == 'forbidden-query-git-call':
                    next(r for r in changed if r.get('original'))['git_calls'] = 1
                else:
                    key, expected_names = {'omitted-catalogue-read': (gc, catalog_reads[gc]),
                        'omitted-history-read': ('history', hreads),
                        'forged-task-read-digest': ('task', treads)}[name]
                    trace = copy.deepcopy(traces[key])
                    if name.startswith('omitted'):
                        trace.pop()
                    else:
                        trace[-1]['sha256'] = '0' * 64
                    reconcile_trace(trace, expected_names, bodies)
                reconcile_queries(changed, expected_queries)
            except ValueError:
                controls.append({'control': name, 'returncode': 2})
            else:
                raise ValueError('independent query/trace corruption was accepted')
        require(before == C.working_snapshot(args.addition), 'actual source/index/modes changed')
        defects = [r for r in observations if not r['expected_contract']]
        result = {'source': SOURCE, 'source_members': 1454, 'source_tree_sha256': source['tree_sha256'],
            'mode': 'optimized' if sys.flags.optimize else 'normal',
            'code_mode': 'working' if args.working_code else 'immutable',
            'inputs': [{**r, 'bytes': len(bodies[r['path']]), 'sha256': C.digest(bodies[r['path']])}
                       for r in source['members'] if r['path'] in bodies],
            'catalogues': [{'path': n, 'sources': catalog_reads[n], 'expanded_bytes': len(expanded[n]),
                            'expanded_sha256': C.digest(expanded[n])} for n in roots],
            'history_capture': h['capture'], 'task_capture': t['capture'],
            'originals': {'history': hrecords, 'task': trecords},
            'read_profiles': traces, 'observations': observations, 'source_defects': len(defects),
            'protocols': protocols, 'forgeries': forgeries, 'actual_omissions': omissions,
            'ledger_controls': controls,
            'exclusions': {'sealed_manifests': [HM, TM],
                'direct_live_history': sorted(n for n in all_rows if n.startswith('docs/changelog/') and n.endswith('.md')),
                'ordinary_task_records': sorted(n for n in all_rows if n.startswith('docs/tasks/') and n.endswith('.md')
                    and n not in {r['path'] for r in trecords}),
                'catalogue_parts': sorted(set(n for v in catalog_reads.values() for n in v) - set(roots))}}
        if refusal_omission is not None:
            result['refusal_omission'] = refusal_omission
        (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({'source': SOURCE, 'mode': result['mode'], 'code_mode': result['code_mode'],
            'inputs': len(bodies), 'catalogues': len(roots), 'history_originals': len(hrecords),
            'task_originals': len(trecords), 'observations': len(observations), 'source_defects': len(defects),
            'actual_omissions': len(omissions), 'ledger_controls': len(controls)}))
        return 1 if args.require_clean and defects else 0
    except (ValueError, OSError, UnicodeError, EOFError, tarfile.TarError,
            subprocess.SubprocessError, StopIteration) as exc:
        print('qualify_query_consumers: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
