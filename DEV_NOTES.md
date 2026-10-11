# DEV_NOTES.md

## _(2026-10-11)_ — authenticate retained Sail reference identity (P4-SYSTEM.14 a30)

Fresh full-CI preflight on clean3960e6b completed all five legs rc0, including
173/17/253 Rust tests and53 smoke-bench arms. This receipt belongs to that
pre-change milestone; it does not claim full CI on this implementation.

Add matched_gpr_identity.read_reference_identity as a finite authenticated method
dependency. Validate request role/ID and used candidate fields before I/O, then
read exactly one immutable pinned descriptor through read_snapshot (64KiB cap).
Validate raw references schema before D's single mapper; require exactly one root,
one Sail candidate and no experiments. Match required id/origin/kind/binary/
binary_sha256 and exact presence/value of release/version/source_commit/asset/
asset_sha256. Do not hash the whole parent dossier, inspect/open the executable
cache, launch a process, bind receipts/producers or claim whole-closure currentness.
Frozen results separate matched/stale/unavailable/refused from underlying pin
findings; expose detached immutable execution fields only on a current match.
A matched pin can still yield invalid syntax or stale execution identity.

The first40-test run exposed this new consumer's KeyError assumption (37 errors):
the established mapper omits absent repeated families. Tools identified the
complete mapper tail; use get(experiment,[]) without changing the mapper. Schema
omission also motivated defensive candidate-count access. Assertion-only mutation
controls use dict.get for optional-result inspection so missing identity fields
produce intended assertion failures rather than harness KeyErrors. Final40/0/0
passes normal/optimized; eight omissions lose4/2/5/1/1/1/20/17 assertions in both
modes, no errors. PROFILE-CONSISTENCY80/0 adds18 outer arms (39 doctrines/885).
First focused registration correctly refused885 versus869: DERIVED-COUNTS counts
literal outer calls. Replace the new loop with18 explicit calls, preserving the
enumerator and all62 old arms; remeasure before accepting the live count.
Actual on-volume files exercise inclusive caps, pre-read oversized refusal,
unsafe/missing/changed pins, schema-before-mapping, all fields/presence, descriptive
metadata, frozen detached results and snapshot reuse after a later path rewrite.
The new reader owns no artifact mutation; fixture lifetimes clean each test.

Teach complete synthetic root-relative writer/reader/staleness example in the GC
book; explicitly separate descriptor pins from executable authentication, replay,
receipt/process attestation, producer ancestry and qualification. Correct a
missing sentence separator in the touched doctrine description. Existing APIs,
canonical records, full history receipts and fixed seals/caps remain protected.
Focused17/sharder12/0/seven books and3038 rendered links/full literal commands
pass. Before/canonical/contract/history/scope tools rc0 protect243 canonical
dictionaries/legacy ASTs, all normative method text/all62 previous checker arms,
1298 other files/modes/Gitlinks and complete old append/task predecessors. The
first published-receipt diagnostic used the pure heads/new-shards sub-check;
inspect both owners and use the full partition judge, which refuses the actual
old shard0241 rc+digest rewrite (MODIFIED ROW). No production archive defect.
No sharding required; all fixed seals/caps remain unchanged. Next a31
receipt/invocation/input/producer binding, then closure/aggregate orchestration,
collector, measured retention/cases, captures and full policy/status consumers.

First COMMIT attempt refuses solely TASK-ACCEPTANCE/SEAM-INTEGRITY: this new
unit's three ticked boxes used rc0, which does not match the declared rc=0 evidence
signature. Inspect the exact enforcer regex, correct only this unit's receipts,
leave all signatures/gates intact and retry hooks. Routine caller/registration/
receipt lessons explicitly declined for promotion in the owning leaf; existing
contracts already own them. No failed hook run is claimed as signoff.

## _(2026-10-11)_ — compare bounded supplied-byte Sail units (P4-SYSTEM.14 a29)

The method's byte-comparison dependency now has one owner: matched_gpr_comparison.
Its immutable GprWitness and three RunBytes carry explicit process exits; no
successful exit is defaulted. Check parent1..4096/witness types/bounds and all
five byte payloads before decoding/parsing: expectations1..1MiB each, traces0..4MiB
each. These are supplied payload limits, not RAM or whole-method authenticated
read/retention budgets. The only file I/O loads the project expectation schema.
No artifact loader, binary lookup, process or qualified Boolean is introduced.

Validate raw expectations before the single dossier mapper; require exactly one
root and the complete ordered parent budget. Duplicate writes refuse before
collapse. Canonical x1..x31 and hexadecimal RV64 values are required; uppercase
and redundant leading zeros remain valid. Unsupported cross_model false,
expect_divergence and fault injection produce an unsupported disposition without
comparison credit. UnitError refuses malformed method inputs, not canonical
record validity. Retained metadata participates in exact sole-change equality,
without new fetch/negative-write/PC/CSR/FP/memory observation credit.

Compute all three run comparisons through the structured public adapter. A valid
failed process/empty or invalid trace yields failed with all run results retained.
Baseline/repeat must agree and all three raw traces be byte-identical. The sole
control expectation change is its named RV64 value; other mapped data stays exact.
Its first structured difference must match the complete baseline/control change
sets at the witness. No reason text is interpreted as success; formatting-only
expectation changes are permitted, same-value hex aliases are not controls.

