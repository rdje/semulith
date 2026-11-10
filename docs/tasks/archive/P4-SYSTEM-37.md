# P4-SYSTEM ordinary history — part 37

Ordinary, directly readable task history: the complete records of the closed `.14` units
a51-0 to a51-14, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0396` on top of commit `987ad95180748075a0d02179c484ed83be0aa4a0`
(16 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a50-1 to a50-c2 and their rows are in part 36,
the earlier ones in parts 13–35. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); `.18` slice b, SEMULITH-P4-0396.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a51-14 | 667 | `aed046985f9fad6ed825f75c5b3b6280d5e0cf2ec62123f84d99a850916df025` |
| record a51-13 | 533 | `d0644160ea95377938ae8ed37a4e256e862f9b8bc23a4fb9154d580055802b93` |
| record a51-12 | 929 | `95a1c5a42f312d4a9a47d7e3e2e4c719591043ce093c21487bf451700da44e53` |
| record a51-11 | 807 | `d75d9b1f94c73fa19b20467061b85b9f24aaf57dbfd94ad1048186233b6eed7f` |
| record a51-10 | 703 | `5b3973c6dd15ae74b645702a3b10bfec5a92b6567dd9a2eebf56d348eebc927c` |
| record a51-9 | 755 | `6036421ac2322f307d1c2553a474a79362d17f3f32d7d4fe49ca08ced55ef245` |
| record a51-8 | 1202 | `7b14dc181e018e7100c117b60710d0cc3222653179e230df24ddf961b913feb9` |
| record a51-7 | 1065 | `93a85f5649b2bcb31a24815c8fe6483770cfaaafdb8a2dd1f13a4e8c8aaf7891` |
| record a51-6 | 737 | `2107a354460c778d74bb70a870687b3e7b3b27e18131e53f3a3c69ac849e12c0` |
| record a51-5 | 709 | `01ea5b7c95b38e6a46914b8e1a6a6d1c8d1f84a56ee4cce15a68a2f997fa70dc` |
| record a51-4 | 999 | `772961eaaa747d350842a66c6b4b4428443260b140813f67b269631a6193f328` |
| record a51-3 | 771 | `bf47682da542c74f0920b49a509e80671dfeb89c0046df465763b73a9da381e1` |
| record a51-2 | 826 | `8adcbac840e588458b020887aef74e5362da245c89a1f4eed7a42c75fd08ce42` |
| record a51-1 | 1311 | `5ad39495d0598585a868e314640082c5f4d559436ddbb1aadb9134abd17c5182` |
| record a51-0 | 978 | `b6195666b301bb6be428fd0d44cd9caea933b1010e544dfd234b409199650b21` |
| acceptance rows a51-14–a51-0 | 12242 | `095122742179e09193c41626750da1c29b46e98804bdd9782959f4a5c6a1ed48` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-37.md)   # a span, by its line range
```

<a id="a51-14"></a>

### .14 a51-14 / SEMULITH-P4-0392: the four with nothing to run credited, and `G-OBLIGATIONS` closes (completed)

Feature 5 of 5 after XTASK-0087. **The credits.** Four records, `authority review`, each on a selection's record: `REQ-D-ABI`, `REQ-D-FP-DEFER`, `REQ-D-ROUTE-FLIP`, `REQ-D-SCOPE-CENSUS`. See `decision_the-four-with-nothing-to-run-credited-implemented.md`. **What moved.** 46 `implemented`, 2 `not-applicable`, none `planned`. `G-OBLIGATIONS` reads green and its open row is gone, so `CPU-SYSTEM` reads 1 of 10 axes open, `G-RELEASE`. Book: `requirement-status.md`, `method-adequacy.md`, `policy-adequacy.md`. Next, the XTASK turn, then `P4-SYSTEM.18`.

<a id="a51-13"></a>

### .14 a51-13 / SEMULITH-P4-0391: the four with nothing to run measured once each (completed)

