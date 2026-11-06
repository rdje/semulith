# P4-SYSTEM ordinary history — part 34

Ordinary, directly readable task history: the complete records of the closed `.14` units
a47-1 to a47-3 and a48-1, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0370` on top of commit `57544407914f8374faaadc1a756ff9fef8e7f40b`
(5 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a46-4 to a46-0 and their rows are in part 33,
the earlier ones in parts 13–32. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a49-3, SEMULITH-P4-0370.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a48-1 | 3059 | `426e1aca2967f37cbaf9156876903e5328e3f52fd7fc544966bb6a3aa3ef1490` |
| record a47-3 | 2354 | `af7ee6adc1b0adaf63314bede7caf5e62cd65bae06a885665f36ac345cf03754` |
| record a47-2 | 2163 | `1567e9043202cd0cfeac57fd2d5ae0a2067826e6f3a95c04d2805313c17e66a1` |
| record a47-1 | 3152 | `c55d6551918fa09cfefd4f733d669829da0d59147ad292fa737b5aff33857cac` |
| acceptance rows a48-1–a47-1 | 4744 | `7a37ae180354816ad7fee9352937d5a9e2064055e465f7010311a6c6d998dc3e` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-34.md)   # a span, by its line range
```

<a id="a48-1"></a>

### .14 a48-1 / SEMULITH-P4-0366: Batch II-b's four programs and cases, declared before their captures, and what writing them found (completed)

Feature 1 of 5 after XTASK-0082. Nothing is captured or credited, and no retained case moved. **The programs.** `atomics-forms`, `c-forms`, `f-forms` and `d-forms`, new in the corpus, 191 guests. All three producers agree: the spec-side author, the pinned Sail and the backend. **The cases.** Each binds one requirement:

| Case | Requirement | Steps | Witnesses | Control |
| --- | --- | --- | --- | --- |
| `rv64gc-atomics-v1` | `REQ-GC-ATOMICS`, high | 246 | 64 | AMOADD.W's old value at 21, x5: a word not sign-extended |
| `rv64gc-c-forms-v1` | `REQ-GC-C`, medium | 223 | 47 | C.JALR's link at 108, x1: a link at pc + 4 |
| `rv64gc-f-forms-v1` | `REQ-GC-F`, high | 293 | 64 | the read-back at 126, x6: a static RDN ignored |
| `rv64gc-d-forms-v1` | `REQ-GC-D`, high | 326 | 64 | the read-back at 130, x6: a static RUP ignored |

`atomics-forms` runs each AMO at both widths, both aliases, the ordering bits, LR and SC history, an access fault on each, and in S an AMO on an execute-only page: 15, never 13. `c-forms` runs all 37 forms, nine HINTs, two reserved encodings, the all-zero parcel, the all-ones diagnostic, the FS gate, a C form between LR and SC, and two parcels written at run time to a page's end, before an invalid page. `f-forms` and `d-forms` share one generator: rounding, each flag and its accrual, tininess after rounding, NaN rules, clipping, boxing and the FS state. Four new excerpts (`materials/RVI_EXTENSION_RETENTION.md`).

**Rehearsed first, on a throwaway clone, end to end.** Each capture `rc=0`, each repeat byte-identical, each control diverging at its predeclared witness and nowhere else, each 10 of 10 legs with the dispositions this unit's scratch holds for a48-3. It found both faults a real capture would have spent a case id on: the fetch fault below, and no directed boundary row in two of the programs.

**What writing them found** (`decision_obligations-route.md`, "What the `defined` remainder found"). A case cannot carry a fetch fault: a step fetches a word of a length or is a delivery boundary, and that file is pinned. So `REQ-GC-C`'s second-parcel fault stays the corpus guest's, named in the case's limitation, and the boundary goes in at the next window: **raised to the director**. The forms are not the requirement: the first drafts agreed with Sail and missed most of what the statements say. 13 declared values were refused at first, each mine, and fixed before any case existed.

Rolled to archive part 33: a46-0 to a46-4, so this file is at about 113 KiB of its 128 KiB. Re-stated: the input probe's tables and census (`1 + 27 * 22 + 4 * 8`), the case and property probes' populations, the status probe's rows and counts (`31, 19, 4, 19, 19`), `retained-pin` 17. **Frozen until the captures:** each case's 67 children and the 13 authority views. Book: `requirement-status.md`, `prepared-inputs.md`, the generated case table. Next, a48-2: the captures.

<a id="a47-3"></a>

### .14 a47-3 / SEMULITH-P4-0365: Batch II-a credited: five more requirements `implemented`, and a `configuration` requirement that names no form (completed)

