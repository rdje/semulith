# The first retained canonical division capture

Most versioned cases this page names have since left the tree. Each is listed with its last commit in [Cases retired from the tree](retired-cases.md); the tables here stay as what was measured.

On 2026-10-19, `P4-SYSTEM.14` a42am collected the predeclared
`rv64gc-signed-div-truncation-v2` case. Three fresh executions of the selected
public Sail executable exited zero. Baseline and repeat agreed across all 27
boundaries. The wrong-quotient control diverged exactly at boundary 2, x7.
These are retained finite observations; complete method/policy qualification and
CPU acceptance remain pending. They do not validate every M instruction.

## What was committed before execution

Commit `b160c66e183dee267ebf12edf25066412fe96ff6` contains the reviewed entrypoint,
three exact native predeclarations and prepared inputs. The [capture plan](capture-plan.md)
explains their separate execution, source, semantic and review identities.
The preflight checked every selected input against that committed state and
verified the pinned executable through the public anchored reader. Its 3,801,664
bytes fit the collector's 8 MiB member bound. No reference implementation source
was inspected.

All twelve output names and both result names were absent before the single
capture invocation. Collection used the existing three-run combined helper,
with one 128 MiB artifact-read allowance, 30 seconds per process and the fixed 16 MiB
evaluator snapshot ceiling. Preparation/schema/runtime I/O remains separately
bounded; these limits make no atomic-view or total process-RAM guarantee.

The observed process IDs were 39909, 39914 and 39918, with zero exits. They identify
these historical executions; they are not current processes or execution
attestation independent of the trusted collector and runtime.

## The finite result

| Run | Computed result | Evidence |
| --- | --- | --- |
| Baseline | AGREE | All 27 declared boundaries and every required GPR change row agree with the source-derived expectations. |
| Repeat | AGREE | Same executed inputs, a fresh process and byte-identical raw trace. |
| Wrong quotient | DIVERGE | Only the boundary 2 x7 expectation differs: actual signed−7/2 is−3; the control expects−4. The raw reference trace remains identical. |

At boundary 2 the instruction is `0x0262c3b3` at `0x80000008`. The observed x7 bits
are `0xfffffffffffffffd`; the control expects `0xfffffffffffffffc`. This is the
reviewed rounding-toward-zero witness, not a complete division or M campaign.
Each raw trace is 2,298 bytes and has SHA256
`64551458d50ec4345b716abd9f2caf4b42053d6f3a8640735ee539d89a968bde`.

The combined conservative artifact-read charge was 24,337,600 bytes. Retained
evaluation authenticated 85 distinct files totaling 1,048,756 bytes and retained
33,759 snapshot bytes before releasing payloads from its returned summary.
The independent reconstruction of the collection charge counts before/after
input pins, the three output-read passes and receipt authentication; it agrees
with the collector counters. A preflight upper projection of 76,590,974 bytes
covered collection plus evaluation within 134,217,728 bytes. These are different
quantities: actual bounded charges, authenticated file bytes, retained payloads
and a conservative projection.

## Retained artifacts and independent findings

All files live under `evidence/rv64gc-signed-div-truncation-v2/`:

| Files | Meaning |
| --- | --- |
| `baseline`, `repeat`, `control`, each with `.trace`, `.stdout`, `.stderr`, `.receipt.sexp` | Twelve actual observations with typed sizes/digests, fresh process metadata and public invocation receipts. |
| `measured-experiment.sexp` | The native predeclared graph with actual observation sizes/hashes and checked zero exits. Every other field and structured comment is preserved. Verdict words remain claims checked against computed comparisons. |
| `verification.json` | A bounded derived receipt: source/declaration commit, measured-record pin, process metadata, comparison details, separate findings and accounting. It explicitly records qualification as false. Pinned `object` fields name repository-root identities; readers map them to the native `path` contract. Re-evaluation uses the native record and bytes rather than trusting this JSON's verdict. |

The family contains all 22 declared files, including its index, four prepared
inputs and three native declarations. Its count/16 MiB aggregate/4 MiB member
ceilings stay fixed. The measured and JSON result documents each fit 64 KiB.
The three original native declarations and all prepared inputs are unchanged.

