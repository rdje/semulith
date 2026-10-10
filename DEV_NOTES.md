# DEV_NOTES.md

## _(2026-10-10)_ — preserve completed task receipts under fixed caps (P4-SYSTEM.13 c26a)

P4 tree123960/131072 B leaves7112 B. Six completed spans total81532 B; archive8
already59436 B, combined140968 cannot fit. Archive9 retains all payload bytes/
order/SHA markers in83418 B; live partition45205 B before new receipt. Inverse
extracts exact payloads, removes only new routes/ownership/receipts, restores
committed5eaef2a source123960 B SHA256
 efd367b86309c45a53ddf736352135e18ea56171f1669d43c43941626c7fb4ac.

partition.py/verify.py rc=0: all prior code/canonical/author/98 registry/generated/
frozen/archive bytes exact, effective96/114 unchanged; explicit new-file/cap
census and all kept segments exact. No Rust changes. Focused gates/all six books rc=0;
hooks next. LIVE unchanged652 arms/49 chapters/P4 12/18. promotion: declined
(established exact inverse; retained in archive9/tree and worked book example).

Own next c26b: cadence refusal still recommends approval-variable-only git push,
but pre-push correctly requires approved_push.sh's record (13266aa guidance vs
ac07ff8 recorded-act enforcement). Reproduced rc=1/contradictory public recovery
text. Fix guidance/behavioral controls next; no real push or approval fabrication.

## _(2026-10-10)_ — observe FENCE fields and preservation (P4-SYSTEM.13 c25)

Authenticated RV32I1.1.7 requires reserved-config acceptance and ignored rs1/rd.
Direct matrix4096 configs × three modes × five register pairs=61440 boundaries,
plus three LR.D/FENCE/SC.D/LD and three translated ADDI/FENCE/ADDI programs.
Full GPR/FPR/26 CSR owner/PC/mode/memory and exact requests preserve reservations
and warm mappings. Direct61461/122922/122934requests; companions39/78 yield
pair61500/123000. POS ordinary/TSO; NEG adversarial accepted forms, not traps.

Ten wrong tables reject; initial mask-control reason was corrected with public
step_over diagnosis: ReservedDecode advances time but not retirement, so CSR
counter comparison fails before final outcome. Actual disabled-GPR observer RED
rc=101, restored; missing-binding RED rc=101 before two Execution entries.
Small provenance defect owned/fixed: STOCK fence's1.1.6 locator introduced by
022f557 points at Load/Store, correct Memory Ordering is1.1.7. Exact one-line
source delta; canonical fault-fence already correct. Independent all61440 words/
full states and six integration programs rc=0; author omits nine data requests,
which public CPU observer judges separately. No architectural defect found.

verify.py rc=0: prior96 entries/112 base+348 GC input/core/generated/frozen bytes
exact; all scripts/author bytes exact except locator. Full167/5365/10524 unchanged.
make check rc=0, Rust167/17/214. Registry98/effective96/114, nine pairs/freeze.
LIVE unchanged652 arms/49 chapters/P4 12/18. Focused gates/all six books rc=0; hooks next.
promotion: declined (finite matrix, masks' retirement distinction and author-log
limits retained in worked memory chapter/tree). c26a task containment next.

## _(2026-10-10)_ — observe implicit Sv39 requests and no-write faults (P4-SYSTEM.13 c24)

Bind WALK-IMPLICIT with 20 actual CPU cases: nine Fetch/LD/SD × one/two/three
levels, two boundaries each; eleven Svade/invalid/refused/noncanonical faults.
Direct total29 boundaries/50 parcels/104 requests. Literal physical paths and
full GPR/PC/mode/status/satp/trap/counters/memory precede CPU execution. Exact
requests distinguish walks, parcels and explicit data; second access hits the
same-page cache. Faults leave all PTE bytes unchanged and stop before data.
Existing three-level CPU boundary/core tests remain; this binds the missing pair.

Seven corrupted-capture controls reject; actual disabled-request observer RED
rc=101. Actual walker Load+D/Response::Load and write-A-before-fault mutations
both RED rc=101 at request predicate, then core bytes restored. Missing-binding
RED rc=101 precedes two Execution entries. Successful walk-as-Load paths
retain state/memory with request guard disabled, rc=0; all-case state-only probe
correctly RED rc=101 because Walk-only refusal is bypassed. Write-A with request
guard disabled still memory-RED rc=101; with request+memory guards disabled,
original trap/state GREEN rc=0. Final restored make check rc=0. Authenticated supervisor/introduction
sources; independent20-case word/path/state/memory/fetch-walk proof rc=0. Author
omits explicit data logs; public observer verifies those. Companions188/376 POS,
255/510 NEG plus direct29/50 yield472/936.

verify.py rc=0: prior94 bindings,112 base/348 GC inputs/core/author/generated/
frozen bytes exact; full167/5365/10524 unchanged. make check rc=0, Rust167/17/212.
Registry96/effective94/114 (13 scope/23 guest/6 boundary/5 execution pairs), ten
runtime pairs/freeze. LIVE unchanged652 arms/49 chapters/P4 12/18. Focused gates/
all six books rc=0. Hooks precede c25. promotion: declined (finite matrix and independent-log limits
retained in worked runtime chapter and tree). c25 FENCE follows clean workflow.

## _(2026-10-10)_ — retain 64-bit user registers and addresses (P4-SYSTEM.13 c23b)

