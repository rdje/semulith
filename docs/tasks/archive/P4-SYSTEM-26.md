# P4-SYSTEM ordinary history — part 26

Ordinary, directly readable task history: the complete records of the closed `.14` units
a43b-2d, a43b-2e, a43b-3a, a43b-3b and a43b-3c, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0339` on top of commit `a6f7d8fdfa1e863e21171bf97d2766b6ba0d2310`
(7 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a43a-3 … a43b-2c and their rows are in part 25,
the earlier ones in parts 13–24. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a43b-3g, SEMULITH-P4-0339.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a43b-3c | 3814 | `55324444f0295785c11d4bed1f4c444e2eb061af52c138ec61fdf64fe65714e1` |
| record a43b-3b | 2058 | `67e16215bd70361e2879095a2a4682cc08b6759b9305afbbcab1db76b37a590f` |
| record a43b-3a | 5540 | `00ff894c81c5a8993cca782a273d7a60a50fadfa7a142b25c6aa214b0fe12551` |
| record a43b-2e | 2697 | `272640614a5bb78ec9087b76703620dde08f160069141fddf80cdac67a1dc7ee` |
| record a43b-2d | 2332 | `3e1e236a32d019be4e3c57b9055c6820ff965cd81b633c5fe60bc2ebfa69a77d` |
| acceptance rows a43b-2d–a43b-2e | 2510 | `d8d682f3682d96253c5a6b0cc5f66b7ecea66a3a7b04c05f567f212f4578d558` |
| acceptance rows a43b-3c–a43b-2e | 4544 | `ef929cf2671565248f2f69d31af4b2925d07fb56101496526fcfbdb4c2250783` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-26.md)   # a span, by its line range
```

<a id="a43b-3c"></a>

### .14 a43b-3c / SEMULITH-P4-0335: a case's reference configuration, as data — the overlay, its controls and the census tool (completed)

a43b-3a's D1, and its census made reproducible. D6 put the overlay, the program, the case and the family's re-derivation in one slice;
split on the way in, because the overlay moves a tool and a schema while the case moves six probes and the evidence family: this slice is the
mechanism, and the next CSR-SET slice is the program and the case. `schema/overlay.sexp` is a closed vocabulary (`extension`,
`clint`, `instructions_per_tick`, `case_id`, `reason`), and `profiles/rv64gc-lab-v0/reference/rv64gc-csr-set-v1.overlay.sexp` is the first
overlay. `prepare_div_inputs.reference_config(root, case_id)` returns the mapped profile override, under the case's overlay if one
exists; `apply_overlay` makes every change one that changes something, so it refuses an extension already on, a CLINT or a tick rate
the override already declares, a non-positive base, size or rate, an overlapping region, and an overlay naming another case. The device region takes
the pinned binary's published MMIO attributes (`--print-default-config`) and goes where its base puts it, because the binary refuses regions
out of order (measured at a43b-3a). Rendered, the overlay's configuration validates (`sail_riscv_sim --validate-config` `rc=0`) and differs from
a43b-3a's scratch variant only in the two attributes that variant had copied from RAM. **No lapse, and no case moves:** `prepare_div_inputs.py` and the
override are pinned by neither current manifest (a43b-3a), `--verify` still reads `equal` for v5 and xlen-v2, and both credits stay current.
`DOSSIER-SCHEMA` maps `.overlay.sexp` to its schema, and the token-facet probe's schema census moves 27 → 28 (the schema has no anchored pattern, so the facets stay 127); the chain's focused stage refused once on exactly that count. Controls: `scripts/probe_reference_overlay.py`, 14 tests and nine guard omissions each fired RED in
both modes (target/p4-system-14/a43b-3c/probe.txt: `clint-positive` 2, `region-overlap` 3, `region-order` 2, the others 1), now arms of
PROFILE-CONSISTENCY's self-test. **The census is now a tool:** `scripts/census_reference_config.py --case <id>` (live, not CI) re-derives a43b-3a's
table from the tracked route, identically: 171 guests, 151 agreeing under both, the same seven movers (census.txt). Book: the references page. Next:
XTASK.13 b3 (the 5:1 turn), then a43b-3d, the program, the case and the family's sixth re-derivation.

