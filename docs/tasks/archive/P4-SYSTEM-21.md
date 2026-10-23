# P4-SYSTEM ordinary history — part 21

Ordinary, directly readable task history: the complete records of the closed `.14` units
a42aq–a42aw and the acceptance rows of the closed units a42ar–a42ax, retained verbatim from
`docs/tasks/P4-SYSTEM.md` at commit `3cb37d9e43146a345aa4628490ae0b8f745f7a30` (eight contiguous spans, in source
order, one anchor each). The live tree keeps one pointer per record and one for the rows;
the rows through a42aq are in part 20 and the earlier records in parts 13–19. Relative links
inside the retained text are written from `docs/tasks/`, their original base. No seal, reader
or inverse map is involved: moving closed records verbatim into an ordinary archive part is the
task family's standing mechanism (decision_containment-reset, 2026-10-21); a42ba,
SEMULITH-P4-0294.

| Span | Bytes | SHA256 |
| --- | --- | --- |
| record a42aw | 4118 | `a5a10aeef0ca982bc441e7d53c837970e29af2cf5665513cde245487b772dae5` |
| record a42av | 3091 | `bd888a2b484f584519816b1526e27cb71fbbe89fa4a7e18139f6ca80cf678ca9` |
| record a42au | 4189 | `36570e5b4b56d8feeb5b8ce4514308789ae099fd3f17973f66573bfd71ed95a1` |
| record a42at | 4607 | `fc69591d640a0dee666b2c108762aec80b67cb1a9258656e190bf9266514fd88` |
| record a42as | 3203 | `78125b78c295e141faa6ef80b81c963d40a87936b9a694ddf64afc32a2134e26` |
| record a42ar | 3694 | `56aeec4c21acb8a48e047eab87d61150a35a7e061a0ffc0157438d95b3b99797` |
| record a42aq | 1226 | `46a140e48f049d377ce4ca50174700e984f27c2be00a34cda6436773b2c5e47a` |
| acceptance rows a42ar–a42ax | 32158 | `4a784632a06bc4c1347487352eb574820ba96bbc5a820a48150c66954e010e31` |

From the repository root:

```sh
cat docs/tasks/archive/P4-SYSTEM-21.md
```

<a id="a42aw"></a>

### .14 a42aw / SEMULITH-P4-0291: capture the m-forms case (completed)

Owned on clean 4af5a68. `rv64gc-m-forms-v3` was declared (a42au, re-emitted a42av) and the evaluation
binds the case it is asked to; the pinned Sail binary was present with the retained identity's
digest. The first capture (a42am) had been invoked by a scratch script in its evidence directory
(target/p4-system-14/a42am/capture-once.py) that published the measured record and the derived
receipt by hand; no tracked script wrote `div-capture-verification-v1` (reproduce.log). Built:
`scripts/retain_div_capture.py` — preflight without a process (the case reviewed and pinned, every one
of the twelve observation names and two result names absent, the three declarations on disk equal to
their regeneration, the reference binary's bytes carrying the retained identity's digest through the
public anchored reader, the declaration commit a 40-hex id recorded and never verified: no Git), one
invocation of `capture_div.capture(case_id)` never retried with every reached observation preserved,
and the exclusive publication of `measured-experiment.sexp` and `verification.json` in the a42am
receipt shape with qualification false; `--preflight-only` reports readiness. The probe
`scripts/probe_div_capture_retention.py` runs eleven controls in a copied runtime with the command
probe's synthetic reference — one invocation retains fourteen files and an uncredited receipt; a rerun,
a changed declaration and a changed binary refuse before any process; a failed process preserves its
outputs and publishes an incomplete receipt; an escaped invocation publishes nothing; publication is
exclusive; preflight-only writes nothing; malformed inputs refuse; CLI exit codes; the tool's code
names no Git and launches nothing of its own — with seven seams; gate arms added. Then the capture,
once: preflight `ready` on the real tree (binary 3,801,664 B, digest 16de42a8…, declarations
16,915 / 14,488 / 17,043 B, 14 names absent), one invocation at 2026-10-22T20:04Z: `pending`, complete,
collection recorded, evaluation pending, record valid, all nine findings matched, processes 33523 /
33562 / 33599 exit 0, verdicts AGREE / AGREE / DIVERGE with the control at boundary 12 x15 alone
(0xfffffffffffffffd observed, 0xfffffffffffffffc expected), 85 files authenticated (1,076,834 B),
24,396,002 B charged of 134,217,728; `measured-experiment.sexp` 16,942 B and `verification.json`
published; 21 of 21 files. Defect found by the gate and fixed here (§15): the first commit attempt
was blocked after 50 min by FIXTURE-FINGERPRINT — the receipt pinned its twelve observations under
`path` + `sha256`, which that doctrine resolves relative to the record's own directory, while the
first receipt names repository-root identities under `object`; the probe had held the receipt's
shape to the tool's own output instead of the retained first receipt (the a42au lesson,
`docs/knowledge/a-fixture-must-have-the-real-records-shape.md`). The tool now emits `object`, the
probe holds every key list to the first receipt and asserts no `path`+`sha256` pair, and the published
receipt was re-rendered from its own data with the twelve keys renamed before any commit
(receipt-rerender.log: 6,993 B → 7,017 B, every other field identical; the measured record and the
observations untouched). The offline re-evaluation of the retained bytes with the case named
agrees (`pending valid satisfied`, AGREE AGREE DIVERGE, 25 properties bound, three byte-identical
2,794-byte traces). The family holds all 43 declared files (the index at 3,967 B); `requirement_status`
counts both cases pending and none credited; the inputs and status probes follow; LIVE_STATUS arm total
re-derived 1653. The retained reviews still read the invalidated first case by design: a42ax switches
`RETAINED_CASE_ID`, the measured pins and commits and `review_div_policy.CASE_ID`, makes the method
probe's fixture and the policy probe's real-tree arm follow, and measures the ten legs; the crediting
record for `REQ-GC-M` is a separately owned decision after that. Commit: SEMULITH-P4-0291.

<a id="a42av"></a>

### .14 a42av / SEMULITH-P4-0290: the evaluation binds the case it is asked to (completed)

Owned on clean 1c13a60. The m-forms case was declared, but its capture could not run as the modules
stood: the retained evaluation bound `G.reviewed_case(G.CASE_ID)`, the module constant of
`matched_gpr_property.py` naming the retained case, so capturing `rv64gc-m-forms-v3` would have
bound the retained case's claims against the m-forms record and refused by name — and moving that
constant is an edit to one of the 64 pinned children of every declaration, invalidating the one just
committed while pointing the method and policy reviews at a measured record that does not exist.
Measured first (target/p4-system-14/a42av/reproduce.log): no `case_id` parameter on
`evaluate_retained_unit`, `capture_and_evaluate` or `freeze_review`; the binding module pinned by
the m-forms manifest; the m-forms record refused under the retained case (a42at smoke). Built: the
case is an argument of the callers that know it — `evaluate_retained_unit(..., case_id=…)` (frozen
before any artifact read; an unknown case refuses there), `capture_and_evaluate(..., case_id=…)`
(frozen in the evaluation plan before any process), `matched_gpr_adequacy.freeze_review(...,
case_id=…)` with `MethodReview.case_id`, `capture_div.capture(case_id)` passing the case it prepares;
the method review keeps its own `RETAINED_CASE_ID` outside the pinned modules and passes the case
through; the retained case stays the default everywhere, so every existing caller and fixture is
unchanged (`decision_caller-names-the-case.md`, `answers:`). The m-forms declaration was re-emitted
once over the three edited pinned modules and retained (redeclare.log): the dependency manifest moved
exactly the pins of `capture_div.py` and `matched_gpr_evaluation.py` (64 children unchanged), the
planned record moved only its manifest pin and the collector's, the authority record those four;
every byte apart from the pins is identical and the three files regenerate byte for byte
(`re-declare byte-identical: True 3`). The four prepared inputs are untouched. Probes:
property-evaluation 25 tests / 16 seams (`case-pass-through`; the m-forms case refuses this record's
claims by name, an unknown case refuses before the manifest read), unit-evaluation 30 / 26
(`case-forward`; one capture per fixture, the m-forms case collects then refuses by name, an unknown
case never collects), the method probe's `declaration-binding` seam repointed at the per-case prefix;
every other probe unchanged in count and every seam equal to the gate's table. Real tree unchanged:
status ok with 2 cases / 1 declared, method `stale`, policy `invalidated` rc 0. No capture, receipt or
credit; `REQ-GC-M` planned. Commit: SEMULITH-P4-0290. Next: a42aw — capture the m-forms case
(`--capture --case rv64gc-m-forms-v3`, the pinned binary present with the retained digest), retain
the twelve observations and two results through a tracked receipt writer, switch `RETAINED_CASE_ID`,
the measured pins and `review_div_policy.CASE_ID`, measure the ten legs.

