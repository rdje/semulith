# P4-SYSTEM ordinary history — part 24

Ordinary, directly readable task history: the complete records of the closed `.14` units
a44-2b, a44-2c, a44-3, a44-4, a44-5 and a43a-2a … a43a-2f, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0328` on top of commit `b7420b1b518a662708b5817551e1e39210672349`
(12 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a43a-1 … a44-2a and the rows a43b-1–a44-2a are in part 23,
the earlier ones in parts 13–22. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a43b-2a, SEMULITH-P4-0328.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a43a-2f | 2633 | `97db4cd83ff0c81b5433ab2c59395b18985875a9a343b605384575fda56d1ca1` |
| record a43a-2e | 1576 | `b79ab8fc16a6778555ff2035c613f6e10b348f89a6813eae970454e9f36297a6` |
| record a43a-2d | 1937 | `60119abb63f4627d51a641ee93617a8b81f57d9d23d19da684a32d36b8c1c9ee` |
| record a43a-2c | 1038 | `a55d31ce4fa5330b3a1a0b7c14c3793ee26935ccd7379df8619e65b00bcc757e` |
| record a43a-2b | 2450 | `a6abaae2992d2282bf1f1f4c83a463b2aac7249b831414c87e73cdeb475442ef` |
| record a43a-2a | 2471 | `efd38788e97180b380941707afd48ce4292d341c0f01f07d16f6b38bdee0f5b3` |
| record a44-5 | 1916 | `11de9ac89318b317a6e1f27a153c4f5a89bfce65043392ca60cde2f59614402b` |
| record a44-4 | 1312 | `3b2130934d88c1751833de7a3d0f48308f2a810780397f66b5856101d7d7b4c4` |
| record a44-3 | 2063 | `2125701450ae4b6d01afa813ef521f77400ed92413809b808b0662058b468d4f` |
| record a44-2c | 2407 | `04811dacdb90cff69e9272b6e7830bfa0716795946ad836c063c628e07db2b7c` |
| record a44-2b | 4131 | `af3c31e8ccff484d6f1fd4ec93a70f7c79f9b2134e119ecc67d3d47b95a6c15d` |
| acceptance rows a44-2b–a43a-2f | 13252 | `3cecce7176c8d32c4e5b5c98192cdf40066bd8c78b2f8c829b37822fafa82c09` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-24.md)   # a span, by its line range
```

<a id="a43a-2f"></a>

### .14 a43a-2f / SEMULITH-P4-0326: the retained reviews read every reviewed capture — the XLEN case measured ten of ten (completed)

The finite method review (`scripts/review_div_method.py`) held one retained case; the policy review refused any other
(`unsupported: no reviewed capture`), and measured on the XLEN case's own bytes through `--method-json` it read 7 of 10:
`boundary-fixtures` 0 rows (it knew M's `Table` citations only), `feature-rules` "OB-XLEN: feature disposition
undeclared", `form-coverage` "0 of 0 forms" — a `state` requirement names no instruction (before/,
policy-xlen-before.json). Both reviews are consumers no manifest pins (a42av), so generalizing them lapses nothing.
The method review now holds `RETAINED_CAPTURES`, one row per reviewed capture: v4's named pins kept (the probe's
synthetic copy re-pins them) and the XLEN row — declared 5c2cde93, captured e32cc645, measured 14,958 B `d39825b0…`;
a case without a row (v2, v3) is `unsupported` and reads nothing. The policy review accepts those cases and
`--every-retained` measures each, one line per case, the worst exit code; `PROFILE-CONSISTENCY`'s real run calls it.
A directed boundary row is a `Table` citation or a `(boundary: …)` tag (the XLEN guest's ten; absent from every M
expectation, so M's twelve rows do not move); a `state` requirement naming no form satisfies `form-coverage`
vacuously and says so ("coverage is vacuous, its 17 predeclared witnesses stand for it"); `OB-XLEN`'s feature
disposition is declared: none applies — the access fault at 2^40 and the handler's `CSRRS` of `mtval` observe the
address and claim no trap, CSR or protection behaviour, which REQ-D-FAULT-PRIORITY, REQ-D-CSR-SET and
REQ-GC-CSR-ACCESS own (`decision_reviews-read-every-retained-case.md`). Measured: `rv64gc-m-forms-v4: DIV-POLICY:
satisfied — 10 of 10 legs satisfied; credited by CR-GC-M-2` (its table identical to the single-case run) and
`rv64gc-xlen-forms-v1: DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit`; the XLEN method
`satisfied` over 88 authenticated files (1,092,798 B), exact allowance 1,155,615. The probes hold the rows: the method
probe's real-tree arm runs each row against its own authenticated counts and requires v3 `unsupported`; the policy
probe gains a `(boundary: …)` test and a state-requirement test, each with its seam (`boundary-tag`,
`state-vacuous`), and its real-tree arm reads one `--every-retained` run and re-measures both tables with the module
under test. The book's method and policy pages, stale since v3, now describe both cases. Next: the credit, `CR-D-XLEN-1`.

<a id="a43a-2e"></a>

### .14 a43a-2e / SEMULITH-P4-0325: the XLEN case captured, exactly once — the first non-M capture (completed)

`python3 -B scripts/retain_div_capture.py --case rv64gc-xlen-forms-v1 --declaration-commit 5c2cde93d5ba0940df03513d3e7cb788b364340e`,
one invocation after a `ready` preflight, run by target/p4-system-14/a43a-2e/capture-when-quiet.sh only once no process of a
sibling repository's verification had run for three consecutive minutes and the 1-minute load was below 6 (09:24:32Z,
load 5.71; wait.log): a capture is never retried, so it was not exposed to the foreign load the gate's EPERM struck under.
Three zero-exit processes, baseline and repeat AGREE, the control DIVERGE exactly as declared — boundary 24, x31 observed
2^40 where the control expectation holds 0 — complete, qualification false, 1.3 s. Retained: the twelve observations,
`measured-experiment.sexp` (14,958 B, `d39825b0b4d7ccba…`) and `verification.json` (7,055 B); the case holds 22 of 22,
the family all 89. Status: `4 case(s), 1 credited, 0 declared` (XLEN pending, uncredited until its reviews and credit).
Found in the retained receipt: its first limitation reads "…, not all M or CPU acceptance" — `retain_div_capture.py`
(unpinned) appended an M-specific phrase to every case's coverage; future receipts name the case's own requirement
(`not all REQ-D-XLEN or CPU acceptance`); this receipt is retained as written (retained bytes are never rewritten) and the
phrase claims nothing. Next: XTASK.13 slice b (the 5:1 turn), then a43a-2f, the reviews over several retained cases.

