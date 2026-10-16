#!/usr/bin/env python3
"""Qualify LC0038's actual owned mdBook navigation consumer.

Use a fresh --output target/PATH. Source copies omit Gitlinks. Captures retain
relative book identities and whole protocol books, never absolute contexts.
Default replay retains immutable code; --working-code overlays only the owned
navigation consumer and its permanent probe on the same authenticated data.
"""
from __future__ import annotations

import argparse
import copy
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import posixpath
import re
import shlex
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit

import collect_containment_graph as C
import qualify_book_includes as B

ROOT = C.ROOT
SOURCE = '213f818533f66b024f9dbb2561122d0bb39ddf6a'
NAV = 'scripts/book_navigation.py'
PROBE = 'scripts/probe_book_navigation.py'
require = C.require

READ_HOOK = '''import hashlib,json,os
from pathlib import Path
original=Path.open
root=Path(os.environ['NAV_READ_ROOT'])
class Read:
    def __init__(self,stream,name):self.stream,self.name=stream,name
    def __enter__(self):self.stream.__enter__();return self
    def __exit__(self,*args):return self.stream.__exit__(*args)
    def __getattr__(self,name):return getattr(self.stream,name)
    def read(self,*a,**k):
        value=self.stream.read(*a,**k)
        body=value.encode('utf-8') if isinstance(value,str) else value
        with open(os.environ['NAV_READ_LOG'],'a') as log:
            log.write(json.dumps({'path':self.name,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})+'\\n')
        return value
def opened(path,*a,**k):
    try:name=path.absolute().relative_to(root).as_posix()
    except ValueError:return original(path,*a,**k)
    return Read(original(path,*a,**k),name)
Path.open=opened
'''


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def capture(args):
    fixture = C.U.source_path(ROOT, args.fixture)
    command = [sys.executable, str(fixture / NAV)]
    if args.action is not None:
        result = subprocess.run(command + [args.action] + ([args.renderer] if args.renderer else []),
                                capture_output=True, check=False)
        sys.stdout.buffer.write(result.stdout)
        sys.stderr.buffer.write(result.stderr)
        return result.returncode
    incoming = sys.stdin.buffer.read()
    context, before = json.loads(incoming)
    path = C.U.source_path(ROOT, args.capture_output)
    require(args.capture_output.startswith('target/') and not path.exists(),
            'fresh on-volume capture required')
    path.parent.mkdir(parents=True, exist_ok=True)
    read_log = path.with_suffix('.reads.jsonl')
    read_log.write_bytes(b'')
    if args.passthrough:
        stdout = json.dumps(before, ensure_ascii=False).encode() + b'\n'
        stderr, rc = b'', 0
    else:
        hook = path.parent / 'read-hook'
        hook.mkdir()
        (hook / 'sitecustomize.py').write_text(READ_HOOK)
        env = dict(os.environ, PYTHONPATH=str(hook), NAV_READ_ROOT=str(fixture),
                   NAV_READ_LOG=str(read_log))
        result = subprocess.run(command, input=incoming, capture_output=True, check=False, env=env)
        stdout, stderr, rc = result.stdout, result.stderr, result.returncode
    after = json.loads(stdout) if rc == 0 else None
    root = Path(context['root']).resolve().relative_to(fixture).as_posix()
    write_json(path, {'root': root, 'renderer': context['renderer'],
        'mdbook_version': context['mdbook_version'], 'protocol_input_sha256': C.digest(incoming),
        'before': before, 'after': after, 'returncode': rc,
        'stdout_bytes': len(stdout), 'stdout_sha256': C.digest(stdout),
        'stderr_bytes': len(stderr), 'stderr_sha256': C.digest(stderr),
        'stderr': stderr.decode('utf-8'),
        'reads': [json.loads(line) for line in read_log.read_text().splitlines()]})
    sys.stdout.buffer.write(stdout)
    sys.stderr.buffer.write(stderr)
    return rc


def environment(temporary):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith('MDBOOK_') and k != 'PYTHONOPTIMIZE'}
    env.update(TMPDIR=str(temporary), PYTHONDONTWRITEBYTECODE='1')
    if sys.flags.optimize:
        env['PYTHONOPTIMIZE'] = '1'
    return env


