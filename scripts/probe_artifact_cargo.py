#!/usr/bin/env python3
"""Public Cargo boundary controls in disposable repository-volume fixtures."""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
import probe_artifact_cleanup as P

ROOT = Path(__file__).resolve().parent.parent
MUTATION = None
SEAMS = {
    "build-root": ('"--config", \'build.build-dir="\' + root + \'"\',', '"--config", \'build.jobs=1\','),
    "environment": ('if not name.startswith(("CARGO_", "RUSTC", "RUSTDOC", "GIT_"))', 'if True'),
    "root-binding": ('ROOT == A.ROOT == O.ROOT', 'True'),
    "source-recheck": ('all(O._source(owned, source) == fact for source, fact in snapshots.items())', 'True'),
    "manifest-recheck": ('before == after', 'True'),
    "pipe-bound": ('len(buffers[index]) <= pipe_bytes', 'True'),
    "group-join": ('            _stop(child)\n            return subprocess.CompletedProcess',
                   '            return subprocess.CompletedProcess'),
    "group-kill": ('        os.killpg(child.pid, signal.SIGKILL)', '        pass'),
}
TARGETS = {
    "build-root": "test_exact_command_matches_the_closed_provenance_protocol",
    "environment": "test_ambient_build_overrides_cannot_escape_the_bound_environment",
    "root-binding": "test_root_mismatch_refuses_before_any_public_query",
    "source-recheck": "test_source_change_refuses_a_completed_observation",
    "manifest-recheck": "test_manifest_change_refuses_a_completed_observation",
    "pipe-bound": "test_each_pipe_overflow_refuses_and_joins",
    "group-join": "test_even_success_joins_the_owned_process_group",
    "group-kill": "test_a_descendant_closing_pipes_cannot_outlive_the_invocation",
}


def producer_commands():
    """Evaluate only each producer's actual Cargo launch, with a recording stub."""
    rows = []
    for producer, root in (("scripts/probe_c_engine.py", "c-engine-build"),
                           ("scripts/probe_c_guest_image.py", "c-guest-image-build")):
        tree = ast.parse((ROOT / producer).read_text())
        main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
        block = next(node for node in main.body if isinstance(node, ast.With))
        run = next(node for node in block.body if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "run" for t in node.targets))
        seen = []
        class Runner:
            @staticmethod
            def run(*args, **kwargs):
                seen.append((args, kwargs))
                return None
        env_nodes = [node for node in block.body if isinstance(node, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "env" for t in node.targets)]
        # The old launch's env assignment is executed to reproduce the missing
        # intermediate-root binding; the repaired launch delegates to run().
        namespace = dict(REPO=ROOT, parent=ROOT / "target/p4-system-12",
                         root=ROOT / "target/p4-system-12/fixture-input", os=os,
                         subprocess=Runner, artifact_cargo=Runner)
        ast.fix_missing_locations(tree := ast.Module(body=env_nodes + [run], type_ignores=[]))
        exec(compile(tree, producer, "exec"), namespace)
        args, kwargs = seen[0]
        rows.append((producer, root, args, kwargs))
    return rows