Record validity, manifest authentication, selected identity, receipt binding,
source/image correspondence, all 27 source values, input inventory, expected
author, input influence projection and the finite source property are separate
findings. They all bind for this capture. The comparison is `satisfied`; the
retained evaluator still returns `pending` complete method/policy adequacy.
Producer-pair ancestry remains unexamined and earns no independence credit.

## Check the retained result without running Sail

This complete example uses the public bounded reader, current authority owners
and retained evaluator. It launches no process and does not require a reference
binary. Run from the repository root:

```bash
PYTHONPATH=scripts python3 - <<'PY_CANONICAL_DIV'
import json
from capture_div import prepare_capture, ROOT, PREFIX, S, Unit
from experiment_artifacts import observe_bounded_file, read_snapshot

path = PREFIX + "/verification.json"
observed = observe_bounded_file(ROOT, path, max_bytes=65536)
if observed.disposition != "observed":
    raise ValueError(observed.reason)
report_bytes = read_snapshot(ROOT, "input", dict(id="verification", path=path,
                             sha256=observed.sha256), max_bytes=65536)
if report_bytes.pin.disposition != "matched":
    raise ValueError(report_bytes.pin.reason)
report = json.loads(report_bytes.data)
retained = report["measured_experiment"]
measured_pin = {**retained, "path": retained["object"]}
measured = read_snapshot(ROOT, "observation", measured_pin, max_bytes=65536)
if measured.pin.disposition != "matched":
    raise ValueError(measured.pin.reason)
raw = next(form for form in S.parse(measured.data.decode()) if form[0] == "experiment")
d = prepare_capture()
checked = Unit.Evaluation.evaluate_retained_unit(
    ROOT, raw_experiment=raw, scope=d.authorities.scope,
    current_candidate=dict(d.authorities.reference.fields),
    reviewed_inputs=d.inventory, author_review=d.author,
    impact_review=d.impact, property_authority=d.authorities.property_authority)
print(checked.disposition, checked.record.disposition, checked.comparison.disposition)
print(*(run.comparison.verdict for run in checked.comparison.runs))
print(checked.input_review.disposition, checked.expected_author.disposition,
      checked.source_property.disposition)
print(report["qualification"])
PY_CANONICAL_DIV
```

It prints `pending valid satisfied`, `AGREE AGREE DIVERGE`,
`matched matched matched`, then `False`. Public raw-schema and scoped checks run
before mapping and authentication in the retained evaluator. The JSON pin can
establish measured-file byte identity, but it cannot by itself establish method
adequacy or actual process provenance.

A 101-file runtime copy gives the same retained findings in normal/optimized
Python with no Git, acquired material directory or executable and with the valid
parent checkout available as cwd. Process launching is denied. Missing traces or
receipts report unavailable; changed trace bytes report stale; duplicate raw
fields refuse before authentication. The command suite's actual-capture check
also runs in both modes through PROFILE-CONSISTENCY:

```bash
python3 scripts/probe_div_command.py
python3 -O scripts/probe_div_command.py
```

Each mode runs 19 tests. The other command controls continue to use explicitly
synthetic processes; these two commands never rerun canonical Sail.

## Preserve history and finish the policy work

Do not rerun `--capture` against these names. Existing observations refuse reuse;
failed or partial data must also remain intact. An affected implementation change
requires separately owned retention/revalidation and a fresh declared capture,
not rewriting old pins or expectations until a comparison passes.

This capture supplies one bounded signed-DIV witness and its negative control.
The full source/risk/feature policy, complete closure and impact adequacy,
qualification/status integration and remaining profile evidence still belong to
`P4-SYSTEM.14`. CPU remains 14/18; this capture does not close `REQ-GC-M`,
`OB-GC-M`, the environment contract or the processor gate.

## The m-forms capture (a42aw)

