# P4-SYSTEM ordinary history — part 22

Ordinary, directly readable task history: the complete records of the closed `.14` units
a42ax–a42bc and a43, and the acceptance rows of the closed units a42ay–a43a-1, retained verbatim from
`docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0307` on top of commit `e7c56f4777ee515970ffd5e26c35714b68a5239a` (9
contiguous spans, in source order, one anchor each). The live tree keeps one pointer per record and one
per row span; the records a42aq–a42aw and the rows through a42ax are in part 21, the earlier ones in
parts 13–20. Relative links inside the retained text are written from `docs/tasks/`, their original
base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary
archive part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a43b-1,
SEMULITH-P4-0307.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a43 | 2956 | `91a01937c761c900daf305be5b8d1059d2b9c286df581532742b4d172db11f21` |
| record a42az | 3761 | `bfd346f51436598b8c91cf51e03810fa273b44b9cebe17156074082ce21deed1` |
| record a42bc | 4836 | `1eb4663faad8f6c3794b33f6d52da0fa4307b864b8df4fb93e1c9d488aae654b` |
| record a42bb | 4670 | `f64d0591e8426acec54980fd3623d7b12d037ee03d3e4c4299c746355234cfd9` |
| record a42ba | 1988 | `dd11b302e8377c04a6611693f17959abc10bc4cffa9248dd644ec8ddece3c4e2` |
| record a42ay | 5500 | `66a54ba56e2ebafe0c447dedf249f4d137a302a27e8d04e54e25f431630b262b` |
| record a42ax | 6142 | `40bcaaa41a4cc9777257d3cc7ea75beff7083fe7015f7ebbc8ccddf0d5f1dfdd` |
| acceptance rows a42az–a43a-1 | 8917 | `eec291b2045cd368410b70e3eb04a214ef6d069ac586e805e60643ae3b2587a8` |
| acceptance rows a42ay–a42bb | 11362 | `6c71297bd36f65428e6c8ed3fd5e0b47fa4e3182eae7c4353f036abeb3d9e8c7` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-22.md)   # a span, by its line range
```

<a id="a43"></a>

### .14 a43 / SEMULITH-P4-0305: the state-capture plan — G-STATE's route declared (completed)

Feature 9 of the second cycle (`decision_alternate-port-and-features.md`), on clean a2f4d163. The GS report reads
G-STATE `the hidden-state census: 12 of 12 candidates answered; 0 of 4 state requirements implemented`: REQ-D-XLEN
(defined, low; OB-XLEN), REQ-D-CSR-SET, REQ-D-ZICNTR and REQ-D-SSTC (implementation-defined, high; OB-CSR-SET, OB-ZICNTR,
OB-SSTC), each obligation with its CHK-*-POS/NEG checks, each requirement creditable only through a CURRENT credit record
naming a case (`requirement_status.credited`; today `47 planned, 1 implemented`). The plan (`decision_state-capture-plan.md`):
the four are credited through matched cases in the existing GPR vocabulary (`matched-gpr-v1`, the fixed 11-argv Sail
invocation), one case per requirement, three units each (program + EVD-05 expectations + curated inputs + declaration;
capture with repeat and control + retained reviews; credit signed `review` under the 2026-10-26 delegation + dossier
record + derived status) — XLEN through 64-bit values, wrap and a faulting access's full `mtval`; CSR-SET through
sentinel-loaded reads of the 33, alias pairs, a refused write read back and a non-member's illegal-instruction trap;
ZICNTR through M readability, `mcounteren`/`scounteren` gating and `instret`, with the `cycle`/`time` VALUES named as the
profile difference (the laboratory's fixed-zero cycle and one-tick-per-step time against Sail's `mcycle` per instruction
and `mtime` per two) and left to `mm-counters.expected.sexp`; SSTC through `STCE` gating and boundary-robust schedules
(`stimecmp` 0 and max; `STIE`/`STCE` suppression). Measured for the plan: the pinned Sail sim's `--trace-csr` prints
`CSR mstatus (0x300) <- …` (44 lines over the retained M guest, all at its traps) — a CSR-write vocabulary exists on the
reference side but is not in the fixed invocation; adopting it (`matched-state-v1`: collector parse, comparison rule,
schema pattern, argv, probes) is deferred until a property cannot be witnessed through GPRs. Risk carried into a43a: a
case manifest pins the toolbox beside the semantics (the M case pins `gate_report.py`; the ruling on report generators
is pending), so a43a reviews the dependency closure before capture. Order: a43a XLEN (feature 10), a43b CSR-SET, a43c
ZICNTR, a43d SSTC; G-STATE regenerates green with a43d's status act. Nothing under profiles/ or evidence/ changes in
this unit; the derivation line is unchanged. The first chain's focused stage refused (`KNOWLEDGE-MAP: KNOWLEDGE_MAP.md is
out of sync with its sources`): a new decision record is one of the map's sources and the focused stage judges the map
before the hook regenerates it — `knowledge-map/scripts/gen_knowledge_map.sh > KNOWLEDGE_MAP.md` (+1 line), re-checked ok.
Evidence target/p4-system-14/a43 (design.md, census.txt, sail-trace-csr-sample.txt, chain.log of the refusal).

<a id="a42az"></a>

### .14 a42az / SEMULITH-P4-0296: the crediting act, under the director's delegation (completed)

Owned on clean 1d609ca0. The director delegated the ruling on 2026-10-26
(`decision_four-rulings-delegated.md`): the record `CR-GC-M-1` in `profiles/rv64gc-lab-v0/credits.sexp`
is signed `authority review` under it, never `director`; one finite case (`rv64gc-m-forms-v3`, 25
witnesses: the 13 M forms and the 12 Table 1 cells, one each) whose ten legs measure `satisfied` is
sufficient for `implemented` and for nothing more, its limitations written into the record
(`decision_req-gc-m-credited-implemented.md`); retention came first (a42z, a42bb). The act in one
commit: the record (pins taken from the tree: measured `fb22d5e5…` 16,942 B, receipt `91a90d9c…`
7,017 B, policy `85296cf7…` 9,230 B), `implementation_status implemented` on `REQ-GC-M`, the GS report
regenerated (`48 requirements: 1 implemented, 47 planned`), the two model-book chapters that said the
status kept deriving `planned`. Rehearsed first on a smoke root (target/p4-system-14/a42az/smoke, symlinks
to the real inputs, a copied profile): `CREDIT-RECORDS … 1 current`, `REQUIREMENT-STATUS: ok (… 47 planned,
1 implemented … 1 credited …)`, and two RED controls — the record present with the status left `planned`
→ `drift … recorded planned derived implemented`; a moved measured pin → `lapsed`, the status falls back,
`1 drift, 1 finding`. On the real tree: `DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by
CR-GC-M-1`.

Two defects owned mid-slice. (1) `RECORD-SCHEMA` refused the real catalogue: `check_requirements.sh`
validated it against its schema and then handed every catalogue to the pinned records reader, which
refuses the `credit` head by design (the a42ay design knew this for the reader and gave the credits their
own module, but the gate's loop had no branch for it, and the real tree held no `credits.sexp` to show it).
The loop now reads `credits.sexp` through `credit_records.load_credits` (schema re-validated, bounded,
duplicate ids refused, an empty catalogue invalid) and never through the pinned reader; three arms (GREEN
a catalogue reads; RED a duplicate id; RED an empty catalogue), each fired on the real tree too. (2) The
first version of those arms deleted the tracked `schema/credits.sexp`: the fixture's `$t/schema` is a
link to the real schema directory (`ln -sfn "$ROOT/schema" "$t/schema"`, line 747), and the arm removed
"its" copy through the link. Found by the token-facet probe's closed inventory (`24 != 25`), the culprit
isolated by running each suspect alone and checking the file after each; the file restored from git
(`git checkout -- schema/credits.sexp`, 25 schemas); the arms now neither copy into nor remove under
`$t/schema`. The lesson joins the scratch-hygiene card. One more observation, not a defect: the GS
report's dossier digest covers every *tracked* source file under the profile, so the report regenerated
before `credits.sexp` was staged went out of sync the moment it was (`GATE-REPORT` red in the first focused
run, `8f90fe23…` → `afcaa32c…`); regenerated after staging, in sync — stage a new profile file first, then
regenerate. Two more derived artifacts followed the same inputs in the second focused run: the unit book's
`materials/internal-contracts.md` pins `requirements.sexp`'s digest (`0f006fa9…` → `2f83ca52…`;
`python3 scripts/gen_model_book.py --unit rv64gc-lab-v0`), and `KNOWLEDGE_MAP.md` lists the decision records
(five rows; `gen_knowledge_map.sh > KNOWLEDGE_MAP.md`, as the pre-commit hook writes it). Both regenerated, never
edited; the three derived artifacts a profile change moves are now named here for the next act. Evidence
target/p4-system-14/a42az.

<a id="a42bc"></a>

### .14 a42bc / SEMULITH-P4-0297: the first qualified experiment record — G-TRACE evidenced (completed)

Owned on clean 76d8d203, the first project feature unit under the director's ruling of 2026-10-26 to alternate
tooling and feature work (`decision_alternate-port-and-features.md`). The qualified matched-experiment contract
(`decision_qualified-matched-experiment-contract.md`) had PROFILE-CONSISTENCY refuse every verification-bearing
experiment record in a dossier as `UNQUALIFIED EXPERIMENT VERIFICATION` — "complete method/policy adequacy
pending" — and the GS report read G-TRACE `0 of 1 required kinds evidenced` while the credited M case stood as a
judged experiment under evidence/ with no dossier record. Qualification is now a computed result, in one place:
`credit_records.dossier_qualification(root, profile_dir, form)` returns why a dossier experiment form is NOT
qualified — no credit record names its case; no CURRENT one does (the lapsed reasons quoted); the case has no
measured record; the dossier record differs from the case's `measured-experiment.sexp` form for form — and is
qualified when the list is empty. The gate calls it where the unconditional refusal stood and prints the reasons;
matching pins alone still grant nothing, and the record's own verdict words never do. The measured record of
`rv64gc-m-forms-v3` (33 instructions, 25 finite witnesses, its matched-gpr-v1 graph: baseline, byte-identical
repeat, the wrong-quotient control observed diverging, 21 pinned artifacts) is now the dossier's one `experiment`
(references.sexp 17,926 → 35,344 B; the owner stays evidence/rv64gc-m-forms-v3/measured-experiment.sexp and the
gate refuses the day the two differ), and gate.sexp declares it as the G-TRACE `experiment` evidence; the G-TRACE
open row retires (the axis is measured, never declared) — the eight earlier Sail matched experiments stay prose in
matched_scope, history until each is re-run as a record under the same contract, as the evidence statement says.
Measured before the act: the real dossier scope raised 0 graph findings on the measured form and all 21 pins
matched; CR-GC-M-1 authenticates `current`. After it, the gate's dossier judgement over `profiles` returns 0 with
no UNQUALIFIED line, and two RED controls on a scratch copy refuse — an uncredited id (`no credit record names the
case …; the case has no measured record …`) and a record whose `instructions` reads 34 (`the dossier record
differs from the case's measured record`). The GS report regenerates with G-TRACE **green** (`1 of 1 required kinds
evidenced`, evidence `experiment rv64gc-m-forms-v3` verified `yes`), open axes 6 → 5; the model book's two
fragments that pin references.sexp regenerate. REQUIREMENT-STATUS, DIV-POLICY and the three real-tree probes are
unchanged (47 planned, 1 implemented; 10 of 10 legs; 22/25 tests, `derived-status` 36 failures as the gate expects).
The new probe `scripts/probe_dossier_qualification.py` (six tests over a scratch root that copies every pinned
path and the case, so a test may lapse the credit or change the record while the real tree is only read) joins
the gate's self-test with three seams fired RED (`credit-any`, `mirror-any`, `id-any`), in both Python modes;
the arm that pinned "every block refused" now pins "a block with no current credit stays unqualified".
Evidence target/p4-system-14/a42bc.

The gate's answer to the third chain (2026-10-26T11:21Z, gate3/selftest-refusal.log): `PROFILE-CONSISTENCY`
refused — its self-test pins the real tree's state in three arms that the focused set never runs. The
requirement-status probe's real-tree arm predicted two pending cases and no credit; the policy probe's
predicted `credited` false, and its moved-pin branch a current record with no finding; the source-property
probe's `derived-status` mutation arm predicted 2 failures, a count that follows the real `REQ-GC-M` record
the fixture reads (2 while it recorded `planned`, 36 — every binding — once it records `implemented`). Each
re-predicted from the measured tree, none loosened: one pending case, `implemented` recorded and derived,
`CR-GC-M-1` current, 36. The moved-pin branch was then exercised on the real tree, one byte appended to a
pinned method input (`definitions/riscv/m.sexp`) and then to the policy pin (`EVIDENCE_POLICY.md`), each
restored from the index and verified: the credit's authentication walks the case's dependency manifest, so
any moved input lapses the record — `invalidated — 8 of 10 legs … FINDING credit CR-GC-M-1 names this case
but lapsed`, exit 1, the status falling back with `1 drift, 1 finding`. For the next act: run the three
probes before launching the chain; the full self-test costs the gate's fifty minutes. Carded
(`a-real-tree-probe-arm-is-a-prediction-the-act-re-states.md`).

<a id="a42bb"></a>

### .14 a42bb / SEMULITH-P4-0295: retain the other M statements and Table 1 (completed)

Owned on clean 610783e. The m-forms case's 25 properties cite §11.1.1, §11.1.2 and Table 1 of the pinned
M chapter, but only the DIV/DIVU span is a retained normative excerpt
(`profiles/rv64gc-lab-v0/retained/div-statement.html`, a42z); the crediting record (a42ay) names the
retained sources a credit rests on, so a credit today would rest on cited, unretained text — the
question put to the director at a42at and a42ax. Measured (target/p4-system-14/a42ay/retention-scope.md):
the pinned page (35,588 B, `85e1db6c…`) holds twelve `norm:` spans (2,038 B; DIV/DIVU 182 B already
retained) and Table 1 (1,698 B, static table markup only); `sources.sexp` and any new file under
`retained/` are outside the 64 inputs the m-forms declaration pins, so retention invalidates nothing,
while `scripts/retain_div_statement.py` is pinned and must not change. Build `scripts/retain_m_statements.py`
(`--emit` from the acquired pages, `--verify` offline; the eleven other spans and Table 1 in one attributed
wrapper; the source and licence pins imported from their one owner; an allowlist of static markup), its
probe with seams, the retained file `profiles/rv64gc-lab-v0/retained/m-statements.html` (`RVI-M-STATEMENTS`),
the gate's verify step and arms, the scope note in `materials/RVI_M_RETENTION.md`, a decision record and
the toolbox row. No credit, no status move: the act stays the director's. Evidence target/p4-system-14/a42bb.

Done 2026-10-23. `scripts/retain_m_statements.py` selects the eleven spans in source order (each unique,
terminated, at most 1,024 B, no nested span, only `<code>` inside) and Table 1 by its marker and caption
(unique, terminated, at most 4,096 B, no nested table, only reviewed table markup and `class`/`id`/`style`
attributes with every style a column width), checks both complete pinned inputs and the licence statement
through `retain_div_statement`'s pins and `pinned()` (imported, not edited), and wraps them with the
a42z attribution; the wrapper names the separate DIV/DIVU excerpt instead of repeating it. Emitted through
its own `--emit` from the acquired pages: 6,018 B, `bc777ebb…`, byte-identical to the scratch preview and
on re-emission; `--verify` offline `matched`. Probe `scripts/probe_m_statement_retention.py`: 20 tests in
both modes (19 synthetic, one real-tree offline verification), ten seams each failing its discriminating
tests (1/1/1/1/3/4/1/1/1/2 — the two markup seams fail every unsafe sub-case). Gate: the `--verify` step
beside the DIV statement's and 22 arms; the arm total re-derived 1653 → 1655 in LIVE_STATUS. Real tree
unchanged: method `satisfied`, policy `satisfied — 10 of 10`, 0 credited. Documents: the second scoped
retention in `materials/RVI_M_RETENTION.md` (spans, bytes, markup allowlist, why nothing pinned moved),
`decision_m-statements-retained.md`, toolbox row, policy-adequacy and requirement-status sentences, MEMORY
(ruling (c) answered; (a) authority and (b) sufficiency remain the director's). The first focused run was RED on
`check_gate_report.sh` (`profiles/rv64gc-lab-v0/GS-REPORT.md is out of sync`: its dossier digest covers every tracked source
file under the profile, so the new excerpt moved it, e6777221… → 49ebeb22…); regenerated through `scripts/gate_report.py
rv64gc-lab-v0 --gate GS`, one line changed, `GATE-REPORT: ok (5 generated report(s) in sync with their inputs)`.
Defect owned mid-slice: the gated commit (08:10Z → 09:12Z, other repositories' gates sharing the machine) was refused by
the PROFILE-CONSISTENCY self-test, 1154 pass / 2 fail — and for the first time the kept log named the arms (a42ax's
diagnostic working): the method probe's `artifact-selection` and `typed-findings` seams, normal mode only, each failing in
`setUpClass` with `synthetic current capture failed: {"status": "refused"}` after 31.7 s and 59.1 s, where the same
setup takes 2–4 s; the probe's synthetic capture printed the status and dropped the capture's own reason, the same
discarded-diagnostic defect one level down. The probe now prints the reason. Twelve reruns of both seams passed as the gate
expects (repro-setup.log); a freshly written executable launches in 0.13 s against 0.02 s for a re-run at load 6
(fresh-exec-latency.log) — consistent with, not proof of, a first-execution stall reaching the collector's 30 s process
limit under heavier load. Cause not identified; no speculative fix; the next occurrence names its reason. Next: ARTIFACT-CLEANUP.26
(due since 08:12Z), the LIVE-CONTAINMENT tree's own archive move, then the crediting act on the ruling.

<a id="a42ba"></a>

### .14 a42ba / SEMULITH-P4-0294: move the closed `.14` records into archive part 21 (completed)

Owned on clean 3cb37d9. docs/tasks/P4-SYSTEM.md stands at 117,506 B of the task family's 131,072-byte
per-part ceiling (`doctrine/readme_routes.tsv` row `docs/tasks/`; aggregate and count ungoverned by
`decision_containment-reset.md`): one more slice of the current size crosses it. Apply the family's
standing mechanism, as a42ar did for the rows through a42aq: the complete records of the closed units
a42ak–a42aw and the closed acceptance rows a42ar–a42ax move verbatim into
docs/tasks/archive/P4-SYSTEM-21.md (one anchor per record, one section for the rows), each replaced in
the live tree by a one-line pointer; the active and latest units (a42ax's and a42ay's records, a42ay's
rows) stay live. No seal, reader or inverse map (`decision_containment-reset.md`); the moved bytes are
authenticated by SHA256 before and after the move. No code changes. Evidence target/p4-system-14/a42ba.

Done 2026-10-23 by target/p4-system-14/a42ba/move_closed_records.py (move.log): seven records (a42aw 4,118 B,
a42av 3,091, a42au 4,189, a42at 4,607, a42as 3,203, a42ar 3,694, a42aq 1,226) and the 29 acceptance rows
a42ar–a42ax (32,158 B) moved verbatim, each span's SHA256 listed in the part's own table and found once,
byte-identical, in the part; the live file went from 118,497 to 63,186 B (0.48× of the ceiling), part 21 is
58,207 B (0.44×). The live tree keeps the heading and a `[Record](archive/P4-SYSTEM-21.md#<unit>)` pointer
per moved record and `Rows a42ar–a42ax: [retained verbatim](…#acceptance-rows-through-a42ax)` where the
rows were; a42ay's rows and the a42ax/a42ay records stay live. Next: the director's ruling on the crediting
act (a42az); meanwhile the retention of the §11.1.1 and Table 1 spans (scope measured in
target/p4-system-14/a42ay/retention-scope.md), ARTIFACT-CLEANUP.26 after 08:12Z, the LIVE_STATUS
bounded-snapshot re-derivation (6,137 of 6,144 B).

<a id="a42ay"></a>

### .14 a42ay / SEMULITH-P4-0293: the crediting record — mechanism, no credit (completed)

Owned on clean 818b873. Every leg of the policy measures satisfied on the retained case and
nothing can credit it: `requirement_status.credited()` reads a receipt's `qualification`, the receipt
is written once with `qualification false` by `retain_div_capture.py` and is never replaced, and the
policy makes a credited disposition a structured record linking requirement, obligation, owner, runner
and evidence record — none exists (`decision_ten-legs-satisfied-credit-separate.md`). Build the
mechanism without the act: a third profile catalogue `profiles/<profile>/credits.sexp` (schema
`schema/credits.sexp`: requirement, obligations, case, the measured record / receipt / policy pins by
path, SHA256 and size, the retained sources it rests on, authority, date, decision), read by a new
unpinned `scripts/credit_records.py` over `sexp.py` (`records_sexp.py` and `record_catalog.py` are
pinned children of the m-forms declaration and refuse unknown heads: they do not change);
`requirement_status.py` credits a case only through a credit record whose pins authenticate, whose
receipt is complete and whose policy measurement is `satisfied` at read time (a moved pin lapses the
credit, a drift finding follows); a receipt claiming `qualification` becomes a finding, never a credit;
`review_div_policy.credited` reads the catalogue; `check_requirements.sh` validates the catalogue;
probes with synthetic credit records and seams; chapters, toolbox, decision
`decision_credit-is-a-catalogue-record.md`. Real tree after this unit: no `credits.sexp`, `REQ-GC-M`
`planned`, 0 credited. The act (a42az) is one commit the director authorizes: the credit record and
`implementation_status implemented`. Ruling requested of the director before the act: (a) who signs
the record, (b) whether one finite case of 25 witnesses suffices for `implemented`, (c) whether the
§11.1.1 and Table 1 spans are retained first (a42z-style, CC-BY 4.0 already found). Evidence
target/p4-system-14/a42ay.

Done 2026-10-23. Built: `schema/credits.sexp` (constructs `credit` and `pin`; nine anchored facets, two new
token languages — the date and the decision-record name — each with a reviewed example in
`scripts/probe_schema_token_facets.py`, whose census is now 25 schemas / 100 facets) and
`scripts/credit_records.py` (`load_credits` validates the catalogue against the schema and bounds it to 64
records / 64 KiB; `authenticate` re-hashes the three pins and every input of the case's dependency
manifest, requires a complete canonical capture whose `qualification` is false and a declaration binding
the credited requirement and obligations, and names every reason a record lapsed; `--profile <id>`
prints the census). `requirement_status.py` credits a binding only through a current record naming its
case, requirement and obligation; a receipt's `qualification` true, a lapsed record or one naming an
unknown case or requirement is a finding; the summary gains `N of M credit record(s) current`; the
unused `credited` key left the case rows. `review_div_policy.py` reports `credited` and `credit_ids` from
the catalogue, makes a record over a measurement that is not `satisfied` a finding, and ends its summary
`credited by <record>` when one is current. `check_requirements.sh` validates `credits.sexp` under
RECORD-SCHEMA (its token arms re-measured: loose-end 96 → 105, ignore-pattern 552 → 606; the first run
had refused — another gate that discards its self-test output, read through `--self-test`). Probes: status
22 tests / seven seams — `qualification-word` and `unknown-case-credit` new, `declared-credits` retired
because the receipt pin makes a declared case uncreditable by construction and its mutation no longer
reached any predicate (seams-status.log showed it 1t/0f before the retirement); policy 25 tests / eight
seams (`credit-any`). The derivation's fixtures credit through records whose pins are taken from the
fixture's own bytes, never through the receipt. Real tree unchanged in substance: no `credits.sexp`,
`REQ-GC-M` `planned`, 0 of 0 records, the policy `satisfied — 10 of 10 … no qualification credit`.
Chapters requirement-status ("How a case is credited") and policy-adequacy, three toolbox rows,
`decision_credit-is-a-catalogue-record.md`, KNOWLEDGE_MAP regenerated. The first focused run was RED on
`check_readme_routes.sh`: `OVER CEILING schema/: 25 files > 24` (the schema family had sat exactly at its
ceiling since 2026-10-11, its health line passed since 2026-10-02) and `OVER CEILING docs/decisions/: part
docs/decisions/INDEX.md` (16,537 B over 16,384; the index was 16,127 B at HEAD and two contract records
sit within 300 B of the same bound) — re-derived with the measurements in
`decision_schema-and-decisions-families-rederivation.md` (schema files 24 → 32, health 18 → 27, health
bytes 128 → 256 KiB; decisions per-part 16 → 32 KiB, health files 64 → 136, health bytes 272 → 448 KiB),
the two registry rows changed. The act is not taken: it is the director's ruling (authority;
sufficiency; retention first). Measured for that ruling: `sources.sexp` is not among the seven profile
files the m-forms declaration pins, so new retained spans and source rows invalidate nothing. Next,
pending the ruling: the archive move of the closed `.14` rows (this file at 116 KB of its 128 KiB part
ceiling), then the retention of the §11.1.1 and Table 1 spans.