<a id="a42au"></a>

### .14 a42au / SEMULITH-P4-0289: declare the m-forms case (completed)

Owned on clean 830bdce. The m-forms case was reviewed in the binding (a42at) but nothing outside it
could select the case: `scripts/capture_div.py` prepared, declared and captured the one case its
module constants named, `scripts/review_div_capture.py` exercised the loaders over that one guest,
the evidence family was bounded to one case (22 files / 16 MiB, "no permission to grow the family to
another case"), and `scripts/requirement_status.py` refused a case directory whose planned record
exists without a receipt — the state every declared case is in between declaration and capture.
Measured first (target/p4-system-14/a42au/reproduce.log): `--case` unrecognised; `GUEST` a constant;
the family at 22 of 22 files with a declaration adding 7; the status derivation `REFUSED — unreadable
verification receipt` (rc 2) on a declared fixture. Built: `scripts/prepare_div_inputs.py` (tracked:
`--show`/`--verify`/`--write --case <id>`; the guest ELF, the mapped override, the canonical
expectation copy and the one-value control through the public image/dossier/source-value owners;
`--write` exclusive; it reproduces the retained v2 bytes `equal` ×4 before it was trusted,
prepare-tool.log); the four m-forms inputs written and verified (4,440 / 7,609 / 7,937 / 7,440 B);
`capture_div.py` case-parametric (`prefix()`, `CURATED_INPUTS` per case + the shared identity row,
`prepared_inputs()`, `CurrentAuthorities.case_id`, `prepare_capture(case_id)`, `--case`; the retained
constants `PREFIX`/`PREPARED` unchanged, so `review_div_method.py` and the command/method probes are
untouched); `review_div_capture.py` `review(case_id)`, `exercise_loaders(…, case)`,
`exercise_authorities(…, case)`, `guest_path()`, `--case`; `--declare --case rv64gc-m-forms-v3` emitted
and retained the three declarations (16,915 / 14,488 / 17,043 B: 25 properties, the control naming
`form-div`, 64 children) and regenerates them byte for byte (declare-v3.json); the family re-derived
for two cases — index rewritten (53 lines / 3,762 B), registry row 43 files / 32 MiB, health 40 /
28 MiB, index health 3,890 B — in `decision_evidence-family-two-cases.md`; the status derivation
reports a declared case (`declared`, credits nothing, belongs to the profile whose catalogue names its
requirements). Defect found by the tool and fixed here (§15): the status derivation read `property`
forms at the experiment root while every real record nests them under `verification` — both retained
cases loaded with **0 bindings** (probes-fast.log: `0 declared` on the real tree) behind a flat
fixture; fixed, the fixture given the real shape, a real-tree test asserting both cases' bindings,
one entry per case and requirement; lesson in DEV_NOTES, promoted to
`docs/knowledge/a-fixture-must-have-the-real-records-shape.md`. The toolbox execution table crossed
its 16,384-byte per-part ceiling with the new rows (16,436: routes RED in the focused run) and was
partitioned by the family's own mechanism: seventeen DIV-evidence rows moved verbatim to
`docs/toolbox/div-evidence.md`, indexed in TOOLBOX.md. The promoted card was the knowledge family's
31st file against a ceiling of exactly 30 (and 98,585 B against 98,304): re-derived with the numbers in
`decision_knowledge-family-first-rederivation.md` (40 files / 128 KiB, health 34 / 112 KiB) — the
third exact-ceiling family today; the health targets had printed since September. Probes: inputs rewritten over both cases (34
tests; layout seam 6), status 19 / six seams (`declared-credits`), capture-review, authorities,
command, method unchanged in count; the probe stand-ins for the authority review now take the public
signature. Real tree: `requirement_status` ok — 2 cases, 0 credited, 1 declared; method `stale`,
policy `invalidated` rc 0 (the retained case, unchanged). No capture, receipt or credit: `REQ-GC-M`
planned. Commit: SEMULITH-P4-0289. Next: a42av — capture the m-forms case (pinned Sail binary under
target/refs, retained pointers switched to v3, `--capture --case rv64gc-m-forms-v3`, twelve
observations and two results committed, policy legs measured).

<a id="a42at"></a>

### .14 a42at / SEMULITH-P4-0288: one case, many predeclared properties (completed)

Owned on clean 0aabfef. The policy's two pending legs (boundary-fixtures, form-coverage) need one
capture that predeclares every Table 1 row and every M form, and the property binding supported
exactly one property per case: `_records(graph, "property", 1)` in the relation binder, one
statement and one witness in the context, `graph["property"][0]` in the evaluation and the
collector, the policy's control leg reading the first property. Measured first: a record with a
second property is refused (`method requires 1 property records`); the m-forms program has a
matched source-value finding at boundary 12 x15 (`0xfffffffffffffffd`) and no reviewed case
(target/p4-system-14/a42at/reproduce-*.log). Built: `scripts/matched_gpr_property.py` owns a case
table (`reviewed_case`, `reviewed_case_ids`): `rv64gc-signed-div-truncation-v2` keeps its one
property and stays the retained `CASE_ID`; `rv64gc-m-forms-v3` declares 25 properties over
`m-forms.s` (33 boundaries) — the 13 forms once each (`form:<mnemonic>`) and the 12 Table 1 cells
(`table1:<row>`) — each a reviewed RV64 value, with the reviewed words of all 33 boundaries and the
control `form-div` (boundary 12, x15, −3 → −4, the retained case's discrimination); the probe
re-derives every word from the encoding fields and every value from integer arithmetic and Table 1
(33 of 33, 25 of 25; independent-m-forms.log). `PropertyContext` carries 1..64 `PropertyClaim`s with
distinct identities and witnesses and names its control among them; the binding holds the sorted
claims and the control to the case, the relation plan's properties and control witness to the
context, the reviewed words (3 for v2, 33 for v3), and then every predeclared value against the
source derivation the source-value finding already carries (no second read, no arithmetic engine).
`RelationPlan` carries `properties` (1..64, distinct witnesses) and `control_property_id` /
`control_witness`, the comparison witness; the evaluation and the collector build one claim per
declared property (count and obligations bounded before copying); adequacy, the capture command (one
property form per reviewed property, the control_run naming the control, a per-case limitation
line), the method review (`supported_claims`), the capture review (every reviewed value, the guest
path from the case) and the policy review (the control leg reads the control_run's named property;
1..64 properties) read the case table. Both cases bind through the pure API (1 and 25 observed
values); one wrong value and the wrong case refuse (binding-smoke.log). Probes: property rewritten
(34 tests, 35 seams), property-evaluation 24 / 16 (`control-value`; the fixture now declares the
reviewed identity `signed-quotient`), relations 42 / 19 (`property-count`, `witness-unique`), policy
22 / 7 (`first-property`; its fixture gains a control_run), the value-evaluation seam renamed, field
renames in the manifest, evaluation, method and inputs probes; the seam matrix of ten probes in
normal and -O mode: every seam discriminates and every count equals the gate's table
(seams-*.log); gate arms re-measured; the LIVE_STATUS arm total re-derived to 1651. Real tree
after the change: method `stale`, policy `invalidated — 6 of 10 legs … invalidated by
evidence/rv64gc-signed-div-truncation-v2/planned-experiment.sexp: SHA256 differs` rc 0, capture
review pending with 37 modules / 64 children unchanged (reviews-after.log) — the a42as design, no
credit granted or removed, `REQ-GC-M` planned. Decision record
`decision_many-predeclared-properties-one-control.md` (`answers:`), chapters (source-property: the
API and the m-forms section; policy-adequacy; retained-method; prepared-inputs), toolbox rows (a row
for the property probe), KNOWLEDGE_MAP, book decision count 66. Open for the director: only the DIV
statement is a retained normative excerpt; the multiply statements and the Table 1 rows are cited
in the expectations (what the legs read), not retained — a retention slice like a42z for §11.1.1
and Table 1 before the crediting capture is the thorough answer. Commit: SEMULITH-P4-0288. Next:
a42au — a case selector for `capture_div.py` and `review_div_capture.py` (the retained pointer
stays v2 for the method and policy reviews), fresh prepared inputs under `evidence/rv64gc-m-forms-v3/`
(guest.elf, reference-config.json, baseline and control expectations with boundary 12 x15 −3 → −4),
`--declare`, commit; then a42av captures the three runs and switches the retained pointers.

<a id="a42as"></a>

### .14 a42as / SEMULITH-P4-0287: a stale finite method invalidates, it does not lock (completed)

Owned on clean 8385b8d. Director's ruling 2026-10-22 ("let's follow your recommendation"): the
retained case's pinned inputs must not make every commit that touches one of them refused.
`scripts/review_div_policy.py` (unpinned) reports a `stale` finite method as the `invalidated`
disposition with exit 0 — the policy's own word for a changed input ("changes invalidate
dependent evidence", EVIDENCE_POLICY.md "Records, controls and currentness") — and keeps exit 1
for a receipt claiming qualification over an invalidated method and for a refused, unavailable
or unsupported method. The self-test arms that read the real retained case predict its state
from the dependency manifest's pins independently, so they assert `stale` on a moved tree and
`satisfied` on a current one instead of requiring the tree to be frozen. First measurement:
which arms refuse on a stale tree (experiment: one appended comment line on
`scripts/matched_gpr_property.py`, reverted; target/p4-system-14/a42as/stale-experiment.log).
Then the change, the probes, the gate counts, the chapter, the toolbox mirror and a decision
record. REQ-GC-M stays planned; no credit is granted or removed. Measured first: on the moved tree
the method reports `stale` (planned-experiment.sexp: SHA256 differs), the policy `blocked` rc=1,
requirement status ok, and the self-test 1054 pass / 32 fail — DIV-COMMAND 16 arms (two real-tree
tests), DIV-METHOD 14 arms (the GREEN arm and twelve RED arms, three of them rc=0: seams the stale
stop made unreachable), DIV-POLICY 2 (target/p4-system-14/a42as/stale-selftest.log). Built: the
finite method's probe synthesizes a current retained case once per run (current declarations,
three synthetic processes in 1.6 s, the measured experiment persisted, the copy's method pinned to
it; the method reviews it `satisfied`, 85 files authenticated, checker 39), runs its 14 seams
against it and keeps one real-tree arm that asserts `satisfied` or `stale` as the manifest
predicts; the command probe's two real-tree arms predict the same way (regenerated manifest differs
in exactly the moved inputs; the offline evaluation refuses); the policy probe gains `invalidated`
(two tests, the `lock-stale` seam) and its real-tree arm predicts `pending` or `invalidated`.
Matrix on both tree states (target/p4-system-14/a42as/probe-matrix.log): policy 21 tests, six seams
RED; command 19 tests, seven seams 6/1/1/1/2/1/1; method 21 tests, fourteen seams
4/1/4/2/2/1/2/1/3/4/1/1/1/1 — identical in the current and the moved state; on the moved tree
`review_div_policy.py` prints `invalidated — 6 of 10 legs satisfied; … invalidated by
evidence/rv64gc-signed-div-truncation-v2/planned-experiment.sexp: SHA256 differs` rc=0. Decision
record `decision_stale-method-invalidates-not-locks.md` (`answers:`), chapter section, toolbox rows,
gate counts and comments, book decision count. Commit: SEMULITH-P4-0287. Next: ARTIFACT-CLEANUP.25
(due), then a42at — the property binding's many-property case over m-forms.s, now committable while
v2 is invalidated — a42au the v3 declaration, a42av the capture.