def copy_fixture(source, output, overlays):
    """Authenticate the original copy before overlaying explicitly pinned code.

    The expected-copy view changes byte fingerprints only; its immutable Git
    provenance remains separate from the working code identities in the result.
    """
    fixture, _ = B.copy_source(source, output)
    expected = copy.deepcopy(source)
    for row in expected['members']:
        name = row['path']
        if name in overlays:
            body = overlays[name]
            (fixture / name).write_bytes(body)
            row.update(bytes=len(body), sha256=C.digest(body), lf_lines=body.count(b'\n'))
    B.verify_copy(expected, fixture)
    return fixture, expected


def destination(book, chapter, target, books, members):
    """Independent declared route contract; no production resolver/mask import."""
    url = urlsplit(target)
    if url.scheme or url.netloc or not url.path or '\\' in url.path:
        return None
    parent = posixpath.dirname(chapter)
    source = posixpath.normpath(posixpath.join(book, 'src', parent, url.path))
    if book == 'docs/book':
        if url.query or url.fragment:
            return None
        task = re.fullmatch(r'(?:docs/)?tasks/([A-Z0-9-]+)\.md', url.path)
        if task:
            source, role = 'docs/tasks/' + task[1] + '.md', 'task'
        elif source in {'docs/tasks/archive/P4-SYSTEM-reference-c29e.md',
                        'docs/task-history/README.md'}:
            role = 'history'
        else:
            return None
        require(source in members, 'declared oracle record unavailable')
        return (posixpath.relpath('working/task-trees.md', parent or '.') + '#read-task-history',
                role, source)
    for sibling in books[1:]:
        prefix = sibling + '/src/'
        if sibling == book or not source.startswith(prefix) or not source.endswith('.md'):
            continue
        require(source in members, 'declared oracle sibling unavailable')
        path = source[len(prefix):-3] + '.html'
        replacement = posixpath.relpath(sibling + '/book/' + path,
                                        posixpath.join(book, 'book', parent))
        return urlunsplit(('', '', replacement, url.query, url.fragment)), 'sibling', source
    return None


def rendered_href(value):
    url = urlsplit(value)
    path = url.path[:-3] + '.html' if url.path.endswith('.md') else url.path
    return urlunsplit((url.scheme, url.netloc, path, url.query, url.fragment))


def source_protocols(books, captures, members):
    """Only declared destination tokens may differ; all other book data is exact.

    The candidate scan deliberately includes literal examples. Independent full
    HTML transformation and per-chapter counts distinguish executed links.
    """
    records, mappings, expected_counts = [], {}, {}
    pattern = re.compile(r'\]\(([^\s()]+)\)')
    for book in books:
        protocol = captures[book]
        require(protocol['mdbook_version'] == '0.5.4', 'unreviewed mdBook protocol version')
        before, after = protocol['before'], protocol['after']
        old, new = B.chapters(before), B.chapters(after)
        require(len(old) == len(new), 'whole navigation chapter population differs')
        reconstructed = copy.deepcopy(before)
        rebuilt = B.chapters(reconstructed)
        total = 0
        for a, b, expected in zip(old, new, rebuilt):
            path = a['path']
            require(isinstance(path, str) and path.endswith('.md')
                    and a['source_path'] == b['source_path'] == path,
                    'unsupported source/output chapter identity')
            text, changed = a['content'], b['content']
            cursor, position, edits, candidates, mapping = 0, 0, [], [], {}
            for match in pattern.finditer(text):
                start, end = match.span(1)
                prefix = text[cursor:start]
                require(changed.startswith(prefix, position), 'non-destination chapter text changed')
                position += len(prefix)
                target = match[1]
                route = destination(book, path, target, books, members)
                if route:
                    value, role, source = route
                    key = rendered_href(target)
                    replacement = rendered_href(value)
                    require(key not in mapping or mapping[key][0] == replacement,
                            'ambiguous closed rendered route')
                    mapping[key] = (replacement, role, source)
                    candidates.append({'offset': len(text[:start].encode()), 'target': target,
                                       'replacement': value, 'role': role, 'source': source})
                if changed.startswith(target, position):
                    position += len(target)
                else:
                    require(route is not None and changed.startswith(route[0], position),
                            'unrecognized source destination change')
                    edits.append(candidates[-1])
                    position += len(route[0])
                cursor = end
            require(changed[position:] == text[cursor:], 'trailing chapter content changed')
            expected['content'] = changed
            page = book + '/book/' + path[:-3] + '.html'
            require(page not in mappings, 'duplicate source output page')
            mappings[page], expected_counts[page] = mapping, len(edits)
            total += len(edits)
            records.append({'book': book, 'chapter': path,
                'before_bytes': len(text.encode()), 'before_sha256': C.digest(text.encode()),
                'after_bytes': len(changed.encode()), 'after_sha256': C.digest(changed.encode()),
                'candidates': candidates, 'edits': edits})
        require(reconstructed == after, 'non-content protocol metadata changed')
        require(protocol['stderr'] == f'BOOK-NAVIGATION: resolved {total} declared book links\n',
                'actual consumer witness differs from whole source edits')
    require(len(records) == 93, 'complete observed source chapter population')
    return records, mappings, expected_counts


