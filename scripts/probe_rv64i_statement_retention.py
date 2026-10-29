#!/usr/bin/env python3
"""Cache-free synthetic controls for the retained RV64I statements the XLEN case cites (P4-SYSTEM.14 a43a-2a)."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import retain_div_statement as D
import retain_rv64i_statements as R

ROOT = Path(__file__).resolve().parent.parent
MUTATIONS = {
    "input-pins": ('    pinned(source, SOURCE_BYTES, SOURCE_SHA, "RV64I source")\n', ''),
    "licence-statement": ('require(D.LICENCE_STATEMENT in licence, ', 'require(True, '),
    "unique-statement": ('require(source.count(marker) == 1, ', 'require(True, '),
    "closing-span": ('require(end >= 0, f"{name}: statement is unterminated")', 'require(True, f"{name}: statement is unterminated")'),
    "span-markup": ('any(shape.fullmatch(tag) for shape in OPENING_TAGS)', 'True'),
    "retained-bound": ('require(len(retained) <= RETAINED_BYTES, ', 'require(True, '),
    "retained-pin": ("digest=RETAINED_SHA", "digest=SOURCE_SHA"),
}
XREF = b'<a href="rv32.html#gprs" class="xref page">register state</a>'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def span(name, text=b"synthetic <em>XLEN</em> <code>rs1</code> statement, unchanged whitespace\n"):
    return b'<span id="' + name.encode() + b'">' + text + b"</span>"


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.spans = {name: span(name) for name, _ in R.STATEMENTS}
        self.spans[R.STATEMENTS[0][0]] = span(R.STATEMENTS[0][0], b"64 bits (XLEN=64 in " + XREF + b").")
        self.build()
        self.licence = b"synthetic preface before\n" + D.LICENCE_STATEMENT + b"\nafter"
        self.pin()

    def build(self, *, spans=None, extra=b""):
        spans = self.spans if spans is None else spans
        self.source = (b"<script>excluded()</script>before" + span("norm:ld_op_rv64i")
                       + b"between".join(spans.values()) + b"<nav>excluded</nav>" + extra + b"after")

    def pin(self):
        for owner, name, value in ((R, "SOURCE_SHA", sha(self.source)), (D, "LICENCE_SHA", sha(self.licence))):
            context = patch.object(owner, name, value)
            context.start()
            self.addCleanup(context.stop)

    def emit(self):
        return R.retain_statements(self.source, self.licence)

    def rebuilt_emit(self, **kwargs):
        self.build(**kwargs)
        with patch.object(R, "SOURCE_SHA", sha(self.source)):
            return R.retain_statements(self.source, self.licence)

    def temporary_root(self):
        base = ROOT / "target/rv64i-statement-retention-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def install(self, root, data):
        path = root / R.RETAINED_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_exact_quotes_without_unselected_site_bytes(self):
        out = self.emit()
        for name, quoted in self.spans.items():
            self.assertEqual(out.count(quoted), 1, name)
        for excluded in (b"<script", b"excluded()", b"<nav", b"between", b"before", b"after<", b"norm:ld_op_rv64i"):
            self.assertNotIn(excluded, out)

    def test_attribution_names_the_original_publication_once(self):
        out = self.emit().decode()
        for needle in ("CC BY 4.0", "Copyright © RISC-V International", D.LICENCE_SHA,
                       "scripts/retain_rv64i_statements.py", "establishes no XLEN acceptance"):
            self.assertIn(needle, out)
        # The one publication a case's excerpt is bound to (review_div_capture.PUBLICATION, a44-2c).
        self.assertEqual(out.count("Original page SHA256: <code>" + R.SOURCE_SHA + "</code>"), 1)

    def test_output_is_deterministic(self):
        self.assertEqual(self.emit(), self.emit())

    def test_source_change_refuses(self):
        with self.assertRaises(R.RetentionError):
            R.retain_statements(self.source + b"x", self.licence)

    def test_missing_licence_statement_refuses_even_with_fixture_pin(self):
        licence = b"synthetic preface without the statement"
        with patch.object(D, "LICENCE_SHA", sha(licence)), self.assertRaises(R.RetentionError):
            R.retain_statements(self.source, licence)

    def test_each_missing_statement_refuses(self):
        for name in self.spans:
            with self.subTest(name=name), self.assertRaises(R.RetentionError):
                self.rebuilt_emit(spans={k: v for k, v in self.spans.items() if k != name})

    def test_duplicate_statement_refuses(self):
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(extra=span(R.STATEMENTS[0][0]))

    def test_unterminated_statement_refuses(self):
        """The last statement in source order with no closing span anywhere after it."""
        name = R.STATEMENTS[-1][0]
        spans = dict(self.spans); spans[name] = b'<span id="' + name.encode() + b'">no end'
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(spans=spans)

    def test_nested_span_refuses(self):
        """A nested span is unreviewed markup: the allowlist refuses it (no separate guard)."""
        name = R.STATEMENTS[2][0]
        spans = dict(self.spans); spans[name] = span(name, b"outer <span id=\"x\">inner")
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(spans=spans)

    def test_span_bound_is_inclusive(self):
        name = R.STATEMENTS[1][0]
        overhead = len(span(name, b""))
        fits = dict(self.spans); fits[name] = span(name, b"x" * (R.SPAN_BYTES - overhead))
        self.assertIn(fits[name], self.rebuilt_emit(spans=fits))
        over = dict(self.spans); over[name] = span(name, b"x" * (R.SPAN_BYTES - overhead + 1))
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(spans=over)

    def test_only_the_reviewed_markup_is_retained(self):
        """Emphasis, code and the manual's own same-publication cross-reference pass; anything else refuses."""
        name = R.STATEMENTS[1][0]
        for bad in (b'<a href="https://example.invalid">x</a>', b'<a href="rv32.html#gprs">x</a>',
                    b'<a href="rv32.html#gprs" class="xref page" onclick="x()">x</a>', b"<script>x()</script>",
                    b"<img src=x>", b'<em class="x">y</em>'):
            spans = dict(self.spans); spans[name] = span(name, bad)
            with self.subTest(bad=bad), self.assertRaises(R.RetentionError):
                self.rebuilt_emit(spans=spans)

    def test_retained_bound_is_inclusive(self):
        size = len(self.emit())
        with patch.object(R, "RETAINED_BYTES", size):
            self.assertEqual(len(self.emit()), size)
        with patch.object(R, "RETAINED_BYTES", size - 1), self.assertRaises(R.RetentionError):
            self.emit()

    def test_verification_needs_no_acquired_pages(self):
        root = self.temporary_root()
        data = self.emit()
        self.install(root, data)
        self.assertFalse((root / ".materials").exists())
        with patch.object(R, "RETAINED_SHA", sha(data)):
            pin = R.verify_retained(root)
        self.assertEqual((pin.disposition, pin.byte_size, pin.sha256), ("matched", len(data), sha(data)))

    def test_retained_change_is_not_success(self):
        root = self.temporary_root()
        data = self.emit()
        self.install(root, data + b"changed")
        with patch.object(R, "RETAINED_SHA", sha(data)):
            self.assertEqual(R.verify_retained(root).disposition, "mismatch")

    def test_retained_missing_is_unavailable(self):
        self.assertEqual(R.verify_retained(self.temporary_root()).disposition, "unavailable")

    def test_retained_symlink_refuses(self):
        root = self.temporary_root()
        path = self.install(root, self.emit())
        path.rename(path.with_suffix(".other"))
        path.symlink_to(path.with_suffix(".other").name)
        self.assertEqual(R.verify_retained(root).disposition, "refused")

    def test_real_tree_retained_file_verifies_offline(self):
        """The tracked excerpt authenticates by its pinned digest with no acquired page."""
        pin = R.verify_retained(ROOT)
        self.assertEqual(pin.disposition, "matched", pin.reason)
        self.assertEqual(pin.sha256, R.RETAINED_SHA)


def main():
    global R
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/retain_rv64i_statements.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_rv64i_statements")
        module.__file__ = str(path)
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        R = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(RetentionTests))
    print(f"RV64I-STATEMENT-RETENTION: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic curation controls, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
