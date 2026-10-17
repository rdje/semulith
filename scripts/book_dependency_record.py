#!/usr/bin/env python3
"""Authenticate the finite LC0044 verdict/delivery ledger and retained failures.

The ledger restores every selected heading witness from the pinned LC0043 base.
Raw ordered HTTP/resource timing/DOM streams remain generated diagnostics.
Queries require the pinned Git objects/producers; lazy fetch is disabled.
"""
from __future__ import annotations
import argparse
import base64
from collections import Counter
import json
import lzma
import os
import re
import sys
import trace_book_dependencies as D
R, Q, C = D.R, D.Q, D.C
ROOT = C.ROOT
SOURCE = D.SOURCE
RECORD = 'docs/tasks/artifacts/live-containment/reader-records-retention.md'
MARKER = '## Dependency trace evidence — LC0044\n'
PRODUCER = 'scripts/book_dependency_record.py'
require = C.require


def witness_bases():
    value = R.decode_capture(R.record_frame(R.RECORD))
    return {
        role: {row['observation']['path']: row['observation']['browser']
               for row in value['normal'][role]['observations']}
        for role in ['baseline', 'fixed']
    }


def fp(value):
    return Q.fingerprint(value)


def project_profile(value, role, bases):
    """Keep all verdicts/witnesses/script outcomes and complete delivery footprints.

    Per-resource timings, non-script successful load order and ordered HTTP rows
    are generated diagnostics. Whole-profile fingerprints still identify them.
    """
    observations = []
    for row in value['observations']:
        if 'forensics' not in row:
            observations.append(dict(row))
            continue
        forensic = row['forensics']
        origin = D.urlsplit(forensic['base_uri'])
        prefix = origin.scheme + '://' + origin.netloc
        errors = [event for event in forensic['events'] if event['kind'] != 'resource-load']
        errors = [
            {key: item.removeprefix(prefix) if isinstance(item, str) and key in ['source', 'file'] else item
             for key, item in event.items()}
            for event in errors
        ]
        loads = [
            D.unquote(D.urlsplit(event['source']).path).lstrip('/')
            for event in forensic['events']
            if event['kind'] == 'resource-load' and event['target'] == 'SCRIPT' and event['source']
        ]
        assessment = row.get('assessment')
        observations.append({
            'path': row['path'], 'index': row['index'], 'server': row['server'],
            'qrc': row['qualification_returncode'], 'reason': row['qualification_reason'],
            'checks': assessment['checks'] if assessment else None,
            'witness_delta': list(D.T.metadata_changes(bases[role][row['path']], row['witness'])),
            'witness_fingerprint': fp(row['witness']), 'globals': forensic['globals'],
            'errors': errors, 'script_loads': loads, 'enhancements': row['enhancements'],
            'resource_timing_count': len(forensic['resources']), 'event_count': len(forensic['events']),
        })
    ledgers = []
    for rows in value['http']:
        counts, failed = Counter(), []
        for row in rows:
            event = row['event']
            if event == 'received':
                counts[(row['path'], event, 0, 0)] += 1
            elif event == 'response':
                counts[(row['path'], event, row['status'], row['served_bytes'])] += 1
            elif event == 'written':
                counts[(row['path'], event, row['status'], row['bytes'])] += 1
            elif event != 'closed':
                failed.append(row)
        ledgers.append({
            'events': len(rows), **fp(rows), 'closed': rows[-1],
            'footprint': [[*key, count] for key, count in sorted(counts.items())], 'failures': failed,
        })
    return {
        'raw_profile_fingerprint': fp(value), 'servers': value['servers'],
        'jobs': value['jobs_per_server'], 'backlog': value['backlog'], 'fault': value['fault'],
        'max_active': value['max_active_per_server'], 'observations': observations, 'http': ledgers,
    }


