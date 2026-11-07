# P4-SYSTEM ordinary history — part 36

Ordinary, directly readable task history: the complete records of the closed `.14` units
a50-1 to a50-4, a50-c1 and a50-c2, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0384` on top of commit `45a334a27e2e0b45855da920648abf9559b33a09`
(7 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a49-4 to a49-0 and their rows are in part 35,
the earlier ones in parts 13–34. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a51-6, SEMULITH-P4-0384.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a50-c2 | 1162 | `1005827a6eb0b48eb23b08b60ff7a1d5aa0d0459f44508aec80d25e4ab8f8d81` |
| record a50-c1 | 934 | `1fad3a269952c60e6e57a5ff4e0854dbd130f428a11e7bea6ad708e28255209f` |
| record a50-4 | 1101 | `00aa7cef8646eb80fa351987a94a8f92ae61db8c853594942dc539dae821d6e1` |
| record a50-3 | 1513 | `079cf85ad817a82f8ac79215b7c1f3f8c1a735cc5e03b3ed689658696724c705` |
| record a50-2 | 2100 | `0655133804083eeda7da4f124c0e93dede2b643fef5cce1343a915115790227b` |
| record a50-1 | 1916 | `7ec9a468f141c93ee7f48b7bece2cfb2c66a02fa35593c224814e4261611617e` |
| acceptance rows a50-c2–a50-1 | 6656 | `cb35f26d34ab190716bd722caf7fc2ae6a4365040bef1d02948351e402b23d79` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-36.md)   # a span, by its line range
```

<a id="a50-c2"></a>

### .14 a50-c2 / SEMULITH-P4-0377: the capture guard is a tracked tool, and it held on a real run (completed)

Maintenance, counted neither way. Every capture from a43e-4 to a50-3 ran behind a copy of a script under `target/`, which git does not track, so a lost `target/` would have lost the procedure. **The tool.** `scripts/capture_guarded.py` holds what that script held, with three changes: the tree is judged again after any hold, the declaration commit must be an ancestor of HEAD, and regenerating the declarations is left to the preflight that already does it. **The proof.** `scripts/probe_capture_guarded.py`, 22 tests on stand-ins, 17 mutations each caught. It also ran seven real captures on a clone at the declaration commit: `rc=0` each, a second run skipping all seven, and all 35 compared files byte-identical to the retained captures. It is not an input of what it guards, so no credit moved.

**Also found and fixed.** `probe_config_effect.py` claimed "every retained effect" and read three of ten, since a50-3. It now reads all ten and refuses a retained effect its table does not judge. Book: `capture-plan.md`. Toolbox: `div-evidence.md`.

<a id="a50-c1"></a>

### .14 a50-c1 / SEMULITH-P4-0376: the CLI reads what its usage says (completed)

Maintenance, counted neither way. The live file reached its ceiling, so the closed records a49-0 to a49-4 and their rows moved verbatim to archive part 35. Found running the census at a50-3: the usage writes `--profile NAME` and `--steps N`, and every parser read only `--profile=NAME` and `--steps=N`, so `semulith run x.elf --profile rv64gc-lab-v0` answered `unknown option`. Both spellings now read the same, because a user following the usage is right and the book's and tests' `=` spelling must keep working: `joined_option_values` joins them once, before dispatch. A value option with no value is a usage refusal by name, and an unknown option stays its command's refusal. A unit test holds `VALUE_OPTIONS` to what the parsers read and what the usage shows, so a new option cannot bring this back. No path a case pins moved. Book: `plan/p1.md`.

<a id="a50-4"></a>

### .14 a50-4 / SEMULITH-P4-0375: the seven credited, each measured against what selects otherwise (completed)

Feature 5 of 5 after XTASK-0084. **The credits.** Seven records, `authority review`, each on its own case at 11 of 11 legs: `REQ-D-SVADE`, `REQ-D-ATOMIC-MISALIGN`, `REQ-D-FAULT-PRIORITY`, `REQ-D-PRIV-MODES`, `REQ-D-SV39`, `REQ-D-RESERVATION`, `REQ-D-SC-DETERMINISTIC`. See `decision_seven-credited-implemented.md`.

**What moved.** 30 `implemented`, 17 `planned`, 1 `not-applicable`; 32 cases, 30 credited, 2 fixtures. `G-TRACE` lists all 30. The reviews read the seven: `FEATURE_DISPOSITIONS`, `RETAINED_CAPTURES` from P4-0373 and P4-0374. `probe_div_policy.py`'s new `SWITCHES` table holds each first difference and each disposition's named properties to the case, with no new test method. Book: `requirement-status.md`'s table, `method-adequacy.md`, `policy-adequacy.md`, whose sampled `23 of 23` had been stale since a50-2.

