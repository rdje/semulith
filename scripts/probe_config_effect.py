#!/usr/bin/env python3
"""Controls for the configuration-effect tool (`measure_config_effect.py`, P4-SYSTEM.14 a43b-3f).

A stand-in binary writes a chosen trace, so no reference process runs here: the case's own baseline trace against its baseline
expectation agrees, and against its control expectation differs at the control's step. The last tests judge the retained record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import types
import unittest

import check_sexp_schema as K
import measure_config_effect as M

ROOT = Path(__file__).resolve().parent.parent
CASE = "rv64gc-csr-set-v3"
CASE_DIR = ROOT / "evidence" / CASE
STEP, REGISTER, OBSERVED, EXPECTED = 34, "x20", [], 34
# Every retained effect and the first difference it must show: case, step, register, observed, expected.
RETAINED = ((CASE, STEP, REGISTER, OBSERVED, EXPECTED), ("rv64gc-zicntr-v3", 6, "x5", [], 6), ("rv64gc-sstc-v2", 8, "x5", [], 8),
            ("rv64gc-svade-v1", 93, "x22", [], 13), ("rv64gc-atomic-misalign-v1", 24, "x30", [("x30", 4)], 5),
            ("rv64gc-fault-priority-v1", 159, "x22", [("x22", 13)], 4), ("rv64gc-priv-modes-v1", 5, "x5", [("x5", 9223372036855828781)], 9223372036856090925),
            ("rv64gc-sv39-v1", 17, "x5", [("x5", 10376293541462147075)], 0), ("rv64gc-reservation-v1", 23, "x15", [("x15", 0)], 1),
            ("rv64gc-sc-deterministic-v1", 21, "x15", [("x15", 0)], 1),
            ("rv64gc-no-h-v1", 5, "x5", [("x5", 9223372036856091053)], 9223372036856090925), ("rv64gc-no-pmp-v1", 22, "x7", [], 66))
# P4-SYSTEM.20 slice d moved the profile override (the misaligned AMO), so the ten effects measured against it, or against an
# alternative over it, compare with a configuration that no longer exists. A retained effect is never re-measured under its
# name, so in version 1's window this arm predicts them stale; slice f captures the cases again, and this set empties.
STALE_SINCE_SLICE_D = frozenset({"rv64gc-csr-set-v3", "rv64gc-zicntr-v3", "rv64gc-sstc-v2", "rv64gc-svade-v1",
                                 "rv64gc-priv-modes-v1", "rv64gc-sv39-v1", "rv64gc-reservation-v1",
                                 "rv64gc-sc-deterministic-v1", "rv64gc-no-h-v1", "rv64gc-no-pmp-v1"})
MUTATIONS = {
    "reuse": ("if record_path.exists() or trace_path.exists():", "if False:"),
    "record-reuse": ("if record_path.exists() or trace_path.exists():", "if trace_path.exists():"),
    "own-config": ("if sha(alternative) == sha(case_config.read_bytes()):", "if False:"),
    "process-failed": ('if process.returncode != 0 or not trace.is_file():', "if not trace.is_file():"),
    "trace-missing": ('if process.returncode != 0 or not trace.is_file():', "if process.returncode != 0:"),
    "trace-bound": ("if len(data) > TRACE_BYTES:", "if False:"),
    "no-effect": ('if result.verdict != "DIVERGE":', "if False:"),
    "profile-config": ('config.write_bytes(alternative)', 'config.write_bytes(case_config.read_bytes())'),
    "binary-pin": ("binary=sha(binary.read_bytes())", 'binary=sha(guest.read_bytes())'),
    "declared-ignored": ("    declared = Prep.alternative_config(root, case_id)\n", "    declared = None\n"),
    "declared-refusal": ("    except REFUSALS as refused:\n        return 2, f\"REFUSED: {case_id}'s declared alternative: {refused}\"\n", "    except ZeroDivisionError as refused:\n        return 2, str(refused)\n"),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class EffectTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / "target" / "tmp"
        scratch.mkdir(parents=True, exist_ok=True)
        self.td = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.td.name)
        case = self.root / "evidence" / CASE
        case.mkdir(parents=True)
        for name in ("guest.elf", "reference-config.json", "baseline.expected.sexp"):
            shutil.copy(CASE_DIR / name, case / name)
        (self.root / "schema").mkdir()
        shutil.copy(ROOT / "schema" / "override.sexp", self.root / "schema" / "override.sexp")
        shutil.copy(ROOT / "schema" / "alternative.sexp", self.root / "schema" / "alternative.sexp")
        override = self.root / M.Prep.OVERRIDE
        override.parent.mkdir(parents=True)
        shutil.copy(ROOT / M.Prep.OVERRIDE, override)
        self.case = case
        self.seen = self.root / "seen-config"
        self.ran = self.root / "ran"

    def tearDown(self):
        self.td.cleanup()

    def binary(self, *, trace=CASE_DIR / "baseline.trace", exit_code=0, oversized=False) -> Path:
        """A stand-in reference: it records its configuration, then writes the chosen trace."""
        path = self.root / "stand-in"
        write = "" if trace is None else (
            f"open(out, 'wb').write(open({str(trace)!r}, 'rb').read()" + (" * (64 * 1024)" if oversized else "") + ")")
        path.write_text(f"#!{sys.executable}\nimport sys\nargs = sys.argv[1:]\nout = args[args.index('--trace-output') + 1]\n"
                        f"open({str(self.ran)!r}, 'w').write(' '.join(args))\n"
                        f"open({str(self.seen)!r}, 'wb').write(open(args[args.index('--config-override') + 1], 'rb').read())\n"
                        f"{write}\nsys.exit({exit_code})\n")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def differ(self):
        """The control's expectation in the baseline's place: the stand-in's trace then differs at the control's step."""
        shutil.copy(CASE_DIR / "control.expected.sexp", self.case / "baseline.expected.sexp")

    def retained(self):
        return [path.exists() for path in M.effect_paths(self.root, CASE)]

    def test_a_differing_run_retains_the_raw_trace_and_what_ran(self):
        self.differ()
        binary = self.binary()
        code, detail = M.measure(self.root, CASE, binary)
        self.assertEqual(code, 0, detail)
        self.assertIn("step 130", detail)
        record, trace = M.effect_paths(self.root, CASE)
        self.assertEqual(trace.read_bytes(), (CASE_DIR / "baseline.trace").read_bytes())
        constructs, operators = K.load_schema(ROOT / "schema" / "config-effect.sexp")
        self.assertEqual(K.validate_text(record.read_text(), constructs, operators, "config-effect"), [])
        text = record.read_text()
        for name, digest in (("binary_sha256", sha(binary.read_bytes())), ("guest_sha256", sha((CASE_DIR / "guest.elf").read_bytes())),
                             ("case_config_sha256", sha((CASE_DIR / "reference-config.json").read_bytes())),
                             ("alternative_config_sha256", sha(self.seen.read_bytes())), ("trace_sha256", sha(trace.read_bytes()))):
            self.assertIn(f'({name} "{digest}")', text)
        self.assertIn(f"(trace_bytes {trace.stat().st_size})", text)

    def test_the_record_carries_no_verdict(self):
        self.differ()
        M.measure(self.root, CASE, self.binary())
        record, _ = M.effect_paths(self.root, CASE)
        for word in ("DIVERGE", "AGREE", "verdict (", "(verdict"):
            self.assertNotIn(word, record.read_text())

    def test_the_run_is_under_the_profile_override_not_the_cases(self):
        self.differ()
        M.measure(self.root, CASE, self.binary())
        self.assertEqual(self.seen.read_bytes(), M.profile_config(self.root))
        self.assertNotEqual(self.seen.read_bytes(), (CASE_DIR / "reference-config.json").read_bytes())
        self.assertIn(f"--inst-limit 157", self.ran.read_text())

    def declare(self, switches):
        (self.root / M.Prep.alternative_path(CASE)).write_text(f'(alternative (case_id "{CASE}") (reason "Selects otherwise."){switches})\n')

    def test_a_declared_alternative_is_what_runs_and_what_the_record_names(self):
        self.differ()
        self.declare(' (extension_off "Svade")')
        binary = self.binary()
        code, detail = M.measure(self.root, CASE, binary)
        self.assertEqual(code, 0, detail)
        config = json.loads(self.seen.read_text())
        self.assertIs(config["extensions"]["Svade"]["supported"], False)
        self.assertEqual(self.seen.read_bytes(), M.alternative_config(self.root, CASE)[0])
        self.assertNotEqual(self.seen.read_bytes(), M.profile_config(self.root))
        self.assertIn(f'(alternative_config_sha256 "{sha(self.seen.read_bytes())}")', M.effect_paths(self.root, CASE)[0].read_text())

    def test_a_refused_alternative_runs_nothing_and_retains_nothing(self):
        self.differ()
        self.declare(' (extension_off "NotAnExtension")')
        code, detail = M.measure(self.root, CASE, self.binary())
        self.assertEqual(code, 2, detail)
        self.assertIn("declared alternative", detail)
        self.assertFalse(self.ran.exists())
        self.assertEqual(self.retained(), [False, False])

    def test_an_agreeing_run_under_a_declared_alternative_names_it_and_retains_nothing(self):
        self.declare(' (extension_off "Svade")')
        code, detail = M.measure(self.root, CASE, self.binary())
        self.assertEqual(code, 1, detail)
        self.assertIn("under its declared alternative", detail)
        self.assertEqual(self.retained(), [False, False])

    def test_an_agreeing_run_retains_nothing(self):
        code, detail = M.measure(self.root, CASE, self.binary())
        self.assertEqual(code, 1, detail)
        self.assertIn("no observed effect", detail)
        self.assertEqual(self.retained(), [False, False])

    def test_either_existing_name_refuses_reuse_and_keeps_its_bytes(self):
        for index in range(2):
            with self.subTest(path=index):
                path = M.effect_paths(self.root, CASE)[index]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"retained")
                self.differ()
                code, detail = M.measure(self.root, CASE, self.binary())
                self.assertEqual(code, 2, detail)
                self.assertEqual(path.read_bytes(), b"retained")
                self.assertFalse(self.ran.exists(), "nothing ran")
                path.unlink()

    def test_a_case_without_its_own_configuration_refuses(self):
        (self.case / "reference-config.json").write_bytes(M.profile_config(self.root))
        self.differ()
        code, detail = M.measure(self.root, CASE, self.binary())
        self.assertEqual(code, 2, detail)
        self.assertIn("no configuration of its own", detail)
        self.assertFalse(self.ran.exists(), "nothing ran")

    def test_a_failed_process_retains_nothing(self):
        self.differ()
        code, detail = M.measure(self.root, CASE, self.binary(exit_code=3))
        self.assertEqual(code, 2, detail)
        self.assertIn("rc=3", detail)
        self.assertEqual(self.retained(), [False, False])

    def test_a_missing_trace_retains_nothing(self):
        self.differ()
        code, detail = M.measure(self.root, CASE, self.binary(trace=None))
        self.assertEqual(code, 2, detail)
        self.assertEqual(self.retained(), [False, False])

    def test_an_oversized_trace_retains_nothing(self):
        self.differ()
        code, detail = M.measure(self.root, CASE, self.binary(oversized=True))
        self.assertEqual(code, 2, detail)
        self.assertIn("above", detail)
        self.assertEqual(self.retained(), [False, False])

    def test_each_retained_effect_pins_its_case_and_differs_where_recorded(self):
        held = sorted(path.name.removesuffix(".effect.sexp") for path in (ROOT / "profiles/rv64gc-lab-v0/reference").glob("*.effect.sexp"))
        self.assertEqual(held, sorted(row[0] for row in RETAINED), "a retained effect this table does not judge")
        for case, step, register, observed, value in RETAINED:
            with self.subTest(case=case):
                case_dir = ROOT / "evidence" / case
                record, trace = M.effect_paths(ROOT, case)
                forms = M.S.parse(record.read_text(), record.name)
                fields = {child[0]: child[1] for form in forms for child in form[1:]}
                data = trace.read_bytes()
                self.assertEqual((fields["case_id"], fields["trace_sha256"], fields["trace_bytes"]), (case, sha(data), len(data)))
                self.assertEqual(fields["guest_sha256"], sha((case_dir / "guest.elf").read_bytes()))
                self.assertEqual(fields["case_config_sha256"], sha((case_dir / "reference-config.json").read_bytes()))
                live = sha(M.alternative_config(ROOT, case)[0])
                if case in STALE_SINCE_SLICE_D:
                    self.assertNotEqual(fields["alternative_config_sha256"], live, "a stale effect now pins the live configuration")
                else:
                    self.assertEqual(fields["alternative_config_sha256"], live)
                self.assertNotEqual(fields["alternative_config_sha256"], fields["case_config_sha256"])
                expected = M.D.load_expectations(case_dir / "baseline.expected.sexp")
                result = M.Sail.compare_observations(expected, data.decode("utf-8"))
                self.assertEqual((result.verdict, result.gpr_difference.step_n), ("DIVERGE", step))
                self.assertEqual((result.gpr_difference.observed, result.gpr_difference.expected), (tuple(observed), ((register, value),)))


def main():
    global M
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/measure_config_effect.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_measure_config_effect")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        M = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(EffectTests))
    print(f"CONFIG-EFFECT: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; "
          "synthetic configuration-effect controls, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
