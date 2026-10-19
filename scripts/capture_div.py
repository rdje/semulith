#!/usr/bin/env python3
"""Review current DIV capture authorities; execution and publication are pending.

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
import dossier_sexp as D
import experiment_verification as V
import matched_gpr_identity as I
import matched_gpr_property as P
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


class AuthorityError(ValueError):
    """Current validated views cannot supply this reviewed finite case."""


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
                     "final entrypoint, manifest, review and full policy pending"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-authorities", action="store_true", required=True)
    parser.parse_args()
    try:
        result = review_authorities()
    except OSError as error:
        print(json.dumps(dict(disposition="unavailable", reason=type(error).__name__)))
        return 2
    except (AuthorityError, Review.ReviewError, K.SchemaError, S.SexpError,
            C.CatalogRefused, R.RecordRefused, D.DossierError, I.IdentityError,
            P.PropertyError, UnicodeError) as error:
        print(json.dumps(dict(disposition="refused", reason=str(error))))
        return 1
    print(json.dumps(report(result), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
