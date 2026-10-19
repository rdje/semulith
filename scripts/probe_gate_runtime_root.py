#!/usr/bin/env python3
"""Exercise source-rooted gate imports and local registries in an owned runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import gate_report as G
import record_catalog as C

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "profiles/rv64gc-lab-v0"
REGISTRY = "crates/semulith-verify/src/contract_checks_rv64gc.rs"
MODULES = ("gate_report", "records_sexp", "record_catalog", "dossier_sexp", "sexp")
MUTATION = None
SOURCE_ROOT = "ROOT = Path(__file__).resolve().parent.parent\n"
GIT_ROOT = '''ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
'''

# Only the owned child runs this program. It imports the actual copied module;
# parent cwd/Git metadata cannot supply the runtime's modules or registry.
CHILD = '''from pathlib import Path
import json,subprocess,sys
runtime=Path(sys.argv[1]);mode=sys.argv[2];sys.path.insert(0,str(runtime/'scripts'))
commands=[];original_run=subprocess.run;original_popen=subprocess.Popen
def run(command,*args,**kwargs):
 commands.append(command)
 if mode=='deny-process':raise RuntimeError('unexpected import process')
 return original_run(command,*args,**kwargs)
def popen(command,*args,**kwargs):
 commands.append(command)
 if mode=='deny-process':raise RuntimeError('unexpected import process')
 return original_popen(command,*args,**kwargs)
subprocess.run=run;subprocess.Popen=popen
try:
 import gate_report as owner
except Exception as error:
 print(json.dumps(dict(status='import-error',error=type(error).__name__,commands=commands)))
 sys.exit(0)
finally:
 subprocess.run=original_run;subprocess.Popen=original_popen
report=dict(root_matches=owner.ROOT==runtime,commands=commands,
 local_modules={name:Path(module.__file__).resolve().is_relative_to(runtime)
                for name,module in [('gate_report',owner),('records_sexp',owner.R),
                ('record_catalog',owner.C),('dossier_sexp',owner.D),('sexp',owner.S)]})
try:
 directory=runtime/'profiles/rv64gc-lab-v0'
 obligations=owner.R.load(directory/'contract-obligations.sexp',root=runtime)
 declared,realized=owner.contract_measure(directory,obligations)
 report.update(status='measured',declared=declared,realized=realized)
except FileNotFoundError:
 report.update(status='unavailable',error='FileNotFoundError')
except SystemExit as error:
 report.update(status='refused',reason=str(error))
print(json.dumps(report))
'''


class RuntimeRootTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obligations = C.text(PROFILE / "contract-obligations.sexp")
        cls.expected = G.contract_measure(
            PROFILE, G.R.load(PROFILE / "contract-obligations.sexp"))

    def setUp(self):
        base = ROOT / "target/gate-runtime-root-controls"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.runtime = Path(self.temporary.name) / "runtime with spaces"
        for name in MODULES:
            target = self.runtime / "scripts" / (name + ".py")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / "scripts" / (name + ".py"), target)
        if MUTATION:
            target = self.runtime / "scripts/gate_report.py"
            source = target.read_text()
            if source.count(SOURCE_ROOT) != 1:
                raise RuntimeError("root omission target must be singular")
            target.write_text(source.replace(SOURCE_ROOT, GIT_ROOT, 1))
        directory = self.runtime / "profiles/rv64gc-lab-v0"
        directory.mkdir(parents=True)
        (directory / "contract.sexp").write_bytes((PROFILE / "contract.sexp").read_bytes())
        (directory / "contract-obligations.sexp").write_text(self.obligations)
        self.registry = self.runtime / REGISTRY
        self.registry.parent.mkdir(parents=True)
        self.registry.write_bytes((ROOT / REGISTRY).read_bytes())

    def inspect(self, mode="observe"):
        # Deliberately keep the parent checkout as cwd: a Git-root fallback would
        # see a valid parent registry and conceal a missing or damaged local one.
        result = subprocess.run(
            [sys.executable, *(["-O"] if sys.flags.optimize else []), "-c", CHILD,
             str(self.runtime), mode], cwd=ROOT, capture_output=True, text=True,
            timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_runtime_root_and_dependencies_follow_the_copied_source(self):
        report = self.inspect()
        self.assertEqual(report["status"], "measured", report)
        self.assertTrue(report["root_matches"], report)
        self.assertEqual(report["local_modules"], {name: True for name in MODULES})

    def test_import_needs_no_process(self):
        report = self.inspect("deny-process")
        self.assertEqual(report["status"], "measured", report)
        self.assertEqual(report["commands"], [])

    def test_missing_local_registry_cannot_use_parent_checks(self):
        self.registry.unlink()
        report = self.inspect()
        self.assertEqual(report["status"], "unavailable", report)

    def test_malformed_local_registry_cannot_use_parent_checks(self):
        self.registry.write_text("ContractCheck { broken fixture\n")
        report = self.inspect()
        self.assertEqual(report["status"], "refused", report)
        self.assertIn("registry's shape changed", report["reason"])

    def test_empty_local_registry_realizes_no_checks(self):
        self.registry.write_bytes(b"")
        report = self.inspect()
        self.assertEqual(report["status"], "measured", report)
        self.assertTrue(report["declared"])
        self.assertEqual(report["realized"], [])

    def test_complete_local_registry_preserves_the_current_results(self):
        report = self.inspect()
        self.assertEqual(report["status"], "measured", report)
        self.assertEqual(report["declared"], [list(pair) for pair in self.expected[0]])
        self.assertEqual(report["realized"], [list(pair) for pair in self.expected[1]])


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=("git-root",))
    args = parser.parse_args()
    MUTATION = args.mutation
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(RuntimeRootTests))
    print(f"GATE-RUNTIME-ROOT: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; local authority, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
