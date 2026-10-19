# Predeclaring the first division capture

The proposed first canonical case is `rv64gc-signed-div-truncation-v2`, owned by
`scripts/matched_gpr_property.py`. It runs `m-div.s` for27 boundaries. The finite
claim is the x7 change at boundary2: signed `-7 / 2` produces `-3`. The negative
control changes only that expected value to `-4`. Baseline, repeat and control
must use three fresh reference processes with identical executed inputs. This
does not accept all M instructions or close `REQ-GC-M`/`OB-GC-M`.

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
the final entrypoint, exact manifest and authorities remain pending. The
retained file set must support repeatable offline evaluation without relying on
an acquired reference cache. The retained excerpt supplies the normative input;
its original publication remains separate current authority. The binary remains a separately pinned replay dependency;
offline observation checking and reference replay have different availability.

Measure and register the actual retained family with its fixed count/byte caps.
Keep the existing128 MiB aggregate read and16 MiB snapshot envelopes; a combined
collector/evaluator must carry the collection charge forward. Evaluation now
accepts a [delegated remainder](read-allowance.md), including its manifest seed;
the [combined unit helper](unit-evaluation.md) now carries that allowance and
validates seed-inclusive accounting. The canonical entrypoint remains to be
finalized. Then capture the
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
execution or publication flag. No binary, acquired page, retained trace or guest
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

This selects current context only. The final capture entrypoint, exact manifest,
independent input/author review and old/current impact projection remain pending,
as do reference execution, retained evaluation and full policy/status integration.
The producer review now covers this read-only entrypoint and its current-view
loader. The future execution composition still requires source review before its
manifest is committed. No selected context grants capture or qualification credit.

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
binary or `.materials` directory. It writes no canonical output. Final execution
composition, exact manifest/planned record, independent inventory/author/impact
reviews, three fresh captures and full policy/status evaluation remain pending.
