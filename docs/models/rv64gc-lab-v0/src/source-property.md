# A source-grounded signed-division witness

This finite property and pure API were declared by P4-SYSTEM.14 before their
implementation and before any new canonical capture. The pure API is implemented;
authenticated composition follows separately. Existing experiments
retain their historical scope. No requirement status or CPU gate changes here.

## Reviewed source and scope

The pinned RISC-V Ratified Specifications Library v20260120, M version2.0,
RVI-M §11.1.2 defines signed DIV as division rounding toward zero. The verified
35588-byte page has SHA256
`85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716`.
Its published materials resolver supplies the offline snapshot; the optional
fetched working directory need not exist. No submodule implementation is read.

The canonical catalogue classifies REQ-GC-M as `defined`, risk `medium`, and maps
it to OB-GC-M in contract rv64gc-lab-env-v2/version2. The obligation covers all13
M forms and their boundary behavior. This case supports **one finite quotient
observation**. It does not discharge the whole requirement or obligation.

Case `rv64gc-signed-div-truncation-v1` uses the existing `m-div.s` unchanged:
2512 source bytes, SHA256
`a7cbbe8c3005a7c0da68bf356a0fb6b072dbe0cdcc659eff523e465c60ae907f`.
The whole guest has27 boundaries. The witnessed prefix is:

| Boundary | PC | Instruction word | Meaning / changed register |
| --- | --- | --- | --- |
| 0 | `0x80000000` | `0xff900293` | `addi x5,x0,-7`: x5 becomes −7. |
| 1 | `0x80000004` | `0x00200313` | `addi x6,x0,2`: x6 becomes2. |
| 2 | `0x80000008` | `0x0262c3b3` | `div x7,x5,x6`: x7 becomes −3. |

Each instruction is4 bytes/two parcels. The DIV word independently encodes
opcode0x33, funct7=1, funct3=4, rd7, rs1=5 and rs2=6. The immediate words
independently encode the two operands; this is not an inference from a mnemonic
or annotation supplied by a producer. At the cold entry, the prefix establishes
the operands before division. The source rule gives magnitude floor(7/2)=3 and
negative sign; −7 =2×(−3)+(−1). In RV64 the quotient is
`0xfffffffffffffffd`. A floor-toward-negative-infinity answer would be −4,
`0xfffffffffffffffc`; that is the prospective wrong-result control.

The exact property statement is:

> For signed DIV with x5 = -7 and x6 = 2, the x7 change at boundary 2 is -3 (rounding toward zero).

This credits quotient meaning at step2/x7, not an observation of every internal
CSR, trap, memory request, reservation, later M result or absence of side effects.
The complete source-value and three-run comparison owners retain their separate
whole-budget checks. This API does not execute or credit the prospective control.

## Stable current authority and exact file pins

A whole requirement-file hash would include its derived implementation_status.
The prototype's status-only control changed that field from planned to partial:
its full-file SHA changed from
`0f006fa9bccb664cf461684fd9976fb4cc63ea3ca4272e28c7b731fc52de8802` to
`63e49d3d78656f9e94bca07d1d28951a616d736207b1ecaab4099cd155ea41a6`,
although every other field of REQ-GC-M stayed identical. Making that live file an
authority pin would let publishing derived status invalidate its own evidence.
This design was rejected before this case's first commit or capture.

Use a **current semantic authority view**, separate from captured file inputs.
`project_authority(profile_id, requirement=..., obligation=..., source=...)`
accepts caller-selected, already schema-validated canonical mapped records from
the existing records_sexp/dossier owners. Copy bounded plain trees, require exact
record round trips through records_sexp, then fingerprint the selected records
using that owner's canonical renderer. Normalize only the requirement's derived
implementation_status to planned and its implementation_refs/evidence_ids to
empty lists in this private hashing copy. No source document is rewritten or
created. The projection domain is matched-gpr-property-authority-v1 plus record
kind. The obligation record is fingerprinted in full. The reviewed requirement
fingerprint is `0deea596341b2462d8c61b90c37791e566d58ccfa95c4d30beaeebcd37e30989`;
the obligation fingerprint is
`b441b5339cbe879ba02970b69d7a1b51ce1e548a9c5f2bfe550b39beb04c8090`. Changed statement, source,
category, risk, scope, dependencies or effective contract therefore changes the
reviewed authority; derived output fields do not.

The source view carries the current selected RVI-M ID and page SHA. The helper
requires the selected profile in both records. It returns frozen PropertyAuthority
with profile/requirement/obligation/source IDs and semantic/source digests.
The caller must supply current canonical authority, not echo a capture's own
claims. Mapping/schema validation stays with the existing owners. Trees are
bounded per supplied record to4096 nodes, depth16,1MiB UTF8 string payload,
strings<=65536 characters and integers<=128 bits; malformed inputs raise
PropertyError. Copy dictionaries in key order so mapped parameter order is stable.