<a id="a43a-2d"></a>

### .14 a43a-2d / SEMULITH-P4-0324: the XLEN case re-declared before its capture — its evidence fit for the policy's legs (completed)

Caught before the capture, which was queued and stopped unrun (target/p4-system-14/a43a-2d, 14 output names still absent):
the policy review's `source-located-expectations` leg requires the control's witness step to cite the requirement's own
source and locator, and its `boundary-fixtures` leg requires the case's directed boundary fixtures to be marked and
predeclared — read from the expectation file, which a capture fixes for good. No XLEN step cited RVI-RV64I §3.1.1 (the
control's step 24 cited RVP-MACHINE §2.1.7 alone), and nothing marked XLEN's boundaries (the review knows M's `Table` rows
only). The guest's comments now cite §3.1.1 where the register-width and address-space claims rest on it (steps 1, 5, 8,
9, 21 and 24, the control's step reading `RVI-RV64I §3.1.1; RVP-MACHINE §2.1.7`) and tag ten boundary witnesses
`(boundary: …)` — bit 63, bit 32, a shift amount above 31, 2^63 - 1, the wrap at 2^63, the carry out of bit 63, bit 31
extended to 63, the word's sign bit, `rs2[4:0]` and an address above 2^32 — each a predeclared property's step; the marker
occurs in no other guest or retained expectation (`grep -c "(boundary"` = 0 for m-forms and v4), so M's measurement cannot
move when the review learns it (a43a-2f). The case was re-declared in place under the a42av precedent (declared, never
captured, nothing observed): its eight files removed and recreated by the same tools (kept in target/…/old-v1);
measured, token for token, only digests and sizes changed — the case 6, the planned record 4, the manifest 1, the
authority record 5; the image and the reference configuration are byte-identical (comments do not reach the ELF); the
producer review `pending` with 67 children, the capture preflight `ready`. Next: a43a-2e, the capture, on a quiet host.

<a id="a43a-2c"></a>

### .14 a43a-2c / SEMULITH-P4-0323: the XLEN case's three declarations, committed before its capture (completed)

`python3 -B scripts/capture_div.py --declare --case rv64gc-xlen-forms-v1` emitted the planned experiment (14,931 B), the
dependency manifest (15,173 B, **67** children — the case's declaration, its schema and its reader, and the retained RV64I
statements as the normative child in place of the M excerpt) and the authority record (17,755 B), written exclusively from
the command's `files` map; this commit is the declaration commit the capture (a43a-2d) names. From here to the capture no
pinned input moves (the 67 children, the principals, the 13 authority views). Measured: the declaration agrees with its own
planned record and manifest (`MATCHED-GPR-CASE: 8 tests / 0 failures`, the planned population now four cases);
`REQUIREMENT-STATUS: … 4 case(s), 1 credited, 1 declared … 0 drift` — the XLEN case binds REQ-D-XLEN and credits nothing;
the family holds 75 files. Next: a43a-2d, the capture, exactly once.

<a id="a43a-2b"></a>

### .14 a43a-2b / SEMULITH-P4-0322: the XLEN case declared — the first non-M case, on its own authority (completed)

`evidence/rv64gc-xlen-forms-v1/case.sexp` (9,728 B) declares REQ-D-XLEN's case: `xlen-forms.s`, 25 boundaries, 17
predeclared properties read off the source derivation and each checked against it (bit 63 and the shifts by 63, the
upper word and the 6-bit shift amount, 2^63 - 1, the 2^64 wrap and the discarded carry, RV64 LUI, ADDIW, SRLIW, SRAIW,
ADDW, SUBW, SLLW, the address 2^40 and the handler's `mtval` carrying it whole), all 25 boundaries reviewed; control:
`xlen-address-reported` at 0, the address truncated to 32 bits; authority REQ-D-XLEN / OB-XLEN / RVI-RV64I projected from
the catalogues (`project_authority`), normative input `RVI-RV64I-STATEMENTS` (a43a-2a); `cell` values use the schema's
`form:<mnemonic>` vocabulary — every XLEN witness is an instruction's result, so the pinned schema needed no change. Before
declaring, a43a-1's own defect (§15): five RV64I section labels in the guest's comments disagreed with the page's headings
(LUI and ADDIW are §3.1.2.1, ADDW, SUBW and SLLW §3.1.2.2); corrected, the expectations re-derived (`--parcels --steps 25`,
only those five lines), the corpus fixture regenerated (`GUEST-GEN: ok`), and the case pins the corrected source (3,009 B,
`83668ff2…`). `prepare_div_inputs.py --show/--write/--verify` curated the four prepared inputs through the public owners
(guest.elf 4,408 B; the control expectation's one change at boundary 24, x31); the producer review accepts the case
(`pending`, 67 children, its excerpt the normative child) and so does the authority review — the a44-2c generalization's
first use. The evidence family's fourth re-derivation: 89 files / 64 MiB (four cases at most 55,316,480 B), 72 files
present, the index at 3,717 B. Status unchanged (the case has no declarations yet, so it binds nothing). Announced and
withdrawn the same morning (recorded for honesty): a lapse-inducing fix of the pinned collector, on a diagnosis — macOS
`killpg` answering EPERM for a zombie-only group — that a traced hunt showed could not reach the failing arms
(target/p4-system-14/collector-race/FINDING.md); the gate's EPERM struck only under a sibling repository's load on this host,
and a tracer (`SEMULITH_EPERM_TRACE`, scratch) names its call site the next time. Next: a43a-2c, the XLEN declarations
(`capture_div.py --declare`) and its capture.

<a id="a43a-2a"></a>

### .14 a43a-2a / SEMULITH-P4-0321: the XLEN case's normative statements retained — RVI-RV64I §3.1 (completed)

The first unit of the XLEN case under ruling B (a new case adds data and touches no pinned code). A case's normative
input is a retained excerpt whose wrapper names the original page, and that page must be the case's source publication
(a44-2c), so REQ-D-XLEN's one source, RVI-RV64I (`unpriv/rv64.html`, 49,246 B, its pin in `sources.sexp` and the
snapshot manifest), is retained the way the M statements were: `scripts/retain_rv64i_statements.py` copies ten exact
statements in source order — `norm:rv64i_xreg_sz` (§3.1.1), `norm:rv64_w_sex` (§3.1.2), ADDIW, its overflow, the
`*IW` shifts, RV64 LUI (§3.1.2.1), ADDW/SUBW, their overflow, the 6-bit shift amount and the `*W` shifts (§3.1.2.2) —
under the unprivileged licence evidence, into `profiles/rv64gc-lab-v0/retained/rv64i-statements.html` (4,163 B,
`5c939418…`, `RVI-RV64I-STATEMENTS`), naming the page's digest once. The spans' markup, measured before review, is
five `<em>` and one same-publication cross-reference (`<a href="rv32.html#gprs" class="xref page">`); the spans stay
unmodified, so the extractor accepts exactly those shapes and refuses any other tag or attribute (its first emission
refused the cross-reference, then the emphasis — each reviewed and admitted by shape). Controls:
`scripts/probe_rv64i_statement_retention.py`, 17 cache-free tests and seven guard omissions in PROFILE-CONSISTENCY
(`span-markup` 7, `retained-pin` 2, the others 1); a nested-span guard was dropped as unobservable — the allowlist
refuses a nested span, the test kept. PROFILE-CONSISTENCY's real run verifies the excerpt offline beside the two M
excerpts. The SRC-01 record is `materials/RVI_RV64I_RETENTION.md`; the materials catalogue names it. No case, capture
or credit yet: next a43a-2b, the XLEN case's declaration (its case file, properties and prepared inputs). Containment
(this tree was 132,155 B, over its 131,072 B part ceiling, at the prechecks): the closed records a43a-1, a43b-1, a43d-1,
a44, a44-1 and a44-2a and their acceptance rows moved verbatim into `archive/P4-SYSTEM-23.md` (27,771 B, nine spans with
their digests; the a43b-1 mechanism), 108,108 B live. The first commit chain refused before committing (§15, own defect): GATE-REPORT — the
GS report digests the profile's tracked sources and was not regenerated after the new excerpt was staged (regenerated).

<a id="a44-5"></a>

### .14 a44-5 / SEMULITH-P4-0320: the reviews read v4 and the credit is re-issued — the one lapse closed (completed)

`review_div_method.py` names the v4 capture (`RETAINED_CASE_ID`, the declaration commit 177b43a1, the capture commit
3c464095, the measured record's 16,942 B and digest) and reports `satisfied` over 88 authenticated files (1,098,379 B; v3's
was 85); `review_div_policy.py` reads v4: `DIV-POLICY: satisfied — 10 of 10 legs satisfied`. The crediting act, as at
a42az and under the same rulings (`decision_req-gc-m-credited-implemented.md`, Re-credit): `credits.sexp` recreated with
`CR-GC-M-2` (case v4; the measured record, receipt and policy pinned; authority `review`; ten legs; the three
limitations), `REQ-GC-M` `implemented` — `REQUIREMENT-STATUS: … 47 planned, 1 implemented; 3 case(s), 1 credited … 1 of
1 credit record(s) current; 0 drift`, `CREDIT-RECORDS: … 1 credit(s), 1 current`. The method review stays `satisfied`
after the status edit (the semantic digests normalize the status, as at a42az; measured). The dossier copy is v4's
measured record, form for form, and the gate's `G-TRACE` row names it: GS `G-TRACE … green`, `Open axes (3 of 10)`
(`G-STATE`, `G-OBLIGATIONS`, `G-RELEASE`). Restated, each measured: the method and policy probes' real-tree arms (current
→ satisfied, credited by `CR-GC-M-2`), the dossier probe's (v4 qualifies on the real tree, v3 does not; the mirror keeps
judging the frozen `CR-GC-M-1`), the status probe's, and the property probe's `derived-status` loss back to 37 (36 arms,
0 differ). The lapse lasted a44-2b to a44-5, six commits on one day. Ruling B is carried out; next in this leaf the XLEN,
CSR-SET and SSTC declarations as data, each a new case file touching no pinned code. By the 5:1 rule this is the sixth
feature unit since XTASK-0072 — run so the lapse closed back to back; the next unit is an XTASK slice (`XTASK.13`).

