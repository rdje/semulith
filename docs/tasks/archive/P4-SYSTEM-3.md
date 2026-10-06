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

`P4-SYSTEM`'s Commit Log rows for the closed leaves `.1`–`.6` and the tree's own
`SEMULITH-P4-0001` row, split out verbatim on `2026-10-06` at the live file's crossing
during `.7` slice (c5) (the slice's records would have taken it past 131,072 B); the
stray blank line that split the table after the `.4` slice-(d) row (1
found) is not carried — it broke the table's rendering, and a row is the unit moved:

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `.6` (slice c) + LEAF | `SEMULITH-P4-0037 (leaf P4-SYSTEM.6): slice c — the matched experiment 6 AGREE of 6 + the census re-answer; the LEAF CLOSES` | the override measured first (validate-config rc=0, Zifencei true, unmoved); sail's FENCEI measured in source (fields decoded-not-fixed, nop for the memory model); 6 ELFs at exactly 0x8000_0000; 6 AGREE of 6 (29 steps, the patched fetch reading 7 on both sides, zero non-AGREE cells); the wider corpus unmoved since the verdicts (nothing to re-run); the fetch-cache candidate re-answered in place (the consequence line unchanged; gen_state re-derived); references.sexp's fifth experiment (difference-free); the acceptance box (WITH fencei-selfmod, WITHOUT fault-selfmod, the staleness half the declared latitude); 101/101 corpus; make check + make gate green (DERIVED-COUNTS 430), smoke-bench 53 arms, bench wasm, both books |
| `.6` (slice b) — THE BIND | `SEMULITH-P4-0036 (leaf P4-SYSTEM.6): slice b — THE BIND: the unit composes riscv/zifencei (88 forms, 101 guests, the fencei arms tracked)` | slot→extension; the census dual edit 87→88 (the .4 lesson's four places); definition_rv64gc.rs regenerated; REQ-GC-FENCEI + OB-GC-FENCEI, no new D-*; the fencei re-derivations (the pre-commit fulfilled); fencei-reserved + fencei-selfmod (the acceptance pair); the decision-3 corrections as recorded mirror re-derivations; the flip 88==88; 101/101 corpus; 98/99 identity cmp-clean; 28 cells; EXERCISE-COVERAGE 88/88; make check + make gate green (DERIVED-COUNTS 430) |
| `.6` (slice a) | `SEMULITH-P4-0035 (leaf P4-SYSTEM.6): slice a — the rv_zifencei re-pin + the one-form fragment + zifencei.sem.sexp + the assembler's zero-operand acceptance` | the tracked-route pin (73 bytes, one row, fresh re-fetch byte-identical); the named exclusion (flips at the bind); the fragment (owns NO fields, funct3=1; 6 others byte-identical); zifencei.sem.sexp ((effect (nop)) cited; pair 1/1, both composes, citations offline); the deviation ("no assembler shapes" false for the bare spelling → the named special case; no Sem variant / no generator change TRUE — rustc rc=0 ×2); the trials (53 and 85+3 COMPOSE); the probe (3 named REDs, spike-dasm exact); 87==87/52==52; 99 guests byte-identical; make check + make gate green (DERIVED-COUNTS 430) |
| `.5` (slice d) + LEAF | `SEMULITH-P4-0033 (leaf P4-SYSTEM.5): slice d — the Sail matched attempt (6 AGREE + 6 named of 12, probe-tw's TW gap freshly measured); the LEAF CLOSES` | the override measured first (validate-config rc=0, no change, the tracked .sexp unmoved); 13 ELFs at exactly 0x8000_0000; the delivery-step convention measured identical (sail numbers it, prints no row); 6 AGREE (i-accept/i-deleg/i-enable/i-nest/i-vector/w-sw, 218 steps) + 6 named platform-shaped divergences (STIP's CLINT gate ×2, the `<halted>` counterpart ×4); probe-tw: the TW gap fresh (DIVERGE matched, AGREE 30/30 under the wfi-wait variant, the delivered trap identical); the .4 re-run verdict-neutral (11+1 of 12); the matrix invocation + 3 RED legs; references.sexp's fourth experiment; the acceptance quoted from w-timer's actual run (rdinstret=11, mcause=int\|5, mepc=wfi+4); make check + make gate green (DERIVED-COUNTS 430), smoke-bench 53 arms, bench wasm, both books |
| `.5` (slice c) | `SEMULITH-P4-0032 (leaf P4-SYSTEM.5): slice c — the halted state + WFI's real wake + the `<halted>` vocabulary + the wake corpus + mm-wfi's re-derivation` | wait.rs (the ACTIVE/WAITING bit, cold-ACTIVE, pure function of history); the halted-step head arm + the legal-wfi enter in step_over (the wake first, else tick-and-stay); wake_pending (mip & mie — §2.1.3.3's musts, globals/mideleg ignored); the SEM-08 wait-state candidate carried by gen_state (RED arm 27→28); system.sem.sexp's stated nop superseded; the w-* family (w-timer's rdinstret=11 the acceptance observed) + mm-wfi re-derived (TW/U cells unchanged); 99/99 corpus; 94/95 identity cmp-clean; 28 cells; make check + make gate green (DERIVED-COUNTS 429→430) |
| `.5` (slice b) | `SEMULITH-P4-0031 (leaf P4-SYSTEM.5): slice b — the step-head pending evaluation + interrupt-caused delivery (both vector modes) + the 7-guest acceptance corpus` | interrupts.rs (pending/deliver + 8 tests: the (a)(b)(c) taken-rule + the global rule + the delegation mask + the fixed priorities, the M-source bits read-only 0; the Interrupt-bit delivery honoring xtvec.MODE); the head evaluation wired before the fetch (delivery steps tick, retire nothing); the derivation tool hardened to the field tables + pc-keyed derivations + the (fetches N) convention; 7 i-* guests (36/60/21/31/63/26/53 steps); 95/95 corpus; 88/88 identity cmp-clean; 28 cells resolve; make check + make gate green (DERIVED-COUNTS 429) |
| `.5` (slice a) | `SEMULITH-P4-0030 (leaf P4-SYSTEM.5): slice a — the declared virtual-time domain (one tick per step), counter progress, mm-counters' by-design re-derivation` | timekeeping.rs (the domain advance + 7 tests); the tick in step_over (!frame.trapped for instret); time → view_of mcycle (one domain, the rate as data in state.sexp, the census answered for counter-progress); the latent field-less-view defect fixed at root (full-width shadow); mm-counters 0/1/2/25/51 re-derived, traps 13/39 untouched; 88/88 corpus, 87 guests byte-identical (4,892==4,892); make check + make gate green (DERIVED-COUNTS 429) |
| `.4` (slice f) + LEAF | `SEMULITH-P4-0028 (leaf P4-SYSTEM.4): slice f — the Sail matched experiment (11 AGREE + 1 named of 12); the leaf closes` | the override unchanged (validate-config rc=0); the 12 ELFs via the tracked assembler; the width-cell divergence named (sail address-only vs the declared width-equal policy, both legal); the bind-day uniform-7 misaligned policy measured ILLEGAL for LR and fixed kind-matched (LR→5, SC/AMO→7) with the decision amended; one guest file re-derived; references.sexp's third experiment recorded; `make check` + `make gate` green (DERIVED-COUNTS 429); the leaf done, frontier → `.5` |
| `.4` (slice e) | `SEMULITH-P4-0027 (leaf P4-SYSTEM.4): slice e — THE BIND: the unit composes riscv/a (87 forms, 88 guests, the arms tracked)` | slot→extension; the census dual edit 65→87 (+PARTS); REQ-GC-ATOMICS + three D-* mirrors; definition_rv64gc.rs (22 forms + 3 variants + the 43-forms comment); the evaluator byte-identical to the scratch proof; the 12 guests + matrix cells tracked; the rustfmt fix; 88/88, proofs re-run green, the fetch leg 87==87, BARE-IDENTITY 3,468==3,468; all gates green |
| `.4` (slice d) | `SEMULITH-P4-0026 (leaf P4-SYSTEM.4): slice d — the staged atomics corpus (12/12), the EVD-05 derivation tooling, the matrix + coverage rehearsals` | 12 guests over the families; the four caught authoring defects; 28 cells resolve with 3 named RED legs; coverage 22/22 (87 = 65 + 22); all untracked staging — the bind re-runs it tracked |
| `.4` (slice c) | `SEMULITH-P4-0025 (leaf P4-SYSTEM.4): slice c — the reservation state, the deterministic SC policy as data, the AMO/LR/SC arms proven in scratch` | reservation.rs (PA,width,valid; any LR replaces, any completed SC clears, a trap clears nothing — the Sail zalrsc measurement); the census gate generalised with a RED arm (STATE-GEN 26→27); the policy as state.sexp data; AccessKind::Atomic (R∧W, 15/7); the 16/16 scratch proof; the archive SPLIT (part 2) at the ninth crossing; rv64i's surfaces byte-identical |
| `.4` (slice b) | `SEMULITH-P4-0024 (leaf P4-SYSTEM.4): slice b — the reservation contract + the three atomic operators in the language, a.sem.sexp for all 22 forms, the conditional lowering` | schema/semantics.sexp 40→43 forms (the reservation block citing §12.1.2/§12.1.3 + decisions 2–4/6; load-reserved / store-conditional / amo with the deterministic SC policy and the store/AMO fault rules); a.sem.sexp hand-written, 22/22 checked, citations resolving offline; gen_definition's A surface derived (the funct5 closed set from the composed encodings) and gated (variants emit WITH the fragment; two named guards); scratch module compiles standalone, 3 RED probes; self-tests 15→17 / 17→23; the tracked modules hash-only, no Rust edited |
| `.4` (slice a) | `SEMULITH-P4-0023 (leaf P4-SYSTEM.4): slice a — the rv_a/rv64_a re-pin, the a.sexp fragment, and the assembler's A machinery` | the re-pin through the tracked extensions/ route (sha256+bytes; the scope leg's rv64_* collector gap fixed at root and the A tables under the M exclusion's named shape until the bind); the generated fragment (22 forms, owns aq/rl — no aqrl token in the tables, measured); the suffix rule (.aq/.rl/.aqrl the aq/rl field values, garbage refused by name) + the (rs1) spelling; 88 words assembled, the spike-dasm round-trip exact, 11 named RED refusals; the existing five fragments and rv64i's surfaces byte-identical; the slot and the 65-form census untouched |
| `.3` (slice e part 2; the leaf CLOSES) | `SEMULITH-P4-0020 (leaf P4-SYSTEM.3): slice e part 2 — the sv39 Sail matched experiment (PTW/TLB traces explicit); the leaf closes` | the 14-guest experiment on three explicit dimensions (architecture by the corpus's change-observation rule indexed on sail's printed step numbers with the fetch-fault no-row convention; PTW read-for-read against the spec-side model with the laboratory's 4-entry FIFO live; TLB add/flush counts — 13 AGREE + 1 AGREE-RECORDED with the A/D-placement convention recorded, 0 DIVERGE); the tracked override's medeleg mask 0x3FF → 0xB3FF (the laboratory's discipline restricted to sail's accepted causes — the bisection named 10/14 reserved; verdict-neutral on the mm corpus, measured); the ELF build (the tracked assembler's bytes, .word-only source, PHDRS link at exactly 0x8000_0000); references.sexp's matched_scope updated; the acceptance met (the Result narrative on the leaf row) |
| `.3` (slice e part 1) | `SEMULITH-P4-0019 (leaf P4-SYSTEM.3): slice e part 1 — the sv39 guest corpus, the matrix cells, the fetch-count witness made declarational` | the 14-guest corpus (the three translate guests with the Svade PTE-untouched ld-backs; the four walk-fault guests across causes 12/13/15; the two permission guests incl. the U-mode stage; svade's no-update pair; mprv's MPRV/MPP cells with the fetch-immunity proof; tlb-fence's stale/selective-G/full sequence; the non-contiguous straddle; deleg's selective routing) — every expectation derived by the spec-side model (EVD-05) and falsified green; the spec-side model itself (the pinned walk + Svade + MPRV + medeleg + region bounds + the slice-(d) TLB semantics, with the authoring fixpoint layout and the chain-accumulating audit); the `fetches` declaration (a fetch page fault issues no request; the straddle issues two; the coalescing rule measured as address contiguity); the probe-bug record (mscratch M-only; the x8 no-change; the unit-vs-contiguity model); the matrix cells on the SAME seven axes; Bare byte-exact (62/62); DERIVED-COUNTS 423→424 |
| `.3` (slice d) | `SEMULITH-P4-0018 (leaf P4-SYSTEM.3): slice d — the TLB, sfence.vma's real four cases, the census/snapshot/determinism consequences` | the minimal fully-specified cache (4 entries, fully-associative, FIFO — the minimal parameters making every rule testable; authority laboratory; the census carries them as data and the generator refuses a silent census, RED-armed); the satp-visibility record (MODE/ASID immediate by per-access reads; root-PPN visible on the next miss with stale hits sanctioned until a fence; SUM/MXR never cached); the install discipline (faults install nothing; the D=0 load installs — the legal stale store fault, then the fence restores); the `tlb-invalidate` operator through the full pipeline (schema + system.sem.sexp's effect + gen_definition + the Sem variant + the evaluator arm; the time-scoped nop superseded with its date); the TLB suite (25/25: hit/FIFO/tagging/staleness/Svade-staleness/the four cases with retentions/the non-canonical no-op/the fence instruction end-to-end/determinism tuples identical); the census re-answer (present true with the parameters) + the trait member + the generated field; mm-sfence needs no re-derivation (measured: no nop claim, a fence writes no register); snapshot measured: no rv64gc surface today, a cold-restored cache is always legal; DERIVED-COUNTS 422→423 |
| `.3` (slice c) | `SEMULITH-P4-0017 (leaf P4-SYSTEM.3): slice c — the 10-step Sv39 walk, the fault matrix, the REQ-D-FETCH-IMPLICIT amendment` | the walk cited step-by-step (canonical-VA first; per-level walk-access reads with the step-2 access fault by kind 1/5/7; V=0 and W-without-R (the first draft's inversion caught by the tests); bits 63/62–61/60–54 zero with Svnapot/Svpbmt named unselected; misaligned superpage; non-leaf D/A/U reserved; U/SUM/MXR + R/W/X; Svade page-fault-instead-of-update with the PTE byte-untouched; the PA by level); the straddled fetch live (each parcel's own unit, joined); 17 fault-matrix tests with the walk reads counted per scenario (3/2/1 by leaf size, 0 for Bare and M-effective); the amendment measured first: the mirror's closure never carried REQ-D-FETCH-IMPLICIT, so the amendment is a NEW authored D-WALK-IMPLICIT + verbatim REQ/OB pair and rv64i's owner record stays true of rv64i; the Bare identity byte-exact on the walk-live engine (1,884 trace lines, cmp clean); the slice-(b) probe now faults properly (mcause 12, mtval = the VA) |
| `.3` (slice b) | `SEMULITH-P4-0016 (leaf P4-SYSTEM.3): slice b — the translation module + hooks + effective mode; the Bare-identity proof byte-exact` | translation.rs beside privilege.rs (the effective-mode computation §2.1.1.6.4 — fetch uses the current mode, data accesses use MPP when MPRV=1, SUM/MXR carried; satp.MODE dispatch: M-effective and Bare exact identity, Sv39 enters the walk as slice (c)'s entry, an out-of-vocabulary MODE a named panic); the page-fault causes 12/13/15 as raw u64 with the typed-enum asymmetry stated; fetch in 16-bit parcels with the recorded coalescing choice (one request whenever the translated parcels share one physical 32-bit unit — under Bare every case, so the request shape is byte-exact); the walk-access boundary variant (Request/Response::WalkAccess, 8-byte physical, read-only under Svade; the contract wording routed to .9); the three match-site dispositions (FlatMemory answers, bench census gains walks, rv64i TestEnv panics named); the identity proof byte-level: 62/62 guests, 1,884 trace lines `cmp` clean against the parent commit's engine; the Sv39 entry names itself (the probe's rc=1 with Unimplemented, never a wrong answer) |
| `.3` (slice a) | `SEMULITH-P4-0015 (leaf P4-SYSTEM.3): slice a — the Svade identity edit, the Sail override flip (measured verdict-identical), the validate_gc refusal` | OQ-2 answered by the brief and recorded: the profile implements Svade (the pinned revision's two A/D schemes with the page-fault one named; the U54 precedent already load-bearing in D-SV39; the observation-discipline pricing of the hardware-update default) — Svadu NOT selected (ADUE stays WPRI); the canonical ISA string `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade` by the declared-order rule; D-SV39's "not as this profile's rule" clause superseded by note (the verbatim-mirror rule kept); the override flip changes NO guest verdict (11/12 AGREE, baseline-identical — measured, never assumed); validate_gc refuses register_family/memory_spaces/hardware_stack by name like the rv64i path (three RED arms); the ISA-string census: 2 authored edits with owners named, the derived surfaces need none; sources measured — no new pins (the supervisor chapter covers Svade inline) |
| `.2` (slice h, part 2 + LEAF) | `SEMULITH-P4-0013 (leaf P4-SYSTEM.2): slice h part 2 — the Sail privileged matched experiment (11/12 AGREE, the TW cell named, mm-counters not matchable); the leaf closes` | the matched override tracked (reference/sail-rv64gc-lab-v0.override.sexp; privileged 1.13, the declared selection minus Zicntr, no devices, WFI a nop except in U, medeleg 0x3FF); the dossier-format owners learned the new keys (schema + mapping, self-test 13→14); the evidence chain closed (tracked .sexp → derived JSON → Sail → 11/12 AGREE on the spec's values); mm-wfi's TW=1-in-S cell a named Sail-side gap (both wfi modes measured, the bit provably writable) routed to `.5`; mm-counters NOT MATCHABLE (the CLINT time-source wall vs D-PLATFORM; the counter rate is the environment's); the validator's own rules confirmed the corpus's claims (bit 10 reserved with H off, bit 11 undelegatable); the leaf's acceptance — the same instruction's behaviour tested in each supported mode — is the mode matrix itself |
| `.2` (slice h, part 1) | `SEMULITH-P4-0012 (leaf P4-SYSTEM.2): slice h part 1 — THE ATOMIC FLIP: the payload tracked, the route generated-definition, the corpus on the tracked engine` | the payload byte-exact (state.sexp, encoding.sexp, guests/ 62+run-order, interactions.sexp); D-RESOLUTION-ROUTE superseded by note (the D-FENCE convention; the mirror records' verbatim rule kept), D-ROUTE-FLIP recorded; the three generated mirrors tracked (their inputs tracked in the same commit — decision_generated-mirror-needs-tracked-input); exec_rv64gc ports the evaluator with the trap-END discipline; FlatMemory carries IALIGN as data; the CLI's `--profile` (run/demo wired, the rv64i-scoped commands refuse by name, rv64i byte-exact default); four gate gaps fixed at their owners (extraction refines, coverage pseudo leg, GEN censuses, fact-ownership re-pin); the CSR name↔address ownership migrated to the state document; the guests mirror governor registered (93+5); DERIVED-COUNTS 408→419 |
| `.2` (slice g) | `SEMULITH-P4-0011 (leaf P4-SYSTEM.2): slice g — the interactions.sexp: 7 axes × 28 cells, rehearsed green against the staged unit` | the axis set derived from the leaf's vocabulary (fault/alias/boundary/progress carried from the mirrored layers; legality + delegation added by the privileged machinery; restart reframed GUEST-shaped — the xret/xepc discipline, no mechanism cells; rv64i's event axis absorbed into the mode-cause story); the DIFFS rule forced the mirror's 4th/5th re-derivations (it-fencei/min-fencei's rv64i DIFF-FENCEI-EXECUTED pin is false for this unit — Zifencei declared, slot unbound; the divergence forms dropped with reasons recorded); 3 cells reported degenerate-with-reason; all 62 guests mapped, no new guests needed; the rehearsal ran the check's own invocation (28 cells, every disposition resolves, rc=0) with the three RED legs proven (DIFFS/orphan/omitted); DERIVED-COUNTS 408 unchanged |
| `.2` (slice f) | `SEMULITH-P4-0010 (leaf P4-SYSTEM.2): slice f — the base mirror executed (49/49), the mode-matrix corpus, the coverage rehearsal` | the scratch corpus runner (declared memory map, fault delivery, trap-END discipline, the per-step x-change comparison rule); 3 base guests re-derived BY DESIGN under D-IALIGN-16 (RVI-C 27.1), 46 byte-identical; 13 mm guests cover the 13 new forms across M/S/U (csr rw + per-mode legality, ebreak resume, ecall causes + medeleg delegation, mret/sret/wfi/sfence legality gates, counters + stimecmp gating, read-only/WARL); execution caught 14 stale auipc deltas, 2 M-level-CSR-in-S design bugs, 2 expectation mis-derivations — all re-derived, never fitted; coverage 65/65; no gate arms (untracked corpus; the governor lands at the flip), DERIVED-COUNTS 408 unchanged |
| `.2` (slice e) | `SEMULITH-P4-0009 (leaf P4-SYSTEM.2): slice e — the 65-form census (dual edit), the base-corpus mirror + authored records, the flip's staged encoding` | the pseudo-census decision (the spec's listings name the Zicntr reads; the encoding realizes them as csrrs specializations; coverage observes the spelling) recorded in the profile's scope comment; MIRROR-DERIVE (rule 14) governors the mirror via the registry; the dropped-`(extensions …)`-form pattern censused to SIX readers, all uniform now; the docs/tasks/ aggregate re-derived 1.5→3 MiB (the slice checklists are the designed growth); the staged payload's README records the flip mapping |
| `.2` (slice d) | `SEMULITH-P4-0008 (leaf P4-SYSTEM.2): slice d — the generators parameterize to rv64gc, the privilege machinery lands (tracked, over the generated tables), the scratch execution proof` | privilege.rs + 11 tests; the (legalize …) mini-language replaces prose (the WARL seam closed: engine applies descriptor data at lowering); gen_definition's rv64gc branch (8 operators lowered, PSEUDOS metadata; the THIRD dropped-extensions-form copy fixed); gen_guests directory-derived + run-order.txt (rv64i regenerates hash-only); elf.rs IALIGN parameter; the dossier-digest cascade re-derived; the fragile stale-pin arm fixed; the scratch proof 26/26 |
| `.2` (slice c2) | `SEMULITH-P4-0007 (leaf P4-SYSTEM.2): slice c2 refined — the rv64gc module's tracked landing is flip-bound; the scratch engine proof recorded` | a tracked generated module needs a tracked canonical input — measured against STATE-GEN's fresh-clone property; the three alternatives each dishonest; the scratch `rustc --test` proof (4/4) over the generated module recorded; `decision_generated-mirror-needs-tracked-input` + INDEX |
| `.2` (slice c1) | `SEMULITH-P4-0006 (leaf P4-SYSTEM.2): slice c1 — the privileged state constructs, the staged 33-CSR document, gen_state's rv64gc branch, the csr-set and reset-census gate arms` | slice (c) split recorded ((c1) zero Rust / (c2) the engine consumption); the state document staged at target/p4-system-2/ until the flip (the route contradiction is mechanical); gen_state composes per-field resets and cross-checks the csr-level value — fired RED naturally on the document being authored; csr name↔address ownership migration deferred to the flip, the 33/33 csrs.csv agreement probe recorded; STATE-GEN 17, PROFILE-CONSISTENCY 44, EXTRACTION 9 arms |
| `.2` (slice b) | `SEMULITH-P4-0005 (leaf P4-SYSTEM.2): slice b — the semantics language learns privilege: 8 operators, the zicsr/zicntr/system sem files, ECALL/EBREAK refined by declaration` | schema/semantics.sexp 32→39 forms + the READS-AND-WRITES contract; csr-write's WARL seam deferred to slice (c)'s tables at slice-(d) lowering; the corpus gate's dropped-extensions-form compose bug fixed (RED-first); check_citations --corpus binds sem files to pinning profiles; +encoding.h/+causes.csv pins (mstatus masks are figure-only in the spec); rv64i.sem.sexp untouched, rv64i's generated surfaces byte-exact |
| `.2` (slice a) | `SEMULITH-P4-0004 (leaf P4-SYSTEM.2): slice a — the Zicsr/Zicntr/privileged-system fragments from the re-pinned tables; the csr operand field; IALIGN as profile data` | the rv64gc references.sexp re-pin (5 new tables + shared arg_lut, sha256+bytes); the fetch route's extensions/ mapping (the moved tables hash byte-identical to the pins); the (pseudo …) fragment construct + the disjointness specialization rule (self-test 8→12); the resolver's dropped-extensions-form and advisory-dupes fixes measured at the first 3-extension composition; rv64i.sexp/m.sexp re-derived byte-identical; both profiles' verify routes green |
| `.1` | `SEMULITH-P4-0002 (leaf P4-SYSTEM.1): the profile resolved — rv64gc-lab-v0, every element source-located, the closure measured; the profile-resolution route` | the unit dossier (5 files: profile/sources/requirements/obligations/DOSSIER); 18 decisions mirrored twice (probe-derived, verbatim); schema/profile.sexp +profile-resolution with comparison optional; EXTRACTION/EXERCISE-COVERAGE/INTERACTION-MATRIX honor the route (self-tests 11/21/15); check_citations subdirectory + named-skip fix; gen_platform canonical ISA order; FACT-OWNERSHIP +4 rows (61), fixture re-pinned to six units |
| — | `SEMULITH-P4-0001 (tree P4-SYSTEM)` | the `.1` design brief: the pinned snapshot's privileged chapters measured present (24 priv + 46 unpriv pages); the selection decided (rv64gc-lab-v0, M/S/U, Sv39, IALIGN 16 with C, FP evidence at .7, SBI/psABI contracts); the output shape (unregistered unit dossier start) |

`P4-SYSTEM.7`'s closed slice checklists (b), (c1), (c2), (c3) part 1 and (c3) part 2,
split out verbatim on `2026-10-06` at the live file's crossing during slice (d2) (the
slice's records would have taken it past 131,072 B) — the `.4` slice-(c) precedent: a
completed slice's checklist moves while its leaf stays active:

`P4-SYSTEM.7` slice (b) — the FP state: the f-file + FS gating + the fcsr fix (`2026-10-06`, `SEMULITH-P4-0040`):

- [x] **REPRODUCE / ISSUE** — the brief's two latent defects re-measured live
  (the `target/p4-system-7/fsprobe` probe on the parent engine):

  ```
  permitted(fflags|frm|fcsr, read|write) at FS=Off: Ok ×6 — no gate anywhere
  fcsr reads 0x0 with fflags=0x1F, frm=3 (want 0x7f); the fcsr write REFUSED:
  "a view whose owner has no storage" — the comma literal resolves as ONE name
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — (i) the view resolution was single-owner:
  `index_by_name` looked the literal "fflags, frm" up as ONE CSR name
  (privilege.rs — measured above); (ii) `permitted()` had no FP-CSR arm —
  mstatus.FS was declared (WARL one-of 0..3, reset 0 = Off) and read by nothing.
  The FS-gate placement measured against the reference (`grep -n` over Sail
  0.14): the gate rides DECODE-time legality (`encdec … when
  currentlyEnabled(Ext_F)`, fext_insts.sail:888; `mstatus[FS] != 0b00`,
  fdext_control.sail:19) — dynamic state, not the encoding — so the CSR side
  lands in the permission model now, the instruction side is `fp_enabled()` for
  the binds' arms. No FP instruction decodes pre-bind (an unbound word is
  ReservedDecode → cause 2 already), so the FS=Off INSTRUCTION cells and the
  Dirty-on-f-write cell are the bind's — recorded, per the brief's fallback.

- [x] **FIX** — the `fp_registers` descriptor element (schema/state.sexp +
  dossier_sexp both directions + gen_state's validation/emission: FP_COUNT, the
  fregs field and reset, read_f/write_f, the PrivilegedHart accessor; the 4th
  REQUIRED_CENSUS_CANDIDATES entry) with the census candidate re-answered in
  place and the three FP-CSR statements refined; privilege.rs — the FS section
  (fs/fp_enabled/mark_fp_dirty), the permitted() arm, the multi-owner
  composition (compose_view/write_legalized), FP-CSR writes mark FS=Dirty
  (Sail's write_fcsr → dirty_fd_context, fdext_regs.sail:455); the corpus (2
  guests, EVD-05 spec-side via the forked tool) + the matrix cells.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core --lib → test result: ok. 134 passed (128 + 6:
  the FS cells × modes, the fcsr compose/split/retention, dirty + SD)
  $ bash scripts/check_state_gen.sh --self-test → 29 pass / 0 fail (28 + the
  fp-file RED arm)
  $ cargo test -p semulith-verify run_rv64gc → 4/4 groups, 103 guests
  (fp-fs-off 40 steps, fp-fcsr-view 20)
  $ python3 target/p4-system-7/identity.py <both CLIs, the parent worktree>:
  101 byte-identical, 0 diverge (5,491 trace lines); RED — both new guests
  DIVERGE on the parent engine (it caught the harness's own `--profile=`
  syntax bug first: two identical usage errors are not identity)
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (8 groups); `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 430→431 re-derived; STATE-GEN
  29 arms, both pairs byte-exact — rv64i untouched; DEF-GEN re-derived;
  INTERACTION-MATRIX no orphans; GUEST-GEN + the mirror); bench wasm 134,105
  bytes, smoke-bench 53 arms ok, both books.

- [x] **LOCKSTEP** — same commit: this tree (status + frontier + checklist +
  logs + changelog; the `.7` slice-(a) checklist archived at the 23rd ceiling
  firing, the `.6` slice-(b)/(c) changelog entries at the 24th), `MEMORY.md`
  (next_action → slice c — THE F BIND), `CHANGELOG.md`, `DEV_NOTES.md` (the
  promotion decision: PROMOTED — the must-diverge-control lesson, the knowledge
  card + INDEX + the map), `LIVE_STATUS.md` (431
  re-derived), `docs/book/src/plan/p4.md` (the `.7` section extended within the
  byte bound) + the book index, `docs/TASK_TREE.md` (unchanged — the frontier
  leaf is `.7` still).

`P4-SYSTEM.7` slice (c1) — frm holds any 3-bit value; the slice (c) split recorded (`2026-10-06`, `SEMULITH-P4-0041`):

- [x] **REPRODUCE / ISSUE** — the slice-(b) rule measured against the pinned chapter,
  then on the engine (the guest assembled by the tracked assembler, traced by the CLI):

  ```
  f-st-ext.html §20.1.2: "FSRM … writing a new value obtained from the three
  least-significant bits of integer register rs1 into frm"; rm table: 101–111 are
  "dynamic reserved rounding modes" (111: "In Rounding Mode register, reserved")
  $ semulith run fp-fcsr-view.elf --profile=rv64gc-lab-v0 --steps=20
  [15] x12 <- 0x45   (fcsr after writing 0xE5: frm RETAINED 2 — spec: 0xE5)
  [18] x14 <- 0x2    (frm after writing 6: RETAINED — spec: 6)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — `profiles/rv64gc-lab-v0/state.sexp` `frm_2_0`
  declared `(legalize (one-of 0 1 2 3 4))` at slice (b) — a laboratory WARL where the
  chapter writes the value and labels no WARL; the generated mirror carried it
  (`git diff` on `state_rv64gc.rs`: `Legalize::OneOf(&[0, 1, 2, 3, 4])`) into the
  WARL write path. The same misreading sat in the privilege unit tests (two
  assertions of retention) and the spec-side authoring tool (`grep -n "one-of 0..4"`
  → its frm/fcsr write model), so all three agreed with each other — no check could
  see it. Two companions measured: the tool's header template hard-coded
  "P4-SYSTEM.5 slice b, the interrupts corpus" into both FP guests, and it wrote
  directives into S-expression strings unescaped.

- [x] **FIX** — `frm_2_0` → `(legalize (any))` with the FSRM sentence quoted in its
  statement (and the census candidate's text); `gen_state.py` + `gen_definition.py`
  regenerated (the mirror's legalize row; the manifest's state hash); the unit tests
  rewritten to the spec (7 lands from a fcsr slice; 0b1110 → frm 6); the authoring
  tool's frm/fcsr model and header corrected, a `"` in a directive refused by name;
  `fp-fcsr-view` re-derived spec-side (step 13 now writes bit 8 — fcsr's "shall
  ignore writes … supply a zero value" legality), `fp-fs-off` re-derived (header
  only, values byte-identical); the matrix commentary; the book (below).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 4 passed (103/103)
  RED first — the re-derived expectations against the UNFIXED legalization:
  panicked at run_rv64gc/tests.rs:27:9: fp-fcsr-view: step 15 writes match the
  specification-derived expectations → test result: FAILED. 3 passed; 1 failed
  (restored; gen_state.py --check rc=0)
  $ cargo test -p semulith-core --lib → test result: ok. 134 passed
  $ derive_expectations.py q.s (a directive carrying a "quoted" phrase) → Refusal, rc=1
  ```

- [x] **NO REGRESSION** — `make check` rc=0 (core 134, verify 184, cli 17; fmt +
  clippy `-D warnings`); `make gate` → `=== all doctrines green ===` after the three
  ceiling crossings this slice's text triggered, each resolved by its own procedure:
  DEV_NOTES sharded (`scripts/shard_history.py --head DEV_NOTES.md`: 50,971 → 48,185
  B, "completeness: 22 entries before == 21 kept + 1 moved"); this file's closed-leaf
  changelog entries moved to the new `archive/P4-SYSTEM-3.md` (134,833 → 97,980 B;
  a scripted check: 22 entries before == 2 inline + 20 archived, order and bytes
  exact); the book's `plan/p4.md` (33,544 > 32,768) PARTITIONED per its registry row
  ("one chapter per subject") into six per-leaf chapters — DERIVED-COUNTS re-derived
  33 → 39 book chapters. INTERACTION-MATRIX ok.

- [x] **LOCKSTEP** — same commit: this tree (the split decision, the frontier, this
  checklist, the logs, the changelog entry, the archive-part-3 index line),
  `archive/P4-SYSTEM-3.md` (new) + part 2's forward pointer, `MEMORY.md`
  (next_action → slice c2), `CHANGELOG.md`, `DEV_NOTES.md` (PROMOTED — the
  knowledge card + INDEX + the map) + its shard, `LIVE_STATUS.md` (39 chapters),
  the book (`plan/p4.md` → overview + `plan/p4/*.md`, SUMMARY nested, the index
  regenerated; the duplicated heading and the stale `.3`/`.4` headings fixed),
  `docs/TASK_TREE.md` (unchanged — the frontier leaf is `.7` still).

`P4-SYSTEM.7` slice (c2) — the `rv_f`/`rv64_f` re-pin + the `f.sexp` fragment (`2026-10-06`, `SEMULITH-P4-0042`):

- [x] **REPRODUCE / ISSUE** — the pre-slice census: F pinned nowhere, no fragment.

  ```
  $ grep -c 'rv_f\|rv64_f' profiles/rv64gc-lab-v0/references.sexp → 0
  $ ls definitions/riscv/ → 13 files, no f.sexp; gen_fragments.py FRAGMENTS: 7 entries
  $ curl …/extensions/rv_f, rv64_f → 3,050 / 320 B; 26 + 4 real rows, 13 $pseudo_op
    rows (fmv.x.s/fmv.s.x, fmv.s/fabs.s/fneg.s, the 8 FP-CSR aliases of rv_zicsr)
  $ grep -E '"(rs3|rm)"' arg_lut.csv → "rs3", 31, 27 / "rm", 14, 12 (no re-pin)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the F bind's first input (the
  `.4`/`.6` bind shape — slice (a) of each). The design question this slice answers
  by measurement: which of the 13 pseudo rows the fragment carries. None — every one
  spells a real form, measured by its realizing base:

  ```
  $ grep -c '^$pseudo_op' rv_f rv64_f → 13 / 0
  $ grep -o '^$pseudo_op [a-z_]*::[a-z.]*' rv_f | awk '{print $2}' | sort | uniq -c
    1 rv_f::fmv.w.x  1 rv_f::fmv.x.w  1 rv_f::fsgnj.s  1 rv_f::fsgnjn.s
    1 rv_f::fsgnjx.s  3 rv_zicsr::csrrs  3 rv_zicsr::csrrw  2 rv_zicsr::csrrwi
  ```

  So the rv64i write-it-out policy applies and `gen_fragments.py`'s pseudo flag (for
  forms that exist upstream ONLY as pseudo-ops — Zicntr's) stays off; carrying the 8
  Zicsr-based aliases would also have made `riscv/f` require `riscv/zicsr` for
  spellings alone.

- [x] **FIX** — the ledger: `rv_f`/`rv64_f` pinned (sha256 + bytes) with the
  commentary and the `supplies` list (its missing comma before the A clause fixed in
  passing); `fetch_references.sh`: the F tables under the named exclusion until the
  bind (flip condition: the scope declares `flw`/`fsw`); `gen_fragments.py`: the
  `riscv/f` entry (requires `riscv/rv64i`, owns `rs3`/`rm`, no pseudos) →
  `definitions/riscv/f.sexp` (30 forms).

- [x] **ADDRESSED (verified)** —

  ```
  $ scripts/fetch_references.sh rv64gc-lab-v0 → FETCH riscv-opcodes/extensions/rv_f,
    rv64_f; MATCH both pins; MATCH encoding tables vs profile scope 88 == 88; MATCH
    owned fragments agree with the pinned upstream; fetch_references: ok
  $ cmp (the census fetch) (the tracked-route fetch) → byte-identical, both tables
  RED — the exclusion removed (a scratch copy): DIFFERS tables enumerate 118, profile
    declares 88, symmetric difference: fadd.s,fclass.s,… (exactly the 30 F names)
  $ python3 scripts/gen_fragments.py → regenerated 8 fragment(s); git status: only
    f.sexp new — the seven others byte-identical
  $ python3 scripts/check_sexp_schema.py definitions/riscv/f.sexp schema/fragment.sexp → ok
  $ python3 scripts/check_encoding_disjoint.py <the unit's 6 fragments> f.sexp →
    composed set: 115 instruction(s) (+ 3 pseudo-instruction(s)) from 7 fragment(s);
    no collisions, no duplicate names
  ```

- [x] **NO REGRESSION** — `scripts/fetch_references.sh --verify-only rv64i-lab-v0` →
  ok (52 == 52 unchanged); UNIT-COMPOSITION ok (3 units; rv64gc still PARTIAL with the
  f slot declared — the slot flips at the bind); SOURCE-FORMAT ok (241 files); no Rust
  touched, every generator `--check` byte-exact; `make gate` → `=== all doctrines
  green ===`.

- [x] **LOCKSTEP** — same commit: this tree (checklist, logs, changelog, status,
  frontier), `MEMORY.md` (next_action → slice c3), `CHANGELOG.md` (sharded at its
  ceiling: `shard_history.py` → shard 0193, "26 entries before == 25 kept + 1
  moved, order and bytes exact"), the book
  (`plan/p4/floating-point.md` + the overview's status line), `docs/TASK_TREE.md`
  (unchanged). DEV_NOTES: no entry — a mechanical re-pin on the `.4`/`.6` precedent,
  no new lesson (the pseudo-row decision is recorded above and in the fragment's
  own header).

`P4-SYSTEM.7` slice (c3) part 1 — the FP-CSR locators corrected (`2026-10-06`, `SEMULITH-P4-0043`):

- [x] **REPRODUCE / ISSUE** — found while locating slice (c3)'s citations: the pinned
  chapter's own heading numbers contradict the FP-CSR locators slice (b) wrote.

  ```
  $ (the h3 census of unpriv/f-st-ext.html) → 20.1.1. F Register State / 20.1.2.
    Floating-Point Control and Status Register / 20.1.3. NaN Generation … / 20.1.9
  $ git grep -n "RVI-F §20.1.1" → 9 fflags/frm/fcsr lines in state.sexp, 15 directives
    in the two FP guests (+ their derived expectations), privilege.rs:215, tests.rs:779,
    the c1 CHANGELOG/tree lines — all naming fcsr content; only state.sexp:55 (the f
    registers) is §20.1.1's
  $ (the d-st-ext.html h3 census) → 21.1.1. D Register State (FLEN=64) / 21.1.2. NaN
    Boxing — state.sexp:55 cited §21.1.2 for FLEN=64
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the locators were written from memory of the
  ratified chapter's layout, never measured against the pinned page's headings; the
  only citation tool cannot see the class: `grep -n "glob" scripts/check_citations.py`
  → line 180 reads `definitions/**/*.sem.sexp` rule sources alone, and it proves a §
  EXISTS in the pinned artifact (§20.1.1 does), not that it holds the cited content.
  State-document locators are outside every gate. Owned: tree `CITATION-ACCURACY`
  (opened next, a quoted-phrase-in-section gate).

- [x] **FIX** — every fcsr/fflags/frm locator → §20.1.2 (state.sexp ×9, both guests'
  directives, privilege.rs, the unit test, the c1 CHANGELOG and checklist lines);
  state.sexp:55's FLEN=64 → §21.1.1; the split decision's "§20.1.1–§20.2" → "§20.1.9".

- [x] **ADDRESSED (verified)** —

  ```
  $ git grep -n "RVI-F §20.1.1" (live surfaces) → state.sexp:55 only (the f registers)
  $ derive_expectations.py fp-fcsr-view.s fp-fs-off.s → 20 / 40 steps; git diff: only
    (source …) strings moved, every (value …) byte-identical
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 4 passed (103/103)
  $ python3 scripts/check_citations.py rv64gc-lab-v0 → 52 of 52 instruction citations resolve
  ```

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`
  (STATE-GEN/DEF-GEN/GUEST-GEN re-derived byte-exact — the mirrors re-hash only).

- [x] **LOCKSTEP** — this tree, `CHANGELOG.md`; MEMORY.md (next_action unchanged in
  substance — c3 part 2 after the CITATION-ACCURACY gate); no book surface cites these.

`P4-SYSTEM.7` slice (c3) part 2 — the semantics language learns FP (`2026-10-06`, `SEMULITH-P4-0044`):

- [x] **REPRODUCE / ISSUE** — the pre-slice census: the language had no FP vocabulary.

  ```
  $ git show HEAD:schema/semantics.sexp | grep -c "^(operator" → 44 (no freg, no FP operator)
  $ ls definitions/riscv/f.sem.sexp → absent; riscv_asm.py: registers x0..x31 only
  $ git log -S"the 43 forms" → 44cf271 (.4 slice b) — the typed count was 43 against 44
    operators from the day it was written (schema header, check_semantics docstring, and
    the emitted rv64gc Sem doc)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect for the vocabulary (the bind's input, the
  brief's decision 7); the measured design facts: (1) the register FILE of an operand is in
  no pinned table (`grep -c freg target/refs/riscv-opcodes/rv_f` → 0) — only the semantics
  can say it, so the assembler derives it from `(freg …)` use; (2) the Off gate's spec
  sentence quantifies over "any instruction that attempts to read or write the corresponding
  state" — a property of the rule, so the gate is the contract's, derived, never a per-rule
  guard; (3) Sail 0.14's accrual dirtiness is a configured policy (`fdext_regs.sail:451`,
  default `Fflags_Dirty_Precise`) inside the pinned FS section's implementation-defined
  latitude — the laboratory declares the same resolution.

- [x] **FIX** — `schema/semantics.sexp`: the floating-point block (the FP-state contract
  stated once + 18 operators: freg fbox funbox rounding fadd fsub fmul fdiv fsqrt fmadd fmin
  fmax feq flt fle fclass f2i i2f); `definitions/riscv/f.sem.sexp` (30 cited rules);
  `check_semantics.py` `check_fp` (rm resolved, `(rounding (field rm))` only, literal
  formats/widths/signedness, one register file per operand) + 6 arms; `gen_definition.py`:
  the `Surface` bundle (one value threaded instead of three parameters), the F lowering and
  enum variants gated on `riscv/f`, `check_fp` re-derived, the form count DERIVED (62) + 8
  DEF-GEN arms; `riscv_asm.py`: `load_register_files`, `_reg_of` (f0..f31 by the semantics,
  the other spelling refused), `rs3`/`rm`; the typed "43" removed from the prose.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/check_semantics.py definitions/riscv/f.sexp definitions/riscv/f.sem.sexp
    → 30 of 30 declared instruction(s) have checked semantics
  $ python3 scripts/check_semantics.py --self-test → 23 pass / 0 fail (17 + 6)
  $ check_citation_quotes (f.sem.sexp) → 26 attributed quote(s) judged … 0 finding(s)
  $ bash scripts/check_definition_gen.sh --self-test → DEF-GEN --self-test: 31 pass / 0 fail
    (the staged rv64gc+F composition lowers FReg/Rounding/FMadd/FToI/FUnbox; an unresolved rm
    and an FP operator without riscv/f both refused by name)
  $ python3 target/p4-system-7/asm_roundtrip.py → round trip: 30 of 30 agree (spike-dasm:
    mnemonic + registers; rm as bits 14..12 — this spike-dasm prints no rounding mode,
    measured); refusals: 6 of 6 by name
  ```

- [x] **NO REGRESSION** — both definition modules regenerate with only the generator hash
  and the derived form count moving (`git diff --stat` → 4 + 6 lines; the refactor is
  emission-neutral); both guest fixtures byte-identical (`gen_guests.py --check` rc=0 ×2);
  SEMANTICS ok (10 checks); `make check` rc=0 (core 134, verify 184, cli 17); `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 451 → 455 arms).

- [x] **LOCKSTEP** — this tree, `MEMORY.md` (next_action → c4), `CHANGELOG.md`,
  `LIVE_STATUS.md` (455), the book (`plan/p4/floating-point.md`; `annex/assembler.md` — the
  FP spelling), `docs/TASK_TREE.md` (unchanged — the leaf is `.7`).
