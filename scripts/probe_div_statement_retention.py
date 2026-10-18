#!/usr/bin/env python3
"""Cache-free synthetic controls for licensed DIV statement curation."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import retain_div_statement as R

ROOT = Path(__file__).resolve().parent.parent
MUTATIONS = {
    "input-pins": ("hashlib.sha256(data).hexdigest() == digest", "True"),
    "input-bounds": ("1 <= len(data) <= limit", "True"),
    "licence-statement": ("LICENCE_STATEMENT in licence", "True"),
    "unique-statement": ("source.count(MARKER) == 1", "True"),
    "closing-span": ("end >= 0", "True"),
    "span-bound": ("len(span) <= SPAN_BYTES", "True"),
    "retained-bound": ("len(retained) <= RETAINED_BYTES", "True"),
    "exact-span": ('span = source[start : end + len(b"</span>")]', 'span = b""'),
    "retained-pin": ("digest=RETAINED_SHA", "digest=SOURCE_SHA"),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.span = (
            R.MARKER
            + b"synthetic signed <code>rs1</code> quotient; unchanged whitespace\n"
            + b"</span>"
        )
        self.source = (
            b"<script>excluded()</script>before"
            + self.span
            + b"after<nav>excluded</nav>"
        )
        self.licence = b"synthetic preface before\n" + R.LICENCE_STATEMENT + b"\nafter"
        for name, value in (
            ("SOURCE_SHA", sha(self.source)),
            ("LICENCE_SHA", sha(self.licence)),
        ):
            context = patch.object(R, name, value)
            context.start()
            self.addCleanup(context.stop)

    def emit(self):
        return R.retain_statement(self.source, self.licence)

    def temporary_root(self):
        base = ROOT / "target/div-statement-retention-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def install(self, root, data):
        path = root / R.RETAINED_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_exact_quote_without_unselected_site_bytes(self):
        result = self.emit()
        self.assertEqual(result.count(self.span), 1)
        self.assertNotIn(b"excluded", result)
        self.assertNotIn(b"<script", result)
        self.assertNotIn(b"<nav", result)

    def test_attribution_and_both_original_identities(self):
        result = self.emit()
        for text in (
            R.SOURCE_URL,
            R.SOURCE_SHA,
            R.LICENCE_URL,
            R.LICENCE_SHA,
            "https://creativecommons.org/licenses/by/4.0/",
            "RISC-V International",
            "Copyright © RISC-V International",
            "quoted span is unmodified",
            "wrapper",
        ):
            with self.subTest(text=text):
                self.assertIn(text.encode(), result)

    def test_source_change_outside_quote_refuses(self):
        with self.assertRaises(R.RetentionError):
            R.retain_statement(self.source + b"changed", self.licence)

    def test_licence_change_outside_statement_refuses(self):
        with self.assertRaises(R.RetentionError):
            R.retain_statement(self.source, self.licence + b"changed")

    def test_source_bound_is_inclusive(self):
        with patch.object(R, "SOURCE_BYTES", len(self.source)):
            self.emit()
        with patch.object(R, "SOURCE_BYTES", len(self.source) - 1), self.assertRaises(
            R.RetentionError
        ):
            self.emit()

    def test_licence_bound_is_inclusive(self):
        with patch.object(R, "LICENCE_BYTES", len(self.licence)):
            self.emit()
        with patch.object(R, "LICENCE_BYTES", len(self.licence) - 1), self.assertRaises(
            R.RetentionError
        ):
            self.emit()

    def test_input_types_refuse(self):
        for bad in (None, True, "text", bytearray(self.source)):
            with self.subTest(bad=type(bad)), self.assertRaises(R.RetentionError):
                R.retain_statement(bad, self.licence)
            with self.subTest(bad=type(bad)), self.assertRaises(R.RetentionError):
                R.retain_statement(self.source, bad)

    def test_empty_inputs_refuse(self):
        for which in ("SOURCE_SHA", "LICENCE_SHA"):
            with patch.object(R, which, sha(b"")), self.assertRaises(R.RetentionError):
                R.retain_statement(
                    b"" if which == "SOURCE_SHA" else self.source,
                    b"" if which == "LICENCE_SHA" else self.licence,
                )

    def test_missing_licence_statement_refuses_even_with_fixture_pin(self):
        data = b"synthetic preface without terms"
        with patch.object(R, "LICENCE_SHA", sha(data)), self.assertRaises(
            R.RetentionError
        ):
            R.retain_statement(self.source, data)

    def test_missing_target_refuses_even_with_fixture_pin(self):
        data = b"synthetic source without target"
        with patch.object(R, "SOURCE_SHA", sha(data)), self.assertRaises(
            R.RetentionError
        ):
            R.retain_statement(data, self.licence)

    def test_duplicate_target_refuses_even_with_fixture_pin(self):
        data = self.source + self.span
        with patch.object(R, "SOURCE_SHA", sha(data)), self.assertRaises(
            R.RetentionError
        ):
            R.retain_statement(data, self.licence)

    def test_unterminated_target_refuses(self):
        data = R.MARKER + b"synthetic unterminated target"
        with patch.object(R, "SOURCE_SHA", sha(data)), self.assertRaises(
            R.RetentionError
        ):
            R.retain_statement(data, self.licence)

    def test_span_bound_is_inclusive(self):
        with patch.object(R, "SPAN_BYTES", len(self.span)):
            self.emit()
        with patch.object(R, "SPAN_BYTES", len(self.span) - 1), self.assertRaises(
            R.RetentionError
        ):
            self.emit()

    def test_output_bound_is_inclusive(self):
        size = len(self.emit())
        with patch.object(R, "RETAINED_BYTES", size):
            self.emit()
        with patch.object(R, "RETAINED_BYTES", size - 1), self.assertRaises(
            R.RetentionError
        ):
            self.emit()

    def test_quote_utf8_is_preserved(self):
        span = R.MARKER + "synthetic quotient −3\n".encode() + b"</span>"
        with patch.object(R, "SOURCE_SHA", sha(span)):
            self.assertIn(span, R.retain_statement(span, self.licence))

    def test_invalid_quote_utf8_refuses(self):
        data = R.MARKER + b"\xff</span>"
        with patch.object(R, "SOURCE_SHA", sha(data)), self.assertRaises(UnicodeError):
            R.retain_statement(data, self.licence)

    def test_verification_needs_no_acquired_pages(self):
        root = self.temporary_root()
        data = self.emit()
        self.install(root, data)
        self.assertFalse((root / ".materials").exists())
        with patch.object(R, "RETAINED_SHA", sha(data)):
            pin = R.verify_retained(root)
        self.assertEqual(pin.disposition, "matched")
        self.assertEqual(pin.byte_size, len(data))
        self.assertEqual(pin.sha256, sha(data))

    def test_retained_change_is_not_success(self):
        root = self.temporary_root()
        data = self.emit()
        self.install(root, data + b"changed")
        with patch.object(R, "RETAINED_SHA", sha(data)):
            self.assertEqual(R.verify_retained(root).disposition, "mismatch")

    def test_retained_missing_is_unavailable(self):
        self.assertEqual(
            R.verify_retained(self.temporary_root()).disposition, "unavailable"
        )

    def test_retained_symlink_refuses(self):
        root = self.temporary_root()
        path = self.install(root, self.emit())
        path.rename(path.with_suffix(".other"))
        path.symlink_to(path.with_suffix(".other").name)
        self.assertEqual(R.verify_retained(root).disposition, "refused")


def main():
    global R
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/retain_div_statement.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_div_statement")
        module.__file__ = str(path)
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        R = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(RetentionTests)
    )
    print(
        f"DIV-STATEMENT-RETENTION: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; synthetic curation controls, no capture credit"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
