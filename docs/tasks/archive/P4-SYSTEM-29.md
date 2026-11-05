# P4-SYSTEM ordinary history — part 29

Ordinary, directly readable task history: the complete records of the closed `.14` units
a43c-4, a43c-5 and a43d-2, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0353` on top of commit `0cbc0f42bd57a0539f758e6d3aedb6a565a11b93`
(4 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a43c-1 … a43c-3 and their rows are in part 28,
the earlier ones in parts 13–27. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a43e-c1, SEMULITH-P4-0353.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a43d-2 | 3571 | `a055e9c9524e73cd5f438026e1fdb961ce8f4c6f95cb986888e2ca11baea6e3f` |
| record a43c-5 | 2574 | `71a3ea7f830b51a87724606cc3c7b6a178ce5fb206d8588272ea3ce12939fef8` |
| record a43c-4 | 3144 | `f31b6acd7fa1f8cd67cdac0acf2bb86908d85dd1da109963dcb9469f113d91ed` |
| acceptance rows a43d-2–a43c-4 | 3656 | `680b4e891fdf5cc49627105622b4b4eab3d73e208695c58c7b961c39df3f45b8` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-29.md)   # a span, by its line range
```

<a id="a43d-2"></a>

### .14 a43d-2 / SEMULITH-P4-0346: the SSTC case designed, delivery no longer named out, and its normative statements retained (completed)

Feature 1 of 5 after XTASK-0078. **The route:** ZICNTR's. Five units: this one; a43d-3, the program, its case, its overlay, the family's re-derivation; a43d-4, the declarations; a43d-5, the capture once, with the effect; a43d-6, the reviews and the credit (G-STATE 4 of 4). **What changes from a43d-1:** it named delivery, scheduled time and suppression out, because the override had no timer source. On the case's own configuration the reference has one, so they are in. **Measured on a draft (target/p4-system-14/a43d-2/draft: `gen_program.py`, `sstc-timer.s`, `run.py`, 192 instructions, 315 steps, 622 fetches):** under the configuration ZICNTR's case renders, `AGREE 315 declared steps`; under the profile override, `DIVERGE step 8 (rdtime x5): Sail {}, expectations {'x5': 8}`, a declared property's step. The spec-side author needed no change (it delivers interrupts already), and neither did any pinned tool. It witnesses: M access with both gates clear; all 64 bits; S refused with TM clear, with STCE clear and with either alone, `rd` kept; U refused; the kernel programming its own timer; `sip.STIP` below and at the compare, unsigned; five suppressions (below the compare, STIE clear, SIE clear in S, delegated and in M, STCE clear); delivery to S from S (`scause` `0x8000000000000005`, `sepc` the next instruction, SPP 1) and from U with SIE clear (SPP 0), and to M when not delegated; a schedule 8 ticks out landing after 5 of 12 counted instructions; acknowledgement by writing a compare above `time`. The last instruction of the main body is a spin no run reaches under the case's configuration, because the first draft's override run fell into a handler, `sret` faulted on fetch, and `compare_observations` refuses a missing row, which would have refused the effect record.
**Decisions.** (1) A new program; `sstc.s` stays in the corpus, uncredited, its witnesses all re-witnessed here. (2) The exact boundary is not a latency claim: "If the result of this comparison changes, it is guaranteed to be reflected in STIP eventually, but not necessarily immediately." The scheduled delivery is what both producers do on this configuration, and the limitations will say so; an explicit CSR write is different, since the conditions "must also be evaluated immediately following" it. (3) The control: boundary 172, `sip` below an all-ones compare, expected 0, the wrong value 32, what a signed comparison would read: the statement says "treating the values as unsigned integers". **Retained:** `RVP-SSTC-STATEMENTS` (§12.1, the normative input), `RVP-STIMECMP-STATEMENTS` (§11.1.1.3, §11.1.1.12), `RVP-STCE-STATEMENTS` (§2.1.1.9, §2.1.1.18). The tool gains two selection shapes: the Sstc chapter anchors nothing, and three statements anchor a whole paragraph. `materials/RVP_SSTC_RETENTION.md` records the terms. **Found by a control (§15):** the first draft computed `inner` from the page, so with `closing-span` omitted a later markup check still refused, and that guard's RED read 0 failures; `inner` is now cut from the quoted span, and the omission fires again. 19 → 21 tests, `unique-statement` 1 → 2, `span-markup` 7 → 8, `retained-pin` 4 → 7 (three more rows), re-pinned in PROFILE-CONSISTENCY. Section numbers are read from the pinned pages' headings (`stimecmp` §11.1.1.12, `scause` §11.1.1.8). Nothing a case pins moved; the four credits stay current. Book: the references page. Next: a43d-3.

<a id="a43c-5"></a>

### .14 a43c-5 / SEMULITH-P4-0345: the reviews read the ZICNTR case and `REQ-D-ZICNTR` is credited `implemented` — G-STATE 3 of 4 (completed)