Feature 4 of 5 after XTASK-0087. Each record taken once, through `scripts/selections.py --record`, retained in `profiles/rv64gc-lab-v0/selections/`, with the three objects `REQ-D-ABI` reads. **All 25 facts read their declared value, and all 11 runs exited 0 and repeated byte for byte.** Each record is byte-identical to the rehearsal on a clone. The status does not move, because no credit names them. Next, the credits, and the axis.

<a id="a51-12"></a>

### .14 a51-12 / SEMULITH-P4-0390: the four with nothing to run declared, each fact with its expected value (completed)

Feature 3 of 5 after XTASK-0087. **Declared.** `DS-ABI`, `DS-FP-DEFER`, `DS-ROUTE-FLIP`, `DS-SCOPE-CENSUS`, 25 facts in all, and a statement trace for each. **The readers.** `scripts/selections.py` reads each fact, and `probe_selections.py` holds that each moves when what it names moves. Their traces live beside their records, `profiles/rv64gc-lab-v0/selections/statement-trace.sexp`, since the profile's own stands at its 65,536-byte ceiling. **A finding, named as a limit.** All 44 retained guests are tagged soft-float, on purpose, so the ABI statement holds for what the compiler builds; see `decision_the-seventeen-called.md`. Rehearsed on a clone first: all four records stand at first taking, 46 of 46 traces hold, and the axis would close. Nothing here is measured or credited. Next, the records.

<a id="a51-11"></a>

### .14 a51-11 / SEMULITH-P4-0389: track 4's tool: a credit may name a selection's record (completed)

Feature 2 of 5 after XTASK-0087. **The call.** `decision_a-credit-with-no-case.md`. **Measured first.** `scripts/check_gc_contract_scope.py` already has named positive and negative checks for all four, and the Rust registry runs them. They leave three things unread, which a record reads at a51-12: any compiled object, the backend's other users, and `rv64i-lab-v0`. **What landed.** `scripts/selections.py` and its probe, `schema/credits.sexp` and `schema/dispositions.sexp`, and readers in `credit_records.py`, `dispositions.py`, `requirement_status.py`, `statement_trace.py` and `gate_report.py`. Nothing here is credited, and no status moves. Book: `requirement-status.md`. Next, the four declared.

<a id="a51-10"></a>

### .14 a51-10 / SEMULITH-P4-0388: the four with no switch credited (completed)

Feature 1 of 5 after XTASK-0087. **The credits.** Four records, `authority review`, each on its own case at 11 of 11 legs: `REQ-D-ENDIAN`, `REQ-D-FENCE`, `REQ-D-WALK-IMPLICIT`, `REQ-GC-PARTIAL-PROGRESS`. See `decision_the-four-with-no-switch-credited-implemented.md`. **What moved.** 42 `implemented`, 4 `planned`, 2 `not-applicable`; 44 cases, 42 credited, 2 fixtures. `G-TRACE` lists all 42. The reviews read the four, and `probe_div_policy.py`'s `NO_SWITCH` table holds each to its declared disposition, with no effect claimed. Book: `requirement-status.md`, `method-adequacy.md`, `policy-adequacy.md`. Next, track 4.

<a id="a51-9"></a>

### .14 a51-9 / SEMULITH-P4-0387: the four with no switch captured exactly once each, and the walks compared (completed)

Feature 5 of 5 after XTASK-0086. Each once from the declaration commit `ac03c460`, through `scripts/capture_guarded.py`: each baseline and repeat `AGREE`, each control `DIVERGE` at its predeclared witness. **All 42 compared files are byte-identical to the rehearsal, 0 findings** (`target/p4-system-14/a51-9/compare.py`). The walk record is retained, and the review re-derives its comparison on every read. Re-stated: the input probe's census (`1 + 44 * 22`), the status probe (`44, 38, 0, 38, 38`). Book: `canonical-division.md`, `prepared-inputs.md`, `requirement-status.md`. Family: 969 files. Next, the XTASK turn, then a51-10.