Authenticated RV64I3.1.1 fixes XLEN=64; Sv39 keeps its canonical subset. Two
four-word U/Sv39 programs start at VA 0x100001000/0xffffffff80001000 and map to
PA0x80001000 through one A/D-set user 1GiB leaf each. ADDI retains a high pointer,
LD/SD retain all payload bits, AUIPC retains virtual PC. Literal high-bit sentinels
precede register writes. All GPRs/PC/U/UXL/trap/counters/memory and actual requests
are observed: two cases/eight boundaries/16 parcels/22 total requests.

Seven isolated public effects narrow ADDI/LD/SD/AUIPC/next-PC values or addresses;
all 14 case/control combinations fail. Actual disabled-GPR auditor lets unused
x7 truncation escape (meaningful RED rc=101); restored. Declaration missing-
binding RED rc=101 precedes two Execution entries. Successful walk-as-Load paths
retain state/memory with request guard disabled, rc=0; all-case state-only probe
correctly RED rc=101 because Walk-only refusal is bypassed. Write-A with request
guard disabled still memory-RED rc=101; with request+memory guards disabled,
original trap/state GREEN rc=0. Final restored make check rc=0. Independent author matches
words/PTEs/canonical mappings/GPR/PC/U/memory and fetch/walk logs; it does not
log data requests, which the public CPU observer separately verifies.

verify.py rc=0: prior 92 entries/all 112 base+348 GC input/core/author/generated/
frozen bytes exact; normal full 167/5365/10524 unchanged. Companions 31/62 POS,
89/178 NEG plus direct 8/16 yield pair 128/256. make check rc=0 (Rust 167/17/210).
Registry 94/effective 92/114; eleven runtime pairs/freeze. LIVE_STATUS unchanged
(652 arms,49 chapters,P4 12/18). Focused gates/all six books rc=0; hooks precede
c24 WALK-IMPLICIT. promotion: declined (finite virtual-width/physical-request
separation and author-log limits retained in worked book matrix and owning tree).

## _(2026-10-10)_ — preserve control-transfer witnesses in a bounded chapter (P4-SYSTEM.13 c23a)

Integer runtime chapter reached 31,694/32,768 B (1,074 B room). Move its whole
ordered suffix (immediate transfers, JALR diagnosis and realization) into
contract-control.md, preserving the leading separator and all 9,822 B:
SHA256 d1da14f93bf6f352739edd2a2e784cabd4f782481fb729bc67c2b1fc05b819c0.
Remove only the new navigation/header to reconstruct the original 31,694 B:
SHA256 9beabe26eafc6b026ab8310cddf25f3ca97919ce5787e89536725a62149c7a7b.
Integer/control now 21,969/10,013 B. SUMMARY/index/profile ENV/GS/runtime summary
follow the move; book count 48→49, fixed caps unchanged.

verify.py rc=0 proves inverse, all 92 registry/core/author/generated/frozen bytes
and 112 base/348 GC canonical/guest inputs exact. Explicit new-file census 51
under 80 files/524,288 family bytes/32,768 part caps. Effective90/114 unchanged;
no Rust code changed. LIVE_STATUS changes only book chapters 48→49, doctrine 652
arms/P4 12/18 unchanged. Focused gates/all six books rc=0; hooks precede then c23b
XLEN and remaining runtime pairs/freeze. promotion: declined (existing bounded
suffix-move protocol; exact inverse and ownership retained in tree/book navigation).

## _(2026-10-10)_ — observe JALR targets and links directly (P4-SYSTEM.13 c22b2)

The old GC comparison admits base-JALR bit-1 erasure across all 167 guests.
Bind literal Execution POS/NEG after declaration missing-entry RED rc=101.
Fifteen direct cases cover ordinary/odd targets, immediate limits, carry before
masking, negatives, wrap, high bits, aliases, x0 and two next-fetch faults:
17 boundaries/32 actual parcels. All GPR/PC/mode/trap/counters/requests/memory
are observed; companion guests add 36/71, making the pair 53/103.

Eight incorrect public effects fail named observations. A source-disabled PC
observer lets bit-1 erasure escape (meaningful test RED rc=101); restore GREEN.
Reordering link before target alone is equivalent: Frame snapshots register
reads before all effects. Investigated the initial invalid control, retain its
GREEN result and explicitly use the new link as the aliased base for the RED.
No production CPU/author/generated/canonical change. Prior 90 bindings exact;
independent direct 15/17/32 and full 167/5365/10524 replay/identity rc=0.

make check rc=0 (Rust 167/17/208). Registry92/effective90/114, twelve runtime
pairs/freeze remain. Focused gates/all six books rc=0; hooks precede c23a book
containment then c23b XLEN. Integer chapter 31,694/32,768 B; retain every
witness byte in the next split. LIVE_STATUS unchanged (652 arms,48 chapters,P4 12/18).
promotion: declined (finite target/request distinction and equivalent-mutation
root diagnosis retained with worked examples in book/tree).

## _(2026-10-10)_ — correct inherited IALIGN evidence and own JALR target gap (P4-SYSTEM.13 c22b1)

Six GC source/expectation files for fault-jal-mis, fault-jalr-mis and it-prio-jump
retain base IALIGN=32 trap/no-link prose despite current GC link writes. Import
133e722 copied it; 2611340 added parcels but retained derivations. Full relevant
source histories audited (base roots a199ccf/25862a2). Authenticated RV32I/C
sources confirm IALIGN=16 halfword targets. Correct prose and last it-prio-jump
mnemonic to <fetch fault>; historical basenames and base input files stay fixed.
Literal final states reproduced through independent author and public CPU.

