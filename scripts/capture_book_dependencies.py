#!/usr/bin/env python3
"""One terminal command for D79: pinned replay plus scoped macOS packet capture.

Run as your ordinary user. Only the system tcpdump runs through sudo; preparation,
WebKit, journals and output files remain unprivileged. No permission changes.
--self-test uses an unprivileged substitute process, never sudo or live capture.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import secrets
import signal
import struct
import subprocess
import sys
import tempfile
import threading
import time
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
import trace_book_dependencies as D

ROOT = D.ROOT
PRODUCER = 'scripts/capture_book_dependencies.py'
PACKET_LIMIT = 200000
SNAPLEN = 96
DEADLINE = 600
require = D.require


def capture_command(ports):
    require(isinstance(ports, list) and 1 <= len(ports) <= 4
            and all(type(port) is int and 1024 <= port <= 65535 for port in ports)
            and len(set(ports)) == len(ports), 'invalid owned capture ports')
    expression = ('ip and tcp and src host 127.0.0.1 and dst host 127.0.0.1 and ('
                  + ' or '.join('port ' + str(port) for port in sorted(ports)) + ')')
    return ['/usr/bin/sudo', '--', '/usr/sbin/tcpdump', '-p', '-U', '-i', 'lo0', '-nn',
            '-s', str(SNAPLEN), '-c', str(PACKET_LIMIT), '-w', '-', expression]


def inspect_pcap(path, ports):
    """Read classic pcap independently of tcpdump; enforce every packet's scope."""
    require(24 < path.stat().st_size <= 24 + PACKET_LIMIT * (16 + SNAPLEN),
            'empty or oversized packet capture')
    count, resets, syns = 0, 0, 0
    seen = set()
    with path.open('rb') as stream:
        header = stream.read(24)
        magic = {b'\xd4\xc3\xb2\xa1': ('<', 1000000), b'\xa1\xb2\xc3\xd4': ('>', 1000000),
                 b'\x4d\x3c\xb2\xa1': ('<', 1000000000), b'\xa1\xb2\x3c\x4d': ('>', 1000000000)}
        require(header[:4] in magic, 'unsupported pcap magic')
        endian, resolution = magic[header[:4]]
        major, minor, zone, accuracy, snaplen, link = struct.unpack(endian + 'HHiIII', header[4:])
        require((major, minor, zone, accuracy, snaplen) == (2, 4, 0, 0, SNAPLEN)
                and link in {0, 108}, 'unsupported pcap header or loopback link type')
        while frame := stream.read(16):
            require(len(frame) == 16, 'truncated pcap frame header')
            seconds, fraction, size, original = struct.unpack(endian + 'IIII', frame)
            require(seconds > 0 and fraction < resolution and 44 <= size <= SNAPLEN
                    and original >= size, 'invalid pcap frame length/time')
            packet = stream.read(size)
            require(len(packet) == size, 'truncated pcap packet')
            family = packet[:4]
            require(family in {b'\x02\0\0\0', b'\0\0\0\x02'}, 'non-IPv4 loopback packet')
            ip = packet[4:]
            ihl = (ip[0] & 15) * 4
            require(ip[0] >> 4 == 4 and ihl >= 20 and len(ip) >= ihl + 20
                    and ip[9] == 6 and ip[12:20] == b'\x7f\0\0\x01' * 2
                    and int.from_bytes(ip[6:8], 'big') & 0x3fff == 0,
                    'packet outside unfragmented loopback TCP scope')
            source, destination = struct.unpack('!HH', ip[ihl:ihl + 4])
            matched = {source, destination} & set(ports)
            require(matched, 'packet outside reserved owned ports')
            seen.update(matched)
            resets += bool(ip[ihl + 13] & 4)
            syns += bool(ip[ihl + 13] & 2)
            count += 1
            require(count < PACKET_LIMIT, 'packet ceiling reached; capture may be incomplete')
    require(count > 0 and seen == set(ports), 'capture lacks traffic for an owned server')
    return {'packets': count, 'bytes': path.stat().st_size, 'sha256': D.C.digest(path.read_bytes()),
            'ports': sorted(seen), 'tcp_reset_packets': resets, 'tcp_syn_packets': syns}


