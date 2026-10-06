# P4-SYSTEM — archived completed-leaf evidence (part 3)

The continuation of [`P4-SYSTEM-2.md`](P4-SYSTEM-2.md) (part 2), which reached 130,659 B
of the 131,072 B per-part ceiling on `2026-10-06`: every archive move from the live
tree's slice-(c1) crossing onward lands here — the ceiling was obeyed, not raised, per
the `docs/tasks/` precedent (part 1 → part 2 at `2026-10-04`). The live tree keeps the
frontier, the decisions, the open questions, the blockers, every leaf's
goal/acceptance/result narrative, the ACTIVE leaf's checklists, log rows and changelog
entries.

Archived sections, verbatim:

`P4-SYSTEM`'s Changelog entries for the closed leaves `.2` (its last three — slices
(g), (h) part 1, (h) part 2 — which the twentieth crossing left inline when part 2's
own ceiling bounded that move), `.3` (closed `2026-10-04`, its design-brief entry
included), `.4` and `.5` (both closed `2026-10-05`), split out verbatim on
`2026-10-06` at the live file's crossing during `.7` slice (c1) (134,833 B > 131,072 B):

- `2026-10-05`: `.5` slice (d) done and the LEAF CLOSES (`SEMULITH-P4-0033`) — the
  Sail matched attempt, scoped to what is matchable (decision 9). The override is
  measured first: materialized fresh from the tracked unit (unchanged since
  bfa6aaa), validate-config rc=0, NO change needed. Against it, the
  software-posted-bit cells match exactly — **6 AGREE of 12** (i-accept 36,
  i-deleg 60, i-enable 21, i-nest 31, i-vector 53, w-sw 17 — 218 steps of
  change-observations, with Sail numbering the interrupt-delivery step and
  printing no row, the same convention the laboratory declares, measured on
  i-accept's [9]→[11] jump). The **6 NAMED divergences are all platform-shaped**:
  Sail's timer block gates on plat_have_clint, so STIP never sets without a CLINT
  (i-prio step 24, i-timer step 3); Sail's WFI is a nop under the matched
  platform, so the real halt has no counterpart (the four `<halted>`-step
  guests); and mm-wfi's TW cell is the `.2` named gap freshly measured with the
  isolated probe — DIVERGE under the matched config (Sail never judges TW: the
  judgment lives only in the wait-exit path the nop never reaches), AGREE 30/30
  under the wfi-wait variant with the delivered trap identical (cause 2, mepc =
  the wfi's pc, xtval = the wfi's word). Verdict-neutrality: the `.4` corpus
  re-run under the fresh override reproduces 11 AGREE + 1 NAMED of 12 exactly.
  The matrix invocation resolves 28 cells with the three RED legs fired by name
  (ORPHAN GUEST / OMITTED CELL / UNKNOWN DIFFERENCE); references.sexp records
  the fourth experiment. The LEAF ACCEPTANCE is w-timer's own run: three
  boundaries with no register observation (the two `<halted>` steps and the
  delivery), the handler's first read rdinstret = 11 — nothing retired across
  the halt — then the timer trap with mcause = Interrupt|5 and mepc = the wfi's
  pc + 4. The timer wake occurred WITHOUT CPU RETIREMENT. `make check` rc=0,
  `make gate` green (DERIVED-COUNTS 430), RECORD-SCHEMA 20, PROFILE-CONSISTENCY
  5, smoke-bench 53 arms, bench wasm, both books. Next: `.6` — instruction
  visibility and fence semantics (the design brief first, the cadence).

- `2026-10-05`: `.5` slice (c) done (`SEMULITH-P4-0032`) — the halted state and
  WFI's real wake (decision 4): one ACTIVE/WAITING hart bit (Sail's HART_WAITING
  precedent), cold-ACTIVE at reset, engine-owned hart state on the TLB/reservation
  discipline — the state document's SEM-08 census declares the wait-state
  candidate and gen_state carries the bit (the RED arm; DERIVED-COUNTS 429→430
  re-derived). A legal WFI ENTERS the wait (the nop latitude recorded-not-taken);
  a halted step retires nothing, issues no fetch, and ticks the domain once; the
  step's head evaluates the wake as exactly mip & mie != 0 — regardless of the
  global enables and of mideleg (RVP-MACHINE §2.1.3.3's sentences measured
  verbatim before authoring). On resume the taken-rule decides: the trap with
  xepc = the WFI's pc + 4 (the section's own rule, which the generic delivery
  computes for free — the WFI retires into the halt) or the pc + 4 continuation.
  The wake corpus (EVD-05, before any engine run): w-timer — THE acceptance
  cell: the timer's arrival during the halt delivers the trap, and the handler's
  rdinstret reads 11 at its first step — the wake occurred WITHOUT CPU
  RETIREMENT; w-notrap — wake-without-trap and the idle-loop idiom (two halts);
  w-deleg — a delegated STI wakes an M-mode hart anyway ('even if it has been
  delegated'), the trap firing only once un-delegated; w-sw — the
  software-posted SSIP/SEIP sources with the globals off. mm-wfi re-derives
  (decision 10): its legal cells halt with arranged timer wakes (the S cell's
  source delegated), the TW=1/U trap cells measured unchanged. The `<halted>`
  pseudo-step joins the vocabulary (decision 6 — empty writes, fetches 0). The
  corpus reads 99/99; 94 pre-slice guests byte-identical (only mm-wfi contains
  wfi — the census). The matrix carries the family (28 cells resolve). `make
  check` rc=0, `make gate` green. Next: slice (d) — the matrix cells + the Sail
  attempt + the reports and the book + the leaf acceptance.

- `2026-10-05`: `.5` slice (b) done (`SEMULITH-P4-0031`) — pending evaluation at the
  head of every step (decision 3): the (a)(b)(c) taken-rule + the global rule + the
  delegation mask + the fixed priorities MEI>MSI>MTI>SEI>SSI>STI with the M-source
  bits read-only 0 (decision 5), and interrupt-caused delivery honoring BOTH
  xtvec.MODEs (Direct = BASE, Vectored = BASE + 4×cause) with xcause =
  cause|(1<<63), xepc the un-fetched pc, xtval 0 (declared UNSPECIFIED) and the
  xPIE/xIE/xPP stack. `interrupts.rs` carries pending/deliver + 8 module tests; the
  head evaluation is wired before the fetch and the boundary still ticks (delivery
  steps retire nothing). The acceptance corpus is 7 new i-* guests (the taken-rule
  per mode, the enable immediacy, the timer across the ticking domain, the
  delegation mask with an S round-trip, the fixed-priority drain, both vector modes
  with the synchronous trap keeping BASE, and a nested delivery's stack
  restoration) — 290 steps, 13 of them fetch-less deliveries — with EVD-05
  expectations derived BEFORE any engine run; the corpus reads 95/95. Execution
  caught the authoring model's own defects (the derivation tool's inverted
  trap-entry stack — the engine was right; i-accept's mtvec delta 8 bytes long;
  i-timer's stimecmp authored against a retired-count clock; i-vector's SEIP-clear
  through read-only sip) and re-derived, never fitted. The pre-slice census (0
  interrupt writes in all 88 guests) made the identity proof unconditional, and it
  held: 88/88 demo traces byte-identical against the e37e664 engine. The matrix
  carries the 7 guests (28 cells resolve). `make check` rc=0, `make gate` green
  (DERIVED-COUNTS 429 unchanged). Next: slice (c) — the halted state + WFI's spec
  wake + `<halted>` + mm-wfi's re-derivation.

