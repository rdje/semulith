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

