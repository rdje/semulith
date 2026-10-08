#!/usr/bin/env bash
# Pinned public release provisioning for the doctrine runner and native verification.
# The release digests come from rust-lang/mdBook's v0.5.4 GitHub asset metadata.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION=0.5.4
case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)
    TARGET=x86_64-unknown-linux-gnu
    SHA=3f28de05dafca9d0f2eab99c662116b0e37b89b1d96a08f8f430b9eeae958cd7 ;;
  Darwin-arm64)
    TARGET=aarch64-apple-darwin
    SHA=03e8a6d8b13a2971e0b3280affd03b388373c1485e26f73407c3a76b0b1838df ;;
  *) echo "install-ci-mdbook: unsupported host; no release identity is pinned" >&2; exit 2 ;;
esac
BIN="$ROOT/.app-data/ci-tools/bin"
CACHE="$ROOT/target/ci-tools"
ASSET="mdbook-v$VERSION-$TARGET.tar.gz"
ARCHIVE="$CACHE/$ASSET"
mkdir -p "$BIN" "$CACHE"
if [ ! -f "$ARCHIVE" ]; then
  curl --fail --location --retry 3 --output "$ARCHIVE.part" \
    "https://github.com/rust-lang/mdBook/releases/download/v$VERSION/$ASSET"
  mv "$ARCHIVE.part" "$ARCHIVE"
fi
python3 - "$ARCHIVE" "$SHA" <<'PY'
import hashlib, pathlib, sys
if hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest() != sys.argv[2]:
    sys.exit('install-ci-mdbook: REFUSED — release digest differs; remove the corrupt local cache and retry')
PY
tar -xzf "$ARCHIVE" -C "$BIN" mdbook
chmod +x "$BIN/mdbook"
[ "$("$BIN/mdbook" --version)" = "mdbook v$VERSION" ] || {
  echo "install-ci-mdbook: REFUSED — installed version differs" >&2; exit 1; }
echo "install-ci-mdbook: verified mdbook v$VERSION in .app-data/ci-tools/bin"
