# P4-SYSTEM ordinary history — part 33

Ordinary, directly readable task history: the complete records of the closed `.14` units
a46-0 to a46-4, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0366` on top of commit `2d1704e605ec1d064e47aafa06c30bc0de8f7aa7`
(6 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a43e-5, a43e-4, a43e-3 and their rows are in part 32,
the earlier ones in parts 13–31. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a48-1, SEMULITH-P4-0366.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a46-4 | 2980 | `67fdb11c14e377e1a28c13372ac0db280e52675621ca7a0a2d2c22c45a573fb4` |
| record a46-3 | 3175 | `65bac531b0cfea0fa246c18413d4175a15cc6f243e78f209c5ee40e825052d18` |
| record a46-2 | 3524 | `769b0410120246b6d0f35da97ed874e2bcb224d95921f571ac23d108a4f8274f` |
| record a46-1 | 1902 | `27215dfa5c4d8f8d779ecc010221bd9cf291d41f586881c18f4f41309247e1cf` |
| record a46-0 | 1884 | `b97a7f84b138afaf03fe2ff2dc5a8ddea2d4f472167c627877e14f790202d0ab` |
| acceptance rows a46-4–a46-0 | 5588 | `69c90234fa681e361ea152230bccefd435f8657de03d061c89ce86e06212dd34` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-33.md)   # a span, by its line range
```

<a id="a46-4"></a>

### .14 a46-4 / SEMULITH-P4-0362: Batch I credited: nine more requirements `implemented`, and a form that writes no GPR read after its step (completed)

Feature 2 of 5 after XTASK-0081. **The reviews.** `RETAINED_CAPTURES` names the nine (declared 506788a6, captured 8a40a249): each `satisfied`, 88 authenticated files, 995,992 B to 1,051,503 B; `python3 -B scripts/review_div_policy.py --every-retained` prints fourteen lines, each `satisfied — 10 of 10 legs satisfied`.

**The rule.** The form-coverage leg counted a form only at a witness of its own step, and a branch, a store or a load to `x0` writes no GPR: three of the nine could never satisfy it, 17 forms between them. Such a form is now also predeclared when a property's cell names it and that witness comes after a step of the form. A form with any GPR write, or never exercised, gets no such route. `_declared_cells` reads the cell from the case, since the planned record does not carry it. The leg names what it counted this way. Four tests, 48 → 52, and three seams, one per condition: any form, any cell, any order, each `1 tests / 1 failures`; each new arm runs in both modes. Rehearsing at a46-2 found this rule's first draft reading an empty `(writes)` as a write.

**The dispositions.** Nine, each `none applies` with its reason: arithmetic touches no rule; JALR's and the transfers' targets are word-aligned, so the fetch rule's boundaries are not in play; `OB-LOAD-EXT`'s accesses are aligned with translation off; `OB-LOAD-X0`'s fault and handler are the route that observes it, as `OB-XLEN`'s are.

**The credits.** Nine records beside the five, `authority review`, each pinning its measured record, receipt and the policy: 22,853 B of the file's 65,536 B. `implementation_status implemented` on the nine. `decision_batch-i-credited-implemented.md` (new, INDEX, KNOWLEDGE_MAP). Measured: `CREDIT-RECORDS: … 14 credit(s), 14 current, 0 lapsed`; `REQUIREMENT-STATUS: … 33 planned, 14 implemented, 1 not-applicable; 22 case(s), 14 credited, 0 declared, 14 of 14 credit record(s) current; 0 drift, 0 finding(s)`. `gate.sexp`: nine `G-TRACE` rows, fourteen in all; GS still 2 of 10 open, `G-OBLIGATIONS` at 14 `implemented`.

**The tripwire, read.** The pre-commit gate took 19.3 minutes at 13 cases and 5 credits (a43e-5), 20.1 at Batch I's declarations, 21.3 on the next commit, 22.3 at its captures, under loads of 8 to 24: about 20 seconds per captured case, against the limit of a minute. The credits' cost is measured at this commit and the next. Re-stated: the method probe's rows, the policy probe's cases, the status probe (33 / 14), the dossier probe (fourteen qualify). **Containment:** the window's closed records a43e-5, a43e-4 and a43e-3 and their rows moved verbatim to [archive part 32](archive/P4-SYSTEM-32.md). Book: status, policy, method and division pages. Evidence: `target/p4-system-14/a46-4`. Next: Batch II, system, rehearsed on a clone first. `ARTIFACT-CLEANUP.37` once due.

<a id="a46-3"></a>

### .14 a46-3 / SEMULITH-P4-0361: Batch I captured exactly once each, byte-identical to its rehearsal (completed)

