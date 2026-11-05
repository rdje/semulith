# P4-SYSTEM ordinary history — part 28

Ordinary, directly readable task history: the complete records of the closed `.14` units
a43c-1, a43c-2 and a43c-3, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0350` on top of commit `78c8fea2ada45ab6cd35c55c83a901091c3edeff`
(4 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a43b-3d … a43b-3h and their rows are in part 27,
the earlier ones in parts 13–26. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a45-1, SEMULITH-P4-0350.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a43c-3 | 1871 | `4b48c9cd5a068b0d2d75c142c90c5f1f20660cd9f07eb5046a1ab25af34a533c` |
| record a43c-2 | 2231 | `7fe0df8f38245ea1da630fd5df9d4086cf9169c0318ccd067fa25afa962b32ba` |
| record a43c-1 | 3729 | `11ae7aa819dc97543cf1a712fa494b0db2571fc1fca6393c76742810f325c9c2` |
| acceptance rows a43c-3–a43c-1 | 2858 | `164ee8ad91188b49bdd785fc62962a22cf12af2d29294d2779e2e7ee46b39408` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-28.md)   # a span, by its line range
```

<a id="a43c-3"></a>

### .14 a43c-3 / SEMULITH-P4-0343: the ZICNTR case's three declarations, committed before its capture — and the director's ruling on the dossier copies (completed)

Feature 3 of 5 after XTASK-0077. `python3 -B scripts/capture_div.py --declare --case rv64gc-zicntr-v1` emitted the planned experiment (24,132 B), the dependency manifest (15,175 B, **67** children) and the authority record (17,734 B), written exclusively from the command's output. This commit is the declaration commit a43c-4 names. The manifest differs from CSR-SET's in exactly its two case-specific children: the case's own declaration and `RVI-ZICNTR-STATEMENTS` as the normative child. Neither the overlay nor the prepare tool is a child; the manifest pins the configuration they render, byte for byte. The literal guard holds on the record: "quotient" absent. `retain_div_capture.py --preflight-only` → `ready`. Measured: `MATCHED-GPR-CASE: 8 tests / 0 failures` (the planned population is eight); `REQUIREMENT-STATUS: … 8 case(s), 3 credited, 1 declared … 0 drift`; `CREDIT-RECORDS: … 3 current, 0 lapsed`. Frozen until the capture: the 67 children and the 13 authority views.

**The director's ruling (a43b-c3 closed):** "Let's do as you recommended it", the standard "sota, signoff and production-grade", and "they shall serve the project long-term". `decision_dossier-copies-retire-at-the-next-window.md` records it: no copy for a new case until the next pinned window, which retires them all, and no window opened for this alone. **Measured while recording it:** the report generator is a pinned input of every experiment for one reason, `scripts/experiment_verification.py:39`, `from gate_report import contract_measure`. So the window also moves that function out, and editing a report never lapses evidence again: a class of lapse removed rather than paid for once. Next: a43c-4.

<a id="a43c-2"></a>

### .14 a43c-2 / SEMULITH-P4-0342: the ZICNTR program and its case — 292 steps, 44 predeclared witnesses, in M, S and U (completed)