Feature 5 of 5 after XTASK-0081: the turn is XTASK.13's PLATFORM-GEN, next. **The reviews.** `RETAINED_CAPTURES` names the five (declared 507c3017, captured 3eb61efd): each `satisfied`, 88 authenticated files, 991,491 B to 1,083,654 B; `--every-retained` prints nineteen lines, each `satisfied — 10 of 10 legs satisfied`. **The rule.** The coverage leg allowed a requirement to name no form only for kind `state`, and `REQ-D-IALIGN-16` is `configuration`. Same reading, same honesty, and the leg says so; an `instruction` or `event` requirement naming no form stays pending. One test, 52 → 53, one seam. **The dispositions.** Five, three of them the first to apply a rule rather than say none does: the privilege, CSR, trap and return rule for `OB-GC-ECALL-EBREAK-V3` and `OB-GC-CSR-ACCESS`, the counter rule for `OB-GC-COUNTERS`, the fetch rule for `OB-IALIGN-16` and `OB-GC-FENCEI`. The policy probe now checks, for every Batch case, that each property a disposition lists is one the case declares.

**The credits.** Five records, `authority review`, 30,620 B of the file's 65,536 B: `CR-D-ECALL-EBREAK-1`, `CR-GC-CSR-ACCESS-1`, `CR-GC-COUNTERS-1`, `CR-GC-FENCEI-1`, `CR-D-IALIGN-16-1`. `decision_batch-ii-a-credited-implemented.md` (new, INDEX, KNOWLEDGE_MAP). Measured: `CREDIT-RECORDS: … 19 credit(s), 19 current, 0 lapsed`; `REQUIREMENT-STATUS: … 28 planned, 19 implemented, 1 not-applicable; 27 case(s), 19 credited, 0 declared, 19 of 19 credit record(s) current; 0 drift, 0 finding(s)`. `gate.sexp`: nineteen `G-TRACE` rows; GS still 2 of 10 open. **A stale claim gone (§15):** `gate.sexp`'s `G-OBLIGATIONS` statement said `REQ-D-ECALL-EBREAK` "remains partial on OQ-5", which `gaps.md` already calls rv64i's question. This profile's requirement of that id is now credited, and says nothing of rv64i's.

Re-stated: the method probe's rows, the policy probe's cases and read-after forms, the status probe (28 / 19), the dossier probe (nineteen qualify). Book: status, policy, method and division pages. Evidence: `target/p4-system-14/a47-3`. Next: XTASK.13's PLATFORM-GEN, then the `defined` remainder, `ATOMICS`, `C`, `F`, `D`, rehearsed first. `ARTIFACT-CLEANUP.37` once due.

<a id="a47-2"></a>

### .14 a47-2 / SEMULITH-P4-0364: Batch II-a captured exactly once each, byte-identical to its rehearsal, after the guard refused once (completed)

Feature 4 of 5 after XTASK-0081. **The capture.** `target/p4-system-14/a47-2/capture.sh`, the same guard: a clean tracked tree, no frozen path moved (`git diff --name-only 507c3017 HEAD` is empty), the declarations equal to their regeneration, `--preflight-only` `ready`, the 1-minute load below 8 and 50 of 50 children spawned and reaped before each case. **Its first attempt refused:** load stayed at 12 to 19 past its ten-minute limit, so it stopped with `host not ready after ten minutes; not capturing`, all five still at 8 files. Re-armed behind a wait for load below 7, it ran at 03:57Z, load 6.64 to 7.03.

