#!/usr/bin/env python3
"""Dossier-qualification controls (P4-SYSTEM.14 a42bc): a verification-bearing experiment record in a
dossier is qualified only through a CURRENT credit record naming its case and form-equality with the case's
measured record. The credit decides, never the record. Real-tree arms pin the credited case; synthetic arms
copy it and break one thing at a time."""
from __future__ import annotations

import argparse
import copy
import importlib.util
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "scripts" / "sexp.py").is_file())
sys.path.insert(0, str(ROOT / "scripts"))
import sexp as S  # noqa: E402

MUTATION = None
# Each seam replaces one load-bearing predicate in a copied module; its test must then fail.
SEAMS = {
    "credit-any": ('    current = [c for c in naming if c["disposition"] == "current"]\n',
                   '    current = list(naming)\n'),
    "mirror-any": ('    elif measured[0] != form:\n', '    elif False:\n'),
    "id-any": ('    naming = [c for c in current_credits(root, profile_dir) if c["case_id"] == xid]\n',
               '    naming = list(current_credits(root, profile_dir))\n'),
}
MUTATION_TESTS = {
    "credit-any": "test_a_lapsed_credit_does_not_qualify",
    "mirror-any": "test_a_record_differing_from_the_measured_one_does_not_qualify",
    "id-any": "test_an_uncredited_case_does_not_qualify",
}
UNIT = "rv64gc-lab-v0"
CASE = "rv64gc-m-forms-v3"


def load_module(source: Path, name: str):
    text = source.read_text()
    if MUTATION:
        old, new = SEAMS[MUTATION]
        if text.count(old) != 1:
            raise RuntimeError("singular seam required: " + MUTATION)
        text = text.replace(old, new, 1)
    spec = importlib.util.spec_from_file_location(name, str(source), loader=None)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(source)
    exec(compile(text, str(source), "exec"), module.__dict__)  # noqa: S102 — a copied project module under test
    return module


class DossierQualificationTests(unittest.TestCase):
    """A scratch root mirrors the real unit's credits and the case's records; the real tree is read, never written."""

    def setUp(self):
        base = ROOT / "target" / "doctrine-selftest"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        # the credit module refuses a linked pin target ("not a regular file"), so every pinned path is a
        # COPY: the unit directory, the case, the schemas and each path the case's dependency manifest names;
        # the other profiles and top-level entries are links the credit never reads. The real tree is read,
        # never written.
        unit_src, case_src = ROOT / "profiles" / UNIT, ROOT / "evidence" / CASE
        pinned = set()
        for text_path in (unit_src / "credits.sexp", case_src / "dependencies.sexp"):
            for form in S.read_file(text_path):
                stack = [form]
                while stack:
                    f = stack.pop()
                    if isinstance(f, list):
                        if f and f[0] == "path" and len(f) == 2 and isinstance(f[1], str):
                            pinned.add(f[1])
                        stack.extend(c for c in f if isinstance(c, list))
        for entry in ROOT.iterdir():
            if entry.name not in ("profiles", "evidence", "schema", "target", ".git") and not any(
                    pin.startswith(entry.name + "/") for pin in pinned):
                (self.root / entry.name).symlink_to(entry)
        for pin in sorted(pinned):
            source = ROOT / pin
            if source.is_file() and not pin.startswith(("profiles/" + UNIT + "/", "evidence/" + CASE + "/", "schema/")):
                (self.root / pin).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(source, self.root / pin)
        shutil.copytree(ROOT / "schema", self.root / "schema")
        (self.root / "profiles").mkdir(exist_ok=True)
        for unit_dir in (ROOT / "profiles").iterdir():
            if unit_dir.name != UNIT:
                (self.root / "profiles" / unit_dir.name).symlink_to(unit_dir)
        self.profile = self.root / "profiles" / UNIT
        shutil.copytree(unit_src, self.profile)
        (self.root / "evidence").mkdir(exist_ok=True)
        for case_dir in (ROOT / "evidence").iterdir():
            if case_dir.name != CASE:
                (self.root / "evidence" / case_dir.name).symlink_to(case_dir)
        self.case = self.root / "evidence" / CASE
        shutil.copytree(case_src, self.case)
        self.cr = load_module(ROOT / "scripts" / "credit_records.py", "credit_records_under_test")
        self.measured = [f for f in S.read_file(self.case / "measured-experiment.sexp")
                         if isinstance(f, list) and f and str(f[0]) == "experiment"][0]

    def qualification(self, form, root=None):
        return self.cr.dossier_qualification(root or self.root, (root or self.root) / "profiles" / UNIT, form)

    def test_the_credited_case_qualifies_on_the_real_tree(self):
        real = [f for f in S.read_file(ROOT / "evidence" / CASE / "measured-experiment.sexp")
                if isinstance(f, list) and f and str(f[0]) == "experiment"][0]
        self.assertEqual(self.qualification(real, ROOT), [])

    def test_the_credited_case_qualifies_in_the_mirror_root(self):
        self.assertEqual(self.qualification(self.measured), [])

    def test_an_uncredited_case_does_not_qualify(self):
        other = copy.deepcopy(self.measured)
        other[1] = [S.Symbol("id"), "rv64gc-nobody-credited-this"]
        why = self.qualification(other)
        self.assertEqual(len(why), 2, why)
        self.assertIn("no credit record names the case rv64gc-nobody-credited-this", why[0])
        self.assertIn("no measured record", why[1])

    def test_a_record_differing_from_the_measured_one_does_not_qualify(self):
        changed = copy.deepcopy(self.measured)
        idx = next(i for i, c in enumerate(changed) if isinstance(c, list) and c and c[0] == "instructions")
        changed[idx] = [S.Symbol("instructions"), 34]
        self.assertEqual(self.qualification(changed), ["the dossier record differs from the case's measured record"])

    def test_a_lapsed_credit_does_not_qualify(self):
        policy = self.profile / "EVIDENCE_POLICY.md"
        policy.write_bytes(policy.read_bytes() + b"\n")  # the copy moves; the real file is untouched
        why = self.qualification(self.measured)
        self.assertEqual(len(why), 1, why)
        self.assertTrue(why[0].startswith("no current credit record names the case " + CASE), why[0])
        self.assertIn("SHA256 or size differs", why[0])

    def test_a_non_experiment_form_is_refused(self):
        self.assertEqual(self.qualification([S.Symbol("candidate"), [S.Symbol("id"), "x"]]), ["not an experiment form"])
        self.assertEqual(self.qualification([S.Symbol("experiment")]), ["the record has no id"])


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    suite = (unittest.TestSuite([DossierQualificationTests(MUTATION_TESTS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(DossierQualificationTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"DOSSIER-QUALIFICATION-PROBE: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; the credit decides, never the record")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
