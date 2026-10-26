# A source-grounded signed-division witness

This finite property and pure API were declared by P4-SYSTEM.14 before their
implementation and before any new canonical capture. Both the pure API and
authenticated composition are implemented. Existing experiments retain their
historical scope. No requirement status or CPU gate changes here.

## Reviewed source and scope

The pinned RISC-V Ratified Specifications Library v20260120, M version2.0,
RVI-M §11.1.2 defines signed DIV as division rounding toward zero. The verified
35588-byte page has SHA256
`85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716`.
That original publication digest remains the selected source authority. Runtime
property authentication uses the separately pinned retained excerpt described
below; it does not need the acquired full page. No submodule implementation is read.

The canonical catalogue classifies REQ-GC-M as `defined`, risk `medium`, and maps
it to OB-GC-M in contract rv64gc-lab-env-v2/version2. The obligation covers all13
M forms and their boundary behavior. This case supports **one finite quotient
observation**. It does not discharge the whole requirement or obligation.

Case `rv64gc-signed-div-truncation-v2` supersedes the pre-capture v1 full-page
binding. It uses the existing `m-div.s` unchanged:
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

The manifest must declare this exact flat normative-source child, whose
identity differs from the original publication:

| Input ID / role | Repository-relative path | SHA256 |
| --- | --- | --- |
| RVI-M-DIV-STATEMENT / normative-source | `profiles/rv64gc-lab-v0/retained/div-statement.html` | `bbe3ff9dd6d8e1b452589669cd676d998265327eeaf8ed370bb95fcf15af1a58` |

The1576-byte artifact retains the exact182-byte `norm:div_divu_op` span, with
attribution, source/licence pins and an extraction notice. The scoped terms and
curation decision are in `materials/RVI_M_RETENTION.md`; the bounded extractor is
`scripts/retain_div_statement.py`. The excerpt supplies the rounding rule for
this finite witness. It grants no acceptance for the other M instructions.

`v2` rejects the old full-page child as a substitute, including a correct old
page digest under the old ID. It also refuses changed excerpt role, ID, path,
digest or child membership. The source authority still requires `RVI-M` with
the original full-page digest; substituting the excerpt digest there refuses.
An explicit v1 case selection is unsupported. No canonical capture used v1.

This authority projection does **not** normalize artifact pins or suppress input
impact. Actual producer inputs retain exact full-byte authentication and complete
old/new dependency review. A captured catalogue used as an input needs its own
retained snapshot and exact pin; it must not alias a changing live output file.
Semantic currentness, input authentication and coverage remain distinct checks.

## Pure API contract

`scripts/matched_gpr_property.py` owns the reviewed cases as a table (a42at):
`reviewed_case(case_id)` returns a fresh frozen `ReviewedPropertyCase`, and
`reviewed_case_ids()` lists them — `rv64gc-signed-div-truncation-v2`
(`signed_division_case()`, the retained case, `CASE_ID`) and `rv64gc-m-forms-v3`
(`m_forms_case()`, declared before its declaration record and capture; see the
last section). A case carries its program, boundary budget, source size and
digest, its `properties` — one `ReviewedProperty` each with an identity, the
policy cell it serves (`form:<mnemonic>` or `table1:<row>`), its statement, its
typed `GprWitness` and its reviewed RV64 value — the identity of the one property
the control discriminates (`control_property_id`, with `control_value`, the wrong
value the mutant expectation carries), the reviewed instruction words
(`reviewed_steps`), the authority pins and the finite coverage. The code is the
reviewed case owner; there is no new canonical file format or parser.

