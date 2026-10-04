# P4-SYSTEM — archived completed-leaf evidence (part 1)

The full, unedited acceptance checklists for the completed work of the
[`P4-SYSTEM`](../P4-SYSTEM.md) tree (leaf `.1` and leaf `.2`'s slices (a)–(g)), split
out on `2026-10-03` when the live file crossed its per-part ceiling (144,086 B >
131,072) — the ceiling was obeyed, not raised, per the `docs/tasks/` precedent set by
`SOT-FORMAT`, `P1-LAB`, `P2-SCALAR` and `P3-BREADTH`. The live tree keeps the
frontier, the decisions, the open questions, the blockers, every leaf's
goal/acceptance/result narrative, the ACTIVE slice's checklist (`.2` slice (h)),
and both logs.

Archived sections, verbatim:

`P4-SYSTEM.1` (`2026-10-03`, `SEMULITH-P4-0002`):

- [x] **REPRODUCE / ISSUE** — the roadmap's "provisionally RV64GC" had no resolved,
  source-located selection: no unit, no pins for the privileged chapters in any unit
  ledger, and a recorded uncertainty about whether the pinned snapshot even carries
  them. Measured pre-conditions:

  ```
  $ ls profiles/rv64gc-lab-v0
  ls: …: No such file or directory          # no unit at all
  $ ls .materials/riscv/pinned-v20260120/
  SHA256SUMS  biblio  index.html  priv  unpriv   # priv/ EXISTS — 24 pages
  $ ls .materials/riscv/pinned-v20260120/priv/ | wc -l && ls …/unpriv/ | wc -l
  24 / 46                                     # the catalog's "46+24" claim confirmed;
  #  the 2026-09-27 category census's "privileged volume absent" phrasing measured false
  $ ls .materials/riscv/*.pdf
  riscv-sbi-2.0.pdf  riscv-elf-psabi-1.0.pdf  riscv-brs-1.0.pdf …   # the "wanted"
  #  contracts already cached; digests re-verified against the catalog pins (3/3)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — WHY the leaf is more than a document: the
  selection's elements lived as prose in ROADMAP.md and a frozen contract
  (`docs/ARCHOGEN_INTEGRATION.md`), the pinned corpus's privileged coverage was
  misrecorded, and the dossier machinery had no lifecycle stage for "resolved but no
  definition pipeline" (EXTRACTION refuses a bare processor unit by design). WHERE: the
  new unit `profiles/rv64gc-lab-v0/` (5 files); `schema/profile.sexp` (the
  `profile-resolution` route + optional `comparison`); `scripts/check_extraction.py` +
  `.sh`, `scripts/check_exercise_coverage.sh`, `scripts/check_interaction_matrix.py` +
  `.sh` (the route honored by declaration, contradiction = RED);
  `scripts/check_citations.py` (subdirectory `file` fields + named non-snapshot skips);
  `scripts/gen_platform.py` (canonical ISA-string order); `doctrine/fact_ownership.tsv`
  + `scripts/check_fact_ownership.sh` (the re-pin to six units).
- [x] **FIX** — the resolution as data (the Result above): 24 pinned sources, 18
  decisions, 18 verbatim requirement mirrors + 18 contract obligations (contract
  `rv64gc-lab-env-v0` v0, POS+NEG check pairs declared), the closure measured (G =
  IMAFDZicsr_Zifencei; D⇒F; F⇒Zicsr; C⇒Zca+Zcd at RV64), the DOSSIER narrative with the
  locator table and the rejected rv64imac alternative.
- [x] **ADDRESSED (verified)** — the acceptance: nothing inferred from "GC", every
  element located:

  ```
  # every chapter version measured from the pinned pages' own titles:
  #   M 2.0, A 2.1, F 2.2, D 2.2, C 2.0, Zicsr 2.0, Zifencei 2.0, Zicntr/Zihpm 2.0,
  #   RVWMO 2.0, RV64I 2.1; Machine 1.13, Supervisor 1.13, Sstc 1.0
  # every snapshot pin re-hashed against the tracked SHA256SUMS: 21/21 match
  # the three PDF pins re-verified against materials/catalog.sexp: 3/3 match
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (18 record file(s) validate and agree with their profile; …)
  $ bash scripts/check_extraction.sh
  … profiles/rv64gc-lab-v0: profile-resolution route declared (52 scope forms; …)
  EXTRACTION: ok (5 unit(s) sufficient — P1-LAB may cite this)
  $ python3 scripts/check_citations.py rv64gc-lab-v0
  …  52 of 52 instruction citations resolve in the pinned artifact (…, 21 pinned source(s))
  #  (the shared rv64i semantics resolve against the new unit's pins, offline; the three
  #   declared non-snapshot pins skipped BY NAME)
  $ bash scripts/check_profile_consistency.sh
  PROFILE-CONSISTENCY: ok (5 profile dossier(s) internally consistent)
  $ bash scripts/check_exercise_coverage.sh
  EXERCISE-COVERAGE: ok (5 profile(s) …)
  #  (the wrapper prints the summary only; the declaration leg is proven by the new
  #   self-test arm: "GREEN profile-resolution route: composition and exercise n/a by
  #   declaration" — and the RED arms contradict it with an encoding.sexp / a guests/
  #   corpus, both named)
  $ bash scripts/check_interaction_matrix.sh
  INTERACTION-MATRIX: ok (5 unit(s) — …)
  $ bash scripts/check_fact_ownership.sh
  FACT-OWNERSHIP: ok (61 fact kind(s): one owner each, every mirror governed)
  ```

- [x] **NO REGRESSION** — the three route-aware gates' self-tests green with the new
  arms (EXTRACTION 11/11, EXERCISE-COVERAGE 21/21, INTERACTION-MATRIX 15/15 — every RED
  asserting its reason: a resolution declaration contradicted by an encoding.sexp or a
  guests/ corpus, a scope count lying about its own enumeration); rv64i-lab-v0's
  citation run unchanged (52/52); the netboard manifest regenerated byte-identical but
  for the embedded generator hash after the ISA-order fix; `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS re-derived 376→383 arms in
  LIVE_STATUS.md; doctrines still 34). No Rust surface touched.