<a id="a51-8"></a>

### .14 a51-8 / SEMULITH-P4-0386: the four with no switch declared, each with its disposition, and a call corrected (completed)

Feature 4 of 5 after XTASK-0086. Nothing is captured or credited, and no retained case moved. **The programs.** `endian-forms`, `fence-forms`, `walk-implicit-forms`, `partial-progress-forms`: 44 witnesses over 341 steps, each held to the spec-side author, the lab engine and the pinned Sail. **The dispositions.** `profiles/rv64gc-lab-v0/dispositions.sexp`, four records, written before the cases. **The rehearsal.** On a clone: captured, the walk record retained, each 11 of 11 legs (`target/p4-system-14/a51-7/rehearse.txt`). **A call corrected.** a51-0 said to move these to `source-specific`. RECORD-SCHEMA's mirror rule refused it for two, and the source's own words say why it was wrong for all four, so each keeps `implementation-defined` and the review reads the disposition in the row's place; see `decision_the-seventeen-called.md`. Two excerpts, `RVI-MEMORY-STATEMENTS` and `RVI-PRECISE-STATEMENTS`. Family: 913 files, 44 of 50 cases. Book: `policy-adequacy.md`, `references.md`, `requirement-status.md`, `prepared-inputs.md`. Next, the XTASK turn, then a51-9.

<a id="a51-7"></a>

### .14 a51-7 / SEMULITH-P4-0385: track 3's tools: a declared disposition is a row the review reads, and a walk's reads are compared (completed)

Feature 3 of 5 after XTASK-0086. Nothing is declared or credited here, and no retained case moved. **The row.** `scripts/dispositions.py` and `schema/dispositions.sexp`, with the walk record's shape joining `schema/config-effect.sexp` to stay inside `schema/`'s ceiling; the policy review's `source-specific` branch, with nine tests and seven mutations; RECORD-SCHEMA's rule 15, with three arms. **The walks.** `semulith run --trace-walks`, and `scripts/measure_walk_trace.py` with `scripts/probe_walk_trace.py`, 15 tests, 10 mutations. Measured on the corpus first: 30 translating guests read the same PTEs on both, 23 in the same order. **The bound.** One sentence moved from 38 records' limitations to `credits.sexp`'s header: 63,828 B to 54,439 B, and all 38 stay current. See `decision_the-seventeen-called.md`. Book: `policy-adequacy.md`, `references.md`. Toolbox: `execution.md`. Next, a51-8 declares the four.

<a id="a51-6"></a>

### .14 a51-6 / SEMULITH-P4-0384: the two with a switch credited (completed)

Feature 2 of 5 after XTASK-0086. **The credits.** Two records, `authority review`, each on its own case at 11 of 11 legs: `REQ-D-NO-H`, `REQ-D-NO-PMP`. See `decision_the-two-with-a-switch-credited-implemented.md`. **What moved.** 38 `implemented`, 8 `planned`, 2 `not-applicable`; 40 cases, 38 credited, 2 fixtures. `G-TRACE` lists all 38. The reviews read the two, and `probe_div_policy.py`'s `LAST_SWITCHES` table holds each first difference. Book: `requirement-status.md`, `method-adequacy.md`, `policy-adequacy.md`. The live file reached its ceiling, so the closed records a50-1 to a50-c2 and their rows moved verbatim to archive part 36. Next, track 3.

<a id="a51-5"></a>

### .14 a51-5 / SEMULITH-P4-0383: the two with a switch captured exactly once each, each effect at a witness (completed)

Feature 1 of 5 after XTASK-0086. Each once from the declaration commit `daadeb52`, through `scripts/capture_guarded.py`: each baseline and repeat `AGREE`, each control `DIVERGE` at its predeclared witness, each effect retained with its first difference at a witness. **All 22 compared files are byte-identical to the rehearsal, 0 findings** (`target/p4-system-14/a51-5/compare.py`). Re-stated: the input probe's census (`1 + 40 * 22`), the status probe (`40, 36, 0, 36, 36`). Book: `canonical-division.md`, `prepared-inputs.md`, `requirement-status.md`. Family: 881 files. Next, a51-6.