Feature 1 of 5 after XTASK-0081. **The capture.** `target/p4-system-14/a46-3/capture.sh`, the guard the window's decision set for later captures: a clean tracked tree; no frozen path moved (`git diff --name-only 506788a6 HEAD` ∩ the 89 frozen paths = ∅, the one commit since being XTASK-0081); the declarations equal to their regeneration; `--preflight-only` `ready`; before each case the 1-minute load below 8 and 50 of 50 children spawned and reaped the collector's way. It held for four and a half minutes, load 13.74 down to 8.21, then ran beside seven to nine sibling processes at load 7.31 to 7.82.

| Case | Baseline, repeat | Control | Ran | Measured | Receipt | Trace |
| --- | --- | --- | --- | --- | --- | --- |
| `rv64gc-alu-imm-v1` | AGREE, 19 steps | DIVERGE at 12, x16 | 1.3 s | 13,251 B `27bf858d…` | 6,975 B | 1,628 B |
| `rv64gc-alu-reg-v1` | AGREE, 18 steps | DIVERGE at 11, x15 | 1.3 s | 12,154 B `41ec7ae6…` | 7,008 B | 1,512 B |
| `rv64gc-lui-auipc-v1` | AGREE, 10 steps | DIVERGE at 8, x11 | 1.4 s | 12,201 B `c9e17ce2…` | 7,014 B | 827 B |
| `rv64gc-jalr-lsb-v1` | AGREE, 16 steps | DIVERGE at 3, x7 | 1.2 s | 12,476 B `04ff5c6f…` | 6,995 B | 1,347 B |
| `rv64gc-no-delay-slots-v1` | AGREE, 21 steps | DIVERGE at 3, x10 | 1.2 s | 13,753 B `e8d3d275…` | 7,093 B | 1,596 B |
| `rv64gc-shamt-v1` | AGREE, 21 steps | DIVERGE at 6, x11 | 1.2 s | 13,497 B `8fad52b3…` | 6,924 B | 1,800 B |
| `rv64gc-wsuffix-v1` | AGREE, 17 steps | DIVERGE at 11, x16 | 1.2 s | 12,951 B `961ce2c7…` | 7,008 B | 1,446 B |
| `rv64gc-load-ext-v1` | AGREE, 32 steps | DIVERGE at 16, x12 | 1.3 s | 12,832 B `bc4b2d3b…` | 7,027 B | 2,507 B |
| `rv64gc-load-x0-v1` | AGREE, 68 steps | DIVERGE at 10, x30 | 1.3 s | 14,719 B `d5fda2b4…` | 6,994 B | 6,520 B |

Each ran once, never retried: three zero-exit processes, `complete_canonical_capture` true, qualification false, all nine findings matched or satisfied, each case's three traces byte-identical. **Against the rehearsal** (`check/compare.txt`): all nine compared files of all nine cases, traces, stdout, guest, expectations, case and declaration, are byte-identical to the clone's. The family holds 485 files, 3,497,781 B. Each case is on the override, so there is no configuration effect to retain. `REQUIREMENT-STATUS: … 22 case(s), 5 credited, 0 declared`: all nine `pending`, the five credits current.

Re-stated: the input probe's census (359 → 485), the status probe's rows and counts (`22, 5, 0, 5, 5`). As at a43e-4, the retained-capture rows move with the reviews: a row names its capture commit, which is this commit. A word corrected (§15): XTASK.13 d's record said the nine cases have 93 distinct manifest children; 93 is all 22 cases', and the nine's are 77. Its claim stands, since no board or part unit is among either. Book: the division page (the batch's table), status and prepared-inputs pages; the retained cases regenerate. Evidence: `target/p4-system-14/a46-3`. Next: a46-4, the review's rule for a form that writes no GPR, nine dispositions and nine credits.

<a id="a46-2"></a>

### .14 a46-2 / SEMULITH-P4-0360: Batch I's nine programs and cases, declared before their captures, and rehearsed first (completed)

Feature 5 of 5 after XTASK-0080: the turn is XTASK.13's BOARD-GEN, next. Nothing is captured or credited, and no retained case moved. **The programs.** `alu-imm-forms`, `alu-reg-forms`, `lui-auipc-forms`, `jalr-lsb`, `no-delay-slots`, `shamt-forms`, `wsuffix-forms`, `load-ext-forms` and `load-x0`, new in the corpus (`run-order.txt`, a boundary cell in `interactions.sexp`, `guests_rv64gc.rs` regenerated): 182 guests. **Judged three ways:** the spec-side author; the lab engine, `every_guest_matches_its_expectations` among 34 `every_` tests `ok`; the pinned Sail, `AGREE` on all nine, 222 declared steps between them. The census now reads 167 of 182 agreeing.

