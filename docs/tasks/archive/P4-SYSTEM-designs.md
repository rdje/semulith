# P4-SYSTEM — archived completed-leaf designs

The recorded-before-execution design briefs of the completed leaves of the
[`P4-SYSTEM`](../P4-SYSTEM.md) tree — `.2` (privilege and mode transitions) and `.1`
(the profile resolution) — split from the live file on `2026-10-04` at its sixth
per-part ceiling crossing (the ceiling was obeyed, not raised — the
`P2-SCALAR-designs` precedent). The checklists live in `P4-SYSTEM.md` beside this
file. Archived design sections, verbatim:

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

