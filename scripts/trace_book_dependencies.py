#!/usr/bin/env python3
"""Trace LC0044 dependency delivery independently of successful qualification.

Fresh target output, public source-pinned builds and nonpersistent OS WebKit.
Measurement0 is not a clean verdict; --require-clean fails1 for observed faults.
Unavailable inputs/native or malformed observations refuse2, retaining forensics.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import http.server
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from urllib.parse import quote, unquote, urljoin, urlsplit

import qualify_heading_repair as R

C, Q, B, N, T = R.C, R.Q, R.B, R.N, R.T
ROOT = C.ROOT
SOURCE = 'f3c5e81e519ac8c69215cfb2d4797f10de33c4ff'
REPRODUCTION = R.SOURCE
PRODUCER = 'scripts/trace_book_dependencies.py'
FORENSICS_ID = 'semulith-dependency-forensics'
MIME = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript',
        '.json': 'application/json', '.css': 'text/css', '.svg': 'image/svg+xml',
        '.woff2': 'font/woff2', '.png': 'image/png', '.ico': 'image/x-icon'}
require = C.require

# Resource errors are separate from ErrorEvent: preserve both, with their targets.
FORENSICS = r'''<script id="semulith-dependency-observer">
(() => {
    const events = [];
    const node = document.createElement('script');
    node.id = 'semulith-dependency-forensics'; node.type = 'application/json';
    document.head.appendChild(node);
    function finite(value) { return typeof value === 'number' && Number.isFinite(value) ? value : null; }
    function snapshot() {
        const resources = performance.getEntriesByType('resource').map(e => ({
            name: e.name, type: e.initiatorType, status: finite(e.responseStatus),
            transfer: finite(e.transferSize), encoded: finite(e.encodedBodySize),
            decoded: finite(e.decodedBodySize), start: finite(e.startTime), duration: finite(e.duration)
        }));
        node.textContent = JSON.stringify({ready: document.readyState === 'complete', base_uri: document.baseURI, events: events,
            globals: {Mark: typeof Mark, elasticlunr: typeof elasticlunr, hljs: typeof hljs,
                      ClipboardJS: typeof ClipboardJS, define: typeof define,
                      module: typeof module, exports: typeof exports}, resources: resources});
    }
    window.addEventListener('error', e => {
        events.push({kind: e instanceof ErrorEvent ? 'javascript-error' : 'resource-error',
            target: e.target.tagName || '', source: e.target.src || e.target.href || '',
            message: e.message || '', file: e.filename || '', line: e.lineno || 0, column: e.colno || 0});
        snapshot();
    }, true);
    // Document is the capture ancestor for resource loads; load does not reach Window.
    document.addEventListener('load', e => {
        if (e.target.tagName) events.push({kind: 'resource-load', target: e.target.tagName,
                                         source: e.target.src || e.target.href || ''});
        snapshot();
    }, true);
    window.addEventListener('load', snapshot);
    window.addEventListener('unhandledrejection', e => {
        events.push({kind: 'promise-rejection', message: String(e.reason)}); snapshot();
    });
    snapshot();
})();
</script>'''


class Journal:
    """Every event reaches disk before returning to the producer, including errors."""
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.rows = []
        self.path.write_bytes(b'')

    def append(self, **value):
        with self.lock:
            row = {'sequence': len(self.rows), **value}
            body = Q.canonical(row) + b'\n'
            with self.path.open('ab') as stream:
                stream.write(body)
            self.rows.append(row)
            return row['sequence']


def owned_target(path):
    relative = path.relative_to(ROOT).as_posix()
    C.Q.relative_path(relative)
    require(relative.startswith('target/') and C.U.source_path(ROOT, relative) == path,
            'owned same-volume target path required')


@contextlib.contextmanager
def serve(site, cases, output, *, backlog, fault):
    owned_target(site)
    owned_target(output)
    require(type(backlog) is int and backlog in {5, 32, 128} and isinstance(fault, str)
            and fault in {'none', 'missing-mark', 'empty-mark', 'missing-mark-and-book'},
            'unsupported bounded dependency profile')
    output.mkdir()
    manifest = B.file_set(site)
    pages = {case['path'] for case in cases}
    mark = [name for name in manifest if name.startswith('docs/book/book/mark-') and name.endswith('.js')]
    book = [name for name in manifest if name.startswith('docs/book/book/book-') and name.endswith('.js')]
    require(len(mark) == len(book) == 1, 'unique original Mark/book assets required')
    journal = Journal(output / 'http.jsonl')

    class Handler(http.server.BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            # Bound pre-opened connections so shutdown can join every handler.
            self.connection.settimeout(5)

        def do_GET(self):
            name = unquote(urlsplit(self.path).path).lstrip('/')
            request_id = journal.append(event='received', path=name,
                referrer_path=unquote(urlsplit(self.headers.get('Referer', '')).path).lstrip('/'))
            denied = (fault in {'missing-mark', 'missing-mark-and-book'} and name == mark[0]
                      or fault == 'missing-mark-and-book' and name == book[0])
            if name not in manifest or denied:
                body, status = b'owned dependency trace: unavailable\n', 404
                original_sha = None
            else:
                body = (site / name).read_bytes()
                original_sha = C.digest(body)
                if original_sha != manifest[name]:
                    journal.append(event='input-changed', path=name, request_id=request_id)
                    body, status = b'owned dependency trace: changed input\n', 503
                else:
                    status = 200
                    if name in pages:
                        require(body.count(b'<head>') == 1 and Q.WITNESS.encode() not in body
                                and FORENSICS_ID.encode() not in body, 'unsupported observer insertion')
                        body = body.replace(b'<head>', b'<head>' + Q.OBSERVER.encode() + FORENSICS.encode(), 1)
                    elif fault == 'empty-mark' and name == mark[0]:
                        body = b'; // actual owned empty-Mark response\n'
            journal.append(event='response', path=name, request_id=request_id, status=status, original_sha256=original_sha,
                           served_bytes=len(body), served_sha256=C.digest(body), fault=fault)
            try:
                self.send_response(status)
                self.send_header('Content-Type', MIME.get(Path(name).suffix, 'application/octet-stream'))
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
                journal.append(event='written', path=name, request_id=request_id, status=status, bytes=len(body))
            except OSError as exc:
                journal.append(event='write-failed', path=name, request_id=request_id,
                               error=type(exc).__name__, message=str(exc))

        def log_message(self, *unused):
            pass

    class Server(http.server.ThreadingHTTPServer):
        request_queue_size = backlog
        daemon_threads = False
        block_on_close = True

        def handle_error(self, request, address):
            error = sys.exception()
            journal.append(event='handler-failed', error=type(error).__name__, message=str(error))

    server = Server(('127.0.0.1', 0), Handler)
    worker = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': .1}, daemon=True)
    worker.start()
    try:
        yield 'http://127.0.0.1:' + str(server.server_port), journal
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=10)
        require(not worker.is_alive(), 'dependency server did not terminate')
        require(B.file_set(site) == manifest, 'dependency tracing changed original bundle')
        journal.append(event='closed', input_unchanged=True)


def node_json(document, identifier):
    found = [node for node in Q.elements(document.root) if node.attribute('id') == identifier]
    require(len(found) == 1 and found[0].tag == 'script'
            and found[0].attribute('type') == 'application/json', 'dependency witness unavailable')
    return json.loads(Q.text_content(found[0].children))


def inspect(case, dom):
    document = Q.Document(dom)
    witness = node_json(document, Q.WITNESS)
    forensics = node_json(document, FORENSICS_ID)
    require(isinstance(witness, dict) and set(witness) == {'ready', 'errors', 'headers', 'navigation',
            'regions', 'active', 'bindings', 'title'}, 'unsupported dependency witness fields')
    require(witness['headers'] == document.headers() and witness['navigation'] == document.navigation()[1]
            and witness['bindings'] == document.bindings() and witness['title'] == document.title(),
            'independent complete dependency DOM readers differ')
    require(isinstance(forensics, dict) and set(forensics) == {'ready', 'base_uri', 'events', 'globals', 'resources'}
            and forensics['ready'] is True, 'unsupported or incomplete dependency forensic fields')
    require(unquote(urlsplit(forensics['base_uri']).path).lstrip('/') == case['document_base_path'],
            'independent static/browser document bases differ')
    outcomes = {unquote(urlsplit(event['source']).path).lstrip('/') for event in forensics['events']
                if event['kind'] in {'resource-load', 'resource-error'} and event['target'] == 'SCRIPT'}
    require(set(case['script_sources']) <= outcomes, 'declared script outcomes missing from dependency trace')
    try:
        assessment = Q.assess(case, dom)
    except ValueError as exc:
        verdict, reason, assessment = 2, str(exc), None
    else:
        verdict = 0 if assessment['expected_contract'] else 1
        reason = ''
    nodes = list(Q.elements(document.root))
    return {'path': case['path'], 'qualification_returncode': verdict, 'qualification_reason': reason,
            'witness': witness, 'forensics': forensics, 'assessment': assessment,
            'enhancements': {'hljs_classes': sum(node.has_class('hljs') for node in nodes),
                             'hljs_spans': sum(node.tag == 'span' and 'hljs' in
                                               (node.attribute('class') or '') for node in nodes),
                             'clip_buttons': sum(node.has_class('clip-button') for node in nodes)}}


def execute(program, base, case, output):
    try:
        dom, process = Q.browser_run(program, output, base + '/' + quote(case['path'], safe='/'))
        value = inspect(case, dom)
        value['process'] = process
        return value
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        return {'path': case['path'], 'qualification_returncode': 2,
                'qualification_reason': str(exc), 'unjudgeable': True,
                'diagnostics': {name: {'bytes': (output / name).stat().st_size,
                                      'sha256': C.digest((output / name).read_bytes())}
                                for name in ['dom.html', 'stderr.log'] if (output / name).is_file()}}


def run_profile(program, site, cases, output, *, servers, jobs, backlog, fault):
    owned_target(output)
    require(type(servers) is int and type(jobs) is int and servers in {1, 2}
            and jobs in {1, 2, 4} and servers * jobs <= 4,
            'bounded dependency concurrency required')
    output.mkdir()
    # Journals and partial page records survive every qualification/native failure.
    rows, journals = [], []
    observations = Journal(output / 'observations.jsonl')
    active, peak, concurrency_lock = [0] * servers, [0] * servers, threading.Lock()
    with contextlib.ExitStack() as stack:
        origins = []
        for server in range(servers):
            base, journal = stack.enter_context(serve(site, cases, output / ('server-' + str(server)),
                                                    backlog=backlog, fault=fault))
            origins.append(base)
            journals.append(journal)
        tasks = [(server, index, case) for index, case in enumerate(cases) for server in range(servers)]
        def call(item):
            server, index, case = item
            with concurrency_lock:
                active[server] += 1
                peak[server] = max(peak[server], active[server])
            try:
                return {'server': server, 'index': index, **execute(program, origins[server], case,
                        output / ('browser-' + str(server)) / ('page-' + str(index).zfill(3)))}
            finally:
                with concurrency_lock:
                    active[server] -= 1
        pools = [stack.enter_context(concurrent.futures.ThreadPoolExecutor(max_workers=jobs))
                 for _ in range(servers)]
        futures = [pools[item[0]].submit(call, item) for item in tasks]
        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            rows.append(row)
            observations.append(event='observed', case=row)
    rows.sort(key=lambda row: (row['server'], row['index']))
    require(active == [0] * servers and all(value <= jobs for value in peak), 'dependency concurrency exceeded')
    value = {'servers': servers, 'jobs_per_server': jobs, 'backlog': backlog, 'fault': fault,
             'max_active_per_server': peak, 'observations': rows, 'http': [journal.rows for journal in journals]}
    N.write_json(output / 'result.json', value)
    return value


def script_inputs(site, cases, manifest):
    """Independent static declaration set; trace must preserve load/error outcomes."""
    result = []
    for case in cases:
        document = Q.Document((site / case['path']).read_bytes())
        bases = [node.attribute('href') for node in Q.elements(document.root)
                 if node.tag == 'base' and node.attribute('href') is not None]
        location = 'http://owned.invalid/' + case['path']
        base = urljoin(location, bases[0]) if bases else location
        require(urlsplit(base).scheme == 'http' and urlsplit(base).netloc == 'owned.invalid',
                'unsupported external document base')
        declared = []
        for node in Q.elements(document.root):
            if node.tag != 'script' or not node.attribute('src'):
                continue
            url = urlsplit(urljoin(base, node.attribute('src')))
            require(url.scheme == 'http' and url.netloc == 'owned.invalid', 'unsupported external script declaration')
            name = unquote(url.path).lstrip('/')
            declared.append(name)
        result.append({**case, 'document_base_path': unquote(urlsplit(base).path).lstrip('/'),
                       'script_sources': declared,
                       'unavailable_script_declarations': [name for name in declared if name not in manifest]})
    return result


def prepare(output):
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    current = C.source_census(SOURCE)
    require(len(current['members']) == 1485, 'whole dependency owner source differs')
    members = {row['path']: row for row in current['members']}
    helpers = ['scripts/qualify_heading_repair.py', 'scripts/qualify_book_headings.py',
               'scripts/book_headings_webkit.swift', 'scripts/collect_containment_graph.py',
               'scripts/qualify_book_includes.py', 'scripts/qualify_book_navigation.py',
               'scripts/qualify_book_toc.py', 'scripts/unit_books.py',
               'scripts/book_navigation.py', 'scripts/book_includes.py']
    for name in helpers:
        row = members[name]
        require(C.file_identity(name) == {'bytes': row['bytes'], 'sha256': row['sha256'],
                                        'mode': int(row['mode'][-3:], 8)}, 'unreviewed dependency helper: ' + name)
    source, original_members = R.source_inputs()
    fixture, baseline_site, baseline_stage, original_cases, pins = Q.prepare(source, original_members, output)
    products, config = R.product_inputs()
    for name, body in [(R.CONFIG, config), (R.SCRIPT, (ROOT / R.SCRIPT).read_bytes())]:
        path = fixture / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        path.chmod(products[name]['mode'])
    books = [row['book'] for row in baseline_stage['builds']]
    site, stage = R.build(fixture, output / 'fixed', books)
    cases = R.recase(site, original_cases)
    retained = R.decode_capture(R.record_frame(R.RECORD))
    require(stage['files'] == retained['normal']['fixed']['stage']['files'],
            'whole original345-file reproduction manifest differs')
    require(len(cases) == 120 and len(stage['files']) == 345, 'complete dependency page/output population differs')
    original_cases = script_inputs(baseline_site, original_cases, baseline_stage['files'])
    cases = script_inputs(site, cases, stage['files'])
    return baseline_site, original_cases, site, cases, {'owner_source': SOURCE, 'owner_members': len(current['members']),
        'owner_tree_sha256': current['tree_sha256'], 'reproduction_source': REPRODUCTION,
        'reproduction_members': len(source['members']), 'reproduction_tree_sha256': source['tree_sha256'],
        'inputs': pins, 'products': products, 'helpers': [members[name] for name in helpers], 'stage': stage}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--servers', type=int, choices=[1, 2], default=2)
    parser.add_argument('--jobs', type=int, choices=[1, 2, 4], default=2)
    parser.add_argument('--backlog', type=int, choices=[5, 32, 128], default=5)
    parser.add_argument('--pages', choices=['all', 'print'], default='all')
    parser.add_argument('--fault', choices=['none', 'missing-mark', 'empty-mark', 'missing-mark-and-book'], default='none')
    parser.add_argument('--warmup', action='store_true', help='execute original source pages before fixed pages')
    parser.add_argument('--require-clean', action='store_true')
    args = parser.parse_args()
    try:
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'owned target dependency output required')
        output = C.U.source_path(ROOT, args.output)
        require(not output.exists(), 'fresh dependency output required')
        before = C.working_snapshot([PRODUCER])
        output.mkdir()
        program, compiler = Q.compile_webkit(output)
        mdbook = R.mdbook_version(program.parent / 'tmp')
        engine = Q.browser_identity(program)
        calibration = Q.calibrate(program, output)
        baseline_site, original_cases, site, cases, inputs = prepare(output)
        if args.pages == 'print':
            cases = [case for case in cases if case['path'] == 'docs/book/book/print.html']
            original_cases = [case for case in original_cases if case['path'] == 'docs/book/book/print.html']
        warmup = run_profile(program, baseline_site, original_cases, output / 'warmup', servers=args.servers,
                             jobs=args.jobs, backlog=args.backlog, fault='none') if args.warmup else None
        result = run_profile(program, site, cases, output / 'profile', servers=args.servers,
                             jobs=args.jobs, backlog=args.backlog, fault=args.fault)
        require(Q.browser_identity(program) == engine and R.mdbook_version(program.parent / 'tmp') == mdbook,
                'dependency toolchain changed during trace')
        require(C.working_snapshot([PRODUCER]) == before, 'actual source/index/modes changed during trace')
        N.write_json(output / 'working-before.json', before)
        N.write_json(output / 'working-after.json', before)
        bad = sum(row['qualification_returncode'] != 0 or any(event['kind'] != 'resource-load'
                  for event in row.get('forensics', {}).get('events', [])) for row in result['observations'])
        http_failures = sum(row['event'] in {'input-changed', 'write-failed', 'handler-failed'}
                            or row['event'] == 'response' and row['status'] != 200
                            for rows in result['http'] for row in rows)
        unjudgeable = sum(row.get('unjudgeable', False) for row in result['observations'])
        value = {'mode': 'optimized' if sys.flags.optimize else 'normal', 'inputs': inputs,
                 'producer': C.file_identity(PRODUCER), 'python': sys.version,
                 'installed_default_backlog': http.server.ThreadingHTTPServer.request_queue_size,
                 'engine': engine, 'compiler': compiler, 'mdbook': mdbook,
                 'calibration': calibration, 'warmup': warmup, 'profile': result,
                 'bad_observations': bad, 'http_failures': http_failures, 'unjudgeable': unjudgeable}
        N.write_json(output / 'result.json', value)
        print(json.dumps({'pages': len(result['observations']), 'bad': bad,
                          'servers': args.servers, 'jobs': args.jobs, 'backlog': args.backlog,
                          'fault': args.fault, 'http_events': sum(len(rows) for rows in result['http']),
                          'http_failures': http_failures, 'unjudgeable': unjudgeable}))
        return 2 if unjudgeable else 1 if args.require_clean and (bad or http_failures) else 0
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print('DEPENDENCY-TRACE: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