class Hrefs(HTMLParser):
    """Record actual quoted anchor attribute spans without a Markdown mask."""
    def __init__(self, body):
        super().__init__(convert_charrefs=True)
        self.offsets = [0] + [m.end() for m in re.finditer('\n', body)]
        self.hrefs = []
        self.feed(body)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        values = [value for key, value in attrs if key == 'href']
        if not values:
            return
        raw = self.get_starttag_text()
        spans = list(re.finditer(r'\bhref\s*=\s*([\'"])(.*?)\1', raw, re.S))
        require(len(values) == len(spans) == 1 and values[0] is not None,
                'ambiguous/unquoted rendered anchor')
        line, column = self.getpos()
        offset = self.offsets[line - 1] + column
        self.hrefs.append((offset + spans[0].start(2), offset + spans[0].end(2), values[0]))


def rendered_oracle(output, books, stages, mappings, expected_counts):
    bare, actual = output / 'bare/site', output / 'captured/site'
    files = stages['bare']['files']
    require(set(files) == set(stages['captured']['files']), 'complete bare/actual output membership differs')
    # An authored index owns its own mapping. Otherwise authenticate mdBook's
    # first-chapter alias before reusing that chapter's source mapping.
    for book in books:
        first = next(p for p in mappings if p.startswith(book + '/book/'))
        alias = book + '/book/index.html'
        if alias in mappings:
            continue
        require(files[alias] == files[first], 'unqualified first-chapter index alias')
        mappings[alias], expected_counts[alias] = mappings[first], expected_counts[first]
    print_maps = {book: {} for book in books}
    for page, mapping in mappings.items():
        book = next(b for b in books if page.startswith(b + '/book/'))
        parent = posixpath.dirname(page[len(book + '/book/'):])
        for old, (new, role, source) in mapping.items():
            a, b = urlsplit(old), urlsplit(new)
            key = urlunsplit(('', '', posixpath.normpath(posixpath.join(parent, a.path)),
                              a.query, a.fragment))
            value = '#read-task-history' if book == 'docs/book' else urlunsplit(
                ('', '', posixpath.normpath(posixpath.join(parent, b.path)), b.query, b.fragment))
            candidate = (value, role, source)
            require(key not in print_maps[book] or print_maps[book][key] == candidate,
                    'ambiguous closed print route')
            print_maps[book][key] = candidate
    routes, exclusions, counts = [], [], {}
    for name in files:
        body = (bare / name).read_bytes()
        if not name.endswith('.html'):
            require(body == (actual / name).read_bytes(), 'non-HTML generated bytes changed')
            continue
        text = body.decode('utf-8')
        book = next(b for b in books if name.startswith(b + '/book/'))
        mapping = print_maps[book] if name.endswith('/print.html') else mappings.get(name, {})
        edits = []
        for start, end, value in Hrefs(text).hrefs:
            if value not in mapping:
                url = urlsplit(value)
                reason = 'remote' if url.scheme or url.netloc else 'fragment' if not url.path else 'not-declared-navigation-route'
                exclusions.append({'page': name, 'href': value, 'reason': reason})
                continue
            replacement, role, source = mapping[value]
            edits.append((start, end, html.escape(replacement, quote=True)))
            routes.append({'page': name, 'offset': len(text[:start].encode()), 'href': value,
                           'replacement': replacement, 'role': role, 'source': source})
        expected = text
        for start, end, value in reversed(edits):
            expected = expected[:start] + value + expected[end:]
        require(expected.encode() == (actual / name).read_bytes(),
                'whole independently transformed rendered bytes differ: ' + name)
        counts[name] = len(edits)
    require(all(counts[page] == n for page, n in expected_counts.items()),
            'actual source edit counts differ from independently rendered links')
    outputs = [actual / book / 'book' for book in books]
    findings, checked = C.U.navigation_findings(actual / 'docs', outputs)
    require(not findings and checked == len(routes) + len(exclusions),
            'actual rendered navigation/count differs')
    return {'routes': routes, 'exclusions': exclusions, 'hyperlinks': checked,
            'changed_files': [n for n in files if files[n] != stages['captured']['files'][n]]}