<a id="a42ax"></a>

### .14 a42ax / SEMULITH-P4-0292: the retained reviews read the m-forms capture (completed)

Owned on clean e775705. The m-forms capture is retained and complete, but the retained reviews still
read the invalidated first case: `scripts/review_div_method.py` names `rv64gc-signed-div-truncation-v2`
(`RETAINED_CASE_ID`, its 9,928-byte measured pin, the b160c66/c91d08f commits) and reports `stale`;
`scripts/review_div_policy.py` names it too and reports `invalidated — 6 of 10 legs`; the method probe's
fixture builds its synthetic current capture from the retained constants of the first case and the
policy probe's real-tree arm asserts the first case's numbers. The preview over the m-forms bytes under
a satisfied method already reads `satisfied — 10 of 10 legs` (target/p4-system-14/a42aw/
policy-legs-preview-v3.log). Switch the consumers only — no pinned module moves (`decision_caller-names-
the-case.md`): `RETAINED_CASE_ID`, `MEASURED_SHA256`/`MEASURED_BYTES` (fb22d5e5…, 16,942 B),
`SOURCE_DECLARATION_COMMIT` 4af5a68…, `RETAINED_CAPTURE_COMMIT` e775705…, `review_div_policy.CASE_ID`;
make the method probe's fixture and the shared synthetic reference follow the retained case, and the
policy probe's real-tree arm assert the ten legs; re-measure the method review's numbers for the
chapter; update the policy-adequacy, method-adequacy and canonical-division chapters, the family index,
the toolbox rows and LIVE_STATUS. Measurement, not credit: `credited` stays false and `REQ-GC-M` keeps
deriving `planned`; the crediting act is a separately owned record after this. Containment note for the
director's eye (not a defect): LIVE_STATUS.md stands at 6,138 of its 6,144-byte ceiling (health 4,096
passed long ago) — a bounded-snapshot rewrite or re-derivation is due before the next note grows it.
Evidence target/p4-system-14/a42ax.