class Capture:
    """A single sudo child, with startup acknowledgement and joined shutdown."""
    def __init__(self, output, ports, *, launcher=subprocess.Popen, startup_timeout=180, deadline=DEADLINE):
        self.output, self.ports = output, ports
        self.launcher, self.startup_timeout, self.deadline = launcher, startup_timeout, deadline
        self.process = None
        self.timer = None
        self.expired = threading.Event()
        self.streams = contextlib.ExitStack()

    def check(self):
        require(not self.expired.is_set(), 'capture deadline reached; evidence incomplete')
        require(self.process is not None and self.process.poll() is None,
                'packet capture ended before replay completed; inspect tcpdump.stderr.log')

    def expire(self):
        self.expired.set()
        if self.process is not None and self.process.poll() is None:
            with contextlib.suppress(ProcessLookupError):
                self.process.send_signal(signal.SIGTERM)

    def __enter__(self):
        self.output.mkdir()
        command = capture_command(self.ports)
        D.N.write_json(self.output / 'scope.json', {'command': command, 'ports': self.ports,
                       'snaplen': SNAPLEN, 'packet_limit': PACKET_LIMIT, 'deadline_seconds': self.deadline})
        try:
            packets = self.streams.enter_context((self.output / 'traffic.pcap').open('xb'))
            errors = self.streams.enter_context((self.output / 'tcpdump.stderr.log').open('xb'))
            # sudo reads its password directly from the terminal, never from Python.
            self.process = self.launcher(command, stdout=packets, stderr=errors, cwd=ROOT)
            self.timer = threading.Timer(self.deadline, self.expire)
            self.timer.daemon = True
            self.timer.start()
            until = time.monotonic() + self.startup_timeout
            while True:
                self.check()
                text = (self.output / 'tcpdump.stderr.log').read_text(errors='replace')
                if 'listening on lo0,' in text:
                    break
                require(time.monotonic() < until, 'capture startup timed out; authentication/readiness missing')
                time.sleep(.05)
            return self
        except BaseException:
            self.stop()
            raise

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer.join()
        try:
            if self.process is not None and self.process.poll() is None:
                # sudo documents forwarding user-process SIGINT/TERM to its child.
                self.process.send_signal(signal.SIGINT)
                try:
                    self.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.process.terminate()
                    self.process.wait(timeout=10)
            if self.process is not None:
                D.N.write_json(self.output / 'exit.json', {'returncode': self.process.returncode,
                               'deadline_reached': self.expired.is_set()})
        finally:
            self.streams.close()

    def __exit__(self, *unused):
        self.stop()

    def verify(self):
        require(self.process.returncode == 0 and not self.expired.is_set(),
                'packet capture refused or expired; inspect tcpdump.stderr.log')
        text = (self.output / 'tcpdump.stderr.log').read_text(errors='replace')
        dropped = re.findall(r'^(\d+) packets dropped by kernel$', text, re.M)
        captured = re.findall(r'^(\d+) packets captured$', text, re.M)
        require(dropped == ['0'] and len(captured) == 1, 'packet drop/capture counters unavailable or nonzero')
        result = inspect_pcap(self.output / 'traffic.pcap', self.ports)
        require(int(captured[0]) == result['packets'], 'pcap and capture counter differ')
        return result


