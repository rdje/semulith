# CHANGELOG shard — SEMULITH-P4-0018 … SEMULITH-P4-0017

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0018 (leaf P4-SYSTEM.3, slice d) — the TLB, sfence.vma's real four cases, the census/snapshot/determinism consequences

- The minimal fully-specified TLB: **4 entries, fully-associative, FIFO replacement,
  ASID-tagged at ASIDLEN=16, keyed by 4 KiB page** — the minimal parameters that make
  every rule testable (a superpage's other pages re-walk and install independently —
  conformant, and it keeps the fence's per-address case exact). Authority laboratory;
  the same parameters live as data in the state document's SEM-08 census (the
  `address-translation caches (TLBs)` candidate re-answered `present true` — the
  census's own ".3 reopens this candidate" hook), and gen_state emits the storage as
  hart state from that declaration — refusing, RED-armed, a descriptor whose census
  is silent on the cache (STATE-GEN 25→26 arms).
- The visibility record: satp is read per access, so MODE and ASID changes take
  effect immediately (dispatch and tagging); a root-PPN change is visible on the
  next miss, and stale entries may hit until a fence — §11.1.2.1's sanctioned
  staleness, the fence being the contract (the cache never auto-invalidates).
  SUM/MXR are read per access, never cached, always immediate. The install
  discipline: a faulting access installs nothing; a load past a D=0 leaf installs
  the D=0 entry — the cached entry's D bit then faults a later store after software
  sets D without fencing (a LEGAL stale fault), and the fence restores the walk's
  truth. The walk's step-9 A/D check uses the entry's stored bits — under Svade
  there is no hardware update for a cache to skip, and the fault path must not be
  cached.
- sfence.vma's effect lands through the full pipeline: the `tlb-invalidate` operator
  (schema/semantics.sexp, the four-case contract) → `system.sem.sexp`'s effect
  `(tlb-invalidate (reg rs1) (reg rs2))` — the time-scoped nop superseded with its
  date, the legality untouched — → gen_definition's extended map + the
  `Sem::TlbInvalidate` variant (DEF-GEN both pairs green, rv64i fingerprint-only) →
  the evaluator arm (rs1 the VA, rs2's low 16 the ASID, no register written). The
  over-fence latitude is recorded-not-taken, so the G-bit retention and the
  per-ASID cases are genuinely tested.
- The TLB suite (25/25 with the walk's 17): a hit skips the walk (count frozen);
  FIFO evicts in order (6 installs, the oldest re-walks); ASID tags with G hitting
  under any ASID; staleness legal without a fence then restored by it; Svade
  staleness through the cache (the D=0 install → the legal stale store fault → the
  fence); all four fence cases with their retentions (per-ASID and per-address+ASID
  keep globals; per-address evicts them; all-spaces empties everything); the
  non-canonical rs1 no-op; the fence INSTRUCTION end-to-end (sfence.vma x3,x4
  through the evaluator empties the entry); and cold-reset determinism — two runs,
  outcome tuples identical (the cache is a pure function of the hart's own history).
  Snapshot measured and recorded: no rv64gc snapshot surface today (the CLI's
  snapshot/resume is rv64i-scoped by refusal), and a cold-restored cache is always
  a legal state — a miss is never wrong.
- mm-sfence's expectations needed NO re-derivation — measured: its legal fence
  cells never claimed a nop, and a fence writes no register, exactly what they
  record. The Bare identity is byte-exact on the TLB engine: both CLIs over all
  62 guests, 1,884 == 1,884 trace lines, `cmp` clean (worktree removed after).
  `make check` 8/8, `make gate` all green (DERIVED-COUNTS 422→423), smoke-bench
  53 arms, bench wasm, both books.
  Next: slice (e) — MPRV/SUM/MXR + the sv39 guests + matrix cells + the Sail
  matched experiment + the reports and the book.

## SEMULITH-P4-0017 (leaf P4-SYSTEM.3, slice c) — the 10-step Sv39 walk, the fault matrix, the REQ-D-FETCH-IMPLICIT amendment

- The walk is live in `crates/semulith-core/src/translation.rs`, cited step-by-step
  (§11.1.3.2 with LEVELS=3/PTESIZE=8 per §11.1.4.1): the canonical-VA check
  (bits 63:39 == bit 38) before any read; per-level PTE reads through slice (b)'s
  walk-access boundary kind, a boundary fault reported as the ORIGINAL access's
  access fault (1/5/7 by kind, step 2); V=0 and the W-without-R reserved encoding
  (step 3 — the first draft's R∧W inversion caught by the fault-matrix tests
  written before the fix); reserved/PBMT/N bits 63/62–61/60–54 zero with
  Svnapot/Svpbmt named unselected (step 4); misaligned superpage (step 5);
  non-leaf D/A/U reserved per §11.1.3.1 (step 6); the shadow-stack step named
  N/A (step 7); U/SUM/MXR and R/W/X by access kind (step 8); Svade's
  page-fault-instead-of-update with the PTE byte-untouched (step 9 — the
  permitted page-table side effects are NONE, by construction not by inspection);
  the physical address by level (step 10).
- The fault-matrix suite: 17 translation tests covering all three leaf sizes with
  their walk-read counts (3 for 4 KiB, 2 for 2 MiB, 1 for 1 GiB), the canonical-VA
  fault, V=0, reserved-RW, the reserved bits ×3, misaligned superpage, non-leaf
  D/A/U ×3 + the last-level pointer, the U/SUM/MXR cells (S-page from S, U-page
  from S with and without SUM, S-fetch of a U-page unconditionally, U-page from
  U, MXR on/off), the R/W/X cells, the Svade A/D cells with the region
  byte-identical across the fault, the step-2 access fault by kind, the MPRV
  selection (data walks like S, fetch ignores MPRV, M never walks), and the
  satp.MODE named defect. The straddled fetch is live end-to-end: two parcels on
  non-adjacent physical pages, each fetched from its own unit and joined —
  2 fetch requests, 6 walk reads, the word exact (the coalescing rule is over
  translated addresses, not pages: adjacent physical pages correctly coalesce).
- The requirement amendment was measured first: rv64gc's catalogue NEVER carried
  REQ-D-FETCH-IMPLICIT (the mirror's closure is 13 records and it is not among
  them — `grep -c FETCH` → 0), so the amendment lands as a NEW authored pair:
  D-WALK-IMPLICIT in the profile and the verbatim REQ/OB mirrors
  (CHK-WALK-IMPLICIT-POS/NEG, dependencies REQ-D-SV39 + REQ-D-SVADE), naming the
  translated composition's implicit-access vocabulary (the fetch + up to LEVELS
  implicit 8-byte walk reads per access; no implicit writes under Svade).
  rv64i's owner record stays true of rv64i — no translation exists there;
  RECORD-SCHEMA green by its own run.
- The Bare identity is byte-exact on the walk-live engine: both CLIs (the parent
  commit's and this one) over all 62 guests — 1,884 == 1,884 trace lines, `cmp`
  clean (worktree removed after) — beside the standing cargo assertions (62/62,
  fetch counts unchanged). The slice-(b) stub probe now faults properly: an
  S-mode fetch under Sv39 with an empty root table page-faults (V=0) with
  mcause 12 and mtval = the faulting VA; the walk-access boundary fault path is
  measured separately (satp.PPN outside the region → access fault by kind with
  tval = the original VA). `make check` 8/8 groups, `make gate` all green,
  smoke-bench 53 arms, bench wasm, both books. The guests exercising the walk
  end-to-end land in slice (e), per the brief.
  Next: slice (d) — the TLB + sfence.vma's real four-case effect + the census /
  snapshot / determinism consequences.

