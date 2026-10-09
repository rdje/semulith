# P4-SYSTEM — archive part 6

Completed receipts moved byte-verbatim from the active tree, continuing part 5.

`P4-SYSTEM.12` slice (e1c1) — independent selected cache (`2026-10-08`, `SEMULITH-P4-0096`):

- [x] **REPRODUCE / ROOT CAUSE** — `python3 scripts/probe_gc_cache_author.py
  --author-revision ff75610` rc=1: “cache must retain stale mapping until fence”.
  `rg -n 'def walk|sfence.vma' scripts/derive_rv64gc_expectations.py` locates the
  unconditional PTE walk and fence prose without an effect. Prior parcel census
  sv39-tlb-fence disagrees at steps 191/192/195; pinned supervisor four scopes and
  state.sexp:664 select cached translation behavior independently of engine outputs.
- [x] **FIX** — successful translations install four FIFO slots keyed by 4-KiB VPN
  and 16-bit ASID; G propagates through non-leaves. Hits recheck live effective mode,
  SUM/MXR against cached leaf permissions/A/D; faults install nothing. M/Bare bypass,
  root-on-miss and current ASID visibility remain explicit. Legal fences use x0 identity,
  masked ASID and canonical selected page, retaining globals when ASID-scoped and the
  FIFO cursor for every invalidation. Illegal fences leave cache unchanged. Three
  existing direct PTE-edit fixtures execute legal full fences before requiring freshness.
- [x] **ADDRESSED (verified)** — `python3 scripts/probe_gc_cache_author.py` rc=0:
  hand PTE/PA fixtures cover stale mappings, four zero-operand scopes, masked ASIDs,
  invalid VA, illegal U/TVM fences, inherited globals, root/ASID/Bare/MPRV visibility,
  live SUM/MXR/U, cached D=0, no-fault-installation, FIFO and independent superpage
  keys. Cold cache guest request logs repeat exactly. Thirteen mutants each rc=1 with
  named behavioral assertions; the uncached parent is RED. One initially overbroad
  illegal-fence mutant failed a legal scope first; refine it to illegal cases, then
  the gate names the intended no-effect failure. An invalid-VA guard deletion alone
  has no observable effect for canonical cache keys; the control instead injects
  actual invalid-address over-fencing. Final self-test: 103 pass / 0 fail.
- [x] **NO REGRESSION** — full non-writing author census: parcel 139 exact, zero
  disagreements/refusals; historical word route 120 exact / one corrected cache text
  / zero new, with the same 18 bounded refusals. `--check-owned`: 42 guest(s)
  byte-identical; no records written. All 139 expected-record hashes retained. GUEST-GEN
  rc=0: both generated fixtures match and mirror 91 exact / seven declared rederivations.
  DERIVED-COUNTS rc=0 derives 582 arms; make book rc=0 for project/all model books.
  Rust/production profile/guest/count files unchanged; no broad Rust rerun warranted.
- [x] **LOCKSTEP / PRESSURE** — MEMORY/tree/index/live docs/toolbox/doctrine and
  C/Sv39 book updated; LIVE_STATUS remains P4 11/18, CPU-SYSTEM incomplete. DEV_NOTES
  50,021→47,771 B, shard-0209 carries one oldest record; shard tool asserts 32 ==
  31 kept + one moved, order/bytes exact. CHANGELOG new summary 118 B, full detail here.
  Archive 212 files / 784,318 B, only 2,114 B remaining; next CHANGELOG cut needs
  2,377 B before header/manifest and current head has eight bytes left. `.4` owns the
  urgent lifecycle prerequisite, with exact 210-shard / 211-member archive retrieval
  proof and proposed transaction in its tree. No cap or existing frozen bytes changed.
  promotion: declined (hand cache fixtures/thirteen RED controls retain the lesson).

`P4-SYSTEM.12` slice (e1d0) — honest author provenance (`2026-10-09`, `SEMULITH-P4-0097`):

- [x] **REPRODUCE / ROOT CAUSE** — `python3 scripts/probe_gc_provenance.py
  --author-revision 5ac3514` rc=1: generic output inherited FP provenance.
  `rg -n 'floating-point corpus|def emit' scripts/derive_rv64gc_expectations.py`
  pinpoints emit's unconditional FP fallback, inferred from unmatched filenames.
