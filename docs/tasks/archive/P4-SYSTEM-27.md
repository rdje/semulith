# P4-SYSTEM ordinary history — part 27

Ordinary, directly readable task history: the complete records of the closed `.14` units
a43b-3d, a43b-3e, a43b-3f, a43b-3g and a43b-3h, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0345` on top of commit `e5814f187a28360d1ad8b2df31785444b5701ed1`
(6 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a43b-2d … a43b-3c and their rows are in part 26,
the earlier ones in parts 13–25. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a43c-5, SEMULITH-P4-0345.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a43b-3h | 2045 | `90c8d48b5faf0ddf27d8f396bc1672756bad54dd4ec5277af7230682d06e6ed0` |
| record a43b-3g | 3168 | `e220379422379298b231df6d7c794904589fd78cb15106835d98eb9db57a0447` |
| record a43b-3f | 3218 | `10c4d011776f4cf811ba9d8cda2ae9f55b7899d805bfc4e583b5a0a6bd8eff19` |
| record a43b-3e | 1953 | `134ad507da9f67a965bc11a7429986e3ffb0b058287a05f7da91702909172d5c` |
| record a43b-3d | 3024 | `b160ff1d3e67f9f4caf382b8363de53d4cc6fc8f26d86503325f34d00bd18a5e` |
| acceptance rows a43b-3h–a43b-3d | 6663 | `ebcabd6873fda81204a896453b01bc9e0643da4d624632abd20de5b646fbf0ad` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-27.md)   # a span, by its line range
```

<a id="a43b-3h"></a>

### .14 a43b-3h / SEMULITH-P4-0340: `REQ-D-CSR-SET` credited `implemented` — the first `implementation-defined` requirement, G-STATE 2 of 4 (completed)

The third step of the capture plan's route for its second case. `CR-D-CSR-SET-1` in `credits.sexp`, `authority review`: the measured record (`a0de4f8c…`, 27,346 B), the receipt
(`69e526d5…`, 7,050 B), the policy pinned, `RVP-CSR-STATEMENTS` retained, seven limitations. `implementation_status implemented` on `REQ-D-CSR-SET`. `decision_req-d-csr-set-credited-implemented.md`
(new, INDEX, KNOWLEDGE_MAP). Measured: `REQUIREMENT-STATUS: … 45 planned, 3 implemented; 7 case(s), 3 credited, 0 declared, 3 of 3 credit record(s) current; 0 drift`;
`CREDIT-RECORDS: … 3 current, 0 lapsed`; `rv64gc-csr-set-v1: DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-D-CSR-SET-1`. GS: `2 of 4 state requirements implemented`,
3 of 10 axes open, G-TRACE green. **What the credit does not claim is in its record:** `mip`'s value directly, a CLINT or any device, a non-member address trapping (the deriver's vocabulary is the 33,
pinned), field semantics, counter rates, timer delivery, numerics. **The dependencies stay `planned`:** the derivation reads obligations, and the plan orders CSR-SET before ZICNTR and SSTC; the status probe
states it. **Departure from the plan's step (iii), raised to the director (a43b-c3):** the dossier copy and its `G-TRACE` row are left out. `references.sexp` is 50,323 B, the measured record 27,346 B, together 77,669 B against the
per-part 65,536 B; all three manifests pin `scripts/gate_report.py` and `scripts/dossier_sexp.py` (`grep -c`, each 1), so a split lapses all three credits. The qualification still reads true (`probe_dossier_qualification`: the record qualifies, and a test holds the
dossier to the other two, so a later copy re-states it). Stale claim fixed: LIVE_STATUS's "the pinned reference has no Zicntr or timer source", superseded by a43b-3a and missed there. Feature 5 of 5 after XTASK-0076: the turn is XTASK.13 b4, next.

<a id="a43b-3g"></a>

