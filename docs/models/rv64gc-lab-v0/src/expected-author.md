# Reviewed expected-author binding

The source-value check rederives numbers. A separate check must bind the declared
expected producers to the author selected by the caller's review. P4-SYSTEM.14
implements the finite contract below, declared before its implementation. The legacy evaluator
continues to leave producer adequacy pending; this API does not change that result.

## Caller authority and inputs

`matched_gpr_expected_author.ExpectedAuthorReview` contains a full `InputReview`,
an `author_input_id`, and route `snapshot-parcels-v1`. Call `freeze_review` with the
selected `profile_id` and `experiment_id` before artifact I/O. It validates and
copies the inventory through the existing input-review owner, selects exactly
one role `expected-author`, and copies its identity. The selected ID must name
that entry. Review quality and complete dependency discovery remain the caller's
responsibility. Copying a record's own inventory supplies no independent review.

`bind_expected_author(review, profile_id=..., experiment_id=..., manifest=...,
derivation=...)` is pure: it opens no files, runs no process, and accepts the
existing validated `ManifestPlan` and the existing author's `SnapshotDerivation`.
It freezes the review again so direct calls receive the same checks. The manifest
and derivation must come from their public owners; this function does not replace
raw schema/graph validation, artifact authentication or source rederivation.

## Exact binding rules

- The complete declared inventory must equal the caller review by ID, role,
  repository-relative path and lowercase SHA256; order is irrelevant.
- The selected author must be a flat manifest child with role `expected-author`.
  It cannot stand in for a principal input or the manifest itself.
- The relation plan's common expected-producer version must be
  `sha256:<reviewed author SHA256>`. Both actual expected producers must consume
  the selected guest-source and dependency-manifest principals. Existing relation
  checks already require the selected expectation and equal common inputs.
- The snapshot's author path and route must match the selected author and route;
  its source SHA256 must match the selected guest-source pin and its instruction
  budget must match the frozen execution plan.

The result is frozen `ExpectedAuthorCheck`: `matched` with metadata facts, or
`refused` with no facts and a reason. Malformed review authority raises the bounded
`AuthorReviewError` from `freeze_review`; the binding API returns a refusal for it.
Unexpected programming failures propagate. The API has no filesystem or memory
budget beyond existing bounded metadata containers; it reads no source payload.

## What a match means

The finding establishes declared metadata relationships only. File authentication
remains the shared reader's job. Even authenticated author bytes do not attest
which code was loaded or executed when old outputs were produced. A trusted
capture procedure, reviewed runtime/dependency closure and fresh controls remain
necessary. It does not establish independence, source-grounded property meaning,
collector provenance, ancestry, freshness, full method adequacy or qualification.
The version convention is prospective for this opt-in review; existing arbitrary
version labels remain uncredited by the legacy evaluator.

## Complete synthetic example

Run from the repository root. This creates temporary fixtures under `target`,
authenticates their manifest through its public owner, and removes the fixture
at exit. It starts no reference process. The inventory is supplied independently
of the manifest reader; these deliberately synthetic pins do not represent a
canonical dependency review. The author leaf contains opaque fixture bytes:
a match demonstrates metadata binding, **not** that those bytes executed.

```bash
python3 - <<'PYCODE'
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
sys.path.insert(0, str(Path('scripts').resolve()))
import matched_gpr_expected_author as A
import probe_matched_gpr_evaluation as P

base = Path('target/expected-author-example')
base.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=base) as directory:
    f = P.Fixture(Path(directory))
    snapshot = A.Author.derive_snapshot(f.source, program=f.experiment['program'], instructions=1)
    author = dict(id='author leaf', role='expected-author', path=snapshot.author_path, sha256='0' * 64)
    f.write(author, b'# synthetic author identity; never executed\n')
    f.write(f.inputs['dependency-manifest'], P.F.encode_dependencies(dict(
        format_version='matched-gpr-dependencies-v1', input=[author]),
        path=f.inputs['dependency-manifest']['path']))
    for producer in f.graph['producer'][1:]:
        producer['version'] = 'sha256:' + author['sha256']
    f.publish_receipts()
    inventory = A.T.InputReview('synthetic', f.experiment['id'], tuple(
        A.E.InputBinding(item['role'], item['id'], item['path'], item['sha256'])
        for item in [*f.graph['input'], author]))
    review = A.freeze_review(A.ExpectedAuthorReview(inventory, author['id'], snapshot.route),
        profile_id='synthetic', experiment_id=f.experiment['id'])
    manifest = A.M.read_dependency_manifest(f.root,
        experiment=f.experiment, current_candidate=f.candidate)
    assert manifest.disposition == 'matched', manifest.reason
    def bind(plan):
        return A.bind_expected_author(review, profile_id='synthetic',
            experiment_id=f.experiment['id'], manifest=plan, derivation=snapshot)
    checked = bind(manifest.plan)
    print(checked.disposition, checked.facts.route)
    bad = replace(manifest.plan, relations=replace(manifest.plan.relations,
        expected_version='unreviewed-version'))
    checked = bind(bad)
    print(checked.disposition, checked.reason)
PYCODE
```

Expected output:

```text
matched snapshot-parcels-v1
refused expected author: expected producer version differs from reviewed author digest
```

Authenticated evaluator composition follows in a separate owned slice. This pure
API grants no CPU or board milestone credit.