Done 2026-10-23. Switched: the five pointers of `scripts/review_div_method.py` and `CASE_ID` of
`scripts/review_div_policy.py` (a comment at each names the switch and the first case as retained
history). `probe_div_command.synthesize_reference(runtime, *, exit_code, case_id)` derives the synthetic
trace from the named case's guest, program and instruction count (`A.Review.guest_path(case)`), default
the first case, so the command and retention probes are unchanged; `probe_div_method` builds its fixture,
controller, paths and real-tree arm from `M.RETAINED_CASE_ID` (prefix, prepared inputs,
`prepare_capture(case)`, `capture(case)`, `freeze_review(..., case_id)`, `evaluate_retained_unit(...,
case_id)`, `moved_inputs(ROOT, case)`), with no `A.PREFIX`/`A.PREPARED` left; three first-run failures
were exactly the three places still on the default case (the moved-inputs question asked of the first
case, the graph-evidence freeze refusing `review differs from the supported finite DIV case`, the
pinned triple 85 / 1,048,756 / 33,759) and each was repointed, not relaxed. The policy probe's real-tree
arm asserts the ten legs, `credited` false, the twelve boundary rows present and predeclared, the
thirteen forms required, predeclared and exercised, and the summary line — or `invalidated` missing
`matched-reference-comparison` and `currentness` with 8 satisfied once a pin moves. Real tree: method
`satisfied | rv64gc-m-forms-v3` over 85 files / 1,076,834 B / 40,438 snapshot bytes, 1,142,222 charged
(the exact allowance boundary: 1,142,222 exit 0, 1,142,221 refused), 39 checker sources; `DIV-POLICY:
satisfied — 10 of 10 legs satisfied; no qualification credit`; `requirement_status` 2 cases, 0 credited,
0 declared. Every seam count unchanged (method 14, command 7, retention 7, policy 7; seams-*.log).
Documents: policy-adequacy (ten legs, "what a satisfied measurement is, and is not", the first case as
history), method-adequacy (pins, commits, numbers, the allowance boundary), canonical-division,
requirement-status, evidence/README (4,045 of 4,096 B after a trim), docs/toolbox/div-evidence rows,
LIVE_STATUS (6,137 B after shortening the P4 note), gate comments, CHANGELOG (50,207 B: past its 48 KiB
health line, under the 64 KiB shard ceiling), `decision_ten-legs-satisfied-credit-separate.md` indexed,
KNOWLEDGE_MAP regenerated. Measurement, not credit.