| Case | Requirement | Steps | Witnesses | Control |
| --- | --- | --- | --- | --- |
| `rv64gc-alu-imm-v1` | `REQ-D-ALU-IMM`, low | 19 | 13 | SLTIU at 12, x16: an immediate not sign-extended |
| `rv64gc-alu-reg-v1` | `REQ-D-ALU-REG`, low | 18 | 10 | SLTU at 11, x15: read as signed |
| `rv64gc-lui-auipc-v1` | `REQ-D-LUI-AUIPC`, medium | 10 | 9 | AUIPC at 8, x11: an offset not sign-extended |
| `rv64gc-jalr-lsb-v1` | `REQ-D-JALR-LSB`, medium | 16 | 10 | the landing at 3, x7: the least-significant bit kept |
| `rv64gc-no-delay-slots-v1` | `REQ-D-NO-DELAY-SLOTS`, low | 21 | 11 | JAL's landing at 3, x10: a delay slot that ran |
| `rv64gc-shamt-v1` | `REQ-D-SHAMT`, high | 21 | 15 | SLL at 6, x11: an amount not masked to 6 bits |
| `rv64gc-wsuffix-v1` | `REQ-D-WSUFFIX`, high | 17 | 12 | ADDW at 11, x16: a word not sign-extended |
| `rv64gc-load-ext-v1` | `REQ-D-LOAD-EXT`, high | 32 | 12 | LW at 16, x12: not sign-extended |
| `rv64gc-load-x0-v1` | `REQ-D-LOAD-X0`, high | 68 | 16 | the handler at 10, x30: a discarded load that skipped its fault |

Each witness's value was written from the retained statements and held to the derivation; none disagreed. 67 manifest children each, no report or book generator, 8 files each. **Rehearsed first** (`target/p4-system-14/a46-2/rehearse.sh`, a throwaway clone, nothing of it reaching the real tree): nine captures, AGREE, AGREE, each control DIVERGE at its declared step, three byte-identical traces each, and all nine 10 of 10 once the review learned the rule below. It found two faults: `REQ-D-NO-DELAY-SLOTS` had no witness at a `JAL` or `JALR` step, which would have spent a case id after a real capture, and my first rule read an empty `(writes)` form as a write. **The review's rule, not landed here** (it lands with the credits; the review is not pinned): a form that writes no GPR cannot be witnessed at its own step, 6 branches, 4 stores and 7 loads to `x0` across three cases.

**The family's ninth re-derivation, once for all five batches:** 903 files, 541 MiB, the probe holding the declared cases to the bound and each case to its 22 slots. Three commits a batch, not four: programs and declarations share one. Re-stated: the input probe's tables and census (`1 + 13 * 22 + 9 * 8`), the case probe's planned population, the property probe's ids, the status probe's rows and counts (`22, 5, 9, 5, 5`). `REQUIREMENT-STATUS: … 22 case(s), 5 credited, 9 declared, 5 of 5 credit record(s) current; 0 drift`. **Frozen until the captures:** each case's 67 children and the 13 authority views. Book: requirement status, prepared inputs; the retained cases regenerate. Evidence: `target/p4-system-14/a46-2`. Next: XTASK.13's BOARD-GEN, then a46-3, each captured once.

<a id="a46-1"></a>

### .14 a46-1 / SEMULITH-P4-0359: Batch I's walls cleared — the case index generated, its statements retained (completed)

Feature 4 of 5 after XTASK-0080. No case, credit or pinned file moves. **The index.** `evidence/README.md` stood at 4,094 of 4,096 B with a table it called the complete membership, so the next row could not land. `gen_model_book.py` now emits `materials/retained-cases.md` for a unit holding cases, one row per `evidence/*/case.sexp`, its state read from the credit catalogue, and the book gains [the retained cases](../models/rv64gc-lab-v0/src/retained-cases.md). MATERIALS-BILL's drift check holds it with no new doctrine: a lapse changes a row, and the commit refuses until the page is regenerated. Six controls in `test_gen_model_book.py` (every directory one row; a current credit read and a lapsed one not; no receipt reads declared; history names the holder; a unit with no case has no fragment; an unreadable case refuses). **The README** fell to 3,129 B, and a batch no longer edits it for membership.

