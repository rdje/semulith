# P4-SYSTEM ordinary history — part 25

Ordinary, directly readable task history: the complete records of the closed `.14` units
a43a-3, a43b-2a, a43b-2b and a43b-2c, and the acceptance rows of the same units,
retained verbatim from `docs/tasks/P4-SYSTEM.md` as staged for `SEMULITH-P4-0332` on top of commit `2988d6a2bfc613d0b6be0677e785c7b42730214a`
(5 contiguous spans, in source order, one anchor each). The live tree keeps one
pointer per record and one per row span; the records a44-2b … a43a-2f and their rows are in part 24,
the earlier ones in parts 13–23. Relative links inside the retained text are written from `docs/tasks/`, their
original base. No seal, reader or inverse map is involved: moving closed records verbatim into an ordinary archive
part is the task family's standing mechanism (decision_containment-reset, 2026-10-21); a43b-2e, SEMULITH-P4-0332.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a43b-2c | 3103 | `c31a589e5fe6f1dd73ff3bbb51368e37f4e1ca86cadbe699729b618190d72ea6` |
| record a43b-2b | 7082 | `97bf1e9df7238099f949287ace27d04c252d94ff50862e04b40628f8376b82ab` |
| record a43b-2a | 7371 | `9051f44ecc5ef0a1b97a9eaa2e2d08aa209182e878d918d2b940edeed0b3a390` |
| record a43a-3 | 3300 | `2c68a596c77043ed913e5749454a1d6b7a8b24a073b28267725647b0eaf3efb1` |
| acceptance rows a43a-3–a43b-2c | 7401 | `6d33821484a6a96352f77126661afac72fff290286168dddbec23b85bb1a3246` |

From the repository root:

```
shasum -a 256 <(sed -n '<first>,<last>p' docs/tasks/archive/P4-SYSTEM-24.md)   # a span, by its line range
```

<a id="a43b-2c"></a>

### .14 a43b-2c / SEMULITH-P4-0330: v5 and xlen-v2 declared — the control the case's own, the predeclaration otherwise identical (completed)

