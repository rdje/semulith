# P4-SYSTEM ordinary history — part 32

Ordinary, directly readable task history: the complete records of the closed `.14` units
a43e-3, a43e-4 and a43e-5, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0362` on top of commit `8a40a2495533bdb90d16c8eb283229122097bb8b`
(4 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a45-1, a43e-c1, a43e-2, a43e-1 and their rows are in part 31,
the earlier ones in parts 13–30. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a46-4, SEMULITH-P4-0362.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a43e-5 | 4122 | `029578a1bf48290046e1bffca4e38fe846617cd9d8d79cd7316eced76c60a59b` |
| record a43e-4 | 4233 | `8f493aa49d17ed89da71dab43d2e52082e4946902a995e7e0de823657b181c70` |
| record a43e-3 | 3155 | `7e0ffb633c4f463dc07c86c8242b952cfb08137bad8589a2dce046148d8aba4a` |
| acceptance rows a43e-5–a43e-3 | 4622 | `f7c7f1f73a74ca3565d9f6467365adc0d76dbe7107415834e8796b6d8c83cf93` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-32.md)   # a span, by its line range
```

<a id="a43e-5"></a>

### .14 a43e-5 / SEMULITH-P4-0357: five credits, `REQ-D-SSTC` `implemented`, G-STATE 4 of 4, and G-TRACE read from `evidence/` — the window closed (completed)

Feature 2 of 5 after XTASK-0080. **The reviews.** `RETAINED_CAPTURES` names the five (declared 18a09566, captured 178f9c6c); `review_div_policy.CASE_ID` is v6.

| Case | Method: authenticated files, bytes, snapshot | Policy | Credit | Receipt |
| --- | --- | --- | --- | --- |
| `rv64gc-m-forms-v6` | 88, 1,019,799 B, 40,438 B | 10 of 10 | `CR-GC-M-4` | 7,021 B |
| `rv64gc-xlen-forms-v3` | 88, 1,014,785 B, 35,646 B | 10 of 10 | `CR-D-XLEN-3` | 7,061 B |
| `rv64gc-csr-set-v2` | 88, 1,144,922 B, 141,763 B | 10 of 10 | `CR-D-CSR-SET-2` | 7,047 B |
| `rv64gc-zicntr-v2` | 88, 1,219,908 B, 207,186 B | 10 of 10 | `CR-D-ZICNTR-2` | 7,016 B |
| `rv64gc-sstc-v1` | 88, 1,228,962 B, 216,358 B | 10 of 10 | `CR-D-SSTC-1` | 6,997 B |

Each authenticated total is 83,275 B below its predecessor's, or 82,729 B for XLEN with its 546 B of derivation prose. The manifests shed the report generator (a43e-1): the 67 children net −83,282 B (`check/authenticated-drop.txt`), and the other authenticated files moved +7 B. **`OB-SSTC`'s disposition** is the first to witness all of the counter rule: it names every one of the 39 properties under its part, and the probe holds that set equal to the case's declaration, so a witness cannot go unread. The review itself needed no change, the third case through the `implementation-defined` branch. The comparison leg ends `observed effect under the profile override: step 8 (rdtime x5): Sail {}, expectations {'x5': 8}`.

**The credits.** `profiles/rv64gc-lab-v0/credits.sexp` re-created, `authority review`, each pinning its measured record, receipt and the policy (`85296cf7…`, unmoved); the four keep their predecessors' limitations, and `CR-D-SSTC-1` carries six, its retained sources the three SSTC statements. `implementation_status implemented` on the five, moving with them. `decision_req-d-sstc-credited-implemented.md` (new, INDEX, KNOWLEDGE_MAP), a re-credit section in the other four. Measured: `CREDIT-RECORDS: … 5 credit(s), 5 current, 0 lapsed`; `REQUIREMENT-STATUS: … 42 planned, 5 implemented, 1 not-applicable; 13 case(s), 5 credited, 0 declared, 5 of 5 credit record(s) current; 0 drift, 0 finding(s)`.

**G-TRACE from `evidence/`, the ruling's second half** (`decision_dossier-copies-retire-at-the-next-window.md`). `gate_report.py` takes each current credit's case as an experiment; the record stays in `evidence/`, and a credit authenticates its pins on every read, so a lapse is no evidence and there is no copy to fall back on. The ruling also said `G-TRACE` lists every credited case, which until now was a promise: a credit with no row now keeps the axis open and names the case. Four arms (24 → 28), `gate_report --self-test: 28 pass / 0 fail`; each guard omitted in memory misses its arm, 4, 1 and 1 (`check/gate-report-red.txt`). `gate.sexp`: five rows; the open items on G-STATE and G-TRACE gone; G-OBLIGATIONS re-stated. GS: `Open axes (2 of 10): G-OBLIGATIONS, G-RELEASE`, `4 of 4 state requirements implemented`.