class CargoTests(unittest.TestCase):
    def setUp(self):
        self.fixture = P.CohortTests(methodName="runTest");self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root, self.a = self.fixture.root, self.fixture.m
        self.modules = {}
        for short in ("artifact_output_provenance", "artifact_cargo"):
            name = "scripts/" + short + ".py"
            text = (ROOT / name).read_text()
            if MUTATION and short == "artifact_cargo":
                old, new = SEAMS[MUTATION]
                if text.count(old) != 1:raise RuntimeError("singular omission seam: " + MUTATION)
                text = text.replace(old, new, 1)
            path = self.fixture.file(name, text.encode())
            module_name = short + "_" + hashlib.sha256(str(self.root).encode()).hexdigest()
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec);sys.modules[module_name] = module
            self.addCleanup(sys.modules.pop, module_name)
            with patch.dict(sys.modules, artifact_cleanup=self.a, **self.modules):
                spec.loader.exec_module(module)
            self.modules[short] = module
        self.c = self.modules["artifact_cargo"];self.o = self.modules["artifact_output_provenance"]
        self.producer = "scripts/probe_c_engine.py"
        self.fixture.file(self.producer, b"owned fixture producer\n")
        self.manifest = self.fixture.file("target/p4-system-12/fixture-input/Cargo.toml",
            b'[package]\nname="owned-cargo-boundary"\nversion="0.0.0"\nedition="2021"\n[workspace]\n')
        self.fixture.file("target/p4-system-12/fixture-input/src/lib.rs",
                          b"#[cfg(test)] mod c_engine { #[test] fn owned() { assert_eq!(2+2,4); } }\n")

    def run_bound(self, effect=None):
        def child(*args):
            if effect:effect()
            return subprocess.CompletedProcess(args[0], 0, "fixture stdout", "fixture stderr")
        with patch.object(self.c, "_process", side_effect=child) as process:
            result = self.c.run(self.producer, self.manifest)
        return result, process

    def test_exact_command_matches_the_closed_provenance_protocol(self):
        for producer in self.o.PRODUCERS:
            argv = self.c.command(producer, self.manifest.relative_to(self.root).as_posix())
            root, test_filter = self.o.PRODUCERS[producer]
            self.assertEqual(argv, ("cargo", "test", "--offline", "--manifest-path",
                "target/p4-system-12/fixture-input/Cargo.toml", "--target-dir", root,
                "--config", 'build.build-dir="' + root + '"', "--lib", test_filter, "--", "--nocapture"))

    def test_actual_producers_delegate_without_ambient_directory_selection(self):
        for producer, _, args, kwargs in producer_commands():
            self.assertTrue(args == (producer, ROOT / "target/p4-system-12/fixture-input/Cargo.toml")
                            and not kwargs, "producer must delegate its actual bound invocation")

    def test_ambient_build_overrides_cannot_escape_the_bound_environment(self):
        names = ("CARGO_BUILD_BUILD_DIR", "CARGO_BUILD_TARGET", "CARGO_ENCODED_RUSTFLAGS",
                 "RUSTC_WRAPPER", "RUSTFLAGS", "RUSTDOCFLAGS", "GIT_DIR")
        with patch.dict(os.environ, {name: "foreign" for name in names}):
            env = self.c.environment()
        self.assertFalse(set(names) & set(env))
        self.assertEqual(env["CARGO_HOME"], str(self.root / ".app-data/cargo-home"))
        for name in ("TMPDIR", "TMP", "TEMP"):
            self.assertEqual(env[name], str(self.root / "target/p4-system-12"))

    def test_completed_result_and_original_command_are_preserved(self):
        result, process = self.run_bound()
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "fixture stdout", "fixture stderr"))
        self.assertEqual(process.call_args.args[0], self.c.command(self.producer, self.manifest.relative_to(self.root).as_posix()))

    def test_nonzero_build_is_returned_without_claiming_success(self):
        with patch.object(self.c, "_process", return_value=subprocess.CompletedProcess([], 42, "", "failure")):
            self.assertEqual(self.c.run(self.producer, self.manifest).returncode, 42)

    def test_root_mismatch_refuses_before_any_public_query(self):
        self.o.ROOT = self.fixture.base
        with patch.object(self.a, "tracked_paths") as inventory:
            with self.assertRaisesRegex(self.o.ProvenanceError, "roots differ"):
                self.c.run(self.producer, self.manifest)
            self.assertEqual(inventory.call_count, 0)

    def test_foreign_or_unowned_manifest_and_unknown_producer_refuse(self):
        for producer, manifest in (("scripts/unknown.py", self.manifest),
                (self.producer, self.fixture.base / "Cargo.toml"),
                (self.producer, self.root / self.o.PRODUCERS[self.producer][0] / "Cargo.toml")):
            with self.subTest(manifest=manifest), patch.object(self.c, "_process") as process:
                with self.assertRaises(self.o.ProvenanceError):self.c.run(producer, manifest)
                self.assertEqual(process.call_count, 0)

    def test_source_change_refuses_a_completed_observation(self):
        with self.assertRaisesRegex(self.o.ProvenanceError, "source changed"):
            self.run_bound(lambda: self.fixture.file(self.producer, b"changed during build"))

    def test_manifest_change_refuses_a_completed_observation(self):
        with self.assertRaisesRegex(self.o.ProvenanceError, "manifest changed"):
            self.run_bound(lambda: self.manifest.write_bytes(b"changed during build"))

    def test_symlink_and_nested_git_output_roots_refuse_before_launch(self):
        path = self.root / self.o.PRODUCERS[self.producer][0];path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(self.manifest.parent, target_is_directory=True)
        with patch.object(self.c, "_process") as process:
            with self.assertRaises(self.a.Boundary):self.c.run(self.producer, self.manifest)
            self.assertEqual(process.call_count, 0)
        path.unlink();path.mkdir();(path / ".git").mkdir()
        with patch.object(self.c, "_process") as process:
            with self.assertRaises(self.a.Boundary):self.c.run(self.producer, self.manifest)
            self.assertEqual(process.call_count, 0)

    def test_each_pipe_overflow_refuses_and_joins(self):
        refused = []
        for target in ("stdout", "stderr"):
            try:
                self.c._process([sys.executable, "-B", "-c", f"import sys;sys.{target}.write('x'*1024)"],
                                self.c.environment(), pipe_bytes=128)
            except self.o.ProvenanceError as error:
                if "output exceeds bound" in str(error):refused.append(target)
                else:raise
        self.assertEqual(refused, ["stdout", "stderr"])

    def test_deadline_refuses_and_joins_the_owned_process(self):
        with self.assertRaisesRegex(self.o.ProvenanceError, "timed out"):
            self.c._process([sys.executable, "-B", "-c", "import time;time.sleep(10)"],
                            self.c.environment(), timeout=0.05)

    def test_even_success_joins_the_owned_process_group(self):
        with patch.object(self.c, "_stop", wraps=self.c._stop) as stop:
            result = self.c._process([sys.executable, "-B", "-c", "print('owned result')"], self.c.environment())
        self.assertEqual(result.stdout, "owned result\n");self.assertEqual(stop.call_count, 1)

    def test_interruption_joins_the_owned_process_group(self):
        with patch.object(self.c.selectors.DefaultSelector, "select", side_effect=KeyboardInterrupt), \
                patch.object(self.c, "_stop", wraps=self.c._stop) as stop:
            with self.assertRaises(KeyboardInterrupt):
                self.c._process([sys.executable, "-B", "-c", "import time;time.sleep(10)"], self.c.environment())
            self.assertEqual(stop.call_count, 1)

    def test_a_descendant_closing_pipes_cannot_outlive_the_invocation(self):
        descendant = ("from pathlib import Path;import time;"
            "Path('started').write_text('started');time.sleep(0.3);Path('outlived').write_text('outlived')")
        code = ("import subprocess,sys,time;from pathlib import Path;"
                "p=subprocess.Popen([sys.executable,'-B','-c'," + repr(descendant) + "],"
                "stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);"
                "\nwhile not Path('started').exists(): time.sleep(0.01)\nprint(p.pid)")
        result = self.c._process([sys.executable, "-B", "-c", code], self.c.environment(), timeout=2)
        pid = int(result.stdout.strip())
        try:
            self.assertTrue((self.root / "started").is_file())
            time.sleep(0.5)
            self.assertFalse((self.root / "outlived").exists(), "owned descendant outlived its invocation")
        finally:
            try:os.kill(pid, self.c.signal.SIGKILL)
            except ProcessLookupError:pass

    def test_deadline_still_applies_after_both_pipes_close(self):
        with self.assertRaisesRegex(self.o.ProvenanceError, "timed out"):
            self.c._process([sys.executable, "-B", "-c",
                "import os,time;os.close(1);os.close(2);time.sleep(10)"], self.c.environment(), timeout=0.05)

    def test_actual_cargo_build_in_cold_copy_preserves_cache_shaped_input(self):
        retained = self.fixture.file(self.o.PRODUCERS[self.producer][0] +
            "/debug/incremental/retained-fixture/s/dep-graph.bin", b"unchanged owned fixture input")
        before = retained.read_bytes()
        env = dict(os.environ, **self.fixture.fake_git())
        code = ("import sys;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv[1]);"
                "import artifact_cargo as C;from pathlib import Path;"
                "r=C.run('scripts/probe_c_engine.py',C.ROOT/'target/p4-system-12/fixture-input/Cargo.toml');"
                "print(r.stdout);print(r.stderr);raise SystemExit(r.returncode)")
        result = subprocess.run([sys.executable, "-B", "-c", code, str(self.root / "scripts")],
            cwd=ROOT.parent, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("1 passed", result.stdout);self.assertEqual(retained.read_bytes(), before)
        caches = list((self.root / self.o.PRODUCERS[self.producer][0]).glob("debug/incremental/*/*/query-cache.bin"))
        self.assertTrue(caches, "actual public Cargo must generate observed incremental output")
        self.assertFalse((self.root / self.o.LEDGER).exists(), "command binding grants no provenance")


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    parser.add_argument("--producer-contract", action="store_true")
    args = parser.parse_args();MUTATION = args.mutation
    if args.producer_contract:
        for producer, root, argv, kwargs in producer_commands():
            print(producer, "args=", argv, "env-build-dir=", kwargs.get("env", {}).get("CARGO_BUILD_BUILD_DIR"))
        return 0
    suite = (unittest.TestSuite([CargoTests(TARGETS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(CargoTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"artifact Cargo: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