Two defects owned mid-slice (both left open by a42ar). The first commit attempt (focused set 26 of 26
green, 23:22Z) was refused at 02:17Z by the gate's PROFILE-CONSISTENCY self-test — `REFUSED — the check
does not discriminate (self-test failed)` and nothing else, the MISS line discarded by `self_test
>/dev/null 2>&1`, 2 h 55 min in the hook with two other repositories' gates loading the machine (load
average 8–19 on 12 cores). A captured rerun from the shell on the same tree passed every arm (1130 / 0 in
45 min, selftest.log); no self-test probe calls git or reads the clock; every probe child under the same
load used at most 7 % of its subprocess timeout (children-timing-loaded.log) and a fresh Python child
wrote its first file within 38 ms against the collector probe's 2 s heartbeat wait
(child-start-latency.log). Cause not identified, as on 2026-10-21 — and this time the tree keeps what
the next refusal needs: the gate writes its self-test's complete output to
`target/profile-consistency-selftest.log` and prints the `self-test MISS` lines on REFUSED, fired RED
in a detached worktree with one probe deliberately broken before landing (gate-fire.log). The second
defect was the leak: `scripts/check_citations.py --self-test` left its 19 fixture directories under
`target/doctrine-selftest` on every run — 5,494 of the 5,505 entries, 87 MB, by the gate run of
2026-10-23 (census by content shape: 3,770 citation fixtures, 1,450 corpus fixtures, 290 empty), the
rest aborted self-tests' leftovers; the self-test now removes what it creates and fails if one is left
behind, and the leaked directories were removed (5,524 → 0 entries, 88,412 → 0 KiB). Knowledge card
`a-gate-that-discards-its-self-tests-output-cannot-be-diagnosed.md`; toolbox rows for both tools.
Next: a42ay, the crediting act for `REQ-GC-M` (authority, mechanism, retained excerpts) as its own record.

<a id="acceptance-rows-a42az-to-a43a-1"></a>

## acceptance-rows-a42az-to-a43a-1

- [x] `.14` a42az **ROOT CAUSE** — `python3 -B scripts/requirement_status.py` at 1d609ca0 → `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 48 planned; 2 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current …)`; `ls profiles/rv64gc-lab-v0/credits.sexp` → absent; `grep -c "implementation_status planned" profiles/rv64gc-lab-v0/requirements.sexp` row `REQ-GC-M` = 1; the pins `shasum -a 256` / `wc -c`: measured fb22d5e5554a0e132c231e5551ed8314ab4be35ff93e7f086fceeacb6235a152 16942, receipt 91a90d9c56487af1a6b4306e9007d771e17246ddf41b358185374680090a5a5d 7017, policy 85296cf7ae694f0d40e08ed398989d32f20f4720d4a798bf46a18caf22825071 9230; the gate defect: `grep -n "recs = R.load(cat, root=root)" scripts/check_requirements.sh` = 339 with no `credits.sexp` branch before it → `UNREADABLE profiles/rv64gc-lab-v0/credits.sexp: conforms to its schema but does not map to records — not a record form`.
- [x] `.14` a42az **ADDRESSED** — real-tree.log: `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 47 planned, 1 implemented; 2 case(s), 1 credited, 0 declared, 1 of 1 credit record(s) current; 0 drift, 0 finding(s) …)`, `CREDIT-RECORDS: rv64gc-lab-v0: 1 credit(s), 1 current, 0 lapsed`, `DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-GC-M-1`; smoke REDs: red-status-planned.log `drift rv64gc-lab-v0 REQ-GC-M: recorded \`planned\` derived \`implemented\`` rc 1, red-lapsed.log `CREDIT-RECORDS … 0 current, 1 lapsed` and `finding … credit CR-GC-M-1 lapsed: measured pin … SHA256 or size differs`, `1 drift, 1 finding(s)` rc 1; gate: st2.log `RECORD-SCHEMA --self-test: 73 pass / 0 fail`, real2.log `RECORD-SCHEMA: ok (21 record file(s) validate and agree with their profile; …)`, red-dup.log `UNREADABLE profiles/rv64gc-lab-v0/credits.sexp: conforms to its schema but does not read as credits — … duplicate credit id` rc 1, red-empty.log `INVALID    profiles/rv64gc-lab-v0/credits.sexp: contains no records` rc 1, restored `profiles/rv64gc-lab-v0/credits.sexp: OK` (shasum -c); `ls schema/*.sexp | wc -l` = 25 after the self-test and the real run.
- [x] `.14` a42az **NO REGRESSION** — gate3/selftest-refusal.log: `PROFILE-CONSISTENCY self-test MISS` ×6 (`RED finite source property derived-status`, `GREEN requirement status derivation`, `GREEN policy legs measured`, each in both modes); re-predicted: `python3 -B [-O] scripts/probe_requirement_status.py` → `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors`, `python3 -B [-O] scripts/probe_div_policy.py` → `DIV-POLICY-PROBE: 25 tests / 0 failures / 0 errors`, `python3 [-O] scripts/probe_matched_gpr_property.py --mutation derived-status` → `MATCHED-GPR-PROPERTY: 34 tests / 36 failures / 0 errors`; gate3/moved-m.sexp.log and moved-EVIDENCE_POLICY.md.log: `DIV-POLICY-PROBE: 25 tests / 0 failures / 0 errors` under each moved pin, `DIV-POLICY: invalidated — 8 of 10 legs satisfied; missing matched-reference-comparison, currentness; … FINDING credit CR-GC-M-1 names this case but lapsed: manifest input definitions/riscv/m.sexp: SHA256 differs` rc 1 (the policy pin: `policy pin profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md: SHA256 or size differs`), `REQUIREMENT-STATUS: drift or finding (… 0 of 1 credit record(s) current; 1 drift, 1 finding(s) …)` rc 1; restored: `shasum -a 256 definitions/riscv/m.sexp` = 0f48d4348b850b5fcfd296b220409a2a711d8b13075fdea9059b33d67544a386 and `profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md` = 85296cf7ae694f0d40e08ed398989d32f20f4720d4a798bf46a18caf22825071 as before, `git ls-files -s | shasum -a 256` identical before and after (index-content-before.txt, index-content-after.txt), `.git/config` 5fa9bf39d1cee284f370824209c0efc7dc2358c7554526d8345987a599a279d5 unchanged, HEAD 1d609ca0.
- [x] `.14` a42bc **ROOT CAUSE** — at 76d8d203: `grep -c 'complete method/policy adequacy pending' scripts/check_profile_consistency.sh` = 1 (the unconditional refusal), `grep -c '(experiment (id' profiles/rv64gc-lab-v0/references.sexp` = 0, `grep -c '(axis G-TRACE) (kind experiment)' profiles/rv64gc-lab-v0/gate.sexp` = 0 while GS-REPORT.before.md reads `G-TRACE … 0 of 1 required kinds evidenced — open: experiment` and `Open axes (6 of 10)`; the credited case already judged: `python3 -B scripts/credit_records.py` → CR-GC-M-1 `current`, 0 graph findings and 21 of 21 pins `matched` on its measured form against the real dossier scope (probe in the a42bc notes).
- [x] `.14` a42bc **ADDRESSED** — judgement-after.log: `check_profiles profiles` rc 0, `__CHECKED__ 5`, `grep -c UNQUALIFIED` = 0; RED controls on a scratch copy: the id renamed → rc 1 `UNQUALIFIED EXPERIMENT VERIFICATION rv64gc-lab-v0/rv64gc-nobody-credited-this: no credit record names the case rv64gc-nobody-credited-this; the case has no measured record at evidence/rv64gc-nobody-credited-this/measured-experiment.sexp`; `instructions 34` → rc 1 `… rv64gc-m-forms-v3: the dossier record differs from the case's measured record`; `python3 -B scripts/probe_dossier_qualification.py` → `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures / 0 errors` (normal and `-O`), `--mutation credit-any|mirror-any|id-any` → `1 tests / 1 failures / 0 errors` each; `python3 -B scripts/gate_report.py rv64gc-lab-v0 --gate GS` → `wrote … GS-REPORT.md (6377 bytes)`, `git diff` 4 insertions, 5 deletions: `Open axes (5 of 10)`, `G-TRACE … 1 of 1 required kinds evidenced | **green**`, `experiment \`rv64gc-m-forms-v3\` | yes`; `check_sexp_schema.py` → references.sexp and gate.sexp conform; `DOSSIER-SCHEMA: ok (272 …)`.
- [x] `.14` a42bc **NO REGRESSION** — `python3 -B scripts/requirement_status.py` → `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 47 planned, 1 implemented; 2 case(s), 1 credited, … 1 of 1 credit record(s) current; 0 drift, 0 finding(s) …)`; `review_div_policy.py` → `DIV-POLICY: satisfied — 10 of 10 legs satisfied; credited by CR-GC-M-1`; `probe_requirement_status.py` `22 tests / 0 failures`, `probe_div_policy.py` `25 tests / 0 failures`, `probe_matched_gpr_property.py --mutation derived-status` `34 tests / 36 failures` (= `derived-status:36` in the gate); `gen_model_book.py --unit rv64gc-lab-v0` → 4 fragments, 2 changed (the references.sexp digest pins); `shasum -a 256`: credit_records.py be844ea99a0b5b36…, check_profile_consistency.sh e1a187fec3171f59…, probe_dossier_qualification.py 7b3acf1009f4f7ef…, references.sexp c06a4aef7fa762e1…, gate.sexp 7b1248c3b8adedac…; `grep -c 'score "'` = 494 (+2 arms); `ls target/doctrine-selftest | wc -l` = 0; the staged focused run before the chain.
- [x] `.14` a43 **ROOT CAUSE** — at a2f4d163: `grep -c '(kind state)' profiles/rv64gc-lab-v0/requirements.sexp` = 4; GS-REPORT.md line 14 reads `0 of 4 \`state\` requirements implemented`; `python3 -B scripts/requirement_status.py` → `47 planned, 1 implemented; 2 case(s), 1 credited`: no state requirement has a case, and a requirement leaves `planned` only through one.
- [x] `.14` a43 **ADDRESSED** — `docs/decisions/decision_state-capture-plan.md` (+ INDEX row): per requirement the GPR-vocabulary witnesses, the controls, the named limitations and the order; `grep -c '^CSR' target/p4-system-14/a43/sail-trace-csr-sample.txt` = 44 (the deferred vocabulary measured present); `grep -c 'a43' docs/tasks/P4-SYSTEM.md` ≥ 6.
- [x] `.14` a43 **NO REGRESSION** — docs-only: `git diff --cached --name-only -- profiles evidence schema scripts` empty; `python3 -B scripts/requirement_status.py` after the edits → the same `47 planned, 1 implemented; … 1 of 1 credit record(s) current; 0 drift, 0 finding(s)`; GS-REPORT.md byte-identical.
- [x] `.14` a43a-1 **ROOT CAUSE** — at 2429670f: `grep -c xlen-forms profiles/rv64gc-lab-v0/guests/run-order.txt` = 0; the GS report reads `0 of 4 \`state\` requirements implemented`; the plan's first case has no program to witness REQ-D-XLEN.
- [x] `.14` a43a-1 **ADDRESSED** — `python3 scripts/derive_rv64gc_expectations.py --parcels --steps 25 xlen-forms.s` → `wrote xlen-forms.expected.sexp (25 steps)`, `check_sexp_schema: ok`; `gen_guests.py --check … guests_rv64gc.rs` → `matches the tracked guests` (169 guests); `cargo test -p semulith-verify every_guest_matches_its_expectations` → `test result: ok. 1 passed`; live Sail: `AGREE on 25 of 25 declared steps` (draft/sail_experiment.py).
- [x] `.14` a43a-1 **NO REGRESSION** — `grep -c xlen-forms evidence/rv64gc-m-forms-v3/dependencies.sexp` = 0 and no touched path appears in that manifest (checked by name); `python3 -B scripts/requirement_status.py` → `47 planned, 1 implemented; 2 case(s), 1 credited, 0 declared, 1 of 1 credit record(s) current; 0 drift`; `bash scripts/check_guest_gen.sh` rc=0 (192 s), EXERCISE-COVERAGE 19/19, INTERACTION-MATRIX ok, DERIVED-COUNTS ok, GATE-REPORT ok, MATERIALS-BILL ok; probes 22/0, 25/0, 34 tests / 36 failures as pinned.

