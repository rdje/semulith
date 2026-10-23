# Checking the retained finite method

The retained DIV case has a read-only method consumer. It composes the
existing declaration, source review and authenticated evaluation owners, then
checks the supplied findings against the independently selected finite method.
For the retained case — `rv64gc-m-forms-v3` since a42ax (2026-10-23); the first case,
`rv64gc-signed-div-truncation-v2`, was the retained case from a42ao to a42aw and is
`invalidated` history — the method result is `satisfied`, full policy is `pending`
as the method sees it (the [policy legs](policy-adequacy.md) measure all ten
satisfied), and replay is `not-checked`. This is thirteen M forms and twelve Table 1
cells under one program, with the −7/2 rounding witness's wrong quotient as the
control. It does not qualify the profile, credit `REQ-GC-M` or `OB-GC-M`, or
establish CPU acceptance or reference independence.

## The selected authority and capture

`scripts/review_div_method.py` owns the fixed case selection. The pure composition
in `scripts/matched_gpr_adequacy.py` opens no artifact and launches no process;
the existing schema tools retain their own I/O. Neither a stored qualified flag
nor `verification.json` supplies a verdict or method authority to this consumer.

The consumer selects the measured record by its reviewed 16,942-byte identity
and SHA256
`fb22d5e5554a0e132c231e5551ed8314ab4be35ff93e7f086fceeacb6235a152`.
Source and predeclarations were committed in
`4af5a68bbec9f1bf0922ec3787f829e029c15f29`; capture was retained in
`e775705e2cebbafabe05f0458da8d52004d604cb`. Those labels are historical review
facts, not a runtime Git check or independent execution attestation. The review
trusts the tracked collector and the committed procedure that produced the
historical processes. Unknown/shared ancestry earns no independence credit. The
pointers live in `scripts/review_div_method.py`, which no case pins, so moving them
to a new capture invalidates nothing (`decision_caller-names-the-case.md`); the
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
unproved. The independent inventory covers nine principals and 64 manifest
children. All 73 selected input identities must agree with the declaration.

## Computed findings and failure behavior

The consumer requires a plain typed result from each public owner: valid scoped
record, matching manifest, selected reference, input inventory, expected author,
influence projection, image/source correspondence, all source values, finite
source property, three receipts and the complete baseline/repeat/control result.
It checks the authenticated identities of all 73 inputs and twelve observations,
and refuses a summary that retains payload data or substitutes another manifest.
Baseline/repeat must agree and the declared wrong quotient must diverge.

Missing findings remain pending. Failed, stale, unavailable, refused and
unsupported findings retain their distinct meanings. A later checker-source
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

The producer's reviewed import population remains 37 modules. The new consumer
adds two modules outside that producer population, for 39 checked modules. Their
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
r = review_method()
print(r.disposition, r.policy_disposition, r.replay_disposition)
print(r.record_disposition, r.capture_binding, r.evaluation_disposition)
print(r.authenticated_files, r.authenticated_bytes, r.snapshot_bytes)
print(r.charged_read_bytes, r.read_limit, len(r.checker_sources))
PY_METHOD
```

The output is `satisfied pending not-checked`, `valid matched pending`,
`85 1076834 40438`, then `1142222 134217728 39`.

```bash
python3 -B scripts/review_div_method.py
python3 -B scripts/review_div_method.py --max-read-bytes 1142222
```

Both emit derived JSON within 64 KiB and exit zero. An allowance of 1,142,221
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

Each unmutated mode passes 20 tests. The targeted origin omission runs one test
and reports one failure with no errors; that nonzero exit is the expected
negative control. PROFILE-CONSISTENCY runs both modes and all fourteen targeted
guard omissions. Their failure counts are respectively
4/1/4/2/2/1/2/1/3/4/1/1/1/1, with no errors.

A 103-file runtime copy contains only the retained package and required code,
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
