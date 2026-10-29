#!/usr/bin/env python3
"""Retain the licensed, source-pinned RV64I statements the XLEN case's properties cite, never the website shell.

The XLEN case (`P4-SYSTEM.14` a43a; REQ-D-XLEN, RVI-RV64I §3.1.1) needs its normative text retained the way the
M case's was (`scripts/retain_div_statement.py`, a42z; `scripts/retain_m_statements.py`, a42bb): ten exact
statements of RVI-RV64I §3.1 — the 64-bit registers and address space, the shift amount, LUI's sign extension
and the `*W` family — from the pinned page, under the same unprivileged licence evidence, in one attributed
wrapper that names the original page's digest (the publication a case's excerpt is bound to, a44-2c).
Emission is a bounded pure transformation plus explicit acquired-input reads; verification authenticates only
the retained file, without those acquired pages. Neither operation is a comparison, capture, property binding,
credit or qualification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import experiment_artifacts as A
import retain_div_statement as D  # the unprivileged licence evidence has one owner (a42z)

ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = ".materials/riscv/pinned-v20260120/unpriv/rv64.html"
SOURCE_SHA = "6eadb316c2d535ccb87a7a6feb03ff54af6f4b5bbeb5c1a5102a02af81f13abd"  # RVI-RV64I, 49,246 B (sources.sexp)
SOURCE_URL = "https://docs.riscv.org/reference/isa/v20260120/unpriv/rv64.html"
SOURCE_BYTES = 65536
RETAINED_PATH = "profiles/rv64gc-lab-v0/retained/rv64i-statements.html"
RETAINED_SHA = "5c93941804b6bab707d3c0345529fc918b10a953d72bc82d5735bcf78788f2a5"  # 4,163 B, emitted 2026-10-29 (a43a-2a)
RETAINED_ID = "RVI-RV64I-STATEMENTS"
RETAINED_BYTES = 8192
SPAN_BYTES = 1024
# Source order: the statements the XLEN case's 25 witnesses rest on.
STATEMENTS = (
    ("norm:rv64i_xreg_sz", "§3.1.1"), ("norm:rv64_w_sex", "§3.1.2"), ("norm:addiw_op", "§3.1.2.1"),
    ("norm:addiw_overflow", "§3.1.2.1"), ("norm:slliw_srliw_sraiw_op", "§3.1.2.1"), ("norm:lui_op_rv64i", "§3.1.2.1"),
    ("norm:addw_subw_op", "§3.1.2.2"), ("norm:addw_subw_overflow", "§3.1.2.2"),
    ("norm:sll_srl_sra_sh_amt_rv64i", "§3.1.2.2"), ("norm:sllw_srlw_sraw_op", "§3.1.2.2"),
)
# A statement's markup, measured over the ten spans: emphasis, code, and the manual's own cross-reference to another
# page of the same publication (the register-width statement links the RV32I register-state section) — kept
# unmodified, as the licence's reproduction asks; any other tag or attribute refuses.
OPENING_TAGS = (re.compile(rb"<em>"), re.compile(rb"<code>"),
                re.compile(rb'<a href="[a-z0-9-]+\.html#[A-Za-z0-9_-]+" class="xref page">'))


class RetentionError(ValueError):
    """No partial retained artifact escapes a refused source transformation."""


def require(condition, reason):
    if not condition:
        raise RetentionError(reason)


def pinned(data, limit, digest, name):
    require(type(data) is bytes and 1 <= len(data) <= limit, name + " byte bound/type")
    require(hashlib.sha256(data).hexdigest() == digest, name + " pin differs")


def select_span(source: bytes, name: str) -> bytes:
    marker = b'<span id="' + name.encode() + b'">'
    start = source.find(marker)
    require(start >= 0, f"{name}: statement is absent")
    require(source.count(marker) == 1, f"{name}: statement is duplicated")
    end = source.find(b"</span>", start + len(marker))
    require(end >= 0, f"{name}: statement is unterminated")
    span = source[start: end + len(b"</span>")]
    require(len(span) <= SPAN_BYTES, f"{name}: statement exceeds bound")
    inner = span[len(marker): -len(b"</span>")]
    for tag in re.findall(rb"<[a-zA-Z0-9][^>]*>", inner):
        require(any(shape.fullmatch(tag) for shape in OPENING_TAGS), f"{name} carries unreviewed markup {tag[:40]!r}")
    span.decode("utf-8")
    return span


def retain_statements(source: bytes, licence: bytes) -> bytes:
    """Copy ten exact spans after checking both complete, frozen primary inputs."""
    pinned(source, SOURCE_BYTES, SOURCE_SHA, "RV64I source")
    pinned(licence, D.LICENCE_BYTES, D.LICENCE_SHA, "licence evidence")
    require(D.LICENCE_STATEMENT in licence, "reviewed licence statement is absent")
    spans = [(name, section, select_span(source, name)) for name, section in STATEMENTS]
    header = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>Retained RVI-RV64I statements — v20260120</title>
<body>
<h1>RVI-RV64I §3.1: the 64-bit registers and address space, the shift amount, LUI and the *W instructions</h1>
<p>Copyright © RISC-V International.
Manual text by RISC-V International and the original RISC-V ISA manual authors.
The quoted statements are licensed under
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
Semulith adds this wrapper and retains only the named statements; all surrounding
text, diagrams and website assets are omitted. Each quoted span is unmodified.
No endorsement is implied.</p>
<p>Source: <a href="{SOURCE_URL}">RISC-V Ratified Specifications Library,
v20260120, RV64I Base Integer Instruction Set Version 2.1, §3.1</a>.<br>
Original page SHA256: <code>{SOURCE_SHA}</code>.<br>
Licence evidence: <a href="{D.LICENCE_URL}">unprivileged preface to Version 2.2</a>,
whose statement also covers future manual versions.<br>
Licence-evidence page SHA256: <code>{D.LICENCE_SHA}</code>.<br>
Transformation: <code>scripts/retain_rv64i_statements.py</code>, reviewed 2026-10-29.
This excerpt establishes no XLEN acceptance.</p>
""".encode("utf-8")
    body = b"".join(f'<h2>{section}: <code>{name}</code></h2>\n<blockquote><p>'.encode("utf-8") + span
                    + b"</p></blockquote>\n" for name, section, span in spans)
    retained = header + body + b"</body></html>\n"
    require(len(retained) <= RETAINED_BYTES, "retained artifact exceeds bound")
    return retained