def public_cases(fixture, output):
    """Execute real stdin/argument contracts, including the observed depth fault."""
    context = {'root': str(fixture / 'docs/book'), 'renderer': 'html'}
    book = {'items': [{'Chapter': {'path': 'status.md', 'content':
            '[Task é](docs/tasks/P4-SYSTEM.md)\n', 'sub_items': []}}]}
    expected = copy.deepcopy(book)
    expected['items'][0]['Chapter']['content'] = '[Task é](working/task-trees.md#read-task-history)\n'
    records = []

    def observe(name, *, args=(), payload=None, want=2, body=b'', fault=False):
        env = environment(output / 'tmp')
        log = output / 'public'
        log.mkdir(exist_ok=True)
        fault_log = log / (name + '.faults')
        fault_log.write_bytes(b'')
        if fault:
            hook = output / 'fault-hook'
            hook.mkdir(exist_ok=True)
            (hook / 'sitecustomize.py').write_text(
                "import os\nfrom pathlib import Path\noriginal=Path.open\n"
                "def read(path,*a,**k):\n"
                "    if str(path)==os.environ['NAV_FAULT_PATH']:\n"
                "        with open(os.environ['NAV_FAULT_LOG'],'a') as f:f.write('fault\\n')\n"
                "        raise OSError('LC0038 controlled registry input open failure')\n"
                "    return original(path,*a,**k)\nPath.open=read\n")
            env.update(PYTHONPATH=str(hook), NAV_FAULT_PATH=str(fixture / 'materials/units.sexp'),
                       NAV_FAULT_LOG=str(fault_log))
        command = [sys.executable, str(fixture / NAV), *args]
        result = subprocess.run(command, input=payload, capture_output=True, check=False,
                                env=env, timeout=60)
        (log / (name + '.stdout')).write_bytes(result.stdout)
        (log / (name + '.stderr')).write_bytes(result.stderr)
        calls = len(fault_log.read_text().splitlines())
        require(calls == int(fault), 'actual registry input fault did not fire once')
        traceback = b'Traceback' in result.stderr
        good = (result.returncode == want and not traceback and result.stdout == body
                and (want != 2 or result.stderr.startswith(b'BOOK-NAVIGATION: REFUSED')))
        records.append({'case': name, 'command': ['python3', NAV, *args],
            'input_sha256': C.digest(payload) if payload is not None else None,
            'expected_returncode': want, 'returncode': result.returncode,
            'stdout_bytes': len(result.stdout), 'stdout_sha256': C.digest(result.stdout),
            'stderr_sha256': C.digest(result.stderr), 'traceback': traceback,
            'expected_contract': good, 'fault_calls': calls})

    def encoded(ctx=context, value=book):
        return json.dumps([ctx, value], ensure_ascii=False).encode()

    observe('supports-html', args=['supports', 'html'], want=0)
    observe('supports-pdf', args=['supports', 'pdf'], want=1)
    observe('unsupported-arity', args=['unknown'], want=1)
    observe('valid-public-protocol', payload=encoded(), want=0,
            body=(json.dumps(expected, ensure_ascii=False) + '\n').encode())
    for name, payload in [('malformed-json', b'{'), ('invalid-utf8', b'\xff'),
                          ('invalid-shape', b'{}'), ('invalid-context', b'[null,{}]'),
                          ('invalid-renderer', encoded({**context, 'renderer': 'pdf'}))]:
        observe(name, payload=payload)
    for name, field, value in [('unsafe-chapter', 'path', '../escape.md'),
                              ('invalid-children', 'sub_items', 'bad'),
                              ('missing-record', 'content', '[Missing](tasks/NO-SUCH-TREE.md)')]:
        altered = copy.deepcopy(book)
        altered['items'][0]['Chapter'][field] = value
        observe(name, payload=encoded(value=altered))
    model = {**context, 'root': str(fixture / 'docs/models/lan9118-lab-v0')}
    altered = copy.deepcopy(book)
    altered['items'][0]['Chapter'].update(path='introduction.md', content=
        '[Missing](../../netboard-lab-v0/src/NO-SUCH-CHAPTER.md)')
    observe('missing-sibling', payload=encoded(model, altered))
    observe('actual-registry-open-failed', payload=encoded(model, altered), fault=True)
    for depth in [20, 1200]:
        node = '{"Chapter":{"path":null,"content":"","sub_items":['
        payload = ('[' + json.dumps(context) + ',{"items":[' + node * depth
                   + ']}}' * depth + ']}]').encode()
        body = (json.dumps(json.loads(payload)[1], ensure_ascii=False) + '\n').encode() if depth == 20 else b''
        observe('depth-' + str(depth), payload=payload, want=0 if depth == 20 else 2, body=body)
    return records


