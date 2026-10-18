# Predeclaring the first division capture

The proposed first canonical case is `rv64gc-signed-div-truncation-v1`, owned by
`scripts/matched_gpr_property.py`. It runs `m-div.s` for27 boundaries. The finite
claim is the x7 change at boundary2: signed `-7 / 2` produces `-3`. The negative
control changes only that expected value to `-4`. Baseline, repeat and control
must use three fresh reference processes with identical executed inputs. This
does not accept all M instructions or close `REQ-GC-M`/`OB-GC-M`.

## Review the producers before declaring their inputs

`scripts/review_div_capture.py --review` reports the current reviewed population
as JSON on stdout. Redirect it into an owned directory under `target/` when a
local receipt is useful. It launches no reference process and writes no files.

The source review starts at the unit collector, retained evaluator and expected
author. It conservatively follows every ordinary project-local Python import,
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
repository paths, and before/after byte checks. The pinned guest and normative
M page must match the reviewed case. An absent primary page reports unavailable,
never success. The report includes file sizes/digests, import edges, exercised
data paths and runtime identity. A successful review remains `pending`; it
supplies neither an experiment manifest nor qualification.

## Proposed flat input population

The collector and public Sail adapter are two of the existing nine principals.
The proposed dependency children are the other32 imported project modules,
27 exercised data files, the normative M page, the profile evidence policy and
the review tool itself:62 children before a future capture entrypoint is added.
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

This curation slice does not replace the property case's existing full-page
input. That binding and its controls must change explicitly in the next slice,
preserving the original publication digest as current semantic authority and
using the excerpt's separate digest as a retained artifact input. Extend the
reviewed producer population with the extraction tool before adopting it: the
proposed child population then grows from62 to63, leaving one slot for the final
entrypoint. The diagnostic's current cache-bound case still reports62.

The asset belongs to the existing registered `profiles/` family; its measured
addition must fit that family's unchanged count, aggregate and member caps.
Final capture outputs still require their own measured retention declaration.

### Complete the capture declaration

Before any canonical run, commit the final entrypoint and exact manifest,
property/author/impact authorities, output namespace and retention family. The
retained file set must support repeatable offline evaluation without relying on
an acquired reference cache. Resolve the normative page's retained location and
binding explicitly. The binary remains a separately pinned replay dependency;
offline observation checking and reference replay have different availability.

Measure and register the actual retained family with its fixed count/byte caps.
Keep the existing128 MiB aggregate read and16 MiB snapshot envelopes; a combined
collector/evaluator must carry the collection charge forward. Then capture the
three processes, authenticate every retained input/output and evaluate all27
boundaries, exact repeat bytes and the intended control. Only after that may the
full source/risk/feature policy and derived statuses be integrated. The blanket
qualification refusal remains in force throughout this predeclaration slice.

Run the synthetic diagnostic controls without any acquired material:

```bash
python3 scripts/probe_div_capture_review.py
python3 -O scripts/probe_div_capture_review.py
```

Run the current population review with the already acquired pinned M page:

```bash
python3 scripts/review_div_capture.py --review
```

Its changing digests and byte totals are derived output, not constants to copy
into this chapter. A missing primary source exits2; a refused review exits1;
`pending` exits0 and still grants no canonical capture or method credit.