**Corrected.** `CR-GC-ATOMICS-1` called its neighbours "still planned", and they no longer are. Next, `a50-c1` and `a50-c2`, then the XTASK turn, then the 17.

<a id="a50-3"></a>

### .14 a50-3 / SEMULITH-P4-0374: the seven captured exactly once each, the guard's load limit measured, and a CSR write census (completed)

Feature 4 of 5 after XTASK-0084. **The captures.** Each once from the declaration commit `40488d5b`, 1.2 s to 1.4 s each at load 21 to 26: each baseline and repeat `AGREE`, each control `DIVERGE` at its predeclared witness, each effect retained with its first difference at a witness. **All 77 compared files are byte-identical to the rehearsal, 0 findings** (`target/p4-system-14/a50-3/compare.py`).

**The guard.** The captures had waited 2 h 20 min for load below 8. 210 captures on a throwaway clone at load 15 to 73 gave 0 refusals, so the limit is now 32, with the spawn probe kept. See `decision_capture-guard-measured-at-load.md`.

**The census.** The `medeleg` read-back difference was an open item from a50-2. Written with all ones, it reads three ways, and the defect is in the pinned author, along with `mtvec` and `stvec`'s reserved MODE. No retained expectation reaches it (164 guests measured), and the fixes ride the next window, with the table's `medeleg` narrowed to `0xb3ff`. See `decision_csr-write-three-producers.md`.

Re-stated: the input probe's census (`1 + 32 * 22`), the status probe (`32, 23, 0, 23, 23`). Book: `canonical-division.md`'s table and effects, `prepared-inputs.md`, `requirement-status.md`. Corrected: `decision_declared-alternative-configuration.md`'s stale "eight retained effects". Family: 705 files, 6,076,510 B. Next, a50-4.

<a id="a50-2"></a>

### .14 a50-2 / SEMULITH-P4-0373: the seven with a real switch, declared, and what writing them found (completed)

