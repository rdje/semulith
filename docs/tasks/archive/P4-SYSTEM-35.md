# P4-SYSTEM ordinary history — part 35

Ordinary, directly readable task history: the complete records of the closed `.14` units
a49-0 to a49-4, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0376` on top of commit `524914a84e9f9f95e4df5568e6ea7888bd1a2862`
(6 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a48-1 to a47-1 and their rows are in part 34,
the earlier ones in parts 13–33. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a50-c1, SEMULITH-P4-0376.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a49-4 | 2729 | `32f70c415bb417314525727981f9cfdb04f8468d269218bdcb20b96d13ac9c7e` |
| record a49-3 | 1388 | `423f2e641c0ed3d2154c976602add87234dbb90dac917a5b3a7e86881dab7c01` |
| record a49-2 | 1367 | `c767cfa28cc639f4ab88b0c610c5175d0ae3d00e9f8ccbc507c8493934262e01` |
| record a49-1 | 2879 | `f2fe034e8a5f46b9f7b4d2e4a831d9f468424b907abcde1f2d78199e2aa67852` |
| record a49-0 | 1922 | `84bb916315673f7e653972b539076ad03e9c6ce1e53ddd9ccbc4b6f823fc5546` |
| acceptance rows a49-4–a49-0 | 5490 | `67e94bb17975eab385635ae42fcd150faf73dd8dd5b878413e84aa895ed79f7e` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-35.md)   # a span, by its line range
```

<a id="a49-4"></a>

### .14 a49-4 / SEMULITH-P4-0371: the superseded cases leave the tree, listed, and the list reads back from history (completed)

Feature 1 of 5 after XTASK-0084, and the window's last unit: `decision_the-window-that-carries-fetch-faults.md` closes. **The change.** 23 directories (3,700,566 B, 506 files) and the 16 overlay and effect files named for them (118,103 B) are out, `evidence/` holds 551 files and 25 cases, and no credit, report or pinned input moved: 23 current, 23 `implemented`, 24 `planned`. `rv64gc-signed-div-truncation-v2` and `rv64gc-m-forms-v3` stay because a pinned file names them (`decision_superseded-cases-retired.md`). **The list is checked.** `docs/models/rv64gc-lab-v0/src/retired-cases.md` gives each of the 25 its last commit, Git tree and measured-record digest, and each of the 16 its commit and digest, and a new test reads every row back from history and holds each absent from the tree. Fired on a throwaway clone of the staged tree (`target/p4-system-14/a49-4/red-states.txt`):

| Damage | Test |
| --- | --- |
| none | `rc=0` |
| a row's Git tree wrong | `rc=1` |
| a row removed | `rc=1`, `24 != 25` |
| a row's measured digest wrong | `rc=1` |
| a file row's digest wrong | `rc=1` |
| a retired directory back in the tree | `rc=1` |
| a retired file back in the tree | `rc=1` |

**The probes moved to cases in the tree.** The capture-input probe drops 180 lines of pins for cases that left, and its per-case controls read `rv64gc-csr-set-v3`, `rv64gc-zicntr-v3` and `rv64gc-sstc-v2`. The overlay and effect probes read the same three. Their retained-effect table goes from five rows to the three that remain.

**A defect this found, fixed here.** The book's runnable examples had drifted at a49-3, in two pages. `method-adequacy.md` ran the review on `rv64gc-m-forms-v4` and `rv64gc-xlen-forms-v1`, which it had stopped reading, so its stated output could not be reproduced, and it still called v4 the default. Both now name today's cases with re-measured numbers, and each stated limit was run: `--max-read-bytes 1088325` `rc=0`, 1088324 `rc=1`, and the same for the XLEN case at 1079426 and 1079425. `references.md` and `requirement-status.md` carried dated census output under commands naming retiring cases, so they now show today's: 191 guests, 168 agreeing on both configurations. The three retained effects are byte-identical to their predecessors' (the same `trace_sha256`), so those examples could move with no number changing. Recognised late: a page's runnable example has no check that it still runs, and only this retirement's search surfaced it.

**The cap stands.** 551 of 1101 files and 25 of 50 cases: lowering it now would only force a re-derivation at the next window.

<a id="a49-3"></a>

### .14 a49-3 / SEMULITH-P4-0370: 23 credits under eleven legs, G-STATE and G-TRACE restored, and Batch II-b `implemented` (completed)

Feature 5 of 5 after XTASK-0082: the turn is XTASK.13's MATERIALS-BILL, next. **The reviews.** `RETAINED_CAPTURES` names the 23 (declared 3b24bd52, captured 57544407): each `satisfied`, 88 authenticated files; `--every-retained` prints 23 lines, each `satisfied — 11 of 11 legs satisfied`. The four new dispositions name 22 to 69 properties each, and the probe holds each name to a declared property.