- [x] **FIX / ADDRESSED** — the tracked author names its actual word or explicit-budget
  C-capable parcel route. Historical capture headers apply only to the 42 canonical
  owned word inputs, never copied names or a new parcel derivation. No invented
  pre-engine chronology. `python3 scripts/probe_gc_provenance.py` rc=0: generic,
  nine borrowed names, raw C.ADDI observation/schema, owned parcel route, unknown-route
  refusal and all 42 historical records exact. Four targeted mutations each rc=1
  with the intended provenance/route reason. No production record is written.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh` rc=0: 109 pass / 0 fail;
  both tracked generated fixtures exact, base mirror 91 exact / seven declared.
  DERIVED-COUNTS --list derives 605 arms. Only new-output comments change; existing
  139 expectation files, production encoding and Rust modules unchanged.
- [x] **LOCKSTEP** — MEMORY/frontier/live status (P4 11/18 unchanged), logs,
  toolbox/doctrine and C book updated. Completed e1c0 receipt moved verbatim to
  archive part 5 (2,979 B); reconstruction asserted, archive 63,976 B. README neutral
  body and claim-verification source body identical to read-only policy sources.
  Containment guide read (SHA-256 8f77fa39c9bcb9cfc43166259a627a6ced64682030088400b727dccc5d674a53);
  full adoption remains LIVE-CONTAINMENT.4. `make book` and commit gate must pass.
  promotion: declined (permanent provenance fixtures and four RED controls retain the rule).

`P4-SYSTEM.12` slice (e1d1) — historical parcel-count staging (`2026-10-09`, `SEMULITH-P4-0098`):

- [x] **REPRODUCE / ROOT CAUSE** — `python3 scripts/derive_gc_parcel_counts.py`
  rc=0: derives 139 exact architectural write traces at their 4,913 declared boundaries:
  4,888 prior word requests -> 9,770 actual parcel requests. Five guests differ
  from blind doubling (runoff/fetch faults). The encoding's C slot remains unbound;
  e1d's declared count-provenance prerequisite precedes adopting any new extent.
- [x] **FIX / ADDRESSED** — tracked census derives each run independently, checks
  all writes against its prior record and the step fetch sum against the actual
  request log. Deterministic staging manifest carries 393 conservative input hashes,
  including instrument code, schemas/definition data, unit metadata and every paired
  source/record. `python3 scripts/derive_gc_parcel_counts.py --check` rc=0; no guest
  record written. Hand word/mixed/runoff counts and repeat pass. Observation/extent
  mutations each rc=1 with the intended boundary/request-log diagnosis; a damaged
  stored count is DRIFT (rc=1), the unchanged manifest is green.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh` rc=0: 113 pass / 0 fail,
  both generated fixtures and the base mirror exact. Existing 139 expectation records,
  encoding and both generated Rust modules remain byte-exact against eaad766;
  no Rust change, no broad Rust rerun warranted. DERIVED-COUNTS --list derives 609 arms.
- [x] **LOCKSTEP** — MEMORY/frontier/index, live status (P4 11/18 unchanged), logs,
  C book and toolbox/doctrine updated. e1c1 moved byte-verbatim to archive part 6
  (3,392 B; reconstruction asserted). `scripts/shard_history.py` cuts CHANGELOG
  79 == 76 kept + 3 moved (65,383 -> 57,215 B) and DEV_NOTES 41 == 35 + 6
  (48,995 -> 40,281 B), bytes/order exact; shards 0215/0216, fixed bounds unchanged.
  `make book` rc=0; commit gate enforced. Git diff whitespace check reports only
  retained whole-record blank separators at the two sharded heads' EOF; code diff
  is clean. Next e1d2: the independently authored C corpus.
  promotion: declined (permanent hand/RED/drift controls retain the count distinction).

`P4-SYSTEM.12` slice (e1d2) — specification-derived compressed corpus (`2026-10-09`, `SEMULITH-P4-0099`):

