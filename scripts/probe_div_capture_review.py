#!/usr/bin/env python3
"""Synthetic, cache-independent controls for the first DIV dependency review."""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import review_div_capture as R
import matched_gpr_property as P
import retain_div_statement as Retain
import capture_div as A

ROOT = Path(__file__).resolve().parent.parent
MUTATIONS = {
    "module-population": ("seen == set(reviewed)", "True", 1),
    "dynamic-import": (
        'called\n                    not in {"__import__", "import_module", "spec_from_file_location"}',
        "True",
        1,
    ),
    "external-import": ("base in REVIEWED_EXTERNALS", "True", 1),
    "data-population": ("set(observed) == DATA_PATHS", "True", 1),
    "child-bound": ("len(paths) <= 64", "True", 1),
    "symlink": ("path.lstat()", "path.stat()", 2),
    "git-boundary": ('not os.path.lexists(path / ".git")', "True", 1),
    "file-bound": ("0 <= info.st_size <= FILE_BYTES", "True", 1),
    "aggregate-bound": ("self.total + info.st_size <= TOTAL_BYTES", "True", 1),
    "byte-recheck": ("self.read(path) == data", "True", 1),
    "retained-identity": (
        "(primary.role, primary.input_id, primary.path, primary.sha256)\n"
        '        == ("normative-source", "RVI-M-DIV-STATEMENT", PRIMARY, Retain.RETAINED_SHA)',
        "True",
        1,
    ),
    "publication-authority": (
        'case.authority.source_id == "RVI-M"\n'
        "        and case.authority.source_sha256 == Retain.SOURCE_SHA",
        "True",
        1,
    ),
    "retained-pin": ("hashlib.sha256(data).hexdigest() == primary.sha256", "True", 1),
    "authority-declaration": ("set(A.VIEW_PATHS) == AUTHORITY_PATHS", "True", 1),
    "authority-preopen": ("relative in AUTHORITY_PATHS", "True", 1),
    "authority-readonly": ('not any(flag in mode for flag in "wax+")', "True", 1),
    "authority-view-pin": (
        'type(view.byte_size) is int\n'
        '            and view.byte_size == len(snapshots.data[view.path])\n'
        '            and view.sha256 == hashlib.sha256(snapshots.data[view.path]).hexdigest()\n'
        '            and view.role == expected_role',
        "True", 1,
    ),
    "authority-process": (
        'subprocess, "Popen", denied_process',
        'subprocess, "Popen", subprocess.Popen', 1,
    ),
}


class ReviewTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/div-capture-review-controls"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "scripts").mkdir()

    def write(self, path, data):
        location = self.root / path
        location.parent.mkdir(parents=True, exist_ok=True)
        location.write_bytes(data)

    def census(self, source, *, reviewed=frozenset({"entry"})):
        self.write("scripts/entry.py", source)
        return R.import_census(
            R.Snapshots(self.root), roots={"entry"}, reviewed=reviewed
        )

    def test_import_graph_includes_function_local_edges(self):
        self.write("scripts/child.py", b"from pathlib import Path\n")
        names, edges, external = self.census(
            b"import json\ndef f():\n import child\n", reviewed={"entry", "child"}
        )
        self.assertEqual(names, ("child", "entry"))
        self.assertEqual(edges, (("entry", "child"),))
        self.assertEqual(external, ("json", "pathlib"))

    def test_extra_project_import_refuses(self):
        self.write("scripts/child.py", b"pass\n")
        with self.assertRaises(R.ReviewError):
            self.census(b"import child\n")

    def test_absent_reviewed_module_refuses(self):
        with self.assertRaises(R.ReviewError):
            self.census(b"pass\n", reviewed={"entry", "unused"})

    def test_relative_import_refuses(self):
        with self.assertRaises(R.ReviewError):
            self.census(b"from . import child\n")

    def test_dynamic_import_refuses(self):
        for source in (b"__import__('json')\n", b"loader.import_module('json')\n"):
            with self.subTest(source=source), self.assertRaises(R.ReviewError):
                self.census(source)

    def test_unknown_external_refuses(self):
        with self.assertRaises(R.ReviewError):
            self.census(b"import unreviewed_dependency\n")

    def test_local_package_cannot_hide_as_standard_library(self):
        (self.root / "scripts/json").mkdir()
        self.write("scripts/json/__init__.py", b"pass\n")
        with self.assertRaises(R.ReviewError):
            self.census(b"import json\n")

    def test_module_bound_is_inclusive(self):
        self.write("scripts/child.py", b"pass\n")
        with patch.object(R, "MODULE_LIMIT", 2):
            self.census(b"import child\n", reviewed={"entry", "child"})
        with patch.object(R, "MODULE_LIMIT", 1), self.assertRaises(R.ReviewError):
            self.census(b"import child\n", reviewed={"entry", "child"})

    def test_data_population_exact_order_independent(self):
        R.check_data_population(
            [*reversed(sorted(R.DATA_PATHS)), *sorted(R.DATA_PATHS)]
        )

    def test_missing_data_refuses(self):
        with self.assertRaises(R.ReviewError):
            R.check_data_population(sorted(R.DATA_PATHS)[1:])

    def test_extra_data_refuses(self):
        with self.assertRaises(R.ReviewError):
            R.check_data_population([*R.DATA_PATHS, "schema/unreviewed.sexp"])

    def test_child_population_and_inclusive_bound(self):
        children = R.child_paths(R.REVIEWED_MODULES)
        self.assertEqual(len(children), 64)
        self.assertFalse(set(children) & R.PRINCIPAL_CODE)
        self.assertIn(R.SELF, children)
        self.assertIn(R.PRIMARY, children)
        self.assertIn("retain_div_statement", R.ROOT_MODULES)
        self.assertIn("scripts/retain_div_statement.py", children)
        self.assertIn("capture_div", R.ROOT_MODULES)
        self.assertEqual(len(R.child_paths(R.REVIEWED_MODULES - {"capture_div"})), 63)
        with self.assertRaises(R.ReviewError):
            R.child_paths(R.REVIEWED_MODULES | {"extra_a"})

    def authority_fixture(self):
        """Use current tracked views; substitute only the public owner's action."""
        snapshots = R.Snapshots(ROOT)
        for path in R.AUTHORITY_PATHS:
            snapshots.pin(path)
        context = A.review_authorities()

        def owner(*args, **kwargs):
            for path in sorted(R.AUTHORITY_PATHS):
                with (ROOT / path).open("rb") as stream:
                    stream.read(1)
            return context

        return snapshots, context, owner

    def test_authority_declaration_population_is_checked_before_owner_call(self):
        snapshots, _, owner = self.authority_fixture()
        with patch.object(A, "VIEW_PATHS", (*A.VIEW_PATHS, "extra")), \
                patch.object(A, "review_authorities", side_effect=owner) as invoked:
            with self.assertRaises(R.ReviewError):
                R.exercise_authorities(snapshots)
            invoked.assert_not_called()

    def test_unknown_authority_open_refuses_before_the_real_open(self):
        snapshots, _, owner = self.authority_fixture()
        unknown = self.root / "unreviewed"
        unknown.write_bytes(b"owned unknown data")
        snapshots.pin(unknown.relative_to(ROOT).as_posix())
        opened = []
        original = Path.open

        def observed(path, *args, **kwargs):
            opened.append(Path(path))
            return original(path, *args, **kwargs)

        def extra_owner(*args, **kwargs):
            with unknown.open("rb") as stream:
                stream.read(1)
            return owner()

        with patch.object(Path, "open", observed), \
                patch.object(A, "review_authorities", side_effect=extra_owner):
            with self.assertRaises(R.ReviewError):
                R.exercise_authorities(snapshots)
        self.assertNotIn(unknown, opened)

    def test_contradictory_authority_view_pin_refuses(self):
        snapshots, context, owner = self.authority_fixture()
        view = replace(context.views[0], sha256="0" * 64)
        changed = replace(context, views=(view, *context.views[1:]))

        def wrong_owner(*args, **kwargs):
            owner()
            return changed

        with patch.object(A, "review_authorities", side_effect=wrong_owner), \
                self.assertRaises(R.ReviewError):
            R.exercise_authorities(snapshots)

    def test_authority_write_mode_refuses_before_the_real_open(self):
        snapshots, context, owner = self.authority_fixture()
        original = Path.open
        write_opens = []

        def observed(path, mode="r", *args, **kwargs):
            if any(flag in mode for flag in "wax+"):
                write_opens.append(Path(path))
                # Observe a forbidden delegation without modifying tracked data.
                mode = "rb"
            return original(path, mode, *args, **kwargs)

        def writing_owner(*args, **kwargs):
            with (ROOT / sorted(R.AUTHORITY_PATHS)[0]).open("r+b"):
                pass
            return owner()

        with patch.object(Path, "open", observed), \
                patch.object(A, "review_authorities", side_effect=writing_owner):
            with self.assertRaises(R.ReviewError):
                R.exercise_authorities(snapshots)
        self.assertEqual(write_opens, [])

    def test_malformed_authority_view_fact_refuses_without_attribute_error(self):
        snapshots, context, owner = self.authority_fixture()
        changed = replace(context, views=(None, *context.views[1:]))

        def wrong_owner(*args, **kwargs):
            owner()
            return changed

        with patch.object(A, "review_authorities", side_effect=wrong_owner), \
                self.assertRaises(R.ReviewError):
            R.exercise_authorities(snapshots)

    def test_authority_process_attempt_refuses_before_launch(self):
        snapshots, context, owner = self.authority_fixture()

        def process_owner(*args, **kwargs):
            owner()
            process = subprocess.Popen(
                [sys.executable, "-c", "pass"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            process.communicate(timeout=10)
            return context

        with patch.object(A, "review_authorities", side_effect=process_owner), \
                self.assertRaises(R.ReviewError):
            R.exercise_authorities(snapshots)

    def retained_case(self, data):
        case = P.signed_division_case()
        pin = replace(case.required_inputs[0], sha256=hashlib.sha256(data).hexdigest())
        return replace(case, required_inputs=(pin,))

    def test_retained_identity_and_population_are_exact(self):
        data = b"synthetic retained statement"
        case = self.retained_case(data)
        with patch.object(Retain, "RETAINED_SHA", case.required_inputs[0].sha256):
            R.check_retained_input(case, data)
            for change in [
                dict(role="implementation"),
                dict(input_id="RVI-M"),
                dict(path="other/statement.html"),
                dict(sha256="a" * 64),
            ]:
                with self.subTest(change=change), self.assertRaises(R.ReviewError):
                    R.check_retained_input(
                        replace(
                            case,
                            required_inputs=(
                                replace(case.required_inputs[0], **change),
                            ),
                        ),
                        data,
                    )
            for pins in [(), case.required_inputs * 2]:
                with self.subTest(count=len(pins)), self.assertRaises(R.ReviewError):
                    R.check_retained_input(replace(case, required_inputs=pins), data)

    def test_original_publication_authority_cannot_be_replaced_by_excerpt(self):
        data = b"synthetic retained statement"
        case = self.retained_case(data)
        with patch.object(Retain, "RETAINED_SHA", case.required_inputs[0].sha256):
            for change in [
                dict(source_id="RVI-M-DIV-STATEMENT"),
                dict(source_sha256=case.required_inputs[0].sha256),
            ]:
                with self.subTest(change=change), self.assertRaises(R.ReviewError):
                    R.check_retained_input(
                        replace(case, authority=replace(case.authority, **change)), data
                    )

    def test_changed_retained_bytes_refuse(self):
        data = b"synthetic retained statement"
        case = self.retained_case(data)
        with patch.object(
            Retain, "RETAINED_SHA", case.required_inputs[0].sha256
        ), self.assertRaises(R.ReviewError):
            R.check_retained_input(case, data + b" changed")

    def test_read_and_recheck(self):
        self.write("input", b"checked")
        snapshots = R.Snapshots(self.root)
        self.assertEqual(snapshots.pin("input"), b"checked")
        self.assertEqual(snapshots.total, 7)
        self.assertEqual(snapshots.pin("input"), b"checked")
        self.assertEqual(snapshots.total, 7)
        snapshots.recheck()
        self.assertEqual(snapshots.total, 7)

    def test_changed_reviewed_bytes_refuse(self):
        self.write("input", b"before")
        snapshots = R.Snapshots(self.root)
        snapshots.pin("input")
        self.write("input", b"after!")
        with self.assertRaises(R.ReviewError):
            snapshots.recheck()

    def test_file_bound_is_inclusive(self):
        self.write("input", b"abcd")
        with patch.object(R, "FILE_BYTES", 4):
            self.assertEqual(R.Snapshots(self.root).pin("input"), b"abcd")
        with patch.object(R, "FILE_BYTES", 3), self.assertRaises(R.ReviewError):
            R.Snapshots(self.root).pin("input")

    def test_aggregate_bound_is_inclusive(self):
        self.write("one", b"123")
        self.write("two", b"456")
        with patch.object(R, "TOTAL_BYTES", 6):
            snapshots = R.Snapshots(self.root)
            snapshots.pin("one")
            snapshots.pin("two")
        with patch.object(R, "TOTAL_BYTES", 5):
            snapshots = R.Snapshots(self.root)
            snapshots.pin("one")
            with self.assertRaises(R.ReviewError):
                snapshots.pin("two")

    def test_noncanonical_paths_refuse(self):
        for path in (
            "../other",
            "/outside",
            "a/./b",
            "a//b",
            "a\\b",
            "a:b",
            "a\nb",
            "",
        ):
            with self.subTest(path=path), self.assertRaises(R.ReviewError):
                R.Snapshots(self.root).pin(path)

    def test_symlink_file_refuses(self):
        self.write("input", b"checked")
        (self.root / "link").symlink_to("input")
        with self.assertRaises(R.ReviewError):
            R.Snapshots(self.root).pin("link")

    def test_symlink_parent_refuses(self):
        self.write("directory/input", b"checked")
        (self.root / "link").symlink_to("directory", target_is_directory=True)
        with self.assertRaises(R.ReviewError):
            R.Snapshots(self.root).pin("link/input")

    def test_nested_git_marker_refuses(self):
        self.write("directory/input", b"checked")
        # Even a dangling marker revokes this diagnostic's traversal authority.
        (self.root / "directory/.git").symlink_to("missing")
        with self.assertRaises(R.ReviewError):
            R.Snapshots(self.root).pin("directory/input")

    def test_directory_input_refuses(self):
        with self.assertRaises(R.ReviewError):
            R.Snapshots(self.root).pin("scripts")

    def test_missing_input_is_unavailable(self):
        with self.assertRaises(FileNotFoundError):
            R.Snapshots(self.root).pin("missing")


def main():
    global R
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        source = (ROOT / "scripts/review_div_capture.py").read_text()
        before, after, count = MUTATIONS[args.mutation]
        if source.count(before) != count:
            raise RuntimeError(
                "mutation no longer selects its exact reviewed guard population"
            )
        module = types.ModuleType("mutated_div_capture_review")
        module.__file__ = str(ROOT / "scripts/review_div_capture.py")
        exec(
            compile(source.replace(before, after), module.__file__, "exec"),
            module.__dict__,
        )
        R = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ReviewTests)
    )
    print(
        f"DIV-CAPTURE-REVIEW: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; synthetic population controls, no capture credit"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