`PropertyContext` contains profile_id, experiment_id, program, `claims` — one
`PropertyClaim` per declared property: property_id, requirement_id,
obligation_ids, statement and the existing `GprWitness` — `control_property_id`
and the copied PropertyAuthority.
`freeze_context(context, profile_id=..., experiment_id=...)` validates bounded
plain metadata and copies it before future artifact I/O. Canonical raw property
schema/scoped graph validation remains the existing owner's responsibility.
Construct the claims from the actual declared properties and the parent program;
the pure API cannot recover fields absent from RelationPlan. Authenticated
composition binds those fields before reads.
Strings are 1..65536 characters, a context carries 1..64 claims with distinct
identities and distinct witnesses and names its control among them, obligation
IDs form a plain unique tuple of 1..64 per claim, and each copied witness uses
step 0..4095 and x1..x31. Malformed context raises `PropertyError`; this is not a
second canonical loader.

`bind_source_property(context, profile_id=..., experiment_id=..., manifest=...,
source_values=..., case_id='rv64gc-signed-div-truncation-v2')` re-freezes context
for direct calls, then binds the public ManifestPlan and SourceExpectationCheck.
It copies inventory metadata through the existing input-review owner, without
creating independent review authority. Current semantic authority must equal the
independently reviewed case fingerprints. Bind the sorted claims — identity,
requirement, obligations, exact statement and witness of every declared property —
and the control's identity to the reviewed case; the relation plan's properties
and its control property/witness to the context; program/budget/entry/source
identity; the selected baseline expectation digest; stable semantic authority
and the normative child pin; the actual snapshot's reviewed words, widths, PCs,
fetch counts and GPR changes (the three-boundary prefix for the retained case,
all 33 boundaries for the m-forms case); and then every predeclared value: each
property's witness must be an actual derived register change carrying exactly
the reviewed RV64 value, read from the source derivation the source-value finding
already carries (that finding's own witness is the control's). Source
annotation/derivation strings carry no authority and are ignored.

Return frozen `SourcePropertyCheck`: matched with copied finite facts (the case,
one `ObservedProperty` per reviewed property with its witness and value, the
source and the authority pins), refused with no facts for contradictions or
malformed inputs — a record declaring a property the case does not review, or
one wrong predeclared value, is refused by name — unsupported with no facts for
an unknown case or unsupported source-value scope. Unexpected programming
failures propagate. A match establishes this reviewed finite property binding;
file authentication, expected-author provenance, actual collection/control,
review completeness, full policy and requirement-status derivation remain separate.
No file, binary or process is opened. Existing raw schema, manifest, source-value
and snapshot owners retain their contracts; this API does not reinterpret source
code or introduce an arithmetic engine.


## Complete synthetic example

Run from the repository root. The fixture reads the tracked canonical guest,
expectation and mapped catalogues and constructs public-owner metadata facts.
The checker opens no files. This does not authenticate the declared normative
excerpt or run a reference process; it demonstrates finite source meaning and the
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
print(checked.disposition, hex(checked.facts.observed[0].value), checked.facts.case.coverage)
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


## Authenticated composition contract (a42u)

`evaluate_retained_unit(..., property_authority=..., case_id=...)`
requires `author_review`. The caller names the reviewed case the properties are bound to
(`case_id`, the retained case by default); an unknown case refuses before any artifact read,
and a record that is not that case's refuses by name (a42av: the capture of a declared case
names it, so no constant inside a pinned module has to move). Build PropertyContext from **every** declared property
of the actual validated record — its ID, requirement, obligations and statement,
with the relation plan's witness for it — the frozen parent program, scoped IDs
and the property the control run names. Bound the property count (1..64) and
each property's obligations before tuple copying. Freeze context and its supplied current canonical authority before the
manifest or any artifact read. Caller-supplied context text cannot replace the
selected raw property.

Append EvaluationCheck.source_property after all old fields. After matched
source values and reviewed-author metadata, invoke the pure owner once with the
frozen context, authenticated manifest plan and retained source-value finding.
Reuse existing bytes; the declared normative child is authenticated through the
same file-set ledger. No source reopening or additional checker reads. Preserve
all earlier record, authentication, receipt, comparison, image, value and author
findings. Invalid result types/dispositions/reasons/facts or facts contradicting
the reviewed case, actual context, selected source/value or authenticated authority
pins refuse without retaining the invalid property finding. A typed refusal
terminates refused; a typed unsupported result stays pending without credit.
Earlier failures skip this phase. Matches remain pending full method/policy.