def validate(value):
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    require(isinstance(value, dict) and set(value) == {'runs', 'probes', 'failure', 'packet_access',
            'tcp_statistics', 'producer_sources', 'book_seams', 'task_seams'}, 'unreviewed dependency evidence fields')
    source = C.source_census(SOURCE)
    require(len(source['members']) == 1485, 'dependency evidence source population differs')
    bases = witness_bases()
    require(len(bases['baseline']) == len(bases['fixed']) == 120, 'dependency witness base population differs')
    require(set(value['runs']) == {'normal-queue32', 'optimized-queue32', 'normal-queue5', 'optimized-queue5'},
            'complete dependency comparison membership differs')
    producers = {}
    for row in value['producer_sources']:
        body = row['text'].encode()
        require(type(row['bytes']) is int and 0 < row['bytes'] <= 65536
                and len(body) == row['bytes'] and C.digest(body) == row['sha256'], 'execution producer bytes differ')
        require(row['sha256'] not in producers, 'duplicate execution producer')
        producers[row['sha256']] = row
    for name, run in value['runs'].items():
        require(run['mode'] == ('optimized' if name.startswith('optimized') else 'normal')
                and run['inputs']['owner_source'] == SOURCE
                and run['inputs']['owner_members'] == 1485
                and run['inputs']['owner_tree_sha256'] == source['tree_sha256']
                and run['inputs']['reproduction_source'] == R.SOURCE, 'dependency run source/mode differs')
        require(run['producer']['sha256'] in producers
                and run['producer']['bytes'] == producers[run['producer']['sha256']]['bytes'],
                'actual execution producer unavailable')
        for key, role in [('warmup', 'baseline'), ('profile', 'fixed')]:
            profile = run[key]
            require(type(profile['servers']) is int and type(profile['jobs']) is int
                    and type(profile['backlog']) is int and profile['servers'] == 1 and profile['jobs'] == 2
                    and profile['backlog'] == (32 if name.endswith('queue32') else 5)
                    and profile['max_active'] == [2], 'bounded comparison profile differs')
            rows = profile['observations']
            require([row['path'] for row in rows] == sorted(bases[role])
                    and [row['index'] for row in rows] == list(range(120)), 'complete ordered case ledger differs')
            for row in rows:
                require(type(row['qrc']) is int and row['qrc'] in {0, 1, 2}
                        and type(row['index']) is int and type(row['server']) is int,
                        'invalid qualification verdict/index type')
                witness = Q.apply_changes(bases[role][row['path']], row['witness_delta'])
                require(fp(witness) == row['witness_fingerprint'], 'whole restored browser witness differs')
            require(len(profile['http']) == 1, 'complete server ledger differs')
            for ledger in profile['http']:
                require(ledger['closed']['event'] == 'closed' and ledger['closed']['input_unchanged'] is True,
                        'delivery ledger did not close with exact inputs')
                keys = [tuple(row[:4]) for row in ledger['footprint']]
                require(keys == sorted(set(keys)) and all(type(row[4]) is int and row[4] > 0
                        for row in ledger['footprint']), 'delivery footprint ordering/count differs')
                require(sum(row[4] for row in ledger['footprint']) + len(ledger['failures']) + 1 == ledger['events'],
                        'complete delivery event count differs')
    require(set(value['probes']) == {'normal', 'optimized'}, 'both permanent probe modes required')
    for mode, probe in value['probes'].items():
        require(probe['mode'] == mode and len(probe['controls']) == 6, 'complete permanent controls differ')
        for key in ['producer', 'trace_producer']:
            require(probe[key]['sha256'] in producers
                    and probe[key]['bytes'] == producers[probe[key]['sha256']]['bytes'],
                    'permanent probe execution producer unavailable')
    failure = value['failure']
    require(failure['observation']['path'] == 'docs/book/book/annex/assembler.html'
            and len([event for event in failure['observation']['forensics']['events']
                     if event['kind'] == 'resource-error']) == 10,
            'complete pre-receipt failure observation differs')
    require(value['packet_access']['returncode'] == 1 and value['packet_access']['pcap_bytes'] == 0
            and 'Permission denied' in value['packet_access']['stderr'], 'precise BPF access blocker differs')
    for key in ['book_seams', 'task_seams']:
        for name, seams in value[key].items():
            C.Q.relative_path(name)
            text = C.Q.git('show', SOURCE + ':' + name).decode()
            for old, new in seams:
                require(text.count(old) == 1, 'retained old source seam differs')
                text = text.replace(old, new, 1)
    return value


def encode(value):
    validate(value)
    body = Q.canonical(value)
    require(0 < len(body) <= 8 * 1024 * 1024, 'dependency metadata exceeds bound')
    blob = lzma.compress(body, format=lzma.FORMAT_XZ,
                         filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6, 'dict_size': 8 * 1024 * 1024}])
    return {'schema_version': 1, 'encoding': 'xz6/base64 canonical UTF-8 JSON',
            'metadata_bytes': len(body), 'metadata_sha256': C.digest(body),
            'compressed_bytes': len(blob), 'compressed_sha256': C.digest(blob),
            'metadata_xz_base64': base64.b64encode(blob).decode(), 'producer': C.file_identity(PRODUCER)}


