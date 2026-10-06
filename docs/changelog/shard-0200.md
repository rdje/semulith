# DEV_NOTES shard — _(2026-10-04)_ … _(2026-10-04)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-04)_ — the matched experiment that caught its own config (P4-SYSTEM.3 slice e part 2; the leaf closes)

Execution of the `.3` brief's checkpoint (e), part 2, measured:

- **The experiment's first DIVERGE was the override's, not the models'.**
  sv39-deleg came back `sail x22=13 vs expected x7=13` — the delegated page
  fault reached M on Sail. The engine delegates bit 13 (the corpus is green),
  Sail delegates it when allowed — the tracked override's `delegatable_bits`
  0x3FF (causes 0-9, authored at `.2` before page faults existed in the
  corpus) was the stale fact. The laboratory's state.sexp pins 0-10 | 12-15 |
  18-20 WARL-any; Sail 0.14 REFUSES a mask covering its reserved causes, so
  the matched value is the bisection's 0xB3FF (0-9 | 12 | 13 | 15) — the
  widest both sides honor, proven verdict-neutral on the mm corpus before the
  sv39 run went green. The override mirrors the laboratory only up to the
  reference's own validation; the latitude is recorded, never hidden (the
  override-mirror discipline is the rv64i dossier's DIFF-PLATFORM-DEFAULT
  lesson applied — the census before the config, the measurement before the
  claim; promotion: declined).
- **A/D placement is a vocabulary difference, not a behavior one.** sv39-svade
  was the lone non-AGREE: the model's walk faults at step 9 (A=0 → page fault,
  never an update), Sail's `--trace-ptw` prints `Success` and takes the fault
  a step later. Same reads, same delivered trap — where the check is JUDGED
  differs. Recorded as the A/D-placement convention, never normalized away:
  the trace comparison keys on the read sequence, and the architecture leg
  proves the outcomes identical.
- **Sail prints no row for a fetch that page-faults — but numbers it.** The
  step counter jumps across the faulting fetch; indexing the comparison by the
  PRINTED number (never list position) makes the expectations' `<fetch page
  fault>` pseudo-steps exactly the no-row, no-write steps. And the TLB
  dimensions needed no normalization at all: sv39-tlb-fence's 7 adds and 2
  flushes match the laboratory's 4-entry FIFO event-for-event — a stronger
  match than the brief priced (TLB-size/timing differences were budgeted as
  recorded differences; on THIS corpus, Sail's defaults and the laboratory's
  minimal cache produce identical event counts).

## _(2026-10-04)_ — the corpus that made the walk real, and three probe bugs it paid for (P4-SYSTEM.3 slice e part 1)

Execution of the `.3` brief's checkpoint (e), part 1 (the corpus), measured:

- **A guest is a different falsifier than a unit test.** The walk, TLB, MPRV
  and Svade had 25 unit tests; the first full guest (`sv39-translate-4k`, 111
  steps — build five page-table pages in M, csrw satp, drop to S, translate a
  load/store/load, ecall home, then read the walked PTE back in M) passed only
  after the pc-map audit trusted `pc_of` over the printed line index (a label
  occupies an index but no bytes — the print lied, the map was right) and after
  the stage token moved OUT of the S-mode cells: `csrrw mscratch` in S is an
  illegal-instruction trap (cause 2), which the engine delivered correctly.
  The family rule paid again: an unexpected-but-correct trace is a probe bug
  until proven an engine bug. Tokens S must set now travel in sscratch, and
  the handler routes on a two-token scheme.
- **The fetch-count witness had to learn the architecture.** The corpus's
  no-extraneous-fetch assertion was `fetches == steps`. Two real guests break
  it honestly: a step whose FETCH page-faults in the walk issues walk accesses
  but never a `Request::Fetch` (0 for that step), and the straddled
  instruction on non-contiguous pages issues 2. The expectations schema grew
  the optional `fetches` field — the count is a DECLARED observation with a
  parcel-bounds refusal in the generator (RED-armed), never a computed
  allowance — and the 62 pre-slice guests keep the old strictness by default.
  My first model of the coalescing rule (one physical 32-bit unit) was wrong;
  the engine's recorded rule is address contiguity (`pa[1] == pa[0] + 2`), and
  the measured 53 fetches corrected the probe, not the engine.
- **EVD-05 by a spec-side model.** `target/p4-system-2/sv39/sv39gen.py`'s
  `Spec` re-derives the pinned 10-step walk (§11.1.3.2, LEVELS=3/PTESIZE=8 per
  §11.1.4.1), Svade (a needed A/D update is a page fault, never a write), MPRV
  effective mode, medeleg, the region bounds, and the slice-(d) TLB semantics
  in Python — every expectation value comes from the chapters, and the corpus
  runner falsifies all of them. The auipc+addi chain discipline (lui
  sign-extends bit 19; ≤ 2047 per step; fixpoint layout; the audit accumulates
  chains and knows the table targets) is what kept 14 guests' pc maps honest
  (the classes above are the family's recorded probe-bug and pc-map
  disciplines applied, and this slice's checklist carries the instances —
  promotion: declined).

