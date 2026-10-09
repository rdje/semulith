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