def replay(program, origins, cases, output, capture):
    """Two workers per origin, preserving every observation before any refusal."""
    output.mkdir()
    observations = D.Journal(output / 'observations.jsonl')
    rows = []
    def call(server, index, case):
        capture.check()
        row = {'server': server, 'index': index, **D.execute(program, origins[server], case,
               output / ('browser-' + str(server)) / ('page-' + str(index).zfill(3)))}
        observations.append(event='observed', case=row)
        return row
    pools = [concurrent.futures.ThreadPoolExecutor(max_workers=2) for _ in origins]
    futures = []
    try:
        futures = [pools[server].submit(call, server, index, case)
                   for index, case in enumerate(cases) for server in range(len(origins))]
        for future in concurrent.futures.as_completed(futures):
            rows.append(future.result())
            capture.check()
    finally:
        # Stop queued work on interrupt/refusal; only the bounded active pages join.
        for future in futures:
            future.cancel()
        for pool in pools:
            pool.shutdown(wait=True, cancel_futures=True)
    return sorted(rows, key=lambda row: (row['server'], row['index']))


def run(*, check_preparation=False):
    require(sys.platform == 'darwin' and os.geteuid() != 0,
            'run on macOS as your ordinary user, without prefixing Python with sudo')
    label = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + secrets.token_hex(3)
    relative = 'target/live-containment/packet-' + label
    output = D.C.U.source_path(ROOT, relative)
    D.owned_target(output)
    before = D.C.working_snapshot([PRODUCER])
    output.mkdir(parents=True)
    (output / 'environment-tmp').mkdir()
    os.environ['TMPDIR'] = str(output / 'environment-tmp')
    print('Preparing pinned books and nonpersistent WebKit; output: ' + relative, flush=True)
    D.N.write_json(output / 'working-before.json', before)
    program, compiler = D.Q.compile_webkit(output)
    mdbook = D.R.mdbook_version(program.parent / 'tmp')
    engine = D.Q.browser_identity(program)
    calibration = D.Q.calibrate(program, output)
    baseline, original_cases, site, cases, inputs = D.prepare(output)
    profiles = {}
    try:
        with contextlib.ExitStack() as stack:
            ports = []
            for phase, bundle, population in [('warmup', baseline, original_cases), ('profile', site, cases)]:
                directory = output / phase
                directory.mkdir()
                origins, journals = [], []
                for server in range(2):
                    base, journal = stack.enter_context(D.serve(bundle, population,
                        directory / ('server-' + str(server)), backlog=5, fault='none'))
                    origins.append(base)
                    ports.append(urlsplit(base).port)
                    journals.append(journal)
                profiles[phase] = {'origins': origins, 'journals': journals, 'cases': population}
            if not check_preparation:
                print('Only tcpdump needs administrator access; enter your password if sudo asks.', flush=True)
                with Capture(output / 'capture', ports) as capture:
                    print('Capture ready: four owned loopback ports, 96 bytes per packet. Replaying source then repair.', flush=True)
                    for phase, profile in profiles.items():
                        profile['observations'] = replay(program, profile['origins'], profile['cases'],
                                                         output / phase / 'pages', capture)
                        print(phase + ': ' + str(len(profile['observations'])) + ' page observations saved.', flush=True)
                packets = capture.verify()
        require(D.Q.browser_identity(program) == engine and D.R.mdbook_version(program.parent / 'tmp') == mdbook,
                'toolchain changed during capture')
        require(D.C.working_snapshot([PRODUCER]) == before, 'source/index/modes changed during capture')
        D.N.write_json(output / 'working-after.json', before)
        if check_preparation:
            D.N.write_json(output / 'preparation.json', {'producer': D.C.file_identity(PRODUCER),
                           'inputs': inputs, 'compiler': compiler, 'engine': engine, 'mdbook': mdbook,
                           'calibration': calibration, 'reserved_ports': ports,
                           'capture': 'not requested; no sudo executed'})
            print('Preparation verified; all four servers closed. No sudo or packet capture.', flush=True)
            return 0
        saved = {}
        for phase, profile in profiles.items():
            saved[phase] = {'servers': 2, 'jobs_per_server': 2, 'backlog': 5, 'fault': 'none',
                            'observations': profile['observations'],
                            'http': [journal.rows for journal in profile['journals']]}
        value = {'producer': D.C.file_identity(PRODUCER), 'inputs': inputs, 'compiler': compiler,
                 'engine': engine, 'mdbook': mdbook, 'calibration': calibration, 'capture': packets,
                 'profiles': saved, 'D79': 'unresolved; captured evidence requires causal analysis'}
        D.N.write_json(output / 'result.json', value)
        unjudgeable = sum(row.get('unjudgeable', False) for p in saved.values() for row in p['observations'])
        print('Capture saved: ' + relative + '/result.json; D79 remains open pending analysis.', flush=True)
        return 2 if unjudgeable else 0
    except BaseException as exc:
        D.N.write_json(output / 'failure.json', {'error': type(exc).__name__, 'message': str(exc),
                       'D79': 'unresolved; partial diagnostics retained'})
        raise


