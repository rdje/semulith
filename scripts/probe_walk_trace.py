#!/usr/bin/env python3
"""Controls for the page-table read comparison (`measure_walk_trace.py`, P4-SYSTEM.14 a51-7).

Synthetic traces, and stand-in binaries, so no reference process runs here.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import types
import unittest

import measure_walk_trace as M

ROOT = Path(__file__).resolve().parent.parent
CASE = "rv64gc-csr-set-v3"
CASE_DIR = ROOT / "evidence" / CASE
MUTATIONS = {
    "no-walk": ('    if not steps:\n        return False, "the reference\'s trace shows no walk"\n', "    if not steps:\n        return True, \"\"\n"),
    "different-ptes": ("    if ours != theirs:\n", "    if False:\n"),
    "width": ("    if narrow or set(widths) != addresses:\n", "    if False:\n"),
    "per-walk": ("    if max(walks) > LEVELS:\n", "    if False:\n"),
    "written": ("    if written:\n", "    if False:\n"),
    "reuse": ("    if any(path.exists() for path in paths):\n", "    if False:\n"),
    "reference-failed": ("        if process.returncode != 0 or not trace.is_file():\n", "        if not trace.is_file():\n"),
    "engine-failed": ("    if done.returncode != 0:\n", "    if False:\n"),
    "trace-bound": ("    if len(reference) > TRACE_BYTES or len(lab) > TRACE_BYTES:\n", "    if False:\n"),
    "held-only": ("    if not held:\n", "    if False:\n"),
}


def read(addr, value, level=2):
    return f"PTW: Start, vpn=0x400, access_type=R, privilege=S\nmem[R,0x{addr:016X}] -> 0x{value:016X}\nPTW: Step, level={level}, pte=0x{value:X}, pte_addr=0x{addr:X}\n"


def engine_line(addr, value):
    return f"ptw[0x{addr:016x}] -> 0x{value:016x}\n"


TWO = read(0x80003000, 0x20001001) + read(0x80004010, 0x20001401, 1) + "PTW: Success, final_ppn=0x80007, level=1\n"
OURS = engine_line(0x80003000, 0x20001001) + engine_line(0x80004010, 0x20001401)


class CompareTests(unittest.TestCase):
    def test_the_same_reads_hold(self):
        held, detail = M.compare(TWO, OURS)
        self.assertTrue(held, detail)
        self.assertIn("2 distinct PTEs read on both with the same values, in the same order", detail)
        self.assertIn("at most 2 per walk", detail)

    def test_another_order_holds_and_says_so(self):
        held, detail = M.compare(TWO, engine_line(0x80004010, 0x20001401) + engine_line(0x80003000, 0x20001001))
        self.assertTrue(held, detail)
        self.assertIn("in a different order, which TLB replacement allows", detail)

    def test_no_walk_refuses(self):
        held, detail = M.compare("[0] [M]: 0x80000000\n", "")
        self.assertEqual((held, detail), (False, "the reference's trace shows no walk"))

    def test_a_pte_only_one_side_read_refuses(self):
        held, detail = M.compare(TWO, engine_line(0x80003000, 0x20001001))
        self.assertFalse(held)
        self.assertIn("1 only on the reference", detail)

    def test_another_value_at_the_same_address_refuses(self):
        held, detail = M.compare(TWO, engine_line(0x80003000, 0x20001001) + engine_line(0x80004010, 0x20001402))
        self.assertFalse(held)
        self.assertIn("different PTEs", detail)

    def test_a_narrow_read_refuses(self):
        narrow = TWO.replace("mem[R,0x0000000080004010] -> 0x0000000020001401", "mem[R,0x0000000080004010] -> 0x20001401")
        held, detail = M.compare(narrow, OURS)
        self.assertFalse(held)
        self.assertIn("not 8 bytes", detail)

    def test_a_walk_of_four_reads_refuses(self):
        four = "".join(read(0x80003000 + 8 * i, 0x100 + i) for i in range(4)) + "PTW: Success, final_ppn=0x1, level=0\n"
        held, detail = M.compare(four, "".join(engine_line(0x80003000 + 8 * i, 0x100 + i) for i in range(4)))
        self.assertFalse(held)
        self.assertIn("read 4 PTEs", detail)

    def test_a_write_to_a_pte_after_the_first_walk_refuses(self):
        held, detail = M.compare(TWO + "mem[W,0x0000000080004010] <- 0x0000000020001441\n", OURS)
        self.assertFalse(held)
        self.assertIn("a PTE was written", detail)

    def test_a_write_to_a_pte_before_the_first_walk_is_the_program_building_its_tables(self):
        held, detail = M.compare("mem[W,0x0000000080004010] <- 0x0000000020001401\n" + TWO, OURS)
        self.assertTrue(held, detail)


class MeasureTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / "target" / "tmp"
        scratch.mkdir(parents=True, exist_ok=True)
        self.td = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.td.name)
        case = self.root / "evidence" / CASE
        case.mkdir(parents=True)
        for name in ("guest.elf", "reference-config.json", "baseline.expected.sexp"):
            shutil.copy(CASE_DIR / name, case / name)
        for path in M.walk_paths(self.root, CASE):
            path.parent.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.td.cleanup()

    def script(self, name, body):
        path = self.root / name
        path.write_text(f"#!{sys.executable}\nimport sys\n{body}\n")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def reference(self, text=TWO, exit_code=0):
        return self.script("reference", f"args = sys.argv[1:]\nopen(args[args.index('--trace-output') + 1], 'w').write({text!r})\nsys.exit({exit_code})")

    def engine(self, text=OURS, exit_code=0):
        return [str(self.script("engine", f"sys.stdout.write({'[0] [M]: 0x80000000' + chr(10) + text!r})\nsys.exit({exit_code})"))]

    def retained(self):
        return [path.exists() for path in M.walk_paths(self.root, CASE)]

    def test_a_holding_comparison_retains_the_raw_traces_and_what_ran(self):
        code, detail = M.measure(self.root, CASE, self.reference(), self.engine())
        self.assertEqual(code, 0, detail)
        self.assertEqual(self.retained(), [True, True, True])
        record, trace, lab = M.walk_paths(self.root, CASE)
        self.assertEqual(trace.read_text(), TWO)
        self.assertEqual(lab.read_text(), OURS)
        self.assertIn(M.sha(TWO.encode()), record.read_text())

    def test_a_retained_measure_refuses_reuse(self):
        self.assertEqual(M.measure(self.root, CASE, self.reference(), self.engine())[0], 0)
        code, detail = M.measure(self.root, CASE, self.reference(), self.engine())
        self.assertEqual(code, 2)
        self.assertIn("refuse reuse", detail)

    def test_a_failed_reference_retains_nothing(self):
        code, detail = M.measure(self.root, CASE, self.reference(exit_code=1), self.engine())
        self.assertEqual(code, 2)
        self.assertIn("reference process failed", detail)
        self.assertEqual(self.retained(), [False, False, False])

    def test_a_failed_engine_retains_nothing(self):
        code, detail = M.measure(self.root, CASE, self.reference(), self.engine(exit_code=1))
        self.assertEqual(code, 2)
        self.assertIn("engine process failed", detail)
        self.assertEqual(self.retained(), [False, False, False])

    def test_an_oversized_trace_retains_nothing(self):
        code, detail = M.measure(self.root, CASE, self.reference(TWO * 200000), self.engine())
        self.assertEqual(code, 2)
        self.assertIn("above", detail)
        self.assertEqual(self.retained(), [False, False, False])

    def test_a_comparison_that_does_not_hold_retains_nothing(self):
        code, detail = M.measure(self.root, CASE, self.reference(), self.engine(engine_line(0x80003000, 0x1)))
        self.assertEqual(code, 1)
        self.assertEqual(self.retained(), [False, False, False])


def main():
    global M
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/measure_walk_trace.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_measure_walk_trace")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        M = module
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(CompareTests), unittest.defaultTestLoader.loadTestsFromTestCase(MeasureTests)])
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"WALK-TRACE: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; "
          "synthetic traces and stand-in binaries, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