def decode(frame):
    try:
        require(isinstance(frame, dict) and set(frame) == {'schema_version', 'encoding', 'metadata_bytes',
                'metadata_sha256', 'compressed_bytes', 'compressed_sha256', 'metadata_xz_base64', 'producer'},
                'unreviewed dependency frame fields')
        require(type(frame['schema_version']) is int and frame['schema_version'] == 1
                and frame['encoding'] == 'xz6/base64 canonical UTF-8 JSON'
                and frame['producer'] == C.file_identity(PRODUCER), 'dependency frame/reader identity differs')
        require(type(frame['metadata_bytes']) is int and 0 < frame['metadata_bytes'] <= 8 * 1024 * 1024
                and type(frame['compressed_bytes']) is int and 0 < frame['compressed_bytes'] <= 1024 * 1024
                and R.H.identity(frame['metadata_sha256'], 64) and R.H.identity(frame['compressed_sha256'], 64),
                'dependency identity/bound differs')
        require(isinstance(frame['metadata_xz_base64'], str)
                and len(frame['metadata_xz_base64']) <= 2 * frame['compressed_bytes'], 'dependency base64 exceeds bound')
        blob = base64.b64decode(frame['metadata_xz_base64'], validate=True)
        require(len(blob) == frame['compressed_bytes'] and C.digest(blob) == frame['compressed_sha256'],
                'dependency compressed identity differs')
        decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=64 * 1024 * 1024)
        body = decoder.decompress(blob, max_length=frame['metadata_bytes'] + 1)
        require(decoder.eof and not decoder.unused_data and len(body) == frame['metadata_bytes']
                and C.digest(body) == frame['metadata_sha256'], 'dependency expansion identity/bound differs')
        return validate(R.H.json_object(body))
    except (KeyError, TypeError, IndexError, UnicodeError, RecursionError, lzma.LZMAError) as exc:
        raise ValueError('dependency evidence refused') from exc


def record_frame():
    path = C.U.source_path(ROOT, RECORD)
    require(path.is_file() and path.stat().st_size <= 131072, 'bounded dependency record required')
    text = path.read_text()
    require(text.count(MARKER) == 1, 'unique dependency evidence phase required')
    match = re.search(r'^```json\n(.*?)\n```$', text.split(MARKER, 1)[1], re.M | re.S)
    require(match is not None, 'dependency evidence frame unavailable')
    return R.H.json_object(match[1].encode())


def controls(frame):
    original = decode(frame)
    rows = []
    for name in ['sha', 'bool-bound', 'trailing-xz', 'missing-case', 'bool-verdict', 'producer-source', 'failed-source-seam']:
        changed = json.loads(Q.canonical(frame))
        value = json.loads(Q.canonical(original))
        inner = False
        if name == 'sha':
            changed['compressed_sha256'] = '0' * 64
        elif name == 'bool-bound':
            changed['metadata_bytes'] = True
        elif name == 'trailing-xz':
            blob = base64.b64decode(changed['metadata_xz_base64']) + b'trailing'
            changed.update(compressed_bytes=len(blob), compressed_sha256=C.digest(blob),
                           metadata_xz_base64=base64.b64encode(blob).decode())
        elif name == 'missing-case':
            value['runs']['normal-queue5']['profile']['observations'].pop()
            inner = True
        elif name == 'bool-verdict':
            value['runs']['normal-queue5']['profile']['observations'][0]['qrc'] = False
            inner = True
        elif name == 'producer-source':
            value['producer_sources'][0]['text'] += '# changed\n'
            inner = True
        else:
            value['task_seams'] = {'docs/tasks/LIVE-CONTAINMENT.md': [['not a retained source', 'pointer']]}
            inner = True
        if inner:
            body = Q.canonical(value)
            blob = lzma.compress(body, format=lzma.FORMAT_XZ,
                filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6, 'dict_size': 8 * 1024 * 1024}])
            changed.update(metadata_bytes=len(body), metadata_sha256=C.digest(body), compressed_bytes=len(blob),
                           compressed_sha256=C.digest(blob), metadata_xz_base64=base64.b64encode(blob).decode())
        try:
            decode(changed)
        except ValueError as exc:
            rows.append({'case': name, 'refused': True, 'reason': str(exc)})
        else:
            raise ValueError('dependency decoder accepted control: ' + name)
    require(decode(frame) == original, 'dependency controls changed original')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--verify-record', action='store_true')
    args = parser.parse_args()
    try:
        require(args.self_test or args.verify_record, 'record query option required')
        frame = record_frame()
        value = decode(frame)
        tested = controls(frame) if args.self_test else []
        print(json.dumps({'runs': len(value['runs']), 'page_observations': 960,
                          'controls': len(tested), 'D79': 'unresolved; BPF access blocked', 'D80': 'owned'}))
        return 0
    except (ValueError, OSError, D.subprocess.SubprocessError) as exc:
        print('DEPENDENCY-RECORD: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