**The statements.** `RVI-RV32I-STATEMENTS`, twenty statements of §1.1.2 and §1.1.4 to §1.1.6, 6,428 B, `c476fd87…`; `RVI-RV64I-FORMS-STATEMENTS`, six of §3.1.2.1 and §3.1.3, 2,993 B, `f254c3fe…`; `materials/RVI_BASE_RETENTION.md`. No tool change, and `--emit` reproduces each byte for byte. The gate's first run refused on the retention probe's `retained-pin` arm, `21 tests / 9 failures` against a pin of 7: two more excerpts for that omission to break, so the arm is re-stated at 9, measured in both modes. `REQ-D-SHAMT` and `REQ-D-WSUFFIX` rest on the XLEN case's older excerpt. **Containment:** the closed records a45-1, a43e-c1, a43e-2 and a43e-1 and their rows moved verbatim to [archive part 31](archive/P4-SYSTEM-31.md). Next: a46-2, Batch I's programs and cases, and the family re-derived for them. XTASK.13's BOARD-GEN follows it, the 5:1 turn.

<a id="a46-0"></a>

### .14 a46-0 / SEMULITH-P4-0358: G-OBLIGATIONS' other 42 routed — 28 in batches on the tools as they are, 14 raised for a ruling (completed)

Feature 3 of 5 after XTASK-0080. No case, credit or pinned file moves. **Measured** (`target/p4-system-14/a46-0`): all 42 have their two contract checks realized; `census_reference_config.py --case rv64gc-sstc-v1`, 346 Sail runs in 3.9 s, reads 158 of 173 guests agreeing on at least one configuration, and the other 15 fall into five families, read from their detail lines and not yet root-caused (wait, MTIP, injection, reservation width, not compared). Crossing checks with guests: 15 guest-evidenced, 13 execution-evidenced, 12 statements of selection, 2 reaching past the reference. A first cross-reference read 0 checks, my regex having the fields in the wrong order: fixed and re-run, not a finding.

**The route.** One case at a time would be 140 units and 56 hours of gate; five batches of four commits are 20 units and 8, on tools that already did it (a43e-3 … a43e-5: five cases in three). A family case is rejected for now: a pinned schema field, all five credits lapsing, and a policy rule each leg would have to learn. **Raised, not decided:** the 12 selection statements, for which the policy allows an alternative disposition but `authenticate` reads only a case and the policy text is pinned; and the 2 that may rightly end `partial`, which turns on `P4-SYSTEM.18`. **Walls named before they stop a batch:** `evidence/README.md` at 4,094 of 4,096 B cannot take another row, so its table leaves for a generated page first (a46-1); `credits.sexp` runs out at about 32 records. **The tripwire:** gate time per case is unmeasured, and it is the estimate's weakest number. Batch I measures it; over a minute a case, the work stops and the cost is raised. Book: requirement status. Next: a46-1, Batch I's programs and cases.

<a id="acceptance-rows-a46-4-to-a46-0"></a>

## acceptance-rows-a46-4-to-a46-0