<a id="a51-4"></a>

### .14 a51-4 / SEMULITH-P4-0382: the two with a switch of the last 17 declared (completed)

Feature 5 of 5 after XTASK-0085. Nothing is captured or credited, and no retained case moved. **The programs.** `no-h-forms`, 5 witnesses, and `no-pmp-forms`, 4, each held to the spec-side author, the lab engine and the pinned Sail, and each first differing at a witness under what selects otherwise: `extension_on "H"` at `misa`, `pmp_count 16` at a load at S's privilege. **The rehearsal.** On a clone: captured, each effect retained, each 11 of 11 legs (`target/p4-system-14/a51-4/rehearse.txt`). **What writing them found.** A refused fetch reads as absent evidence, so PMP's difference is measured on data accesses through `MPRV`; see `decision_the-seventeen-called.md`. **The tools.** `schema/alternative.sexp` and `prepare_div_inputs.py` gain `pmp_count`, with three tests and three mutations. One excerpt, `RVP-PMP-STATEMENTS`. Family: 853 files, 40 of 50 cases. Next, the XTASK turn, then a51-5.

<a id="a51-3"></a>

### .14 a51-3 / SEMULITH-P4-0381: the first six of the last 17 credited (completed)

Feature 4 of 5 after XTASK-0085. **The credits.** Six records, `authority review`, each on its own case at 11 of 11 legs: `REQ-D-GC-COMPOSITION`, `REQ-D-EXT-CLOSURE`, `REQ-D-PRIV-REVISION`, `REQ-D-RVWMO`, `REQ-D-PRIV-INSNS`, `REQ-GC-PRIV-INSNS`. See `decision_six-defined-credited-implemented.md`. **What moved.** 36 `implemented`, 10 `planned`, 2 `not-applicable`; 38 cases, 36 credited, 2 fixtures. `G-TRACE` lists all 36. `REQ-GC-PRIV-INSNS`, which the route expected to end `partial`, reads `implemented`. The reviews read the six, and `probe_div_policy.py`'s `LAST_DEFINED` table holds them. Book: `requirement-status.md`, `method-adequacy.md`, `policy-adequacy.md`. Next, a51-4.

<a id="a51-2"></a>

### .14 a51-2 / SEMULITH-P4-0380: the first six of the last 17 captured exactly once each, through the tracked guard (completed)

Feature 3 of 5 after XTASK-0085. **The captures.** Each once from the declaration commit `83f9ca4d`, at load 14, through `scripts/capture_guarded.py`: its first real use. Each baseline and repeat `AGREE`, each control `DIVERGE` at its predeclared witness. **All 60 compared files are byte-identical to the rehearsal, 0 findings** (`target/p4-system-14/a51-2/compare.py`). Re-stated: the input probe's census (`1 + 38 * 22`), the status probe (`38, 30, 0, 30, 30`). Book: `canonical-division.md`'s table, `prepared-inputs.md`, `requirement-status.md`. **Corrected in the book:** `policy-adequacy.md` still said 55 tests, ten legs, v6 and `CR-GC-M-4`. Family: 837 files, 7,009,366 B. Next, a51-3.

<a id="a51-1"></a>

### .14 a51-1 / SEMULITH-P4-0379: the first six of the last 17 declared, and the reference's wfi turned on (completed)

Feature 2 of 5 after XTASK-0085. Nothing is captured or credited, and no retained case moved. **The programs.** Six written for their statements, 68 witnesses over 549 steps, each held to the spec-side author, the lab engine and the pinned Sail: `composition-forms`, `ext-closure-forms`, `priv-revision-forms`, `rvwmo-forms`, `priv-insns-forms`, `priv-forms`. **The rehearsal.** On a clone, through `scripts/capture_guarded.py`, each captured and each read 11 of 11 legs (`target/p4-system-14/a51-1/rehearse.txt`).

