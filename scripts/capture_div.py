#!/usr/bin/env python3
"""Declare or collect the finite DIV case; full policy qualification is pending.

Direct current-view snapshots use the existing bounded review reader. Canonical
schema/catalogue/scope tools retain their own I/O. This command assumes a trusted,
quiescent runtime tree; before/after checks do not make the views one atomic set.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import sys

import check_sexp_schema as K
import change_impact as Change
import dossier_sexp as D
import experiment_artifacts as Artifacts
import experiment_verification as V
import matched_gpr_artifacts as F
import matched_gpr_execution as Execution
import matched_gpr_expected_author as Author
import matched_gpr_identity as I
import matched_gpr_impact as Impact
import matched_gpr_input_review as Inputs
import matched_gpr_property as P
import matched_gpr_relations as Relations
import matched_gpr_unit_collector as Unit
import record_catalog as C
import records_sexp as R
import review_div_capture as Review
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
PROFILE = "rv64gc-lab-v0"
DIRECTORY = "profiles/" + PROFILE
PARTS = tuple(DIRECTORY + "/contract-v" + str(version) + ".obligations.sexp"
              for version in (0, 1))
CATALOGUES = tuple(DIRECTORY + "/" + name + ".sexp" for name in (
    "requirements", "contract-obligations", "contract", "sources", "references"))
SCHEMAS = tuple("schema/" + name + ".sexp" for name in (
    "requirements", "contract-obligations", "contract", "sources", "references"))
REGISTRY = "crates/semulith-verify/src/contract_checks_rv64gc.rs"
VIEW_PATHS = tuple(sorted((*CATALOGUES, *PARTS, *SCHEMAS, REGISTRY)))
RECORDS = 4096
PREFIX = "evidence/" + P.CASE_ID
IDENTITY_PATH = DIRECTORY + "/retained/sail-identity.sexp"
SMALL_BYTES = 65536
# Curated inputs have identities distinct from their producer sources.
PREPARED = (
    ("guest-image", "guest-image", PREFIX + "/guest.elf", 4416,
     "38a327660cb1c699e15694fe98d0467e909726555688074d558768300138e153"),
    ("reference-config", "reference-config", PREFIX + "/reference-config.json", 7609,
     "666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2"),
    ("expectation", "expectation", PREFIX + "/baseline.expected.sexp", 5847,
     "87a5b54c50e147017a2dc60d69869d36679067026d7f449d75db6a344199907e"),
    ("expectation", "mutant-expectation", PREFIX + "/control.expected.sexp", 5443,
     "3f8d591db326a6a83a47921b7743297edc758eb602fa70660b770d37a07c758e"),
    ("reference-identity", "reference-identity", IDENTITY_PATH, 711,
     "b0d88c7ae4b3cbb6b856af338811947dd58c6d8e754043d901f2952aeaecea77"),
)


class AuthorityError(ValueError):
    """Current validated views cannot supply this reviewed finite case."""


class CaptureUnavailable(OSError):
    """The artifact owner could not read an input; no specific errno is inferred."""


@dataclass(frozen=True)
class ViewIdentity:
    path: str
    role: str
    byte_size: int
    sha256: str


@dataclass(frozen=True)
class CurrentAuthorities:
    scope: V.Scope
    reference: I.ReferenceIdentity
    property_authority: P.PropertyAuthority
    views: tuple[ViewIdentity, ...]


def require(condition, reason):
    if not condition:
        raise AuthorityError(reason)


def _raw(payload, schema, path, heads):
    text = payload.decode("utf-8")
    issues = K.validate_text(text, *schema, path)
    require(not issues, "authority shape: " + (issues[0] if issues else ""))
    forms = [form for form in S.parse(text, path) if form[0] != "comment"]
    require(1 <= len(forms) <= RECORDS, "authority form count exceeds envelope")
    require(all(form[0] in heads for form in forms), "unexpected authority root form")
    return forms


def _unique(records, family):
    require(type(records) is list and 1 <= len(records) <= RECORDS,
            "invalid " + family + " record population")
    result = {}
    for record in records:
        identity = record["id"]
        require(identity not in result, "duplicate " + family + " ID: " + identity)
        result[identity] = record
    return result


def _one(forms, head):
    require(len(forms) == 1 and forms[0][0] == head,
            "expected exactly one " + head + " authority document")
    return forms[0]


def review_authorities() -> CurrentAuthorities:
    """Freeze current selected scope, execution identity and DIV semantic authority.

    No binary, retained capture or acquired material is read. The function starts
    no process and publishes no capture or authority file. Public tool reads are
    separate from direct snapshots: at most 1 MiB/file, 8 MiB/pass and two passes.
    Provenance hashes describe the views; they are not execution input pins or
    proof of complete policy, producer review, loaded-code identity or currentness.
    """
    snapshots = Review.Snapshots(ROOT)
    payloads = {path: snapshots.pin(path) for path in VIEW_PATHS}
    schemas = {Path(path).stem: K.load_schema(ROOT / path) for path in SCHEMAS}
    raw = {}
    for name, heads in (
        ("requirements", {"requirement"}),
        ("contract-obligations", {"obligation", "include-obligations"}),
        ("contract", {"contract", "registry"}),
        ("sources", {"sources"}),
        ("references", {"references"}),
    ):
        path = DIRECTORY + "/" + name + ".sexp"
        raw[name] = _raw(payloads[path], schemas[name], path, heads)
    obligation_sources = (DIRECTORY + "/contract-obligations.sexp", *PARTS)
    for path in PARTS:
        raw[path] = _raw(payloads[path], schemas["contract-obligations"], path,
                         {"obligation", "include-obligations"})
    # Refuse an unknown include BEFORE the public expansion owner could read it.
    for path in obligation_sources:
        forms = raw["contract-obligations"] if path == obligation_sources[0] else raw[path]
        for form in forms:
            if form[0] == "include-obligations":
                require(S.field(form, "path", path) in PARTS,
                        "unreviewed authority include")
    originals = {}
    expanded = C.text(ROOT / obligation_sources[0], root=ROOT, source_texts=originals)
    require({path.relative_to(ROOT).as_posix() for path in originals}
            == set(obligation_sources), "authority include population differs")
    require(all(text.encode("utf-8") == payloads[path.relative_to(ROOT).as_posix()]
                for path, text in originals.items()), "authority include bytes changed")
    obligations = _raw(expanded.encode("utf-8"), schemas["contract-obligations"],
                       "expanded obligations", {"obligation"})
    requirements = _unique([R.form_to_dict(form) for form in raw["requirements"]],
                           "requirement")
    obligation_index = _unique([R.form_to_dict(form) for form in obligations], "obligation")
    # The public effective-contract owner indexes by version ID. Reject repeats
    # before delegating; raw schema alone checks fields within individual forms.
    contract_ids = [S.field(form, "id", "contract") for form in raw["contract"]
                    if form[0] == "contract"]
    require(contract_ids and len(contract_ids) == len(set(contract_ids)),
            "duplicate or missing contract ID")
    registries = [S.field(form, "path", "registry") for form in raw["contract"]
                  if form[0] == "registry"]
    require(registries == [REGISTRY], "authority registry differs from reviewed source")
    sources = D.sources_to_doc(_one(raw["sources"], "sources"))
    references = D.references_to_doc(_one(raw["references"], "references"))
    require(references["profile"] == PROFILE, "reference authority profile differs")
    source_index = _unique(sources["source"], "source")
    candidates = _unique(references["candidate"], "candidate")
    case = P.signed_division_case()
    require(case.requirement_id in requirements and case.source_id in source_index
            and len(case.obligation_ids) == 1 and case.obligation_ids[0] in obligation_index
            and "sail-riscv" in candidates, "selected DIV authority is missing")
    try:
        scope = V.load_scope(ROOT / DIRECTORY, PROFILE, set(candidates))
    except SystemExit as error:
        raise AuthorityError("effective authority: " + str(error)) from None
    require(case.requirement_id in scope.requirement_ids
            and set(case.obligation_ids) <= scope.obligation_ids,
            "selected DIV authority is foreign or not effective")
    authority = P.project_authority(
        PROFILE, requirement=requirements[case.requirement_id],
        obligation=obligation_index[case.obligation_ids[0]],
        source=source_index[case.source_id])
    require(authority == case.authority, "current DIV semantic authority differs from reviewed case")
    reference = I.bind_reference_identity(candidates["sail-riscv"])
    snapshots.recheck()
    views = tuple(ViewIdentity(
        path, "schema-tool" if path in SCHEMAS else
        "registry-tool" if path == REGISTRY else "current-catalogue",
        len(payloads[path]), hashlib.sha256(payloads[path]).hexdigest())
        for path in VIEW_PATHS)
    return CurrentAuthorities(scope, reference, authority, views)


def report(context):
    return dict(
        disposition="pending", case_id=P.CASE_ID, profile_id=PROFILE,
        reference_identity=dict(context.reference.fields),
        property_authority=asdict(context.property_authority),
        scope=dict(candidate_ids=sorted(context.scope.candidate_ids),
                   requirement_ids=sorted(context.scope.requirement_ids),
                   obligation_ids=sorted(context.scope.obligation_ids)),
        views=[asdict(view) for view in context.views],
        direct_snapshots=dict(file_bytes=Review.FILE_BYTES,
                              per_pass_bytes=Review.TOTAL_BYTES, passes=2),
        canonical_capture=False, qualification=False,
        limitations=["public tool I/O is separate from direct snapshots",
                     "trusted quiescent runtime; no atomic-view or RAM guarantee",
                     "view hashes are provenance, not execution input pins",
                     "catalogue/contract integrity remains a repository gate obligation",
                     "exact native declaration, canonical runs and full policy pending"])


@dataclass(frozen=True)
class CaptureDeclaration:
    authorities: CurrentAuthorities
    planned_experiment: bytes
    dependencies: bytes
    authority_record: bytes
    inventory: Inputs.InputReview
    author: Author.ExpectedAuthorReview
    impact: Impact.ImpactReview


def _digest(payload):
    return hashlib.sha256(payload).hexdigest()


def _record(binding):
    return dict(id=binding.input_id, role=binding.role,
                path=binding.path, sha256=binding.sha256)


def _read_pinned(binding, size=None):
    snapshot = Artifacts.read_snapshot(ROOT, "input", _record(binding), max_bytes=SMALL_BYTES)
    if snapshot.pin.disposition == "unavailable":
        raise CaptureUnavailable("capture input unavailable: " + binding.path + ": " + snapshot.pin.reason)
    require(snapshot.pin.disposition == "matched", "capture input pin refuses: " + binding.path)
    require(size is None or len(snapshot.data) == size, "capture input size differs")
    return snapshot.data


def _planned_record(context, inputs, author):
    """Build claims to be tested, with explicit unmeasured output placeholders."""
    case = P.signed_division_case()
    common = list(Execution.COMMON_ROLES)
    selected = dict(context.reference.fields)
    producers = [dict(id="reference", role="reference", candidate_id="sail-riscv",
                      version="sha256:" + selected["binary_sha256"], input_ids=common)]
    for identity, expectation in (("expected", "expectation"),
                                  ("expected-mutant", "mutant-expectation")):
        producers.append(dict(id=identity, role="expected", version="sha256:" + author.sha256,
                              input_ids=["guest-source", expectation, "dependency-manifest"]))
    by_role = {item.role: item for item in inputs if item.role != "expectation"}
    observations, runs = [], []
    suffixes = ("trace", "stdout", "stderr", "receipt.sexp")
    for kind in Execution.RUN_KINDS:
        outputs = [dict(id=kind + "-" + role, role=role,
                        path=PREFIX + "/" + kind + "." + suffix,
                        sha256="0" * 64, byte_size=0)
                   for role, suffix in zip(Execution.OUTPUT_ROLES, suffixes)]
        observations.extend(outputs)
        control = kind == "control"
        run = dict(id=kind, kind=kind,
                   input_ids=common + ["mutant-expectation" if control else "expectation"],
                   producer_ids=["reference", "expected-mutant" if control else "expected"],
                   observation_ids=[item["id"] for item in outputs], process_exit=0,
                   verdict="DIVERGE" if control else "AGREE",
                   argv=[selected["binary"], "--config-override", by_role["reference-config"].path,
                         "--inst-limit", str(case.instructions), "--trace-instr", "--trace-gpr",
                         "--trace-exception", "--trace-output", outputs[0]["path"],
                         by_role["guest-image"].path])
        if kind == "repeat":
            run["repeat_of"] = "baseline"
        runs.append(run)
    pairs = [dict(id=identity + "-pair", left="reference", right=identity,
                  subsystem="gpr-change", assessment="not-examined",
                  shared_input_ids=["guest-source", "dependency-manifest"],
                  evidence="Selected public reference; snapshot-parcels-v1 source author. Ancestry unexamined.",
                  consequence="No producer-independence or qualification credit.")
             for identity in ("expected", "expected-mutant")]
    graph = dict(format_version="matched-gpr-v1", comparison_rule="sail-gpr-change-v1",
                 limitations=["The planned record uses zero output placeholders; collection replaces sizes, hashes and exits with measurements.",
                              "One finite DIV witness; full source/risk/feature policy remains pending."],
                 input=[_record(item) for item in inputs], producer=producers,
                 observation=observations, run=runs, producer_pair=pairs,
                 property=[dict(id="signed-quotient", statement=case.statement,
                                requirement_id=case.requirement_id,
                                obligation_ids=list(case.obligation_ids), observation_kinds=["gpr-change"],
                                gpr_witness=asdict(case.witness))],
                 control_run=[dict(id="wrong-quotient", run_id="control", baseline_id="baseline",
                                   property_ids=["signed-quotient"], mutation_input_ids=["mutant-expectation"],
                                   expected_verdict="DIVERGE", observed_verdict="DIVERGE",
                                   reason="Only boundary2 x7 expectation changes from -3 to -4.")])
    experiment = dict(id=case.case_id, program=case.program, instructions=case.instructions,
                      models=["sail-riscv"], verdict="AGREE", verification=graph,
                      reproduced="Predeclared target: fresh baseline and exact-byte repeat.",
                      control="Predeclared target: wrong quotient must diverge.")
    # Use the sole dossier mapper; raw validation follows before any mapped use.
    candidate = dict(selected, role="selected execution identity", status="declared",
                     lineage="unexamined; no independence credit")
    document = dict(profile=PROFILE, retrieved="planned", work_dir="target/refs",
                    host=dict(os="unmeasured", kernel="unmeasured", arch="unmeasured", cxx="unmeasured"),
                    candidate=[candidate], experiment=[experiment])
    raw = next(form for form in D.references_to_form(document)
               if isinstance(form, list) and form and form[0] == "experiment")
    payload = R.render_forms([[S.Symbol("comment"),
                               "Predeclared claims, not observations or qualification."], raw]).encode()
    require(0 < len(payload) <= SMALL_BYTES, "planned record exceeds65536 bytes")
    issues = V.check_experiment(raw, context.scope)
    require(not issues, "planned record shape/scoped graph refuses: " + str(issues[:1]))
    mapped = D.references_to_doc([S.Symbol("references"), raw])["experiment"][0]
    relations = Relations.bind_relations(mapped, selected)
    require(relations.disposition == "matched", "planned relationships refuse: " + relations.reason)
    Unit.freeze_unit(relations.plan.execution, outputs=tuple(
        Unit.C.OutputTarget(item["role"], item["id"], item["path"]) for item in observations))
    return payload


def _authority_record(context, inventory, author):
    # This is a declaration of public-owner facts, not a second authority loader.
    # Changing live status/view hashes are deliberately excluded from this record.
    def fields(name, values):
        return [S.Symbol(name), *[[S.Symbol(key), value] for key, value in values]]
    form = [S.Symbol("capture-authorities"), [S.Symbol("case_id"), P.CASE_ID],
            fields("reference_identity", context.reference.fields),
            fields("property_authority", asdict(context.property_authority).items()),
            [S.Symbol("expected_author"), author.input_id, Author.SNAPSHOT_ROUTE],
            [S.Symbol("influence"), "Conservative edges from this planned evidence to every reviewed input; initial equal old/new projection, no earlier capture claim."],
            *[fields("input", _record(item).items()) for item in inventory.inputs]]
    payload = R.render_forms([form]).encode()
    require(0 < len(payload) <= SMALL_BYTES, "authority declaration exceeds65536 bytes")
    return payload


def prepare_capture() -> CaptureDeclaration:
    """Compose bounded native declarations; no artifact output or reference process.

    Producer/authority review I/O keeps its existing separate limits. Five curated
    principals are read twice at64KiB each (640KiB maximum), outside the later
    combined artifact allowance. Runtime/schema I/O and RAM are separate costs.
    """
    context = review_authorities()
    review = Review.review()
    require(review["authorities"]["context"] == report(context), "authority views changed during preparation")
    rows = {row["path"]: row for row in review["files"]}
    children = []
    normative = P.signed_division_case().required_inputs[0]
    for path in review["proposed_children"]:
        role = ("expected-author" if path == "scripts/derive_rv64gc_expectations.py" else
                "normative-source" if path == normative.path else "dependency")
        identity = normative.input_id if path == normative.path else "dependency-" + _digest(path.encode())
        children.append(Execution.InputBinding(role, identity, path, rows[path]["sha256"]))
    children = tuple(children)
    require(len(children) == 64, "reviewed flat population differs")
    require(normative in children, "reviewed normative input differs")
    dependencies = F.encode_dependencies(dict(format_version="matched-gpr-dependencies-v1",
                                             input=[_record(item) for item in children]),
                                         path=PREFIX + "/dependencies.sexp")
    prepared = tuple(Execution.InputBinding(role, identity, path, digest)
                     for role, identity, path, _, digest in PREPARED)
    data = tuple(_read_pinned(item, row[3]) for item, row in zip(prepared, PREPARED))
    identity = I.check_reference_identity_bytes(data[-1], path=IDENTITY_PATH, context=context.reference)
    require(identity.disposition == "matched", "selected retained identity differs")
    require(prepared[0].sha256 == review["exercised"]["image_sha256"], "prepared image differs from reviewed build")
    paths = (("guest-source", Review.GUEST), ("collector", "scripts/matched_gpr_unit_collector.py"),
             ("adapter", "scripts/run_rv64gc_sail.py"))
    inputs = tuple(Execution.InputBinding(role, role, path, rows[path]["sha256"])
                   for role, path in paths) + prepared + (
        Execution.InputBinding("dependency-manifest", "dependency-manifest",
                               PREFIX + "/dependencies.sexp", _digest(dependencies)),)
    inventory = Inputs.freeze_review(Inputs.InputReview(PROFILE, P.CASE_ID, inputs + children),
                                     profile_id=PROFILE, experiment_id=P.CASE_ID)
    author = next(item for item in children if item.role == "expected-author")
    author_review = Author.freeze_review(Author.ExpectedAuthorReview(
        inventory, author.input_id, Author.SNAPSHOT_ROUTE), profile_id=PROFILE, experiment_id=P.CASE_ID)
    planned = _planned_record(context, inputs, author)
    projection = Impact.project_inputs(inventory)
    evidence = Change.DependencyNode(projection.evidence_key, "evidence", (PROFILE,), _digest(planned), None)
    graph = Change.DependencyGraph((PROFILE,), (*projection.nodes, evidence),
                                   tuple((evidence.key, node.key) for node in projection.nodes))
    impact = Impact.ImpactReview(PROFILE, P.CASE_ID, graph, graph)
    frozen = Impact.freeze_review(impact, profile_id=PROFILE, experiment_id=P.CASE_ID)
    require(Impact.check_inputs(frozen, inventory.inputs, inventory.inputs).disposition == "matched",
            "initial input influence projection refuses")
    authority_record = _authority_record(context, inventory, author)
    require(tuple(_read_pinned(item, row[3]) for item, row in zip(prepared, PREPARED)) == data,
            "prepared inputs changed during preparation")
    return CaptureDeclaration(context, planned, dependencies, authority_record,
                              inventory, author_review, impact)


def declaration_files(declaration):
    return (("planned-experiment.sexp", declaration.planned_experiment),
            ("dependencies.sexp", declaration.dependencies),
            ("authorities.sexp", declaration.authority_record))


def capture():
    """Require exact native predeclarations, then delegate one fresh three-run unit.

    The operator must commit source and declarations before this call. This
    function does not use Git to establish that workflow fact. The existing
    collector exclusively creates observations; the caller retains returned
    measured record/findings. Failed/partial outputs are never removed or retried.
    """
    declaration = prepare_capture()
    for name, payload in declaration_files(declaration):
        binding = Execution.InputBinding("declaration", name, PREFIX + "/" + name, _digest(payload))
        require(_read_pinned(binding, len(payload)) == payload, "native predeclaration differs")
    return Unit.capture_and_evaluate(
        ROOT, planned_experiment=declaration.planned_experiment,
        scope=declaration.authorities.scope, current_candidate=dict(declaration.authorities.reference.fields),
        reviewed_inputs=declaration.inventory, author_review=declaration.author,
        impact_review=declaration.impact, property_authority=declaration.authorities.property_authority,
        max_read_bytes=Unit.C.TOTAL_BYTES)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--review-authorities", action="store_true")
    action.add_argument("--declare", action="store_true", help="print native declarations as JSON strings; no writes")
    action.add_argument("--capture", action="store_true", help="collect only after committing exact native declarations")
    args = parser.parse_args()
    try:
        if args.declare:
            declaration = prepare_capture()
            result = dict(disposition="pending", canonical_capture=False, qualification=False,
                          files={PREFIX + "/" + name: payload.decode()
                                 for name, payload in declaration_files(declaration)})
        elif args.capture:
            captured = capture()
            # Keep the existing typed result API; stdout is only a bounded receipt.
            result = dict(disposition=captured.disposition, reason=captured.reason,
                          charged_read_bytes=captured.charged_read_bytes, qualification=False,
                          measured_experiment=None if captured.experiment is None else captured.experiment.decode(),
                          collection=None if captured.collection is None else captured.collection.disposition,
                          evaluation=None if captured.evaluation is None else captured.evaluation.disposition)
        else:
            result = report(review_authorities())
    except OSError as error:
        print(json.dumps(dict(disposition="unavailable", reason=type(error).__name__)))
        return 2
    except (AuthorityError, Review.ReviewError, F.ArtifactError, R.RecordRefused,
            Unit.C.CaptureError, Inputs.ReviewError, Author.AuthorReviewError,
            Impact.ImpactReviewError, Change.ImpactError, K.SchemaError, S.SexpError,
            C.CatalogRefused, D.DossierError, I.IdentityError,
            P.PropertyError, UnicodeError) as error:
        print(json.dumps(dict(disposition="refused", reason=str(error))))
        return 1
    print(json.dumps(result, indent=2))
    if args.capture and result["disposition"] != "pending":
        return 2 if result["disposition"] == "unavailable" else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