<a id="a42ar"></a>

### .14 a42ar / SEMULITH-P4-0286: author the crediting M corpus program (completed)

Owned on clean b469800; the tree's closed acceptance, verification and commit rows through
a42aq (84,165 B / 1,025 LF, SHA256
4d524652fc7ed971b8329a484fb5b95f39abcd2450da23048512c654380a6ca6) moved verbatim into
docs/tasks/archive/P4-SYSTEM-20.md with one pointer per section — the standing mechanism, no
inverse map. The policy measurement named what a crediting capture must predeclare: every
Table 1 row and every M form. profiles/rv64gc-lab-v0/guests/m-forms.s (33 instructions) is
that program: the 13 forms once each with operands that tell each form from its neighbour
(MULW from MUL, DIVW from DIV, REMW from REM, REMUW from REMU, MULHSU from MULH and MULHU),
then the 12 Table 1 cells — division by zero and signed overflow for DIV, DIVU, REM, REMU and
their word forms — each step citing "RVI-M §11.1.2 (Table 1)". Expectations derived on the
explicit-budget parcel route (derive_rv64gc_expectations.py --parcels --steps 33): schema-valid,
byte-identical on --check, every M value equal to an independent arithmetic. Registered in
run-order.txt and the interaction matrix (boundary × boundary), not in the author's owned corpus: the
expected author is one of the 64 inputs the retained case pins, and the first commit attempt showed
that a one-line PARCEL_OWNED_GUESTS registration stales the finite method (DIV-POLICY blocked), so
the program stays an explicitly budgeted guest (--parcels --steps 33) until the author changes with a
fresh capture; guests_rv64gc.rs regenerated, so the verify differential executes it on every commit;
the generated internal-contracts.md fragment regenerated for the matrix change. Live
Sail 0.14: AGREE, 33 declared steps, two traces byte-identical
(target/p4-system-14/a42ar/sail-m-forms.log) — an experiment, not a capture: no case,
predeclaration, receipt or credit names it; REQ-GC-M stays planned. The guest pair put profiles/
8,516 B over its 3 MiB aggregate (3,154,244 B, 526 files) with no health warning possible — the
family had stood above its target since 2026-10-06 — so both aggregates are re-derived by the
registry's reviewed mechanism, as the 2026-10-06 record scheduled: 4 MiB / 800 files, health
3,586,000 B / 684 files below the family, per-part 65,536 unchanged
(docs/decisions/decision_profiles-family-corpus-second-rederivation.md); the director's
alternative, the aggregate ungoverned as for docs/tasks/, is named there and applies on the
director's word only. Verification: guest-gen,
interaction-matrix and exercise-coverage rc=0; make check rc=0 (cargo test 173 + 17 + 287 passed, 0 failed; fmt and clippy clean); focused checks
rc=0; seven books. The second commit attempt was refused by the gate's own PROFILE-CONSISTENCY
self-test (REFUSED — does not discriminate) after 2 h 10 min in the hook, the missing arm's
output discarded by the gate's design; the self-test then passed twice — from the shell and
under a real pre-commit hook environment, about 35 min each — and the five arms that carry hard
time budgets passed under a 12-thread CPU burn with durations roughly doubled
(target/p4-system-14/a42ar/selftest.log, hook-selftest.log, timed-probes.log). Cause not
identified. Open for .14: the gate lacks the diagnostic that would have named the arm — persist
the self-test's MISS lines on REFUSED — and target/doctrine-selftest holds thousands of leaked
fixture directories (85 MB) from the project checks' self-tests. Commit: SEMULITH-P4-0286. Next: a42as — one case with many predeclared
properties (one per Table 1 cell and per form) in the property binding, then the v3
declaration and the capture.