**The credits.** 23 records, `authority review`, 38,516 B of the file's 65,536 B: the 19 re-issued, each id one on, and `CR-GC-ATOMICS-1`, `CR-GC-C-1`, `CR-GC-F-1`, `CR-GC-D-1` (`decision_batch-ii-b-credited-implemented.md`). Measured: `CREDIT-RECORDS: … 23 credit(s), 23 current, 0 lapsed`; `REQUIREMENT-STATUS: … 24 planned, 23 implemented, 1 not-applicable; 48 case(s), 23 credited`. **`G-STATE` 4 of 4, `G-TRACE` green, 2 of 10 axes open.**

**The tripwire, read.** The pre-commit gate took 25.3 minutes at a48-1, 26.1 at a49-1 and 27.3 at a49-2, 48 cases in the tree: about 2 minutes for 17 more cases, against the limit of 1 minute per case. Rolled to archive part 34: a47-1 to a47-3 and a48-1. Re-stated: the policy, method, status and dossier probes' real-tree predictions, and `derived-status` back to 37. Next, XTASK.13, then a49-4.

<a id="a49-2"></a>

### .14 a49-2 / SEMULITH-P4-0369: the window's 23 cases captured exactly once each, and no behaviour moved (completed)

Feature 4 of 5 after XTASK-0082. **The captures.** Each once from the declaration commit `3b24bd52`, behind the capture guard, 1.2 s to 1.6 s each: each baseline and repeat `AGREE`, each control `DIVERGE` at its predeclared witness. Three effects retained with `measure_config_effect.py`: `csr-set` step 34, `zicntr` step 6, `sstc` step 8.

**The comparison** (`target/p4-system-14/a49-2/compare.py`). All 153 files compared with the 17 unchanged predecessors are byte-identical, every compared file of all 23 matches its rehearsal, and the three effect traces match their predecessors'. **0 findings**, so the window's stop condition did not fire: the pinned edits moved no behaviour. `rv64gc-c-forms-v1` is the first case carrying fetch faults.

**A ceiling, measured:** `profiles/` went 59,772 B over, and retiring the window's peak would not hold it for the next batch, so it goes to 6 MiB, once for the rest of the route (`decision_profiles-family-corpus-third-rederivation.md`). Re-stated: the input probe's census (`1 + 48 * 22`), the status probe (`48, 0, 0, 0, 0`, each new case now `pending`). Book: `canonical-division.md`'s table of the 23, `prepared-inputs.md`, `requirement-status.md`. Family: 1057 files, 8,212,396 B. Next, a49-3.

<a id="a49-1"></a>

### .14 a49-1 / SEMULITH-P4-0368: the window opens: a case carries a fetch fault, the review reads every clause, and 23 cases declared on it (completed)

Feature 3 of 5 after XTASK-0082. **`G-STATE` and `G-TRACE` read open, and no requirement `implemented`, until a49-3:** that is the cost `decision_the-window-that-carries-fetch-faults.md` measured.

**The pinned edits.** A wordless boundary is an event, and writes nothing: a delivered interrupt reads no parcel, and a fetch fault, spelled `<fetch page fault>` or `<fetch fault>`, reads none or one (`matched_gpr_case`, `matched_gpr_property`, `matched_gpr_comparison`). The adapter holds a spelling to its cause, 12 or 1. `MAX_PROPERTIES` goes from 64 to 96.

**The eleventh leg.** `statement-trace`: every clause of a requirement's statement names declared properties or a limit its case states, and every property stands for a clause (`scripts/statement_trace.py`, `schema/statement-trace.sexp`, `profiles/rv64gc-lab-v0/statement-trace.sexp`, declared in `EVIDENCE_POLICY.md`). 23 requirements, all tracing. It found two clauses of `REQ-GC-CSR-ACCESS`, two of `REQ-GC-FENCEI` and one of `REQ-D-IALIGN-16` that the ten legs had passed, and each is witnessed or named now.

**The 23 cases.**

| Cases | Witnesses | What moved |
| --- | --- | --- |
| 17 re-issued unchanged | 325 | The id, and the fresh authority: no prepared input moved |
| `rv64gc-csr-access-v2`, `rv64gc-fencei-v2` | 25, 4 | New programs, closing the holes |
| `rv64gc-atomics-v1`, `rv64gc-c-forms-v1` | 64, 52 | `c-forms` gets its second-parcel fault back |
| `rv64gc-f-forms-v1`, `rv64gc-d-forms-v1` | 90, 93 | All ten FCLASS classes, FMIN's NaN rules, the fused invalid rule, the five rounding modes, FS Off on three kinds of form |