def consumer_omissions(source, output, books, captures, overlays):
    """Run mutated copies of the real public consumer on every captured book."""
    seams = [('task', 'if task:', 'if False: # LC0038 omitted task routing'),
             ('history', 'if source not in history:', 'if True: # LC0038 omitted history routing'),
             ('sibling', 'for unit in B.registered_units(root):',
              'for unit in []: # LC0038 omitted sibling routing')]
    records = []
    for name, old, new in seams:
        directory = output / ('omit-' + name)
        directory.mkdir()
        fixture, expected_copy = copy_fixture(source, directory, overlays)
        path = fixture / NAV
        code = path.read_bytes()
        require(code.count(old.encode()) == 1, 'unique actual navigation omission')
        changed = code.replace(old.encode(), new.encode(), 1)
        path.write_bytes(changed)
        observations = []
        for i, book in enumerate(books):
            context = {'root': str(fixture / book), 'renderer': 'html'}
            payload = json.dumps([context, captures[book]['before']], ensure_ascii=False).encode()
            result = subprocess.run([sys.executable, str(path)], input=payload,
                                    capture_output=True, check=False,
                                    env=environment(output / 'tmp'), timeout=60)
            (directory / f'{i}.stdout').write_bytes(result.stdout)
            (directory / f'{i}.stderr').write_bytes(result.stderr)
            require(result.returncode == 0 and b'Traceback' not in result.stderr,
                    'actual omission must execute successfully, not fail on syntax/input')
            actual = json.loads(result.stdout)
            expected = captures[book]['after']
            observations.append({'book': book, 'returncode': result.returncode,
                'stdout_bytes': len(result.stdout), 'stdout_sha256': C.digest(result.stdout),
                'stderr_sha256': C.digest(result.stderr), 'whole_expected_book': actual == expected})
        require(any(not r['whole_expected_book'] for r in observations),
                'actual consumer omission did not discriminate')
        require(path.read_bytes() == changed, 'actual omitted code identity changed')
        # Restore only this owned fixture copy, then authenticate its whole
        # original population/modes. The project source and index never move.
        path.write_bytes(code)
        B.verify_copy(expected_copy, fixture)
        records.append({'role': name, 'source_old': old, 'source_new': new,
            'mutated_code_sha256': C.digest(changed), 'observations': observations,
            'qualification_returncode': 1})
    return records