**The window's own claim, measured.** "Editing a report should never lapse evidence": this commit edits `gate_report.py`, and all five stay current. `grep -c gate_report evidence/rv64gc-sstc-v1/dependencies.sexp` = 0.

Re-stated: the method probe's real-tree rows, the policy probe's cases and SSTC's assertions, the status probe (42 / 5, each credited case), the dossier probe (the five qualify, their predecessors do not), the runtime-root probe's module list (`credit_records`, `check_sexp_schema` now local to the report; it failed 6 of 6 until they were), the property probe's `derived-status` pin 2 → 37 (`36 tests / 37 failures` measured, as at a43b-2e). The window ran a43e-1 … a43e-5 on 2026-11-05 (`decision_sstc-delivery-needs-the-pinned-window.md`, Closed). Book: status, policy, method, division and references pages. Evidence: `target/p4-system-14/a43e-5`. Next: G-OBLIGATIONS' 42 `planned` requirements, feature 3 of 5; `ARTIFACT-CLEANUP.37` once due.

<a id="a43e-4"></a>

### .14 a43e-4 / SEMULITH-P4-0356: the window's five cases captured exactly once each, and three effects retained (completed)

Feature 1 of 5 after XTASK-0080. **The capture.** `target/p4-system-14/a43e-4/capture-when-quiet.sh` ran 107 one-minute checks without three quiet ones in a row (a sibling's verification; `run/wait.log`). Asked for a quiet window, the director answered "try runnung". I stopped the waiter and ran `capture-now.sh` from the same guards: a clean tracked tree; no frozen path moved (`git diff --name-only 18a09566 HEAD` ∩ the 199 frozen paths = ∅, the one commit since being XTASK-0080); the declarations equal to their regeneration; `--preflight-only` `ready`. The sibling wait went, and two checks took its place before each case: the 1-minute load below 8, and 50 of 50 children spawned and reaped the collector's way. **So this was not a quiet host:** ten sibling processes ran throughout, at load 4.71 to 5.13.

| Case | Baseline, repeat | Control | Ran | Measured | Receipt | Trace |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-m-forms-v6` | AGREE, 33 steps | DIVERGE at 12, x15 | 1.2 s | 16,943 B `7998edb1…` | 7,021 B | 2,794 B |
| `rv64gc-xlen-forms-v3` | AGREE, 25 steps | DIVERGE at 24, x31 | 1.2 s | 14,980 B `db272820…` | 7,061 B | 2,260 B |
| `rv64gc-csr-set-v2` | AGREE, 157 steps | DIVERGE at 130, x28 | 1.4 s | 27,347 B `d8f18593…` | 7,047 B | 13,833 B |
| `rv64gc-zicntr-v2` | AGREE, 292 steps | DIVERGE at 109, x21 | 1.5 s | 24,163 B `c2b55c23…` | 7,016 B | 26,277 B |
| `rv64gc-sstc-v1` | AGREE, 315 steps | DIVERGE at 172, x11 | 1.5 s | 22,241 B `801b9383…` | 6,997 B | 26,417 B |

Each ran once, never retried: three zero-exit processes, `complete_canonical_capture` true, qualification false, all nine findings matched or satisfied, and each case's three traces byte-identical. The family holds all 287 files, 2,492,207 B.

**What the prototype left open.** All 12 traces and 12 stdout streams of the four are byte-identical to their predecessors' (`check/compare.txt`), and each of the 12 stderr streams equals its predecessor's with the case id substituted. With the id substituted, each measured record moved in exactly 10 tokens (`check/measured-diff.txt`): the dependency manifest's digest, 3 stderr digests, 3 receipt digests, `sha256:007f…` → `sha256:ec2a…` as the two expected producers' version (the digest of `scripts/derive_rv64gc_expectations.py`, which a43e-2 edited), and the control reason's one recovered space. XLEN's moved in two more, its two expectation digests, measured at a43e-3.

**The effects.** `scripts/measure_config_effect.py`, exactly once each: `rv64gc-csr-set-v2` `step 34 (csrrs x20, mcycle, x0): Sail {}, expectations {'x20': 34}`; `rv64gc-zicntr-v2` `step 6 (rdcycle x5): Sail {}, expectations {'x5': 6}`; `rv64gc-sstc-v1` `step 8 (rdtime x5): Sail {}, expectations {'x5': 8}`. The first two raw traces are byte-identical to their predecessors' (14,236 B, 27,617 B); SSTC's is 25,773 B, `2b673858…`, and first differs at line 16, where the override traps on `time` before any Sstc behaviour is reached.

**The quiet wait, read (§9).** It is my procedure, not a doctrine, and of its possible reasons only one holds: `start_new_session` or the reap answering EPERM under load would burn a case id. The bytes do not depend on load, and the captures use 1.5 s of a 30 s limit. For later captures `capture-now.sh`'s guard replaces the wait, which cost 190 minutes at a43c-4 and 107 here against 15 seconds of work (`decision_sstc-delivery-needs-the-pinned-window.md`). One run proves that at load 5, not at load 28, which is why the load guard stays.

Re-stated: the input probe's census (217 → 287), the status probe's rows and counts (`13, 0, 0, 0, 0`), `RETAINED` in the effect probe (five rows). `REQUIREMENT-STATUS: … 13 case(s), 0 credited, 0 declared`: all five `pending`, and nothing credited. As at a43c-4, the retained-capture rows move with the reviews (a43e-5): a row names its capture commit, which is this commit. Book: the division page (the five's table), references (SSTC's effect), status and prepared-inputs pages. Evidence: `target/p4-system-14/a43e-4`. Next: a43e-5, the reviews and five credits.

<a id="a43e-3"></a>

### .14 a43e-3 / SEMULITH-P4-0355: the window's five cases declared on contract v3, committed before their captures (completed)

Feature 4 of 5 after XTASK-0079; PNT resumed on the director's word, 2026-11-05 ("Go in full PNT mode until all work is exhausted."). Nothing is captured or credited here, and no retained case moved. **The four re-declared.** `rv64gc-m-forms-v6`, `rv64gc-xlen-forms-v3`, `rv64gc-csr-set-v2`, `rv64gc-zicntr-v2`, each its predecessor with the id, the contract (`rv64gc-lab-env-v3`, version 3) and one fix: the control reason's lost space (`boundary 109`, §15, the a43e-c1 family, which PROSE-SPACING does not read here). The authority moved in nothing for all four, so contract v3 touched none of their requirements. Prepared pins: three cases byte for byte; `xlen-forms-v3`'s guest and configuration too, its two expectations 273 B longer each, because a43e-2 resolved `{new}`: 21 lines moved, each only in its derivation prose, no value. **SSTC.** `rv64gc-sstc-v1` from its held draft, which now reads v3: REQ-D-SSTC / OB-SSTC on RVP-SSTC §12.1, 39 witnesses, 17 boundary rows, every value held to the derivation by the draft, control `compare-read-as-signed` at x11 of boundary 172, its own overlay rendering CSR-SET's 8,748 B configuration, baseline 53,750 B, control 51,552 B. **The declarations.** `capture_div.py --declare` for each, written exclusively from its output and equal to their regeneration: planned 14,953 to 27,317 B; dependencies 15,173 to 15,182 B, each **67** children with no report or book generator (the window's rider, on real manifests); authorities 17,721 to 17,762 B. The manifests differ from v6's in the case's own declaration and its normative child alone. "quotient" reaches only v6's record. This commit is the declaration commit a43e-4 names. **The family's eighth re-derivation** (`decision_evidence-family-two-cases.md`, Addendum a43e-3): 287 files, 172 MiB, `retention_limits()` 179,769,344 B, 217 present. `evidence/README.md` dropped a column every retired row filled alike to hold five more within 4,096 B (4,084 B). **Measured beyond the draft:** the input probe enumerates its per-case classes in `main`, twice, so a new class ran nowhere until both lists named it (64 tests read green; 79 once they did; `SstcCaseInputTests`); PROFILE-CONSISTENCY's two arms pin the new count. **Found by the gate:** the first chain refused on `RED case declarations delivery-render`, expecting 1 failure and reading 2: SSTC is the first real case with a delivered boundary, so the byte-for-byte round trip over every declaration now catches that mutation as well as the synthetic test does. The check got stronger, and the arm states it. Re-stated: the input probe's census and tables, the case probe's planned population, the property probe's ids, the status probe's rows and counts. `REQUIREMENT-STATUS: … 13 case(s), 0 credited, 5 declared … 0 drift`. **Frozen until the captures:** each case's 67 children and the 13 authority views. Book: prepared inputs, references, requirement status. Evidence: `target/p4-system-14/a43e-3`. Next: a43e-4, each captured exactly once on a quiet host.

<a id="acceptance-rows-a43e-5-to-a43e-3"></a>

## acceptance-rows-a43e-5-to-a43e-3

- [x] `.14` a43e-5 **ROOT CAUSE** — a capture credits nothing by itself, and nothing could read a credit from `evidence/`: at 178f9c6c `git ls-tree 178f9c6c profiles/rv64gc-lab-v0/credits.sexp | wc -l` = 0, `git show 178f9c6c:scripts/review_div_method.py | grep -c rv64gc-sstc-v1` = 0 (so the review read `refused — unsupported: no reviewed capture`), `git show 178f9c6c:scripts/review_div_policy.py | grep -c '"OB-SSTC"'` = 0, and `git show 178f9c6c:scripts/gate_report.py | grep -c current_credits` = 0, its `G-TRACE` reader naming only `references.sexp`, which holds no copy since a43e-1.
- [x] `.14` a43e-5 **ADDRESSED** — `python3 -B scripts/review_div_policy.py --every-retained` `rc=0`, five lines `DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by …`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `5 credit(s), 5 current, 0 lapsed`; `python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0` → `42 planned, 5 implemented, 1 not-applicable; 13 case(s), 5 credited, 0 declared, 5 of 5 credit record(s) current; 0 drift, 0 finding(s)`; GS `4 of 4 state requirements implemented`, `Open axes (2 of 10): G-OBLIGATIONS, G-RELEASE`.
- [x] `.14` a43e-5 **NO REGRESSION** — `gate_report --self-test: 28 pass / 0 fail`, each new guard omitted misses its arm (target/p4-system-14/a43e-5/check/gate-report-red.txt); `DIV-METHOD: 22 tests / 0 failures`, `DIV-POLICY-PROBE: 48 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`, `GATE-RUNTIME-ROOT: 6 tests / 0 failures`; no pinned input moved: `git diff --name-only 178f9c6c --cached` ∩ the 199 frozen paths = `profiles/rv64gc-lab-v0/requirements.sexp` alone, its status field, which no authority view reads, and the five stay current over it.
- [x] `.14` a43e-4 **ROOT CAUSE** — the window's five held no observation: at 8784edfe `git ls-files evidence/rv64gc-sstc-v1 | wc -l` = 8 of its 22 slots, the same for the other four, and `git ls-files 'profiles/*/reference/rv64gc-sstc-v1.effect.*' | wc -l` = 0, so SSTC's effect stood only on a draft measurement and the four's byte-identical traces only on a prediction.
- [x] `.14` a43e-4 **ADDRESSED** — `python3 -B scripts/retain_div_capture.py --case <each> --declaration-commit 18a09566…` `rc=0`, once each (target/p4-system-14/a43e-4/run/*/capture.json), baseline and repeat AGREE, each control DIVERGE at its declared step (12, 24, 130, 109, 172), complete, qualification false; `python3 -B scripts/measure_config_effect.py` `rc=0` three times (check/effect-*.txt); `CONFIG-EFFECT: 10 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS: ok (… 13 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift, 0 finding(s))`.
- [x] `.14` a43e-4 **NO REGRESSION** — the four's 24 traces and stdout streams `cmp` silent against their predecessors' (check/compare.txt); no pinned input moved: `git diff --name-only 18a09566 HEAD` ∩ the 199 frozen paths = ∅ at the capture, and `grep -c 'measure_config_effect\|probe_config_effect' evidence/rv64gc-sstc-v1/dependencies.sexp` = 0; `DIV-CAPTURE-INPUTS: 79 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`.
- [x] `.14` a43e-3 **ROOT CAUSE** — the window's cases did not exist, and the family could not hold them: `python3 -B scripts/probe_div_capture_inputs.py` at 1104889b pins 177 files; thirteen cases need `len(retention_limits())` 287, 179,769,344 B. `git grep -c '{new}'` on `evidence/rv64gc-xlen-forms-v2/baseline.expected.sexp` 21: why xlen's pins alone moved.
- [x] `.14` a43e-3 **ADDRESSED** — `DIV-CAPTURE-INPUTS: 79 tests / 0 failures / 0 errors`, `actual-layout` `79 tests / 6 failures`; `MATCHED-GPR-CASE: 10 tests / 0 failures`; `MATCHED-GPR-PROPERTY: 36 tests / 0 failures`; `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`; `REQUIREMENT-STATUS: ok (… 13 case(s), 0 credited, 5 declared … 0 drift`; `prepare_div_inputs.py --verify` `rc=0` on all five, and each `capture_div.py --declare` equals the committed bytes.
- [x] `.14` a43e-3 **NO REGRESSION** — RED: a byte appended to `evidence/rv64gc-sstc-v1/control.expected.sexp`, `--verify` `rc=1`; the control id altered, `probe_matched_gpr_case.py` `rc=1` naming both values; each restored byte-exact, `rc=0` (target/p4-system-14/a43e-3/red-verify.txt, red-case.txt). `DIV-AUTHORITIES: 19 tests`, `DIV-COMMAND: 20 tests`, `EXPERIMENT-GRAPH: 74 pass / 0 fail`, `CONFIG-EFFECT: 10 tests`, `REFERENCE-OVERLAY: 14 tests`, `GATE-RUNTIME-ROOT: 6 tests`, `MATCHED-GPR-DERIVATION: 27 tests`, 0 failures each. The full gate at commit.

