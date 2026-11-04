# Checking the retained finite method

The retained matched cases have a read-only method consumer. It composes the
existing declaration, source review and authenticated evaluation owners, then
checks the supplied findings against the independently selected finite method.
It reads every case it holds a reviewed capture for: the M case's
`rv64gc-m-forms-v4` (the default; v3 from a42ax and the first case,
`rv64gc-signed-div-truncation-v2`, from a42ao, are `invalidated` history) and,
since a43a-2f (2026-10-29), the XLEN case `rv64gc-xlen-forms-v1`. For each the
method result is `satisfied`, full policy is `pending` as the method sees it (the
[policy legs](policy-adequacy.md) measure all ten satisfied), and replay is
`not-checked`. The M case is thirteen M forms and twelve Table 1 cells under one
program, with the −7/2 rounding witness's wrong quotient as the control; the XLEN
case is seventeen witnesses of the 64-bit registers, the `*W` family and the
64-bit address space, with a 32-bit-truncated address as the control. The method
result credits nothing and establishes no CPU acceptance or reference independence.

## The selected authority and capture

`scripts/review_div_method.py` owns the case selection: one `RETAINED_CAPTURES` row per
reviewed capture, and a case without a row is `unsupported` before any read. The pure composition
in `scripts/matched_gpr_adequacy.py` opens no artifact and launches no process;
the existing schema tools retain their own I/O. Neither a stored qualified flag
nor `verification.json` supplies a verdict or method authority to this consumer.

The consumer selects each case's measured record by its reviewed identity:

| Case | Measured record | Declared in | Captured in |
| --- | --- | --- | --- |
| `rv64gc-m-forms-v4` | 16,942 B, `aadb5ef3…` | `177b43a1` (a44-3) | `3c464095` (a44-4) |
| `rv64gc-xlen-forms-v1` | 14,958 B, `d39825b0…` | `5c2cde93` (a43a-2d) | `e32cc645` (a43a-2e) |

v3's row was 16,942 B `fb22d5e5…`, declared in `4af5a68b` and retained in `e775705e`. Those labels
are historical review facts, not a runtime Git check or independent execution attestation. The review
trusts the tracked collector and the committed procedure that produced the
historical processes. Unknown/shared ancestry earns no independence credit. The
pointers live in `scripts/review_div_method.py`, which no case pins, so adding a row for a
new capture invalidates nothing (`decision_caller-names-the-case.md`,
`decision_reviews-read-every-retained-case.md`); the
first case's pointers were the 9,928-byte record `2cb6c704…`, commits `b160c66…` /
`c91d08f…`.

The three native declarations must equal the current public generator's output.
To bind the measured native graph to its predeclaration, the checker restores
only the twelve observation sizes/digests and the three run exit fields to their
planned values. Every other parsed field, structured comment, ordering choice,
property statement and control reason must remain equal. That binding alone
does not turn a failed process into success; the evaluated receipts and run
findings must separately establish zero exits and the required comparisons.

The reviewed influence graph selects the experiment's evidence node with the
SHA256 of the planned native document and no file path. The measured record has
its separate actual digest. Checking both identities connects this capture to
the selected evidence; input reachability alone would leave that connection
unproved. The independent inventory covers nine principals and the manifest's
children (64 for the two retained captures; 67 for a case reviewed since `P4-SYSTEM.14`
a44-2b). All selected input identities (73; 76) must agree with the declaration.

## Computed findings and failure behavior

The consumer requires a plain typed result from each public owner: valid scoped
record, matching manifest, selected reference, input inventory, expected author,
influence projection, image/source correspondence, all source values, finite
source property, three receipts and the complete baseline/repeat/control result.
It checks the authenticated identities of all 73 inputs and twelve observations,
and refuses a summary that retains payload data or substitutes another manifest.
Baseline/repeat must agree and the declared wrong quotient must diverge.

Missing findings remain pending. Failed, stale, unavailable, refused and
unsupported findings retain their distinct meanings. A case declared before
`P4-SYSTEM.14` a43b-2b names no control id or statement, so the producer refuses to
prepare it; the review then reads the capture's own dependency manifest through the
measured record's pin and re-checks the pins of the declaration's route (the case
file, then its schema): the first that moved makes the method `stale`, naming it —
v4 and xlen-v1 read `stale: schema/matched-case.sexp: SHA256 differs` from 2026-11-02
until their re-captures took the rows (a43b-2e: the rows now name v5 and xlen-v2, and since a43b-3g the
CSR-SET case, each `satisfied` over 88 authenticated files) — and a refusal with nothing moved stays `refused`. A later checker-source
change refuses the method result while preserving earlier computed record,
binding and evaluation findings. No result silently becomes policy credit.

The existing evaluator still returns `pending`: it does not own this additional
finite-method review or complete policy qualification. A satisfied composition
therefore coexists with `valid` record, `matched` capture binding and `pending`
evaluation. Complete source/risk/feature policy and status integration remain
separate work under `P4-SYSTEM.14`; PROFILE-CONSISTENCY still refuses qualification.

