# P4-SYSTEM — archived completed-leaf designs

The recorded-before-execution design briefs of the completed leaves of the
[`P4-SYSTEM`](../P4-SYSTEM.md) tree — `.4` (atomics and reservations), `.3` (Sv39
translation and protection), `.2` (privilege and mode transitions) and `.1` (the
profile resolution) — split from the live file: `.2` and `.1` at its sixth per-part
ceiling crossing, `.3` at its seventh, `.4` at its thirteenth (the ceiling was
obeyed, not raised — the `P2-SCALAR-designs` precedent). The checklists live in
`P4-SYSTEM.md` beside this file. Archived design sections, verbatim:

- `2026-10-03` (design brief for `.2`, recorded before its execution; sources: the
  resolved unit dossier `profiles/rv64gc-lab-v0/` re-read in full this day; the pinned
  privileged chapters under `.materials/riscv/pinned-v20260120/priv/`; the route-branching
  gate code read at `scripts/check_extraction.py:200-288`, `scripts/check_exercise_coverage.sh`,
  `scripts/check_interaction_matrix.py`; the generator refusals at `scripts/gen_state.py`,
  `scripts/gen_definition.py`, `scripts/gen_guests.py`; two explore-agent censuses
  (definition-pipeline precedent; C15 feature inventory) — the reports are
  conversation-only, every load-bearing fact below re-measured by the signing engineer):
  **The measured pre-conditions.** (1) **The flip is atomic by construction.** Under
  `(vehicle (route profile-resolution))` an `encoding.sexp`, `state.sexp` or `guests/`
  beside the declaration is a refused contradiction (`check_extraction.py:224-239`,
  verified); the generated-definition legs demand scope == encoding == semantics ==
  requirements as sets both directions, every state element a reset, every obligation
  both checks (`check_extraction.py:259-288`); EXERCISE-COVERAGE demands every declared
  scope form EXECUTED by a guest; INTERACTION-MATRIX demands a complete, resolved
  matrix. A partial flip is RED by name — the unit-dir artifacts and the route edit
  land in ONE green commit. (2) **The unit today:** 5 dossier files, route
  `profile-resolution` (`profile.sexp:28`), scope = the 52-form RV64I census
  (`profile.sexp:27`), the 33-CSR committed minimum declared (`profile.sexp:25`,
  D-CSR-SET); no definition-pipeline artifact exists. (3) **The model has no privilege
  or CSR concept** — census: `git grep -ni 'csr\|privilege' -- crates/semulith-core/src
  definitions/ schema/semantics.sexp` finds only report-only comments:
  `crates/semulith-core/src/outcome.rs` reports traps to the harness ("this profile
  models no privileged CSR to hold it"); the generated `state.rs` census reads "no
  privilege modes are modelled"; the semantics language's 32 operators have no
  csr/mode/xret form, only `(trap cause tval)`. (4) **The generators are single-profile
  by refusal:** `gen_state.py` hard-codes `PROFILE = "rv64i-lab-v0"` and refuses any
  special-register id but `pc` BY NAME ("extend the generator behind the schema layer,
  never guess"); `gen_definition.py` refuses any unit but rv64i-lab-v0 and any ilen but
  32; `gen_guests.py` hard-codes the unit paths and a 51-name guest list and refuses
  expectation registers outside x0..x31 — so STATE-GEN/DEF-GEN/GUEST-GEN do not fire on
  rv64gc at all today. (5) **`m.sexp` has no semantics file** — census: `git ls-files |
  grep '\.sem\.sexp'` returns only `rv64i.sem.sexp`; M exists as the MODEL-COMPOSE.2
  composition test case, so any unit composing `riscv/m` must author `m.sem.sexp`
  (rv64gc does not compose M in `.2` — the slot is declared; the M evidence leaf owns
  the sem file). (6) **The assembler has no csr operand field** (the
  `USED_FIELDS`/`CONTIGUOUS_OPERANDS`/`SCRAMBLED_OPERANDS` closed sets) and hard-codes
  IALIGN=32 (`riscv_asm.py:486`) while rv64gc declares IALIGN=16 (D-IALIGN-16).
  (7) **No privileged matched experiment has ever run** — census: `ls
  target/refs/guests/*.log` and `git grep -l 'sstatus\|medeleg\|mret' -- profiles/
  target/refs/` show only user-mode rv64i evidence; Sail 0.14 exposes the full
  extension/privileged config namespace (unmatched; the effective-config dump attempt
  is recorded unsupported); Spike's bundled platform (Sv57 MMU, CLINT/PLIC, 16550)
  conflicts with this profile's Sv39 and no-CLINT — the DIFF-PLATFORM-SPIKE lesson
  applies, worse than for rv64i. (8) `.1` answered the tree's privilege-revision open
  question: Machine 1.13 + Supervisor 1.13 (D-PRIV-REVISION).
  **The design, decided** (the execution measures and fixes at root, the `.1`
  discipline):
  1. **`.2`'s own scope, drawn against its siblings.** `.2` owns: xRET semantics AND
     legality per mode (the privilege-stack pop, MPRV clear, pc←xepc — RVP-MACHINE
     §2.1.1.6.1, §2.1.3.2); trap entry/exit for **synchronous exceptions** (ECALL per
     mode, EBREAK, illegal-instruction — xPIE/xIE/xPP, xepc/xcause/xtval; ECALL/EBREAK
     set xepc to the instruction's own address, §2.1.3.1); the CSR access-permission
     matrix (address-map mode bits, read-only CSRs and read-only fields — RVP-CSR
     §1.1.1) with the 33 CSRs' per-field WPRI/WARL/WLRL tables (D-CSR-SET's deferred
     job); delegation mechanics (medeleg/mideleg — §2.1.1.8 — with this
     implementation's delegatable subset pinned in the state document as laboratory
     WARL choices: every synchronous cause delegatable except the read-only-zero
     `medeleg[11]` and `medeleg[16]`); mode-dependent decode legality: WFI
     (TW=0/1 × M/S/U; illegal in U with S present), SFENCE.VMA (illegal in U; TVM=1 in
     S; TVM also gates satp access), counter access (mcounteren/scounteren gating of
     cycle/time/instret; mcounteren.TM also gates stimecmp), Sstc's STCE gate.
     **Drawn out:** interrupt-CAUSED entry is `.5`'s (`.2` tests entry via exceptions,
     `.5` via interrupt injection); counter VALUES/rate/wrap/progress are `.5`/`.9`
     (D-ZICNTR), only the access-legality matrix is `.2`'s; WFI's WAKE is `.5`
     (D-PRIV-INSNS), only its trapping decode is `.2`'s; satp's Sv39 BEHAVIOUR is
     `.3`'s, only its access permissions are `.2`'s; MPRV's clear-on-xRET is `.2`'s,
     MPRV=1's load/store translation effects are `.3`'s; fault PRIORITY among
     simultaneous causes is `.8`'s. mcountinhibit stays excluded (the committed 33
     stands; inhibit semantics are `.5`'s contract decision); mtime/mtimecmp are
     memory-mapped environment state, not CSRs (`.5`/`.9`).
  2. **Composition at flip:** base `riscv/rv64i` plus new per-extension fragments —
     Zicsr (csrrw/csrrs/csrrc + immediate forms), the privileged system instructions
     (mret/sret/wfi/sfence.vma; census RVP-INSNS 18.1), Zicntr (rdcycle/rdtime/
     rdinstret) — with `(status partial)` and declared slots for m/a/f/d/c/zifencei
     (UNIT-COMPOSITION's declared-hole mechanism; m gets `m.sem.sexp` from its own
     evidence leaf, not `.2`). The scope census grows 52→65 with the new family lists
     by the mandated dual edit (`schema/profile.sexp` scope construct +
     `dossier_sexp._SCOPE_LISTS` together). The exact riscv-opcodes table carving is
     execution's measurement, per-table sha256 provenance as usual.
  3. **State:** `schema/state.sexp` gains a CSR construct and a current-privilege-mode
     element (a sanctioned schema edit — no construct exists today); `gen_state.py` is
     extended behind the schema layer exactly as its refusal instructs, to BOTH
     profiles, with rv64i's generated `state.rs` re-derived byte-identical. The 33
     CSRs' resets and per-field discipline tables carry their chapter locators; the
     SEM-08 hidden-state census is re-earned for the privileged state.
  4. **Engine + semantics language:** `schema/semantics.sexp` gains the CSR-read/
     CSR-write/mode-query/trap-delivery/xret operators (the operator set is
     schema-closed; the extension is a sanctioned schema edit); Zicsr refines the
     base's ECALL/EBREAK behaviour via a declared `(refines …)` — the case
     MODEL-COMPOSE.6's motivating comment names. semulith-core gains CSR state, the
     privilege stack, trap delivery per mtvec/stvec + delegation, and xRET;
     `outcome.rs`'s report-only vocabulary and the user-mode-only census lines are
     brought in line in the same commits (no stale comments).
  5. **Base-corpus inheritance by mirror-derivation.** rv64gc's base-form guests and
     instruction requirements are DERIVED from rv64i-lab-v0's corpus byte-identically
     by a recorded probe, registered in `doctrine/fact_ownership.tsv` (owner:
     `profiles/rv64i-lab-v0/guests/` + its requirements; mirror: the rv64gc base
     subset; governor: the derivation check), and then EXECUTED on the rv64gc engine —
     coverage is re-run, never inherited-by-claim. Soundness: same fragments, same
     semantics files, and base-form x-register observations are mode-independent
     under the reset state (M-mode, MPRV=0, no PMP) — asserted here, measured by
     execution. Weighed and rejected: relocating the corpus to a shared home (touches
     the registered unit's green gates for no `.2` benefit; revisit when a third unit
     arrives); inheritance-by-declaration without execution (execution on THIS unit
     is the coverage doctrine's point).
  6. **The mode-matrix corpus shape** (the leaf acceptance): guests ENTER S and U via
     delegation + xRET and execute the same instruction in each mode, observing
     through the ISA — CSR values read into x-registers by csrr, trap delivery
     observed through handler control flow, causes/xtval read inside the handler. The
     expectations vocabulary stays x0..x31 (no expectations-schema change at v0); the
     current mode is observed indirectly via per-mode CSR-access legality.
  7. **Generators parameterize, never fork:** gen_state/gen_definition/gen_guests
     extend to rv64gc behind the schema layer; every rv64i generated surface
     re-derives byte-identical (the three GEN gates stay green on rv64i); rv64gc's
     generated surfaces gain their own owner→mirror FACT-OWNERSHIP rows and the gates'
     census extends to both units. gen_guests' hard-coded 51-name list becomes
     directory-derived (a guest it cannot reconcile is still refused by name). The
     csr operand field enters the assembler whitelists derived from the pinned
     `arg_lut.csv` (the fence/fm precedent — never hand-typed); IALIGN becomes
     profile data (rv64i 32, rv64gc 16), retiring the `riscv_asm.py:486` assumption.
  8. **References:** the differential leg is a Sail privileged matched experiment,
     ATTEMPTED (the config namespace exists; the matched-override precedent from
     rv64i). Spike is recorded platform-conflicted for this profile (Sv57/CLINT vs
     Sv39/no-CLINT) with no matching claim. The primary evidence stays
     specification-derived expectations (EVD-05). If Sail's matched experiment fails,
     the affected axes read `incomplete`, never `passed` — the gap is recorded, not
     closed by prose.
  9. **Registration stays out of `.2`** (the `.1` precedent): units.sexp, the
     category-needs dispositions (C15's rv64gc row among them) and the model book
     arrive at registration day, a later leaf. The pinned-but-unselected privileged
     pages (hypervisor, smepmp, smstateen, smcdeleg, smcntrpmf, smctr, smdbltrp,
     ssdbltrp, sscofpmf, rnmi, zpm, priv-cfi, indirect-csr) are named here as
     pinned-not-selected (D-NO-H, D-NO-PMP) so the citation base has no silent gap.
  10. **Execution slicing** (checkpoints inside the leaf, each committed with the leaf
      id): (a) fragments + assembler whitelist + IALIGN data; (b) semantics-language
      operators + the new sem files; (c) state schema + gen_state + engine state and
      trap delivery; (d) gen_definition/gen_guests parameterization + engine exec of
      the CSR/trap instructions; (e) unit artifacts (state.sexp, encoding.sexp with
      slots, requirements growth, census dual-edit); (f) the guests corpus (base
      mirror + mode matrix) + coverage; (g) interactions.sexp; (h) the atomic flip
      commit + the full gate suite + the Sail attempt + the reports and the book.
  **Not `.2`'s scope:** m.sem.sexp and the M composition; C decode and IALIGN-16
  fetch changes (C uncomposed; IALIGN becomes DATA only); Sv39 walk/A/D/ASID (`.3`);
  atomics (`.4`); interrupt injection, counter progress, WFI wake (`.5`); FENCE.I
  (`.6`); FP (`.7`); fault priority (`.8`); contract v1 (`.9`); registration; the
  gate.


- `2026-10-02` (design brief for `.1`, recorded before its execution; sources: the
  materials census — `materials/catalog.sexp`, the pinned snapshot measured on disk this
  day; the explore-agent census of the profile machinery, references dossier, and P4
  history; `ROADMAP.md` §P4/§P6; `docs/CPU_ENVIRONMENT.md` §2; the explore report is
  conversation-only, every load-bearing fact below re-measured by the signing engineer):
  **The measured pre-conditions.** (1) The pinned snapshot **carries the privileged
  chapters**: `.materials/riscv/pinned-v20260120/` holds `priv/` (24 pages —
  `machine.html`, `supervisor.html`, `priv-csrs.html`, `priv-insns.html`, `sstc.html`,
  `smepmp.html`, …) and `unpriv/` (46 pages — `m/a/f/d/c-st-ext.html`, `zicsr.html`,
  `zifencei.html`, `counters.html`, `rvwmo.html`, `naming.html`, `rv-32-64g.html`, …),
  every file digest-pinned by the tracked `SHA256SUMS`. This matches the catalog's
  "46 unprivileged + 24 privileged pages" claim and **contradicts the category census's
  closing notes** (C12/C14/C15 say the privileged volume is "absent from this
  unprivileged snapshot" — measured false today; the census predates the snapshot's
  current content; the rows' corrections land with the unit's category-needs
  dispositions at registration, and this brief is their measured basis). (2) The
  "wanted" support materials are already in the cache: `riscv-sbi-2.0.pdf`,
  `riscv-elf-psabi-1.0.pdf`, `riscv-brs-1.0.pdf` under `.materials/riscv/` —
  digest-verifiable, adoption = citing them. (3) The encoding corpus has exactly one
  extension fragment (`m.sexp`, generated from the pinned riscv-opcodes rv_m/rv64_m);
  rv_a/rv_f/rv_d/rv_c/zicsr… tables are NOT pinned — that re-pin belongs to the evidence
  leaves, not `.1`. (4) References: Sail 0.14 exposes the full extension/privileged
  config namespace (the matched override disables it today); Spike's default platform
  (Sv57, CLINT/PLIC/16550) is not matchable from its command line — the
  DIFF-PLATFORM-SPIKE lesson applies to any P4 matching; the SoftFloat shared ancestry
  (184/199 byte-identical) is already routed to `.7`. (5) The Rust bare-metal minimum is
  `riscv64imac` (`reference_what-running-real-rust-actually-requires`); the toolchain is
  clang/lld 21.1.8 (`decision_c-guest-routing-and-toolchain`).
  **The selection, decided** (the full per-element locator table is the execution's
  business; these are the design decisions it must evidence):
  1. **The unit is `rv64gc-lab-v0`.** Base RV64I + extensions **M, A, F, D, C, Zicsr,
     Zifencei**; privilege modes **M, S, U**; translation **Sv39**; harts 1 (multicore
     is MC-MULTICORE's, never smuggled); xlen 64, endianness little (the field is data
     since `P5-BOARD.6`). With C present, **IALIGN is 16** (ILEN stays 32) — a concrete
     consequence the resolution must state, with its locator. The revision is the
     pinned publication's (`v20260120`) with each chapter's own stated version measured
     from the page — the rv64i-lab-v0 versioning model, extended to the privileged
     chapters.
  2. **The closure is measured, not inferred from "GC".** G = IMAFD + Zicsr + Zifencei
     (`naming.html` / `rv-32-64g.html`); D implies F; F/D imply Zicsr (the FP CSRs);
     C's RV64 decomposition (Zca, and Zcd with D) — every implication cited from the
     pinned chapter that states it (SCP-02).
  3. **FP is IN the profile; its execution evidence is `.7`'s.** Linux's standard
     userspace ABI is lp64d (psABI — measured at execution), which requires D; the
     roadmap's provisional GC stands. The alternative (declare rv64imac now, FD later)
     is rejected: it would fork the profile identity at the .7 landing, and the
     honest-verdict machinery already carries declared-but-unevidenced scope as
     `incomplete`, never as a pass. The model implements no FP before `.7`'s backend
     qualification (the tree's non-goal, unchanged).
  4. **Interrupt/counter acceptance semantics are CPU-contract content** (the privileged
     interrupt model, `counters.html`, `sstc.html`); CLINT/PLIC are board-layer — the
     P4-profile board branch, not this tree (the P5-BOARD archive records the layering).
  5. **Firmware/toolchain requirements:** SBI 2.0 (cached, ratified) as the M-mode
     firmware contract the P6 route will execute (ROADMAP §P6: real firmware, never a
     host-modelled SBI silently); psABI 1.0 (cached) for the toolchain ABI; the
     toolchain stays clang/lld 21.1.8 with the rv64gc target. DT-SPEC/BRS stay `wanted`
     — P6's boot hardware description is not `.1`'s.
  6. **The citation rule extends, unchanged in kind:** the pinned snapshot's `priv/`
     pages are the citation authority for privileged content (same publication identity
     as the unprivileged pages); the PDFs stay reference-only (the numbering trap —
     `docs/knowledge/a-version-string-is-not-an-identity.md`). Each page's stated
     version is measured from the page, not presumed.
  7. **The output shape:** `profiles/rv64gc-lab-v0/` carries `profile.sexp` (the
     selection as data — the schema already supports every field needed, `extensions`
     and `privilege_modes` and the state block's `csrs` included), `sources.sexp` (the
     pinned pages, digests re-derived from the tracked SHA256SUMS), and `DOSSIER.md`
     (the resolution narrative: the per-element locator table, the closure, the
     rejected alternatives). **Unregistered** — registration day and its consequences
     (units.sexp, category-needs dispositions, the book) belong to a later leaf, the
     `.2`/`.11` precedent. Requirements/obligations/expectations catalogues arrive with
     the evidence leaves (`.2`+); `.1` ends with the selection complete and citable.
  **Not `.1`'s scope:** the extension encoding fragments and their riscv-opcodes re-pin;
  reference rv64gc matching (Sail config exists; Spike's platform problem is recorded);
  OpenSBI adoption; the P4-profile board branch; the CSR list's *semantics* (`.2`+);
  registration; the gate.


---

(archived verbatim from `docs/tasks/P4-SYSTEM.md` at that file's seventh per-part ceiling
crossing, `2026-10-04` — the `.3` design brief, its leaf closed `2026-10-04`; the ceiling
was obeyed, not raised. What follows is the verbatim text of the decision entry.)

- `2026-10-03` (design brief for `.3`, recorded before its execution; sources: the pinned
  privileged chapters re-read (`.materials/riscv/pinned-v20260120/priv/supervisor.html`
  §11.1.1.11–§11.1.10, `machine.html` §2.1.1.6.4, §2.1.7.2, Table 7); the `.2` landing
  measured in tree (`exec_rv64gc.rs` hooks, `state.sexp:569-581` satp,
  `system.sem.sexp:53` the stated sfence nop); the U54 data point re-verified from the
  pinned PDF `.materials/sifive/fu540-c000-v1p5.pdf` §4.7; Sail 0.14's TLB and A/D code
  paths measured in `target/refs/sail-riscv-src/model/sys/vmem*.sail`; two explore-agent
  censuses (C12 scope; translation machinery deltas) — the reports are conversation-only,
  every load-bearing fact below re-measured by the signing engineer):
  **The measured pre-conditions.** (1) **The hooks are three sites**: fetch
  (`exec_rv64gc.rs:87`), load (`:291`), store (`:328`) go straight to the boundary with
  physical addresses; page-fault causes 12/13/15 exist nowhere in core (census: `git
  grep -c PageFault -- crates/ | wc -l` → 0); satp's storage/discipline landed at `.2`
  (`state.sexp:569-581` — MODE `(one-of 0 8)`, reset Bare; the census names `.3`'s
  reopen); sfence.vma is a stated nop in four places (`system.sem.sexp:14-19,53-59`,
  the generated mirror, the state census). (2) **The walk falsifies a load-bearing
  requirement**: REQ-D-FETCH-IMPLICIT's "Explicit reads and writes are made only by
  load and store instructions" (`profiles/rv64i-lab-v0/requirements.sexp:27`) is false
  the moment satp.MODE=Sv39 — every S/U access entails up to 3 implicit 8-byte reads.
  (3) **The observation vocabulary cannot see memory**: expectations are x0..x31 writes
  + `never_written` + one-fetch-per-step (`schema/expectations.sexp:48-53`;
  `run_rv64gc/tests.rs:22-47`); a hardware A/D update is an implicit store no
  instruction owns — no expectation form can pin it (measured, both files). (4) **The
  A/D crux**: the pinned 1.13 text makes hardware update the DEFAULT when neither
  Svade nor Svadu is implemented (§11.1.3.1), and the profile selects neither
  (`profile.sexp:25`); the one measured implementation precedent — the U54 the
  profile's Sv39 choice already cites (D-SV39) — "does not automatically set the A and
  D bits … Instead, the U54 MMU will raise a page fault" (FU540 §4.7, re-verified from
  the pinned PDF). (5) **Sail models a 64-entry unified TLB** "so that we can
  meaningfully test SFENCE.VMA which would be a no-op without a TLB"
  (`vmem_tlb.sail:9-12`); `--trace-ptw`/`--trace-tlb` exist but are excluded from
  `--trace`; its A/D code (`vmem.sail:92-128`) does hardware update exactly when
  `¬Svadu ∧ ¬Svade` — the tracked override's current setting — and flipping to the
  Svade policy is a one-field override change its validator accepts
  (`validate_config.sail:176-181`). (6) **A generator hole**: `gen_state.py`'s rv64gc
  path (`validate_gc`) silently IGNORES `memory_spaces` instead of refusing it (the
  rv64i path refuses at :103-106) — to be closed the next time the state document is
  edited.
  **The design, decided** (the execution measures and fixes at root, the `.1`/`.2`
  discipline):
  1. **OQ-2 answered: the profile ADDS Svade** (page-fault-instead-of-A/D-update).
     The evidence chain the acceptance demands ("validated against the selected
     extensions and revision, not chosen as a knob"): (i) the pinned revision defines
     exactly two schemes and names the page-fault one Svade (§11.1.3.1, §11.1.10); (ii)
     the profile's own translation precedent — the U54, already load-bearing in D-SV39
     — implements exactly that scheme (FU540 §4.7, quoted above); (iii) the
     laboratory's observe-through-the-ISA discipline (`.2` decision 6) can evidence a
     page fault (scause/stval via csrr) but CANNOT evidence an implicit PTE write
     (pre-condition 3), so the hardware-update default would price a new observation
     vocabulary (sized like `.2`'s slice-b) to test a side effect the laboratory need
     not produce. The identity cost is recorded: the extension list and ISA string
     gain `svade` (`rv64imafdc_zicntr_zicsr_zifencei_sstc_svade`, canonical order —
     the `.1` gen_platform fix); Svadu is NOT selected (menvcfg's ADUE stays WPRI);
     the Sail override's `Svade` flag flips `true`. Weighed and rejected: hardware
     update + a memory-write expectations vocabulary (the pricing above; it can arrive
     with Svadu the day a consumer needs it, never silently). The DOSSIER's OQ-2
     closes with this brief; the profile-identity edit (D-SVADE decision + REQ/OB
     mirrors) is execution's first slice.
  2. **A minimal, fully-specified TLB is modelled.** The leaf's own goal names
     "translation invalidation", and invalidation is testable only with something to
     invalidate (the Sail comment, pre-condition 5, is the same reasoning). Shape: a
     small fully-associative cache (size and FIFO replacement stated in the state
     census), ASID-tagged (ASIDLEN = 16, the Sv39 maximum and Sail's default —
     laboratory choice, recorded; ASID=0-only rejected: it would make the tagging
     rules untestable), G-bit retention per §11.1.2.1. The TLB is hidden state: the
     SEM-08 census re-answers `present true` with the cache described; the
     determinism rule is stated — the cache is a pure function of the hart's own
     history, so cold-reset re-execution and snapshot/replay stay exact (corpus must
     never depend on stale-hit behaviour outside the spec's latitude). sfence.vma
     gains its real effect with the FOUR rs1/rs2 cases implemented as specified
     (§11.1.2.1); the over-fence latitude ("always legal") is recorded-not-taken, so
     the G-bit retention and per-ASID cases are genuinely tested. Weighed and
     rejected: no cache (walk every access) — conformant, but it leaves the leaf's
     goal item untestable and forfeits the Sail PTW/TLB differential.
  3. **Translation is evaluator machinery, not a tree operator** — a
     `translation.rs` core module beside `privilege.rs` (the `.2` pattern), hooked at
     the three sites (pre-condition 1). Fetch is not a tree node, so a `(translate …)`
     operator could never cover it; hook-level uniformity beats tree-level
     partiality. The 10-step walk (§11.1.3.2 with LEVELS=3/PTESIZE=8 per §11.1.4.1)
     is cited step-by-step in the module: the canonical-VA check, reserved-bit/
     PBMT/N checks (bits 63/62–61/60–54 zero — neither Svnapot nor Svpbmt selected),
     superpage misalignment, U/SUM/MXR (step 6), R/W/X (step 8), and Svade's step-9
     page fault. Page-fault causes 12/13/15 enter the core vocabulary (the raw-u64
     rv64gc cause path absorbs them; the typed-enum asymmetry is a stated choice).
  4. **Effective mode is a single computation**: fetch uses the current mode;
     loads/stores use MPP when MPRV=1 (§2.1.1.6.4 — the `.2` deferral lands, with
     SUM/MXR per the effective mode); M-mode fetch is never translated.
  5. **Fetch translates in 16-bit parcels.** With C in the profile (IALIGN=16), a
     4-byte instruction may straddle a 4 KiB boundary; each 16-bit parcel translates
     independently (the architecturally natural reading; Sail's two-16-bit-fetch
     granularity is the measured reference precedent, DIFF-FETCH-GRANULARITY).
  6. **Walk accesses get their own boundary variant.** The D-FETCH-IMPLICIT precedent
     (implicit accesses observable as their own `Request` variant) applies: PTE
     reads/writes cross the environment boundary as a distinct walk-access kind
     (8-byte, physical), never silently as data `Load`s. REQ-D-FETCH-IMPLICIT is
     AMENDED by a new versioned requirement record naming the walk's implicit
     accesses (the old record superseded, never edited); the one-fetch-per-step test
     keeps its meaning (walk reads are not fetches); a walk-count witness may join
     the sv39 guests. **Contract negotiation, recorded:** the FORMAL contract
     versioning of this boundary vocabulary is `.9`'s charter ("translation inputs",
     versioned not edited) — `.3` lands the engine variant and the requirement
     amendment, and routes the contract-document wording to `.9`; it does not
     pre-empt it.
  7. **Misaligned-vs-page-fault priority is pinned now**: the current engine judges
     misaligned before the boundary (= higher priority than page/access faults);
     Table 7 makes this implementation-defined, so the choice is legal and stays;
     the full priority TOPIC is `.8`'s, with this hand-off line recorded (the `.2`
     decision-1 pattern).
  8. **No new instructions, no new matrix axis.** The scope census, EXTRACTION and
     EXERCISE-COVERAGE denominators are unchanged (Sv39 adds machinery, not forms);
     the 62-guest corpus stays green because satp resets to Bare, an EXACT identity
     path (measured: every existing guest runs in M/Bare). New sv39 guests join the
     EXISTING matrix cells (fault×fault, fault×delegation, legality×…): translation
     is machinery under the declared interaction kinds, not a new kind (an 8th axis
     would cost 8 new cells to buy nothing).
  9. **Corpus shape**: guests build page tables in M-mode (stores), csrw satp,
     sfence.vma, sret into S/U; observation stays through the ISA (csrr scause/stval;
     `ld`-back of PTEs — under Svade the permitted page-table side effects are NONE,
     so the acceptance's second half is evidenced by proving the tables byte-identical
     after accesses, plus the staleness/fence behaviour through the TLB). Expectations
     stay x0..x31 (no vocabulary change — the discipline that priced decision 1).
  10. **Execution slicing** (checkpoints inside the leaf, each committed with the leaf
      id): (a) the Svade identity edit (profile.sexp + D-SVADE + REQ/OB mirrors +
      sources + Sail override flip) and the `validate_gc` memory_spaces refusal; (b)
      the translation module + the three hooks + effective mode + the Bare-identity
      proof (62/62 unchanged); (c) the walk with its fault matrix + reserved-bit and
      superpage checks + the requirement amendment + walk-access boundary variant;
      (d) the TLB + sfence.vma's real four-case effect + the census/snapshot/
      determinism consequences; (e) MPRV=1/SUM/MXR + the sv39 guests + matrix cells +
      the Sail matched experiment (PTW/TLB traces explicit) + the reports and the
      book.
  **Not `.3`'s scope:** fault priority as a topic (`.8` — the pinned option and the
  hand-off line above); interrupt injection during walks (`.5`); LR/SC page
  constraints (`.4`); contract v1's formal wording (`.9`); Svnapot/Svpbmt/Svadu/
  Sv48/Sv57 (unselected, named); PMP (D-NO-PMP); the hypervisor extension (D-NO-H);
  registration.



---

(archived verbatim from `docs/tasks/P4-SYSTEM.md` at that file's thirteenth
per-part ceiling crossing, `2026-10-05` — the `.4` design brief, its leaf closed
the same day; the ceiling was obeyed, not raised. What follows is the verbatim
text of the decision entry.)

- `2026-10-04` (design brief for `.4`, recorded before its execution; sources: the pinned
  A and memory-model chapters re-read (`.materials/riscv/pinned-v20260120/unpriv/
  a-st-ext.html` §12.1.1–§12.1.4 — 39 norm anchors — Version 2.1 measured from the page
  title; `unpriv/rvwmo.html` §17.1–§17.1.3 incl. Tables 6/7 — Version 2.0; `priv/
  machine.html` §2.1.6.3–§2.1.6.4 the atomicity PMAs and the exception table; `priv/
  supervisor.html` the AMO fault rules); the unit measured in tree (`encoding.sexp:14`
  the declared slot, `profile.sexp:29` the 65-form scope, `state.sexp:640-641` the
  pre-declared reservation candidate, `references.sexp:84-92` the pins, `override.sexp:6`
  the Sail platform attributes); Sail 0.14's A implementation measured in
  `target/refs/sail-riscv-src/model/extensions/A/` + `sys/sys_reservation.sail` +
  `sys/sys_control.sail`; two explore-agent censuses (the C16/A-extension scope against
  the pinned chapters; the machinery deltas) — the reports are conversation-only, every
  load-bearing fact below re-measured by the signing engineer, including one census
  claim measured FALSE and corrected at pre-condition 7):
  **The measured pre-conditions.** (1) **The slot is declared, the fragment absent**:
  `encoding.sexp:14` `(slot (id a) (requires "riscv/a"))` under `(status partial)`;
  `definitions/riscv/` holds no `a.sexp`/`a.sem.sexp` (census: `ls definitions/riscv/` —
  9 files; M is the same shape of hole: `m.sexp` landed, `m.sem.sexp` is its own
  evidence leaf's); `gen_fragments.py:46-88`'s FRAGMENTS tuple has 5 entries, no A. The
  scope census is 65 forms with A contributing 0 (`profile.sexp:29`; D-SCOPE-CENSUS:
  the declared scope grows only with the fragment). (2) **The encoding tables are not
  pinned**: `references.sexp:85-92` pins 8 files with `rv_a`/`rv64_a` absent by the
  stated policy ("pinning a table nothing derives from would invite a reader to believe
  it is used", :84; census: `grep -n 'rv_a\|rv64_a' references.sexp` rc=1); the fetch
  route maps `rv_*` names to `extensions/<name>` (`fetch_references.sh:175-179`, the
  `2026-10-03` upstream move). The pinned A chapter carries NO encodings — the format
  diagrams are images (the rv64i dossier's measured finding); the pinned RVWMO Tables
  6/7 (`rvwmo.html` §17.1.3) enumerate exactly the 22 forms (11 `.W` + 11 `.D`) that
  upstream `rv_a`/`rv64_a` row-list, so the pin corroborates rather than surprises.
  (3) **The assembler cannot express an A form**: the whitelists carry no
  `aqrl`/`aq`/`rl` (`riscv_asm.py:68-74`), the mnemonic token is looked up whole so
  `lr.w.aq` misses (`riscv_asm.py:589-601`), and the `lr.w rd, (rs1)` /
  `sc.w rd, rs2, (rs1)` parenthesized-address spelling has no operand-shape special
  case. The pinned `arg_lut.csv` already carries the positions (`"aqrl",26,25`,
  `"aq",26,26`, `"rl",25,25`, `"amoop",31,27`) — derived, never typed; no re-pin of it.
  (4) **The semantics language has no atomic operator, and a tree decomposition is
  wrong on the fault cause**: the memory operators are exactly `(load width signed?
  addr)` and `(store width addr value)` (`schema/semantics.sexp:71-72`); the boundary
  vocabulary is `Request::{Fetch, Load, Store, WalkAccess}` (`env.rs:67-103`) — no
  atomic kind; no operator sets, matches, or cancels a reservation. An AMO decomposed
  as `seq(load, op, store)` is expressible but delivers cause 13 where the architecture
  demands a store/AMO cause: "AMOs never raise load page-fault exceptions … attempting
  to perform an AMO on an unreadable page always raises a store page-fault exception"
  (`supervisor.html`); "load and load-reserved instructions generate load exceptions,
  whereas store, store-conditional, and AMO instructions generate store/AMO exceptions"
  (`machine.html`). (5) **The reservation is pre-declared but ungated**:
  `state.sexp:640-641` declares the "reservation set (LR/SC)" candidate `present true`
  with `.4` owning it ("recorded here so .4 cannot smuggle it in silently");
  `gen_state.py:472-481`'s census gate fires only on the TLB candidate — the
  reservation's emit path (field + reset + accessor, the TLB precedent at
  `gen_state.py:540,560,702`) is this leaf's to build. (6) **The spec's single-hart
  surface is exact** (the a-st-ext re-read, every phrase located): any SC invalidates
  the reservation, success or failure ("Regardless of success or failure, executing an
  SC.W instruction invalidates any reservation held by this hart", §12.1.2); an SC
  pairs only with the most recent LR in program order (§12.1.2); the must-fails that
  can fire at one hart are the address-not-in-reservation-set and the intervening-SC
  cases — the other-hart-store and device-write must-fails are vacuous at harts=1 and
  are the environment's inputs when they exist (the `CPU_ENVIRONMENT.md` §2 row,
  verified: "Report external invalidation events required by the selected contract");
  failure writes a nonzero code to rd (value 1 = unspecified failure; "Portable
  software should only assume the failure code will be non-zero"), writes no memory,
  and "does not give rise to any memory operations" (RVWMO §17.1.1.1); success writes
  0 to rd. The constrained loop is at most 16 sequential instructions of the base-I
  subset (Zca/Zcb permitted), same address and size, and the eventuality guarantee is
  on the EXECUTION ENVIRONMENT (§12.1.3) — "Implementations are permitted to
  unconditionally fail any unconstrained LR/SC sequence." Misalignment raises "an
  address-misaligned exception or an access-fault exception" — the implementation's
  choice (§12.1.2, §12.1.4; causes 6/7, `machine.html`'s exception table), its priority
  against page/access faults implementation-defined (the `.3` decision-7 precedent
  already pins misaligned-first). The failed-SC UNSPECIFIED translation side effects
  (§12.1.2) are DISCHARGED by the profile's Svade: the named side effect is the D-bit
  update Svade replaces with a fault — no side effect can exist. (7) **Sail 0.14's
  reservation is four platform externs** (`sys_reservation.sail:20-23`: load/match/
  cancel/valid, taking `physaddrbits` — physical-address keyed), cancelled at exactly
  two call sites (census: `grep -rn cancel_reservation model/ --include='*.sail'`):
  every SC (`zalrsc_insts.sail:76`) and reset (`sys_control.sail:448`, "For
  implementations with the "A" standard extension, there is no valid load
  reservation"). The explore census's "cancelled on privilege transitions" is measured
  FALSE for 0.14 — the header comment's aspiration is not the code. The override needs
  NO change: A is `supported true` (Zaamo/Zalrsc `false` is Sail's internal naming; A
  enables them), and the memory region already declares `atomic_support "AMOCASQ"`,
  `reservability "RsrvEventual"`, misaligned `(amo "AccessFault") (lrsc "AccessFault")`
  (`override.sexp:6`). (8) **C16's disposition is rv64i's row**: no rv64gc section
  exists in `materials/category-needs.sexp` (census: `grep -n rv64gc` rc=1 over the
  file); the rv64i row routes the memory-consistency closure wholesale to MC-MULTICORE.
  `.4` SPLITS C16 — the single-hart reservation semantics land here; everything whose
  truth needs ≥2 observers (the global memory order, PPO rules 5–7, RCsc/RCpc effects,
  the Atomicity Axiom's other-hart clause, Ztso; locators `rvwmo.html` §17.1.1–
  §17.1.1.4, every aq/rl effect defined "as viewed by other RISC-V harts" §12.1.1)
  stays MC-MULTICORE's, as D-RVWMO (`profile.sexp:47`) already records. The rv64gc C16
  disposition lands at registration day (the `.1` precedent — the unit is deliberately
  unregistered).
  **The design, decided** (the execution measures and fixes at root, the `.1`/`.2`
  discipline):
  1. **Scope: the A fragment is Zaamo + Zalrsc's 22 forms** — the chapter's own
     composition ("The A extension comprises instructions provided by the Zaamo and
     Zalrsc extensions", §12.1): LR/SC and the nine AMOs, each `.W` and `.D` (RVWMO
     Tables 6/7 the pinned enumeration; `rv_a`/`rv64_a` the encoding source, pinned
     through the `extensions/` route). The scope census grows 65 → 87 by the mandated
     dual edit at the bind, not before (D-SCOPE-CENSUS). aq/rl DECODE but order nothing
     observable at one hart — every effect is defined "as viewed by other RISC-V
     harts" (§12.1.1); all four aq/rl combinations assemble and execute identically,
     including the software-discouraged ones (the "Software should not" of §12.1.2 is
     a software rule, not a decode illegality — execution measures the wording).
  2. **The reservation is exact, minimal hart state**: one reservation = (physical
     address, width, valid) of the most recent LR — the reservation SET is exactly the
     accessed word's/doubleword's bytes, the minimal conformant set ("An implementation
     can register an arbitrarily large reservation set … provided [it] includes all
     bytes of the addressed data word or doubleword", §12.1.2; the TLB's
     minimal-fully-specified precedent). Keyed on the PHYSICAL address (the Sail
     precedent; the aliasing latitude — "allowed to succeed … using an alias … also
     allowed to fail" — resolved to exact physical match, laboratory authority).
  3. **The deterministic SC policy is DATA**: SC succeeds iff reservation valid ∧
     physical address equal ∧ width equal, writing rs2's value and rd←0; otherwise it
     fails with rd←1 (the "unspecified failure" code), writing nothing. It NEVER
     spuriously fails — one legal point of the architectural nondeterminism, picked so
     the exact-value expectations stay derivable (EVD-05 + the declared policy);
     authority laboratory, stated in the state document beside the reservation. Under
     it, a constrained loop at one hart succeeds on its FIRST SC — the eventuality
     guarantee's degenerate one-hart form, recorded; the environment-fairness wording
     is `.9`'s contract (the `CPU_ENVIRONMENT.md` §3 "eventually" rule cited).
  4. **Invalidation is exactly the spec's set at one hart**: any LR replaces; any SC
     (success or failure, any address) clears; nothing else — a trap does NOT
     invalidate (the spec gives no such rule; §12.1.3's trap is only a loop-exit
     event), and the context-switch guidance ("a store-conditional instruction to a
     scratch word … during a preemptive context switch") is SOFTWARE's duty, not
     machinery. The external-invalidation event (another hart's store, a device write)
     cannot arise at harts=1 with no devices: the CPU-side RULE (an invalidated
     reservation fails its SC) is validated at the module level by direct
     invalidation; the boundary vocabulary for an environment to DELIVER such an event
     is `.9`'s contract item (the `.3` contract-wording routing), never smuggled.
     Sail 0.14's exact two cancellation points (every SC, reset — pre-condition 7)
     match this set at one hart.
  5. **AMOs lower as one new operator with store/AMO fault semantics** — NOT a
     `seq(load, op, store)` tree: the decomposition is expressible but delivers the
     wrong fault cause (pre-condition 4). The operator carries the closed nine
     operations; it translates ONCE under the store/AMO rules (never a load page
     fault; an unreadable page faults 15), reads the old value, computes, writes, and
     sets rd to the old value (`.W` sign-extended) — one instruction, the `.8`
     candidate's discipline ("every instruction completes or faults as a unit"). The
     boundary crossing is a load followed by a store to the same address (Sail's own
     write_ea→read→write_value shape); a new `Request::Atomic` variant was weighed and
     rejected: it would push the nine operations' semantics into the environment — the
     wrong layer — and at one hart the pair IS the single operation of RVWMO
     §17.1.1.1. LR/SC get their own operators (`load-reserved`;
     `store-conditional` yielding the code for rd) — the `tlb-invalidate` precedent
     for an operator's full pipeline path (schema → sem file → gen_definition → Sem
     variant → evaluator arm).
  6. **Misaligned atomics take the access-fault cause (7), matching the pinned
     reference**: the spec offers misaligned-or-access-fault (§12.1.2/§12.1.4); the
     laboratory's plain load/store policy is cause 4/6 (measured: `exec_rv64gc.rs`'s
     Load arm delivers 4 before the boundary) but the tracked override's region
     declares `(amo "AccessFault") (lrsc "AccessFault")` — choosing 7 for the atomic
     kinds is equally legal and makes the matched experiment's misaligned cells AGREE
     rather than recorded-divergent. Authority laboratory, reference-matched; the
     alternative named in the decision record. The misaligned-before-translation
     priority stands (the `.3` decision-7 hand-off; the fault-priority TOPIC stays
     `.8`'s).
  7. **The observation vocabulary is unchanged**: SC's code is an ordinary rd write;
     an AMO's memory effect is observed by a later load (the bound-ext read-back
     pattern); the reservation itself stays hidden by design (the census's candidate).
     No expectations-schema change — the discipline that priced `.3`'s decision 1.
  8. **The corpus families** (names at execution): `a-amo-*` — the nine operations ×
     `.W`/`.D`, the sign-extension edges, min/max signed-vs-unsigned cells, rd=rs1/rs2
     overlaps, the aq/rl suffixes executed; `a-lrsc-*` — the paired sequence
     succeeding, the must-fails (SC to a different address; an intervening SC to any
     address; LR replacing a reservation), the any-SC-clears case, a failed SC's
     no-memory-write proven by read-back, a constrained loop terminating on the first
     SC under the declared policy (decision 3's degenerate form); the misaligned cells
     (cause 7) and the translated-AMO cells (an AMO on an unreadable Sv39 page → 15,
     never 13) riding the `.3` machinery.
  9. **No new matrix axis** (the `.3` precedent): the new guests ride the seven
     existing axes — fault (the misaligned and translated-AMO cells), legality
     (reserved encodings: LR with rs2≠0, reserved AMO funct values — execution
     measures the tables), alias (rd=rs1=rs2), boundary (the `.W` sign-extension),
     progress (LR/SC sequences), delegation (a translated AMO's page fault routed),
     restart (a faulting atomic's xepc discipline).
  10. **The landing is an ATOMIC BIND, the `.2` discipline**: binding the slot
      (`(extensions "riscv/a")` replacing `(slot (id a) …)`) makes EXTRACTION and
      EXERCISE-COVERAGE judge the 22 forms — encoding AND semantics AND requirement
      AND execution, one green commit. Slices (a)–(d) build and prove in staging
      (untracked `target/`, the `.2` precedent); the pins, fragment, assembler,
      operators and reservation state land tracked-green BEFORE the bind exactly as
      `m.sexp` and the TLB did (additive, no unit artifact judged).
  11. **Execution slicing** (checkpoints inside the leaf, each committed with the
      leaf id): (a) the `rv_a`/`rv64_a` re-pin + the `a.sexp` fragment (the FRAGMENTS
      entry, the aqrl field ownership) + the assembler's A machinery (the field
      whitelist, the `.aq`/`.rl` suffix rule, the `(rs1)` spelling); (b) `a.sem.sexp`
      + the new operators through the schema/check/generator path; (c) the
      reservation state (the census-candidate gate generalised, the emit, the
      module) + the deterministic policy as data + the engine's AMO/LR/SC arms proven
      in scratch; (d) the staged corpus + expectations + the matrix rehearsal; (e)
      THE BIND: slot→extension, the 65→87 census dual edit, the requirement/
      obligation growth, the generated mirrors, the corpus tracked, the matrix
      cells — one green commit with the full gate suite; (f) the Sail matched
      experiment + the reports and the book + the leaf acceptance.
  **Not `.4`'s scope:** the multicore memory model (MC-MULTICORE, pre-condition 8's
  locators); the external-invalidation boundary vocabulary and the eventuality/
  fairness contract wording (`.9`); fault priority as a topic (`.8` — the
  misaligned-first precedent stands); Zacas/Zawrs/Zabha and the other unselected
  atomic extensions (named, pinned-not-selected); `m.sem.sexp` (M's own evidence
  leaf); F/D/C/Zifencei (their leaves); the rv64gc C16 disposition (registration
  day); registration; the gate.

The closed leaves `.5` (interrupts, counters and wait), `.6` (instruction visibility) and
`.7` (the floating-point backend qualification — its design brief and its four slice-split
and slice decisions), split from the live file verbatim on `2026-10-06` at the `.8` design
brief's crossing (the ceiling was obeyed, not raised):

- `2026-10-06` (slice (e) execution split, recorded with (e1) — the Sail leg measured first,
  as each prior leaf's matched attempt was; sources: the override re-materialized from the
  tracked unit (byte-identical to the `.6` materialization; validate-config rc=0; F and D
  supported, `Fflags_Dirty_Precise` sail's default; FourState FS), the brief's decision 2
  re-read): **(e1)** the Sail matched experiment over the FP corpus — an ENCODING/STATE match
  (sail's FP is SoftFloat externs: one opinion with spike's, EVD-04), recorded as the
  ledger's sixth experiment; **(e2)** the independent numeric fixtures AT SCALE — tracked and
  gated, expected values from the exact-rational reference (`scripts/specfp.py`: neither
  SoftFloat, APFloat nor MPFR), seeded directed + random operands per operation × mode ×
  width, run against `fp.rs` by a unit test under FP-VECTORS' DRIFT rule (the 230 directed
  vectors are the rules; the fixtures are the breadth), and the model layer's per-op cost
  re-measured on this host (the leaf's performance evidence, slice (a)'s harness shape);
  **(e3)** the reports (the decision record's closing measurement), the book, and the LEAF
  ACCEPTANCE — "a decision record with measured correctness and performance evidence" —
  then the frontier to `.8`.

- `2026-10-06` (slice (d) execution split, recorded with (d1) — its measurements taken before
  any (d) edit; sources: the fetched `rv_d`/`rv64_d` (2,091/465 B — 26 + 6 = 32 forms, the
  brief's census re-derived; 3 `$pseudo_op` rows, fmv.d/fabs.d/fneg.d); the pinned
  `d-st-ext.html` re-read (§21.1.1–§21.1.7); `rv_f`/`rv64_f` on upstream master re-fetched
  byte-identical to the pins; the machinery re-measured): **the FP vocabulary is already
  width-generic** — every operator takes the format `n` as data (`schema/semantics.sexp`'s
  FP block: `fbox`/`funbox` "n = 64 is the identity", `fp::funbox` returns `v` at 64), the
  f-file is FLEN=64 since slice (b), `misa` already reads `0x14112D` (D's bit 3 set — the
  declared selection) — so D's 32 rules reuse the 18 operators, and the language gains
  exactly ONE: the format conversion FCVT.S.D/FCVT.D.S (`f2f`: a signaling-NaN input raises
  NV and yields the canonical NaN; widening is exact, narrowing rounds by rm). Its model
  carries the qualification record's deviation (ii) — the backend raises no NV for an sNaN
  through a format conversion (24 measured cases) — patched in `fp.rs`, the record's own
  disposition. **The execution split** (the (c) shape, minus what (c) already built): (d1)
  the `rv_d`/`rv64_d` re-pin + the `d.sexp` fragment (requires `riscv/f` by name — D
  depends on F and reuses its rs3/rm; owns no field; the pseudo rows written out, as F's)
  under the bind-gated named exclusion; (d2) the language: `f2f` (schema, check, lowering,
  `Sem` variant), `d.sem.sexp` (32 rules), the gated lowering and the assembler's derived
  register files on a staged composition; (d3) `fp.rs`'s format conversions with deviation
  (ii) patched, `specfp`'s conversion, FP-VECTORS extended; (d4) the staged D corpus with
  its EVD-05 derivations; (d5) THE BIND (slot → extension, the census 118 → 150, the arms,
  the corpus, the matrix). ⚠ **Corrected at (d3)**: deviation (ii) does not exist — the
  backend, measured, raises NV for a signaling NaN through a format conversion; the record's
  24 cases were the MPFR oracle's (it has no signaling NaN). `fp.rs` patches nothing there;
  the record carries a second amendment.

- `2026-10-06` (slice (c4) part 1, recorded before execution — a §13 data-locality defect of
  slice (a), measured while preparing (c4)'s scratch driver): `ls ~/.cargo/registry/src/*/`
  → `rustc_apfloat-0.2.3+llvm-462a31f5a5ab` (src + `.crate`, mtime 2026-10-06 08:39 — slice
  (a)'s landing) inside the SHARED user-home cache (666 crates of many projects). Slice (a)
  recorded "the cargo cache stays on-volume" for its own fetch, but the workspace has no
  mechanism making ROUTINE builds use it: no `.cargo/config.toml`, no `CARGO_HOME` in the
  Makefile, the shell's `CARGO_HOME` unset — so since the workspace's first registry
  dependency every plain `cargo` run (`make check`, the wasm gate) resolves `rustc_apfloat`,
  `bitflags` and `smallvec` through `~/.cargo`. **The fix, decided:** `.cargo/config.toml`
  source replacement — the one mechanism EVERY cargo invocation inside the repository obeys
  — to an UNTRACKED on-volume directory `.app-data/vendor/` populated by `make vendor`
  (`cargo vendor --locked` under the on-volume `CARGO_HOME`; `cargo vendor` ignores
  `[source]` by default, so it populates a missing directory); identity stays the tracked
  `Cargo.lock`'s checksums. Untracked, not committed: the repository's stance on third-party
  content is "catalogue identity, cache locally, never redistribute" (`.materials/`), and a
  commit of 1.1 MB of third-party source would be permanent in history; the cost is one
  populate step in each CI workflow and in bootstrap. The shared cache is NOT cleaned (§13:
  never delete an ambiguously shared global cache); the project stops consulting it.

- `2026-10-06` (slice (c) execution split + a slice-(b) defect, recorded before execution;
  sources: the fetched `rv_f`/`rv64_f` (3,050/320 bytes — 26 + 4 = 30 forms, 13 pseudo
  rows: the two old fmv names, fmv.s/fabs.s/fneg.s, the 8 FP-CSR aliases — the brief's
  census re-derived exactly); the pinned `f-st-ext.html` re-read (§20.1.1–§20.1.9); the
  machinery re-measured (`gen_definition.py`'s per-fragment variant emission,
  `exec_rv64gc.rs`'s `Frame`, `riscv_asm.py`'s x-only register spelling)):
  **The defect, measured — `frm` must hold any 3-bit value.** Slice (b) declared
  `frm_2_0` WARL one-of 0..4 with an illegal write RETAINING the old value. The pinned
  chapter states the opposite twice: "FSRM … writing a new value obtained from the three
  least-significant bits of integer register rs1 into frm" (no legalization), and the
  rm table names 101–111 *dynamic reserved rounding modes* — a state frm can only reach
  by holding them (the table's 111 row: "In Rounding Mode register, reserved"). The spec
  labels no WARL on frm; a laboratory WARL where the spec writes the value is a
  deviation, not a latitude. `fp-fcsr-view` pinned the wrong rule (steps 13–18), the
  privilege unit tests asserted it, and the authoring tool modelled it. Its reach: the
  dyn-rm resolution this slice lands needs frm=5..7 reachable. **The pinned revision's
  reserved-rm wording, recorded**: "The behavior of floating-point instructions that
  depend on rounding mode when executed with a reserved rounding mode is reserved"
  (weakened from the ratified illegal-instruction mandate, which "is still valid
  behavior") — the laboratory takes illegal-instruction (cause 2, xtval the word) for
  both static 101/110 and dynamic 101–111, Sail's `Fcsr_RM_Illegal` shape
  (`fext_insts.sail:51-63`). Two book defects ride the same fix: `plan/p4.md` carries
  a duplicated `## Gate CPU-SYSTEM` heading (introduced at slice (b)) and the `.3`/`.4`
  section headings still read "underway" over bodies recording closed leaves.
  **The execution split** (the brief's slice (c) is the `.4`/`.6` bind shape — four of
  `.4`'s six slices — so it executes as checkpoints, each committed with the leaf id):
  (c1) the frm defect fixed at root (state.sexp + the generated mirror + the unit tests
  + the authoring tool + `fp-fcsr-view` re-derived, its header's stale `.5` provenance
  line corrected with `fp-fs-off`'s) + the two book defects; (c2) the `rv_f`/`rv64_f`
  re-pin + the `f.sexp` fragment (owning `rs3`/`rm`) under the bind-gated named
  exclusion; (c3) the semantics language learns FP — the FP-state contract stated once
  (the f-file read/write, the Off gate judged at the instruction head for any rule
  that touches FP state, accrual sticky and Dirty-marking), the operators, `f.sem.sexp`,
  the lowering — and the assembler's FP spelling (f-register class DERIVED from the
  semantics' own operand use, never typed); (c4) `fp.rs`, the model layer over
  rustc_apfloat (the target policy + the two measured deviations patched + sqrt), unit-
  proven; (c5) the staged F corpus with its EVD-05 derivations; (c6) THE BIND (slot →
  extension, the census 88 → 118, the arms tracked, the corpus tracked, the matrix).
  The FS gate's placement is decided here: the Off sentence quantifies over "any
  instruction that attempts to read or write the corresponding state", so the gate is
  the FP-state contract's, judged at the head of every instruction whose rule touches
  FP state — never a per-rule guard a rule could forget, never the f-file accessor
  (an `flw` at FS=Off must raise 2, not the load's own fault).

- `2026-10-05` (design brief for `.7`, recorded before its execution; sources: the pinned
  FP chapters re-read (`.materials/riscv/pinned-v20260120/unpriv/f-st-ext.html` §20.1.1–
  §20.1.4, `d-st-ext.html` §21.1.2 — Versions 2.2/2.2 measured from the page titles;
  `priv/machine.html` the FS field); the routed ancestry record re-read in full
  (`docs/decisions/reference_softfloat-shared-ancestry.md`); the rule texts quoted
  (`RULES.md` RUST-01/SEM-03/EVD-04, `docs/ARCHITECTURE.md` §6); the unit measured in tree
  (`state.sexp:70` misa, `:101-103` FS, `:604-631` the FP CSRs, `:642-643` the census
  candidate; `privilege.rs:163-166` the single-owner view resolution; `encoding.sexp:
  16-17` the slots); Sail 0.14's FP measured in `target/refs/sail-riscv-src/model/core/
  softfloat_interface.sail` + `extensions/FD/`; two explore-agent censuses (the candidate
  landscape + ancestry; the machinery deltas) — the reports are conversation-only, every
  load-bearing fact below re-measured by the signing engineer where it lives in this
  repository, and the candidate-landscape claims re-measured at slice (a), which IS the
  qualification):
  **The measured pre-conditions.** (1) **The declared-then-trapping window is real**:
  misa advertises F and D (read-only `0x14112D`, `state.sexp:70`) while every FP word
  decodes reserved → cause 2 (the decode miss → `run_rv64gc.rs:99-104`); the f/d slots
  sit at `encoding.sexp:16-17`; no `f.sexp`/`d.sexp` (7 FRAGMENTS entries), no
  `rv_f`/`rv_d`/`rv64_f`/`rv64_d` pins. The upstream census (execution re-derives from
  the fetched tables): F = 30 forms (26 rv_f + 4 rv64_f; 13 pseudos incl. the 8 FP-CSR
  aliases), D = 32 (26 rv_d + 6 rv64_d; 3 pseudos); the pinned `arg_lut.csv` already
  carries `rs3` (31..27) and `rm` (14..12). (2) **The SoftFloat shared ancestry is
  re-verified**: 184/199 `.c` files byte-identical across the two vendored copies (the
  active decision record); Sail's ENTIRE FP surface is SoftFloat externs
  (`softfloat_interface.sail:42` — every operation `pure {cpp: "softfloat_*"}`; no
  independent Sail FP path exists); both checkouts present (sail `29e6158`, spike
  `1e05dda`). Two descendants agreeing is one opinion (EVD-04); the record's own
  escape: "a hardware observation, an independently implemented arithmetic, or a
  specification-derived expected value computed by hand." (3) **The candidate
  landscape** (web research, re-measured at slice (a)): exactly two pure-Rust,
  wasm-compilable, non-SoftFloat candidates — `rustc_apfloat 0.2.3+llvm-462a31f5a5ab`
  (LLVM APFloat lineage; the version string pins the source commit; its docs claim no
  unsafe/global state/side-effects) and `softfloat 1.0.0` (independent authorship,
  no_std + const, TestFloat-verified upstream); every SoftFloat-derived option fails
  RUST-01 (FFI) or PORT-WEB (wasm) or EVD-04 (ancestry); native host floats fail §6 on
  CAPABILITY grounds (no per-op rounding-mode control, no flag access, NaN-payload
  nondeterminism on wasm32) — the textual bar is "silent", the capability bar is
  decisive. MPFR is a third independent lineage for expected-value generation;
  `testfloat_gen`'s operands-only mode is lineage-clean, its computed expectations are
  not. (4) **The target policy is model-layer, never backend** (ARCH §6's own
  sentence): canonical NaN (`0x7fc00000` single, §20.1.3 — "Except when otherwise
  stated, if the result of a floating-point operation is NaN, it is the canonical
  NaN"); NaN-boxing ("The upper bits of a valid NaN-boxed value must be all 1s";
  unboxed input → the n-bit canonical NaN; §21.1.2); the FMA ∞×0 NV rule; the
  fmin/fmax NaN rules; subnormals full IEEE 754-2008, no FTZ latitude (§20.1.4);
  sticky accrued flags (§20.1.1); dyn/frm resolution with rm 101/110 reserved →
  illegal. No crate ships this policy — APFloat quiets sNaNs and follows LLVM payload
  conventions; the model layer owns the mapping opStatus → NV/DZ/OF/UF/NX.
  (5) **Two latent defects `.7` owns at root** (re-measured): (i) fcsr's
  `(view_of "fflags, frm")` is a TWO-owner view — the engine resolves ONE
  (`privilege.rs:163-166`; the generated mirror carries the literal `"fflags, frm"`,
  `state_rv64gc.rs:427`), so fcsr reads 0 and writes refuse TODAY; (ii) mstatus.FS is
  declared (bits 14:13, WARL one-of 0 1 2 3, reset 0 = Off, `state.sexp:101-103`)
  with NO gate anywhere — `permitted()` has no fflags/frm/fcsr arm, so FP CSR access
  at FS=Off is not illegal today; the spec gates the unit's instructions AND its CSRs
  (machine.html's Off-state sentence; Sail's `fdext_control.sail:19`).
  (6) **Observation through x-registers is complete** (the machinery census's table,
  spot-verified): `fmv.x.w`/`fmv.x.d` move raw bits, `feq/flt/fle` land 0/1, `fclass`
  the 10-bit mask, the `fcvt.*.w/l` forms convert, `fsw/fsd` read back by integer
  loads, fflags/frm via csrrs — no expectations-vocabulary change (the `.2`
  mode-matrix discipline); the f-file stays census-hidden state (`state.sexp:642-643`
  names `.7` its owner). (7) **The FS policy the corpus needs**: FS resets 0 = Off
  (laboratory), so every FP instruction and FP-CSR access is illegal until M software
  enables — the corpus sets FS first (the `.2` counter-gating precedent); the
  four-state FS with Dirty-on-f-write (Sail's `dirty_fd_context`; the override's
  `fs_legal_states FourState`) is the measurable, reference-matching choice; SD is
  already computed. (8) **Performance machinery**: `semulith bench` refuses rv64gc by
  name (`main.rs:1092` — "a later leaf"); the leaf's performance evidence is a
  scratch timing harness over the candidates (per-op costs on this host), not the
  tracked bench; the PORT-WEB wasm gate mechanically excludes every C-FFI option.
  (9) **C07 and the Zcd inheritance**: FP is category C07; rv64i's row reads
  "Closing: an F/D-admitting profile revision" — this unit IS that revision, but no
  rv64gc section exists in `category-needs.sexp` (registration day, the `.1`
  precedent). The C slot inherits 4 Zcd forms when D binds (D-EXT-CLOSURE: "C
  decomposes as Zca always plus Zcd when D is present") — Zcd rides the C leaf,
  named, never smuggled; the override already runs Zcd true.
  **The design, decided** (the execution measures and fixes at root, the `.1`/`.2`
  discipline):
  1. **The qualification runs FIRST, in scratch, and is the leaf's own slice (a)** —
     the leaf's title is the qualification. Probe harnesses (untracked `target/`)
     evaluate both candidates against (i) each other, (ii) MPFR-generated expected
     vectors over a directed operand corpus (zeros, subnormals, NaNs with payloads,
     infinities, rounding-boundary halves, conversion edges — plus seeded pseudorandom
     streams; `testfloat_gen`'s operands-only mode if fetchable, a recorded generator
     otherwise), per operation × rounding mode × both widths, and (iii) per-op timing
     on this host. The criteria are ARCH §6's: rounding modes, flags, result bits,
     conversions, NaN payloads, the boxing surface. The outcome is a decision record
     in `docs/decisions/` with the measured tables — and the fallback named: if
     neither passes, implement the required subset in Rust and defer the capability
     (the gate reads `incomplete`, never `passed`).
  2. **The independence argument, stated once**: the qualified backend is confirmed
     by the OTHER candidate + MPFR vectors — three lineages, none Berkeley. Sail/Spike
     FP agreement is recorded as one opinion (EVD-04); the closing Sail matched
     experiment is an ENCODING/STATE match (decode, FS gating, NaN-boxing, flag
     accrual points, the fmv paths), never numeric independence — the numeric
     independence comes from the fixtures. This is the honest reading of the routed
     constraint.
  3. **The dependency joins as a workspace crate with its ancestry recorded** —
     RUST-01 satisfied (pure Rust by default); the decision record carries the exact
     version, the pinned source commit, the license (measured at execution), the
     ancestry inventory, and the wasm-build proof (PORT-WEB stays green; the cargo
     cache stays on-volume, the `.app-data/cargo-home` precedent). If license or wasm
     fails: the other candidate; if both: the fallback (decision 1).
  4. **The model layer owns the target policy** (pre-condition 4): a new core module
     (`fp.rs`, the privilege/translation pattern) between the evaluator arms and the
     backend crate, every rule cited to the pinned chapter — canonical NaN, NaN-
     boxing/unboxing, the opStatus→flags mapping, dyn/frm resolution (reserved rm →
     illegal), the FMA and fmin/fmax NaN rules, subnormal passthrough.
  5. **FS gating lands with FP** (pre-conditions 5, 7): the four-state FS with
     Dirty-on-f-write (SD already computed); the gate applied to FP instructions AND
     the fflags/frm/fcsr CSRs — both latent defects fixed at root with tests; the
     FS=Off illegal cells are guests; the corpus sets FS≠0 before any FP use.
  6. **fcsr's two-owner view fixed at root** (pre-condition 5): the view resolution
     learns the composition (the generator already splits the comma list for
     validation — the engine's read/write paths learn it; the cheapest honest fix,
     measured), with fcsr read/write guests.
  7. **The semantics language gains fp operators** — op-as-data where the encoding
     carries it (the `(amo op …)` precedent); the flags side channel is genuinely new
     (values are `(u64, width)` today): the fp operator yields result+flags and the
     tree accrues (Sail's `accrue_fflags` shape), the exact form execution measures
     with the sem-corpus gate as judge. NaN-boxing is bit-level (expressible today);
     the IEEE arithmetic is the backend's.
  8. **Observation stays through x-registers** (pre-condition 6): no expectations-
     vocabulary change; the corpus bootstraps on the fmv/fclass/compare forms
     arriving with the same bind.
  9. **Execution slicing** (checkpoints inside the leaf, each committed with the
     leaf id): (a) the backend qualification (the scratch harnesses, the measured
     tables, the decision record, the dependency landing with the wasm proof); (b)
     the FP state (the f-file + FS gating + the fcsr fix + fflags/frm semantics +
     the census re-answer) with the FS=Off corpus; (c) the F bind (30 forms +
     pseudos, the pin/fragment/assembler/corpus — the `.4`/`.6` bind shape); (d) the
     D bind (32 forms + FLEN=64 NaN-boxing + the corpus); (e) the independent
     numeric fixtures at scale + the Sail encoding/state match + the reports and
     the book + the leaf acceptance.
  **Not `.7`'s scope:** Zcd's 4 compressed forms (the C leaf — pre-condition 9);
  Zfa/Zfh/Zfinx/Zdinx/Zfhmin (unselected, named); Q (unselected); the tracked rv64gc
  bench mix (a later leaf — scratch timing here); the rv64gc C07 disposition
  (registration day); the m/c slots (their leaves); the hypervisor (D-NO-H);
  registration; the gate.

- `2026-10-05` (design brief for `.6`, recorded before its execution; sources: the pinned
  chapters re-read (`.materials/riscv/pinned-v20260120/unpriv/zifencei.html` — Version 2.0
  measured from the page title; `unpriv/intro.html` the implicit-reads latitude;
  `unpriv/rvwmo.html` §17.1); the unit measured in tree (`encoding.sexp:18` the slot;
  `state.sexp:652-653` the fetch-cache candidate; the four selfmod/fencei guests;
  `references.sexp` both profiles; `rv64i.sem.sexp:137-138` the fence nop); Sail 0.14's
  FENCEI measured in `target/refs/sail-riscv-src/model/extensions/Zifencei/
  zifencei_insts.sail:20-33` + an icache grep over `model/`; two explore-agent censuses
  (the C13/Zifencei scope; the machinery deltas) — the reports are conversation-only,
  every load-bearing fact below re-measured by the signing engineer):
  **The measured pre-conditions.** (1) **The slot waits; the pin and fragment are
  absent**: `(slot (id zifencei) (requires "riscv/zifencei"))` at `encoding.sexp:18`
  (five slots remain after `.4`'s bind); no `definitions/riscv/zifencei.sexp`, no
  FRAGMENTS entry (6 entries, `gen_fragments.py:46-99`), `rv_zifencei` pinned nowhere
  and absent from `target/refs/riscv-opcodes/` (both censuses re-run); upstream
  carries exactly one row (73 bytes) under the `extensions/` route. The SPEC side is
  already pinned (`sources.sexp:49` RVI-ZIFENCEI 2.0). (2) **The engine is
  always-coherent by construction**: fetch re-reads every step (`fixtures.rs:161-162`
  — "Re-read every time: OB-CODE-VISIBILITY — a store to a later-fetched address is
  visible to the next fetch immediately"); a store commits before StoreDone; no write
  buffer; the TLB caches translations, never contents (`translation.rs:62-87`). The
  census candidate "instruction-fetch cache state" is `present false`
  (`state.sexp:652-653`) — but its why is rv64i's verbatim recording and says
  "without Zifencei", FALSE for this declaring unit the moment the slot binds.
  (3) **fence.i is a nop on both sides of the differential**: the base fence is a
  declared nop (`rv64i.sem.sexp:137-138`, D-FENCE); Sail's FENCEI execute is
  `sail_barrier` + "fence.i is a nop for the memory model"
  (`zifencei_insts.sail:20-33`) with NO icache state anywhere in `model/` (grep
  census); the tracked override already carries `Zifencei supported true` — the only
  gap is the unbound slot on this side. (4) **The spec's contract is three sentences
  and two latitudes** (the zifencei re-read, every phrase located): "RISC-V does not
  guarantee that stores to instruction memory will be made visible to instruction
  fetches on a RISC-V hart until that hart executes a FENCE.I instruction"; "A
  FENCE.I instruction ensures that a subsequent instruction fetch … will see any
  previous data stores already visible to the same RISC-V hart"; "A FENCE.I
  instruction orders all explicit memory accesses that precede the FENCE.I in
  program order before all instruction fetches that follow" — and "An instruction
  fetch is always ordered before any explicit memory accesses that instruction gives
  rise to." The latitudes: coherent caches or uncached RAM means "just the fetch
  pipeline needs to be flushed at a FENCE.I" (a re-read-per-fetch machine has nothing
  to flush); "base implementations shall ignore these fields [funct12, rs1, rd], and
  standard software shall zero these fields". RVWMO §17.1 explicitly does NOT
  formalize fetches/FENCE.I — no memory-model obligations to discharge. intro.html's
  implicit-reads sentence is the sharpest stale-state form (a valid implementation
  could "cache as many fetchable (executable) bytes as possible … and avoid reading
  main memory for instruction fetches ever again") — the locator D-CODE-VISIBILITY
  cites. (5) **The inherited obligations are named in the corpus**: it-fencei and
  min-fencei's comment blocks pre-commit "the slot-binding leaf re-derives this file
  to the legal fence.i when the slot binds" (both quoted); fault-selfmod (a rewrite
  with NO synchronization) and dir-selfmod-fence (a rewrite behind the DATA fence —
  which per decision 4's contract does NOT synchronize fetches) already execute;
  DIFF-FENCEI-EXECUTED is rv64i's record, dropped for this unit at `.2` slice (g).
  (6) **The vocabulary suffices, with one named limit**: visibility is observed
  through the patched instruction's EFFECTS (fault-selfmod's step-5 x2←7) or a
  trap's tval — the per-step insn text is not machine-asserted
  (`run_rv64gc/tests.rs:22-31` compares order + writes); on an always-coherent
  engine a with/without-fence.i pair cannot differ observably beyond fence.i's
  decode legality itself.
  **The design, decided** (the execution measures and fixes at root, the `.1`/`.2`
  discipline):
  1. **The bind is the `.4` checklist miniaturized to one form**: pin `rv_zifencei`
     through the `extensions/` route; the FRAGMENTS entry → generated
     `zifencei.sexp` (owns NO fields — imm12/rs1/rd are the base's; requires
     `riscv/rv64i`; funct3=1 against fence's 0); a hand-written `zifencei.sem.sexp`
     with `(effect (nop))` and the shall-ignore rule cited; slot→extension with the
     mandated census dual edit 87→88 (a one-form `zifencei_*` family); gen_definition
     regenerates (no new Sem variant — the existing nop); the fetch-leg census flips
     on its own (88==88); no new operators, no new state, no assembler shapes (the
     zero-operand ecall/ebreak precedent).
  2. **fence.i's effect is the declared nop — the honest landing, not a shortcut**:
     the coherent/uncached-RAM latitude (pre-condition 4) sanctions it; Sail lands
     identically ("a nop for the memory model"), so the matched experiment can AGREE
     rather than recorded-diverge. Weighed and rejected: modelling a caching hart so
     staleness becomes executable — it contradicts the `present false` census to
     demonstrate a machine this unit is not; the acceptance's "when stale state MAY
     persist" half is a LATITUDE, pinned by declaration with the intro.html sentence,
     not by a fixture.
  3. **The acceptance pair**: WITH synchronization — a new rewrite-code guest
     carrying fence.i between the store and the fetch (the architectural
     synchronization executed and legal; the patched instruction observed through
     its effects, derivation EVD-05); WITHOUT — the existing fault-selfmod stays,
     its derivation naming D-CODE-VISIBILITY (immediate visibility is the
     laboratory's declared choice, a legal subset of the spec's may-or-may-not).
     dir-selfmod-fence is measured at execution: if its comments read the data fence
     as the synchronization, they are corrected to the spec's contract (fence ≠
     fence.i) in the same commit — no stale comments.
  4. **it-fencei/min-fencei re-derive to the legal fence.i** (their comments
     pre-commit it): the word retires as a nop; this unit records NO DIFF
     counterpart (both sides execute it legally — `references.sexp` stays
     difference-free, measured).
  5. **The reserved-fields cell**: a `.word` probe with nonzero funct12/rs1/rd
     executes (the shall-ignore rule); the assembler accepts the zero-operand
     `fence.i` spelling (standard software zeroes).
  6. **The census re-answer**: the fetch-cache candidate's why drops the rv64i
     "without Zifencei" clause — Zifencei is declared and now bound; the re-read
     choice stays laboratory policy, and FENCE.I's nop is the unit's sanctioned
     implementation of the synchronization (the `.4` reservation-candidate
     precedent: re-answered in place, the consequence line unchanged).
  7. **Execution slicing** (checkpoints inside the leaf, each committed with the
     leaf id): (a) the re-pin + the fragment + `zifencei.sem.sexp` + the assembler
     acceptance (the slot stays declared); (b) THE BIND: slot→extension, 87→88,
     the re-derived fencei guests, the reserved-fields probe, the acceptance pair,
     the matrix cells, the identity proof for the 97 untouched guests; (c) the
     Sail matched experiment + the census re-answer + the reports and the book +
     the leaf acceptance.
  **Not `.6`'s scope:** a caching-hart model (decision 2, rejected); the rv64gc C13
  disposition (registration day — no rv64gc section exists in `category-needs.sexp`);
  fence.tso/pause pseudo spellings (D-FENCE's numeric-spelling precedent stands);
  RVWMO's fetch formalization (the spec itself defers it); Zicbom/Zicboz cache-block
  operations (unselected, named); the m/f/d/c slots (their leaves); the hypervisor
  (D-NO-H); registration; the gate.

- `2026-10-05` (design brief for `.5`, recorded before its execution; sources: the pinned
  chapters re-read (`.materials/riscv/pinned-v20260120/priv/machine.html` §2.1.1.6.1,
  §2.1.1.8–§2.1.1.12, §2.1.2.1, §2.1.3.3; `priv/supervisor.html` §11.1.1.3, §11.1.1.12;
  `priv/sstc.html` 12.1; `unpriv/counters.html` §6.1 — versions 1.13/1.13/1.0/2.0 measured
  from the page titles); the unit measured in tree (`state.sexp:274-316` mip, `:583-588`
  stimecmp, `:590-600` the counter views; `privilege.rs:202-206` the live STIP overlay,
  `:423-435` the synchronous-only delivery; `exec_rv64gc.rs:88-191` the hookless step;
  `run_rv64gc.rs:77-131` the count-driven runner; `system.sem.sexp:7-12,51-57` the stated
  WFI nop; `env.rs:7-8,178-179` the CPU-driven boundary); Sail 0.14's interrupt/wait
  machinery measured in `target/refs/sail-riscv-src/model/` (`sys_control.sail:117-178`,
  `interrupt_regs.sail:241-262`, `step.sail:11,49-77,310-326`, `validate_config.sail:
  876-879`); two explore-agent censuses (the C14/C17 scope; the machinery deltas) — the
  reports are conversation-only, every load-bearing fact below re-measured by the
  signing engineer):
  **The measured pre-conditions.** (1) **The seam is marked in the state document, and
  one computed bit is already live**: mip's MSIP/MTIP/MEIP are `(read-only 0)` by
  legalization ("Pending-state behaviour is P4-SYSTEM.5's", `state.sexp:316`); STIP is
  `(computed)` — `time >= stimecmp` evaluated live on every mip/sip access
  (`privilege.rs:202-206`). **The reset quirk, measured**: time and stimecmp both reset
  0 (laboratory, RVP-MACHINE §2.1.4 UNSPECIFIED cited), so the honest computation reads
  **STIP=1 at reset** — legal (§11.1.1.3; mip's "Nothing pending at reset" speaks of
  STORAGE — STIP is computed, not stored), unobserved today (census: `grep 'mip\|sip'
  guests/mm-*.expected.sexp` → 0), and the corpus must face it. (2) **No pending evaluation exists anywhere** — census:
  `grep -n 'mip\|mie\|mideleg' crates/semulith-core/src/exec_rv64gc.rs` → 0 matches;
  `trap_deliver` is synchronous-only by name (`privilege.rs:423-429`: "interrupt-caused
  delivery is P4-SYSTEM.5's … the vectored mode is the interrupt case's"); delegation
  reads only medeleg. (3) **The step model has no hook,
  no halt, and the vocabulary cannot say "nothing retired"** — `step_over`
  (`exec_rv64gc.rs:88-191`) runs fetch→decode→eval→pc+=4 with no pre-instruction
  check; no halted bit exists; the runner loops exactly `executed_steps` with
  `steps.len` asserted (`run_rv64gc.rs:77-131`, `tests.rs:17-21`); the expectations
  schema is strictly per-step — "N ticks passed, nothing retired" is inexpressible
  (measured, both files). The `.3` `<fetch page fault>` pseudo-step is the
  vocabulary-extension precedent. (4) **WFI is a stated nop when legal**
  (`system.sem.sexp:51-57` + header `:7-12` — "the wake event is P4-SYSTEM.5's"); the
  legality latitudes are resolved FOR immediate trapping (illegal in U with S
  present; illegal in S with TW=1 — §2.1.3.3/§2.1.1.6.6's "may always raise"
  resolved deterministically); the `.2` Sail experiment named mm-wfi's TW cell a
  Sail-side gap (Sail judges TW only on forced wait exit, `step.sail:65-75`) and
  routed it here. (5) **The boundary is CPU-driven only** — `env.rs:178-179`:
  "Implementors answer every request; they never initiate one — the CPU drives";
  `:7-8`: "No device, no time source, no asynchronous event exists to model";
  FlatMemory's one region makes a CLINT mtime load fault by contract
  (guest-no-device, D-PLATFORM); `ScriptedEnv` answers FIXED values only — no
  progress, no asynchrony (measured, `fixtures.rs:192-226`).
  (6) **The spec's acceptance machinery is exact** (the machine/supervisor re-read,
  every phrase located): the taken rule — for M: (a) mode M with MIE set OR any lower
  mode, (b) the bit set in mip AND mie, (c) the bit NOT in mideleg (§2.1.1.9); the
  S-form (supervisor §11.1.1.3); the global rule — higher-privilege interrupts always
  enabled, lower always disabled (§2.1.1.6.1); delegation masks at the delegator
  (§2.1.1.8); fixed priorities (M: MEI MSI MTI SEI SSI STI; S: SEI SSI STI);
  evaluation bounded and immediate after xRET or a dependent-CSR write (§2.1.1.9);
  per-bit mip writability (MTIP read-only, cleared via mtimecmp; SSIP
  writable; SEIP's B∥E; STIP read-only under Sstc, set when time ≥ stimecmp, cleared
  by writing stimecmp above time — §11.1.1.3/§11.1.1.12). WFI's resume rule: MUST
  resume on a locally-enabled pending interrupt "regardless of the global interrupt
  enable at each privilege level" and of mideleg, even globally disabled; resumption
  "for any reason" permitted (the nop latitude); the taken trap resumes "on the
  following instruction … mepc = pc + 4" (§2.1.3.3). (7) **Rates are environment property everywhere** — Zicntr §6.1 ("The
  execution environment should provide a means to determine the current rate"); mtime
  §2.1.2.1 ("must increment at constant frequency"); STIP/MTIP reflection
  "eventually, but not necessarily immediately" — the fairness assumption
  `CPU_ENVIRONMENT.md` §3 demands be named, never a test timeout. mm-counters stayed
  NOT MATCHABLE at `.2` because Sail refuses Zicntr without a CLINT time source
  (`validate_config.sail:876-879`) and D-PLATFORM declares no devices. (8)
  **Determinism is the design's spine** — every modelled state so far is a pure
  function of the hart's own history (the TLB/reservation census discipline,
  `state.sexp:656-657`); `every_guest_re_executes_identically_from_cold_reset`
  (`run_rv64gc/tests.rs:96-109`) and EVD-05's exact values both break if time and
  event injection are not a replayable, DECLARED schedule. Sail's own time ticks
  only per-instruction (`step.sail:319-326`) and its loop never dwells in WFI
  (`exit_wait=true`, `:310`) — time-without-retirement is unmatched-by-construction
  on the reference side, recorded now. (9) **C14/C17 and the contract rows name the split** — no rv64gc
  section exists in `category-needs.sexp` (the unit is deliberately unregistered);
  `CPU_ENVIRONMENT.md` §2's Interrupts / Counter input / Waiting rows assign the CPU
  the mask/priority/acceptance/return, access/width/state, and suspend/continue
  rules, and the environment the source state, the declared virtual-time progress,
  and event progress while the CPU waits ("Timer/interrupt wake without CPU
  retirement" — the acceptance's exact words); §6: "Time-based devices need progress
  when no instruction retires." The `.2` brief's drawn-out list routes in:
  interrupt-CAUSED entry, counter values/rate/wrap/progress (with `.9`), WFI's wake,
  the mcountinhibit contract decision, mtime/mtimecmp as environment state
  (with `.9`).
  **The design, decided** (the execution measures and fixes at root, the `.1`/`.2`
  discipline):
  1. **A declared virtual-time domain, uniform and replayable** — the acceptance's
     enabling choice. The laboratory's time advances **one tick per step boundary,
     retired or halted** (authority laboratory — the Zicntr latitude "the rate … will
     depend on the implementation and operating environment", §6.1; pre-condition 7's
     fairness assumption answered: progress is a pure function of the step index,
     declared as data, never a timeout). `time` reads the domain directly (the state
     document's "environment's mtime" phrasing is refined, not contradicted: the
     domain IS the environment's supply; the contract wording is `.9`'s). `mcycle`
     reads the same domain ("cycle count might represent a valid implementation of
     RDTIME", §6.1). `minstret` counts GENUINELY: +1 per retired instruction, never
     for a halted or a faulting step (the `.8`-candidate unit discipline).
     Determinism holds by construction (pre-condition 8).
  2. **The counter-reading corpus re-derives BY DESIGN** — measured: `mm-counters.s`
     is the ONLY guest reading counters (7 reads; census `grep -c 'rdcycle\|rdtime\|
     rdinstret' guests/*.s | grep -v ':0'` → 1 file); its zero-expecting cells
     re-derive to the declared tick values (the `.2` IALIGN-16 precedent — re-derived,
     never fitted); mm-stimecmp measured clean of counter reads.
  3. **Pending evaluation and interrupt-caused delivery, at the spec's own evaluation
     points** — the engine gains the (a)(b)(c) computation with the global rule, the
     delegation mask, and the fixed priorities, evaluated at the HEAD of every step
     (the Sail `dispatchInterrupt`-at-head precedent, `sys_control.sail:117-141`
     measured): per-step evaluation satisfies "bounded amount of time" and covers the
     xRET/CSR-write immediacy by construction. Delivery: mcause's Interrupt bit set
     (bit 63 — the field already declared), mepc ← the next instruction's pc
     (interrupts are taken BETWEEN instructions), the xPIE/xIE/xPP stack, pc ← the
     vector — **both mtvec/stvec modes delivered as declared** (synchronous keeps
     BASE; interrupt delivery honors MODE — the storage already admits it, and
     delivering MODE=1 as BASE would be a description lie). mideleg is read for the
     first time, with the delegator-masking rule.
  4. **The halted state and WFI's real wake** — the nop latitude recorded-not-taken
     (the `.3` over-fence precedent: taking it would leave the leaf's acceptance
     untestable). A hart-state bit (ACTIVE/WAITING — Sail's `HART_WAITING` precedent,
     `step.sail:11`), cold-ACTIVE at reset, a pure function of hart history under the
     declared time domain; it joins the SEM-08 census (the named `.5` reopen,
     `state.sexp:658`) with the TLB/reservation discipline. While WAITING a step
     retires nothing, issues no fetch, advances time one tick, and evaluates the
     wake: resume on a LOCALLY-enabled pending interrupt at ANY privilege regardless
     of global enables and mideleg (§2.1.3.3's must); on resume the trap is taken if
     the taken-conditions hold (mepc = pc + 4 — the WFI-specific rule), else
     execution continues at pc + 4 and software may loop. The `.2` TW resolutions
     stand; mm-wfi's TW cell re-tests against Sail's named gap unchanged.
  5. **The source set is exactly what the platform can supply** — STIP (the live
     stimecmp-vs-time computation, Sstc), SSIP and SEIP's software-writable B parts
     (already storage). **MTIP/MSIP/MEIP STAY read-only 0 BY DECLARATION**:
     mtime/mtimecmp are memory-mapped ENVIRONMENT registers (§2.1.2.1) in a platform
     that declares no I/O region (D-PLATFORM; guest-no-device proves the fault
     today), MSIP is read-only-0-legal at one hart (§2.1.1.9's own latitude), and no
     external controller exists — the M-level machinery is fully testable through
     the software-writable bits (mideleg clear → SSIP/SEIP trap to M). The mtime/
     MMIO contract and any source-delivery vocabulary are `.9`'s charter — the `.4`
     external-invalidation routing precedent; nothing is smuggled. The timer wake
     the acceptance names rides the Sstc path, which needs no MMIO.
  6. **The expectations vocabulary gains the halted step, minimally** — a `<halted>`
     pseudo-step (the `.3` `<fetch page fault>` precedent): declared
     `(insn "<halted>")`, empty `(writes)`, `fetches 0` (the `.3` declarational fetch
     witness gains the 0 arm); the wake step itself is ordinary — the taken trap is
     observed through handler control flow and csrr reads (the `.2` mode-matrix
     discipline), an untrapped resume through the pc+4 continuation. The runner's
     count-driven termination is unchanged — halted steps count as steps; the
     fetch-count and steps.len assertions gain exactly the halted-step arm, recorded
     as the harness convention.
  7. **mcountinhibit stays excluded, now as the measured equivalence** — §2.1.1.12:
     "If the mcountinhibit register is not implemented, the implementation behaves
     as though the register were set to zero" — counters always count, exactly what
     decision 1 models; the contract decision the `.2` brief deferred is ANSWERED
     here by that citation (the committed 33 stands).
  8. **The corpus families** (names at execution): acceptance cells (eligible/
     ineligible boundaries per mode, the global rule, per-cause enables, pending/
     clear through the software-writable bits, delegation masking, the fixed
     priorities among simultaneous pending); the timer guests (STIP set/clear
     through stimecmp writes, the landed STCE/TM gates re-exercised against live
     STIP); the wake guests (halt with time observed passing through the handler's
     rdtime, wake-with-trap (mepc=pc+4) and wake-without-trap (pc+4 continuation),
     the locally-enabled-regardless-of-delegation cell); nesting and return (an
     interrupt inside a handler, the xRET stack restoration); counters (the
     declared rate observed, instret's genuine count incl. zero across halted
     steps, the mode-gating matrix on live values). Matrix: the seven existing
     axes (the progress axis's own wording already names wfi) — no new axis.
  9. **The Sail matched experiment, scoped to what is matchable** — EVD-05 stays
     primary. MATCHABLE: the acceptance/delegation/priority cells driven by the
     software-writable pending bits (no external source needed on either side —
     SSIP/SEIP via csrrs), the override measured first (the `.4` validate-config
     discipline). NOT MATCHABLE, recorded: time-without-retirement (pre-condition
     8), the counter rate (the `.2` CLINT wall stands — enabling Sail's CLINT/SIG
     to force a match was weighed and rejected at `.2`), the TW cell (the named
     gap). Any override change re-proves verdict-neutrality on the existing corpus
     (the `.3`/`.4` pattern).
  10. **No new instructions, no bind** — `.5` is machinery, not forms (the `.3`
      precedent): the scope census (87), the encoding composition and the assembler
      are untouched; slices land tracked and green incrementally. The corpus
      consequences (decision 2's re-derivation; mm-wfi's legal-WFI cells facing the
      real halt) land with the slices that cause them, each with its per-guest
      identity measurement (the `.3` discipline).
  11. **Execution slicing** (checkpoints inside the leaf, each committed with the
      leaf id): (a) the virtual-time domain + counter progress (the rate as data,
      instret genuine, cycle=time) + mm-counters' by-design re-derivation + the
      determinism proof; (b) pending evaluation + interrupt-caused delivery (both
      vector modes) + the acceptance corpus; (c) the halted state + WFI's wake +
      the `<halted>` vocabulary + the wake corpus + mm-wfi's re-derivation + the
      census reopen; (d) the matrix cells + the Sail attempt + the reports and the
      book + the leaf acceptance.
  **Not `.5`'s scope:** mtime/mtimecmp's MMIO and the MTIP/MSIP/MEIP sources (`.9`'s
  contract; the board's CLINT is the P5 layer); mcountinhibit the REGISTER (excluded —
  decision 7's equivalence); HPM/Zihpm (unselected); the hypervisor timer (D-NO-H);
  fault priority as a topic (`.8`); multicore time synchronization (MC-MULTICORE —
  vacuous at harts=1); the counter-rate and event-delivery CONTRACT wording (`.9` —
  the laboratory's domain is data here, the TLB-parameter precedent); the rv64gc
  C14/C17 dispositions (registration day); registration; the gate.

<!-- archived verbatim from docs/tasks/P4-SYSTEM.md at the 2026-10-06 `.10` design (`.8` and `.9` closed) -->

- `2026-10-06` (design brief for `.8`, recorded before its execution, `SEMULITH-P4-0057`;
  sources: a read-only census of the engine's multi-suboperation paths (an explore agent's
  report — conversation-only; every load-bearing fact below re-measured where it lives);
  `RULES.md:27,29` (SEM-04, SEM-06); `docs/ARCHITECTURE.md:186`;
  `docs/CPU_ENVIRONMENT.md:24`; `docs/INFORMATION_CATALOG.md:19,27` (C08, C11); the pinned
  `priv/machine.html` synchronous-exception priority table and `unpriv/intro.html`'s trap
  section; a scratch probe on both engines (`target/p4-system-8/probe/`)):
  **The measured pre-conditions.** (1) **The rules**: SEM-04 — "Exposed sequencing, operand
  visibility, partial progress, and restart state follow the target definition rather than
  universal instruction atomicity"; SEM-06 — "Side-effecting accesses occur only at their
  prescribed semantic point and are not rolled back by assumption". Preciseness is the EEI's
  to declare ("The EEI defines for each trap whether it is handled precisely, though the
  recommendation is to maintain preciseness where possible", intro.html), and this
  laboratory declared it: rv64i's `OB-ENV-PARTIAL-PROGRESS` ("completes or faults as a
  unit … the architectural state exactly as it was before the faulting instruction, except
  for the fault report itself"), `.4` decision 5, `schema/semantics.sexp:200-201`. rv64gc
  carries NO partial-progress obligation (44 obligations, none of them), and
  `state.sexp:661-662`'s candidate "pending or partially committed effects" is `present
  false` with "P4-SYSTEM.8 … reopens this candidate". (2) **The engine has no staging**:
  `Frame` snapshots only reads (`pre_regs`/`pre_fregs`); every write goes straight to state;
  the one guard is `trapped`, checked at `run`'s head and inside `Set` after the value is
  evaluated — so the unit discipline holds only where every fault point precedes every
  commit in tree order. (3) **A defect, measured on both engines**: a CSR instruction with
  rd≠x0 whose WRITE is refused commits rd before it traps — the zicsr rules read
  `(seq (set (reg rd) (csr-read …)) (csr-write …))` and `csr_write`'s permission check runs
  second. Probe `csrrw x5, cycle, x6` in M with x5 = 7: semulith `x5 <- 5` THEN cause 2;
  sail 0.14 (matched config) cause 2 and NO x5 write. Reachable on every read-only CSR the
  profile carries (mhartid, cycle, time, instret) by csrrw/csrrwi always, csrrs/csrrc with
  rs1≠x0, csrrsi/csrrci with uimm≠0; no guest exercises it (mm-readonly writes with rd=x0).
  ⚠ **Corrected at (a)**: the sail half of this probe is confounded — the matched override
  runs Zicntr OFF (the recorded CLINT wall), so sail traps on `cycle` because the CSR is
  absent, not because it is read-only. Re-measured on `mhartid` (implemented on both
  engines): sail traps with no rd write — the clean evidence (`mm-csr-ro-write`, AGREE).
  Two smaller ones ride along: LR's boundary-Misaligned arm delivers 7 where the leaf's rule
  is 5 (unreachable — misalignment is judged first — but wrong), and `a-lrsc-fault.s:18`'s
  comment says the LR raises 7 while its expectations and the engine say 5. (4) **The
  crossings that stand** (SEM-06's "not rolled back"): a load/store's TLB fill before a
  boundary fault, the earlier levels' walk reads before a later level faults, a straddling
  fetch's first parcel before the second faults, and an AMO's load before its store faults
  — all IMPLICIT or completed reads, none an architectural write; today none is
  reachable as a split by the corpus, because `FlatMemory` refuses only by region and
  alignment and an AMO's two halves share address and width. (5) **No fault injection
  exists for rv64gc**: `ScriptedEnv` (semulith-verify) is wired to no rv64gc run;
  the translation tests' `WalkEnv.walk_fault` is declared and never set. (6) **Fault priority** is the pinned
  table (`priv/machine.html`, "Synchronous exception priority in decreasing priority
  order"): instruction-translation faults, instruction access fault, then illegal /
  instruction-misaligned / ecall / ebreak, then (OPTIONALLY) load/store/AMO misaligned,
  then the explicit access's translation faults, its access fault, and misaligned "if not
  higher priority" — "implementation-defined" between misaligned and page faults. The
  laboratory took misaligned-first at `.3` decision 7 and handed "the full priority TOPIC"
  here (four deferrals in the archived briefs). The corpus already pins several pairs
  (it-prio-load, it-prio-jump, the FS-Off FLW, a-amo-sv39's misaligned-before-translation).
  **The design, decided:**
  1. **The unit discipline is declared for rv64gc** (the leaf's subject): every instruction
     completes or faults as a unit — a delivered synchronous exception leaves architectural
     state as before the instruction except the trap report — and the STANDING crossings of
     pre-condition 4 are declared, not hidden (SEM-06): implicit and completed reads that
     reached the environment before the fault are not rolled back. It lands as rv64gc's
     partial-progress obligation (the rv64i obligation adapted, with its POS/NEG checks
     pointing at real guests this time) and as the state candidate's re-answer.
  2. **The CSR defect is fixed at root in the semantics**, so the write's permission is
     judged before any commit (sail's check-before-execute shape); the exact language form is
     execution's to measure (the sem-corpus gate judges it). RED first: the probe becomes a
     guest that diverges on the parent engine; sail AGREE after.
  3. **The priority table is declared** as a profile decision quoting the pinned table and
     naming the laboratory's one optional choice (misaligned first); every adjacent pair the
     profile can produce gets a guest unless one already pins it (the census says which).
  4. **Fault injection is TYPED and environment-shaped**, never a mid-instruction hook: the
     corpus environment learns declared regions with per-kind refusal (readable but not
     writable; not walkable; not fetchable), declared in the guest's expectations and
     honoured by the runner and the authoring tool alike — so "a fault injected after the Nth
     suboperation" is an AMO whose store half is refused after its load completed, a walk
     refused at level N, a straddling fetch refused at its second parcel, an SC/FSD refused
     at its store. The injection carrier gets its own RED/GREEN controls.
  5. **Observation stays through x-registers** (the `.2` discipline): suppressed writes as
     the absence of a change, memory as read-back through an allowed load; a crossing that
     no register can show is stated in the derivation, never claimed observed.
  6. **Execution slicing** (checkpoints, each committed with the leaf id): (a) the CSR defect
     + the two small ones, RED-first, sail-matched; (b) the priority table declared + its
     missing pairs; (c) the typed injection carrier (schema, runner, authoring tool, its
     controls); (d) the injected-fault corpus + the obligation + the candidate re-answer;
     (e) the sail matched attempt over the non-injected guests (sail's config cannot carry
     the laboratory's refusal regions — measured at execution), the reports, the book, the
     leaf acceptance.
  **Not `.8`'s scope:** imprecise or deferred traps (none declared); breakpoints/triggers
  (no Sdtrig); multi-hart partial visibility (`MC-MULTICORE`); the environment contract's
  v1 versioning (`.9` — `.8` adds the one obligation its subject needs, under the existing
  version's discipline); the vector extension's lane faults (C08 — V unselected); the gate.

- `2026-10-06` (design brief for `.9`, recorded before its execution, `SEMULITH-P4-0063`;
  sources: a read-only census of the contract representation, the rv64gc obligations and every
  deferral routed to `.9` (an explore agent's report — conversation-only; the load-bearing
  facts re-measured where they live); `schema/contract-obligations.sexp`;
  `docs/CPU_ENVIRONMENT.md` §2–§4; `RULES.md` ENV-01; `scripts/gate_report.py`;
  `crates/semulith-core/src/env.rs`):
  **The measured pre-conditions.** (1) **A contract has no version mechanism**: no
  contract-level construct exists — `contract_id`/`contract_version` repeat on every
  obligation, nothing checks either, and the contract-level text is prose (rv64i's
  `ENVIRONMENT.md`; rv64gc has none). "Versioned, not edited in place" is acceptance text
  only (`MC-MULTICORE.md:39`, `DOSSIER.md:87-88`); the one precedent is the requirement rule
  "AMENDED by a new versioned record … the old record superseded, never edited". Every
  rv64gc obligation is `"0"` (`grep -n contract_version … | grep -vc '"0"'` → 0), and leaves
  `.2`–`.8` added records under it. MIRROR-DERIVE requires the 13 base mirrors to keep rv64i's
  fields. (2) **rv64gc states no environment assumption at all**: 46 obligations, every one a
  `cpu-guarantee`. The four topics the leaf names are routed here by name a dozen times —
  "translation inputs" (`env.rs:96-98`, `translation.rs:42-44`, `.3` decision 6), the
  reservation's external-invalidation vocabulary and the eventuality/fairness wording
  (`reservation.rs:26-28`, `.4`), the time supply (`timekeeping.rs:8-9`, `state.sexp:604`),
  the interrupt sources and mtime/MMIO (`state.sexp:652`, `.5` decision 5) — and
  `docs/CPU_ENVIRONMENT.md` §2 has a row for each (Translation, Interrupts, Counter input,
  Reservations) that rv64i dispositioned "out of scope". (3) **Stale v0 statements**,
  measured: `OB-GC-PRIV-INSNS` says wfi "executes as a no-op when legal" (WFI ENTERS a wait
  since `.5` — `wait.rs`) and sfence.vma is "a stated no-op … no translation caches are
  modelled" (a TLB since `.3`); `OB-ZICNTR`/`OB-GC-COUNTERS` defer rate and progress to
  "P4-SYSTEM.5 and P4-SYSTEM.9"; `env.rs`'s module doc says "No device, no time source, no
  asynchronous event". (4) **No profile check is implemented**: RECORD-SCHEMA demands a
  `-POS` and a `-NEG` id per obligation (rule 6) but nothing names a fixture; the gate
  report counts a check implemented only when its id appears under `scripts/`/`crates/`
  (`gate_report.py:63-77`) — rv64i reads 0 of 72, rv64gc has no report path. (5) **The
  boundary in code** has four request kinds and no time/interrupt/invalidation variant; time
  is the hart's own virtual domain (`timekeeping::advance`), STIP is computed in the hart
  (`time >= stimecmp`), MTIP/MSIP/MEIP are read-only 0 by declaration, and the reservation has
  no external entry point beyond `clear`.
  **The design, decided:**
  1. **A contract becomes a versioned document**: a `contract` construct (id, version, the
     version it extends, its member obligations, the members it supersedes) — v0 recorded as
     it stands (46 members), v1 extending it. **"Not edited in place" is mechanized**: v0's
     members are frozen by a content manifest (the SHARD-FREEZE pattern) and a gate refuses
     any change to a frozen version's records; a v0 statement that later work made wrong is
     SUPERSEDED by a v1 record with a new id, never rewritten.
  2. **v1 states the four environment assumptions** (the first rv64gc has): translation
     inputs (page tables are main memory, read through the walk's own request kind,
     coherent with the hart's stores, never written — Svade; a refused walk read is the
     original access's access fault); interrupt sources (v1's environment supplies NONE —
     the M-level sources read-only 0, STIP the hart's own comparison, SSIP software's; a
     platform's CLINT is a later version, P5's); counter progress (the time supply IS the
     virtual-time domain — one tick per step boundary, retired or halted — the wake reaching
     a halted hart without retirement); reservation invalidation (one hart: no external
     invalidation event exists in v1, the reservation's lifetime is the hart's own rules,
     and the "eventually" requirement holds trivially — a constrained LR/SC loop succeeds on
     its first iteration). Each states what would make it false.
  3. **Every new v1 assumption has a POSITIVE and a NEGATIVE fixture that exist and run**: a
     tracked check registry maps each v1 CHK id to corpus guests, and a test executes them —
     the gate report's own "implemented" measure then counts them honestly (an id named in
     `crates/`). Missing fixtures are written, not waived.
  4. **The stale v0 statements are superseded in v1** (`OB-GC-PRIV-INSNS`'s wfi/sfence
     clauses, the counters' "deferred to .9" clauses); stale code prose (`env.rs`'s module
     doc) is corrected in place — code comments are not contract records.
  5. **Execution slicing**: (a) the contract construct + v0 recorded + the freeze manifest and
     its gate (RED: an edited frozen record refused); (b) v1's four assumptions + the check
     registry + any missing fixture; (c) the supersessions + the stale prose; (d) the
     reports (rv64gc's ENVIRONMENT document, the book), the leaf acceptance.
  **Not `.9`'s scope:** the CLINT/PLIC as interrupt sources (a later contract version,
  P5-BOARD's platform); multi-hart reservation invalidation (`MC-MULTICORE` — "a new
  contract version"); the gate report itself (`.10`); rv64i's contract (frozen at its own v0).

