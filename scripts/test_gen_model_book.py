#!/usr/bin/env python3
"""Regression cases for the processor catalogue's version and coverage disclosure."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import gen_model_book as G


class ProcessorCatalogueRole(unittest.TestCase):
    def test_single_version_is_declared_catalogue_not_effective_coverage(self):
        self.assertEqual(
            G._processor_catalogue_role([{"contract_id": "lab-v0"}]),
            "the declared environment-obligation catalogue (`lab-v0`): "
            "positive AND negative checks per record; counts include historical records",
        )

    def test_mixed_versions_are_all_named_once_in_stable_order(self):
        records = [{"contract_id": name} for name in ["lab-v2", "lab-v0", "lab-v2", "lab-v1"]]
        self.assertEqual(
            G._processor_catalogue_role(records),
            "the declared environment-obligation catalogue (`lab-v0`, `lab-v1`, `lab-v2`): "
            "positive AND negative checks per record; counts include historical records",
        )

    def test_empty_catalogue_refuses_instead_of_describing_coverage(self):
        with self.assertRaisesRegex(G.GenError, "obligation catalogue is empty"):
            G._processor_catalogue_role([])


class DeclaredShape(unittest.TestCase):
    """A dossier holding neither declaration is refused by name, not read as a processor."""

    def test_a_dossier_declaring_no_shape_is_refused_by_its_name(self):
        with tempfile.TemporaryDirectory(dir=G.REPO / "target") as held:
            unit = Path(held) / "no-shape-lab-v0"
            unit.mkdir()
            with self.assertRaisesRegex(G.GenError, "no-shape-lab-v0 holds neither"):
                G.generate(unit)


class RetainedCases(unittest.TestCase):
    """The case index is generated, so these judge the rule on three small frozen cases: a damaged real one fails the real check by name (XTASK.13 slice f)."""
    root = Path(__file__).resolve().parent / "fixtures" / "materials-bill"
    unit = root / "profiles" / "rv64i-lab-v0"
    ONE = dict(id="CR-FX-1", case_id="rv64gc-fx-one-v2", requirement_id="REQ-FX-ONE", disposition="current")

    def setUp(self):
        patcher = patch.object(G, "REPO", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        credits = patch.object(G.CR, "current_credits", return_value=[self.ONE])
        self.current = credits.start()
        self.addCleanup(credits.stop)

    def rows(self):
        return {line.split("`")[1]: line for line in G.emit_cases(self.unit).splitlines() if line.startswith("| `")}

    def test_every_case_directory_has_exactly_one_row(self):
        self.assertEqual(set(self.rows()), {path.parent.name for path in (self.root / "evidence").glob("*/case.sexp")})

    def test_a_current_credit_is_read_and_a_lapsed_one_is_not(self):
        self.assertIn("credited, `CR-FX-1`", self.rows()["rv64gc-fx-one-v2"])
        self.current.return_value = [dict(self.ONE, disposition="lapsed")]
        self.assertIn("captured, credited by nothing", self.rows()["rv64gc-fx-one-v2"])

    def test_a_case_with_no_receipt_reads_declared(self):
        self.assertIn("| declared |", self.rows()["rv64gc-fx-two-v1"])

    def test_a_superseded_case_names_the_one_holding_the_credit(self):
        self.assertIn("history: `rv64gc-fx-one-v2` holds the credit", self.rows()["rv64gc-fx-one-v1"])

    def test_a_unit_holding_no_case_has_no_fragment(self):
        other = self.root / "profiles" / "sifive-uart-lab-v0"
        self.assertIsNone(G.emit_cases(other))
        self.assertNotIn("retained-cases.md", G.generate(other))

    def test_a_dossier_re_rooted_elsewhere_holds_no_case(self):
        with patch.object(G, "REPO", self.root.parent):
            self.assertIsNone(G.emit_cases(self.unit))

    def test_a_case_that_cannot_be_read_refuses(self):
        with patch.object(G.K, "read_case", side_effect=G.K.CaseError("no declaration")):
            with self.assertRaisesRegex(G.GenError, "the retained cases cannot be read: no declaration"):
                G.emit_cases(self.unit)


if __name__ == "__main__":
    unittest.main()