Closed dbd4e43 scripts census finds no previous compare_unit owner.52 methods
pass normal/O, including inclusive1MiB/4MiB/4096 limits. Fourteen independent
omissions lose6/1/8/1/3/1/10/6/1/1/7/6/5/4 assertions, no errors, both modes.
GUEST-GEN204/0 retains174 old outer arms/adds30; derive39 doctrines/867 arms.
Focused17/sharder12/0/seven books pass;243 canonical dictionaries/legacy ASTs
and dispatch exact. Normal/print phrases, literal example plus both control
commands and3034 rendered links pass. All old method requirements/index rows
reconstruct exactly after restoring current implementation metadata/pointer.

A late adversarial probe found two native ValueError escapes: STEP_RE/WRITE_RE
admit5000-digit indices that Python refuses to convert. Stop only the verified
own commit-hook subtree (exit143, no commit), log ownership, then normalize both
conversions to SailError in one public parser helper. Four old public API crashes
become four refusals/two failed byte units, normal/O. Whole adapter inverse
restores only that helper/two calls; ten other definition ASTs stay exact.
An initial global-int test mock interfered with isinstance and gave false REDs;
isolate the conversion injection in copied helper globals before accepting it.
Native controls use distinct fresh step/register fixtures and restore Python's
configured limit. The new omission loses four clean assertions in each mode.

No Rust, canonical capture, producer/policy/qualification, CPU, fixed cap or sealed
history changes. Promote the native-conversion lesson in the existing method
record; current metadata/book own the implementation boundary. The complete append/task predecessor and protected-scope proofs plus
staged byte equality remain required before COMMIT. Evidence target/p4-system-14/a29.
Measured head pressure uses only the published whole-entry sharder when needed;
no prose compaction or past receipt rewrite is allowed. Next a30 authenticated
receipt/closure orchestration, reviewed fresh collector, retention/predeclared
cases/captures and full policy/status. Full CI remains a25 preflight d8083a9;
a30 owns a fresh full-CI preflight after this completed byte-unit milestone.

## _(2026-10-11)_ — expose structured Sail differences with complete validation (P4-SYSTEM.14 a28)

The method needs exact first GPR changes, not a verdict/reason substring. Expose
immutable Comparison/GprDifference from the public adapter's single comparison
owner; the legacy tuple wrapper delegates. Complete observed/expected sets are
canonical sorted tuples, with no caller-dictionary alias. Delivery mismatches
carry no GPR difference. Byte/schema/authentication/method checks stay separate.

Before signoff, the controls expose an old defect: both early DIVERGE returns
precede later required-row/x0 validation. Recover9bad4c4's public adapter: four
GPR/delivery differences hide missing/nonzero-x0 tails; a fifth delivery mismatch
hides nonzero x0 in that same row. Both repaired APIs refuse all five, normal/O.
Retain the first difference while validating every boundary; complete valid
legacy outcomes/details stay exact. Full adapter inverse undoes only declared
result packaging/validation continuation; seven other definitions are byte-exact.
819 complete valid legacy tuples match normally and optimized.

34 methods pass in both modes; ten omitted protections lose11/10/10/1/3/1/1/2/2/2
assertions with no setup errors. GUEST-GEN174/0 retains152 old outer arms and adds22;
derive39 doctrines/837 arms. Legacy Sail probe passes; its explicit budget controls
also pass under optimization, without claiming optimized effectiveness for old
assert statements. Diagnostic alias/fixture/newline mistakes were corrected;
only successful final proof runs supply signoff.

Fix duplicate GC book status left stale by a26: route to the included canonical
method boundary and artifact chapter; clarify historical a20 text. Teach structured
results, full-tail validation and a complete synthetic example. Normal/print
phrases, stale-intro absence, all3030 hyperlinks and the literal example plus both
control commands pass. Promote the validation lesson in the existing method
record, compressing only current routing prose within fixed caps; no new decision
file. Focused17/sharder12/0/seven books pass;243 canonical dictionaries and legacy
mapping ASTs/dispatch remain exact. Scope1293 other tracked files exact, Git links
unchanged without traversal. No Rust, canonical capture, policy, seals/caps or CPU
acceptance changes. Whole append/task predecessors and original count-edit REDs
must pass again with staged-byte equality before COMMIT. Evidence target/p4-system-14/a28.
Next a29 bounded comparison unit, then authenticated closure/orchestration,
collector, measured retention/captures and full policy/status. Full CI remains the
d8083a9 a25 preflight; subsequent slices have focused gates and complete hooks.

## _(2026-10-11)_ — close exact-token schema end anchors (P4-SYSTEM.14 a27)

A26's SHA256 control exposes an existing grammar defect: re.search with `$`
also admits one terminal newline. Closed inventory24 schemas/91 patterned fields
finds83 affected declarations in13 files; eight prospective artifact facets
already use strict ends. Recover the old24 schemas and five real complete docs
from1861712 into an on-volume no-Git fixture:7 methods/88 assertion failures
(83 facets+5 docs), no errors, normally/optimized. Fixture removed.