def nesting_catch_omission(source, output, overlays):
    """Remove the actual API catch and repeat the complete public input matrix."""
    directory = output / 'omit-nesting-catch'
    directory.mkdir()
    (directory / 'tmp').mkdir()
    fixture, expected = copy_fixture(source, directory, overlays)
    path = fixture / NAV
    code = path.read_bytes()
    old, new = b'except RecursionError as exc:', b'except ArithmeticError as exc:'
    require(code.count(old) == 1, 'unique repaired navigation nesting catch')
    changed = code.replace(old, new, 1)
    path.write_bytes(changed)
    observations = public_cases(fixture, directory)
    wrong = [r for r in observations if not r['expected_contract']]
    require(len(wrong) == 1 and wrong[0]['case'] == 'depth-1200'
            and wrong[0]['returncode'] == 1 and wrong[0]['traceback']
            and wrong[0]['stdout_bytes'] == 0,
            'actual nesting catch omission did not restore the measured defect')
    require(b'RecursionError' in (directory / 'public/depth-1200.stderr').read_bytes(),
            'omission failed for a different exception')
    require(path.read_bytes() == changed, 'omitted code changed during execution')
    path.write_bytes(code)
    B.verify_copy(expected, fixture)
    return {'source_old': old.decode(), 'source_new': new.decode(),
            'mutated_code_sha256': C.digest(changed), 'observations': observations,
            'qualification_returncode': 1}