- [x] **REPRODUCE / ROOT CAUSE** — e1d requires a new C corpus before binding.
  `python3 scripts/stage_gc_c_corpus.py` rc=0: 28 staged guests, all 37 selected
  forms, 429 predeclared boundaries, 708 actual parcels. The production encoding
  still carries the C slot. Primary chapter digest re-verified and read in full.
- [x] **FIX / ADDRESSED** — tracked producer declares programs/budgets and hand
  final/PC/state checkpoints before any processor-engine run. Independent author
  derives every observation and request. Coverage requires an actual expansion
  derivation, excluding source annotations at interrupt/fetch-fault boundaries.
  `--check` rc=0, schemas 28/28. Observation and extent mutants each rc=1 with
  named semantic reasons; a saved budget changed 15->16 makes --check DRIFT (rc=1),
  then regeneration restores exact output. Initial LR/SC source syntax was refused;
  corrected to the documented parenthesized-address interface, no oracle changed.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh` rc=0: 117 pass / 0 fail,
  both generated fixtures and base mirror exact. `python3 scripts/derive_gc_parcel_counts.py
  --check` rc=0: all 139 historical traces still exact at 4,913 boundaries / 9,770
  requests; its conservative fingerprints regenerated for the new producer. All
  142 production records/encoding/generated modules byte-exact against 4754419.
  DERIVED-COUNTS --list derives 613 arms. No Rust or production guest/count changes.
- [x] **LOCKSTEP** — MEMORY/frontier/index/live status (P4 remains 11/18), logs,
  toolbox/doctrine and C book updated. Closed e1d0/e1d1 receipts moved byte-verbatim
  to archive part 6, reconstruction asserted; bounds unchanged. `make book` and
  commit gate enforced. Staged sources/records total 204,698 B: projected profile
  family 519 files / 3,091,575 B before bind metadata, inside current 600 / 3,145,728
  ceilings. Next: e2 preflight of count/mirror contracts, atomic C bind, matched Sail.
  promotion: declined (permanent source/hand/mutation/drift controls retain the method).

`P4-SYSTEM.12` slice (e2a) — govern the count-only mirror migration (`2026-10-09`, `SEMULITH-P4-0100`):

- [x] **REPRODUCE / ROOT CAUSE** — target-local copy adopts independently staged
  parcel counts; current shell governor rc=1 at bound-alias, because full-byte
  comparison cannot express the declared extent migration. Log e2a/before.log.
  Production is still unbound and no production file changes in this prerequisite.
- [x] **FIX / ADDRESSED** — `python3 scripts/check_gc_mirror.py --self-test` rc=0:
  hand word/mixed/runoff counts, repeat, composition selection, wrong count,
  comment/CRLF/write/source drift, stale exceptions, duplicate/direct/nested/string
  field controls pass. C mode independently derives every supplied guest's writes
  and actual requests before surgical direct-field transformation; all other bytes
  governed. The seven named re-derivations must still differ after normalization.
  Four weakened-check mutations each rc=1 for the intended accepted-defect reason.
- [x] **NO REGRESSION** — real target-local migrated corpus on temporary full-C
  composition rc=0: 49 exact files + 42 checked count-only records + seven declared
  re-derivations; same copy with unbound composition rc=1. Production governor
  rc=0: 91 exact / zero adjusted / seven declared, unchanged from pre-slice.
  `bash scripts/check_guest_gen.sh` rc=0: 122 pass / 0 fail, both generated fixtures
  exact. All 142 production records/encoding/modules byte-exact against 413c7da.
  DERIVED-COUNTS derives 618 arms. No Rust change.
- [x] **LOCKSTEP** — live docs/frontier/toolbox/doctrine and C book synchronized;
  P4 remains 11/18. e1d2 receipt moved byte-verbatim (2,185 B) to archive part 6,
  reconstruction asserted. Fixed ceilings unchanged. Active brief now names c1's
  parcel-first replacement, removing the superseded coalescing direction.
  `make book` rc=0. First hook refused derived book-index drift; regenerated through
  gen_book_index.py, then rebuilt the book. Next e2b: atomic composition/corpus/
  contract bind, then matched Sail and leaf acceptance. Commit gate enforced.
  promotion: declined (permanent literal/extent/mutation controls retain the distinction).

## Closed design — e1d2 corpus

- `2026-10-09` (e1d2 corpus design, before changes): primary RVI-C chapter read in
  full from the pinned cache, digest 3f7e7d853d6e12e9d44c3d1bb488d1c312179a308d608182fb01db43a49d6aeb.
  Track a staging producer with predeclared budgets for all 37 selected forms:
  signed/scaled limits, word overflow, aliases/x0/HINTs, stack/compact integer and D
  memory, mixed branches and pc+2 links (rd=rs1), LR/SC with valid C arithmetic,
  reserved original-bit diagnostics/EBREAK and four FS=Off memory gates. Derive
  all expected values spec-side before engine runs. Adapt the existing public
  sv39-straddle source into C.NOP at the final halfword versus a required second
  parcel on a non-executable page; budgets 52 and 51, cause 12/tval next page,
  saved start PCs and actual requests hand-checked. Use temporary full-C composition
  with copied profile/state metadata, emit only target-local staged sources/records
  and a fingerprinted manifest, and discriminate changed observations/extent.
  Production sources/counts/composition/modules remain untouched until e2. Archive
  completed e1d0 verbatim to part 6 to preserve the fixed live-tree ceiling.

`P4-SYSTEM.12` slice (e2b) — historical author extent preflight (`2026-10-09`, `SEMULITH-P4-0101`):

- [x] **REPRODUCE / ROOT CAUSE** — full-C target-local snapshot with independently
  migrated counts makes --check-owned rc=1: all 42 records DRIFT (e2b/before.log).
  The historical word route regenerates capture text and word extent together;
  the new boundary needs a separately derived count, not replacement prose.
- [x] **FIX / ADDRESSED** — `python3 scripts/probe_gc_owned_extent.py` rc=0:
  42-record unbound check, full-C unmigrated refusal, migrated/repeat checks,
  count/write/comment/CRLF drift, canonical word-write refusal with byte identity,
  and explicit parcel write/provenance pass. Bound checks compare independently
  derived parcel writes to the historical derivation and reconcile the actual
  request log before the shared direct-field transform. Four author mutants each
  rc=1: old counts, parcel prose, bad request log and permitted word overwrite.
- [x] **NO REGRESSION** — `bash scripts/check_guest_gen.sh` rc=0: 127 pass / 0 fail;
  both generated fixtures and production mirror (91 exact/seven declared) match.
  First unstaged cold check named the new untracked helper as missing; a temporary
  target-local index included the pending Python files for the tracked-input test.
  Actual index SHA-256 unchanged (verified); no gate weakened. All 142 production
  records/encoding/modules byte-exact against ce6a6d8. No Rust change; 623 arms.
- [x] **LOCKSTEP** — live docs/frontier/book/toolbox/doctrine updated, P4 11/18
  unchanged. Closed e2a receipt and e1d2 design moved byte-verbatim to archive part 6;
  reconstruction asserted, fixed caps unchanged. `make book` and commit gate enforced.
  Next e2c binds the production composition, staged corpus/counts, contract and matrix;
  matched Sail and leaf acceptance follow.
  promotion: declined (permanent snapshot/byte/write/mutation controls retain the rule).


## Closed pre-bind design notes (e2b/e2a)

- `2026-10-09` (e2b author preflight, before changes): the bind also changes the
  42 historical author-owned records' extents. Own this prerequisite before e2c's
  atomic bind: reproduce --check-owned on a target-local full-C snapshot with
  independently staged parcel counts. Preserve the original word-derived capture
  text; independently execute each fixed budget, compare every write and actual
  request log, and transform only its direct fetch field. Share the surgical helper
  with the mirror governor through a small text module, avoiding a dependency from
  the author to its governor. Unbound historical checks stay byte-exact. Refuse a
  default word-route CLI write to a canonical C-composed record; an explicit parcel
  route remains available. Retain controls for migrated/unmigrated counts, wrong
  observations/comments, request-log disagreement, write refusal and the original
  42 records. Archive closed e2a verbatim; production remains unchanged here.

- `2026-10-09` (e2a bind preflight, before changes): own the mirror/count governor
  prerequisite here before the atomic bind. Diagnose the current governor against a
  target-local copy with independently staged parcel counts: exact byte comparison
  must refuse. Replace only its fetch-field comparison for a C-composed unit with a
  surgical transformation; compare every other byte and retain the seven declared
  semantic re-derivations, which must still differ after count normalization. Independently
  derive all supplied records' writes and actual request counts before accepting any
  parcel extent. The unbound production route stays byte-exact. Add permanent controls
  for word/mixed/runoff extents, wrong counts, non-count comments/observations/source
  drift, stale re-derivations, duplicate/nested/string field traps and exact repeat.
  No production record/composition/module change in this prerequisite. Correct the
  active brief's superseded coalescing sentence to the c1 parcel-first decision already
  recorded below. Commit e2a, then e2b binds the staged corpus and contract together.


## Closed e1d staging/provenance design notes

- `2026-10-09` (e1d split, before changes): e1d1 first tracks a reproducible,
  non-writing census of all historical guests at their already-declared budgets.
  Compare every independently derived architectural write to the existing records;
  derive parcel counts from actual request logs and check the per-step sum. Emit a
  deterministic fingerprinted staging manifest, with no production count changes.
  Hand word/mixed/runoff counts, wrong-observation and wrong-extent controls must
  discriminate. Then e1d2 authors the C corpus before e2 binds. Archive e1c1 verbatim
  to part 6 at the live-tree ceiling, with exact reconstruction asserted.

- `2026-10-09` (e1d0 provenance prerequisite, before changes): emit currently falls
  through to the FP-corpus header for generic/C/Sv39 source names. Preserve exact
  historical headers only for the 42 canonical owned sources on their word route;
  every new output names the tracked spec-side author and its actual word or
  explicit-budget C-capable parcel route, without inventing original family or
  pre-engine chronology. Guard generic sources, borrowed historical basenames,
  raw C parcels and parcel re-derivation of an owned input, with parent and targeted
  mutations. Check all 42 owned records exact and historical record hashes unchanged.
  Commit this bounded repair before e1d stages any new corpus/count records.


### Owned e1d provenance prerequisite

`rg -n 'floating-point corpus|P4-SYSTEM.7' scripts/derive_rv64gc_expectations.py`
locates emit's fallback: non-family generic/C/Sv39 source names receive an FP-corpus
header. No such new production record is adopted here; prior outputs keep provenance.
Before publishing the staged C corpus/counts, e1d must derive an explicit correct
family/provenance header and guard generic/C text, while preserving the 42 historical
owned records. Schedule as high priority within e1d, before its first authored record.


## Closed e1c1 cache design

- `2026-10-08` (e1c1 execution plan, before changes): derive the declared four-slot,
  fully associative FIFO cache independently from state.sexp's selected policy and
  pinned supervisor 11.1.2.1/11.1.3.2/11.1.4.1. Cache successful 4-KiB translations
  with ASIDLEN=16, inherited G and leaf permissions; recheck live mode/SUM/MXR/MPRV
  before hits, retain cached A/D, and never install a fault. M/Bare bypass and satp
  root/ASID changes do not implicitly flush. Hits do not refresh FIFO; fences retain
  the replacement cursor and select x0 identity, masked ASID and canonical page.
  Hand PTE/physical-address fixtures, all four zero-operand fences, inherited globals,
  FIFO, stale permissions, fault non-installation and cold repeat must discriminate
  targeted mutations and the uncached parent. Repair direct permission fixtures that
  rewrite PTEs to execute a real legal full fence before requiring a fresh view; retain
  their existing negative controls. Census all 139 parcel architectural traces and
  all 121 historical word texts. The known erroneous unadopted sv39-tlb-fence word
  output may change to the pinned policy; investigate every other difference. Keep
  all 42 owned records byte-exact, and write no expected record or profile binding.
  Document the author cache and its provenance without claiming CPU acceptance.
  Archive-family pressure is now a resumption dependency: 211 files / 781,740 B
  leave 4,692 B, while the oldest required head records total 4,628 B before shard
  headers/manifest. Route the measured lifecycle defect to LIVE-CONTAINMENT.4;
  record its retrieval options and exact evidence before any migration. One DEV_NOTES
  shard and a concise changelog summary can finish this slice without a cap increase.