The window's re-captures, declared by a44-3's procedure, both in one commit. `evidence/rv64gc-m-forms-v5/case.sexp` is
v4's declaration with the new id and the control declared — `wrong-quotient`, "Predeclared target: wrong quotient must
diverge." (true for M); `evidence/rv64gc-xlen-forms-v2/case.sexp` is xlen-v1's with `truncated-address`, "Predeclared
target: the address truncated to 32 bits must diverge." (its control's reason already said so). Each was rendered by
`matched_gpr_case.render`, every field but the id and the control equal to its predecessor's
(target/p4-system-14/a43b-2c/case-files.txt). The prepared inputs are case-independent: `prepare_div_inputs.py --show
--case` reported each predecessor's four pins byte for byte, `--write` created them, `--verify` re-derived them, and
`cmp` holds all eight identical to v4's and xlen-v1's. `capture_div.py --declare --case` emitted three declarations
each (v5: planned 16,915 B, dependencies 15,166 B with 67 children, authorities 17,721 B; xlen-v2: 14,952, 15,173 and
17,755 B), written exclusively from the output's `files` map and committed here — this commit is the declaration commit
a43b-2d names. **The predeclaration changed only what was declared:** with the id substituted, v5's planned record
differs from v4's in one atom, the dependency manifest's digest (the manifest pins the edited producer and the new case
file), and xlen-v2's from xlen-v1's in three — that digest, the control-run id (`wrong-quotient` → `truncated-address`)
and the control prose (planned-vs-predecessor.txt). The literal guard holds on both real records (no prose outside the
case file and the neutral set; "quotient" absent from xlen-v2's). The case probe's retained-control check, written at
a43b-2b, is live: both records equal their declarations, and xlen-v2's control id altered fails it naming both values
(restored byte-exact; control-check-red.txt). The evidence family's fifth re-derivation
(`decision_evidence-family-two-cases.md`, Addendum a43b-2c): 133 files / 80 MiB (health 130 / 70 MiB); six cases hold
at most 82,972,672 B (`retention_limits()`), 105 files present at declaration; `evidence/README.md` compressed to hold
both rows (3,795 B of 4,096). `REQUIREMENT-STATUS: … 48 planned; 6 case(s), 0 credited, 2 declared`. Re-stated: the
input probe's census and case tables, the case probe's planned population, the property probe's case ids, the status
probe's rows and counts. Frozen until the captures: each case's 67 manifest children (36 scripts, the definitions, the
policy, the profile records and schemas) and the 13 authority views (`capture_div.VIEW_PATHS`, `requirements.sexp` and
`references.sexp` among them) — XTASK.13's next slice, taken at the 5:1 turn before a43b-2d, must touch none of them.
Book: the prepared-inputs page (the six-case envelope; its single- and two-case figures stale since a44-3) and the
status page. Next: XTASK.13 slice b2, then a43b-2d.

<a id="a43b-2b"></a>

### .14 a43b-2b / SEMULITH-P4-0329: the one pinned edit — the control declared per case, CSR-SET's second-method vocabulary, both credits retired (completed)

The window's pinned-edit commit, as a43b-2a designed it (`decision_producer-debt-paid-before-the-next-case.md`,
Implemented). **D1.** The control form of `schema/matched-case.sexp` gains optional `id` and `statement`;
`matched_gpr_case.py` reads them (absent → `None`) and renders them only when present, so the four retained declarations
render to their own bytes (render identity 4 of 4) and a declaration carrying every new field round-trips;
`matched_gpr_property.py` carries `control_id`/`control_statement`; `capture_div.py:330,337` emit them, and
`prepare_capture` refuses by name a case declaring neither ("case … declares no control id/statement: a declaration older
than a43b-2b is history, not a capture input"). `grep -c 'wrong-quotient\|quotient must' scripts/capture_div.py` = 0.
**D2.** Two optional case forms: `second_method` (one of the policy's four kinds as a token, two or more unique
producers, one or more common inputs, what is independently derived) and `adversarial` (one or more properties, the
failure mode; the reader refuses an adversarial property the case does not declare). The risk-method leg of
`review_div_policy.py` reads them from the case's `case.sexp` structurally, as it reads the planned record (the case
reader validates the file at preparation and the manifest pins it; absent → undeclared), and judges a declaration at
any risk by five one-line conditions against the record's graph: (1) both forms, the kind named; (2) two or more record
producers with distinct versions; (3) every pair a recorded `producer_pair` whose shared inputs are exactly the declared
common inputs; (4) no pair recorded `shared` and the independent derivation named, reported beside the recorded ancestry
with no independence credit; (5) the adversarial properties declared in the capture and its baseline `AGREE`. Refined
from the design: (4) refuses a `shared` pair (a value the schema's assessment vocabulary holds), and a low- or
medium-risk declaration is judged by all five. Undeclared keeps today's meaning; no retained case declares the forms.
**D3.** `probe_div_command.py`, the probe that plans in copies, holds the guard: a unique-token control planned verbatim,
and every prose string of the planned record from the case file or the reviewed `NEUTRAL_PROSE` — the five producer
strings the a43b-2a audit found neutral (measured on v4's and xlen-v1's retained planned records: of the producer's own
prose, only the M control statement was case-specific). `probe_matched_gpr_case.py` maps the two fields and holds a
declared control equal to its retained planned record (live from a43b-2c, the first declarations carrying it).
**Found while measuring, repaired in the slice.** (a) Between the edit and the v5/xlen-v2 declarations no case can be
planned, and five probes planned history — `DIV-COMMAND: 19 tests / 7 failures / 4 errors`, `DIV-CAPTURE-RETENTION: 11
tests / 10 failures`, `DIV-METHOD` a setUpClass error, `DIV-AUTHORITIES` one failure, each the new refusal
(target/p4-system-14/a43b-2b/before/*.d1.log): their runtime copies now declare a control (`declare_control`: the
historical words, true for the M-family cases), and the command probe's two in-process arms assert the real tree's
history refused by name — its regeneration check moved into the copy; the offline evaluation's positive branch had
been unreachable since v2's invalidation (2026-10-22). (b) The method review detected `stale` by regenerating, so the
history the producer refuses read `refused` (before/method-without-route.txt, both cases), which the policy review
blocks on (exit 1) — against the 2026-10-22 ruling. On a refused preparation it now re-checks the pins of the
declaration route (the case file, then its schema) on the capture's own manifest, read through the measured record's
`dependency-manifest` pin; the first moved stops it `stale`, and a refusal with nothing moved stands. A walk over every
pinned input was ruled out by measurement: one is 97,811 B, above the 64 KiB snapshot bound. Knowledge card
`a-producer-refusal-hides-staleness-detected-by-regeneration.md`. (c) The first whole check measured `PROFILE-CONSISTENCY
--self-test: 1218 pass / 6 fail` (selftest-1.log; no EPERM), three misses in both modes: the property probe's
`derived-status` loss is status-dependent and fell 37 → 2 with `REQ-GC-M` `planned`, as at a44-2b (re-pinned, commented;
37 returns with the re-credit); the method probe's `capture-origin` seam target was no longer singular because the
route repeated the measured-record pin — now one helper, `_measured_record`, both paths read; and the policy probe's
real-tree arm predicted a lapsed credit, so it now derives the credits from the live catalogue as it derives the moved
pins from the manifests, holding through the whole window. (d) The commit chain's focused stage refused before the
gate: `RECORD-SCHEMA: REFUSED — the check does not discriminate (self-test failed)` — the schema token-facet probe holds a
closed inventory of anchored patterns, each with a reviewed example, and the five new facets had none
(`no reviewed token example: matched-case.sexp/control/id`). The two new token languages are registered (a control id;
the second method's kind), the inventory 122 → 127, and the measured mutation losses re-pinned in
`check_requirements.rs` — `loose-end` 127 → 132 (one per facet), `ignore-pattern` 738 → 768 (six per facet),
`fullmatch` 1 unchanged, each in both modes; `RECORD-SCHEMA --self-test: 81 pass / 0 fail`.
**The lapse.** `CR-GC-M-2` and `CR-D-XLEN-1` lapsed (`… lapsed: manifest input schema/matched-case.sexp`) and were
retired by removal with `credits.sexp` (both decision records); `REQ-GC-M` and `REQ-D-XLEN` `planned`; the v4 and XLEN
dossier copies and `G-TRACE` rows removed, `G-TRACE` open (owner `P4-SYSTEM.14`); GS `Open axes (4 of 10)`.
`REQUIREMENT-STATUS: … 48 planned; 4 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift`; both
cases `DIV-POLICY: invalidated — 8 of 10 legs satisfied; … invalidated by schema/matched-case.sexp: SHA256 differs; no
qualification credit` (exit 0); the method `stale` (110,209 and 105,395 B charged, each predicted by the probe from its
manifest). Re-stated: the status probe (48 / 0), the dossier probe (no record qualifies), the method probe's real-tree
arm. Counts: DIV-COMMAND 20 tests (seams `control-id-literal`, `control-statement-literal`), DIV-METHOD 22 (seam
`stale-route`), DIV-POLICY-PROBE 33 (seams `both-forms`, `distinct-versions`, `recorded-common`, `shared-pair`,
`adversarial-executed`), each new seam one failure; `check_profile_consistency.rs` mirrors them. Books: the unit book's
policy, method, status, capture-plan and division pages and its fragments; three toolbox rows, stale since v3 (21 and
25 tests, eight seams, the capture CLI's default), made current. Next: a43b-2c, v5 and xlen-v2 declared.

<a id="a43b-2a"></a>

### .14 a43b-2a / SEMULITH-P4-0328: the lapse window that opens CSR-SET, designed — the control declared per case, the high-risk vocabulary, the order (completed)

Documentation only, as a44-1 was for ruling B, on `decision_producer-debt-paid-before-the-next-case.md`'s rule: every
pinned file the window moves, every probe and count that moves with it, the order, before the first pinned edit. The
inventory is target/p4-system-14/a43b-2a/inventory.md (read-only, taken on 7f1b8059; its anchors re-checked at b7420b1b by
`grep -n`: `capture_div.py:330` `control_run … id="wrong-quotient"`, `:337` `control="Predeclared target: wrong quotient
must diverge."`, `schema/matched-case.sexp:36` the control construct, `matched_gpr_case.py:74,90,120`,
`review_div_policy.py:34,74,184,276–277`, `probe_div_capture_inputs.py:37–38`, `review_div_method.py:52`,
`doctrine/readme_routes.tsv:488`). The audit of the knowledge card, run over every string `_planned_record` emits
(`capture_div.py:279–345`), finds the two control literals and nothing else case-specific; `M_FORMS_CASE_ID`
(`matched_gpr_property.py:32`) is a probe-selection constant naming a historical case, never emitted, and stays.
**D1 — the control declared per case.** The control construct gains `id` (pattern `^[a-z0-9][a-z0-9-]*\Z`) and `statement`
(min-length 1), `(optional yes)` in the schema and required by the producer: the four retained declarations (v2, v3, v4,
xlen-v1) are retained bytes the probes and reviews still read and cannot gain fields, so a required field would refuse each
of them; `capture_div.py` refuses by name to plan a case whose control lacks either, so no case planned after the window
falls back to a literal. `matched_gpr_case.py` reads them (absent → `None`) and renders them only when present, so the
retained declarations still render to their own bytes (a44-2a's identity test); `matched_gpr_property.py` carries
`control_id`/`control_statement`; `capture_div.py:330,337` emit them. Rejected: a second schema — two constructs for one
meaning and a version branch in every reader, for two fields. Values: v5 `wrong-quotient` with v4's statement (true for
M); xlen-v2 `truncated-address` with "Predeclared target: the address truncated to 32 bits must diverge." (its declared
`reason` already says so).
**D2 — the high-risk vocabulary, declared in the case and judged by the policy review.** Two more optional `case` fields in
the same schema move: `second_method` — `kind`, one of the policy's four named methods as a token
(`independent-exact-expectation`, `bounded-exhaustive-check`, `source-grounded-invariant-check`,
`qualified-hardware-observation`; the policy's text stays the authority), `producer_ids` (at least two, unique),
`common_input_ids` (at least one) and `independently_derived` (non-empty) — and `adversarial` — `property_ids` (at least
one) and `failure_mode` (non-empty). The review takes risk from the catalogue (`review_div_policy.py:184`) and reads the
declaration from the case file its own manifest pins, so the method review's currentness authenticates it; no record
schema moves. For high or critical risk, `risk-method` is satisfied only when all five hold, the failing one named in the
cell: (1) both forms are declared; (2) the declared producers are producers of the measured graph with pairwise distinct
versions — two wrappers around one producer share a version (`expected` and `expected-mutant` both carry the author's
digest, `capture_div.py:286–291`) and are refused; (3) every pair of them is a recorded `producer_pair` and
`common_input_ids` equals the intersection of those pairs' `shared_input_ids` — "the producers and common inputs
recorded", checked against the record, not restated; (4) `independently_derived` is reported beside the recorded pair's
assessment and earns no independence credit (today `not-examined`: "Unexamined comparator ancestry earns no independence
credit"); (5) every adversarial property is a declared property of the capture and its baseline AGREEs — the adversarial
case executed and matched, not only named. Low and medium risk keep today's meaning; a declaration there is judged by
(2)–(5), never ignored. CSR-SET's own declaration is written at its unit: `independent-exact-expectation`, producers
`expected` and `reference`, common inputs `guest-source` and `dependency-manifest` (the pair's recorded shared inputs),
adversarial the refused `csrrw` to mhartid and `mscratch` refused from S (a43b-1's witnesses), failure mode "a forbidden
CSR write or access commits its destination or another architectural side effect". Not widened: the cell vocabulary.
**D3 — the guard.** The capture-input probe asserts, for each case declaring the fields, that the planned record's
control-run id and control prose equal the declaration's, plus a synthetic arm (unique-token id and statement → a planned
record carrying exactly those tokens and no string outside the case file and the producer's neutral set), fired RED by
restoring either literal in a scratch copy of the producer; the policy probe gains one arm per condition of D2, each with
its seam, each fired RED, and a CSR-SET-shaped synthetic declaration.
**D4 — the order (the a44 pattern).** a43b-2b: D1–D3 in one commit; `CR-GC-M-2` and `CR-D-XLEN-1` retired by removal
(recorded in their decision records); `REQ-GC-M`, `REQ-D-XLEN` `planned` (48 / 0); the v4 and xlen-v1 dossier copies and
`G-TRACE` rows removed; GS regenerated. a43b-2c: `rv64gc-m-forms-v5` and `rv64gc-xlen-forms-v2` declared (D1's fields;
prepared inputs byte-exact from v4 / xlen-v1; three declarations each, committed); the evidence family 89 → 133 files
(registry row, `FAMILY_FILES`, `TOTALS`, `BUDGETS`). a43b-2d: each captured exactly once on a quiet host (a43a-2e's
script), its three traces `cmp`-identical to v4's / xlen-v1's; `RETAINED_CAPTURES` rows moved; both reviews 10 of 10.
a43b-2e: `CR-GC-M-3`, `CR-D-XLEN-2` through the crediting act; statuses 46 / 2; dossier copies and `G-TRACE` rows. Then
a43b-3: CSR-SET declared on the clean producers. **D5:** each count above is re-measured by the slice that moves it (the
family's files and bytes, REQUIREMENT-STATUS and CREDIT-RECORDS, the policy, status and dossier probes' predictions,
PROFILE-CONSISTENCY's probe loss counts, the model book's pages and fragment digests); none is carried by hand. Risk named:
a field CSR-SET later needs and D2 lacks is a second lapse, hence D3's CSR-SET-shaped declaration.
Containment, same unit: the closed records a44-2b … a43a-2f and their 33 acceptance rows moved verbatim into
[`archive/P4-SYSTEM-24.md`](archive/P4-SYSTEM-24.md) (the a42ba mechanism; 11 records and one row span, each span's SHA256
in the part's table); this file 129,223 → 93,927 B of 131,072 before this record; a43a-3 stays live (the design cites it).
`CHANGELOG.md` sharded ahead of its 65,536 B ceiling (at 64,028 B): 15 entries into `docs/changelog/shard-0422.md`, the head
48,866 B. `LIVE_STATUS.md`'s P4 row compacted to states (the file 6,055 B of its 6,144 B ceiling, 24 B of headroom after
this unit's line; now 5,557 B). Found and fixed: the main book's "Read task history" named archive parts 13–19 only — 20–23 had never been added
— and now lists the parts by glob, so it cannot drift again. Next: a43b-2b, the one pinned-edit commit.

<a id="a43a-3"></a>

### .14 a43a-3 / SEMULITH-P4-0327: `REQ-D-XLEN` credited `implemented` — the first `state` requirement (completed)

The crediting act of the state-capture plan's third step, as a44-5 did it for the M case and on the same rulings
(`decision_req-d-xlen-credited-implemented.md`): `CR-D-XLEN-1` in `credits.sexp` — case `rv64gc-xlen-forms-v1`, the
measured record (14,958 B, `d39825b0…`), the receipt (7,055 B, `72413fdf…`) and the policy pinned, retained source
`RVI-RV64I-STATEMENTS`, authority `review`, ten legs, four limitations; `REQ-D-XLEN` `implemented`. Derived:
`REQUIREMENT-STATUS: … 46 planned, 2 implemented; 4 case(s), 2 credited, 0 declared, 2 of 2 credit record(s) current; 0
drift`; `CREDIT-RECORDS: … 2 credit(s), 2 current`; `rv64gc-xlen-forms-v1: DIV-POLICY: satisfied — 10 of 10 legs
satisfied; credited by CR-D-XLEN-1`; both method reviews stay `satisfied` after the status edit (the semantic digests
normalize the status, as at a44-5). The dossier holds the case's measured record form for form beside v4's, both
qualifying (`dossier_qualification` → `[]`), and `gate.sexp` its `G-TRACE` evidence row; the G-STATE and G-OBLIGATIONS
open statements now say what is implemented. GS: G-STATE `1 of 4 state requirements implemented`, G-TRACE both rows
verified, `Open axes (3 of 10)`. Found while building the dossier copy: the measured record's `control` prose ("wrong
quotient must diverge") and control-run id (`wrong-quotient`) are `capture_div.py`'s fixed M literals — pinned by both
captures, so fixing them now would lapse both credits for prose that grants nothing; the credit's limitations name them
with the receipt's M phrase (a43a-2e), and the pattern is a knowledge card
(`docs/knowledge/a-producer-generalized-from-its-first-case-keeps-its-literals.md`). Found by the act: RECORD-SCHEMA
refused it — `MIRROR DRIFT requirements.sexp [REQ-D-XLEN]: field 'implementation_status' differs from the owner's
record` — rule 14 holding the rv64gc mirror to rv64i's `planned` while REQUIREMENT-STATUS derives rv64gc's
`implemented`; the status is now the mirror's own exactly where its profile carries `EVIDENCE_POLICY.md` (every
meaning field still compared), with two arms each shown to discriminate (`80 pass / 1 fail` without the exemption and
with it unconditional; `81 pass / 0 fail`); the condition is asked of `requirement_status.derives_statuses`, never copied
(`decision_mirror-status-is-per-profile.md`). Re-stated, each measured: the
policy probe's XLEN block (credited; a moved pin lapses `CR-D-XLEN-1`), the status probe's real-tree prediction (46 / 2,
the XLEN row), the dossier probe (the XLEN record qualifies); the property probe's `derived-status` loss stays 37. The
model book's status and policy pages, and its fragments' input digests, regenerated. Decided on the director's question
(2026-10-29): the literals are removed in one planned lapse window that opens CSR-SET, before any further case is
declared — the control declared per case, CSR-SET's high-risk predeclaration vocabulary in the same pinned-schema move,
v4 and xlen-v1 re-captured once as v5 and xlen-v2 (traces byte-identical), both re-credited
(`decision_producer-debt-paid-before-the-next-case.md`). Next: a43b-2, that window, designed before its first pinned edit.

<a id="acceptance-rows-a43a-3-to-a43b-2c"></a>

## acceptance-rows-a43a-3-to-a43b-2c

- [x] `.14` a43a-3 **ROOT CAUSE** — REQ-D-XLEN's ten legs were satisfied and no record credited them: at 7ff63fef `python3 -B scripts/review_div_policy.py --every-retained` `rc=0` → `rv64gc-xlen-forms-v1: … no qualification credit`, `python3 -B scripts/requirement_status.py` → `47 planned, 1 implemented; 4 case(s), 1 credited`.
- [x] `.14` a43a-3 **ADDRESSED** — `python3 -B scripts/credit_records.py --profile rv64gc-lab-v0` → `2 credit(s), 2 current, 0 lapsed`; `python3 -B scripts/requirement_status.py` `rc=0` → `46 planned, 2 implemented; 4 case(s), 2 credited, 0 declared, 2 of 2 credit record(s) current; 0 drift`; `--every-retained` `rc=0` → `credited by CR-D-XLEN-1`; both dossier records `dossier_qualification` → `[]`; `grep -c 'rv64gc-xlen-forms-v1' profiles/rv64gc-lab-v0/gate.sexp` = 1; GS G-STATE → `1 of 4` state requirements implemented; `RECORD-SCHEMA --self-test: 81 pass / 0 fail`, `RECORD-SCHEMA: ok`; with `derives_statuses` single-sourced, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors` both modes and its seven seams `1 tests / 1 failures` each.
- [x] `.14` a43a-3 **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1208 pass / 0 fail`, traced (`ls target/p4-system-14/a43a-3/eperm | wc -l` = 0), the whole check `rc=0` on a quiet host; `DIV-POLICY-PROBE: 27 tests / 0 failures / 0 errors`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures / 0 errors`, `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures / 0 errors`, each in both modes; `MATCHED-GPR-PROPERTY: 35 tests / 37 failures` under `derived-status` (unchanged); `MATERIALS-BILL: ok`, `GATE-REPORT: ok`, `UNIT-BOOKS: ok`; `DERIVED-COUNTS: ok` (1700 arms); the staged prechecks and the commit gate (chain log).
- [x] `.14` a43b-2a **ROOT CAUSE** — the window had no design before its first pinned edit, and its two files sat at their ceilings: `grep -n 'wrong-quotient\|quotient must diverge' scripts/capture_div.py` → lines 330 and 337 (the M literals both captures pin); `grep -n 'no declaration vocabulary' scripts/review_div_policy.py` → line 34; `wc -c` → `docs/tasks/P4-SYSTEM.md` 129223 of 131072, `CHANGELOG.md` 64028 of 65536.
- [x] `.14` a43b-2a **ADDRESSED** — the design (D1–D5) recorded here, in `decision_producer-debt-paid-before-the-next-case.md` and on the unit book's policy page; target/p4-system-14/a43b-2a/move.log → `records 11, row spans 1 (33 rows)`, each span's SHA256 re-checked in part 24, and independently 224 of 224 nonblank removed lines present in part 24 (removed-lines.txt); `python3 -B scripts/shard_history.py --max-bytes 49152` → `66 entries before == 51 kept + 15 moved, order and bytes exact`, `head: 64028 -> 48866 bytes` (shard.log); `bash scripts/check_changelog_shards.sh` → `SHARD-FREEZE: ok (424 shard row(s) frozen, 2 heads + shards append-only, exactly partitioned)`.
- [x] `.14` a43b-2a **NO REGRESSION** — documentation only: `git diff --cached --name-only | grep -vE '\.md$'` → `docs/changelog/SHARDS.sha256` alone (the manifest the sharder regenerates); the focused stage and the commit gate (target/p4-system-14/a43b-2a chain log).
- [x] `.14` a43b-2b **ROOT CAUSE** — the producer emitted the first case's control words: `git show 715ed26e:scripts/capture_div.py | grep -n 'wrong-quotient\|quotient must'` → lines 330 and 337, and `review_div_policy.py:277` read every high-risk case `second method and adversarial case undeclared` (target/p4-system-14/a43b-2b/before/literals-at-head.txt); once the producer refused history, the method review read both retained cases `refused` (before/method-without-route.txt: `refused | case rv64gc-m-forms-v4 declares no control id/statement …`) and five probes went red on the refusal alone (before/*.d1.log: `DIV-COMMAND: 19 tests / 7 failures / 4 errors`, `DIV-CAPTURE-RETENTION: 11 tests / 10 failures`).
- [x] `.14` a43b-2b **ADDRESSED** — `grep -c 'wrong-quotient\|quotient must' scripts/capture_div.py` = 0; render identity 4 of 4 retained declarations; `python3 -B scripts/review_div_method.py --case rv64gc-m-forms-v4` `rc=1` → `stale | schema/matched-case.sexp: SHA256 differs | 110209` (xlen-v1 105395); `python3 -B scripts/review_div_policy.py --every-retained` `rc=0` → both `invalidated — 8 of 10 legs satisfied; … no qualification credit`; `python3 -B scripts/requirement_status.py` → `48 planned; 4 case(s), 0 credited, 0 declared, 0 of 0 credit record(s) current; 0 drift`; `DIV-POLICY-PROBE: 33 tests / 0 failures / 0 errors`, `DIV-METHOD: 22 tests / 0 failures / 0 errors`, `DIV-COMMAND: 20 tests / 0 failures / 0 errors`, each new seam `1 failures / 0 errors` (`distinct-versions` one assertion over high and low risk).
- [x] `.14` a43b-2b **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1224 pass / 0 fail` (target/p4-system-14/a43b-2b/selftest.log; the first run's `1218 pass / 6 fail`, selftest-1.log, measured and repaired: `derived-status` 37 → 2, the `capture-origin` target, the policy real-tree prediction), traced: `ls target/p4-system-14/a43b-2b/eperm | wc -l` = 0; the whole check `rc=0` → `PROFILE-CONSISTENCY: ok (5 profile dossier(s) internally consistent)` on a quiet host (wait.log); `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DOSSIER-QUALIFICATION-PROBE: 6 tests / 0 failures`, `DIV-AUTHORITIES: 19 tests / 0 failures`, `MATCHED-GPR-CASE: 8 tests / 0 failures`; `cargo fmt --all -- --check` `rc=0`, `cargo clippy -p xtask --all-targets -- -D warnings` `rc=0`; `RECORD-SCHEMA --self-test: 81 pass / 0 fail` and `RECORD-SCHEMA: ok (25 record file(s) …)` after the focused stage's refusal (record-schema-selftest.log); `DERIVED-COUNTS: ok`; the staged prechecks and the commit gate (chain log).
- [x] `.14` a43b-2c **ROOT CAUSE** — the re-captures had no declarations: at ac08c9e1 `ls evidence` held four case directories (v2, v3, v4, xlen-v1), each refused by the producer since a43b-2b (`case … declares no control id/statement`), and the family was bounded for four (`sed -n 488p doctrine/readme_routes.tsv` → 89 files, 67108864 B).
- [x] `.14` a43b-2c **ADDRESSED** — `python3 -B scripts/prepare_div_inputs.py --verify --case rv64gc-m-forms-v5` `rc=0` and the same for xlen-v2; `cmp` 8 of 8 prepared inputs equal to the predecessors'; the planned records' diff against their predecessors with the id substituted: 1 atom (v5) and 3 atoms (xlen-v2), target/p4-system-14/a43b-2c/planned-vs-predecessor.txt; `python3 -B scripts/requirement_status.py` → `48 planned; 6 case(s), 0 credited, 2 declared … 0 drift`; `retention_limits()` → 133 slots, 82972672 B; `DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors` both modes; the control check fired RED (`MATCHED-GPR-CASE: 8 tests / 1 failures`, control-check-red.txt) and restored (`8 tests / 0 failures`).
- [x] `.14` a43b-2c **NO REGRESSION** — `PROFILE-CONSISTENCY --self-test: 1224 pass / 0 fail` (target/p4-system-14/a43b-2c/selftest.log), traced: `ls target/p4-system-14/a43b-2c/eperm | wc -l` = 0; the whole check `rc=0` → `PROFILE-CONSISTENCY: ok (5 profile dossier(s) internally consistent)` on a quiet host (wait.log); `MATCHED-GPR-PROPERTY: 35 tests / 0 failures`, `REQUIREMENT-STATUS-PROBE: 22 tests / 0 failures`, `DIV-METHOD: 22 tests / 0 failures`, `DIV-POLICY-PROBE: 33 tests / 0 failures`, `DIV-COMMAND: 20 tests / 0 failures`; `README-STABILITY: OK`; the staged prechecks and the commit gate (chain log).

