#!/usr/bin/env python3
"""Copied DIV command controls; synthetic processes, no Sail or qualification."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import capture_div as A
import derive_rv64gc_expectations as Author

ROOT = Path(__file__).resolve().parent.parent
MUTATION = None
SEAMS = {
    "native-declarations": ('require(_read_pinned(binding, len(payload)) == payload, "native predeclaration differs")',
                            'require(True, "native predeclaration differs")'),
    "authority-stability": ('review["authorities"]["context"] == report(context)', 'True'),
    "retained-identity": ('identity.disposition == "matched", "selected retained identity differs"',
                          'True, "selected retained identity differs"'),
    "planned-schema": ('not issues, "planned record shape/scoped graph refuses: "',
                       'True, "planned record shape/scoped graph refuses: "'),
    "author-delegation": ('author_review=declaration.author,', 'author_review=None,'),
    "impact-delegation": ('impact_review=declaration.impact,', 'impact_review=None,'),
    "property-delegation": ('property_authority=declaration.authorities.property_authority,',
                            'property_authority=None,'),
}
CHILD = r'''
from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest.mock import patch
import hashlib,json,subprocess,sys
runtime=Path(sys.argv[1]);mode=sys.argv[2];sys.path.insert(0,str(runtime/'scripts'))
import capture_div as A

def declaration():
 return A.prepare_capture()

def publish(d):
 for name,payload in A.declaration_files(d):
  with (runtime/A.PREFIX/name).open('xb') as stream:stream.write(payload)

def deny(*args,**kwargs):raise RuntimeError('unexpected reference process')

try:
 if mode=='integration':
  d=declaration();publish(d);r=A.capture();evaluation=r.evaluation
  findings={name:None if evaluation is None or getattr(evaluation,name) is None else getattr(evaluation,name).disposition
            for name in ('input_review','impact','expected_author','source_property','source_values','source_image')}
  result=dict(status=r.disposition,collection=None if r.collection is None else r.collection.disposition,
              evaluation=None if evaluation is None else evaluation.disposition,findings=findings,
              pids=0 if r.collection is None else len({run.process.pid for run in r.collection.runs if run.process}),
              measured=isinstance(r.experiment,bytes),charge=0<r.charged_read_bytes<=134217728,
              reuse=None,preserved=None,offline=None)
  if r.disposition=='pending':
   files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (runtime/A.PREFIX).iterdir()}
   again=A.capture();result['reuse']=again.disposition
   result['preserved']=files=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (runtime/A.PREFIX).iterdir()}
   # Offline checking uses the real public evaluator without the executable.
   binary=runtime/dict(d.authorities.reference.fields)['binary'];binary.unlink()
   raw=next(form for form in A.S.parse(r.experiment.decode()) if form[0]=='experiment')
   with patch.object(subprocess,'Popen',deny):
    checked=A.Unit.Evaluation.evaluate_retained_unit(runtime,raw_experiment=raw,
      scope=d.authorities.scope,current_candidate=dict(d.authorities.reference.fields),
      reviewed_inputs=d.inventory,author_review=d.author,impact_review=d.impact,
      property_authority=d.authorities.property_authority)
   result['offline']=checked.disposition
 elif mode=='audit':
  writes=[];opened=Path.open
  def traced(path,*args,**kwargs):
   access=args[0] if args else kwargs.get('mode','r')
   if any(flag in access for flag in 'wax+'):writes.append(str(path))
   return opened(path,*args,**kwargs)
  with patch.object(subprocess,'Popen',deny),patch.object(Path,'open',traced):d=declaration()
  documents=dict(A.declaration_files(d));manifest=A.F.parse_dependencies(d.dependencies,path=A.PREFIX+'/dependencies.sexp')
  raw=next(form for form in A.S.parse(d.planned_experiment.decode()) if form[0]=='experiment')
  mapped=A.D.references_to_doc([A.S.Symbol('references'),raw])['experiment'][0]
  native=A.Unit.Evaluation.B.bind_relations(mapped,dict(d.authorities.reference.fields))
  principals=(*native.plan.execution.common_inputs,native.plan.execution.baseline_expectation,native.plan.execution.control_expectation)
  children=tuple(A.Execution.InputBinding(row['role'],row['id'],row['path'],row['sha256']) for row in manifest['input'])
  supplied=tuple(sorted((*principals,*children),key=lambda item:item.input_id))
  frozen=[]
  for obj,field in ((d,'dependencies'),(d.authorities,'scope'),(d.inventory,'inputs'),(d.author,'route'),(d.impact,'current')):
   try:setattr(obj,field,None)
   except FrozenInstanceError:frozen.append(True)
  result=dict(status='pending',children=len(children),inputs=len(d.inventory.inputs),
    exact_inventory=supplied==d.inventory.inputs,writes=writes,frozen=frozen,
    raw_issues=A.V.check_experiment(raw,d.authorities.scope),
    declarations={name:len(payload) for name,payload in documents.items()},
    witnesses=mapped['verification']['property'][0]['gpr_witness'],
    roots=(A.ROOT==runtime and A.Review.ROOT==runtime and A.V.ROOT==runtime))
 elif mode.startswith(('missing:','changed:')):
  operation,name=mode.split(':',1);d=declaration();publish(d);path=runtime/A.PREFIX/name
  if operation=='missing':path.unlink()
  else:path.write_bytes(path.read_bytes()+b'\n')
  # A reached delegate is reported, so an omitted guard is an assertion failure.
  with patch.object(A.Unit,'capture_and_evaluate',return_value=A.Unit.UnitEvaluation('pending','injected')):
   result=dict(status=A.capture().disposition)
 elif mode=='drift':
  original=A.review_authorities;calls=0
  def change():
   global calls
   context=original();p=runtime/A.DIRECTORY/'requirements.sexp'
   if calls==0:p.write_bytes(p.read_bytes()+b'\n(comment "owned between-view drift")\n')
   calls+=1;return context
  with patch.object(A,'review_authorities',change):declaration()
  result=dict(status='pending')
 elif mode=='bad-raw':
  original=A.D.references_to_form
  def malformed(document):
   form=original(document)
   for exp in A.S.children(form,'experiment'):exp.append([A.S.Symbol('instructions'),27])
   return form
  with patch.object(A.D,'references_to_form',malformed):declaration()
  result=dict(status='pending')
 elif mode=='existing-output':
  d=declaration();publish(d);p=runtime/A.PREFIX/'baseline.trace';p.write_bytes(b'old historical bytes')
  with patch.object(subprocess,'Popen',deny):r=A.capture()
  result=dict(status=r.disposition,runs=0 if r.collection is None else len(r.collection.runs),old=p.read_bytes().decode())
 elif mode=='failed-cli':
  with patch.object(sys,'argv',['capture_div.py','--capture']),patch.object(A,'capture',return_value=A.Unit.UnitEvaluation('failed','synthetic failure')):
   code=A.main()
  print(json.dumps(dict(exit=code)));sys.exit(0)
 elif mode=='unavailable-kind':
  from types import SimpleNamespace
  binding=A.Execution.InputBinding('expectation','fixture','inputs/fixture','0'*64)
  pin=SimpleNamespace(disposition='unavailable',reason='permission denied')
  with patch.object(A.Artifacts,'read_snapshot',return_value=SimpleNamespace(pin=pin)):
   try:A._read_pinned(binding)
   except OSError as error:
    result=dict(status='unavailable',kind=type(error).__name__,reason=str(error))
 else:
  with patch.object(subprocess,'Popen',deny):declaration()
  result=dict(status='pending')
except (FileNotFoundError,A.CaptureUnavailable) as error:result=dict(status='unavailable',reason=str(error))
except (A.AuthorityError,A.Review.ReviewError,A.F.ArtifactError,A.K.SchemaError,A.D.DossierError,A.S.SexpError) as error:
 result=dict(status='refused',reason=str(error))
print(json.dumps(result))
'''


class CommandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        review = A.Review.review()
        cls.paths = {row["path"] for row in review["files"]} | {row[2] for row in A.PREPARED}

    def setUp(self):
        base = ROOT / "target/div-command-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.runtime = Path(temporary.name) / "runtime"
        for relative in sorted(self.paths):
            path = self.runtime / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, path)
        if MUTATION:
            path = self.runtime / "scripts/capture_div.py"
            source = path.read_text()
            before, after = SEAMS[MUTATION]
            if source.count(before) != 1:
                raise RuntimeError("command omission target must be singular")
            path.write_text(source.replace(before, after, 1))

    def inspect(self, mode="audit"):
        result = subprocess.run([sys.executable, *(["-O"] if sys.flags.optimize else []),
                                 "-B", "-c", CHILD, str(self.runtime), mode], cwd=ROOT,
                                capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout.splitlines()[-1])

    def candidate(self):
        path = self.runtime / A.DIRECTORY / "references.sexp"
        forms = A.S.parse(path.read_text())
        document = next(form for form in forms if form[0] == "references")
        candidate = next(form for form in A.S.children(document, "candidate")
                         if A.S.field(form, "id") == "sail-riscv")
        return path, forms, candidate

    def synthetic_reference(self, *, exit_code=0):
        """Change only owned fixture identities; the child imports them fresh."""
        source = (self.runtime / A.Review.GUEST).read_bytes()
        derived = Author.derive_snapshot(source, program="m-div.s", instructions=27)
        lines = []
        for step in derived.steps:
            lines.append(f"[{step.n}] [M]: 0x{step.pc:016x} (0x{step.instruction_bits:08x}) synthetic fixture")
            lines.extend(f"x{reg} <- 0x{value:016x}" for reg, value in step.writes)
        trace = ("\n".join(lines) + "\n").encode()
        path, forms, candidate = self.candidate()
        old = A.S.field(candidate, "binary_sha256")
        binary = self.runtime / A.S.field(candidate, "binary")
        binary.parent.mkdir(parents=True, exist_ok=True)
        binary.write_text("#!" + sys.executable + " -B\nfrom pathlib import Path\nimport sys\n"
                          + "Path(sys.argv[9]).write_bytes(" + repr(trace) + ")\n"
                          + "sys.exit(" + str(exit_code) + ")\n")
        binary.chmod(0o755)
        digest = hashlib.sha256(binary.read_bytes()).hexdigest()
        A.S.children(candidate, "binary_sha256")[0][1] = digest
        path.write_text(A.R.render_forms(forms))
        identity = self.runtime / A.IDENTITY_PATH
        identity.write_bytes(identity.read_bytes().replace(old.encode(), digest.encode()))
        entry = self.runtime / "scripts/capture_div.py"
        entry.write_text(entry.read_text().replace(A.PREPARED[-1][-1], hashlib.sha256(identity.read_bytes()).hexdigest(), 1))

    def test_exact_real_declaration_inventory_and_readonly_copy(self):
        result = self.inspect()
        self.assertEqual((result["status"], result["children"], result["inputs"]), ("pending", 64, 73))
        self.assertTrue(result["exact_inventory"])
        self.assertEqual(result["writes"], [])
        self.assertEqual(result["frozen"], [True] * 5)
        self.assertEqual(result["raw_issues"], [])
        self.assertEqual(result["witnesses"], dict(step_n=2, register="x7"))
        self.assertTrue(result["roots"])
        self.assertTrue(all(0 < size <= 65536 for size in result["declarations"].values()))
        self.assertFalse((self.runtime / ".git").exists())
        self.assertFalse((self.runtime / ".materials").exists())
        self.assertEqual(len(list((self.runtime / A.PREFIX).iterdir())), 4)

    def test_three_fresh_synthetic_processes_offline_evaluation_and_preserved_reuse(self):
        self.synthetic_reference()
        result = self.inspect("integration")
        self.assertEqual(result, dict(status="pending", collection="recorded", evaluation="pending",
                                     findings={name: "matched" for name in (
                                         "input_review", "impact", "expected_author", "source_property", "source_values", "source_image")},
                                     pids=3, measured=True, charge=True, reuse="refused", preserved=True, offline="pending"))

    def test_failed_process_remains_data_and_stops_collection(self):
        self.synthetic_reference(exit_code=7)
        result = self.inspect("integration")
        self.assertEqual((result["status"], result["collection"], result["evaluation"], result["pids"]),
                         ("failed", "failed", None, 1))
        receipt = self.runtime / A.PREFIX / "baseline.receipt.sexp"
        self.assertTrue(receipt.is_file())
        self.assertFalse((self.runtime / A.PREFIX / "repeat.trace").exists())

    def test_each_missing_native_declaration_stops_before_delegate(self):
        for name in ("planned-experiment.sexp", "dependencies.sexp", "authorities.sexp"):
            with self.subTest(name=name):
                try:
                    result = self.inspect("missing:" + name)
                    self.assertEqual(result["status"], "unavailable", result)
                finally:
                    self.clear_declarations()

    def test_each_changed_native_declaration_stops_before_delegate(self):
        for name in ("planned-experiment.sexp", "dependencies.sexp", "authorities.sexp"):
            with self.subTest(name=name):
                try:
                    result = self.inspect("changed:" + name)
                    self.assertEqual(result["status"], "refused", result)
                finally:
                    self.clear_declarations()

    def clear_declarations(self):
        for name in ("planned-experiment.sexp", "dependencies.sexp", "authorities.sexp"):
            path = self.runtime / A.PREFIX / name
            if path.exists():
                path.unlink()

    def test_assertion_failures_cannot_contaminate_later_declaration_subcases(self):
        from unittest.mock import patch

        for method in ("test_each_missing_native_declaration_stops_before_delegate",
                       "test_each_changed_native_declaration_stops_before_delegate"):
            observed = []

            def injected(case, mode):
                paths = [case.runtime / A.PREFIX / name for name in (
                    "planned-experiment.sexp", "dependencies.sexp", "authorities.sexp")]
                observed.append(not any(path.exists() for path in paths))
                for path in paths:
                    path.write_bytes(b"owned injected fixture")
                return dict(status="pending")

            result = unittest.TestResult()
            with patch.object(CommandTests, "inspect", injected):
                CommandTests(method).run(result)
            self.assertEqual(result.errors, [])
            self.assertEqual(len(result.failures), 3)
            self.assertEqual(observed, [True] * 3)

    def test_missing_prepared_input_is_unavailable(self):
        (self.runtime / A.PREPARED[0][2]).unlink()
        self.assertEqual(self.inspect("prepare")["status"], "unavailable")
        result = self.inspect("unavailable-kind")
        self.assertEqual((result["status"], result["kind"]), ("unavailable", "CaptureUnavailable"))
        self.assertIn("permission denied", result["reason"])

    def test_changed_prepared_input_refuses(self):
        (self.runtime / A.PREPARED[0][2]).write_bytes(b"changed")
        self.assertEqual(self.inspect("prepare")["status"], "refused")

    def test_oversized_prepared_input_refuses(self):
        (self.runtime / A.PREPARED[0][2]).write_bytes(b"x" * 65537)
        self.assertEqual(self.inspect("prepare")["status"], "refused")

    def test_linked_prepared_input_refuses_even_with_correct_bytes(self):
        path = self.runtime / A.PREPARED[0][2]
        payload = path.read_bytes()
        path.unlink()
        target = path.with_name("owned-copy")
        target.write_bytes(payload)
        path.symlink_to(target.name)
        self.assertEqual(self.inspect("prepare")["status"], "refused")

    def test_nested_repository_boundary_refuses(self):
        (self.runtime / "evidence/.git").write_text("owned fixture")
        self.assertEqual(self.inspect("prepare")["status"], "refused")

    def test_changed_selected_binary_pin_does_not_match_retained_identity(self):
        path, forms, candidate = self.candidate()
        A.S.children(candidate, "binary_sha256")[0][1] = "0" * 64
        path.write_text(A.R.render_forms(forms))
        self.assertEqual(self.inspect("prepare")["status"], "refused")

    def test_authority_view_drift_between_reviews_refuses(self):
        self.assertEqual(self.inspect("drift")["status"], "refused")

    def test_duplicate_raw_field_refuses_before_mapping(self):
        self.assertEqual(self.inspect("bad-raw")["status"], "refused")

    def test_existing_observation_refuses_without_process_or_replacement(self):
        self.synthetic_reference()
        result = self.inspect("existing-output")
        self.assertEqual(result, dict(status="refused", runs=0, old="old historical bytes"))

    def test_failed_cli_findings_return_nonzero(self):
        self.assertEqual(self.inspect("failed-cli"), dict(exit=1))

    def test_cli_declaration_is_readonly_and_capture_is_unavailable(self):
        command = [sys.executable, *(["-O"] if sys.flags.optimize else []), "-B",
                   str(self.runtime / "scripts/capture_div.py")]
        result = subprocess.run([*command, "--declare"], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        declared = json.loads(result.stdout)
        self.assertEqual((declared["canonical_capture"], declared["qualification"]), (False, False))
        self.assertEqual(len(declared["files"]), 3)
        result = subprocess.run([*command, "--capture"], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["disposition"], "unavailable")


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CommandTests)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"DIV-COMMAND: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; synthetic processes, no Sail or qualification")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
