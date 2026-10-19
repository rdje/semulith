#!/usr/bin/env python3
"""Copied current-authority controls; no reference execution or qualification."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import capture_div as A

ROOT = Path(__file__).resolve().parent.parent
MUTATION = None
SEAMS = {
    "raw-validation": ('    issues = K.validate_text(text, *schema, path)\n'
                       '    require(not issues, "authority shape: " + (issues[0] if issues else ""))\n'),
    "registry-binding": ('    require(registries == [REGISTRY], "authority registry differs from reviewed source")\n'),
    "authority-binding": ('    require(authority == case.authority, "current DIV semantic authority differs from reviewed case")\n'),
}
CHILD = '''from pathlib import Path
from dataclasses import FrozenInstanceError
from unittest.mock import patch
import json,subprocess,sys
runtime=Path(sys.argv[1]);mode=sys.argv[2];sys.path.insert(0,str(runtime/'scripts'))
processes=[]
def deny(command,*args,**kwargs):
 processes.append(command)
 raise RuntimeError('unexpected authority process')
subprocess.Popen=deny
import capture_div as A
events=[];reads=[];writes=[];original_open=Path.open
def opened(path,*args,**kwargs):
 selected=Path(path).resolve().relative_to(runtime).as_posix()
 access=args[0] if args else kwargs.get('mode','r')
 (writes if any(flag in access for flag in 'wax+') else reads).append(selected)
 return original_open(path,*args,**kwargs)
validate=A.K.validate_text;map_record=A.R.form_to_dict
map_sources=A.D.sources_to_doc;map_references=A.D.references_to_doc
def validated(*args,**kwargs):
 events.append('validate');return validate(*args,**kwargs)
def mapped(owner):
 def call(*args,**kwargs):
  events.append('map');return owner(*args,**kwargs)
 return call
recheck=A.Review.Snapshots.recheck
def drift(snapshot):
 path=runtime/A.DIRECTORY/'references.sexp'
 path.write_bytes(path.read_bytes()+b'\\n(comment "owned late change")\\n')
 return recheck(snapshot)
try:
 with patch.object(Path,'open',opened),patch.object(A.K,'validate_text',validated),patch.object(A.R,'form_to_dict',mapped(map_record)),patch.object(A.D,'sources_to_doc',mapped(map_sources)),patch.object(A.D,'references_to_doc',mapped(map_references)),patch.object(A.Review.Snapshots,'recheck',drift if mode=='drift' else recheck):
  context=A.review_authorities()
 report=A.report(context);frozen=[]
 for value,field in [(context,'views'),(context.scope,'profile_id'),(context.reference,'fields'),(context.property_authority,'profile_id'),(context.views[0],'sha256')]:
  try:setattr(value,field,None)
  except FrozenInstanceError:frozen.append(True)
  else:frozen.append(False)
 result=dict(status='pending',report=report,frozen=frozen)
except OSError as error:
 result=dict(status='unavailable',reason=type(error).__name__)
except (A.AuthorityError,A.Review.ReviewError,A.K.SchemaError,A.S.SexpError,A.C.CatalogRefused,A.R.RecordRefused,A.D.DossierError,A.I.IdentityError,A.P.PropertyError,UnicodeError) as error:
 result=dict(status='refused',reason=str(error))
except Exception as error:
 result=dict(status='unexpected-error',reason=type(error).__name__+': '+str(error))
result.update(reads=reads,writes=writes,events=events,processes=processes)
print(json.dumps(result))
'''


def field(form, name):
    selected = [child for child in form[1:] if isinstance(child, list) and child[0] == name]
    if len(selected) != 1:
        raise RuntimeError("fixture field is not singular: " + name)
    return selected[0]


class AuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = {f"scripts/{name}.py" for name in A.Review.REVIEWED_MODULES
                     | {"review_div_capture", "capture_div"}} | set(A.VIEW_PATHS)
        cls.authority = asdict(A.P.signed_division_case().authority)

    def setUp(self):
        base = ROOT / "target/div-authority-controls"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.runtime = Path(self.temporary.name) / "runtime"
        for path in sorted(self.paths):
            target = self.runtime / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / path, target)
        if MUTATION:
            path = self.runtime / "scripts/capture_div.py"
            source = path.read_text()
            seam = SEAMS[MUTATION]
            if source.count(seam) != 1:
                raise RuntimeError("authority omission target must be singular")
            path.write_text(source.replace(seam, "", 1))

    def inspect(self, mode="audit"):
        result = subprocess.run([sys.executable, *(["-O"] if sys.flags.optimize else []),
                                 "-c", CHILD, str(self.runtime), mode], cwd=ROOT,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def load(self, name):
        path = self.runtime / A.DIRECTORY / (name + ".sexp")
        return path, A.S.parse(path.read_text())

    def save(self, path, forms):
        path.write_text(A.R.render_forms(forms))

    def document(self, forms):
        return next(form for form in forms if form[0] != "comment")

    def record(self, forms, head, identity):
        population = forms if head in {"requirement", "obligation", "contract"} else self.document(forms)[1:]
        return next(form for form in population if isinstance(form, list) and form[0] == head
                    and field(form, "id")[1] == identity)

    def refuses(self, expected="refused", needle=None, mode="audit"):
        result = self.inspect(mode)
        self.assertEqual(result["status"], expected, result)
        if needle:
            self.assertIn(needle, result["reason"])
        return result

    def test_current_context_has_exact_views_bounds_and_selected_authorities(self):
        before = {path: (self.runtime / path).read_bytes() for path in self.paths}
        result = self.inspect()
        report = result["report"]
        self.assertEqual(result["status"], "pending", result)
        self.assertEqual(len(A.VIEW_PATHS), 13)
        self.assertEqual(len(self.paths), 50)
        self.assertEqual({view["path"] for view in report["views"]}, set(A.VIEW_PATHS))
        self.assertEqual(set(result["reads"]), set(A.VIEW_PATHS))
        self.assertEqual(result["writes"], [])
        self.assertEqual(result["processes"], [])
        self.assertEqual(report["property_authority"], self.authority)
        self.assertIn("REQ-GC-M", report["scope"]["requirement_ids"])
        self.assertIn("OB-GC-M", report["scope"]["obligation_ids"])
        self.assertEqual(report["direct_snapshots"],
                         dict(file_bytes=1048576, per_pass_bytes=8388608, passes=2))
        self.assertFalse(report["canonical_capture"])
        self.assertFalse(report["qualification"])
        self.assertEqual({path: (self.runtime / path).read_bytes() for path in self.paths}, before)
        self.assertFalse((self.runtime / ".materials").exists())
        self.assertFalse((self.runtime / "target/refs").exists())

    def test_returned_context_and_each_fact_are_frozen(self):
        result = self.inspect()
        self.assertEqual(result["status"], "pending", result)
        self.assertEqual(result["frozen"], [True] * 5)

    def test_every_raw_view_validates_before_canonical_mapping(self):
        result = self.inspect()
        events = result["events"]
        self.assertEqual(result["status"], "pending", result)
        self.assertEqual(events.count("validate"), 8)
        self.assertEqual(events[:events.index("map")], ["validate"] * 8)

    def test_only_readonly_command_is_exposed(self):
        command = [sys.executable, *(["-O"] if sys.flags.optimize else []), "scripts/capture_div.py"]
        result = subprocess.run([*command, "--review-authorities"], cwd=self.runtime,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["disposition"], "pending")
        result = subprocess.run([*command, "--capture"], cwd=self.runtime,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 2)

    def test_missing_required_view_is_unavailable(self):
        (self.runtime / "schema/requirements.sexp").unlink()
        self.refuses("unavailable", "FileNotFoundError")

    def test_unsafe_or_oversized_view_refuses(self):
        path = self.runtime / A.DIRECTORY / "sources.sexp"
        original = path.read_bytes()
        for kind in ("link", "oversized"):
            with self.subTest(kind=kind):
                path.unlink()
                if kind == "link":
                    path.symlink_to(ROOT / A.DIRECTORY / "sources.sexp")
                else:
                    path.write_bytes(b"x" * (A.Review.FILE_BYTES + 1))
                try:
                    self.refuses()
                finally:
                    path.unlink()
                    path.write_bytes(original)

    def test_direct_aggregate_is_shared_before_schema_or_mapping(self):
        payload = b";" + b"x" * (A.Review.FILE_BYTES - 2) + b"\n"
        for path in A.VIEW_PATHS[:9]:
            (self.runtime / path).write_bytes(payload)
        result = self.refuses(needle="aggregate bound")
        self.assertEqual(result["events"], [])
        self.assertEqual(len(result["reads"]), 8)

    def test_duplicate_record_ids_refuse_before_selection(self):
        for name, head, identity in (("requirements", "requirement", "REQ-GC-M"),
                                     ("contract-obligations", "obligation", "OB-GC-M"),
                                     ("sources", "source", "RVI-M"),
                                     ("references", "candidate", "sail-riscv"),
                                     ("contract", "contract", "rv64gc-lab-env-v2")):
            with self.subTest(family=head):
                path, forms = self.load(name)
                original = path.read_bytes()
                record = deepcopy(self.record(forms, head, identity))
                (forms if head in {"requirement", "obligation", "contract"} else self.document(forms)).append(record)
                self.save(path, forms)
                try:
                    self.refuses(needle="duplicate")
                finally:
                    path.write_bytes(original)

    def test_duplicate_raw_singular_field_refuses_before_mapping(self):
        path, forms = self.load("references")
        document = self.document(forms)
        document.append(deepcopy(field(document, "profile")))
        self.save(path, forms)
        result = self.refuses()
        self.assertNotIn("map", result["events"])

    def test_schema_facets_are_not_replaced_by_selected_digest_checks(self):
        path, forms = self.load("sources")
        source = self.record(forms, "source", "RVI-M")
        field(source, "bytes")[1] = str(field(source, "bytes")[1])
        self.save(path, forms)
        self.refuses(needle="authority shape")

    def test_foreign_parent_profile_refuses(self):
        path, forms = self.load("references")
        field(self.document(forms), "profile")[1] = "foreign"
        self.save(path, forms)
        self.refuses(needle="profile differs")

    def test_missing_selected_records_refuse(self):
        for name, head, identity in (("requirements", "requirement", "REQ-GC-M"),
                                     ("contract-obligations", "obligation", "OB-GC-M"),
                                     ("sources", "source", "RVI-M"),
                                     ("references", "candidate", "sail-riscv")):
            with self.subTest(family=head):
                path, forms = self.load(name)
                original = path.read_bytes()
                selected = self.record(forms, head, identity)
                (forms if head in {"requirement", "obligation"} else self.document(forms)).remove(selected)
                self.save(path, forms)
                try:
                    self.refuses(needle="missing")
                finally:
                    path.write_bytes(original)

    def test_changed_selected_semantics_refuse(self):
        for name, head, identity, attribute, value in (
            ("requirements", "requirement", "REQ-GC-M", "risk", A.S.Symbol("high")),
            ("contract-obligations", "obligation", "OB-GC-M", "statement", "changed authority"),
            ("sources", "source", "RVI-M", "sha256", "b" * 64),
        ):
            with self.subTest(family=head):
                path, forms = self.load(name)
                original = path.read_bytes()
                field(self.record(forms, head, identity), attribute)[1] = value
                self.save(path, forms)
                try:
                    self.refuses(needle="semantic authority differs")
                finally:
                    path.write_bytes(original)

    def test_derived_status_changes_provenance_but_not_semantic_authority(self):
        path, forms = self.load("requirements")
        old_pin = hashlib.sha256(path.read_bytes()).hexdigest()
        field(self.record(forms, "requirement", "REQ-GC-M"), "implementation_status")[1] = A.S.Symbol("partial")
        self.save(path, forms)
        result = self.inspect()
        self.assertEqual(result["status"], "pending", result)
        self.assertEqual(result["report"]["property_authority"], self.authority)
        view = next(view for view in result["report"]["views"] if view["path"].endswith("/requirements.sexp"))
        self.assertNotEqual(view["sha256"], old_pin)

    def test_selected_identity_excludes_parent_prose_and_tracks_binary_pin(self):
        baseline = self.inspect()["report"]["reference_identity"]
        path, forms = self.load("references")
        candidate = self.record(forms, "candidate", "sail-riscv")
        field(candidate, "lineage")[1] += " changed description"
        self.save(path, forms)
        self.assertEqual(self.inspect()["report"]["reference_identity"], baseline)
        field(candidate, "binary_sha256")[1] = "b" * 64
        self.save(path, forms)
        result = self.inspect()
        self.assertEqual(result["status"], "pending", result)
        self.assertEqual(result["report"]["reference_identity"], dict(baseline, binary_sha256="b" * 64))
        self.assertEqual(set(result["reads"]), set(A.VIEW_PATHS))

    def test_effective_scope_and_cycle_refusals_reuse_public_owner(self):
        path, forms = self.load("contract")
        original = path.read_bytes()
        first = self.record(forms, "contract", "rv64gc-lab-env-v0")
        first.append([A.S.Symbol("extends"), "rv64gc-lab-env-v1"])
        self.save(path, forms)
        self.refuses(needle="CONTRACT CYCLE")
        path.write_bytes(original)
        path, forms = self.load("contract")
        forms += A.S.parse('''(contract (id "rv64gc-lab-env-v3") (version "3")
          (profile_ids "rv64gc-lab-v0") (extends "rv64gc-lab-env-v2") (status open)
          (statement "owned supersession fixture") (member (id "OB-AI-REPLACEMENT"))
          (supersede (record "OB-GC-M") (by "OB-AI-REPLACEMENT") (why "owned fixture")))''')
        self.save(path, forms)
        obligations, records = self.load("contract-obligations")
        replacement = deepcopy(self.record(records, "obligation", "OB-GC-M"))
        for name, value in (("id", "OB-AI-REPLACEMENT"), ("contract_id", "rv64gc-lab-env-v3"), ("contract_version", "3")):
            field(replacement, name)[1] = value
        records.append(replacement)
        self.save(obligations, records)
        self.refuses(needle="not effective")

    def test_unknown_include_and_registry_refuse_before_their_read(self):
        path, forms = self.load("contract-obligations")
        original = path.read_bytes()
        unknown = A.DIRECTORY + "/unreviewed.obligations.sexp"
        (self.runtime / unknown).write_bytes((self.runtime / A.PARTS[0]).read_bytes())
        include = next(form for form in forms if form[0] == "include-obligations")
        field(include, "path")[1] = unknown
        self.save(path, forms)
        result = self.refuses(needle="unreviewed authority include")
        self.assertNotIn(unknown, result["reads"])
        path.write_bytes(original)
        path, forms = self.load("contract")
        unknown = "crates/semulith-verify/src/alternate.rs"
        (self.runtime / unknown).write_bytes((self.runtime / A.REGISTRY).read_bytes())
        field(next(form for form in forms if form[0] == "registry"), "path")[1] = unknown
        self.save(path, forms)
        result = self.refuses(needle="registry differs")
        self.assertNotIn(unknown, result["reads"])

    def test_changed_view_during_review_refuses(self):
        self.refuses(needle="reviewed bytes changed", mode="drift")


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=tuple(SEAMS))
    args = parser.parse_args()
    MUTATION = args.mutation
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(AuthorityTests))
    print(f"DIV-AUTHORITIES: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; current views, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