<a id="a42aq"></a>

### .14 a42aq / SEMULITH-P4-0285: policy legs of the retained case (completed)

Owned on clean d121b50; a42ap's whole record/acceptance/verification/commit rows (4 spans,
3,031 B) retired into task-claims-2.md with exact inverses. scripts/review_div_policy.py
reads the policy's requirements for a `defined` medium-risk requirement as ten legs and
measures each against the retained case's own bytes (predeclaration, expectation file,
receipt, dependency manifest, catalogue) on top of the finite method review: 8 of 10
satisfied; pending boundary-fixtures (six Table 1 rows at steps 10–13, 17, 19 present,
none predeclared) and form-coverage (div predeclared; div/divu/rem/remu exercised; 13
required). Feature disposition for OB-GC-M declared (none applies). Measurement grants no
credit; a receipt claiming qualification the legs refuse fails PROFILE-CONSISTENCY, which
measures on every commit. Probe 19 tests normal/O, five seam omissions RED. REQ-GC-M stays
planned. Chapter, toolbox, doctrine mirrors, decision record. Evidence target/p4-system-14/a42aq.
promotion: declined (the chapter and the decision record carry the rule).
Next: a crediting capture predeclaring the Table 1 rows and every M form; .14 mirrors.

<a id="acceptance-rows-through-a42ax"></a>

## acceptance-rows-through-a42ax