Feature 5 of 5 after XTASK-0077: the turn is XTASK.13 b5, next. **The reviews.** `RETAINED_CAPTURES` names the case (declared 86a35987, captured e5814f18, `723c2967…`, 24,162 B). `python3 -B scripts/review_div_method.py --case rv64gc-zicntr-v1`:
`satisfied`, 88 authenticated files, 1,303,183 B, snapshot 207,186 B, 1,384,386 B charged of 134,217,728. `FEATURE_DISPOSITIONS["OB-ZICNTR"]` is the first to name the counter rule, and it reads the rule's three parts honestly: the schedule is the step boundary, a guest count and never host time; the suppression is the trap that retires nothing; nothing is delivered, since no interrupt or wait is scheduled. The privilege and CSR rule applies too. A probe assertion checks that each of its 26 property names is one the case declares.
`python3 -B scripts/review_div_policy.py --every-retained` prints `rv64gc-zicntr-v1: DIV-POLICY: satisfied — 10 of 10 legs satisfied`, and the comparison leg ends `observed effect under the profile override: step 6 (rdcycle x5): Sail {}, expectations {'x5': 6}`. 26 boundary rows, 44 vacuous-coverage witnesses, the control at step 109 x21, `risk high` through its five conditions, the 13 rd-kept properties executed. No change to the review itself: the second case through the `implementation-defined` branch needed none.
**The credit.** `CR-D-ZICNTR-1` in `credits.sexp`, `authority review`: the measured record, the receipt (`62e4ba5e…`, 7,019 B), the policy pinned, `RVI-ZICNTR-STATEMENTS` and `RVP-COUNTEREN-STATEMENTS` retained, seven limitations. `implementation_status implemented` on `REQ-D-ZICNTR`. `decision_req-d-zicntr-credited-implemented.md` (new, INDEX, KNOWLEDGE_MAP). Measured: `REQUIREMENT-STATUS: … 44 planned, 4 implemented; 8 case(s), 4 credited, 0 declared, 4 of 4 credit record(s) current; 0 drift`; `CREDIT-RECORDS: … 4 current, 0 lapsed`. GS: `3 of 4 state requirements implemented`, 3 of 10 axes open.
**What the credit does not claim is in its record:** a write through `mcycle` or `minstret`, Zihpm's absence, rate and progress semantics, a CLINT or any device, timer delivery. `REQ-D-PRIV-MODES`, its dependency, stays `planned`. No dossier copy, by the director's ruling. Containment: the five closed CSR-SET records a43b-3d … a43b-3h and their rows moved verbatim to archive part 27. Book: policy page (the leg table and the counter rule), method, division, status pages. Next: XTASK.13 b5, then SSTC.

<a id="a43c-4"></a>

### .14 a43c-4 / SEMULITH-P4-0344: the ZICNTR case captured exactly once, and its configuration's effect retained (completed)

