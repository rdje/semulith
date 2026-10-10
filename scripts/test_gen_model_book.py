#!/usr/bin/env python3
"""Regression cases for the processor catalogue's version and coverage disclosure."""

import unittest

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


if __name__ == "__main__":
    unittest.main()
