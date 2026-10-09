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

