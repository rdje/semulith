#!/usr/bin/env python3
"""Regression cases for the processor catalogue's version and coverage disclosure."""

from pathlib import Path
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


class RetainedCases(unittest.TestCase):
    """The case index is generated, so these judge the rule and name no particular case or credit (P4-SYSTEM.14 a46-1)."""
    unit = G.REPO / "profiles" / "rv64gc-lab-v0"

    def rows(self):
        return {line.split("`")[1]: line for line in G.emit_cases(self.unit).splitlines() if line.startswith("| `")}

    def test_every_case_directory_has_exactly_one_row(self):
        self.assertEqual(set(self.rows()), {path.parent.name for path in (G.REPO / "evidence").glob("*/case.sexp")})

    # A stub credit on a case that stays in the tree: authenticating one is CREDIT-RECORDS', and these hold through a window (a49-1).
    ONE = dict(id="CR-FX-1", case_id="rv64gc-m-forms-v3", requirement_id="REQ-GC-M", disposition="current")

    def test_a_current_credit_is_read_and_a_lapsed_one_is_not(self):
        with patch.object(G.CR, "current_credits", return_value=[self.ONE]):
            self.assertIn("credited, `CR-FX-1`", self.rows()[self.ONE["case_id"]])
        with patch.object(G.CR, "current_credits", return_value=[dict(self.ONE, disposition="lapsed")]):
            self.assertIn("captured, credited by nothing", self.rows()[self.ONE["case_id"]])

    def test_a_case_with_no_receipt_reads_declared(self):
        real = Path.is_file
        with patch.object(G.CR, "current_credits", return_value=[]), patch.object(
                Path, "is_file", lambda path: path.name != "verification.json" and real(path)):
            self.assertIn("| declared |", self.rows()[self.ONE["case_id"]])

    def test_a_superseded_case_names_the_one_holding_the_credit(self):
        with patch.object(G.CR, "current_credits", return_value=[self.ONE]):
            rows = self.rows()
        same = [r for case, r in rows.items() if case != self.ONE["case_id"] and "`REQ-GC-M`" in r and "| declared |" not in r]
        self.assertTrue(same)
        for row in same:
            self.assertIn(f"history: `{self.ONE['case_id']}` holds the credit", row)

    def test_a_unit_holding_no_case_has_no_fragment(self):
        other = G.REPO / "profiles" / "rv64i-lab-v0"
        self.assertIsNone(G.emit_cases(other))
        self.assertNotIn("retained-cases.md", G.generate(other))

    def test_a_case_that_cannot_be_read_refuses(self):
        with patch.object(G.K, "read_case", side_effect=G.K.CaseError("no declaration")):
            with self.assertRaisesRegex(G.GenError, "the retained cases cannot be read: no declaration"):
                G.emit_cases(self.unit)


if __name__ == "__main__":
    unittest.main()