### .14 a43b-3g / SEMULITH-P4-0339: the reviews read the CSR-SET case, and the comparison leg reads the requirement's category — 10 of 10 (completed)

**The defect the case surfaced (§15).** `review_div_policy.py` measured `defined`'s row for every category: a case on its own configuration would have satisfied the
`matched-reference-comparison` leg with the configuration alone, against the policy's words ("A configuration file without an observed effect" is insufficient). Measured
before the fix, on a43b-3f's bytes: the leg read `method …; baseline AGREE; …` and never opened the effect record. **The fix.** `_category_row`: `defined` asks nothing more,
and its measured text stays byte-identical for M and XLEN (a test pins it); `implementation-defined` needs `source_semantics.detail` and `_config_effect`; any other category
stays pending and is named. `_config_effect` reads `<case>.effect.sexp` and trusts no verdict: seven pins against the case's own bytes (its case, the guest, the case's
configuration, the reference producer's version as the binary, an alternative different from the case's and equal to the profile override as rendered, the trace's digest and
size), then `compare_observations` re-derives the first difference offline, which must fall at a declared property's step. A record without its trace, or malformed, refuses.
No process runs. The profile override stays unpinned by any case: if it moves, `DIV-CAPTURE-INPUTS` already refuses every case's `--verify`, so this adds no quieter coupling.

**The reviews.** `RETAINED_CAPTURES` names the case (declared 02835e0f, captured a6f7d8fd, `a0de4f8c…`, 27,346 B). `python3 -B scripts/review_div_method.py --case rv64gc-csr-set-v1`:
`satisfied`, 88 authenticated files, 1,228,197 B, snapshot 141,763 B, 1,315,764 B charged of 134,217,728. `FEATURE_DISPOSITIONS["OB-CSR-SET"]` is the first that says a rule applies:
the privilege and CSR rule, covered by the case's properties for legal and refused modes, aliases and state preserved after every refusal; the counter and floating-point rules stay
with their own requirements. A probe test checks that each of its 20 property names is one the case declares. `python3 -B scripts/review_div_policy.py --every-retained` prints
`rv64gc-csr-set-v1: DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit`, and the leg ends `selection recorded; observed effect under the profile override: step
34 (csrrs x20, mcycle, x0): Sail {}, expectations {'x20': 34}`. Seven boundary rows, 53 vacuous-coverage witnesses, the control at step 130 x28, `risk high` through its five conditions.
**The controls.** `DIV-POLICY-PROBE`: 33 → 48 tests, 15 → 27 seams, each RED in both modes (`seams.txt`); PROFILE-CONSISTENCY re-pinned. Book: the policy page (a new section with both tables,
the ten legs and the run), method, division, references, status pages; toolbox row. Containment: five closed records and their rows moved verbatim to archive part 26. Next: a43b-3h,
the credit, carrying the limits: `mip`'s value through `sip` only, the CLINT unclaimed, no non-member witness, field semantics with P4-SYSTEM.2, one finite case.

<a id="a43b-3f"></a>

### .14 a43b-3f / SEMULITH-P4-0338: the CSR-SET case captured exactly once, and its configuration's effect retained (completed)

**The capture.** `target/p4-system-14/a43b-3f/capture-when-quiet.sh` ran it once, never retried, after three consecutive quiet minutes to 04:21Z
(no stitchcad or specforge process, 1-minute load 5.69, 5.82, 5.22: `rv64gc-csr-set-v1/wait.log`) and its guards: a clean tracked tree; no frozen path moved
(`02835e0f` was still HEAD, 91 paths); the declarations equal to their regeneration; `--preflight-only` `ready`. `retain_div_capture.py --case rv64gc-csr-set-v1
--declaration-commit 02835e0f…` ran 1.3 s: three zero-exit processes; baseline and repeat AGREE over 157 declared steps; the control DIVERGE at its declared
step 130, `csrrs x28, mscratch, x0`, Sail x28 = 5, the expectation 9. `complete_canonical_capture` true, qualification false, all nine findings matched or
satisfied, 24,908,272 B charged of 134,217,728. 14 files retained: three traces of 13,833 B, byte-identical (`cmp`), three stdout streams identical, each stderr
printing its own trace's name; the measured record 27,346 B (`a0de4f8c…`), `verification.json` 7,050 B (`69e526d5…`). The family holds all 155 files, 987,939 B.
`REQUIREMENT-STATUS: … 7 case(s), 2 credited, 0 declared`: the case `pending`, both credits current. Re-stated: the input probe's member count (141 → 155), the
status probe's row. As at a43b-2d, the retained-capture row moves with the reviews (a43b-3g): a row names its capture commit, which is this commit.