- `2026-10-05`: `.5` slice (a) done (`SEMULITH-P4-0030`) — the declared virtual-time
  domain: one tick per step boundary, retired or halted (authority laboratory, the
  Zicntr §6.1 rate latitude, a pure function of the step index). The storage shape
  is ONE domain — `mcycle` is its storage, `time` views it read-only ("cycle count
  might represent a valid implementation of RDTIME", §6.1) — and `minstret` counts
  GENUINELY (+1 per retired instruction, never for a trap-delivered, reserved or
  halted step); the rate and the count rule ride as DATA in the state document, and
  the census's `.5` reopen is answered for the counter-progress part. The moving
  counters exposed a LATENT defect: a field-less CSR view masked to zero, so the
  counter views would have read 0 forever — fixed at root (a field-less view is a
  full-width shadow of its owner). mm-counters — the ONLY counter-reading guest of
  all 88 (the full census re-measured; 0 mip/sip readers, so the STIP-at-reset
  quirk and the ticking STIP are unobservable today) — re-derives 5 cells BY
  DESIGN (time at executed step k is k: 0/1/2/25/51; the gating traps 13/39
  untouched), never fitted. `timekeeping.rs` carries the advance and 7 module
  tests (the ticking STIP included); the corpus reads 88/88; the other 87 guests
  are byte-identical against the parent engine (4,892 == 4,892 trace lines, both
  CLIs) — time ticking is invisible outside the counter reads, and the CLI/demo
  surface is unchanged. `make check` rc=0, `make gate` green (DERIVED-COUNTS 429
  unchanged). Next: slice (b) — pending evaluation + interrupt-caused delivery
  (both vector modes) + the acceptance corpus.

- `2026-10-05`: `.4` slice (f) done and the LEAF CLOSES (`SEMULITH-P4-0028`) — the
  Sail matched experiment: **11 AGREE + 1 NAMED DIVERGENCE of 12** on the corpus's
  change-observation rule, the override untouched (validate-config rc=0 — A,
  AMOCASQ, RsrvEventual, AccessFault all re-measured present). The divergence is
  the flagged width cell: Sail's platform reservation matches a `.D` SC after a
  `.W` LR on the physical address alone, while the laboratory's declared
  width-equal policy fails with code 1 — both legal under §12.1.2's latitude,
  recorded with the mm-wfi honesty. The experiment also caught a REAL defect: the
  bind-day uniform-cause-7 misaligned policy is illegal for LR (Sail delivered 5;
  the exception table maps load-reserved to load exceptions) — fixed at root to
  the kind-matched family (LR → 5, SC/AMO → 7) with the decision amended and its
  mirrors verbatim; exactly one guest expectation re-derived, the other 87 guests
  and the override untouched. Sail's SC proves deterministic under RsrvEventual,
  matching the declared never-spurious policy; the alias cell confirms the
  reservation physical-keyed on both sides. The acceptance reads as measured:
  single-core reservation behaviour validated — atomic widths, reservation
  semantics, failed conditional stores, overlap and external-write cases — and
  the multicore boundary named (MC-MULTICORE, never smuggled). `make check`,
  `make gate` green (DERIVED-COUNTS 429). Next: `P4-SYSTEM.5` — interrupts,
  counters and wait, its design brief first.

- `2026-10-05`: `.4` slice (e) done (`SEMULITH-P4-0027`) — THE BIND: one green commit
  makes the A extension real in the tracked unit — slot→extension; the census dual
  edit 65→87; REQ-GC-ATOMICS + the reservation/SC-policy/misaligned-cause-7 decision
  mirrors; `definition_rv64gc.rs` (22 forms + 3 `Sem` variants); the evaluator arms
  ported byte-identical from the scratch proof; the 12 guests tracked (88/88
  through the tracked engine, the 16/16 proof re-run green); the matrix cells
  resolve; the fetch leg flips on its own to 87==87; every pre-bind guest
  byte-identical (3,468 == 3,468 trace lines). One defect fixed at root (the
  emission's rustfmt stability at five fragments). `make check`, `make gate`
  (DERIVED-COUNTS 429), smoke-bench, bench, both books green. Next: slice (f) —
  the Sail matched experiment + the leaf acceptance.

- `2026-10-05`: `.4` slice (d) done (`SEMULITH-P4-0026`) — the staged atomics corpus:
  12 guests over the brief's families, EVD-05 spec-side expectations, every word
  through the tracked assembler, **12 PASS / 0 FAIL** through the slice-(c) scratch
  engine (deterministic re-run identical). Execution caught four authoring defects —
  each re-derived, never fitted (the tool's unapplied register writes; the
  same-value-write rule; a "reserved" funct5 that was LR's own; the sv39 data PA
  in the root table). Matrix rehearsal 28 cells resolve with three named RED legs;
  coverage 22/22 (87 = 65 + 22). All untracked staging; `make gate` green
  (DERIVED-COUNTS 429). Next: slice (e) — THE BIND: slot→extension, the 65→87
  census, the corpus tracked, the evaluator arms — one green commit.

- `2026-10-05`: `.4` slice (c) done (`SEMULITH-P4-0025`) — the reservation state
  (`reservation.rs`: (PA, width, valid); any LR replaces, any COMPLETED SC clears, a
  trap clears nothing — measured on Sail 0.14), the deterministic SC policy as
  state.sexp data, the generalised census gate (+1 RED arm), `AccessKind::Atomic`
  (R∧W, 15 never 13), and the AMO/LR/SC arms proven in scratch (16/16 after three
  caught test-design defects of mine). The tracked evaluator is untouched; the
  bind's port mapping is recorded. `make check` rc=0, `make gate` green
  (DERIVED-COUNTS 428→429). Next: slice (d) — the staged corpus + the matrix
  rehearsal.

- `2026-10-04`: `.4` slice (b) done (`SEMULITH-P4-0024`) — the reservation contract and
  the three atomic operators in the semantics language, `a.sem.sexp` for all 22 forms,
  and the generator's conditional lowering. The schema grows 40→43 forms: the
  RESERVATION block states the contract once (the minimal exact set, physical-keyed;
  any LR replaces, any SC clears, traps do not invalidate — §12.1.2/§12.1.3 cited,
  decisions 2–4; misaligned atomics take access-fault 7, reference-matched, decision
  6), and the operators carry the policies: `load-reserved` (load-rules translation,
  sets the reservation), `store-conditional` (yields the rd code — 0/1 under the
  declared deterministic never-spurious policy, decision 3; clears the reservation
  either way), `amo` (the closed nine by funct5 encoding; ONE store/AMO-rules
  translation, never a load page fault; reads old, computes, writes, yields old; the
  boundary pair load-then-store, a `Request::Atomic` variant recorded as rejected —
  decision 5). `a.sem.sexp` is hand-written with every rule locator-cited — 22/22
  checked, the citations resolving offline against rv64gc's pins (RVI-A §12.1.2 ×4,
  §12.1.4 ×18). Measured in execution: the AMO's operation cannot ride as a bare
  symbol (the walk refuses it as a phantom operand — measured rc=1), so the op is the
  funct5 literal and gen_definition RE-DERIVES the closed nine from the composed
  encodings; and the variants emit exactly when the composition composes `riscv/a`
  (the evaluator's exhaustive match is the .2 slice-d wall) — the tracked modules
  regenerate HASH-ONLY, the scratch composition (base+Zicsr+Zicntr+system+A) lowers
  and compiles standalone, and three RED probes name the guards. Self-tests
  15→17 / 17→23; `make check` rc=0, `make gate` green (DERIVED-COUNTS 424→428).
  Next: slice (c) — the reservation state (the census-candidate gate generalised,
  the emit, the module) + the deterministic policy as data + the engine's AMO/LR/SC
  arms proven in scratch.

- `2026-10-04`: `.4` slice (a) done (`SEMULITH-P4-0023`) — the `rv_a`/`rv64_a` re-pin,
  the `a.sexp` fragment, and the assembler's A machinery. The two tables came through
  the tracked `extensions/` fetch route and are pinned in the rv64gc ledger
  (sha256+bytes; 11 + 11 real rows — Zaamo's nine AMOs and Zalrsc's lr/sc, each `.W`
  and `.D`, exactly the pinned RVWMO Tables 6/7 enumeration). Measured in execution
  and fixed at root: the scope-vs-tables leg never collected `rv64_*` tables (latent —
  no profile had ever declared an A or M form while pinning the 64-bit table), and the
  A pin then broke that leg (87 enumerated vs 65 declared) until the M exclusion's
  declared shape — "pinned for the fragment, not the scope" — was extended to the A
  tables with the same flip condition (the bind, slice e). The fragment owns the `aq`
  and `rl` fields (the brief's "aqrl" phrasing measured imprecise: the tables carry no
  `aqrl` operand token — the rows list `aq rl` separately; the pinned csv's combined
  `aqrl` 26..25 is where the suffix's value lands). The assembler whitelists `aq`/`rl`
  (positions from the pinned arg_lut.csv, derived never typed), parses the
  `.aq`/`.rl`/`.aqrl` suffix as the aq/rl FIELD VALUES (garbage suffixes and
  suffix-on-non-atomic refused by name), and accepts the `(rs1)` parenthesized-address
  spelling — all 22 forms × 4 suffix combinations assemble (88 words) and round-trip
  through spike-dasm exactly, with 11 named RED refusals. The `(slot (id a) …)` stays
  declared and the census stays 65 — both grow only at the atomic bind. The existing
  five fragments re-derive byte-identical; no Rust touched; `make gate` green.
  Next: slice (b) — `a.sem.sexp` + the new operators (AMO with store/AMO fault
  semantics, load-reserved, store-conditional) through the schema/check/generator path.

- `2026-10-04`: `.3` slice (e) part 2 done and the LEAF CLOSES (`SEMULITH-P4-0020`) —
  the sv39 Sail matched experiment on three explicit dimensions: the architecture
  (the corpus's change-observation rule against sail 0.14 under the tracked
  Svade-flipped override), the walks (`--trace-ptw` against the spec-side model's
  walk log — read-for-read identical), and the TLB events (`--trace-tlb`; the same
  7 add / 2 flush). 13 AGREE + 1 AGREE-RECORDED of 14 — sail judges A/D after the
  walk, the laboratory at step 9, the delivered trap identical. The override's
  medeleg mask widened 0x3FF → 0xB3FF (verdict-neutral on the mm corpus).
  Acceptance met: the correct fault AND the permitted page-table side effects
  (none under Svade); A/D validated, not a knob. Frontier → `.4` atomics.

- `2026-10-04`: `.3` slice (e) part 1 done (`SEMULITH-P4-0019`) — the 14-guest sv39
  corpus: the happy-path translates with the M-mode ld-back of the walked PTE
  (byte-untouched under Svade), the superpage walks, the four walk-fault guests
  (canonical/V=0/reserved/misaligned superpage), the R/W/X and U/SUM/MXR
  permission matrices (fetch page fault included), the Svade no-update proofs,
  MPRV's translated-vs-physical distinction, the TLB's stale/fence/G-retention
  sequence as a guest, the non-contiguous-page straddle, and medeleg's selective
  routing. Every expectation spec-side derived (EVD-05); the fetch-count witness
  is now a declared observation (`fetches`) — a fetch page fault issues no
  request, the straddle two. Bare byte-exact (62/62); the matrix names all 14;
  DERIVED-COUNTS 424. Part 2 (the Sail matched experiment + leaf acceptance)
  remains.

- `2026-10-04`: `.3` slice (d) done (`SEMULITH-P4-0018`) — the minimal fully-specified
  TLB and sfence.vma's real four-case effect, with the census, snapshot and
  determinism consequences answered. The cache: **4 entries, fully-associative,
  FIFO replacement, ASID-tagged at ASIDLEN=16, keyed by 4 KiB page** (a superpage's
  other pages re-walk and install independently — conformant, and it keeps the
  fence's per-address case exact) — the minimal parameters that make every rule
  testable, authority laboratory, carried as data in the state document's SEM-08
  census (the `address-translation caches (TLBs)` candidate re-answered
  `present true` — the census's own ".3 reopens this candidate" hook) and emitted
  as hart state by gen_state, which now REFUSES a descriptor whose census is
  silent on the cache (a RED arm proves the refusal: STATE-GEN 25→26). The
  visibility record: satp is read per access, so MODE and ASID changes take
  effect immediately (dispatch and tagging); a root-PPN change is visible on the
  next miss, and stale entries may hit until a fence — §11.1.2.1's sanctioned
  staleness, the fence being the contract (the TLB never auto-invalidates);
  SUM/MXR are read per access, never cached, always immediate. The install
  discipline: a faulting access installs nothing, and a load past a D=0 leaf
  installs the D=0 entry — the two interact exactly as the spec sanctions (the
  cached entry's D bit faults a later store after software sets D without
  fencing — a LEGAL stale fault — and the fence restores the walk's truth). The
  fence's effect lands through the full pipeline: the `tlb-invalidate` operator
  (schema/semantics.sexp with its four-case contract) → `system.sem.sexp`'s
  sfence.vma effect `(tlb-invalidate (reg rs1) (reg rs2))` (the time-scoped nop
  superseded with its date; the legality untouched) → gen_definition's extended
  map + the `Sem::TlbInvalidate` variant (DEF-GEN both pairs green; rv64i
  fingerprint-only) → the evaluator arm (rs1 the VA, rs2's low 16 the ASID, no
  register written). The over-fence latitude is recorded-not-taken, so the G-bit
  retention and the per-ASID cases are genuinely tested — and they are: the TLB
  suite (25/25 with the walk's 17) covers a hit skipping the walk (count frozen),
  FIFO evicting in order, ASID tags with G hitting under any ASID, staleness
  legal without a fence then restored by it, Svade staleness through the cache,
  all four fence cases with their retentions (per-ASID and per-address+ASID keep
  globals; per-address evicts them; all-spaces empties everything), the
  non-canonical rs1 no-op, the fence INSTRUCTION end-to-end (sfence.vma x3,x4
  through the evaluator empties the entry), and cold-reset determinism — two
  runs, outcome tuples identical (the cache is a pure function of the hart's own
  history). Snapshot measured and recorded: the rv64gc path has no snapshot
  surface today (the CLI's snapshot/resume is rv64i-scoped by refusal), and a
  cold-restored cache is always a legal state — a miss is never wrong.
  mm-sfence's expectations needed NO re-derivation (measured: its legal fence
  cells never claimed a nop — a fence writes no register, exactly what they
  record). The Bare identity is byte-exact on the TLB engine: both CLIs over all
  62 guests, 1,884 == 1,884 trace lines, `cmp` clean. `make check` 8/8, `make
  gate` all green (DERIVED-COUNTS 422→423), smoke-bench 53 arms, bench wasm,
  both books.
  Next: slice (e) — MPRV/SUM/MXR + the sv39 guests + matrix cells + the Sail
  matched experiment + the reports and the book.

- `2026-10-04`: `.3` slice (c) done (`SEMULITH-P4-0017`) — the 10-step Sv39 walk is
  live, with the fault matrix proven and the requirement amended honestly. The walk
  (§11.1.3.2 with LEVELS=3/PTESIZE=8) is cited step-by-step in
  `crates/semulith-core/src/translation.rs`: the canonical-VA check (bits 63:39 ==
  bit 38) before any read; per-level PTE reads through slice (b)'s walk-access
  boundary kind, a boundary fault reported as the ORIGINAL access's access fault
  (1/5/7 by kind, step 2); V=0 and the W-without-R reserved encoding (step 3 — the
  first draft's R∧W inversion caught by the fault-matrix tests written before the
  fix, EVD-05 at the test layer); reserved/PBMT/N bits 63/62–61/60–54 zero with
  Svnapot/Svpbmt named unselected (step 4); misaligned superpage (step 5);
  non-leaf D/A/U reserved per §11.1.3.1 (step 6); the shadow-stack step named N/A
  (step 7); U/SUM/MXR and R/W/X by access kind (step 8); Svade's
  page-fault-instead-of-update with the PTE byte-untouched (step 9 — the permitted
  page-table side effects are NONE, by construction not by inspection); the
  physical address by level (step 10). The straddled fetch is live: each parcel's
  own physical unit, 16 bits from each, joined (the coalescing rule is over
  translated addresses, not pages — adjacent physical pages correctly coalesce).
  The fault-matrix suite: 17 tests covering all three leaf sizes with their walk
  counts (3/2/1), the canonical-VA fault, V=0, reserved-RW, the reserved bits
  ×3, misaligned superpage, non-leaf D/A/U ×3 + the last-level pointer, the
  U/SUM/MXR cells, the R/W/X cells, the Svade A/D cells with the region
  byte-identical across the fault, the step-2 access fault by kind, the MPRV
  selection, and the satp.MODE named defect. The requirement amendment was
  measured first: rv64gc's catalogue NEVER carried REQ-D-FETCH-IMPLICIT (the
  mirror's closure is 13 records and it is not among them), so the amendment
  lands as a NEW authored pair — D-WALK-IMPLICIT + verbatim REQ/OB mirrors —
  naming the translated composition's implicit-access vocabulary (the fetch + up
  to 3 implicit 8-byte walk reads per access; no implicit writes under Svade),
  with rv64i's owner record staying true of rv64i. The Bare identity is
  byte-exact on the walk-live engine: both CLIs over all 62 guests, 1,884 ==
  1,884 trace lines, `cmp` clean; the slice-(b) stub probe now faults properly
  (an S-mode fetch under Sv39 with an empty root: V=0 → mcause 12, mtval = the
  faulting VA). `make check` 8/8, `make gate` all green, smoke-bench 53 arms,
  bench wasm, both books. The guests exercising the walk end-to-end land in
  slice (e), per the brief.
  Next: slice (d) — the TLB + sfence.vma's real four-case effect + the census /
  snapshot / determinism consequences.

- `2026-10-04`: `.3` slice (b) done (`SEMULITH-P4-0016`) — the translation machinery
  shell, with Bare proven an exact identity path byte-for-byte. The new
  `crates/semulith-core/src/translation.rs` (the privilege.rs pattern) carries the
  effective-mode computation as ONE computation (RVP-MACHINE §2.1.1.6.4: fetch
  uses the hart's current mode — M-mode fetch never translated — loads and stores
  use MPP when mstatus.MPRV=1, with SUM/MXR carried for the walk), satp.MODE
  dispatch (M-effective and Bare are exact identity; Sv39 enters
  `Translate::Walk`, slice (c)'s entry — until then the named unimplemented case,
  never a wrong answer; an out-of-vocabulary MODE is a named panic), and the
  page-fault causes 12/13/15 entering core as raw u64 (the typed-enum asymmetry
  stated: the privileged engine's causes are delivered raw through the one
  trap-deliver path). The three hooks wired in exec_rv64gc: fetch in 16-bit
  parcels (decision 5) with the recorded coalescing choice — parcels translate
  independently, and the fetch issues exactly one request whenever both
  translated addresses share one physical 32-bit unit, which under Bare is every
  case, so the Bare request shape is byte-exact by construction; loads and stores
  translate after the model-side misalignment check (the pinned
  implementation-defined priority, decision 7). The walk-access boundary variant
  lands engine-side (`Request::WalkAccess` + `Response::WalkAccess`, 8-byte
  physical, read-only by construction under Svade — the D-FETCH-IMPLICIT
  precedent applied; the formal contract wording routed to `.9`), and its three
  exhaustive-match sites are answered per profile: FlatMemory answers it (never a
  fetch — the one-fetch-per-step census keeps its meaning), the bench census
  gains `walks`, and rv64i's TestEnv panics named (the base profile has no
  translation machinery). The Bare-identity proof is byte-level: both CLIs (the
  parent commit's and this one) drive all 62 guests and 1,884 trace lines compare
  `cmp`-clean, beside the cargo assertions (62/62, per-step writes, step counts,
  never_written, fetch counts, cold-reset determinism) and the Sv39-entry probe
  (`model error: Unimplemented … slice (c)'s`, cli rc=1). `make check` 8/8,
  `make gate` all green (DERIVED-COUNTS 422 unchanged), smoke-bench 53 arms,
  bench wasm, both books.
  Next: slice (c) — the 10-step walk with its fault matrix, the reserved-bit and
  superpage checks, and the REQ-D-FETCH-IMPLICIT amendment.

- `2026-10-03`: `.3` slice (a) done (`SEMULITH-P4-0015`) — the Svade identity edit, the
  Sail override flip, and the generator refusal. OQ-2 closes with evidence: the
  profile implements **Svade** — a translation needing an A/D PTE update raises a
  page fault, never a hardware update — on three legs: the pinned revision defines
  exactly two A/D schemes and names the page-fault one Svade (RVP-SUPERVISOR
  §11.1.3.1, §11.1.10, inline in the already-pinned chapter — no new sources); the
  U54 MMU the Sv39 choice already cites implements exactly that scheme (FU540
  §4.7); and the laboratory's observe-through-the-ISA discipline can evidence a
  page fault but not an implicit PTE write, so the hardware-update default would
  price a new observation vocabulary to test a side effect the laboratory need not
  produce. Svadu is NOT selected — menvcfg's ADUE stays WPRI (measured inside the
  state document's wpri_62_0 field). The identity edit: `(extensions "Svade")` in
  declared order (the canonical ISA string is now
  `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade`, the gen_platform declared-order
  rule), D-SVADE with authority laboratory and its verbatim REQ/OB mirrors (the
  D-ROUTE-FLIP shape), D-SV39's "not as this profile's rule" clause superseded by
  note (the mirror rule kept), DOSSIER's OQ-2 closed with the legs quoted, and the
  two ISA-string surfaces amended with owners named (the gen_platform derivation
  needs no regeneration — no board pins rv64gc today). The reference flips to
  match: `Svade supported: true` in the tracked override — one field, as the brief
  priced it — and the full 12-guest re-run measures the effect: 11/12 AGREE,
  IDENTICAL to the pre-flip baseline (no guest activates translation; the mm-wfi
  DIVERGE is the known TW cell, not a new effect). The generator hole the brief's
  pre-condition 6 named closes: `validate_gc` refuses
  register_family/memory_spaces/hardware_stack by name with the rv64i path's own
  wording (three RED self-test arms on mapping-valid injected shapes; both real
  pairs byte-identical). `make check` 8/8, `make gate` all green (DERIVED-COUNTS
  419→422 re-derived).
  Next: slice (b) — the translation module + the three hooks + effective mode +
  the Bare-identity proof.

- `2026-10-03`: the `.3` design brief recorded (`SEMULITH-P4-0014`). The measured
  pre-conditions: translation hooks are exactly three sites in `exec_rv64gc.rs`; the
  walk falsifies REQ-D-FETCH-IMPLICIT's "explicit accesses only by load/store";
  expectations cannot observe memory (a hardware A/D update is an implicit store no
  instruction owns); Sail models a 64-entry TLB precisely so sfence.vma is testable;
  a `validate_gc` hole silently ignores `memory_spaces`. The design: **OQ-2 answered —
  the profile ADDS Svade** (page-fault-instead-of-A/D-update; the pinned revision's
  two schemes, the U54 precedent, and the observation discipline as the three legs;
  hardware update + a memory-write vocabulary weighed and rejected); a minimal
  fully-specified TLB (ASIDLEN 16, G-bit retention, determinism as a pure function of
  hart history) with sfence.vma's four cases implemented as specified; translation as
  evaluator machinery (`translation.rs`, three hooks, MPRV effective mode) not a tree
  operator; fetch in 16-bit parcels; walk accesses a distinct boundary variant with
  the requirement amended and the formal contract wording routed to `.9`;
  misaligned-first priority pinned with the topic handed to `.8`; no new instructions,
  no new matrix axis. Five execution checkpoints named.

- `2026-10-03`: `.2` slice (h) part 2 done (`SEMULITH-P4-0013`) — THE LEAF CLOSES. The
  Sail privileged matched experiment (decision 8), attempted and honestly recorded.
  The matched override lands tracked at `profiles/rv64gc-lab-v0/reference/
  sail-rv64gc-lab-v0.override.sexp` (the .sexp is the truth, the JSON derived):
  privileged ISA 1.13, misa held, FS four-state / VS off, the declared selection
  (M/A/F/D/C, Zicsr, Zifencei, Sstc, Sv39, S, U) minus Zicntr, no devices, no PMP,
  WFI a nop except in U, medeleg 0x3FF — the validator itself confirming the
  corpus's own claims (cause 10 is reserved with H off; bit 11, ecall from M, is
  undelegatable by law). The dossier-format owners learned the override's new
  keys (schema optional fields — rv64i's override re-validated; the mapping both
  directions, self-test 13→14; the round-trip field-for-field exact). The evidence
  chain closes end to end: the tracked .sexp derives the JSON, Sail 0.14 runs the
  mm guests under it, and **11 of 12 AGREE step-for-step against the
  specification-derived expectations** — csr semantics, per-mode legality,
  delivered breakpoints, ecall causes and delegation, the xret rules, the mstatus
  all-ones WARL read-back bit-exact (`0x8000000A007E79AA`), the stimecmp and TVM
  gates. The two honest boundaries: mm-wfi's TW=1-in-S legality cell is a NAMED
  DIVERGENCE — Sail 0.14 does not implement mstatus.TW's effect on WFI legality
  (measured under both `wfi_is_nop` settings; the bit provably writable; no config
  knob exists), our expectation stands on the pinned spec, the finding routed to
  P4-SYSTEM.5 with its measurement; and mm-counters is NOT MATCHABLE — Sail
  requires a CLINT time source for Zicntr while the platform declares no devices,
  and the counter rate is the environment's own declaration (ours holds zero).
  Spike stayed platform-conflicted, no attempt. The leaf's acceptance criterion —
  the same instruction's behaviour tested in each supported mode — is evidenced
  by the mode matrix itself: 13 guests, every cell a mode crossing, falsified by
  the tracked engine (62/62) and differentially confirmed (11/13 full + 1
  partial). Frontier: `.3` — Sv39 translation and protection.

- `2026-10-03`: `.2` slice (h) part 1 done (`SEMULITH-P4-0012`) — THE ATOMIC FLIP. The
  staged payload lands tracked byte-exact from the proven staging: the 33-CSR state
  document, the encoding composition (base + Zicsr + Zicntr + the privileged-system
  fragment, `(status partial)` with six declared slots), the 62-guest corpus with
  run-order, and the 7-axis × 28-cell interaction matrix. The dossier's vehicle route
  flips to `generated-definition`; D-RESOLUTION-ROUTE is superseded by note (the
  D-FENCE "Corrected by" convention — its verbatim statement stays because the
  requirement catalogue mirrors it) and D-ROUTE-FLIP records the flip with its
  evidence, with the REQ/OB pair in the authored-records shape. The generated mirrors
  are tracked because their canonical inputs are tracked in the same commit
  (decision_generated-mirror-needs-tracked-input): `state_rv64gc.rs`,
  `definition_rv64gc.rs`, `guests_rv64gc.rs` — content-hash-identical to the
  scratch-proven modules. The tracked engine runs the corpus: `exec_rv64gc` ports
  the evaluator with the scratch runner's trap-END discipline ridden in (a delivered
  trap ends the step's remaining effects), delivery through the tracked privilege
  machinery, and the reserved-decode conversion reported for the policy layer one
  layer up; `cargo test -p semulith-verify run_rv64gc` proves all 62 guests on the
  tracked path (per-step writes exact, never_written, one fetch per step, cold-reset
  determinism). The CLI takes `--profile=` — run and demo wired for rv64gc
  (IALIGN as profile data, the memory fixture's fetch alignment parameterized), the
  rv64i-scoped commands (bench/bundle/reduce/replay/snapshot/resume/mutations)
  refuse by name, and rv64i stays the byte-exact default. Four gate gaps the flip
  measured, each fixed at its owner with RED-first arms: check_extraction honors
  the refinement relation (13 arms); EXERCISE-COVERAGE's closure leg counts the
  composition's pseudos (23); the three GEN gates' censuses loop owner→mirror pairs
  (STATE 22, DEF 17, GUEST 15 — including the base-mirror governor: 93 files
  byte-identical + 5 recorded re-derivations); FACT-OWNERSHIP re-pins to 5 units /
  74 kinds. The CSR name↔address ownership migrated: the state document owns, the
  assembler reads it, csrs.csv stays the upstream derivation source (33/33, and
  `pmpaddr0` is refused by name). gen_state's rv64gc emission learned rustfmt-
  stability (cargo fmt runs over crates/; STATE-GEN compares against regeneration).
  `make check` (76 core / 184 verify), `make gate` all green (DERIVED-COUNTS
  408→419 re-derived), bench wasm + smoke-bench + both books green, every rv64i
  verdict unchanged. The split is recorded: the flip is its own commit; the Sail
  privileged matched-experiment attempt lands as part 2.
  Next: slice (h) part 2 — the Sail attempt + the leaf acceptance.

- `2026-10-03`: `.2` slice (g) done (`SEMULITH-P4-0011`) — the unit's interaction matrix,
  declared and rehearsed. Seven axes — the leaf's own vocabulary: fault, alias, boundary
  and progress carried from the mirrored base layers; **legality** (mode-dependent
  permission and refusal — M/S/U, the TW/TVM/TSR gates, read-only/WARL, encoding
  validity) and **delegation** (interception routing — medeleg, the counter enables,
  STCE) added by the privileged machinery; and **restart reframed guest-shaped** —
  rv64i's mechanism-shaped restart (cold-reset determinism, a closed registry with no
  rv64gc mechanism) becomes the xret/xepc return discipline, observable by guests
  (mm-mret's MPRV rule, mm-sret's SPP, mm-ebreak's resume); rv64i's event axis is
  absorbed into the mode-cause and delegation story. 7 axes → 28 cells, all
  dispositioned: every one of the 62 staged guests maps onto ≥1 cell (no new guests
  needed), and three cells (alias×restart, boundary×delegation, boundary×restart) are
  REPORTED degenerate-with-reason — the doctrine's sanction for a cell the corpus
  honestly does not compose. The DIFFS rule forced the mirror's fourth and fifth
  re-derivations: it-fencei/min-fencei carried rv64i's `DIFF-FENCEI-EXECUTED` pin, whose
  record is false for this unit (rv64gc DECLARES Zifencei; the staged encoding leaves
  the slot unbound) — the divergence forms dropped with the reason recorded in each
  file, steps unchanged, the corpus re-proven 62/62; the mirror now reads 49 `.s`
  byte-identical, 44 expectations byte-identical, 5 re-derived. The rehearsal ran the
  check's own invocation against the staged unit (`check_interaction_matrix.py
  <unit-dir>` — the driver discovers tracked `profiles/*/` at the flip): 28 cells
  declared, every disposition resolves, rc=0; the RED legs fired by name against a
  scratch copy (DIFFS on the pre-re-derivation state, ORPHAN GUEST, OMITTED CELL).
  `make gate` green (DERIVED-COUNTS unchanged at 408 — no arms this slice).
  Next: slice (h) — the atomic flip.