Feature 2 of 5 after XTASK-0077. **The program.** `profiles/rv64gc-lab-v0/guests/zicntr.s`, 163 instructions, 292 executed steps, new in the corpus (`run-order.txt`, an `interactions.sexp` cell beside `mm-counters`). **Judged three ways before anything was declared:** the spec-side author wrote 292 steps, 584 fetches, schema-valid; the lab fixture `every_guest_matches_its_expectations` `ok` (172 guests, byte fixture regenerated); the pinned Sail under the overlay `AGREE 292 declared steps`. **The overlay.** `reference/rv64gc-zicntr-v1.overlay.sexp`: the same three knobs as CSR-SET's, and its rendered configuration is byte-identical (`05746ed6…`, 8,748 B). **The case.** `evidence/rv64gc-zicntr-v1/case.sexp` (43,349 B): REQ-D-ZICNTR / OB-ZICNTR on RVI-ZICNTR §6.1, normative input `RVI-ZICNTR-STATEMENTS`, `implementation-defined`, high; 44 properties, each value written from the chapters and held to the derivation (target/p4-system-14/a43c/draft/draft_case.py, every assertion passing on its first run: `cycle` is the boundary, `instret` the boundary minus the trapped boundaries before it, read from the program's shape); 26 `(boundary: …)` rows, each a declared property's step, which the draft asserts; control `refused-read-committed`, x21 at boundary 109 expected 21, the wrong value 102, the count S's refused read at boundary 102 would have committed; `second_method` as CSR-SET's; `adversarial` the 13 rd-kept properties. **The prepared inputs:** `prepare_div_inputs.py --write` (guest 4,960 B; configuration 8,748 B; baseline 50,381 B; control 48,335 B). **The family's seventh re-derivation** (`decision_evidence-family-two-cases.md`, Addendum a43c-2): 177 files, 112 MiB, `retention_limits()` 110,628,864 B, 160 present. The input probe gains `ZicntrCaseInputTests` (49 → 64 tests; `actual-layout` still 6). CHANGELOG shard: head compacted (`scripts/shard_history.py`). Book: the prepared-inputs and references pages. No retained case moved; `CR-D-CSR-SET-1` and the other two stay current. Status unchanged: a case with no declarations binds nothing. Next: a43c-3.

<a id="a43c-1"></a>

### .14 a43c-1 / SEMULITH-P4-0341: the ZICNTR case designed, and its normative statements retained (completed)

Feature 1 of 5 after XTASK-0077. **The route:** CSR-SET's, without its one-time costs: the overlay, the effect tool, the category branch and the credit's shape exist. Five units: this one; a43c-2, the program, its case, its overlay, the family's re-derivation; a43c-3, the declarations; a43c-4, the capture once, with the effect; a43c-5, the reviews and the credit (G-STATE 3 of 4). **Measured on a draft (target/p4-system-14/a43c/draft, `gen_program.py`, `zicntr.s`, 163 instructions, 292 steps, expected 50,381 B):** under the overlay's configuration `AGREE 292 declared steps`; under the profile override `DIVERGE step 6 (rdcycle x5): Sail {}, expectations {'x5': 6}`. The capture plan's item 2 had `cycle` and `time` values stay corpus-judged; a43b-3a's measurement withdrew that, and here they agree at every read. The engine judges it at a43c-2, when the guest enters the corpus.

**The program's sections:** M with no gate (the three views, the two machine views); progress (`instret` by retirement, `cycle` by boundary); five read-only write attempts in M with `rd` kept, plus the two legal read forms; a trap retires nothing (`cycle` minus `instret` grows by the refused boundary); S with each gate configuration (closed; CY alone; all three, the read a kernel needs); U under both gates (`scounteren` clear; IR alone; `mcounteren.IR` clear with `scounteren.IR` set); `mcycle`/`cycle` and `minstret`/`instret` at adjacent boundaries. Control: S's refused `rdcycle` at closed gates, expecting the count it would have committed: "a refused counter read that committed must diverge". The handler dispatches on the cause: a refused access returns to its own mode, an environment call to M.

**Three drafts failed and taught something (the draft's history, §15):** my first entry offset returned to the `mret` itself, which S then refused: the extra traps were visible as `x30` writes the program did not plan; a refused read's sentinel of -1 repeated across gates was no change after the first, so its witness vanished ("a same-value write is not a change"): each now has its own; and a hand count of the budget was wrong, so the budget is read from the derivation. **Out of scope, both to be named in the limitations:** a write through `mcycle` or `minstret` (the deriver refuses: "writable counter rebasing is outside this bounded author's scope"; it is pinned, and the laboratory's `time` is a view of `mcycle` in `state.sexp` where the reference's comes from its CLINT, so a write would separate them), and Zihpm's absence (the deriver's vocabulary is the 33).