An isolated public BASE JALR table masks with ~3 instead of ~1; all 167/5365/10524
old observations still pass. fault-jalr-mis final PC 2→0; it-prio-jump fault
EPC/tval40000002→40000000. The GC rule lacks these observations. Production
is correct. Own priority-next c22b2 direct target-state witnesses before credit.
The initial census's dir-chain candidate has no JALR; actual six-guest census
and finite limits are in task/book. Do not treat this diagnostic as a realized pair.

Identity rc=0: 112 base exact; 342 GC exact plus six annotation-only changes, all
images/numeric writes/budgets unchanged. Generated Rust differs ONLY by six input
hash strings; executable arrays byte-exact. All 90 registry/core/author/frozen
bytes exact; effective 88/114 unchanged. Normal full167/5365/10524 rc=0; make check
rc=0 (Rust167/17/206). GUEST-GEN rc=0 (147/0 self-test); make ci rc=0 (all five legs, including
all six books). Hooks precede c22b2.
LIVE_STATUS changes only doctrine arms 650→652 (48 chapters / P4 12/18 unchanged). promotion: declined
(worked target/observation distinction and priority repair retained in book/tree).

The first GUEST-GEN run refused source annotations (142/145 pass). Its governor
now pins exactly three reviewed base/GC source pairs and independently requires
identical assembled images. Stale exceptions and changed owner/mirror pins or
instructions refuse; two isolated bypass mutations fail. All other source bytes,
seven expectation exceptions and write/parcel checks remain governed.

## _(2026-10-10)_ — retain whole development receipts (P4-SYSTEM.13 c22a)

Live notes reached 47,462 B under fixed 49,152 B cap. Existing sharder targets
32,768 B: 20 entries=13 kept+7 moved, head 31,228 B. New shard 0224 preserves the
16,234 B ordered suffix, SHA256 0ad12ca063f04407f2aee04a06b2bec7a250050fc9135d5f8044f0bed7631af1.
Remove only this new note/footer and concatenate kept+shard entries to recover
47,462 B SHA256 8f3064fc70b5929072632f333171ba281d77a926a512013ae3d827f2a9277a46.
Old manifest prefix/sealed history exact; one appended row, 226 logical frozen
shard rows. Runtime/canonical/guest/registry/frozen bytes exact; 88/114 unchanged.
Inverse/no-op rc=0; focused gates and all six books rc=0, including 226 frozen
rows, six derived claims and 40 index rows. Hooks then c22b JALR-LSB. LIVE_STATUS unchanged (650 arms, 48 chapters, P4 12/18).
promotion: declined (existing whole-entry containment protocol; exact proof in
owning task and book example).

## _(2026-10-10)_ — require immediate architectural transfers (P4-SYSTEM.13 c21b)

NO-DELAY-SLOTS was declared/unbound. Authenticated RV32I 1.1.5 and all eight
requirement associations reviewed. POS guest-control/c-branches and NEG
scope-branch/dir-cmp-branch/c-links retain exact 63/111 observations. Base skipped
writes pin x6/x13, x20–x24 and x8; not-taken fall-through remains visible. C
programs add five compressed control forms and mixed 2/4-byte lengths.

Thirteen isolated author drivers defer one named taken transfer until after one
actual instruction, preserving correct link values. All fail named observations.
A separate public-CPU delayed-PC driver reproduces all thirteen first differences;
normal driver matches writes, never-written markers and fetch counts. Book retains
the matrix. No production/author/guest change or pipeline implementation claim.
Declaration test first missing-entry RED rc=101; then exact two Guest bindings.
make check rc=0 (Rust 167/17/206). Independent probes/full 167/5365/10524 rc=0;
prior 88 bindings/112 base+348 GC inputs/core/author/generated/frozen identity rc=0.
Registry 90, effective 88/114: scope 13/guest 23/boundary 6/execution 2 pairs; thirteen
runtime pairs/freeze remain. LIVE_STATUS unchanged (650 arms, 48 chapters, P4 12/18).
Focused gates/books rc=0 (shards, fixed bounds, frontiers, six derived claims,
frozen contracts, fresh reports, schema, main+five model books). Hooks precede
c22a live-note containment, then c22b JALR-LSB.
promotion: declined (ordinary control-flow discrimination and finite limits
retained with exact witnesses in integer book and owning tree).


## _(2026-10-10)_ — keep memory witnesses in a bounded book chapter (P4-SYSTEM.13 c21a)

The integer chapter reached 32,287 B against fixed 32,768 B per-part ceiling,
leaving 481 B for future runtime work. Book family has 49 tracked files, not its
80-file cap, and 448,559 B against 524,288 B. Move LOAD-EXT/LOAD-X0/ENDIAN as an
ordered suffix into contract-memory.md, preserving every section and separator.
The suffix is 10504 B, SHA256 098a50b7a66bd45c39c91dbf5a73025e75f7720c16a2397a00ef61db9d241109.
Remove only the new navigation line and chapter header to reconstruct the exact
32,287 B original, SHA256 37589ade3b38e2065f8399cb7f475d74b0c2209636b33e836aa69a6629f64c28.
Integer/memory chapters now 21,872/10,782 B; caps unchanged. SUMMARY, index,
profile pointers/GS report and current runtime summary follow the split.

`python3 target/p4-system-13/c21a/verify.py` rc=0 verifies inverse and all prior
88 registry/core/author/generated/frozen bytes plus 112 base/348 GC canonical/
guest inputs. Effective 86/114 unchanged; no Rust code changed. LIVE_STATUS
changes only book chapters 47→48, doctrine arms 650/P4 12/18 unchanged. Focused
gates and main+five model books rc=0, including six derived claims and 40 index
rows. Explicit new-file census: 50 files/449,248 B, fixed caps hold. Hooks then
c21b NO-DELAY-SLOTS.
promotion: declined (lossless partition under existing fixed containment policy;
source/suffix/inverse hashes retained in this entry and owning task).