- [x] `.14` a46-4 **ROOT CAUSE** — captures credit nothing, and three of the nine could not satisfy the coverage leg: at 8a40a249 `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` reads `5 credit(s)`, `python3 -B scripts/review_div_policy.py --case rv64gc-load-x0-v1` reads `refused — unsupported: no reviewed capture`, and `git show 8a40a249:scripts/review_div_policy.py | grep -c read_after` = 0, so a form that writes no GPR had no way to be predeclared.
- [x] `.14` a46-4 **ADDRESSED** — `python3 -B scripts/review_div_policy.py --every-retained` `rc=0`, fourteen lines `satisfied — 10 of 10 legs satisfied; credited by …`; `CREDIT-RECORDS: … 14 credit(s), 14 current, 0 lapsed`; `REQUIREMENT-STATUS: ok (… 33 planned, 14 implemented, 1 not-applicable; 22 case(s), 14 credited, 0 declared, 14 of 14 credit record(s) current; 0 drift, 0 finding(s))`.
- [x] `.14` a46-4 **NO REGRESSION** — `DIV-POLICY-PROBE: 52 tests / 0 failures`, the three new seams each `1 tests / 1 failures`; `DIV-METHOD: 22 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`; `gate_report --self-test: 28 pass / 0 fail`; the five earlier credits current over the review's edit, since no case pins it (`grep -c review_div_policy evidence/rv64gc-sstc-v1/dependencies.sexp` = 0).
- [x] `.14` a46-3 **ROOT CAUSE** — Batch I held no observation: at 669ff846 `git ls-files evidence/rv64gc-load-x0-v1 | wc -l` = 8 of its 22 slots, the same for the other eight, so each program's agreement with Sail stood only on a rehearsal in a throwaway clone.
- [x] `.14` a46-3 **ADDRESSED** — `python3 -B scripts/retain_div_capture.py --case <each> --declaration-commit 506788a6…` `rc=0`, once each (target/p4-system-14/a46-3/run/*/capture.json), baseline and repeat AGREE, each control DIVERGE at its declared step, complete, qualification false; `DIV-CAPTURE-INPUTS: 79 tests / 0 failures`; `REQUIREMENT-STATUS: ok (… 22 case(s), 5 credited, 0 declared, 5 of 5 credit record(s) current; 0 drift, 0 finding(s))`.
- [x] `.14` a46-3 **NO REGRESSION** — no pinned input moved: `git diff --name-only 506788a6 HEAD` ∩ the 89 frozen paths = ∅ at the capture; every compared file byte-identical to the rehearsal's (check/compare.txt); `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `5 credit(s), 5 current, 0 lapsed`; `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`.
- [x] `.14` a46-2 **ROOT CAUSE** — no case existed for any of Batch I's nine: at 6d5d2c8f `git ls-files 'evidence/rv64gc-alu-*' | wc -l` = 0 and `git ls-files profiles/rv64gc-lab-v0/guests | grep -c 'alu-imm-forms\|load-x0\|shamt-forms'` = 0, and the family's ceiling, 287 files, was already full at 13 cases.
- [x] `.14` a46-2 **ADDRESSED** — `DIV-CAPTURE-INPUTS: 79 tests / 0 failures / 0 errors`, `rc=0`; `REQUIREMENT-STATUS: ok (… 22 case(s), 5 credited, 9 declared, 5 of 5 credit record(s) current; 0 drift, 0 finding(s))`; `cargo test -q -p semulith-verify every_` `rc=0`, 34 passed over 182 guests; the rehearsal `rc=0`, nine `capture rc=0`, nine `10 of 10 legs` (target/p4-system-14/a46-2/rehearse.txt).
- [x] `.14` a46-2 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `5 credit(s), 5 current, 0 lapsed`, over nine new guests, cases and a re-derived family; `MATCHED-GPR-CASE: 10 tests / 0 failures`, `MATCHED-GPR-PROPERTY: 36 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`; `python3 -B scripts/check_interaction_matrix.py profiles/rv64gc-lab-v0` `rc=0`.
- [x] `.14` a46-1 **ROOT CAUSE** — the next case could not land: `wc -c evidence/README.md` = 4,094 of the probe's and the registry's 4,096 B, with a row per case in it; and `git ls-files profiles/rv64gc-lab-v0/retained | grep -c 'rv32i\|rv64i-forms'` = 0 at 5f2a971f, so no Batch I case naming RVI-RV32I, `REQ-D-LUI-AUIPC` or `REQ-D-LOAD-EXT` had a normative input to pin.
- [x] `.14` a46-1 **ADDRESSED** — `python3 -B scripts/gen_model_book.py --check --unit rv64gc-lab-v0` `rc=0`, 5 fragments, one row per `evidence/*/case.sexp` (13); `python3 -B scripts/test_gen_model_book.py` `rc=0`, 9 tests; `python3 -B scripts/retain_statements.py --verify` `rc=0`, both new excerpts `matched`, and `--emit` of each `cmp` silent against its retained bytes.
- [x] `.14` a46-1 **NO REGRESSION** — `git diff --cached --name-only | grep -c '^evidence/rv64'` = 0; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `5 credit(s), 5 current, 0 lapsed`; `python3 -B scripts/probe_statement_retention.py` → `STATEMENT-RETENTION: 21 tests / 0 failures`; `python3 -B scripts/probe_div_capture_inputs.py` → `DIV-CAPTURE-INPUTS: 79 tests / 0 failures`.
- [x] `.14` a46-0 **ROOT CAUSE** — no route existed for the rest of the axis: `python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0` `rc=0` reads 42 planned, and `git grep -c 'G-OBLIGATIONS' -- docs/decisions/decision_state-capture-plan.md` = 1, the one line saying they are not that plan's.
- [x] `.14` a46-0 **ADDRESSED** — `decision_obligations-route.md` classes all 42 (`15 + 13 + 12 + 2`), measured by `python3 -B scripts/census_reference_config.py --case rv64gc-sstc-v1` `rc=0` (target/p4-system-14/a46-0/census.txt) and the cross-reference (census-rows.txt).
- [x] `.14` a46-0 **NO REGRESSION** — no case moved: `git diff --cached --name-only | grep -c '^evidence/'` = 0, and `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `5 credit(s), 5 current, 0 lapsed`.