<a id="a44-4"></a>

### .14 a44-4 / SEMULITH-P4-0319: the M v4 case captured, exactly once (completed)

`python3 -B scripts/retain_div_capture.py --case rv64gc-m-forms-v4 --declaration-commit 177b43a10745fc5406e787b601d8699b946dbb63`,
one invocation after its preflight (`ready`: 14 output names absent, the reference binary's digest the retained identity's,
`16de42a8…`): three zero-exit processes, baseline and repeat AGREE, the control DIVERGE (boundary 12, x15, −3 → −4),
complete, qualification false, in 1.2 s (target/p4-system-14/a44-4: preflight.json, capture.json). Retained: the twelve
observations, `measured-experiment.sexp` (16,942 B, `aadb5ef3360f1d14…`) and `verification.json` (7,017 B, `1d4b1b5d5472a85b…`);
the case directory holds its 22 of 22. Ruling 1's reproduction rule holds: every trace and stdout is byte-identical to
v3's, and the three stderr streams differ only by the case directory in the trace path they print — the manifest is the
only declared difference. Status: `3 case(s), 0 credited, 0 declared` (v4 pending, uncredited until a44-5). The method
and policy reviews still name v3: a44-5 points them at v4, naming this commit as the capture commit, and issues the
credit. Restated: the input probe's member census (67 present), the status probe's real-tree arm, the index's v4 row.