def build_stage(fixture, output, books, stage):
    site = output / stage / 'site'
    captures, builds = {}, []
    for i, book in enumerate(books):
        env = environment(output / 'tmp')
        if stage != 'baseline':
            destination = output / stage / 'captures' / book / 'protocol.json'
            command = [sys.executable, str(Path(__file__).resolve()), '--capture',
                       '--fixture', fixture.relative_to(ROOT).as_posix(),
                       '--capture-output', destination.relative_to(ROOT).as_posix()]
            if stage == 'bare':
                command.append('--passthrough')
            prefix = 'MDBOOK_PREPROCESSOR__PROJECT_RECORD_LINKS__'
            env.update({prefix + 'COMMAND': shlex.join(command),
                        prefix + 'AFTER': '["links"]', prefix + 'BEFORE': '[]',
                        prefix + 'OPTIONAL': 'false', prefix + 'RENDERERS': '["html"]'})
        destination = site / book / 'book'
        result = subprocess.run(['mdbook', 'build', str(fixture / book), '-d', str(destination)],
                                capture_output=True, check=False, env=env, timeout=60)
        log = output / stage
        log.mkdir(parents=True, exist_ok=True)
        (log / f'build-{i}.stdout').write_bytes(result.stdout)
        (log / f'build-{i}.stderr').write_bytes(result.stderr)
        require(result.returncode == 0, 'public build refused: ' + book)
        builds.append({'book': book, 'returncode': result.returncode,
                       'stdout_sha256': C.digest(result.stdout),
                       'stderr_sha256': C.digest(result.stderr)})
        if stage != 'baseline':
            captures[book] = json.loads((output / stage / 'captures' / book / 'protocol.json').read_text())
    return {'files': B.file_set(site), 'captures': captures, 'builds': builds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    parser.add_argument('--addition', action='append', default=[])
    parser.add_argument('--require-clean', action='store_true')
    parser.add_argument('--working-code', action='store_true')
    parser.add_argument('--capture', action='store_true')
    parser.add_argument('--fixture')
    parser.add_argument('--capture-output')
    parser.add_argument('--passthrough', action='store_true')
    parser.add_argument('action', nargs='?')
    parser.add_argument('renderer', nargs='?')
    args = parser.parse_args()
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    try:
        if args.capture:
            require(args.fixture is not None and args.fixture.startswith('target/'),
                    'owned capture fixture required')
            C.Q.relative_path(args.fixture)
            require(args.action is not None or args.capture_output is not None,
                    'capture output required')
            return capture(args)
        require(not any([args.action, args.renderer, args.fixture, args.capture_output, args.passthrough]),
                'capture arguments require --capture')
        require(args.output is not None, '--output is required')
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'on-volume target output required')
        output = C.U.source_path(ROOT, args.output)
        require(not output.exists(), 'fresh output required')
        before = C.working_snapshot(args.addition)
        source = C.source_census(SOURCE)
        require(len(source['members']) == 1459, 'whole immutable source population')
        overlays, code_inputs = {}, []
        if args.working_code:
            members_by_path = {r['path']: r for r in source['members']}
            for name in [NAV, PROBE]:
                pin = before['members'][name]
                original = members_by_path[name]
                require(pin['mode'] == int(original['mode'][-3:], 8),
                        'working navigation code mode differs')
                body = (ROOT / name).read_bytes()
                require(C.digest(body) == pin['sha256'] and len(body) == pin['bytes'],
                        'working navigation code changed during read')
                overlays[name] = body
                code_inputs.append({'path': name, 'source_oid': original['oid'], **pin})
        output.mkdir(parents=True)
        (output / 'tmp').mkdir()
        fixture, expected_copy = copy_fixture(source, output, overlays)
        units = C.U.registered_units(fixture)
        require(not C.U.catalogue_findings(fixture, units), 'source catalogue differs')
        books = ['docs/book', *[u['book'].rstrip('/') for u in units]]
        require(len(books) == 7 and len(set(books)) == 7, 'seven distinct source books')
        stages = {name: build_stage(fixture, output, books, name)
                  for name in ['baseline', 'captured', 'bare']}
        require(stages['baseline']['files'] == stages['captured']['files'],
                'capture wrapper changed complete output population/bytes')
        for book in books:
            actual, bare = stages['captured']['captures'][book], stages['bare']['captures'][book]
            require(actual['root'] == bare['root'] == book and actual['returncode'] == 0,
                    'actual public consumer identity/verdict differs')
            require(actual['before'] == bare['before'] == bare['after'],
                    'complete pre-navigation protocol differs')
        members = {r['path'] for r in source['members'] if r['mode'] != '160000'}
        registry = next(r for r in source['members'] if r['path'] == 'materials/units.sexp')
        registry_read = {k: registry[k] for k in ['path', 'bytes', 'sha256']}
        for book in books:
            reads = stages['captured']['captures'][book]['reads']
            require(reads == [registry_read] * len(reads)
                    and (not reads if book == 'docs/book' else bool(reads)),
                    'complete actual canonical registry data reads differ')
        chapters, mappings, counts = source_protocols(books, stages['captured']['captures'], members)
        rendered = rendered_oracle(output, books, stages, mappings, counts)
        observations = public_cases(fixture, output)
        omissions = consumer_omissions(source, output, books, stages['captured']['captures'], overlays)
        refusal_omission = (nesting_catch_omission(source, output, overlays)
                            if args.working_code else None)
        component = subprocess.run([sys.executable, str(fixture / PROBE)],
                                   capture_output=True, check=False,
                                   env=environment(output / 'tmp'), timeout=60)
        (output / 'component.stdout').write_bytes(component.stdout)
        (output / 'component.stderr').write_bytes(component.stderr)
        tests = 27 if args.working_code else 26
        require(component.returncode == 0 and f'Ran {tests} tests'.encode() in component.stderr,
                'navigation component controls did not pass')
        B.verify_copy(expected_copy, fixture)
        require(before == C.working_snapshot(args.addition), 'actual source/index/modes changed')
        result = {'source': SOURCE, 'source_members': 1459, 'source_tree_sha256': source['tree_sha256'],
                  'mode': 'optimized' if sys.flags.optimize else 'normal',
                  'books': books, 'stages': stages, 'chapters': chapters,
                  'rendered': rendered, 'observations': observations, 'actual_omissions': omissions,
                  'component': {'returncode': component.returncode, 'tests': tests,
                                'stderr_sha256': C.digest(component.stderr)},
                  'source_defects': sum(not r['expected_contract'] for r in observations)}
        if args.working_code:
            result.update(code_mode='working', code_inputs=code_inputs,
                          refusal_omission=refusal_omission)
        write_json(output / 'result.json', result)
        print(json.dumps({'source': SOURCE, 'books': len(books),
                          'files': len(stages['baseline']['files']), 'capture_unchanged': True,
                          'chapters': len(chapters), 'source_rewrites': sum(len(r['edits']) for r in chapters),
                          'rendered_rewrites': len(rendered['routes']), 'hyperlinks': rendered['hyperlinks'],
                          'observations': len(observations), 'source_defects': result['source_defects'],
                          'actual_omissions': len(omissions), 'original_controls': 26}))
        return 1 if args.require_clean and result['source_defects'] else 0
    except (ValueError, OSError, UnicodeError, TypeError, RecursionError,
            subprocess.SubprocessError, KeyError) as exc:
        print('qualify_book_navigation: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