The manifest must also declare this exact flat normative-source child:

| Input ID / role | Repository-relative path | SHA256 |
| --- | --- | --- |
| RVI-M / normative-source | `.materials/riscv/pinned-v20260120/unpriv/m-st-ext.html` | `85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716` |

This authority projection does **not** normalize artifact pins or suppress input
impact. Actual producer inputs retain exact full-byte authentication and complete
old/new dependency review. A captured catalogue used as an input needs its own
retained snapshot and exact pin; it must not alias a changing live output file.
Semantic currentness, input authentication and coverage remain distinct checks.

## Pure API contract

`scripts/matched_gpr_property.py` supplies `signed_division_case()` returning a
fresh frozen reviewed case, including its statement, witness, expected/control
values, authority pins and finite coverage. The code is the reviewed case owner;
there is no new canonical file format or parser.

`PropertyContext` contains profile_id, experiment_id, program, property_id,
requirement_id, obligation_ids, statement, the existing `GprWitness`, and the
copied PropertyAuthority.
`freeze_context(context, profile_id=..., experiment_id=...)` validates bounded
plain metadata and copies it before future artifact I/O. Canonical raw property
schema/scoped graph validation remains the existing owner's responsibility. Construct the context
from the actual selected property and parent program; the pure API cannot recover
fields absent from RelationPlan. Authenticated composition will bind those fields
before reads.
Strings are1..65536 characters, obligation IDs form a plain unique tuple of1..64,
and the copied witness uses step0..4095 and x1..x31. Malformed context raises
`PropertyError`; this is not a second canonical loader.

`bind_source_property(context, profile_id=..., experiment_id=..., manifest=...,
source_values=..., case_id='rv64gc-signed-div-truncation-v1')` re-freezes context
for direct calls, then binds the public ManifestPlan and SourceExpectationCheck.
It copies inventory metadata through the existing input-review owner, without
creating independent review authority. Current semantic authority must equal the
independently reviewed case fingerprints. Bind the selected relation/property,
requirement, obligation, exact statement and witness; program/budget/entry/source
identity; selected baseline expectation digest; stable semantic authority and
the normative child pin; and the
actual snapshot prefix's words, widths, PCs, fetch counts and GPR changes.
The source-derived witness must be exactly the reviewed RV64 quotient. Source
annotation/derivation strings carry no authority and are ignored.

Return frozen `SourcePropertyCheck`: matched with copied finite facts, refused
with no facts for contradictions or malformed inputs, unsupported with no facts
for an unknown case or unsupported source-value scope. Unexpected programming
failures propagate. A match establishes this reviewed finite property binding;
file authentication, expected-author provenance, actual collection/control,
review completeness, full policy and requirement-status derivation remain separate.
No file, binary or process is opened. Existing raw schema, manifest, source-value
and snapshot owners retain their contracts; this API does not reinterpret source
code or introduce an arithmetic engine. Authenticated composition follows later.


## Complete synthetic example

Run from the repository root. The fixture reads the tracked canonical guest,
expectation and mapped catalogues and constructs public-owner metadata facts.
The checker opens no files. This does not authenticate the declared normative
page or run a reference process; it demonstrates finite source meaning and the
status-cycle repair, with no capture/qualification credit.

```bash
python3 - <<'PYCODE'
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import sys
sys.path.insert(0, str(Path('scripts').resolve()))
import matched_gpr_property as G
import probe_matched_gpr_property as P

f = P.fixture()
def bind(context):
    return G.bind_source_property(context, profile_id='rv64gc-lab-v0',
        experiment_id=f.context.experiment_id, manifest=f.manifest, source_values=f.values)
checked = bind(f.context)
print(checked.disposition, hex(checked.facts.observed_value), checked.facts.case.coverage)
requirement = deepcopy(f.requirement)
requirement.update(implementation_status='implemented', evidence_ids=['new-output'])
authority = G.project_authority('rv64gc-lab-v0', requirement=requirement,
    obligation=f.obligation, source=f.source)
print(bind(replace(f.context, authority=authority)).disposition, authority == f.context.authority)
requirement['risk'] = 'high'
authority = G.project_authority('rv64gc-lab-v0', requirement=requirement,
    obligation=f.obligation, source=f.source)
checked = bind(replace(f.context, authority=authority))
print(checked.disposition, checked.reason)
PYCODE
```

Expected output:

```text
matched 0xfffffffffffffffd one signed-DIV quotient witness
matched True
refused source property: current semantic authority differs from reviewed case
```

The first line supports the declared finite quotient. The second leaves source
meaning stable when derived output changes; it does not grant that output's
status. The third refuses a changed risk disposition, which needs different
policy evidence. No other M form is credited by these lines.