<a id="acceptance-rows-a42ay-to-a42bb"></a>

## acceptance-rows-a42ay-to-a42bb

- [x] `.14` a42bb **ROOT CAUSE** — `ls profiles/rv64gc-lab-v0/retained` → `div-statement.html sail-identity.sexp` (one normative excerpt); target/p4-system-14/a42ay/retention-scope.md: twelve `norm:` spans 2,038 B in the pinned page (`shasum -a 256 .materials/riscv/pinned-v20260120/unpriv/m-st-ext.html` = 85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716), Table 1 1,698 B with tags `br caption col colgroup em p sup table tbody td th thead tr` and attributes `class id style`; `grep -o '(path "profiles/[^"]*")' evidence/rv64gc-m-forms-v3/dependencies.sexp …` → seven pinned profile files, `sources.sexp` and any new `retained/` file not among them; `grep -c "scripts/retain_div_statement.py" evidence/rv64gc-m-forms-v3/dependencies.sexp` = 1 (pinned, so not edited).
- [x] `.14` a42bb **ADDRESSED** — probe-and-seams.log: `python3 -B scripts/retain_m_statements.py --verify` → `{"disposition": "matched", … "byte_size": 6018, "sha256": "bc777ebb97814f7361ececfa0dcfc16074374df2ddfeab71cf6684597681d518"}` rc 0; `--emit | cmp - profiles/rv64gc-lab-v0/retained/m-statements.html` → `re-emission byte-identical`; `python3 -B [-O] scripts/probe_m_statement_retention.py` → `M-STATEMENT-RETENTION: 20 tests / 0 failures / 0 errors` both modes; seams in both modes `input-pins: 20 tests / 1 failures / 0 errors`, `licence-statement` 1, `unique-statement` 1, `closing-span` 1, `span-markup` 3, `table-markup` 4, `style-shape` 1, `table-caption` 1, `retained-bound` 1, `retained-pin` 2 — the gate's table.
- [x] `.14` a42bb **NO REGRESSION** — real-tree.log: `python3 -B scripts/review_div_method.py` → `method satisfied rv64gc-m-forms-v3`, `python3 -B scripts/review_div_policy.py` → `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit`, `python3 -B scripts/requirement_status.py` → `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 48 planned; 2 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; …)`; `bash scripts/check_derived_counts.sh` COUNT DRIFT `claims '1653' self-test arms; the repository has 1655` → re-derived → `DERIVED-COUNTS: ok (3 derived count claim(s) re-derived)`; `bash scripts/check_readme_routes.sh`, `check_requirements.sh` (`RECORD-SCHEMA: ok (20 record file(s) …)`), `check_fixture_fingerprints.sh` (`FIXTURE-FINGERPRINT: ok (1 pinned fingerprint(s) re-derived)`), `check_docpaths.sh` rc 0; `bash -n scripts/check_profile_consistency.sh` rc 0; first focused run `focused: 1 red of 26` — `bash scripts/check_gate_report.sh` rc 1 (GS-REPORT dossier digest `e6777221ab2ed1396f9dfe5153015edafec8401327b8006e956e98d9a9ecf636` vs `49ebeb22c982e3f1413efe0732b4078cc548e40849345fc8cf80efc8356da9cf`) → `python3 scripts/gate_report.py rv64gc-lab-v0 --gate GS` → `wrote profiles/rv64gc-lab-v0/GS-REPORT.md (6768 bytes)`, `git diff --stat` 1 insertion / 1 deletion, `GATE-REPORT: ok (5 generated report(s) in sync with their inputs)`; second focused run rc 0 (focused-checks.json); `git status`: the tool, its probe, the retained file, the regenerated GS report, the gate, documents — no pinned module, evidence byte, Rust or definition file changed.
- [x] `.14` a42bb **ROOT CAUSE** (defect owned mid-slice) — commit.log `❌ PROJECT-SPECIFIC` with the kept log target/profile-consistency-selftest.log (copied to selftest-refusal.log): `PROFILE-CONSISTENCY --self-test: 1154 pass / 2 fail`, `self-test MISS: RED omitted DIV method artifact-selection normal … got rc=1` and `… typed-findings normal …`, each `RuntimeError: synthetic current capture failed: {"status": "refused"}` after `Ran 0 tests in 31.722s` / `59.072s`; `grep -n 'print(json.dumps(dict(status=result.disposition)))' scripts/probe_div_method.py` = 40 (the reason dropped); `grep -n PROCESS_SECONDS scripts/matched_gpr_collector.py` = 24 `PROCESS_SECONDS = 30`, 473 `reference exceeded process time limit` (a pinned module: not changed).
- [x] `.14` a42bb **ADDRESSED** (defect owned mid-slice) — the synthetic capture prints `dict(status=…, reason=result.reason)` and setup checks `.get("status")`; `python3 -B [-O] scripts/probe_div_method.py` → `DIV-METHOD: 21 tests / 0 failures / 0 errors` both modes (probe-method-after.log); repro-setup.log: 12 runs, `artifact-selection` → `DIV-METHOD: 1 tests / 2 failures / 0 errors` and `typed-findings` → `DIV-METHOD: 1 tests / 1 failures / 0 errors` every time, wall 2–4 s at load 6.0–6.7; fresh-exec-latency.log `fresh n=30 median 0.129s p90 0.154s max 0.218s`, `rerun n=30 median 0.021s … max 0.022s`. Cause open; recorded in the knowledge card.
- [x] `.14` a42ba **ROOT CAUSE** — `wc -c docs/tasks/P4-SYSTEM.md` = 117506 at 3cb37d9 (118497 with this leaf opened) against `awk -F'\t' '$1=="docs/tasks/"{print $9}' doctrine/readme_routes.tsv` = 131072; the closed records a42aq–a42aw and the rows a42ar–a42ax measured 24,128 + 32,158 B (move.log); a42ar's move (part 20) covered rows through a42aq only.
- [x] `.14` a42ba **ADDRESSED** — move.log: `live: 118497 -> 63186 B; part 21: 58207 B; records moved: 7, rows: 29 lines / 32158 B`, spans `a42aw 4118 B a5a10aeef0ca982bc441e7d53c837970e29af2cf5665513cde245487b772dae5`, `a42av 3091 B bd888a2b484f584519816b1526e27cb71fbbe89fa4a7e18139f6ca80cf678ca9`, `a42au 4189 B 36570e5b4b56d8feeb5b8ce4514308789ae099fd3f17973f66573bfd71ed95a1`, `a42at 4607 B fc69591d640a0dee666b2c108762aec80b67cb1a9258656e190bf9266514fd88`, `a42as 3203 B 78125b78c295e141faa6ef80b81c963d40a87936b9a694ddf64afc32a2134e26`, `a42ar 3694 B 56aeec4c21acb8a48e047eab87d61150a35a7e061a0ffc0157438d95b3b99797`, `a42aq 1226 B 46a140e48f049d377ce4ca50174700e984f27c2be00a34cda6436773b2c5e47a`, `rows 32158 B 4a784632a06bc4c1347487352eb574820ba96bbc5a820a48150c66954e010e31`, each found exactly once in docs/tasks/archive/P4-SYSTEM-21.md (the script asserts `part.count(b) == 1` and the digest); `grep -c '^\[Record\](archive/P4-SYSTEM-21.md#' docs/tasks/P4-SYSTEM.md` = 7 record stubs and `grep -c '^Rows a42ar–a42ax: ' docs/tasks/P4-SYSTEM.md` = 1 rows pointer.
- [x] `.14` a42ba **NO REGRESSION** — checks.log: `bash scripts/check_docpaths.sh`, `check_tree_claims.sh`, `check_frontier_sync.sh`, `check_readme_routes.sh` (→ `README-ROUTING-CLOSURE: ok (44 governed destination(s))`), `check_task_history.sh`, `check_table_arity.sh`, `check_book_index.sh` rc 0; focused checks rc 0 (focused-checks.json); `git status`: docs/tasks/P4-SYSTEM.md, the new docs/tasks/archive/P4-SYSTEM-21.md, CHANGELOG.md and MEMORY.md only — no code, schema, profile or evidence byte changed.
- [x] `.14` a42ay **ROOT CAUSE** — `grep -n "def credited" -A2 scripts/requirement_status.py` (HEAD 818b873) → 80 `return receipt.get(CREDITED_FIELD) is True`; `grep -n "qualification=False" scripts/retain_div_capture.py` → 143 (the receipt is written once with `qualification` false and never replaced); real tree before: `python3 -B scripts/review_div_policy.py` → `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit` while `python3 -B scripts/requirement_status.py` → `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 48 planned; 2 case(s), 0 credited, 0 declared; …)` — nothing could credit; `grep -c "scripts/records_sexp.py" evidence/rv64gc-m-forms-v3/dependencies.sexp` = 1 and `grep -c "scripts/record_catalog.py" …` = 1 (the records reader is a pinned child; `records_sexp.form_to_dict` raises `not a record form` for any head but requirement / obligation / unit / category-need, so a `credit` kind cannot go through it); `ls profiles/rv64gc-lab-v0 | grep -c credits` = 0; design.md, smoke-reader.log over the real pins: `CR-GC-M-1 current []`, `CR-GC-M-lapsed lapsed ['measured pin evidence/rv64gc-m-forms-v3/measured-experiment.sexp: SHA256 or size differs']`.
- [x] `.14` a42ay **ADDRESSED** — `python3 -B scripts/check_sexp_schema.py target/p4-system-14/a42ay/smoke/profiles/rv64gc-lab-v0/credits.sexp target/p4-system-14/a42ay/credits.schema.sexp` → `check_sexp_schema: ok — … conforms to credits.schema.sexp`; `python3 -B [-O] scripts/probe_requirement_status.py` → `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors` both modes (probe-status.log; the first run `22 tests / 0 failures / 1 errors` — the other-profile fixture pinned a policy file that profile never had — fixed in the fixture, not the reader), seven seams each `1t/1f/0e rc=1` in both modes (seams-status.log: credit-pending, qualification-word, ignore-drift, skip-supersession, unresolved-closes, argument-optional, unknown-case-credit); `python3 -B [-O] scripts/probe_div_policy.py` → `DIV-POLICY-PROBE: 25 tests / 0 failures / 0 errors` both modes, eight seams `1t/1f/0e` (seams-policy.log, credit-any included); real tree (real-tree.log): `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `CREDIT-RECORDS: rv64gc-lab-v0: 0 credit(s), 0 current, 0 lapsed; records read and authenticated, nothing granted` rc 0, `python3 -B scripts/requirement_status.py` → `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 48 planned; 2 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift, 0 finding(s); …)` rc 0, `python3 -B scripts/review_div_policy.py` → `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit` rc 0.
- [x] `.14` a42ay **NO REGRESSION** — `bash scripts/check_requirements.sh` first → `RECORD-SCHEMA: REFUSED — the check does not discriminate (self-test failed).` with `--self-test` (record-schema-selftest.log) naming `ValueError: no reviewed token example: credits.sexp/credit/date: ^20[0-9]{2}-[0-9]{2}-[0-9]{2}` ×4 and `wrong reason (no FAILED (failures=96))`; after two reviewed examples and the census 25 / 100: token-facets.log `python3 [-O] … GREEN: rc=0 Ran 7 tests OK`, `loose-end: rc=1 … FAILED (failures=105)`, `ignore-pattern: rc=1 … FAILED (failures=606)`, `fullmatch: rc=1 … FAILED (failures=1)` in both modes, `bash scripts/check_requirements.sh --self-test` → `RECORD-SCHEMA --self-test: 70 pass / 0 fail` rc 0 and `bash scripts/check_requirements.sh` → `RECORD-SCHEMA: ok (20 record file(s) validate and agree with their profile; the Rust graph checker accepts the examples bundle)` rc 0; `bash scripts/check_dossier_schema.sh` → `DOSSIER-SCHEMA: ok (271 __SKIPPED__ 3 (baseline.sexp, portability.sexp, sail-identity.sexp))` rc 0; `bash knowledge-map/scripts/check_knowledge_map.sh` rc 0 after regeneration; first focused run (focused-and-commit.log) `focused: 1 red of 26` — `bash scripts/check_readme_routes.sh` rc 1 `OVER CEILING schema/: 25 files > 24`, `OVER CEILING docs/decisions/: part docs/decisions/INDEX.md` (`wc -c docs/decisions/INDEX.md` = 16537; `git ls-tree -r -l HEAD schema/` = 24 files / 135,259 B; `git show HEAD:docs/decisions/INDEX.md | wc -c` = 16127) — then after the re-derivation `bash scripts/check_readme_routes.sh` → `README-ROUTING-CLOSURE: ok (44 governed destination(s))` rc 0 and `bash scripts/check_registry_mirror.sh` rc 0; focused checks rc 0 on the second run (focused-checks.json); `wc -c` docs/toolbox/div-evidence.md 12706 (ceiling 16384), CHANGELOG.md 52523 (ceiling 65536); `git status`: the new reader and schema, five consumers/probes, two gates, documents — no pinned module, no evidence byte, no profile catalogue (no `credits.sexp`), no Rust file changed.

