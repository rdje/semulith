# References and comparison limits

The generated [reference table](materials.md#reference-candidates) identifies each
candidate and its recorded matching scope. `references.sexp` is canonical;
`reference/sail-rv64gc-lab-v0.override.sexp` declares the public configuration.
Adapters and author scripts are tracked project tools. Dependency interaction uses
published configuration, builds, APIs and outputs; source access grants no license
to infer a submodule's internal implementation or ancestry.

## What the earlier comparisons mean

Earlier privilege, Sv39, atomic, interrupt/wake, FENCE.I, FP, fault, M and C runs
are historical finite observations. They name agreement, architectural latitude
and platform differences separately. The live adapter compares declared GPR changes
and witnessed delivery gaps. It does not infer complete PC, instruction-word, FP,
memory, CSR or request equality from the same text output.

For example, the compressed timer guest differs at the boundary where the
laboratory delivers STI and the matched reference proceeds with C.ADDI. Public
configuration and fresh public traces identify an unmatched timer source.
That result is not a compressed arithmetic defect and is not acceptance for
Sstc timing. Likewise disabled reference Zicntr and absent injected physical
refusal regions leave those observations unmatched.

A deliberately wrong C.LI result must diverge through a fresh reference run.
An adapter that accepts a failed producer, stale trace or changed expected value
is itself a defect, even if the reference program normally succeeds. Controls
must exercise the actual execution/comparison path and then prove restoration.

## Independence has a denominator too

No current claim authenticates Sail/Spike implementation ancestry. Agreement is
useful on named inputs, but it does not establish independent numeric derivation.
The spec-side author and engine can share opcode tables or arithmetic producers;
record those common inputs and do not count two wrappers as two methods.

For an FP requirement, a source-derived exact arithmetic fixture can provide a
second method when its producer and scope are explicit. A Sail GPR-only trace
cannot by itself qualify FP result bits/flags. For translation, a separately
specified request-path expectation can expose a walk or fault-order defect that
a final handler register masks. The policy requires methods to address the same
property, with their controls and limitations recorded.

## Artifact syntax you can inspect

Two prospective artifact documents now have schemas and one mapping owner,
`scripts/dossier_sexp.py`. `schema/matched-gpr-dependencies.sexp` describes a
`dependencies` root with version `matched-gpr-dependencies-v1` and 1–64 `input`
children. Each input has `id`, `role`, canonical repository-relative `path` and
lowercase 64-hex `sha256`. IDs and paths are unique. The document cannot name
itself or declare a child with role `dependency-manifest`. Detecting manifest
content hidden behind another role and authenticating the complete closure still
belong to the forthcoming evaluator.

For example, this is valid **syntax with a dummy pin**, not a verified file:

```lisp
(dependencies (format_version "matched-gpr-dependencies-v1")
  (input (id "mapper") (role "mapping") (path "scripts/dossier_sexp.py")
    (sha256 "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")))
```

`schema/sail-gpr-capture.sexp` describes a `capture` root with version
`sail-gpr-capture-v1`. It records the following data:

| Field/child | Content |
| --- | --- |
| `run_id`, `run_kind` | Run identity and `baseline`, `repeat` or `control` |
| Repeated `argv`, integer `process_exit` | Exact argument order, including repeated/empty arguments; actual process result |
| `reference_candidate_id`, `reference_binary_sha256`, `collector_input_id` | Recorded executable identity and the collector's input identity |
| Repeated `input` | Unique `id` and exact SHA256; collector ID must occur in this inventory |
| Three `observation` children | Unique `id`/`path`, nonnegative `byte_size`, SHA256; exactly one each of `raw-gpr`, `process-stdout`, `process-stderr` |
| `host`, repeated `tool` | Nonempty host `os`/`kernel`/`arch`; unique tool `id` with nonempty `version` |

The receipt never contains its own hash or names itself as an output. Empty output
files and nonzero or signal exits are valid recorded data; they do not meet the
method's success requirements. Versions and provenance are recorded observations,
not attestation that a process executed. The bounded receipt-binding check below
now matches selected run/argv/input/output/candidate fields; complete graph and
method evaluation remain separate obligations.

From the repository root, these commands print complete illustrative documents to
stdout and run the controls. They create no capture and their dummy pins do not
authenticate anything:

```bash
python3 scripts/probe_matched_gpr_artifacts.py --emit dependencies
python3 scripts/probe_matched_gpr_artifacts.py --emit capture
python3 scripts/probe_matched_gpr_artifacts.py
python3 -O scripts/probe_matched_gpr_artifacts.py
bash scripts/check_dossier_schema.sh --self-test
```

The public `parse_dependencies(payload, path=...)` and `parse_capture(payload,
path=...)` in `scripts/matched_gpr_artifacts.py` accept immutable bytes plus the
artifact's canonical relative location. Each refuses more than 64 KiB **before**
decoding/parsing, malformed UTF-8, extra/missing roots, unknown fields, duplicate
singulars and invalid types/facets. They validate raw shape before dictionary
mapping, then check the identities above. They never open an artifact or launch
a process; future consumers must pass bytes from the anchored authenticated
snapshot reader. Parsing does not authenticate a pin. Schema files themselves
are read as project tools. These are payload limits, not total process RAM caps.
The convenience encoders refuse unknown keys, lossy mappings and oversized
serialized documents; rendering a caller-owned dictionary has no separate RAM
budget guarantee.

DOSSIER-SCHEMA runs these offline controls before its existing tracked dossier
sweep. That sweep covers `profiles/*/*.sexp`; it does not yet sweep a prospective
nested capture store. No such store or canonical v1 capture exists. The future
retention/capture slice must explicitly connect its files to evaluation and gates.

## Retained method checks

The [retained Sail method chapter](retained-method.md) contains the complete
identity, receipt and invocation examples, plus witness/control/derivation/pair
bindings. Their frozen results bind declarations and selected files separately;
complete authenticated method evaluation and policy qualification remain pending.

## What comes next

A27 repairs the terminal-newline defect found at a26: all project exact-token
facets now use strict end anchors. For example a 64-hex SHA256 followed by a newline,
`"AGREE\n"`, `"baseline\n"` or `"x31\n"` refuses schema validation, rather than
becoming a subtly different identity/verdict. Generic `pattern "needle"` still
accepts `"hayneedlehay"`; the schema kernel deliberately implements substring
search, so exactness belongs to the declared token pattern. The repair changes
83 declarations in 13 schemas; all 91 patterned fields have positive and boundary
controls, including five complete canonical-document regressions. Run:

```bash
python3 scripts/probe_schema_token_facets.py
python3 -O scripts/probe_schema_token_facets.py
bash scripts/check_requirements.sh --self-test
```

These offline controls preserve all canonical document bytes. They prove grammar
behavior, not file authenticity, producer execution or evidence qualification.

Historical comparisons remain prose in the canonical dossier. Optional structured
graphs, typed witnesses/baselines, bounded pin/snapshot readers and these artifact
formats and a [bounded byte comparison](evidence.md#bounded-three-run-byte-comparison)
and retained reference-identity authentication, [receipt binding](retained-method.md#authenticating-and-binding-a-process-receipt)
and [execution binding](retained-method.md#binding-the-declared-sail-invocations) exist; complete method evaluation,
reviewed fresh collection, measured
retention and canonical captures are still pending. PROFILE-CONSISTENCY continues
to refuse v1 blocks as unqualified. The [policy](policy.md) was declared after
implementation and is prospective; this book does not backdate it. Candidate
availability, a successful book build and syntax checks do not advance requirement
status or close G-TRACE. Full policy/status consumers follow verified captures.
