# CHANGELOG shard — SEMULITH-P4-0039 … SEMULITH-P4-0036

> Sharded from `CHANGELOG.md` under its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0039 (leaf P4-SYSTEM.7, slice a) — the backend qualification: rustc_apfloat QUALIFIED by measurement

- The candidate landscape re-measured against the fetched artifacts (the census's
  web claims were leads): `rustc_apfloat 0.2.3+llvm-462a31f5a5ab` (updated
  2025-06-11, ~6.3M downloads; Apache-2.0 WITH LLVM-exception, LICENSE-DETAILS.md
  recording the port's provenance; forbid(unsafe_code), no_std, pure-value API)
  and `softfloat 1.0.0` (koute, 2023-11-03; MIT OR Apache-2.0; musl-libc lineage
  via const_soft_float — EVD-04-clean). The negatives re-confirmed from the
  metadata: softfloat-sys/softfloat-wrapper are Berkeley C FFI; softfloat-pure
  does not resolve. One census claim measured UNVERIFIABLE (softfloat's
  "TestFloat-verified upstream" — the crate's own documents carry no such
  statement; recorded, not counted).
- The capability measurement (the extracted sources): softfloat has NO rounding
  modes, NO exception flags, NO FMA, NO 64-bit int conversions, NO min/max — five
  of ARCH §6's explicit requirements; rustc_apfloat carries the whole surface
  EXCEPT sqrt (never ported) and two measured LLVM-vs-IEEE flag deviations
  (opOverflow only for ±inf results; no NV on sNaN format conversions). The
  **correctness tables** (63,752 cases vs MPFR, directed + seeded streams, per op
  × 5 modes × f32/f64): the arithmetic core (add/sub/mul/div/fma values, all
  modes, both widths) has **ZERO disagreements**; the 612 value disagreements are
  all model-layer policy surfaces (NaN→int 340, fmin/fmax signed-zero +
  both-NaN canonical 240, NaN payloads on format conversion 32) and the 386 flag
  disagreements are the two named deviations. softfloat vs MPFR on its 4,416-case
  shared set: 68, ALL the NaN-sign family (its arithmetic core is MPFR-exact
  where it exists, INCLUDING sqrt — the bar fp.rs's own sqrt must match).
- The MPFR path, recorded: no CLI/gmpy2/mpmath on this host — the system Homebrew
  libmpfr 4.2.2 driven by a scratch C generator with MPFR's own semantics
  measured and corrected spec-side (the DON'T-USE MPFR_RNDNA, the
  exponent-range-shaped OF/UF flags, the NaN canonicalization, the NAN-flag-is-
  not-NV mapping). Timing on this host: apfloat f64 add 10.1 / mul 10.5 / div
  40.7 ns/op (fma 15.7, conversions 3.5-5.4); softfloat ~3-5× cheaper where it
  exists. Both candidates build clean for wasm32-unknown-unknown (PORT-WEB).
- **The decision record** (`docs/decisions/decision_fp-backend-qualification.md`
  + INDEX; the candidate-landscape lesson PROMOTED to
  `docs/knowledge/a-candidate-landscape-census-entry-is-a-lead.md`): the FP
  backend is rustc_apfloat, pinned `=0.2.3+llvm-462a31f5a5ab`; the model layer
  (fp.rs, slice b) owns the RISC-V target policy AND the named deviations;
  softfloat disqualified on capability; the fallback stays named. The dependency
  lands in semulith-core (Cargo.lock 4 → 7 packages: rustc_apfloat + bitflags +
  smallvec; the cargo home stays on-volume), the lib.rs re-export as the
  compile-use. `make check` rc=0, `make gate` green (DERIVED-COUNTS 430
  unchanged), make bench wasm 133,715 bytes + smoke-bench 53 arms + both books.
  Next: slice (b) — the FP state (the f-file + FS gating + the fcsr fix +
  fflags/frm semantics + the census re-answer) with the FS=Off corpus.

## SEMULITH-P4-0037 (leaf P4-SYSTEM.6, slice c) — the matched experiment 6 AGREE of 6; the LEAF CLOSES

- The Sail matched experiment for the fence.i surface — decision 2's designed
  AGREE measured, not assumed. The override is measured first (materialized
  fresh from the tracked unit, unmoved since bfa6aaa; validate-config rc=0;
  Zifencei supported true; NO change needed); sail's FENCEI measured in source:
  its encdec carries the fields as VARIABLES (decoded-not-fixed — the
  shall-ignore sentence quoted in its own comment), and its execute is a nop
  for the memory model. Against the matched configuration, **6 AGREE of 6**:
  it-fencei 3, min-fencei 1, fencei-reserved 2, fencei-selfmod 8,
  fault-selfmod 7, dir-selfmod-fence 8 — 29 steps' change-observations exact,
  the patched fetch reading the new value on both engines; ZERO non-AGREE
  cells. Verdict-neutrality measured: the wider corpus's expectations are
  unmoved since their verdicts (the bind touched only the fencei surface).
- The fetch-cache census candidate is re-answered in place (decision 6):
  Zifencei declared AND bound; the re-read choice stays laboratory policy;
  FENCE.I's nop is the unit's sanctioned implementation of the synchronization
  (the consequence line unchanged; gen_state re-derived, build rc=0). One brief
  phrasing measured imprecise and recorded: pre-condition 2's 'without
  Zifencei' clause lives in rv64i's verbatim text, referenced by the candidate,
  not in the candidate itself. references.sexp records the fifth experiment
  (difference-free re-measured: 0 difference records).
- **The LEAF ACCEPTANCE closes**: rewrite-code fixtures with and without the
  architectural synchronization, measured on BOTH engines — WITH:
  fencei-selfmod's fence.i retires between the store and the fetch, the patched
  word reading 7 on both; WITHOUT: fault-selfmod's patch visible with no
  synchronization, D-CODE-VISIBILITY named (the laboratory's declared legal
  subset). The staleness half is answered as the declared latitude: intro.html's
  implicit-reads sentence lets a valid implementation cache every fetchable
  byte forever, and modelling such a hart would contradict the unit's
  always-coherent census (rejected at the brief). `make check` rc=0, `make
  gate` green (DERIVED-COUNTS 430 unchanged), RECORD-SCHEMA 20,
  PROFILE-CONSISTENCY 5, smoke-bench 53 arms, bench wasm, both books. Frontier
  → `.7` (floating-point backend qualification — the design brief first,
  starting from the routed-in SoftFloat shared-ancestry measurement).

## SEMULITH-P4-0036 (leaf P4-SYSTEM.6, slice b) — THE BIND: the unit composes riscv/zifencei

- The slot becomes the extension and fence.i is legal in the tracked engine.
  encoding.sexp's `(slot (id zifencei) …)` becomes `(extensions "riscv/zifencei")`
  (four slots stay, partial stays, the header's census restated); the census dual
  edit 87→88 lands in all four places (schema/profile.sexp +
  dossier_sexp._SCOPE_LISTS + the scope block + PROFILE-CONSISTENCY's PARTS key —
  the one-form zifencei_fencei family, RVI-ZIFENCEI §4.1);
  `definition_rv64gc.rs` regenerates with fence.i over the existing `Sem::Nop`
  (mask 0x0000707f — the shall-ignore decode, the manifest cascade);
  REQ-GC-FENCEI + OB-GC-FENCEI with no new D-* decision (the nop is the sem
  file's stated decision — the wfi-nop precedent; RECORD-SCHEMA both files ok).
- The fencei guests re-derive to the legal fence.i — the `.2` slice-(g)
  pre-commit FULFILLED: it-fencei grows 2→3 steps with the continuation marker
  committing (x2 ← 7, exactly as on both references); min-fencei is one retiring
  nop — and its demo trace stays byte-identical anyway (the pre-bind delivery
  wrote nothing observable at mtvec=0, measured). `fencei-reserved` exercises
  the shall-ignore decode end-to-end (0x0011118F ignored); `fencei-selfmod` is
  the acceptance pair's WITH member (the store, the legal fence.i, the patched
  fetch reading 7 through the new memory-backed derivation); fault-selfmod
  stands WITHOUT. The decision-3 comment corrections land as RECORDED mirror
  re-derivations — the governor measured my direct .s edits as drift: the mirror
  holds .s byte-identical to rv64i's owners ALWAYS, so the bound-state story
  lives in the expectation comment blocks (dir-selfmod-fence's data fence is
  not the fetch synchronization; fault-selfmod's stale qualifier corrected).
- The fetch leg's exclusion flipped on its own (88==88, rv64i 52==52); the
  corpus reads **101/101**; the identity proof holds 98/99 (it-fencei the
  designed exception, worktree removed); the matrix resolves 28 cells;
  EXERCISE-COVERAGE 88/88; EXTRACTION ok; GUEST-GEN 16/16; UNIT-COMPOSITION 3;
  SHARD-FREEZE 186 rows. `make check` rc=0, `make gate` green (DERIVED-COUNTS
  430 unchanged).
