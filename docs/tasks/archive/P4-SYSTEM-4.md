# P4-SYSTEM — archived completed-leaf evidence (part 4)

Completed acceptance checklists archived verbatim from [`../P4-SYSTEM.md`](../P4-SYSTEM.md)
under its per-part ceiling (part 3 at its own). Opened `2026-10-06` at the `.11` design.

<!-- archived verbatim from docs/tasks/P4-SYSTEM.md at the 2026-10-06 `.11` design crossing: `.8` slices (a)–(e) -->

`P4-SYSTEM.8` slice (a) — the CSR rd-before-trap defect fixed at root; two stale texts and a wrong unreachable cause (`2026-10-06`, `SEMULITH-P4-0058`):

- [x] **REPRODUCE / ISSUE** — the brief's pre-condition 3, as a RED guest before any fix:

  ```
  probe csrrw x5, cycle, x6 (M, x5 = 7) on the HEAD engine → [5] x5 <- 0x5, then cause 2
  $ cargo test -p semulith-verify run_rv64gc (mm-csr-ro-write added, the old engine) →
    FAILED: "mm-csr-ro-write: step 9 writes match the specification-derived expectations"
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — the zicsr rules committed rd before judging the write:
  `git show HEAD:definitions/riscv/zicsr.sem.sexp | grep -c "(seq (set (reg rd) (csr-read
  (field csr)))"` → 6 rules of that shape — `Set` writes rd as soon as its value evaluates,
  and `csr-write`'s permission check (`privilege.rs`) ran second. No guest caught it because
  the authoring tool REFUSED read-only writes ("fix the guest") and knew no immediate forms.

- [x] **FIX** — `schema/semantics.sexp`: `(csr-rw a v)` — the atomic read-write (CSRRW
  "atomically swaps"): read and write judged first, v written, the OLD value yielded, a
  refusal delivered before any effect; `gen_definition.py` lowers it (`Sem::CsrRw`, the
  extended surface); `exec_rv64gc.rs`: the `CsrRw` arm; `zicsr.sem.sexp`: every writing form
  with a destination is `(set (reg rd) (csr-rw …))`. Riding along: LR's unreachable
  boundary-Misaligned arm 7 → 5 (an LR is a load); `a-lrsc-fault`'s ".s" and expectation
  prose ("cause 7 every visit" — the LR's is 5) corrected and RE-DERIVED (every value
  identical; the current tool also fixed a text the `.4` tool had keyed by instruction text);
  the authoring tool taught read-only writes, the immediate forms, `mhartid`, and a
  family-aware header (it stamped the FP header on every file). Two guests:
  `mm-csr-ro-write` (mhartid — implemented on both engines) and `mm-csr-ro-counters`
  (cycle/time/instret).