- [x] **LOCKSTEP** — tree (leaf + frontier + checklist + logs), `MEMORY.md`,
  `CHANGELOG.md`, `DEV_NOTES.md` (the lifecycle-stage gap lesson; promotion: declined (the by-declaration discipline has its decision records and the route's behavior is armed by self-test REDs in three gates)), `LIVE_STATUS.md` (the P4 row),
  `docs/TASK_TREE.md`, mdBook
  `plan/p4.md` (the `.1` section), the book index regenerated. TOOLBOX.md unchanged —
  no new diagnostic tool (the records probe is recorded below, one-off by design; the
  citation checker's edit is a fix to an existing row's tool).

`P4-SYSTEM.2` slice (a) — fragments + assembler whitelist + IALIGN data (`2026-10-03`, `SEMULITH-P4-0004`):

- [x] **REPRODUCE / ISSUE** — the brief's pre-conditions re-measured, then the upstream
  census the slice stands on (the brief delegated the table carving to execution):

  ```
  $ ls profiles/rv64gc-lab-v0/
  contract-obligations.sexp  DOSSIER.md  profile.sexp  requirements.sexp  sources.sexp
  #  no references.sexp — the new fragments' tables were pinned nowhere (a fragment
  #  generated from an unpinned source is a model built on something nobody can re-derive)
  $ grep -n '"csr"' target/refs/riscv-opcodes/arg_lut.csv; grep -c csr scripts/riscv_asm.py
  "csr", 31, 20          # the pinned arg_lut carries the field…
  0                      # …but the assembler's whitelists had no csr operand (pre-edit count)
  $ grep -n 'IALIGN=32 for this profile' scripts/riscv_asm.py
  486:        raise AsmError(f"entry {entry:#x} is not 4-byte aligned; IALIGN=32 for this profile")
  #  a hard-coded 32 while rv64gc-lab-v0 declares (ialign 16) — D-IALIGN-16
  # THE CENSUS (master fetched via the same raw.githubusercontent route fetch_references.sh uses):
  $ for m in csrrw csrrs csrrc csrrwi csrrsi csrrci mret sret wfi sfence.vma \
             rdcycle rdtime rdinstret; do echo "== $m"; grep -rlE "^$m[[:space:]]" extensions/; done
  == csrrw … == csrrci   → extensions/rv_zicsr    (the 6 real rows; csrrwi/csrrsi/csrrci take zimm5)
  == mret, == wfi        → extensions/rv_system
  == sret, == sfence.vma → extensions/rv_s
  == rdcycle/rdtime/rdinstret → NO real row in any table
  $ cat extensions/rv_zicntr
  $pseudo_op rv_zicsr::csrrs  rdcycle    rd 19..15=0 31..20=0xC00 14..12=2 6..2=0x1C 1..0=3
  $pseudo_op rv_zicsr::csrrs  rdtime     rd … 31..20=0xC01 …
  $pseudo_op rv_zicsr::csrrs  rdinstret  rd … 31..20=0xC02 …   # exist ONLY as pseudo-ops of csrrs
  $ for f in rv_i rv64_i rv_m rv64_m; do shasum -a 256 target/refs/riscv-opcodes/$f master/extensions/$f; done
  IDENTICAL ×4           # upstream moved the tables root → extensions/ WITHOUT changing the bytes
  $ grep -E '"(csr|zimm5)"' target/refs/riscv-opcodes/arg_lut.csv
  "csr", 31, 20   /   "zimm5", 19, 15      # both fields already pinned — no arg_lut re-pin needed
  # the four privileged instructions' census reference (RVP-INSNS 18.1): the chapter's own
  # listing is an unpinned figure IMAGE (the encodings-as-images doctrine again); the four
  # are named in the pinned chapters — mret ×7 / wfi ×27 in priv/machine.html,
  # sret ×7 / sfence.vma ×4 in priv/supervisor.html (D-PRIV-INSNS cites exactly these)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in existing behavior; the slice runs the
  decided design, and execution measured four things the brief did not know (each fixed at
  root, none weakened a check):
  1. **Upstream restructured.** The tables moved from the repository root to `extensions/`,
     so the fetch route's `master/<file>` would 404 any FRESH fetch of the pinned tables
     (verify-only stayed green — the bytes are on disk). WHERE: the subpath case in
     `scripts/fetch_references.sh`; fixed by mapping `rv_*` under `extensions/` — honest
     for both profiles because the moved tables hash byte-identical to the pins (measured ×4).
  2. **Zicntr adds no encodings.** Its three counter reads exist upstream only as
     `$pseudo_op` rows of `csrrs`, and emitting them as `(insn …)` collides with csrrs in
     the disjointness gate by mask math (csrrs constrains only bits 14..12 and 6..0;
     rdcycle agrees on all of them). WHERE: `schema/fragment.sexp` gained the `(pseudo …)`
     construct (assembler spellings, never encodings), and `zicntr.sexp` declares
     `(requires "riscv/rv64i") (requires "riscv/zicsr")` — the pinned rows themselves name
     `rv_zicsr::csrrs` as the base, so the dependency is declared, not composed by luck.
  3. **Two latent resolver/gate defects, exposed by the first multi-extension composition.**
     `riscv_asm.resolve_composition` read only `ext[0][1:]` — every `(extensions …)` FORM
     after the first was silently dropped (the schema's `(repeat yes)` is one string per
     form; no tracked composition ever had two). And `check_encoding_disjoint.py` printed
     `DUPLICATE NAME(S)` and STILL returned 0 — an advisory where the verdict text claimed
     "no duplicate names". WHERE: `scripts/riscv_asm.py` (the resolver loop) and
     `scripts/check_encoding_disjoint.py` `main()`; both fixed, both armed by new self-test
     RED arms.
  4. **The assembler's label pass ate csr names** (`label 'cycle' is never defined` on
     `csrrw x1, cycle, x2` — names were label-resolved for EVERY operand position), and
     IALIGN was the hard-coded 32 at the line-486 check. WHERE: `riscv_asm.py` `assemble()`
     (labels now resolve only for B/J scrambled-offset operands; a csr name falls through
     to the operand parser, which resolves it through the pinned `csrs.csv`) and
     `write_elf64()` (ialign is now a required parameter; `Assembler` derives it from the
     sibling `profile.sexp`'s `(ialign …)` through the dossier mapping owner).

- [x] **FIX** — at the lowest-risk level that works, no Rust touched:
  `scripts/fetch_references.sh` (the `extensions/` subpath mapping);
  `profiles/rv64gc-lab-v0/references.sexp` (NEW — the encoding-source re-pin: rv_zicsr,
  rv_zicntr, rv_system, rv_s, csrs.csv + the shared arg_lut.csv, sha256+bytes each, plus
  the two candidates with re-derived binary digests; rv64i's ledger untouched);
  `schema/fragment.sexp` (+`(pseudo …)`, `requires` now `(repeat yes)`);
  `scripts/gen_fragments.py` (+3 fragments, per-table sha256 provenance, pseudo emission,
  multi-requires emission); `definitions/riscv/{zicsr,zicntr,system}.sexp` (NEW, generated);
  `scripts/riscv_asm.py` (csr/zimm5 whitelists — positions always from the pinned
  arg_lut.csv; the csr operand parser; pseudo flow through the canonical path; the
  resolver fixes; derived IALIGN); `scripts/check_encoding_disjoint.py` (pseudo support
  under the specialization rule, dupes a rejection; self-test 8→12 arms);
  `scripts/check_unit_composition.sh` (the new return shape + pseudo verdict; self-test
  8→9); `scripts/run_smoke.py`, `scripts/run_semulith_smoke.py` (pass `asm.ialign`).
  Routed INSIDE the tree (intra-tree, later slices): `crates/semulith-verify/src/elf.rs`'s
  IALIGN=32 entry check is the Rust twin of the retired Python assumption — slice (d) brings
  it in line when the engine learns IALIGN (slice (a) touches no Rust by boundary); csr
  NAME resolution reads the pinned-but-untracked csrs.csv — when slice (c)'s state.sexp
  owns the CSR addresses, resolution migrates to the tracked document; rdcycle's
  decode/coverage naming (a pseudo of csrrs) is slice (e)/(f)'s scope-census design input.

- [x] **ADDRESSED (verified)** —

  ```
  $ bash scripts/fetch_references.sh --verify-only rv64gc-lab-v0
  MATCH ×6 (the new tables + arg_lut) … MATCH encoding tables vs profile scope 52 == 52 … ok
  $ bash scripts/fetch_references.sh --verify-only rv64i-lab-v0
  … MATCH matched-profile ISA string rv64i_zvl32b … ok      # rv64i's verification stays green
  $ mv target/refs/riscv-opcodes/rv_s /tmp && bash scripts/fetch_references.sh rv64gc-lab-v0
  FETCH    riscv-opcodes/extensions/rv_s  →  MATCH … refetched bytes identical   # the new route, live
  $ python3 scripts/check_sexp_schema.py profiles/rv64gc-lab-v0/references.sexp schema/references.sexp
  check_sexp_schema: ok           # (the schema exists — no DOSSIER-SCHEMA skip-by-name)
  $ python3 scripts/check_sexp_schema.py definitions/riscv/{zicsr,zicntr,system}.sexp schema/fragment.sexp
  ok ×3 (and rv64i.sexp / m.sexp still conform)
  $ git diff --stat -- definitions/            # after regeneration
  (empty — rv64i.sexp and m.sexp re-derive BYTE-IDENTICAL)
  $ python3 scripts/check_encoding_disjoint.py definitions/riscv/rv64i.sexp definitions/riscv/<ext>.sexp
  base+m 65 / base+zicsr 58 / base+system 56 instructions — COMPOSE; base+zicsr+zicntr
  58 (+ 3 pseudo-instruction(s)) — COMPOSE; the 4-fragment trial union through a synthetic
  unit doc: 62 instruction(s) (+ 3 pseudo) — no collisions, no duplicate names — COMPOSE
  # the assembler probe (synthetic rv64gc-trial unit, untracked):
  rv64gc-trial ialign: 16     rv64i-lab-v0 ialign: 32
  0xc00110f3 csrrw x1, cycle, x2 … 0x30200073 mret … 0x12e68073 sfence.vma x13, x14
  $ target/refs/spike-build/spike-dasm < emitted-words      # the second-decoder round-trip
  csrrw ra, cycle, sp / csrrs gp, mstatus, tp / csrrc t0, mepc, t1 / csrrwi t2, mcause, 3
  csrrsi s0, sie, 17 / csrrci s1, mip, 31 / csrr a0, cycle / csrr a1, time / csrr a2, instret
  mret / sret / wfi / sfence.vma a3, a4         # all 13 forms exact (rdcycle prints as csrr —
                                                # the same encoding, spike's own pseudo preference)
  ```

- [x] **NO REGRESSION** — the changed logic fired RED first, then the guard set:
  `check_encoding_disjoint.py --self-test` 12/12 (the 3 new pseudo arms: unrealized →
  "extend the encoding space", partial overlap → "without specializing", and
  GREEN-specialization; the dupes arm → "DUPLICATE NAME(S)" rc=1);
  `check_unit_composition.sh --self-test` 9/9 (the new pseudo RED arm); the assembler's
  manual RED probes (recorded with commands above): `csrrw x1, 0x1000, x2` → "outside the
  unsigned 12-bit range"; `csrrw x1, notacsr, x2` → "not in the pinned csrs.csv";
  `csrrwi x1, cycle, 32` → "zimm5 value 32 does not fit in 5 bits"; entry 2 mod 4 →
  refused at IALIGN=32, accepted at IALIGN=16. Gates: UNIT-COMPOSITION / SEMANTICS /
  EXTRACTION / EXERCISE-COVERAGE (21/21) / INTERACTION-MATRIX / SOURCE-FORMAT /
  DOSSIER-SCHEMA (the new references.sexp validated, not skipped) / PROFILE-CONSISTENCY
  (the new dossier passes the candidate-shape arms) all green; GUEST-GEN / DEF-GEN /
  STATE-GEN byte-exact (no Rust surface touched); `make gate` → `=== all doctrines green ===`
  (DERIVED-COUNTS 383→384 arms re-derived in LIVE_STATUS.md). Census behind the
  "no other consumer" claim: `grep -n 'children(.*"insn"' scripts/*.py` →
  check_extraction.py:72 and check_semantics.py:223 only, both rv64i-scoped today, so the
  pseudo-bearing fragments have no unintended reader.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice b),
  `CHANGELOG.md`, `DEV_NOTES.md` (the execution findings; promotion: declined (the
  durability is the machinery — the resolver/gate fixes are armed by new self-test REDs,
  and the pseudo/ialign designs are data in the schema and the pins)),
  `LIVE_STATUS.md` (the re-derived arms count only — no row's state changed),
  `docs/book/src/plan/p4.md` (the `.2` slice note) + the regenerated book index.

`P4-SYSTEM.2` slice (b) — semantics-language operators + the new sem files (`2026-10-03`, `SEMULITH-P4-0005`):

- [x] **REPRODUCE / ISSUE** — the language could not say what the leaf must say, measured
  on the pre-slice tree:

  ```
  $ git show HEAD:schema/semantics.sexp | grep -c '^(operator'
  32                                   # no csr/mode/xret/trap-delivery form…
  $ git show HEAD:definitions/riscv/rv64i.sem.sexp | grep -A1 'insn ecall'
  (sem (insn ecall) … (effect (trap (lit 11) (lit 0))))
                                       # …only the harness-reporting (trap cause tval);
                                       # ECALL's cause was a CONSTANT 11 — a model with no
                                       # privilege modes cannot write 8/9/11 per mode
  $ python3 scripts/check_semantics.py definitions/riscv/zicntr.sexp <a sem naming rdcycle>
  zicntr.sem.sexp [rdcycle]: no instruction of that name in zicntr.sexp
                                       # a pseudo could not carry semantics at all
  $ git show HEAD:scripts/check_citations.py | grep -n 'rv64i.sem.sexp'
  178:        sem = REPO / "definitions" / "riscv" / "rv64i.sem.sexp"
                                       # the citation checker was single-file: locators in
                                       # any NEW sem file resolved against nothing
  # and the spec-side pre-condition: the mstatus field positions (TSR/TW/TVM/MPRV) exist in
  # the pinned chapters only as FIGURE images — `grep -c 'TSR' priv/machine.html` finds the
  # behaviour text, never a bit position (the encodings-as-images doctrine, one level down)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in existing behaviour; the slice runs the
  brief's decision 4, and execution measured five things:
  1. **The register-swap hazard.** csrrw/csrrs exchange a register with a CSR; a
     state-threaded `(reg rs1)` read after `(set (reg rd) …)` is wrong for rd==rs1, and no
     RV64I rule reads a register after writing it — so the language could adopt, without
     changing any existing meaning, the contract stated in `schema/semantics.sexp` (READS
     AND WRITES): register reads see the PRE-INSTRUCTION register file; memory and CSR
     reads see the state at their evaluation point; `(pc)`/`(inst)` are frame constants.
  2. **A pseudo's semantics specialize by NAME, not by refines.** Measured: the compose
     rule keys on names; rdcycle ≠ csrrs, so no `(refines …)` is possible or needed — the
     pseudo gets its own `(sem …)` whose effect IS the specialization (rs1=x0 → no write;
     the row's fixed address), exact because the counter gating lives in csr-read's uniform
     permission model. WHERE: `scripts/check_semantics.py`'s `check_pair` now indexes
     `(pseudo …)` operand rows (checked, never demanded nor coverage-counted).
  3. **Refinements name foreign instructions by construction.** zicsr.sem.sexp's
     ecall/ebreak rules name BASE instructions, which pair mode rejected. WHERE:
     `scripts/check_semantics.py`'s `check_pair` accepts a foreign name exactly when the
     file declares it in `(refines …)` (language-only checks; the compose rule owns the
     override's honesty) — and refuses both refines lies locally too (no override behind
     it; refining yourself).
  4. **Two checker/gate gaps the new corpus exposed.** `scripts/check_semantics_corpus.sh`'s
     COMPOSE leg carried the SAME dropped-`(extensions …)`-form bug slice (a) fixed in the
     resolver (a silent override in the second form was invisible — the new self-test arm
     MISSED pre-fix, passes post-fix); and `scripts/check_citations.py` was hard-coded to
     rv64i.sem.sexp (line 178), so the new files' locators resolved against nothing — the
     `--corpus` mode binds each sem file to every profile pinning all its cited sources
     (derived, never hard-coded) and names a file no profile fully pins.
  5. **Field positions are figure-only in the spec.** mstatus.TSR/TW/TVM/MPRV and the cause
     codes had no pinned machine-readable source; upstream riscv-opcodes' checked-in
     `encoding.h` (masks) and `causes.csv` (in the cache since the rv64i era, measured
     byte-identical to upstream) joined the rv64gc ledger. WHERE: the sem rules cite them
     in comments; the permission/gating internals cite the pinned chapters.

- [x] **FIX** — data + schema + checks, no Rust:
  `schema/semantics.sexp` (+8 operators: `(field X)` raw operand-field value;
  `(inst)` instruction word; `(mode)` current privilege 0/1/3; `(csr-state a)` the
  machine's own state read, no permission model; `(csr-read a)` architectural read under
  the uniform permission model — mode bits + read-only bits (RVP-CSR §1.1.1),
  counter-enables, TM/STCE, TVM; `(csr-write a v)` architectural write, WARL legalization
  deferred to slice (c)'s tables applied at slice-(d) lowering — the seam is recorded in
  the operator's comment and the sem headers; `(trap-deliver c t)` delegation + x-stack +
  xepc/xcause/xtval + pc←xtvec; `(xret x)` the §2.1.3.2 stack pop incl. MPRV clear, x as
  the architectural mode code — `(xret m)`'s bare symbol read as an operand reference,
  measured, so x is the xPP encoding itself);
  `definitions/riscv/{zicsr,zicntr,system}.sem.sexp` (NEW — the per-instruction decisions:
  csrrw rd=x0 ⇒ no read; csrrs/csrrc rs1=x0 ⇒ no write; uimm=0 likewise for the imm forms
  (RVI-ZICSR §5.1.1); ecall cause 8/9/11 by mode, ebreak tval=pc (§2.1.3.1, both measured
  on the references); mret legal in M only, sret legal in M/S + TSR gate in S (§2.1.3.2,
  §2.1.1.6.6); wfi a NOP when legal, illegal in U, illegal in S with TW=1 — the spec's
  latitudes resolved FOR trapping, laboratory authority (§2.1.3.3, §2.1.1.6.6); sfence.vma
  illegal in U, in S with TVM=1 (§11.1.2.1, §11.1.9, §2.1.1.6.6), its invalidation effect a
  stated NOP — no translation caches modelled, Sv39 is `.3`'s);
  `scripts/check_semantics.py` (`check_pair` extracted; pseudo + refines handling; schema
  validation reaches pair mode — self-test 8→15); `scripts/check_semantics_corpus.sh`
  (COMPOSE-leg multi-form fix + the RED arm — self-test 7→8);
  `scripts/check_citations.py` (`--corpus` mode — self-test 10→13);
  `profiles/rv64gc-lab-v0/references.sexp` (+encoding.h, +causes.csv pins).
  Routed INSIDE the tree: the slice-(d) lowering of the 8 operators (gen_definition refuses
  them today by name — checked); slice (c) owns the WARL tables csr-write legalizes under.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/check_semantics.py definitions/riscv/{zicsr,zicntr,system}.sexp …sem.sexp
  6 of 6 declared instruction(s) have checked semantics          (zicsr)
  0 of 0 declared instruction(s) … (+ 3 pseudo-instruction(s))   (zicntr)
  4 of 4 declared instruction(s) have checked semantics          (system)
  $ python3 scripts/check_semantics.py --compose rv64i.sem zicsr.sem zicntr.sem system.sem
  zicsr.sem.sexp declares refinement point(s): ebreak, ecall
  the semantics compose — every override is declared.
  $ python3 scripts/check_citations.py --corpus
  rv64i.sem.sexp:   52 of 52 resolve (rv64i-lab-v0, netboard-lab-v0, rv64gc-lab-v0)
  zicsr.sem.sexp:    8 of 8 resolve (rv64gc-lab-v0, 21 pinned sources)
  zicntr.sem.sexp:   3 of 3 resolve; system.sem.sexp: 4 of 4 resolve — corpus: 6 resolution(s)
  $ bash scripts/fetch_references.sh --verify-only rv64gc-lab-v0   # +encoding.h +causes.csv
  MATCH ×8 … fetch_references: ok (rv64gc-lab-v0)     # rv64i-lab-v0 also ok
  ```

- [x] **NO REGRESSION** — RED-first, then the guard set:
  `check_semantics.py --self-test` 15/15 (7 new arms: the slice-b operators GREEN, pseudo
  operand refusal, foreign-name-without-refines, refines-without-override,
  refines-own-instruction, new-operator arity, unknown operator at the schema layer);
  `check_citations.py --self-test` 13/13 (+3 `--corpus` arms); the corpus gate's new
  dropped-form arm proven RED pre-fix (reverting the one hunk → "right verdict, wrong
  reason — no SILENT REDEFINITION"), 8/8 post-fix; rv64i.sem.sexp UNTOUCHED (its ecall/
  ebreak rules intact — the refinement lives in zicsr.sem.sexp); rv64i's generated
  surfaces byte-exact (DEF-GEN / STATE-GEN / GUEST-GEN ok); the schema fixpoint green
  (check_sexp_schema 51/51); `make gate` → `=== all doctrines green ===` (DERIVED-COUNTS
  384→385 arms re-derived). Census behind the "no book language chapter" claim:
  `grep -rln 'sem.sexp\|(effect\|set-pc' docs/book/src/` → plan/p2.md and
  annex/building-first-model.md only — a guide for new projects, not an operator-vocabulary
  reference, so no book language chapter needed updating.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice c),
  `CHANGELOG.md`, `DEV_NOTES.md` (the execution findings; promotion: declined (the
  contracts are data in the schema and armed by self-test REDs)), `LIVE_STATUS.md` (the
  re-derived arms count only), `docs/book/src/plan/p4.md` (the `.2` note extended) — the
  append-history heads sharded per `scripts/shard_history.py` where the ceilings required.

`P4-SYSTEM.2` slice (c) — split decision (recorded `2026-10-03`): **(c1)** the state schema
constructs + the staged 33-CSR document + gen_state's rv64gc branch + the gate arms —
zero Rust, everything validated from the scratch path; **(c2)** the engine-side consumption.
The seam is clean: (c1) changes no executable surface at all, and (c2) changes no schema
or document. **(c2) refined the same day, measured** (`SEMULITH-P4-0007`,
[`decision_generated-mirror-needs-tracked-input`](../decisions/decision_generated-mirror-needs-tracked-input.md)):
the generated rv64gc module CANNOT land in `crates/` before the flip — a tracked generated
artifact whose canonical input is untracked is a copy, not a derivation (a fresh clone
could not re-derive it, and STATE-GEN could not judge it there); the measured alternatives
(skip-if-absent gate leg; a hand-written interim module; a non-unit tracked descriptor
home) are each dishonest in a different way. So (c2)'s tracked landing rides the flip —
the descriptor moves, the module lands, the STATE-GEN census and FACT-OWNERSHIP rows
extend, in one green commit — and its interim evidence is the scratch proof: the emitted
module (40,198 bytes) compiles standalone and a `rustc --test` harness exercises it
behaviorally (reset per the document, the 33-CSR address lookup, the view discipline, the
field tables, x0 and the mode transitions — 4/4, the harness and module at
`target/p4-system-2/gen/`).

`P4-SYSTEM.2` slice (c1) — the state schema, the staged 33-CSR document, gen_state's second profile (`2026-10-03`, `SEMULITH-P4-0006`):

- [x] **REPRODUCE / ISSUE** — the leaf's state leg had no home and the gates had no arms
  for it, measured:

  ```
  $ grep -n "csr\|privilege" schema/state.sexp | head -3
  (no matches)                          # the state schema had no privileged construct at all
  $ ls profiles/rv64gc-lab-v0/
  contract-obligations.sexp  DOSSIER.md  profile.sexp  references.sexp  requirements.sexp
                                        # NO state.sexp — and placing one is RED by name:
  $ sed -n '224,233p' scripts/check_extraction.py   # the profile-resolution contradiction leg
  … contradictions = [encoding.sexp, state.sexp, guests] …  # the flip is the leaf's last commit
  $ git show HEAD:scripts/gen_state.py | grep -n "profile_id !=\|scoped to"
  84:    if doc["profile_id"] != PROFILE: … "a second profile is generator work"
  # the two gate gaps the brief's exploration measured:
  $ git show HEAD:scripts/check_profile_consistency.sh | grep -c "csrs"
  0            # nothing cross-checked profile.sexp's (csrs …) list against the state document
  $ git show HEAD:scripts/check_extraction.py | sed -n '127,158p' | grep -c 'csr\|privilege_mode'
  0            # _state_resets counted integer_registers + special_registers only
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect; the slice runs the brief's decision 3, and
  execution measured four things:
  1. **The staging problem is the design.** state.sexp under `profiles/rv64gc-lab-v0/` is a
     refused contradiction until the atomic flip — so the document is authored at
     `target/p4-system-2/state.sexp` and validated from there: `scripts/check_sexp_schema.py`
     takes the path explicitly, the new `scripts/check_profile_consistency.sh --csr-cross`
     runs the same csr-set rule against explicit paths, and
     `scripts/check_extraction.py`'s `_state_resets` runs on the scratch dir as a unit.
     WHERE the path-discovery was measured: `scripts/check_dossier_schema.sh` scans
     `profiles/*/*.sexp`, `scripts/check_profile_consistency.sh` reads profile.sexp +
     a sibling state.sexp, `scripts/check_extraction.py` reads the unit dir — none sees
     target/, so nothing can contradict, and the flip moves the file unchanged.
  2. **The house shape decides the nesting.** The schema kernel's form-field rule (a field
     named like its head IS the list; otherwise one nested form per value) made my first
     draft's `(fields (field …) (field …))` and the 11-child `(candidates …)` wrapper
     REFUSED by name — the construct now repeats bare `(field …)` under `(csr …)` and
     `(candidates (checked …))` per candidate, exactly the `register_family`/rv64i shapes.
  3. **One fact, stated twice, must agree — mechanically.** gen_state composes a CSR's
     reset from its per-field resets and cross-checks it against the csr-level declared
     value; the check fired NATURALLY on the document while it was being authored
     (mstatus's UXL=2|SXL=2 composite is 0xA0000000, not the hand-computed 0x300000000 —
     the descriptor was wrong, the check named it).
  4. **The mip/mie/mideleg/view "rest" rows must not overlap the named bits.** A
     full-width WPRI row beside named fields is an ambiguous legalization table — the
     coverage probe (every bit accounted, no overlap) computed the true gap sets and the
     document carries them as explicit rows.

- [x] **FIX** — schema + document + generator + gates, zero Rust:
  `schema/state.sexp` (+`privilege_mode`, +`csr` with `view_of`, +`field` with
  discipline/legalization/reset per RVP-CSR §1.1.3.1–3);
  `target/p4-system-2/state.sexp` (NEW, staged, untracked — the 33 CSRs of D-CSR-SET with
  per-field tables, the mode element, the re-earned SEM-08 census naming what each later
  slice reopens);
  `scripts/dossier_sexp.py` (the mapping owner learns both constructs, both directions,
  round-trip proven);
  `scripts/gen_state.py` (both profiles; rv64i emission byte-identical — the rv64i code
  path untouched; the rv64gc branch validates by refusal and emits storage/mode/reset/
  field-table data, to a scratch `--out` — emission into crates/ switches on in (c2));
  `scripts/check_state_gen.sh` (self-test 10→17: the rv64gc GREEN emit+sync arms and the
  RED arms — no reset, undeclared view, composed-reset disagreement, duplicate address,
  privileged constructs under rv64i);
  `scripts/check_profile_consistency.sh` (the CSR SET cross-check arm, both directions, +
  the `--csr-cross` staging probe; self-test +3 arms);
  `scripts/check_extraction.py` (`_state_resets` counts privilege_mode and every csr;
  self-test +3 arms).
  FACT-OWNERSHIP / csr-name ownership (slice (a)'s routed follow-up): the migration's
  precise remainder — the OWNER lands with the document at the flip (a fact-ownership row
  naming an untracked owner cannot register); TODAY the state document's name↔address map
  is proven against the pinned csrs.csv (33/33 exact, the probe below), csrs.csv stays the
  derivation source, and the assembler keeps reading it until the flip moves the document
  and the row registers. Deferred, recorded, nothing weakened.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/check_sexp_schema.py target/p4-system-2/state.sexp schema/state.sexp
  check_sexp_schema: ok                                        # the fixpoint stays green too (51/51)
  $ bash scripts/check_profile_consistency.sh --csr-cross profiles/rv64gc-lab-v0 target/p4-system-2/state.sexp
  csr-cross: ok (33 csr(s) agree, both directions)             # the (csrs …) list == the document
  $ python3 -c '… check_extraction._state_resets(Path("target/p4-system-2"))'
  EVERY ELEMENT HAS A RESET                                    # the reset leg over the scratch doc
  $ python3 - <<'PY'  (the address/field probes)
  csrs: 33 … csrs.csv agreement: ALL 33 EXACT … profile-only: NONE | doc-only: NONE
  field probes: ok   # no overlap, every register's bits accounted, ids unique
  $ python3 scripts/gen_state.py --check
  (rc=0 — rv64i's state.rs re-derives BYTE-IDENTICAL)
  $ python3 scripts/gen_state.py --state target/p4-system-2/state.sexp … --out target/p4-system-2/gen/state_rv64gc.rs
  gen_state: wrote … (40198 bytes)
  $ rustc --edition 2021 --crate-type lib target/p4-system-2/gen/state_rv64gc.rs   → rc=0
  # the composed-reset check earning its place (the natural RED, pre-fix of the descriptor):
  gen_state: REFUSED — mstatus: the per-field resets compose to 0xa00000000 but the
  csr-level reset declares 0x300000000 — one reset, one value
  ```

- [x] **NO REGRESSION** — RED-first, then the guard set: STATE-GEN self-test 17/17 (the 7
  new arms, every RED asserting its reason; the composed-reset RED fired naturally on the
  real document before the arm existed); PROFILE-CONSISTENCY 44/44 (+3 csr arms);
  EXTRACTION python arms 6→9 (+csr/privilege_mode reset legs) and the wrapper 11/11;
  rv64i's state.rs byte-identical under the extended generator (STATE-GEN ok);
  DOSSIER-SCHEMA / SOURCE-FORMAT / SEMANTICS (7 checks) / UNIT-COMPOSITION / DEF-GEN /
  GUEST-GEN / FACT-OWNERSHIP (61 kinds) all green; `make gate` → `=== all doctrines green
  ===` (DERIVED-COUNTS 385→395 arms re-derived).

- [x] **LOCKSTEP** — same commit: this tree (split decision + leaf status + frontier +
  checklist + verification/commit logs + changelog), `MEMORY.md` (next_action → slice c2),
  `CHANGELOG.md`, `DEV_NOTES.md` (the authoring findings; promotion: declined (the
  consistency rules are armed by self-test REDs and the natural RED is recorded)),
  `LIVE_STATUS.md` (the re-derived arms count only), `docs/book/src/plan/p4.md` (the `.2`
  note extended) — the append-history heads sharded per `scripts/shard_history.py` where
  the ceilings required.

`P4-SYSTEM.2` slice (d) — generator parameterization + the privileged machinery + the scratch execution proof (`2026-10-03`, `SEMULITH-P4-0008`):

- [x] **REPRODUCE / ISSUE** — the generators and the engine could not see the privileged
  slice-(a)/(b) artifacts, measured on the pre-slice tree:

  ```
  $ git show HEAD:scripts/gen_definition.py | grep -n 'profile != PROFILE'
  321: … "a second unit is generator work, not a config knob"      # refuses rv64gc by name
  $ git show HEAD:scripts/gen_guests.py | grep -c '"[a-z-]*",'   # the hard-coded list
  49 names (the brief said 51 — measured 49; the brief's number was stale)
  $ grep -c "Sem::" crates/semulith-core/src/exec.rs; grep -rn "trap_deliver\|csr_read" crates/ | wc -l
  the evaluator has no privileged arms; no CSR/trap-delivery machinery exists in the crate
  $ grep -n "IALIGN=32" crates/semulith-verify/src/elf.rs
  88:            "the entry address is not 4-byte aligned (IALIGN=32)",   # the routed twin
  $ grep -n "use semulith_core::definition" crates/semulith-cli/src/main.rs
  83: use semulith_core::definition::{decode, INSNS};   # the CLI's profile is STATIC — rv64i's
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the two-profile shape was decided by measuring what
  blocks each alternative; the wall is exact: the tracked evaluator matches on rv64i's
  generated `Sem` enum, which is byte-frozen (DEF-GEN) and lacks the slice-(b) variants,
  so the new operators' EVALUATION arms cannot compile tracked until the rv64gc definition
  module is tracked (the flip) — `decision_generated-mirror-needs-tracked-input` applied
  one level up. Measured: `grep -c '^(operator' schema/semantics.sexp` → 40 while
  `grep -c 'CsrRead\|TrapDeliver' crates/semulith-core/src/definition.rs` → 0 (the frozen
  module), and the three rejected shapes are recorded in DEV_NOTES.md. The shape chosen: `crates/semulith-core/src/privilege.rs` (tracked,
  hand-authored) owns the MACHINERY — the permission model, legalization, trap delivery,
  xret — over a `PrivilegedHart` trait whose metadata types it also owns; the GENERATED
  rv64gc state module (scratch until the flip) implements the trait with the descriptor's
  tables; the scratch proof compiles the tracked privilege.rs byte-identically
  (cmp-verified copies) against the scratch-generated modules. The WARL seam closed as
  designed in slice (b): the document's prose legalization became the structured
  `(legalize …)` mini-language (`(any)`/`(read-only V)`/`(one-of V…)`/`(computed)` —
  schema + document + mapping + generator), so the engine applies legalization as a
  lookup. Measured in execution, fixed at root:
  1. `scripts/gen_definition.py`'s composition name list was the THIRD copy of slice (a)'s
     dropped-`(extensions …)`-form bug — the rv64gc composition's semantics walk saw only
     zicsr, and "4 declared instruction(s) have NO semantics: mret, sfence.vma, sret, wfi"
     named it.
  2. The dossier digest rotated when `run-order.txt` became a tracked dossier source —
     the designed cascade re-derived (G0/G1/GC reports, the board's pin, the board
     artifacts, the platform manifest, both model books), and the PLATFORM-GEN stale-pin
     self-test arm assumed the digest's LEADING DIGIT (`s/"9/"0/`) — the rotation made the
     mutation a no-op; the arm now rewrites to a fixed wrong value of the same shape.
  3. The proof harness caught two authoring defects of mine: privilege.rs's write path
     preserved every bit of a CSR with NO field table (atomic registers write wholesale —
     fixed at the source), and the g3 guest delegated medeleg[8] where an S-mode ecall is
     cause 9 (the proof's RED trace named it: pc=0, the unprogrammed mtvec).

- [x] **FIX** — tracked: `crates/semulith-core/src/privilege.rs` + `privilege/tests.rs`
  (the machinery + 11 tests over a fixture hart), `crates/semulith-core/src/lib.rs`
  (the module + doc line); `crates/semulith-verify/src/elf.rs` (IALIGN is a parameter —
  the routed elf.rs:88 twin) + its tests + `crates/semulith-cli/src/main.rs`
  (`IALIGN_BITS = 32`, the rv64i profile datum, passed explicitly); `scripts/gen_state.py`
  (the `(legalize …)` consumption + the read-only/reset cross-checks + the PrivilegedHart
  impl emission); `scripts/gen_definition.py` (the rv64gc branch: both profiles, the 8
  operators lowered, pseudos emitted as PSEUDOS metadata, multi-form extensions);
  `scripts/gen_guests.py` (the guest SET is directory-derived; the run order is the
  tracked `profiles/rv64i-lab-v0/guests/run-order.txt`, cross-checked both directions —
  a guest it cannot reconcile is refused by name); `schema/state.sexp` (+the legalize
  mini-language, prose retired); `scripts/dossier_sexp.py` (the mapping, both directions);
  the three gates' self-test arms; the digest cascade's regenerated surfaces (the rv64i
  reports, netboard's board.sexp pin + artifacts + platform.sexp, both books' materials
  fragments); `scripts/check_platform_gen.sh` (the fragile arm fixed).
  Scratch (untracked, proven, flip-gated): `target/p4-system-2/gen/state_rv64gc.rs` +
  `definition_rv64gc.rs` + the proof crate `target/p4-system-2/proof/`.
  rv64i's generated modules regenerate hash-only (the embedded generator fingerprints —
  the diff shown below). The exec.rs evaluator arms for the new variants land at the flip
  (they cannot compile tracked today — measured in ROOT CAUSE); the scratch harness's
  tree-walker carries them for the proof and ports verbatim then.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core --lib privilege
  test result: ok. 11 passed; 0 failed   # the machinery: permission model, legalization,
  #   views, trap delivery (M and delegated S), xret both levels, the computed SD
  $ target/p4-system-2/proof/proof        # the scratch execution proof
  [g1 csr-rw] 6 steps …     PASS ×5  (the read/write disciplines incl. rs1=x0 never writes)
  [g2 trap-return] 11 steps PASS ×4  (mcause=11, mepc=own address, resume, still M)
  [g3 delegation] 20 steps  PASS ×4  (scause=9, the S handler, sret, back in S)
  [g4 legality] 24 steps    PASS ×4  (wfi/sret in U → cause 2, xtval=the word; wfi in M: nop)
  [g5 counter gating] 19    PASS ×3  (rdcycle gated → illegal; CY=1 → reads; back in S)
  [g6 sfence/TVM] 40 steps  PASS ×2  (TVM=0 legal nop, TVM=1 illegal)
  the scratch execution proof PASSES — the engine executes the new semantics
  $ python3 scripts/gen_definition.py --encoding target/p4-system-2/rv64gc/encoding.sexp …
  gen_definition: wrote …/definition_rv64gc.rs (60984 bytes)   # rustc --crate-type lib rc=0
  $ git diff crates/semulith-core/src/definition.rs | grep -cE '^[+-][^+-]'
  4                                  # rv64i's module: the generator-hash lines ONLY
  $ python3 scripts/gen_guests.py --encoding <trial> --guests-dir <mini-corpus> --out …
  gen_guests: wrote … (1 guests)     # the rv64gc-shaped mini-corpus parameterization
  # and its RED probes: a missing run-order.txt and a ghost entry both refused, named
  ```

- [x] **NO REGRESSION** — RED-first, then the guard set: the new gate arms (STATE-GEN
  17→20, DEF-GEN 9→15, GUEST-GEN 7→10 — every RED asserting its reason; the DEF-GEN RED
  fires the operator guard on the rv64i path); the natural REDs recorded in ROOT CAUSE;
  `make check` green (fmt + clippy -D warnings + the workspace tests: 76 core / 180 verify
  / the rest — the 11 privilege tests included); PORT-WEB green inside `make gate` (the
  wasm build compiles the new module for the browser target); `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 395→404 arms re-derived; the bench's
  RUST-02 mode agreement is untouched — no exec-path change; PORT-WEB and the elf loader
  tests re-run green).

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice e),
  `CHANGELOG.md`, `DEV_NOTES.md` (the cascade + the arm-fragility lesson; promotion:
  declined (the digest cascade is machinery with its own gates; the fragile-arm lesson
  has its repaired arm)) , `LIVE_STATUS.md` (the re-derived arms count only),
  `docs/book/src/plan/p4.md` (the `.2` note extended) — sharded where the ceilings
  required. outcome.rs's profile-scoped comments measured still TRUE (they name rv64i's
  model, which is unchanged); state.rs's census lines are rv64i's generated file —
  frozen and true of that profile; both revisit at the flip.

`P4-SYSTEM.2` slice (e) — the scope census dual-edit, the requirements growth, the staged encoding (`2026-10-03`, `SEMULITH-P4-0009`):

- [x] **REPRODUCE / ISSUE** — the profile's census was the base-only 52 while the fragments
  and sem files exist; the catalogues covered only the 18 decision mirrors; the flip's
  encoding document existed only as slice (d)'s trial (absolute fragment-root — not the
  flip's bytes). Measured:

  ```
  $ python3 -c 'import dossier_sexp as D; …scope…' profiles/rv64gc-lab-v0/profile.sexp
  count_total = 52                       # the fragments carry 62 insns + 3 pseudos
  $ python3 -c '…records…'  →  rv64gc requirements 18 / obligations 18 (decision mirrors only)
  $ python3 -c '… rv64i instruction requirements …'
  the 9 instruction records cover 49 of 52 base forms — ecall/ebreak/fence ride the
  event/memory records (REQ-D-ECALL-EBREAK, REQ-D-FENCE) — the closure is derived, not assumed
  $ grep -n "insn\b" scripts/check_exercise_coverage.sh | … the numerator
  exercised.add(text.split()[0].lower())   # the FIRST TOKEN of (step (insn "…")) — a guest
  #  writing `rdcycle x5` counts rdcycle EXERCISED even though the decode is csrrs
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in prior behaviour; the slice stages the
  flip's documents, and execution measured:
  1. **The pseudo-census decision.** The Zicntr reads ARE in the census (65 forms): the
     specification's Zicntr listings name them as instructions (RVI-ZICNTR §6.1.1), the
     profile's scope is the SPEC-FACING form set, and the encoding's pseudo relation is
     the realization's own record (`definitions/riscv/zicntr.sexp`). The integrative claim
     at the flip needs the composition's pseudo names in its encoding set — WHERE:
     `scripts/check_extraction.py`'s `_encoding_names` (insn children only, extended to
     include `(pseudo …)`), and the FOURTH copy of the dropped-`(extensions …)`-form bug
     in `_semantics_names` (line 84 — the last one: `git grep -n 'ext\[0\]\[1:\]'` over
     scripts/ now finds none).
  2. **The mirror extent is a closure, not a list.** The base corpus's requirement
     records = the base-covering records (11) + their dependency closure (+REQ-D-XLEN,
     REQ-D-ENDIAN) = 13, and their 13 obligations — measured by the probe, not typed.
  3. **The parts-sum and the fetch leg had to learn the census.** PROFILE-CONSISTENCY's
     PARTS DRIFT rule knew only base+rv64i (40+12 != 65 fired honestly);
     `scripts/fetch_references.sh`'s scope leg read only the base tables (52 vs 65) —
     extended to the ledger's pinned tables, with the rv64i M-tables exclusion kept by
     name (they are pinned for the fragment test case, not the scope) and pseudo-only
     tables contributing their pseudo names (the Zicntr listings ARE those rows).

- [x] **FIX** — `schema/profile.sexp` + `scripts/dossier_sexp.py` `_SCOPE_LISTS` (the
  mandated dual edit: +`zicsr_csrs`, +`system_privileged`, +`zicntr_counters`);
  `profiles/rv64gc-lab-v0/profile.sexp` (count_total 65, the three family lists, the scope
  comment carrying the pseudo-census decision);
  `profiles/rv64gc-lab-v0/requirements.sexp` + `contract-obligations.sexp` (the 13+13
  mirrored records with `mirrored_from` provenance + the 3+3 authored records for the new
  forms, statements verbatim per the MIRROR rule);
  `scripts/check_requirements.sh` (rule 14 MIRROR-DERIVE, registry-driven, +4 self-test
  arms); `doctrine/fact_ownership.tsv` (+2 rows, 63 kinds);
  `scripts/check_extraction.py` (pseudo names in the encoding set + the fourth
  dropped-form fix; +2 self-test arms); `scripts/check_profile_consistency.sh` (PARTS
  DRIFT learns the extension families); `scripts/fetch_references.sh` (the scope leg over
  the pinned tables, pseudo-aware).
  Scratch: `target/p4-system-2/profiles/rv64gc-lab-v0/encoding.sexp` (the flip's bytes —
  relative fragment-root, depth-3 staging + the `definitions` symlink; `(status partial)`
  + six slots), `target/p4-system-2/README.md` (the staged-payload inventory), the staged
  `profile.sexp` symlink (the assembler's IALIGN derivation reads it).

- [x] **ADDRESSED (verified)** —

  ```
  $ bash scripts/fetch_references.sh --verify-only rv64gc-lab-v0
  MATCH    encoding tables vs profile scope  65 == 65, symmetric difference NONE
  # (rv64i-lab-v0 unchanged: 52 == 52)
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (20 record file(s) validate …)   # 34 records each in rv64gc's catalogues
  $ bash scripts/check_fact_ownership.sh
  FACT-OWNERSHIP: ok (63 fact kind(s): one owner each, every mirror governed)
  $ python3 scripts/check_encoding_disjoint.py target/p4-system-2/profiles/rv64gc-lab-v0/encoding.sexp
  62 instruction(s) (+ 3 pseudo-instruction(s)) — COMPOSE; PARTIAL — 6 slot(s) unbound
  $ python3 scripts/check_sexp_schema.py <staged encoding> schema/encoding.sexp   → ok
  $ python3 scripts/check_semantics.py --compose rv64i.sem zicsr.sem zicntr.sem system.sem
  the semantics compose — every override is declared.
  # the slice-(d) proof, regenerated FROM the staged encoding and re-run: 26/26 PASS
  ```

- [x] **NO REGRESSION** — RED-first: the MIRROR-DERIVE arms (drift / missing record /
  ungoverned authored record / the owner's contract kept) and the EXTRACTION pseudo arms
  (counted / omitted-mismatch) fire with their reasons; PROFILE-CONSISTENCY's PARTS DRIFT
  fired on the real 40+12≠65 mid-edit (then learned the families); the fetch leg's
  pre-fix rv64gc run printed 52 vs 65 DIFFERS (post-fix NONE; rv64i 52==52 unchanged);
  EXERCISE-COVERAGE 21/21 (the DENOMINATOR LIE arm included); EXTRACTION 11/11 (+2);
  RECORD-SCHEMA self-test 43/43 (+4); UNIT-COMPOSITION 9/9; `make gate` →
  `=== all doctrines green ===` (DERIVED-COUNTS 404→408 arms re-derived).

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice f),
  `CHANGELOG.md`, `DEV_NOTES.md` (the closure-derived mirror + the fourth dropped-form
  copy; promotion: declined (the mirror rule is a running governor and the census decision
  is data in the profile)) , `LIVE_STATUS.md` (the re-derived arms count only),
  `docs/book/src/plan/p4.md` — sharded where the ceilings required.

`P4-SYSTEM.2` slice (f) — the guests corpus: the base mirror EXECUTED (49/49), the mode-matrix corpus (13 guests), the coverage rehearsal (65/65) (`2026-10-03`, `SEMULITH-P4-0010`):

- [x] **REPRODUCE / ISSUE** — the leaf's checkpoint (f): the rv64i guest corpus must run
  on the rv64gc engine (the base mirror) and the 13 new forms must be exercised per mode
  (the mode matrix), with EVD-05 expectations derived BEFORE any engine run. Measured
  pre-slice:

  ```
  $ ls profiles/rv64i-lab-v0/guests/*.s | wc -l
  49                        # the mirror's extent (c-scope.c is toolchain-scoped:
                            # scripts/build_c_guest.sh hard-codes -march=rv64i — the
                            # rv64gc C-guest question is the flip's, recorded)
  $ grep -c 'region\|REGION' target/p4-system-2/proof/corpus.rs   # the laboratory map:
  const REGION_BASE: u64 = 0x8000_0000;  REGION_SIZE = 0x8000_0000   # the one declared
  # MainMemory region; outside = the boundary's access fault; reserved decode = the
  # laboratory's D-RESERVED-DECODE policy conversion, DELIVERED (zicsr's refinement)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in prior tracked behaviour; the slice
  authors and executes, and execution measured four things:
  1. **Three base guests diverge BY DESIGN under D-IALIGN-16, not by soundness
     contradiction.** fault-jal-mis, fault-jalr-mis, it-prio-jump target addresses
     2 mod 4 — illegal at IALIGN=32, LEGAL with C (RVI-C 27.1): the link write lands
     and no misaligned-fetch fault fires. Their rv64gc expectations were RE-DERIVED
     from the pinned chapters (`never_written x5` dropped; it-prio-jump gained the
     delivered-fetch-fault row), never edited to match output:

     ```
     $ for f in profiles/rv64i-lab-v0/guests/*.expected.sexp; do cmp -s "$f" \
         target/p4-system-2/profiles/rv64gc-lab-v0/guests/$(basename $f) || echo "REDERIVED: $(basename $f)"; done
     REDERIVED: fault-jal-mis.expected.sexp
     REDERIVED: fault-jalr-mis.expected.sexp
     REDERIVED: it-prio-jump.expected.sexp      # the other 46 byte-identical, as are all 49 .s
     $ for f in profiles/rv64i-lab-v0/guests/*.expected.sexp; do cmp -s "$f" \
         target/p4-system-2/profiles/rv64gc-lab-v0/guests/$(basename $f) || echo REDERIVED; done | grep -c REDERIVED
     3
     ```
  2. **The scratch harness's trap-END discipline was wrong** (found by it-fault-alias):
     a delivered trap must abort the step's remaining effects — the runner's `Frame`
     gained a `trapped` flag checked at the top of `run()` and in `Set`, re-derived
     from exec.rs's Err-propagation.
  3. **Fourteen vector-address defects in the mode-matrix guests, all one root:**
     labels assemble to NO word, so auipc+addi deltas computed against a line count
     that charged labels 4 bytes were stale (mtvec/mepc/sepc targets landing in pad).
     Measured by printing every auipc+addi pair's target through the real assembler
     (`auipc@0x… -> 0x…` audit, every target now the intended instruction).
  4. **Two guest-DESIGN bugs only execution could catch:** mm-mret and mm-ecall-modes
     wrote M-level CSRs (mtvec/mstatus) inline AFTER dropping to S — illegal in S
     (RVP-CSR §2.1), so the guests trapped into an unprogrammed vector. Fix: program
     every M-level CSR BEFORE the drop, and route the second mode drop through the
     M handler (mm-ecall-modes' handler became stage-aware). Also caught: one
     hex-digit slip in the mstatus WARL constant (0x8000000A007E79AA, confirmed
     against the state document's field table) and one no-change mis-derivation
     (mm-stimecmp step 30 — x10 already held the mepc value).

- [x] **FIX** — the scratch corpus harness
  (`target/p4-system-2/proof/corpus.rs` + generated `corpus_data.rs`): the declared
  memory map, fetch/load/store fault delivery against the pinned cause vocabulary,
  the trap-END discipline, and the rv64i verify runner's comparison rule (per-step
  x-register CHANGES exact; a register written its own value is no observation — the
  discipline that re-derived several rows). The mirror staged byte-identically
  (49 `.s`, 46+3 `.expected.sexp`, `run-order.txt` + the 13 mm names). The 13
  mode-matrix guests authored at `target/p4-system-2/mm/` and mirrored:
  mm-csr-rw (the six zicsr forms' read/write/read-modify-write semantics),
  mm-csr-legality-s/-u (M-CSR access traps per mode, mtval = the word),
  mm-ebreak (delivered breakpoints resume), mm-ecall-modes (causes 11/9/8 by mode),
  mm-ecall-deleg (medeleg delegation to S, sret return, M-ecall never delegates),
  mm-mret (mode pops; MPRV cleared when xRET targets below M, preserved at M),
  mm-readonly (read-only CSR writes trap; misa WARL; mstatus all-ones WARL),
  mm-counters (mcounteren then scounteren gating), mm-stimecmp (TM then STCE),
  mm-wfi (TW gate; the laboratory's WFI-in-U policy), mm-sfence (TVM gates
  sfence.vma AND satp reads), mm-sret (legal in M/S, illegal in U, TSR gate).
  Every expectation value derived from the pinned chapters BEFORE the run; the
  runner then FALSIFIED, and every mismatch above was re-derived, never fitted.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 /tmp/authorexp.py && python3 scripts/check_sexp_schema.py \
      <each mm expectation> schema/expectations.sexp     → ok ×13
  $ cd target/p4-system-2/proof && rustc --edition 2021 -O -o corpus corpus.rs && ./corpus
  PASS mm-csr-rw 9/9 … PASS mm-sret 50/50      # per-guest steps' writes exact
  corpus: 62 guest(s) PASS, 0 FAIL             # 49 base mirror + 13 mode matrix
  # the coverage rehearsal (the gate's own numerator rule — first token of (step (insn …))
  # — over the staged profile's 65-form scope):
  denominator: 65 forms enumerated, count_total 65 CONSISTENT
  exercised & denominator: 65/65
  UNEXERCISED: none — all 65 declared forms exercised   # base 52 via the mirror,
  # the 13 extension forms via mm-* (per-guest declared-form counts recorded)
  ```

- [x] **NO REGRESSION** — nothing tracked changed this slice (`git status --porcelain`
  empty before the docs lockstep): the corpus is untracked scratch under
  `target/p4-system-2/`, so no new gate arms — the guests mirror's
  FACT-OWNERSHIP/RECORD-SCHEMA governor lands at the flip (an untracked file cannot
  be registry-owned), recorded here. The corpus is deterministic (re-run: 62 PASS, 0
  FAIL); every new check the slice DID add fired RED first in execution (the 3
  designed divergences, the trap-END bug, the 14 stale deltas, the 2 design bugs,
  the 2 mis-derivations — each named above with its falsifier). `make gate` →
  `=== all doctrines green ===` (13 checks; DERIVED-COUNTS unchanged at 408 arms —
  verified, no arm added or removed).

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice g),
  `CHANGELOG.md`, `DEV_NOTES.md` (the two execution-caught guest-design lessons;
  promotion: declined — the auipc-delta audit is now a recorded step in this leaf's
  own guest-authoring discipline and the M-level-before-drop rule is encoded in the
  guests themselves), `LIVE_STATUS.md` (unchanged — no gate arms, the leaf still
  pending), `docs/book/src/plan/p4.md` — `CHANGELOG.md`/`DEV_NOTES.md` sharded at
  their ceilings.

`P4-SYSTEM.2` slice (g) — the interactions.sexp: the 7-axis × 28-cell matrix authored and rehearsed green against the staged unit (`2026-10-03`, `SEMULITH-P4-0011`):

- [x] **REPRODUCE / ISSUE** — the leaf's checkpoint (g): the unit's interaction matrix,
  modelled on rv64i's (`profiles/rv64i-lab-v0/interactions.sexp`, 6 axes → 21 cells) and
  judged by `scripts/check_interaction_matrix.py` (COMPLETE — the N(N+1)/2 cells
  re-derived; RESOLVED — guest cells need both `guests/g.s` and `g.expected.sexp`,
  mechanisms come from the check's closed registry, degenerate needs a reason and
  nothing else; NO ORPHANS — every guest named by ≥1 cell; DIFFS — every difference id,
  including any named guest's `expect_divergence`, must exist in the unit's
  references.sexp). Measured pre-slice:

  ```
  $ grep -l expect_divergence target/p4-system-2/profiles/rv64gc-lab-v0/guests/*.expected.sexp | wc -l
  2                        # it-fencei + min-fencei carry rv64i's DIFF-FENCEI-EXECUTED —
                           # an id rv64gc's references.sexp does NOT record (measured:
  $ grep -c difference profiles/rv64gc-lab-v0/references.sexp
  0                        # …and its semantics are false here: rv64gc DECLARES Zifencei;
                           # the staged encoding leaves the slot unbound)
  $ ls target/p4-system-2/profiles/rv64gc-lab-v0/guests/*.expected.sexp | wc -l
  62                       # the matrix must absorb all 62 (49 base mirror + 13 mm)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in prior behaviour; the slice designs and
  declares, and the design measured three things:
  1. **The axis set is the leaf's own vocabulary.** rv64i's four corpus-layer axes
     (fault, alias, boundary, progress) carry over — the mirrored base guests are
     evidence of exactly those layers. The privileged machinery adds three: **legality**
     (mode-dependent permission and refusal — M/S/U, TW/TVM/TSR, read-only/WARL, plus
     encoding validity), **delegation** (interception routing — medeleg, the counter
     enables, STCE), and **restart REFRAMED**: rv64i's restart is mechanism-shaped
     (cold-reset determinism — no rv64gc mechanism exists today and the registry is
     closed), but the privileged leaf makes restart GUEST-shaped — the xret/xepc
     return discipline is observable by guests (mm-mret's MPRV rule, mm-sret's SPP,
     mm-ebreak's resume). rv64i's **event** axis is absorbed: ecall/ebreak are now the
     mode-cause and delegation story, not a separate layer. 7 axes → 28 cells.
  2. **The DIFFS rule forced the mirror's fourth and fifth re-derivations.** The two
     fencei files' `expect_divergence` pins DIFF-FENCEI-EXECUTED, whose record
     ("the matched configuration excludes Zifencei") is FALSE for this unit — rv64gc
     declares Zifencei and the staged encoding honestly declares the slot unbound.
     Per the brief's preference (no difference ids), the two staged files were
     re-derived: steps/writes/`never_written` unchanged (the observed behaviour is
     identical — reserved decode, delivered, run ended at the trap), the divergence
     form dropped with the reason recorded in each file's comment. The mirror now
     reads 49 `.s` byte-identical, 44 expectations byte-identical, 5 re-derived (3
     IALIGN-16 + 2 fencei-slot), each with provenance:

     ```
     $ for f in profiles/rv64i-lab-v0/guests/*.expected.sexp; do cmp -s "$f" \
         target/p4-system-2/profiles/rv64gc-lab-v0/guests/$(basename $f) || echo REDERIVED; done | grep -c REDERIVED
     5
     ```
  3. **Three cells are honestly REPORTED, not filled.** alias×restart, boundary×
     delegation, boundary×restart compose nothing in the staged corpus (delegation
     keys on cause/mode, never data edges; the restart cells observe control state;
     an xret to a domain-edge target is semantics this leaf has not derived). The
     doctrine's sanction — an unexercised cell is a degenerate-with-reason
     disposition, never an omission — is exactly their shape.

- [x] **FIX** — `target/p4-system-2/profiles/rv64gc-lab-v0/interactions.sexp` (the 7
  axes with grounded `covers` text, all 28 cells dispositioned, the design rationale in
  the header — route-contradicted until the flip, staged like the corpus);
  `target/p4-system-2/profiles/rv64gc-lab-v0/guests/it-fencei.expected.sexp` and
  `min-fencei.expected.sexp` (the two re-derivations, schema-valid); the corpus data
  regenerated and the runner re-proven. No new guests were needed — the staged 62 map
  onto the cells as designed (every mm guest lands on its machinery's cells; the base
  guests keep rv64i's layer mapping).

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/check_sexp_schema.py <staged interactions.sexp> schema/interactions.sexp
  check_sexp_schema: ok — … conforms to interactions.sexp
  $ python3 scripts/check_interaction_matrix.py target/p4-system-2/profiles/rv64gc-lab-v0
  …28 cell report lines…
  28 cells declared, every disposition resolves       # rc=0 — COMPLETE (28/28 derived
  # cells present), RESOLVED (every guest has both artifacts, 3 degenerate cells carry
  # reasons and nothing else), NO ORPHANS (62/62 named), DIFFS (no ids named)
  $ ./corpus        # target/p4-system-2/proof, after the fencei re-derivation
  corpus: 62 guest(s) PASS, 0 FAIL
  ```

- [x] **NO REGRESSION** — the gate's own arms fired RED against the real states this
  slice passed through, each by name: DIFFS with the pre-re-derivation fencei files
  (`NO REFERENCES …` + `UNKNOWN DIFFERENCE … 'DIFF-FENCEI-EXECUTED'`, rc=1); NO
  ORPHANS with smoke-arith dropped from its only cell (`ORPHAN GUEST … 'smoke-arith'`,
  rc=1); COMPLETE with the delegation×restart cell deleted (`OMITTED CELL …
  delegation×restart`, rc=1) — all three probed against a scratch copy of the staged
  unit, the real unit green (rc=0). `scripts/check_interaction_matrix.sh --self-test`
  15/15 and the tracked driver `INTERACTION-MATRIX: ok (5 unit(s))` — the tracked
  units untouched; nothing tracked changed this slice (`git status --porcelain`
  empty before the docs lockstep); `make gate` → `=== all doctrines green ===`
  (DERIVED-COUNTS unchanged at 408 — no arm added or removed).

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice h, the
  atomic flip), `CHANGELOG.md`, `DEV_NOTES.md` (the DIFFS-forced re-derivation +
  the guest-shaped restart reframing; promotion: declined — the axis rationale is
  data in the staged matrix header and this checklist), `LIVE_STATUS.md`
  (unchanged — no gate arms, the leaf still pending), `docs/book/src/plan/p4.md` —
  `CHANGELOG.md`/`DEV_NOTES.md` sharded at their ceilings.

`P4-SYSTEM.2` slice (h) parts 1–2 (the flip and the Sail attempt, completed
`2026-10-03`), split out on `2026-10-04` at the live file's second ceiling firing:

`P4-SYSTEM.2` slice (h) part 1 — THE ATOMIC FLIP: the staged payload lands tracked, the route flips to `generated-definition`, the tracked engine runs the corpus 62/62 (`2026-10-03`, `SEMULITH-P4-0012`):

- [x] **REPRODUCE / ISSUE** — the leaf's checkpoint (h): one atomic green commit moving
  the proven staging into `profiles/rv64gc-lab-v0/`, flipping the route, generating the
  tracked mirrors, wiring consumption, and extending the gate census — then the full
  suite. Measured pre-flip:

  ```
  $ for f in state.sexp encoding.sexp interactions.sexp guests/*; do cmp -s staging flip …; done
  payload byte-exact: state + encoding + interactions + 125 guest files
  $ python3 scripts/check_extraction.py /tmp/flip-rehearse/profiles/rv64gc-lab-v0   # a flipped-route copy
  REFUSED — zicsr.sem.sexp [ecall]: defined twice across the unit's semantics   # GATE GAP 1
  $ python3 scripts/check_interaction_matrix.py /tmp/flip-rehearse/…   → 28 cells, rc=0
  # the split decision (recorded): the flip is a complete, proven, atomic unit; the Sail
  # privileged matched-experiment attempt is genuinely uncertain scope (the 0.14 config
  # namespace for a privileged matched override) — it lands as part 2, its own commit.
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the flip's fallout was measured, not guessed; each
  item names where:
  1. **check_extraction didn't honor MODEL-COMPOSE.6's refinement relation** — its
     `_semantics_names` flagged zicsr.sem.sexp's declared `(refines (insn "ecall/
     ebreak"))` overrides as duplicates (the compose gate's own rule, not re-implemented:
     the file-level refines set now excepts declared overrides; the two refines lies
     stay the compose gate's jurisdiction). Self-test 11→13 arms.
  2. **EXERCISE-COVERAGE's SCP-02 closure leg was pseudo-blind** — the composition
     provides rdcycle/rdtime/rdinstret AS csrrs specializations (the fragment's
     `(pseudo …)` rows); the leg counted only `(insn …)` children. The seventh
     pseudo-census site, same class as slice (e)'s six. Self-test 21→23 arms.
  3. **FlatMemory hard-coded the 4-byte fetch alignment** — under IALIGN=16 the rv64gc
     corpus fetches legally at 2 mod 4. The fixture gained `with_fetch_align` (IALIGN
     as profile data); `new` keeps the 4-byte default byte-exact for rv64i.
  4. **gen_state's rv64gc emission was not rustfmt-stable** — `cargo fmt --all` runs
     over `crates/`, and STATE-GEN's `--check` compares against regeneration, so the
     generated module must be the formatter's fixed point (the csr reset array, the
     CsrMeta/FieldMeta tables, the trait impl now emit in the exploded shape).
  5. **The FACT-OWNERSHIP corpus scan found the new restatement pairs first** — the
     registry gained 11 rows (state/encodings/semantics/guest-programs/guest-
     expectations/base-guest-programs/base-guest-expectations/csr-name-address for
     rv64gc), and the same-unit census arm re-pinned 4→5 units. 63→74 fact kinds.
  6. **The supersession convention is the `(note …)` field** (D-FENCE's "Corrected
     by" precedent): D-RESOLUTION-ROUTE keeps its verbatim statement (RECORD-SCHEMA
     rule 4 mirrors it) and gains the supersession note; D-ROUTE-FLIP records the
     flip with its evidence; its REQ/OB pair follows the authored-records shape.
  7. **DERIVED-COUNTS re-derived 408→419** (+11 census arms; never hand-incremented).

- [x] **FIX** — the payload (byte-exact): `profiles/rv64gc-lab-v0/state.sexp` (33-CSR
  document), `encoding.sexp` (partial, 6 slots), `guests/` (62 + run-order.txt),
  `interactions.sexp` (7×28). The dossier: profile.sexp's route flip + stage comment,
  the two decisions, the two record pairs. The generated mirrors:
  `crates/semulith-core/src/state_rv64gc.rs`, `definition_rv64gc.rs`,
  `crates/semulith-verify/src/guests_rv64gc.rs` (content-hash-identical to the
  scratch-proven modules; provenance lines tracked-honest). The engine:
  `crates/semulith-core/src/exec_rv64gc.rs` (the evaluator with the trap-END
  discipline ridden in from the scratch runner; delivery via the tracked
  `privilege`; reserved decode reported for the policy layer),
  `crates/semulith-verify/src/run_rv64gc.rs` (+ tests: the corpus on the tracked
  path), `fixtures.rs` (fetch alignment). The CLI: `--profile=` on run/demo with
  named refusals from the rv64i-scoped commands; rv64i the byte-exact default.
  The gates: the three GEN census loops + arms, the extraction refines fix + arms,
  the coverage pseudo leg + arms, riscv_asm's CSR-name migration (the state
  document owns; csrs.csv stays the derivation source — the 33/33 probe re-run),
  the guests mirror governor (93 byte-identical + 5 recorded re-derivations),
  the registry rows.

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify run_rv64gc
  test run_rv64gc::tests::corpus_base_mirror_smoke ... ok
  test run_rv64gc::tests::corpus_mode_matrix ... ok
  test run_rv64gc::tests::every_guest_matches_its_expectations ... ok
  test run_rv64gc::tests::every_guest_re_executes_identically_from_cold_reset ... ok
  test result: ok. 4 passed; 0 failed          # 62/62 on the TRACKED engine path
  $ python3 scripts/check_extraction.py profiles/rv64gc-lab-v0
  the definition is SUFFICIENT for an engine: 65 instructions, each with encoding +
  semantics + requirement; reset everywhere; obligations checked both ways
  $ bash scripts/check_exercise_coverage.sh | tail -1   →  EXERCISE-COVERAGE: ok (… 65/65)
  $ bash scripts/check_interaction_matrix.sh | tail -1  →  INTERACTION-MATRIX: ok (5 unit(s))
  $ bash scripts/check_state_gen.sh    → ok ×2 pairs    $ bash scripts/check_definition_gen.sh → ok ×2
  $ bash scripts/check_guest_gen.sh    → ok ×2 + the base mirror holds: 93 file(s)
    byte-identical, 5 recorded re-derivation(s)
  $ bash scripts/check_fact_ownership.sh → ok (74 fact kind(s))
  $ bash scripts/fetch_references.sh --verify-only rv64gc-lab-v0
  MATCH encoding tables vs profile scope  65 == 65, symmetric difference NONE
  $ make check → 8× 'test result: ok' (76 core / 184 verify)   $ make gate → all doctrines green
  $ make bench → wasm 133662 bytes   $ make smoke-bench → ok (53 arms)   $ make book → both books
  $ semulith demo --profile=rv64gc-lab-v0 --guest=mm-csr-rw → expectations met
  $ semulith bench --profile=rv64gc-lab-v0 → the named refusal, rc=2
  ```

- [x] **NO REGRESSION** — every census arm RED-first (the hand-edit arms catch drift
  on all three GEN pairs; the extraction duplicate-without-refines arm; the coverage
  pseudo-removal arm; the mirror governor's drift and stale-record arms; the
  FACT-OWNERSHIP re-pinned census arm). rv64i byte-exactness: `state.rs`/`guests.rs`
  regenerate byte-identical; `definition.rs` differs only by the embedded generator
  fingerprint (the slice-(d) precedent); rv64i's gate verdicts quoted unchanged
  (52/52 exercised; its smoke-bench 53 arms; `semulith demo --guest=smoke-arith`
  verdict line identical); the CSR migration's RED probe (`csrrs x1, pmpaddr0, x0`
  → refused, naming the state document, though pmpaddr0 IS in csrs.csv); the CLI's
  default path byte-identical. `git grep -c IALIGN_BITS -- crates/semulith-cli` → rc=1
  (no match: the static constant is gone; the profile carries the datum).

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → the Sail
  attempt), `CHANGELOG.md`, `DEV_NOTES.md` (the four gate gaps the flip measured;
  promotion: the pseudo-census class is already owned by the family's running
  lesson and this leg joins the registry of readers — declined), `LIVE_STATUS.md`
  (the re-derived 419 arms only), `docs/book/src/plan/p4.md` — `DEV_NOTES.md`
  sharded at its ceiling.

`P4-SYSTEM.2` slice (h) part 2 — the Sail privileged matched-experiment attempt + the leaf acceptance (`2026-10-03`, `SEMULITH-P4-0013`):

- [x] **REPRODUCE / ISSUE** — the brief's decision 8: a Sail privileged matched
  experiment ATTEMPTED (Sail 0.14, the full config namespace; the rv64i matched-
  override precedent), platform matched as far as the config allows, a set of mm-*
  guests, the outcome recorded honestly. Measured at the attempt's start:

  ```
  $ target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim --version
  0.14        # git 29e6158; the config schema + default config pinned under target/refs/
  $ ls profiles/rv64i-lab-v0/reference/
  sail-rv64i-lab-v0.override.sexp        # the precedent: the TRACKED truth is the .sexp,
                                         # the JSON is derived (materialize_sail_override)
  $ python3 scripts/check_sexp_schema.py profiles/rv64gc-lab-v0/guests/mm-wfi.expected.sexp \
      schema/expectations.sexp | wc -l      # 13 mm guests with EVD-05 expectations to compare
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the attempt measured the match's boundary, cell
  by cell; three findings are the record:
  1. **Sail 0.14 cannot express "Zicntr without a CLINT"** — the validator refuses:
     "Zicntr is enabled but there is no source of time (currently only
     `platform.clint.supported`) must be enabled" — and D-PLATFORM declares NO
     devices. Even with the CLINT enabled the counter RATE is environment-defined
     (our laboratory holds the counters at zero; Sail advances them). So
     **mm-counters is NOT MATCHABLE**, named, with the validator line and the
     first-step divergence (Sail's rdcycle traps illegal, tval = the word — the
     same vocabulary, the opposite legality) as the evidence.
  2. **Sail 0.14's WFI ignores mstatus.TW in S-mode** — the TW=1-in-S legality
     cell of mm-wfi: with `wfi_is_nop=true` the wfi RETIRES as a nop (the trace
     continues at +0x48); with `wfi_is_nop=false` it waits forever ("remaining in
     WAIT-WFI state"). mstatus.TW is provably writable and read back — mm-
     readonly's all-ones WARL read-back AGREES bit-exact
     (`0x8000000A007E79AA`, bit 21 included) — and the config namespace carries
     no TW knob (`grep -c '"wfi' sail_config_schema.json` → the two wfi keys
     only). The M-nop, S-TW=0-nop and U-illegal cells AGREE (the U cell via
     `wfi_available_to_user_mode=false`, tval = the word). **mm-wfi is a PARTIAL
     match with the TW cell a NAMED DIVERGENCE** — our expectation stands on
     RVP-INSNS (TW=1 makes WFI illegal below M); the gap is Sail-side, routed to
     P4-SYSTEM.5 (the wfi/wake leaf, whose brief already owns WFI's wake
     semantics) with this measurement as the routing evidence.
  3. **The delegation-mask defaults outrun the configuration** — the validator
     rejects the stock `medeleg.delegatable_bits` twice: cause 10 is reserved
     with H off, and bit 11 (ecall from M) is undelegatable BY LAW — the very
     rule mm-ecall-deleg proves. The matched mask is 0x3FF. `mideleg`'s default
     `len` is the string `"xlen"`, which a uint64 override cannot merge over —
     dropped (the corpus never touches mideleg), the override staying honest
     about what it configures.

- [x] **FIX** — the matched override `profiles/rv64gc-lab-v0/reference/
  sail-rv64gc-lab-v0.override.sexp` (the tracked truth; the JSON derived):
  privileged ISA 1.13, misa held (our WARL), FS four-state / VS off (the field
  table), the declared selection (M/A/F/D/C, Zicsr, Zifencei, Sstc, Sv39, S, U —
  the unbound slots present-but-unused by the corpus), Zicntr OFF (finding 1),
  no devices, no PMP, WFI a nop except in U, medeleg 0x3FF, the one 2 GiB
  MainMemory region. The dossier-format owners learned the new keys:
  `schema/override.sexp` (optional fields — rv64i's override still validates)
  and `dossier_sexp`'s override mapping both directions (self-test 13→14).
  The experiment driver is scratch evidence under `target/p4-system-2/sail/`
  (the rv64gc smoke route is the verify leaf's, P4-SYSTEM.6).

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/convert_dossier.py verify <json> profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp
  round-trip ok: override — document field-for-field equal … conforms to override.sexp
  $ python3 -c 'import dossier_sexp as D; D.materialize_sail_override(repo, "rv64gc-lab-v0")'
  materialized: 7610 bytes            # the tracked artifact derives the experiment's JSON
  $ python3 target/p4-system-2/sail/compare_sail.py   # against the tracked-derived config:
  AGREE mm-csr-rw 9/9 · AGREE mm-csr-legality-s 17/17 · AGREE mm-csr-legality-u 16/16
  AGREE mm-ebreak 24/24 · AGREE mm-ecall-modes 61/61 · AGREE mm-ecall-deleg 56/56
  AGREE mm-mret 43/43 · AGREE mm-readonly 14/14 · AGREE mm-stimecmp 35/35
  DIVERGE mm-wfi step 28 (the TW cell, finding 2) · AGREE mm-sfence 43/43 · AGREE mm-sret 50/50
  experiment: 11/12 guests AGREE against the tracked override's derived JSON
  # the comparison is against the SPEC-DERIVED expectations (EVD-05), normalized to the
  # corpus's own change-observation rule — Sail's trace, the specification's values
  $ make check → 8× 'test result: ok'        $ make gate → === all doctrines green ===
  ```

- [x] **NO REGRESSION** — the attempt changed three tracked files beyond the unit:
  `schema/override.sexp` (optional fields only — rv64i's override re-validated:
  `check_sexp_schema: ok … conforms to override.sexp`), `scripts/dossier_sexp.py`
  (mapping extension; its self-test 13→14 arms, the new-keys round-trip arm
  included), and the unit's own `reference/` (new directory, the rv64i pattern).
  No gate arm weakened; the comparison never edited an expectation (the mm-wfi
  divergence is recorded, not fitted). `make gate` green; DERIVED-COUNTS 419
  unchanged (no gate census grew — the dossier self-test is not a gate arm
  census member; verified by the re-derivation).

- [x] **LOCKSTEP** — same commit: this tree (leaf status → **done** with the Result
  narrative + frontier → `.3` + checklist + logs + changelog), `MEMORY.md`
  (next_action → P4-SYSTEM.3), `LIVE_STATUS.md` (the P4 row 2/10),
  `docs/TASK_TREE.md` (the frontier names `.3`), `CHANGELOG.md`, `DEV_NOTES.md`
  (the Sail outcome; promotion: declined (the TW gap's routing is recorded in this leaf)),
  `docs/book/src/plan/p4.md` — shards at their ceilings.

`P4-SYSTEM.3` slices (a)–(c) (the Svade identity edit, the translation
machinery shell, the 10-step walk, completed `2026-10-04`), split out on
`2026-10-04` at the live file's third ceiling firing:

`P4-SYSTEM.3` slice (a) — the Svade identity edit + the Sail override flip + the validate_gc refusal (`2026-10-03`, `SEMULITH-P4-0015`):

- [x] **REPRODUCE / ISSUE** — the leaf's checkpoint (a): the profile's identity gains
  Svade (the .3 brief's OQ-2 answer — page-fault-instead-of-A/D-update), the Sail
  matched override flips to match, and gen_state's rv64gc path stops silently
  ignoring three constructs. Measured pre-slice:

  ```
  $ grep -n 'ADUE\|wpri_62_0' profiles/rv64gc-lab-v0/state.sexp | head -2
  (field (id "wpri_62_0") (bit_hi 62) (bit_lo 0) (discipline wpri) …)   # ADUE is WPRI
                                                                          # by construction
  $ grep -c 'Svade' profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp
  1                        # (extension (name "Svade") (supported false)) — the .2 config
                           # disabled it; the flip is one field, as the brief priced it
  $ sed -n 385,386p scripts/gen_state.py    # validate_gc: NO register_family /
  # memory_spaces / hardware_stack refusals (the brief's pre-condition 6 — the rv64i
  # path refuses all three at :100-112)
  $ git grep -l 'rv64imafdc' -- profiles/ docs/ scripts/ bench/ crates/ definitions/ schema/ materials/
  docs/book/src/plan/p4.md · docs/models/rv64i-lab-v0/src/references.md · docs/tasks/P4-SYSTEM.md
  docs/tasks/archive/P0-PROFILE.md · profiles/rv64gc-lab-v0/DOSSIER.md ·
  profiles/rv64gc-lab-v0/profile.sexp · profiles/rv64i-lab-v0/DOSSIER.md
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in prior behavior (the .2 experiment
  never activated translation); the slice executes the brief's identity decision and
  closes its own named hole. Three measurements shaped it:
  1. **The override must NAME the flag it depends on.** Sail's default config has
     `Svade.supported = true`, but the .2 override's template-driven generation set
     it explicitly `false` — the .2 experiment ran with hardware-update policy
     (irrelevant then: no guest activates translation). The flip to `true` is the
     D-SVADE match, and the re-run measures it, never assumes:

     ```
     $ grep -o '(extension (name "Svade") (supported [a-z]*))' \
         profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp
     (extension (name "Svade") (supported true))     # false before this slice's flip
     $ python3 -c "import json; print(json.load(open('target/refs/sail_default_config.clean.json'))['extensions']['Svade'])"
     {'supported': True}
     ```
  2. **The canonical ISA order is the DECLARED order** (gen_platform's own rule —
     the .1 fix): single-letters concatenated, then multi-letter underscore-joined,
     Z* before S* and alphabetical within — `sstc` then `svade`. The string is
     `rv64imafdc_zicntr_zicsr_zifencei_sstc_svade`, matching the brief exactly.
  3. **D-SV39's own text anticipated the follow-up** — its "not as this profile's
     rule" clause is now historical; per the dossier's convention (the D-FENCE /
     D-RESOLUTION-ROUTE precedent) it keeps its verbatim statement (RECORD-SCHEMA
     rule 4 mirrors it) and gains a `(note …)` naming D-SVADE.

- [x] **FIX** — `profiles/rv64gc-lab-v0/profile.sexp` (`(extensions "Svade")` in
  declared order, the ISA-string comment, the D-SV39 note, the D-SVADE decision with
  the brief's three evidence legs and authority laboratory);
  `requirements.sexp` + `contract-obligations.sexp` (the verbatim REQ/OB mirrors,
  the D-ROUTE-FLIP shape — contract `rv64gc-lab-env-v0` version `"0"` unchanged,
  CHK-SVADE-POS/NEG); `DOSSIER.md` (OQ-2 CLOSED with the three legs quoted, the
  ISA-string and Extensions and Translation table rows);
  `profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp` (the one-field
  flip); `scripts/gen_state.py` (validate_gc's three refusals, the rv64i path's own
  wording); `scripts/check_state_gen.sh` (three RED arms with mapping-valid injected
  shapes, so the refusal that fires is validate_gc's own); the two ISA-string
  surfaces (`docs/book/src/plan/p4.md`, the `.1` Result narrative — each amended
  with the owner named). sources.sexp: NO new pins — measured: Svade is defined
  inline in the already-pinned RVP-SUPERVISOR chapter (§11.1.3.1, §11.1.10; the pin
  at sources.sexp:55 covers both), and the U54 FU540 pin D-SV39 already cites.

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 scripts/check_sexp_schema.py profiles/rv64gc-lab-v0/profile.sexp schema/profile.sexp
  check_sexp_schema: ok — … conforms to profile.sexp
  $ bash scripts/check_requirements.sh
  RECORD-SCHEMA: ok (20 record file(s) validate and agree with their profile; …)
  $ target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim \
      --config-override target/refs/sail-rv64gc-lab-v0.override.json --validate-config
  The default configuration merged with target/refs/sail-rv64gc-lab-v0.override.json is valid.
  $ python3 <the slice-(h) compare driver>     # against the tracked-derived JSON:
  re-run after the Svade flip: 11/12 guests AGREE against the tracked override's
  derived JSON            # IDENTICAL to the pre-flip baseline — the flip changes NO
                          # guest's verdict (the mm-wfi DIVERGE is the known TW cell)
  $ bash scripts/check_state_gen.sh --self-test
  STATE-GEN --self-test: 25 pass / 0 fail     # 22→25: the three construct refusals,
                                              # each RED-named (register_family /
                                              # memory_spaces / hardware_stack)
  $ python3 scripts/gen_state.py --state profiles/rv64gc-lab-v0/state.sexp --arith … --out /tmp/sg.rs
  real descriptor still regenerates byte-identical
  $ make check → 8× 'test result: ok'   $ make gate → === all doctrines green ===
  ```

- [x] **NO REGRESSION** — the refusals fire RED on synthetic descriptors and never on
  the real one (both STATE-GEN pairs still `ok`, the modules byte-identical); the
  experiment re-run is a full verdict census, not a spot check (all 12 guests,
  baseline-versus-flip identical); the ISA-string census is quoted above with every
  governed occurrence's disposition (two authored edits with owners named, the two
  Sail-default mentions untouched, the archive untouched, gen_platform's derivation
  needs no regeneration — no board pins rv64gc today); RECORD-SCHEMA's mirror rules
  verified by its own run (rule 4 statement-identity, rule 9 restatement, the D-SV39
  note not mirrored); `make gate` green with DERIVED-COUNTS 419→422 re-derived
  (+3 STATE-GEN arms, never hand-incremented).

- [x] **LOCKSTEP** — same commit: this tree (leaf `.3` status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → `.3` slice b),
  `CHANGELOG.md`, `DEV_NOTES.md` (the override-must-name-its-flag measurement;
  promotion: declined (the matched-override discipline is already the reference
  dossier's own record, and this slice's checklist carries the measurement)),
  `LIVE_STATUS.md` (the re-derived 422 arms only), `docs/TASK_TREE.md`,
  `docs/book/src/plan/p4.md` — shards at their ceilings.

`P4-SYSTEM.3` slice (b) — the translation module + the three hooks + effective mode + the Bare-identity proof (`2026-10-04`, `SEMULITH-P4-0016`):

- [x] **REPRODUCE / ISSUE** — the leaf's checkpoint (b): translation lands as
  evaluator machinery (the brief's decisions 3–6) — a `translation.rs` beside
  `privilege.rs`, hooked at the three access sites, with satp.MODE dispatch and
  the effective-mode computation — and the corpus must not notice (Bare is an
  exact identity path). Measured pre-slice:

  ```
  $ grep -n 'Request::Fetch\|Request::Load\|Request::Store' crates/semulith-core/src/exec_rv64gc.rs | head -3
  87:    let word = match env.request(Request::Fetch { addr: pc }) {
  291:                match self.env.request(Request::Load { width, addr: a }) {
  328:                match self.env.request(Request::Store {
  # …the brief's three hook sites, physical addresses straight to the boundary
  $ grep -c 'MODE' profiles/rv64gc-lab-v0/state.sexp   # satp.MODE (one-of 0 8), reset Bare
  $ git grep -c PageFault -- crates/ | wc -l
  0                        # causes 12/13/15 exist nowhere in core yet
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in prior behavior; the slice lands
  the machinery the brief designed, and two measurements shaped it:
  1. **The parcel split must not change the Bare request shape.** Decision 5
     fetches in 16-bit parcels (the C slot's straddle is real), but the corpus
     pins one `Request::Fetch` per step (`run_rv64gc/tests.rs`'s fetch-count
     assertion family). The recorded choice: parcels translate independently,
     and the fetch COALESCES into one request whenever both translated addresses
     share one physical 32-bit unit — under Bare that is every case, so the Bare
     request shape is byte-exact by construction. The measurement:

     ```
     $ grep -n 'exactly one fetch per executed step' crates/semulith-verify/src/run_rv64gc/tests.rs
     58:        "{name}: exactly one fetch per executed step (no extraneous fetch)"
     $ grep -c 'fetch_count' crates/semulith-verify/src/run_rv64gc.rs
     1                        # the runner's fetch-request witness — the assertion's subject
     ```
  2. **The boundary variant ripples through exhaustive matches by design.**
     Adding `Request::WalkAccess` broke three match sites, each answered for its
     own profile: `fixtures.rs`'s FlatMemory (answers it — 8-byte aligned region
     read, never a fetch), bench's Counting census (a `walks` field — zero on the
     rv64i bench), and `exec/tests.rs`'s rv64i TestEnv (a named panic — the base
     profile has no translation machinery, a fixture seeing one is a test bug).

- [x] **FIX** — `crates/semulith-core/src/translation.rs` (new: `effective_mode`
  per §2.1.1.6.4 — fetch uses the current mode, data accesses use MPP when
  MPRV=1, SUM/MXR carried for the walk; `translate` — M-effective and Bare are
  exact identity, Sv39 enters `Translate::Walk` as slice (c)'s entry, an
  out-of-vocabulary satp.MODE is a named panic; the page-fault causes 12/13/15
  as raw u64 with the stated typed-enum asymmetry; `fetch_parcels`; 6 unit
  tests); `crates/semulith-core/src/env.rs` (`Request::WalkAccess { addr }` +
  `Response::WalkAccess(u64)` — the D-FETCH-IMPLICIT precedent applied,
  read-only by construction under Svade; the formal contract wording routed to
  `.9` in the variant's own doc); `crates/semulith-core/src/exec_rv64gc.rs`
  (the three hooks wired: fetch parcels with the coalescing rule, loads/stores
  translate after the model-side misalignment check — the pinned priority,
  decision 7; the walk entry reports `ModelError::Unimplemented` named, never a
  wrong answer; the module header's rules brought in line);
  `crates/semulith-verify/src/fixtures.rs` + `bench.rs` + `exec/tests.rs` (the
  three match sites above); `lib.rs` (both crates, the new module).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core translation
  test result: ok. 6 passed; 0 failed       # Bare-identity, M-never-translated,
  # sub-M walk entry, MPRV selects MPP (data only, fetch ignores), the named
  # satp.MODE defect, the 12/13/15 vocabulary
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed; 0 failed       # 62/62: per-step writes, step counts,
  # never_written, AND the fetch-count assertions — 1 fetch per step, unchanged
  $ git worktree add /tmp/pre-slice-b 4fdac5b   # the pre-change engine, both CLIs
  # driving all 62 guests through `demo`:
  wc -l /tmp/traces-pre.txt /tmp/traces-post.txt
  1884  1884
  cmp /tmp/traces-pre.txt /tmp/traces-post.txt
  BARE-IDENTITY: all 62 guest traces byte-identical (pre-change vs post-change engine)
  $ target/debug/semulith run /tmp/sv39-probe.elf --profile=rv64gc-lab-v0 --steps=20
  run: model error: Unimplemented { what: "Sv39 translation — the walk is P4-SYSTEM.3 slice (c)'s" }
  cli rc=1               # the Sv39 entry names itself — never a wrong answer
  $ make check → 8× 'test result: ok'   $ make gate → === all doctrines green ===
  $ make smoke-bench → ok (53 arms)     $ make bench → wasm builds   $ make book → both books
  ```

- [x] **NO REGRESSION** — the identity proof is byte-level and complete (1,884
  trace lines over 62 guests, `cmp` clean between the parent commit's engine and
  this one, worktree removed after); rv64i's engine is untouched (`git diff
  4fdac5b..HEAD -- crates/semulith-core/src/exec.rs` → empty; its TestEnv's new
  arm is a named panic for a case rv64i cannot produce); the fetch-count
  assertions hold (the parcels coalesce — the measurement above); smoke-bench's
  53 arms unchanged; the walk-access variant is vocabulary only (no gate arm
  changed, DERIVED-COUNTS 422 re-derived unchanged); no expectation edited, no
  check weakened.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice c),
  `CHANGELOG.md`, `DEV_NOTES.md` (the enum-addition census lesson; promotion:
  declined (the ripple is structural — the compiler names every match site, and
  the checklist records the dispositions)), `LIVE_STATUS.md` (unchanged — 422
  arms), `docs/TASK_TREE.md` (unchanged — `.3` first), `docs/book/src/plan/p4.md`
  — shards at their ceilings.

`P4-SYSTEM.3` slice (c) — the 10-step walk + the fault matrix + the REQ-D-FETCH-IMPLICIT amendment (`2026-10-04`, `SEMULITH-P4-0017`):

- [x] **REPRODUCE / ISSUE** — the leaf's checkpoint (c): the walk itself
  (§11.1.3.2 with LEVELS=3/PTESIZE=8, cited step-by-step) and the requirement
  amendment (decision 6). The boundary variant landed in slice (b); the walk
  entry was a named unimplemented case. Measured pre-slice:

  ```
  $ grep -n 'Translate::Walk' crates/semulith-core/src/translation.rs | wc -l
  1                        # the stub the slice replaces with the 10-step walk
  $ grep -o 'id "REQ-D-[A-Z-]*"' profiles/rv64gc-lab-v0/requirements.sexp | grep -c FETCH
  0                        # REQ-D-FETCH-IMPLICIT is NOT in rv64gc's catalogue —
                         # measured: the mirror's closure is 13 records and it is not
                         # among them; rv64i's owner record stays true of rv64i
  $ grep -n 'fetch_parcels\|WalkAccess' crates/semulith-core/src/exec_rv64gc.rs | wc -l
  4                        # the hooks and the variant, landed in slice (b)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in prior behavior; the slice fills
  the walk. Two execution measurements shaped it:
  1. **The reserved PTE encoding is W-without-R, and the walk caught my own
     inversion.** The first draft faulted on R=1 ∧ W=1; the fault-matrix tests
     named it instantly (three cells PageFault-for-the-wrong-reason). The pinned
     rule: W=1 requires R=1; R=0 ∧ W=1 is the reserved case. The tests were
     written before the fix and drove it (EVD-05 discipline at the test layer).
  2. **The amendment has no mirrored record to supersede — the mirror never
     carried it.** The brief's "old record superseded, never edited" read like a
     mirror edit; the measurement (the `grep -c FETCH` above) shows rv64gc's
     catalogue lacks the record entirely, so the honest shape is a NEW authored
     decision+record pair naming the translated composition's implicit-access
     vocabulary, with the owner relationship recorded in its statement.
     rv64i's REQ-D-FETCH-IMPLICIT stays true of rv64i — no translation exists
     there.

- [x] **FIX** — `crates/semulith-core/src/translation.rs` (the 10-step walk,
  cited step-by-step: §11.1.4.1's canonical-VA check before any read; per-level
  PTE reads through the slice-(b) walk-access kind with a boundary fault
  reported as the ORIGINAL access's access fault (1/5/7 by kind, step 2);
  V=0 and W-without-R (step 3); reserved/PBMT/N bits 63/62–61/60–54 zero —
  Svnapot/Svpbmt unselected (step 4); misaligned superpage (step 5); non-leaf
  D/A/U reserved (step 6, §11.1.3.1); the shadow-stack step named N/A (step 7);
  U/SUM/MXR and R/W/X by kind (step 8); Svade's page-fault-instead-of-update
  with the PTE byte-untouched (step 9); the physical address by level (step 10));
  the straddled fetch now LIVE in `exec_rv64gc.rs` (each parcel's own unit, 16
  bits from each, joined; the coalescing rule is over translated addresses, not
  pages). `profiles/rv64gc-lab-v0/profile.sexp` (D-WALK-IMPLICIT + the REQ/OB
  verbatim mirrors, CHK-WALK-IMPLICIT-POS/NEG; dependencies REQ-D-SV39,
  REQ-D-SVADE).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core translation
  test result: ok. 17 passed; 0 failed    # the fault matrix: 4 KiB / 2 MiB / 1 GiB
  # leaves with their walk-read counts (3/2/1), canonical-VA, V=0, W-without-R,
  # reserved bits 63/61/54, misaligned superpage, non-leaf D/A/U ×3 + last-level
  # pointer, U/SUM/MXR (6 cells), R/W/X (3 cells), Svade A/D (4 cells with the
  # byte-untouched proof), step-2 access fault by kind (1/5/7), the MPRV cells,
  # the satp.MODE defect, the straddle (2 fetches, 6 walk reads, the word joined)
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed; 0 failed     # 62/62 on the walk-live engine
  $ git worktree add /tmp/pre-slice-c f9a78f5   # both CLIs, all 62 guests:
  1884  1884
  cmp /tmp/traces-pre-c.txt /tmp/traces-post-c.txt
  BARE-IDENTITY (slice c): all 62 guest traces byte-identical on the walk-live engine
  $ target/debug/semulith run /tmp/sv39-probe.elf --profile=rv64gc-lab-v0 --steps=24
  x7 <- 0x000000000000000c   # mcause = 12 (instruction page fault), delivered
  x8 <- 0x0000000080000054   # mtval = the faulting VA — the slice-(b) stub probe
                             # now faults properly through the live walk
  $ make check → 8× 'test result: ok'   $ make gate → === all doctrines green ===
  $ make smoke-bench → ok (53 arms)     $ make bench → wasm builds   $ make book → both books
  ```

- [x] **NO REGRESSION** — the identity proof is byte-level on the walk-live
  engine (1,884 == 1,884 trace lines, `cmp` clean, worktree removed after);
  the walk makes no silent reads (the tests assert walk counts per scenario: 3
  for a 4 KiB leaf, 2 for 2 MiB, 1 for 1 GiB, 0 for Bare and for the canonical
  check and for every M-effective access); the Svade cells prove the region
  byte-identical across the fault (the permitted page-table side effects are
  NONE, by construction not by inspection); rv64i's catalogue and engine
  untouched (`git diff f9a78f5..HEAD -- profiles/rv64i-lab-v0 crates/semulith-core/src/exec.rs`
  → empty); no expectation edited, no check weakened; the guests that exercise
  the walk end-to-end land in slice (e), per the brief.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice d),
  `CHANGELOG.md`, `DEV_NOTES.md` (the probe-delta and slli-shift-out bugs —
  the same class as the auipc audit; promotion: declined (the pc-map discipline
  is already the family's recorded rule and this slice's checklist carries the
  instances)), `LIVE_STATUS.md` (unchanged — 422 arms), `docs/TASK_TREE.md`
  (unchanged — `.3` first), `docs/book/src/plan/p4.md` — shards at their
  ceilings.


`P4-SYSTEM.3` slice (d) — the TLB + sfence.vma's real four-case effect + the census / snapshot / determinism consequences (`2026-10-04`, `SEMULITH-P4-0018`):

- [x] **REPRODUCE / ISSUE** — the leaf's checkpoint (d): a minimal fully-specified
  TLB and the fence's real effect (the brief's decision 2), replacing the stated
  nop in `system.sem.sexp` and re-answering the SEM-08 census. Measured pre-slice:

  ```
  $ grep -c 'nop' definitions/riscv/system.sem.sexp
  2                        # the stated nop: the header bullet + sfence.vma's effect
  $ grep -o 'candidate "address-translation caches (TLBs)"' profiles/rv64gc-lab-v0/state.sexp | wc -l
  1                        # the census's own reopen hook, (present false) with ".3
                         # reopens this candidate" — the brief's own wording
  $ grep -n 'sfence.vma x0, x0' profiles/rv64gc-lab-v0/guests/mm-sfence.s | wc -l
  3                        # mm-sfence's fence cells (M legal, S/TVM=0 legal, S/TVM=1 illegal)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in prior behavior; the slice makes
  the cache real. Three design measurements, each recorded in the code:
  1. **The parameters are the minimal ones that make every rule testable.** 4
     entries, fully-associative, FIFO replacement, ASID-tagged at ASIDLEN=16,
     keyed by 4 KiB page (a superpage's other pages re-walk and install
     independently — conformant, and it keeps the fence's per-address case
     exact). Authority laboratory; the state document's census carries the same
     parameters as data, and the generator REFUSES a descriptor whose census
     does not declare the cache present (a RED arm proves it:
     `STATE-GEN --self-test: 26 pass / 0 fail`).
  2. **satp visibility is per-access reads, never invalidation.** satp is read
     at every access, so MODE and ASID changes are visible immediately (dispatch
     and tagging); a root-PPN change is visible on the next MISS, and stale
     entries may hit until a fence — §11.1.2.1's sanctioned staleness, the fence
     being the contract. SUM/MXR are read per access in `effective_mode`, never
     cached, so they always take effect immediately. The staleness tests prove
     both halves (legal stale hit before the fence, restored truth after).
  3. **A faulting access installs nothing — and a load past a D=0 leaf installs
     the D=0 entry.** The two interact exactly as the spec sanctions: the cached
     entry's D bit then faults a later store even after software sets D in the
     PTE without fencing (a LEGAL stale fault), and the fence restores the
     walk's truth. The walk's step-9 A/D check uses the entry's stored bits —
     under Svade there is no hardware update for a cache to skip, and the fault
     path must not be cached; both are tested.

- [x] **FIX** — `crates/semulith-core/src/translation.rs` (`Tlb`/`TlbEntry` with
  the stated parameters, `lookup`/`install`/`invalidate`, `fence`, the
  lookup-before-walk dispatch with `finish` shared by hit and leaf, install only
  on success); `schema/semantics.sexp` (the `tlb-invalidate` operator with its
  four-case contract); `definitions/riscv/system.sem.sexp` (sfence.vma's effect
  becomes `(tlb-invalidate (reg rs1) (reg rs2))`; the time-scoped nop bullet
  superseded with its date; the fence's legality unchanged);
  `scripts/gen_definition.py` (the extended binary map + the Sem variant);
  `crates/semulith-core/src/definition_rv64gc.rs` (re-derived, DEF-GEN green;
  rv64i's module fingerprint-only as always); `crates/semulith-core/src/privilege.rs`
  (the `tlb` trait member — hart state like mode and the CSR file);
  `profiles/rv64gc-lab-v0/state.sexp` (the census candidate re-answered
  `present true` with the full parameter statement); `scripts/gen_state.py`
  (the census-driven field emission + the refusal when the census is silent);
  `crates/semulith-core/src/state_rv64gc.rs` (re-derived, STATE-GEN green);
  `crates/semulith-core/src/exec_rv64gc.rs` (the `Sem::TlbInvalidate` arm —
  rs1 the VA, rs2's low 16 the ASID, no register written).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-core translation
  test result: ok. 25 passed; 0 failed   # the walk's 17 fault-matrix tests PLUS the
  # TLB suite: a hit skips the walk (walk count frozen), FIFO evicts in order
  # (6 installs, the oldest re-walks), ASID tags (hit/miss by ASID, G hits under
  # any), staleness legal without a fence then restored by it, Svade staleness
  # through the cache (the D=0 install → the legal stale store fault → the fence),
  # the four fence cases with their retentions, the non-canonical rs1 no-op, the
  # fence INSTRUCTION end-to-end (sfence.vma x3,x4 through the evaluator empties
  # the entry), and cold-reset determinism (two runs, outcome tuples identical)
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed; 0 failed    # 62/62 on the TLB engine
  $ git worktree add /tmp/pre-slice-d 9f65984   # both CLIs, all 62 guests:
  1884  1884
  cmp /tmp/traces-pre-d.txt /tmp/traces-post-d.txt
  BARE-IDENTITY (slice d): all 62 guest traces byte-identical on the TLB engine
  $ bash scripts/check_state_gen.sh --self-test
  STATE-GEN --self-test: 26 pass / 0 fail   # +1 RED arm: a census silent on the
                                            # translation cache is refused, named
  $ bash scripts/check_definition_gen.sh | tail -2   # both pairs ok
  $ make check → 8× 'test result: ok'   $ make gate → === all doctrines green ===
  $ make smoke-bench → ok (53 arms)     $ make bench → wasm builds   $ make book → both books
  ```

- [x] **NO REGRESSION** — the identity proof is byte-level on the TLB engine
  (1,884 == 1,884 trace lines, `cmp` clean, worktree removed after); mm-sfence's
  expectations needed NO re-derivation — measured: its two legal fence cells
  never claimed a nop (their derivations say only "legal", and a fence writes no
  register — exactly what the expectations record); the corpus's fetch counts
  and determinism assertions hold; rv64i's engine and module untouched (its
  definition.rs differs only by the embedded generator fingerprint, the standing
  precedent); `git grep -c 'present false' profiles/rv64gc-lab-v0/state.sexp` →
  the OTHER candidates unchanged (the translation cache is the only re-answered
  one); the determinism rule is TESTED, not asserted (two cold runs, tuples
  equal); snapshot measured and recorded: the rv64gc path has no snapshot
  surface today (the CLI's snapshot/resume is rv64i-scoped by refusal from the
  flip), and a cold-restored cache is always a legal state — a miss is never
  wrong; DERIVED-COUNTS re-derived 422→423 (+1 STATE-GEN census arm).

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog), `MEMORY.md` (next_action → slice e),
  `CHANGELOG.md`, `DEV_NOTES.md` (the test-vs-cache classes — the reserved-word
  encoding and the page-vs-address lookup; promotion: declined (both are the
  family's own recorded disciplines applied, and this slice's checklist carries
  the instances)), `LIVE_STATUS.md` (the re-derived 423 arms only),
  `docs/TASK_TREE.md` (unchanged — `.3` first), `docs/book/src/plan/p4.md` —
  shards at their ceilings.


`P4-SYSTEM.3` slice (e) part 1 — the sv39 guest corpus + the matrix cells + the Bare-identity proof (`2026-10-04`, `SEMULITH-P4-0019`):

- [x] **REPRODUCE / ISSUE** — the leaf's checkpoint (e): MPRV=1/SUM/MXR + the sv39
  guests + the matrix cells + the Sail matched experiment + the reports and the
  book — the leaf's LAST slice, split at execution: part 1 is the corpus (this
  commit); part 2 is the Sail matched experiment + leaf acceptance (`0020`).
  Measured pre-slice: the tracked sv39 path was proven only by the 25 translation
  unit tests — no full guest had ever executed a walk — and the corpus's
  one-fetch-per-step witness had no way to speak about a guest whose FETCH
  page-faults (such a step issues walk accesses but no `Request::Fetch`):

  ```
  $ grep -c 'sv39' profiles/rv64gc-lab-v0/guests/run-order.txt
  0                        # no sv39 guest existed
  $ grep -n 'trace.fetches as usize, g.executed_steps' crates/semulith-verify/src/run_rv64gc/tests.rs | wc -l
  1                        # the witness that would misread a fetch page fault
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in prior behavior; the slice builds
  the guest-level falsification. Five design decisions, each recorded in the
  authoring tooling (`target/p4-system-2/sv39/`):
  1. **The tables are page-aligned and the code is identity-mapped** (the walk
     reads `ppn×4096 + vpn×8`): ROOT/L1T/L0T/L1C/L0C each on its own page at
     entry+0x1000..0x5000, code through root[2]→L1C[0]→L0C[0], the translated
     test VA at 0x0040_2000 (vpn 0/2/2) landing on the staged data page.
  2. **Addresses materialize by auipc+addi chains, never plain lui** (lui
     sign-extends bit 19 of the upper half), ≤ 2047 per step, laid out by a
     fixpoint and AUDITED: `author.py::write_guest` accumulates every chain and
     refuses a target that is neither an in-range instruction nor a declared
     table/data page.
  3. **EVD-05 by a spec-side model** (`sv39gen.py::Spec`): the pinned 10-step
     walk (RVP-SUPERVISOR §11.1.3.2, LEVELS=3/PTESIZE=8 per §11.1.4.1), Svade
     (a needed A/D update is a page fault, never a write), MPRV effective mode,
     medeleg, the laboratory's region bounds (access faults 1/5/7), and the
     slice-(d) TLB semantics — re-derived in Python from the chapters, never
     read from an engine run; the corpus runner falsifies every value.
  4. **The stage-token handler discipline** — the run's own probe lesson:
     mscratch is an M-only CSR, so an S-mode `csrrw mscratch` traps illegal
     (cause 2) — the FIRST draft of two guests did exactly that and the engine
     measured right (the family rule: a wrong trace answer is a probe bug until
     proven an engine bug). Tokens that S must set travel in sscratch; the
     handler routes on a two-token scheme (1 → the drop-to-M/U section, else
     the fault-record path).
  5. **The fetch count is a declared observation** (`fetches`): a step whose
     fetch page-faults in the walk issues NO fetch request; a page-straddling
     instruction whose parcels' physical addresses are non-contiguous issues
     TWO — and the recorded coalescing rule is ADDRESS CONTIGUITY
     (`parcel_pas[1] == parcel_pas[0] + 2`, exec_rv64gc.rs), which the slice's
     first (unit-based) model got wrong and the measured 53 fetches corrected.

- [x] **FIX** — the 14-guest corpus at `profiles/rv64gc-lab-v0/guests/`:
  `sv39-translate-4k` (the happy path + the M-mode ld-back of the walked PTE,
  byte-untouched at 0x2001_80CF after two translated loads and a translated
  store — the Svade side-effect proof, x7/x8/x9 never_written), `-2m` and `-1g`
  (the superpage walks terminating at levels 1/2); `sv39-fault-canonical`
  (walk step 1), `-invalid` (V=0, step 3), `-reserved` (W-without-R, step 4),
  `-superpage` (misaligned mega + giga); `sv39-perm-rwx` (R-only store → 15,
  X-only load with MXR=0 → 13, a FETCH into the X=0 page → 12);
  `sv39-perm-usr` (U/SUM/MXR from S via sstatus, then a U-mode stage on its own
  U=1 code page — the U fetch from a U=0 page would fault, the negative shape);
  `sv39-svade` (A=0 load → 13, D=0 store → 15, D=0 load LEGAL, both PTEs
  ld-backed byte-untouched); `sv39-mprv` (MPRV=1/MPP=S translated load+store in
  M with NO code mapping present — execution continuing is the fetch-immunity
  proof; MPP=U → page fault 13; MPRV=0 → access fault 5, visibly distinct);
  `sv39-tlb-fence` (stale before the fence, ASID-selective fence retaining the
  G=1 entry, full fence restoring truth — the slice-(d) semantics as a guest);
  `sv39-straddle` (a 32-bit instruction whose parcels live on non-contiguous
  pages — two fetch requests — plus the IALIGN-16 cells that coalesce);
  `sv39-deleg` (medeleg bit 13 routes the load page fault to the S handler —
  scause/stval/sepc + sret — while the ecall still lands in M). Supporting:
  `run-order.txt` (+14), `guests_rv64gc.rs` (regenerated, 76 guests),
  `interactions.sexp` (the 14 mapped onto the SAME seven axes, no axis added),
  `schema/expectations.sexp` + `scripts/dossier_sexp.py` (the optional
  `fetches` field), `scripts/gen_guests.py` (the field + the parcel-bounds
  refusal), `crates/semulith-verify/src/run_rv64gc/tests.rs` (the witness
  compares the declared count), `crates/semulith-verify/src/guests.rs`
  (regenerated — rv64i gains the struct field only),
  `scripts/check_guest_gen.sh` (+1 RED arm).

- [x] **ADDRESSED (verified)** —

  ```
  $ for g in sv39-translate-4k sv39-translate-2m sv39-translate-1g sv39-fault-canonical \
             sv39-fault-invalid sv39-fault-reserved sv39-fault-superpage sv39-perm-rwx \
             sv39-perm-usr sv39-svade sv39-mprv sv39-tlb-fence sv39-straddle sv39-deleg; do
      semulith demo --profile=rv64gc-lab-v0 --guest=$g | tail -1; done
  guest <name> (rv64gc-lab-v0): expectations met          # ×14
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed; 0 failed     # 76/76 on the walk+TLB engine, per-step
    # writes exact, never_written, cold-reset determinism, declared fetch counts
  $ python3 scripts/check_interaction_matrix.py profiles/rv64gc-lab-v0 | tail -1
  28 cells declared, every disposition resolves
  $ bash scripts/check_guest_gen.sh --self-test
  GUEST-GEN --self-test: 16 pass / 0 fail   # +1 RED arm: a fetches count outside
                                            # the parcel bounds is refused
  $ bash scripts/check_derived_counts.sh | grep -c DRIFT; echo 0 drift after LIVE_STATUS 423->424
  $ make check → 8× 'test result: ok'   $ make gate → === all doctrines green ===
  $ make smoke-bench → ok (53 arms)   $ make bench → wasm (133715 bytes)   $ make book → both books
  ```

- [x] **NO REGRESSION** — the Bare-identity proof is byte-level on the
  corpus-extended engine: both CLIs (a scratch worktree at `e839c1b`, removed
  after) drive all 62 pre-slice guests, every demo output byte-identical. The
  62 pre-slice guests' expectations are untouched — `fetches` is OPTIONAL and
  defaults to the declared instruction count, so the witness is exactly as
  strict for them; rv64i's engine and expectations untouched (its fixture
  regenerates with the new struct field only, the standing
  generator-fingerprint precedent); DERIVED-COUNTS re-derived, never
  incremented:

  ```
  $ <the identity loop over the parent's run-order, both CLIs> | tail -1
  identity: 62 byte-identical, 0 diverge
  $ git diff e839c1b -- profiles/rv64i-lab-v0/ | wc -l
  0                        # rv64i's profile is untouched
  $ git diff e839c1b --name-only -- profiles/rv64gc-lab-v0/guests/ | grep -v sv39
  profiles/rv64gc-lab-v0/guests/run-order.txt   # the only non-sv39 change: the +14 order lines
  $ bash scripts/check_derived_counts.sh >/dev/null; echo rc=$?
  rc=0                     # 423->424 re-derived (+1 GUEST-GEN arm)
  ```

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + the
  slice-(d) checklist archived at the FOURTH per-part ceiling crossing +
  checklist + verification/commit logs + changelog), `MEMORY.md` (next_action →
  the Sail matched experiment, part 2), `CHANGELOG.md`, `DEV_NOTES.md` (the
  probe-bug classes — the M-only-CSR token and the coalescing-rule model;
  promotion: declined (both are the family's own recorded disciplines — a wrong
  trace answer is a probe bug until proven an engine bug — and this slice's
  checklist carries the instances)), `LIVE_STATUS.md` (the re-derived 424 arms
  only), `docs/TASK_TREE.md` (unchanged — `.3` first), `docs/book/src/plan/p4.md`
  — CHANGELOG/DEV_NOTES sharded at their ceilings.


`P4-SYSTEM.2`'s LEAF ACCEPTANCE record and `P4-SYSTEM.3` slice (e) part 2's checklist
(completed `2026-10-03` / `2026-10-04`), split out on `2026-10-04` at the live file's
sixth ceiling firing:

**LEAF ACCEPTANCE — `P4-SYSTEM.2` (privilege and mode transitions).** The criterion:
"the same instruction's behaviour is tested **in each supported mode**, not once."
Evidence: the mode-matrix corpus — 13 guests whose every cell is a mode crossing
(CSR access in M vs S vs U (mm-csr-legality-s/-u, mm-readonly, mm-csr-rw); ecall's
cause by mode (11/9/8) and its delegation to S with the M-ecall never delegating
(mm-ecall-modes, mm-ecall-deleg); breakpoints delivered and resumed from M and U
(mm-ebreak); mret's mode pops with MPRV cleared below M and preserved at M
(mm-mret); sret legal in M and S, illegal in U, gated by TSR (mm-sret); wfi in
M/S/U with the TW gate (mm-wfi); sfence.vma and satp under TVM (mm-sfence); the
counter enables gating S then U (mm-counters); stimecmp under TM then STCE
(mm-stimecmp)) — all falsified against EVD-05 expectations by the tracked engine
(62/62, `cargo test -p semulith-verify run_rv64gc`, 4/4 groups) and 11 of the 13
differentially AGREED against the matched Sail 0.14 (the twelfth partial, one
cell named). The leaf is **done**.

`P4-SYSTEM.3` slice (e) part 2 — the Sail matched experiment (PTW/TLB traces explicit) + the leaf's acceptance (`2026-10-04`, `SEMULITH-P4-0020`):

- [x] **REPRODUCE / ISSUE** — the privileged matched experiment for the sv39
  corpus. Pre-slice census:

  ```
  $ grep -c 'sv39' target/p4-system-2/sail/compare_sail.py
  0                        # the mm driver names no sv39 guest
  $ grep -c '0x0000_0000_0000_03FF' profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp
  1                        # the override's medeleg mask: causes 0-9 only — page faults NOT
                         # delegatable; state.sexp pins 0-10 | 12-15 | 18-20 as WARL-any
  $ target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim --help | grep -c 'trace-ptw\|trace-tlb'
  2                        # sail's PTW/TLB trace flags exist (own flags, never in --trace)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no engine defect; the slice makes the
  implicit accesses explicit and matched. Three measurements:
  1. **The image must sit at EXACTLY 0x8000_0000.** The chains compute
     absolute table addresses; lld's `--image-base` lands .text at base+0x1158
     (the mm guests never noticed — pc-relative addressing). The build
     (`build_sv39_elfs.py`) lowers the TRACKED assembler's words to a
     .word-only source and links with a PHDRS script — the tracked assembler
     owns the bytes, clang never parses the corpus's operand syntax.
  2. **Sail numbers the fetch-fault step but prints no row for it.** The
     architecture leg indexes by Sail's PRINTED step number; the expectations'
     `<fetch page fault>` pseudo-steps are then exactly the no-row, no-write
     steps — the recorded harness convention (measured on sv39-perm-rwx).
  3. **The tracked override's medeleg mask predated sv39.** `0x3FF` (causes
     0-9) made medeleg bit 13 read-only-zero on Sail, so sv39-deleg's page
     fault reached M, not S — measured as a one-register divergence (sail's
     x22=13 vs the expectation's x7=13). state.sexp pins 0-10 | 12-15 | 18-20
     WARL-any; Sail 0.14 REFUSES its reserved causes (the bisection named 10
     and 14, 17-20 rejected wholesale), so the matched mask is `0xB3FF`
     (0-9 | 12 | 13 | 15) — the widest both sides honor, the WARL latitude
     recorded (no guest delegates the rejected causes):

     ```
     $ sail_riscv_sim --config-override <0x43FF-mask>.json sv39-deleg.elf 2>&1 | tail -1
     Bits for reserved exceptions are set in `base.medeleg.delegatable_bits`.
     $ sail_riscv_sim --config-override <0xB3FF-mask>.json sv39-deleg.elf 2>&1 | tail -1; echo rc=$?
     Entry point: 0x80000000
     rc=0
     ```

- [x] **FIX** — `profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp`
  (delegatable_bits 0x3FF → 0xB3FF — the laboratory's medeleg discipline restricted
  to what Sail 0.14 accepts; the only tracked content change — the experiment
  tooling is untracked per convention: `build_sv39_elfs.py`, `compare_sail_sv39.py`,
  sv39gen's walk/TLB logs + `simulate_n`/`simulate_until`);
  `profiles/rv64gc-lab-v0/references.sexp` (matched_scope + trace_granularity, both
  stale since slice h).

- [x] **ADDRESSED (verified)** —

  ```
  $ python3 target/p4-system-2/sail/compare_sail_sv39.py
    AGREE           sv39-translate-4k      arch: 111 steps' change-observations exact
                                           ptw:  2 walks read-for-read identical
                                           tlb:  2 add(s), 0 flush(es) on both sides
    ... (all three dimensions AGREE for translate-2m/1g, the four fault guests,
         perm-rwx, perm-usr, mprv, tlb-fence (7 walks; 7 add / 2 flush), straddle,
         deleg) ...
    AGREE-RECORDED  sv39-svade             arch: 135 steps' change-observations exact
                                           ptw:  3 walks read-for-read identical; 1 walk(s)
                                                carry the A/D-placement convention
                                           tlb:  2 add(s), 0 flush(es) on both sides
  sv39 sail experiment: 13 AGREE, 1 AGREE-RECORDED, 0 DIVERGE of 14
  $ python3 target/p4-system-2/sail/compare_sail.py | grep -c AGREE
  11                       # the mm baseline reproduces (mm-wfi's named TW cell unchanged)
  $ <the 12 mm guests' arch legs under the WIDENED tracked override> | grep -c AGREE
  11                       # the mask widening is verdict-neutral (mm-wfi named as committed)
  $ cargo test -p semulith-verify run_rv64gc
  test result: ok. 4 passed; 0 failed    # 76/76 — the engine is untouched by the experiment
  $ make check → 8× ok   $ make gate → === all doctrines green ===
  ```

- [x] **NO REGRESSION** — the only tracked content change is the override's
  medeleg mask, proven verdict-neutral on the corpus that predates it (the
  ADDRESSED box's two 11/12 measurements); the engine, the 76-guest corpus and
  every gate are unchanged:

  ```
  $ git diff SEMULITH-P4-0019 -- crates/ profiles/rv64gc-lab-v0/guests/ | wc -l
  0                        # the engine and the corpus are untouched
  $ bash scripts/check_derived_counts.sh >/dev/null; echo rc=$?
  rc=0                     # 424 arms, unchanged
  ```

- [x] **LOCKSTEP** — same commit: this tree (leaf status **done** + the Result
  narrative + frontier → `.4` + checklist + logs + changelog), `docs/TASK_TREE.md`
  (the row → `.4`, 3/10), `MEMORY.md` (next_action → `P4-SYSTEM.4`),
  `LIVE_STATUS.md` (3/10), `CHANGELOG.md`, `DEV_NOTES.md` (the matched-mask
  measurement and the A/D-placement convention; promotion: declined (the
  override-mirror discipline is the rv64i dossier's recorded
  DIFF-PLATFORM-DEFAULT lesson applied)), `docs/book/src/plan/p4.md`,
  `profiles/rv64gc-lab-v0/references.sexp` (matched_scope + trace_granularity).


`P4-SYSTEM.4` slice (a)'s checklist (completed `2026-10-04`,
`SEMULITH-P4-0023`), split out on `2026-10-04` at the live file's eighth
ceiling firing (slice (b) landing):

`P4-SYSTEM.4` slice (a) — the rv_a/rv64_a re-pin + the a.sexp fragment + the
assembler's A machinery (`2026-10-04`, `SEMULITH-P4-0023`):

- [x] **REPRODUCE / ISSUE** — the brief's pre-conditions re-measured, then the pinned
  tables fetched through the tracked route and censused:

  ```
  $ grep -n 'rv_a\|rv64_a' profiles/rv64gc-lab-v0/references.sexp; echo rc=$?
  rc=1                     # the A tables pinned nowhere (the :84 policy: pin only what is derived from)
  $ ls definitions/riscv/ | wc -l; grep -c '^    ("definitions' scripts/gen_fragments.py
  9 files, no a.sexp — FRAGMENTS has 5 entries, no A
  $ grep -c '"aq"' scripts/riscv_asm.py; grep -n 'aq' target/refs/riscv-opcodes/arg_lut.csv
  0 (pre-edit)             # the whitelists had no aq/rl …
  "aqrl", 26, 25 / "aq", 26, 26 / "rl", 25, 25 / "amoop", 31, 27   # … but the pinned csv carries them
  $ python3 -c "assemble('lr.w x1, (x2)')"        # the .2/-era assembler
  AsmError: 'lr.w' is not in the canonical definition's encoding space
  # the pinned A chapter (a-st-ext.html, Version 2.1) carries NO encodings (the format
  # diagrams are images — the rv64i dossier's measured finding); rvwmo.html §17.1.3
  # Tables 6/7 enumerate exactly the 22 forms (11 .W + 11 .D)
  $ curl -sSL …/riscv-opcodes/master/extensions/{rv_a,rv64_a} | shasum -a 256; wc -c
  d9eaa988c4779ca3…  858 bytes (rv_a) / 819e0487131bc97c…  885 bytes (rv64_a)
  # census of the rows: 11 + 11 real forms, operand tokens `aq rl` (NO aqrl/amoop token —
  # the funct5 is literal fixed bits in every row), lr's rs2-must-be-zero the row's own
  # 24..20=0 fixed field; every mnemonic matches a Tables 6/7 row
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — no defect in existing behavior: the slice executes
  the brief's decision 11 as recorded, and the WHY+WHERE of the two root fixes is
  tool-backed, not read:

  ```
  $ python3 -  # the ledger's file names through BOTH collector shapes (scripts/dossier_sexp.py)
  pre-fix collector  startswith('rv_')          -> ['rv_zicsr', 'rv_zicntr', 'rv_system', 'rv_s', 'rv_a']
  fixed collector    startswith(('rv_','rv64_')) -> ['rv_zicsr', 'rv_zicntr', 'rv_system', 'rv_s', 'rv_a', 'rv64_a']
  invisible to the pre-fix census: ['rv64_a']        # WHERE: the extra collector in scripts/fetch_references.sh
  $ python3 -  # the pre-exclusion leg over the A-pinned ledger (the fix removed)
  without the A exclusion: tables 87 vs declared 65, diff: ['amoadd.d', 'amoadd.w', 'amoand.d', ...]
  ```

  1. **The scope-vs-tables leg never collected rv64_* tables** — the `extra` collector
     tested `n.startswith("rv_")`, so rv64_a (and rv64_m before it) was invisible to the
     census; latent because no profile had ever declared an A or M form while pinning the
     64-bit table (the first measurement above). Fixed to `startswith(("rv_", "rv64_"))`,
     behavior-preserving for both existing profiles (65==65 and 52==52 unchanged, below).
  2. **The A pin then breaks that leg without the declared distinction** (the second
     measurement: 87 enumerated vs 65 declared). The rv64i dossier declares the
     distinction for M ("pinned for the fragment test case, not the scope — excluded
     unless the profile declares an M form"); the A tables get the SAME named exclusion
     with the same flip condition (a declared lr./sc./amo form includes them — slice
     (e)'s bind grows the census to 87 and flips it).
  3. **The brief's "aqrl field ownership" phrasing measured imprecise**: the tables carry
     no `aqrl` operand TOKEN — every row lists `aq rl` separately (the pinned csv's
     `"aqrl",26,25` is the combined field). The fragment owns `aq` and `rl`, the fields its
     instructions actually use (the generator's own rule: a field nothing references
     invites a reader to believe it is supported).

- [x] **FIX** — at the lowest-risk level that works, no Rust touched:
  `profiles/rv64gc-lab-v0/references.sexp` (the rv_a/rv64_a re-pin: sha256+bytes, the
  supplies sentence and the re-pin comment extended; rv64i's ledger untouched);
  `scripts/fetch_references.sh` (the rv64_* collector fix + the named A exclusion);
  `scripts/gen_fragments.py` (+1 FRAGMENTS entry: tables rv_a/rv64_a, requires rv64i,
  owns aq/rl, the note recording the suffix-as-field-value design);
  `definitions/riscv/a.sexp` (NEW, generated — never hand-authored);
  `scripts/riscv_asm.py` (aq/rl whitelisted — positions always from the pinned
  arg_lut.csv at load time; the `.aq`/`.rl`/`.aqrl` mnemonic-suffix rule re-applied as
  the aq/rl FIELD VALUES, with garbage-suffix and suffix-on-non-atomic refusals by
  name; the `(rs1)` parenthesized-address spelling for the lr/sc/amo shapes, every
  other shape refused by name).

- [x] **ADDRESSED (verified)** —

  ```
  $ bash scripts/fetch_references.sh --verify-only rv64gc-lab-v0
  MATCH ×10 (the tables incl. rv_a/rv64_a + arg_lut) … MATCH encoding tables vs profile
  scope 65 == 65, symmetric difference NONE … MATCH owned fragments agree … ok
  $ bash scripts/fetch_references.sh --verify-only rv64i-lab-v0
  … MATCH 52 == 52 … MATCH matched-profile ISA string rv64i_zvl32b … ok
  $ mv target/refs/riscv-opcodes/rv_a /tmp && bash scripts/fetch_references.sh rv64gc-lab-v0
  FETCH riscv-opcodes/extensions/rv_a → MATCH — refetched bytes identical (d9eaa988…)
  $ python3 scripts/gen_fragments.py && git diff --stat -- definitions/
  regenerated 6 fragment(s) — (empty diff: the existing five re-derive BYTE-IDENTICAL)
  $ python3 scripts/check_sexp_schema.py definitions/riscv/a.sexp schema/fragment.sexp
  check_sexp_schema: ok
  $ python3 scripts/check_encoding_disjoint.py <synthetic unit doc>   # untracked, the .2 slice-a pattern
  base+A: 74 instruction(s) — COMPOSE; base+zicsr+zicntr+system+A (m slotted):
  84 instruction(s) (+ 3 pseudo-instruction(s)) — COMPOSE, PARTIAL declared
  # the assembler probe (synthetic rv64a-trial unit, untracked):
  assembled 88 words (22 forms × 4 suffix combinations)
  0x100120af lr.w x1, (x2) … 0x0874232f amoswap.w x6, x7, (x8) … 0x1e42a1af sc.d.aqrl x3, x4, (x5)
  $ target/refs/spike-build/spike-dasm < DASM-wrapped words    # the second-decoder round-trip
  lr.w ra, (sp) / sc.w.aq gp, tp, (t0) / amoadd.w.rl t1, t2, (s0) / amomaxu.d.aqrl t1, t2, (s0)
  … all 88 exact — lr's four suffix words decode to plain `lr.w` (spike's own printing
  preference, the rdcycle-prints-as-csrr precedent; the aq/rl BITS measured set in the words)
  ```

- [x] **NO REGRESSION** — the changed leg fired RED first (the 87-vs-65 measurement above),
  then the guard set: `check_encoding_disjoint.py --self-test` 12/12;
  `check_unit_composition.sh --self-test` 9/9 and the tracked run `ok (3 unit
  composition(s) decided)` — the rv64gc slot stays DECLARED, unbound, the census 65;
  `check_source_format.sh` ok (210 files, a.sexp parses); `compare_readers.py` 1/1 agree
  on a.sexp; gen_guests / gen_definition / gen_state / gen_board / gen_platform /
  gen_model_book / gen_book_index `--check` all byte-exact (no Rust surface touched);
  the assembler's manual RED probes (recorded with commands above): `lr.w.zz` →
  "ordering suffix 'zz' is not one of .aq/.rl/.aqrl"; `add.aq` / `csrrw.aq` → "an
  .aq/.rl ordering suffix belongs to an A form"; `lr.w x1, x2` / `lr.w x1, 0(x2)` /
  `sc.w x3, x4, x5` / `amoadd.w x6, x7, 8(x8)` → "the address operand is spelled
  (rs1)"; wrong arities named; `lr.w.aq.aq` / `amomaxu.q` → "not in the canonical
  definition's encoding space". No self-test arms added: the slice changes no check's
  semantics (the A fragment composes under the existing rules; the assembler's RED
  arms are the recorded probes, the .2 slice-a pattern), so DERIVED-COUNTS stays 424.
  `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — same commit: this tree (leaf status + frontier + checklist +
  verification/commit logs + changelog; the `.3` design brief archived verbatim to
  `archive/P4-SYSTEM-designs.md` at this file's seventh per-part ceiling crossing — the
  ceiling obeyed, not raised), `MEMORY.md` (next_action → slice b), `CHANGELOG.md`,
  `DEV_NOTES.md` (the execution findings; the dated lesson's promotion decision:
promotion: declined (the durability is the machinery — the collector fix and the named exclusion are armed by the fetch leg's own RED verdict, and the suffix/field design is data in the generated fragment)),
  `LIVE_STATUS.md` (unchanged — no row's state moved and the arms count stays 424),
  `docs/book/src/plan/p4.md` (the `.4` section opened) + the regenerated book index.

