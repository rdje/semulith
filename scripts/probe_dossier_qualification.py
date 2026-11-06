#!/usr/bin/env python3
"""Dossier-qualification controls (P4-SYSTEM.14 a42bc): a verification-bearing experiment record in a
dossier is qualified only through a CURRENT credit record naming its case and form-equality with the case's
measured record. The credit decides, never the record. The real-tree arm predicts the live catalogue's verdict
on the m-forms case; the synthetic arms judge a mirror root whose credit is a FROZEN copy of the retired record
CR-GC-M-1 (scripts/fixtures/dossier-qualification/credits.sexp, ruling 5) and whose dependency manifest is
re-pinned to the mirror's own bytes — a current synthetic capture, as probe_div_method builds one — and break
one thing at a time (P4-SYSTEM.14 a44-2b)."""
from __future__ import annotations

import argparse
import copy
import hashlib
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
CASE = "rv64gc-m-forms-v3"  # the mirror's case: the frozen credit CR-GC-M-1 names it
LIVE_CASE = "rv64gc-m-forms-v6"  # the M case the live catalogue credits (CR-GC-M-4, P4-SYSTEM.14 a43e-5)
FROZEN_CREDITS = HERE / "fixtures" / "dossier-qualification" / "credits.sexp"


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
        for text_path in (FROZEN_CREDITS, case_src / "dependencies.sexp"):
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
        shutil.copy(FROZEN_CREDITS, self.profile / "credits.sexp")
        (self.root / "evidence").mkdir(exist_ok=True)
        for case_dir in (ROOT / "evidence").iterdir():
            if case_dir.name != CASE:
                (self.root / "evidence" / case_dir.name).symlink_to(case_dir)
        self.case = self.root / "evidence" / CASE
        shutil.copytree(case_src, self.case)
        # The mirror's capture is current: each manifest row re-pinned to the mirror's own bytes of its path.
        manifest = self.case / "dependencies.sexp"
        text = manifest.read_text()
        for form in S.read_file(manifest):
            for row in S.children(form, "input"):
                path, pin = S.field(row, "path"), S.field(row, "sha256")
                current = hashlib.sha256((self.root / path).read_bytes()).hexdigest()
                old = f'(path "{path}") (sha256 "{pin}")'
                if text.count(old) != 1:
                    raise RuntimeError("manifest row is not singular: " + path)
                text = text.replace(old, f'(path "{path}") (sha256 "{current}")')
        manifest.write_text(text)
        self.cr = load_module(ROOT / "scripts" / "credit_records.py", "credit_records_under_test")
        self.measured = [f for f in S.read_file(self.case / "measured-experiment.sexp")
                         if isinstance(f, list) and f and str(f[0]) == "experiment"][0]

    def qualification(self, form, root=None):
        return self.cr.dossier_qualification(root or self.root, (root or self.root) / "profiles" / UNIT, form)

    def test_the_real_tree_predicts_the_live_catalogue(self):
        """The live catalogue credits the window's five (P4-SYSTEM.14 a43e-5) Batch I's nine (a46-4) and Batch II-a's five (a47-3): their measured records qualify on the real tree; their
        predecessors', which no live record names, do not. The dossier holds no copy of any of them, by the ruling
        (decision_dossier-copies-retire-at-the-next-window.md): G-TRACE reads each from evidence/."""
        def measured(case):
            return [f for f in S.read_file(ROOT / "evidence" / case / "measured-experiment.sexp")
                    if isinstance(f, list) and f and str(f[0]) == "experiment"][0]
        references = next(f for f in S.read_file(ROOT / "profiles" / UNIT / "references.sexp")
                          if isinstance(f, list) and f and str(f[0]) == "references")
        self.assertEqual([e for e in S.children(references, "experiment") if S.children(e, "verification")], [])
        for case in (LIVE_CASE, "rv64gc-xlen-forms-v3", "rv64gc-csr-set-v2", "rv64gc-zicntr-v2", "rv64gc-sstc-v1", "rv64gc-alu-imm-v1", "rv64gc-alu-reg-v1", "rv64gc-lui-auipc-v1", "rv64gc-jalr-lsb-v1", "rv64gc-no-delay-slots-v1", "rv64gc-shamt-v1", "rv64gc-wsuffix-v1", "rv64gc-load-ext-v1", "rv64gc-load-x0-v1", "rv64gc-ecall-ebreak-v1", "rv64gc-csr-access-v1", "rv64gc-counters-v1", "rv64gc-fencei-v1", "rv64gc-ialign-16-v1"):
            self.assertEqual(self.qualification(measured(case), ROOT), [], case)
        for case in ("rv64gc-m-forms-v5", "rv64gc-xlen-forms-v2", "rv64gc-csr-set-v1", "rv64gc-zicntr-v1", "rv64gc-m-forms-v4", "rv64gc-xlen-forms-v1", CASE):
            self.assertEqual(self.qualification(measured(case), ROOT), ["no credit record names the case " + case])

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