Change only83 token-end declarations to strict \Z, with escaped source spelling.
Generic substring search stays byte-exact in the kernel. Named valid tokens,
newline/CRLF/NUL/tab boundaries and five real documents pass:7 methods/91 facets,
normal/optimized. Loose ends lose96 assertions; ignored patterns552; a proposed
fullmatch kernel loses1 generic-search assertion. RECORD-SCHEMA70/0 retains62
old outer arms/adds8; derive39 doctrines/815 arms. No pattern is silently skipped.
83 semantic/full-source inverses across13 files and all24 public schema loads
plus the schema fixpoint pass. Correct an initial proof assumption: schema.sexp
alone does not declare operators; load_schema owns their existing meta-validation.
That instrument refusal was not a schema defect or accepted signoff result.

All243 canonical dossier dictionaries and legacy ASTs/dispatch stay exact.
Focused16/sharder12/0/seven books,3024 hyperlinks, normal/print teaching boundaries
and three literal new book commands pass. New bounded decision promotes the
lesson; shorten only three hot index labels/hooks, preserving their full records.
Canonical bytes, policy, fixed seals/caps and CPU status unchanged. No reference
execution or qualification. Scope1279 other tracked files byte/mode exact; Git
links unchanged, kernel/full old decision records protected. Complete append/task
predecessor inverses and original receipt-edit refusals pass; no sharding needed.
Evidence target/p4-system-14/a27; preserve complete
append/task predecessors and staged bytes before COMMIT. Next a28 bounded
comparison core, then authenticated closure/orchestration, collector/retention/
captures and full policy/status consumers. Full CI preflight remains d8083a9.

## _(2026-10-11)_ — carry bounded prospective artifact formats (P4-SYSTEM.14 a26)

Add matched-gpr-dependencies-v1/dependencies and sail-gpr-capture-v1/capture
schemas, pure dossier mappings and bounded bytes-only validation. Exactly one
raw document validates before mapping; duplicate singulars cannot collapse.
Require immutable1..65536B before decoding/parsing, strict version/digest facets,
canonical locations/paths, unique IDs/paths, manifest1..64/no self/declared nesting,
collector inventory membership and exactly one trace/stdout/stderr output with
nonnegative size. Failed exits and empty output files remain honest data.
Writers refuse unknown keys and lossy serialization. No unbounded legacy-loader
entry, artifact opening, pin authentication, process or qualification is added.
Hidden nested content, canonical run/invocation matching, aggregate method bounds
and retained-store integration remain evaluator/collector obligations.

36 tests pass normally/optimized; ten omissions lose3/1/2/1/1/3/4/1/1/1 assertions
in each mode. DOSSIER-SCHEMA47/0 retains25 old outer arms and adds22; derive39
doctrines/807 outer arms. All243 canonical dictionaries, legacy function/class
ASTs and family dispatch stay exact. Focused15/sharder12/0/seven books pass;
3024 rendered hyperlinks, normal/print boundaries, illustrative manifest and
five literal book commands pass. First mutation driver correctly refuses an
ambiguous self-path replacement seam; narrow it to the dependency guard before
accepting the ten omission results. No failed instrument supplied signoff.

Reproduce existing references schema accepting sha256='a'*64+'\n': regex search
with `$` permits a terminal newline. New artifact facets use strict end anchors;
a27 owns inventory/repair/controls before a28 evaluator. Pin reader already uses
fullmatch; grammar acceptance is still a defect. Existing policies, canonical
records, CPU status, fixed seals and caps stay unchanged. Own published DEV
whole-suffix sharding, exact append/task predecessors and staged-byte proof.
Published DEV29==23+6 retains8528B in shard0240/8761B, SHA256
f1c4d0b9efe531d83a32058d3e037f4b3934a70d8eee3d36707015deb3452a2f; old
manifest prefix/99 complete append predecessors and full task inverse pass.
Scope proves1285 other tracked files byte/mode exact, Git links untouched.
Evidence target/p4-system-14/a26; full CI preflight remains scoped to d8083a9.

## _(2026-10-11)_ — preserve live history predecessors (P4-SYSTEM.14 a25)

Reproduce both a23 overbroad Focused11 edits in the5de7c27 history corpus: the
old partition judge reports240 frozen rows/rc0 despite changed live bodies.
The new guard refuses each. SHARD-FREEZE now compares complete predecessor
entries/preambles in both index and working views; new prefixes and whole oldest
suffix moves retain exact bytes/order. New shards use published wrappers/digests.
The existing partition judge also authenticates the complete staged corpus in an
owned disposable snapshot, so restored working bytes cannot hide staged edits.
Git failures refuse; only a successful closed inventory establishes absence.
Snapshots stay on-volume, bounded8MiB/1024 paths. No secondary Git repo is created.
Corrections belong in new entries; byte preservation does not establish prose truth.