The second reviewed case, `rv64gc-m-forms-v3`, was captured once on 2026-10-22 by the tracked tool
`scripts/retain_div_capture.py` — the procedure the first capture ran by hand, now with a preflight
(every output and result name absent, the three declarations regenerating byte for byte, the
binary's digest equal to the retained identity, the declaration commit named), one invocation of
`capture_div.capture` with the case named, and the exclusive publication of the two results. The
declaration commit it records is `4af5a68bbec9f1bf0922ec3787f829e029c15f29` (the re-emitted
declarations of a42av); the binary is the pinned Sail 0.14 release, 3,801,664 bytes.

```bash
python3 -B scripts/retain_div_capture.py --case rv64gc-m-forms-v3 \
    --declaration-commit 4af5a68bbec9f1bf0922ec3787f829e029c15f29 --preflight-only
python3 -B scripts/retain_div_capture.py --case rv64gc-m-forms-v3 \
    --declaration-commit 4af5a68bbec9f1bf0922ec3787f829e029c15f29
```

The first command prints `ready` and starts nothing; the second was run exactly once and refuses
ever since (`outputs already exist; a capture is never rerun`). Its receipt and the offline
re-evaluation of the retained bytes agree:

| Run | Computed result | Evidence |
| --- | --- | --- |
| Baseline | AGREE | All 33 declared boundaries and every GPR change row agree with the source-derived expectations; process 33523 exited 0. |
| Repeat | AGREE | Same executed inputs, a fresh process (33562), a byte-identical raw trace. |
| Wrong quotient | DIVERGE | Only boundary 12's x15 differs: `div x15, x5, x6` observed `0xfffffffffffffffd` (−3), the control expects `0xfffffffffffffffc` (−4); process 33599 exited 0, raw trace identical. |

Each raw trace is 2,794 bytes with SHA256
`784645dcd85f2ce0cc8e734cc22c8c50231ba28434958dec7a6f855ae1cb7f05`. The measured record
`measured-experiment.sexp` is 16,942 bytes (SHA256
`fb22d5e5554a0e132c231e5551ed8314ab4be35ff93e7f086fceeacb6235a152`); the receipt
`verification.json` is 7,017 bytes (SHA256
`91a90d9c56487af1a6b4306e9007d771e17246ddf41b358185374680090a5a5d`) with `qualification` false;
like the first receipt it names repository-root identities under `object`, because a JSON object
carrying both `path` and `sha256` is a fixture pin resolved relative to the record's own directory.
Retained evaluation authenticated 85 files totalling 1,076,834 bytes and kept 40,438 snapshot
bytes; the combined conservative artifact-read charge was 24,396,002 bytes of the 134,217,728
allowance. All 25 predeclared properties bind to the source derivation — the 13 forms and the 12
Table 1 cells — with the control's observed value equal to the source finding's.

Check the retained result without running Sail, naming the case:

```bash
PYTHONPATH=scripts python3 - <<'PY_M_FORMS'
import json
from capture_div import prepare_capture, ROOT, S, Unit, prefix
from experiment_artifacts import observe_bounded_file, read_snapshot

case = "rv64gc-m-forms-v3"
path = prefix(case) + "/verification.json"
observed = observe_bounded_file(ROOT, path, max_bytes=65536)
report = json.loads(read_snapshot(ROOT, "input", dict(id="verification", path=path,
                    sha256=observed.sha256), max_bytes=65536).data)
retained = report["measured_experiment"]
measured = read_snapshot(ROOT, "observation", {**retained, "path": retained["object"]}, max_bytes=65536)
raw = next(form for form in S.parse(measured.data.decode()) if form[0] == "experiment")
d = prepare_capture(case)
checked = Unit.Evaluation.evaluate_retained_unit(
    ROOT, raw_experiment=raw, scope=d.authorities.scope,
    current_candidate=dict(d.authorities.reference.fields), reviewed_inputs=d.inventory,
    author_review=d.author, impact_review=d.impact,
    property_authority=d.authorities.property_authority, case_id=case)
print(checked.disposition, checked.record.disposition, checked.comparison.disposition)
print(*(run.comparison.verdict for run in checked.comparison.runs))
print(len(checked.source_property.facts.observed), report["qualification"])
PY_M_FORMS
```

It prints `pending valid satisfied`, `AGREE AGREE DIVERGE`, then `25 False`. Since a42ax
(2026-10-23) the retained reviews read this capture: `scripts/review_div_method.py` names it
(`RETAINED_CASE_ID`, the 16,942-byte measured pin, the declaration and capture commits) and reports
`satisfied` over 85 authenticated files, and `scripts/review_div_policy.py` measures
[all ten legs satisfied](policy-adequacy.md) with `credited` false. The first case is `invalidated`
history, never rerun. Nothing here credits `REQ-GC-M`; `scripts/requirement_status.py` derives it
`planned` with both cases pending, and the crediting act is a separately owned record
(`decision_ten-legs-satisfied-credit-separate.md`). That act came at a42az (`CR-GC-M-1`, 2026-10-26) and was
retired at `P4-SYSTEM.14` a44-2b (2026-10-29): moving the matched cases' declarations into data moved pinned
inputs of this capture, so the method review reports it `stale`, the policy review `invalidated`, and this
capture joins the first as history. The M case returned as `rv64gc-m-forms-v4`, declared (a44-3, 177b43a1) and
captured once (a44-4, 3c464095) under the new manifest of 67 children: every trace and stdout byte-identical to
v3's, the stderr streams differing only by the case directory they print. The retained reviews read v4 —
`satisfied` over 88 authenticated files, all ten legs — and `CR-GC-M-2` credited it (a44-5) until the planned
lapse that opens CSR-SET retired it (a43b-2b, 2026-11-02): v4 is history in turn, re-captured as v5 (a43b-2c … 2e).

The re-capture is the window's proof that it changed only what was declared. `rv64gc-m-forms-v5` and the XLEN case's
`rv64gc-xlen-forms-v2` were each captured exactly once on 2026-11-02 (a43b-2d), on a quiet host, from the declaration
commit `7b1a8f44`: baseline and repeat AGREE, the control DIVERGE at its declared step (12 for M, 24 for XLEN). All six
traces and all six stdout streams are byte-identical to v4's and xlen-v1's (`cmp`); each stderr stream equals its
predecessor's with the case directory it prints substituted. With the case id substituted, each measured record
differs from its predecessor's only in seven digests — the dependency manifest, the three stderr streams and the three
receipts that record them — and, for XLEN, in the control's id and prose, now `truncated-address` and "the address
truncated to 32 bits must diverge". Since a43b-2e the reviews read the two captures — each `satisfied` over 88
authenticated files, all ten legs — and `CR-GC-M-3` and `CR-D-XLEN-2` credit them.

`rv64gc-csr-set-v1` is the first case on [its own reference configuration](references.md) and the first whose requirement
is `implementation-defined`. It was captured exactly once on 2026-11-04 (a43b-3f), on a quiet host, from its declaration
commit `02835e0f`, in 1.3 s:

| Run | Compared with | Verdict |
| --- | --- | --- |
| `baseline` | `baseline.expected.sexp` | AGREE, 157 declared steps |
| `repeat` | `baseline.expected.sexp` | AGREE, 157 declared steps |
| `control` | `control.expected.sexp`, boundary 130 wrong on purpose | DIVERGE at 130: `csrrs x28, mscratch, x0`, Sail x28 = 5, the expectation 9 |

The control is the case's failure mode: an S-mode write of 9 to `mscratch`, refused, read back in M. Expecting 9 is what a
refused write that had committed would look like, and it must diverge. All three traces are byte-identical (13,833 B,
`cmp`), and so are the stdout streams; each stderr stream prints its own trace's name. The capture is complete with
qualification false. Since a43b-3g the reviews read it, `satisfied` over 88 authenticated files, all ten legs, and
`CR-D-CSR-SET-1` credits it (a43b-3h).

`rv64gc-zicntr-v1` follows it on the same configuration, byte for byte. It was captured exactly once on 2026-11-05 (a43c-4), on a
quiet host, from its declaration commit `86a35987`, in 1.4 s:

| Run | Compared with | Verdict |
| --- | --- | --- |
| `baseline` | `baseline.expected.sexp` | AGREE, 292 declared steps |
| `repeat` | `baseline.expected.sexp` | AGREE, 292 declared steps |
| `control` | `control.expected.sexp`, boundary 109 wrong on purpose | DIVERGE at 109: `addi x21, x20, 0`, Sail x21 = 21, the expectation 102 |

The control is the case's failure mode: S's `rdcycle` at boundary 102, refused while `mcounteren.CY` is clear, leaves `x20` at its sentinel, and
boundary 109 copies it to `x21`. Expecting 102 is what a refused read that had committed the count would look like, and it must diverge. All three traces
are byte-identical (26,277 B, `cmp`), and so are the stdout streams; each stderr stream prints its own trace's name. The capture is complete with qualification
false. Since a43c-5 the reviews read it, `satisfied` over 88 authenticated files, all ten legs, and `CR-D-ZICNTR-1` credits it.

**Since `P4-SYSTEM.14` a43e-1 (2026-11-05) these four captures are history in their turn.** The window that opens SSTC moved inputs each manifest pins, so `CR-GC-M-3`, `CR-D-XLEN-2`, `CR-D-CSR-SET-1` and `CR-D-ZICNTR-1` were retired. Each case is re-captured once under a new id; none of their steps is a delivery and neither their guests nor their configurations move, so their traces should be byte-identical, and a difference would be a finding (`decision_sstc-delivery-needs-the-pinned-window.md`).

## The window's five (a43e-4)

The four came back byte-identical, and `rv64gc-sstc-v1` joined them. Each was captured exactly once on 2026-11-05, from the declaration commit `18a09566`, with no retry:

```text
$ python3 -B scripts/retain_div_capture.py --case rv64gc-sstc-v1 --declaration-commit 18a09566408b1d78d24ee2c0eb83b7ef19eed3bc
```

| Case | Baseline, repeat | Control | Ran | Measured record | Each trace |
| --- | --- | --- | --- | --- | --- |
| `rv64gc-m-forms-v6` | AGREE, 33 steps | DIVERGE at 12: `div x15, x5, x6`, Sail -3, the expectation -4 | 1.2 s | 16,943 B, `7998edb1…` | 2,794 B |
| `rv64gc-xlen-forms-v3` | AGREE, 25 steps | DIVERGE at 24: `csrrs x31, mtval, x0`, Sail 2^40, the expectation 0 | 1.2 s | 14,980 B, `db272820…` | 2,260 B |
| `rv64gc-csr-set-v2` | AGREE, 157 steps | DIVERGE at 130: `csrrs x28, mscratch, x0`, Sail 5, the expectation 9 | 1.4 s | 27,347 B, `d8f18593…` | 13,833 B |
| `rv64gc-zicntr-v2` | AGREE, 292 steps | DIVERGE at 109: `addi x21, x20, 0`, Sail 21, the expectation 102 | 1.5 s | 24,163 B, `c2b55c23…` | 26,277 B |
| `rv64gc-sstc-v1` | AGREE, 315 steps | DIVERGE at 172: `csrrs x11, sip, x0`, Sail 0, the expectation 32 | 1.5 s | 22,241 B, `801b9383…` | 26,417 B |

SSTC's control is the case's failure mode: an all-ones `stimecmp` read as a signed -1 would sit below every `time`, so `sip` would read `0x20`, and the statement says the comparison is unsigned. Each capture is complete with qualification false. Since a43e-5 the reviews read all five, `satisfied` over 88 authenticated files, all ten legs, and a record credits each ([requirement status](requirement-status.md)).

**What the window changed.** You can check the prediction yourself:

```text
$ cmp <(git show e5814f18:evidence/rv64gc-zicntr-v1/baseline.trace) <(git show 178f9c6c:evidence/rv64gc-zicntr-v2/baseline.trace)
```

All 12 traces and all 12 stdout streams of the four are byte-identical to their predecessors'. Each of the 12 stderr streams equals its predecessor's with the case id substituted. With the id substituted, each measured record moved in ten tokens: the dependency manifest's digest, three stderr digests, three receipt digests, the deriver's digest as the version of the two expected producers (a43e-2 edited the deriver), and the control reason's one recovered space. XLEN's moved in two more, its expectations' digests, which a43e-3 had already measured.

**These five did not run on a quiet host.** Earlier captures waited for three minutes with no sibling repository's process. This one waited 107 minutes without reaching that, and the director then asked for the run ("try runnung"). Ten sibling processes were running, at a 1-minute load of 4.71 to 5.13. Every other guard held, and two took the wait's place: the load below 8, and 50 children spawned and reaped the collector's way before each case (`decision_sstc-delivery-needs-the-pinned-window.md`). A capture's bytes do not depend on the load: the four's traces are the proof.

## Batch I, the RV64I base (a46-3)

The first batch of `decision_obligations-route.md`: nine requirements, one case each, on the profile's own override. Each was captured exactly once on 2026-11-06, from the declaration commit `506788a6`, with no retry:

| Case | Baseline, repeat | Control | Measured record | Each trace |
| --- | --- | --- | --- | --- |
| `rv64gc-alu-imm-v1` | AGREE, 19 steps | DIVERGE at 12: `sltiu x16, x15, -1`, Sail 1, the expectation 0 | 13,251 B, `27bf858d…` | 1,628 B |
| `rv64gc-alu-reg-v1` | AGREE, 18 steps | DIVERGE at 11: `sltu x15, x6, x5`, Sail 0, the expectation 1 | 12,154 B, `41ec7ae6…` | 1,512 B |
| `rv64gc-lui-auipc-v1` | AGREE, 10 steps | DIVERGE at 8: `auipc x11, 0x80000`, Sail 32, the expectation `0x100000020` | 12,201 B, `c9e17ce2…` | 827 B |
| `rv64gc-jalr-lsb-v1` | AGREE, 16 steps | DIVERGE at 3: `auipc x7, 0`, Sail base + 20, the expectation base + 21 | 12,476 B, `04ff5c6f…` | 1,347 B |
| `rv64gc-no-delay-slots-v1` | AGREE, 21 steps | DIVERGE at 3: `addi x10, x20, 10`, Sail 10, the expectation 109 | 13,753 B, `e8d3d275…` | 1,596 B |
| `rv64gc-shamt-v1` | AGREE, 21 steps | DIVERGE at 6: `sll x11, x5, x10`, Sail 2, the expectation 0 | 13,497 B, `8fad52b3…` | 1,800 B |
| `rv64gc-wsuffix-v1` | AGREE, 17 steps | DIVERGE at 11: `addw x16, x7, x8`, Sail the sign-extended word, the expectation `0x80000000` | 12,951 B, `961ce2c7…` | 1,446 B |
| `rv64gc-load-ext-v1` | AGREE, 32 steps | DIVERGE at 16: `lw x12, x1, 4`, Sail the sign-extended word, the expectation `0x88776655` | 12,832 B, `bc4b2d3b…` | 2,507 B |
| `rv64gc-load-x0-v1` | AGREE, 68 steps | DIVERGE at 10: `csrrs x30, mcause, x0`, Sail 5, the expectation 77 | 14,719 B, `d5fda2b4…` | 6,520 B |

Each control is that case's failure mode, predeclared: an immediate not sign-extended, a compare read as signed, a target that keeps its low bit, a delay slot that ran, an amount not masked, a word not sign-extended, a load extended the wrong way, a discarded load that skipped its fault. Each capture is complete with qualification false, and each case's three traces are byte-identical. Since a46-4 the reviews read all nine, 10 of 10 legs each, and a record credits each.

**They were rehearsed first.** Every compared file of the real capture, traces, stdout, guest, expectations, case and declaration, is byte-identical to the throwaway clone's. So a capture's bytes do not depend on which commit declared it, or on the load, which stood at 7.3 to 7.8 beside seven to nine sibling processes. The guard held the first case for four and a half minutes, until the load fell below 8.

## Batch II-a, the `defined` half of system (a47-2)

Five requirements, one case each, each captured exactly once on 2026-11-06 from the declaration commit `507c3017`. The counters case carries its own overlay; the other four run under the profile's override.

| Case | Baseline, repeat | Control | Measured record | Each trace |
| --- | --- | --- | --- | --- |
| `rv64gc-ecall-ebreak-v1` | AGREE, 116 steps | DIVERGE at 50: `csrrs x10, mcause, x0`, Sail 9, the expectation 11 | 17,655 B, `61742b70…` | 10,386 B |
| `rv64gc-csr-access-v1` | AGREE, 66 steps | DIVERGE at 15: `csrrs x15, mscratch, x0`, Sail 31, the expectation all ones | 15,911 B, `b6f7c30b…` | 6,106 B |
| `rv64gc-counters-v1` | AGREE, 84 steps | DIVERGE at 23: `addi x21, x20, 0`, Sail 21, the expectation 15 | 12,150 B, `76d4a37b…` | 7,198 B |
| `rv64gc-fencei-v1` | AGREE, 10 steps | DIVERGE at 9: `.word 0x00700113`, Sail 7, the expectation 2 | 10,225 B, `9fc3b954…` | 732 B |
| `rv64gc-ialign-16-v1` | AGREE, 11 steps | DIVERGE at 3: `auipc x3, 0`, Sail base + 14, the expectation base + 12 | 11,368 B, `bad8453d…` | 854 B |

Each control is that case's failure mode: a cause that does not name its mode, a CSR immediate sign-extended, a refused read that committed, a stale fetch, a target rounded to a word. Each capture is complete with qualification false, and every compared file is byte-identical to the rehearsal's. Since a47-3 the reviews read all five, 10 of 10 legs each, and a record credits each.

**The guard refused first, as it should.** Its first attempt held for its full ten minutes at a load above 8 and stopped, capturing nothing, so no case id was spent. Armed again, it ran when the load fell below 7.

## The window that carries fetch faults (a49-2)

23 cases, each captured exactly once on 2026-11-06 from the declaration commit `3b24bd52`. Each baseline and repeat `AGREE`, and each control `DIVERGE` at its predeclared witness and nowhere else.

| Case | Steps | Witnesses | Control's divergence | Measured record | Each trace |
| --- | --- | --- | --- | --- | --- |
| `rv64gc-m-forms-v7` | 33 | 25 | 12: `div x15, x5, x6` | 16,943 B, `7527a85c…` | 2,794 B |
| `rv64gc-xlen-forms-v4` | 25 | 17 | 24: `csrrs x31, mtval, x0` | 14,980 B, `0b87cbce…` | 2,260 B |
| `rv64gc-csr-set-v3` | 157 | 53 | 130: `csrrs x28, mscratch, x0` | 27,347 B, `bf24e258…` | 13,833 B |
| `rv64gc-zicntr-v3` | 292 | 44 | 109: `addi x21, x20, 0` | 24,163 B, `88b6adfb…` | 26,277 B |
| `rv64gc-sstc-v2` | 315 | 39 | 172: `csrrs x11, sip, x0` | 22,241 B, `0c84e833…` | 26,417 B |
| `rv64gc-alu-imm-v2` | 19 | 13 | 12: `sltiu x16, x15, -1` | 13,251 B, `d8159cef…` | 1,628 B |
| `rv64gc-alu-reg-v2` | 18 | 10 | 11: `sltu x15, x6, x5` | 12,154 B, `fc17ca34…` | 1,512 B |
| `rv64gc-lui-auipc-v2` | 10 | 9 | 8: `auipc x11, 0x80000` | 12,201 B, `3bd11dba…` | 827 B |
| `rv64gc-jalr-lsb-v2` | 16 | 10 | 3: `auipc x7, 0` | 12,476 B, `c4856561…` | 1,347 B |
| `rv64gc-no-delay-slots-v2` | 21 | 11 | 3: `addi x10, x20, 10` | 13,753 B, `6c12cb8b…` | 1,596 B |
| `rv64gc-shamt-v2` | 21 | 15 | 6: `sll x11, x5, x10` | 13,497 B, `84c147cd…` | 1,800 B |
| `rv64gc-wsuffix-v2` | 17 | 12 | 11: `addw x16, x7, x8` | 12,951 B, `e036103d…` | 1,446 B |
| `rv64gc-load-ext-v2` | 32 | 12 | 16: `lw x12, x1, 4` | 12,832 B, `c93bdd56…` | 2,507 B |
| `rv64gc-load-x0-v2` | 68 | 16 | 10: `csrrs x30, mcause, x0` | 14,719 B, `de9b732a…` | 6,520 B |
| `rv64gc-ecall-ebreak-v2` | 116 | 25 | 50: `csrrs x10, mcause, x0` | 17,655 B, `ed55336b…` | 10,386 B |
| `rv64gc-csr-access-v2` | 81 | 25 | 15: `csrrs x15, mscratch, x0` | 17,178 B, `20f7d58d…` | 7,518 B |
| `rv64gc-counters-v2` | 84 | 8 | 23: `addi x21, x20, 0` | 12,150 B, `3aa72b51…` | 7,198 B |
| `rv64gc-fencei-v2` | 18 | 4 | 9: `.word 0x00700113` | 11,052 B, `bf596e7c…` | 1,349 B |
| `rv64gc-ialign-16-v2` | 11 | 6 | 3: `auipc x3, 0` | 11,405 B, `3a6a0f30…` | 854 B |
| `rv64gc-atomics-v1` | 246 | 64 | 21: `amoadd.w x5, x6, (x1` | 27,721 B, `a9c6a2f0…` | 20,411 B |
| `rv64gc-c-forms-v1` | 251 | 52 | 108: `c.jalr x1` | 23,555 B, `a8795ba6…` | 21,088 B |
| `rv64gc-f-forms-v1` | 338 | 90 | 127: `fmv.x.w x6, f8` | 33,297 B, `098f2565…` | 28,316 B |
| `rv64gc-d-forms-v1` | 350 | 93 | 131: `fmv.x.d x6, f8` | 34,607 B, `ab063035…` | 28,949 B |

**What moved, measured.** The 17 unchanged cases' 153 files, each trace, stream, image and expectation, are byte-identical to their predecessors'. That is what a re-capture is for: the tools moved and the behaviour did not. Every file is also byte-identical to the rehearsal's on a clone, and the three effects retained for `rv64gc-csr-set-v3`, `rv64gc-zicntr-v3` and `rv64gc-sstc-v2` read steps 34, 6 and 8 as before, each trace byte-identical to its predecessor's. Each capture is complete with qualification false.

`rv64gc-c-forms-v1` is the first case to carry fetch faults. Step 225's `<fetch page fault>` reads the first parcel at the page's last halfword and faults at the second, and the handler reads that parcel's address and the instruction's start; step 245's comes only at the next instruction, after a sixteen-bit form in that last halfword ran. Since a49-3 the reviews read all 23, 11 of 11 legs each, and a record credits each.

## The seven with a switch (a50-3)

Seven cases, each captured exactly once on 2026-11-06 from the declaration commit `40488d5b`, at load 21 to 26, 1.2 s to 1.4 s each. Each baseline and repeat `AGREE`, and each control `DIVERGE` at its predeclared witness.

| Case | Steps | Witnesses | Control's divergence | Measured record | Each trace |
| --- | --- | --- | --- | --- | --- |
| `rv64gc-svade-v1` | 137 | 15 | 129: `ld x6, x8, 0` | 13,822 B, `d0ad7094…` | 11,519 B |
| `rv64gc-atomic-misalign-v1` | 180 | 26 | 24: `csrrs x30, mcause, x0` | 17,750 B, `a78b3318…` | 16,572 B |
| `rv64gc-fault-priority-v1` | 271 | 37 | 159: `csrrs x22, scause, x0` | 21,562 B, `884f7191…` | 24,888 B |
| `rv64gc-priv-modes-v1` | 109 | 15 | 5: `csrrs x5, misa, x0` | 13,782 B, `c25f84ea…` | 9,529 B |
| `rv64gc-sv39-v1` | 135 | 11 | 17: `csrrs x5, satp, x0` | 12,765 B, `62ea14c6…` | 11,144 B |
| `rv64gc-reservation-v1` | 190 | 24 | 23: `sc.w x15, x6, (x3` | 17,095 B, `9704f8d4…` | 15,676 B |
| `rv64gc-sc-deterministic-v1` | 159 | 21 | 21: `sc.w x15, x6, (x3` | 16,274 B, `d956f455…` | 13,331 B |

Each of these requirements is the profile's choice among options the reference also offers, so each case retains an effect: the same guest through the same binary under what selects otherwise, with the first difference at a declared witness.

| Case | Compared with | First difference |
| --- | --- | --- |
| `rv64gc-svade-v1` | its declared alternative | 93: `csrrs x22, scause, x0` |
| `rv64gc-atomic-misalign-v1` | its declared alternative | 24: `csrrs x30, mcause, x0` |
| `rv64gc-fault-priority-v1` | its declared alternative | 159: `csrrs x22, scause, x0` |
| `rv64gc-priv-modes-v1` | its declared alternative | 5: `csrrs x5, misa, x0` |
| `rv64gc-sv39-v1` | its declared alternative | 17: `csrrs x5, satp, x0` |
| `rv64gc-reservation-v1` | the profile override | 23: `sc.w x15, x6, (x3` |
| `rv64gc-sc-deterministic-v1` | the profile override | 21: `sc.w x15, x6, (x3` |

**What moved, measured.** All 77 files compared are byte-identical to the rehearsal: the eleven each case keeps for comparison, its effect trace among them. Only `verification.json` differs between two runs of one case, in its process ids. All seven were credited at a50-4.