def read_pin(root, *, path, digest, limit, input_id):
    return A.read_snapshot(root, "input", dict(id=input_id, path=path, sha256=digest), max_bytes=limit)


def verify_retained(root=ROOT):
    """Authenticate the curated input alone; no acquired source/cache access."""
    return read_pin(root, path=RETAINED_PATH, digest=RETAINED_SHA, limit=RETAINED_BYTES,
                    input_id=RETAINED_ID).pin


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--emit", action="store_true", help="print the retained artifact from the acquired pages")
    actions.add_argument("--verify", action="store_true", help="authenticate the tracked artifact without the acquired pages")
    args = parser.parse_args(argv)
    if args.verify:
        pin = verify_retained()
        print(json.dumps(dict(disposition=pin.disposition, reason=pin.reason, path=pin.path,
                              byte_size=pin.byte_size, sha256=pin.sha256)))
        return 0 if pin.disposition == "matched" else 2 if pin.disposition == "unavailable" else 1
    inputs = []
    for path, digest, limit, input_id in ((SOURCE_PATH, SOURCE_SHA, SOURCE_BYTES, "RVI-RV64I"),
                                          (D.LICENCE_PATH, D.LICENCE_SHA, D.LICENCE_BYTES, "RVI-UNPRIV-LICENCE")):
        snapshot = read_pin(ROOT, path=path, digest=digest, limit=limit, input_id=input_id)
        if snapshot.pin.disposition != "matched":
            print(json.dumps(dict(disposition=snapshot.pin.disposition, reason=snapshot.pin.reason)), file=sys.stderr)
            return 2 if snapshot.pin.disposition == "unavailable" else 1
        inputs.append(snapshot.data)
    try:
        output = retain_statements(*inputs)
    except (RetentionError, UnicodeError) as exc:
        print(json.dumps(dict(disposition="refused", reason=str(exc))), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
