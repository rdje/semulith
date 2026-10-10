# DEV_NOTES shard — _(2026-10-10)_ … _(2026-10-10)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-10)_ — ground FP-state claims in public evidence (P4-SYSTEM.13 c29b)

Scoped exec review found fdext_control.sail:19/wF implementation references.
FP book twice says Dirty only on actual value changes, unlike its own
write-Dirty operator paragraph/current evaluator. Source history dd9bc1c ported
those comments. Authenticated RVP-MACHINE2.1.1.6.7 explicitly permits Dirty on
unchanged f/fcsr writes; the laboratory selects every f-register write.

Diagnose.py rc=0: independent12-step same-value write before CPU; temporary
core probe observes identical f1 bits with FS Dirty after FMV.D.X, and Clean
after read-only FMV.X.D. Initial scratch comparison confused raw CSR owner
with computed architectural view; corrected to privilege::csr_read before
credit. Source restored SHAab6cdb46…170017a. Public12/24parcels AGREE twice;
wrong Clean expectation DIVERGE10. Existing24 FP guests/927 boundaries AGREE
in two identical traces each. Machine/F/D ISA and binary pins authenticated.

Two evaluator comment repairs, two book dirty-sentence corrections and a
reference-backend assumption replaced by scoped public-observation limits.
Exact declared text delta/all non-comment Rust lines preserved. Entire profiles/
reports/canonical/author/generated/registry104/frozen/archive bytes exact;
independent167/5365/10524 unchanged. make check rc=0 Rust167/17/223; focused/
all six books in tree. No policy/behavior or contract credit change (102/114).

C29b1 owns DEV sharding before source-prose/provenance c29c (additional state
internal names and stale F requirement detail). C29d owns bounded book history
containment before remaining runtime features; fixed ceilings stay unchanged.
Evidence: target/p4-system-13/c29b and worked floating-point book.
promotion: declined (existing published-interface policy; the identical-value/read-only/wrong-Clean controls and book retain the diagnosis).


## _(2026-10-10)_ — ground atomic rationale in public evidence (P4-SYSTEM.13 c29a)

Scoped history:1c554fc introduced reservation.rs internal Err/cancellation-site
claims;495b4b8 ported the SC evaluator commentary. Replace those explanations
and the reset-site aside with ISA/declared profile choices. Book no longer calls
trap preservation a universal specification invalidation rule. Clarify failed
SC explicit Load/Store exclusion separately from prior WalkAccess reads.
Only standalone Rust comments change, with exact declared text deltas and all
non-comment lines byte-identical. No semantic-source/generator changes needed.

Public.py rc=0: all12 original A guests fresh, pinned binary/unchanged override;
11AGREE/290boundaries in two identical traces each. Known a-lrsc-mustfail width
policy divergence at22 repeats in two identical traces; not agreement. Wrong
surviving-SC expected code1 gives DIVERGE39 in a fresh a-lrsc-fault run (actual
code0), retaining the subsequent read42 observation. No universal reference
reservation assertion or internal-source inspection. Historical raw quotes in
P4-SYSTEM-designs/P4-SYSTEM-2 stay byte-exact with a live annotation in the tree.

Entire dossiers/guests/reports, core code, author, generators, registry104 and
frozen/archive/knowledge/ledger bytes exact. Independent full167/5365/10524
corpus and effective102/114 unchanged. make check rc=0 Rust167/17/223; focused
checks/all six books in tree. Scoped review also encountered two FP internal
rationales, owned by priority-next c29b before GC-COUNTERS. Evidence in
target/p4-system-13/c29a and worked atomics book.
promotion: declined (established published-interface boundary; the public result/control and historical annotation retain the diagnosis and limits).


## _(2026-10-10)_ — discriminate atomic execution and faults (P4-SYSTEM.13 c29)

Missing-binding control selects GC-ATOMICS/count104 and fails rc101 for
CHK-GC-ATOMICS-POS before registration. Authenticate RVI-A56889B/SHAafbd8def
and supervisor186455B/SHAd5186efc; independent literal tables/assembler992
words/author12024 boundaries precede CPU execution. Initial scratch Sem
width-node construction corrected to published scalar Trunc/Sext API before
runtime control credit. Ten vectors ×11operations×W/D×aqrl×M/S/U×four rd patterns
=10560 successful cells; includes rd=rs1/rs2/x0 and two rs2 alias/zero controls.
Another960 SC address-mismatch cells return1/clear/no data requests.

Three-level MPRV AMO path: VA10000→PA5000, Walk2000/3000/4080 with PTEs
c01/1001/14c7. Nineops×two widths×four ordering cells:72 successes,432 page
faults (six leaf configurations),144 physical load/store refusals. Trap cause15
for pages/7 for physical failures, virtual tval, unchanged rd/memory/reservation.
Full GPR/FPR/26CSR/memory/reservation/TLB cursor/wait/PC/mode/outcome/request
observer; direct12168 boundaries/24336 parcels/45840 requests. Seven unchanged
companions198/396 give pair12366/24732. Author omits explicit data requests,
retained invalid fields and two-phase physical refusals; direct observer owns
these distinctions. No multicore proof from a one-hart request pair.