**The observed effect.** The policy's `implementation-defined` row asks for a behavior-changing control, and a capture observes only its own configuration, so
`scripts/measure_config_effect.py` ran the same guest through the same pinned binary under the profile override, exactly once, and retained the raw trace
(`profiles/rv64gc-lab-v0/reference/rv64gc-csr-set-v1.effect.trace`, 14,236 B, `2a828052…`) and what ran by digest (`.effect.sexp`, 762 B, `schema/config-effect.sexp`:
binary, guest, both configurations, step budget, trace). It printed `step 34 (csrrs x20, mcycle, x0): Sail {}, expectations {'x20': 34}`, a43b-3a's measured
result, now on retained bytes. The alternative's digest `666d9373…` is the digest of each of the other six cases' `reference-config.json`. Diffing the raw traces: identical through
line 66, then at line 67 the case's `x20 <- 0x0000000000000022` against `trapping from M to M to handle illegal-instruction`. The record carries no verdict; a43b-3g's
review re-derives it. `scripts/probe_config_effect.py`: 10 tests, nine guard omissions RED in both modes (`effect/mutations.txt`), now in PROFILE-CONSISTENCY, with a stand-in
binary so no reference process runs, and one test holding the retained record to its case's bytes. The schema census: 29 files, 133 facets, all six new facets using two
already-reviewed token languages; RECORD-SCHEMA's pinned mutation counts re-derived with them (loose-end 132 → 138, ignore-pattern 768 → 804, the focused run named the miss). Book: the division page (the capture's table), the references page (the record and the commands), status and prepared-inputs pages.
Next: a43b-3g, the reviews.

<a id="a43b-3e"></a>

### .14 a43b-3e / SEMULITH-P4-0337: the CSR-SET case's three declarations, committed before its capture (completed)

`python3 -B scripts/capture_div.py --declare --case rv64gc-csr-set-v1` emitted the planned experiment (27,316 B), the dependency manifest (15,170 B, **67** children) and the authority record (17,735 B), written exclusively from the command's `files` map; this
commit is the declaration commit a43b-3f names. The manifest differs from xlen-v2's in exactly its two case-specific children: the case's own declaration and `RVP-CSR-STATEMENTS` as the normative child. Neither the overlay nor the prepare tool is a child: the case pins the
configuration they render, byte for byte (`reference-config.json`), so a later overlay edit cannot reach this capture, and `--verify` would name it. The literal guard holds on the record: control id `refused-write-committed`, control prose "Predeclared target: a refused CSR write that committed
must diverge.", "quotient" absent. `retain_div_capture.py --preflight-only` → `ready`. Measured: `MATCHED-GPR-CASE: 8 tests / 0 failures` (the planned population is seven); `REQUIREMENT-STATUS: … 7 case(s), 2 credited, 1 declared … 0 drift`: the case binds REQ-D-CSR-SET and credits nothing; the family holds 141 files.
Frozen until the capture: the 67 children and the 13 authority views. No XTASK slice is due before it. **Found by the gate, a flake fixed (§15):** the commit gate refused once on `DIV-COMMAND`, `1260 pass / 4 fail`, each miss the same `TimeoutExpired`: `probe_div_command.py` gave `capture_div.py --declare` 15 s, and a sibling repository's verification held this host at load 28 (selftest-load-timeout.log). The command takes 0.58 s on a quiet host, so the timeout measured the neighbour, not the tool; it is now the probe's own 120 s, as its other process arm already was, and the command is still bounded. Next: a43b-3f, the capture, exactly once, and the alternative trace.

