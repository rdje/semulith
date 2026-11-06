#!/usr/bin/env python3
"""Controls for one case's reference-configuration overlay (`prepare_div_inputs.apply_overlay`, P4-SYSTEM.14 a43b-3c)."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import types
import unittest

import prepare_div_inputs as Prep

ROOT = Path(__file__).resolve().parent.parent
CASE = "rv64gc-csr-set-v3"
MUTATIONS = {
    "extension-known": ('_require(entry is not None, f"overlay names unknown extension {name}")', 'entry = entry if entry is not None else {"supported": False}'),
    "extension-changes": ('_require(entry["supported"] is False, ', '_require(True, '),
    "clint-absent": ('_require(platform["clint"] == {"supported": False}, ', '_require(True, '),
    "clint-positive": ('_require(base > 0 and size > 0, ', '_require(True, '),
    "tick-positive": ('_require(overlay["instructions_per_tick"] >= 1, ', '_require(True, '),
    "tick-absent": ('_require("instructions_per_tick" not in platform, ', '_require(True, '),
    "region-overlap": ('_require(base + size <= start or start + int(region["size"]["value"], 16) <= base,', '_require(True,'),
    "region-order": ('position = sum(1 for region in regions if int(region["base"]["value"], 16) < base)', 'position = len(regions)'),
    "case-binding": ('_require(overlay["case_id"] == case_id, ', '_require(True, '),
    "alternative-known": ('_require(entry is not None, f"alternative names unknown extension {name}")', 'entry = entry if entry is not None else {"supported": not wanted}'),
    "alternative-extension-changes": ('_require(entry["supported"] is not wanted, ', '_require(True, '),
    "alternative-misaligned-changes": ('_require(exceptions.get(kind) != rendered, ', '_require(True, '),
    "overlay-amo-changes": ('_require(exceptions.get("amo") != rendered, ', '_require(True, '),
    "overlay-exact-changes": ('_require("require_exact_reservation_addr" not in reservation, ', '_require(True, '),
    "overlay-nothing": ('_require(result != config, "the overlay changes nothing")', '_require(True, "the overlay changes nothing")'),
    "alternative-nothing": ('_require(result != config, "the alternative changes nothing")', '_require(True, "the alternative changes nothing")'),
    "alternative-binding": ('_require(alternative["case_id"] == case_id, ', '_require(True, '),
    "alternative-over-case": ('return apply_alternative(reference_config(root, case_id), alternative)', 'return apply_alternative(map_document(root, read_bounded(root / OVERRIDE), "override", D.override_to_doc), alternative)'),
}
ALTERNATIVE_TEXT = """(alternative (case_id "{case}") (reason "What selects otherwise."){switches})"""


def region(base, size):
    return {"base": {"len": 64, "value": hex(base)}, "size": {"len": 64, "value": hex(size)}, "attributes": {}}


def configuration():
    return {"extensions": {"Zicntr": {"supported": False}, "Sstc": {"supported": True}},
            "platform": {"clint": {"supported": False}, "wfi_is_nop": True},
            "memory": {"regions": [region(0x80000000, 0x80000000)]}}


def overlay(**changes):
    return {"case_id": CASE, "extensions": ["Zicntr"], "clint_base": 0x2000000, "clint_size": 0xC000,
            "instructions_per_tick": 1, **changes}


OVERLAY_TEXT = """(overlay (case_id "{case}") (reason "synthetic")
  (extension "Zicntr") (clint (base 0x2000000) (size 0xC000)) (instructions_per_tick 1){extra})