38 controls pass normally/optimized; five omissions lose17/1/2/2/1 assertions in
both modes. SHARD-FREEZE43/0 includes the original31 controls and12 new shell
arms; published sharder12/0 passes. Actual a24 source inverses reconstruct46331B
CHANGELOG/f7911fea77ea6063eece04fa524c8bae97d1b260fd73df3ce83f09e81c40c8e0
and47829B DEV/fed228c3151e8b7da96fe8b3ca76bd6e3760e9cdb4e8521a565661a62ad73e35.
Two retained count edits and a real moved rc edit with updated digest refuse.
Both proposed/working views prove97 complete predecessor entries at d8083a9.
Focused12/seven books and3022 rendered hyperlinks/literal book commands pass;
1283 protected files stay exact, Git links untouched. Derive39 doctrines/785 outer
arms; no fixed cap, old seal/archive, canonical input or CPU acceptance change.

Final review reproduces an import-time Git read outside refusal handling from
shard_history's CLI setup. Extract six shared definitions/constants into the pure
history_entries owner; public sharder aliases and all remaining definition ASTs
stay exact. Fresh-process no-Git import control, sharder/event proofs pass.
Correct three initial fixture errors by allocating its scratch parent; correct
an actual-proof assumption by locating the old notes count in its retained head,
then test a real moved rc field separately. No failed instrument supplied signoff.
The new decision records the contract; contain only one hot index label/hook,
keeping its full record unchanged. Book explains new corrections and dry-run moves.

Full CI preflight on d8083a9 plus only a25 ownership/resume text passed all five
legs (Rust173/17/253, all doctrines, bench, smoke-bench53, seven books), with
tracked sources frozen until session79683 closed. Post-guard focused checks and
hooks verify the new history behavior; no Rust changes. Next a26 dependency and
capture artifact schemas/mapping, then evaluator/collector, retention/captures and
full policy/status consumers. Evidence target/p4-system-14/a25. Repeat full append
predecessor/root inverses and staged-byte equality before commit.

## _(2026-10-11)_ — gate fresh book navigation and catalogue (P4-SYSTEM.14 a24)

Reproduce six ordinary/four print missing sibling destinations and the stale
RV64GC overview. Registration last changed47cb436; the overview last changed
141c1bd, so resolution-stage prose survived registration. The old UNIT-BOOKS
helper also accepts an absolute source outside its supplied corpus in an owned
fixture. Reuse records_sexp's unit mapper; validate relative source components,
symlinks, volume/Git boundaries before builds. Compare catalogue IDs/kinds and
build all seven books into an isolated disposable bundle. Check every rendered
local hyperlink path/HTML fragment, including print; remote availability and
semantic/chapter completeness remain separate. Stale output cannot qualify.

Extend the public after-include resolver to registered sibling chapters. All62
model HTML inverses differ only at six normal/four print hrefs;3016 hyperlinks
resolve,12 shared-root loopback HTTP reads pass and the server closes. Preserve
all authored model chapters. Book examples describe make book/shared docs root
and RV64GC registration separately from still-incomplete CPU-SYSTEM acceptance.
Probe26/0 and gate23/0 pass normally/optimized. Omissions route/mask/relative/
source fail20/11/15/2; catalogue/navigation/path/freshness fail4/9/12/2, also
optimized. UNIT-BOOKS16/0 includes12 shell arms and four nested-suite runs.
Derive773 outer arms/39 doctrines; focused12/sharder12/0/seven books pass.
1268 protected tracked files stay byte/mode exact; Git links remain untouched.

Part14 retains the whole2621B old overview and1956B completed c26a/c28a receipt
span. Two full source inverses and six damaged controls pass; ordinary6102B
archive SHA72a9c810ef2d1262f8e31557ad224d26192ae79417ba0b3fc7898f85c9ce1269
stays outside the closed12-file seal. Published DEV sharding preserves30==26+4;
5874B suffix,6107B shard0239 SHAb4fce8c284a6cf61c9c6b03014067c98fc4a0a900136032121cda8731ee4e169,
prior manifest prefix exact. Both append predecessors and task inverse are checked
again before staging; old receipts must not change. Fixed caps remain unchanged.

The public rendered comparison caught my wrong relative -d assumption: CLI help
says explicit relative destinations use cwd. Restore the original Makefile;
reproduce all41 misdirected generated files exactly, remove that output, and
rerun correct normal builds. Fresh absolute scratch builds were unaffected.
Promote the collection contract into decision_book-record-navigation. Next clean
unit starts with the full CI milestone check, then a25's permanent shard-aware
history guard, then a26 artifacts/evaluator/collector/captures. No Rust, canonical
input, qualification, CPU acceptance or roadmap-count advance. Evidence a24 under
target/p4-system-14; latest full CI remains a18 until that milestone check runs.

## _(2026-10-11)_ — resolve included book record links (P4-SYSTEM.14 a23)

Actual seven-book census found56 missing paths (main50; three board/device books2
apiece), no missing fragments. Includes keep repository-relative links while the
renderer changes .md to .html. Add an HTML-only public-protocol preprocessor after
include expansion for the main book's declared task/history inline links. Preserve
canonical inputs, metadata, labels, examples and other destinations; the book
shows the exact record-reading commands. Missing/symlinked declared records and
invalid protocol refuse without partial stdout. Unsupported syntax stays unchanged.

