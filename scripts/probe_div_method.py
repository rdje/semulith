#!/usr/bin/env python3
"""Finite DIV method controls in isolated runtime copies; never execute Sail."""

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

sys.dont_write_bytecode = True

import capture_div as A
import probe_div_command as Command  # the synthetic reference and the manifest reading (a42as)
import review_div_method as M


ROOT = Path(__file__).resolve().parent.parent
DECLARATIONS = ("planned-experiment.sexp", "dependencies.sexp", "authorities.sexp")
# Builds a CURRENT synthetic retained case in a runtime copy: current declarations, three
# synthetic processes, the measured experiment persisted. No Sail, no reference binary.
SYNTHESIZE = r'''
from pathlib import Path
import json, sys
runtime = Path(sys.argv[1]); sys.path.insert(0, str(runtime / "scripts")); sys.dont_write_bytecode = True
import capture_div as A
import review_div_method as M
case, prefix = M.RETAINED_CASE_ID, A.prefix(M.RETAINED_CASE_ID)
declaration = A.prepare_capture(case)
for name, payload in A.declaration_files(declaration):
    with (runtime / prefix / name).open("xb") as stream: stream.write(payload)
result = A.capture(case)
if result.disposition == "pending":
    with (runtime / prefix / "measured-experiment.sexp").open("xb") as stream: stream.write(result.experiment)
print(json.dumps(dict(status=result.disposition, reason=result.reason)))  # a42bb: the reason is kept
'''
MUTATION = None
SEAMS = {
    "declaration-binding": ("review_div_method.py", '''        for name, payload in A.declaration_files(declaration):
            budget.snapshot("input", dict(id=name, path=A.prefix(case_id) + "/" + name,
                                          sha256=hashlib.sha256(payload).hexdigest()), expected=payload)
''', ""),
    "capture-origin": ("review_div_method.py", "sha256=MEASURED_SHA256, byte_size=MEASURED_BYTES",
                       'sha256=A.Artifacts.observe_bounded_file(ROOT, A.prefix(RETAINED_CASE_ID) + "/measured-experiment.sexp", max_bytes=A.SMALL_BYTES).sha256, byte_size=MEASURED_BYTES'),
    "record-binding": ("matched_gpr_adequacy.py", '''        _need(normalized == planned_forms, "measured record changes non-observation predeclaration data")
''', ""),
    "influence-selection": ("matched_gpr_adequacy.py", '''            _need(len(selected) == 1
                  and (selected[0].kind, selected[0].profile_ids, selected[0].fingerprint, selected[0].path)
                  == ("evidence", (frozen.profile_id,), digest, None),
                  "reviewed evidence fingerprint differs from actual predeclaration")
''', ""),
    "finding-completeness": ("matched_gpr_adequacy.py", '''        if missing:
            return MethodFinding("pending", "required method findings have not been computed", missing)
''', ""),
    "evaluation-selection": ("matched_gpr_adequacy.py", '''        _need(type(evaluation.manifest.plan) is M.ManifestPlan
              and evaluation.manifest.plan == review.manifest,
              "evaluated manifest/relations differ from independently reviewed selection")
''', ""),
    "artifact-selection": ("matched_gpr_adequacy.py", '''            _need((item.role, item.path, item.pin.disposition, item.pin.sha256)
                  == (role, path, "matched", digest) and item.data is None
                  and (size is None or item.pin.byte_size == size),
                  "authenticated file differs from bound record or retains payload")
''', ""),
    "typed-findings": ("matched_gpr_adequacy.py", '''            _need(type(value) is expected_types[name], "invalid required finding type: " + name)
''', ""),
    "shared-budget": ("review_div_method.py", "        self.charged -= allowance - pin.byte_size\n",
                      "        self.charged -= allowance\n"),
    "evaluation-accounting": ("review_div_method.py", '''            if (type(authentication) is not A.Unit.Evaluation.AuthenticationSummary
                    or type(authentication.charged_read_bytes) is not int
                    or not 0 <= authentication.charged_read_bytes <= allowance
                    or type(authentication.authenticated_bytes) is not int
                    or not 0 <= authentication.authenticated_bytes <= authentication.charged_read_bytes):
                raise _Stopped("refused", "evaluator read receipt exceeds delegated allowance")
''', ""),
    "checker-census": ("review_div_method.py", '''        A.Review.import_census(sources, roots=frozenset({"review_div_method"}), reviewed=SOURCE_MODULES)
''', ""),
    "checker-recheck": ("review_div_method.py", "                sources.recheck()\n", "                pass\n"),
    "runtime-root": ("review_div_method.py", '''        if ROOT != A.ROOT or ROOT != A.Review.ROOT or ROOT != A.V.ROOT:
            raise _Stopped("refused", "method owners do not share the selected runtime root")
''', ""),
    "native-envelope": ("matched_gpr_adequacy.py", '''    _need(type(payload) is bytes and 0 < len(payload) <= F.DOCUMENT_BYTES,
          "native record must be immutable bytes within 1..65536")
''', ""),
}