**What writing them found.** The override's `wfi_is_nop` had been hiding the reference's own `wfi`: overlays can now turn it off, and all 345 steps of `priv-forms` agree. `REQ-D-PRIV-INSNS` named no form, a catalogue fault, now fixed, and a `memory` requirement may name none. See `decision_the-seventeen-called.md`. **The tools.** `schema/overlay.sexp` and `prepare_div_inputs.py` gain `wfi_is_nop`, with two new tests and two mutations. Four excerpts: `RVI-NAMING-STATEMENTS`, `RVI-ZC-STATEMENTS`, `RVI-RVWMO-STATEMENTS`, `RVP-XRET-STATEMENTS`. Family: 753 files, 38 of 50 cases. Book: `references.md`, `policy-adequacy.md`, `requirement-status.md`, `prepared-inputs.md`.

<a id="a51-0"></a>

### .14 a51-0 / SEMULITH-P4-0378: the last 17 called, and measuring the reference overturned the route's reading of them (completed)

Feature 1 of 5 after XTASK-0085. **The measurement.** All 198 guests under each candidate switch of the pinned binary (`target/p4-system-14/a51-0/variants.py`), and its walk and memory traces. The route had said most of the 17 had nothing to compare. `H` on moves 45 guests' verdicts, 16 PMP entries move 51, each extension letter shows at `misa`, and `--trace-ptw` prints what the walk reads. **The calls.** Every one has a route: six real `defined` cases, two with a real switch, four real cases with a declared `source-specific` disposition, four `source-specific` records with nothing to run, and `REQ-D-SBI` out of the CPU's scope to `P6-LINUX.2`, carried out here. See `decision_the-seventeen-called.md`. No policy edit, so no credit lapsed: 30 current, 30 `implemented`, 2 `not-applicable`, 16 `planned`. Book: `requirement-status.md`.

<a id="acceptance-rows-a51-14-to-a51-0"></a>

## acceptance-rows-a51-14-to-a51-0