<a id="a44-3"></a>

### .14 a44-3 / SEMULITH-P4-0318: the M case declared as v4 under the declaration-as-data manifest (completed)

The one re-capture of ruling 1, declared. `evidence/rv64gc-m-forms-v4/case.sexp` is v3's declaration with the new id,
rendered by `matched_gpr_case.render` (every field but the id equal, measured). The prepared inputs derive from the
canonical program, override and expectation only, never from the case id: `prepare_div_inputs.py --show --case
rv64gc-m-forms-v4` reported v3's four pins byte for byte, `--write` created them and `--verify` re-derived them. `capture_div.py
--declare --case rv64gc-m-forms-v4` emitted the three declarations (planned 16,915 B, dependencies 15,166 B with **67**
children — the case's declaration, its schema and its reader among them — authorities 17,721 B), written exclusively and
committed here: this commit is the declaration commit a44-4 names. From here to the capture no pinned input may move —
the manifest's 67 children, the nine principals and the 13 authority views the capture regenerates `authorities.sexp`
from. The evidence family's third re-derivation (`decision_evidence-family-two-cases.md`, Addendum a44-3): 67 files /
48 MiB (health 64 / 42 MiB); three cases hold at most 41,488,384 B (`retention_limits()`), 53 files present at
declaration; `evidence/README.md` compressed to hold the third row (3,383 B of its 4,096 B cap). Status: `3 case(s), 0
credited, 1 declared` — v4 binds `REQ-GC-M` and credits nothing until its capture and credit. Probes restated: the input
probe's census (v4's pins are v3's), the declaration probe's planned-record population, the property probe's case ids,
the status probe's real-tree arm. Own slip (§15): the first write of the declarations parsed the command's JSON object
as the file map and created three stray files (`disposition`, `case_id`, an empty `canonical_capture`) in the new case
directory; they were removed, untracked and never staged, before the three declarations were written from its `files`
map. Next: a44-4, the capture, exactly once.

<a id="a44-2c"></a>

### .14 a44-2c / SEMULITH-P4-0316: the checks specific to the M source become checks of the case's own authority (completed)

The rest of a44-1's generalization, before v4 so the capture pins the final code. `review_div_capture.check_retained_input`
no longer compares a case with the DIV excerpt's constants (`RVI-M-DIV-STATEMENT`, `PRIMARY`, `retain_div_statement`'s
`RETAINED_SHA` and `SOURCE_SHA`): a case declares 1–8 normative inputs (`RETAINED_INPUTS`), each retained under its
profile's `retained/` directory with unique ids and paths, its bytes its pin, and its wrapper naming exactly one original
publication (`Original page SHA256: <code>…</code>`, which both retained excerpts carry) equal to the case's source digest
— which the authority review holds equal to the current source catalogue; an excerpt is never its own publication. The
case's excerpts, not a fixed path, are its normative manifest children (`child_paths`, `prepare_capture`), and
`capture_div.review_authorities` accepts the case's declared obligations, each in the catalogue, projecting the one its
authority names (not exactly one, at index 0). Measured: both cases review `pending` with 67 children; the review probe
33 tests — a non-M case (a synthetic `RVP-X` excerpt) accepted on its own authority and refused when its excerpt names
another page, its excerpt the child in place of the M one — with `publication-authority` 2 → 4 and `retained-pin` 1 → 2
losses and two new seams (`excerpt-not-publication`, `excerpt-population`, 1 each); the authority probe 19 tests, the
new `obligation-binding` seam losing the projected-obligation test. The method checker's census lost the extractor (no
checker code imports it now): `SOURCE_MODULES` excludes `retain_div_statement`, 39 checker sources (measured: the
method review refused `project module population differs` until then). Not generalized here, by design: the policy
review's per-obligation feature table holds `OB-GC-M` alone (`review_div_policy.py`, unpinned) — a non-M case's policy
measurement adds its own row without a lapse. The first self-test run missed one arm (`1187 pass / 1 fail`): the
method probe's `evaluation-accounting` in optimized mode, a child past its 20 s hang guard under the self-test pool (1–2 s
idle, the arm green alone); the guard is 60 s now, as the probe's heavier children have 120 s. Next: `.15` slice g, then a44-3.

<a id="a44-2b"></a>

### .14 a44-2b / SEMULITH-P4-0315: the tools read the case declarations; the in-code tables removed; `CR-GC-M-1` retired (completed)

The second half of a44-1's a44-2, and the one lapse. `scripts/matched_gpr_case.py` returns neutral data — a dictionary
of the schema's fields, tuples for the repeated forms — and `matched_gpr_property.reviewed_case` maps it onto the
review's records on every call; `capture_div.prepared_inputs` reads the declaration's pins. Removed (one definition):
`_CASES`, both case builders and their tables (`_PUBLICATION_SHA`, `_REQUIRED_INPUT_ROWS`, the two semantic digests,
`_DIV_*`, `_M_FORMS_*`) and `capture_div.CURATED_INPUTS` / `PREPARED`; before removal each declaration mapped equal to
its in-code case and its prepared rows to the pins (target/p4-system-14/a44-2b/equality-before-removal.txt). Why
neutral data: the property probe executes a mutated copy of the module as a separate module, and a dataclass compares
unequal across two class objects, so loader-built records would have moved every loss count (measured: all 35 arms
unchanged; knowledge card `records-built-by-a-loader-break-a-mutated-module-copy.md`). Re-derived, each measured: the
producer review pins each case's declaration and its schema as children (`declaration_paths`) and requires the reviewed
case to equal the one its pinned bytes declare (`check_declaration`): 38 modules, 67 children, 82 reviewed files (37,
64, 79 before); `MANIFEST_INPUTS` becomes a ceiling of 96 (`capture_div.py` and `matched_gpr_adequacy.py` count the
population instead of requiring 64, and `capture_div.py` requires the declaration among the pinned children); the
binding stays pure when its caller passes the selected case (the evaluation does), the authority review takes the
reviewed case so its traced window still reads exactly the 13 views, and the unit collector checks its scope before
reading the case. 18 of 41 matched-GPR/DIV/status probes refused after the switch (green-1) and were re-pointed with
every changed count measured: the authority, command, method and retention runtimes copy the declaration (53, 106
files; a case directory stages 8 files, 22 after a capture); the review probe's populations (67, 66) and its inclusive
ceiling patched to the population; the synthetic bound tests derive from the ceiling; the method probe's checker
sources 40 and authenticated files 88. New controls: `passed-case` (property, 1 loss; 35 tests), `declaration-children`
and `declaration-binding` (review, 1 each; 32 tests), the declaration probe's agreement with each retained planned
record and manifest (8 tests); the retention probe asserts its first retain's code (a44-1's hardening). One count
moves with the lapse itself: the property probe's `derived-status` mutation loses 2, not 37, while `REQ-GC-M` records
`planned` (the mutation reads the record's own status, invisible on a planned record); a44-5 restates it. The lapse:
`CR-GC-M-1` retired by removal, with the catalogue file (RECORD-SCHEMA refuses an empty catalogue and reads an absent
one as no credits, the state before a42az; a44-5 recreates it) — its text frozen as
`scripts/fixtures/dossier-qualification/credits.sexp`, the credit of the dossier probe's re-pinned mirror root; `REQ-GC-M` records `planned` (`REQUIREMENT-STATUS: … 48 planned; 2
case(s), 0 credited … 0 drift`), the dossier copy and the `G-TRACE` row removed, the axis open and owned here (GS: 5 of
10 open); the method review reports the m-forms capture `stale`, the policy review `invalidated — 8 of 10 legs`; the
decision records carry the Retirement and the Addendum. `.15` slice g (the workload kind, which edits the pinned report
generator) is no longer blocked by a current capture: it lands before a44-4, so v4 pins the final generator. The first
commit chain refused before committing (§15, own defects): MATERIALS-BILL — the model book's dossier fragments were
not regenerated after `references.sexp` changed (`gen_model_book.py --unit rv64gc-lab-v0`) — and RECORD-SCHEMA — the
retirement left an empty `credits.sexp`, which the schema refuses (removed). Next: a44-2c.

<a id="acceptance-rows-a44-2b-to-a43a-2f"></a>

## acceptance-rows-a44-2b-to-a43a-2f

- [x] `.14` a44-2b **ROOT CAUSE** — the tools still read the cases from code after a44-2a: at HEAD `git show HEAD:scripts/matched_gpr_property.py | grep -c '^_CASES = '` = 1 and `git show HEAD:scripts/capture_div.py | grep -c '^CURATED_INPUTS = '` = 1, so declaring a case edited two pinned scripts; the review's population was a fixed 64 (`capture_div.py` `len(children) == 64`).
- [x] `.14` a44-2b **ADDRESSED** — `grep -c "_CASES\|signed_division_case\|m_forms_case\|_REQUIRED_INPUT_ROWS" scripts/matched_gpr_property.py` = 0 and `grep -c CURATED_INPUTS scripts/capture_div.py` = 0, after target/p4-system-14/a44-2b/equality-before-removal.txt (both cases `case-equal True prepared-equal True`); `python3 scripts/review_div_capture.py --review` → `pending 38 27 13 39 67 82`, `False False`; the property probe's 36 arms measured against the table (property-arms.txt: `36 arms, 0 differ`); `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `0 credit(s)`; `python3 -B scripts/requirement_status.py` → `48 planned; 2 case(s), 0 credited … 0 drift, 0 finding(s)`.
- [x] `.14` a44-2b **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1182 pass / 0 fail` (target/p4-system-14/a44-2b/pc-selftest-2.log, 478 s; the first run's 4 misses — `derived-status` 37 → 2 with the status change, the `case-pass-through` seam text — re-measured, pc-selftest-1.log); every matched-GPR/DIV/status probe green in both modes inside it; the staged prechecks green (target/p4-system-14/a44-2b/prechecks.txt) and the commit gate (chain log).
- [x] `.14` a44-2c **ROOT CAUSE** — after a44-2b the review still bound a case to the M source's constants: `git show HEAD:scripts/review_div_capture.py | grep -c 'RVI-M-DIV-STATEMENT", PRIMARY, Retain.RETAINED_SHA'` = 1 and `git show HEAD:scripts/capture_div.py | grep -c 'len(case.obligation_ids) == 1'` = 1, so a non-M case would be refused by pinned code.
- [x] `.14` a44-2c **ADDRESSED** — `grep -c "Retain\.\|RVI-M" scripts/review_div_capture.py` = 0; `grep -c "len(case.obligation_ids) == 1" scripts/capture_div.py` = 0; `python3 -B scripts/probe_div_capture_review.py` → `33 tests / 0 failures / 0 errors` (the non-M case accepted on its own authority); `python3 -B scripts/probe_div_authorities.py` → `19 tests / 0 failures / 0 errors`; seams measured: `publication-authority` 4, `excerpt-not-publication` 1, `excerpt-population` 1, `retained-pin` 2, `obligation-binding` 1.
- [x] `.14` a44-2c **NO REGRESSION** — the 41 matched-GPR/DIV/status probes rc=0 (target/p4-system-14/a44-2c/green-1 and the method/policy re-runs); `python3 -B scripts/review_div_method.py` → `stale`, 39 checker sources; `PROFILE-CONSISTENCY --self-test: 1187 pass / 1 fail` (pc-selftest-1.log: the load timeout above, its arm green alone, `DIV-METHOD: 1 tests / 4 failures`, as expected), the guard raised; the staged prechecks (prechecks.txt) and the commit gate's self-test (chain log).
- [x] `.14` a44-3 **ROOT CAUSE** — the M case's only capture (v3) is invalidated since a44-2b and ruling 1 re-captures it once under the new manifest: at 1e0a0e8b `ls evidence/ | grep -c m-forms-v4` = 0 and `python3 -B scripts/requirement_status.py` → `2 case(s), 0 credited, 0 declared`.
- [x] `.14` a44-3 **ADDRESSED** — `python3 -B scripts/prepare_div_inputs.py --show --case rv64gc-m-forms-v4` → v3's four pins (4,440 / 7,609 / 7,937 / 7,440 B), `cmp` identical for all four after `--write`; `grep -o "(input " evidence/rv64gc-m-forms-v4/dependencies.sexp | wc -l` = 67 with `evidence/rv64gc-m-forms-v4/case.sexp` among them; `python3 -B scripts/requirement_status.py` → `3 case(s), 0 credited, 1 declared … 0 drift`.
- [x] `.14` a44-3 **NO REGRESSION** — `DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors` plain and `-O` (the census at 67 files, 41,488,384 B); the 41 matched-GPR/DIV/status probes rc=0 (target/p4-system-14/a44-3/green-1 and the three re-runs); `PROFILE-CONSISTENCY --self-test: 1188 pass / 0 fail` (pc-selftest-1.log); `RECORD-SCHEMA: ok (25 record file(s) …)`; the staged prechecks (prechecks.txt) and the commit gate (chain log).
- [x] `.14` a44-4 **ROOT CAUSE** — v4 was declared and uncaptured: at 177b43a1 `ls evidence/rv64gc-m-forms-v4 | wc -l` = 8 and `python3 -B scripts/requirement_status.py` → `1 declared`.
- [x] `.14` a44-4 **ADDRESSED** — `retain_div_capture.py … --preflight-only` → `ready` (14 absent); the one invocation rc=0 → `pending`, `complete True qualification False`, runs `baseline 0, repeat 0, control 0`, verdicts `AGREE AGREE DIVERGE`; `ls evidence/rv64gc-m-forms-v4 | wc -l` = 22; `cmp` of the three traces and three stdout streams with v3's: identical; `diff` of each stderr: only the trace path's case directory.
- [x] `.14` a44-4 **NO REGRESSION** — `DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors` (67 members); `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors`; the 41 probes (target/p4-system-14/a44-4/green-1); the staged prechecks (prechecks.txt) and the commit gate (chain log).
- [x] `.14` a44-5 **ROOT CAUSE** — the lapse: at 3c464095 `ls profiles/rv64gc-lab-v0/credits.sexp` absent, `python3 -B scripts/requirement_status.py` → `48 planned; 3 case(s), 0 credited`, `grep -c 'RETAINED_CASE_ID = "rv64gc-m-forms-v3"' scripts/review_div_method.py` = 1.
- [x] `.14` a44-5 **ADDRESSED** — `python3 -B scripts/review_div_method.py` → `satisfied` (88 files); `python3 -B scripts/review_div_policy.py` → `DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-GC-M-2`; `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `1 credit(s), 1 current, 0 lapsed`; `python3 -B scripts/requirement_status.py` → `47 planned, 1 implemented; 3 case(s), 1 credited … 0 drift, 0 finding(s)`; GS `Open axes (3 of 10)`.
- [x] `.14` a44-5 **NO REGRESSION** — the property arms `36 arms, 0 differ` (target/p4-system-14/a44-5/property-arms.txt; `derived-status` 37); the 41 matched-GPR/DIV/status probes rc=0 (target/p4-system-14/a44-5/green-1); `PROFILE-CONSISTENCY --self-test: 1188 pass / 0 fail` (pc-selftest-1.log); the staged prechecks (prechecks.txt) and the commit gate (chain log).
- [x] `.14` a43a-2a **ROOT CAUSE** — the XLEN case's source had no retained excerpt: `ls profiles/rv64gc-lab-v0/retained/` held `div-statement.html`, `m-statements.html` and `sail-identity.sexp` only, and a case's excerpt must name its own source page (`grep -c PUBLICATION scripts/review_div_capture.py` ≥ 1, a44-2c).
- [x] `.14` a43a-2a **ADDRESSED** — `python3 -B scripts/retain_rv64i_statements.py --verify` → `matched` (4,163 B, `5c939418…`); `--emit` twice byte-identical; `grep -c "Original page SHA256: <code>6eadb316" profiles/rv64gc-lab-v0/retained/rv64i-statements.html` = 1; `python3 -B scripts/probe_rv64i_statement_retention.py` → `17 tests / 0 failures / 0 errors`, the seven omissions measured (`span-markup` 7, `retained-pin` 2, five at 1).
- [x] `.14` a43a-2a **NO REGRESSION** — `MATERIALS-BILL: ok`; `materials --self-test: 20 pass / 0 fail`; `DERIVED-COUNTS: ok` (the arm total re-derived, 1698); `PROFILE-CONSISTENCY --self-test: 1202 pass / 2 fail` (pc-selftest-1.log): every new arm green; the two misses are the unit-collector probe's arms hit by `process/output I/O: Operation not permitted` — the host sandbox refusing `start_new_session` under the pool's load (bash's own `setpgid` printed the same EPERM this session); each arm alone measures as recorded (`2 failures`, `15 failures`), and the collector is pinned by the credited v4 capture, so it is not edited; the commit gate (chain log).
- [x] `.14` a43a-2b **ROOT CAUSE** — REQ-D-XLEN had no declared case (`ls evidence | grep -c xlen` = 0) and the guest's RV64I citations disagreed with the page (`git show a9e1c6d4:profiles/rv64gc-lab-v0/guests/xlen-forms.s | grep -c '§3.1.2.2'` = 1, on the LUI line; §3.1.2.1 is LUI's heading).
- [x] `.14` a43a-2b **ADDRESSED** — `python3 -B scripts/review_div_capture.py --review --case rv64gc-xlen-forms-v1` `rc=0` → `pending`, 67 children; `python3 -B scripts/capture_div.py --review-authorities --case rv64gc-xlen-forms-v1` → `pending`, REQ-D-XLEN / OB-XLEN / RVI-RV64I; `prepare_div_inputs.py --verify` → `pending` (re-derived); `python3 -B scripts/probe_div_capture_inputs.py` → `34 tests / 0 failures / 0 errors` over four cases.
- [x] `.14` a43a-2b **NO REGRESSION** — the 41 probes rc=0 (target/p4-system-14/a43a-2b/green-1); `GUEST-GEN: ok`; `EXERCISE-COVERAGE` 52/52; `INTERACTION-MATRIX: ok`; `RECORD-SCHEMA: ok (26 record file(s) …)`; `MATERIALS-BILL: ok`; the staged prechecks and the commit gate (chain log).
- [x] `.14` a43a-2c **ROOT CAUSE** — the XLEN case had no declarations, so it could not be captured: at dfbc9f3d `ls evidence/rv64gc-xlen-forms-v1 | wc -l` = 5.
- [x] `.14` a43a-2c **ADDRESSED** — `capture_div.py --declare --case rv64gc-xlen-forms-v1` `rc=0` → `pending`; `grep -o "(input " evidence/rv64gc-xlen-forms-v1/dependencies.sexp | wc -l` = 67; `python3 -B scripts/requirement_status.py` → `4 case(s), 1 credited, 1 declared … 0 drift`.
- [x] `.14` a43a-2c **NO REGRESSION** — `MATCHED-GPR-CASE: 8 tests / 0 failures / 0 errors` (the planned-record agreement over four cases); `DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors`; `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors`; the 41 probes (green-1); the staged prechecks and the commit gate (chain log).
- [x] `.14` a43a-2d **ROOT CAUSE** — at 792820b2 the control's witness step cited no RVI-RV64I §3.1.1 (`git show 792820b2:evidence/rv64gc-xlen-forms-v1/baseline.expected.sexp | grep -c 'RVI-RV64I §3.1.1'` = 0) and no XLEN boundary was marked (`grep -c "(boundary"` = 0), so the policy's source-located and boundary legs could not be met once captured.
- [x] `.14` a43a-2d **ADDRESSED** — `grep -c "(boundary:" profiles/rv64gc-lab-v0/guests/xlen-forms.s` = 10, every tagged step a property's; step 24's source `RVI-RV64I §3.1.1; RVP-MACHINE §2.1.7 (…)`; the re-declaration's token diff: digests and sizes only (6 / 4 / 1 / 5); `retain_div_capture.py … --preflight-only` `rc=0` → `ready`.
- [x] `.14` a43a-2d **NO REGRESSION** — the 41 probes rc=0 (green-1); `GUEST-GEN: ok`; `EXERCISE-COVERAGE` 52/52; `INTERACTION-MATRIX: ok`; `RECORD-SCHEMA: ok (26 record file(s) …)`; the staged prechecks and the commit gate (chain log).
- [x] `.14` a43a-2e **ROOT CAUSE** — the XLEN case was declared and uncaptured: at 5c2cde93 `ls evidence/rv64gc-xlen-forms-v1 | wc -l` = 8.
- [x] `.14` a43a-2e **ADDRESSED** — the preflight `rc=0` → `ready` (14 absent); the one invocation `rc=0` → `pending`, `complete True qualification False`, runs `baseline 0, repeat 0, control 0`, verdicts `AGREE AGREE DIVERGE`, the control's difference `step_n 24, x31 2^40 vs 0`; `ls evidence/rv64gc-xlen-forms-v1 | wc -l` = 22.
- [x] `.14` a43a-2e **NO REGRESSION** — `DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors` (89 members); `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors`; `DIV-CAPTURE-RETENTION: 11 tests / 0 failures / 0 errors` (the wording fix); the 41 probes (green-1); the staged prechecks and the commit gate (chain log).
- [x] `.14` a43a-2f **ROOT CAUSE** — the reviews read one case: at f81bf9f8 `review_div_policy.py --case rv64gc-xlen-forms-v1` `rc=2` → `refused — unsupported: no reviewed capture` (policy-xlen-at-f81bf9f8.log); measured through `--method-json`, `pending — 7 of 10 legs satisfied; missing boundary-fixtures, feature-rules, form-coverage` (policy-xlen-before.err): `0 directed boundary rows`, `OB-XLEN: feature disposition undeclared`, `0 of 0 forms predeclared`.
- [x] `.14` a43a-2f **ADDRESSED** — `python3 -B scripts/review_div_method.py --case rv64gc-xlen-forms-v1` `rc=0` → `satisfied`, 88 files, 1,092,798 B; `--max-read-bytes 1155615` `rc=0`, 1155614 `rc=1`; `--case rv64gc-m-forms-v3` `rc=2` `unsupported`, 0 bytes read; `python3 -B scripts/review_div_policy.py --every-retained` `rc=0` → `rv64gc-m-forms-v4: … 10 of 10 legs satisfied; credited by CR-GC-M-2`, `rv64gc-xlen-forms-v1: … 10 of 10 legs satisfied; no qualification credit`; v4's table identical to the single-case run (`cmp`); `grep -c '(boundary' evidence/rv64gc-m-forms-v4/baseline.expected.sexp` = 0.
- [x] `.14` a43a-2f **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1208 pass / 0 fail` (1204 + the two new seams in both modes), traced: `ls target/p4-system-14/a43a-2f/eperm | wc -l` = 0; the whole check `rc=0` → `PROFILE-CONSISTENCY: ok (5 profile dossier(s) internally consistent)` through `--every-retained` (check.log, run on a quiet host, wait.log); `DIV-METHOD: 21 tests / 0 failures / 0 errors`, `--mutation capture-origin` `1 tests / 1 failures` both modes; `DIV-POLICY-PROBE: 27 tests / 0 failures / 0 errors` both modes, each of the ten seams `1 tests / 1 failures`; `DERIVED-COUNTS: ok` (the arm total 1698 unchanged: the seams are loop rows); the first chain's focused stage refused before the gate, `focused: 2 red of 29` — `cargo fmt` (the new `tool(…)` call) and `KNOWLEDGE-MAP` (the new decision record's row) — both fixed, `cargo fmt --all -- --check` `rc=0`, the map check `rc=0`; the staged prechecks and the commit gate (chain log).