# Each omission runs its discriminating test. Both ordinary suites run all 21
# tests; repeating unrelated cold-runtime cases under every broken fixture adds
# no evidence about the omitted predicate.
MUTATION_TESTS = {
    "declaration-binding": "test_missing_and_changed_predeclarations_cannot_borrow_current_parent",
    "capture-origin": "test_self_consistent_unreviewed_capture_is_not_the_curated_origin",
    "record-binding": "test_only_measured_metadata_may_change_the_predeclaration",
    "influence-selection": "test_influence_evidence_selects_the_actual_predeclaration",
    "finding-completeness": "test_partial_and_unsupported_findings_never_become_satisfied",
    "evaluation-selection": "test_evaluation_cannot_supply_another_selected_plan",
    "artifact-selection": "test_authenticated_selection_and_payload_release_bind",
    "typed-findings": "test_plain_public_finding_types_are_required",
    "shared-budget": "test_native_and_evaluator_reads_share_exact_and_short_allowances",
    "evaluation-accounting": "test_bad_evaluator_accounting_keeps_the_full_reservation",
    "checker-census": "test_checker_import_census_and_late_recheck_are_required",
    "checker-recheck": "test_late_checker_change_keeps_independent_computed_findings",
    "runtime-root": "test_runtime_root_cannot_fall_back_to_valid_parent_data",
    "native-envelope": "test_native_envelope_precedes_parsing",
}