## _(2026-10-10)_ — discriminate the selected little-endian byte lanes (P4-SYSTEM.13 c20)

OB-ENDIAN was declared but unbound. Authenticated RV32I 1.1.6 delegates the
choice to the EEI and requires byte-address invariance; canonical profile chooses
little-endian. POS scope-mem and NEG dir-ext-matrix independently match 64/128,
all seven integer load/four store forms. The NEG matrix stores sign-edge values
then reads different widths/addresses. It distinguishes a pair of wrong read/
write orders that a same-width round trip might hide.

Nine isolated author controls reverse each LH/LHU/LW/LWU/LD, SH/SW/SD, or both
directions. All fail NEG at named steps; SH-only reversal survives scope-mem's
all-ones store, while SW fails its later pattern at step 28. A separate public
client reverses H/W/D provider reads/writes/both: nine more NEG refusals. Byte
reversal changes neither selected guest; all 256 public byte values keep their
address/value. Existing literal DataAccess witnesses give provider composition
context; no new core/author/guest semantics or configurable endian mode.

Declaration check observed missing-entry RED rc=101 before registration. Exact
two Guest bindings pass make check rc=0 (Rust 167/17/206). Independent author/
public probes rc=0, full 167/5365/10524 normal replay exact; identity rc=0 for all
prior 86 bindings and 112 base/348 GC inputs/core/author/generated/frozen bytes.
Registry 88, effective 86/114: scope 13/guest 22/boundary 6/execution 2 pairs; fourteen
runtime pairs/freeze remain. Book retains lane values, controls and limits.
LIVE_STATUS unchanged (650 arms, 47 chapters, P4 12/18). Focused gates/books rc=0 (shards, fixed bounds, frontiers, six derived claims,
frozen contracts, fresh reports, schema, main+five model books). Hooks precede
c21a book partition under fixed cap, then c21b NO-DELAY-SLOTS.
promotion: declined (ordinary lane/symmetry reasoning retained with worked
observations in the integer book and owning task).


## _(2026-10-10)_ — require x0 load requests and delivered faults (P4-SYSTEM.13 c19)

The GC mirror's shared corpus rule compares register changes, never-written
registers and fetch counts; neither final trap state nor data requests is judged.
Root is the route flip/mirror at 133e722 (base fault fixtures originate a199ccf;
registry reuses that rule from 072b211). Base-specific crossing/fault assertions
remain valid. Isolated author and independent public conditional bad table both
skip loads only when rd=0 and still satisfy all 167/5365/10524 old observations,
including the two fault guests. Their cause/EPC/tval/PC/retirement actually differ:
book retains exact before/after values. Own and resolve this previously uncredited
LOAD-X0 witness gap here; no core misbehavior was found.

New literal public-interface cases cover all seven load encodings: seven success,
seven access refusals, five misalignments and seven Sv39 invalid-root page faults.
Audit exact width/address request sequence, GPRs/x0, PC, mode, cause/EPC/tval,
cycles, retirement, parcels and memory. Page faults require the implicit root
walk and no explicit Load. Direct 26/52 plus unchanged companions 52/104=78/156.
Seven erased and seven duplicate tables refuse; each erased form also fails each
applicable fault case. Disabling the request observer causes the terminal control
to fail rc=101; restoring it passes. Disabled access-fault injection also refuses.
Declaration test first missing-entry RED rc=101, then two exact Execution bindings.

make check rc=0 (167 core/17 DSP/206 verify). Independent author/public probes
rc=0; exact prior 84 registry entries and 112 base/348 GC input files, core,
definitions, author, generated data and frozen records verified rc=0. Registry 86,
effective 84/114, fifteen runtime pairs/freeze remain. LIVE_STATUS unchanged:
650 arms, 47 chapters, P4 12/18. Book retains matrix, root cause and finite limits.
Focused gates/books rc=0 (shards, fixed bounds, frontiers, counts, frozen contracts,
fresh reports, schema, main+five model books). Hooks precede c20 ENDIAN.
promotion: declined (the worked
request/trap distinction and controls remain in the integer book and owning tree).


## _(2026-10-10)_ — authenticate citation evidence at both readers (P4-SYSTEM.13 c18c)

Actual locator/quote readers both returned rc=0 on three fetched RISC-V HTML
pages whose hashes differed from the source ledger, despite identical lengths.
Full byte diff isolates one Antora UI-version metadata value per page; architecture
text unchanged. The snapshot matches exact pins. The failure is reader identity,
not an ISA disagreement: published read headings without checking bytes, and
quote corpus used the same preferred fetched route. History roots: 32b72dbc's
reader, 3afd2757's route, bf2070a7's quote consumer. SEMANTICS also gated locator
work only on cache availability; cache failures could become an absence skip.

Shared verified_source now requires a regular file, valid SHA256/byte-length pin,
exact length and exact digest before either reader uses a page. Both paths refuse
alteration and malformed identity clearly; no silent fallback or repin. Shared
presence-only dispatch checks fetched-only data, treats partial/corrupt evidence
as present and permits a named skip only for absence. Cache resolution errors
propagate; quote entrypoint distinguishes source refusal from a text mismatch.
Non-snapshot http_status=0 handling and explicit synthetic --pages interface stay
unchanged. Locator controls run with SEMANTICS. All self-test scratch now derives
from target/doctrine-selftest; synthetic root paths are relative, not serialized
absolute paths. Correct the old pre-integration "not a commit gate" docstring.