- [x] **ADDRESSED (verified)** —

  ```
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 4 passed (127 guests)
  $ identity_8a.py <fixed CLI> <HEAD CLI> → identity: 125 byte-identical, 0 diverge;
    RED mm-csr-ro-write and mm-csr-ro-counters — both diverge on the parent engine
  $ compare_sail.py (matched config) → AGREE mm-csr-ro-write 51 steps; AGREE a-lrsc-fault
    41 (its re-derived expectations); DIVERGE mm-csr-ro-counters at step 45, the LEGAL read
    of cycle — "verdict: 2 AGREE of 3", rc=1: the matched override runs Zicntr OFF (the
    recorded CLINT wall), so cycle/time/instret do not exist on sail; a Zicntr+CLINT variant
    fails validate-config ("The CLINT … is not in a defined memory region") — the named
    not-matchable cell, as mm-counters before it
  the derivation tool before/after over the corpus: 76 of 76 jointly derivable files
    byte-identical; the newly derivable mm-csr-ro-write/mm-csr-rw match their tracked
    writes; F/D re-derived 22/22 identical with the family-aware header
  ```

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`;
  the brief's pre-condition 3 corrected in place (its sail half was the Zicntr-absent trap).

- [x] **LOCKSTEP** — this tree (the brief's correction note, checklist, logs, changelog,
  frontier), `DEV_NOTES.md` (sharded first; PROMOTED — the oracle card's mirror case),
  `CHANGELOG.md`, `MEMORY.md` (next_action → b), the book (the new P4.8 chapter, SUMMARY,
  the P4 index), `schema/semantics.sexp`.

`P4-SYSTEM.8` slice (b) — the fault-priority table declared; its missing pairs pinned on both engines (`2026-10-06`, `SEMULITH-P4-0059`):

- [x] **REPRODUCE / ISSUE** — the priority TOPIC was handed to `.8` four times (the archived
  `.2`/`.3`/`.4` briefs) and never declared; the census of what was pinned:

  ```
  $ git show HEAD:profiles/rv64gc-lab-v0/profile.sexp | grep -c "D-FAULT-PRIORITY" → 0
  pinned already: fault-fetch (fetch fault over decode), it-prio-load (misaligned over the
    out-of-region access fault, bare), f-fs-off/d-fs-off (illegal over the access fault),
    a-amo-sv39 (an AMO's misaligned over translation)
  unpinned: a plain load/store's misaligned over a PAGE fault; illegal over misaligned and
    over a page fault; translation succeeding then the physical access refused (grep of the
    sv39 expectations for "access fault" → nothing)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the engine already orders every pair as
  the table and `.3` decision 7 require (both engines agree below); what was missing was the
  DECLARATION and the pins. The table, measured where it lives: priv/machine.html §2.1.1.15,
  "Synchronous exception priority in decreasing priority order" — its one
  implementation-defined position is load/store/AMO misaligned (high or low).

- [x] **FIX** — `profile.sexp`: `D-FAULT-PRIORITY` (the table, the laboratory's HIGH choice,
  the unreachable rows named — instruction-misaligned under IALIGN 16, breakpoints without
  Sdtrig — and the guest pinning each adjacent pair) + REQ-D-FAULT-PRIORITY + OB-FAULT-PRIORITY
  (identical statements, the MIRROR rule); `prio-sv39`: sv39-fault-invalid's page-table
  prologue verbatim up to its last table store (its auipc chains are pc-relative), one leaf
  added by absolute address (VA 0x0040_3000 → PA 0x1000_0000, outside the region), eight
  S-mode cells; the matrix's placements; the authoring tool's header learns `prio-`.

- [x] **ADDRESSED (verified)** —

  ```
  prio-sv39 derived spec-side (128 steps) — the cells' causes: misaligned+unmapped ld 4,
    sd 6; aligned+unmapped 13 (the control); misaligned+mapped-outside 4; aligned
    mapped-outside ld 5, sd 7; FS=Off flw on the unmapped VA 2; FS=Off misaligned fld 2
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 4 passed (128 guests)
  $ compare_sail.py (matched config) → AGREE prio-sv39 128 steps; "verdict: 1 AGREE of 1", rc=0
  $ bash scripts/check_requirements.sh → RECORD-SCHEMA: ok (20 record file(s) …)
  $ python3 scripts/check_interaction_matrix.py profiles/rv64gc-lab-v0 → 28 cells, every
    disposition resolves
  ```

- [x] **NO REGRESSION** — no engine change (the guest pins existing behaviour; it passes on
  the parent engine by design — a characterization, not a RED); `make check` rc=0; `make
  gate` → `=== all doctrines green ===`. Observed on the way: `check_sexp_schema` judges each
  top-level form against the declared constructs and so accepted a decision placed AFTER the
  profile's closing form; the dossier loader (RECORD-SCHEMA, PROFILE-CONSISTENCY) refused it
  ("expected exactly one document form … found 2") — the one-root rule is the loader's, by
  design (record files hold many forms), and it held.

- [x] **LOCKSTEP** — this tree, `profile.sexp` + the two record files, `CHANGELOG.md`,
  `MEMORY.md` (next_action → c), the book (P4.8 chapter).
  `promotion: declined (the priority table is the decision record itself; no new lesson).`

`P4-SYSTEM.8` slice (c) — the typed fault-injection carrier (`2026-10-06`, `SEMULITH-P4-0060`):

- [x] **REPRODUCE / ISSUE** — the acceptance needs "a fault injected after the Nth
  suboperation", and no rv64gc mechanism could inject one:

  ```
  $ git show HEAD:schema/expectations.sexp | grep -c refuse → 0
  $ git show HEAD:crates/semulith-verify/src/run_rv64gc.rs | grep -c Refusing → 0
  the corpus environment (FlatMemory) refuses only by region and alignment; an AMO's two
    halves share address and width, so no split was reachable (the brief's pre-condition 4)
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the brief's decision 4 builds it. The
  boundary already carries the shape — four request kinds (`git show HEAD:crates/semulith-core/src/env.rs | grep -cE '^    (Fetch|Load|Store|WalkAccess) \{'` → 4; an AMO issues a Load then a Store) and one access-fault answer the
  engine maps to the architectural cause by kind — so injection is a refusal at the boundary,
  never a hook inside an instruction.

- [x] **FIX** — `schema/expectations.sexp`: `(refuse (kind fetch|load|store|walk) (base …)
  (size …))`, the experiment's refusal regions; `dossier_sexp.py`: their round trip;
  `gen_guests.py`: `RefusalKind`/`Refusal` and a per-guest refusal table in both generated
  modules (empty for every guest that injects nothing — `guests.rs` regenerated too);
  `run_rv64gc.rs`: `Refusing`, under the fetch counter (a refused fetch is still counted),
  answering every request whose kind matches and whose bytes intersect a region with an
  access fault; the authoring tool: `#|refuse:` honoured with the engine's own per-half causes
  (a refused LR/plain load 5, store/SC 7, either half of an AMO 7, a walk read the original
  access's access fault) — and its walk now answers an out-of-region PTE read with that access
  fault where it read zeros (a page fault) before; fetch refusals refused by name (it has no
  fetch translation model). `inj-carrier`: the carrier's end-to-end proof.

- [x] **ADDRESSED (verified)** —

  ```
  inj-carrier derived: the refused store 7 (A unchanged, read back 0); the refused load 5
    and the word inside its bytes 5 (sentinels untouched); the unrefused C round-trips 0x55;
    the AMO on A — its load completes, its store is refused — cause 7, x11 untouched, A 0
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 4 passed (129 guests)
    RED — the runner's refusals emptied: FAILED, "inj-carrier: step 12 writes match the
    specification-derived expectations"; restored → ok
  $ cargo test -p semulith-verify the_refusal_predicate → test result: ok. 1 passed (inside,
    straddling both edges, adjacent both sides, another kind, a PTE read)
  $ check_sexp_schema (an unknown kind, a scratch copy) → REFUSED … "poke" is not one of
    ['fetch', 'load', 'store', 'walk'], rc=1
  the tool before/after over the corpus: 80 of 80 jointly derivable files byte-identical
  ```

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`; every
  pre-existing guest's expectations byte-identical; the matrix 28 cells.

- [x] **LOCKSTEP** — this tree, `CHANGELOG.md`, `MEMORY.md` (next_action → d), the book (P4.8
  chapter). `promotion: declined (the carrier's design is the schema comment and the brief's decision 4).`

`P4-SYSTEM.8` slice (d) — the injected-fault corpus; rv64gc's partial-progress obligation; the state candidate re-answered (`2026-10-06`, `SEMULITH-P4-0061`):

- [x] **REPRODUCE / ISSUE** — rv64gc declared no partial-progress obligation and its state
  candidate waited on `.8`:

  ```
  $ git show HEAD:profiles/rv64gc-lab-v0/contract-obligations.sexp | grep -c PARTIAL-PROGRESS → 0
  state.sexp's "pending or partially committed effects": "… P4-SYSTEM.8's, which reopens
    this candidate"; the carrier (c) had one proof guest and no corpus
  ```

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the leaf's acceptance ("a fault injected
  after the Nth suboperation leaves the architecturally required state") needs the injected
  cells and the declared discipline; the census of which suboperations exist is the brief's
  pre-condition 2 (`git show HEAD:crates/semulith-core/src/env.rs | grep -cE '^    (Fetch|Load|Store|WalkAccess) \{'` → 4 boundary request kinds).

- [x] **FIX** — five guests over the carrier: `inj-atomics` (an LR whose load is refused —
  cause 5, no reservation, so the next SC fails rd←1; an SC whose store is refused — 7, rd
  and memory untouched; an AMO's store refused after its load, and an AMO's load refused so
  its store never issues — 7 both, rd untouched), `inj-fp` (FLD/FLW refused — 5, the f-register
  unwritten and FS NOT dirtied; FSD/FSW refused — 7, memory unchanged), `inj-walk-l2/l1/l0`
  (a walk read refused at each Sv39 level — the ORIGINAL access's access fault 5/7/7, never a
  page fault); `OB-GC-PARTIAL-PROGRESS` + its mirror `REQ-GC-PARTIAL-PROGRESS` (the unit
  discipline, the standing reads declared, the fixtures named); `state.sexp`'s candidate
  re-answered (`state_rv64gc.rs` regenerated); the matrix's placements. Two authoring defects
  re-derived, never fitted: the walk guests' prologue sliced one line early (its own `csrrw
  mtvec` doubled, every pc-relative table address off by 4 — the derivation showed the table
  stores faulting with 6); read-backs into registers already 0 (no observable change —
  sentinels added). Out of scope, named: a FETCH-refusal guest — the carrier honours fetch
  refusals, but the authoring model has no fetch translation model; fetch faults stay covered
  by fault-fetch (region) and sv39-straddle (translation).

- [x] **ADDRESSED (verified)** —

  ```
  derived: inj-atomics lr.d 5, sc.d (no reservation) x6 <- 1, M still 0, sc.d 7, amoadd.w 7,
    A still 0, amoor.d 7; inj-fp fld 5, mstatus FS Clean (0x4080), fsd 7, A still 0, flw 5,
    fsw 7, FS still Clean; inj-walk-l2/l1/l0 ld 5, sd 7, amoadd.d 7
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 5 passed (134 guests)
    RED — a refused walk read mutated into a page fault (translation.rs): FAILED, "inj-walk-l2:
    step 64 writes match…" — the first failing guest, so the 129 before it were blind to it;
    restored → ok
  $ bash scripts/check_requirements.sh → RECORD-SCHEMA: ok (20 record file(s) …)
  gen_state → state_rv64gc.rs: the candidate's why only (2 lines); definition_rv64gc.rs
    re-fingerprints the state document (DEF-GEN named the drift); the matrix 28 cells
  ```

- [x] **NO REGRESSION** — no engine change; every pre-existing guest unchanged; `make check`
  rc=0; `make gate` → `=== all doctrines green ===`.

- [x] **LOCKSTEP** — this tree, the two record files and `state.sexp` (+ its module),
  `CHANGELOG.md`, `MEMORY.md` (next_action → e), the book (P4.8 chapter).
  `promotion: declined (per-slice corpus; the discipline is the obligation record itself).`

`P4-SYSTEM.8` slice (e) — the sail attempt, the reports, the book and THE LEAF ACCEPTANCE; the leaf CLOSES (`2026-10-06`, `SEMULITH-P4-0062`):

- [x] **REPRODUCE / ISSUE** — the leaf's acceptance reads "a fault injected after the Nth
  suboperation leaves the architecturally required state"; the second engine's view of the
  `.8` corpus was unmeasured for the injected guests.

- [x] **ROOT CAUSE (WHY + WHERE)** — not a defect: the closing step. What sail can say was
  measured, not assumed: its configuration has no refusal regions
  (`grep -c refuse target/refs/sail-rv64gc-lab-v0.override.json` → 0), so an injected guest's
  refused access PROCEEDS there — those cells are not matchable by construction.

- [x] **FIX** — the experiment over all ten `.8` guests (`target/p4-system-8/sail/`); the
  ledger's seventh experiment (`references.sexp`); the leaf's status **done** and Result;
  the frontier → `.9` (the environment contract v1 — the design brief first);
  `docs/TASK_TREE.md`, MEMORY, LIVE_STATUS; the book's P4.8 chapter closed.

- [x] **ADDRESSED (verified)** —

  ```
  $ compare_sail.py (matched config, ten guests) → AGREE mm-csr-ro-write 51, a-lrsc-fault 41,
    prio-sv39 128; DIVERGE mm-csr-ro-counters at its legal cycle read (Zicntr off — named);
    DIVERGE inj-carrier step 12, inj-atomics 14, inj-fp 21, inj-walk-l2/l1/l0 64 — each at its
    FIRST refused access (sail lets it proceed; the walks reach L0T[3]'s V=0 and page-fault 13)
    — "verdict: 3 AGREE of 10"
  $ cargo test -p semulith-verify run_rv64gc → test result: ok. 5 passed (134 guests)
  ```

- [x] **THE LEAF ACCEPTANCE** — "a fault injected after the Nth suboperation leaves the
  architecturally required state": the typed carrier (c) refuses a chosen suboperation's
  access, and on every multi-suboperation instruction the profile has, the state is the
  required one — an AMO's store refused after its completed load (inj-carrier, inj-atomics:
  rd and memory untouched), an LR's load (no reservation registered), an SC's store, the FP
  transfers (no f-register write, FS not dirtied), a translation walk refused at each of its
  three levels (the original access's access fault) — each derived spec-side and satisfied by
  the engine (134/134), with the mutation that maps a refused walk read to a page fault caught.
  The goal's other parts: fault priority declared (D-FAULT-PRIORITY) and pinned on both engines
  (prio-sv39 AGREE); suppressed effects (the CSR rd-before-trap defect fixed at root, sail
  AGREE); restart locations (every cell resumes at xepc + 4 through its handler — the
  continuation proofs); partial commits under the new system features declared impossible and
  checked (OB-GC-PARTIAL-PROGRESS), the standing reads declared (SEM-06).

- [x] **NO REGRESSION** — `make check` rc=0; `make gate` → `=== all doctrines green ===`;
  records only.

- [x] **LOCKSTEP** — `references.sexp`, this tree (status, result, frontier, checklist, logs,
  changelog), `docs/TASK_TREE.md`, `MEMORY.md` (P4 8/10; next_action → the `.9` design brief),
  `LIVE_STATUS.md`, `CHANGELOG.md`, the book.
  `promotion: declined (the leaf's lessons were promoted at their slices — the oracle card's mirror case).`