"""


class OverlayTests(unittest.TestCase):
    def temporary_root(self, overlay_text=None):
        base = ROOT / "target/reference-overlay-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "schema").mkdir()
        for name in ("override.sexp", "overlay.sexp", "alternative.sexp", "schema.sexp"):
            shutil.copy(ROOT / "schema" / name, root / "schema" / name)
        override = root / Prep.OVERRIDE
        override.parent.mkdir(parents=True)
        shutil.copy(ROOT / Prep.OVERRIDE, override)
        if overlay_text is not None:
            (root / Prep.overlay_path(CASE)).write_text(overlay_text)
        return root

    def declared(self, switches, case=CASE, overlay=None):
        root = self.temporary_root(overlay)
        (root / Prep.alternative_path(CASE)).write_text(ALTERNATIVE_TEXT.format(case=case, switches=switches))
        return root

    def canonical(self, root):
        return Prep.map_document(root, Prep.read_bounded(root / Prep.OVERRIDE), "override", Prep.D.override_to_doc)

    def test_each_switch_changes_its_own_place_and_nothing_else_moves(self):
        root = self.declared(' (extension_off "S") (extension_off "Sstc") (extension_on "Sv48") (misaligned_load_store None) (misaligned_lrsc AlignmentException)'
                             ' (misaligned_amo AccessFault)')
        expected = self.canonical(root)
        expected["extensions"]["S"]["supported"] = False
        expected["extensions"]["Sstc"]["supported"] = False
        expected["extensions"]["Sv48"]["supported"] = True
        expected["memory"]["misaligned"]["exceptions"] = {"load_store": {"None": None}, "lrsc": {"Some": "AlignmentException"}, "amo": {"Some": "AccessFault"}}
        self.assertEqual(Prep.alternative_config(root, CASE), expected)
        self.assertEqual(json.loads(json.dumps(expected)), expected, "the configuration renders to JSON unchanged")

    def test_a_case_declaring_no_alternative_has_none(self):
        self.assertIsNone(Prep.alternative_config(self.temporary_root(), CASE))

    def test_an_alternative_applies_over_the_cases_own_configuration(self):
        root = self.declared(' (extension_off "S")', overlay=OVERLAY_TEXT.format(case=CASE, extra=""))
        expected = Prep.reference_config(root, CASE)
        self.assertTrue(expected["platform"]["clint"]["supported"])
        expected["extensions"]["S"]["supported"] = False
        self.assertEqual(Prep.alternative_config(root, CASE), expected)

    def test_an_alternative_naming_an_unknown_extension_refuses(self):
        with self.assertRaisesRegex(Prep.CurationRefused, "unknown extension"):
            Prep.alternative_config(self.declared(' (extension_off "NotAnExtension")'), CASE)

    def test_a_switch_that_changes_nothing_refuses_on_every_knob(self):
        for switches, needle in ((' (extension_off "Sv48")', "turns Sv48 off"), (' (extension_on "S")', "turns S on"),
                                 (' (misaligned_load_store AlignmentException)', "for misaligned load_store")):
            with self.subTest(switches=switches), self.assertRaisesRegex(Prep.CurationRefused, needle):
                Prep.alternative_config(self.declared(switches), CASE)

    def test_an_overlay_may_name_no_device_and_moves_only_what_it_names(self):
        root = self.temporary_root('(overlay (case_id "%s") (reason "A selection.") (misaligned_amo AccessFault) (require_exact_reservation_addr true))' % CASE)
        expected = self.canonical(root)
        expected["memory"]["misaligned"]["exceptions"]["amo"] = {"Some": "AccessFault"}
        expected["platform"]["reservation"] = {"require_exact_reservation_addr": True}
        self.assertEqual(Prep.reference_config(root, CASE), expected)
        self.assertEqual(expected["platform"]["clint"], {"supported": False})

    def test_a_selection_the_override_already_declares_refuses(self):
        canonical = self.canonical(self.temporary_root())
        canonical["memory"]["misaligned"]["exceptions"]["amo"] = {"Some": "AccessFault"}
        canonical["platform"]["reservation"] = {"require_exact_reservation_addr": True}
        for doc, needle in (({"misaligned_amo": "AccessFault"}, "misaligned AMO"), ({"require_exact_reservation_addr": True}, "exact reservation")):
            with self.subTest(doc=doc), self.assertRaisesRegex(Prep.CurationRefused, needle):
                Prep.apply_overlay(canonical, {"case_id": CASE, "extensions": [], **doc})

    def test_an_overlay_of_no_knob_refuses(self):
        with self.assertRaisesRegex(Prep.CurationRefused, "changes nothing"):
            Prep.apply_overlay(self.canonical(self.temporary_root()), {"case_id": CASE, "extensions": []})

    def test_an_alternative_of_no_switch_refuses(self):
        with self.assertRaisesRegex(Prep.CurationRefused, "changes nothing"):
            Prep.alternative_config(self.declared(""), CASE)

    def test_an_alternative_naming_another_case_refuses(self):
        with self.assertRaisesRegex(Prep.CurationRefused, "declares case"):
            Prep.alternative_config(self.declared(' (extension_off "S")', case="rv64gc-some-other-v1"), CASE)

    def test_the_schema_refuses_a_knob_the_alternative_does_not_name(self):
        with self.assertRaises(Prep.CurationRefused):
            Prep.alternative_config(self.declared(' (writable_misa true)'), CASE)

    def test_the_schema_refuses_a_value_the_binary_does_not_publish(self):
        with self.assertRaises(Prep.CurationRefused):
            Prep.alternative_config(self.declared(' (misaligned_amo AlignmentFault)'), CASE)

    def test_every_change_is_the_overlays_and_nothing_else_moves(self):
        before = configuration()
        after = Prep.apply_overlay(before, overlay())
        self.assertEqual(before, configuration(), "the input configuration is not mutated")
        self.assertEqual(after["extensions"]["Zicntr"], {"supported": True})
        self.assertEqual(after["extensions"]["Sstc"], {"supported": True})
        self.assertEqual(after["platform"]["clint"], {"supported": True, "base": 0x2000000, "size": 0xC000})
        self.assertEqual(after["platform"]["instructions_per_tick"], 1)
        self.assertEqual(after["platform"]["wfi_is_nop"], True)

    def test_the_device_region_goes_where_its_base_puts_it(self):
        regions = Prep.apply_overlay(configuration(), overlay())["memory"]["regions"]
        self.assertEqual([r["base"]["value"] for r in regions], ["0x2000000", hex(0x80000000)])
        self.assertEqual(regions[0]["size"]["value"], "0xC000")
        self.assertEqual(regions[0]["attributes"]["mem_type"], "IOMemory")
        above = Prep.apply_overlay(configuration(), overlay(clint_base=0x100000000))["memory"]["regions"]
        self.assertEqual([r["base"]["value"] for r in above], [hex(0x80000000), "0x100000000"])

    def test_an_unknown_extension_refuses(self):
        with self.assertRaisesRegex(Prep.CurationRefused, "unknown extension"):
            Prep.apply_overlay(configuration(), overlay(extensions=["Znope"]))

    def test_an_extension_already_on_refuses_because_it_changes_nothing(self):
        with self.assertRaisesRegex(Prep.CurationRefused, "already supports"):
            Prep.apply_overlay(configuration(), overlay(extensions=["Sstc"]))

    def test_a_clint_over_a_declared_one_refuses(self):
        config = configuration()
        config["platform"]["clint"] = {"supported": True, "base": 1, "size": 1}
        with self.assertRaisesRegex(Prep.CurationRefused, "declares one"):
            Prep.apply_overlay(config, overlay())

    def test_a_nonpositive_clint_refuses(self):
        for changes in (dict(clint_base=0), dict(clint_size=0)):
            with self.subTest(changes=changes), self.assertRaisesRegex(Prep.CurationRefused, "positive base and size"):
                Prep.apply_overlay(configuration(), overlay(**changes))

    def test_a_nonpositive_tick_rate_refuses(self):
        with self.assertRaisesRegex(Prep.CurationRefused, "tick rate must be positive"):
            Prep.apply_overlay(configuration(), overlay(instructions_per_tick=0))

    def test_a_tick_rate_over_a_declared_one_refuses(self):
        config = configuration()
        config["platform"]["instructions_per_tick"] = 2
        with self.assertRaisesRegex(Prep.CurationRefused, "already declares"):
            Prep.apply_overlay(config, overlay())

    def test_an_overlapping_region_refuses_on_either_side(self):
        for base, size in ((0x80000000, 0x1000), (0x7FFFF000, 0x2000), (0xFFFFF000, 0x2000)):
            with self.subTest(base=hex(base)), self.assertRaisesRegex(Prep.CurationRefused, "overlaps"):
                Prep.apply_overlay(configuration(), overlay(clint_base=base, clint_size=size))

    def test_regions_that_only_touch_do_not_overlap(self):
        regions = Prep.apply_overlay(configuration(), overlay(clint_base=0x7FFFF000, clint_size=0x1000))["memory"]["regions"]
        self.assertEqual(len(regions), 2)

    def test_a_case_without_an_overlay_keeps_the_profile_override_exactly(self):
        root = self.temporary_root()
        canonical = Prep.map_document(root, Prep.read_bounded(root / Prep.OVERRIDE), "override", Prep.D.override_to_doc)
        self.assertEqual(Prep.reference_config(root, CASE), canonical)

    def test_an_overlay_naming_another_case_refuses(self):
        root = self.temporary_root(OVERLAY_TEXT.format(case="rv64gc-some-other-v1", extra=""))
        with self.assertRaisesRegex(Prep.CurationRefused, "declares case"):
            Prep.reference_config(root, CASE)

    def test_the_schema_refuses_a_knob_it_does_not_name(self):
        root = self.temporary_root(OVERLAY_TEXT.format(case=CASE, extra=' (writable_misa true)'))
        with self.assertRaises(Prep.CurationRefused):
            Prep.reference_config(root, CASE)

    def test_the_real_overlay_differs_from_the_profile_override_only_by_itself(self):
        canonical = Prep.map_document(ROOT, Prep.read_bounded(ROOT / Prep.OVERRIDE), "override", Prep.D.override_to_doc)
        config = Prep.reference_config(ROOT, CASE)
        expected = deepcopy(canonical)
        expected["extensions"]["Zicntr"]["supported"] = True
        expected["platform"]["clint"] = {"supported": True, "base": 0x2000000, "size": 0xC000}
        expected["platform"]["instructions_per_tick"] = 1
        device, *rest = config["memory"]["regions"]
        expected["memory"]["regions"] = [device, *canonical["memory"]["regions"]]
        self.assertEqual(config, expected)
        self.assertEqual(rest, canonical["memory"]["regions"])
        self.assertEqual(device["attributes"], Prep.DEVICE_REGION_ATTRIBUTES)
        self.assertEqual(json.loads(json.dumps(config)), config, "the configuration renders to JSON unchanged")


def main():
    global Prep
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/prepare_div_inputs.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_prepare_div_inputs")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module  # dataclasses resolve their module while the copy executes
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        Prep = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(OverlayTests))
    print(f"REFERENCE-OVERLAY: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; "
          "synthetic configuration controls, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