def self_test():
    """Independent packet oracle and actual child lifecycle, without privileges."""
    parent = ROOT / 'target/live-containment/capture-controls'
    parent.mkdir(parents=True, exist_ok=True)
    tests = []
    def refused(label, operation):
        try:
            operation()
        except ValueError:
            tests.append(label)
        else:
            raise ValueError('control accepted: ' + label)
    with tempfile.TemporaryDirectory(dir=parent) as temporary:
        directory = Path(temporary)
        for value in [[], [True], [80], [1234, 1234], [65536], [1234] * 5, '1234']:
            refused('port-scope', lambda v=value: capture_command(v))
        ports = [23456]
        command = capture_command(ports)
        require(command[:3] == ['/usr/bin/sudo', '--', '/usr/sbin/tcpdump']
                and command[-1] == 'ip and tcp and src host 127.0.0.1 and dst host 127.0.0.1 and (port 23456)',
                'closed privileged command differs')
        ip = bytes.fromhex('4500002800004000400600007f0000017f000001')
        tcp = struct.pack('!HHIIHHHH', ports[0], 34567, 0, 0, 0x5002, 8192, 0, 0)
        packet = b'\x02\0\0\0' + ip + tcp
        header = b'\xd4\xc3\xb2\xa1' + struct.pack('<HHiIII', 2, 4, 0, 0, SNAPLEN, 0)
        body = header + struct.pack('<IIII', 1, 0, len(packet), len(packet)) + packet
        path = directory / 'valid.pcap'
        path.write_bytes(body)
        require(inspect_pcap(path, ports)['packets'] == 1, 'positive pcap refused')
        # System tcpdump is an independently implemented offline packet reader.
        oracle = subprocess.run(['/usr/sbin/tcpdump', '-nn', '-r', str(path)], capture_output=True, timeout=10)
        require(oracle.returncode == 0 and b'127.0.0.1.23456 > 127.0.0.1.34567' in oracle.stdout,
                'independent offline tcpdump disagrees')
        tests.append('independent-pcap')
        for label, changed in [('magic', b'bad!' + body[4:]), ('truncated', body[:-1]),
                               ('trailing-header', body + b'x'), ('snaplen', body[:16] + struct.pack('<I', 65535) + body[20:]),
                               ('nonlocal', body[:60] + b'\x7f\0\0\x02' + body[64:])]:
            target = directory / (label + '.pcap')
            target.write_bytes(changed)
            refused(label, lambda p=target: inspect_pcap(p, ports))
        refused('wrong-port', lambda: inspect_pcap(path, [23457]))
        refused('missing-server', lambda: inspect_pcap(path, ports + [23457]))
        child = directory / 'capture.py'
        child.write_text('import signal, sys, time\n'
                         'from pathlib import Path\n'
                         'def stop(*unused):\n'
                         ' print("1 packets captured\\n0 packets dropped by kernel", file=sys.stderr, flush=True)\n'
                         ' sys.exit(0)\n'
                         'signal.signal(signal.SIGINT, stop)\n'
                         'signal.signal(signal.SIGTERM, stop)\n'
                         'sys.stdout.buffer.write(Path(sys.argv[1]).read_bytes()); sys.stdout.buffer.flush()\n'
                         'print("listening on lo0, link-type NULL", file=sys.stderr, flush=True)\n'
                         'while True: time.sleep(.1)\n')
        launched = []
        def launch(actual, **kwargs):
            require(actual == command, 'unexpected privileged command in control')
            process = subprocess.Popen([sys.executable, str(child), str(path)], **kwargs)
            launched.append(process)
            return process
        with Capture(directory / 'positive', ports, launcher=launch) as capture:
            capture.check()
        require(capture.verify()['packets'] == 1, 'actual child shutdown/capture failed')
        tests.append('joined-child')
        log = capture.output / 'tcpdump.stderr.log'
        original = log.read_bytes()
        log.write_bytes(original.replace(b'0 packets dropped', b'1 packets dropped'))
        refused('capture-drops', capture.verify)
        log.write_bytes(original.replace(b'1 packets captured', b'2 packets captured'))
        refused('capture-counter', capture.verify)
        log.write_bytes(original)
        try:
            with Capture(directory / 'interrupted', ports, launcher=launch):
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            pass
        tests.append('interrupt-cleanup')
        def denied(actual, **kwargs):
            require(actual == command, 'unexpected denied command')
            process = subprocess.Popen([sys.executable, '-c', 'import sys; sys.exit(1)'], **kwargs)
            launched.append(process)
            return process
        refused('authentication-denied', lambda: Capture(directory / 'denied', ports, launcher=denied).__enter__())
        def silent(actual, **kwargs):
            process = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)'], **kwargs)
            launched.append(process)
            return process
        refused('startup-timeout', lambda: Capture(directory / 'silent', ports, launcher=silent,
                                                 startup_timeout=.1).__enter__())
        refused('deadline', lambda: Capture(directory / 'deadline', ports, launcher=silent,
                                          deadline=.1).__enter__())
        require(all(process.poll() is not None for process in launched), 'control stranded a child')
        # Exercise the actual scheduling/journaling path, including pending-work cancellation.
        from unittest.mock import patch
        class Active:
            def check(self):
                pass
        cases = [{'path': str(index)} for index in range(100)]
        calls = []
        def execute(program, base, case, output):
            calls.append(case['path'])
            time.sleep(.01)
            if case['path'] == '0':
                raise ValueError('controlled replay refusal')
            return {'path': case['path'], 'qualification_returncode': 0}
        with patch.object(D, 'execute', execute):
            refused('pending-cancellation', lambda: replay(None, ['http://owned'], cases,
                                                          directory / 'cancelled', Active()))
        require(len(calls) < len(cases), 'refused replay ran all pending work')
        with patch.object(D, 'execute', lambda program, base, case, output:
                          {'path': case['path'], 'qualification_returncode': 0}):
            rows = replay(None, ['http://owned', 'http://owned2'], cases[:2],
                          directory / 'replay', Active())
        streamed = [json.loads(line)['case'] for line in
                    (directory / 'replay/observations.jsonl').read_text().splitlines()]
        require(len(rows) == 4 and rows == sorted(streamed, key=lambda r: (r['server'], r['index'])),
                'complete replay stream differs')
        tests.append('replay-stream')
    print(json.dumps({'controls': len(tests), 'failed': 0, 'privileged_processes': 0}))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--self-test', action='store_true')
    mode.add_argument('--check-preparation', action='store_true',
                      help='verify real pinned builds, WebKit and four servers without running sudo')
    args = parser.parse_args()
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    if not args.self_test:
        signal.signal(signal.SIGTERM, interrupted)
        signal.signal(signal.SIGHUP, interrupted)
    try:
        return self_test() if args.self_test else run(check_preparation=args.check_preparation)
    except KeyboardInterrupt:
        print('BOOK-CAPTURE: interrupted; capture/server workers joined, partial output retained.', file=sys.stderr)
        return 130
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print('BOOK-CAPTURE: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