**The credits.** All 19 retired by removal, the catalogue file with them, recoverable from `82498e5e`; the statuses read `planned`. `G-TRACE`'s 19 rows left with them. **Two predecessors left early:** `rv64gc-csr-access-v1` and `rv64gc-fencei-v1`, whose guests changed in place. **The family's cap:** 50 cases, the peak (`decision_evidence-family-two-cases.md`, tenth).

**Arms that named real cases** now judge a stub: `gate_report.py --self-test`'s four credit arms and `test_gen_model_book.py`'s three, so a window no longer breaks them. **Rehearsed on a clone of the staged tree:** 23 of 23 captured in 40 s, 11 of 11 legs each, every control where declared, and all 153 files compared with the 17 unchanged predecessors byte-identical. It found `review_div_policy.py` still refusing above 64 properties: fixed, and held equal to the tools' bound by a probe. Re-stated: the input probe's tables and census (`1 + 25 * 22 + 23 * 8`), the case, property, relation and evaluation probes for the binding and the cap, the status probe (`48, 0, 23, 0, 0`), the dossier probe. **Frozen until the captures.** Next, a49-2.

<a id="a49-0"></a>

### .14 a49-0 / SEMULITH-P4-0367: the director's ruling recorded, a call reversed on its measurement, and the window proved on a throwaway clone (completed)

Feature 2 of 5 after XTASK-0082. **Only records move:** the pinned files, the cases and the credits stay as they were. **The ruling.** The calls on the engineer's findings are the engineer's, to the director's standard; pushes stay the director's (`decision_findings-are-the-engineers-to-call.md`). **The call it reverses.** P4-0366 kept a fetch fault out of `c-forms` as "one sentence of one requirement". Measured: three planned requirements state one (`REQ-GC-C`, `REQ-D-FAULT-PRIORITY`, `REQ-GC-PARTIAL-PROGRESS`), and two more only mention a fetch (`REQ-GC-PRIV-INSNS`, `REQ-D-WALK-IMPLICIT`); four corpus guests carry one. A window costs less the earlier it opens, so it opens now.

**The clone** (`target/p4-system-14/a49-0/prototype.sh`, `prototype.txt`). The pinned edits, in 8 files, lapse exactly the 19. Nineteen cases re-declared under new ids and Batch II-b with `c-forms`' faults back: 23 of 23 `capture rc=0`, in 42 s in all. **All 171 files compared with the 19 predecessors are byte-identical.** Each case reads 10 of 10 legs, and each control diverges at its old step. Nine of the twelve probes run need re-stating, one of them for the family's cap: 50 cases against 41.

**What the window carries** (`decision_the-window-that-carries-fetch-faults.md`): the fetch fault as a typed event; `MAX_PROPERTIES` 96; a statement-trace leg, so that an omitted clause cannot pass the review, which is the mechanical answer to P4-0366's second finding; and the 27 superseded directories out of the tree, reachable in history. A false alarm, recorded so nobody repeats it: `run_rv64gc_sail.py` and `matched_gpr_unit_collector.py` are absent from `dependencies.sexp` because each case pins them by their own roles in `planned-experiment.sexp`. Next, a49-1.

<a id="acceptance-rows-a49-4-to-a49-0"></a>

## acceptance-rows-a49-4-to-a49-0