**Retained:** `RVI-ZICNTR-STATEMENTS` (§6.1, §6.1.1; six statements; `ee5bca84…`, 3,094 B), the normative input; `RVP-COUNTEREN-STATEMENTS` (§2.1.1.11; four; `a47ba183…`, 2,806 B), what the refused reads rest on. Two rows in `retain_statements.py`, whose page bound moved from 262,144 to 524,288 B because `priv/machine.html` is 271,851 B; the tool is pinned by no case. `scounteren`'s statement has no anchor in its page, so it is cited and not retained (`materials/RVI_ZICNTR_RETENTION.md`). `--verify` `matched` for all three excerpts; `STATEMENT-RETENTION: 19 tests / 0 failures`; the gate refused once on my own miss, the `retained-pin` seam's count, which fails once per tracked excerpt (2 → 4). No case or credit moves. **Logged for the EPERM hunt:** on 2026-11-04 under load, the shell itself printed `child setpgid (63594 to 63594): Operation not permitted`, bash's own process-group setup with no tool involved, so the host refuses process-group calls in some racy states; no gate strike this session has named its site yet.

<a id="acceptance-rows-a43c-3-to-a43c-1"></a>

## acceptance-rows-a43c-3-to-a43c-1

- [x] `.14` a43c-3 **ROOT CAUSE** — the case had no declarations: at cab19894 `git ls-files evidence/rv64gc-zicntr-v1 | wc -l` = 5 of its 22 slots, and `python3 -B scripts/requirement_status.py` read `7 case(s), 3 credited, 0 declared`.
- [x] `.14` a43c-3 **ADDRESSED** — `python3 -B scripts/capture_div.py --declare --case rv64gc-zicntr-v1` `rc=0`, three files written exclusively (target/p4-system-14/a43c/declare.json); `python3 -B scripts/retain_div_capture.py --preflight-only` `rc=0`, `ready`; `grep -c 'experiment_verification' docs/decisions/decision_dossier-copies-retire-at-the-next-window.md` = 1, the ruling recorded.
- [x] `.14` a43c-3 **NO REGRESSION** — `MATCHED-GPR-CASE: 8 tests / 0 failures`, `DIV-CAPTURE-INPUTS: 64 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DIV-METHOD: 22 tests / 0 failures`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `3 credit(s), 3 current, 0 lapsed`.
- [x] `.14` a43c-2 **ROOT CAUSE** — no program or case for the requirement: at 533f945c `git ls-files evidence/rv64gc-zicntr-v1 | wc -l` = 0 and `git ls-files profiles/rv64gc-lab-v0/guests/zicntr.s | wc -l` = 0, and the family's bound held seven cases (`grep -c 'seven by a43b-3d' doctrine/readme_routes.tsv` = 1).
- [x] `.14` a43c-2 **ADDRESSED** — `python3 -B scripts/derive_rv64gc_expectations.py --parcels --steps 292` wrote 292 steps, schema-valid; `every_guest_matches_its_expectations` `ok`, 172 guests; `python3 -B scripts/prepare_div_inputs.py --verify --case rv64gc-zicntr-v1` `rc=0`; `python3 -B scripts/probe_div_capture_inputs.py` → `DIV-CAPTURE-INPUTS: 64 tests / 0 failures / 0 errors`.
- [x] `.14` a43c-2 **NO REGRESSION** — `bash scripts/check_guest_gen.sh` `rc=0` → `GUEST-GEN: ok`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `3 credit(s), 3 current, 0 lapsed`; `git diff --cached --name-only` holds no path of the three manifests (`grep -c` 0 each, target/p4-system-14/a43c/staged2.txt).
- [x] `.14` a43c-1 **ROOT CAUSE** — ZICNTR had no program or retained statement: at 8aa34ba0 `git ls-files profiles/rv64gc-lab-v0/guests/zicntr.s | wc -l` = 0 and `grep -c 'Excerpt(' scripts/retain_statements.py` = 1; CHK-ZICNTR-POS and -NEG rest on two corpus guests no case names.
- [x] `.14` a43c-1 **ADDRESSED** — `python3 -B scripts/retain_statements.py --verify | grep -c matched` = 3, `rc=0`; target/p4-system-14/a43c/draft on the draft: `zicntr-clint-ipt1 AGREE 292 declared steps`, `base DIVERGE step 6 (rdcycle x5)`.
- [x] `.14` a43c-1 **NO REGRESSION** — `python3 -B scripts/probe_statement_retention.py` → `STATEMENT-RETENTION: 19 tests / 0 failures / 0 errors`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `3 credit(s), 3 current, 0 lapsed`; `grep -c retain_statements evidence/rv64gc-csr-set-v1/dependencies.sexp` = 0.