Observed new controls against old code: locator 15 pass/3 fail (same-size text,
wrong length, absent identity), quote 14/1 (default-corpus changed bytes accepted).
After repair: locator 21/0, quote 15/0, SEMANTICS 8/0. Actual mismatched pages then
refuse through locator/quote tools and both wrappers (rc=1/2/1/2), naming source
and sha256. Seven route cases cover total absence, fetched-only, cache-only,
changed preferred source with valid fallback, quote integration, changed cache
page with valid manifest and corrupt manifest. No named skip hides corruption.

Authenticate snapshot manifest and all 72 files (0 failures), save/verify the old
three fetched pages on-volume, prove metadata-only diff, restore exactly 3 files /
226648 B and rehash against unchanged ledger. Public locators resolve 10 files/
12 bindings; quote corpus 118 attributed, 0 findings, 88 unattributed, two named
non-HTML source IDs (three instances). All 84 registry entries, production/core/
author/generated/frozen and 112 base/348 GC input files remain exact; 82/114 unchanged.
make ci rc=0, all five legs green (Rust 167/17/203, doctrines, bench, smoke bench,
main+five model books). Focused identities/controls/routes also rc=0. LIVE_STATUS
changes only doctrine arms 649→650; 47 chapters/P4 12/18 unchanged. Next c19 LOAD-X0.

Promoted to [a-version-string-is-not-an-identity](docs/knowledge/a-version-string-is-not-an-identity.md)
and its index: authenticating at acquisition does not authenticate a later reader;
presence dispatch must never turn corruption into absence.

## _(2026-10-10)_ — realize load extension and low-bit stores (P4-SYSTEM.13 c18b)

Bind LOAD-EXT POS scope-mem, NEG bound-ext/dir-ext-matrix, all eleven forms and
111 boundaries/222 parcels. Literal sign-edge arithmetic pins 8/16/32 widths on
both sides and unsigned partners; zero LB visibly overwrites -1. Wider reads
observe narrow stores leaving higher lanes zero, full SD/LD preserves the pattern,
and cross-width high lanes use the read width's sign. Non-clamping source values
distinguish truncation from saturation.

Before credit, seventeen isolated author copies fail committed observations:
signed LB/LH/LW zero-extension at scope-mem steps 12/14/16; unsigned LBU/LHU/LWU
sign-extension at steps 13/15/17; LD low-word18; SB/SH/SW high-bit selection at
bound-ext steps 23/28/33, overwide writes at scope-mem steps 22/24/26, saturation at
bound-ext steps 42/44 and scope-mem step 28; SD low-word at scope-mem step 17. Public registry gate
first fails the missing LOAD-EXT entry (rc=101), then both bindings run. Normal
full independent replay is 167/5365/10524 exact; Rust 167/17/203 passes make check.
Only registry/tests, review docs and derived GS change; every prior 82 entry and
112 base/348 GC canonical+guest inputs, production core/author, generated data and
frozen definitions remain exact. Effective 82/114, registry 84, sixteen pairs/freeze
remain. NEG is a legal semantic counterexample, not an invented trap.

Source review found fetched RV32I/RV64I bytes differ from ledger digests, with
same lengths. Exact diff is one Antora UI-version meta value per page; the local
snapshot matches both pinned hashes, and its full relevant sections supplied this
review. check_citations._work_dir prefers any fetched directory; published reads
without digest checks, and quote reader uses the route directly. Owned priority
c18c repairs both evidence paths immediately after this commit, before further
runtime pairs. No architecture-body or processor mismatch; no repin or silent
fallback authorized. Details/reproduction and repair schedule are in the task.

Focused identity/reports/freeze/schema/bounds/counts and main+five model books
pass (rc=0). Required hooks precede c18c. The first hook refused the combined
acceptance box; split ROOT CAUSE/ADDRESSED/NO REGRESSION into distinct ticked
boxes with their own actual tool results, then rerun the required hook.
LIVE_STATUS unchanged: 649 arms/47 chapters/P4 12/18. .14 retains status/experiment work.
promotion: declined (worked matrix and finite controls live in the integer book; the separate identity defect is owned with immediate repair in the task).

## _(2026-10-10)_ — bound live history and correct current summary pointers (P4-SYSTEM.13 c18a)

Move eight oldest whole DEV entries through shard_history into shard-0223; old
21 entries = 13 live + 8 moved, exact order/bytes. Head 46093→31607 B before this
new note; inverse SHA 0f5b1aae5a4f4d5db4c98a64935d5d5c98b5cc1d2d1dc360bae49b502c92167f.
Manifest 15 live rows, 225 logical with sealed history; old prefix/index untouched.
A new navigation footer follows the preserved tail separator. Removing only that
footer and this new entry restores the exact old-head inverse.

Move completed c17a–f designs/diagnosis, acceptance, verification, commit and
changelog blocks verbatim into archive 8: 16048/13941/1758/904/2093 B. Task
88963→54940 B at partition; ordered inverse SHA
6dc33f903c724b56063445e4d3c162b5e5f06d0673fe0a0ba7c959443bf1bac7.
The ownership plan was the sole pre-partition addition; every moved block matches
committed d5519fb. Also move 22982 B of appended profile progress (SHA
8702aa8818fd213186bdafcf103cb513ad2cb26df70904d5bc2753d1c6b3e184).
Archive payload markers declare exact byte lengths/hashes; all six re-read exact.
The archive is 59436 B, below the fixed 131072 part cap; archive 7 stays untouched.
Current profile keeps normative interface sections, canonical/GS/registry/book
pointers and history link. Historical "current" labels retain their source context
inside the explicitly historical archive, not live authority.