- [x] `.14` a51-14 **ROOT CAUSE** — the four were measured with no credit: `git show a20a08e4:profiles/rv64gc-lab-v0/credits.sexp | grep -c '(credit (id '` = 42.
- [x] `.14` a51-14 **ADDRESSED** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `46 credit(s), 46 current, 0 lapsed`; `grep -c 'G-OBLIGATIONS. .*\*\*green\*\*' profiles/rv64gc-lab-v0/GS-REPORT.md` = 1; `grep -c 'Open axes (1 of 10)' profiles/rv64gc-lab-v0/GS-REPORT.md` = 1.
- [x] `.14` a51-14 **NO REGRESSION** — `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`; `SELECTIONS-PROBE: 46 tests / 0 failures / 0 errors`; `git diff --cached --name-only | grep -c evidence/` = 0.
- [x] `.14` a51-13 **ROOT CAUSE** — the four were declared with no record: `git ls-tree -r d63be692 --name-only profiles/rv64gc-lab-v0/selections | grep -c selection.sexp` = 0.
- [x] `.14` a51-13 **ADDRESSED** — `ls profiles/rv64gc-lab-v0/selections | grep -c selection.sexp` = 4; `grep -c 'SELECTIONS: .*: stands' target/p4-system-14/a51-13/record.log` = 4; `grep -c 'same as the rehearsal' target/p4-system-14/a51-13/compare.txt` = 8.
- [x] `.14` a51-13 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `42 credit(s), 42 current, 0 lapsed`; `git diff --cached --name-only | grep -c evidence/` = 0; `DOSSIER-SCHEMA` `rc=0`.
- [x] `.14` a51-12 **ROOT CAUSE** — no disposition answers the four: `git show 3213d875:profiles/rv64gc-lab-v0/dispositions.sexp | grep -c '(kind record)'` = 0.
- [x] `.14` a51-12 **ADDRESSED** — `grep -c '(kind record)' profiles/rv64gc-lab-v0/dispositions.sexp` = 4; `grep -c '(expect (fact ' profiles/rv64gc-lab-v0/dispositions.sexp` = 25; `SELECTIONS-PROBE: 46 tests / 0 failures / 0 errors`; `STATEMENT-TRACE-PROBE: 15 tests / 0 failures / 0 errors`.
- [x] `.14` a51-12 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `42 credit(s), 42 current, 0 lapsed`; `git diff --cached --name-only | grep -c evidence/` = 0; `ls profiles/rv64gc-lab-v0/selections | grep -c selection.sexp` = 0.
- [x] `.14` a51-11 **ROOT CAUSE** — a credit needs a case: `git show 605b49cd:scripts/credit_records.py | grep -c 'case_dir = root / "evidence" / credit\["case_id"\]'` = 1, and `git show 605b49cd:schema/credits.sexp | grep -c '(name case_id) (type string) (pattern'` = 1.
- [x] `.14` a51-11 **ADDRESSED** — `SELECTIONS-PROBE: 31 tests / 0 failures / 0 errors`; `python3 -B scripts/probe_selections.py --mutation live-fact 2>&1 | grep -c ' 0 errors'` = 1, and it fails.
- [x] `.14` a51-11 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `42 credit(s), 42 current, 0 lapsed`; `git diff --cached --name-only | grep -c evidence/` = 0; `DIV-POLICY-PROBE: 70 tests / 0 failures / 0 errors`.
- [x] `.14` a51-10 **ROOT CAUSE** — the four were captured with no credit: `git show 815c7afb:profiles/rv64gc-lab-v0/credits.sexp | grep -c '(credit (id '` = 38.
- [x] `.14` a51-10 **ADDRESSED** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `42 credit(s), 42 current, 0 lapsed`; `python3 -B scripts/review_div_policy.py --every-retained 2>&1 | grep -c '11 of 11 legs satisfied; credited by'` = 42; `grep -c 'experiment "rv64gc-' profiles/rv64gc-lab-v0/gate.sexp` = 42.
- [x] `.14` a51-10 **NO REGRESSION** — `DIV-POLICY-PROBE: 70 tests / 0 failures / 0 errors`; `DIV-METHOD: 22 tests / 0 failures / 0 errors`; `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`.
- [x] `.14` a51-9 **ROOT CAUSE** — the four held declarations and no capture: `git ls-tree -r ac03c460 --name-only evidence/rv64gc-fence-v1 | grep -c trace` = 0.
- [x] `.14` a51-9 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a51-9/capture.log` = 4; `python3 -B target/p4-system-14/a51-9/compare.py | grep -c 'byte-identical with the rehearsal: 42 findings: 0'` = 1; `grep -c 'no PTE written from the first walk on' target/p4-system-14/a51-9/walk.txt` = 1.
- [x] `.14` a51-9 **NO REGRESSION** — `DIV-CAPTURE-INPUTS: 80 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `38 credit(s), 38 current, 0 lapsed`.
- [x] `.14` a51-8 **ROOT CAUSE** — the four held no case: at c2e30d7c `git ls-tree c2e30d7c evidence/ | grep -cE 'endian|fence-v|walk-implicit|partial-progress'` = 0; and moving a mirrored requirement's category drifts: `MIRROR DRIFT requirements.sexp [REQ-D-ENDIAN]`, whose `grep -c 'implementation-defined' <(grep 'REQ-D-ENDIAN\"' profiles/rv64i-lab-v0/requirements.sexp)` = 1.
- [x] `.14` a51-8 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a51-7/rehearse.txt` = 4; `grep -c '11 of 11 legs satisfied' target/p4-system-14/a51-7/rehearse.txt` = 4; `grep -c 'walk rc=0' target/p4-system-14/a51-7/rehearse.txt` = 1; `DIV-POLICY-PROBE: 70 tests / 0 failures / 0 errors`; `STATEMENT-TRACE: rv64gc-lab-v0: 42 of 42 requirements with a declared case trace`.
- [x] `.14` a51-8 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `38 credit(s), 38 current, 0 lapsed`; `RECORD-SCHEMA --self-test: 88 pass / 0 fail`; `DIV-CAPTURE-INPUTS: 80 tests / 0 failures / 0 errors`; `cargo test -p semulith-verify every_guest_matches` `rc=0`, on 210 guests.
- [x] `.14` a51-7 **ROOT CAUSE** — the review had no branch for this category: `git show dd298484:scripts/review_div_policy.py | grep -c 'source-specific'` = 0; a matched comparison cannot see a walk: `git show dd298484:crates/semulith-cli/src/main.rs | grep -c 'trace-walks'` = 0.
- [x] `.14` a51-7 **ADDRESSED** — `DIV-POLICY-PROBE: 68 tests / 0 failures / 0 errors`; `WALK-TRACE: 15 tests / 0 failures / 0 errors`; `RECORD-SCHEMA --self-test: 88 pass / 0 fail`; `cargo test -p semulith-cli --test option_spellings` `rc=0`, 5 passed; `wc -c < profiles/rv64gc-lab-v0/credits.sexp` = 54439.
- [x] `.14` a51-7 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `38 credit(s), 38 current, 0 lapsed`; `python3 -B scripts/review_div_policy.py --every-retained 2>&1 | grep -c '11 of 11 legs satisfied; credited by'` = 38; `git diff --name-only dd298484 | grep -c '^evidence/'` = 0.
- [x] `.14` a51-6 **ROOT CAUSE** — the two were captured with no credit: `git show 45a334a2:profiles/rv64gc-lab-v0/credits.sexp | grep -c '(credit (id '` = 36.
- [x] `.14` a51-6 **ADDRESSED** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `38 credit(s), 38 current, 0 lapsed`; `python3 -B scripts/review_div_policy.py --every-retained 2>&1 | grep -c '11 of 11 legs satisfied; credited by'` = 38; `grep -c 'experiment "rv64gc-' profiles/rv64gc-lab-v0/gate.sexp` = 38.
- [x] `.14` a51-6 **NO REGRESSION** — `DIV-POLICY-PROBE: 59 tests / 0 failures / 0 errors`; `DIV-METHOD: 22 tests / 0 failures / 0 errors`; `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`.
- [x] `.14` a51-5 **ROOT CAUSE** — the two held declarations and no capture: `git ls-tree -r daadeb52 --name-only evidence/rv64gc-no-h-v1 | grep -c trace` = 0.
- [x] `.14` a51-5 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a51-5/capture.log` = 2; `python3 -B target/p4-system-14/a51-5/compare.py | grep -c 'byte-identical with the rehearsal: 22 findings: 0'` = 1; `git ls-files --others --exclude-standard profiles/rv64gc-lab-v0/reference | grep -c effect` = 4 before the commit.
- [x] `.14` a51-5 **NO REGRESSION** — `DIV-CAPTURE-INPUTS: 80 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `36 credit(s), 36 current, 0 lapsed`.
- [x] `.14` a51-4 **ROOT CAUSE** — the two held no case: at 2ff127b8 `git ls-tree 2ff127b8 evidence/ | grep -cE 'no-h|no-pmp'` = 0; and the alternative could not give a hart PMP entries: `git show 2ff127b8:schema/alternative.sexp | grep -c pmp_count` = 0.
- [x] `.14` a51-4 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a51-4/rehearse.txt` = 2; `grep -c 'effect rc=0' target/p4-system-14/a51-4/rehearse.txt` = 2; `grep -c '11 of 11 legs satisfied' target/p4-system-14/a51-4/rehearse.txt` = 2; `STATEMENT-TRACE: rv64gc-lab-v0: 38 of 38 requirements with a declared case trace`.
- [x] `.14` a51-4 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `36 credit(s), 36 current, 0 lapsed`; `REFERENCE-OVERLAY: 31 tests / 0 failures / 0 errors`; `DIV-CAPTURE-INPUTS: 80 tests / 0 failures / 0 errors`; `cargo test -p semulith-verify every_guest_matches` `rc=0`, on 206 guests.
- [x] `.14` a51-3 **ROOT CAUSE** — the six were captured with no credit: `git show b3d1f8e8:profiles/rv64gc-lab-v0/credits.sexp | grep -c '(credit (id '` = 30.
- [x] `.14` a51-3 **ADDRESSED** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `36 credit(s), 36 current, 0 lapsed`; `python3 -B scripts/review_div_policy.py --every-retained 2>&1 | grep -c '11 of 11 legs satisfied; credited by'` = 36; `grep -c 'experiment "rv64gc-' profiles/rv64gc-lab-v0/gate.sexp` = 36.
- [x] `.14` a51-3 **NO REGRESSION** — `DIV-POLICY-PROBE: 59 tests / 0 failures / 0 errors`; `DIV-METHOD: 22 tests / 0 failures / 0 errors`; `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`.
- [x] `.14` a51-2 **ROOT CAUSE** — the six held declarations and no capture: `git ls-tree -r 83f9ca4d --name-only evidence/rv64gc-priv-forms-v1 | grep -c trace` = 0.
- [x] `.14` a51-2 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a51-2/capture.log` = 6; `python3 -B target/p4-system-14/a51-2/compare.py | grep -c 'byte-identical with the rehearsal: 60 findings: 0'` = 1.
- [x] `.14` a51-2 **NO REGRESSION** — `DIV-CAPTURE-INPUTS: 80 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `30 credit(s), 30 current, 0 lapsed`.
- [x] `.14` a51-1 **ROOT CAUSE** — the six held no case: at 28b6fd30 `git ls-tree 28b6fd30 evidence/ | grep -cE 'composition|ext-closure|priv-revision|rvwmo|priv-insns|priv-forms'` = 0; and the override hid `wfi`: `grep -c '"wfi_is_nop": true' evidence/rv64gc-sstc-v2/reference-config.json` = 1.
- [x] `.14` a51-1 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a51-1/rehearse.txt` = 6; `grep -c '11 of 11 legs satisfied' target/p4-system-14/a51-1/rehearse.txt` = 6; `grep -c '"wfi_is_nop": false' evidence/rv64gc-priv-forms-v1/reference-config.json` = 1; `STATEMENT-TRACE: rv64gc-lab-v0: 36 of 36 requirements with a declared case trace`.
- [x] `.14` a51-1 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `30 credit(s), 30 current, 0 lapsed`; `REFERENCE-OVERLAY: 28 tests / 0 failures / 0 errors`; `DIV-POLICY-PROBE: 59 tests / 0 failures / 0 errors`; `DIV-CAPTURE-INPUTS: 80 tests / 0 failures / 0 errors`; `cargo test -p semulith-verify every_guest_matches` `rc=0`, on 204 guests.
- [x] `.14` a51-0 **ROOT CAUSE** — the route read the 17 from the override and not the binary: `grep -c 'moved verdict' target/p4-system-14/a51-0/variants.txt` = 17, `grep -c 'PTW: Step' target/p4-system-14/a51-0/ptw.trace` = 10, and at 620afecd `git show 620afecd:docs/decisions/decision_obligations-route.md | grep -c 'no behaviour a reference could be compared on'` = 1.
- [x] `.14` a51-0 **ADDRESSED** — `decision_the-seventeen-called.md` names a track for each of the 17, 6 + 2 + 4 + 4 + 1; `python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0 --json | grep -c 'excluded with an explicit not-applicable argument'` = 2.
- [x] `.14` a51-0 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `30 credit(s), 30 current, 0 lapsed`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`; `git diff --name-only 620afecd | grep -c EVIDENCE_POLICY` = 0.

