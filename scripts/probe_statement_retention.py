#!/usr/bin/env python3
"""Cache-free synthetic controls for the retained-statement table (`scripts/retain_statements.py`, P4-SYSTEM.14 a43b-3b)."""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest

import retain_statements as R

ROOT = Path(__file__).resolve().parent.parent
MUTATIONS = {
    "input-pins": ('    pinned(source, PAGE_BYTES, excerpt.source.sha256, excerpt.source.input_id)\n', ''),
    "licence-pins": ('    pinned(licence, LICENCE_BYTES, excerpt.licence.sha256, "licence evidence")\n', ''),
    "licence-statement": ('require(LICENCE_STATEMENT in licence, ', 'require(True, '),
    "unique-statement": ('require(source.count(marker) == 1, ', 'require(True, '),
    "closing-span": ('require(end >= 0, f"{name}: statement is unterminated")', 'require(True, f"{name}: statement is unterminated")'),
    "span-bound": ('require(len(span) <= SPAN_BYTES, ', 'require(True, '),
    "span-markup": ('any(shape.fullmatch(tag) for shape in OPENING_TAGS)', 'True'),
    "retained-bound": ('require(len(retained) <= RETAINED_BYTES, ', 'require(True, '),
    "retained-pin": ("digest=excerpt.retained_sha256", "digest=excerpt.source.sha256"),
}
XREF = b'<a href="hypervisor.html#sec:hcauses" class="xref page">Trap Cause Codes</a>'
NAMES = (("norm:first", "§1"), ("norm:second", "§1"), ("norm:third", "§2"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def span(name, text=b"synthetic <em>CSR</em> <code>csr[11:10]</code> statement, unchanged whitespace\n"):
    return b'<span id="' + name.encode() + b'">' + text + b"</span>"


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.spans = {name: span(name) for name, _ in NAMES}
        self.spans[NAMES[0][0]] = span(NAMES[0][0], b"see " + XREF + b".")
        self.licence = b"synthetic preface before\n" + R.LICENCE_STATEMENT + b"\nafter"
        self.build()

    def build(self, *, spans=None, extra=b""):
        spans = self.spans if spans is None else spans
        self.source = (b"<script>excluded()</script>before" + span("norm:unselected")
                       + b"between".join(spans.values()) + b"<nav>excluded</nav>" + extra + b"after")
        self.excerpt = R.Excerpt("SYNTHETIC-STATEMENTS", "A synthetic heading",
                                 R.Page("SYNTHETIC", "priv/synthetic.html", sha(self.source), "a synthetic page"),
                                 R.Page("SYNTHETIC-LICENCE", "priv/preface.html", sha(self.licence), "a synthetic preface"),
                                 "profiles/synthetic/retained/statements.html", "0" * 64, NAMES,
                                 "This excerpt establishes no acceptance.")

    def emit(self):
        return R.retain_statements(self.excerpt, self.source, self.licence)

    def rebuilt_emit(self, **kwargs):
        self.build(**kwargs)
        return self.emit()

    def temporary_root(self):
        base = ROOT / "target/statement-retention-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def install(self, root, data):
        path = root / self.excerpt.retained_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_exact_quotes_without_unselected_site_bytes(self):
        out = self.emit()
        for name, quoted in self.spans.items():
            self.assertEqual(out.count(quoted), 1, name)
        for excluded in (b"<script", b"excluded()", b"<nav", b"between", b"before", b"after<", b"norm:unselected"):
            self.assertNotIn(excluded, out)

    def test_statements_stay_in_the_rows_order(self):
        out = self.emit()
        self.assertLess(out.index(self.spans["norm:first"]), out.index(self.spans["norm:second"]))
        self.assertLess(out.index(self.spans["norm:second"]), out.index(self.spans["norm:third"]))

    def test_attribution_names_the_original_publication_once(self):
        out = self.emit().decode()
        for needle in ("CC BY 4.0", "Copyright © RISC-V International", self.excerpt.licence.sha256,
                       "scripts/retain_statements.py", "This excerpt establishes no acceptance."):
            self.assertIn(needle, out)
        # The one publication a case's excerpt is bound to (review_div_capture.PUBLICATION, a44-2c).
        self.assertEqual(out.count("Original page SHA256: <code>" + self.excerpt.source.sha256 + "</code>"), 1)

    def test_output_is_deterministic(self):
        self.assertEqual(self.emit(), self.emit())

    def test_source_change_refuses(self):
        with self.assertRaises(R.RetentionError):
            R.retain_statements(self.excerpt, self.source + b"x", self.licence)

    def test_licence_change_refuses(self):
        with self.assertRaises(R.RetentionError):
            R.retain_statements(self.excerpt, self.source, self.licence + b"x")

    def test_missing_licence_statement_refuses_even_with_a_matching_pin(self):
        licence = b"synthetic preface without the statement"
        excerpt = replace(self.excerpt, licence=replace(self.excerpt.licence, sha256=sha(licence)))
        with self.assertRaises(R.RetentionError):
            R.retain_statements(excerpt, self.source, licence)

    def test_each_missing_statement_refuses(self):
        for name in dict(NAMES):
            with self.subTest(name=name), self.assertRaises(R.RetentionError):
                self.rebuilt_emit(spans={k: v for k, v in self.spans.items() if k != name})

    def test_duplicate_statement_refuses(self):
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(extra=span(NAMES[0][0]))

    def test_unterminated_statement_refuses(self):
        """The last statement in source order with no closing span anywhere after it."""
        name = NAMES[-1][0]
        spans = dict(self.spans); spans[name] = b'<span id="' + name.encode() + b'">no end'
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(spans=spans)

    def test_nested_span_refuses(self):
        """A nested span is unreviewed markup: the allowlist refuses it (no separate guard)."""
        name = NAMES[1][0]
        spans = dict(self.spans); spans[name] = span(name, b"outer <span id=\"x\">inner")
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(spans=spans)

    def test_span_bound_is_inclusive(self):
        name = NAMES[1][0]
        overhead = len(span(name, b""))
        fits = dict(self.spans); fits[name] = span(name, b"x" * (R.SPAN_BYTES - overhead))
        self.assertIn(fits[name], self.rebuilt_emit(spans=fits))
        over = dict(self.spans); over[name] = span(name, b"x" * (R.SPAN_BYTES - overhead + 1))
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(spans=over)

    def test_only_the_reviewed_markup_is_retained(self):
        """Emphasis, code and the manual's own same-publication cross-reference pass; anything else refuses."""
        name = NAMES[1][0]
        for bad in (b'<a href="https://example.invalid">x</a>', b'<a href="rv32.html#gprs">x</a>',
                    b'<a href="rv32.html#gprs" class="xref page" onclick="x()">x</a>', b"<script>x()</script>",
                    b"<img src=x>", b'<em class="x">y</em>'):
            spans = dict(self.spans); spans[name] = span(name, bad)
            with self.subTest(bad=bad), self.assertRaises(R.RetentionError):
                self.rebuilt_emit(spans=spans)

    def test_retained_bound_is_inclusive(self):
        original = R.RETAINED_BYTES
        self.addCleanup(setattr, R, "RETAINED_BYTES", original)
        size = len(self.emit())
        R.RETAINED_BYTES = size
        self.assertEqual(len(self.emit()), size)
        R.RETAINED_BYTES = size - 1
        with self.assertRaises(R.RetentionError):
            self.emit()

    def test_verification_needs_no_acquired_pages(self):
        root = self.temporary_root()
        data = self.emit()
        self.install(root, data)
        self.assertFalse((root / ".materials").exists())
        pin = R.verify_retained(replace(self.excerpt, retained_sha256=sha(data)), root)
        self.assertEqual((pin.disposition, pin.byte_size, pin.sha256), ("matched", len(data), sha(data)))

    def test_retained_change_is_not_success(self):
        root = self.temporary_root()
        data = self.emit()
        self.install(root, data + b"changed")
        self.assertEqual(R.verify_retained(replace(self.excerpt, retained_sha256=sha(data)), root).disposition, "mismatch")

    def test_retained_missing_is_unavailable(self):
        self.assertEqual(R.verify_retained(self.excerpt, self.temporary_root()).disposition, "unavailable")

    def test_retained_symlink_refuses(self):
        root = self.temporary_root()
        data = self.emit()
        path = self.install(root, data)
        path.rename(path.with_suffix(".other"))
        path.symlink_to(path.with_suffix(".other").name)
        self.assertEqual(R.verify_retained(replace(self.excerpt, retained_sha256=sha(data)), root).disposition, "refused")

    def test_real_tree_excerpts_verify_offline(self):
        """Each tracked excerpt authenticates by its pinned digest with no acquired page, under its own row's path."""
        self.assertTrue(R.EXCERPTS)
        for excerpt in R.EXCERPTS.values():
            with self.subTest(excerpt=excerpt.input_id):
                pin = R.verify_retained(excerpt, ROOT)
                self.assertEqual(pin.disposition, "matched", pin.reason)
                self.assertEqual(pin.sha256, excerpt.retained_sha256)
                self.assertNotEqual(excerpt.retained_sha256, excerpt.source.sha256)


def main():
    global R
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/retain_statements.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_retain_statements")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module  # dataclasses resolve their module while the copy executes
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        R = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(RetentionTests))
    print(f"STATEMENT-RETENTION: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic curation controls, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