Scoped review also found duplicated summaries that escaped append-only progress:
ENV intro v2=11 and runtime count76, old frozen-v1 STIP source, and book intro64.
Canonical probe gives 12 members and 80/114, with v2 STCE-selected software/
comparator pending. Blame locates member row at e0f3daea, count76 at 01154383,
old boundary source at 75c20ff0, book64 at c0507d02. Correct the effective source,
remove the stale self-currency phrase, label v1 bindings historical, and route
live totals to canonical membership/derived report/current book summary. The
archived old runtime table remains exact for audit; all current feature examples
stay in the book. No production, frozen-record or contract-credit change.

Focused partition/source identity, shard freeze/bounds/frontier/counts/contracts/
reports and main/model books all pass (rc=0). The new frozen shard intentionally
retains its source entry’s trailing blank line: exclude only that byte-proven file
from diff whitespace review; every other changed file passes. LIVE_STATUS
remains 649 arms/47 chapters/P4 12/18, effective 80/114. c18b load matrix next.
promotion: declined (byte-authenticated archive payloads, canonical/derived pointers and existing containment doctrine retain the proof and prevent duplicate summary drift).


## _(2026-10-10)_ — realize signed word results and ignored overflow (P4-SYSTEM.13 c17f)

Bind WSUFFIX POS scope-alu/bound-arith, NEG bound-shiftw: all nine RV64I forms
in REQ-D-WSUFFIX over 122 boundaries/244 parcels. M's five word forms retain
separate existing M evidence. Sixteen isolated author copies fail named
observations before credit: nine zero-extended results, four full-width right
sources, three signed-32 saturating add/subtracts. Zero-extension first fails
ADDIW bound-arith 17; SLLIW bound-shiftw 41; SRLIW 34; SRAIW scope-alu 29;
ADDW scope-alu 23; SUBW bound-arith 20; SLLW bound-shiftw 53; SRLW 51;
SRAW scope-alu 27. Source-width errors first fail SRLIW scope-alu 28, SRAIW
bound-shiftw 59, SRLW scope-alu 26, SRAW bound-shiftw 58. Saturation fails
ADDIW bound-arith 17, ADDW 19 and SUBW scope-alu 24. Shared finishes condition
only the named mnemonic; every other expression stays unchanged.

ADDIW on 0xdeadb7ef7fffffff plus one ignores the upper word and wraps to
0xffffffff80000000; zero-extension gives positive 0x80000000, saturation
0x7fffffff. SUBW on INT32_MIN minus 1620 wraps to positive 0x7ffff9ac, whereas
saturation stays INT32_MIN. Right-shift source width matters; for add/subtract
and left shift, pre-truncation commutes with a correct final low32 truncation,
so equivalent rewrites are not misclassified as faulty countermodels.

Registry 82, effective 80/114: thirteen scope/twenty guest/six boundary/one
execution pairs, seventeen runtime pairs/freeze remain. Make check passes
fmt/clippy and Rust 167/17/203; normal selected/full corpus exact 167/5365/10524.
Identity preserves all 112 base/348 GC canonical/guest files and prior 80 entries,
production/core/author/definitions/generated/frozen bytes. Integer probe retains
23 arithmetic/10 branches, 17 gaps/476 steps, 42 owned records; guest generators
49/167 fresh, mirror 49 with 42 count migrations/7 explicit re-derivations.
Five reports/count claims, three frozen versions/zero findings, schema 270/two
named skips, 37 bounded routes and main/model books pass. LIVE_STATUS unchanged
649 arms/47 chapters/P4 12/18. No live reference rerun for unchanged inputs/rules.
Next c18a losslessly contains near-ceiling DEV/profile history, then c18b loads.
promotion: declined (canonical independent witnesses, executable registry pair and integer runtime chapter retain the signed-word guarantee).


## _(2026-10-10)_ — complete SHAMT requirement associations (P4-SYSTEM.13 c17e)

The original base associations (1abba2e) omitted SLLW/SRLW/SRAW; GC copied the
nine-form list at b95af58. The statement already names all twelve. Aggregate
extraction still covers the omitted forms through WSUFFIX, hiding the individual
requirement's missing associations. Two focused owner/mirror assertions query
canonical catalogs and compare the complete twelve-form list; observe cargo test
rc101 / 0 passed / 2 failed BEFORE data repair. Both diagnostics print nine
actual names against twelve expected. Add only the three insns fields to
REQ-D-SHAMT in both catalogs; then the same command passes 2/0. Order does not
matter; duplicates fail. Shared catalog client preserves the old obligation
query/caching behavior while serving the two flat requirement catalogs.

No statement/status/obligation/instruction/expectation change. Identity proves
every other requirement field/record and 111 other base/347 other GC inputs exact;
production/core/definitions/generated/frozen/80 registry entries exact. Re-pin
base dossier 267e8e23…a55f → f9246561…a8dc after profile documentation; regenerate
board/platform/model/report owners. Eight board data documents retain all other
values, with only shared pin and the three associations in its composed requirement
changed; map/four model material bodies retain all but display pin/provenance.

Make check passes fmt/clippy and Rust 167/17/203. RECORD-SCHEMA validates 20 files
and the Rust graph examples, EXTRACTION five units sufficient, five reports
fresh, freeze three versions/zero findings, dossier schema 270/two named skips,
materials five units, derived counts five claims, bounded routes 37 and main/model
books pass. LIVE_STATUS unchanged at 649 arms/47 chapters/P4 12/18; effective
78/114 unchanged. The association defect is closed, c17f word-result review next;
.14 retains statuses/experiment/registration work. No reference rerun is needed
for metadata-only changes: all execution inputs and rules remain byte-exact.
promotion: declined (two refusing cross-record assertions and integer runtime chapter retain the association repair and history root).