- [x] `.14` a49-4 **ROOT CAUSE** — the window left its predecessors in the tree until the new credits were current: at b4574553 `git ls-files evidence | wc -l` = 1057, 48 cases, and `git grep -c 'rv64gc-sstc-v1' b4574553 -- scripts/probe_div_capture_inputs.py` names a directory no credit reads; `python3 -B scripts/review_div_method.py --case rv64gc-m-forms-v4` at that commit, the book's own example, read `unsupported`.
- [x] `.14` a49-4 **ADDRESSED** — `git ls-files evidence | wc -l` = 551; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `23 credit(s), 23 current, 0 lapsed`; `python3 -B scripts/probe_div_capture_inputs.py` `rc=0` → `DIV-CAPTURE-INPUTS: 80 tests / 0 failures`; `grep -c 'rc=1' target/p4-system-14/a49-4/red-states.txt` = 6.
- [x] `.14` a49-4 **NO REGRESSION** — `grep -c 'green' target/p4-system-14/a49-4/red-states.txt` = 2, each `rc=0`; `git diff --cached --name-only | grep -Fxcf target/p4-system-14/a49-4/pinned.txt` = 0, so no file a case pins moved; `python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0` `rc=0` → `24 planned, 23 implemented, 1 not-applicable`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures`; `MATCHED-GPR-CASE: 11 tests / 0 failures`; `MATCHED-GPR-PROPERTY: 36 tests / 0 failures`; `CONFIG-EFFECT: 10 tests / 0 failures`; `REFERENCE-OVERLAY: 14 tests / 0 failures`; `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`.
- [x] `.14` a49-3 **ROOT CAUSE** — the window's 23 captures were credited by nothing: at 57544407 `git ls-files profiles/rv64gc-lab-v0/credits.sexp | wc -l` = 0, and `python3 -B scripts/review_div_method.py --case rv64gc-m-forms-v7` had no row to read.
- [x] `.14` a49-3 **ADDRESSED** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `23 credit(s), 23 current, 0 lapsed`; `python3 -B scripts/review_div_policy.py --every-retained 2>&1 | grep -c '11 of 11 legs satisfied; credited by'` = 23; `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 24 planned, 23 implemented, 1 not-applicable; 48 case(s), 23 credited, 0 declared, 23 of 23 credit record(s) current; 0 drift, 0 finding(s)`.
- [x] `.14` a49-3 **NO REGRESSION** — `DIV-POLICY-PROBE: 55 tests / 0 failures`; `DIV-METHOD: 22 tests / 0 failures`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures`; `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`; `gate_report --self-test: 28 pass / 0 fail`, `rc=0`; `GATE-REPORT: ok`.
- [x] `.14` a49-2 **ROOT CAUSE** — the window's 23 declarations had no capture: at 3b24bd52 `git ls-files 'evidence/rv64gc-m-forms-v7/*.trace' | wc -l` = 0.
- [x] `.14` a49-2 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a49-2/capture.log` = 23; `python3 -B target/p4-system-14/a49-2/compare.py | grep -c 'byte-identical with predecessors: 153 findings: 0'` = 1; `DIV-CAPTURE-INPUTS: 79 tests / 0 failures`, `rc=0`.
- [x] `.14` a49-2 **NO REGRESSION** — `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 47 planned, 1 not-applicable; 48 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift, 0 finding(s)`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures`; each of the three effects `rc=0`, `cmp` silent against its predecessor's trace.
- [x] `.14` a49-1 **ROOT CAUSE** — a case could not carry a fetch fault and the review could not see an omitted clause: at 82498e5e `grep -c 'fetches not in (0, 1)' scripts/matched_gpr_case.py` = 0, and `git ls-files profiles/rv64gc-lab-v0/statement-trace.sexp | wc -l` = 0.
- [x] `.14` a49-1 **ADDRESSED** — `python3 -B scripts/statement_trace.py --profile rv64gc-lab-v0` `rc=0` → `23 of 23 requirements with a declared case trace`; `STATEMENT-TRACE-PROBE: 15 tests / 0 failures`, each of seven seams `1 tests / 1 failures`; `MATCHED-GPR-DERIVATION: 29 tests / 0 failures`; `python3 -B target/p4-system-14/a49-1/hold.py | grep -c 'disagreements 0'` = 1; `bash target/p4-system-14/a49-1/rehearse.sh` `rc=0`, `grep -c 'capture rc=0' target/p4-system-14/a49-1/rehearse.txt` = 23, `grep -c '11 of 11 legs' target/p4-system-14/a49-1/rehearse.txt` = 23, `grep -c '153 files byte-identical, 0 differ' target/p4-system-14/a49-1/rehearse.txt` = 1.
- [x] `.14` a49-1 **NO REGRESSION** — `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 47 planned, 1 not-applicable; 48 case(s), 0 credited, 23 declared, 0 of 0 credit record(s) current; 0 drift, 0 finding(s)`; `DIV-CAPTURE-INPUTS: 79 tests / 0 failures`, `rc=0`; `gate_report --self-test: 28 pass / 0 fail`; `cargo test -q -p semulith-verify` `rc=0`.
- [x] `.14` a49-0 **ROOT CAUSE** — P4-0366 recorded a call on a claim it had not measured: `python3 -B target/p4-system-14/a48-w/census_events.py | grep -c '<fetch'` = 3 spellings, in 4 guests, and three planned requirement statements state a fetch fault, against the record's "one sentence of one requirement".
- [x] `.14` a49-0 **ADDRESSED** — `decision_the-window-that-carries-fetch-faults.md` and `decision_findings-are-the-engineers-to-call.md`; `grep -c 'capture rc=0' target/p4-system-14/a49-0/prototype.txt` = 23, `grep -c '10 of 10 legs' target/p4-system-14/a49-0/prototype.txt` = 23, `grep -c '171 files byte-identical, 0 differ' target/p4-system-14/a49-0/prototype.txt` = 1.
- [x] `.14` a49-0 **NO REGRESSION** — nothing pinned moved: `git diff --name-only HEAD -- scripts schema evidence profiles | wc -l` = 0; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `19 credit(s), 19 current, 0 lapsed`.

