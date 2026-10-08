#!/usr/bin/env python3
"""Cold single-leg controls using hand stubs of the published Cargo/Rustup interface."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
CASES = [
    ('cold-miri-linux', 'miri', 'Linux', 'green', 0, 'miri: green', False),
    ('cold-endian-linux', 'cross-endian', 'Linux', 'green', 0, 'cross-endian: green', False),
    ('cold-miri-darwin', 'miri', 'Darwin', 'green', 0, 'miri: green', False),
    ('cold-endian-darwin', 'cross-endian', 'Darwin', 'green', 0, 'cross-endian: green', False),
    ('linux-target-query', 'cross-endian', 'Linux', 'green', 0, 'cross-endian: green', True),
    ('miri-fails', 'miri', 'Linux', 'red', 1, 'miri: red', False),
    ('endian-fails', 'cross-endian', 'Linux', 'red', 1, 'cross-endian: red', False),
    ('miri-absent', 'miri', 'Linux', 'absent', 1, 'miri: absent', False),
    ('endian-absent', 'cross-endian', 'Linux', 'absent', 1, 'cross-endian: absent', False),
    ('setup-fails', 'miri', 'Linux', 'setup-red', 1, 'miri: red', False),
    ('vendor-fails', 'miri', 'Linux', 'vendor-red', 1, 'miri: red', False),
    ('translated-agrees', 'x86-64', 'Darwin', 'green', 0, 'x86-64: green', True),
    ('translated-differs', 'x86-64', 'Darwin', 'x86-diff', 1, 'x86-64: red', False),
    ('translated-stale-record', 'x86-64', 'Darwin', 'stale', 0, 'x86-64: green', True),
    ('translated-digest-fails', 'x86-64', 'Darwin', 'digest-red', 1, 'x86-64: red', False),
]
CARGO = '''#!/bin/sh
printf '%s\n' "$*" >> "$CONTROL_CALLS"
case "$*" in
  'test --all --target x86_64-apple-darwin') echo 'test result: ok. 1 passed; 0 failed';;
  'run -q '* )
    [ "$CONTROL_OUTCOME" != digest-red ] || exit 1
    case "$*" in *'-- demo --guest=stub --json') :;; *) exit 2;; esac
    case "$*" in
      *'--target x86_64-apple-darwin'*)
        [ "$CONTROL_OUTCOME" != x86-diff ] || { echo 'different fixture'; exit 0; };;
    esac
    echo 'same fixture';;
  "+nightly miri --version"|"+$CONTROL_NIGHTLY miri --version")
    [ "$CONTROL_OUTCOME" != absent ] || exit 1
    echo 'miri fixture';;
  "+$CONTROL_NIGHTLY vendor --locked --sync $CONTROL_ROOT/toolchain/lib/rustlib/src/rust/library/Cargo.toml .app-data/vendor")
    [ "$CONTROL_OUTCOME" != vendor-red ] || { echo 'stub vendor failure'; exit 1; }
    echo 'stub locked vendor ok';;
  "+$CONTROL_NIGHTLY miri setup"*)
    case "$MIRI_SYSROOT" in "$CONTROL_ROOT/target/portability/sysroots/"*) :;; *) exit 2;; esac
    [ "$CARGO_HOME" = "$CONTROL_ROOT/.app-data/cargo-home" ] || exit 2
    [ "$TMPDIR" = "$CONTROL_ROOT/target/portability/tmp" ] || exit 2
    [ "$CONTROL_OUTCOME" != setup-red ] || { echo 'stub setup failure'; exit 1; }
    mkdir -p "$MIRI_SYSROOT"; echo 'stub setup ok';;
  "+nightly miri test "*|"+$CONTROL_NIGHTLY miri test "*)
    [ "$CONTROL_OUTCOME" != red ] || { echo 'test result: FAILED. 0 passed; 1 failed'; exit 1; }
    echo 'test result: ok. 1 passed; 0 failed';;
  *) echo 'unexpected cargo call' >&2; exit 2;;
esac
'''
RUSTUP = '''#!/bin/sh
printf '%s\n' "$*" >> "$CONTROL_CALLS"
case "$*" in
  'target list --installed') echo x86_64-apple-darwin; exit 0;;
  "run $CONTROL_NIGHTLY rustc --print sysroot") echo "$CONTROL_ROOT/toolchain"; exit 0;;
  "target list --toolchain $CONTROL_NIGHTLY --installed") :;;
  'target list --toolchain nightly-aarch64-apple-darwin --installed')
    [ "$CONTROL_OS" = Darwin ] || exit 1;;
  *) exit 2;;
esac
[ "$CONTROL_OUTCOME" != absent ] || exit 0
echo powerpc64-unknown-linux-gnu
'''


def executable(path, body):
    path.write_text(body)
    path.chmod(0o755)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script', type=Path, default=ROOT / 'scripts/check_portability.sh')
    parser.add_argument('--case', choices=[case[0] for case in CASES])
    args = parser.parse_args()
    nightly = subprocess.check_output(
        ['bash', str(ROOT / 'scripts/check_portability.sh'), '--print-toolchain'], text=True).strip()
    scratch = ROOT / 'target/ci-recovery/cold-controls'
    scratch.mkdir(parents=True, exist_ok=True)
    passed = failed = 0
    for name, leg, host, outcome, rc, reason, warm in CASES:
        if args.case and args.case != name:
            continue
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            root = Path(directory)
            binary = root / 'bin'
            binary.mkdir()
            executable(binary / 'git', '#!/bin/sh\nprintf "%s\\n" "$CONTROL_ROOT"\n')
            executable(binary / 'cargo', CARGO)
            executable(binary / 'rustup', RUSTUP)
            executable(binary / 'uname', '''#!/bin/sh
if [ "$1" = -s ]; then echo "$CONTROL_OS"
elif [ "$CONTROL_OS" = Darwin ]; then echo arm64
else echo x86_64; fi
''')
            executable(binary / 'arch', '#!/bin/sh\nexit 0\n')
            if leg == 'x86-64':
                registry = root / 'crates/semulith-verify/src/guests.rs'
                registry.parent.mkdir(parents=True)
                registry.write_text('name: "stub"\n')
                record = root / 'profiles/rv64i-lab-v0/portability.sexp'
                record.parent.mkdir(parents=True)
                native_digest = hashlib.sha256(hashlib.sha256(b'same fixture\n').hexdigest().encode()).hexdigest()
                record.write_text('sha256 '+ ('0'*64 if outcome == 'stale' else native_digest)+'\n')
            if warm:
                (root / 'target/portability').mkdir(parents=True)
            calls = root / 'calls.txt'
            env = dict(os.environ, PATH=str(binary)+os.pathsep+os.environ['PATH'],
                       CONTROL_ROOT=str(root), CONTROL_OS=host, CONTROL_NIGHTLY=nightly,
                       CONTROL_CALLS=str(calls), CONTROL_OUTCOME=outcome)
            result = subprocess.run(['bash', str(args.script.resolve()), '--leg', leg],
                                    capture_output=True, text=True, env=env)
            output = result.stdout + result.stderr
            invoked = calls.read_text() if calls.exists() else ''
            log_name = {'miri': 'miri', 'cross-endian': 'cross', 'x86-64': 'x86-64'}[leg]
            log = root / f'target/portability/{log_name}.log'
            valid = result.returncode == rc and reason in output
            if leg != 'x86-64':
                valid = valid and 'test --all' not in invoked
            if outcome in ('green', 'stale'):
                valid = valid and log.is_file() and 'test result: ok.' in log.read_text()
                if leg != 'x86-64':
                    valid = valid and f'+{nightly} miri setup' in invoked
            if outcome in ('absent', 'setup-red', 'vendor-red'):
                valid = valid and 'miri test' not in invoked
            if outcome == 'vendor-red':
                valid = valid and 'miri setup' not in invoked
            if valid:
                passed += 1
            else:
                failed += 1
                print(f'PORTABILITY-COLD: MISS {name}: rc={result.returncode}, want {rc}\n{output}')
    print(f'PORTABILITY-COLD: {passed} pass / {failed} fail')
    return int(failed != 0)


if __name__ == '__main__':
    raise SystemExit(main())