## Bounds and source checks

One inclusive 134,217,728-byte artifact-read allowance covers the three native
declarations, measured record and delegated retained evaluation. Every public
read receives only the remaining allowance. A failed read retains its full
reservation; a completed authenticated result refunds only unused allowance.
Malformed, boolean, negative, excessive or underreported receipts are refused.

| Quantity for this retained check | Bytes |
| --- | ---: |
| Three native declarations | 41,514 |
| Measured native record | 9,928 |
| Retained evaluator charge, including manifest seed | 1,048,756 |
| Total artifact-read charge | 1,100,198 |
| Evaluator retained snapshots | 33,759 |

The evaluator authenticates 85 files and releases payloads from the returned
summary. Its 16 MiB snapshot ceiling is separate from the read allowance. This
offline check's charge differs from the historical collection/evaluation charge
of 24,337,600 bytes: no executable is read and no reference is launched here.

The producer's reviewed import population is 38 modules (37 before a44-2b added the
declaration reader). The checker reaches 37 of them — not the excerpt extractor, which
no checker code imports since a44-2c bound excerpts to the case's own authority — and
adds two modules outside that population, for 39 checked modules (39, then 40, before). Their
current bytes are read under the existing 1 MiB member/8 MiB pass contract and
rechecked before returning source identities. Existing producer/authority
preparation retains its separate limits, including the five curated principal
reads and rechecks within 640 KiB; schema/tool/runtime I/O stays separate.
These bounds do not assert peak RAM, loaded-code attestation or an atomic view
of all files. Neither Git, acquired materials nor a reference binary is needed.

## Run the read-only consumer

Run from the repository root:

```bash
PYTHONPATH=scripts python3 -B - <<'PY_METHOD'
from review_div_method import review_method
for case in ("rv64gc-m-forms-v4", "rv64gc-xlen-forms-v1"):
    r = review_method(case_id=case)
    print(r.disposition, r.policy_disposition, r.replay_disposition, "|",
          r.record_disposition, r.capture_binding, r.evaluation_disposition, "|",
          r.authenticated_files, r.authenticated_bytes, r.snapshot_bytes, "|",
          r.charged_read_bytes, r.read_limit, len(r.checker_sources))
PY_METHOD
```

The output is `satisfied pending not-checked | valid matched pending | 88 1098379 40438 |
1165123 134217728 39` for v4, the same with `88 1092798 35100 | 1155615` for the XLEN case, and
`88 1228197 141763 | 1315764` for the CSR-SET case, whose 157 steps make the larger snapshot.

```bash
python3 -B scripts/review_div_method.py
python3 -B scripts/review_div_method.py --max-read-bytes 1165123
python3 -B scripts/review_div_method.py --case rv64gc-xlen-forms-v1 --max-read-bytes 1155615
```

All emit derived JSON within 64 KiB and exit zero. One byte less (1,165,122; 1,155,614)
cannot satisfy the method (`refused files: artifact exceeds snapshot byte limit`,
exit 1). Exit 2 means unavailable or unsupported; exit 1 means
another unsatisfied disposition. These commands neither write historical
artifacts nor repeat canonical execution. Preserve the original capture names.

## Controls that distinguish the safeguards

```bash
python3 -B scripts/probe_div_method.py
python3 -B -O scripts/probe_div_method.py
python3 -B scripts/probe_div_method.py --mutation capture-origin
```

Each unmutated mode passes 22 tests; the real-tree arm runs every row and requires a
retained case without one (v3) to be `unsupported` having read nothing, and predicts each
stale row's reason and charged bytes from its own manifest. A synthetic arm strips the
control from a copy's declaration and expects `stale` naming the case file; a refusal
with nothing moved stays `refused`. The targeted origin omission runs one test
and reports one failure with no errors; that nonzero exit is the expected
negative control. PROFILE-CONSISTENCY runs both modes and all fifteen targeted
guard omissions, the last `stale-route` (a43b-2b). Their failure counts are respectively
4/1/4/2/2/1/2/1/3/4/1/1/1/1/1, with no errors.

A 106-file runtime copy (the default case's) contains only the retained package and required code,
without Git, acquired materials or a binary. Child process launching is denied;
the valid parent checkout remains available as cwd to expose accidental borrowing.
Controls cover missing/changed native declarations and traces, exact/short read
limits, malformed accounting, unreviewed imports and late checker-source drift.

One deliberately forged copy changes stdout and consistently updates its receipt
and measured digests. Lower byte evaluation still binds that self-consistent
copy; it cannot establish actual process provenance. The consumer rejects it
because it differs from the selected reviewed historical record. All forged
bytes and omitted guards exist only in disposable on-volume fixtures. The real
capture, its declarations and original producer inputs remain byte-exact.