The permanent composition controls copy the actual tracked1576-byte excerpt into
an owned temporary fixture and authenticate it with the real bounded reader.
No primary-page authentication double or acquired materials cache is used. The
23 declared files are read once each; the excerpt contributes its own exact byte
charge and pin. Missing excerpt bytes return unavailable, changed bytes return
stale, and both stop before property binding. The observations and expected-author
identity in this fixture remain synthetic; these controls run no reference process
and grant no canonical capture or qualification credit.


## Composition examples

This self-contained example authenticates the real retained excerpt alongside
the other fixture files. The observations remain synthetic. It exercises
orchestration and byte authentication, without a reference capture.

```bash
python3 - <<'PYCODE'
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
sys.path.insert(0, str(Path('scripts').resolve()))
import matched_gpr_evaluation as E
import probe_matched_gpr_property_evaluation as P

base = Path('target/property-composition-example')
base.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=base) as directory:
    f = P.Fixture(Path(directory))
    checked = E.evaluate_retained_unit(f.root, **f.arguments())
    print(checked.disposition, checked.expected_author.disposition,
          checked.source_property.disposition)
    f.graph['property'][0]['statement'] = 'an unrelated claim'
    checked = E.evaluate_retained_unit(f.root, **f.arguments())
    print(checked.disposition, checked.source_values.disposition,
          checked.source_property.disposition)
PYCODE
```

Output:

```text
pending matched matched
refused matched refused
```

The second call binds the actual changed raw statement and refuses its property
claim while retaining matched source values. Supplying a known authority does not
replace that statement.

Run the cache-free retained-excerpt smoke directly:

```bash
python3 scripts/probe_matched_gpr_property_evaluation.py --retained-excerpt-smoke
```

It prints:

```text
RETAINED EXCERPT SMOKE: pending / finite property matched / 23 authenticated files / 0xfffffffffffffffd; no capture credit
```

The fixture copies the tracked excerpt into an owned on-volume temporary directory
and removes the directory at exit. Missing bytes return2/UNAVAILABLE; a changed
pin refuses. The checker runs no reference process and grants no whole-M or
qualification credit. This supersedes the v1 optional acquired-page smoke.

## The m-forms case: twenty-five predeclared properties (a42at)

The policy's two pending legs ask for one capture that predeclares every Table 1 row and
every M form (see [Policy legs measured](policy-adequacy.md)). `m_forms_case()` is that
case, declared in the binding before its declaration record and its capture:
`rv64gc-m-forms-v3`, 33 boundaries over `profiles/rv64gc-lab-v0/guests/m-forms.s`
(3,886 bytes, SHA256 `232b4d96d87125c3ab876b2ec415d250a572433df57d5696afffde6a95f8d7a6`),
the same requirement, obligation, contract and semantic authority as the retained case, and
the same pinned normative excerpt. Its reviewed words cover all 33 boundaries, not a prefix.
The control is the DIV rounding witness again — `form-div`, boundary 12, x15, −3 → −4 — so
the three-run comparison discriminates the same wrong result the retained case's control did.