Public disabled/repaired builds:50missing->0, exactly50href changes; all50normal
HTML page inverses are byte-exact otherwise, print paths/fragments resolve, and
five literal book commands return exact retained bytes. Decision-index guard
correctly refused16509B; shorten three hot labels/hooks to16320B without changing
full records or targets.1281 protected files stay exact. Final seven-book build
runs sequentially after UNIT-BOOKS to avoid concurrent output writers. Configuration
restores in finally before repaired rendering.19 API/CLI tests pass normally and
optimized; independent route/mask/relative-context/source-guard omissions fail
16/10/13/2 assertions, also optimized. All fixtures cleaned on this volume.
Focused12/seven books/protected scope pass; no Rust/canonical/CPU/qualification/
cap/LIVE or outer-count change. Remaining6cross-unit routes/full gate are a24
next; no all-book completion claim. Evidence target/p4-system-14/a23; CI a18 green.
Catch my overbroad focused-count replacement changing two older LC0007 receipt
lines. Stop only this pending commit/hook subtree(rc143, HEAD still5de7c27,
actual census OK); restore both complete predecessor suffixes. History proof
confirms all45659DEV/45463CHANGELOG predecessor bytes exact and refuses both
original edit controls. A25 owns the permanent shard-aware preservation guard
before a26 artifacts; a24 remains the six cross-unit routes/full navigation gate.
promotion: decision_book-record-navigation.md, retrievable by canonical-link question.

## _(2026-10-11)_ — preserve completed evidence records (P4-SYSTEM.14 a22)

Before the task's fixed128KiB ceiling, move six whole completed a1–a19 spans
(88967B) and one whole old book receipt(1462B) into ordinary part13. Preserve
source offsets, lengths and hashes; authenticate seven bodies and reconstruct
the complete task130487B/book18441B sources. All21 corrupt/missing-marker/
omitted-body controls refuse. First inverse harness mistakenly dropped the old
scheduled-a22 block; exact diff isolated it, restore that predecessor block and
rerun before signoff. Two older relative history routes stay in their source
context; ten incoming root links require no moved anchors/live includes.

Part13 stays outside the closed twelve-file seal. Current features, active graph,
frontier and recent receipts remain directly live. Published DEV sharder targets
45000:30entries/48712B==28kept/43759B+2moved/4953B, exact bytes/order;
shard0238 is5186B SHA25691157a12f0d07f51181885936cc6c0771bd84b633c2f84810c350c7b0da9ef3c.
Earlier manifest/history exact. Focused10/sharder12/0/TASK-HISTORY46, seven books,
rendered navigation/source inverses/protected scope pass. No code/canonical/
qualification/CPU/LIVE or cap change;768outer arms. Next rendered-link census, then bounded artifact mappings.
Actual rendered check caught mdBook rewriting archive links to missing HTML.
Own/fix five current chapter routes through local reading instructions; preserve
four original targets in the inverse map. High-priority broader book census is
a23 next, before artifact mappings. Exclude the generated heading self-link
from the content-link meter before accepting five repaired routes. Three literal
book retrieval commands return exact originals;1281 protected files exact. Evidence target/p4-system-14/a22; CI a18 green.
promotion: declined (finite preservation receipts; existing task-book policy unchanged).

## _(2026-10-11)_ — bound authentication reads (P4-SYSTEM.14 a21)

Separate retention from limits in the shared anchored reader; expose read_bounded_pin
with required nonnegative/nonboolean max_bytes and no payload. Snapshot growth
probes also stay within the cap. At an exact cap, metadata checks refuse growth
without another read; legacy pin-only behavior remains. Actual cap3 diagnostic:
old snapshot consumes4 then refuses, current consumes3 and refuses without data.
No old false agreement is claimed. Aggregate method budgets remain evaluator work.

Limits53/0 also optimized; four independent omissions lose6/5/10/3 intended cases,
also optimized. Preserve pins39/snapshots24 and17 old omission controls, plus real
multi-chunk pin reads and cleanup. Review reproduced a new probe's false RED on
legitimate short reads: it summed requested bytes. Count consumed bytes and run
the complete snapshot suite through short reads; reinstated wrong meter52/1 fails
exactly that case. The literal book harness initially passed a Path, correctly
refused; use its required canonical string before accepting the result.

Focused13/profile62/0/schema25/0, seven books, actual book helper, rendered checks
and protected scope pass. Derive768outer arms; no canonical/qualification/status/
cap advance. Evidence target/p4-system-14/a21; latest full CI a18 green.
promotion: matched-experiment/first-method decisions and GC-book read-budget API.

## _(2026-10-11)_ — typed comparison locators (P4-SYSTEM.14 a20)

Carry optional singular gpr_witness(step_n,register) and control baseline_id in the
existing reference schema/single mapper. Validate canonical x1..x31, raw shape
before mapping, witness budget/GPR observation kind and baseline run endpoints.
Generic omission/different baselines stay valid; exact first-method adequacy and
all qualification remain pending. Correct the stale schema evaluator comment.

Graph74/0 (also optimized); removing budget/kind/baseline guards loses4/1/3 named
refusals, also optimized. New shape/roundtrip/mapper controls, two writer omissions
and a register-facet omission discriminate. Old schema refuses each new field;
old graph owner with new grammar/mapper66/8 isolates missing semantic checks.
All243canonical dictionaries exact. Actual production prefix names bad bounds/
baselines and keeps unqualified refusal; temporary fixture removed, no live run.