**Two defects found while drafting the program, both logged here and scheduled (§15).** (1) *37 citations in 16 guests name sections their page does not
have* (`RVP-INSNS §3.3.2` 22, `RVP-SSTC §2.1` 8, `RVP-SUPERVISOR §1.1.x` 6, `RVP-SSTC §1` 1; census of 1,577 citations against the pinned pages' headings,
target/p4-system-14/a43b-3c/citation-census.txt), and others resolve but to the wrong section (`csr-set.s` cited `RVP-MACHINE §2.1.5` for `mtvec`, which is
§2.1.1.7). `CITATION-QUOTES` checks quoted phrases and these carry no quote. Impact: a reader sent to the wrong place, no verdict; neither pinned guest
carries one (`grep -c` 0 for `m-forms.s` and `xlen-forms.s`). Owner: `.14` a43b-c1, after the CSR-SET case; the new `csr-set.s` is written correct from the
start. (2) *The deriver's docstring promises `{new}` interpolation that a guest's directive does not get:* retained expectations read literally "…, {new} — a
64-bit register". Prose only; the value is in the step's write. The deriver is pinned by every capture, so the fix waits for the next window that moves it
anyway (a pinned producer is not moved for prose, `decision_producer-debt-paid-before-the-next-case.md`); until then new sources do not use the key.
Owner: `.14` a43b-c2.

<a id="a43b-3b"></a>

### .14 a43b-3b / SEMULITH-P4-0334: CSR-SET's normative statements retained — RVP-CSR §1.1.1, the first from the privileged volume (completed)

The first slice of a43b-3a's order. REQ-D-CSR-SET names six sources, and a case's excerpts name one publication
(`check_retained_input`): RVP-CSR is the one stating what the case's refused accesses rest on. Five exact statements of §1.1.1 —
`norm:Zicsr_higher_priv`, `norm:Zicsr_rw`, `norm:Zicsr_access`, `norm:Zicsr_illegal_mode`, `norm:Zicsr_illegal_acc` — are retained in
`profiles/rv64gc-lab-v0/retained/rvp-csr-statements.html` (2,750 B, `0f2d75c5…`, `RVP-CSR-STATEMENTS`), naming the page's digest once. Licence
evidence: `priv/priv-preface.html` (54,715 B, `6e4ba2ab…`), the privileged volume's own statement in the words the unprivileged
preface uses; the SRC-01 record is `materials/RVP_CSR_RETENTION.md`, and the catalogue names it. **A table, not a fourth module:** the M and RV64I
excerpts each have their own script, and ZICNTR and SSTC would make it five, so `scripts/retain_statements.py` holds one row per excerpt
through one bounded transformation; a row is a page and its pin, the licence evidence and its pin, the statements and the retained pin. The
earlier excerpts' scripts stay as they are: `retain_div_statement.py` is pinned by every capture. The spans' markup, measured before review, is
`<code>` five times and one same-publication cross-reference; the allowlist's fragment admits the `:` that
`hypervisor.html#sec:hcauses` carries, and refuses any other tag or attribute. Controls: `scripts/probe_statement_retention.py`, 19
cache-free tests over a synthetic row and nine guard omissions, each fired RED in both modes (`span-markup` 7, `retained-pin` 2, the
others 1, target/p4-system-14/a43b-3b/probe.txt), now arms of PROFILE-CONSISTENCY's self-test (20 more arms per mode), whose real run
verifies every row offline. `--emit` is reproducible (`cmp` equal). No case, capture or credit yet: next a43b-3c, the overlay, the
program, the case and the family's re-derivation.

<a id="a43b-3a"></a>

### .14 a43b-3a / SEMULITH-P4-0333: the CSR-SET case designed — the reference configuration the case's own, all 33 CSRs witnessed, the category row judged (completed)

