#!/usr/bin/env python3
"""Actual LC0044 delivery/observation controls, including failures with journals."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import trace_book_dependencies as D

PRODUCER = 'scripts/probe_book_dependency_trace.py'
require = D.require


def journal_check(output, result):
    for index, rows in enumerate(result['http']):
        saved = [json.loads(line) for line in (output / ('server-' + str(index)) / 'http.jsonl').read_text().splitlines()]
        require(saved == rows and [row['sequence'] for row in rows] == list(range(len(rows))),
                'complete streamed journal differs')
        require(rows[-1]['event'] == 'closed' and rows[-1]['input_unchanged'] is True,
                'journal did not survive through cleanup')
        received = {row['sequence']: row for row in rows if row['event'] == 'received'}
        responses, written = {}, {}
        for row in rows:
            if row['event'] not in {'response', 'written'}:
                continue
            request = row['request_id']
            require(request in received and row['path'] == received[request]['path'],
                    'journal request linkage differs')
            group = responses if row['event'] == 'response' else written
            require(request not in group, 'duplicate delivery leg')
            group[request] = row
        require(set(received) == set(responses) == set(written), 'complete delivery membership differs')
        for request, row in written.items():
            require(row['status'] == responses[request]['status']
                    and row['bytes'] == responses[request]['served_bytes'], 'delivery byte/status legs differ')
    streamed = [json.loads(line)['case'] for line in (output / 'observations.jsonl').read_text().splitlines()]
    require(sorted(streamed, key=lambda row: (row['server'], row['index'])) == result['observations'],
            'complete observation stream differs')


def original_failed_witness():
    R = D.R
    value = R.decode_capture(R.record_frame(R.RECORD))
    base = next(row['observation']['browser'] for row in value['normal']['fixed']['observations']
                if row['observation']['path'] == 'docs/book/book/print.html')
    text = (D.ROOT / R.RECORD).read_text().split('### D79 complete failed browser witness\n', 1)[1]
    import re
    match = re.search(r'^```json\n(.*?)\n```$', text, re.M | re.S)
    require(match is not None, 'original D79 witness descriptor missing')
    row = R.H.json_object(match[1].encode())
    require(D.Q.fingerprint(base) == row['base_fingerprint'], 'original D79 witness predecessor differs')
    bad = D.Q.apply_changes(base, row['witness_changes'])
    require(D.Q.fingerprint(bad) == row['witness_fingerprint'], 'original complete D79 witness differs')
    return bad


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        D.C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'owned probe output required')
        output = D.C.U.source_path(D.ROOT, args.output)
        require(not output.exists(), 'fresh dependency probe output required')
        before = D.C.working_snapshot([D.PRODUCER, PRODUCER])
        output.mkdir()
        program, compiler = D.Q.compile_webkit(output)
        _, _, site, cases, inputs = D.prepare(output)
        selected = [case for case in cases if case['path'] == 'docs/book/book/print.html']
        require(len(selected) == 1, 'unique real print case')
        for label, arguments in [('bool-server', {'servers': True, 'jobs': 1}),
                                 ('bool-job', {'servers': 1, 'jobs': True})]:
            path = output / label
            try:
                D.run_profile(program, site, selected, path, backlog=128, fault='none', **arguments)
            except ValueError:
                require(not path.exists(), 'invalid concurrency wrote output')
            else:
                raise ValueError('boolean concurrency accepted')
        try:
            D.owned_target(D.ROOT / 'docs/book')
        except ValueError:
            pass
        else:
            raise ValueError('non-target mutation boundary accepted')
        results = {}
        for fault in ['none', 'missing-mark', 'empty-mark', 'missing-mark-and-book']:
            path = output / ('control-' + fault)
            result = D.run_profile(program, site, selected, path, servers=1, jobs=1, backlog=128, fault=fault)
            journal_check(path, result)
            row = result['observations'][0]
            require(not row.get('unjudgeable'), 'actual fault lost its full forensic observation')
            errors = [event for event in row['forensics']['events'] if event['kind'] != 'resource-load']
            resources = [event for event in errors if event['kind'] == 'resource-error']
            if fault == 'none':
                require(row['qualification_returncode'] == 0 and not errors
                        and row['forensics']['globals']['Mark'] == 'function', 'positive control failed')
            else:
                require(row['qualification_returncode'] == 2 and row['forensics']['globals']['Mark'] == 'undefined'
                        and row['witness']['errors'][0]['message'] == "ReferenceError: Can't find variable: Mark",
                        'actual Mark failure accepted or lost')
                require(len(resources) == {'missing-mark': 1, 'empty-mark': 0,
                                          'missing-mark-and-book': 2}[fault], 'delivery/semantic errors conflated')
            if fault == 'missing-mark-and-book':
                require(row['witness'] == original_failed_witness() and all(value == 0 for value in row['enhancements'].values()),
                        'complete original failed witness/enhancements not reproduced')
            elif fault != 'none':
                require(row['enhancements']['clip_buttons'] == 97 and row['enhancements']['hljs_classes'] == 1917,
                        'Mark-only fault incorrectly removes book enhancements')
            results[fault] = result
        # Actual observer omission: Window cannot capture descendant load events.
        original = D.FORENSICS
        old = "document.addEventListener('load', e => {"
        require(original.count(old) == 1, 'unique actual load-observer omission')
        try:
            D.FORENSICS = original.replace(old, "window.addEventListener('load', e => {", 1)
            path = output / 'omit-document-load'
            result = D.run_profile(program, site, selected, path, servers=1, jobs=1, backlog=128, fault='none')
            journal_check(path, result)
            row = result['observations'][0]
            require(row.get('unjudgeable') is True and 'declared script outcomes missing' in row['qualification_reason'],
                    'actual load-observer omission falsely accepted')
            results['omit-document-load'] = result
        finally:
            D.FORENSICS = original
        path = output / 'missing-native'
        result = D.run_profile(output / 'not-a-program', site, selected, path,
                               servers=1, jobs=1, backlog=128, fault='none')
        journal_check(path, result)
        require(result['observations'][0].get('unjudgeable') is True, 'native launch failure accepted')
        results['missing-native'] = result
        require(D.C.working_snapshot([D.PRODUCER, PRODUCER]) == before, 'probe changed actual source/index/modes')
        D.N.write_json(output / 'result.json', {'mode': 'optimized' if sys.flags.optimize else 'normal',
            'producer': D.C.file_identity(PRODUCER), 'trace_producer': D.C.file_identity(D.PRODUCER),
            'compiler': compiler, 'inputs': inputs, 'controls': results})
        print(json.dumps({'controls': len(results), 'failures': 0,
                          'original_failed_witness_reproduced': True, 'journals_survive_refusal': True}))
        return 0
    except (ValueError, OSError, D.subprocess.SubprocessError) as exc:
        print('DEPENDENCY-PROBE: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