CHILD = r'''
from pathlib import Path
from dataclasses import asdict,replace,FrozenInstanceError
from copy import deepcopy
from unittest.mock import patch
from types import SimpleNamespace
from contextlib import redirect_stdout,redirect_stderr
from io import StringIO
import hashlib,json,subprocess,sys
root=Path(sys.argv[1]);mode=sys.argv[2];argument=sys.argv[3] if len(sys.argv)>3 else None
sys.path.insert(0,str(root/'scripts'));sys.dont_write_bytecode=True
processes=[]
def denied(*args,**kwargs):
 processes.append(True);raise RuntimeError('unexpected reference process')
subprocess.Popen=denied
import capture_div as A
import matched_gpr_adequacy as K
import review_div_method as M
PREFIX=A.prefix(M.RETAINED_CASE_ID)
def digest(data):return hashlib.sha256(data).hexdigest()
def fixture(evaluate=True):
 d=A.prepare_capture(M.RETAINED_CASE_ID)
 c=K.freeze_review(planned_experiment=d.planned_experiment,dependencies=d.dependencies,
                  scope=d.authorities.scope,current_candidate=dict(d.authorities.reference.fields),
                  inventory=d.inventory,impact_review=d.impact,case_id=M.RETAINED_CASE_ID)
 data=(root/PREFIX/'measured-experiment.sexp').read_bytes()
 b=K.bind_measured_capture(c,data)
 e=None
 if evaluate:
  raw=next(f for f in A.S.parse(data.decode()) if f[0]=='experiment')
  e=A.Unit.Evaluation.evaluate_retained_unit(root,raw_experiment=raw,scope=d.authorities.scope,
    current_candidate=dict(d.authorities.reference.fields),reviewed_inputs=d.inventory,
    author_review=d.author,impact_review=d.impact,property_authority=d.authorities.property_authority,case_id=M.RETAINED_CASE_ID)
 return d,c,data,b,e
def report(result):
 value=asdict(result);value['checker_source_count']=len(value.pop('checker_sources'))
 value['root']=M.ROOT==root and A.ROOT==root and A.Review.ROOT==root and A.V.ROOT==root
 value['processes']=len(processes);return value
if mode=='normal':
 result=report(M.review_method())
elif mode=='unknown':
 with patch.object(A,'prepare_capture',side_effect=RuntimeError('unexpected preparation')):
  result=report(M.review_method(case_id='not-reviewed'))
elif mode=='invalid-budget':
 bad={'boolean':True,'negative':-1,'large':M.TOTAL_BYTES+1,'zero':0}[argument]
 with patch.object(A.Review,'Snapshots',side_effect=RuntimeError('unexpected source I/O')):
  result=report(M.review_method(max_read_bytes=bad))
elif mode=='budget':
 result=report(M.review_method(max_read_bytes=int(argument)))
elif mode=='bad-accounting':
 d,c,data,b,e=fixture()
 bad={'boolean':True,'negative':-1,'overflow':M.TOTAL_BYTES+1,
      'under':e.authentication.authenticated_bytes-1}[argument]
 corrupt=replace(e,authentication=replace(e.authentication,charged_read_bytes=bad))
 with patch.object(A.Unit.Evaluation,'evaluate_retained_unit',return_value=corrupt):
  result=report(M.review_method())
elif mode=='read-only':
 before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
 r=M.review_method();after={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
 result=report(r);result['unchanged']=before==after
elif mode=='immutable':
 r=M.review_method();blocked=[]
 for value,field in [(r,'disposition'),(r.checker_sources[0],'sha256')]:
  try:setattr(value,field,None)
  except FrozenInstanceError:blocked.append(True)
  else:blocked.append(False)
 result=report(r);result['frozen']=blocked
elif mode=='root-mismatch':
 (root/PREFIX/'baseline.trace').unlink();M.ROOT=Path.cwd().resolve()
 result=report(M.review_method())
elif mode=='late-source':
 original=A.Unit.Evaluation.evaluate_retained_unit
 def late(*args,**kwargs):
  result=original(*args,**kwargs)
  p=root/'scripts/review_div_method.py';p.write_bytes(p.read_bytes()+b'\n# owned late source change\n')
  return result
 with patch.object(A.Unit.Evaluation,'evaluate_retained_unit',side_effect=late):
  result=report(M.review_method())
elif mode=='bad-import':
 # The fixture appended the harmless stdlib import before this fresh child loaded.
 result=report(M.review_method())
elif mode=='forged':
 p=root/PREFIX/'baseline.stdout';p.write_bytes(p.read_bytes()+b'\n')
 receipt=root/PREFIX/'baseline.receipt.sexp';doc=A.F.parse_capture(receipt.read_bytes(),path=PREFIX+'/baseline.receipt.sexp')
 item=next(row for row in doc['observation'] if row['role']=='process-stdout')
 item.update(sha256=digest(p.read_bytes()),byte_size=p.stat().st_size)
 receipt.write_bytes(A.F.encode_capture(doc,path=PREFIX+'/baseline.receipt.sexp'))
 measured=root/PREFIX/'measured-experiment.sexp';forms=A.S.parse(measured.read_text())
 raw=next(f for f in forms if f[0]=='experiment');graph=A.S.children(raw,'verification')[0]
 for row in A.S.children(graph,'observation'):
  identity=A.S.field(row,'id')
  if identity in {'baseline-process-stdout','baseline-process-receipt'}:
   source=p if identity.endswith('stdout') else receipt;payload=source.read_bytes()
   A.S.children(row,'sha256')[0][1]=digest(payload);A.S.children(row,'byte_size')[0][1]=len(payload)
 measured.write_text(A.R.render_forms(forms))
 d,c,data,b,e=fixture();result=report(M.review_method());result.update(lower=e.disposition,binding=b.disposition)
elif mode=='changed-parent':
 d,c,data,b,e=fixture(False);forms=A.S.parse(data.decode());raw=next(f for f in forms if f[0]=='experiment')
 graph=A.S.children(raw,'verification')[0]
 if argument=='prose':A.S.children(raw,'reproduced')[0][1]='changed historical prose'
 elif argument=='comment':next(f for f in forms if f[0]=='comment')[1]='changed original comment'
 elif argument=='control':A.S.children(A.S.children(graph,'control_run')[0],'reason')[0][1]='changed control reason'
 elif argument=='property':A.S.children(A.S.children(graph,'property')[0],'statement')[0][1]='different property claim'
 result=asdict(K.bind_measured_capture(c,A.R.render_forms(forms).encode()))
elif mode=='allowed-metadata':
 d,c,data,b,e=fixture(False);forms=A.S.parse(data.decode());raw=next(f for f in forms if f[0]=='experiment')
 graph=A.S.children(raw,'verification')[0]
 row=A.S.children(graph,'observation')[0];A.S.children(row,'sha256')[0][1]='0'*64;A.S.children(row,'byte_size')[0][1]=0
 A.S.children(A.S.children(graph,'run')[0],'process_exit')[0][1]=7
 result=asdict(K.bind_measured_capture(c,A.R.render_forms(forms).encode()))
elif mode=='envelope':
 d,c,data,b,e=fixture(False)
 bad={'mutable':bytearray(data),'empty':b'','oversized':b' '*65537}[argument]
 result=asdict(K.bind_measured_capture(c,bad))
elif mode=='graph-evidence':
 d,c,data,b,e=fixture(False);key=A.Impact.project_inputs(d.inventory).evidence_key
 def corrupt(graph):
  nodes=tuple(replace(n,**({'fingerprint':'0'*64} if argument=='digest' else {'path':'evidence/unrelated.sexp'})) if n.key==key else n for n in graph.nodes)
  return replace(graph,nodes=nodes)
 impact=replace(d.impact,previous=corrupt(d.impact.previous),current=corrupt(d.impact.current))
 try:
  K.freeze_review(planned_experiment=d.planned_experiment,dependencies=d.dependencies,scope=d.authorities.scope,
    current_candidate=dict(d.authorities.reference.fields),inventory=d.inventory,impact_review=impact,case_id=M.RETAINED_CASE_ID)
 except K.AdequacyError as error:result=dict(disposition='refused',reason=str(error))
 else:result=dict(disposition='accepted')
elif mode=='exact-charge':
 # The accounting invariant, read independently of the budget: every declaration's bytes, the measured
 # record's bytes and the evaluator's own read receipt — nothing refunded, nothing counted twice.
 d,c,data,b,e=fixture()
 declared=sum((root/PREFIX/name).stat().st_size for name in ('planned-experiment.sexp','dependencies.sexp','authorities.sexp'))
 result=dict(expected=declared+len(data)+e.authentication.charged_read_bytes,evaluator=e.authentication.charged_read_bytes)
elif mode=='missing-finding':
 d,c,data,b,e=fixture();result=asdict(K.assess_findings(c,b,replace(e,**{argument:None})))
elif mode=='unsupported-finding':
 d,c,data,b,e=fixture();partial=replace(e,source_values=replace(e.source_values,disposition='unsupported',facts=None),expected_author=None,source_property=None)
 result=asdict(K.assess_findings(c,b,partial))
elif mode=='terminal-finding':
 d,c,data,b,e=fixture();result=asdict(K.assess_findings(c,b,replace(e,disposition=argument,reason='owned terminal fixture')))
elif mode=='foreign-plan':
 d,c,data,b,e=fixture();plan=replace(e.manifest.plan,relations=replace(e.manifest.plan.relations,control_property_id='other-property'))
 result=asdict(K.assess_findings(c,b,replace(e,manifest=replace(e.manifest,plan=plan))))
elif mode=='foreign-file':
 d,c,data,b,e=fixture();items=list(e.authentication.files)
 if argument=='digest':items[0]=replace(items[0],pin=replace(items[0].pin,sha256='0'*64))
 else:items[0]=replace(items[0],data=b'unreleased')
 result=asdict(K.assess_findings(c,b,replace(e,authentication=replace(e.authentication,files=tuple(items)))))
elif mode=='typed-finding':
 d,c,data,b,e=fixture();fake=SimpleNamespace(**asdict(e.input_review))
 result=asdict(K.assess_findings(c,b,replace(e,input_review=fake)))
elif mode=='cli':
 if argument=='missing':(root/PREFIX/'authorities.sexp').unlink()
 sys.argv=['review_div_method.py',*({'valid':[],'unknown':['--case','other'],'zero':['--max-read-bytes','0'],'missing':[]}[argument])]
 output=StringIO()
 with redirect_stdout(output):exitcode=M.main()
 result=dict(exit=exitcode,payload=json.loads(output.getvalue()),bytes=len(output.getvalue().encode()))
else:raise RuntimeError('unknown fixture mode')
result['processes']=len(processes)
print(json.dumps(result))
'''


class MethodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case, cls.prefix = M.RETAINED_CASE_ID, A.prefix(M.RETAINED_CASE_ID)
        cls.paths = ({row["path"] for row in A.Review.review(cls.case)["files"]}
                     | {row[2] for row in A.prepared_inputs(cls.case)}
                     | {p.relative_to(ROOT).as_posix() for p in (ROOT / cls.prefix).iterdir()}
                     | {"scripts/matched_gpr_adequacy.py", "scripts/review_div_method.py"})
        if len(cls.paths) != 103:
            raise RuntimeError("retained method runtime population changed")
        # The deep arms exercise the method's logic against a CURRENT synthetic retained case built
        # once from the live modules and prepared inputs, so every seam stays reachable whether or
        # not the curated capture is still current; only the real-tree arm reads the curated one and
        # predicts its outcome from the manifest (P4-SYSTEM.14 a42as). The copy's method pins the
        # synthetic measured experiment the way the live one pins the curated capture.
        base = ROOT / "target/div-method-controls"
        base.mkdir(parents=True, exist_ok=True)
        cls.template_directory = TemporaryDirectory(dir=base)
        cls.template = Path(cls.template_directory.name) / "runtime"
        outputs = ({p.relative_to(ROOT).as_posix() for p in (ROOT / cls.prefix).iterdir()}
                   - {row[2] for row in A.prepared_inputs(cls.case)})
        for name in sorted(cls.paths - outputs):
            target = cls.template / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)
        Command.synthesize_reference(cls.template, case_id=cls.case)
        done = subprocess.run([sys.executable, "-B", "-c", SYNTHESIZE, str(cls.template)], cwd=ROOT,
                              capture_output=True, text=True, timeout=120)
        if done.returncode != 0 or json.loads(done.stdout.splitlines()[-1]).get("status") != "pending":
            raise RuntimeError("synthetic current capture failed: " + done.stdout + done.stderr)
        measured = (cls.template / cls.prefix / "measured-experiment.sexp").read_bytes()
        path = cls.template / "scripts/review_div_method.py"
        source = path.read_text()
        for before, after in ((f'MEASURED_SHA256 = "{M.MEASURED_SHA256}"',
                               f'MEASURED_SHA256 = "{hashlib.sha256(measured).hexdigest()}"'),
                              (f"MEASURED_BYTES = {M.MEASURED_BYTES}", f"MEASURED_BYTES = {len(measured)}")):
            if source.count(before) != 1:
                raise RuntimeError("curated capture pin must be singular: " + before)
            source = source.replace(before, after, 1)
        path.write_text(source)

    @classmethod
    def tearDownClass(cls):
        cls.template_directory.cleanup()

    def setUp(self):
        base = ROOT / "target/div-method-controls"
        self.temporary = TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.runtime = Path(self.temporary.name) / "runtime"
        shutil.copytree(self.template, self.runtime)
        if MUTATION:
            name, before, after = SEAMS[MUTATION]
            target = self.runtime / "scripts" / name
            source = target.read_text()
            if source.count(before) != 1:
                raise RuntimeError("method omission target must be singular: " + MUTATION)
            target.write_text(source.replace(before, after, 1))

    def inspect(self, mode="normal", argument=None):
        result = subprocess.run(
            [sys.executable, *(["-O"] if sys.flags.optimize else []), "-B", "-c", CHILD,
             str(self.runtime), mode, *([] if argument is None else [str(argument)])],
            cwd=ROOT, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["processes"], 0, payload)
        return payload

    def test_synthetic_current_capture_is_finite_satisfied_and_policy_pending(self):
        r = self.inspect()
        self.assertEqual((r["disposition"], r["policy_disposition"], r["record_disposition"],
                          r["capture_binding"], r["evaluation_disposition"]),
                         ("satisfied", "pending", "valid", "matched", "pending"), r)
        self.assertEqual(r["authenticated_files"], 85, r)
        self.assertGreater(r["authenticated_bytes"], 0, r)
        self.assertGreater(r["snapshot_bytes"], 0, r)
        self.assertEqual((r["checker_disposition"], r["checker_source_count"]), ("matched", 39), r)
        self.assertTrue(r["root"])
        self.assertEqual(r["replay_disposition"], "not-checked")
        self.assertFalse((self.runtime / ".git").exists())
        self.assertFalse((self.runtime / ".materials").exists())
        # The only thing under the copy's target/ is the synthetic reference script the copy pins.
        _, _, candidate = Command.reference_candidate(self.runtime)
        binary = (self.runtime / str(A.S.field(candidate, "binary"))).resolve()
        self.assertEqual([p.resolve() for p in (self.runtime / "target").rglob("*") if p.is_file()], [binary])

    def test_actual_retained_method_is_satisfied_or_stale_as_its_manifest_predicts(self):
        """The curated capture on the real tree: finite satisfied while every pin is current; stale,
        naming the first moved declaration and reading nothing beyond it, once a pinned input moved
        (the policy then measures `invalidated`). The expectation comes from the manifest, not the tree."""
        moved = Command.moved_inputs(ROOT, M.RETAINED_CASE_ID)
        done = subprocess.run([sys.executable, *(["-O"] if sys.flags.optimize else []), "-B",
                               str(ROOT / "scripts/review_div_method.py")],
                              cwd=ROOT, capture_output=True, text=True, timeout=120)
        r = json.loads(done.stdout)
        if moved:
            self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
            self.assertEqual((r["disposition"], r["policy_disposition"], r["record_disposition"],
                              r["capture_binding"], r["evaluation_disposition"]),
                             ("stale", "pending", None, None, None), r)
            self.assertTrue(r["reason"].startswith(self.prefix + "/"), r["reason"])
            self.assertEqual(r["charged_read_bytes"], A.SMALL_BYTES, r)
            self.assertEqual((r["authenticated_files"], r["authenticated_bytes"], r["snapshot_bytes"]),
                             (None, None, None), r)
        else:
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertEqual((r["disposition"], r["policy_disposition"], r["record_disposition"],
                              r["capture_binding"], r["evaluation_disposition"]),
                             ("satisfied", "pending", "valid", "matched", "pending"), r)
            self.assertEqual((r["authenticated_files"], r["authenticated_bytes"], r["snapshot_bytes"]),
                             (85, 1076834, 40438), r)  # the m-forms capture (a42ax)
        self.assertEqual((r["checker_disposition"], len(r["checker_sources"])), ("matched", 39), r)
        self.assertEqual(r["replay_disposition"], "not-checked")

    def test_all_runtime_files_remain_exact_and_results_are_immutable(self):
        self.assertTrue(self.inspect("read-only")["unchanged"])
        self.assertEqual(self.inspect("immutable")["frozen"], [True, True])

    def test_unknown_case_and_invalid_allowances_stop_before_preparation(self):
        self.assertEqual(self.inspect("unknown")["disposition"], "unsupported")
        for value in ("boolean", "negative", "large", "zero"):
            with self.subTest(value=value):
                r = self.inspect("invalid-budget", value)
                self.assertEqual((r["disposition"], r["charged_read_bytes"]), ("refused", 0), r)

    def test_missing_and_changed_predeclarations_cannot_borrow_current_parent(self):
        for name in ("planned-experiment.sexp", "dependencies.sexp", "authorities.sexp"):
            path = self.runtime / self.prefix / name
            original = path.read_bytes()
            for change, expected in (("missing", "unavailable"), ("changed", "stale")):
                with self.subTest(name=name, change=change):
                    if change == "missing":
                        path.unlink()
                    else:
                        path.write_bytes(original + b"\n")
                    self.assertEqual(self.inspect()["disposition"], expected)
                    path.write_bytes(original)

    def test_missing_or_changed_observations_preserve_their_dispositions(self):
        path = self.runtime / self.prefix / "baseline.trace"
        original = path.read_bytes()
        path.unlink()
        self.assertEqual(self.inspect()["disposition"], "unavailable")
        path.write_bytes(original + b"\n")
        self.assertEqual(self.inspect()["disposition"], "stale")

    def test_self_consistent_unreviewed_capture_is_not_the_curated_origin(self):
        r = self.inspect("forged")
        self.assertEqual((r["lower"], r["binding"]), ("pending", "matched"), r)
        self.assertEqual(r["disposition"], "stale", r)

    def test_only_measured_metadata_may_change_the_predeclaration(self):
        for field in ("prose", "comment", "control", "property"):
            with self.subTest(field=field):
                self.assertEqual(self.inspect("changed-parent", field)["disposition"], "refused")
        self.assertEqual(self.inspect("allowed-metadata")["disposition"], "matched")

    def test_native_envelope_precedes_parsing(self):
        for value in ("mutable", "empty", "oversized"):
            with self.subTest(value=value):
                self.assertEqual(self.inspect("envelope", value)["disposition"], "refused")

    def test_influence_evidence_selects_the_actual_predeclaration(self):
        for value in ("digest", "path"):
            with self.subTest(value=value):
                r = self.inspect("graph-evidence", value)
                self.assertEqual(r["disposition"], "refused", r)
                self.assertIn("actual predeclaration", r["reason"])

    def test_partial_and_unsupported_findings_never_become_satisfied(self):
        for value in ("input_review", "impact"):
            with self.subTest(value=value):
                r = self.inspect("missing-finding", value)
                self.assertEqual((r["disposition"], r["missing"]), ("pending", [value]), r)
        self.assertEqual(self.inspect("unsupported-finding")["disposition"], "unsupported")

    def test_terminal_findings_keep_their_separate_kind(self):
        for value in ("failed", "stale", "unavailable", "refused", "unsupported"):
            with self.subTest(value=value):
                self.assertEqual(self.inspect("terminal-finding", value)["disposition"], value)

    def test_evaluation_cannot_supply_another_selected_plan(self):
        self.assertEqual(self.inspect("foreign-plan")["disposition"], "refused")

    def test_authenticated_selection_and_payload_release_bind(self):
        for value in ("digest", "payload"):
            with self.subTest(value=value):
                self.assertEqual(self.inspect("foreign-file", value)["disposition"], "refused")

    def test_plain_public_finding_types_are_required(self):
        self.assertEqual(self.inspect("typed-finding")["disposition"], "refused")

    def test_native_and_evaluator_reads_share_exact_and_short_allowances(self):
        exact = self.inspect("exact-charge")["expected"]  # independent of the method's own accounting
        self.assertGreater(exact, A.SMALL_BYTES)
        for limit in (134217728, exact):
            with self.subTest(limit=limit):
                r = self.inspect("budget", limit)
                self.assertEqual((r["disposition"], r["charged_read_bytes"]), ("satisfied", exact), r)
        r = self.inspect("budget", exact - 1)
        self.assertNotEqual(r["disposition"], "satisfied", r)
        self.assertLessEqual(r["charged_read_bytes"], exact - 1)

    def test_bad_evaluator_accounting_keeps_the_full_reservation(self):
        for value in ("boolean", "negative", "overflow", "under"):
            with self.subTest(value=value):
                r = self.inspect("bad-accounting", value)
                self.assertEqual((r["disposition"], r["charged_read_bytes"]), ("refused", 134217728), r)

    def test_checker_import_census_and_late_recheck_are_required(self):
        path = self.runtime / "scripts/review_div_method.py"
        path.write_bytes(path.read_bytes() + b"\nimport socket\n")
        r = self.inspect("bad-import")
        self.assertEqual((r["disposition"], r["checker_disposition"], r["checker_source_count"]),
                         ("refused", "refused", 0), r)

    def test_late_checker_change_keeps_independent_computed_findings(self):
        r = self.inspect("late-source")
        self.assertEqual((r["disposition"], r["checker_disposition"]), ("refused", "refused"), r)
        self.assertEqual((r["record_disposition"], r["capture_binding"], r["evaluation_disposition"]),
                         ("valid", "matched", "pending"), r)

    def test_runtime_root_cannot_fall_back_to_valid_parent_data(self):
        self.assertEqual(self.inspect("root-mismatch")["disposition"], "refused")

    def test_cli_exit_statuses_and_bounded_derived_json(self):
        for value, expected in (("valid", 0), ("unknown", 2), ("zero", 1), ("missing", 2)):
            with self.subTest(value=value):
                r = self.inspect("cli", value)
                self.assertEqual(r["exit"], expected, r)
                self.assertLessEqual(r["bytes"], 65536)
                self.assertEqual(r["payload"]["policy_disposition"], "pending")


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    if set(MUTATION_TESTS) != set(SEAMS):
        raise RuntimeError("every omitted guard needs its own discriminating test")
    suite = (unittest.TestSuite([MethodTests(MUTATION_TESTS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(MethodTests))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"DIV-METHOD: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; retained finite method, no Sail or policy credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
