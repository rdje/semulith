#!/usr/bin/env python3
"""Retain the licensed, source-pinned DIV/DIVU statement, never the website shell.

Emission is a bounded pure transformation plus explicit acquired-input reads.
Verification authenticates only the retained file, without those acquired pages.
Neither operation is a comparison, capture, property binding or qualification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import experiment_artifacts as A

ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = ".materials/riscv/pinned-v20260120/unpriv/m-st-ext.html"
SOURCE_SHA = "85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716"
SOURCE_URL = "https://docs.riscv.org/reference/isa/v20260120/unpriv/m-st-ext.html"
LICENCE_PATH = ".materials/riscv/pinned-v20260120/unpriv/colophon.html"
LICENCE_SHA = "7f48c2cb52c7d325520b00a02153222492bd5c4ffa0ae02adecda7ecc4c2a25c"
LICENCE_URL = "https://docs.riscv.org/reference/isa/v20260120/unpriv/colophon.html"
RETAINED_PATH = "profiles/rv64gc-lab-v0/retained/div-statement.html"
RETAINED_SHA = "bbe3ff9dd6d8e1b452589669cd676d998265327eeaf8ed370bb95fcf15af1a58"
SOURCE_BYTES = 65536
LICENCE_BYTES = 131072
RETAINED_BYTES = 4096
SPAN_BYTES = 1024
MARKER = b'<span id="norm:div_divu_op">'
LICENCE_STATEMENT = (
    b"Commons Attribution 4.0 International License by the original authors,\n"
    b"and this and future versions of this document will be released under the\n"
    b"same license."
)


class RetentionError(ValueError):
    """No partial retained artifact escapes a refused source transformation."""


def require(condition, reason):
    if not condition:
        raise RetentionError(reason)


def pinned(data, limit, digest, name):
    require(type(data) is bytes and 1 <= len(data) <= limit, name + " byte bound/type")
    require(hashlib.sha256(data).hexdigest() == digest, name + " pin differs")


def retain_statement(source: bytes, licence: bytes) -> bytes:
    """Copy one exact span after checking both complete, frozen primary inputs."""
    pinned(source, SOURCE_BYTES, SOURCE_SHA, "M source")
    pinned(licence, LICENCE_BYTES, LICENCE_SHA, "licence evidence")
    require(LICENCE_STATEMENT in licence, "reviewed licence statement is absent")
    start = source.find(MARKER)
    require(start >= 0, "source statement is absent")
    require(source.count(MARKER) == 1, "source statement is duplicated")
    end = source.find(b"</span>", start + len(MARKER))
    require(end >= 0, "source statement is unterminated")
    span = source[start : end + len(b"</span>")]
    require(len(span) <= SPAN_BYTES, "source statement exceeds bound")
    # This exact pinned span contains only static text and code markup. The
    # original bytes, including whitespace, are retained; no HTML is executed.
    span.decode("utf-8")
    header = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>Retained RVI-M division statement — v20260120</title>
<body>
<h1>RVI-M §11.1.2: DIV/DIVU statement</h1>
<p>Copyright © RISC-V International.
Manual text by RISC-V International and the original RISC-V ISA manual authors.
The quoted statement is licensed under
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
Semulith adds this wrapper and retains only the named statement; all surrounding
text, diagrams and website assets are omitted. The quoted span is unmodified.
No endorsement is implied.</p>
<p>Source: <a href="{SOURCE_URL}">RISC-V Ratified Specifications Library,
v20260120, M extension Version 2.0, §11.1.2</a>.<br>
Original page SHA256: <code>{SOURCE_SHA}</code>.<br>
Licence evidence: <a href="{LICENCE_URL}">unprivileged preface to Version 2.2</a>,
whose statement also covers future manual versions.<br>
Licence-evidence page SHA256: <code>{LICENCE_SHA}</code>.<br>
Transformation: <code>scripts/retain_div_statement.py</code>, reviewed 2026-10-18.
This excerpt does not retain other M operations or establish their acceptance.</p>
<blockquote><p>""".encode(
        "utf-8"
    )
    retained = header + span + b"</p></blockquote>\n</body></html>\n"
    require(len(retained) <= RETAINED_BYTES, "retained artifact exceeds bound")
    return retained


def read_pin(root, *, path, digest, limit, input_id):
    return A.read_snapshot(
        root, "input", dict(id=input_id, path=path, sha256=digest), max_bytes=limit
    )


def verify_retained(root=ROOT):
    """Authenticate the curated input alone; no acquired source/cache access."""
    result = read_pin(
        root,
        path=RETAINED_PATH,
        digest=RETAINED_SHA,
        limit=RETAINED_BYTES,
        input_id="RVI-M-DIV-STATEMENT",
    )
    return result.pin


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--emit", action="store_true")
    actions.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        pin = verify_retained()
        print(
            json.dumps(
                dict(
                    disposition=pin.disposition,
                    reason=pin.reason,
                    path=pin.path,
                    byte_size=pin.byte_size,
                    sha256=pin.sha256,
                )
            )
        )
        return (
            0
            if pin.disposition == "matched"
            else 2 if pin.disposition == "unavailable" else 1
        )
    inputs = []
    for path, digest, limit, input_id in (
        (SOURCE_PATH, SOURCE_SHA, SOURCE_BYTES, "RVI-M"),
        (LICENCE_PATH, LICENCE_SHA, LICENCE_BYTES, "RVI-UNPRIV-LICENCE"),
    ):
        snapshot = read_pin(
            ROOT, path=path, digest=digest, limit=limit, input_id=input_id
        )
        if snapshot.pin.disposition != "matched":
            print(
                json.dumps(
                    dict(
                        disposition=snapshot.pin.disposition, reason=snapshot.pin.reason
                    )
                ),
                file=sys.stderr,
            )
            return 2 if snapshot.pin.disposition == "unavailable" else 1
        inputs.append(snapshot.data)
    try:
        output = retain_statement(*inputs)
    except (RetentionError, UnicodeError) as exc:
        print(json.dumps(dict(disposition="refused", reason=str(exc))), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
