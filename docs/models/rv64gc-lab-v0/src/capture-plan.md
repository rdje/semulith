# Predeclaring the first division capture

The first canonical case is `rv64gc-signed-div-truncation-v2`, owned by
`scripts/matched_gpr_property.py`. It runs `m-div.s` for27 boundaries. The finite
claim is the x7 change at boundary2: signed `-7 / 2` produces `-3`. The negative
control changes only that expected value to `-4`. Baseline, repeat and control
must use three fresh reference processes with identical executed inputs. This
does not accept all M instructions or close `REQ-GC-M`/`OB-GC-M`. The
[first retained canonical capture](canonical-division.md) now supplies these finite
observations; full policy/qualification remains pending.

## Review the producers before declaring their inputs

`scripts/review_div_capture.py --review` reports the current reviewed population
as JSON on stdout. Redirect it into an owned directory under `target/` when a
local receipt is useful. It launches no reference process and writes no files.

The source review starts at the unit collector, retained evaluator, expected
author, retained-statement extractor and current-authority entrypoint. It conservatively follows every ordinary project-local Python import,
including function-local imports, and checks the result against an explicit
reviewed module set. Unknown external imports, relative/dynamic imports, changed
population and unsafe paths refuse. Python's standard library and interpreter
are external runtime identities, not copied project dependencies. This is an
import census, not proof that arbitrary Python has no hidden dependency.

Separately, the tool exercises the canonical GC image builder, the snapshot
expected author and the four schema loaders used by this route. It records
`sexp.read_file` calls and compares their complete unique population with the
reviewed data set: encoding/profile/state, ten encoding fragments, ten semantic
fragments and four schemas. It checks the independently built image and source
derivation agree. This trace covers those loaders and this case; it cannot
discover an arbitrary new reader that bypasses them. Changes to reviewed source
require another source review even when the population is unchanged.

Inputs are read with finite per-file/aggregate bounds, regular same-volume
repository paths, and before/after byte checks. The pinned guest and retained
DIV excerpt must match the reviewed case. An absent retained excerpt reports unavailable,
never success. The report includes file sizes/digests, import edges, exercised
data paths and runtime identity. A successful review remains `pending`; it
supplies neither an experiment manifest nor qualification.

## Proposed flat input population

The collector and public Sail adapter are two of the existing nine principals.
The proposed dependency children are the other35 imported project modules,
27 exercised execution-data files, the retained DIV excerpt and the profile evidence
policy:64 children, including the review tool and current-authority entrypoint.
The diagnostic derives these counts from path sets and refuses overflow of the
existing64-child limit. Its JSON lists the complete paths; the manifest must be
built from this reviewed population, rather than treating its own declarations
as evidence that the review was complete.