| Case | Baseline, repeat | Control | Ran | Measured | Receipt | Trace |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-ecall-ebreak-v1` | AGREE, 116 steps | DIVERGE at 50, x10 | 1.3 s | 17,655 B `61742b70…` | 7,037 B | 10,386 B |
| `rv64gc-csr-access-v1` | AGREE, 66 steps | DIVERGE at 15, x15 | 1.2 s | 15,911 B `b6f7c30b…` | 7,050 B | 6,106 B |
| `rv64gc-counters-v1` | AGREE, 84 steps | DIVERGE at 23, x21 | 1.2 s | 12,150 B `76d4a37b…` | 6,951 B | 7,198 B |
| `rv64gc-fencei-v1` | AGREE, 10 steps | DIVERGE at 9, x2 | 1.1 s | 10,225 B `9fc3b954…` | 6,929 B | 732 B |
| `rv64gc-ialign-16-v1` | AGREE, 11 steps | DIVERGE at 3, x3 | 1.1 s | 11,368 B `bad8453d…` | 6,991 B | 854 B |

Each ran once: three zero-exit processes, complete, qualification false, all nine findings matched or satisfied, each case's three traces byte-identical. All ten compared files of all five match the rehearsal's (`check/compare.txt`). The family holds 595 files, 4,173,028 B. `REQUIREMENT-STATUS: … 27 case(s), 14 credited, 0 declared`: all five `pending`, the fourteen credits current. Re-stated: the input probe's census (525 → 595), the status probe's rows and counts (`27, 14, 0, 14, 14`). Book: the division page, status and prepared-inputs pages. Evidence: `target/p4-system-14/a47-2`. Next: a47-3, the coverage rule for a `configuration` requirement, five dispositions and five credits.

<a id="a47-1"></a>

### .14 a47-1 / SEMULITH-P4-0363: Batch II-a's five programs and cases, declared before their captures, and what reading them found (completed)

Feature 3 of 5 after XTASK-0081. Nothing is captured or credited, and no retained case moved. **The programs.** `ecall-ebreak`, `csr-access`, `counters-reads`, `fencei-forms` and `ialign-16`, new in the corpus, 187 guests. All three producers agree: the spec-side author, the lab engine (34 `every_` tests `ok`), and the pinned Sail, `AGREE` on all five, 287 declared steps between them, the first run.

| Case | Requirement | Steps | Witnesses | Control |
| --- | --- | --- | --- | --- |
| `rv64gc-ecall-ebreak-v1` | `REQ-D-ECALL-EBREAK`, high | 116 | 25 | M's handler at 50, x10: a cause that does not name its mode |
| `rv64gc-csr-access-v1` | `REQ-GC-CSR-ACCESS`, high | 66 | 21 | the read-back at 15, x15: an immediate sign-extended |
| `rv64gc-counters-v1` | `REQ-GC-COUNTERS`, medium | 84 | 8 | the copy at 23, x21: a refused read that committed |
| `rv64gc-fencei-v1` | `REQ-GC-FENCEI`, low | 10 | 2 | the patched word at 9, x2: a stale fetch |
| `rv64gc-ialign-16-v1` | `REQ-D-IALIGN-16`, medium | 11 | 6 | the landing at 3, x3: a target rounded to a word |

`ecall-ebreak` runs every cause from M, S and U, with `medeleg` choosing the handler, a delegated cause taken in M staying in M, and an illegal instruction ending delegation partway. `counters-reads` carries its own overlay: the profile's override has no Zicntr. Witness values came from the statements and from each program's layout, computed by a small builder, and none disagreed with the derivation. **Rehearsed first** (`target/p4-system-14/a47-1/rehearse.sh`): five captures, each control where declared, all 10 of 10. **Statements:** four excerpts (`materials/RVI_SYSTEM_RETENTION.md`), `retained-pin` 9 → 13, measured.

**What reading them found** (`decision_obligations-route.md`, "What Batch II found"). Ten of the 28 are `implementation-defined`, a row measured against a case's own configuration, while for them the override is the selection; the pinned Sail has a real switch for seven, so a behaviour-changing control exists, and the tool must learn to read a declared alternative. The three with none join the ruling: 17, not 14. A `configuration` requirement naming no form could never satisfy the coverage leg; that lands with these credits (a47-3). **A false finding, fixed here (§15):** a declared case guessed its profile from any catalogue naming its requirement, and `REQ-D-ECALL-EBREAK` is in both `rv64i` and `rv64gc` with different obligations, so `REQUIREMENT-STATUS` raised a finding on `rv64i`. `_declared_profile` reads the case's own `case.sexp`. One test, 22 → 23, one seam, `1 tests / 1 failures`.

Re-stated: the input probe's tables and census (`1 + 22 * 22 + 5 * 8`), the case and property probes' populations, the status probe's rows and counts (`27, 14, 5, 14, 14`). **Frozen until the captures:** each case's 67 children and the 13 authority views. Book: requirement status, prepared inputs; the retained cases regenerate. Evidence: `target/p4-system-14/a47-1`. Next: a47-2, each captured once.

<a id="acceptance-rows-a48-1-to-a47-1"></a>

## acceptance-rows-a48-1-to-a47-1

- [x] `.14` a48-1 **ROOT CAUSE** — no case existed for the `defined` remainder: at 2d1704e6 `git ls-files 'evidence/rv64gc-atomics-*' | wc -l` = 0, and the same for `rv64gc-c-forms`, `rv64gc-f-forms` and `rv64gc-d-forms`. Located by `python3 -B target/p4-system-14/a48-1/draft.py`, whose first drafts `AGREE`d while the requirement statements named behaviour no row reached.
- [x] `.14` a48-1 **ADDRESSED** — `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 28 planned, 19 implemented, 1 not-applicable; 31 case(s), 19 credited, 4 declared, 19 of 19 credit record(s) current; 0 drift, 0 finding(s))`; `DIV-CAPTURE-INPUTS: 79 tests / 0 failures`, `rc=0`; `python3 -B target/p4-system-14/a48-1/hold.py | grep -c 'disagreements 0'` = 1; `cargo test -q -p semulith-verify` `rc=0`.
- [x] `.14` a48-1 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `19 credit(s), 19 current, 0 lapsed`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures`; `STATEMENT-RETENTION: 21 tests / 0 failures`; `MATCHED-GPR-CASE: 10 tests / 0 failures`; `MATCHED-GPR-PROPERTY: 36 tests / 0 failures`; the rehearsal's `bash target/p4-system-14/a48-1/rehearse.sh` `rc=0`, four `capture rc=0`, 19 credits current.
- [x] `.14` a47-3 **ROOT CAUSE** — captures credit nothing, and `REQ-D-IALIGN-16` could not satisfy the coverage leg: at 3eb61efd `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` reads `14 credit(s)`, and `git show 3eb61efd:scripts/review_div_policy.py | grep -c '"configuration"'` = 0, so a `configuration` requirement naming no form stayed pending whatever it witnessed.
- [x] `.14` a47-3 **ADDRESSED** — `python3 -B scripts/review_div_policy.py --every-retained` `rc=0`, nineteen lines `satisfied — 10 of 10 legs satisfied; credited by …`; `CREDIT-RECORDS: … 19 credit(s), 19 current, 0 lapsed`; `REQUIREMENT-STATUS: ok (… 28 planned, 19 implemented, 1 not-applicable; 27 case(s), 19 credited, 0 declared, 19 of 19 credit record(s) current; 0 drift, 0 finding(s))`.
- [x] `.14` a47-3 **NO REGRESSION** — `DIV-POLICY-PROBE: 53 tests / 0 failures`, the new seam `1 tests / 1 failures` and `state-vacuous` still so; `DIV-METHOD: 22 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures`, `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`; `gate_report --self-test: 28 pass / 0 fail`; the fourteen earlier credits current over the review's edit, since no case pins it.
- [x] `.14` a47-2 **ROOT CAUSE** — Batch II-a held no observation: at 507c3017 `git ls-files evidence/rv64gc-ecall-ebreak-v1 | wc -l` = 8 of its 22 slots, the same for the other four.
- [x] `.14` a47-2 **ADDRESSED** — `python3 -B scripts/retain_div_capture.py --case <each> --declaration-commit 507c3017…` `rc=0`, once each (target/p4-system-14/a47-2/run/*/capture.json), baseline and repeat AGREE, each control DIVERGE at its declared step, complete, qualification false; `DIV-CAPTURE-INPUTS: 79 tests / 0 failures`; `REQUIREMENT-STATUS: ok (… 27 case(s), 14 credited, 0 declared, 14 of 14 credit record(s) current; 0 drift, 0 finding(s))`.
- [x] `.14` a47-2 **NO REGRESSION** — no pinned input moved: `git diff --name-only 507c3017 HEAD | wc -l` = 0 at the capture; every compared file byte-identical to the rehearsal's (check/compare.txt); the guard's refusal left all five at 8 files; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `14 credit(s), 14 current, 0 lapsed`.
- [x] `.14` a47-1 **ROOT CAUSE** — no case existed for Batch II-a, and a declared case could be claimed by the wrong profile: at 9af28b50 `git ls-files 'evidence/rv64gc-ecall-*' | wc -l` = 0, and declaring `rv64gc-ecall-ebreak-v1` made `python3 -B scripts/requirement_status.py` report `finding rv64i-lab-v0: case rv64gc-ecall-ebreak-v1 names obligation OB-GC-ECALL-EBREAK-V3 outside the effective contract`, `rc=1` in the probe.
- [x] `.14` a47-1 **ADDRESSED** — `REQUIREMENT-STATUS: ok (… 27 case(s), 14 credited, 5 declared, 14 of 14 credit record(s) current; 0 drift, 0 finding(s))`, no finding on any profile; `DIV-CAPTURE-INPUTS: 79 tests / 0 failures`, `rc=0`; `cargo test -q -p semulith-verify every_` `rc=0`, 34 passed over 187 guests; the rehearsal `rc=0`, five `capture rc=0`, five `10 of 10 legs` (target/p4-system-14/a47-1/rehearse.txt).
- [x] `.14` a47-1 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `14 credit(s), 14 current, 0 lapsed`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures`, the new seam `1 tests / 1 failures`; `STATEMENT-RETENTION: 21 tests / 0 failures`, `retained-pin` `13 failures` in both modes; `python3 -B scripts/check_interaction_matrix.py profiles/rv64gc-lab-v0` `rc=0`.