<a id="a43b-3d"></a>

### .14 a43b-3d / SEMULITH-P4-0336: the CSR-SET program and its case — all 33 CSRs, 53 predeclared witnesses, in M, S and U (completed)

a43b-3a's D2 and D3, on the overlay of a43b-3c. **The program.** `profiles/rv64gc-lab-v0/guests/csr-set.s`, rewritten before any capture: 136 instructions, 157 executed steps.
Every CSR of the committed 33 is witnessed: 32 read into a sentinel-loaded register, so a reset value of 0 is still an observed change; `mip` read with `rd` = x0 and a marker after it, because
this case's reference holds `mip.MTIP` (a43b-3a, M3). Then four alias pairs: `sie`→`mie` 2; `mip`→`sip` 2, the pair the plan named and a43b-1 dropped, and `sip`'s clear before S could take it; `sstatus`→`mstatus`;
`fflags` and `frm`→`fcsr` 0x9f; FS Dirty with SD. The refused accesses: `csrrw` and `csrrs` with `rs1` ≠ x0 on the read-only `mhartid`, each with `rd` read back (7, 8) and `mhartid` kept; S's write of 9 to `mscratch` and
U's to `sscratch`, the handler reading both in M. Their legal neighbours: `csrrs` with `rs1` = x0 on `mhartid`, `sscratch` in S, `fflags` in U. Seven `(boundary: …)` tags, each a declared property's step. **Judged three ways before
anything was declared:** the spec-side author wrote 157 steps, 314 fetches, schema-valid; the lab fixture `every_guest_matches_its_expectations` `ok` (171 guests, byte fixture regenerated); the pinned Sail under the overlay `AGREE 157 declared
steps`. Every section the source cites was checked against the pinned page's headings, which the old source's were not (a43b-3c, a43b-c1). **The case.** `evidence/rv64gc-csr-set-v1/case.sexp` (34,135 B): REQ-D-CSR-SET / OB-CSR-SET on RVP-CSR §1.1.1, normative input `RVP-CSR-STATEMENTS`,
`implementation-defined`, high; 53 properties, each value written from the chapters and held to the derivation (target/p4-system-14/a43b-3c/draft/draft_case.py, every assertion passing); control `refused-write-committed`, x28 at boundary 130 expected 5,
the wrong value 9; `second_method` `independent-exact-expectation`, producers `expected` and `reference`, common inputs `guest-source` and `dependency-manifest`, the first case declaring one; `adversarial` the seven refused-access properties.
**The prepared inputs:** `prepare_div_inputs.py --write` (guest 4,856 B; the configuration 8,748 B, `05746ed6…`, the first that differs from every other case's; baseline 34,930 B; control 33,688 B), `--verify` four `equal`. **The family's sixth re-derivation** (`decision_evidence-family-two-cases.md`, Addendum a43b-3d): 155
files, 96 MiB, `retention_limits()` 96,800,768 B measured, 138 files present; `evidence/README.md` compressed to hold the row (3,764 of 4,096 B). The input probe gains a `CsrSetCaseInputTests` class, so the case's pins are held through the overlay (34 → 49 tests; `actual-layout` still 6). Book: the prepared-inputs page. No retained case moved. Status unchanged: a case with no declarations binds nothing. Next: a43b-3e, the three declarations, committed before the capture.

<a id="acceptance-rows-a43b-3h-to-a43b-3d"></a>

## acceptance-rows-a43b-3h-to-a43b-3d

- [x] `.14` a43b-3h **ROOT CAUSE** — a satisfied measurement credits nothing by itself: at 94afcab2 `python3 -B scripts/requirement_status.py` read `46 planned, 2 implemented; 7 case(s), 2 credited` and `rv64gc-csr-set-v1: DIV-POLICY: satisfied … no qualification credit`.
- [x] `.14` a43b-3h **ADDRESSED** — `python3 -B scripts/requirement_status.py --profile rv64gc-lab-v0` → `45 planned, 3 implemented; 7 case(s), 3 credited, 0 declared, 3 of 3 credit record(s) current; 0 drift`; `python3 -B scripts/review_div_policy.py --every-retained` → `credited by CR-D-CSR-SET-1`; `grep -c 'implementation_status implemented' profiles/rv64gc-lab-v0/requirements.sexp` = 3; GS `2 of 4 state requirements implemented`.
- [x] `.14` a43b-3h **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `3 credit(s), 3 current, 0 lapsed`, the M and XLEN lines unchanged; `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`, `DIV-POLICY-PROBE: 48 tests / 0 failures`; G-TRACE green on its two records (`grep -c 'axis G-TRACE' profiles/rv64gc-lab-v0/gate.sexp` = 2).
- [x] `.14` a43b-3g **ROOT CAUSE** — the comparison leg judged one category's row for all: at a6f7d8fd `grep -c 'source_semantics' scripts/review_div_policy.py` = 1, the line reading the category into the report, never the leg; and `RETAINED_CAPTURES` held no row for the captured case (`python3 -B scripts/review_div_method.py --case rv64gc-csr-set-v1` → `unsupported`).
- [x] `.14` a43b-3g **ADDRESSED** — `python3 -B scripts/review_div_policy.py --every-retained` → `rv64gc-csr-set-v1: DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit`; `python3 -B scripts/probe_div_policy.py` → `DIV-POLICY-PROBE: 48 tests / 0 failures / 0 errors`, the twelve new seams each `1 tests / 1 failures / 0 errors` in both modes (target/p4-system-14/a43b-3g/seams.txt); `DIV-METHOD: 22 tests / 0 failures`.
- [x] `.14` a43b-3g **NO REGRESSION** — the M and XLEN lines unchanged, `credited by CR-GC-M-3` and `credited by CR-D-XLEN-2`; a `defined` case's measured text is pinned to the byte by `test_a_defined_requirements_comparison_reads_as_it_always_has`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `2 credit(s), 2 current, 0 lapsed`; nothing pinned moved (`grep -c 'review_div_policy' evidence/rv64gc-m-forms-v5/dependencies.sexp` = 0).
- [x] `.14` a43b-3f **ROOT CAUSE** — two facts were missing: the case had declarations and no observations (at 02835e0f `git ls-files evidence/rv64gc-csr-set-v1 | wc -l` = 8 of its 22 slots), and nothing retained what its configuration does (`git ls-files 'profiles/*/*.effect.*' | wc -l` = 0), so the policy's "observed effect" stood only on a43b-3a's scratch measurement.
- [x] `.14` a43b-3f **ADDRESSED** — `python3 -B scripts/retain_div_capture.py --case rv64gc-csr-set-v1 --declaration-commit 02835e0f…` `rc=0`, once, baseline and repeat AGREE, control DIVERGE at 130, complete, qualification false (target/p4-system-14/a43b-3f/rv64gc-csr-set-v1/capture.json); `cmp` baseline.trace against repeat.trace and control.trace silent; `python3 -B scripts/measure_config_effect.py --case rv64gc-csr-set-v1` printed `step 34 (csrrs x20, mcycle, x0): Sail {}, expectations {'x20': 34}`, `rc=0`; `python3 -B scripts/probe_config_effect.py` → `CONFIG-EFFECT: 10 tests / 0 failures / 0 errors`, nine omissions RED in both modes (effect/mutations.txt).
- [x] `.14` a43b-3f **NO REGRESSION** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `2 credit(s), 2 current, 0 lapsed`; no pinned input moved: `git diff --name-only 02835e0f HEAD` ∩ the 91 frozen paths = ∅ at the capture, and the tool, schema and records added after it are unpinned (`grep -c 'measure_config_effect' evidence/rv64gc-csr-set-v1/dependencies.sexp` = 0); `DIV-CAPTURE-INPUTS: 49 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DIV-METHOD: 22 tests / 0 failures`, `DIV-POLICY-PROBE: 33 tests / 0 failures`.
- [x] `.14` a43b-3e **ROOT CAUSE** — the case had no declarations: at c0ef6f51 `git ls-files evidence/rv64gc-csr-set-v1 | wc -l` = 5 of its 22 slots, and `python3 -B scripts/requirement_status.py` read `6 case(s), 2 credited, 0 declared`.
- [x] `.14` a43b-3e **ADDRESSED** — `python3 -B scripts/capture_div.py --declare --case rv64gc-csr-set-v1` `rc=0`, three files written exclusively (target/p4-system-14/a43b-3e/declare.json); `python3 -B scripts/retain_div_capture.py --preflight-only` → `ready` (preflight.json); `python3 -B scripts/requirement_status.py` → `7 case(s), 2 credited, 1 declared … 0 drift`; `MATCHED-GPR-CASE: 8 tests / 0 failures`, `DIV-CAPTURE-INPUTS: 49 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`.
- [x] `.14` a43b-3e **NO REGRESSION** — `grep -c 'scripts/prepare_div_inputs.py' evidence/rv64gc-csr-set-v1/dependencies.sexp` = 0 and the manifest's children differ from xlen-v2's in two paths only; `DIV-METHOD: 22 tests / 0 failures`, `DIV-POLICY-PROBE: 33 tests / 0 failures`, `DIV-COMMAND: 20 tests / 0 failures` (`grep -c 'timeout=15' scripts/probe_div_command.py` = 0); v5 and xlen-v2 still credited (`2 of 2 credit record(s) current`); the staged prechecks and the commit gate (chain log).
- [x] `.14` a43b-3d **ROOT CAUSE** — the old program witnessed 28 of 33 and could not carry the case: `git show 76e74a52:profiles/rv64gc-lab-v0/guests/csr-set.s | grep -c 'mcycle\|minstret\|cycle\|time\|instret'` = 0, `grep -c 'boundary:'` = 0, no `sret`, and no case directory (`ls evidence | wc -l` = 7 with the index).
- [x] `.14` a43b-3d **ADDRESSED** — `python3 -B scripts/derive_rv64gc_expectations.py --parcels --steps 157 …/csr-set.s` → `wrote csr-set.expected.sexp (157 steps)`, `check_sexp_schema: ok`; `cargo test -p semulith-verify every_guest_matches_its_expectations` → `test result: ok. 1 passed`; the pinned Sail under the overlay `AGREE 157 declared steps` (target/p4-system-14/a43b-3c/draft); `python3 -B scripts/prepare_div_inputs.py --verify --case rv64gc-csr-set-v1` four `equal`; `DIV-CAPTURE-INPUTS: 49 tests / 0 failures / 0 errors` both modes.
- [x] `.14` a43b-3d **NO REGRESSION** — `bash scripts/check_guest_gen.sh` `rc=0` → `GUEST-GEN: ok` (target/p4-system-14/a43b-3d/guest-gen.log); `python3 -B scripts/requirement_status.py` → `46 planned, 2 implemented … 2 of 2 credit record(s) current; 0 drift`; v5 and xlen-v2 still `--verify` `equal`; `MATCHED-GPR-PROPERTY: 35 tests / 0 failures`, `MATCHED-GPR-CASE: 8 tests / 0 failures`; `RECORD-SCHEMA: ok`; the staged prechecks and the commit gate (chain log).