Correct two instrument assumptions: use the exact min-length diagnostic and test
old-schema fields separately because a root reports its first failure. Focused13,
schema25/0/profile57/0, seven books/eleven rendered checks/literal typed syntax pass;
protected scope checked before commit. Derive763outer arms; milestone states and
caps unchanged. Evidence target/p4-system-14/a20; latest full CI a18 green.
promotion: first-method/matched-experiment decisions and GC-book typed API/limits.

## _(2026-10-11)_ — declare the first GPR comparison method (P4-SYSTEM.14 a19)

Declare sail-gpr-change-v1 prospectively, before canonical execution: one typed
step/register witness, baseline/repeat and an exact one-value control. Fix roles,
producer pairs, relative argv, receipt cross-checks, dependency closure and finite
per-file/aggregate bounds. Keep method success distinct from full policy adequacy.
Retained executable identity plus reviewed collector provenance permits offline
comparison without a transient binary cache; replay availability stays explicit.
Hashes do not attest execution. Required project-file pins remain mandatory.

The full decision is live-included in the GC book. Current schema refuses both
new fields by name; implementation/capture/qualification remain pending. Correct
only the shape-probe's stale evaluator docstring; executable AST is exact.
Make room by moving the two oldest whole notes, 29==27kept+2moved, exact bytes/order,
to shard-0237 (4171B, SHA f7355839fce7c1483a4ef078b2111854543e9a7bd505f8d6ff7c591b449c3433).
Old manifest records remain exact; no ceiling rises. Evidence target/p4-system-14/a19.
Focused10, sharder12/0, seven books,15 rendered checks and exact old-book inverse
pass; protected scope is checked before commit. Latest full CI is a18 green.
promotion: decision_sail-gpr-comparison-method and its live GC-book include.

## _(2026-10-11)_ — refuse duplicate expectation keys (P4-SYSTEM.14 a18)

Public mapper/adapter reproduction: conflicting x1 values are shape-valid, collapse
to the last value, then AGREE. Reject duplicate write keys per step in the single
mapper, even for equal values; dossier gate maps expectations after shape checks.
Name program/step/key. Preserve distinct keys, empty writes, device labels and
repeated keys in different steps; grammar unchanged. Mapping12/0, optimized12/0,
guard removal six intended failures, actual gate0→1 and cached adapter refusal2
pass. DOSSIER-SCHEMA22/0 and existing mapper14/0 pass.

Raw census222documents/6057steps/4105entries finds zero duplicates. Initial census
misused S.field's scalar return; corrected the instrument before drawing a result.
Expanded probe's first emitter had a late global declaration; the new positive/
reason-specific arms refused it. Fix the declaration and rerun all controls.
All243canonical dictionaries exact; full five-leg CI, Rust173/17/253 and seven
books/literal+rendered refusal pass. No canonical capture/status/cap change.
Evidence target/p4-system-14/a18.
promotion: matched-experiment decision and GC book own the identity rule and limits.

## _(2026-10-11)_ — bounded authenticated snapshots (P4-SYSTEM.14 a17)

PinResult intentionally carries metadata. Reopening after its check can observe
a different file. Share the existing anchored traversal with read_snapshot,
requiring an explicit nonnegative/nonboolean byte bound; oversized files refuse
before payload reading. Return immutable bytes/result only after all pin/path/
stability checks and close callbacks succeed; failure has no data. Pin-only API
and39controls retain their behavior; snapshot memory is proportional to the bound,
not an exact process-memory ceiling, and multiple snapshots need an aggregate budget.

Snapshot24/0 (also optimized), five independent mutations and twelve old pin
predicate removals pass. Cases cover partial I/O/close errors, races, no reopen,
immutability and real multi-chunk bytes, with tracked descriptor/fixture cleanup.
No canonical capture, store, retention decision, cap or CPU acceptance change.
Focused13/profile54/0/seven books/rendered API and actual book helper pass;
protected scope checked before commit. Comparison review reproduces a conflicting
duplicate x1 write collapsed by the mapper, allowing AGREE; own priority-high a18
next, before qualification. No claim that current canonical records contain it.
Evidence target/p4-system-14/a17. promotion: matched-experiment decision and GC book
own the API, examples, memory bounds and remaining qualification boundary.

## _(2026-10-11)_ — reject surplus Sail observations (P4-SYSTEM.14 a16)

Predecessor11ee6d4 compares one expected NOP as AGREE even with an extra row/x1
write, interrupt or fetch delivery. Parsing keeps these; expected-only iteration
ignores their tail. Refuse out-of-budget rows and witnessed deliveries before
value comparison. Five tail cases/three exact-boundary agreements pass; removing
either check fails for its intended reason, also under optimization. Retain the
older offline controls; no blanket optimized-assertion claim.

Live pinned public diagnostics retain atomic242cases/3146boundaries per repeat
with wrong-granule divergence and the timer's named platform difference. These
are fresh diagnostic traces, not canonical qualification. Evidence target/p4-system-14/a16.
Move two oldest complete notes through the existing sharder:28==26+2, exact order/
bytes, head48971→44439B before this entry; immutable prior shards stay intact.
GUEST-GEN152/0, focused13, sharder12/0 and seven books/rendered rule pass. All167
cached guests/334traces retain exact predecessor verdict/reason pairs; this does
not authenticate process status. Protected1265other tracked files remain exact.
promotion: matched-experiment decision and GC book own the budget rule and limits.

