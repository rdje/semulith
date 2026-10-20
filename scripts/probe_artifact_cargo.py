#!/usr/bin/env python3
"""Public Cargo boundary controls in disposable repository-volume fixtures."""
from __future__ import annotations

import argparse
import ast
from dataclasses import asdict
import hashlib
import importlib.util
import json
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
    "capture-success": ('    if result.returncode == 0:\n', '    if True:\n'),
    "capture-version": ('    O.need(result.returncode == 0, "Cargo version query failed")\n', ''),
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
    "capture-success": "test_failed_build_records_nothing_and_retires_only_absent_rows",
    "capture-version": "test_failed_or_unbounded_version_query_refuses_capture",
}


def producer_commands():
    """Evaluate only each producer's actual Cargo launch, with a recording stub."""
    rows = []
    for producer, root in (("scripts/probe_c_engine.py", "c-engine-build"),
                           ("scripts/probe_c_guest_image.py", "c-guest-image-build")):
        tree = ast.parse((ROOT / producer).read_text())
        main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
        block = next(node for node in main.body if isinstance(node, ast.With))
        launch = next(node for node in block.body if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
                      and any(isinstance(t, ast.Name) and t.id in {"run", "capture"} for t in node.targets))
        seen = []
        class Runner:
            @staticmethod
            def run(*args, **kwargs):
                seen.append((args, kwargs))
                return None

            @staticmethod
            def capture(*args, **kwargs):
                seen.append((args, kwargs))
                return None
        env_nodes = [node for node in block.body if isinstance(node, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "env" for t in node.targets)]
        # The old launch's env assignment is executed to reproduce the missing
        # intermediate-root binding; the repaired launch delegates to capture().
        namespace = dict(REPO=ROOT, parent=ROOT / "target/p4-system-12",
                         root=ROOT / "target/p4-system-12/fixture-input", os=os,
                         subprocess=Runner, artifact_cargo=Runner)
        ast.fix_missing_locations(tree := ast.Module(body=env_nodes + [launch], type_ignores=[]))
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

    def capture_bound(self, effect=None, *, version=(0, "cargo 1.0.0 (fixture)")):
        def child(argv, *args, **kwargs):
            if argv[1] == "--version":
                return subprocess.CompletedProcess(argv, version[0], version[1] + "\n", "")
            if effect:effect()
            return subprocess.CompletedProcess(argv, 0, "fixture stdout", "fixture stderr")
        with patch.object(self.c, "_process", side_effect=child):
            return self.c.capture(self.producer, self.manifest)

    def outcome(self, function, *args, **kwargs):
        try:
            return "ok", function(*args, **kwargs)
        except (self.o.ProvenanceError, self.a.CleanupError, self.a.Boundary, OSError) as error:
            return "refused", str(error)

    def source(self, name):
        data = (self.root / name).read_bytes()
        return self.o.Source(name, len(data), hashlib.sha256(data).hexdigest())

    @property
    def incremental(self):
        return self.o.PRODUCERS[self.producer][0] + "/debug/incremental"

    def test_capture_records_new_and_changed_outputs_with_complete_pins(self):
        base = self.incremental
        self.fixture.file(base + "/kept-1/s-1/dep-graph.bin", b"unchanged owned input")
        changing = self.fixture.file(base + "/probe-1/s-1/query-cache.bin", b"old cache")
        def build():
            changing.write_bytes(b"regenerated cache")
            self.fixture.file(base + "/probe-1/s-1/work-products.bin", b"new output")
        capture = self.capture_bound(build)
        self.assertEqual((capture.result.returncode, capture.observed, capture.recorded, capture.unclaimed), (0, 3, 2, 0))
        self.assertEqual((capture.publication.written, capture.publication.added, capture.publication.records), (True, 2, 2))
        raw = (self.root / self.o.LEDGER).read_bytes();ledger = self.o.decode(raw)
        self.assertEqual(ledger.format, self.o.CAPTURE_FORMAT)
        self.assertEqual([(row.after.path, row.before is None) for row in ledger.outputs],
                         [(base + "/probe-1/s-1/query-cache.bin", False), (base + "/probe-1/s-1/work-products.bin", True)])
        pins = tuple(self.source(name) for name in self.o.SUPPORTING_OBJECTS)
        self.assertTrue(all(row.supporting_sources == pins and row.recorder == self.source(self.o.OBJECT)
                            and row.producer == self.source(self.producer) and row.tool_version == "cargo 1.0.0 (fixture)"
                            and row.argv == self.c.command(self.producer, self.manifest.relative_to(self.root).as_posix())
                            for row in ledger.outputs))
        self.assertIn("recorded 2 of 3 observed outputs (0 unclaimed); ledger 2 records", self.c.describe(capture))
        self.assertEqual(hashlib.sha256(raw).hexdigest(), capture.publication.ledger_sha256)

    def test_run_publishes_no_provenance(self):
        self.run_bound(lambda: self.fixture.file(self.incremental + "/probe-1/s-1/dep-graph.bin", b"new output"))
        self.assertFalse((self.root / self.o.WORKSPACE).exists(), "command binding grants no provenance")

    def test_failed_build_records_nothing_and_retires_only_absent_rows(self):
        base = self.incremental
        def first():
            self.fixture.file(base + "/probe-1/s-1/dep-graph.bin", b"first build")
            self.fixture.file(base + "/probe-1/s-1/query-cache.bin", b"first build cache")
        self.assertEqual(self.capture_bound(first).publication.records, 2)
        def failing(argv, *args, **kwargs):
            if argv[1] == "--version":
                return subprocess.CompletedProcess(argv, 0, "cargo 1.0.0 (fixture)\n", "")
            (self.root / base / "probe-1/s-1/query-cache.bin").unlink(missing_ok=True)  # rustc GC of a recorded session; fixture only
            self.fixture.file(base + "/probe-1/s-2/dep-graph.bin", b"partial output of a failed build")
            return subprocess.CompletedProcess(argv, 42, "", "failure")
        with patch.object(self.c, "_process", side_effect=failing):
            disposition, capture = self.outcome(self.c.capture, self.producer, self.manifest)
        self.assertEqual(disposition, "ok", capture)
        publication = capture.publication
        self.assertEqual((capture.result.returncode, capture.observed, capture.recorded, publication.written,
                          publication.added, publication.retired, publication.retained, publication.records), (42, 2, 0, True, 0, 1, 1, 1))
        ledger = self.o.decode((self.root / self.o.LEDGER).read_bytes())
        self.assertEqual([row.after.path for row in ledger.outputs], [base + "/probe-1/s-1/dep-graph.bin"])
        self.assertIn("recorded 0 of 2 observed outputs (0 unclaimed); ledger 1 records", self.c.describe(capture))
        with patch.object(self.c, "_process", side_effect=failing):
            self.assertFalse(self.c.capture(self.producer, self.manifest).publication.written, "nothing further to retire")

    def test_source_change_after_the_build_refuses_before_publication(self):
        base = self.incremental
        original = self.c._invoke
        def invoke(*args, **kwargs):
            outcome = original(*args, **kwargs)
            path = self.root / "scripts/artifact_cleanup.py";path.write_bytes(path.read_bytes() + b"\n# changed after the build\n")
            return outcome
        with patch.object(self.c, "_invoke", side_effect=invoke):
            disposition, detail = self.outcome(self.capture_bound, lambda: self.fixture.file(base + "/probe-1/s-1/dep-graph.bin", b"new"))
        self.assertEqual(disposition, "refused", detail);self.assertIn("current recorder, producer and support pins", detail)
        self.assertFalse((self.root / self.o.WORKSPACE).exists())

    def test_failed_or_unbounded_version_query_refuses_capture(self):
        base = self.incremental
        effect = lambda: self.fixture.file(base + "/probe-1/s-1/dep-graph.bin", b"new")
        disposition, detail = self.outcome(self.capture_bound, effect, version=(1, "cargo 1.0.0 (fixture)"))
        self.assertEqual(disposition, "refused", detail);self.assertIn("version query failed", detail)
        self.assertFalse((self.root / self.o.WORKSPACE).exists())
        refused = []
        for text in ("", "x" * 1025, "two\nlines"):
            disposition, detail = self.outcome(self.capture_bound, effect, version=(0, text))
            if disposition == "refused" and "tool version bound" in detail:refused.append(text)
        self.assertEqual(len(refused), 3)

    def test_capture_retires_absent_rows_when_nothing_changes(self):
        base = self.incremental
        def build():
            self.fixture.file(base + "/probe-1/s-1/dep-graph.bin", b"a");self.fixture.file(base + "/probe-1/s-1/query-cache.bin", b"b")
        first = self.capture_bound(build)
        self.assertEqual((first.recorded, first.publication.records), (2, 2))
        (self.root / base / "probe-1/s-1/query-cache.bin").unlink()  # Only this test's disposable fixture.
        second = self.capture_bound()
        publication = second.publication
        self.assertEqual((second.recorded, publication.written, publication.added, publication.retired, publication.retained, publication.records),
                         (0, True, 0, 1, 1, 1))
        third = self.capture_bound()
        self.assertEqual((third.recorded, third.publication.written, third.publication.records), (0, False, 1))
        self.assertIn("ledger unchanged (1 records, sha256 " + publication.ledger_sha256[:16] + ")", self.c.describe(third))
        self.assertEqual(self.o.decode((self.root / self.o.LEDGER).read_bytes()).outputs[0].after.path, base + "/probe-1/s-1/dep-graph.bin")

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

    def test_actual_cargo_build_in_cold_copy_publishes_provenance_and_preserves_input(self):
        name = self.incremental + "/retained-fixture/s/dep-graph.bin"
        retained = self.fixture.file(name, b"unchanged owned fixture input")
        before = retained.read_bytes()
        env = dict(os.environ, **self.fixture.fake_git())
        code = ("import json,sys;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv[1]);"
                "import artifact_cargo as C;from dataclasses import asdict;"
                "c=C.capture('scripts/probe_c_engine.py',C.ROOT/'target/p4-system-12/fixture-input/Cargo.toml');"
                "print(json.dumps(dict(stdout=c.result.stdout,observed=c.observed,recorded=c.recorded,unclaimed=c.unclaimed,"
                "publication=None if c.publication is None else asdict(c.publication),line=C.describe(c))));"
                "raise SystemExit(c.result.returncode)")
        result = subprocess.run([sys.executable, "-B", "-c", code, str(self.root / "scripts")],
            cwd=ROOT.parent, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("1 passed", report["stdout"]);self.assertEqual(retained.read_bytes(), before)
        caches = list((self.root / self.incremental).glob("*/*/query-cache.bin"))
        self.assertTrue(caches, "actual public Cargo must generate observed incremental output")
        publication = report["publication"]
        self.assertTrue(report["recorded"] >= 1 and publication["written"] and publication["added"] == report["recorded"]
                        and report["observed"] == report["recorded"] + 1 and report["unclaimed"] == 0, report)
        ledger = self.o.decode((self.root / self.o.LEDGER).read_bytes())
        pins = tuple(self.source(name) for name in self.o.SUPPORTING_OBJECTS)
        self.assertEqual((ledger.format, len(ledger.outputs)), (self.o.CAPTURE_FORMAT, report["recorded"]))
        self.assertNotIn(name, [row.after.path for row in ledger.outputs])
        self.assertTrue(all(row.supporting_sources == pins and row.before is None and row.tool_version.startswith("cargo ")
                            and row.recorder == self.source(self.o.OBJECT) for row in ledger.outputs))
        self.assertIn("output provenance: recorded " + str(report["recorded"]) + " of ", report["line"])


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