Current requirements, effective obligations and source catalogue entries are
live semantic authority views. They must be validated and projected through
their existing owners. In particular, the property projection excludes derived
requirement implementation status/references; hashing a live status output into
its own evidence inputs would create a cycle. The current parent catalogue is
also selection authority, not an execution input. Capture an immutable reference
identity document with only the selected execution identity. Do not pin the
whole changing parent catalogue in that identity.
The [bounded identity emitter](retained-method.md#emitting-a-selected-execution-descriptor)
constructs and verifies that selected projection. The [canonical descriptor and
its publication metadata](selected-identity.md) are now retained; the remaining
capture declaration must still be committed before execution.

## Execution and retention still required

### Retain licensed text with its own identity

The source catalogue's former claim that the HTML snapshot contains no CC-BY
statement was too broad. The [pinned unprivileged colophon](https://docs.riscv.org/reference/isa/v20260120/unpriv/colophon.html), in its preface
to Version2.2, states CC-BY4.0 applies to that manual and future versions. The
privileged preface has a corresponding statement for its own volume. Website
footers and specification text have different scopes; this does not establish
rights to redistribute the complete website rendering or its assets.

`scripts/retain_div_statement.py` derives one bounded retained input:
`profiles/rv64gc-lab-v0/retained/div-statement.html`. It copies exactly the
`norm:div_divu_op` span from the pinned M page, with a new attribution/provenance
wrapper. The statement retains signed/unsigned XLEN division and rounding toward
zero. It omits the diagrams, other operations, navigation, scripts and styles.
Its identity is distinct from the original full-page identity. The wrapper names
the original URL/digest, the licence-evidence URL/digest, RISC-V International,
the CC-BY4.0 licence and the extraction/change notice. It grants no extra M
coverage, execution, capture or qualification credit.

The emitter requires the exact immutable M page and licence-evidence bytes,
checks their pins and bounds before extraction, and writes only to stdout.
The verifier checks the retained file's own fixed pin through the existing
anchored reader, without opening either acquired source page:

```bash
python3 scripts/retain_div_statement.py --emit
python3 scripts/retain_div_statement.py --verify
python3 scripts/probe_div_statement_retention.py
python3 -O scripts/probe_div_statement_retention.py
```

`--emit` needs the acquired snapshot; a missing input exits2. `--verify` can work
in a fresh checkout and reports byte identity only. Synthetic controls require
no acquired materials. Review the retained text at the source path above.

The v2 property binding now authenticates this excerpt under the separate
`RVI-M-DIV-STATEMENT` input ID. Current semantic authority retains the original
`RVI-M` publication digest; the excerpt cannot replace that authority. The v1
full-page input cannot substitute for the v2 excerpt. The property statement,
guest,27-boundary budget, quotient and negative control are unchanged. No
canonical capture used v1, and explicit v1 selection is unsupported.

The reviewed producer population includes the extractor, even though the capture
route consumes the already curated bytes and does not rerun extraction. Neither
the full source page nor its licence-evidence page is a runtime input on that
route. Their exact provenance remains in the retained artifact and terms record.
The diagnostic checks the excerpt's metadata/bytes and original publication
identity independently. Its37 modules and64 children reach the unchanged64-child
ceiling. The final execution composition must fit this reviewed population or
receive another bounded design review before execution. A copied reviewed input set can
run the diagnostic with no `.materials` directory; success still stays pending.

The asset belongs to the existing registered `profiles/` family; its measured
addition must fit that family's unchanged count, aggregate and member caps.
The [prepared capture inputs and bounded evidence family](prepared-inputs.md)
now declare the first case's output names and retention envelope. Actual fresh
outputs still need measurement against those bounds.

### Complete the capture declaration

Before any canonical run, commit the final entrypoint and exact manifest,
property/author/impact authorities, output namespace and retention family. The
prepared input pins, output namespace and retention family are now declared;
the composed entrypoint and its exact native manifest, planned record and
authorities are retained. Commit them before canonical execution. The
retained file set must support repeatable offline evaluation without relying on
an acquired reference cache. The retained excerpt supplies the normative input;
its original publication remains separate current authority. The binary remains a separately pinned replay dependency;
offline observation checking and reference replay have different availability.

Measure and register the actual retained family with its fixed count/byte caps.
Keep the existing128 MiB aggregate read and16 MiB snapshot envelopes; a combined
collector/evaluator must carry the collection charge forward. Evaluation now
accepts a [delegated remainder](read-allowance.md), including its manifest seed;
the [combined unit helper](unit-evaluation.md) now carries that allowance and
validates seed-inclusive accounting. The [composed command](#the-composed-div-command)
now delegates that helper. Commit its exact native declarations, then capture the
three processes, authenticate every retained input/output and evaluate all27
boundaries, exact repeat bytes and the intended control. Only after that may the
full source/risk/feature policy and derived statuses be integrated. The blanket
qualification refusal remains in force throughout this predeclaration slice.

Run the synthetic diagnostic controls without any acquired material:

```bash
python3 scripts/probe_div_capture_review.py
python3 -O scripts/probe_div_capture_review.py
```

Run the current population review using only tracked inputs:

```bash
python3 scripts/review_div_capture.py --review
```

Its changing digests and byte totals are derived output, not constants to copy
into this chapter. A missing retained excerpt exits2; a refused review exits1;
`pending` exits0 and still grants no canonical capture or method credit.

## Rejecting cyclic version ancestry

A contract version inherits through `extends`. The declaration must terminate:
`v0 -> v1 -> v0` cannot supply an effective contract, even when each individual
form passes the raw schema. The version-order check can report a gap without
making an unguarded ancestry walk terminate.

`scripts/check_contract_freeze.sh` now remembers the versions visited for each
declared version. A repeat returns exit1 with `EXTENDS CYCLE`. The public
`gate_report.contract_measure` similarly refuses a repeat on the selected latest
version's ancestry with `CONTRACT CYCLE`, through its existing `SystemExit`
refusal channel. Scope loading and gate generation reuse that measure. Neither
owner returns partial effective-contract credit for a cycle. Valid inheritance,
supersession, frozen-record pins and realized check bindings keep their meanings.

The regression uses the current complete catalogues and adds self, two-version
and complete-ancestry cycles. Every changed contract passes raw schema checking.
The acyclic control independently recounts effective pairs and checks frozen
records. Run from the repository root:

```bash
python3 scripts/probe_contract_ancestry.py
python3 -O scripts/probe_contract_ancestry.py
```

Each command reports4 tests,0 failures and0 errors. CONTRACT-FREEZE registers both
modes and two independent guard omissions; removing either guard loses three
assertions with0 errors. The diagnostic gives each real owner a three-second
deadline, kills and joins a hung process group, and removes its fixtures under
`target/`. This deadline protects the regression harness; it is no production
runtime guarantee. These are contract-reader controls, with no reference run,
canonical capture or CPU acceptance credit.

## Gate roots follow the loaded source

The public effective-contract owner now derives its repository root from
`gate_report.py`'s source location. Importing it launches no Git process. A copied
runtime therefore imports its own record/dossier/parser modules and reads its own
declared registry, even when launched with the valid parent checkout as its
working directory. Report operations that enumerate tracked files still use Git;
this is a statement about import and the selected contract-measure path.

Before this repair, import-time Git discovery selected the surrounding checkout.
A copied module then credited 114/114 realized pairs while its own registry was
absent. The tracked current checkout's report counts were not changed by that
fixture; the failure concerned attribution in the copied context. Merely copying
files and omitting `.materials` did not prove complete isolation from parent data.

Run the complete controls from the repository root:

```bash
python3 scripts/probe_gate_runtime_root.py
python3 -O scripts/probe_gate_runtime_root.py
```

Each reports 6 tests, 0 failures and 0 errors. The fixture contains five copied
runtime modules, the real contract, an expanded obligation catalogue and its
registry: eight files under a temporary directory on the repository volume.
It checks source/module roots, process-free import, missing/malformed/empty local
registries and unchanged complete results. The valid parent stays available,
making fallback observable. Restoring Git-root selection loses five assertions
with 0 errors in both modes. GATE-REPORT registers these controls and the omission.
This is a selected runtime-boundary check, with no reference run, capture,
arbitrary dependency-completeness proof or qualification credit.

## Selecting current authority views

`scripts/capture_div.py --review-authorities` is the read-only preparation command
for the finite DIV case. It selects current authority through the existing schema,
catalogue, mapping, effective-contract, identity and property owners. It has no
execution or publication side effect in this mode. No binary, acquired page, retained trace or guest
image is opened, and no reference process runs. The selected binary path and SHA
are declarations from the current candidate; this command does not verify them
against an executable or the separately retained descriptor.

The declared population contains exactly thirteen repository-relative views:

| Group | Files and purpose |
| --- | --- |
| Seven catalogue/contract views | `profiles/rv64gc-lab-v0/requirements.sexp`, `profiles/rv64gc-lab-v0/contract-obligations.sexp`, `profiles/rv64gc-lab-v0/contract-v0.obligations.sexp`, `profiles/rv64gc-lab-v0/contract-v1.obligations.sexp`, `profiles/rv64gc-lab-v0/contract.sexp`, `profiles/rv64gc-lab-v0/sources.sexp`, `profiles/rv64gc-lab-v0/references.sexp` |
| Five schema tools | `schema/requirements.sexp`, `schema/contract-obligations.sexp`, `schema/contract.sexp`, `schema/sources.sexp`, `schema/references.sexp` |
| One registry tool | `crates/semulith-verify/src/contract_checks_rv64gc.rs`, read by the public effective-contract owner |

The bounded review reader takes stable, regular, same-volume snapshots before
the canonical tools run. Each direct snapshot is at most 1 MiB; one shared pass
permits at most 8 MiB. A second bounded pass checks that every declared view still
has the same bytes. These direct reads total at most 16 MiB. Public schema,
catalogue and scope tools retain their own I/O, separately from these snapshots
and from the later collector/evaluator's 128 MiB artifact allowance. The command
assumes a trusted, quiescent runtime. Its checks do not make all views one atomic
snapshot or promise a total process-RAM limit.

Every raw catalogue source validates before any record mapper runs. Included
obligations expand through `record_catalog.text`, with original part bytes checked
against the snapshots. Only the two declared parts may be included, and the sole
registry path must equal the declared registry before scope delegation. The first
prototype accepted an alternate valid registry while still listing the original
thirteen views; the actual binding now refuses it before that file can be read.
Raw field validation and unique record IDs are separate checks. Duplicate IDs
refuse before constructing the selected indexes.

The command selects `REQ-GC-M`, its effective `OB-GC-M`, source `RVI-M` and candidate
`sail-riscv`. The public scope owner supplies candidate, requirement and effective
obligation sets, including inherited members and supersession. Missing, foreign
or superseded selected authority refuses. The property projection must equal the
independently reviewed v2 case: changing its risk, obligation statement or original
publication digest refuses. Canonical catalogue/contract integrity remains the
existing repository gates' responsibility; this is no replacement for those gates
or the full evidence policy.

Derived requirement status/references remain excluded only from the semantic
authority projection. A status-only edit therefore changes the diagnostic view
SHA while preserving that authority. Unrelated parent prose likewise changes the
references view SHA without changing the selected execution identity. Changing
the candidate's binary pin changes that identity, without opening the binary.
Do not turn these whole changing view hashes into the experiment's own execution
inputs: that would restore the status/parent-output cycle this design avoids.

Run a complete review and its normal/optimized controls from the repository root:

```bash
set -euo pipefail
python3 scripts/capture_div.py --review-authorities | python3 -c 'import json,sys; r=json.load(sys.stdin); print(r["disposition"], len(r["views"]), r["canonical_capture"], r["qualification"])'
python3 scripts/probe_div_authorities.py
python3 -O scripts/probe_div_authorities.py
```

The first line prints `pending 13 False False`; each probe reports 18 tests with
zero failures and errors. Its fifty-file copied runtime contains no `.materials`
or reference binary. It observes the actual view reads, process absence, raw-before-
mapping order, direct aggregate bound, duplicate/missing/unsafe/oversized views,
semantic changes, supersession/cycles, closed include/registry selection and late
view drift. Three independent omissions lose 3/1/3 assertions in both modes,
with zero test errors. PROFILE-CONSISTENCY runs every outcome.

The Python API returns frozen `CurrentAuthorities`: the public immutable `Scope`,
`ReferenceIdentity`, `PropertyAuthority` and a tuple of `ViewIdentity` facts
(`path`, role, byte size and SHA256). It retains no raw view payloads. The mutable
diagnostic dictionary returned by `report` is detached from those facts:

```bash
PYTHONPATH=scripts python3 - <<'PY_DIV_AUTHORITIES'
from dataclasses import FrozenInstanceError
from capture_div import review_authorities, report

context = review_authorities()
diagnostic = report(context)
print(diagnostic["disposition"], len(context.views),
      context.property_authority.requirement_id)
diagnostic["reference_identity"]["binary_sha256"] = "0" * 64
print(dict(context.reference.fields)["binary_sha256"] != "0" * 64)
try:
    context.views = ()
except FrozenInstanceError:
    print("frozen")
PY_DIV_AUTHORITIES
```

It prints `pending 13 REQ-GC-M`, `True`, then `frozen`. Direct Python callers retain
the component owners' typed exceptions; the CLI emits JSON `pending` with exit0,
`refused` with exit1 for expected invalid views, and `unavailable` with exit2 for
I/O failure. Wrong usage also exits2 on stderr. Unexpected programming exceptions
propagate. Redirect diagnostic output only into an owned on-volume work directory
when a local receipt is needed; it is no canonical authority-file publication.

This mode selects current context only. The composed command below now binds
its input/author review and conservative input influence projection. Native
predeclarations, canonical reference execution and full policy/status integration
remain pending. The producer review covers the module population and selected
loaders; source review after an edit remains a separate engineering obligation.
No selected context grants capture or qualification credit.

## Reviewing the authority loader within the producer route

The producer review also calls `capture_div.review_authorities()` through its
public API. An independently written thirteen-path set must match the owner's
declaration before delegation. The review traces ordinary `Path.open` calls,
refuses unknown paths before opening them, rejects write modes and prevents
`subprocess.Popen` within this selected call. It checks the complete observed
view population and the returned frozen fact types, roles, byte sizes and digests
against its preloaded snapshots. The selected property authority must still equal
the reviewed DIV case. A changed declaration, unknown read, contradictory fact or
process attempt refuses; success remains `pending` with both credit flags false.

These are scoped observations of reviewed Python, not an operating-system sandbox
or proof about arbitrary I/O. The outer diagnostic retains its original 1 MiB
member and 8 MiB shared pass, with two passes totaling at most 16 MiB of direct
reads. The nested public authority loader retains its separate 16 MiB direct
snapshot contract and separate schema/catalogue/scope I/O. Runtime import I/O is
also separate. Neither contract promises a combined process-I/O or RAM cap.

The report now derives 37 project modules, 27 execution-data files, 13 current
view files and 39 unique data/view paths. `schema/references.sexp` belongs to both
sets. Including the guest, retained excerpt and policy, the review snapshots
79 unique files. The proposed flat execution children remain exactly 64: the
current requirements, source/parent catalogues and registry are observed authority
views, not additional flat capture inputs. Their whole-file hashes stay diagnostic
provenance. Relevant semantic/schema influence must be carried by the separately
reviewed current/old impact projection, avoiding derived-status cycles.

Run the complete current route and controls:

```bash
set -euo pipefail
python3 scripts/review_div_capture.py --review | python3 -c 'import json,sys; r=json.load(sys.stdin); c=r["counts"]; print(r["disposition"], c["modules"], c["data_files"], c["authority_files"], c["all_data_files"], c["children"], c["reviewed_files"]); print(r["canonical_capture"], r["qualification"])'
python3 scripts/probe_div_capture_review.py
python3 -O scripts/probe_div_capture_review.py
```

The report prints `pending 37 27 13 39 64 79`, then `False False`. Each probe
reports 31 tests with zero failures and errors. The five authority guard omissions
(declaration, pre-open namespace, read-only mode, returned view pin and process)
each lose one assertion with zero errors in both modes; existing thirteen guard
omissions retain their measured losses. PROFILE-CONSISTENCY registers all outcomes.
A copied 79-file runtime gives the same file facts and populations in both modes,
with the valid parent checkout available as its working directory and no copied
binary or `.materials` directory. It writes no canonical output. The composed
entrypoint, predeclarations and [canonical observations](canonical-division.md)
are now retained; full policy/status evaluation remains pending.

## The composed DIV command

`capture_div.prepare_capture()` now composes the finite v2 case from the current
validated authorities and independently reviewed producer/data population. It
returns frozen `CaptureDeclaration` facts. It launches no reference process and
writes no artifact. `--declare` prints three native S-expression documents as
strings in one JSON envelope; it does not create their files:

```bash
set -euo pipefail
python3 scripts/capture_div.py --declare | python3 -c 'import json,sys; r=json.load(sys.stdin); print(r["disposition"], len(r["files"]), r["qualification"]); print(all(0 < len(p.encode()) <= 65536 for p in r["files"].values()))'
```

The output is `pending 3 False`, then `True`. The JSON envelope transports text;
S-expression remains the declaration format. The three fixed names under
`evidence/rv64gc-signed-div-truncation-v2/` are:

| Document | Meaning |
| --- | --- |
| `planned-experiment.sexp` | Nine principals,27 boundaries, three runs, twelve fresh output targets, the typed boundary2/x7 witness and the single wrong quotient. Zero output hashes/sizes and zero exits are explicitly unmeasured placeholders. Collection replaces them with actual metadata. Baseline/repeat AGREE and control DIVERGE are targets to test. |
| `dependencies.sexp` | Exactly64 flat children from the independently enumerated source/data review, with current file pins. The retained normative input keeps its public ID. The snapshot expected author has the sole `expected-author` role. |
| `authorities.sexp` | A native declaration of selected reference/property identities, the separate73-input inventory, expected-author route and conservative influence choice. It is checked for exact generated bytes before capture; it is not another authority loader. |

The input review is constructed from the separately selected nine principals and
64 reviewed children before manifest consumption. Matching a manifest against a
copy of its own input list would supply no independent coverage check. The public
input/author owners freeze this inventory and select `snapshot-parcels-v1`.
The public impact owner projects each reviewed input's full metadata and checks
a conservative edge from the planned evidence to every input. Initial old/new
projections are equal because no earlier canonical capture is claimed. This is a
reviewed finite input-influence projection, not the complete source/risk/feature
policy or an automatic general dependency analysis.

Whole changing catalogue/view hashes stay outside execution inputs and the native
authority declaration. Preparation compares its independently read current-view
facts with the producer review's view facts to reject between-review drift.
Later derived status/prose changes can change those diagnostic hashes without
changing the selected semantic authority. The retained execution descriptor must
match the current selected binary identity; no executable is needed to declare.
The prepared image pin must match the public image reconstruction.

Direct producer/authority reviews retain their separate snapshot bounds and
canonical-tool I/O contracts. Five curated principals are additionally read twice
through the anchored reader at64KiB each: at most640KiB, outside the later combined
artifact allowance. Capture also reads at most three64KiB native declarations.
These bounds neither combine all tool I/O into one budget nor promise atomic
views or total process RAM. The runtime must remain trusted and quiescent.

The pure declarations can be inspected without acquired materials or a binary:

```bash
PYTHONPATH=scripts python3 - <<'PY_DIV_COMMAND'
from capture_div import prepare_capture, declaration_files, F, PREFIX, Impact, PROFILE, P

d = prepare_capture()
manifest = F.parse_dependencies(d.dependencies, path=PREFIX + "/dependencies.sexp")
context = Impact.freeze_review(d.impact, profile_id=PROFILE, experiment_id=P.CASE_ID)
print(len(manifest["input"]), len(d.inventory.inputs), d.author.route)
print(Impact.check_inputs(context, d.inventory.inputs, d.inventory.inputs).disposition)
print(len(declaration_files(d)), all(len(payload) <= 65536 for _, payload in declaration_files(d)))
PY_DIV_COMMAND
```

It prints `64 73 snapshot-parcels-v1`, `matched`, then `3 True`.

The three emitted documents are now retained at those exact native paths; commit
them with the reviewed entrypoint before a canonical run. `capture_div.capture()` and CLI
`--capture` regenerate the current declaration and authenticate every native
predeclaration against its exact expected bytes before delegating collection.
The operator owns the committed-predeclaration workflow; the command does not
launch Git to attest it. Missing declarations report unavailable; changed, unsafe
or oversized declarations refuse before the combined helper can run.

Execution delegates the existing `capture_and_evaluate` with current scope,
selected candidate, separate input/author/impact reviews and property authority.
It grants exactly one128MiB combined artifact-read allowance; the evaluator's
16MiB snapshot ceiling stays fixed. The helper exclusively creates the twelve
observation files and rejects output reuse. Failed/partial historical outputs are
preserved without retry. The returned measured record and independent findings
remain pending complete policy; the caller must retain them under the declared
result names. CLI stdout is a JSON receipt with optional measured S-expression,
not an automatic result-file publisher. It returns0 for pending,2 for unavailable
and1 for other terminal findings. Unexpected programming exceptions propagate.

The package-copy controls use84 tracked runtime/data/principal files, keep the
valid parent checkout available as cwd and have no Git or acquired cache. The
end-to-end fixture installs its own explicitly synthetic executable, changes its
owned parent/descriptor pins and imports the copied code fresh. Three fresh
processes, actual retained authentication, all27 source expectations, exact repeat,
wrong quotient and the separate review findings are exercised together. A repeat
call preserves outputs and refuses. The executable is then removed and the public
retained evaluator still returns pending. A synthetic exit7 leaves its real
baseline receipt and stops before repeat. None of this is a Sail observation.

Run the complete synthetic controls from the repository root:

```bash
python3 scripts/probe_div_command.py
python3 -O scripts/probe_div_command.py
```

Each mode runs19 tests with zero failures/errors, including actual native-file
currentness and process-free retained-capture evaluation. Controls cover missing/changed
native documents, prepared pins/sizes/links/Git boundaries, selected identity,
authority drift, raw-schema-before-mapping, immutable facts, output reuse,
failed-process preservation and CLI exit status. Injected assertion failures also
prove declaration subcases clean their fixtures before the next case. Guard
omissions independently exercise declaration reads, authority stability, retained
identity, raw schema and author/impact/property delegation. Their failure counts
are registered in PROFILE-CONSISTENCY after being measured in both modes.

## Retained native predeclarations

P4-SYSTEM.14 a42al retains the exact three documents under
`evidence/rv64gc-signed-div-truncation-v2/`. Each fits its64KiB bound; the command
below derives the current byte sizes from the complete retained payloads. The
evidence family now has22 files after the [canonical capture](canonical-division.md),
within its22-file/16MiB envelope. That chapter reports the measured findings.

Verify the complete current native bytes without a binary or reference process:

```bash
PYTHONPATH=scripts python3 - <<'PY_DIV_DECLARATION'
import hashlib
from capture_div import prepare_capture, declaration_files, PREFIX, ROOT
from experiment_artifacts import read_snapshot

d = prepare_capture()
for name, payload in declaration_files(d):
    record = dict(id=name, role="declaration", path=PREFIX + "/" + name,
                  sha256=hashlib.sha256(payload).hexdigest())
    snapshot = read_snapshot(ROOT, "input", record, max_bytes=65536)
    if snapshot.pin.disposition != "matched" or snapshot.data != payload:
        raise ValueError("native declaration differs: " + name)
    print(name, len(snapshot.data), snapshot.data == payload)
PY_DIV_DECLARATION
```

It prints all three names with their measured byte sizes and `True`. The command controls
perform this actual-package comparison in both Python modes; changing producer
code or a selected input makes stale declarations fail even before a Sail run.
After observations exist, preserve their original declarations; an affected
change needs a separately owned capture/revalidation workflow.
The emitted JSON remains transport; these retained documents remain native
S-expression. Planned output hashes/sizes/exits are unmeasured placeholders and
AGREE/DIVERGE values remain claims to test.

An87-file runtime copy also verifies the exact published declarations with no
Git, acquired cache or executable. Its final collector is explicitly replaced by
a recording delegate: no reference process runs. Six missing/changed native-file
variants stop before that delegate. Derived requirement-status or unrelated
parent-prose edits change current view hashes while preserving declaration bytes
and the selected semantic identity; the status-output cycle stays excluded.
The actual baseline/repeat/control results are [retained](canonical-division.md);
full policy remains next.

### The m-forms declaration (a42au)

`scripts/capture_div.py --declare --case rv64gc-m-forms-v3` emits the three native declarations of
the second reviewed case from the same producers: `planned-experiment.sexp` (16,915 B: 25
properties, the control naming `form-div`, 33 boundaries, twelve zero-placeholder
observations), `dependencies.sexp` (14,488 B: the same 64 children) and `authorities.sexp`
(17,043 B). They are retained under `evidence/rv64gc-m-forms-v3/` beside the four prepared inputs,
and the command regenerates them byte for byte from the current tree. The `--case` selector
reaches any reviewed case with pinned prepared inputs; without it the command prepares the
retained case, so the method review, the command probe and the method probe are unchanged. The
capture review takes the same selector (`scripts/review_div_capture.py --review --case <id>`) and
exercises the loaders over that case's guest. A declared case without a receipt is reported
`declared` by `scripts/requirement_status.py` and credits nothing; the capture is the next unit.