## _(2026-10-11)_ — authenticate file pins (P4-SYSTEM.14 a15)

experiment_artifacts.py reuses is_canonical_path. Descriptor-anchored traversal
refuses symlinks, special files, nested Git markers and foreign devices. Regular
files stream in1MiB chunks, bounded by initial size plus one. Descriptor, filename,
parent and renewed Git-boundary checks refuse replacement. ExitStack attempts all
close callbacks; callback failure cannot yield a match.

Pin39/0 (also optimized), graph63/0/profile53/0 and focused13 pass. Real on-volume
fixtures exercise streaming, timed replacement and descriptor cleanup; foreign
devices and I/O/close errors are injected. Marker-only fixtures never initialize
another repository. Twelve independent predicate omissions expose intended
controls, with cleanup even for mutants. Actual checker integration diagnoses bad
hashes/missing files; matching files still receive the pending comparison refusal.

Pins establish check-time bytes, not execution, comparison, currentness or adequacy.
No capture/store/canonical/runtime/generated/archive/cap/acceptance change. Seven
books and rendered examples pass. The final route check caught live-note overflow;
this entry was tightened without raising its ceiling. Evidence target/p4-system-14/a15.
promotion: matched-experiment decision and GC book own the contract and limits.

## _(2026-10-10)_ — check declared capture edges before artifact qualification (P4-SYSTEM.14 a14)

Add experiment_verification.py with one raw-form entrypoint: schema validation
precedes the existing mapper. Check scoped requirements/effective obligations,
unique child IDs, producer/model/input relationships, run observations and repeat
edges, control relationships and pair assessments. load_scope reuses the public
gate_report.contract_measure selector and filters profile membership. Keep failed
controls and ancestry uncertainty honestly representable; these checks confer no
adequacy/independence credit. Lexical paths/nonnegative sizes are checked; actual
filesystem, pin, process, comparison and policy validation remain pending.

Graph63/0 and PROFILE-CONSISTENCY52/0 pass. Nine separately removed predicates
expose their intended controls, including effective-version filtering. Refine the
reused-observation/control endpoint assertions to require their own diagnostic,
so an orphan side effect cannot mask the omitted predicate. Actual checker
integration against predecessor9ec6bfe shows newly specific missing-repeat and
raw-duplicate refusals; a consistent graph still gets only the pending qualifier
refusal. An added U+0085 case reproduces a false GREEN in the initial C0/DEL-only
path predicate; cover C1 as well and retain the regression. Graph63/0 also passes
under Python optimization. Focused13 and seven books/rendered explanation pass;
protected existing files/canonical data/generated consumers/archive/caps stay exact.
No fresh capture or acceptance credit; artifact/comparison evaluation follows.

Evidence target/p4-system-14/a14. promotion: the matched-experiment decision and
its live GC book explanation retain the implemented scope, examples and limits.

## _(2026-10-10)_ — implement matched-GPR grammar without premature credit (P4-SYSTEM.14 a13)

The a12 prospective block is now an optional experiment child in the existing
reference schema and single mapper. Repeated property/input/producer/observation/
run/control/pair records survive; argv preserves order, repetitions and empty
arguments. Runs name producers and repeat_of explicitly. Structure checks cover
types/arity/cardinality/facets, not artifact identity or evidence adequacy.
PROFILE-CONSISTENCY therefore refuses every new block pending its evaluator.

Predecessor6afe055 refuses the block and loses it on writing; the new roundtrip
matches independently constructed data. All243 current dossier dictionaries,
including three reference dossiers, remain exact against that predecessor.
Every old schema construct/field survives unchanged. Seven deliberate writer/
reader child-family omissions each fail; removing version/digest/uniqueness facets
exposes their controls. Removing only the qualification guard gives50pass/1fail
for its intended reason. Current schema17/0 and consistency51/0, focused13 and
seven books pass. Complete illustrative book record and printed fixture validate;
neither represents execution. Full five-leg shared-mapping CI passes, including
Rust173/17/253, every doctrine, browser build/smoke and seven books.

No canonical data/runtime/frozen/archive change, no cap expansion or CPU credit.
Evidence target/p4-system-14/a13. Next relationship/pin/artifact evaluator, then
bounded retention and fresh captures. promotion: the existing matched-experiment
decision owns the implemented vocabulary, examples and explicit pending boundary.


## _(2026-10-10)_ — declare prospective matched-GPR capture contract (P4-SYSTEM.14 a12)

The existing flat experiment fields do not carry the typed capture graph required
by the prospective GC policy. Declare one versioned verification extension to the
existing S-expression document/mapping, without a parallel source format. Require
input/producer/observation/run/control identities, exact pins, property scope,
comparison limits, repeats and producer assessments. Distinguish a recorded capture
from computed currentness/adequacy; absent artifacts and unknown ancestry earn no
success/independence credit. Declare the bounded retention/budget review before
any first fresh canonical capture; this creates no store or cap expansion.