| Property | Cell | Boundary | Register | Reviewed RV64 value |
| --- | --- | --- | --- | --- |
| `form-mul` | form:mul | 7 | x10 | `0xfffffffffffffff2` (−14) |
| `form-mulh` | form:mulh | 8 | x11 | `0xffffffffffffffff` (−1) |
| `form-mulhsu` | form:mulhsu | 9 | x12 | `0xfffffffffffffff9` (−7) |
| `form-mulhu` | form:mulhu | 10 | x13 | `0x0000000000000001` |
| `form-mulw` | form:mulw | 11 | x14 | `0xffffffff80000000` |
| `form-div` | form:div | 12 | x15 | `0xfffffffffffffffd` (−3; the control's property) |
| `form-divu` | form:divu | 13 | x16 | `0x7fffffffffffffff` |
| `form-rem` | form:rem | 14 | x17 | `0xffffffffffffffff` (−1) |
| `form-remu` | form:remu | 15 | x18 | `0x0000000000000001` |
| `form-divw` | form:divw | 16 | x19 | `0xffffffffc0000000` (−2^30) |
| `form-divuw` | form:divuw | 17 | x20 | `0x0000000040000000` |
| `form-remw` | form:remw | 18 | x21 | `0xfffffffffffffffe` (−2) |
| `form-remuw` | form:remuw | 19 | x22 | `0xffffffff80000000` |
| `table1-div-by-zero` | table1:div-by-zero | 20 | x23 | `0xffffffffffffffff` |
| `table1-divu-by-zero` | table1:divu-by-zero | 21 | x24 | `0xffffffffffffffff` |
| `table1-rem-by-zero` | table1:rem-by-zero | 22 | x25 | `0xfffffffffffffff9` (the dividend) |
| `table1-remu-by-zero` | table1:remu-by-zero | 23 | x26 | `0xfffffffffffffff9` (the dividend) |
| `table1-div-overflow` | table1:div-overflow | 24 | x27 | `0x8000000000000000` (the dividend) |
| `table1-rem-overflow` | table1:rem-overflow | 26 | x28 | `0x0000000000000000` |
| `table1-divw-by-zero` | table1:divw-by-zero | 27 | x29 | `0xffffffffffffffff` |
| `table1-divuw-by-zero` | table1:divuw-by-zero | 28 | x30 | `0xffffffffffffffff` |
| `table1-remw-by-zero` | table1:remw-by-zero | 29 | x31 | `0xffffffff80000000` |
| `table1-remuw-by-zero` | table1:remuw-by-zero | 30 | x10 | `0xffffffff80000000` |
| `table1-divw-overflow` | table1:divw-overflow | 31 | x11 | `0xffffffff80000000` |
| `table1-remw-overflow` | table1:remw-overflow | 32 | x12 | `0x0000000000000000` |

The thirteen form properties are the mnemonics `REQ-GC-M` names, once each; the twelve
Table 1 properties are exactly the expectation steps whose source cites `RVI-M §11.1.2
(Table 1)`. The probe re-derives every one of the 33 words from the encoding fields
(I-type `addi`/`slli`, R-type `OP`/`OP-32` with `funct7 = 1`) and every value with plain
integer arithmetic and the chapter's Table 1 rules, with no author and no assembler, and
compares them with the case table and with the snapshot author's derivation. It then binds
the case through the pure API with a 25-claim context and checks that one wrong predeclared
value, a renamed or missing claim, a wrong control identity or a swapped witness refuses.

```bash
python3 scripts/probe_matched_gpr_property.py
python3 -O scripts/probe_matched_gpr_property.py
python3 scripts/probe_matched_gpr_property.py --mutation claim-values
```

The first two print `MATCHED-GPR-PROPERTY: 34 tests / 0 failures / 0 errors; synthetic
metadata, finite source witnesses only`; the third omits the per-property value check and
fails the three tests that depend on it. The binding grants the m-forms case nothing: no
declaration record names it yet, no capture retains its runs, no receipt cites it, and
`REQ-GC-M` kept deriving `planned` (until the m-forms capture and its credit record of 2026-10-26). The declaration (`capture_div.py --declare`) and the
capture are the next units; the retained case stays `rv64gc-signed-div-truncation-v2` until
the capture lands and is `invalidated` meanwhile, because this binding is one of its pinned
inputs (`decision_many-predeclared-properties-one-control.md`).