Documentation only, as a43b-2a was: the design before the first slice (`decision_reference-config-per-case.md`). The plan was to
declare CSR-SET as a43b-1 left it, 28 of 33 matched and the five counters named out, and credit `implemented` — on a
requirement whose statement is "the committed minimum of 33". Before writing that credit the limit itself was measured,
and it does not hold as stated. **M1: the pinned binary implements Zicntr; our override turns it off.** With `Zicntr`
supported Sail refuses by name ("Zicntr is enabled but there is no source of time"); with a CLINT but no region, "The CLINT
… is not in a defined memory region"; with a device region at the CLINT's default base, `--validate-config` `rc=0`, the same
binary (`16de42a8…`, the identity both retained cases name). No re-pin (target/p4-system-14/a43b-3a/config-validation.txt).
**M2: the values agree too.** At the default `instructions_per_tick` 2, `mcycle` reads 2 where the laboratory reads 4 — Sail counts
ticks; at 1, all five counters agree step for step (`AGREE 20 declared steps`, live-verdicts.txt). So the plan's "fixed-zero
cycle" and its declared value difference were misreadings (`mm-counters` step 0 writes nothing because x5 already holds 0);
the laboratory's one tick per step boundary is a rate the reference can select. **M3: the census.** All 171 guests under both
configurations (census-table.txt): 151 agree under both; `mm-counters` REFUSED → AGREE (52 steps), `mm-csr-ro-counters` DIVERGE →
AGREE (49), `c-irq` DIVERGE → AGREE (19); `csr-set` and `w-sw` AGREE → DIVERGE at `mip` — the reference's CLINT resets
`mtimecmp` to 0, so `MTIP` reads set — and `w-deleg`, `w-timer` move between DIVERGE and REFUSED. Better for the counters, worse
for `mip` readers: not a profile-wide change. **M4: it costs no lapse.** `grep -c` over both current manifests:
`scripts/prepare_div_inputs.py` 0, the override 0, `scripts/dossier_sexp.py` 1 (before/pins.txt) — the closed mapping
`override_to_doc` (no `clint.base`, no `instructions_per_tick`) is pinned, the tool that renders each case's
`reference-config.json` is not.
**D1 — the configuration is the case's data.** `profiles/rv64gc-lab-v0/reference/<case-id>.overlay.sexp`, one small schema, read by
`prepare_div_inputs.py` and applied over the mapped profile override: Zicntr on, a CLINT in its own device region,
`instructions_per_tick` 1. The profile override does not move, so v5, xlen-v2 and every live corpus run keep their
configuration; the case's prepared pin holds the result. **D2 — the program, rewritten before any capture.** `csr-set.s`: 136
instructions, 157 steps (M 137, S 13, U 7), `AGREE 157 declared steps` as a draft (target/p4-system-14/a43b-3/probe/csr-draft.s).
All 33 CSRs: 32 read into a sentinel; `mip` read with `rd` = x0 and a marker, because of M3, its value witnessed through
the `sip` alias. Added: the `sip`/`mip` alias the plan named and a43b-1 dropped; `csrrs` with `rs1` ≠ x0 refused on `mhartid`
beside `csrrw`; every refused access read back (`rd` kept, a GPR change the vocabulary can see); M writes `mscratch` 5 and
`sscratch` 3, S's refused write to `mscratch` and U's to `sscratch` are read by the handler in M and still hold them; U enters
through `sret`, reads `fflags` legally — so the feature rule's "legal/refused modes" covers M, S and U. **D3 — the case.** `source_id`
RVP-CSR, locator 1.1 (a case's excerpts name one publication, `check_retained_input`), retained
`norm:Zicsr_higher_priv`, `_rw`, `_access`, `_illegal_mode`, `_illegal_acc`; `second_method` `independent-exact-expectation`, producers
`expected` and `reference`, common inputs `guest-source` and `dependency-manifest`; `adversarial` the refused-write
properties; control `refused-write-committed`, x28 at the handler 9 where the case expects 5; `(boundary: …)` on the seven
privilege and read-only edges, each a declared property. **D4 — the category row, now judged.** `review_div_policy.py:251` reads
the category and only reports it: `matched-reference-comparison` measures `defined`'s row for every case. Measured gap, so
the leg gains a category branch: `implementation-defined` needs the selection recorded in the catalogue and "a behavior-changing
control", read offline from a retained alternative trace — this guest under the profile override, first differing at a
declared property's step (the draft: step 34, `mcycle`, `Sail {}`, expected 34, an illegal-instruction trap). Any category
without a branch reads pending. Ten legs still; M and XLEN do not move; the review is pinned by no manifest. **D5 — the credit.**
`implemented` rests on all 33 witnessed; its limitations name `mip`'s value not compared and per-CSR field semantics
staying with `P4-SYSTEM.2`. **D6 — the order.** a43b-3b the retained statements; a43b-3c the overlay, the program, the case and the
family's re-derivation (a seventh case); XTASK.13 b3 at the 5:1 turn; a43b-3d the declarations; a43b-3e the capture once and the
alternative trace; a43b-3f the reviews; a43b-3g the credit. Then ZICNTR and SSTC on the same route: this also removes what the
ZICNTR program was waiting for (Open Questions; raised to the director, who may overrule). The scratch instruments become a tracked
census tool at a43b-3c, and the census is re-derived there. Books: the references page. Next: a43b-3b.

<a id="a43b-2e"></a>

### .14 a43b-2e / SEMULITH-P4-0332: the reviews read v5 and xlen-v2 and both are re-credited — the window closed (completed)

The close of the planned lapse that opens CSR-SET, as a44-5 closed ruling B's. `review_div_method.py`'s
`RETAINED_CAPTURES`: the default row v4 → v5 (declared 7b1a8f44, captured 2988d6a2, measured 16,942 B `1530832d…`), the XLEN
row xlen-v1 → xlen-v2 (the same commits, 14,979 B `3e536d08…`); `review_div_policy.CASE_ID` v5. Measured: both method
reviews `satisfied` over 88 authenticated files (1,103,074 and 1,097,514 B; snapshots 40,438 and 35,100 B); `--every-retained`
`rv64gc-m-forms-v5: DIV-POLICY: satisfied — 10 of 10 legs satisfied` and the same for xlen-v2. The crediting act, on the
rulings of `decision_req-gc-m-credited-implemented.md` and `decision_req-d-xlen-credited-implemented.md`:
`profiles/rv64gc-lab-v0/credits.sexp` re-created with `CR-GC-M-3` (v5) and `CR-D-XLEN-2` (xlen-v2) — each pinning its
measured record, receipt and the policy; authority `review`; ten legs; three limitations each. `CR-D-XLEN-2` carries two
fewer than `CR-D-XLEN-1`: its receipt names `REQ-D-XLEN` and its record carries its own control, so the limitations that
named the producer's M text are gone — what the window was for. `REQ-GC-M` and `REQ-D-XLEN` `implemented`:
`REQUIREMENT-STATUS: … 46 planned, 2 implemented; 6 case(s), 2 credited, 0 declared, 2 of 2 credit record(s) current; 0
drift`; `CREDIT-RECORDS: … 2 credit(s), 2 current, 0 lapsed`; the policy review `credited by CR-GC-M-3` /
`CR-D-XLEN-2`. The dossier holds both measured records form for form (each the measured file's experiment line), both
qualifying (`dossier_qualification` → `[]`); `gate.sexp` their `G-TRACE` rows, the G-TRACE open entry closed, G-STATE and
G-OBLIGATIONS restated; GS `Open axes (3 of 10)`, G-TRACE green, G-STATE `1 of 4`. Re-stated: the method probe's
real-tree rows and counts, the policy probe's XLEN case, the status probe (46 / 2), the dossier probe (now requiring v5
and xlen-v2 to qualify and v4, xlen-v1, v3 not); the property probe's `derived-status` pin 2 → 37 (`35 tests / 37
failures` measured). The window ran a43b-2a … a43b-2e on 2026-11-02 (`decision_producer-debt-paid-before-the-next-case.md`,
Closed). Containment, same unit: the closed records a43a-3 … a43b-2c and their 12 rows moved verbatim into
[`archive/P4-SYSTEM-25.md`](archive/P4-SYSTEM-25.md) (121,260 → 93,870 B before this record; 186 of 186 removed lines
present). Books: the policy, status, method and division pages, the fragments; `evidence/README.md`. Next: a43b-3, the
CSR-SET case declared on the clean producers, with its second method and adversarial case.

<a id="a43b-2d"></a>

### .14 a43b-2d / SEMULITH-P4-0331: v5 and xlen-v2 captured, exactly once each — traces byte-identical to their predecessors' (completed)

`target/p4-system-14/a43b-2d/capture-when-quiet.sh <case>` ran each capture once, never retried, only after three
consecutive quiet minutes (no sibling verification, 1-minute load below 6: 4.68 and 4.76, `<case>/wait.log`) and three
guards: a clean tracked tree; no path frozen for the captures changed between the declaration commit `7b1a8f44` and HEAD
(`f47ad4a7`, XTASK.13 b2 having landed between: `git diff --name-only` ∩ the 100 frozen paths = ∅); the committed
declarations equal to a fresh `capture_div.py --declare`; then `retain_div_capture.py --preflight-only` `ready`. Each
`retain_div_capture.py --case <id> --declaration-commit 7b1a8f44…` ran 1.3 s: three zero-exit processes, baseline and
repeat AGREE, the control DIVERGE at its declared step (12 for M, x15; 24 for XLEN, x31), `complete_canonical_capture`
true, qualification false; 14 files retained per case — v5's measured record 16,942 B (`1530832d…`), receipt 7,021 B;
xlen-v2's 14,979 B (`3e536d08…`), 7,064 B. **The window changed only what was declared:** all six traces and all six
stdout streams are byte-identical to v4's and xlen-v1's (`cmp`, cmp.txt); each stderr stream equals its predecessor's
with the one case directory it prints substituted; with the case id substituted, each measured record differs from its
predecessor's only in seven digests — the dependency manifest, the three stderr streams and the three receipts that
record them, each matched to its file — and, for XLEN, in the control's id and prose (measured-vs-predecessor.txt).
The family holds all 133 files (727,984 B); `REQUIREMENT-STATUS: … 48 planned; 6 case(s), 0 credited, 0 declared` — v5
and xlen-v2 `pending` (receipts, no credit). Re-stated: the input probe's member count (105 → 133), the status probe's
rows. Refined from a43b-2a's D4: the retained-capture rows move with the re-credits at a43b-2e, not here — a row names
its capture commit, which is this commit (as a44-5 and a43a-2f followed their captures). Book: the division page (the
re-capture's proof), the status and prepared-inputs pages; `evidence/README.md` (3,914 B). Next: a43b-2e, the reviews
read v5 and xlen-v2 and both are re-credited.

<a id="acceptance-rows-a43b-2d-to-a43b-2e"></a>

## acceptance-rows-a43b-2d-to-a43b-2e

- [x] `.14` a43b-2d **ROOT CAUSE** — the two re-captures were declared and not captured: `git ls-tree --name-only f47ad4a7 evidence/rv64gc-m-forms-v5/ | wc -l` = 8 of the case's 22 slots, and 8 for xlen-v2 (the case file, four prepared inputs, three declarations); `retain_div_capture.py --preflight-only` → `ready` for both; `REQUIREMENT-STATUS: … 6 case(s), 0 credited, 2 declared` (a43b-2c).
- [x] `.14` a43b-2d **ADDRESSED** — target/p4-system-14/a43b-2d/<case>/wait.log → `capture rc=0` once each; `verification.json`: baseline/repeat `AGREE`, control `DIVERGE` at step 12 (v5) and 24 (xlen-v2), `complete_canonical_capture` true, qualification false; cmp.txt: 6 of 6 traces and 6 of 6 stdout `identical`, the stderr equal but for the case directory (`True` ×6); measured-vs-predecessor.txt: 7 differing digests each, all named; `python3 -B scripts/requirement_status.py` → `6 case(s), 0 credited, 0 declared … 0 drift`; `DIV-CAPTURE-INPUTS: 34 tests / 0 failures` both modes.
- [x] `.14` a43b-2d **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1224 pass / 0 fail` (target/p4-system-14/a43b-2d/selftest.log), traced: `ls target/p4-system-14/a43b-2d/eperm | wc -l` = 0; the whole check `rc=0` → `PROFILE-CONSISTENCY: ok (5 profile dossier(s) internally consistent)`; `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures` both modes; `DIV-METHOD: 22 tests / 0 failures`, `DIV-POLICY-PROBE: 33 tests / 0 failures`, `MATCHED-GPR-CASE: 8 tests / 0 failures`; the staged prechecks and the commit gate (chain log).
- [x] `.14` a43b-2e **ROOT CAUSE** — the re-captures were retained but unreviewed and uncredited: at 2988d6a2 `REQUIREMENT-STATUS: … 48 planned; 6 case(s), 0 credited, 0 declared` and `review_div_policy.py --every-retained` measured v4 and xlen-v1 `invalidated` (target/p4-system-14/a43b-2e/before/policy.txt); `grep -c 'rv64gc-m-forms-v5' scripts/review_div_method.py` = 0.
- [x] `.14` a43b-2e **ADDRESSED** — `python3 -B scripts/review_div_method.py --case rv64gc-m-forms-v5` `rc=0` → `satisfied`, 88 files, 1103074 B (xlen-v2 1097514 B); `--every-retained` → both `10 of 10 legs satisfied; credited by CR-GC-M-3` / `CR-D-XLEN-2`; `CREDIT-RECORDS: rv64gc-lab-v0: 2 credit(s), 2 current, 0 lapsed`; `REQUIREMENT-STATUS: … 46 planned, 2 implemented; 6 case(s), 2 credited … 0 drift`; both dossier records `dossier_qualification` → `[]`; GS `Open axes (3 of 10)`, G-TRACE green; move.log `records 4, row spans 1 (12 rows)`, 186 of 186 removed lines in part 25.

<a id="acceptance-rows-a43b-3c-to-a43b-2e"></a>

## acceptance-rows-a43b-3c-to-a43b-2e

- [x] `.14` a43b-3c **ROOT CAUSE** — a case could not carry its own configuration: `prepare_div_inputs.curate` read the one `OVERRIDE` for every case (`grep -n 'OVERRIDE' scripts/prepare_div_inputs.py`, target/p4-system-14/a43b-3c/before/verify.txt), and the closed `dossier_sexp.override_to_doc` has no `clint.base` or `instructions_per_tick` and is pinned (`grep -c 'scripts/dossier_sexp.py'` = 1 on both manifests); the a43b-3a census lived in a scratch script.
- [x] `.14` a43b-3c **ADDRESSED** — `python3 -B scripts/probe_reference_overlay.py` → `REFERENCE-OVERLAY: 14 tests / 0 failures / 0 errors` both modes, each of the nine omissions RED (probe.txt); `sail_riscv_sim --validate-config` `rc=0` on the rendered configuration; `python3 -B scripts/census_reference_config.py --case rv64gc-csr-set-v1` → `171 guests`, `151  profile AGREE -> case AGREE`, a43b-3a's table re-derived (census.txt).
- [x] `.14` a43b-3c **NO REGRESSION** — `python3 -B scripts/prepare_div_inputs.py --verify` `rc=0` for v5 and xlen-v2, all four inputs `equal`; `python3 -B scripts/requirement_status.py` → `46 planned, 2 implemented … 2 of 2 credit record(s) current; 0 drift`; `DIV-CAPTURE-INPUTS: 34 tests / 0 failures`; `bash scripts/check_dossier_schema.sh` ok; `RECORD-SCHEMA --self-test: 81 pass / 0 fail`; `cargo clippy -p xtask --all-targets -- -D warnings` `rc=0`; the staged prechecks and the commit gate (chain log).
- [x] `.14` a43b-3b **ROOT CAUSE** — CSR-SET had no retained normative input, and its publication had no retention route: at 5c58ce7b `git ls-tree --name-only HEAD profiles/rv64gc-lab-v0/retained/ | wc -l` = 4 (three excerpts and the Sail identity, none from the privileged volume), `git grep -c 'priv-preface' HEAD -- 'scripts/retain_*.py' | wc -l` = 0, and `check_retained_input` binds a case's excerpts to one page.
- [x] `.14` a43b-3b **ADDRESSED** — `python3 -B scripts/retain_statements.py --verify` `rc=0` → `RVP-CSR-STATEMENTS` `matched` (2750 B, `0f2d75c5…`); `--emit` `cmp`-equal to the tracked excerpt; `STATEMENT-RETENTION: 19 tests / 0 failures / 0 errors` both modes, and each of the nine omissions `1 failures` (`span-markup` 7, `retained-pin` 2), target/p4-system-14/a43b-3b/probe.txt.
- [x] `.14` a43b-3b **NO REGRESSION** — no pinned path touched: `git diff --cached --name-only` against both current `dependencies.sexp`: `grep -c` 0; `python3 -B scripts/requirement_status.py` unchanged, `46 planned, 2 implemented … 0 drift`; `cargo test -p xtask` and `cargo clippy -p xtask --all-targets -- -D warnings` `rc=0`; the staged prechecks and the commit gate (chain log).
- [x] `.14` a43b-3a **ROOT CAUSE** — the design rested on a limit nobody had measured against the binary: `grep -n 'no Zicntr' docs/decisions/decision_state-capture-plan.md` and `sail_riscv_sim --validate-config` → `rc=0` with Zicntr and a CLINT device region (target/p4-system-14/a43b-3a/config-validation.txt); `review_div_policy.py:251` reads `category` and only reports it (`grep -n 'category' scripts/review_div_policy.py` → lines 251, 393).
- [x] `.14` a43b-3a **ADDRESSED** — the design D1–D6 recorded here and in `decision_reference-config-per-case.md`; target/p4-system-14/a43b-3a/live-verdicts.txt: `AGREE 20 declared steps` (counters, one tick per instruction), `AGREE 157 declared steps` (the draft, all 33 CSRs), `DIVERGE step 34 (csrrs x20, mcycle, x0)` under the profile override; census-table.txt: 171 guests, 151 agree under both; before/pins.txt: `grep -c 'scripts/prepare_div_inputs.py' evidence/rv64gc-xlen-forms-v2/dependencies.sexp` = 0, `grep -c 'scripts/dossier_sexp.py'` = 1 on both manifests.
- [x] `.14` a43b-3a **NO REGRESSION** — documentation only (`git diff --cached --name-only | grep -cvE '\.md$'` = 0); `python3 -B scripts/requirement_status.py` unchanged, `46 planned, 2 implemented`; the focused stage and the commit gate (target/p4-system-14/a43b-3a chain log).
- [x] `.14` a43b-2e **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1224 pass / 0 fail` (target/p4-system-14/a43b-2e/selftest.log), traced: `ls target/p4-system-14/a43b-2e/eperm | wc -l` = 0; the whole check `rc=0`; `MATCHED-GPR-PROPERTY: 35 tests / 37 failures` under `derived-status` (re-pinned); `DIV-METHOD: 22 tests / 0 failures`, `DIV-POLICY-PROBE: 33 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`; `RECORD-SCHEMA: ok (26 record file(s) …)`, `GATE-REPORT: ok`; the staged prechecks and the commit gate (chain log).