The full decision is included live in the GC book. Focused9/seven builds/rendered
field matrix/worked control/first-last limits/pending-status checks pass. Actual
mapper rejects a synthetic verification field as undeclared, confirming no grammar
or implementation was silently added. Protected code/schema/runtime/profile/frozen/
history/archive/LIVE populations remain byte-exact. No CPU axis closes; P4 13/18.
Next shared schema/mapping/validator, then bounded retention and fresh qualification.
Evidence target/p4-system-14/a12; all scratch on the repository volume.
promotion: decision_qualified-matched-experiment-contract.md owns the complete declaration.

## _(2026-10-10)_ — enforce experiment identity edges (P4-SYSTEM.14 a11)

Before adding GC records, four controls against the byte-identical production
prefix reproduce false GREENs: a single undeclared model, conflicting experiments
sharing one ID, repeated model entries and an independence pair naming one model
twice. Original46 pass/4 fail. Scoped git -S pins experiment metadata tob8d09f5
and pair logic to147de76. The candidate-ID set existed, but experiment IDs and
model membership/distinctness were not checked; pair length counted entries.

Track experiment IDs, check every model against candidate identities, reject
repetition and require two distinct candidates per independence pair. Fifty
controls pass, and five current dossiers remain GREEN. Restore each missing
predicate separately:49/1 each for its intended control. The repeated-model
control also requires its own reason when a separate bad-pair rule refuses.
The reference schema grammar AST is identical; remove only its stale39arm comment.
Correct three residual SEAM current-corpus descriptions; no historical-box claim.

Focused13/seven books/protected byte census pass; model-book examples and error
names explain the exact metadata boundary. Derive39doctrines/732arms/38routes.
All runtime/canonical/profile/frozen/fixture/history/archive data and existing
ceilings remain unchanged. CPU incomplete7axes/P4 13/18; this does not establish
adequacy or independence. Next structured GC runs/controls/producers, then policy/
status/mirrors. Evidence target/p4-system-14/a11, repository-volume only.
promotion: declined (the existing graph contract, permanent controls and book retain this repair).

## _(2026-10-10)_ — expose temporary controls in the review book (LIVE-CONTAINMENT.4e)

LC0007's book paragraph names the detailed reference path without including its
mode matrix or limitations. The director reviews the book, so this leaves that
new workflow insufficiently reviewable there. Anchor the canonical reference body,
include it directly in the existing chapter and add five runnable positive examples.
Whole old reference bytes remain after removing only anchors/examples; replacing
the new include with the original paragraph reconstructs the complete old chapter.
Seven books build; rendered first/last limits and all five commands are present.
Focused8/protected scope1269unchanged rc=0. No implementation,
profile, archive, cap or LIVE change; full containment adoption still remains.
Evidence target/live-containment/locality-book, on the repository volume.
promotion: declined (the existing canonical reference and direct include retain the lesson).

## _(2026-10-10)_ — repository-volume scratch and discriminating acceptance fixture (LIVE-CONTAINMENT.4d)

The previously owned bare task-acceptance allocator reproduces across12 shell
sites and two Python self-tests. The expanded shell census includes direct
stdout helpers and executable task artifacts:56sites, not the first narrow16.
Guard actual allocation expressions before any foreign write: predecessor44/56
shell and0/2Python; repaired56/56 and2/2, with same-device checks and exact cleanup.
Materials now scopes all20 self-test fixtures under one temporary lifetime.
Synth creates its missing parent and guards allocation before use. Driver/hook/
entrypoints/push boundary constrain child TMPDIR;28 unset/foreign child cases pass.
The push self-test uses its published synthetic-repository interface, never a push.

The published acceptance probes expose CTRL-4b returning GREEN without its
custom declaration. d8c2337 broadened the generic verdict family; WIDGET-COVERAGE
ceased to discriminate the seam. Use widget_evidence_ok outside that family:
10pass/0fail. Ten new SEAM-INTEGRITY controls preserve earlier nine, detect bare
allocators, leaked qualified fixtures and unconstrained children, and run the
whole acceptance probe. Current tracked boxes are reported honestly; no comparison
with their original commits is claimed. Correct stale SHARD-FREEZE display prose
without changing its logical-predecessor contract. Derive39doctrines/728arms/38routes.

Focused11, published acceptance10/0, waiver5/0 and synth6/0 pass. Full CI's first
run passed Rust173/17/253 but refused after a registry prose edit overlapped Bash
reading that file (unexpected EOF). Current syntax is valid; retain ci-first.log
and repeat the complete suite with source files fixed: all five legs pass.
Review then found the new shim's asserts disappeared under optimization; a mock
allocator proves the bypass without a write. Replace all harness asserts with
explicit guards, check parent devices before allocation and add an optimized
negative control. Mock levels0/1/2 now refuse before allocator; SEAM19/0 passes.
Final complete CI after this hardening passes all five legs, including seven books.
Protected runtime/canonical/profile/frozen/fixture/earlier-history/archive populations
remain byte-exact; existing caps and CPU acceptance unchanged. The reference record
states allocator, child-block and legacy-residue limits; no shared cache is deleted.
Evidence target/live-containment/locality, all on the repository volume.
promotion: reference_temporary-allocation-controls.md retains the complete control scope and reproduction.