Feature 4 of 5 after XTASK-0077. **The capture.** `target/p4-system-14/a43c-4/capture-when-quiet.sh` ran it once, never retried, after 190 minutes' wait and three consecutive quiet minutes to 03:39Z
(no stitchcad or specforge process, 1-minute load 5.45, 5.03, 5.64: `rv64gc-zicntr-v1/wait.log`) and its guards: a clean tracked tree; no frozen path moved
(`git diff --name-only 86a35987 HEAD` ∩ the 91 frozen paths = ∅, the one commit since being the cleanup's); the declarations equal to their regeneration; `--preflight-only` `ready`.
`retain_div_capture.py --case rv64gc-zicntr-v1 --declaration-commit 86a35987…` ran 1.4 s: three zero-exit processes; baseline and repeat AGREE over 292 declared steps; the control DIVERGE at its declared
step 109, `addi x21, x20, 0`, Sail x21 = 21, the expectation 102. `complete_canonical_capture` true, qualification false, all nine findings matched or
satisfied, 25,174,439 B charged of 134,217,728. 14 files retained: three traces of 26,277 B, byte-identical (`cmp`), three stdout streams identical, each stderr
printing its own trace's name; the measured record 24,162 B (`723c2967…`), `verification.json` 7,019 B (`62e4ba5e…`). The family holds all 177 files, 1,318,561 B.
`REQUIREMENT-STATUS: … 8 case(s), 3 credited, 0 declared`: the case `pending`, the three credits current. Re-stated: the input probe's member count (163 → 177), the
status probe's row. As at a43b-3f, the retained-capture row moves with the reviews (a43c-5): a row names its capture commit, which is this commit.

**The observed effect.** `scripts/measure_config_effect.py --case rv64gc-zicntr-v1` ran the same guest through the same pinned binary under the profile override, exactly once, and retained the raw trace
(`profiles/rv64gc-lab-v0/reference/rv64gc-zicntr-v1.effect.trace`, 27,617 B, `896814f3…`) and what ran by digest (`.effect.sexp`, 760 B). It printed `step 6 (rdcycle x5): Sail {}, expectations {'x5': 6}`, a43c-1's draft result
now on retained bytes. The alternative's digest is CSR-SET's, `666d9373…`. Diffing the raw traces: identical through line 12, then at line 13 the case's `x5 <- 0x0000000000000006` against `trapping from M to M to handle illegal-instruction`.
The record carries no verdict; a43c-5's review re-derives it. `scripts/probe_config_effect.py`'s retained-record test now judges every retained effect (`RETAINED`, one subtest per case): still 10 tests, and all nine pinned omission results re-measured unchanged (`profile-config` still 2 failures, both in synthetic controls: that mutation changes only what `measure` hands the process, and the retained test runs none), so `check_profile_consistency.rs` needs no change. The new row fired RED three ways in memory: a wrong step, value and register, each `FAILED (failures=1)` (target/p4-system-14/a43c-4/retained-red.txt).
Book: the division page (the capture's table), the references page (the effect), status and prepared-inputs pages. Next: a43c-5, the reviews and the credit, G-STATE 3 of 4.

<a id="acceptance-rows-a43d-2-to-a43c-4"></a>

## acceptance-rows-a43d-2-to-a43c-4

- [x] `.14` a43d-2 **ROOT CAUSE** — SSTC had no design that could witness delivery, and its statements were not retained: at 76d7649c `git ls-files 'profiles/*/retained/*stimecmp*' | wc -l` = 0, `grep -c 'opening:' scripts/retain_statements.py` = 0, and a43d-1's record names delivery out because the override has no timer source.
- [x] `.14` a43d-2 **ADDRESSED** — `python3 -B scripts/retain_statements.py --verify | grep -c matched` = 6, `rc=0`; target/p4-system-14/a43d-2/draft on the draft: `case-config rc 0 AGREE 315 declared steps`, `profile-override rc 0 DIVERGE step 8 (rdtime x5)`.
- [x] `.14` a43d-2 **NO REGRESSION** — `python3 -B scripts/probe_statement_retention.py` → `STATEMENT-RETENTION: 21 tests / 0 failures / 0 errors`, all nine omissions RED in both modes (target/p4-system-14/a43d-2/retention-mutations.txt); `--emit` of the older excerpts `cmp` silent against their retained bytes; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `4 credit(s), 4 current, 0 lapsed`.
- [x] `.14` a43c-5 **ROOT CAUSE** — a capture credits nothing by itself: at e5814f18 `python3 -B scripts/requirement_status.py` `rc=0` read `45 planned, 3 implemented; 8 case(s), 3 credited`, `python3 -B scripts/review_div_method.py --case rv64gc-zicntr-v1` read `unsupported` (no `RETAINED_CAPTURES` row) and the policy review had no `OB-ZICNTR` disposition, which stays pending and is never inferred.
- [x] `.14` a43c-5 **ADDRESSED** — `python3 -B scripts/review_div_policy.py --every-retained` `rc=0`, `rv64gc-zicntr-v1: DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-D-ZICNTR-1`; `python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0` → `44 planned, 4 implemented; 8 case(s), 4 credited, 0 declared, 4 of 4 credit record(s) current; 0 drift`; GS `3 of 4 state requirements implemented`.
- [x] `.14` a43c-5 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `4 credit(s), 4 current, 0 lapsed`, the other three lines unchanged; `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DIV-METHOD: 22 tests / 0 failures`, `DIV-POLICY-PROBE: 48 tests / 0 failures`, `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`; the 27 policy seams still RED in both modes.
- [x] `.14` a43c-4 **ROOT CAUSE** — two facts were missing: at 98f1134c `git ls-files evidence/rv64gc-zicntr-v1 | wc -l` = 8 of its 22 slots (declarations, no observations), and `git ls-files 'profiles/*/reference/rv64gc-zicntr-v1.effect.*' | wc -l` = 0, so the case's "observed effect" stood only on a43c-1's draft measurement.
- [x] `.14` a43c-4 **ADDRESSED** — `python3 -B scripts/retain_div_capture.py --case rv64gc-zicntr-v1 --declaration-commit 86a35987…` `rc=0`, once, baseline and repeat AGREE, control DIVERGE at 109, complete, qualification false (target/p4-system-14/a43c-4/rv64gc-zicntr-v1/capture.json); `cmp` baseline.trace against repeat.trace and control.trace silent; `python3 -B scripts/measure_config_effect.py --case rv64gc-zicntr-v1` printed `step 6 (rdcycle x5): Sail {}, expectations {'x5': 6}`, `rc=0`; `python3 -B scripts/probe_config_effect.py` → `CONFIG-EFFECT: 10 tests / 0 failures / 0 errors`, nine omissions RED.
- [x] `.14` a43c-4 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `3 credit(s), 3 current, 0 lapsed`; no pinned input moved: `git diff --name-only 86a35987 HEAD` ∩ the 91 frozen paths = ∅ at the capture, and `grep -c 'measure_config_effect\|probe_config_effect' evidence/rv64gc-zicntr-v1/dependencies.sexp` = 0; `DIV-CAPTURE-INPUTS: 64 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`.