Feature 3 of 5 after XTASK-0084. Nothing is captured or credited, and no retained case moved. **The programs.** Seven written for their statements, 149 witnesses over 1,181 steps, each held to the spec-side derivation, the lab engine and the pinned Sail on the case's configuration; 198 guests. **The clause trace.** Each statement is sliced at its own words, so `statement-trace.sexp` cannot drift from it, and every witness stands for a clause. **The finding.** Under the pinned override a misaligned AMO is judged after translation, where the statement and the lab judge it before, and no guest had that cell. Two cases select it through an overlay; the override moves with the next window. **Overlays and alternatives.** An overlay may now name no device, and gains `misaligned_amo` and `require_exact_reservation_addr`, so "covering exactly" is witnessed. The alternative's two reservation knobs, which a50-1 added on a measurement, leave: nothing uses them once those two cases compare with the override. **Four excerpts** (`materials/RVI_EXTENSION_RETENTION.md`; `materials/` is at its ceiling, so they joined the record that already holds that table's kind of review). **Rehearsal:** on a clone, 7 captured in 10 s, each control where declared, each effect retained, 11 of 11 legs each (`target/p4-system-14/a50-2/rehearse.txt`). Re-reading the witnesses before declaring found one defect of mine that every check had passed: a witness called the word zero "the address", so `illegal-tval` left before anything froze. The gate's citation arm found a second: `menvcfg` cited at a section the pinned page does not have, corrected to `§2.1.1.18` before anything froze. It also read a self-test miss on `unit-charge` at a host load of 35, a sibling project's build: the collector's known EPERM race (`target/p4-system-14/collector-race/FINDING.md`), one more than the arm's 3 failures, so this gate waited for the load to fall. `decision_seven-with-a-switch.md` holds the table.

<a id="a50-1"></a>

### .14 a50-1 / SEMULITH-P4-0372: a case may declare what selects otherwise, and its effect is measured against that (completed)

Feature 2 of 5 after XTASK-0084. **The change.** `reference/<case-id>.alternative.sexp` (`schema/alternative.sexp`, a closed vocabulary of seven knobs) states the choice the profile did not make; `prepare_div_inputs.py` renders it over the case's configuration, `measure_config_effect.py` runs it, the review pins its rendering, and `census_reference_config.py --alternative` says what it moves. No case declares one yet, and nothing a case pins moved: 23 credits current. **Why this slice alone.** The seven need three new guests, and proving the tool first means a capture can only fail for a reason of its own. **Measured before the design** (`target/p4-system-14/a50-0/`, then `target/p4-system-14/a50-1/census-*.txt` through the real tool): each candidate over the 190 compared guests, in `decision_declared-alternative-configuration.md`, and it corrects the route's first table. The binary refuses `S`, `U` or `Sv39` off alone, so a declaration holds a set; the region's own misaligned attribute moves nothing, so the vocabulary names the global check; and zero guests witness `Sv48` or a same-hart store's invalidation. **The controls.** `REFERENCE-OVERLAY` 14 to 24 tests with seven new mutations, `CONFIG-EFFECT` 10 to 13 with two, `DIV-POLICY-PROBE` 55 to 58 with one, each fired. **Two defects, each mine, caught here.** a49-4's first gate failed on a stated test count in `xtask/`, a tree my search for it had left out, so this unit greps `xtask/` too; and `gate_report.py <profile> --help` wrote `G0-REPORT.md` because the tool reads no such flag: it was removed before it reached a commit, and it stays a wart of that usage line. **The tripwire, read.** The gate took 23.5 minutes at a49-4 with 25 cases, down from 28.7 with 48, so a case costs about 13 seconds of gate.

<a id="acceptance-rows-a50-c2-to-a50-1"></a>

## acceptance-rows-a50-c2-to-a50-1

- [x] `.14` a50-c2 **ROOT CAUSE** — the guard was untracked: at 25be8741 `git ls-tree -r 25be8741 --name-only scripts | grep -c capture_guarded` = 0, and `git check-ignore -q target/p4-system-14/a50-3/capture.sh` `rc=0`.
- [x] `.14` a50-c2 **ADDRESSED** — `CAPTURE-GUARD: 22 tests / 0 failures / 0 errors`; every mutation caught: `grep -c 'capture guard' target/p4-system-14/a50-c2/mutations.txt` = 34, the 17 in both Python modes, and `grep -c '0 failures / 0 errors' target/p4-system-14/a50-c2/mutations.txt` = 0; on a clone `grep -c 'capture rc=0' target/p4-system-14/a50-c2/clone-run.txt` = 7, and `grep -c 'byte-identical 35 differ 0' target/p4-system-14/a50-c2/clone-run.txt` = 1.
- [x] `.14` a50-c2 **NO REGRESSION** — `CONFIG-EFFECT: 13 tests / 0 failures / 0 errors`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `30 credit(s), 30 current, 0 lapsed`; `grep -c capture_guarded evidence/rv64gc-svade-v1/dependencies.sexp` = 0.
- [x] `.14` a50-c1 **ROOT CAUSE** — the usage named a spelling no parser read: at 524914a8 `git show 524914a8:crates/semulith-cli/src/main.rs | grep -c 'strip_prefix("--steps ")'` = 0, while the usage's `[--steps N]` was on every `run` line; `semulith run x.elf --profile rv64gc-lab-v0` answered `run: unknown option --profile`, rc=2.
- [x] `.14` a50-c1 **ADDRESSED** — `cargo test -p semulith-cli --bin semulith` `rc=0`, 4 passed; `cargo test -p semulith-cli --test option_spellings` `rc=0`, 4 passed. They discriminate: `grep -c FAILED target/p4-system-14/a50-c1/mutations.txt` = 2, a list missing `--warmup` (1 of 4 unit tests) and the join removed (3 of 4 integration tests).
- [x] `.14` a50-c1 **NO REGRESSION** — `cargo test -p semulith-cli` `rc=0`, every target ok, including the `=` spelling the existing replay and reduce tests use; `git diff --name-only 524914a8 | grep -c evidence/` = 0.
- [x] `.14` a50-4 **ROOT CAUSE** — the seven were captured with no credit: at 633fe0cb `git show 633fe0cb:profiles/rv64gc-lab-v0/credits.sexp | grep -c '(credit (id '` = 23, and `git show 633fe0cb:profiles/rv64gc-lab-v0/credits.sexp | grep -c SVADE` = 0.
- [x] `.14` a50-4 **ADDRESSED** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `30 credit(s), 30 current, 0 lapsed`; `python3 -B scripts/review_div_policy.py --every-retained 2>&1 | grep -c '11 of 11 legs satisfied; credited by'` = 30; `grep -c 'experiment "rv64gc-' profiles/rv64gc-lab-v0/gate.sexp` = 30.
- [x] `.14` a50-4 **NO REGRESSION** — `DIV-POLICY-PROBE: 58 tests / 0 failures / 0 errors`; `DIV-METHOD: 22 tests / 0 failures / 0 errors`; `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`; `MATCHED-GPR-PROPERTY: 36 tests / 0 failures / 0 errors`; the only frozen-list path moved is the status record the act must move, `profiles/rv64gc-lab-v0/requirements.sexp`, an authority view no manifest pins: `git diff --name-only 633fe0cb | sort | comm -12 - <(sort target/p4-system-14/a50-3/frozen-paths.txt) | wc -l` = 1, and all 30 credits read current.
- [x] `.14` a50-3 **ROOT CAUSE** — the seven held declarations and no capture: at 40488d5b `git ls-tree -r 40488d5b --name-only evidence/rv64gc-svade-v1 | grep -c trace` = 0. The guard's limit was unmeasured: `grep -c holding target/p4-system-14/a50-3/run/wait.log` = 41. The author stores `medeleg` as written: `grep -c 'author!=rust' target/p4-system-14/a50-3/csr-write/census.txt` = 3.
- [x] `.14` a50-3 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a50-3/capture.log` = 7; `python3 -B target/p4-system-14/a50-3/compare.py | grep -c 'byte-identical with the rehearsal: 77 findings: 0'` = 1; `grep -c 'captures 210; rc non-zero 0; EPERM mentions 0' target/p4-system-14/a50-3/load-rehearsal/summary.txt` = 1; `grep -c 'outside the table' target/p4-system-14/a50-3/csr-write/guest_writes.txt` = 1 with `: []`; the two records name each next-window fix.
- [x] `.14` a50-3 **NO REGRESSION** — `DIV-CAPTURE-INPUTS: 80 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 23 tests / 0 failures / 0 errors`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `23 credit(s), 23 current, 0 lapsed`; the status probe re-states `32, 23, 0, 23, 23`; no pinned path moved: `git diff --name-only 40488d5b | sort | comm -12 - <(sort target/p4-system-14/a50-3/frozen-paths.txt) | wc -l` = 0.
- [x] `.14` a50-2 **ROOT CAUSE** — the seven held no case: at 9331acac `ls evidence | grep -cE 'svade|atomic-misalign|fault-priority|priv-modes|sv39|reservation|sc-deterministic'` = 0, and each reads `planned`.
- [x] `.14` a50-2 **ADDRESSED** — `grep -c 'capture rc=0' target/p4-system-14/a50-2/rehearse.txt` = 7; `grep -c 'effect rc=0' target/p4-system-14/a50-2/rehearse.txt` = 7; `grep -c '11 of 11 legs satisfied' target/p4-system-14/a50-2/rehearse.txt` = 7; `python3 -B scripts/statement_trace.py --profile rv64gc-lab-v0 --requirement REQ-D-SVADE` `rc=0`; `cargo test -p semulith-verify every_guest` passes over 198 guests.
- [x] `.14` a50-2 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `23 credit(s), 23 current, 0 lapsed`; `python3 -B scripts/prepare_div_inputs.py --verify --case rv64gc-sstc-v2` `rc=0`, an existing overlay byte-identical; `git diff --cached --name-only | grep -Fxcf target/p4-system-14/a49-4/pinned.txt` = 0; `REFERENCE-OVERLAY: 26 tests / 0 failures`, 18 mutations each `rc=1`; `DIV-CAPTURE-INPUTS: 80 tests / 0 failures`.
- [x] `.14` a50-1 **ROOT CAUSE** — `_config_effect` compares only with the profile override, and for these requirements the override is the selection: at dd0d2282 `grep -c 'alternative.sexp' scripts/measure_config_effect.py` = 0, and `python3 -B scripts/measure_config_effect.py --help` offers no way to name another choice.
- [x] `.14` a50-1 **ADDRESSED** — `python3 -B scripts/probe_reference_overlay.py` `rc=0` → `REFERENCE-OVERLAY: 24 tests / 0 failures`; `python3 -B scripts/probe_config_effect.py` `rc=0` → `CONFIG-EFFECT: 13 tests / 0 failures`; `python3 -B scripts/probe_div_policy.py` `rc=0` → `DIV-POLICY-PROBE: 58 tests / 0 failures`; `grep -c 'DIVERGE  |' target/p4-system-14/a50-1/census-svade.txt` = 1, the real binary through the real tool.
- [x] `.14` a50-1 **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` `rc=0` → `23 credit(s), 23 current, 0 lapsed`; `git diff --cached --name-only | grep -Fxcf target/p4-system-14/a49-4/pinned.txt` = 0; `grep -c 'observed effect under the profile override' scripts/probe_div_policy.py` = 4, the existing cases' text unchanged.