- [x] `.14` a42ax **ROOT CAUSE** — target/p4-system-14/a42ax/reproduce.log: `grep -n "^RETAINED_CASE_ID\|^SOURCE_DECLARATION_COMMIT\|^RETAINED_CAPTURE_COMMIT\|^MEASURED_SHA256\|^MEASURED_BYTES" scripts/review_div_method.py` → lines 29–33 naming `rv64gc-signed-div-truncation-v2`, `b160c66e…`, `c91d08f5…`, `2cb6c704…`, 9928 and `grep -n "^CASE_ID" scripts/review_div_policy.py` → 64 `rv64gc-signed-div-truncation-v2`; real tree before: `python3 -B scripts/review_div_method.py` → `method stale | rv64gc-signed-div-truncation-v2 | evidence/rv64gc-signed-div-truncation-v2/planned-experiment.sexp: SHA256 differs`, `python3 -B scripts/review_div_policy.py` → `DIV-POLICY: invalidated — 6 of 10 legs satisfied; missing boundary-fixtures, matched-reference-comparison, currentness, form-coverage; …` while the complete capture's receipt reads `rv64gc-m-forms-v3 pending complete True qualification False` and the a42aw preview under a satisfied method already read `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit`; the method probe's first run after the switch (probe-method-failures.log): `DIV-METHOD: 21 tests / 3 failures / 0 errors` — `AssertionError: 0 != 1` (moved inputs asked of the first case), `'actual predeclaration' not found in 'review differs from the supported finite DIV case'` ×2 (the graph-evidence freeze on the default case), then `Tuples differ: (85, 1076834, 40438) != (85, 1048756, 33759)`.
- [x] `.14` a42ax **ADDRESSED** — reproduce.log after the switch: `python3 -B scripts/review_div_method.py` rc 0 → `{'disposition': 'satisfied', 'case_id': 'rv64gc-m-forms-v3', 'policy_disposition': 'pending', 'record_disposition': 'valid', 'capture_binding': 'matched', 'evaluation_disposition': 'pending', 'authenticated_files': 85, 'authenticated_bytes': 1076834, 'snapshot_bytes': 40438, 'charged_read_bytes': 1142222}` (review-method.json: `planned_sha256` c18146fc2a12e1ff2c66ddad5d7d79753b37d890493ae2592fca62e7d383c081, `record_sha256` fb22d5e5554a0e132c231e5551ed8314ab4be35ff93e7f086fceeacb6235a152, 39 checker sources; `--max-read-bytes 1142222` rc 0, `1142221` → `refused files: artifact exceeds snapshot byte limit` rc 1); `python3 -B scripts/review_div_policy.py` rc 0 → `DIV-POLICY: satisfied — 10 of 10 legs satisfied; no qualification credit` (policy-legs-v3-detail.log: `boundary-fixtures … 12 directed boundary rows present at steps [20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32]; 12 predeclared as properties`, `form-coverage … 13 of 13 forms predeclared … 13 exercised`, `discriminating-control … control DIVERGE at step 12 registers ['x15']; witness step 12 x15`, `credited False disposition satisfied invalidated_by None`); `python3 -B [-O] scripts/probe_div_method.py` → `DIV-METHOD: 21 tests / 0 failures / 0 errors` both modes (probe-method.log) and `grep -c "A.PREFIX\|A.PREPARED" scripts/probe_div_method.py` = 0; `python3 -B scripts/probe_div_policy.py` → `DIV-POLICY-PROBE: 22 tests / 0 failures / 0 errors`; seams-method.log 4/1/4/2/2/1/2/1/3/4/1/1/1/1 and seams-policy.log 1×7, each equal to the gate's table in both modes.
- [x] `.14` a42ax **NO REGRESSION** — `python3 -B scripts/probe_div_command.py` → `DIV-COMMAND: 19 tests / 0 failures / 0 errors` with seams 6/1/1/1/2/1/1 (seams-command.log) and `python3 -B scripts/probe_div_capture_retention.py` → `DIV-CAPTURE-RETENTION: 11 tests / 0 failures / 0 errors` with seams 1/1/1/2/1/1/1 (seams-retention.log), both callers of the now case-parametric synthetic reference on its default case; `python3 -B scripts/requirement_status.py` → `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 48 planned; 2 case(s), 0 credited, 0 declared; 0 drift, 0 finding(s); …)`; `bash knowledge-map/scripts/check_knowledge_map.sh` rc 0 after regeneration; `wc -c` LIVE_STATUS.md 6137 (ceiling 6144), evidence/README.md 4045 (ceiling 4096), CHANGELOG.md 50207 (ceiling 65536); `bash -n scripts/check_profile_consistency.sh` rc 0 with every seam table unchanged; focused checks rc 0 (focused-checks.json); `git status` shows the two consumers, three probes, the gate's comments and documents only — no pinned module, no evidence byte, no profile, definition or Rust file changed.
- [x] `.14` a42ax **ROOT CAUSE** (defects owned mid-slice) — commit.log: `❌ PROJECT-SPECIFIC` / `PROFILE-CONSISTENCY: REFUSED — the check does not discriminate (self-test failed).` / `=== 1 doctrine breach(es) — commit blocked ===` with `grep -c "self-test MISS" target/p4-system-14/a42ax/commit.log` = 0 because `grep -n "self_test >/dev/null 2>&1" scripts/check_profile_consistency.sh` = 2237; `bash scripts/check_profile_consistency.sh --self-test` from the shell (selftest.log) → `PROFILE-CONSISTENCY --self-test: 1130 pass / 0 fail`, `selftest rc=0`, 02:19:42Z → 03:05:15Z; children-timing-loaded.log (load 8–10): `probe_div_method: 21 tests … 56 children`, `timeout=20: 54 children, max 1.4s … (7% of budget)`, `probe_div_authorities … timeout=10: 33 children, max 0.3s`, `probe_div_command … timeout=15: 2 children, max 0.6s`; child-start-latency.log (load 19.18): `child start→first write: n=40 median 0.030s p90 0.034s max 0.038s (the collector probe waits 2.0s)`; the leak: `ls target/doctrine-selftest | wc -l` = 5505, `du -sh` = 87M, name shapes `5494 tmp*` (11 chars) + 10 six-char, `grep -n "mkdtemp(dir=temporary_root)" scripts/check_citations.py` = 304, 356, 384 with no `rmtree` in `_selftest`, and one unpatched `python3 -B scripts/check_citations.py --self-test` → `leaked dirs before=5505 after=5524` (citations-leak.log).
- [x] `.14` a42ax **ADDRESSED** (defects owned mid-slice) — the gate keeps its self-test output (`grep -n 'selftest_log=' scripts/check_profile_consistency.sh` → `target/profile-consistency-selftest.log`, the MISS lines printed on REFUSED) and `bash -n scripts/check_profile_consistency.sh` rc 0; observed GREEN and RED in the detached worktree `target/gate-fire` (HEAD e775705 + the patch): with the tree intact `bash scripts/check_profile_consistency.sh` → `PROFILE-CONSISTENCY: ok (5 profile dossier(s) internally consistent)` rc 0 and the kept log holds `PROFILE-CONSISTENCY --self-test: 1130 pass / 0 fail` (gate-fire-green.log, gate-fire-green-kept-log.txt; a first attempt that appended the break after `main()` never ran it and passed, so the break moved to the first line); with `raise SystemExit(3)` as the first line of its `probe_div_policy.py` (`SyntaxError … from __future__`, rc 1, no summary line) → gate-fire.log: `PROFILE-CONSISTENCY: REFUSED — the check does not discriminate (self-test failed).` followed by `PROFILE-CONSISTENCY self-test MISS: GREEN policy legs measured normal expected rc=0 reason=DIV-POLICY-PROBE: 22 tests / 0 failures / 0 errors; … got rc=1` and the probe's `SyntaxError` lines, `gate-fire rc=2`, the kept log 7,419 B with `grep -c "self-test MISS"` = 16 and `PROFILE-CONSISTENCY --self-test: 1114 pass / 16 fail` (gate-fire-kept-log.txt); `python3 -B scripts/check_citations.py --self-test` → `check_citations --self-test: 21 pass / 0 fail; 19 fixture directories removed, 0 left behind` rc 0 in both modes with `leaked dirs before=5524 after=5524` (citations-leak.log); `bash scripts/check_semantics_corpus.sh` rc 0 (check_semantics_corpus.log) with `ls target/doctrine-selftest | wc -l` = 0 afterwards; the leaked fixtures removed after a census by content shape (`3770 s.sexp sources.sexp w`, `1450 definitions profiles`, `290` empty, 3 odd, then 30 → 0): `remaining leaked fixtures removed: 30 -> 0 entries; 0 KiB`.
- [x] `.14` a42aw **ROOT CAUSE** — target/p4-system-14/a42aw/reproduce.log: `git ls-files scripts | grep -c retain_div_capture` = 0 and no tracked script writes `div-capture-verification-v1` (`grep -ln` over scripts/*.py); the writer survives only as target/p4-system-14/a42am/capture-once.py (`git ls-files target | wc -l` = 0); `ls evidence/rv64gc-m-forms-v3 | wc -l` = 7 (declared, uncaptured) and `python3 -B scripts/requirement_status.py` → `REQUIREMENT-STATUS: ok (… 2 case(s), 0 credited, 1 declared …)`; `shasum -a 256 target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim` = 16de42a86e4ea7a300385092632cd95d153cb3f6c119d31eaa9384953990b7bf = the retained identity's `binary_sha256`.
- [x] `.14` a42aw **ADDRESSED** — `python3 -B scripts/retain_div_capture.py --case rv64gc-m-forms-v3 --declaration-commit 4af5a68bbec9f1bf0922ec3787f829e029c15f29 --preflight-only` → `ready` (14 names absent, declarations 16,915 / 14,488 / 17,043 B, binary 3,801,664 B); the one invocation (capture-report.json) → `pending`, `complete_canonical_capture` true, `qualification` false, findings all `matched` / `satisfied`, runs `('baseline', 33523, 0, 7773397), ('repeat', 33562, 0, 7773373), ('control', 33599, 0, 7772398)`, verdicts `AGREE AGREE DIVERGE`, control `gpr_difference {'step_n': 12, 'observed': [['x15', 18446744073709551613]], 'expected': [['x15', 18446744073709551612]]}`, authentication 85 files / 1,076,834 B / 40,438 snapshot bytes, charged 24,396,002 of 134,217,728, publications `measured-experiment.sexp` 16,942 B `fb22d5e5554a0e132c231e5551ed8314ab4be35ff93e7f086fceeacb6235a152` and `verification.json` (re-rendered with `object` keys, receipt-rerender.log: 7,017 B `91a90d9c56487af1a6b4306e9007d771e17246ddf41b358185374680090a5a5d`; `bash scripts/check_fixture_fingerprints.sh` → `FIXTURE-FINGERPRINT: ok` after `MISSING` ×12 blocked the first commit attempt); offline-reevaluation.log (no process allowed): `pending valid satisfied`, `AGREE AGREE DIVERGE`, 25 properties bound, control observed 0xfffffffffffffffd, each trace 2,794 B `784645dcd85f2ce0cc8e734cc22c8c50231ba28434958dec7a6f855ae1cb7f05`, byte-identical; `python3 -B [-O] scripts/probe_div_capture_retention.py` → `DIV-CAPTURE-RETENTION: 11 tests / 0 failures / 0 errors` both modes, seven seams RED 1/1/1/2/1/1/1 (seams-retention.log); `python3 -B scripts/retain_div_capture.py … --preflight-only` for the retained case → `refused … outputs already exist; a capture is never rerun`.
- [x] `.14` a42aw **NO REGRESSION** — `python3 -B [-O] scripts/probe_div_capture_inputs.py` → `DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors` both modes, `--mutation actual-layout` 6 failures (census 43 of 43 members); `python3 -B [-O] scripts/probe_requirement_status.py` → `REQUIREMENT-STATUS-PROBE: 19 tests / 0 failures / 0 errors` both modes, six seams 1t/1f; real tree: `python3 -B scripts/requirement_status.py` → `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 48 planned; 2 case(s), 0 credited, 0 declared; 0 drift, 0 finding(s); …)`, `python3 -B scripts/review_div_policy.py` rc 0 → `DIV-POLICY: invalidated — 6 of 10 legs satisfied; …` (the retained case, unchanged by design); `bash scripts/check_readme_routes.sh` → `README-ROUTING-CLOSURE: ok (44 governed destination(s))`; `bash scripts/check_derived_counts.sh` → `DERIVED-COUNTS: ok` after the arm total re-derived to 1653 (`arm_total`); no retained v2 byte, no pinned module, no profile or definition changed (`git status`: the tool, its probe, the gate, the fourteen new files under evidence/rv64gc-m-forms-v3/ and documents).
- [x] `.14` a42aw **LOCKSTEP** — tree record + rows; scripts/retain_div_capture.py (new), probe_div_capture_retention.py (new), probe_div_capture_inputs.py, probe_requirement_status.py; check_profile_consistency.sh arms (capture retention 11 / 7 seams); evidence/rv64gc-m-forms-v3/ twelve observations and two results, evidence/README.md; canonical-division (the m-forms capture), prepared-inputs and capture-plan chapters; toolbox div-evidence row; MEMORY; one CHANGELOG entry; LIVE_STATUS arm total 1653 and the P4 note (14/18 unchanged).
- [x] `.14` a42av **ROOT CAUSE** — target/p4-system-14/a42av/reproduce.log: `python3 -B -c` with `inspect.signature` → `evaluate_retained_unit case_id param: False`, `capture_and_evaluate case_id param: False`, `adequacy.freeze_review case_id param: False`; `grep -n "G.reviewed_case(G.CASE_ID)" scripts/matched_gpr_evaluation.py` = 391 and `grep -n "P.reviewed_case(P.CASE_ID)" scripts/matched_gpr_adequacy.py` = 119, 314 (the binding chose the case from a module constant); `grep -o '(input … (path "scripts/matched_gpr_property.py") …' evidence/rv64gc-m-forms-v3/dependencies.sexp` → the binding module is a pinned child of the m-forms declaration (moving its constant would invalidate it); target/p4-system-14/a42at/binding-smoke.log line 13: the m-forms record under the retained case → `property claims differ from reviewed finite case`.
- [x] `.14` a42av **ADDRESSED** — redeclare.log: `python3 -B scripts/capture_div.py --declare --case rv64gc-m-forms-v3` rc 0; `dependencies.sexp 14488 -> 14488 B; children 64 -> 64; moved pins: ['scripts/capture_div.py', 'scripts/matched_gpr_evaluation.py']`; `planned-experiment.sexp 16915 -> 16915 B; pins moved: [dependencies.sexp, scripts/matched_gpr_unit_collector.py]; text apart from pins identical: True`; `authorities.sexp 17043 -> 17043 B; … identical: True`; `re-declare byte-identical: True 3`; `shasum -a 256` of the retained re-emitted declarations: planned-experiment.sexp `c18146fc2a12e1ff2c66ddad5d7d79753b37d890493ae2592fca62e7d383c081`, dependencies.sexp `a49949807e7678e6cea7911cd255666ef046c009df0c1e33f9eccd3df9a16d82`, authorities.sexp `61353fb59de7b36ca3b2a49e2b25071d1c98f5b3ed4f7dd9c52f7fe358705ac3`; `python3 -B [-O] scripts/probe_matched_gpr_property_evaluation.py` → `MATCHED-GPR-PROPERTY-EVALUATION: 25 tests / 0 failures / 0 errors` both modes, 16 seams all RED with `case-pass-through` 1 failure (seams-property-evaluation.log); `python3 -B [-O] scripts/probe_matched_gpr_unit_evaluation.py` → `MATCHED-GPR-UNIT-EVALUATION: 30 tests / 0 failures / 0 errors` both modes, 26 seams with `case-forward` 1 failure, the 25 others equal to the gate's table (seams-unit-evaluation.log); `python3 -B [-O] scripts/probe_div_method.py --mutation declaration-binding` → `DIV-METHOD: 1 tests / 4 failures / 0 errors` both modes after repointing the seam.
- [x] `.14` a42av **NO REGRESSION** — probes-long.log, both modes: `DIV-CAPTURE-INPUTS: 34 tests / 0 failures / 0 errors`, `DIV-AUTHORITIES: 18 tests / 0 failures / 0 errors`, `DIV-CAPTURE-REVIEW: 31 tests / 0 failures / 0 errors`, `DIV-POLICY-PROBE: 22 tests / 0 failures / 0 errors`, `MATCHED-GPR-UNIT-COLLECTOR: 26 tests / 0 failures / 0 errors`, `MATCHED-GPR-MANIFEST: 33 tests / 0 failures / 0 errors`, `DIV-COMMAND: 19 tests / 0 failures / 0 errors` with seven seams equal to the table, `DIV-METHOD: 21 tests / 0 failures / 0 errors` with fourteen seams equal to the table, `MATCHED-GPR-EVALUATION: 42 tests / 0 failures / 0 errors` with 29 seams equal to the table (compared by script); real tree: `python3 -B scripts/requirement_status.py` → `REQUIREMENT-STATUS: ok (rv64gc-lab-v0: 48 requirements derived 48 planned; 2 case(s), 0 credited, 1 declared; 0 drift, 0 finding(s); …)`, `python3 -B scripts/review_div_method.py` → `stale | rv64gc-signed-div-truncation-v2`, `python3 -B scripts/review_div_policy.py` rc 0 → `DIV-POLICY: invalidated — 6 of 10 legs satisfied; … no qualification credit`; the four prepared inputs' bytes unchanged (`git status`: only the three declarations under evidence/ differ); no Rust, profile, definition or retained v2 byte changed.
- [x] `.14` a42av **LOCKSTEP** — tree record + rows; scripts/matched_gpr_evaluation.py, matched_gpr_unit_collector.py, matched_gpr_adequacy.py, capture_div.py, review_div_method.py; probe_matched_gpr_property_evaluation.py, probe_matched_gpr_unit_evaluation.py, probe_div_method.py; check_profile_consistency.sh (property-evaluation 25 / 16 incl. case-pass-through, unit-evaluation 30 / 26 incl. case-forward); evidence/rv64gc-m-forms-v3/ three declarations re-emitted; decision record + INDEX row; source-property, unit-evaluation and capture-plan chapters; toolbox div-evidence rows; KNOWLEDGE_MAP regenerated; MEMORY; one CHANGELOG entry; LIVE_STATUS unchanged (P4 14/18); book count 69 decisions / 30 lesson cards.
- [x] `.14` a42au **ROOT CAUSE** — target/p4-system-14/a42au/reproduce.log: `python3 -B scripts/capture_div.py --declare --case rv64gc-m-forms-v3` → `error: unrecognized arguments: --case`; `grep -n '^GUEST = ' scripts/review_div_capture.py` = 89 (one guest constant); `grep -n '^evidence/' doctrine/readme_routes.tsv` → ceilings 22 files / 16777216 B and `git ls-tree -r -l HEAD evidence/` = 22 files / 99,878 B, a declaration adds 7 → 29 > 22; `python3 -B -` fixture (planned record, receipt removed) → `REQUIREMENT-STATUS: REFUSED — unreadable verification receipt … missing input` rc 2; defect measured mid-slice (probes-fast.log): `python3 -B scripts/requirement_status.py` → `1 case(s), 0 credited, 0 declared` with the m-forms record present, `load_cases` → `('rv64gc-m-forms-v3', None, 'declared', 0), ('rv64gc-signed-div-truncation-v2', 'rv64gc-lab-v0', 'pending', 0)` — zero bindings for both because `S.children(exp, "property")` read the root while the records nest properties under `(verification …)`.
- [x] `.14` a42au **ADDRESSED** — prepare-tool.log: `python3 -B scripts/prepare_div_inputs.py --verify --case rv64gc-signed-div-truncation-v2` → `equal` ×4 rc 0; `--show --case rv64gc-m-forms-v3` → 4440 / 7609 / 7937 / 7440 B with digests `2088…`, `666d…`, `561b…`, `ba99…`; `--write` → files created, `--verify` `equal` ×4, second `--write` → `refused … already exists` rc 1; declare-v3.json: `python3 -B scripts/capture_div.py --declare --case rv64gc-m-forms-v3` rc 0, three files retained (16,915 / 14,488 / 17,043 B), re-declare `True 3` (byte-identical), `grep -o "(property " … | wc -l` = 25, `control_run … (property_ids "form-div")`, `grep -o "(input " dependencies.sexp | wc -l` = 64; `python3 -B scripts/review_div_capture.py --review --case rv64gc-m-forms-v3` → pending, 37 modules / 64 children, 33 boundaries, image 4,440 B; `bash scripts/check_readme_routes.sh` rc 0 with the re-derived row (29 of 43 files; health 40); `python3 -B scripts/requirement_status.py` → `ok (rv64gc-lab-v0: 48 requirements derived 48 planned; 2 case(s), 0 credited, 1 declared …)` and REQ-GC-M `uncredited` = `['rv64gc-m-forms-v3:declared', 'rv64gc-signed-div-truncation-v2:pending']`; `python3 -B [-O] scripts/probe_div_capture_inputs.py` 34 / 0 both modes, `--mutation actual-layout` 34 / 6 both; `python3 -B [-O] scripts/probe_requirement_status.py` 19 / 0 both, six seams 1t/1f (seams-status.log).
- [x] `.14` a42au **NO REGRESSION** — `python3 -B [-O] scripts/probe_div_capture_review.py` 31 / 0 both modes and 18 seams equal to the gate's table (seams-capture-review.log; the five authority stand-ins now take the public signature); `probe_div_command.py` 19 / 0 both, seven seams 6/1/1/1/2/1/1 equal to the table (seams-command.log); `probe_div_method.py` 21 / 0 both, fourteen seams equal (probes-long.log); `probe_div_authorities.py` 18 / 0 both, mutations 3/1/3 unchanged; `probe_div_policy.py` 22 / 0 both (focused-checks.json); real tree: `python3 -B scripts/review_div_method.py` `stale`, `python3 -B scripts/review_div_policy.py` rc 0 `invalidated — 6 of 10 legs …` unchanged, `review_div_capture.py --review` (retained case) pending 37 / 64; focused checks: 24 of 25 rc 0 on the first run with `check_readme_routes.sh` RED `OVER CEILING docs/toolbox/: part docs/toolbox/execution.md 16436 bytes > 16384` (focused-run.log), fixed by the partition, then `check_readme_routes.sh`, `check_registry_mirror.sh`, `check_seam_integrity.sh`, `check_docpaths.sh`, `check_derived_counts.sh`, `check_book_index.sh` rc 0 and `check_table_arity.sh --all` 0 defective rows; `make book` rc 0; `bash knowledge-map/scripts/check_knowledge_map.sh` rc 0 after regeneration; `git status` shows scripts, evidence declarations/inputs and documents only — no Rust, profile, definition or retained v2 byte changed.
- [x] `.14` a42au **LOCKSTEP** — tree record + rows; scripts/prepare_div_inputs.py (new), capture_div.py, review_div_capture.py, requirement_status.py; probe_div_capture_inputs.py (rewritten), probe_requirement_status.py, probe_div_capture_review.py, probe_div_command.py (stand-ins); check_profile_consistency.sh arms (inputs 34 / 6, status 19 + `declared-credits`); evidence/rv64gc-m-forms-v3/ (7 files), evidence/README.md; two decision records + INDEX rows (evidence family, knowledge family); DEV_NOTES lesson + knowledge card + INDEX row; doctrine/readme_routes.tsv (three rows); prepared-inputs and capture-plan chapters; toolbox: div-evidence.md (new family), execution.md, TOOLBOX.md; KNOWLEDGE_MAP regenerated; MEMORY; one CHANGELOG entry; LIVE_STATUS P4 note (v2 invalidated, v3 declared; 14/18 unchanged); book counts 68 decisions / 30 lesson cards.
- [x] `.14` a42at **ROOT CAUSE** — `grep -n '"property", 1' scripts/matched_gpr_relations.py` = 93 (`_records(graph, "property", 1)`); `grep -n 'graph\["property"\]\[0\]' scripts/matched_gpr_evaluation.py scripts/matched_gpr_unit_collector.py` = 184, 372; `grep -n 'witnesses\[0\]' scripts/review_div_policy.py` = 192 (target/p4-system-14/a42at/reproduce-before.log); experiment `python3 -B` (reproduce-two-properties.log): the synthetic fixture with a second property → `bind_relations` `refused | method requires 1 property records`; `compare_source_expectation` over m-forms.s at (12, x15) → `matched 0xfffffffffffffffd`; reviewed cases in the binding `['signed_division_case']`; `python3 -B scripts/review_div_policy.py` rc=0 `DIV-POLICY: pending — 8 of 10 legs satisfied; missing boundary-fixtures, form-coverage`.
- [x] `.14` a42at **ADDRESSED** — `python3 -B` independent re-derivation (target/p4-system-14/a42at/independent-m-forms.log): `reviewed steps re-derived: 33 of 33`, `properties consistent with reviewed steps: 25 of 25`, `forms covered: 13`, `table1 cells: 12 steps [20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32]` = the source's Table 1 lines, source sha and size match; binding-smoke.log: v2 `bind: matched` (1 observed), v3 `bind: matched` (25 observed, control `0xfffffffffffffffd`), wrong last value → `snapshot steps differ from reviewed words/operands/values`, each record under the other case → `property claims differ from reviewed finite case`; `python3 -B [-O] scripts/probe_matched_gpr_property.py` 34 tests / 0 failures / 0 errors both modes, 35 seams all RED (seams-property.log: claim-values 3, reviewed-words 8, control-claim 2, claim-count 1, claim-copy 6, …); `probe_matched_gpr_property_evaluation.py` 24 / 0 both modes, 16 seams (seams-property-evaluation.log: control-value 1, property-fact-binding 19); `probe_matched_gpr_relations.py` 42 / 0, 19 seams (seams-relations.log: property-count 2, witness-unique 2, control-property 1); `probe_div_policy.py` 22 / 0, 7 seams 1t/1f (seams-policy.log: first-property); real tree (reviews-after.log): `python3 -B scripts/review_div_method.py` `stale | evidence/rv64gc-signed-div-truncation-v2/planned-experiment.sexp: SHA256 differs`, `python3 -B scripts/review_div_policy.py` rc=0 `DIV-POLICY: invalidated — 6 of 10 legs satisfied; missing boundary-fixtures, matched-reference-comparison, currentness, form-coverage; invalidated by evidence/rv64gc-signed-div-truncation-v2/planned-experiment.sexp: SHA256 differs; no qualification credit`.
- [x] `.14` a42at **NO REGRESSION** — probes with unchanged counts: `python3 -B scripts/probe_matched_gpr_manifest.py` 33 / 0, `probe_matched_gpr_evaluation.py` 42 / 0, `probe_matched_gpr_unit_evaluation.py` 29 / 0, `probe_matched_gpr_unit_collector.py` 26 / 0, `probe_div_capture_inputs.py` 16 / 0, `probe_div_capture_review.py` 31 / 0, `probe_div_authorities.py` 18 / 0, `probe_div_command.py` 19 / 0, `probe_div_method.py` 21 / 0, `probe_matched_gpr_value_evaluation.py` 19 / 0; seam matrices normal and -O for evaluation (29 seams), value-evaluation (12), capture-review (18), unit-evaluation (25), command (7: 6/1/1/1/2/1/1), method (14: 4/1/4/2/2/1/2/1/3/4/1/1/1/1), every count equal to the gate's table (target/p4-system-14/a42at/seams-probe_*.log, compared by script); `python3 -B scripts/review_div_capture.py --review` pending, modules 37 / children 64 unchanged; focused checks rc=0 (target/p4-system-14/a42at/focused-checks.json) after two repairs — `bash scripts/check_derived_counts.sh` COUNT DRIFT 1647 → re-derived 1651 with the doctrine's own `arm_total` (four new static `score` lines), `bash scripts/check_unit_books.sh` BOOK-LINK missing-path → the decision referenced as the other chapters do, then `make book` rc=0 and UNIT-BOOKS ok (6 units + project book, 3660 hyperlinks); `bash knowledge-map/scripts/check_knowledge_map.sh` rc=0 after regeneration; `bash scripts/check_table_arity.sh --all` 0 defective rows; `git status` shows scripts and documents only — no Rust, profile, definition or evidence byte changed.
- [x] `.14` a42at **LOCKSTEP** — tree record + rows; scripts/matched_gpr_property.py, matched_gpr_relations.py, matched_gpr_evaluation.py, matched_gpr_unit_collector.py, matched_gpr_adequacy.py, capture_div.py, review_div_method.py, review_div_capture.py, review_div_policy.py; eleven probes; check_profile_consistency.sh arms (property 34 / 35 seams, property-evaluation 24 / 16, relations 42 / 19, policy 22 / 7); decision record + INDEX row; source-property, policy-adequacy, retained-method, prepared-inputs chapters; toolbox rows (execution 11, 14, new property row; guest-evidence 13); KNOWLEDGE_MAP regenerated; MEMORY; one CHANGELOG entry; LIVE_STATUS arm total 1651 (P4 14/18 unchanged); book decision count 66.
- [x] `.14` a42as **ROOT CAUSE** — `evidence/rv64gc-signed-div-truncation-v2/dependencies.sexp` pins 64 inputs + 4 principals (`grep -o '(input ' … | wc -l` = 64; 35 scripts, 20 definitions/riscv/*.sexp, 6 profile files, 4 schemas, 1 guest); `git log --since=30.days --name-only` touched 67 of the 68 (0 commits since the capture c91d08f); experiment (one appended comment line on scripts/matched_gpr_property.py, reverted): `python3 -B scripts/review_div_method.py` rc=1 `stale | evidence/…/planned-experiment.sexp: SHA256 differs`; `python3 -B scripts/review_div_policy.py` rc=1 `DIV-POLICY: blocked — 6 of 10 legs satisfied; … FINDING finite method not satisfied (stale)`; `bash scripts/check_profile_consistency.sh --self-test` rc=1 `1054 pass / 32 fail`: GREEN composed DIV command ×2 (`'mismatch' != 'matched'` for the three declarations, `'refused' != 'pending'` offline), its seven RED arms ×2 (19 tests / N failures no longer exact), GREEN retained DIV method ×2 (`('stale', 'pending', None, None, None)`), six method RED arms ×2 (evaluation-selection, typed-findings, native-envelope rc=0: the seam never reached), GREEN policy legs ×2 (target/p4-system-14/a42as/stale-experiment.log, stale-selftest.log).
- [x] `.14` a42as **ADDRESSED** — moved tree: `python3 -B scripts/review_div_policy.py` rc=0 `DIV-POLICY: invalidated — 6 of 10 legs satisfied; missing boundary-fixtures, matched-reference-comparison, currentness, form-coverage; invalidated by evidence/rv64gc-signed-div-truncation-v2/planned-experiment.sexp: SHA256 differs; no qualification credit`; `python3 -B scripts/requirement_status.py` rc=0 (48 planned, 0 credited); probe matrix both states (target/p4-system-14/a42as/probe-matrix.log): `probe_div_policy.py` 21 tests / 0 failures normal+O, six seams `1 tests / 1 failures` (lock-stale new); `probe_div_command.py` 19 / 0, seven seams 6,1,1,1,2,1,1 in both states; `probe_div_method.py` 21 / 0 normal+O (after the synthetic-target and exact-charge fixes: target/p4-system-14/a42as/fix-method-green.err, fix-method-O.log), fourteen seams 4,1,4,2,2,1,2,1,3,4,1,1,1,1 in both states; synthetic current capture `status pending` in 1.6 s, reviewed `satisfied`, record valid, binding matched, 85 files, checker 39 (template-trial).
- [x] `.14` a42as **NO REGRESSION** — current tree unchanged: `python3 -B scripts/review_div_method.py` satisfied; `python3 -B scripts/review_div_policy.py` rc=0 `pending — 8 of 10 legs satisfied; missing boundary-fixtures, form-coverage`; `bash scripts/check_readme_routes.sh` rc=0; `bash knowledge-map/scripts/check_knowledge_map.sh` rc=0; focused checks rc=0 and staged checks rc=0 (target/p4-system-14/a42as/focused-checks.json, staged-checks.json); gate `--self-test` arms for the three probes re-measured in both states (above); no Rust, no profile, no definition, no evidence byte changed (`git status` shows four scripts and documents only).
- [x] `.14` a42as **LOCKSTEP** — tree record + rows; scripts/review_div_policy.py, probe_div_policy.py, probe_div_method.py, probe_div_command.py, check_profile_consistency.sh (counts 21/21, lock-stale, comments); decision record + INDEX row; policy-adequacy chapter ("What a moved pin does"); toolbox rows 9, 11, 31; book decision count 65 + replay line; KNOWLEDGE_MAP regenerated; MEMORY; one CHANGELOG entry; LIVE_STATUS unchanged (P4 14/18).
- [x] `.14` a42ar **ROOT CAUSE** — `python3 -B scripts/review_div_policy.py` rc=0 at b469800: `DIV-POLICY: pending — 8 of 10 legs satisfied; missing boundary-fixtures, form-coverage`; no tracked program carried all 13 M forms: `grep -c 'Table 1)' profiles/rv64gc-lab-v0/guests/m-div.expected.sexp` = 6 and `grep -o '(insn "[a-z]*' profiles/rv64gc-lab-v0/guests/m-div.expected.sexp | sort -u | wc -l` = 6 (four M forms); with the program staged `bash scripts/check_readme_routes.sh` rc=1: `OVER CEILING profiles/: 3154244 aggregate bytes > 3145728` (target/p4-system-14/a42ar/routes-red.log), the first signal the gate could give because the family stood above its health target by the 2026-10-06 design; first commit attempt blocked by pre-commit PROFILE-CONSISTENCY `DIV-POLICY: blocked — 6 of 10 legs satisfied; missing boundary-fixtures, matched-reference-comparison, currentness, form-coverage; FINDING finite method not satisfied (stale)` because scripts/derive_rv64gc_expectations.py, one of the 64 inputs the retained case pins, carried a one-line PARCEL_OWNED_GUESTS registration, and by MATERIALS-BILL `DRIFT rv64gc-lab-v0: internal-contracts.md` (target/p4-system-14/a42ar/commit-blocked.log).
- [x] `.14` a42ar **ADDRESSED** — `grep -c 'Table 1)' profiles/rv64gc-lab-v0/guests/m-forms.expected.sexp` = 12; all 13 forms present (`grep -o '(insn "[a-z]*' … | sort -u | wc -l` = 15 with addi and slli); `python3 -B scripts/derive_rv64gc_expectations.py --check --parcels --steps 33 …` rc=0 byte-identical; `python3 -B scripts/run_rv64gc_sail.py m-forms` rc=0: AGREE 33 declared steps, two traces byte-identical; `bash scripts/check_readme_routes.sh` rc=0 under the re-derived row (ceilings 800 / 4,194,304, health 684 / 3,586,000, per-part 65,536; decision_profiles-family-corpus-second-rederivation.md); the author and its two probes restored to b469800 (`python3 -B scripts/review_div_method.py` satisfied; `python3 -B scripts/review_div_policy.py` `pending — 8 of 10` again; `--check-owned` 42 byte-identical, m-forms checked with `--check --parcels --steps 33`); `python3 scripts/gen_model_book.py --unit rv64gc-lab-v0` regenerated the fragment, `bash scripts/check_materials_bill.sh` rc=0.
- [x] `.14` a42ar **NO REGRESSION** — `bash scripts/check_guest_gen.sh` rc=0; `bash scripts/check_interaction_matrix.sh` rc=0; `bash scripts/check_exercise_coverage.sh` rc=0; `make check` rc=0 (cargo test 173 + 17 + 287 passed, 0 failed; fmt and clippy clean); focused checks rc=0; seven books; `python3 -B scripts/review_div_policy.py` unchanged (pending 8 of 10: the retained case is untouched).
- [x] `.14` a42ar **LOCKSTEP** — tree record + rows; archive part 20 + three section pointers; policy-adequacy chapter; run-order.txt, interactions.sexp, regenerated guests_rv64gc.rs and internal-contracts.md fragment; the pinned-author lesson promoted into decision_policy-legs-measured-two-pending.md (`answers:`); registry row + comment, decision record + INDEX row, book count line; DEV_NOTES lesson promoted (`answers:`); MEMORY; one CHANGELOG line; LIVE_STATUS unchanged (P4 14/18).