## _(2026-10-10)_ — realize all twelve shift-count domains (P4-SYSTEM.13 c17d)

Bind SHAMT POS to scope-alu and NEG to bound-shift/bound-shiftw: 180 boundaries /
360 parcels. The frozen statement and pinned RV64I 3.1.2.1–2 specify six bits for
XLEN immediate/register counts, five for word immediates and low-five rs2 for
word registers. Twelve isolated author copies each change one mnemonic count
expression; all fail before credit. XLEN five-bit copies first fail SLLI
bound-shift 1, SRLI 35, SRAI 73, SLL 87, SRA 88 and SRL bound-shiftw 49. Four-bit
word-immediate copies fail SLLIW bound-shiftw 46, SRLIW scope-alu 28, SRAIW 29.
Six-bit word-register copies fail SLLW scope-alu 25, SRLW bound-shiftw 51 and SRAW 55.
The repaired SRAW count-96 witness now independently closes its old masking gap;
source-width witnesses remain exact. These legal counterexamples invent no traps.

Add only two registry entries and their declared-check closure: registry 80,
effective 78/114, thirteen scope/nineteen guest/six boundary/one execution pairs.
Eighteen runtime pairs/freeze remain. Make check passes fmt/clippy and Rust
167/17/201; integer probe retains 23 arithmetic/10 branches, 17 gaps/476 steps,
42 owned records exact. Full independent author corpus is 167/5365/10524 exact.
Byte comparisons preserve all 112 base/348 GC canonical/guest files, prior 78
registry entries, production/core/definitions/generated/frozen data. Freeze
three versions/zero findings, schema 270/two named skips, five fresh reports,
five derived counts, 37 bounded routes and main/model books pass. LIVE_STATUS
stays 649 arms/47 chapters/P4 12/18. Profile/book/resume report the new pair.

Scoped requirement review found REQ-D-SHAMT's insns fields omit SLLW/SRLW/SRAW
in BOTH owner and GC mirror, although its statement explicitly covers all twelve.
Record probes confirm 9/12; git log -S and git show locate incomplete base
associations at 1abba2e and the GC copy at b95af58 (original d3fecbf had none).
WSUFFIX covers the three in aggregate extraction, hiding per-requirement metadata
incompleteness. No execution/frozen-statement defect. Own c17e metadata repair
immediately next with a refusing closure assertion and dependent regeneration;
keep this binding's exact-input proof bounded. c17f WSUFFIX follows; .14 retains
statuses/structured experiments/registration work.
promotion: declined (canonical witnesses, executable registry pair and integer runtime chapter retain independently discriminated count domains).


## _(2026-10-10)_ — distinguish arithmetic-W source width (P4-SYSTEM.13 c17c)

The separate width diagnosis showed both isolated full-width arithmetic-W authors
survived every old corpus observation: all 38 source occurrences already were
canonical signed words. Both public literal forms on zero-extended 0x80000001 by
one distinguish correct 0xffffffffc0000000 from bad positive 0x40000000.

Append four pre-derived instructions to both bound-shiftw programs: AND obtains
x17=0x0000000080000001 from x8/x12; ADDI sets x18=1; SRAW x19,x17,x18 and SRAIW
x20,x17,1 each require 0xffffffffc0000000. Literal words are 00c478b3, 00100913,
4128d9bb and 4018da1b at 0x800000e0/e4/e8/ec, recorded before models execute.
All 56 old instruction positions/bytes/observations stay exact; budgets become
60 steps, base 60 word requests / GC 120 parcels. Each isolated wrong author now
fails only its new boundary (58/59); public wrong tables first fail there too.

Existing hand-encoded garbage-upper-word cases already discriminate both rules.
Add isolated sraw-width/sraiw-width mutation routes, observe each rc1 with its
named arithmetic-word reason before arm registration, then register two controls.
Normal probe retains 23 arithmetic/10 branch cases and 42 owned records exact;
17 gaps now have 476 steps. Derived doctrine total becomes 649 (GUEST-GEN 145).
The independent full corpus matches 167/5365/10524; make check passes Rust
167/17/201, fmt/clippy. Fresh pinned Sail agrees on all 60 declared rows/change
observations and repeats byte-identically. Base live smoke passes all enabled
comparisons/reproductions, including the changed program against Sail and Spike.

Identity proves 110 other base/346 other GC inputs, production/core/definitions,
frozen records/78 entries and all other generated guest data exact. Re-pin shared
base dossier df48b3a6…f38a → 267e8e23…a55f through the declared board definition;
eight board S-expression data documents retain every other value; map/four
material bodies change only display pin/provenance. Derive all five reports and
both model-book units, including base expected-step total 644→648. Freshness,
freeze (three versions/zero findings), schema (270/two named skips), counts (five
claims), main/five model books pass. Both source-width evidence defects close;
core rules stay correct and unchanged, effective credit stays 76/114. c17d SHAMT
binding follows isolated mask controls. Finite reference/platform limits remain.
promotion: declined (durable isolated controls, derived guest boundaries and integer runtime book retain the verified repair).


## _(2026-10-10)_ — close SRAW mask discrimination with a pre-derived boundary (P4-SYSTEM.13 c17b)

