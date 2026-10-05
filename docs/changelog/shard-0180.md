# CHANGELOG shard — SEMULITH-P4-0005 … SEMULITH-P4-0005

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0005 (leaf P4-SYSTEM.2, slice b) — the semantics language learns privilege: 8 operators, the zicsr/zicntr/system sem files, ECALL/EBREAK refined by declaration

- `schema/semantics.sexp` grew from 32 to 39 forms, each operator's meaning tied to the
  pinned chapters: `(field X)` (a raw operand field — the csrrs "rs1=x0 shall not write"
  discipline is a fact about the field, not the register), `(inst)` (the instruction word,
  for illegal-instruction xtval), `(mode)` (current privilege 0/1/3), `(csr-state a)` (the
  machine's own state read — no permission model, no recursion through the gates),
  `(csr-read a)` / `(csr-write a v)` (the architectural CSR access under a UNIFORM
  permission model: address mode bits and read-only bits per RVP-CSR §1.1.1, counter-enable
  gates, TM/STCE on stimecmp, TVM on satp — every CSR instruction gets it once),
  `(trap-deliver c t)` (delegation selection, the xPIE/xIE/xPP stack, xepc/xcause/xtval,
  pc←xtvec), and `(xret x)` (the §2.1.3.2 privilege-stack pop incl. the MPRV clear). The
  language's READS-AND-WRITES contract is now stated: register reads see the
  pre-instruction register file (the csrrw swap is exact even for rd==rs1); no RV64I rule
  changes meaning.
- Three authored sem files, every rule locator-cited and resolution-checked: `zicsr.sem`
  (the read/write side-effect disciplines, RVI-ZICSR §5.1.1; ECALL/EBREAK refined by
  declaration — MODEL-COMPOSE.6's anticipated case — cause 8/9/11 by mode, ebreak tval=pc,
  both measured on the references), `zicntr.sem` (the pseudo-semantics mechanism, measured:
  a pseudo specializes csrrs by NAME — no refines possible or needed — exact because the
  counter gating lives in csr-read), `system.sem` (mret M-only, sret M/S + the TSR gate;
  wfi a stated NOP-when-legal, illegal in U and in S with TW=1, the spec's latitudes
  resolved for trapping under laboratory authority; sfence.vma's invalidation a stated NOP
  — no translation caches exist yet, Sv39 is `.3`'s). The WARL seam is recorded: csr-write
  legalizes under slice (c)'s per-field tables, applied at slice-(d) lowering.
- Measured in execution, fixed at root: the semantics corpus gate's COMPOSE leg carried
  slice (a)'s dropped-`(extensions …)`-form bug (a silent override in the second form was
  invisible — the new self-test arm proven RED pre-fix); `check_citations.py` was
  hard-coded to rv64i.sem.sexp, so the new files' locators resolved against nothing — the
  `--corpus` mode binds each sem file to every profile pinning all its cited sources
  (52/52 ×3 profiles, 8/8, 3/3, 4/4 resolved); the mstatus field positions are figure-only
  in the pinned spec, so `encoding.h` (masks) and `causes.csv` (trap causes) joined the
  rv64gc encoding-source pin.
- Validation: check_semantics self-test 15/15 (+7 arms), check_citations 13/13 (+3),
  corpus gate 8/8 (+1); rv64i.sem.sexp untouched and rv64i's generated surfaces byte-exact
  (DEF-GEN/STATE-GEN/GUEST-GEN); both profiles' fetch verify green; `make gate` green
  (DERIVED-COUNTS 384→385 arms).