Nine wrong public tables and14 corrupt captures reject; request auditor off
admits state-identical extra Load (RED101), Atomic→Load translation gives
wrong page cause (RED101). Both actual sources restored by SHA before normal
checks. Registry104/effective102/114, six pairs/freeze remain. make check rc0:
167 core/17DSP/223 verifier; independent full167 corpus and focused/all six
books recorded in tree. Frozen/core/author/old102 registry/archives exact.

Encountered internal atomic cancellation/error-site rationales are owned by
priority-next c29a; c29 derives no dependency assumptions from them. All work
and measurements: target/p4-system-13/c29, tracked worked atomics book/tree.
promotion: declined (established direct-observer discipline; the worked atomic values, request paths and refusing controls retain the reusable evidence).

## _(2026-10-10)_ — ground fence reference claims in public evidence (P4-SYSTEM.13 c28e)

Scoped history/text census identifies b5621de's internal Sail-file quotation in
zifencei.sem.sexp, repeated by fence-i book/old .6 Result. User §20 requires
published boundaries. Replace maintained semantic/book rationale with authenticated
ISA/local coherence and public observations; annotate the historical receipt
without rewriting it. Three identified locations addressed; no repository-wide
internal-assumption audit is claimed. No dependency implementation was inspected.

Fresh public six guests/29 boundaries AGREE with two byte-identical traces each;
nonzero0011118f continues to x9=42. Wrong expected43 gives fresh DIVERGE at1,
rc1. This covers declared GPR changes/deliveries, not all ignored-field combinations.
Reference binary/config/pins exact; no new structured experiment/status credit.
Parsed semantic forms exactly equal. Stale generated provenance RED rc1; owner
regenerates the Rust module with only two source SHA replacements:
048555ac8a792789fb534d37d05c0f099a658f822520689e214265ecd2afcd5c →
91a6e728d1448d2f440a8672564c5912b6451ed105d87194429ded0f73b75164.
Every instruction/decode/effect token stays exact; no hand edit of generated code.

verify.py rc0: all profile/guest/frozen/registry102/evaluator/author/archive bytes
exact; independent167/5365/10524 corpus unchanged. make check rc0 Rust167/17/220;
DEF-GEN/SEMANTICS/focused/all six books rc0; hooks next. Effective100/114 and
LIVE652/49/P4 12/18 unchanged. Next c29 GC-ATOMICS SEMULITH-P4-0162, seven runtime
pairs/freeze; .14 statuses/experiments remain. promotion: declined (established
public-boundary policy; worked visibility book retains evidence/provenance limits).
Evidence: target/p4-system-13/c28e (fresh public/control, exact comment delta,
provenance RED, checks and identity proof).


## _(2026-10-10)_ — observe FENCE.I visibility and ignored fields (P4-SYSTEM.13 c28d)

Authenticated RVI-ZIFENCEI4.1,32380 B SHA4026de34713f4b898595eb4a17bb58176a0e2905196705a904d3d8fab4432a91.
Direct61440 field cells =4096 funct12×five rs1/rd pairs×M/S/U; POS3 canonical,
NEG61437 ignored-field words. Full GPR/FPR/26 CSR owners/memory/reservation/TLB
including FIFO cursor/Active wait/PC/mode/outcome/parcels/requests preserved.
Only PC+4/cycle+1/retired+1 and two parcel fetches.36 five-boundary SH/fence/LHU/
marker/patched-target programs cross W/C,0/2 mod4,M/S/U,canonical/nonzero/no-fence.
Word00200413 high-halfword0070 becomes00700413; C4409→441d, both x8=7.
The coherent no-fence subset and arbitrary-provider limits remain explicit.

Independent derivation first verifies all61440 states and36 program words/state/
fetch logs; direct61620/123222/123294 requests. Author omits72 SH/LHU requests;
CPU observer owns them and complete retained TLB/reservation fields. Three unchanged
companions17/34 give pair61637/123256. Initial diagnostic expected a shortened
source label; inspection found the existing full4.1/decision2/visibility locator,
retained verbatim and corrected the diagnostic (no producer change).

Eleven wrong public tables and16 corrupt captures reject, including cursor-only
TLB. Actual request auditor disabled admits state-equivalent extra Load, RED101;
actual WFI condition admitting FENCE.I fails wait state, RED101. Both restored
exact SHA. Wait entry has no public Sem node, so the actual core condition is
used instead of inventing one. Missing-binding completeness RED101, then two
Execution entries; prior100 entries exact. Registry102/effective100/114, seven
runtime pairs/freeze. make check rc0: Rust167/17/220. Independent full corpus
167/5365/10524; code/author/canonical/frozen/prior archives exact. Focused gates/
all six books rc0; hooks next. LIVE652/49/P4 12/18 unchanged.

Next c28e owns replacing obsolete Sail-internal explanatory assertions in the
semantics commentary/book (plus annotation of the old task receipt) with public
observations, preserving semantic forms/provenance. Current binding relies only
on authenticated ISA/local provider. .14 still owns statuses/experiments.
promotion: declined (existing direct-auditor discipline; worked visibility book and refusing controls retain the diagnosis and finite limits).
Evidence: target/p4-system-13/c28d (source auth, literal derivation, mutations,
missing-binding RED, direct/check logs, pair census and identity verification).



Older whole entries remain in [shard 0229](docs/changelog/shard-0229.md);
`docs/changelog/SHARDS.sha256` authenticates the live shard history.