Append SRAW x16,x8,x10 = 0x40a4583b at 0x800000dc to both bound-shiftw profiles.
Existing x8=0xffffffff80000001 and x10=96 give count zero; literal expected x16
is 0xffffffff80000001, recorded before either engine executes. Preserve all 55
old instruction positions/bytes and observations. Budgets become 56 steps, base
56 word requests / GC 112 parcels. Correct SRLW step 51's explanatory six-bit
alternative to zero in the explicitly defined wide evaluator; its required
expected identity remains unchanged. No production instruction rule changes.

The isolated SRAW author now fails only new boundary 55; public step_over bad
table also fails there (rc101). The normal independent corpus matches all 167
guests / 5361 boundaries / 10516 parcels. Add one hand-encoded count-96/garbage-
upper-word case and isolated sraw-count mutation to the durable integer probe.
Observe rc1 with SRAW five-bit count before registering the GUEST-GEN arm.
Normal probe: 23 arithmetic/10 branches, 17 gaps/472 steps, 42 owned records exact.
GUEST-GEN 143, global arms 647. Fresh pinned Sail agrees on 56 declared rows and
change observations; two traces byte-identical, including the added SRAW.

Identity keeps 110 other base and 346 other GC canonical/guest files, all core,
definitions, production author, frozen records and 78 entries exact. Both Rust
guest fixtures retain every other guest datum byte-exact. Re-pin base dossier
from 9f7cecb3…d784 to df48b3a6…f38a, regenerate board/platform/model-book outputs;
parsed board data stays exact except the pin, map/material bodies except display
and provenance. Rust make check passes 167/17/201; focused gates and final make ci
pass all five legs (check, gate, bench, smoke-bench, main/model books).
SRAW count-mask coverage and SRLW explanatory defects closed,
no new contract credit: 76/114, nineteen pairs/freeze remain. Initial CI refused
the base material's old 643 expected-step total; second refused G0/G1's matching
old totals. Re-derive through the owners; fresh base live smoke rc0 verifies all
enabled comparisons, including bound-shiftw against Sail/Spike over 56 steps.

Adjacent width review confirms a separate evidence defect, OPEN priority-next
c17c before c17d SHAMT binding: isolated SRAW and SRAIW full-width source authors
each match the entire 167/5361/10516 corpus. Public bad tables match 105 boundaries;
all 38 arithmetic-W source occurrences already are canonical signed words.
Both literal SRAW/SRAIW with x8=0x0000000080000001 and count one distinguish
correct 0xffffffffc0000000 from bad 0x40000000. The current count-zero witness
cannot test pre-shift truncation. Core correct; add derived witnesses and durable
isolated controls next. Task and integer book retain the diagnosis and ownership.
promotion: declined (durable author case/refusing control, boundary guest and integer runtime book retain the verified repair).


## _(2026-10-10)_ — diagnose SRAW mask coverage and retain bounded evidence (P4-SYSTEM.13 c17a)

Before registering SHAMT, isolate SRAW's five-to-six-bit count mutation in a
spec-side author copy. It still matches all 167 guests / 5360 boundaries /
10514 parcels. The public step_over API with a caller-supplied mutated SRAW
Sem tree also matches all three SRAW-bearing programs / 104 boundaries.
Root: count 20 gives the same mask; -1 shifts the negative word by 31 or 63
to all-ones; remaining destination is x0. Immediate SRAIW sweeps do not
exercise this register-count distinction. Core semantics are correct; corpus
coverage defect OPEN and owned priority-next c17b, before c17c binding.

Hand-encoded SRAW x16,x8,x10 = 0x40a4583b, x8=0xffffffff80000001 and x10=96,
yields x16=0xffffffff80000001 under the correct count-zero rule, all-ones under
the six-bit/count-32 copy. Both independent author and public core agree.
Also diagnose SRLW step 51's explanatory alternative: widening its count in
the present wide evaluator yields zero, not the old prose's 0xffffffff80000000.
The existing correct expected value is unchanged. c17b adds the pre-derived
SRAW boundary to both profiles and corrects only the misleading explanation.

Before further evidence growth, shard CHANGELOG's oldest 35 entries to 0221
(101=66+35) and DEV_NOTES's oldest 13 to 0222 (28=15+13). Ordered inverse byte
identity hashes: 27d7e70f97cba0f6100be7bf89bf0959831fcb4e00f598d2b9eee36ccff91d92
and 68c5290cc5d653f6cba04960ddd190eaf4e3b726c06dfed2f5ff8941f28c9526.
Manifest now fourteen shards; no sealed archive descriptor changes. Move fourteen
each of completed c8–c16 designs, acceptance, verification, commit and changelog
blocks byte-verbatim to task archive part 7; full inverse hash
0a208867adf4e332fca70d2d9c19639030425778c244667024acd4a2451b552c.
Task 126431 to 53929 B at partition, archive 125593 B under fixed 131072 cap.
Move 6973 B of completed integer book sections exactly (SHA256
c6c65a32bb94ea55c25ed01d2c27a13c8d07236d882d0de36e016f045562f30d)
into a linked chapter, retaining old anchor routes. Add diagnosis and repair
ownership there; chapters 46 to 47, the only changed LIVE_STATUS metric.
All production/core/author/guest/canonical data and 76/114 credit remain exact.
SHARD-FREEZE passes 224 logical rows/two heads; bounds 37 destinations, frontier
33 trees, five derived claims, freeze three/zero findings, five fresh reports/
20 controls and main/model books pass. Post-edit history/book comparison retains
every old byte in order. Commit hooks precede priority-next c17b.
promotion: declined (integer runtime chapter and scheduled task retain the diagnosis; c17b owns durable controls and repair).


Earlier entries: [history manifest](docs/changelog/SHARDS.sha256).
